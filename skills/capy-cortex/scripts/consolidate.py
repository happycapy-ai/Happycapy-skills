#!/usr/bin/env python3
"""Capy Cortex v2 - LLM-Powered Consolidation Engine.
Clusters similar rules, synthesizes principles via LLM, quality-scores all rules,
deprecates junk, merges duplicates. The brain's sleep cycle.

Pipeline:
  1. Score all unscored rules via Haiku (quality gate retroactive)
  2. Deprecate rules scoring < 2/4 on quality
  3. Merge near-duplicate rules (TF-IDF cosine > 0.85)
  4. Cluster remaining rules via AgglomerativeClustering
  5. Synthesize principles from clusters via Sonnet LLM
  6. Promote source rules to 'established'
  7. Rebuild entity graph + retrain TF-IDF
"""

import json
import sys
import sqlite3
import pickle
import time
from pathlib import Path
from collections import Counter

DB_PATH = Path(__file__).parent.parent / "cortex.db"
TFIDF_DIR = Path(__file__).parent.parent / "tfidf"
SCRIPTS_DIR = Path(__file__).parent

# Clustering parameters
MIN_CLUSTER_SIZE = 3
DISTANCE_THRESHOLD = 0.5
MAX_PRINCIPLES_PER_RUN = 20
QUALITY_THRESHOLD = 2  # Minimum quality score to keep a rule
DUPLICATE_THRESHOLD = 0.85  # Cosine similarity for near-duplicate detection

# LLM synthesis prompt
SYNTHESIS_PROMPT = """Synthesize these {count} related rules into ONE clear, actionable principle.
The principle should be a single imperative sentence that captures the common pattern.
Rules (category: {category}):
{rules_text}

Return ONE JSON: {{"principle": "imperative sentence", "confidence": 0.8}}
No markdown. Just JSON."""


def get_db():
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA busy_timeout=5000")
    return db


def consolidate(verbose=False):
    """Run full v2 consolidation pipeline. Returns stats dict."""
    if not DB_PATH.exists():
        return {"error": "cortex.db not found"}

    stats = {
        "rules_scored": 0, "rules_deprecated": 0, "duplicates_merged": 0,
        "clusters_found": 0, "principles_created": 0, "rules_promoted": 0,
    }

    db = get_db()

    # Step 1: Score unscored rules
    scored = _score_unscored_rules(db, verbose)
    stats["rules_scored"] = scored

    # Step 2: Deprecate low-quality rules
    deprecated = _deprecate_low_quality(db, verbose)
    stats["rules_deprecated"] = deprecated

    # Step 3: Merge near-duplicates
    merged = _merge_near_duplicates(db, verbose)
    stats["duplicates_merged"] = merged

    # Step 4-6: Cluster and synthesize principles
    cluster_stats = _cluster_and_synthesize(db, verbose)
    stats.update(cluster_stats)

    # Step 7: Retrain TF-IDF
    _retrain_tfidf(db)

    # Step 8: Rebuild entity graph
    _rebuild_graph()

    # Record event
    db.execute(
        "INSERT INTO events (event_type, metadata) VALUES (?, ?)",
        ("consolidation_v2", json.dumps(stats))
    )
    db.commit()
    db.close()
    return stats


# --- PLACEHOLDER FUNCTIONS (to be filled via Edit) ---

def _score_unscored_rules(db, verbose=False):
    """Score all rules with quality_score=0 via Haiku LLM."""
    sys.path.insert(0, str(SCRIPTS_DIR))
    from llm_extract import score_existing_rule

    unscored = db.execute("""
        SELECT id, content FROM rules
        WHERE quality_score = 0 AND maturity <> 'deprecated'
        AND LENGTH(content) > 20
        ORDER BY occurrences DESC
        LIMIT 100
    """).fetchall()

    scored = 0
    for rule in unscored:
        try:
            score = score_existing_rule(rule["content"])
            if score is not None and score >= 0:
                db.execute(
                    "UPDATE rules SET quality_score = ? WHERE id = ?",
                    (score, rule["id"])
                )
                scored += 1
                if verbose:
                    print(f"  Scored rule {rule['id']}: {score}/4 - {rule['content'][:60]}")
        except Exception:
            continue
        if scored % 10 == 0 and scored > 0:
            db.commit()  # Checkpoint every 10

    db.commit()
    return scored

