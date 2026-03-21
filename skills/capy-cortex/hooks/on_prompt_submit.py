#!/usr/bin/env python3
"""Capy Cortex Hook: UserPromptSubmit - Task analyst + success tracker.
Retrieves task-specific rules based on user's message using FTS5.
Records surfaced rule IDs for later success crediting by on_tool_success.py.
Runs every user message. Must be fast (<100ms) -- uses FTS5 only, no sklearn."""

import json
import sys
import sqlite3
import importlib.util
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "cortex.db"
MIN_PROMPT_LENGTH = 15  # Skip very short messages


def main():
    try:
        data = json.loads(sys.stdin.read())
    except Exception:
        return

    prompt = data.get("prompt", "")
    if len(prompt) < MIN_PROMPT_LENGTH or not DB_PATH.exists():
        return

    try:
        db = sqlite3.connect(str(DB_PATH))
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA journal_mode=WAL")
        db.execute("PRAGMA busy_timeout=2000")

        current_workspace = data.get("cwd", "")
        session_id = data.get("session_id", "")

        # Extract meaningful words for FTS5 query
        stop_words = {
            "the", "a", "an", "is", "are", "was", "were", "be", "been",
            "being", "have", "has", "had", "do", "does", "did", "will",
            "would", "could", "should", "may", "might", "can", "shall",
            "i", "you", "he", "she", "it", "we", "they", "me", "my",
            "your", "his", "her", "its", "our", "their", "this", "that",
            "to", "of", "in", "for", "on", "with", "at", "by", "from",
            "and", "or", "not", "but", "if", "then", "so", "just",
            "want", "need", "please", "help", "make", "let", "get",
        }
        words = [w for w in prompt.lower().split()
                 if len(w) > 2 and w.isalnum() and w not in stop_words][:10]

        if not words:
            db.close()
            return

        fts_query = " OR ".join(words)

        # Phase v3: Triple Fusion Retrieval (hybrid + graph + RRF)
        sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
        hybrid_results = []
        graph_results = []

        # Signal 1: Hybrid retrieval (FTS5 + TF-IDF embeddings)
        try:
            from embeddings import hybrid_retrieve
            hybrid_results = hybrid_retrieve(prompt, top_k=15, workspace=current_workspace)
        except Exception:
            pass

        # Signal 2: Graph retrieval (entity graph traversal)
        try:
            from graph_builder import graph_retrieve
            graph_results = graph_retrieve(prompt, top_k=10)
        except Exception:
            pass

        if hybrid_results or graph_results:
            # RRF fusion: merge hybrid + graph rankings
            K = 60
            rule_map = {}  # rule_id -> {rule_dict, rrf_score}
            for rank, r in enumerate(hybrid_results):
                rid = r.get('id')
                if rid is None:
                    continue
                rule_map.setdefault(rid, {'rule': r, 'score': 0})
                rule_map[rid]['score'] += 1.0 / (K + rank + 1)
            for rank, r in enumerate(graph_results):
                rid = r.get('id')
                if rid is None:
                    continue
                if rid not in rule_map:
                    rule_map[rid] = {'rule': r, 'score': 0}
                rule_map[rid]['score'] += 0.8 / (K + rank + 1)

            # Quality gates + workspace/helpful boosts
            filtered_rules = []
            for rid, entry in rule_map.items():
                r = entry['rule']
                if r.get('confidence', 0) < 0.5:
                    continue
                if r.get('category') == 'error':
                    if (r.get('helpful_count') or 0) == 0 and (r.get('occurrences') or 0) < 5:
                        continue
                score = entry['score']
                if current_workspace and r.get('source_workspace'):
                    if current_workspace.startswith(r['source_workspace']) or \
                       r['source_workspace'].startswith(current_workspace):
                        score *= 1.5
                helpful = r.get('helpful_count') or 0
                if helpful > 0:
                    score *= (1 + min(helpful / 10, 0.5))
                filtered_rules.append((r, score))
            filtered_rules.sort(key=lambda x: x[1], reverse=True)
            top_rules = [r for r, _ in filtered_rules[:5]]
        else:
            # Fallback: FTS5-only retrieval
            raw_rules = db.execute("""
                SELECT r.id, r.content, r.confidence, r.category, r.helpful_count,
                       r.occurrences, r.source_workspace, rank AS fts_rank
                FROM rules_fts JOIN rules r ON rules_fts.rowid = r.id
                WHERE rules_fts MATCH ? AND r.maturity != 'deprecated'
                ORDER BY rank LIMIT 30
            """, (fts_query,)).fetchall()

            if not raw_rules:
                db.close()
                return

            filtered_rules = []
            for r in raw_rules:
                if r['confidence'] < 0.5:
                    continue
                if r['category'] == 'error':
                    if (r['helpful_count'] or 0) == 0 and (r['occurrences'] or 0) < 5:
                        continue
                score = -r['fts_rank']
                if current_workspace and r['source_workspace']:
                    if current_workspace.startswith(r['source_workspace']) or \
                       r['source_workspace'].startswith(current_workspace):
                        score *= 1.5
                helpful = r['helpful_count'] or 0
                if helpful > 0:
                    score *= (1 + min(helpful / 10, 0.5))
                filtered_rules.append((r, score))
            filtered_rules.sort(key=lambda x: x[1], reverse=True)
            top_rules = [r for r, _ in filtered_rules[:5]]

        if not top_rules:
            db.close()
            return

        # Record surfaced rules for success tracking
        if session_id:
            # Clear old uncredited surfaced rules for this session
            # (new prompt = new context, old surfaced rules are stale)
            db.execute(
                "DELETE FROM surfaced_rules WHERE session_id = ? AND credited = 0",
                (session_id,)
            )
            # Record newly surfaced rules
            for r in top_rules:
                db.execute(
                    "INSERT INTO surfaced_rules (session_id, rule_id) VALUES (?, ?)",
                    (session_id, r['id'])
                )
            db.commit()

        db.close()

        lines = ["## Cortex: Task-Relevant Rules"]
        for r in top_rules:
            helpful = r['helpful_count'] or 0
            help_marker = f" +{helpful}" if helpful > 0 else ""
            lines.append(f"- [{r['confidence']:.1f}|{r['category']}{help_marker}] {r['content']}")

        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": "\n".join(lines)
            }
        }
        print(json.dumps(output))

    except Exception:
        pass  # Hooks must NEVER crash


if __name__ == "__main__":
    main()
