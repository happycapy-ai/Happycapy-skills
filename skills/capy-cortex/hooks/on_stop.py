#!/usr/bin/env python3
"""Capy Cortex Hook: Stop - The sleep cycle.
Extracts lessons from the just-completed interaction. Runs async (non-blocking).
Scans last assistant message for patterns: corrections, preferences, successes."""

import json
import sys
import re
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

DB_PATH = Path(__file__).parent.parent / "cortex.db"
SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"

# Noise patterns to filter out (session continuations, system messages, skill metadata)
NOISE_PATTERNS = [
    r"session is being continued from a previous",
    r"Base directory for this skill",
    r"<teammate-message",
    r"<task-notification>",
    r"system-reminder",
    r"^##\s+",  # Markdown headers from system injections
    r"^###\s+",
]

# Patterns that indicate user corrections (learned from research)
CORRECTION_PATTERNS = [
    r"(?:no[,!.]?\s+(?:don'?t|do not|that'?s not|wrong|stop|never))",
    r"(?:instead\s+(?:use|try|do))",
    r"(?:I\s+(?:said|meant|asked|wanted))",
    r"(?:that'?s\s+(?:wrong|incorrect|not what))",
    r"(?:please\s+(?:don'?t|stop|never))",
]

# Preference patterns - more strict now
PREFERENCE_PATTERNS = [
    r"^(?:always\s+(?:use|do|prefer|make))",  # Only at sentence start
    r"^(?:I\s+(?:prefer|like|want)\s+)",
    r"(?:from\s+now\s+on)",
    r"(?:remember\s+(?:to|that))",
]

# Auto-maintenance interval (every N sessions)
MAINTENANCE_INTERVAL = 10


def main():
    try:
        data = json.loads(sys.stdin.read())
    except Exception:
        return

    if not DB_PATH.exists():
        return

    # Don't recurse if already in a stop hook
    if data.get("stop_hook_active"):
        return

    session_id = data.get("session_id", "")
    transcript_path = data.get("transcript_path", "")

    try:
        db = sqlite3.connect(str(DB_PATH))
        db.execute("PRAGMA journal_mode=WAL")
        db.execute("PRAGMA busy_timeout=3000")

        # Extract user messages from recent transcript
        user_messages = _extract_recent_user_messages(transcript_path, limit=5)

        for msg in user_messages:
            # Source filtering: skip noise
            if _is_noise(msg):
                continue

            # Skip overly long messages (code dumps, not preferences)
            if len(msg) > 2000:
                continue

            msg_lower = msg.lower()

            # Check for corrections -> anti-patterns (only in short messages)
            if len(msg) < 500:
                for pattern in CORRECTION_PATTERNS:
                    match = re.search(pattern, msg_lower)
                    if match:
                        # Extract just the correction, not the whole message
                        result = _extract_correction(msg, match)
                        if result:
                            content, cat, topic = result
                            if content and not _is_noise(content):
                                _add_rule_safe(db, content, cat, 0.6, session_id, topic=topic)
                        break

            # Check for preferences (only in short messages)
            if len(msg) < 300:
                for pattern in PREFERENCE_PATTERNS:
                    # Check if pattern is at sentence start
                    sentences = re.split(r'[.!?]\s+', msg)
                    for sentence in sentences:
                        sentence_lower = sentence.lower().strip()
                        if re.match(pattern, sentence_lower):
                            # Extract just the preference statement
                            preference = sentence.strip()[:200]
                            if preference and not _is_noise(preference):
                                _add_preference_safe(db, preference)
                            break

        # LLM session extraction: deep analysis of session learnings
        llm_learnings_count = 0
        if len(user_messages) >= 2:
            try:
                sys.path.insert(0, str(SCRIPTS_DIR))
                from llm_extract import extract_session_learnings
                learnings = extract_session_learnings(user_messages, session_id=session_id)
                for learning in learnings:
                    content = learning.get('content', '')
                    if content and not _is_noise(content):
                        _add_rule_safe(
                            db, content, learning.get('category', 'pattern'),
                            0.7, session_id, topic=learning.get('topic'),
                            quality_score=learning.get('quality_score', 0),
                            extraction_method=learning.get('extraction_method', 'llm_v2_session'))
                        llm_learnings_count += 1
            except Exception:
                pass  # LLM extraction is best-effort

        # Record session event
        db.execute(
            "INSERT INTO events (event_type, metadata) VALUES (?, ?)",
            ("session_reflection", json.dumps({
                "session_id": session_id,
                "messages_scanned": len(user_messages),
                "llm_learnings": llm_learnings_count,
            }))
        )

        # Auto-maintenance: run every MAINTENANCE_INTERVAL sessions
        session_count = db.execute(
            "SELECT COUNT(*) FROM events WHERE event_type = 'session_reflection'"
        ).fetchone()[0]

        if session_count % MAINTENANCE_INTERVAL == 0 and session_count > 0:
            _run_maintenance(db)

        # Check if TF-IDF needs retraining
        dirty = db.execute(
            "SELECT value FROM meta WHERE key = 'tfidf_dirty'"
        ).fetchone()
        rule_count = db.execute(
            "SELECT COUNT(*) FROM rules"
        ).fetchone()[0]

        db.commit()
        db.close()

        # Retrain TF-IDF if dirty and enough rules
        if dirty and dirty[0] == "1" and rule_count >= 5:
            try:
                sys.path.insert(0, str(SCRIPTS_DIR))
                from cortex import retrain_tfidf
                retrain_tfidf()
            except Exception:
                pass

        # Bridge sync: import skills as principles (lightweight, fast)
        try:
            sys.path.insert(0, str(SCRIPTS_DIR))
            from bridge_claudeception import import_skills_as_principles
            import_skills_as_principles()
        except Exception:
            pass

        # Output nothing -- this hook is silent
        print(json.dumps({"suppressOutput": True}))

    except Exception:
        pass  # Hooks must NEVER crash


