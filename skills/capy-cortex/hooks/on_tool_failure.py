#!/usr/bin/env python3
"""Capy Cortex Hook: PostToolUseFailure - Pain reflex.
Records actionable tool failures as error patterns. Runs async (non-blocking)."""

import json
import sys
import sqlite3
import re
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "cortex.db"

# Tools to skip - errors from these are not actionable
SKIP_TOOLS = {"TaskOutput", "Read"}

# Error pattern extractors with categories
ERROR_PATTERNS = [
    # npm/yarn dependency errors
    (r"(?:npm|yarn) ERR.*?(?:ERESOLVE|peer dep|conflict)", "dependency_error",
     "npm dependency resolution: use --legacy-peer-deps or resolve version conflicts"),
    (r"Cannot find module ['\"]([^'\"]+)['\"]", "dependency_error",
     lambda m: f"Missing Node.js module '{m.group(1)}': run npm install"),
    (r"ModuleNotFoundError: No module named ['\"]([^'\"]+)['\"]", "dependency_error",
     lambda m: f"Missing Python module '{m.group(1)}': run pip install"),

    # File system errors
    (r"(?:No such file or directory|ENOENT).*?['\"]([^'\"]+)['\"]", "file_not_found",
     lambda m: f"File not found: verify path exists: {m.group(1)}"),
    (r"(?:Permission denied|EACCES)", "permission_denied",
     "Permission denied: check file permissions or run with appropriate access"),
    (r"(?:EEXIST|File exists)", "file_exists",
     "File already exists: remove existing file or use different path"),

    # Compilation errors
    (r"(?:SyntaxError|ParseError|Unexpected token)", "syntax_error",
     "Syntax error: review code for syntax issues"),
    (r"TypeError: .* is not a function", "type_error",
     "Type error: verify function exists and is callable"),
    (r"ReferenceError: (\\w+) is not defined", "reference_error",
     lambda m: f"Undefined reference: '{m.group(1)}' not declared"),
    (r"(?:compilation failed|build error|compile error)", "compilation_error",
     "Compilation failed: review error output for specific issues"),

    # Network errors
    (r"(?:ECONNREFUSED|Connection refused|ETIMEDOUT)", "network_error",
     "Network connection failed: verify service is running and accessible"),
    (r"(?:getaddrinfo|DNS lookup failed|EAI_AGAIN)", "network_error",
     "DNS resolution failed: check network connectivity"),
    (r"(?:404|Not Found|HTTP.*?404)", "network_error",
     "HTTP 404: verify URL endpoint exists"),
    (r"(?:401|403|Unauthorized|Forbidden)", "auth_error",
     "Authentication failed: verify credentials or permissions"),

    # Git errors
    (r"fatal: (?:not a git repository|Not a git repository)", "git_error",
     "Not a git repository: initialize git or run from git root"),
    (r"error: Your local changes.*?would be overwritten", "git_error",
     "Git conflict: commit or stash local changes before merge/checkout"),
    (r"fatal: remote.*?already exists", "git_error",
     "Git remote exists: use different name or update existing remote"),

    # Database errors
    (r"(?:OperationalError|database is locked)", "database_error",
     "Database locked: close other connections or retry"),
    (r"(?:IntegrityError|UNIQUE constraint failed)", "database_error",
     "Database integrity violation: check for duplicate entries"),

    # Port/socket errors
    (r"(?:EADDRINUSE|address already in use).*?port (\\d+)", "port_conflict",
     lambda m: f"Port {m.group(1)} already in use: stop existing service or use different port"),

    # Memory/resource errors
    (r"(?:OutOfMemoryError|heap out of memory|Cannot allocate memory)", "resource_error",
     "Out of memory: reduce memory usage or increase available memory"),
    (r"(?:EMFILE|too many open files)", "resource_error",
     "Too many open files: close unused file handles or increase limit"),
]


