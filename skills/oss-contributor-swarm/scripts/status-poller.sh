#!/bin/bash
# Status Poller - Poll GitHub for PR status updates
# Part of OSS Contributor Swarm v3.0

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
HISTORY_FILE="$SKILL_DIR/history/pr-history.json"
POLL_INTERVAL="${POLL_INTERVAL:-300}"  # Default 5 minutes

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

# Check if gh CLI is available
check_gh() {
    if ! command -v gh &> /dev/null; then
        log "${RED}Error: GitHub CLI (gh) is required but not installed${NC}"
        exit 1
    fi

    if ! gh auth status &>/dev/null; then
        log "${RED}Error: GitHub CLI is not authenticated. Run 'gh auth login'${NC}"
        exit 1
    fi
}

# Poll a single PR for updates
poll_pr() {
    local repo="$1"
    local pr_num="$2"
    local current_status="$3"

    local pr_data=$(gh pr view "$pr_num" --repo "$repo" --json state,merged,mergeable,reviewDecision,reviews,comments 2>/dev/null)

    if [[ -z "$pr_data" ]]; then
        log "${YELLOW}Warning: Could not fetch PR #$pr_num from $repo${NC}"
        return 1
    fi

    local state=$(echo "$pr_data" | jq -r '.state')
    local merged=$(echo "$pr_data" | jq -r '.merged')
    local review_decision=$(echo "$pr_data" | jq -r '.reviewDecision // "PENDING"')
    local comments_count=$(echo "$pr_data" | jq '.comments | length')
    local reviews_count=$(echo "$pr_data" | jq '.reviews | length')
    local approvals=$(echo "$pr_data" | jq '[.reviews[] | select(.state == "APPROVED")] | length')
    local changes_requested=$(echo "$pr_data" | jq '[.reviews[] | select(.state == "CHANGES_REQUESTED")] | length')

    # Determine new status
    local new_status="open"
    if [[ "$merged" == "true" ]]; then
        new_status="merged"
    elif [[ "$state" == "CLOSED" ]]; then
        new_status="closed"
    fi

    # Determine review state
    local review_state="pending"
    if [[ "$review_decision" == "APPROVED" ]]; then
        review_state="approved"
    elif [[ "$review_decision" == "CHANGES_REQUESTED" ]]; then
        review_state="changes_requested"
    elif [[ "$reviews_count" -gt 0 ]]; then
        review_state="commented"
    fi

    # Return data as JSON
    cat << EOF
{
  "status": "$new_status",
  "review_state": "$review_state",
  "comments_count": $comments_count,
  "approvals_count": $approvals,
  "changes_requested": $changes_requested,
  "changed": $([ "$current_status" != "$new_status" ] && echo "true" || echo "false")
}
EOF
}

# Update PR in history file
update_pr_in_history() {
    local repo="$1"
    local pr_num="$2"
    local update_data="$3"

    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    local new_status=$(echo "$update_data" | jq -r '.status')
    local review_state=$(echo "$update_data" | jq -r '.review_state')
    local comments=$(echo "$update_data" | jq -r '.comments_count')
    local approvals=$(echo "$update_data" | jq -r '.approvals_count')
    local changes_requested=$(echo "$update_data" | jq -r '.changes_requested')
    local changed=$(echo "$update_data" | jq -r '.changed')

    # Update the PR record
    jq --arg repo "$repo" \
       --argjson pr_num "$pr_num" \
       --arg status "$new_status" \
       --arg review_state "$review_state" \
       --argjson comments "$comments" \
       --argjson approvals "$approvals" \
       --argjson changes_requested "$changes_requested" \
       --arg ts "$timestamp" \
       '(.prs[] | select(.repository.full_name == $repo and .pr.number == $pr_num)) |= (
         .pr.status = $status |
         .pr.updated_at = $ts |
         .review.review_state = $review_state |
         .review.comments_count = $comments |
         .review.approvals_count = $approvals |
         .review.changes_requested = $changes_requested
       ) |
       .metadata.last_updated = $ts' "$HISTORY_FILE" > "$HISTORY_FILE.tmp" && mv "$HISTORY_FILE.tmp" "$HISTORY_FILE"

    # Add timeline event if status changed
    if [[ "$changed" == "true" ]]; then
        jq --arg repo "$repo" \
           --argjson pr_num "$pr_num" \
           --arg status "$new_status" \
           --arg ts "$timestamp" \
           '(.prs[] | select(.repository.full_name == $repo and .pr.number == $pr_num)).timeline += [{
             "event": "status_polled",
             "timestamp": $ts,
             "description": "Status updated to \($status) via polling"
           }]' "$HISTORY_FILE" > "$HISTORY_FILE.tmp" && mv "$HISTORY_FILE.tmp" "$HISTORY_FILE"
    fi
}

