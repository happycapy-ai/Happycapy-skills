#!/usr/bin/env python3
"""Phase 4C: Classify all existing rules into topics using topic_engine."""
import sqlite3
from pathlib import Path
from topic_engine import detect_topic_for_rule

DB_PATH = Path(__file__).parent.parent / "cortex.db"


def classify():
    db = sqlite3.connect(str(DB_PATH))
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA busy_timeout=3000")

    # Get all rules
    rules = db.execute("SELECT id, content, category FROM rules").fetchall()
    print(f"Classifying {len(rules)} rules into topics...")

    # Get topic name -> id map
    topics = db.execute("SELECT id, name FROM topics").fetchall()
    topic_map = {name: tid for tid, name in topics}

    assigned = 0
    for rule_id, content, category in rules:
        # Check if already assigned
        existing = db.execute(
            "SELECT 1 FROM rule_topics WHERE rule_id = ? LIMIT 1", (rule_id,)
        ).fetchone()
        if existing:
            continue

        topic_name = detect_topic_for_rule(content or "", category or "")
        topic_id = topic_map.get(topic_name)
        if not topic_id:
            topic_id = topic_map.get("universal")

        if topic_id:
            db.execute(
                "INSERT OR IGNORE INTO rule_topics (rule_id, topic_id) VALUES (?, ?)",
                (rule_id, topic_id)
            )
            assigned += 1

    # Update rule_count for all topics
    db.execute("""
        UPDATE topics SET rule_count = (
            SELECT COUNT(*) FROM rule_topics WHERE rule_topics.topic_id = topics.id
        )
    """)

    db.commit()

    # Report
    print(f"Assigned {assigned} rules to topics")
    results = db.execute(
        "SELECT t.name, t.rule_count FROM topics t WHERE rule_count > 0 ORDER BY rule_count DESC"
    ).fetchall()
    for name, count in results:
        print(f"  {name}: {count} rules")

    db.close()
    return assigned


if __name__ == "__main__":
    classify()