def _deprecate_low_quality(db, verbose=False):
    """Deprecate rules that scored below quality threshold.
    Only deprecates rules that have been scored (quality_score > 0)
    and scored below the threshold. Preserves high-occurrence rules."""
    # Don't deprecate rules with high occurrence (proven useful through repetition)
    result = db.execute("""
        UPDATE rules SET maturity = 'deprecated', confidence = 0.1
        WHERE quality_score > 0 AND quality_score < ?
        AND maturity <> 'deprecated'
        AND occurrences < 3
        AND helpful_count = 0
    """, (QUALITY_THRESHOLD,))
    deprecated = result.rowcount
    if verbose and deprecated > 0:
        print(f"  Deprecated {deprecated} low-quality rules (score < {QUALITY_THRESHOLD})")
    db.commit()
    return deprecated

def _merge_near_duplicates(db, verbose=False):
    """Merge near-duplicate rules using TF-IDF cosine similarity.
    Keeps the higher-quality rule and deprecates the duplicate."""
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        import numpy as np
    except ImportError:
        return 0

    rules = db.execute("""
        SELECT id, content, confidence, quality_score, occurrences, helpful_count
        FROM rules WHERE maturity <> 'deprecated' AND LENGTH(content) > 20
        ORDER BY id
    """).fetchall()

    if len(rules) < 2:
        return 0

    texts = [r["content"] for r in rules]
    vectorizer = TfidfVectorizer(max_features=3000, stop_words="english")
    tfidf = vectorizer.fit_transform(texts)

    # Find pairs above similarity threshold
    merged = 0
    deprecated_ids = set()

    for i in range(len(rules) - 1):
        if rules[i]["id"] in deprecated_ids:
            continue
        # Compute similarity with remaining rules
        remaining = tfidf[i+1:]
        if remaining.shape[0] == 0:
            break
        sims = cosine_similarity(tfidf[i:i+1], remaining).flatten()
        for j_offset, sim in enumerate(sims):
            j = i + 1 + j_offset
            if sim >= DUPLICATE_THRESHOLD and rules[j]["id"] not in deprecated_ids:
                # Keep the better rule (higher quality score, then more occurrences)
                r_i, r_j = rules[i], rules[j]
                score_i = (r_i["quality_score"] or 0) * 10 + (r_i["occurrences"] or 0) + (r_i["helpful_count"] or 0) * 5
                score_j = (r_j["quality_score"] or 0) * 10 + (r_j["occurrences"] or 0) + (r_j["helpful_count"] or 0) * 5

                keep, drop = (r_i, r_j) if score_i >= score_j else (r_j, r_i)
                # Merge occurrences into keeper
                db.execute("""
                    UPDATE rules SET occurrences = occurrences + ?,
                    confidence = MAX(confidence, ?) WHERE id = ?
                """, (drop["occurrences"], drop["confidence"], keep["id"]))
                # Deprecate the duplicate
                db.execute(
                    "UPDATE rules SET maturity = 'deprecated' WHERE id = ?",
                    (drop["id"],)
                )
                deprecated_ids.add(drop["id"])
                merged += 1
                if verbose:
                    print(f"  Merged: kept #{keep['id']}, deprecated #{drop['id']} (sim={sim:.2f})")

    db.commit()
    return merged

