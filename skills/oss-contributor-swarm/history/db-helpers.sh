#!/usr/bin/env bash
#
# PR History Database Helper Functions
# Version: 1.0.0
#
# Usage: source this file to use helper functions
# Requirements: jq (JSON processor)
#

# Database file path
DB_FILE="${PR_HISTORY_DB:-/home/node/.claude/skills/oss-contributor-swarm/history/pr-history.json}"
BACKUP_FILE="${DB_FILE%.json}.backup.json"
SCHEMA_FILE="${DB_FILE%.json}.schema.json"

# Check dependencies
check_dependencies() {
    if ! command -v jq &> /dev/null; then
        echo "Error: jq is required but not installed" >&2
        return 1
    fi
}

# Initialize database if it doesn't exist
db_init() {
    if [[ ! -f "$DB_FILE" ]]; then
        local timestamp
        timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
        cat > "$DB_FILE" << EOF
{
  "metadata": {
    "version": "1.0.0",
    "schema_version": "1.0",
    "last_updated": "$timestamp",
    "created_at": "$timestamp",
    "description": "PR History Tracking Database for OSS Contributor Swarm",
    "backup_enabled": true,
    "backup_frequency": "on_write"
  },
  "prs": [],
  "statistics": {
    "total_prs": 0,
    "merged_prs": 0,
    "open_prs": 0,
    "closed_prs": 0,
    "rejected_prs": 0,
    "merge_rate": 0,
    "repos_contributed": 0,
    "unique_repos": [],
    "domains": {"ROS2": 0, "AI_ML": 0, "Web": 0, "CLI": 0, "Other": 0},
    "contribution_types": {"bugfix": 0, "feature": 0, "docs": 0, "test": 0, "refactor": 0, "typo": 0},
    "total_lines_added": 0,
    "total_lines_removed": 0,
    "total_files_changed": 0,
    "avg_value_score": 0,
    "avg_review_comments": 0,
    "avg_time_to_merge_hours": null,
    "last_calculated": "$timestamp"
  },
  "repositories": [],
  "domains": {
    "ROS2": {"count": 0, "repositories": [], "merged": 0, "open": 0, "avg_value_score": 0},
    "AI_ML": {"count": 0, "repositories": [], "merged": 0, "open": 0, "avg_value_score": 0},
    "Web": {"count": 0, "repositories": [], "merged": 0, "open": 0, "avg_value_score": 0},
    "CLI": {"count": 0, "repositories": [], "merged": 0, "open": 0, "avg_value_score": 0},
    "Other": {"count": 0, "repositories": [], "merged": 0, "open": 0, "avg_value_score": 0}
  },
  "_schema": {
    "pr_statuses": ["open", "merged", "closed", "rejected"],
    "contribution_types": ["bugfix", "feature", "docs", "test", "refactor", "typo"],
    "domains": ["ROS2", "AI_ML", "Web", "CLI", "Other"],
    "review_states": ["pending", "approved", "changes_requested", "commented"]
  }
}
EOF
        echo "Database initialized at: $DB_FILE"
    fi
}

# Create backup before write
db_backup() {
    if [[ -f "$DB_FILE" ]]; then
        cp "$DB_FILE" "$BACKUP_FILE"
    fi
}

# Generate UUID v4
generate_uuid() {
    if command -v uuidgen &> /dev/null; then
        uuidgen | tr '[:upper:]' '[:lower:]'
    else
        # Fallback using /dev/urandom
        local hex
        hex=$(od -An -tx1 -N16 /dev/urandom | tr -d ' \n')
        printf '%s-%s-%s-%s-%s\n' \
            "${hex:0:8}" \
            "${hex:8:4}" \
            "4${hex:13:3}" \
            "$(printf '%x' $((0x8 | (0x${hex:16:1} & 0x3))))${hex:17:3}" \
            "${hex:20:12}"
    fi
}

# Update timestamp in metadata
db_update_timestamp() {
    local timestamp
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    jq --arg ts "$timestamp" '.metadata.last_updated = $ts' "$DB_FILE" > "${DB_FILE}.tmp" && mv "${DB_FILE}.tmp" "$DB_FILE"
}

