#!/usr/bin/env python3
"""Capy Cortex - Bootstrap Script (the awakening).
Mines all historical session transcripts for day-one knowledge.

Aristotelian Axioms:
  A1: Historical sessions contain accumulated wisdom
  A2: Processing must be incremental (resumable if interrupted)
  A3: Rate-limiting prevents database lock contention
  A4: Bootstrap is a one-time operation (idempotent via diary check)
  A5: Progress must be visible (printed to stdout)
  A6: Memory-safe (process one transcript at a time, don't load all)

Pipeline:
  1. Discover all .jsonl transcript files
  2. Filter out subagent transcripts (noise)
  3. Process each through reflect.py
  4. Run consolidation after all sessions
  5. Retrain TF-IDF model
  6. Print summary
"""

import json
import sys
import os
import time
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "cortex.db"
SCRIPTS_DIR = Path(__file__).parent
PROJECTS_DIR = Path.home() / ".claude" / "projects"

# Bootstrap safety limits
MAX_SESSIONS = 10000       # Safety cap
BATCH_COMMIT_SIZE = 50     # Commit to DB every N sessions
PROGRESS_INTERVAL = 25     # Print progress every N sessions


def get_db():
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA busy_timeout=5000")
    return db


def discover_transcripts():
    """Find all main session transcripts (not subagent ones)."""
    transcripts = []
    if not PROJECTS_DIR.exists():
        return transcripts

    for workspace_dir in PROJECTS_DIR.iterdir():
        if not workspace_dir.is_dir():
            continue
        workspace_id = workspace_dir.name

        # Main session files are directly in workspace dir
        for jsonl in workspace_dir.glob("*.jsonl"):
            transcripts.append({
                "path": str(jsonl),
                "session_id": jsonl.stem,
                "workspace_id": workspace_id,
                "size": jsonl.stat().st_size,
            })

        # Also check session subdirectories (but skip subagents/)
        for session_dir in workspace_dir.iterdir():
            if not session_dir.is_dir():
                continue
            if session_dir.name == "subagents":
                continue
            for jsonl in session_dir.glob("*.jsonl"):
                if "subagent" not in str(jsonl):
                    transcripts.append({
                        "path": str(jsonl),
                        "session_id": jsonl.stem,
                        "workspace_id": workspace_id,
                        "size": jsonl.stat().st_size,
                    })

    # Sort by size descending (bigger sessions = more knowledge)
    transcripts.sort(key=lambda x: x["size"], reverse=True)
    return transcripts[:MAX_SESSIONS]


def get_already_reflected(db):
    """Get set of session_ids already reflected on."""
    rows = db.execute("SELECT session_id FROM diary WHERE session_id IS NOT NULL").fetchall()
    return {r["session_id"] for r in rows}


