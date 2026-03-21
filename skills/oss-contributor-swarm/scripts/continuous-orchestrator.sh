#!/bin/bash
#
# OSS Contributor Swarm - Continuous Orchestrator
# Runs the 9-agent swarm in continuous 24/7 mode
# Goal: 3-5 contributions per day
#

set -euo pipefail

# Configuration
SWARM_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORKSPACE="$SWARM_ROOT/workspace"
SHARED="$SWARM_ROOT/shared"
LOGS="$SWARM_ROOT/logs"
CONFIG="$SWARM_ROOT/config/swarm-config.json"
HISTORY="$SHARED/contribution-history.json"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# Global state
CYCLE_COUNT=0
DAILY_PR_COUNT=0
ACTIVE_PRS=()
LAST_DAILY_RESET=$(date +%Y-%m-%d)

# Logging
log() {
    local level=$1
    local message=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "${timestamp} [${level}] ${message}"
    echo "${timestamp} [${level}] ${message}" >> "$LOGS/orchestrator.log"
}

log_info() { log "${BLUE}INFO${NC}" "$1"; }
log_success() { log "${GREEN}SUCCESS${NC}" "$1"; }
log_warn() { log "${YELLOW}WARN${NC}" "$1"; }
log_error() { log "${RED}ERROR${NC}" "$1"; }

# Banner
print_banner() {
    echo -e "${CYAN}"
    cat << 'EOF'
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║   ██████╗ ███████╗███████╗     ██████╗ ██████╗ ███╗   ██╗████████╗        ║
║  ██╔═══██╗██╔════╝██╔════╝    ██╔════╝██╔═══██╗████╗  ██║╚══██╔══╝        ║
║  ██║   ██║███████╗███████╗    ██║     ██║   ██║██╔██╗ ██║   ██║           ║
║  ██║   ██║╚════██║╚════██║    ██║     ██║   ██║██║╚██╗██║   ██║           ║
║  ╚██████╔╝███████║███████║    ╚██████╗╚██████╔╝██║ ╚████║   ██║           ║
║   ╚═════╝ ╚══════╝╚══════╝     ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝           ║
║                                                                            ║
║              🤖 CONTINUOUS CONTRIBUTOR MODE 🤖                             ║
║                    24/7 Open Source Contributions                          ║
║                       Target: 3-5 PRs per day                              ║
║                                                                            ║
╚═══════════════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# Initialize
init_workspace() {
    log_info "Initializing continuous mode workspace..."

    mkdir -p "$WORKSPACE"/{agent-0-qualifier,agent-1-scout,agent-2-analyst,agent-3-explorer,agent-4-coder,agent-5-tester,agent-6-docs,agent-7-pr,agent-8-reviews,repos}
    mkdir -p "$SHARED"
    mkdir -p "$LOGS"

    # Initialize history if not exists
    if [[ ! -f "$HISTORY" ]]; then
        cat > "$HISTORY" << 'EOF'
{
  "schema_version": "1.0.0",
  "stats": {"total_contributions": 0, "prs_merged": 0},
  "contributions": [],
  "success_patterns": {"best_issue_types": ["documentation", "typo"]},
  "repositories": {"successful": [], "avoid": [], "pending": []}
}
EOF
    fi

    # Initialize swarm status
    cat > "$WORKSPACE/swarm-status.json" << EOF
{
  "mode": "continuous",
  "started_at": "$(date -Iseconds)",
  "cycle": 0,
  "daily_prs": 0,
  "active_prs": [],
  "current_phase": "idle",
  "agents": {
    "0-qualifier": {"status": "idle"},
    "1-scout": {"status": "idle"},
    "2-analyst": {"status": "idle"},
    "3-explorer": {"status": "idle"},
    "4-coder": {"status": "idle"},
    "5-tester": {"status": "idle"},
    "6-docs": {"status": "idle"},
    "7-pr": {"status": "idle"},
    "8-reviews": {"status": "idle"}
  }
}
EOF

    log_success "Workspace initialized for continuous mode"
}

# Check rate limits
check_rate_limits() {
    local remaining=$(gh api rate_limit --jq '.resources.core.remaining')
    local reset_time=$(gh api rate_limit --jq '.resources.core.reset')

    if [[ $remaining -lt 100 ]]; then
        local wait_seconds=$((reset_time - $(date +%s)))
        if [[ $wait_seconds -gt 0 ]]; then
            log_warn "Rate limit low ($remaining remaining). Waiting ${wait_seconds}s..."
            sleep $wait_seconds
        fi
    fi
}

# Check daily limits
check_daily_limits() {
    local today=$(date +%Y-%m-%d)

    # Reset daily counter if new day
    if [[ "$today" != "$LAST_DAILY_RESET" ]]; then
        DAILY_PR_COUNT=0
        LAST_DAILY_RESET=$today
        log_info "New day - reset daily PR count"
    fi

    # Check against limit
    local daily_limit=$(jq -r '.continuous.daily_pr_limit // 10' "$CONFIG")
    if [[ $DAILY_PR_COUNT -ge $daily_limit ]]; then
        log_warn "Daily PR limit reached ($DAILY_PR_COUNT/$daily_limit). Waiting until tomorrow..."
        return 1
    fi

    return 0
}

# Check concurrent PR limit
check_concurrent_limits() {
    local max_concurrent=$(jq -r '.continuous.max_concurrent_prs // 3' "$CONFIG")
    local active_count=${#ACTIVE_PRS[@]}

    if [[ $active_count -ge $max_concurrent ]]; then
        log_warn "Max concurrent PRs reached ($active_count/$max_concurrent). Monitoring existing PRs..."
        return 1
    fi

    return 0
}

# Update active PRs status
update_active_prs() {
    log_info "Checking status of ${#ACTIVE_PRS[@]} active PRs..."

    local still_active=()
    for pr_url in "${ACTIVE_PRS[@]}"; do
        local owner=$(echo "$pr_url" | cut -d'/' -f4)
        local repo=$(echo "$pr_url" | cut -d'/' -f5)
        local pr_num=$(echo "$pr_url" | cut -d'/' -f7)

        local state=$(gh pr view "$pr_num" --repo "$owner/$repo" --json state --jq '.state' 2>/dev/null || echo "UNKNOWN")

        case $state in
            "OPEN")
                still_active+=("$pr_url")
                ;;
            "MERGED")
                log_success "PR merged: $pr_url"
                record_outcome "$pr_url" "merged"
                ;;
            "CLOSED")
                log_warn "PR closed without merge: $pr_url"
                record_outcome "$pr_url" "closed"
                ;;
            *)
                log_warn "Unknown PR state for $pr_url: $state"
                still_active+=("$pr_url")
                ;;
        esac
    done

    ACTIVE_PRS=("${still_active[@]}")
}

