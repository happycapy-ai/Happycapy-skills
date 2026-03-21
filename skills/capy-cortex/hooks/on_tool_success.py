#!/usr/bin/env python3
"""Capy Cortex Hook: PostToolUse - Success credit.
When tools succeed, credit recently surfaced rules to close the feedback loop.
This is the MISSING PIECE that makes Cortex actually learn from success."""

import json
import sys
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "cortex.db"

# Tools where success is meaningful (skip Read, Glob, Grep - they always "succeed")
CREDIT_TOOLS = {"Bash", "Write", "Edit", "NotebookEdit"}

# Skip tools that are internal/meta
SKIP_TOOLS = {"TaskOutput", "TodoWrite", "SendMessage", "AskUserQuestion"}

# Confidence boost per successful credit (small, accumulates over time)
CONFIDENCE_BOOST = 0.02
MAX_CONFIDENCE = 0.95


def is_success(tool_name, tool_response):
    """Determine if a tool response indicates success."""
    if not tool_response:
        return False

    response_str = str(tool_response)

    # Bash: check for error indicators
    if tool_name == "Bash":
        # Explicit failure indicators
        fail_indicators = [
            "Exit code", "Error:", "error:", "ENOENT", "EACCES",
            "Permission denied", "command not found", "No such file",
            "npm ERR", "ModuleNotFoundError", "SyntaxError",
            "TypeError", "ReferenceError", "fatal:",
        ]
        for indicator in fail_indicators:
            if indicator in response_str:
                return False
        return True

    # Write/Edit: success if no error
    if tool_name in ("Write", "Edit", "NotebookEdit"):
        if "error" in response_str.lower() or "failed" in response_str.lower():
            return False
        return True

    return True


def main():
    try:
        data = json.loads(sys.stdin.read())
    except Exception:
        return

    if not DB_PATH.exists():
        return

    try:
        tool_name = data.get("tool_name", "unknown")
        tool_response = str(data.get("tool_response", ""))
        session_id = data.get("session_id", "")

        # Skip non-meaningful tools
        if tool_name in SKIP_TOOLS:
            return
        if tool_name not in CREDIT_TOOLS:
            return

        # Only credit on success
        if not is_success(tool_name, tool_response):
            return

        db = sqlite3.connect(str(DB_PATH))
        db.execute("PRAGMA journal_mode=WAL")
        db.execute("PRAGMA busy_timeout=2000")

        # Find recently surfaced rules for this session (not yet credited)
        surfaced = db.execute("""
            SELECT id, rule_id FROM surfaced_rules
            WHERE session_id = ? AND credited = 0
            ORDER BY surfaced_at DESC LIMIT 10
        """, (session_id,)).fetchall()

        if not surfaced:
            db.close()
            return

        credited_count = 0
        for surf_id, rule_id in surfaced:
            # Increment helpful_count and boost confidence
            db.execute("""
                UPDATE rules SET
                    helpful_count = helpful_count + 1,
                    confidence = MIN(confidence + ?, ?),
                    last_seen = datetime('now')
                WHERE id = ? AND maturity != 'deprecated'
            """, (CONFIDENCE_BOOST, MAX_CONFIDENCE, rule_id))

            # Mark as credited so we don't double-count
            db.execute(
                "UPDATE surfaced_rules SET credited = 1 WHERE id = ?",
                (surf_id,)
            )
            credited_count += 1

        if credited_count > 0:
            # Log the credit event
            db.execute(
                "INSERT INTO events (event_type, metadata) VALUES (?, ?)",
                ("success_credit", json.dumps({
                    "session_id": session_id,
                    "tool": tool_name,
                    "rules_credited": credited_count,
                }))
            )

        db.commit()
        db.close()

    except Exception:
        pass  # Hooks must NEVER crash


if __name__ == "__main__":
    main()
