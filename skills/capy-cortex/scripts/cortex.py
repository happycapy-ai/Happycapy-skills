#!/usr/bin/env python3
"""Capy Cortex - Core engine. Two-stage retrieval: FTS5 pre-filter -> TF-IDF re-rank."""

import sqlite3
import json
import sys
import os
import pickle
import math
from pathlib import Path
from datetime import datetime, timedelta

DB_PATH = Path(__file__).parent.parent / "cortex.db"
TFIDF_DIR = Path(__file__).parent.parent / "tfidf"

# Confidence decay: 90-day half-life, 4x harmful multiplier
DECAY_HALF_LIFE_DAYS = 90
HARMFUL_MULTIPLIER = 4


def get_db():
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA busy_timeout=5000")
    return db


def decay_factor(last_seen_str):
    """Compute confidence decay factor based on time since last seen."""
    if not last_seen_str:
        return 1.0
    try:
        last = datetime.fromisoformat(last_seen_str)
        days = (datetime.utcnow() - last).days
        return 0.5 ** (days / DECAY_HALF_LIFE_DAYS)
    except Exception:
        return 1.0


# --------------- RETRIEVAL ---------------

def retrieve_fts(db, query, limit=50):
    """Stage 1: FTS5 broad retrieval (O(log n), fast)."""
    try:
        safe_query = " OR ".join(
            w for w in query.split() if len(w) > 2 and w.isalnum()
        )
        if not safe_query:
            safe_query = query.split()[0] if query.split() else "help"
        rows = db.execute("""
            SELECT r.*, rank AS fts_rank
            FROM rules_fts JOIN rules r ON rules_fts.rowid = r.id
            WHERE rules_fts MATCH ? AND r.maturity != 'deprecated'
            AND r.is_latest != 0
            ORDER BY rank LIMIT ?
        """, (safe_query, limit)).fetchall()
        return rows
    except Exception:
        return []


def retrieve_fallback(db, limit=30):
    """Fallback: highest confidence rules when FTS5 returns too few."""
    return db.execute("""
        SELECT * FROM rules WHERE maturity != 'deprecated'
        AND is_latest != 0
        ORDER BY confidence * occurrences DESC LIMIT ?
    """, (limit,)).fetchall()


def retrieve_tfidf_rerank(candidates, query, top_k=15, workspace=None):
    """Stage 2: TF-IDF re-rank using sklearn (semantic similarity).
    Now with workspace-aware scoring and helpful_count boost."""
    vec_path = TFIDF_DIR / "vectorizer.pkl"
    if not vec_path.exists() or len(candidates) <= top_k:
        return _apply_workspace_boost(candidates[:top_k], workspace)
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        vectorizer = pickle.load(open(vec_path, "rb"))
        query_vec = vectorizer.transform([query])
        texts = [c["content"] for c in candidates]
        cand_vecs = vectorizer.transform(texts)
        sims = cosine_similarity(query_vec, cand_vecs)[0]
        scored = []
        for i, c in enumerate(candidates):
            df = decay_factor(c["last_seen"])
            freq = min(c["occurrences"] / 10.0, 1.0)
            helpful = min((c["helpful_count"] or 0) / 5.0, 1.0)
            ws_boost = _workspace_match(c, workspace)
            score = (0.30 * sims[i] + 0.25 * c["confidence"] * df +
                     0.15 * freq + 0.15 * helpful + 0.10 * ws_boost + 0.05)
            scored.append((score, c))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [s[1] for s in scored[:top_k]]
    except Exception:
        return _apply_workspace_boost(candidates[:top_k], workspace)


def retrieve(query, top_k=15, workspace=None):
    """Full two-stage retrieval: FTS5 -> TF-IDF re-rank with workspace awareness."""
    db = get_db()
    candidates = retrieve_fts(db, query, limit=top_k * 4)
    if len(candidates) < 5:
        candidates = list(candidates) + list(retrieve_fallback(db, top_k * 3))
    results = retrieve_tfidf_rerank(candidates, query, top_k, workspace=workspace)
    db.close()
    return results


def _workspace_match(rule, workspace):
    """Score workspace relevance (0.0 to 1.0)."""
    if not workspace or not rule.get("source_workspace"):
        return 0.0
    rule_ws = rule["source_workspace"]
    if workspace == rule_ws:
        return 1.0
    if workspace.startswith(rule_ws) or rule_ws.startswith(workspace):
        return 0.7
    return 0.0


def _apply_workspace_boost(candidates, workspace):
    """Simple workspace boost when TF-IDF is unavailable."""
    if not workspace or not candidates:
        return candidates
    scored = []
    for c in candidates:
        ws = _workspace_match(c, workspace)
        helpful = min((c["helpful_count"] or 0) / 5.0, 1.0)
        score = c["confidence"] + 0.2 * ws + 0.1 * helpful
        scored.append((score, c))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [s[1] for s in scored]


