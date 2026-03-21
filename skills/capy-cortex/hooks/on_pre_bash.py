#!/usr/bin/env python3
"""Capy Cortex Hook: PreToolUse (Bash) - The guardian.
Checks bash commands against known anti-patterns. Can BLOCK dangerous commands.
Must be fast (<50ms) -- simple string matching only."""

import json
import sys
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "cortex.db"


def main():
    try:
        data = json.loads(sys.stdin.read())
    except Exception:
        return

    if not DB_PATH.exists():
        return

    tool_input = data.get("tool_input", {})
    command = tool_input.get("command", "")
    if not command:
        return

    try:
        db = sqlite3.connect(str(DB_PATH))
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA journal_mode=WAL")
        db.execute("PRAGMA busy_timeout=2000")

        # Check anti-patterns for command matches
        anti_patterns = db.execute(
            "SELECT content, severity FROM anti_patterns ORDER BY severity DESC"
        ).fetchall()

        cmd_lower = command.lower()
        for ap in anti_patterns:
            ap_content = ap["content"].lower()
            # Extract key phrases from anti-pattern to match against command
            # Look for repo names, file paths, dangerous patterns
            if _matches_command(cmd_lower, ap_content):
                db.close()
                output = {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": (
                            f"CORTEX GUARDIAN: Blocked by anti-pattern - "
                            f"{ap['content']}"
                        ),
                        "additionalContext": (
                            f"WARNING: This command was blocked by Capy Cortex. "
                            f"Anti-pattern [{ap['severity'].upper()}]: {ap['content']}. "
                            f"Please find an alternative approach."
                        )
                    }
                }
                print(json.dumps(output))
                return

        db.close()

    except Exception:
        pass  # Hooks must NEVER crash


def _matches_command(cmd, anti_pattern):
    """Check if a command matches an anti-pattern. Conservative matching.

    Path-aware: distinguishes between a keyword being the TARGET of a command
    vs merely appearing in a file path being read/accessed. Reading a file
    whose path contains a keyword should NOT trigger a block.
    """
    # Extract identifiers from anti-pattern (repo names, paths, etc.)
    keywords = []
    for word in anti_pattern.split():
        word = word.strip(".,;:!?'\"()-")
        if "/" in word and len(word) > 5:
            keywords.append(word)
        elif word.startswith("--") and len(word) > 3:
            keywords.append(word)
        elif "." in word and len(word) > 4:
            keywords.append(word)

    if not keywords:
        return False

    # Read-only commands that should never be blocked
    read_only_prefixes = (
        "cat ", "head ", "tail ", "less ", "more ", "wc ",
        "file ", "stat ", "ls ", "find ", "grep ", "rg ",
        "diff ", "md5sum ", "sha256sum ", "du ",
    )
    cmd_stripped = cmd.lstrip()
    is_read_only = cmd_stripped.startswith(read_only_prefixes)

    for kw in keywords:
        if kw not in cmd:
            continue

        # If this is a read-only command, the keyword is just a path argument -- skip
        if is_read_only:
            continue

        # Check if keyword appears as a write target vs just a path reference
        # e.g. "git push ndpvt-web/capy-bridge" should block
        # but "cat ~/.claude/skills/cm/SKILL.md" should not
        # Heuristic: if keyword is preceded by a path separator deeper than 2 levels,
        # it's likely a file being accessed, not the target of a dangerous action
        idx = cmd.find(kw)
        prefix = cmd[:idx]
        # Count path depth before the keyword
        if prefix.count("/") >= 2 and not any(
            dangerous in cmd_stripped[:20]
            for dangerous in ("rm ", "git push", "git force", "mv ", "cp ", "write ", "echo ")
        ):
            continue

        return True
    return False


if __name__ == "__main__":
    main()