def _is_noise(text):
    """Check if text matches any noise patterns."""
    for pattern in NOISE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def _extract_correction(msg, match):
    """Extract clean, actionable correction from user message.
    Uses LLM extraction via AI Gateway, with regex fallback."""
    # Try LLM extraction first (generous timeout -- this hook runs async)
    try:
        sys.path.insert(0, str(SCRIPTS_DIR))
        from llm_extract import extract_correction
        result = extract_correction(msg, timeout=8)
        if result and result.get("actionable"):
            rule = result.get("rule", "")
            if rule and len(rule) >= 10:
                return rule, result.get("category", "correction"), result.get("topic")
    except Exception:
        pass

    # Fallback: extract the most informative sentence (skip noise fragments)
    sentences = re.split(r'[.!?]+\s+', msg)
    match_text = match.group(0).lower()
    best = None
    for sentence in sentences:
        cleaned = re.sub(r'\s+', ' ', sentence).strip()
        if len(cleaned) < 15:
            continue  # Skip noise fragments like "no stop"
        if match_text in cleaned.lower() or (best is None and len(cleaned) > 20):
            if best is None or len(cleaned) > len(best):
                best = cleaned[:300]

    if best:
        return best, "correction", None

    # Last resort: use the whole message if it's short enough
    cleaned = re.sub(r'\s+', ' ', msg).strip()
    if len(cleaned) > 300:
        cleaned = cleaned[:300]
    if len(cleaned) >= 15:
        return cleaned, "correction", None

    return None


def _extract_recent_user_messages(transcript_path, limit=5):
    """Extract recent user messages from session transcript.
    Filters out system messages, skill metadata, and session continuations."""
    messages = []
    if not transcript_path or not Path(transcript_path).exists():
        return messages
    try:
        with open(transcript_path) as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if entry.get("type") == "user":
                        msg = entry.get("message", {})
                        content = msg.get("content", "")
                        if isinstance(content, list):
                            text_parts = [
                                p.get("text", "") for p in content
                                if isinstance(p, dict) and p.get("type") == "text"
                            ]
                            content = " ".join(text_parts)
                        if isinstance(content, str) and len(content) > 10:
                            # Only add if not noise
                            if not _is_noise(content):
                                messages.append(content)
                except (json.JSONDecodeError, KeyError):
                    continue
        return messages[-limit:]
    except Exception:
        return []


