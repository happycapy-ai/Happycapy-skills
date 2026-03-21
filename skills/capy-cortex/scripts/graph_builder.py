#!/usr/bin/env python3
"""Capy Cortex v2 - Entity Graph Builder.
Extracts entities from rules and builds a knowledge graph for graph-based retrieval.
Uses regex for fast extraction + LLM for complex cases.
Provides graph_retrieve() for Phase 3 Triple Fusion."""

import json
import re
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "cortex.db"

# Entity type patterns (regex-based, fast)
ENTITY_PATTERNS = {
    "tool": [
        r"\b(npm|yarn|pip|git|docker|webpack|vite|eslint|prettier|jest|pytest)\b",
        r"\b(Bash|Read|Write|Edit|Glob|Grep|WebFetch|Task)\b",
        r"\b(curl|wget|ssh|rsync|make|cmake|cargo|go)\b",
    ],
    "library": [
        r"\b(react|vue|angular|svelte|next\.?js|express|fastapi|django|flask)\b",
        r"\b(typescript|tailwind|prisma|drizzle|zod|trpc)\b",
        r"\b(sqlite|postgres|redis|mongodb|supabase)\b",
        r"\b(playwright|puppeteer|selenium|cypress)\b",
    ],
    "language": [
        r"\b(python|javascript|typescript|rust|go|java|ruby|php|swift|kotlin)\b",
        r"\b(html|css|sql|bash|zsh|shell)\b",
    ],
    "file": [
        r"(?:^|\s)([\w./\-]+\.(?:js|ts|tsx|jsx|py|rs|go|json|yaml|yml|toml|md|sql|sh|css|html))\b",
        r"\b(package\.json|tsconfig\.json|Dockerfile|Makefile|\.env)\b",
        r"\b(CLAUDE\.md|SKILL\.md|MEMORY\.md)\b",
    ],
    "command": [
        r"\b(npm (?:install|ci|run|build|test))\b",
        r"\b(git (?:push|pull|merge|rebase|checkout|commit|clone))\b",
        r"\b(pip install|python3? -m)\b",
        r"\b(docker (?:build|run|compose|push))\b",
    ],
    "error_type": [
        r"\b(ERESOLVE|ENOENT|EACCES|EADDRINUSE|ECONNREFUSED|ETIMEDOUT)\b",
        r"\b(SyntaxError|TypeError|ReferenceError|ModuleNotFoundError)\b",
        r"\b(OperationalError|IntegrityError|PermissionError)\b",
        r"\b(peer dep(?:endency)?|version conflict)\b",
    ],
    "concept": [
        r"\b(authentication|authorization|CORS|CSRF|XSS|injection)\b",
        r"\b(CI/CD|deployment|migration|rollback|backup)\b",
        r"\b(caching|rate limiting|pagination|middleware)\b",
        r"\b(hook|plugin|extension|skill|agent)\b",
    ],
}

# Relation inference patterns
RELATION_PATTERNS = [
    (r"(\w+)\s+(?:causes?|triggers?|leads? to)\s+(\w+)", "causes"),
    (r"(\w+)\s+(?:fixes?|resolves?|solves?)\s+(\w+)", "fixes"),
    (r"(?:use|run|install)\s+(\w+)", "uses"),
    (r"(\w+)\s+(?:depends? on|requires?)\s+(\w+)", "depends_on"),
    (r"(\w+)\s+(?:instead of|not|rather than)\s+(\w+)", "replaces"),
]


def _get_db():
    """Get DB connection with WAL mode."""
    db = sqlite3.connect(str(DB_PATH))
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA busy_timeout=3000")
    return db


def extract_entities_regex(text):
    """Fast regex-based entity extraction. Returns list of (name, type)."""
    entities = []
    seen = set()
    text_lower = text.lower()
    for entity_type, patterns in ENTITY_PATTERNS.items():
        for pattern in patterns:
            flags = re.IGNORECASE if entity_type != "file" else 0
            for match in re.finditer(pattern, text, flags):
                name = match.group(1) if match.lastindex else match.group(0)
                name = name.strip().lower()
                if len(name) < 2 or name in seen:
                    continue
                seen.add(name)
                entities.append((name, entity_type))
    return entities


def extract_relations_regex(text, entities):
    """Extract relations between entities found in text."""
    relations = []
    entity_names = {e[0] for e in entities}
    for pattern, rel_type in RELATION_PATTERNS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            groups = match.groups()
            if len(groups) >= 2:
                source = groups[0].lower().strip()
                target = groups[1].lower().strip()
                if source in entity_names and target in entity_names:
                    relations.append((source, target, rel_type))
    return relations


def upsert_entity(db, name, entity_type):
    """Insert or update entity, return entity ID."""
    existing = db.execute(
        "SELECT id FROM entities WHERE name = ?", (name,)
    ).fetchone()
    if existing:
        db.execute(
            "UPDATE entities SET mention_count = mention_count + 1 WHERE id = ?",
            (existing[0],)
        )
        return existing[0]
    db.execute(
        "INSERT INTO entities (name, entity_type, mention_count) VALUES (?, ?, 1)",
        (name, entity_type)
    )
    return db.execute("SELECT last_insert_rowid()").fetchone()[0]


def link_entity_to_rule(db, entity_id, rule_id, mention_type="reference"):
    """Create entity-rule link (deduplicated)."""
    try:
        db.execute(
            "INSERT OR IGNORE INTO entity_mentions (entity_id, rule_id, mention_type) "
            "VALUES (?, ?, ?)",
            (entity_id, rule_id, mention_type)
        )
    except Exception:
        pass


