#!/usr/bin/env python3
"""Capy Cortex - Claudeception Bridge.
Bidirectional sync between Cortex knowledge DB and Claudeception file-based skills.

Bridge 1 (Cortex -> Claudeception): Export high-confidence principles as skill files.
Bridge 2 (Claudeception -> Cortex): Import skill knowledge as Cortex principles."""

import json
import re
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / "cortex.db"
SKILLS_DIR = Path.home() / ".claude/skills"
CORTEX_SKILLS_DIR = SKILLS_DIR / "capy-cortex" / "exported_skills"


def get_db():
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA busy_timeout=3000")
    return db


# ---- Bridge 1: Cortex -> Claudeception ----

def export_principles_as_skills(min_confidence=0.8, min_occurrences=2):
    """Export high-confidence Cortex principles as Claudeception-style skill files.
    Returns count of skills exported."""
    db = get_db()
    principles = db.execute("""
        SELECT id, content, source_rule_ids, confidence, occurrences, created_at
        FROM principles
        WHERE confidence >= ?
        ORDER BY confidence DESC, occurrences DESC
    """, (min_confidence,)).fetchall()

    if not principles:
        db.close()
        return 0

    # Group principles by category (inferred from content)
    categorized = {}
    for p in principles:
        category = _infer_category(p["content"])
        if category not in categorized:
            categorized[category] = []
        categorized[category].append(p)

    CORTEX_SKILLS_DIR.mkdir(parents=True, exist_ok=True)
    exported = 0

    for category, principles_list in categorized.items():
        if len(principles_list) < min_occurrences:
            continue

        skill_name = f"cortex-{category}"
        skill_path = CORTEX_SKILLS_DIR / f"{skill_name}.md"

        # Build skill content
        lines = [
            f"# Cortex Learned Skill: {category.replace('_', ' ').title()}",
            "",
            f"Auto-generated from {len(principles_list)} Cortex principles.",
            f"Last updated: {datetime.now().isoformat()[:10]}",
            "",
            "## Principles",
            "",
        ]
        source_ids = []
        for p in principles_list:
            lines.append(f"- [{p['confidence']:.1f}] {p['content']}")
            source_ids.append(p["id"])

        lines.extend(["", "## Source", ""])
        lines.append(f"Exported from Cortex DB, principle IDs: {source_ids}")

        skill_path.write_text("\n".join(lines))
        exported += 1

    # Record export event
    db.execute(
        "INSERT INTO events (event_type, metadata) VALUES (?, ?)",
        ("bridge_export_claudeception", json.dumps({
            "skills_exported": exported,
            "categories": list(categorized.keys()),
        }))
    )
    db.commit()
    db.close()
    return exported


def _infer_category(content):
    """Infer category from principle content."""
    lower = content.lower()
    if any(w in lower for w in ["git", "push", "commit", "branch", "merge"]):
        return "git_workflow"
    if any(w in lower for w in ["npm", "dependency", "package", "install", "module"]):
        return "dependency_management"
    if any(w in lower for w in ["permission", "access", "auth", "credential"]):
        return "security"
    if any(w in lower for w in ["port", "server", "network", "connection"]):
        return "networking"
    if any(w in lower for w in ["file", "path", "directory", "config"]):
        return "filesystem"
    if any(w in lower for w in ["test", "debug", "error", "fix"]):
        return "debugging"
    return "general"


# ---- Bridge 2: Claudeception -> Cortex ----

def import_skills_as_principles():
    """Scan Claudeception skills and import actionable knowledge as Cortex principles.
    Returns count of principles imported."""
    db = get_db()
    imported = 0

    # Scan all skill directories
    for skill_dir in SKILLS_DIR.iterdir():
        if not skill_dir.is_dir():
            continue
        if skill_dir.name == "capy-cortex":
            continue  # Skip self

        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue

        knowledge = _extract_skill_knowledge(skill_file)
        for item in knowledge:
            # Check if already imported
            existing = db.execute(
                "SELECT id FROM principles WHERE content = ?", (item["content"],)
            ).fetchone()
            if existing:
                continue

            # Check for similar via word overlap
            if _find_similar_principle(db, item["content"]):
                continue

            db.execute("""
                INSERT INTO principles (content, source_rule_ids, confidence)
                VALUES (?, ?, ?)
            """, (
                item["content"],
                json.dumps({"source": f"skill:{skill_dir.name}"}),
                item.get("confidence", 0.7),
            ))
            imported += 1

    if imported > 0:
        db.execute(
            "INSERT INTO events (event_type, metadata) VALUES (?, ?)",
            ("bridge_import_claudeception", json.dumps({
                "principles_imported": imported,
            }))
        )
        db.commit()
    db.close()
    return imported


def _extract_skill_knowledge(skill_path):
    """Extract actionable knowledge items from a SKILL.md file."""
    items = []
    try:
        content = skill_path.read_text()
        lines = content.split("\n")

        in_section = False
        for line in lines:
            stripped = line.strip()

            # Look for solution/best-practice/tip sections
            if re.match(r"^#+\s*(Solution|Best Practices?|Tips?|Rules?|Never|Always)", stripped, re.IGNORECASE):
                in_section = True
                continue
            if re.match(r"^#+\s*", stripped) and in_section:
                in_section = False

            # Extract bullet points from relevant sections
            if in_section and stripped.startswith("- "):
                item_text = stripped[2:].strip()
                # Only keep actionable items (not too short, not code)
                if 20 < len(item_text) < 300 and not item_text.startswith("`"):
                    items.append({"content": item_text, "confidence": 0.7})

    except Exception:
        pass
    return items[:20]  # Cap at 20 items per skill


def _find_similar_principle(db, content, threshold=0.5):
    """Check if a similar principle already exists."""
    words = set(content.lower().split())
    existing = db.execute("SELECT content FROM principles").fetchall()
    for row in existing:
        existing_words = set(row[0].lower().split())
        if not words or not existing_words:
            continue
        overlap = len(words & existing_words) / len(words | existing_words)
        if overlap >= threshold:
            return True
    return False


# ---- Stats ----

def bridge_stats():
    """Return bridge integration statistics."""
    db = get_db()
    stats = {
        "export_events": db.execute(
            "SELECT COUNT(*) FROM events WHERE event_type = 'bridge_export_claudeception'"
        ).fetchone()[0],
        "import_events": db.execute(
            "SELECT COUNT(*) FROM events WHERE event_type = 'bridge_import_claudeception'"
        ).fetchone()[0],
        "exported_skill_files": len(list(CORTEX_SKILLS_DIR.glob("*.md")))
            if CORTEX_SKILLS_DIR.exists() else 0,
        "principles_from_skills": db.execute(
            "SELECT COUNT(*) FROM principles WHERE source_rule_ids LIKE '%skill:%'"
        ).fetchone()[0],
    }
    db.close()
    return stats


# ---- CLI ----

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: bridge_claudeception.py <export|import|stats>")
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "export":
        n = export_principles_as_skills()
        print(f"Exported {n} skill files")
    elif cmd == "import":
        n = import_skills_as_principles()
        print(f"Imported {n} principles from skills")
    elif cmd == "stats":
        import pprint
        pprint.pprint(bridge_stats())
    else:
        print(f"Unknown command: {cmd}")
