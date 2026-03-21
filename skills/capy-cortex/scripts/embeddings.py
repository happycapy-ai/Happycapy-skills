#!/usr/bin/env python3
"""Capy Cortex - Embedding-based semantic retrieval.
Uses TF-IDF embeddings for rules, then cosine similarity for retrieval.
Falls back to FTS5 if embeddings are unavailable."""

import json
import os
import sqlite3
import numpy as np
from pathlib import Path
import urllib.request
import urllib.error

DB_PATH = Path(__file__).parent.parent / "cortex.db"
EMBEDDINGS_DIR = Path(__file__).parent.parent / "embeddings"

# Provider-agnostic: reads from same env vars as llm_extract.py
_raw_url = os.environ.get("CORTEX_API_URL",
           os.environ.get("AI_GATEWAY_URL",
           os.environ.get("OPENAI_BASE_URL", "")))
if _raw_url:
    API_URL = _raw_url.rstrip("/")
    if not API_URL.endswith("/chat/completions"):
        API_URL = API_URL + "/chat/completions"
else:
    API_URL = ""
MODEL = os.environ.get("CORTEX_FAST_MODEL", "")
API_KEY = os.environ.get("CORTEX_API_KEY",
          os.environ.get("AI_GATEWAY_API_KEY",
          os.environ.get("OPENAI_API_KEY", "")))

# We use a simple approach: generate a compact text representation for each rule,
# then use TF-IDF with sklearn if available, or hash-based embeddings as fallback.
# For true neural embeddings, we'd need an embedding API endpoint.


def get_rule_embedding_text(rule_content, category):
    """Create a rich text representation for embedding."""
    return f"[{category}] {rule_content}"


def build_embedding_index():
    """Build/rebuild the embedding index from all active rules.
    Uses sklearn TfidfVectorizer with higher feature count for better semantics."""
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
    except ImportError:
        return False

    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    rows = db.execute("""
        SELECT id, content, category FROM rules
        WHERE maturity != 'deprecated'
        ORDER BY id
    """).fetchall()
    db.close()

    if len(rows) < 3:
        return False

    texts = [get_rule_embedding_text(r["content"], r["category"]) for r in rows]
    ids = [r["id"] for r in rows]

    vectorizer = TfidfVectorizer(
        max_features=10000,
        stop_words="english",
        ngram_range=(1, 2),  # Bigrams for better semantic capture
        sublinear_tf=True,    # Logarithmic TF for better scaling
    )
    matrix = vectorizer.fit_transform(texts)

    # Save index
    EMBEDDINGS_DIR.mkdir(exist_ok=True)
    import pickle
    with open(EMBEDDINGS_DIR / "vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)
    with open(EMBEDDINGS_DIR / "matrix.pkl", "wb") as f:
        pickle.dump(matrix, f)
    with open(EMBEDDINGS_DIR / "ids.json", "w") as f:
        json.dump(ids, f)

    # Mark as clean
    db2 = sqlite3.connect(str(DB_PATH))
    db2.execute("INSERT OR REPLACE INTO meta (key, value, updated_at) VALUES ('embeddings_dirty', '0', datetime('now'))")
    db2.commit()
    db2.close()

    return True


def semantic_search(query, top_k=10, workspace=None):
    """Search rules using embedding similarity.
    Returns list of (rule_id, similarity_score) tuples."""
    try:
        from sklearn.metrics.pairwise import cosine_similarity
        import pickle
    except ImportError:
        return []

    vec_path = EMBEDDINGS_DIR / "vectorizer.pkl"
    mat_path = EMBEDDINGS_DIR / "matrix.pkl"
    ids_path = EMBEDDINGS_DIR / "ids.json"

    if not all(p.exists() for p in [vec_path, mat_path, ids_path]):
        # Try to build index
        if not build_embedding_index():
            return []

    try:
        with open(vec_path, "rb") as f:
            vectorizer = pickle.load(f)
        with open(mat_path, "rb") as f:
            matrix = pickle.load(f)
        with open(ids_path) as f:
            ids = json.load(f)

        query_vec = vectorizer.transform([query])
        sims = cosine_similarity(query_vec, matrix)[0]

        # Get top results
        scored = list(zip(ids, sims))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

    except Exception:
        return []


def hybrid_retrieve(query, top_k=10, workspace=None):
    """Hybrid retrieval: combine FTS5 and embedding scores.
    Uses Reciprocal Rank Fusion (RRF) to merge results."""
    # Get FTS5 results
    fts_results = _fts5_search(query, limit=top_k * 3)

    # Get embedding results
    emb_results = semantic_search(query, top_k=top_k * 3)

    if not fts_results and not emb_results:
        return []

    # Reciprocal Rank Fusion (k=60 is standard)
    K = 60
    scores = {}

    for rank, (rule_id, _) in enumerate(fts_results):
        scores[rule_id] = scores.get(rule_id, 0) + 1.0 / (K + rank + 1)

    for rank, (rule_id, sim) in enumerate(emb_results):
        # Weight embedding results slightly higher for semantic matching
        scores[rule_id] = scores.get(rule_id, 0) + 1.2 / (K + rank + 1)

    # Sort by fused score
    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    # Fetch full rule data
    if not ranked:
        return []

    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    results = []
    for rule_id, score in ranked[:top_k]:
        row = db.execute("SELECT * FROM rules WHERE id = ?", (rule_id,)).fetchone()
        if row:
            results.append(dict(row))
    db.close()

    return results


def _fts5_search(query, limit=30):
    """FTS5 search returning (rule_id, rank) pairs."""
    try:
        db = sqlite3.connect(str(DB_PATH))
        safe_query = " OR ".join(
            w for w in query.split() if len(w) > 2 and w.isalnum()
        )
        if not safe_query:
            db.close()
            return []

        rows = db.execute("""
            SELECT r.id, rank FROM rules_fts
            JOIN rules r ON rules_fts.rowid = r.id
            WHERE rules_fts MATCH ? AND r.maturity != 'deprecated'
            ORDER BY rank LIMIT ?
        """, (safe_query, limit)).fetchall()
        db.close()
        return [(r[0], -r[1]) for r in rows]  # Negate rank (lower is better in FTS5)
    except Exception:
        return []


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "build":
            ok = build_embedding_index()
            print(f"Embedding index: {'BUILT' if ok else 'FAILED'}")
        elif cmd == "search":
            query = sys.argv[2] if len(sys.argv) > 2 else "git push"
            results = hybrid_retrieve(query, top_k=5)
            for r in results:
                print(f"  [{r['confidence']:.1f}|{r['category']}] {r['content'][:100]}")
        else:
            print(f"Usage: embeddings.py [build|search <query>]")
    else:
        print("Usage: embeddings.py [build|search <query>]")
