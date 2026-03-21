#!/bin/bash
# PR Tracker CLI - Command line interface for PR history management
# Part of OSS Contributor Swarm v3.0

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
HISTORY_FILE="$SKILL_DIR/history/pr-history.json"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Ensure history directory exists
mkdir -p "$SKILL_DIR/history"

# Initialize history file if it doesn't exist
init_history() {
    if [[ ! -f "$HISTORY_FILE" ]]; then
        cat > "$HISTORY_FILE" << 'EOF'
{
  "metadata": {
    "version": "1.0.0",
    "schema_version": "1.0",
    "last_updated": null,
    "created_at": null,
    "description": "PR History Tracking Database for OSS Contributor Swarm"
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
    "domains": {},
    "contribution_types": {}
  },
  "repositories": [],
  "domains": {}
}
EOF
        echo "Initialized new PR history file at $HISTORY_FILE"
    fi
}

# Show statistics
show_stats() {
    init_history

    echo -e "${CYAN}=======================================================================${NC}"
    echo -e "${CYAN}           PR HISTORY STATISTICS - OSS CONTRIBUTOR SWARM              ${NC}"
    echo -e "${CYAN}=======================================================================${NC}"
    echo ""

    local stats=$(jq '.statistics' "$HISTORY_FILE")
    local total=$(echo "$stats" | jq -r '.total_prs')
    local merged=$(echo "$stats" | jq -r '.merged_prs')
    local open=$(echo "$stats" | jq -r '.open_prs')
    local closed=$(echo "$stats" | jq -r '.closed_prs')
    local repos=$(echo "$stats" | jq -r '.repos_contributed')
    local merge_rate=$(echo "$stats" | jq -r '.merge_rate')
    local lines_added=$(echo "$stats" | jq -r '.total_lines_added // 0')
    local lines_removed=$(echo "$stats" | jq -r '.total_lines_removed // 0')

    echo -e "${GREEN}  Total PRs:${NC}        $total"
    echo -e "${GREEN}  Merged:${NC}           $merged"
    echo -e "${YELLOW}  Open:${NC}             $open"
    echo -e "${RED}  Closed/Rejected:${NC}  $closed"
    echo -e "${BLUE}  Repos:${NC}            $repos"
    echo -e "${CYAN}  Merge Rate:${NC}       ${merge_rate}%"
    echo ""
    echo -e "${GREEN}  Lines Added:${NC}      +$lines_added"
    echo -e "${RED}  Lines Removed:${NC}    -$lines_removed"
    echo ""

    echo -e "${CYAN}------------------- By Domain -------------------${NC}"
    jq -r '.statistics.domains | to_entries[] | select(.value > 0) | "  \(.key): \(.value)"' "$HISTORY_FILE" 2>/dev/null || echo "  No domain data"
    echo ""

    echo -e "${CYAN}------------------- By Type -------------------${NC}"
    jq -r '.statistics.contribution_types | to_entries[] | select(.value > 0) | "  \(.key): \(.value)"' "$HISTORY_FILE" 2>/dev/null || echo "  No type data"
    echo ""

    local last_updated=$(jq -r '.metadata.last_updated // "Never"' "$HISTORY_FILE")
    echo -e "${BLUE}Last Updated:${NC} $last_updated"
}

# List all PRs
list_prs() {
    init_history

    local filter="${1:-all}"

    echo -e "${CYAN}=======================================================================${NC}"
    echo -e "${CYAN}                    PR LIST ($filter)                                  ${NC}"
    echo -e "${CYAN}=======================================================================${NC}"
    echo ""

    local pr_count=$(jq '.prs | length' "$HISTORY_FILE")

    if [[ "$pr_count" -eq 0 ]]; then
        echo -e "${YELLOW}No PRs recorded yet.${NC}"
        return
    fi

    case "$filter" in
        open)
            jq -r '.prs[] | select(.pr.status == "open") | "[\(.pr.status | ascii_upcase)] \(.repository.full_name)#\(.pr.number): \(.pr.title)"' "$HISTORY_FILE"
            ;;
        merged)
            jq -r '.prs[] | select(.pr.status == "merged") | "[\(.pr.status | ascii_upcase)] \(.repository.full_name)#\(.pr.number): \(.pr.title)"' "$HISTORY_FILE"
            ;;
        closed)
            jq -r '.prs[] | select(.pr.status == "closed" or .pr.status == "rejected") | "[\(.pr.status | ascii_upcase)] \(.repository.full_name)#\(.pr.number): \(.pr.title)"' "$HISTORY_FILE"
            ;;
        *)
            jq -r '.prs[] | "[\(.pr.status | ascii_upcase)] \(.repository.full_name)#\(.pr.number): \(.pr.title)"' "$HISTORY_FILE"
            ;;
    esac
}

