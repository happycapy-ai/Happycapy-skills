#!/usr/bin/env python3
"""Capy Cortex - Phase 5: SuperMemory-Inspired Temporal Memory.
Implements 5 ideas extracted from SuperMemory's open-source data model:
1. Immutable version chains (contradiction resolution without data loss)
2. Three relationship types (updates/extends/derives)
3. Two-stage identity resolution (exact match + semantic fallback)
4. Temporal expiration (forget_after)
5. Static/dynamic principle classification"""

import json
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / "cortex.db"

VALID_RELATION_TYPES = ("updates", "extends", "derives")

# Keywords that suggest a principle is static (permanent)
STATIC_KEYWORDS = [
    "always", "never", "prefer", "use", "avoid", "ensure",
    "convention", "standard", "default", "rule", "principle",
]
DYNAMIC_KEYWORDS = [
    "currently", "running", "session", "now", "today", "port",
    "temporary", "this project", "this repo",
]


def get_db():
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA busy_timeout=5000")
    return db


# ---- Schema Migration ----

def migrate_phase5():
    """Add Phase 5 columns and tables. Safe to run multiple times."""
    db = get_db()

    # Add new columns to rules (ignore if already exists)
    for col, typedef in [
        ("parent_rule_id", "INTEGER REFERENCES rules(id)"),
        ("root_rule_id", "INTEGER REFERENCES rules(id)"),
        ("is_latest", "INTEGER DEFAULT 1"),
        ("forget_after", "TEXT"),
    ]:
        try:
            db.execute(f"ALTER TABLE rules ADD COLUMN {col} {typedef}")
        except sqlite3.OperationalError:
            pass  # Column already exists

    # Add is_static to principles
    try:
        db.execute("ALTER TABLE principles ADD COLUMN is_static INTEGER DEFAULT 0")
    except sqlite3.OperationalError:
        pass

    # Create rule_relations table
    db.execute("""
        CREATE TABLE IF NOT EXISTS rule_relations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_rule_id INTEGER NOT NULL REFERENCES rules(id),
            target_rule_id INTEGER NOT NULL REFERENCES rules(id),
            relation_type TEXT NOT NULL CHECK(relation_type IN ('updates', 'extends', 'derives')),
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)

    db.execute("""
        CREATE INDEX IF NOT EXISTS idx_relations_source
        ON rule_relations(source_rule_id)
    """)
    db.execute("""
        CREATE INDEX IF NOT EXISTS idx_relations_target
        ON rule_relations(target_rule_id)
    """)

    db.commit()
    db.close()


# ---- 1. Version Chains ----

def create_version_chain(old_rule_id, new_content, category=None, confidence=None):
    """Create a new version of a rule, forming an immutable version chain.
    The old rule gets is_latest=0. Returns the new rule's ID."""
    db = get_db()

    old_rule = db.execute("SELECT * FROM rules WHERE id = ?", (old_rule_id,)).fetchone()
    if not old_rule:
        db.close()
        return None

    # Determine root: if old rule has a root, use it; otherwise old rule IS the root
    root_id = old_rule["root_rule_id"] or old_rule_id

    cur = db.execute("""
        INSERT INTO rules (content, category, confidence, is_latest,
                          parent_rule_id, root_rule_id, source_workspace, source_session)
        VALUES (?, ?, ?, 1, ?, ?, ?, ?)
    """, (
        new_content,
        category or old_rule["category"],
        confidence if confidence is not None else old_rule["confidence"],
        old_rule_id,
        root_id,
        old_rule["source_workspace"],
        old_rule["source_session"],
    ))
    new_id = cur.lastrowid

    # Mark old rule as no longer latest
    db.execute("UPDATE rules SET is_latest = 0 WHERE id = ?", (old_rule_id,))

    # Auto-create "updates" relation
    db.execute("""
        INSERT INTO rule_relations (source_rule_id, target_rule_id, relation_type)
        VALUES (?, ?, 'updates')
    """, (new_id, old_rule_id))

    # Record event
    db.execute(
        "INSERT INTO events (event_type, rule_id, metadata) VALUES (?, ?, ?)",
        ("rule_versioned", new_id, json.dumps({
            "old_rule_id": old_rule_id,
            "root_rule_id": root_id,
        }))
    )

    db.commit()
    db.close()
    return new_id


def get_version_chain(rule_id):
    """Walk the version chain from root to latest. Returns list of rule dicts."""
    db = get_db()
    rule = db.execute("SELECT * FROM rules WHERE id = ?", (rule_id,)).fetchone()
    if not rule:
        db.close()
        return []

    # Find root
    root_id = rule["root_rule_id"] or rule_id

    # Get all rules in this chain
    chain = db.execute("""
        SELECT * FROM rules
        WHERE root_rule_id = ? OR id = ?
        ORDER BY id ASC
    """, (root_id, root_id)).fetchall()

    db.close()
    return [dict(r) for r in chain]


# ---- 2. Rule Relations ----

def add_rule_relation(source_rule_id, target_rule_id, relation_type):
    """Add a typed relationship between two rules."""
    if relation_type not in VALID_RELATION_TYPES:
        raise ValueError(f"Invalid relation type: {relation_type}. Must be one of {VALID_RELATION_TYPES}")

    db = get_db()
    # Check for existing relation
    existing = db.execute("""
        SELECT id FROM rule_relations
        WHERE source_rule_id = ? AND target_rule_id = ? AND relation_type = ?
    """, (source_rule_id, target_rule_id, relation_type)).fetchone()

    if not existing:
        db.execute("""
            INSERT INTO rule_relations (source_rule_id, target_rule_id, relation_type)
            VALUES (?, ?, ?)
        """, (source_rule_id, target_rule_id, relation_type))
        db.commit()
    db.close()


def get_rule_relations(rule_id):
    """Get all relations for a rule (both as source and target)."""
    db = get_db()
    rels = db.execute("""
        SELECT * FROM rule_relations
        WHERE source_rule_id = ? OR target_rule_id = ?
        ORDER BY created_at DESC
    """, (rule_id, rule_id)).fetchall()
    db.close()
    return [dict(r) for r in rels]


# ---- 3. Contradiction Detection ----

def find_contradictions(threshold=0.4):
    """Find pairs of active rules that likely contradict each other.
    Uses word overlap within the same category as a heuristic."""
    db = get_db()
    rules = db.execute("""
        SELECT id, content, category, confidence FROM rules
        WHERE maturity != 'deprecated' AND is_latest = 1
        ORDER BY category, id
    """).fetchall()
    db.close()

    contradictions = []
    rules_list = list(rules)

    for i in range(len(rules_list)):
        for j in range(i + 1, len(rules_list)):
            a = rules_list[i]
            b = rules_list[j]

            # Same or similar category = higher chance of contradiction
            same_cat = a["category"] == b["category"]

            wa = set(a["content"].lower().split())
            wb = set(b["content"].lower().split())
            if not wa or not wb:
                continue

            overlap = len(wa & wb) / len(wa | wb)

            # Check for negation signals
            negation_words = {"never", "don't", "dont", "not", "avoid", "instead", "no"}
            a_has_neg = bool(wa & negation_words)
            b_has_neg = bool(wb & negation_words)
            opposing = a_has_neg != b_has_neg  # One negates, other doesn't

            # Score: high overlap + opposing sentiment = contradiction
            score = overlap
            if same_cat:
                score += 0.15
            if opposing:
                score += 0.2

            if score >= threshold:
                contradictions.append({
                    "rule_a": a["id"],
                    "rule_b": b["id"],
                    "score": round(score, 3),
                    "reason": f"overlap={overlap:.2f} same_cat={same_cat} opposing={opposing}",
                })

    # Sort by contradiction score
    contradictions.sort(key=lambda x: x["score"], reverse=True)
    return contradictions


def supersede_rule(old_rule_id, new_rule_id):
    """Mark old_rule as superseded by new_rule. Creates an 'updates' relation
    and sets old_rule.is_latest=0. Does NOT create a version chain
    (both rules already exist independently)."""
    db = get_db()
    db.execute("UPDATE rules SET is_latest = 0 WHERE id = ?", (old_rule_id,))

    # Add relation
    existing = db.execute("""
        SELECT id FROM rule_relations
        WHERE source_rule_id = ? AND target_rule_id = ? AND relation_type = 'updates'
    """, (new_rule_id, old_rule_id)).fetchone()

    if not existing:
        db.execute("""
            INSERT INTO rule_relations (source_rule_id, target_rule_id, relation_type)
            VALUES (?, ?, 'updates')
        """, (new_rule_id, old_rule_id))

    db.execute(
        "INSERT INTO events (event_type, rule_id, metadata) VALUES (?, ?, ?)",
        ("rule_versioned", new_rule_id, json.dumps({
            "superseded_rule_id": old_rule_id,
        }))
    )

    db.commit()
    db.close()
    return new_rule_id


# ---- 4. Two-Stage Identity Resolution ----

def two_stage_find_similar(db, content, exact_threshold=1.0, semantic_threshold=0.5):
    """Two-stage dedup: exact content match first, then semantic fallback.
    Stage 1: Exact string match (fast, O(1) with index)
    Stage 2: FTS5 + word overlap (semantic, catches near-duplicates)"""
    # Stage 1: exact match
    exact = db.execute(
        "SELECT * FROM rules WHERE content = ? AND maturity != 'deprecated'",
        (content,)
    ).fetchone()
    if exact:
        return exact

    # Stage 2: semantic match via FTS5 + word overlap
    words = [w for w in content.lower().split() if len(w) > 3 and w.isalnum()][:8]
    if not words:
        return None

    query = " OR ".join(words)
    try:
        candidates = db.execute("""
            SELECT r.* FROM rules_fts JOIN rules r ON rules_fts.rowid = r.id
            WHERE rules_fts MATCH ? AND r.maturity != 'deprecated'
            LIMIT 10
        """, (query,)).fetchall()

        content_words = set(content.lower().split())
        for cand in candidates:
            cand_words = set(cand["content"].lower().split())
            if not content_words or not cand_words:
                continue
            overlap = len(content_words & cand_words) / len(content_words | cand_words)
            if overlap >= semantic_threshold:
                return cand
    except Exception:
        pass

    return None


# ---- 5. Temporal Expiration ----

def expire_forgotten_rules():
    """Deprecate rules whose forget_after date has passed.
    Returns count of expired rules."""
    db = get_db()
    now = datetime.now().isoformat()

    # Find rules to expire
    expired = db.execute("""
        SELECT id FROM rules
        WHERE forget_after IS NOT NULL
        AND forget_after < ?
        AND maturity != 'deprecated'
    """, (now,)).fetchall()

    count = len(expired)
    if count > 0:
        db.execute("""
            UPDATE rules SET maturity = 'deprecated', is_latest = 0
            WHERE forget_after IS NOT NULL
            AND forget_after < ?
            AND maturity != 'deprecated'
        """, (now,))

        db.execute(
            "INSERT INTO events (event_type, metadata) VALUES (?, ?)",
            ("rules_expired", json.dumps({"count": count, "timestamp": now}))
        )
        db.commit()

    db.close()
    return count


# ---- 6. Static/Dynamic Principle Classification ----

def classify_principle_persistence():
    """Classify principles as static (permanent) or dynamic (temporary).
    Static: high confidence, high occurrences, or contains preference keywords.
    Dynamic: low confidence, low occurrences, or contains temporal keywords.
    Returns count of principles classified."""
    db = get_db()
    principles = db.execute("SELECT * FROM principles").fetchall()

    classified = 0
    for p in principles:
        content_lower = p["content"].lower()
        confidence = p["confidence"]
        occurrences = p["occurrences"]

        # Score static-ness
        static_score = 0.0

        # High confidence = likely stable
        if confidence >= 0.8:
            static_score += 0.3
        elif confidence >= 0.6:
            static_score += 0.1

        # High occurrences = reinforced over time = stable
        if occurrences >= 3:
            static_score += 0.3
        elif occurrences >= 2:
            static_score += 0.15

        # Keyword analysis
        for kw in STATIC_KEYWORDS:
            if kw in content_lower:
                static_score += 0.1
                break

        for kw in DYNAMIC_KEYWORDS:
            if kw in content_lower:
                static_score -= 0.3
                break

        is_static = 1 if static_score >= 0.4 else 0

        db.execute(
            "UPDATE principles SET is_static = ? WHERE id = ?",
            (is_static, p["id"])
        )
        classified += 1

    db.commit()
    db.close()
    return classified


# ---- CLI ----

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: temporal.py <migrate|contradictions|expire|classify|chain>")
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "migrate":
        migrate_phase5()
        print("Phase 5 migration complete")
    elif cmd == "contradictions":
        cs = find_contradictions()
        for c in cs[:10]:
            print(f"  Rule #{c['rule_a']} vs #{c['rule_b']}: score={c['score']} ({c['reason']})")
    elif cmd == "expire":
        n = expire_forgotten_rules()
        print(f"Expired {n} rules")
    elif cmd == "classify":
        n = classify_principle_persistence()
        print(f"Classified {n} principles")
    elif cmd == "chain":
        rid = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        chain = get_version_chain(rid)
        for r in chain:
            latest = "*" if r["is_latest"] else " "
            print(f"  [{latest}] #{r['id']}: {r['content'][:80]}")
    else:
        print(f"Unknown command: {cmd}")
