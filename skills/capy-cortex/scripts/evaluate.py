#!/usr/bin/env python3
"""Capy Cortex - Evaluation Layer.
Measures rule quality, retrieval precision, learning velocity, and system health.
Bridge 5: Closes the feedback loop with measurable metrics."""

import json
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta

DB_PATH = Path(__file__).parent.parent / "cortex.db"


def get_db():
    db = sqlite3.connect(str(DB_PATH))
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA journal_mode=WAL")
    db.execute("PRAGMA busy_timeout=3000")
    return db


def evaluate_all():
    """Run all evaluation metrics. Returns comprehensive report."""
    return {
        "rule_quality": evaluate_rule_quality(),
        "retrieval_health": evaluate_retrieval_health(),
        "learning_velocity": evaluate_learning_velocity(),
        "feedback_loop": evaluate_feedback_loop(),
        "noise_ratio": evaluate_noise_ratio(),
        "bridge_health": evaluate_bridge_health(),
        "timestamp": datetime.now().isoformat(),
    }


def evaluate_rule_quality():
    """Measure quality of the rule corpus.
    High-quality = high confidence, high helpful_count, low harmful_count."""
    db = get_db()

    total = db.execute(
        "SELECT COUNT(*) FROM rules WHERE maturity != 'deprecated'"
    ).fetchone()[0]
    if total == 0:
        db.close()
        return {"score": 0.0, "total_rules": 0, "detail": "No rules in DB"}

    # Quality metrics
    high_conf = db.execute(
        "SELECT COUNT(*) FROM rules WHERE confidence >= 0.7 AND maturity != 'deprecated'"
    ).fetchone()[0]
    helped = db.execute(
        "SELECT COUNT(*) FROM rules WHERE helpful_count > 0 AND maturity != 'deprecated'"
    ).fetchone()[0]
    harmed = db.execute(
        "SELECT COUNT(*) FROM rules WHERE harmful_count > 0 AND maturity != 'deprecated'"
    ).fetchone()[0]
    avg_conf = db.execute(
        "SELECT AVG(confidence) FROM rules WHERE maturity != 'deprecated'"
    ).fetchone()[0] or 0
    avg_helpful = db.execute(
        "SELECT AVG(helpful_count) FROM rules WHERE maturity != 'deprecated'"
    ).fetchone()[0] or 0

    # Quality score: weighted combination
    conf_ratio = high_conf / total if total else 0
    help_ratio = helped / total if total else 0
    harm_ratio = harmed / total if total else 0

    score = (0.4 * conf_ratio + 0.3 * help_ratio + 0.3 * (1 - harm_ratio))
    score = min(max(score, 0.0), 1.0)

    db.close()
    return {
        "score": round(score, 3),
        "total_rules": total,
        "high_confidence_rules": high_conf,
        "helped_rules": helped,
        "harmed_rules": harmed,
        "avg_confidence": round(avg_conf, 3),
        "avg_helpful_count": round(avg_helpful, 2),
    }


def evaluate_retrieval_health():
    """Measure retrieval system health.
    Checks FTS5, TF-IDF, embeddings index status."""
    db = get_db()
    tfidf_dirty = db.execute(
        "SELECT value FROM meta WHERE key = 'tfidf_dirty'"
    ).fetchone()
    emb_dirty = db.execute(
        "SELECT value FROM meta WHERE key = 'embeddings_dirty'"
    ).fetchone()

    # Count indexed rules
    indexed = 0
    try:
        indexed = db.execute("SELECT COUNT(*) FROM rules_fts").fetchone()[0]
    except Exception:
        pass

    total = db.execute(
        "SELECT COUNT(*) FROM rules WHERE maturity != 'deprecated'"
    ).fetchone()[0]

    db.close()

    # Check index files
    tfidf_dir = Path(__file__).parent.parent / "tfidf"
    emb_dir = Path(__file__).parent.parent / "embeddings"

    tfidf_exists = (tfidf_dir / "vectorizer.pkl").exists()
    emb_exists = (emb_dir / "vectorizer.pkl").exists()

    issues = []
    if tfidf_dirty and tfidf_dirty[0] == "1":
        issues.append("TF-IDF model is stale")
    if emb_dirty and emb_dirty[0] == "1":
        issues.append("Embedding index is stale")
    if not tfidf_exists:
        issues.append("TF-IDF model not built")
    if not emb_exists:
        issues.append("Embedding index not built")
    if indexed < total:
        issues.append(f"FTS5 index incomplete ({indexed}/{total})")

    score = 1.0 - (len(issues) * 0.2)
    score = max(score, 0.0)

    return {
        "score": round(score, 3),
        "fts5_indexed": indexed,
        "tfidf_model": tfidf_exists,
        "tfidf_dirty": bool(tfidf_dirty and tfidf_dirty[0] == "1"),
        "embeddings_model": emb_exists,
        "embeddings_dirty": bool(emb_dirty and emb_dirty[0] == "1"),
        "issues": issues,
    }