# Show details for a specific PR
show_pr() {
    local pr_id="$1"

    if [[ -z "$pr_id" ]]; then
        echo -e "${RED}Error: Please provide a PR ID or number${NC}"
        exit 1
    fi

    init_history

    local pr_data=$(jq ".prs[] | select(.id == \"$pr_id\" or .pr.number == $pr_id)" "$HISTORY_FILE" 2>/dev/null)

    if [[ -z "$pr_data" ]]; then
        echo -e "${RED}PR not found: $pr_id${NC}"
        exit 1
    fi

    echo -e "${CYAN}=======================================================================${NC}"
    echo -e "${CYAN}                       PR DETAILS                                      ${NC}"
    echo -e "${CYAN}=======================================================================${NC}"
    echo ""

    echo "$pr_data" | jq -r '"Repository: \(.repository.full_name)"'
    echo "$pr_data" | jq -r '"PR #\(.pr.number): \(.pr.title)"'
    echo "$pr_data" | jq -r '"Status: \(.pr.status)"'
    echo "$pr_data" | jq -r '"URL: \(.pr.url)"'
    echo ""
    echo "$pr_data" | jq -r '"Issue: #\(.issue.number) - \(.issue.title)"'
    echo "$pr_data" | jq -r '"Type: \(.contribution.type)"'
    echo "$pr_data" | jq -r '"Domain: \(.contribution.domain)"'
    echo ""
    echo "$pr_data" | jq -r '"Lines: +\(.contribution.lines_added) / -\(.contribution.lines_removed)"'
    echo "$pr_data" | jq -r '"Files Changed: \(.contribution.files_changed | length)"'
    echo ""
    echo -e "${CYAN}Timeline:${NC}"
    echo "$pr_data" | jq -r '.timeline[] | "  [\(.timestamp)] \(.event): \(.description)"'
}

# Add a new PR record
add_pr() {
    local repo="$1"
    local pr_num="$2"
    local issue_num="$3"
    local title="$4"

    if [[ -z "$repo" || -z "$pr_num" ]]; then
        echo -e "${RED}Usage: pr-tracker.sh add <owner/repo> <pr_number> [issue_number] [title]${NC}"
        exit 1
    fi

    init_history

    local owner=$(echo "$repo" | cut -d'/' -f1)
    local name=$(echo "$repo" | cut -d'/' -f2)
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local uuid=$(cat /proc/sys/kernel/random/uuid 2>/dev/null || uuidgen 2>/dev/null || echo "pr-$pr_num-$(date +%s)")

    # Fetch PR details from GitHub if possible
    local pr_title="$title"
    local pr_url="https://github.com/$repo/pull/$pr_num"
    local issue_url=""
    local issue_title=""

    if command -v gh &> /dev/null; then
        pr_title=$(gh pr view "$pr_num" --repo "$repo" --json title -q '.title' 2>/dev/null || echo "$title")
        if [[ -n "$issue_num" ]]; then
            issue_title=$(gh issue view "$issue_num" --repo "$repo" --json title -q '.title' 2>/dev/null || echo "Issue #$issue_num")
            issue_url="https://github.com/$repo/issues/$issue_num"
        fi
    fi

    # Create new PR entry
    local new_pr=$(cat << EOF
{
  "id": "$uuid",
  "repository": {
    "owner": "$owner",
    "name": "$name",
    "url": "https://github.com/$repo",
    "full_name": "$repo"
  },
  "issue": {
    "number": ${issue_num:-null},
    "title": "${issue_title:-null}",
    "url": "${issue_url:-null}"
  },
  "pr": {
    "number": $pr_num,
    "title": "$pr_title",
    "url": "$pr_url",
    "status": "open",
    "created_at": "$timestamp",
    "updated_at": "$timestamp"
  },
  "contribution": {
    "type": "unknown",
    "domain": "Other"
  },
  "review": {
    "comments_count": 0,
    "approvals_count": 0,
    "review_state": "pending"
  },
  "timeline": [
    {
      "event": "pr_created",
      "timestamp": "$timestamp",
      "description": "PR #$pr_num created"
    }
  ],
  "_internal": {
    "created_by": "pr-tracker-cli",
    "created_at": "$timestamp"
  }
}
EOF
)

    # Add to history
    jq --argjson pr "$new_pr" '.prs += [$pr]' "$HISTORY_FILE" > "$HISTORY_FILE.tmp" && mv "$HISTORY_FILE.tmp" "$HISTORY_FILE"

    # Update statistics
    update_stats

    echo -e "${GREEN}Added PR #$pr_num from $repo${NC}"
}

