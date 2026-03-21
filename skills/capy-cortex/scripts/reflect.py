#!/usr/bin/env python3
"""Capy Cortex - Reflection Engine (the dreaming brain).
Deep session analysis: extracts rules, anti-patterns, and diary entries
from session transcripts. More thorough than the on_stop.py hook.

Aristotelian Axioms:
  A1: Every session contains implicit knowledge (patterns, mistakes, preferences)
  A2: Explicit corrections are highest-signal data (user said "no, don't do X")
  A3: Tool failures are empirical evidence of anti-patterns
  A4: Repeated patterns across sessions are more reliable than one-offs
  A5: Reflection must be idempotent (safe to re-run on same session)
"""

import json
import sys
import re
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / "cortex.db"
SCRIPTS_DIR = Path(__file__).parent

# --- Signal extraction patterns ---

CORRECTION_PATTERNS = [
    (r"(?:no[,!.]?\s+(?:don'?t|do not|that'?s not|wrong|stop|never))", "correction", 0.7),
    (r"(?:instead\s+(?:use|try|do))", "correction", 0.65),
    (r"(?:I\s+(?:said|meant|asked|wanted))", "correction", 0.6),
    (r"(?:that'?s\s+(?:wrong|incorrect|not what))", "correction", 0.7),
    (r"(?:please\s+(?:don'?t|stop|never))", "correction", 0.65),
]

PREFERENCE_PATTERNS = [
    (r"(?:always\s+(?:use|do|prefer|make))", "preference"),
    (r"(?:I\s+(?:prefer|like|want)\s+)", "preference"),
    (r"(?:from\s+now\s+on)", "preference"),
    (r"(?:remember\s+(?:to|that))", "preference"),
    (r"(?:never\s+(?:use|do|add|include|put))", "anti_preference"),
]

SUCCESS_PATTERNS = [
    r"(?:perfect|exactly|great|nice|good job|well done|that'?s right)",
    r"(?:yes[,!.]?\s+(?:that|this|exactly))",
    r"(?:thanks|thank you)",
]

# Only match actual error OUTPUT patterns (stack traces, exit codes)
# NOT the AI discussing errors (e.g. "I fixed the error")
ERROR_OUTPUT_PATTERNS = [
    r"^Traceback \(most recent call last\):",
    r"^Error: ",
    r"^ERR!",
    r"^\w+Error: ",    # TypeError:, SyntaxError:, etc.
    r"^fatal: ",       # git fatal errors
    r"exit code [1-9]",
    r"ENOENT|EACCES|EPERM",
    r"command not found$",
    r"Permission denied$",
    r"No such file or directory$",
]


def get_db():
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA busy_timeout=5000")
    return db