# --------------- ADD / UPDATE ---------------

def add_rule(content, category="general", confidence=0.5, source_session=None,
             source_workspace=None, evidence=None):
    """Add a new rule or boost existing if similar content found."""
    db = get_db()
    existing = find_similar(db, content)
    if existing:
        db.execute("""
            UPDATE rules SET occurrences = occurrences + 1,
            confidence = MIN(confidence + 0.15, 1.0),
            last_seen = datetime('now') WHERE id = ?
        """, (existing["id"],))
        db.commit()
        rule_id = existing["id"]
    else:
        cur = db.execute("""
            INSERT INTO rules (content, category, confidence, source_session,
            source_workspace, evidence) VALUES (?, ?, ?, ?, ?, ?)
        """, (content, category, confidence, source_session,
              source_workspace, json.dumps(evidence or [])))
        db.commit()
        rule_id = cur.lastrowid
    mark_tfidf_dirty(db)
    record_event(db, "rule_added", rule_id, {"content": content[:100]})
    db.close()
    return rule_id


def add_anti_pattern(content, severity="high", source_event=None):
    """Add a critical anti-pattern or boost existing."""
    db = get_db()
    existing = db.execute(
        "SELECT * FROM anti_patterns WHERE content = ?", (content,)
    ).fetchone()
    if existing:
        db.execute("""
            UPDATE anti_patterns SET occurrences = occurrences + 1,
            last_seen = datetime('now') WHERE id = ?
        """, (existing["id"],))
        db.commit()
        return existing["id"]
    cur = db.execute("""
        INSERT INTO anti_patterns (content, severity, source_event) VALUES (?, ?, ?)
    """, (content, severity, source_event))
    db.commit()
    ap_id = cur.lastrowid
    record_event(db, "anti_pattern_added", ap_id, {"content": content[:100]})
    db.close()
    return ap_id


def add_preference(content):
    """Add or reinforce a user preference."""
    db = get_db()
    existing = db.execute(
        "SELECT * FROM preferences WHERE content = ?", (content,)
    ).fetchone()
    if existing:
        db.execute("""
            UPDATE preferences SET occurrences = occurrences + 1,
            confidence = MIN(confidence + 0.1, 1.0),
            last_seen = datetime('now') WHERE id = ?
        """, (existing["id"],))
        db.commit()
        return existing["id"]
    cur = db.execute(
        "INSERT INTO preferences (content) VALUES (?)", (content,)
    )
    db.commit()
    pref_id = cur.lastrowid
    db.close()
    return pref_id


# --------------- SIMILARITY ---------------

def find_similar(db, content, threshold=0.6):
    """Find existing rule similar to content using FTS5."""
    words = [w for w in content.lower().split() if len(w) > 3][:8]
    if not words:
        return None
    query = " OR ".join(words)
    try:
        rows = db.execute("""
            SELECT r.* FROM rules_fts JOIN rules r ON rules_fts.rowid = r.id
            WHERE rules_fts MATCH ? LIMIT 5
        """, (query,)).fetchall()
        for row in rows:
            overlap = _word_overlap(content, row["content"])
            if overlap >= threshold:
                return row
    except Exception:
        pass
    return None


def _word_overlap(a, b):
    """Simple Jaccard similarity on words."""
    wa = set(a.lower().split())
    wb = set(b.lower().split())
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / len(wa | wb)


# --------------- TF-IDF MODEL ---------------

def retrain_tfidf():
    """Retrain TF-IDF model from all rules."""
    db = get_db()
    rows = db.execute("SELECT id, content FROM rules WHERE maturity != 'deprecated'").fetchall()
    if len(rows) < 3:
        db.close()
        return False
    from sklearn.feature_extraction.text import TfidfVectorizer
    texts = [r["content"] for r in rows]
    vectorizer = TfidfVectorizer(max_features=5000, stop_words="english")
    vectorizer.fit(texts)
    TFIDF_DIR.mkdir(exist_ok=True)
    pickle.dump(vectorizer, open(TFIDF_DIR / "vectorizer.pkl", "wb"))
    db.execute("UPDATE meta SET value = '0', updated_at = datetime('now') WHERE key = 'tfidf_dirty'")
    db.commit()
    db.close()
    return True


def mark_tfidf_dirty(db):
    db.execute("UPDATE meta SET value = '1', updated_at = datetime('now') WHERE key = 'tfidf_dirty'")


def is_tfidf_dirty():
    db = get_db()
    row = db.execute("SELECT value FROM meta WHERE key = 'tfidf_dirty'").fetchone()
    db.close()
    return row and row["value"] == "1"


# --------------- CONTEXT GENERATION ---------------

