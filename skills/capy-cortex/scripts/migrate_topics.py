#!/usr/bin/env python3
"""Phase 4A: Add topic tables to cortex.db schema."""
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "cortex.db"

PREDEFINED_TOPICS = [
    ("universal", "Rules that apply to all contexts"),
    ("git", "Git version control operations"),
    ("npm", "Node.js package management"),
    ("python", "Python development"),
    ("docker", "Containerization and Docker"),
    ("react", "React/Next.js frontend development"),
    ("api", "API design and HTTP requests"),
    ("database", "Database operations and SQL"),
    ("testing", "Testing and quality assurance"),
    ("build", "Build tools and bundling"),
    ("deployment", "CI/CD and deployment"),
    ("browser-automation", "Browser automation and scraping"),
    ("video-generation", "Video creation and processing"),
    ("skill-creation", "Claude Code skill development"),
    ("security", "Security and authentication"),
    ("instagram", "Instagram and social media"),
    ("email", "Email sending and management"),
    ("audio", "Audio, TTS, and voice"),
]


def migrate():
    db = sqlite3.connect(str(DB_PATH))
    db.execute("PRAGMA journal_mode=WAL")

    # Create topics table
    db.execute("""
        CREATE TABLE IF NOT EXISTS topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT,
            rule_count INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)

    # Create rule_topics junction table
    db.execute("""
        CREATE TABLE IF NOT EXISTS rule_topics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            rule_id INTEGER NOT NULL REFERENCES rules(id) ON DELETE CASCADE,
            topic_id INTEGER NOT NULL REFERENCES topics(id),
            weight REAL DEFAULT 1.0,
            created_at TEXT DEFAULT (datetime('now')),
            UNIQUE(rule_id, topic_id)
        )
    """)

    # Create indexes
    db.execute("CREATE INDEX IF NOT EXISTS idx_rule_topics_rule ON rule_topics(rule_id)")
    db.execute("CREATE INDEX IF NOT EXISTS idx_rule_topics_topic ON rule_topics(topic_id)")

    # Seed predefined topics
    for name, description in PREDEFINED_TOPICS:
        db.execute(
            "INSERT OR IGNORE INTO topics (name, description) VALUES (?, ?)",
            (name, description),
        )

    db.commit()

    # Verify
    count = db.execute("SELECT COUNT(*) FROM topics").fetchone()[0]
    print(f"Topics table ready: {count} topics seeded")

    db.close()
    return count


if __name__ == "__main__":
    n = migrate()
    print(f"Schema migration complete. {n} topics available.")
