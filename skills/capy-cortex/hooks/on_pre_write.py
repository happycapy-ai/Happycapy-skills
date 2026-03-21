#!/usr/bin/env python3
"""Capy Cortex Hook: PreToolUse (Write) - Atomic Write Guardian.
Warns when Write tool content exceeds safe thresholds.
Must be fast (<50ms) -- simple line counting only."""

import json
import sys


# Thresholds derived from Aristotelian analysis of Write tool limits
WARN_LINE_THRESHOLD = 300
BLOCK_LINE_THRESHOLD = 600
WARN_CHAR_THRESHOLD = 25000  # ~8K tokens
BLOCK_CHAR_THRESHOLD = 50000  # ~16K tokens


def main():
    try:
        data = json.loads(sys.stdin.read())
    except Exception:
        return

    tool_input = data.get("tool_input", {})
    content = tool_input.get("content", "")
    file_path = tool_input.get("file_path", "")

    if not content:
        return

    line_count = content.count("\n") + 1
    char_count = len(content)

    # BLOCK: Hard limit -- files this large will almost certainly stall
    if line_count > BLOCK_LINE_THRESHOLD or char_count > BLOCK_CHAR_THRESHOLD:
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": (
                    f"ATOMIC WRITE GUARD: Blocked Write of {line_count} lines "
                    f"({char_count} chars) to {file_path}. "
                    f"Files over {BLOCK_LINE_THRESHOLD} lines WILL stall the agent. "
                    f"Use Scaffold-Then-Fill: Write a skeleton (<150 lines), "
                    f"then use Edit tool to fill each section (<200 lines per Edit). "
                    f"Or decompose into multiple smaller files."
                ),
                "additionalContext": (
                    f"BLOCKED: Write tool call with {line_count} lines / {char_count} chars "
                    f"exceeds safe limit ({BLOCK_LINE_THRESHOLD} lines / {BLOCK_CHAR_THRESHOLD} chars). "
                    f"This WILL cause a silent stall. Break into smaller writes."
                )
            }
        }
        print(json.dumps(output))
        return

    # WARN: Soft limit -- approaching dangerous territory
    if line_count > WARN_LINE_THRESHOLD or char_count > WARN_CHAR_THRESHOLD:
        output = {
            "hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "allow",
                "additionalContext": (
                    f"WARNING: Writing {line_count} lines ({char_count} chars) to {file_path}. "
                    f"This is approaching the safe limit ({WARN_LINE_THRESHOLD} lines). "
                    f"Consider using Scaffold-Then-Fill pattern for reliability. "
                    f"If this write stalls, decompose into smaller files next attempt."
                )
            }
        }
        print(json.dumps(output))
        return


if __name__ == "__main__":
    main()