def get_context(task=None, top_k=15):
    """Generate full context for injection. Returns formatted markdown."""
    db = get_db()
    anti_patterns = db.execute(
        "SELECT * FROM anti_patterns ORDER BY severity DESC, confidence DESC LIMIT 10"
    ).fetchall()
    prefs = db.execute(
        "SELECT * FROM preferences ORDER BY confidence DESC, occurrences DESC LIMIT 5"
    ).fetchall()
    principles = db.execute(
        "SELECT * FROM principles ORDER BY confidence DESC LIMIT 20"
    ).fetchall()
    db.close()

    rules = retrieve(task, top_k) if task else []
    total = count_rules()

    lines = ["## Capy Cortex: Learned Knowledge", ""]
    if anti_patterns:
        lines.append("### NEVER DO")
        for ap in anti_patterns:
            lines.append(f"- [{ap['severity'].upper()}] {ap['content']}")
        lines.append("")
    if prefs:
        lines.append("### User Preferences")
        for p in prefs:
            lines.append(f"- {p['content']}")
        lines.append("")
    if principles:
        lines.append(f"### Principles ({len(principles)} distilled)")
        for p in principles:
            lines.append(f"- {p['content']}")
        lines.append("")
    if rules:
        lines.append(f"### Task-Relevant Rules (top {len(rules)} of {total})")
        for r in rules:
            lines.append(f"- [{r['confidence']:.1f}] {r['content']}")
        lines.append("")
    return "\n".join(lines)


# --------------- STATS ---------------

def count_rules():
    db = get_db()
    n = db.execute("SELECT COUNT(*) FROM rules WHERE maturity != 'deprecated'").fetchone()[0]
    db.close()
    return n


def record_event(db, event_type, rule_id=None, metadata=None):
    db.execute("INSERT INTO events (event_type, rule_id, metadata) VALUES (?, ?, ?)",
               (event_type, rule_id, json.dumps(metadata or {})))


def stats():
    """Return database statistics."""
    db = get_db()
    s = {
        "rules": db.execute("SELECT COUNT(*) FROM rules WHERE maturity != 'deprecated'").fetchone()[0],
        "deprecated": db.execute("SELECT COUNT(*) FROM rules WHERE maturity = 'deprecated'").fetchone()[0],
        "anti_patterns": db.execute("SELECT COUNT(*) FROM anti_patterns").fetchone()[0],
        "preferences": db.execute("SELECT COUNT(*) FROM preferences").fetchone()[0],
        "principles": db.execute("SELECT COUNT(*) FROM principles").fetchone()[0],
        "diary_entries": db.execute("SELECT COUNT(*) FROM diary").fetchone()[0],
        "events": db.execute("SELECT COUNT(*) FROM events").fetchone()[0],
        "tfidf_dirty": is_tfidf_dirty(),
        "categories": {r[0]: r[1] for r in db.execute(
            "SELECT category, COUNT(*) FROM rules WHERE maturity != 'deprecated' GROUP BY category"
        ).fetchall()},
    }
    db.close()
    return s


# --------------- DECAY ---------------

def apply_decay():
    """Apply confidence decay to all rules. Run periodically."""
    db = get_db()
    db.execute("""
        UPDATE rules SET confidence = confidence * 0.95
        WHERE last_seen < datetime('now', '-7 days') AND maturity != 'deprecated'
    """)
    db.execute("""
        UPDATE rules SET maturity = 'deprecated'
        WHERE confidence < 0.2 AND maturity != 'deprecated'
    """)
    db.commit()
    db.close()


# --------------- CLI ---------------

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: cortex.py <command> [args]")
        print("Commands: retrieve, add-rule, add-ap, add-pref, context, stats, retrain, decay")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "retrieve":
        query = sys.argv[2] if len(sys.argv) > 2 else "general"
        for r in retrieve(query):
            print(f"[{r['confidence']:.2f}] [{r['category']}] {r['content']}")
    elif cmd == "add-rule":
        content = sys.argv[2]
        cat = sys.argv[3] if len(sys.argv) > 3 else "general"
        rid = add_rule(content, cat)
        print(f"Rule #{rid} added/boosted")
    elif cmd == "add-ap":
        content = sys.argv[2]
        sev = sys.argv[3] if len(sys.argv) > 3 else "high"
        aid = add_anti_pattern(content, sev)
        print(f"Anti-pattern #{aid} added/boosted")
    elif cmd == "add-pref":
        content = sys.argv[2]
        pid = add_preference(content)
        print(f"Preference #{pid} added/boosted")
    elif cmd == "context":
        task = sys.argv[2] if len(sys.argv) > 2 else None
        print(get_context(task))
    elif cmd == "stats":
        import pprint
        pprint.pprint(stats())
    elif cmd == "retrain":
        ok = retrain_tfidf()
        print(f"TF-IDF retrain: {'OK' if ok else 'SKIPPED (need 3+ rules)'}")
    elif cmd == "decay":
        apply_decay()
        print("Decay applied")
    else:
        print(f"Unknown command: {cmd}")
