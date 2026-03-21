---
name: capy-cortex
description: "Autonomous learning system - learns from mistakes, reflects on sessions, and gets smarter over time. The AI brain."
---

# Capy Cortex - Autonomous Learning System

You have a persistent learning brain powered by SQLite + FTS5 + sklearn TF-IDF.
Knowledge is automatically loaded via hooks. This file describes manual operations.

## Architecture

- **Database**: `~/.claude/skills/capy-cortex/cortex.db` (SQLite + FTS5 + WAL)
- **Hooks** (automatic, never call manually):
  - SessionStart: Loads anti-patterns, preferences, principles
  - UserPromptSubmit: Retrieves task-relevant rules via FTS5
  - PreToolUse(Bash): Blocks known dangerous commands
  - PostToolUseFailure: Records errors as anti-patterns
  - Stop: Extracts corrections and preferences from conversation
- **Scripts** (for manual/scheduled use):
  - `cortex.py`: Core engine (retrieve, add rules, stats)
  - `reflect.py`: Deep session analysis
  - `consolidate.py`: Cluster rules into principles (sklearn)
  - `bootstrap.py`: Mine historical sessions

## Manual Commands

```bash
# Check system health
python3 ~/.claude/skills/capy-cortex/scripts/cortex.py stats

# Retrieve rules for a topic
python3 ~/.claude/skills/capy-cortex/scripts/cortex.py retrieve "react typescript"

# Add a rule manually
python3 ~/.claude/skills/capy-cortex/scripts/cortex.py add-rule "Always use TypeScript strict mode" "best_practice"

# Add an anti-pattern
python3 ~/.claude/skills/capy-cortex/scripts/cortex.py add-ap "Never force push to main" "critical"

# Add a preference
python3 ~/.claude/skills/capy-cortex/scripts/cortex.py add-pref "User prefers functional components over class components"

# Run consolidation (clusters rules into principles)
python3 ~/.claude/skills/capy-cortex/scripts/consolidate.py

# Retrain TF-IDF model
python3 ~/.claude/skills/capy-cortex/scripts/cortex.py retrain

# Apply confidence decay
python3 ~/.claude/skills/capy-cortex/scripts/cortex.py decay
```

## How It Learns

1. **Automatic** (via hooks): Errors are captured, corrections noted, preferences extracted
2. **Reflection**: Deep analysis of session transcripts extracts patterns
3. **Consolidation**: sklearn clustering groups similar rules into principles
4. **Decay**: Old, unreinforced rules fade; validated rules strengthen
5. **Retrieval**: Two-stage FTS5 + TF-IDF returns only relevant knowledge (O(1) context)