# Update statistics
update_stats() {
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    local total=$(jq '.prs | length' "$HISTORY_FILE")
    local merged=$(jq '[.prs[] | select(.pr.status == "merged")] | length' "$HISTORY_FILE")
    local open=$(jq '[.prs[] | select(.pr.status == "open")] | length' "$HISTORY_FILE")
    local closed=$(jq '[.prs[] | select(.pr.status == "closed" or .pr.status == "rejected")] | length' "$HISTORY_FILE")
    local repos=$(jq '[.prs[].repository.full_name] | unique | length' "$HISTORY_FILE")
    local unique_repos=$(jq '[.prs[].repository.full_name] | unique' "$HISTORY_FILE")

    local merge_rate=0
    if [[ "$total" -gt 0 ]]; then
        merge_rate=$(echo "scale=0; $merged * 100 / $total" | bc 2>/dev/null || echo 0)
    fi

    jq --arg ts "$timestamp" \
       --argjson total "$total" \
       --argjson merged "$merged" \
       --argjson open "$open" \
       --argjson closed "$closed" \
       --argjson repos "$repos" \
       --argjson merge_rate "$merge_rate" \
       --argjson unique_repos "$unique_repos" \
       '.statistics.total_prs = $total |
        .statistics.merged_prs = $merged |
        .statistics.open_prs = $open |
        .statistics.closed_prs = $closed |
        .statistics.repos_contributed = $repos |
        .statistics.merge_rate = $merge_rate |
        .statistics.unique_repos = $unique_repos |
        .metadata.last_updated = $ts' "$HISTORY_FILE" > "$HISTORY_FILE.tmp" && mv "$HISTORY_FILE.tmp" "$HISTORY_FILE"
}

# Update PR status
update_status() {
    local pr_id="$1"
    local new_status="$2"

    if [[ -z "$pr_id" || -z "$new_status" ]]; then
        echo -e "${RED}Usage: pr-tracker.sh update <pr_id_or_number> <status>${NC}"
        echo "Valid statuses: open, merged, closed, rejected"
        exit 1
    fi

    init_history

    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    # Update PR status
    jq --arg id "$pr_id" \
       --arg status "$new_status" \
       --arg ts "$timestamp" \
       '(.prs[] | select(.id == $id or .pr.number == ($id | tonumber))) |= (
         .pr.status = $status |
         .pr.updated_at = $ts |
         .timeline += [{"event": "status_changed", "timestamp": $ts, "description": "Status changed to \($status)"}]
       )' "$HISTORY_FILE" > "$HISTORY_FILE.tmp" && mv "$HISTORY_FILE.tmp" "$HISTORY_FILE"

    update_stats

    echo -e "${GREEN}Updated PR $pr_id status to $new_status${NC}"
}

# Export to JSON
export_json() {
    init_history
    cat "$HISTORY_FILE"
}

# Show help
show_help() {
    echo -e "${CYAN}PR Tracker CLI - OSS Contributor Swarm${NC}"
    echo ""
    echo "Usage: pr-tracker.sh <command> [options]"
    echo ""
    echo "Commands:"
    echo "  stats                 Show PR statistics"
    echo "  list [filter]         List PRs (all|open|merged|closed)"
    echo "  show <id>             Show PR details"
    echo "  add <repo> <pr#>      Add a new PR"
    echo "  update <id> <status>  Update PR status"
    echo "  export                Export full history as JSON"
    echo "  help                  Show this help"
    echo ""
    echo "Examples:"
    echo "  pr-tracker.sh stats"
    echo "  pr-tracker.sh list open"
    echo "  pr-tracker.sh add owner/repo 123 456 'Fix typo'"
    echo "  pr-tracker.sh update 123 merged"
}

# Main command handler
case "${1:-help}" in
    stats)
        show_stats
        ;;
    list)
        list_prs "$2"
        ;;
    show)
        show_pr "$2"
        ;;
    add)
        add_pr "$2" "$3" "$4" "$5"
        ;;
    update)
        update_status "$2" "$3"
        ;;
    export)
        export_json
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        show_help
        exit 1
        ;;
esac