# Record outcome to history
record_outcome() {
    local pr_url=$1
    local outcome=$2

    log_info "Recording outcome: $pr_url -> $outcome"

    # Update history file
    jq --arg url "$pr_url" --arg outcome "$outcome" '
        .contributions |= map(
            if .pr.url == $url then
                .outcome = $outcome |
                .pr.state = $outcome
            else .
            end
        ) |
        if $outcome == "merged" then
            .stats.prs_merged += 1
        else .
        end
    ' "$HISTORY" > "$HISTORY.tmp" && mv "$HISTORY.tmp" "$HISTORY"
}

# Run Agent 0: Repo Qualifier
run_agent_0() {
    log_info "Running Agent 0: Repo Qualifier..."

    # Agent 0 qualifies repos based on health metrics
    # Output: qualified-repos.json

    # Simplified version - in production, this would be a full agent
    cat > "$WORKSPACE/qualified-repos.json" << 'EOF'
{
  "agent": "agent-0-qualifier",
  "status": "completed",
  "qualified_repos": []
}
EOF

    return 0
}

# Run contribution cycle
run_contribution_cycle() {
    local cycle=$1
    log_info "═══════════════════════════════════════════════════════"
    log_info "Starting contribution cycle #$cycle"
    log_info "═══════════════════════════════════════════════════════"

    # Update status
    jq --argjson cycle "$cycle" '.cycle = $cycle | .current_phase = "qualifying"' \
        "$WORKSPACE/swarm-status.json" > "$WORKSPACE/swarm-status.tmp" && \
        mv "$WORKSPACE/swarm-status.tmp" "$WORKSPACE/swarm-status.json"

    # Wave 0: Qualify repos (new!)
    log_info "Wave 0: Qualifying repositories..."
    run_agent_0 || { log_error "Agent 0 failed"; return 1; }

    # Wave 1: Find issue
    log_info "Wave 1: Scouting for issues..."
    jq '.current_phase = "scouting"' "$WORKSPACE/swarm-status.json" > "$WORKSPACE/swarm-status.tmp" && \
        mv "$WORKSPACE/swarm-status.tmp" "$WORKSPACE/swarm-status.json"
    # run_agent_1 || { log_error "Agent 1 failed"; return 1; }

    # Wave 2: Analyze issue
    log_info "Wave 2: Analyzing issue..."
    jq '.current_phase = "analyzing"' "$WORKSPACE/swarm-status.json" > "$WORKSPACE/swarm-status.tmp" && \
        mv "$WORKSPACE/swarm-status.tmp" "$WORKSPACE/swarm-status.json"
    # run_agent_2 || { log_error "Agent 2 failed"; return 1; }

    # Wave 3: Explore codebase
    log_info "Wave 3: Exploring codebase..."
    jq '.current_phase = "exploring"' "$WORKSPACE/swarm-status.json" > "$WORKSPACE/swarm-status.tmp" && \
        mv "$WORKSPACE/swarm-status.tmp" "$WORKSPACE/swarm-status.json"
    # run_agent_3 || { log_error "Agent 3 failed"; return 1; }

    # Wave 4: Development (parallel)
    log_info "Wave 4: Development (Code + Tests + Docs in parallel)..."
    jq '.current_phase = "developing"' "$WORKSPACE/swarm-status.json" > "$WORKSPACE/swarm-status.tmp" && \
        mv "$WORKSPACE/swarm-status.tmp" "$WORKSPACE/swarm-status.json"
    # run_agents_4_5_6_parallel || { log_error "Development failed"; return 1; }

    # Wave 5: Create PR
    log_info "Wave 5: Creating PR..."
    jq '.current_phase = "pr_creation"' "$WORKSPACE/swarm-status.json" > "$WORKSPACE/swarm-status.tmp" && \
        mv "$WORKSPACE/swarm-status.tmp" "$WORKSPACE/swarm-status.json"
    # run_agent_7 || { log_error "Agent 7 failed"; return 1; }

    # Track new PR
    if [[ -f "$WORKSPACE/pr-created.json" ]]; then
        local pr_url=$(jq -r '.pr.url' "$WORKSPACE/pr-created.json")
        ACTIVE_PRS+=("$pr_url")
        DAILY_PR_COUNT=$((DAILY_PR_COUNT + 1))
        log_success "Cycle #$cycle complete. PR created: $pr_url"
    fi

    return 0
}