def _cluster_and_synthesize(db, verbose=False):
    """Cluster rules and synthesize principles via LLM."""
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.cluster import AgglomerativeClustering
        import numpy as np
    except ImportError:
        return {"clusters_found": 0, "principles_created": 0, "rules_promoted": 0}

    rules = db.execute("""
        SELECT id, content, category, confidence, occurrences
        FROM rules WHERE maturity <> 'deprecated' AND LENGTH(content) > 20
        ORDER BY confidence DESC
    """).fetchall()

    if len(rules) < MIN_CLUSTER_SIZE * 2:
        return {"clusters_found": 0, "principles_created": 0, "rules_promoted": 0}

    texts = [r["content"] for r in rules]
    vectorizer = TfidfVectorizer(max_features=5000, stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(texts)

    clustering = AgglomerativeClustering(
        n_clusters=None, distance_threshold=DISTANCE_THRESHOLD,
        metric="cosine", linkage="average",
    )
    labels = clustering.fit_predict(tfidf_matrix.toarray())

    cluster_map = {}
    for idx, label in enumerate(labels):
        cluster_map.setdefault(label, []).append(idx)

    stats = {"clusters_found": len(cluster_map), "principles_created": 0, "rules_promoted": 0}

    for cluster_id, indices in cluster_map.items():
        if len(indices) < MIN_CLUSTER_SIZE:
            continue
        if stats["principles_created"] >= MAX_PRINCIPLES_PER_RUN:
            break

        cluster_rules = [rules[i] for i in indices]
        rule_ids = [r["id"] for r in cluster_rules]

        # LLM synthesis
        principle_content, confidence = _synthesize_principle_llm(cluster_rules)
        if not principle_content:
            continue

        # Check for existing similar principle
        existing = db.execute(
            "SELECT id FROM principles WHERE content = ?", (principle_content,)
        ).fetchone()

        if existing:
            db.execute("""
                UPDATE principles SET occurrences = occurrences + 1,
                source_rule_ids = ? WHERE id = ?
            """, (json.dumps(rule_ids), existing["id"]))
        else:
            db.execute("""
                INSERT INTO principles (content, source_rule_ids, confidence)
                VALUES (?, ?, ?)
            """, (principle_content, json.dumps(rule_ids), confidence))
            stats["principles_created"] += 1
            if verbose:
                print(f"  Principle: {principle_content[:80]}... (from {len(rule_ids)} rules)")

        # Promote source rules
        for rid in rule_ids:
            db.execute(
                "UPDATE rules SET maturity = 'established' WHERE id = ? AND maturity = 'candidate'",
                (rid,)
            )
            stats["rules_promoted"] += 1

    db.commit()
    return stats

def _synthesize_principle_llm(cluster_rules):
    """Use Sonnet LLM to synthesize a principle from clustered rules.
    Returns (principle_text, confidence) or (None, 0)."""
    sys.path.insert(0, str(SCRIPTS_DIR))
    from llm_extract import _call_llm, SONNET

    # Determine dominant category
    categories = [r["category"] for r in cluster_rules]
    cat_counts = Counter(categories)
    dominant_cat = cat_counts.most_common(1)[0][0]

    # Build rules text (max 5 rules, truncated)
    rules_text = "\n".join(
        f"- {r['content'][:150]}" for r in cluster_rules[:5]
    )

    prompt = SYNTHESIS_PROMPT.format(
        count=len(cluster_rules), category=dominant_cat, rules_text=rules_text
    )

    try:
        result = _call_llm(prompt, timeout=15, max_tokens=200,
                           model=SONNET)
        if result and result.get("principle"):
            principle = result["principle"][:400]
            confidence = min(max(result.get("confidence", 0.8), 0.5), 0.95)
            return principle, confidence
    except Exception:
        pass

    return None, 0

def _retrain_tfidf(db):
    """Retrain TF-IDF model with current rules."""
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        all_rules = db.execute(
            "SELECT content FROM rules WHERE maturity <> 'deprecated'"
        ).fetchall()
        if len(all_rules) >= 3:
            texts = [r["content"] for r in all_rules]
            vectorizer = TfidfVectorizer(max_features=5000, stop_words="english")
            vectorizer.fit(texts)
            TFIDF_DIR.mkdir(exist_ok=True)
            pickle.dump(vectorizer, open(TFIDF_DIR / "vectorizer.pkl", "wb"))
            db.execute(
                "UPDATE meta SET value = '0', updated_at = datetime('now') WHERE key = 'tfidf_dirty'"
            )
    except Exception:
        pass

def _rebuild_graph():
    """Rebuild entity graph after consolidation."""
    try:
        from graph_builder import build_graph
        build_graph()
    except Exception:
        pass


# --------------- CLI ---------------

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--dry-run":
        print("Dry run: checking prerequisites...")
        db = get_db()
        total = db.execute("SELECT COUNT(*) FROM rules").fetchone()[0]
        unscored = db.execute(
            "SELECT COUNT(*) FROM rules WHERE quality_score = 0 AND maturity <> 'deprecated'"
        ).fetchone()[0]
        active = db.execute(
            "SELECT COUNT(*) FROM rules WHERE maturity <> 'deprecated'"
        ).fetchone()[0]
        db.close()
        print(f"Total rules: {total}")
        print(f"Active (non-deprecated): {active}")
        print(f"Unscored (quality=0): {unscored}")
        print(f"Quality threshold: {QUALITY_THRESHOLD}/4")
    else:
        verbose = "--verbose" in sys.argv or "-v" in sys.argv
        print("Running v2 LLM consolidation pipeline...")
        t0 = time.time()
        result = consolidate(verbose=verbose)
        elapsed = time.time() - t0
        print(f"\nCompleted in {elapsed:.1f}s")
        print(json.dumps(result, indent=2))