def evaluate_learning_velocity():
    """Measure how fast the system is learning.
    Looks at rules added per session, event frequency, and maturity progression."""
    db = get_db()

    # Count sessions
    sessions = db.execute(
        "SELECT COUNT(*) FROM events WHERE event_type = 'session_reflection'"
    ).fetchone()[0]

    # Rules added in last 7 days
    week_ago = (datetime.now() - timedelta(days=7)).isoformat()
    recent_rules = db.execute(
        "SELECT COUNT(*) FROM rules WHERE created_at >= ?", (week_ago,)
    ).fetchone()[0]

    # Total rules
    total_rules = db.execute(
        "SELECT COUNT(*) FROM rules WHERE maturity != 'deprecated'"
    ).fetchone()[0]

    # Principles (consolidated wisdom)
    principles = db.execute("SELECT COUNT(*) FROM principles").fetchone()[0]

    # Events in last 7 days
    recent_events = db.execute(
        "SELECT COUNT(*) FROM events WHERE created_at >= ?", (week_ago,)
    ).fetchone()[0]

    # Deprecated rules (noise removed)
    deprecated = db.execute(
        "SELECT COUNT(*) FROM rules WHERE maturity = 'deprecated'"
    ).fetchone()[0]

    # Established rules (mature knowledge)
    established = db.execute(
        "SELECT COUNT(*) FROM rules WHERE maturity = 'established'"
    ).fetchone()[0]

    db.close()

    # Calculate velocity metrics
    rules_per_session = total_rules / max(sessions, 1)
    maturity_ratio = established / max(total_rules, 1)
    consolidation_ratio = principles / max(total_rules, 1)

    # Learning velocity score
    # Good system: adding rules, consolidating to principles, deprecating noise
    score = min(1.0,
        0.3 * min(rules_per_session / 5.0, 1.0) +  # Adding rules
        0.3 * maturity_ratio +                        # Maturing rules
        0.2 * consolidation_ratio +                   # Consolidating wisdom
        0.2 * min(recent_events / 20.0, 1.0)         # Active learning
    )

    return {
        "score": round(score, 3),
        "total_sessions": sessions,
        "total_rules": total_rules,
        "recent_rules_7d": recent_rules,
        "principles": principles,
        "established_rules": established,
        "deprecated_rules": deprecated,
        "recent_events_7d": recent_events,
        "rules_per_session": round(rules_per_session, 2),
    }


def evaluate_feedback_loop():
    """Measure feedback loop health.
    Checks: surfaced rules -> success credits -> helpful_count growth."""
    db = get_db()

    # Total surfaced rules
    total_surfaced = db.execute("SELECT COUNT(*) FROM surfaced_rules").fetchone()[0]

    # Credited surfaced rules
    credited = db.execute(
        "SELECT COUNT(*) FROM surfaced_rules WHERE credited = 1"
    ).fetchone()[0]

    # Rules with helpful_count > 0
    helped_rules = db.execute(
        "SELECT COUNT(*) FROM rules WHERE helpful_count > 0 AND maturity != 'deprecated'"
    ).fetchone()[0]

    # Total rules
    total_rules = db.execute(
        "SELECT COUNT(*) FROM rules WHERE maturity != 'deprecated'"
    ).fetchone()[0]

    # Success credit events
    credit_events = db.execute(
        "SELECT COUNT(*) FROM events WHERE event_type = 'success_credit'"
    ).fetchone()[0]

    db.close()

    # Credit ratio
    credit_ratio = credited / max(total_surfaced, 1)
    help_ratio = helped_rules / max(total_rules, 1)

    # Feedback loop score
    score = min(1.0,
        0.4 * credit_ratio +      # Credits flowing
        0.3 * help_ratio +          # Help counts growing
        0.3 * min(credit_events / 10.0, 1.0)  # Active crediting
    )

    return {
        "score": round(score, 3),
        "total_surfaced": total_surfaced,
        "credited": credited,
        "credit_ratio": round(credit_ratio, 3),
        "rules_with_help": helped_rules,
        "credit_events": credit_events,
    }


