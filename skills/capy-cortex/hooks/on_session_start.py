#!/usr/bin/env python3
"""Capy Cortex Hook: SessionStart - Morning briefing.
Injects top anti-patterns, preferences, and principles into every new session.
Runs ONCE per session start. Must be fast (<200ms)."""

import json
import sys
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / "cortex.db"


def is_noise_content(content):
    """Filter out garbage content that shouldn't be injected."""
    if not content or len(content) > 300:
        return True

    noise_substrings = [
        "session is being continued",
        "Base directory for this skill",
    ]

    content_lower = content.lower()
    for noise in noise_substrings:
        if noise.lower() in content_lower:
            return True

    # Skip HTML/XML tags
    if content.strip().startswith("<"):
        return True

    return False


def main():
    try:
        data = json.loads(sys.stdin.read())
    except Exception:
        data = {}

    if not DB_PATH.exists():
        return

    try:
        db = sqlite3.connect(str(DB_PATH))
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA journal_mode=WAL")
        db.execute("PRAGMA busy_timeout=3000")

        # Get anti-patterns with quality filter
        all_anti_patterns = db.execute(
            "SELECT content, severity, confidence FROM anti_patterns "
            "WHERE confidence >= 0.6 "
            "ORDER BY severity DESC, confidence DESC LIMIT 20"
        ).fetchall()

        anti_patterns = [
            ap for ap in all_anti_patterns
            if not is_noise_content(ap['content'])
        ][:5]  # Max 5 after filtering

        # Get preferences with quality filter
        all_prefs = db.execute(
            "SELECT content, confidence FROM preferences "
            "WHERE confidence >= 0.6 "
            "ORDER BY confidence DESC, occurrences DESC LIMIT 10"
        ).fetchall()

        prefs = [
            p for p in all_prefs
            if not is_noise_content(p['content'])
        ][:3]  # Max 3 after filtering

        # Get principles with quality filter
        all_principles = db.execute(
            "SELECT content, confidence FROM principles "
            "WHERE confidence >= 0.6 "
            "ORDER BY confidence DESC LIMIT 15"
        ).fetchall()

        principles = [
            p for p in all_principles
            if not is_noise_content(p['content'])
        ][:5]  # Max 5 after filtering

        # Get metadata for header
        rule_count = db.execute(
            "SELECT COUNT(*) FROM rules WHERE maturity != 'deprecated'"
        ).fetchone()[0]

        last_maintenance = db.execute(
            "SELECT value FROM meta WHERE key = 'last_maintenance'"
        ).fetchone()

        maintenance_date = "unknown"
        if last_maintenance and last_maintenance['value']:
            try:
                dt = datetime.fromisoformat(last_maintenance['value'])
                maintenance_date = dt.strftime("%Y-%m-%d")
            except Exception:
                pass

        # Phase 4E: Detect topics from workspace path
        detected_topics = []
        cwd = data.get("cwd", "")
        try:
            import importlib.util
            te_path = str(Path(__file__).parent.parent / "scripts" / "topic_engine.py")
            spec = importlib.util.spec_from_file_location("topic_engine", te_path)
            te = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(te)
            detected_topics = te.detect_topics_fast(cwd, file_paths=[cwd])
        except Exception:
            pass

        # Log session start event with detected topics
        db.execute(
            "INSERT INTO events (event_type, metadata) VALUES (?, ?)",
            ("session_start", json.dumps({
                "session_id": data.get("session_id", ""),
                "cwd": cwd,
                "detected_topics": detected_topics,
            }))
        )
        db.commit()
        db.close()

        lines = []
        if anti_patterns or prefs or principles:
            lines.append("## Cortex v3: Knowledge")
            lines.append(f"({rule_count} rules, last maintained: {maintenance_date})\n")

        if anti_patterns:
            lines.append("### NEVER DO (learned from past mistakes)")
            for ap in anti_patterns:
                lines.append(f"- [{ap['severity'].upper()}] {ap['content']}")
            lines.append("")

        if prefs:
            lines.append("### User Preferences")
            for p in prefs:
                lines.append(f"- {p['content']}")
            lines.append("")

        if principles:
            lines.append("### Principles (distilled from experience)")
            for p in principles:
                lines.append(f"- {p['content']}")
            lines.append("")

        if lines:
            context = "\n".join(lines)
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": context
                }
            }
            print(json.dumps(output))

    except Exception:
        pass  # Hooks must NEVER crash


if __name__ == "__main__":
    main()
