#!/bin/bash
#
# OSS Contributor Swarm Orchestrator
# Runs the 8-agent swarm in continuous mode
#

set -euo pipefail

# Configuration
SWARM_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORKSPACE="$SWARM_ROOT/workspace"
LOGS="$SWARM_ROOT/logs"
CONFIG="$SWARM_ROOT/config/swarm-config.json"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Agent status tracking
declare -A AGENT_STATUS
declare -A AGENT_PID

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
    ╔═══════════════════════════════════════════════════════════════════╗
    ║                                                                    ║
    ║   ██████╗ ███████╗███████╗     ██████╗ ██████╗ ███╗   ██╗████████╗║
    ║  ██╔═══██╗██╔════╝██╔════╝    ██╔════╝██╔═══██╗████╗  ██║╚══██╔══╝║
    ║  ██║   ██║███████╗███████╗    ██║     ██║   ██║██╔██╗ ██║   ██║   ║
    ║  ██║   ██║╚════██║╚════██║    ██║     ██║   ██║██║╚██╗██║   ██║   ║
    ║  ╚██████╔╝███████║███████║    ╚██████╗╚██████╔╝██║ ╚████║   ██║   ║
    ║   ╚═════╝ ╚══════╝╚══════╝     ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ║
    ║                                                                    ║
    ║            🤖 Open Source Contributor Swarm 🤖                     ║
    ║                  Continuous Contribution Engine                    ║
    ║                                                                    ║
    ╚═══════════════════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# Initialize workspace
init_workspace() {
    log_info "Initializing workspace..."

    mkdir -p "$WORKSPACE"/{agent-1-scout,agent-2-analyst,agent-3-explorer,agent-4-coder,agent-5-tester,agent-6-docs,agent-7-pr,agent-8-reviews,repos}
    mkdir -p "$WORKSPACE/shared"
    mkdir -p "$LOGS"

    # Initialize status file
    cat > "$WORKSPACE/swarm-status.json" << 'EOF'
{
    "swarm_id": null,
    "cycle": 0,
    "started_at": null,
    "current_phase": "idle",
    "agents": {
        "1-scout": { "status": "idle", "last_run": null },
        "2-analyst": { "status": "idle", "last_run": null },
        "3-explorer": { "status": "idle", "last_run": null },
        "4-coder": { "status": "idle", "last_run": null },
        "5-tester": { "status": "idle", "last_run": null },
        "6-docs": { "status": "idle", "last_run": null },
        "7-pr": { "status": "idle", "last_run": null },
        "8-reviews": { "status": "idle", "last_run": null }
    },
    "current_issue": null,
    "current_pr": null,
    "stats": {
        "cycles_completed": 0,
        "prs_created": 0,
        "prs_merged": 0,
        "issues_contributed": []
    }
}
EOF

    log_success "Workspace initialized"
}

# Update agent status
update_status() {
    local agent=$1
    local status=$2

    # Update in-memory status
    AGENT_STATUS[$agent]=$status

    # Update JSON file using jq
    jq --arg agent "$agent" --arg status "$status" \
       '.agents[$agent].status = $status | .agents[$agent].last_run = now' \
       "$WORKSPACE/swarm-status.json" > "$WORKSPACE/swarm-status.tmp" && \
       mv "$WORKSPACE/swarm-status.tmp" "$WORKSPACE/swarm-status.json"
}

# Check if agent output exists and is valid
check_agent_output() {
    local output_file=$1

    if [[ -f "$output_file" ]]; then
        local status=$(jq -r '.status' "$output_file" 2>/dev/null)
        if [[ "$status" == "completed" ]]; then
            return 0
        fi
    fi
    return 1
}

# Wait for agent completion with timeout
wait_for_agent() {
    local agent_name=$1
    local output_file=$2
    local timeout=${3:-600}  # Default 10 minutes

    local elapsed=0
    local interval=5

    log_info "Waiting for $agent_name to complete..."

    while [[ $elapsed -lt $timeout ]]; do
        if check_agent_output "$output_file"; then
            log_success "$agent_name completed"
            return 0
        fi

        sleep $interval
        elapsed=$((elapsed + interval))

        # Show progress every 30 seconds
        if [[ $((elapsed % 30)) -eq 0 ]]; then
            log_info "$agent_name still running... (${elapsed}s elapsed)"
        fi
    done

    log_error "$agent_name timed out after ${timeout}s"
    return 1
}