def _run_maintenance(db):
    """Run periodic maintenance tasks:
    - Confidence decay for rules not seen in 30 days
    - Deprecate rules with confidence < 0.15
    - Temporal expiration (forget_after)
    - Static/dynamic principle classification
    - Retrain TF-IDF if dirty"""
    try:
        # Confidence decay: reduce confidence for rules not seen in 30+ days
        thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()
        db.execute("""
            UPDATE rules
            SET confidence = MAX(0.1, confidence * 0.9)
            WHERE last_seen < ?
            AND confidence > 0.15
        """, (thirty_days_ago,))

        # Deprecate rules with very low confidence
        db.execute("""
            UPDATE rules
            SET maturity = 'deprecated'
            WHERE confidence < 0.15
            AND maturity != 'deprecated'
        """)

        # Mark TF-IDF as dirty if we made changes
        db.execute("UPDATE meta SET value = '1' WHERE key = 'tfidf_dirty'")

        db.commit()
    except Exception:
        pass  # Maintenance failures should not crash the hook

    # Phase 5: Temporal expiration and principle classification
    try:
        sys.path.insert(0, str(SCRIPTS_DIR))
        from temporal import expire_forgotten_rules, classify_principle_persistence
        expire_forgotten_rules()
        classify_principle_persistence()
    except Exception:
        pass  # Phase 5 failures should not crash the hook


def _add_rule_safe(db, content, category, confidence, session_id, topic=None,
                   quality_score=0, extraction_method='regex'):
    """Add rule with dedup check, quality metadata, and auto-topic assignment."""
    try:
        existing = db.execute(
            "SELECT id FROM rules WHERE content = ?", (content,)
        ).fetchone()
        if existing:
            db.execute("""
                UPDATE rules SET occurrences = occurrences + 1,
                last_seen = datetime('now') WHERE id = ?
            """, (existing[0],))
            rule_id = existing[0]
        else:
            db.execute("""
                INSERT INTO rules (content, category, confidence, source_session,
                                   quality_score, extraction_method)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (content, category, confidence, session_id,
                  quality_score, extraction_method))
            rule_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]

            # Version chain: link to similar existing rule (Phase 5A)
            try:
                # Find rules with 60%+ word overlap
                new_words = set(content.lower().split())
                candidates = db.execute(
                    "SELECT id, content FROM rules WHERE category = ? AND id != ? LIMIT 50",
                    (category, rule_id)
                ).fetchall()
                for cand_id, cand_content in candidates:
                    cand_words = set(cand_content.lower().split())
                    if not cand_words:
                        continue
                    overlap = len(new_words & cand_words) / max(len(new_words | cand_words), 1)
                    if overlap >= 0.6:
                        sys.path.insert(0, str(SCRIPTS_DIR))
                        from temporal import create_version_chain
                        create_version_chain(cand_id, rule_id)
                        break  # Only chain to one parent
            except Exception:
                pass  # Version chaining is best-effort

        # Auto-assign topic (Phase 4F)
        try:
            sys.path.insert(0, str(SCRIPTS_DIR))
            from topic_engine import detect_topic_for_rule
            assigned_topic = topic or detect_topic_for_rule(content, category)
            topic_row = db.execute(
                "SELECT id FROM topics WHERE name = ?", (assigned_topic,)
            ).fetchone()
            if topic_row:
                db.execute(
                    "INSERT OR IGNORE INTO rule_topics (rule_id, topic_id) VALUES (?, ?)",
                    (rule_id, topic_row[0])
                )
                db.execute(
                    "UPDATE topics SET rule_count = rule_count + 1 WHERE id = ?",
                    (topic_row[0],)
                )
        except Exception:
            pass  # Topic assignment is best-effort

        db.execute("UPDATE meta SET value = '1' WHERE key = 'tfidf_dirty'")
    except Exception:
        pass


def _add_preference_safe(db, content):
    """Add preference without crashing on duplicates."""
    try:
        existing = db.execute(
            "SELECT id FROM preferences WHERE content = ?", (content,)
        ).fetchone()
        if existing:
            db.execute("""
                UPDATE preferences SET occurrences = occurrences + 1,
                last_seen = datetime('now') WHERE id = ?
            """, (existing[0],))
        else:
            db.execute(
                "INSERT INTO preferences (content) VALUES (?)", (content,)
            )
    except Exception:
        pass


if __name__ == "__main__":
    main()