def evaluate_noise_ratio():
    """Measure noise in the system.
    Low noise = good. High unknown_error/generic rules = bad."""
    db = get_db()

    total = db.execute(
        "SELECT COUNT(*) FROM rules WHERE maturity != 'deprecated'"
    ).fetchone()[0]
    if total == 0:
        db.close()
        return {"score": 1.0, "noise_ratio": 0.0, "detail": "No rules"}

    # Count noise indicators
    unknown = db.execute(
        "SELECT COUNT(*) FROM rules WHERE category = 'unknown_error' AND maturity != 'deprecated'"
    ).fetchone()[0]
    low_conf = db.execute(
        "SELECT COUNT(*) FROM rules WHERE confidence < 0.3 AND maturity != 'deprecated'"
    ).fetchone()[0]
    no_evidence = db.execute(
        "SELECT COUNT(*) FROM rules WHERE (evidence IS NULL OR evidence = '[]') AND maturity != 'deprecated'"
    ).fetchone()[0]

    noise_count = unknown + low_conf
    noise_ratio = noise_count / total

    # Score: 1.0 = no noise, 0.0 = all noise
    score = max(0.0, 1.0 - noise_ratio)

    db.close()
    return {
        "score": round(score, 3),
        "noise_ratio": round(noise_ratio, 3),
        "unknown_error_rules": unknown,
        "low_confidence_rules": low_conf,
        "no_evidence_rules": no_evidence,
        "total_active_rules": total,
    }


def evaluate_bridge_health():
    """Measure integration bridge health."""
    db = get_db()

    claudeception_exports = db.execute(
        "SELECT COUNT(*) FROM events WHERE event_type = 'bridge_export_claudeception'"
    ).fetchone()[0]
    claudeception_imports = db.execute(
        "SELECT COUNT(*) FROM events WHERE event_type = 'bridge_import_claudeception'"
    ).fetchone()[0]
    forge_ingests = db.execute(
        "SELECT COUNT(*) FROM events WHERE event_type = 'bridge_forge_ingest'"
    ).fetchone()[0]

    # Check exported skill files
    export_dir = Path(__file__).parent.parent / "exported_skills"
    exported_files = len(list(export_dir.glob("*.md"))) if export_dir.exists() else 0

    db.close()

    # Bridge health: at least some activity
    active_bridges = sum([
        claudeception_exports > 0,
        claudeception_imports > 0,
        forge_ingests > 0,
    ])

    score = active_bridges / 3.0

    return {
        "score": round(score, 3),
        "claudeception_exports": claudeception_exports,
        "claudeception_imports": claudeception_imports,
        "forge_ingests": forge_ingests,
        "exported_skill_files": exported_files,
        "active_bridges": active_bridges,
    }


def generate_report():
    """Generate a human-readable evaluation report."""
    metrics = evaluate_all()
    lines = [
        "=" * 60,
        "CAPY CORTEX EVALUATION REPORT",
        f"Generated: {metrics['timestamp'][:19]}",
        "=" * 60,
        "",
    ]

    for section_name, section_data in metrics.items():
        if section_name == "timestamp":
            continue
        if not isinstance(section_data, dict):
            continue

        score = section_data.get("score", 0)
        grade = _score_to_grade(score)

        lines.append(f"  {section_name.replace('_', ' ').upper()}: {grade} ({score:.1%})")

        for k, v in section_data.items():
            if k == "score":
                continue
            if isinstance(v, list):
                if v:
                    lines.append(f"    {k}:")
                    for item in v:
                        lines.append(f"      - {item}")
            else:
                lines.append(f"    {k}: {v}")
        lines.append("")

    # Overall score
    scores = [
        v.get("score", 0)
        for v in metrics.values()
        if isinstance(v, dict) and "score" in v
    ]
    overall = sum(scores) / len(scores) if scores else 0
    grade = _score_to_grade(overall)

    lines.extend([
        "=" * 60,
        f"OVERALL HEALTH: {grade} ({overall:.1%})",
        "=" * 60,
    ])

    return "\n".join(lines)


def _score_to_grade(score):
    if score >= 0.9:
        return "EXCELLENT"
    if score >= 0.7:
        return "GOOD"
    if score >= 0.5:
        return "FAIR"
    if score >= 0.3:
        return "NEEDS WORK"
    return "CRITICAL"


# ---- CLI ----

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "json":
        print(json.dumps(evaluate_all(), indent=2))
    else:
        print(generate_report())