# Display status dashboard
show_dashboard() {
    clear
    print_banner

    echo -e "\n${PURPLE}═══════════════════ SWARM STATUS ═══════════════════${NC}\n"

    local status_file="$WORKSPACE/swarm-status.json"

    if [[ -f "$status_file" ]]; then
        local cycle=$(jq -r '.cycle' "$status_file")
        local phase=$(jq -r '.current_phase' "$status_file")
        local prs_created=$(jq -r '.stats.prs_created' "$status_file")
        local prs_merged=$(jq -r '.stats.prs_merged' "$status_file")

        echo -e "  Cycle: ${CYAN}#${cycle}${NC}  |  Phase: ${YELLOW}${phase}${NC}"
        echo -e "  PRs Created: ${GREEN}${prs_created}${NC}  |  PRs Merged: ${GREEN}${prs_merged}${NC}"
        echo ""

        echo -e "${PURPLE}───────────────────────────────────────────────────${NC}"
        echo -e "  AGENT                    STATUS"
        echo -e "${PURPLE}───────────────────────────────────────────────────${NC}"

        for i in {1..8}; do
            local agent_key=""
            local agent_name=""
            case $i in
                1) agent_key="1-scout"; agent_name="Issue Scout" ;;
                2) agent_key="2-analyst"; agent_name="Issue Analyst" ;;
                3) agent_key="3-explorer"; agent_name="Codebase Explorer" ;;
                4) agent_key="4-coder"; agent_name="Code Writer" ;;
                5) agent_key="5-tester"; agent_name="Test Writer" ;;
                6) agent_key="6-docs"; agent_name="Documentation Writer" ;;
                7) agent_key="7-pr"; agent_name="PR Creator" ;;
                8) agent_key="8-reviews"; agent_name="Review Responder" ;;
            esac

            local status=$(jq -r ".agents[\"$agent_key\"].status" "$status_file")
            local status_icon=""
            local status_color=""

            case $status in
                "idle") status_icon="⚪"; status_color="${NC}" ;;
                "running") status_icon="🔄"; status_color="${YELLOW}" ;;
                "completed") status_icon="✅"; status_color="${GREEN}" ;;
                "failed") status_icon="❌"; status_color="${RED}" ;;
                "waiting") status_icon="⏳"; status_color="${BLUE}" ;;
            esac

            printf "  %-2s %-22s ${status_color}${status_icon} %-12s${NC}\n" \
                   "$i." "$agent_name" "$status"
        done

        echo -e "${PURPLE}───────────────────────────────────────────────────${NC}"

        # Show current issue if any
        local current_issue=$(jq -r '.current_issue // "None"' "$status_file")
        if [[ "$current_issue" != "None" && "$current_issue" != "null" ]]; then
            echo -e "\n  Current Issue: ${CYAN}$current_issue${NC}"
        fi

        # Show current PR if any
        local current_pr=$(jq -r '.current_pr // "None"' "$status_file")
        if [[ "$current_pr" != "None" && "$current_pr" != "null" ]]; then
            echo -e "  Current PR: ${CYAN}$current_pr${NC}"
        fi
    fi

    echo -e "\n${PURPLE}═══════════════════════════════════════════════════${NC}"
}