def bootstrap(limit=None, skip_consolidation=False):
    """Run full bootstrap pipeline."""
    if not DB_PATH.exists():
        print("[ERROR] cortex.db not found. Run setup.py first.")
        return

    # Import reflect module
    sys.path.insert(0, str(SCRIPTS_DIR))
    from reflect import reflect_on_session

    print("[1/5] Discovering transcripts...")
    transcripts = discover_transcripts()
    print(f"  Found {len(transcripts)} session transcripts")

    if limit:
        transcripts = transcripts[:limit]
        print(f"  Limited to {limit} sessions")

    print("[2/5] Checking already-processed sessions...")
    db = get_db()
    already_done = get_already_reflected(db)
    db.close()

    to_process = [t for t in transcripts if t["session_id"] not in already_done]
    print(f"  Already reflected: {len(already_done)}")
    print(f"  To process: {len(to_process)}")

    if not to_process:
        print("[DONE] No new sessions to process.")
        if not skip_consolidation:
            _run_consolidation()
        return

    print(f"[3/5] Reflecting on {len(to_process)} sessions...")
    stats = {
        "processed": 0,
        "skipped": 0,
        "errors": 0,
        "total_rules": 0,
        "total_anti_patterns": 0,
        "total_preferences": 0,
    }

    start_time = time.time()

    for i, t in enumerate(to_process):
        try:
            result = reflect_on_session(
                t["path"], t["session_id"], t["workspace_id"]
            )

            if result.get("skipped"):
                stats["skipped"] += 1
            elif result.get("error"):
                stats["errors"] += 1
            else:
                stats["processed"] += 1
                stats["total_rules"] += result.get("rules_added", 0)
                stats["total_anti_patterns"] += result.get("anti_patterns_added", 0)
                stats["total_preferences"] += result.get("preferences_added", 0)

        except Exception as e:
            stats["errors"] += 1

        # Progress report
        if (i + 1) % PROGRESS_INTERVAL == 0:
            elapsed = time.time() - start_time
            rate = (i + 1) / elapsed if elapsed > 0 else 0
            remaining = (len(to_process) - i - 1) / rate if rate > 0 else 0
            print(f"  [{i+1}/{len(to_process)}] "
                  f"processed={stats['processed']} rules={stats['total_rules']} "
                  f"({rate:.1f}/s, ~{remaining:.0f}s remaining)")

    elapsed = time.time() - start_time
    print(f"  Completed in {elapsed:.1f}s")

    print(f"[4/5] Bootstrap results:")
    print(f"  Processed: {stats['processed']}")
    print(f"  Skipped: {stats['skipped']}")
    print(f"  Errors: {stats['errors']}")
    print(f"  Rules extracted: {stats['total_rules']}")
    print(f"  Anti-patterns: {stats['total_anti_patterns']}")
    print(f"  Preferences: {stats['total_preferences']}")

    if not skip_consolidation:
        _run_consolidation()
    else:
        print("[5/5] Consolidation skipped (--no-consolidate)")

    # Final stats
    db = get_db()
    total_rules = db.execute("SELECT COUNT(*) FROM rules").fetchone()[0]
    total_principles = db.execute("SELECT COUNT(*) FROM principles").fetchone()[0]
    total_ap = db.execute("SELECT COUNT(*) FROM anti_patterns").fetchone()[0]
    total_prefs = db.execute("SELECT COUNT(*) FROM preferences").fetchone()[0]
    total_diary = db.execute("SELECT COUNT(*) FROM diary").fetchone()[0]
    db.close()

    print(f"\n[FINAL] Cortex database stats:")
    print(f"  Rules: {total_rules}")
    print(f"  Principles: {total_principles}")
    print(f"  Anti-patterns: {total_ap}")
    print(f"  Preferences: {total_prefs}")
    print(f"  Diary entries: {total_diary}")
    print(f"\n[DONE] Capy Cortex is awake.")


def _run_consolidation():
    """Run consolidation and TF-IDF retraining."""
    print("[5/5] Running consolidation (clustering + TF-IDF)...")
    try:
        from consolidate import consolidate
        result = consolidate()
        if result.get("error"):
            print(f"  Consolidation error: {result['error']}")
        elif result.get("skipped"):
            print(f"  Consolidation skipped: {result['reason']}")
        else:
            print(f"  Clusters found: {result.get('clusters_found', 0)}")
            print(f"  Principles created: {result.get('principles_created', 0)}")
            print(f"  Rules promoted: {result.get('rules_promoted', 0)}")
    except Exception as e:
        print(f"  Consolidation failed: {e}")

    # Ensure TF-IDF is trained
    try:
        from cortex import retrain_tfidf
        ok = retrain_tfidf()
        print(f"  TF-IDF retrain: {'OK' if ok else 'SKIPPED'}")
    except Exception as e:
        print(f"  TF-IDF retrain failed: {e}")


# --------------- CLI ---------------

if __name__ == "__main__":
    limit = None
    skip_consolidation = False

    for arg in sys.argv[1:]:
        if arg.startswith("--limit="):
            limit = int(arg.split("=")[1])
        elif arg == "--no-consolidate":
            skip_consolidation = True
        elif arg == "--discover-only":
            transcripts = discover_transcripts()
            print(f"Found {len(transcripts)} transcripts")
            for t in transcripts[:10]:
                size_kb = t["size"] / 1024
                print(f"  [{size_kb:.0f}KB] {t['session_id'][:12]}... ({t['workspace_id'][:30]}...)")
            if len(transcripts) > 10:
                print(f"  ... and {len(transcripts) - 10} more")
            total_mb = sum(t["size"] for t in transcripts) / (1024 * 1024)
            print(f"Total: {total_mb:.1f}MB across {len(transcripts)} sessions")
            sys.exit(0)
        elif arg == "--help":
            print("Usage: bootstrap.py [options]")
            print("  --limit=N           Process only N sessions")
            print("  --no-consolidate    Skip consolidation step")
            print("  --discover-only     Just count transcripts, don't process")
            print("  --help              Show this help")
            sys.exit(0)

    bootstrap(limit=limit, skip_consolidation=skip_consolidation)
