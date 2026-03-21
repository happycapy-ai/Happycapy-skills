#!/usr/bin/env python3
"""Capy Cortex - Forge Bridge.
Bidirectional integration between Cortex learning DB and Forge multi-agent orchestrator.

Bridge 3 (Forge -> Cortex): Log Forge execution outcomes as learning events.
Bridge 4 (Cortex -> Forge): Surface anti-patterns and rules for Forge contracts."""

import json
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / "cortex.db"
FORGE_DIR = Path.home() / ".claude/skills/forge"


def get_db():
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA busy_timeout=3000")
    return db


# ---- Bridge 3: Forge -> Cortex ----

def ingest_forge_outcome(forge_status_path=None, workspace=None):
    """Ingest Forge execution outcome into Cortex as learning events.
    Reads forge-status.json to extract success/failure patterns.
    Returns dict with counts of items ingested."""
    # Find forge status file
    if forge_status_path:
        status_path = Path(forge_status_path)
    elif workspace:
        status_path = Path(workspace) / "forge-status.json"
    else:
        return {"error": "No forge status path or workspace provided"}

    if not status_path.exists():
        return {"skipped": "No forge-status.json found"}

    try:
        status = json.loads(status_path.read_text())
    except (json.JSONDecodeError, IOError):
        return {"error": "Could not read forge-status.json"}

    db = get_db()
    rules_added = 0
    anti_patterns_added = 0

    # Extract agent outcomes
    agents = status.get("agents", [])
    for agent in agents:
        agent_status = agent.get("status", "")
        agent_role = agent.get("role", "unknown")
        agent_errors = agent.get("errors", [])

        # Failed agents -> extract anti-patterns
        if agent_status == "failed" and agent_errors:
            for error in agent_errors[:3]:  # Cap at 3 per agent
                error_text = str(error)[:300]
                content = f"Forge agent '{agent_role}' failed: {error_text}"

                # Check if similar anti-pattern exists
                existing = db.execute(
                    "SELECT id FROM anti_patterns WHERE content = ?", (content,)
                ).fetchone()
                if existing:
                    db.execute("""
                        UPDATE anti_patterns SET occurrences = occurrences + 1,
                        last_seen = datetime('now') WHERE id = ?
                    """, (existing[0],))
                else:
                    db.execute("""
                        INSERT INTO anti_patterns (content, severity, source_event)
                        VALUES (?, ?, ?)
                    """, (content, "medium", f"forge:{agent_role}"))
                    anti_patterns_added += 1

    # Extract contract validation results
    validation = status.get("validation", {})
    validation_failures = validation.get("failures", [])

    for failure in validation_failures[:5]:  # Cap
        content = f"Forge contract violation: {str(failure)[:200]}"
        existing = db.execute(
            "SELECT id FROM rules WHERE content = ?", (content,)
        ).fetchone()
        if not existing:
            db.execute("""
                INSERT INTO rules (content, category, confidence, source_workspace)
                VALUES (?, ?, ?, ?)
            """, (content, "forge_validation", 0.6, workspace))
            rules_added += 1

    # Extract successful patterns
    mode = status.get("mode", "unknown")
    coupling_score = status.get("coupling_score", 0)
    overall_status = status.get("status", "unknown")

    if overall_status == "completed":
        pattern = f"Forge '{mode}' mode succeeded (coupling={coupling_score:.2f})"
        existing = db.execute(
            "SELECT id FROM rules WHERE content = ?", (pattern,)
        ).fetchone()
        if existing:
            db.execute("""
                UPDATE rules SET occurrences = occurrences + 1,
                confidence = MIN(confidence + 0.1, 1.0),
                last_seen = datetime('now') WHERE id = ?
            """, (existing[0],))
        else:
            db.execute("""
                INSERT INTO rules (content, category, confidence, source_workspace)
                VALUES (?, ?, ?, ?)
            """, (pattern, "forge_pattern", 0.6, workspace))
            rules_added += 1

    # Record bridge event
    result = {
        "rules_added": rules_added,
        "anti_patterns_added": anti_patterns_added,
        "forge_mode": mode,
        "forge_status": overall_status,
    }
    db.execute(
        "INSERT INTO events (event_type, metadata) VALUES (?, ?)",
        ("bridge_forge_ingest", json.dumps(result))
    )
    db.commit()
    db.close()
    return result


# ---- Bridge 4: Cortex -> Forge ----

