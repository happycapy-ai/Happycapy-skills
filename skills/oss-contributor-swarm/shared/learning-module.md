# Learning Module

The Learning Module tracks contribution history and improves swarm performance over time.

## Purpose

1. **Track Success Patterns** - What works, what doesn't
2. **Avoid Known Issues** - Don't repeat mistakes
3. **Optimize Selection** - Prefer repos/issue types with high success
4. **Improve Response Time** - Learn maintainer preferences

## Data Structure

### contribution-history.json

```json
{
  "schema_version": "1.0.0",
  "last_updated": "ISO-8601",
  "stats": {
    "total_contributions": 150,
    "prs_created": 150,
    "prs_merged": 120,
    "prs_closed": 15,
    "prs_pending": 15,
    "success_rate": 0.80,
    "avg_time_to_merge_hours": 36
  },
  "contributions": [...],
  "success_patterns": {...},
  "repositories": {...},
  "maintainers": {...},
  "auto_fix_history": {...},
  "timing_analysis": {...}
}
```

## How Agents Use Learning Data

### Agent 0 (Repo Qualifier)

```python
def score_repo_with_learning(repo, history):
    base_score = calculate_base_score(repo)

    # Boost if previously successful
    if repo.full_name in history.repositories.successful:
        base_score += 15

    # Penalize if previously problematic
    if repo.full_name in history.repositories.avoid:
        return 0  # Skip entirely

    # Check maintainer history
    maintainer = history.maintainers.get(repo.owner)
    if maintainer:
        if maintainer.avg_response_hours < 24:
            base_score += 10
        if maintainer.rejection_rate > 0.5:
            base_score -= 20

    return base_score
```

### Agent 1 (Issue Scout)

```python
def score_issue_with_learning(issue, history):
    base_score = calculate_base_score(issue)

    # Boost preferred issue types
    if issue.type in history.success_patterns.best_issue_types[:3]:
        base_score += 10

    # Boost preferred languages
    if issue.language in history.success_patterns.best_languages[:3]:
        base_score += 5

    # Check issue age against optimal range
    optimal = history.success_patterns.optimal_issue_age_days
    if optimal.min <= issue.age_days <= optimal.max:
        base_score += 5

    return base_score
```

### Agent 8 (Review Responder)

```python
def handle_review_with_learning(review, history):
    repo_meta = history.repositories.metadata.get(repo)

    # Check if maintainer has known preferences
    if repo_meta and repo_meta.maintainer_notes:
        apply_known_preferences(repo_meta.maintainer_notes)

    # Check auto-fix success history
    if review.fix_type in history.auto_fix_history.successful_fix_types:
        confidence = "high"
        auto_fix(review)
    elif review.fix_type in history.auto_fix_history.failed_fix_types:
        confidence = "low"
        escalate()
```

## Recording Outcomes

### On PR Merge

```python
def record_merge(pr, contribution):
    history.stats.prs_merged += 1
    history.stats.success_rate = calculate_success_rate()

    # Add to successful repos
    if pr.repo not in history.repositories.successful:
        history.repositories.successful.append(pr.repo)

    # Record time to merge
    time_to_merge = (pr.merged_at - pr.created_at).hours
    update_avg_time_to_merge(time_to_merge)

    # Record maintainer data
    update_maintainer_stats(pr.repo.owner, positive=True)

    # Update success patterns
    update_best_issue_types(contribution.issue.type)
    update_best_languages(contribution.issue.language)

    # Record lessons learned
    contribution.lessons_learned = extract_lessons(pr)
    contribution.outcome = "merged"
```

### On PR Closed (Not Merged)

```python
def record_closure(pr, contribution, reason):
    history.stats.prs_closed += 1

    # Analyze why
    if reason == "duplicate":
        # Another PR merged first - speed issue
        contribution.lessons_learned.append("Need faster response")
    elif reason == "won't fix":
        # Issue was closed/rejected
        history.repositories.avoid.append(pr.repo)
    elif reason == "stale":
        # Maintainer unresponsive
        update_maintainer_stats(pr.repo.owner, slow=True)

    contribution.outcome = "closed"
```

### On Auto-Fix

```python
def record_auto_fix(fix_type, success):
    if success:
        if fix_type not in history.auto_fix_history.successful_fix_types:
            history.auto_fix_history.successful_fix_types.append(fix_type)
        history.auto_fix_history.total_auto_fixes += 1
    else:
        if fix_type not in history.auto_fix_history.failed_fix_types:
            history.auto_fix_history.failed_fix_types.append(fix_type)

    # Update success rate
    history.auto_fix_history.success_rate = calculate_auto_fix_rate()
```

## Pattern Analysis

### Issue Type Success Rates

```python
def analyze_issue_type_success():
    type_stats = {}
    for contrib in history.contributions:
        issue_type = contrib.issue.type
        if issue_type not in type_stats:
            type_stats[issue_type] = {"total": 0, "merged": 0}
        type_stats[issue_type]["total"] += 1
        if contrib.outcome == "merged":
            type_stats[issue_type]["merged"] += 1

    # Sort by success rate
    sorted_types = sorted(
        type_stats.items(),
        key=lambda x: x[1]["merged"] / max(x[1]["total"], 1),
        reverse=True
    )
    return sorted_types
```

### Repository Performance

```python
def analyze_repo_performance():
    repo_stats = {}
    for contrib in history.contributions:
        repo = contrib.repository.full_name
        if repo not in repo_stats:
            repo_stats[repo] = {
                "total": 0, "merged": 0,
                "avg_time_hours": [],
                "maintainer_responsive": True
            }
        repo_stats[repo]["total"] += 1
        if contrib.outcome == "merged":
            repo_stats[repo]["merged"] += 1
            repo_stats[repo]["avg_time_hours"].append(
                contrib.time_to_merge_hours
            )

    return repo_stats
```

## Reporting

### Daily Summary

```markdown
## OSS Contributor Swarm - Daily Report

**Date:** 2024-01-15

### Today's Activity
- Contributions attempted: 5
- PRs created: 5
- PRs merged: 3
- PRs pending: 2

### Success Rate
- Today: 60%
- Rolling 7-day: 75%
- All-time: 80%

### Top Performing
- Best repo: org/repo (100% merge rate)
- Best issue type: documentation (90% merge rate)
- Fastest merge: 2 hours

### Areas to Improve
- Avoid: slow-org/* (0% merge rate, 14+ day wait)
- Issue type to skip: feature-large (20% merge rate)

### Lessons Learned Today
1. maintainer@org prefers conventional commits
2. repo-x requires DCO sign-off
3. repo-y has slow CI (wait before pushing updates)
```

## Continuous Improvement Loop

```
┌─────────────────────────────────────────────────────────────┐
│                    LEARNING LOOP                             │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   1. Attempt contribution                                    │
│        │                                                     │
│        ▼                                                     │
│   2. Record outcome (merge/close/stale)                     │
│        │                                                     │
│        ▼                                                     │
│   3. Extract lessons                                         │
│        │                                                     │
│        ▼                                                     │
│   4. Update patterns                                         │
│        │                                                     │
│        ▼                                                     │
│   5. Adjust agent behavior                                   │
│        │                                                     │
│        └──────────────► Loop back to 1                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Files

- `./shared/contribution-history.json` - Main history data
- `./shared/learning-module.md` - This documentation
- `./logs/learning-updates.log` - Change log for history updates