def normalize_error_text(text):
    """Remove noise from error text for better pattern matching."""
    # Remove tool IDs (toolu_bdrk_xxxx)
    text = re.sub(r"toolu_[a-zA-Z0-9_]+", "", text)
    # Remove common timestamps
    text = re.sub(r"\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}", "", text)
    # Remove hex addresses/hashes
    text = re.sub(r"0x[0-9a-fA-F]+", "", text)
    # Remove UUIDs
    text = re.sub(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", "", text)
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_error_pattern(tool_name, tool_response, tool_input=None):
    """Extract actionable error pattern from tool response.

    Returns (category, actionable_insight, pattern_key) or None if not actionable.
    """
    # Normalize the error text
    normalized = normalize_error_text(tool_response)

    # Try to match known patterns
    for pattern_re, category, insight_template in ERROR_PATTERNS:
        match = re.search(pattern_re, tool_response, re.IGNORECASE | re.DOTALL)
        if match:
            # Generate insight (either static string or lambda)
            if callable(insight_template):
                insight = insight_template(match)
            else:
                insight = insight_template

            # Create pattern key for deduplication (category + normalized pattern)
            pattern_key = f"{category}:{normalized[:200]}"
            return category, insight, pattern_key

    # Check for generic exit codes without useful info
    if re.search(r"Exit code \d+$", tool_response.strip()):
        return None  # Skip generic exit codes

    # If error is too short or too long, skip
    if len(normalized) < 10 or len(normalized) > 1000:
        return None

    return None


def find_similar_pattern(db, insight, category):
    """Check if similar error pattern exists in database.
    Uses exact content match (fast, indexed) with FTS5 fallback.
    Returns rule ID if found, None otherwise.
    """
    try:
        # 1. Exact content match (uses unique index)
        result = db.execute(
            "SELECT id FROM rules WHERE content = ? LIMIT 1",
            (insight,)
        ).fetchone()
        if result:
            return result[0]

        # 2. FTS5 fuzzy fallback - match on significant words
        words = [w for w in insight.lower().split() if len(w) > 4 and w.isalnum()][:5]
        if words:
            fts_q = " AND ".join(words)
            if fts_q:
                result = db.execute("""
                    SELECT r.id FROM rules_fts
                    JOIN rules r ON rules_fts.rowid = r.id
                    WHERE rules_fts MATCH ? AND r.category = ?
                    LIMIT 1
                """, (fts_q, category)).fetchone()
                if result:
                    return result[0]
    except Exception:
        pass
    return None


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
        workspace = data.get("source_workspace", "")

        # Skip non-actionable tools
        if tool_name in SKIP_TOOLS:
            return

        # Skip empty responses
        if not tool_response or len(tool_response.strip()) < 5:
            return

        tool_input = data.get("tool_input", {})
        normalized = normalize_error_text(tool_response)

        # Path 1: Regex extraction (fast, <1ms cache for known patterns)
        result = extract_error_pattern(tool_name, tool_response, tool_input)
        extraction_method = 'regex'
        quality_score = 0

        if result:
            category, insight, pattern_key = result
        elif len(normalized) >= 30:
            # Path 2: LLM quality-gated extraction (causal analysis + quality score)
            try:
                sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
                from llm_extract import extract_with_quality_gate
                llm_rule, score = extract_with_quality_gate(
                    tool_name, tool_input, tool_response, session_id=session_id)
                if llm_rule:
                    category = llm_rule['category']
                    insight = llm_rule['content']
                    pattern_key = f"llm_v2:{category}:{normalized[:150]}"
                    extraction_method = 'llm_v2'
                    quality_score = score
                else:
                    return  # Below quality threshold or LLM failed
            except Exception:
                return
        else:
            return  # Not actionable

        # Store pattern with deduplication
        db = sqlite3.connect(str(DB_PATH))
        db.execute("PRAGMA journal_mode=WAL")
        db.execute("PRAGMA busy_timeout=3000")

        # Check for existing similar pattern
        existing_id = find_similar_pattern(db, insight, category)

        if existing_id:
            # Increment occurrence count
            db.execute("""
                UPDATE rules SET
                    occurrences = occurrences + 1,
                    last_seen = datetime('now')
                WHERE id = ?
            """, (existing_id,))
        else:
            # Create new error pattern
            evidence_json = json.dumps({
                "pattern_key": pattern_key,
                "tool": tool_name,
                "example_response": tool_response[:300]
            })

            db.execute("""
                INSERT INTO rules (
                    content, category, confidence, occurrences,
                    maturity, harmful_count, source_session, source_workspace,
                    evidence, quality_score, extraction_method,
                    created_at, last_seen
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
            """, (insight, category, 0.5, 1, 'candidate', 0, session_id, workspace,
                  evidence_json, quality_score, extraction_method))

            # Auto-assign topic (Phase 4F)
            new_rule_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
            try:
                sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
                from topic_engine import detect_topic_for_rule
                topic = detect_topic_for_rule(insight, category)
                topic_row = db.execute(
                    "SELECT id FROM topics WHERE name = ?", (topic,)
                ).fetchone()
                if topic_row:
                    db.execute(
                        "INSERT OR IGNORE INTO rule_topics (rule_id, topic_id) VALUES (?, ?)",
                        (new_rule_id, topic_row[0])
                    )
                    db.execute(
                        "UPDATE topics SET rule_count = rule_count + 1 WHERE id = ?",
                        (topic_row[0],)
                    )
            except Exception:
                pass  # Topic assignment is best-effort

        # Log event
        db.execute(
            "INSERT INTO events (event_type, metadata) VALUES (?, ?)",
            ("tool_failure_pattern", json.dumps({
                "tool": tool_name,
                "category": category,
                "pattern_key": pattern_key[:100]
            }))
        )

        db.commit()
        db.close()

        # Mark TF-IDF as dirty
        db2 = sqlite3.connect(str(DB_PATH))
        db2.execute("UPDATE meta SET value = '1' WHERE key = 'tfidf_dirty'")
        db2.commit()
        db2.close()

    except Exception:
        pass  # Hooks must NEVER crash


if __name__ == "__main__":
    main()