# Run a single contribution cycle
run_cycle() {
    local cycle_num=$1

    log_info "Starting contribution cycle #$cycle_num"

    # Update cycle number
    jq --argjson cycle "$cycle_num" '.cycle = $cycle | .started_at = now' \
       "$WORKSPACE/swarm-status.json" > "$WORKSPACE/swarm-status.tmp" && \
       mv "$WORKSPACE/swarm-status.tmp" "$WORKSPACE/swarm-status.json"

    # ═══════════════════════════════════════════════════════════════
    # WAVE 1: Issue Discovery
    # ═══════════════════════════════════════════════════════════════
    log_info "Wave 1: Issue Discovery"
    update_status "1-scout" "running"
    jq '.current_phase = "discovery"' "$WORKSPACE/swarm-status.json" > "$WORKSPACE/swarm-status.tmp" && \
       mv "$WORKSPACE/swarm-status.tmp" "$WORKSPACE/swarm-status.json"

    # Launch Agent 1 (in real implementation, this would be a Claude Code agent)
    # Placeholder: simulate agent execution
    log_info "Launching Agent 1: Issue Scout..."

    # Wait for Agent 1
    if ! wait_for_agent "Agent 1" "$WORKSPACE/current-issue.json" 300; then
        log_error "Agent 1 failed to find issue"
        return 1
    fi
    update_status "1-scout" "completed"

    # ═══════════════════════════════════════════════════════════════
    # WAVE 2: Issue Analysis
    # ═══════════════════════════════════════════════════════════════
    log_info "Wave 2: Issue Analysis"
    update_status "2-analyst" "running"
    jq '.current_phase = "analysis"' "$WORKSPACE/swarm-status.json" > "$WORKSPACE/swarm-status.tmp" && \
       mv "$WORKSPACE/swarm-status.tmp" "$WORKSPACE/swarm-status.json"

    log_info "Launching Agent 2: Issue Analyst..."

    if ! wait_for_agent "Agent 2" "$WORKSPACE/issue-analysis.json" 300; then
        log_error "Agent 2 failed to analyze issue"
        return 1
    fi
    update_status "2-analyst" "completed"

    # ═══════════════════════════════════════════════════════════════
    # WAVE 3: Codebase Exploration
    # ═══════════════════════════════════════════════════════════════
    log_info "Wave 3: Codebase Exploration"
    update_status "3-explorer" "running"
    jq '.current_phase = "exploration"' "$WORKSPACE/swarm-status.json" > "$WORKSPACE/swarm-status.tmp" && \
       mv "$WORKSPACE/swarm-status.tmp" "$WORKSPACE/swarm-status.json"

    log_info "Launching Agent 3: Codebase Explorer..."

    if ! wait_for_agent "Agent 3" "$WORKSPACE/codebase-map.json" 600; then
        log_error "Agent 3 failed to explore codebase"
        return 1
    fi
    update_status "3-explorer" "completed"

    # ═══════════════════════════════════════════════════════════════
    # WAVE 4: Parallel Development (Code + Tests + Docs)
    # ═══════════════════════════════════════════════════════════════
    log_info "Wave 4: Parallel Development"
    jq '.current_phase = "development"' "$WORKSPACE/swarm-status.json" > "$WORKSPACE/swarm-status.tmp" && \
       mv "$WORKSPACE/swarm-status.tmp" "$WORKSPACE/swarm-status.json"

    # Launch Agents 4, 5, 6 in parallel
    update_status "4-coder" "running"
    update_status "5-tester" "running"
    update_status "6-docs" "running"

    log_info "Launching Agents 4, 5, 6 in parallel..."
    log_info "  - Agent 4: Code Writer"
    log_info "  - Agent 5: Test Writer"
    log_info "  - Agent 6: Documentation Writer"

    # Wait for all three to complete (in parallel)
    local all_complete=false
    local timeout=600
    local elapsed=0

    while [[ "$all_complete" == "false" && $elapsed -lt $timeout ]]; do
        local code_done=false
        local test_done=false
        local docs_done=false

        check_agent_output "$WORKSPACE/code-changes.json" && code_done=true
        check_agent_output "$WORKSPACE/test-changes.json" && test_done=true
        check_agent_output "$WORKSPACE/docs-changes.json" && docs_done=true

        [[ "$code_done" == "true" ]] && update_status "4-coder" "completed"
        [[ "$test_done" == "true" ]] && update_status "5-tester" "completed"
        [[ "$docs_done" == "true" ]] && update_status "6-docs" "completed"

        if [[ "$code_done" == "true" && "$test_done" == "true" && "$docs_done" == "true" ]]; then
            all_complete=true
        else
            sleep 5
            elapsed=$((elapsed + 5))
        fi
    done

    if [[ "$all_complete" == "false" ]]; then
        log_error "Wave 4 agents timed out"
        return 1
    fi

    log_success "All Wave 4 agents completed"

    # ═══════════════════════════════════════════════════════════════
    # WAVE 5: PR Creation
    # ═══════════════════════════════════════════════════════════════
    log_info "Wave 5: PR Creation"
    update_status "7-pr" "running"
    jq '.current_phase = "pr_creation"' "$WORKSPACE/swarm-status.json" > "$WORKSPACE/swarm-status.tmp" && \
       mv "$WORKSPACE/swarm-status.tmp" "$WORKSPACE/swarm-status.json"

    log_info "Launching Agent 7: PR Creator..."

    if ! wait_for_agent "Agent 7" "$WORKSPACE/pr-created.json" 300; then
        log_error "Agent 7 failed to create PR"
        return 1
    fi
    update_status "7-pr" "completed"

    # Update current PR in status
    local pr_url=$(jq -r '.pr.url' "$WORKSPACE/pr-created.json")
    jq --arg pr "$pr_url" '.current_pr = $pr' "$WORKSPACE/swarm-status.json" > "$WORKSPACE/swarm-status.tmp" && \
       mv "$WORKSPACE/swarm-status.tmp" "$WORKSPACE/swarm-status.json"

    # ═══════════════════════════════════════════════════════════════
    # WAVE 6: Review Monitoring (Continuous)
    # ═══════════════════════════════════════════════════════════════
    log_info "Wave 6: Review Monitoring"
    update_status "8-reviews" "running"
    jq '.current_phase = "review_monitoring"' "$WORKSPACE/swarm-status.json" > "$WORKSPACE/swarm-status.tmp" && \
       mv "$WORKSPACE/swarm-status.tmp" "$WORKSPACE/swarm-status.json"

    log_info "Launching Agent 8: Review Responder..."

    # Agent 8 monitors until PR is merged or closed
    # This can take hours/days, so we run it in background

    if ! wait_for_agent "Agent 8" "$WORKSPACE/review-activity.json" 86400; then
        log_warn "Agent 8 still monitoring (this is expected for long reviews)"
    fi

    # Check final outcome
    local outcome=$(jq -r '.final_outcome.result // "pending"' "$WORKSPACE/review-activity.json" 2>/dev/null)

    if [[ "$outcome" == "merged" ]]; then
        log_success "PR was merged! 🎉"
        update_status "8-reviews" "completed"
        jq '.stats.prs_merged += 1' "$WORKSPACE/swarm-status.json" > "$WORKSPACE/swarm-status.tmp" && \
           mv "$WORKSPACE/swarm-status.tmp" "$WORKSPACE/swarm-status.json"
    elif [[ "$outcome" == "closed" ]]; then
        log_warn "PR was closed without merge"
        update_status "8-reviews" "completed"
    else
        log_info "PR still pending review"
    fi

    # Update stats
    jq '.stats.prs_created += 1 | .stats.cycles_completed += 1' \
       "$WORKSPACE/swarm-status.json" > "$WORKSPACE/swarm-status.tmp" && \
       mv "$WORKSPACE/swarm-status.tmp" "$WORKSPACE/swarm-status.json"

    log_success "Cycle #$cycle_num completed"
    return 0
}