def get_forge_context(workspace=None, task_description=None):
    """Generate Cortex context for Forge contract generation.
    Returns relevant anti-patterns, rules, and principles for the task."""
    db = get_db()

    # Get all anti-patterns (these are critical for any Forge execution)
    anti_patterns = db.execute("""
        SELECT content, severity, confidence FROM anti_patterns
        WHERE confidence >= 0.5
        ORDER BY severity DESC, confidence DESC
        LIMIT 10
    """).fetchall()

    # Get workspace-specific rules
    workspace_rules = []
    if workspace:
        workspace_rules = db.execute("""
            SELECT content, category, confidence FROM rules
            WHERE source_workspace = ? AND maturity != 'deprecated'
            AND confidence >= 0.5
            ORDER BY confidence DESC LIMIT 10
        """, (workspace,)).fetchall()

    # Get task-relevant rules via FTS5
    task_rules = []
    if task_description:
        words = [w for w in task_description.split() if len(w) > 2 and w.isalnum()][:8]
        if words:
            query = " OR ".join(words)
            try:
                task_rules = db.execute("""
                    SELECT r.content, r.category, r.confidence
                    FROM rules_fts JOIN rules r ON rules_fts.rowid = r.id
                    WHERE rules_fts MATCH ? AND r.maturity != 'deprecated'
                    AND r.confidence >= 0.5
                    ORDER BY rank LIMIT 10
                """, (query,)).fetchall()
            except Exception:
                pass

    # Get forge-specific rules
    forge_rules = db.execute("""
        SELECT content, category, confidence FROM rules
        WHERE category LIKE 'forge_%' AND maturity != 'deprecated'
        ORDER BY confidence DESC LIMIT 5
    """).fetchall()

    # Get principles
    principles = db.execute("""
        SELECT content, confidence FROM principles
        WHERE confidence >= 0.7
        ORDER BY confidence DESC LIMIT 10
    """).fetchall()

    db.close()

    # Format as contract-injectable context
    context = {
        "anti_patterns": [
            {"content": r["content"], "severity": r["severity"]}
            for r in anti_patterns
        ],
        "workspace_rules": [
            {"content": r["content"], "category": r["category"], "confidence": r["confidence"]}
            for r in workspace_rules
        ],
        "task_rules": [
            {"content": r["content"], "category": r["category"], "confidence": r["confidence"]}
            for r in task_rules
        ],
        "forge_patterns": [
            {"content": r["content"], "confidence": r["confidence"]}
            for r in forge_rules
        ],
        "principles": [
            {"content": r["content"], "confidence": r["confidence"]}
            for r in principles
        ],
    }

    return context


def format_forge_context_markdown(context):
    """Format Cortex context as markdown for Forge contract injection."""
    lines = ["## Cortex Intelligence for Forge", ""]

    if context.get("anti_patterns"):
        lines.append("### NEVER DO (from Cortex)")
        for ap in context["anti_patterns"]:
            lines.append(f"- [{ap['severity'].upper()}] {ap['content']}")
        lines.append("")

    if context.get("principles"):
        lines.append("### Learned Principles")
        for p in context["principles"]:
            lines.append(f"- [{p['confidence']:.1f}] {p['content']}")
        lines.append("")

    if context.get("task_rules"):
        lines.append("### Task-Relevant Rules")
        for r in context["task_rules"]:
            lines.append(f"- [{r['confidence']:.1f}|{r['category']}] {r['content']}")
        lines.append("")

    if context.get("forge_patterns"):
        lines.append("### Forge Execution Patterns")
        for r in context["forge_patterns"]:
            lines.append(f"- [{r['confidence']:.1f}] {r['content']}")
        lines.append("")

    return "\n".join(lines)


# ---- Stats ----

def bridge_stats():
    """Return Forge bridge statistics."""
    db = get_db()
    stats = {
        "forge_ingest_events": db.execute(
            "SELECT COUNT(*) FROM events WHERE event_type = 'bridge_forge_ingest'"
        ).fetchone()[0],
        "forge_rules": db.execute(
            "SELECT COUNT(*) FROM rules WHERE category LIKE 'forge_%'"
        ).fetchone()[0],
        "forge_anti_patterns": db.execute(
            "SELECT COUNT(*) FROM anti_patterns WHERE source_event LIKE 'forge:%'"
        ).fetchone()[0],
    }
    db.close()
    return stats


# ---- CLI ----

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: bridge_forge.py <ingest|context|stats>")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "ingest":
        path = sys.argv[2] if len(sys.argv) > 2 else None
        result = ingest_forge_outcome(path)
        print(json.dumps(result, indent=2))
    elif cmd == "context":
        task = sys.argv[2] if len(sys.argv) > 2 else None
        ctx = get_forge_context(task_description=task)
        print(format_forge_context_markdown(ctx))
    elif cmd == "stats":
        import pprint
        pprint.pprint(bridge_stats())
    else:
        print(f"Unknown command: {cmd}")