# Monitor active PRs
run_monitoring_cycle() {
    log_info "Running monitoring cycle for ${#ACTIVE_PRS[@]} active PRs..."

    for pr_url in "${ACTIVE_PRS[@]}"; do
        local owner=$(echo "$pr_url" | cut -d'/' -f4)
        local repo=$(echo "$pr_url" | cut -d'/' -f5)
        local pr_num=$(echo "$pr_url" | cut -d'/' -f7)

        # Check for reviews
        local reviews=$(gh api "repos/$owner/$repo/pulls/$pr_num/reviews" --jq 'length' 2>/dev/null || echo "0")

        if [[ "$reviews" -gt 0 ]]; then
            log_info "PR #$pr_num has $reviews reviews - Agent 8 should respond"
            # run_agent_8 "$pr_url"
        fi
    done
}

# Show dashboard
show_dashboard() {
    clear
    print_banner

    echo -e "\n${PURPLE}═══════════════════ CONTINUOUS MODE STATUS ═══════════════════${NC}\n"

    local today=$(date +%Y-%m-%d)
    local uptime=$(($(date +%s) - $(date -d "$(jq -r '.started_at' "$WORKSPACE/swarm-status.json")" +%s 2>/dev/null || echo "0")))
    local uptime_hours=$((uptime / 3600))

    echo -e "  Mode: ${GREEN}CONTINUOUS${NC}  |  Uptime: ${CYAN}${uptime_hours}h${NC}"
    echo -e "  Cycle: ${CYAN}#${CYCLE_COUNT}${NC}  |  Daily PRs: ${GREEN}${DAILY_PR_COUNT}${NC}/10"
    echo -e "  Active PRs: ${YELLOW}${#ACTIVE_PRS[@]}${NC}/3"
    echo ""

    if [[ ${#ACTIVE_PRS[@]} -gt 0 ]]; then
        echo -e "${PURPLE}─────────────────── Active PRs ───────────────────${NC}"
        for pr in "${ACTIVE_PRS[@]}"; do
            echo -e "  • ${CYAN}$pr${NC}"
        done
        echo ""
    fi

    # Show learning stats
    if [[ -f "$HISTORY" ]]; then
        local total=$(jq -r '.stats.total_contributions // 0' "$HISTORY")
        local merged=$(jq -r '.stats.prs_merged // 0' "$HISTORY")
        local rate=0
        if [[ $total -gt 0 ]]; then
            rate=$((merged * 100 / total))
        fi
        echo -e "${PURPLE}─────────────────── Learning Stats ───────────────────${NC}"
        echo -e "  Total contributions: ${CYAN}$total${NC}"
        echo -e "  PRs merged: ${GREEN}$merged${NC}"
        echo -e "  Success rate: ${GREEN}${rate}%${NC}"
    fi

    echo -e "\n${PURPLE}═══════════════════════════════════════════════════════════════${NC}"
}

# Main continuous loop
main() {
    trap 'log_info "Shutting down continuous mode..."; exit 0' SIGINT SIGTERM

    print_banner
    init_workspace

    log_info "Starting continuous contributor mode..."
    log_info "Target: 3-5 contributions per day"
    log_info "Press Ctrl+C to stop"

    local cooldown=$(jq -r '.continuous.cooldown_between_cycles_seconds // 60' "$CONFIG" 2>/dev/null || echo "60")

    while true; do
        # Check rate limits
        check_rate_limits

        # Update dashboard
        show_dashboard

        # Update status of active PRs
        if [[ ${#ACTIVE_PRS[@]} -gt 0 ]]; then
            update_active_prs
        fi

        # Check if we can create new PRs
        if check_daily_limits && check_concurrent_limits; then
            CYCLE_COUNT=$((CYCLE_COUNT + 1))
            run_contribution_cycle $CYCLE_COUNT || {
                log_warn "Cycle $CYCLE_COUNT failed, will retry..."
            }
        fi

        # Run monitoring for active PRs
        if [[ ${#ACTIVE_PRS[@]} -gt 0 ]]; then
            run_monitoring_cycle
        fi

        # Cooldown
        log_info "Cooling down for ${cooldown}s before next cycle..."
        sleep $cooldown

    done
}

main "$@"