# Cleanup function
cleanup() {
    log_info "Shutting down swarm..."

    # Kill any running agent processes
    for agent in "${!AGENT_PID[@]}"; do
        if [[ -n "${AGENT_PID[$agent]}" ]]; then
            kill "${AGENT_PID[$agent]}" 2>/dev/null || true
        fi
    done

    log_info "Swarm shutdown complete"
    exit 0
}

# Main execution
main() {
    trap cleanup SIGINT SIGTERM

    print_banner

    # Check prerequisites
    log_info "Checking prerequisites..."

    if ! command -v gh &> /dev/null; then
        log_error "GitHub CLI (gh) is required but not installed"
        exit 1
    fi

    if ! gh auth status &> /dev/null; then
        log_error "GitHub CLI not authenticated. Run 'gh auth login' first"
        exit 1
    fi

    if ! command -v jq &> /dev/null; then
        log_error "jq is required but not installed"
        exit 1
    fi

    log_success "Prerequisites check passed"

    # Initialize
    init_workspace

    # Parse arguments
    local mode="${1:-continuous}"
    local max_cycles="${2:-0}"  # 0 = infinite

    case $mode in
        "single")
            log_info "Running single cycle mode"
            run_cycle 1
            ;;
        "continuous")
            log_info "Running continuous mode"
            local cycle=1
            while true; do
                show_dashboard
                run_cycle $cycle
                cycle=$((cycle + 1))

                if [[ $max_cycles -gt 0 && $cycle -gt $max_cycles ]]; then
                    log_info "Reached max cycles ($max_cycles)"
                    break
                fi

                # Cooldown between cycles
                log_info "Cooling down before next cycle..."
                sleep 60
            done
            ;;
        "dashboard")
            while true; do
                show_dashboard
                sleep 5
            done
            ;;
        *)
            echo "Usage: $0 [single|continuous|dashboard] [max_cycles]"
            exit 1
            ;;
    esac
}

main "$@"