def reflect_on_session(transcript_path, session_id=None, workspace_id=None):
    """Deep reflection on a single session transcript.

    Returns dict with extracted knowledge counts.
    """
    if not Path(transcript_path).exists():
        return {"error": f"Transcript not found: {transcript_path}"}

    if not DB_PATH.exists():
        return {"error": "cortex.db not found. Run setup.py first."}

    db = get_db()

    # Idempotency check (A5): skip if already reflected
    if session_id:
        existing = db.execute(
            "SELECT id FROM diary WHERE session_id = ?", (session_id,)
        ).fetchone()
        if existing:
            db.close()
            return {"skipped": True, "reason": "Already reflected on this session"}

    # Parse transcript
    messages = _parse_transcript(transcript_path)
    if not messages:
        db.close()
        return {"skipped": True, "reason": "No messages found"}

    results = {
        "rules_added": 0,
        "anti_patterns_added": 0,
        "preferences_added": 0,
        "corrections_found": 0,
        "errors_found": 0,
        "successes_found": 0,
    }

    mistakes = []
    successes = []

    for msg in messages:
        msg_type = msg.get("type")
        content = msg.get("content", "")
        if not content or len(content) < 10:
            continue

        content_lower = content.lower()

        if msg_type == "user":
            # Extract corrections (A2: highest signal)
            for pattern, category, confidence in CORRECTION_PATTERNS:
                if re.search(pattern, content_lower):
                    rule_content = f"User correction: {content[:300]}"
                    _add_rule_safe(db, rule_content, "correction", confidence, session_id)
                    results["corrections_found"] += 1
                    results["rules_added"] += 1
                    mistakes.append(content[:150])
                    break

            # Extract preferences
            for pattern, ptype in PREFERENCE_PATTERNS:
                if re.search(pattern, content_lower):
                    if ptype == "anti_preference":
                        _add_anti_pattern_safe(db, content[:300], "medium", session_id)
                        results["anti_patterns_added"] += 1
                    else:
                        _add_preference_safe(db, content[:200])
                        results["preferences_added"] += 1
                    break

            # Detect success signals
            for pattern in SUCCESS_PATTERNS:
                if re.search(pattern, content_lower):
                    results["successes_found"] += 1
                    successes.append(content[:150])
                    break

        elif msg_type == "tool_error":
            # Extract tool failures (A3: empirical evidence)
            tool_name = msg.get("tool_name", "unknown")
            error_text = content[:300]
            rule_content = f"Tool '{tool_name}' failed: {error_text}"
            _add_rule_safe(db, rule_content, "error", 0.4, session_id)
            results["errors_found"] += 1
            results["rules_added"] += 1
            mistakes.append(f"{tool_name}: {error_text[:100]}")

        elif msg_type == "assistant":
            # Check if assistant output contains actual error output
            # (stack traces, exit codes -- NOT the AI discussing errors)
            lines = content.split("\n")
            for i, line in enumerate(lines):
                for pattern in ERROR_OUTPUT_PATTERNS:
                    if re.search(pattern, line, re.IGNORECASE):
                        ctx = "\n".join(lines[max(0, i-1):i+2])
                        if len(ctx) > 30:
                            rule_content = f"Error pattern: {ctx[:300]}"
                            _add_rule_safe(db, rule_content, "error", 0.3, session_id)
                            results["errors_found"] += 1
                            results["rules_added"] += 1
                        break
                else:
                    continue
                break  # Only capture first error per assistant message

    # Write diary entry
    summary = _generate_summary(messages, results)
    db.execute("""
        INSERT INTO diary (session_id, workspace_id, summary, mistakes, successes)
        VALUES (?, ?, ?, ?, ?)
    """, (
        session_id, workspace_id, summary,
        json.dumps(mistakes[:10]), json.dumps(successes[:10])
    ))

    # Record reflection event
    db.execute(
        "INSERT INTO events (event_type, metadata) VALUES (?, ?)",
        ("reflection", json.dumps({
            "session_id": session_id,
            "messages_analyzed": len(messages),
            **results
        }))
    )

    # Mark TF-IDF dirty if we added rules
    if results["rules_added"] > 0:
        db.execute("UPDATE meta SET value = '1' WHERE key = 'tfidf_dirty'")

    db.commit()
    db.close()

    return results


def _parse_transcript(path):
    """Parse a JSONL transcript into a list of messages."""
    messages = []
    try:
        with open(path) as f:
            for line in f:
                try:
                    entry = json.loads(line.strip())
                    msg_type = entry.get("type")
                    if msg_type not in ("user", "assistant"):
                        continue

                    raw_msg = entry.get("message", {})
                    if isinstance(raw_msg, str):
                        raw_msg = json.loads(raw_msg) if raw_msg.startswith("{") else {}

                    content = raw_msg.get("content", "")
                    if isinstance(content, list):
                        text_parts = []
                        for part in content:
                            if isinstance(part, dict):
                                if part.get("type") == "text":
                                    text_parts.append(part.get("text", ""))
                                elif part.get("type") == "tool_result":
                                    # Check for tool errors
                                    if part.get("is_error"):
                                        messages.append({
                                            "type": "tool_error",
                                            "tool_name": part.get("tool_use_id", "unknown"),
                                            "content": str(part.get("content", ""))[:500],
                                        })
                        content = " ".join(text_parts)

                    if isinstance(content, str) and len(content) > 10:
                        messages.append({
                            "type": msg_type,
                            "content": content,
                            "timestamp": entry.get("timestamp", ""),
                            "session_id": entry.get("sessionId", ""),
                        })

                except (json.JSONDecodeError, KeyError, TypeError):
                    continue
    except Exception:
        pass
    return messages