# =============================================================================
# CREATE Operations
# =============================================================================

# Add a new PR record
# Usage: db_add_pr '<json_object>'
db_add_pr() {
    check_dependencies || return 1
    local pr_json="$1"
    local uuid
    uuid=$(generate_uuid)
    local timestamp
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    db_backup

    # Add id and internal metadata to the PR
    local enriched_pr
    enriched_pr=$(echo "$pr_json" | jq --arg id "$uuid" --arg ts "$timestamp" '
        . + {
            "id": $id,
            "_internal": {
                "created_by": "db_add_pr",
                "created_at": $ts,
                "last_modified_by": "db_add_pr",
                "last_modified_at": $ts
            }
        }
    ')

    # Add to database
    jq --argjson pr "$enriched_pr" '.prs += [$pr]' "$DB_FILE" > "${DB_FILE}.tmp" && mv "${DB_FILE}.tmp" "$DB_FILE"

    # Recalculate statistics
    db_recalculate_stats

    db_update_timestamp
    echo "$uuid"
}

# =============================================================================
# READ Operations
# =============================================================================

# Get all PRs
# Usage: db_get_all_prs
db_get_all_prs() {
    check_dependencies || return 1
    jq '.prs' "$DB_FILE"
}

# Get PR by ID
# Usage: db_get_pr_by_id '<uuid>'
db_get_pr_by_id() {
    check_dependencies || return 1
    local id="$1"
    jq --arg id "$id" '.prs[] | select(.id == $id)' "$DB_FILE"
}

# Get PR by PR number and repository
# Usage: db_get_pr_by_number '<owner>/<repo>' <pr_number>
db_get_pr_by_number() {
    check_dependencies || return 1
    local repo="$1"
    local pr_number="$2"
    jq --arg repo "$repo" --argjson num "$pr_number" \
        '.prs[] | select(.repository.full_name == $repo and .pr.number == $num)' "$DB_FILE"
}

# List PRs with filters
# Usage: db_list_prs [--status=<status>] [--repo=<owner/repo>] [--domain=<domain>]
db_list_prs() {
    check_dependencies || return 1
    local status="" repo="" domain=""

    for arg in "$@"; do
        case "$arg" in
            --status=*) status="${arg#*=}" ;;
            --repo=*) repo="${arg#*=}" ;;
            --domain=*) domain="${arg#*=}" ;;
        esac
    done

    local filter="."
    [[ -n "$status" ]] && filter="$filter | select(.pr.status == \"$status\")"
    [[ -n "$repo" ]] && filter="$filter | select(.repository.full_name == \"$repo\")"
    [[ -n "$domain" ]] && filter="$filter | select(.contribution.domain == \"$domain\")"

    jq ".prs[] | $filter" "$DB_FILE"
}

# Get statistics
# Usage: db_get_stats
db_get_stats() {
    check_dependencies || return 1
    jq '.statistics' "$DB_FILE"
}

# Get repositories summary
# Usage: db_get_repositories
db_get_repositories() {
    check_dependencies || return 1
    jq '.repositories' "$DB_FILE"
}

# Get domain breakdown
# Usage: db_get_domains
db_get_domains() {
    check_dependencies || return 1
    jq '.domains' "$DB_FILE"
}

# Count PRs
# Usage: db_count_prs [--status=<status>]
db_count_prs() {
    check_dependencies || return 1
    local status=""

    for arg in "$@"; do
        case "$arg" in
            --status=*) status="${arg#*=}" ;;
        esac
    done

    if [[ -n "$status" ]]; then
        jq --arg status "$status" '[.prs[] | select(.pr.status == $status)] | length' "$DB_FILE"
    else
        jq '.prs | length' "$DB_FILE"
    fi
}

# =============================================================================
# UPDATE Operations
# =============================================================================

