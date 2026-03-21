#!/usr/bin/env python3
"""Capy Cortex - Database initialization. Creates SQLite schema with FTS5."""

import sqlite3
import os
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "cortex.db"

SCHEMA = """
PRAGMA journal_mode=WAL;
PRAGMA busy_timeout=5000;

CREATE TABLE IF NOT EXISTS rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    category TEXT NOT NULL DEFAULT 'general',
    confidence REAL DEFAULT 0.5,
    occurrences INTEGER DEFAULT 1,
    maturity TEXT DEFAULT 'candidate',
    harmful_count INTEGER DEFAULT 0,
    helpful_count INTEGER DEFAULT 0,
    source_session TEXT,
    source_workspace TEXT,
    evidence TEXT DEFAULT '[]',
    created_at TEXT DEFAULT (datetime('now')),
    last_seen TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS principles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    source_rule_ids TEXT DEFAULT '[]',
    confidence REAL DEFAULT 0.8,
    occurrences INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS anti_patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    severity TEXT DEFAULT 'high',
    source_event TEXT,
    confidence REAL DEFAULT 1.0,
    occurrences INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now')),
    last_seen TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    confidence REAL DEFAULT 0.6,
    occurrences INTEGER DEFAULT 1,
    created_at TEXT DEFAULT (datetime('now')),
    last_seen TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS diary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    workspace_id TEXT,
    summary TEXT,
    mistakes TEXT DEFAULT '[]',
    successes TEXT DEFAULT '[]',
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_type TEXT NOT NULL,
    rule_id INTEGER,
    metadata TEXT DEFAULT '{}',
    created_at TEXT DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS meta (
    key TEXT PRIMARY KEY,
    value TEXT,
    updated_at TEXT DEFAULT (datetime('now'))
);
"""

FTS_SETUP = """
CREATE VIRTUAL TABLE IF NOT EXISTS rules_fts USING fts5(
    content, category,
    content='rules', content_rowid='id',
    tokenize='porter unicode61'
);

CREATE TRIGGER IF NOT EXISTS rules_ai AFTER INSERT ON rules BEGIN
    INSERT INTO rules_fts(rowid, content, category)
    VALUES (new.id, new.content, new.category);
END;

CREATE TRIGGER IF NOT EXISTS rules_ad AFTER DELETE ON rules BEGIN
    INSERT INTO rules_fts(rules_fts, rowid, content, category)
    VALUES ('delete', old.id, old.content, old.category);
END;

CREATE TRIGGER IF NOT EXISTS rules_au AFTER UPDATE ON rules BEGIN
    INSERT INTO rules_fts(rules_fts, rowid, content, category)
    VALUES ('delete', old.id, old.content, old.category);
    INSERT INTO rules_fts(rowid, content, category)
    VALUES (new.id, new.content, new.category);
END;
"""


def init_db():
    db = sqlite3.connect(str(DB_PATH))
    db.executescript(SCHEMA)
    db.executescript(FTS_SETUP)
    db.execute("INSERT OR IGNORE INTO meta (key, value) VALUES ('version', '1.0.0')")
    db.execute("INSERT OR IGNORE INTO meta (key, value) VALUES ('tfidf_dirty', '1')")
    db.commit()
    db.close()
    os.chmod(str(DB_PATH), 0o600)
    return DB_PATH


if __name__ == "__main__":
    path = init_db()
    db = sqlite3.connect(str(path))
    tables = db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    print(f"[OK] Database created at {path}")
    print(f"[OK] Tables: {', '.join(t[0] for t in tables)}")
    fts = db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='rules_fts'").fetchone()
    print(f"[OK] FTS5 index: {'ACTIVE' if fts else 'FAILED'}")
    db.close()
