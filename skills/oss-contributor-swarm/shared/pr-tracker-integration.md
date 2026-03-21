# PR Tracker Integration Guide

This document describes how agents in the OSS Contributor Swarm integrate with the PR tracking system.

## Overview

The PR tracker (`./scripts/pr-tracker.sh`) maintains a history of all pull requests created by the swarm. This enables:

- **Historical analysis** - Understanding contribution patterns
- **Learning** - Identifying successful strategies
- **Metrics** - Tracking merge rates, response times, etc.
- **Prioritization** - Using past data to select future issues

## PR Tracker Commands

### Add a New PR

```bash
./scripts/pr-tracker.sh add \
  --repo "owner/repo" \
  --issue "123" \
  --pr "456" \
  --title "PR title" \
  --domain "documentation" \
  --score "5" \
  --type "docs" \
  --files "2" \
  --lines-added "50" \
  --lines-removed "10"
```

### Update PR Status

```bash
./scripts/pr-tracker.sh update "456" --repo "owner/repo" --fetch
```

### Query PR History

```bash
# List all PRs
./scripts/pr-tracker.sh list

# Show specific PR
./scripts/pr-tracker.sh show "456" --repo "owner/repo"

# Generate statistics
./scripts/pr-tracker.sh stats
```

## Agent Integration Points

### Agent 7: PR Creator

**When**: After successfully creating a PR via `gh pr create`

**Action**: Call `pr-tracker add` with full metadata

**Required Data**:
| Field | Description | Source |
|-------|-------------|--------|
| `--repo` | Repository (owner/name) | current-issue.json |
| `--issue` | Issue number | current-issue.json |
| `--pr` | PR number | gh pr create output |
| `--title` | PR title | PR creation |
| `--domain` | Contribution domain | issue-analysis.json |
| `--score` | Value score (1-10) | Computed |
| `--type` | Contribution type | issue-analysis.json |
| `--files` | Files changed count | code-changes.json |
| `--lines-added` | Lines added | code-changes.json |
| `--lines-removed` | Lines removed | code-changes.json |

**Example**:
```bash
# Extract PR number from creation
PR_URL=$(gh pr create --title "$TITLE" --body "$BODY")
PR_NUMBER=$(echo "$PR_URL" | grep -oP 'pull/\K[0-9]+')

# Add to tracker
./scripts/pr-tracker.sh add \
  --repo "$OWNER/$REPO" \
  --issue "$ISSUE_NUMBER" \
  --pr "$PR_NUMBER" \
  --title "$PR_TITLE" \
  --domain "$DOMAIN" \
  --score "$SCORE" \
  --type "$TYPE" \
  --files "$FILES_COUNT" \
  --lines-added "$ADDITIONS" \
  --lines-removed "$DELETIONS"
```

### Agent 8: Review Responder

**When**:
- After receiving a review
- After pushing changes (auto-fix or manual)
- When CI status changes
- When PR is merged or closed

**Action**: Call `pr-tracker update` to sync latest status

**Example**:
```bash
# Update after any status change
./scripts/pr-tracker.sh update "$PR_NUMBER" --repo "$OWNER/$REPO" --fetch
```

## Data Flow

```
Agent 7 (PR Creation)
    │
    ├── Creates PR via gh CLI
    │
    └── Calls: pr-tracker add --repo ... --pr ...
                    │
                    ▼
            ┌──────────────────┐
            │  PR History DB   │
            │  (JSON/SQLite)   │
            └──────────────────┘
                    ▲
                    │
Agent 8 (Review Monitoring)
    │
    ├── Monitors PR status
    │
    └── Calls: pr-tracker update --repo ... --fetch
```

## Value Score Calculation

The value score (1-10) estimates the contribution's impact:

| Factor | Weight | Scoring |
|--------|--------|---------|
| Complexity | 30% | trivial=1, easy=3, medium=5 |
| Issue demand | 25% | reactions + comments count |
| Repo popularity | 20% | stars tier (1-5) |
| Contribution type | 25% | docs=2, bug=4, feature=5 |

**Formula**:
```
score = (complexity * 0.3) + (demand * 0.25) + (popularity * 0.2) + (type * 0.25)
```

## PR Status Values

| Status | Description |
|--------|-------------|
| `open` | PR is open, awaiting review |
| `review_requested` | Changes requested by reviewer |
| `approved` | Approved, awaiting merge |
| `merged` | PR was merged |
| `closed` | PR was closed without merge |

## Error Handling

If pr-tracker command fails:

1. **Log the error** - Record in agent output JSON
2. **Continue workflow** - Don't block on tracker failures
3. **Retry later** - Tracker can be updated on next poll

```bash
# Safe tracker call with error handling
if ! ./scripts/pr-tracker.sh add ... 2>/dev/null; then
    echo "Warning: Failed to log PR to tracker"
    # Continue with workflow
fi
```

## Statistics and Reporting

The PR tracker provides statistics for learning:

```bash
# Get overall stats
./scripts/pr-tracker.sh stats

# Output example:
# Total PRs: 45
# Merged: 38 (84%)
# Closed: 5 (11%)
# Open: 2 (5%)
# Avg time to merge: 3.2 days
# Top domains: documentation (40%), bug-fix (35%), feature (25%)
```

## Configuration

The PR tracker stores data in:
- **History file**: `./data/pr-history.json`
- **Config file**: `./config/pr-tracker.yaml`

Environment variables:
- `PR_TRACKER_DATA_DIR` - Override data directory
- `PR_TRACKER_VERBOSE` - Enable verbose logging

## Best Practices

1. **Always add PRs immediately after creation** - Don't wait
2. **Update frequently during review** - Keep status current
3. **Record final outcome** - Ensure merged/closed is tracked
4. **Include all metadata** - More data enables better learning
5. **Handle errors gracefully** - Tracker failures shouldn't block workflow