# Update PR status
# Usage: db_update_pr_status '<uuid>' '<new_status>'
db_update_pr_status() {
    check_dependencies || return 1
    local id="$1"
    local new_status="$2"
    local timestamp
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    db_backup

    jq --arg id "$id" --arg status "$new_status" --arg ts "$timestamp" '
        .prs = [.prs[] | if .id == $id then
            .pr.status = $status |
            .pr.updated_at = $ts |
            ._internal.last_modified_at = $ts |
            ._internal.last_modified_by = "db_update_pr_status" |
            (if $status == "merged" then .pr.merged_at = $ts else . end) |
            (if $status == "closed" or $status == "rejected" then .pr.closed_at = $ts else . end)
        else . end]
    ' "$DB_FILE" > "${DB_FILE}.tmp" && mv "${DB_FILE}.tmp" "$DB_FILE"

    db_recalculate_stats
    db_update_timestamp
}

# Update PR review info
# Usage: db_update_pr_review '<uuid>' '<review_json>'
db_update_pr_review() {
    check_dependencies || return 1
    local id="$1"
    local review_json="$2"
    local timestamp
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    db_backup

    jq --arg id "$id" --argjson review "$review_json" --arg ts "$timestamp" '
        .prs = [.prs[] | if .id == $id then
            .review = (.review // {}) + $review |
            ._internal.last_modified_at = $ts |
            ._internal.last_modified_by = "db_update_pr_review"
        else . end]
    ' "$DB_FILE" > "${DB_FILE}.tmp" && mv "${DB_FILE}.tmp" "$DB_FILE"

    db_recalculate_stats
    db_update_timestamp
}

# Add timeline event to PR
# Usage: db_add_timeline_event '<uuid>' '<event>' '<description>'
db_add_timeline_event() {
    check_dependencies || return 1
    local id="$1"
    local event="$2"
    local description="$3"
    local timestamp
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    db_backup

    jq --arg id "$id" --arg event "$event" --arg desc "$description" --arg ts "$timestamp" '
        .prs = [.prs[] | if .id == $id then
            .timeline = (.timeline // []) + [{"event": $event, "timestamp": $ts, "description": $desc}] |
            ._internal.last_modified_at = $ts |
            ._internal.last_modified_by = "db_add_timeline_event"
        else . end]
    ' "$DB_FILE" > "${DB_FILE}.tmp" && mv "${DB_FILE}.tmp" "$DB_FILE"

    db_update_timestamp
}

# Add note to PR
# Usage: db_add_note '<uuid>' '<note>'
db_add_note() {
    check_dependencies || return 1
    local id="$1"
    local note="$2"
    local timestamp
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    db_backup

    jq --arg id "$id" --arg note "$note" --arg ts "$timestamp" '
        .prs = [.prs[] | if .id == $id then
            .notes = (.notes // []) + [$note] |
            ._internal.last_modified_at = $ts |
            ._internal.last_modified_by = "db_add_note"
        else . end]
    ' "$DB_FILE" > "${DB_FILE}.tmp" && mv "${DB_FILE}.tmp" "$DB_FILE"

    db_update_timestamp
}

# =============================================================================
# DELETE Operations
# =============================================================================

# Delete PR by ID
# Usage: db_delete_pr '<uuid>'
db_delete_pr() {
    check_dependencies || return 1
    local id="$1"

    db_backup

    jq --arg id "$id" '.prs = [.prs[] | select(.id != $id)]' "$DB_FILE" > "${DB_FILE}.tmp" && mv "${DB_FILE}.tmp" "$DB_FILE"

    db_recalculate_stats
    db_update_timestamp
}

# =============================================================================
# Statistics Recalculation
# =============================================================================

# Recalculate all statistics
# Usage: db_recalculate_stats
db_recalculate_stats() {
    check_dependencies || return 1
    local timestamp
    timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    jq --arg ts "$timestamp" '
        # Calculate basic counts
        .statistics.total_prs = (.prs | length) |
        .statistics.merged_prs = ([.prs[] | select(.pr.status == "merged")] | length) |
        .statistics.open_prs = ([.prs[] | select(.pr.status == "open")] | length) |
        .statistics.closed_prs = ([.prs[] | select(.pr.status == "closed")] | length) |
        .statistics.rejected_prs = ([.prs[] | select(.pr.status == "rejected")] | length) |

        # Calculate merge rate
        .statistics.merge_rate = (if .statistics.total_prs > 0 then
            ((.statistics.merged_prs / .statistics.total_prs) * 100 | floor)
        else 0 end) |

        # Unique repos
        .statistics.unique_repos = ([.prs[].repository.full_name] | unique) |
        .statistics.repos_contributed = (.statistics.unique_repos | length) |

        # Domain counts
        .statistics.domains.ROS2 = ([.prs[] | select(.contribution.domain == "ROS2")] | length) |
        .statistics.domains.AI_ML = ([.prs[] | select(.contribution.domain == "AI_ML")] | length) |
        .statistics.domains.Web = ([.prs[] | select(.contribution.domain == "Web")] | length) |
        .statistics.domains.CLI = ([.prs[] | select(.contribution.domain == "CLI")] | length) |
        .statistics.domains.Other = ([.prs[] | select(.contribution.domain == "Other")] | length) |

        # Contribution type counts
        .statistics.contribution_types.bugfix = ([.prs[] | select(.contribution.type == "bugfix")] | length) |
        .statistics.contribution_types.feature = ([.prs[] | select(.contribution.type == "feature")] | length) |
        .statistics.contribution_types.docs = ([.prs[] | select(.contribution.type == "docs")] | length) |
        .statistics.contribution_types.test = ([.prs[] | select(.contribution.type == "test")] | length) |
        .statistics.contribution_types.refactor = ([.prs[] | select(.contribution.type == "refactor")] | length) |
        .statistics.contribution_types.typo = ([.prs[] | select(.contribution.type == "typo")] | length) |

        # Line counts
        .statistics.total_lines_added = ([.prs[].contribution.lines_added] | add // 0) |
        .statistics.total_lines_removed = ([.prs[].contribution.lines_removed] | add // 0) |
        .statistics.total_files_changed = ([.prs[].contribution.files_changed | length] | add // 0) |

        # Averages
        .statistics.avg_value_score = (if (.prs | length) > 0 then
            (([.prs[].contribution.value_score] | add) / (.prs | length) | floor)
        else 0 end) |
        .statistics.avg_review_comments = (if (.prs | length) > 0 then
            (([.prs[].review.comments_count // 0] | add) / (.prs | length) | . * 10 | floor | . / 10)
        else 0 end) |

        .statistics.last_calculated = $ts |

        # Update repositories summary
        .repositories = ([.prs | group_by(.repository.full_name)[] | {
            full_name: .[0].repository.full_name,
            owner: .[0].repository.owner,
            name: .[0].repository.name,
            url: .[0].repository.url,
            pr_count: length,
            merged_count: ([.[] | select(.pr.status == "merged")] | length),
            first_contribution: ([.[].pr.created_at] | sort | first),
            last_contribution: ([.[].pr.created_at] | sort | last),
            domain: .[0].contribution.domain
        }]) |

        # Update domain breakdown
        .domains.ROS2 = {
            count: ([.prs[] | select(.contribution.domain == "ROS2")] | length),
            repositories: ([.prs[] | select(.contribution.domain == "ROS2") | .repository.full_name] | unique),
            merged: ([.prs[] | select(.contribution.domain == "ROS2" and .pr.status == "merged")] | length),
            open: ([.prs[] | select(.contribution.domain == "ROS2" and .pr.status == "open")] | length),
            avg_value_score: (if ([.prs[] | select(.contribution.domain == "ROS2")] | length) > 0 then
                (([.prs[] | select(.contribution.domain == "ROS2") | .contribution.value_score] | add) / ([.prs[] | select(.contribution.domain == "ROS2")] | length) | floor)
            else 0 end)
        } |
        .domains.AI_ML = {
            count: ([.prs[] | select(.contribution.domain == "AI_ML")] | length),
            repositories: ([.prs[] | select(.contribution.domain == "AI_ML") | .repository.full_name] | unique),
            merged: ([.prs[] | select(.contribution.domain == "AI_ML" and .pr.status == "merged")] | length),
            open: ([.prs[] | select(.contribution.domain == "AI_ML" and .pr.status == "open")] | length),
            avg_value_score: (if ([.prs[] | select(.contribution.domain == "AI_ML")] | length) > 0 then
                (([.prs[] | select(.contribution.domain == "AI_ML") | .contribution.value_score] | add) / ([.prs[] | select(.contribution.domain == "AI_ML")] | length) | floor)
            else 0 end)
        } |
        .domains.Web = {
            count: ([.prs[] | select(.contribution.domain == "Web")] | length),
            repositories: ([.prs[] | select(.contribution.domain == "Web") | .repository.full_name] | unique),
            merged: ([.prs[] | select(.contribution.domain == "Web" and .pr.status == "merged")] | length),
            open: ([.prs[] | select(.contribution.domain == "Web" and .pr.status == "open")] | length),
            avg_value_score: (if ([.prs[] | select(.contribution.domain == "Web")] | length) > 0 then
                (([.prs[] | select(.contribution.domain == "Web") | .contribution.value_score] | add) / ([.prs[] | select(.contribution.domain == "Web")] | length) | floor)
            else 0 end)
        } |
        .domains.CLI = {
            count: ([.prs[] | select(.contribution.domain == "CLI")] | length),
            repositories: ([.prs[] | select(.contribution.domain == "CLI") | .repository.full_name] | unique),
            merged: ([.prs[] | select(.contribution.domain == "CLI" and .pr.status == "merged")] | length),
            open: ([.prs[] | select(.contribution.domain == "CLI" and .pr.status == "open")] | length),
            avg_value_score: (if ([.prs[] | select(.contribution.domain == "CLI")] | length) > 0 then
                (([.prs[] | select(.contribution.domain == "CLI") | .contribution.value_score] | add) / ([.prs[] | select(.contribution.domain == "CLI")] | length) | floor)
            else 0 end)
        } |
        .domains.Other = {
            count: ([.prs[] | select(.contribution.domain == "Other")] | length),
            repositories: ([.prs[] | select(.contribution.domain == "Other") | .repository.full_name] | unique),
            merged: ([.prs[] | select(.contribution.domain == "Other" and .pr.status == "merged")] | length),
            open: ([.prs[] | select(.contribution.domain == "Other" and .pr.status == "open")] | length),
            avg_value_score: (if ([.prs[] | select(.contribution.domain == "Other")] | length) > 0 then
                (([.prs[] | select(.contribution.domain == "Other") | .contribution.value_score] | add) / ([.prs[] | select(.contribution.domain == "Other")] | length) | floor)
            else 0 end)
        }
    ' "$DB_FILE" > "${DB_FILE}.tmp" && mv "${DB_FILE}.tmp" "$DB_FILE"
}

# =============================================================================
# Export Functions
# =============================================================================

# Export to JSON
# Usage: db_export_json [output_file]
db_export_json() {
    check_dependencies || return 1
    local output="${1:-/home/node/.claude/skills/oss-contributor-swarm/history/exports/pr-history-export.json}"
    mkdir -p "$(dirname "$output")"
    jq '.' "$DB_FILE" > "$output"
    echo "Exported to: $output"
}

# Export to CSV
# Usage: db_export_csv [output_file]
db_export_csv() {
    check_dependencies || return 1
    local output="${1:-/home/node/.claude/skills/oss-contributor-swarm/history/exports/pr-history-export.csv}"
    mkdir -p "$(dirname "$output")"

    # Header
    echo "id,repository,pr_number,pr_title,status,domain,type,value_score,lines_added,lines_removed,created_at,merged_at" > "$output"

    # Data rows
    jq -r '.prs[] | [
        .id,
        .repository.full_name,
        .pr.number,
        (.pr.title | gsub(","; ";")),
        .pr.status,
        .contribution.domain,
        .contribution.type,
        .contribution.value_score,
        .contribution.lines_added,
        .contribution.lines_removed,
        .pr.created_at,
        (.pr.merged_at // "")
    ] | @csv' "$DB_FILE" >> "$output"

    echo "Exported to: $output"
}

# =============================================================================
# Validation
# =============================================================================

# Validate database against schema (requires jsonschema or ajv)
# Usage: db_validate
db_validate() {
    check_dependencies || return 1

    # Basic validation using jq
    local errors=0

    # Check required top-level keys
    for key in metadata prs statistics repositories domains; do
        if ! jq -e ".$key" "$DB_FILE" > /dev/null 2>&1; then
            echo "Error: Missing required key: $key" >&2
            ((errors++))
        fi
    done

    # Check all PRs have required fields
    local missing_fields
    missing_fields=$(jq -r '.prs[] | select(.id == null or .repository == null or .pr == null or .contribution == null) | .id // "unknown"' "$DB_FILE")
    if [[ -n "$missing_fields" ]]; then
        echo "Error: PRs missing required fields: $missing_fields" >&2
        ((errors++))
    fi

    # Check status values
    local invalid_status
    invalid_status=$(jq -r '.prs[] | select(.pr.status != "open" and .pr.status != "merged" and .pr.status != "closed" and .pr.status != "rejected") | .id' "$DB_FILE")
    if [[ -n "$invalid_status" ]]; then
        echo "Error: PRs with invalid status: $invalid_status" >&2
        ((errors++))
    fi

    if [[ $errors -eq 0 ]]; then
        echo "Validation passed"
        return 0
    else
        echo "Validation failed with $errors error(s)" >&2
        return 1
    fi
}

# =============================================================================
# Utility Functions
# =============================================================================

# Print database info
# Usage: db_info
db_info() {
    check_dependencies || return 1
    echo "PR History Database Information"
    echo "================================"
    echo "Database file: $DB_FILE"
    echo "Schema version: $(jq -r '.metadata.schema_version' "$DB_FILE")"
    echo "Last updated: $(jq -r '.metadata.last_updated' "$DB_FILE")"
    echo ""
    echo "Statistics:"
    echo "  Total PRs: $(jq -r '.statistics.total_prs' "$DB_FILE")"
    echo "  Merged: $(jq -r '.statistics.merged_prs' "$DB_FILE")"
    echo "  Open: $(jq -r '.statistics.open_prs' "$DB_FILE")"
    echo "  Merge rate: $(jq -r '.statistics.merge_rate' "$DB_FILE")%"
    echo "  Repos: $(jq -r '.statistics.repos_contributed' "$DB_FILE")"
}

# Restore from backup
# Usage: db_restore
db_restore() {
    if [[ -f "$BACKUP_FILE" ]]; then
        cp "$BACKUP_FILE" "$DB_FILE"
        echo "Restored from backup: $BACKUP_FILE"
    else
        echo "No backup file found: $BACKUP_FILE" >&2
        return 1
    fi
}

# Print usage
db_help() {
    cat << 'EOF'
PR History Database Helper Functions
====================================

CREATE:
  db_add_pr '<json_object>'          Add a new PR record

READ:
  db_get_all_prs                     Get all PR records
  db_get_pr_by_id '<uuid>'           Get PR by ID
  db_get_pr_by_number '<repo>' <num> Get PR by repository and number
  db_list_prs [filters]              List PRs with optional filters
                                     --status=open|merged|closed|rejected
                                     --repo=<owner/repo>
                                     --domain=ROS2|AI_ML|Web|CLI|Other
  db_get_stats                       Get statistics
  db_get_repositories                Get repository summary
  db_get_domains                     Get domain breakdown
  db_count_prs [--status=<status>]   Count PRs

UPDATE:
  db_update_pr_status '<uuid>' '<status>'  Update PR status
  db_update_pr_review '<uuid>' '<json>'    Update review info
  db_add_timeline_event '<uuid>' '<event>' '<desc>'  Add timeline event
  db_add_note '<uuid>' '<note>'            Add note to PR

DELETE:
  db_delete_pr '<uuid>'              Delete PR by ID

EXPORT:
  db_export_json [output_file]       Export to JSON
  db_export_csv [output_file]        Export to CSV

UTILITY:
  db_init                            Initialize empty database
  db_recalculate_stats               Recalculate all statistics
  db_validate                        Validate database
  db_info                            Print database info
  db_backup                          Create backup
  db_restore                         Restore from backup
  generate_uuid                      Generate new UUID
  db_help                            Show this help

Environment Variables:
  PR_HISTORY_DB                      Override default database path
EOF
}

# Auto-check dependencies on source
check_dependencies