def _generate_summary(messages, results):
    """Generate a brief session summary."""
    user_msgs = [m for m in messages if m["type"] == "user"]
    total = len(messages)

    parts = [f"Session: {total} messages ({len(user_msgs)} from user)."]
    if results["corrections_found"]:
        parts.append(f"Found {results['corrections_found']} correction(s).")
    if results["errors_found"]:
        parts.append(f"Found {results['errors_found']} error(s).")
    if results["successes_found"]:
        parts.append(f"Found {results['successes_found']} success signal(s).")
    if results["preferences_added"]:
        parts.append(f"Extracted {results['preferences_added']} preference(s).")

    # First user message as topic hint
    if user_msgs:
        first = user_msgs[0]["content"][:100]
        parts.append(f"Topic: {first}")

    return " ".join(parts)


def _add_rule_safe(db, content, category, confidence, session_id):
    """Add rule with dedup."""
    try:
        # Check for existing similar rule via FTS5
        words = [w for w in content.lower().split() if len(w) > 3 and w.isalnum()][:6]
        if words:
            fts_q = " OR ".join(words)
            existing = db.execute("""
                SELECT r.id, r.content FROM rules_fts
                JOIN rules r ON rules_fts.rowid = r.id
                WHERE rules_fts MATCH ? LIMIT 5
            """, (fts_q,)).fetchall()
            for ex in existing:
                if _word_overlap(content, ex["content"]) > 0.5:
                    db.execute("""
                        UPDATE rules SET occurrences = occurrences + 1,
                        confidence = MIN(confidence + 0.1, 1.0),
                        last_seen = datetime('now') WHERE id = ?
                    """, (ex["id"],))
                    return ex["id"]

        cur = db.execute("""
            INSERT INTO rules (content, category, confidence, source_session)
            VALUES (?, ?, ?, ?)
        """, (content[:500], category, confidence, session_id))
        return cur.lastrowid
    except Exception:
        return None


def _add_anti_pattern_safe(db, content, severity, source_event):
    """Add anti-pattern with dedup."""
    try:
        existing = db.execute(
            "SELECT id FROM anti_patterns WHERE content = ?", (content,)
        ).fetchone()
        if existing:
            db.execute("""
                UPDATE anti_patterns SET occurrences = occurrences + 1,
                last_seen = datetime('now') WHERE id = ?
            """, (existing["id"],))
            return existing["id"]
        cur = db.execute("""
            INSERT INTO anti_patterns (content, severity, source_event) VALUES (?, ?, ?)
        """, (content[:500], severity, source_event))
        return cur.lastrowid
    except Exception:
        return None


def _add_preference_safe(db, content):
    """Add preference with dedup."""
    try:
        existing = db.execute(
            "SELECT id FROM preferences WHERE content = ?", (content,)
        ).fetchone()
        if existing:
            db.execute("""
                UPDATE preferences SET occurrences = occurrences + 1,
                last_seen = datetime('now') WHERE id = ?
            """, (existing["id"],))
            return existing["id"]
        cur = db.execute(
            "INSERT INTO preferences (content) VALUES (?)", (content,)
        )
        return cur.lastrowid
    except Exception:
        return None


def _word_overlap(a, b):
    """Jaccard similarity on words."""
    wa = set(a.lower().split())
    wb = set(b.lower().split())
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / len(wa | wb)


# --------------- CLI ---------------

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: reflect.py <transcript.jsonl> [session_id] [workspace_id]")
        print("  Deep reflection on a session transcript.")
        print("  Extracts rules, anti-patterns, preferences, writes diary entry.")
        sys.exit(1)

    transcript = sys.argv[1]
    sid = sys.argv[2] if len(sys.argv) > 2 else None
    wid = sys.argv[3] if len(sys.argv) > 3 else None

    result = reflect_on_session(transcript, sid, wid)
    print(json.dumps(result, indent=2))