def add_edge(db, source_id, target_id, relation_type, rule_id=None):
    """Add or update knowledge edge."""
    try:
        existing = db.execute(
            "SELECT id, weight FROM knowledge_edges "
            "WHERE source_entity_id = ? AND target_entity_id = ? AND relation_type = ?",
            (source_id, target_id, relation_type)
        ).fetchone()
        if existing:
            db.execute(
                "UPDATE knowledge_edges SET weight = weight + 0.5 WHERE id = ?",
                (existing[0],)
            )
        else:
            db.execute(
                "INSERT INTO knowledge_edges "
                "(source_entity_id, target_entity_id, relation_type, weight, evidence_rule_id) "
                "VALUES (?, ?, ?, 1.0, ?)",
                (source_id, target_id, relation_type, rule_id)
            )
    except Exception:
        pass


def process_rule(db, rule_id, content, category):
    """Extract entities from a single rule and build graph links."""
    entities = extract_entities_regex(content)
    if not entities:
        return 0

    entity_ids = {}
    for name, etype in entities:
        eid = upsert_entity(db, name, etype)
        entity_ids[name] = eid
        link_entity_to_rule(db, eid, rule_id)

    # Extract and store relations
    relations = extract_relations_regex(content, entities)
    for source_name, target_name, rel_type in relations:
        if source_name in entity_ids and target_name in entity_ids:
            add_edge(db, entity_ids[source_name], entity_ids[target_name],
                     rel_type, rule_id)

    # Auto-infer co-occurrence edges (entities in same rule are related)
    eid_list = list(entity_ids.values())
    for i in range(len(eid_list)):
        for j in range(i + 1, min(i + 4, len(eid_list))):
            add_edge(db, eid_list[i], eid_list[j], "co_occurs", rule_id)

    return len(entities)


def build_graph():
    """Process all rules and build the entity graph."""
    db = _get_db()
    rules = db.execute(
        "SELECT id, content, category FROM rules WHERE maturity != 'deprecated'"
    ).fetchall()
    total_entities = 0
    processed = 0
    for rule_id, content, category in rules:
        count = process_rule(db, rule_id, content, category)
        total_entities += count
        processed += 1
    db.commit()

    # Stats
    entity_count = db.execute("SELECT COUNT(*) FROM entities").fetchone()[0]
    mention_count = db.execute("SELECT COUNT(*) FROM entity_mentions").fetchone()[0]
    edge_count = db.execute("SELECT COUNT(*) FROM knowledge_edges").fetchone()[0]
    db.close()

    return {
        "rules_processed": processed,
        "entities": entity_count,
        "mentions": mention_count,
        "edges": edge_count,
    }


def graph_retrieve(query, top_k=10):
    """Graph-based retrieval: find rules connected to query entities.
    Used by Phase 3 Triple Fusion Retrieval.
    Returns list of dicts: {id, content, confidence, graph_score, path}."""
    db = _get_db()
    db.row_factory = sqlite3.Row

    # Extract entities from query
    query_entities = extract_entities_regex(query)
    if not query_entities:
        db.close()
        return []

    # Find matching entity IDs
    entity_ids = []
    for name, _ in query_entities:
        row = db.execute(
            "SELECT id FROM entities WHERE name = ?", (name,)
        ).fetchone()
        if row:
            entity_ids.append(row["id"])

    if not entity_ids:
        db.close()
        return []

    # 1-hop: rules directly mentioning these entities
    placeholders = ",".join("?" * len(entity_ids))
    direct_rules = db.execute(f"""
        SELECT DISTINCT r.id, r.content, r.confidence, r.category,
               r.helpful_count, 1.0 AS graph_score, 'direct' AS path
        FROM entity_mentions em
        JOIN rules r ON em.rule_id = r.id
        WHERE em.entity_id IN ({placeholders})
        AND r.maturity != 'deprecated'
    """, entity_ids).fetchall()

    # 2-hop: rules connected via knowledge edges
    neighbor_rules = db.execute(f"""
        SELECT DISTINCT r.id, r.content, r.confidence, r.category,
               r.helpful_count, ke.weight * 0.5 AS graph_score, 'neighbor' AS path
        FROM knowledge_edges ke
        JOIN entity_mentions em ON em.entity_id = ke.target_entity_id
        JOIN rules r ON em.rule_id = r.id
        WHERE ke.source_entity_id IN ({placeholders})
        AND r.maturity != 'deprecated'
        AND r.id NOT IN (
            SELECT rule_id FROM entity_mentions WHERE entity_id IN ({placeholders})
        )
    """, entity_ids + entity_ids).fetchall()

    # Merge and deduplicate
    seen = set()
    results = []
    for row in list(direct_rules) + list(neighbor_rules):
        if row["id"] in seen:
            continue
        seen.add(row["id"])
        results.append(dict(row))

    # Sort by graph_score * confidence
    results.sort(key=lambda r: r["graph_score"] * r["confidence"], reverse=True)
    db.close()
    return results[:top_k]


if __name__ == "__main__":
    print("=== Capy Cortex Entity Graph Builder ===")
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        stats = build_graph()
        print(f"BUILT: {stats}")
    elif len(sys.argv) > 1 and sys.argv[1] == "query":
        query = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "npm install"
        results = graph_retrieve(query)
        print(f"Query: '{query}' -> {len(results)} rules")
        for r in results[:5]:
            print(f"  [{r['graph_score']:.1f}|{r['path']}] {r['content'][:80]}")
    else:
        print("Usage: python3 graph_builder.py build|query <text>")
        # Quick stats
        db = _get_db()
        for t in ['entities', 'entity_mentions', 'knowledge_edges']:
            c = db.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
            print(f"  {t}: {c}")
        db.close()