# Update statistics after polling
update_statistics() {
    local timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

    local total=$(jq '.prs | length' "$HISTORY_FILE")
    local merged=$(jq '[.prs[] | select(.pr.status == "merged")] | length' "$HISTORY_FILE")
    local open=$(jq '[.prs[] | select(.pr.status == "open")] | length' "$HISTORY_FILE")
    local closed=$(jq '[.prs[] | select(.pr.status == "closed" or .pr.status == "rejected")] | length' "$HISTORY_FILE")

    local merge_rate=0
    if [[ "$total" -gt 0 ]]; then
        merge_rate=$(echo "scale=0; $merged * 100 / $total" | bc 2>/dev/null || echo 0)
    fi

    jq --arg ts "$timestamp" \
       --argjson total "$total" \
       --argjson merged "$merged" \
       --argjson open "$open" \
       --argjson closed "$closed" \
       --argjson merge_rate "$merge_rate" \
       '.statistics.total_prs = $total |
        .statistics.merged_prs = $merged |
        .statistics.open_prs = $open |
        .statistics.closed_prs = $closed |
        .statistics.merge_rate = $merge_rate |
        .statistics.last_calculated = $ts |
        .metadata.last_updated = $ts' "$HISTORY_FILE" > "$HISTORY_FILE.tmp" && mv "$HISTORY_FILE.tmp" "$HISTORY_FILE"
}

# Poll all open PRs
poll_all() {
    if [[ ! -f "$HISTORY_FILE" ]]; then
        log "${YELLOW}No history file found. Nothing to poll.${NC}"
        return
    fi

    log "${CYAN}Starting PR status poll...${NC}"

    local open_prs=$(jq -r '.prs[] | select(.pr.status == "open") | "\(.repository.full_name)|\(.pr.number)|\(.pr.status)"' "$HISTORY_FILE")

    if [[ -z "$open_prs" ]]; then
        log "${GREEN}No open PRs to poll.${NC}"
        return
    fi

    local updated=0
    local total=0

    while IFS='|' read -r repo pr_num current_status; do
        ((total++))
        log "Polling $repo#$pr_num..."

        local update_data=$(poll_pr "$repo" "$pr_num" "$current_status")

        if [[ -n "$update_data" ]]; then
            local changed=$(echo "$update_data" | jq -r '.changed')
            local new_status=$(echo "$update_data" | jq -r '.status')

            update_pr_in_history "$repo" "$pr_num" "$update_data"

            if [[ "$changed" == "true" ]]; then
                log "${GREEN}PR #$pr_num status changed: $current_status -> $new_status${NC}"
                ((updated++))
            else
                log "PR #$pr_num unchanged (still $current_status)"
            fi
        fi

        # Rate limiting
        sleep 1
    done <<< "$open_prs"

    update_statistics

    log "${CYAN}Poll complete. $total PRs checked, $updated updated.${NC}"
}

# Run in continuous mode
run_continuous() {
    log "${CYAN}Starting continuous polling mode (interval: ${POLL_INTERVAL}s)${NC}"

    while true; do
        poll_all
        log "Sleeping for $POLL_INTERVAL seconds..."
        sleep "$POLL_INTERVAL"
    done
}

# Show status
show_status() {
    if [[ ! -f "$HISTORY_FILE" ]]; then
        log "${YELLOW}No history file found.${NC}"
        return
    fi

    echo -e "${CYAN}=======================================================================${NC}"
    echo -e "${CYAN}                    POLLING STATUS                                     ${NC}"
    echo -e "${CYAN}=======================================================================${NC}"
    echo ""

    local last_poll=$(jq -r '.metadata.last_updated // "Never"' "$HISTORY_FILE")
    local open_count=$(jq '[.prs[] | select(.pr.status == "open")] | length' "$HISTORY_FILE")

    echo -e "Last Poll: ${GREEN}$last_poll${NC}"
    echo -e "Open PRs:  ${YELLOW}$open_count${NC}"
    echo ""

    if [[ "$open_count" -gt 0 ]]; then
        echo -e "${CYAN}Open PRs to Monitor:${NC}"
        jq -r '.prs[] | select(.pr.status == "open") | "  - \(.repository.full_name)#\(.pr.number): \(.pr.title)"' "$HISTORY_FILE"
    fi
}

# Show help
show_help() {
    echo -e "${CYAN}Status Poller - OSS Contributor Swarm${NC}"
    echo ""
    echo "Usage: status-poller.sh <command>"
    echo ""
    echo "Commands:"
    echo "  poll        Poll all open PRs once"
    echo "  continuous  Run in continuous polling mode"
    echo "  status      Show polling status"
    echo "  help        Show this help"
    echo ""
    echo "Environment Variables:"
    echo "  POLL_INTERVAL  Seconds between polls (default: 300)"
    echo ""
    echo "Examples:"
    echo "  status-poller.sh poll"
    echo "  POLL_INTERVAL=60 status-poller.sh continuous"
}

# Main
case "${1:-help}" in
    poll)
        check_gh
        poll_all
        ;;
    continuous)
        check_gh
        run_continuous
        ;;
    status)
        show_status
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
