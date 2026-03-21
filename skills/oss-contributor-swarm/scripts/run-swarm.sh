#!/bin/bash
#
# Run the complete OSS Contributor Swarm
# This is the main entry point for continuous contribution
#

set -euo pipefail

SWARM_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPTS="$SWARM_ROOT/scripts"

# Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

print_usage() {
    cat << EOF
${CYAN}╔═══════════════════════════════════════════════════════════════╗
║          OSS Contributor Swarm - Run Script                    ║
╚═══════════════════════════════════════════════════════════════╝${NC}

Usage: $0 <command> [options]

Commands:
  ${GREEN}start${NC}         Start the swarm in continuous mode
  ${GREEN}single${NC}        Run a single contribution cycle
  ${GREEN}dashboard${NC}     Show the status dashboard
  ${GREEN}stop${NC}          Stop all running agents
  ${GREEN}status${NC}        Show current swarm status
  ${GREEN}clean${NC}         Clean workspace for fresh start
  ${GREEN}agent <n>${NC}     Run a specific agent (1-8)

Options:
  --max-cycles <n>    Maximum cycles to run (continuous mode)
  --dry-run           Show what would be done without executing

Examples:
  $0 start                    # Start continuous contribution
  $0 single                   # Run one contribution cycle
  $0 start --max-cycles 5     # Run 5 cycles then stop
  $0 agent 1                  # Run only the Issue Scout
  $0 dashboard                # Monitor swarm progress

EOF
}

check_prerequisites() {
    echo -e "${YELLOW}Checking prerequisites...${NC}"

    local missing=()

    if ! command -v gh &> /dev/null; then
        missing+=("gh (GitHub CLI)")
    fi

    if ! command -v jq &> /dev/null; then
        missing+=("jq")
    fi

    if ! command -v git &> /dev/null; then
        missing+=("git")
    fi

    if ! command -v claude &> /dev/null; then
        missing+=("claude (Claude Code CLI)")
    fi

    if [[ ${#missing[@]} -gt 0 ]]; then
        echo -e "${RED}Missing required tools:${NC}"
        for tool in "${missing[@]}"; do
            echo "  - $tool"
        done
        exit 1
    fi

    # Check GitHub auth
    if ! gh auth status &> /dev/null; then
        echo -e "${RED}GitHub CLI not authenticated${NC}"
        echo "Run: gh auth login"
        exit 1
    fi

    echo -e "${GREEN}All prerequisites satisfied${NC}"
}

cmd="${1:-}"

case "$cmd" in
    start)
        check_prerequisites
        shift
        exec "$SCRIPTS/orchestrator.sh" continuous "$@"
        ;;
    single)
        check_prerequisites
        exec "$SCRIPTS/orchestrator.sh" single
        ;;
    dashboard)
        exec "$SCRIPTS/orchestrator.sh" dashboard
        ;;
    stop)
        echo "Stopping swarm..."
        pkill -f "orchestrator.sh" 2>/dev/null || true
        pkill -f "launch-agent.sh" 2>/dev/null || true
        echo "Swarm stopped"
        ;;
    status)
        if [[ -f "$SWARM_ROOT/workspace/swarm-status.json" ]]; then
            jq '.' "$SWARM_ROOT/workspace/swarm-status.json"
        else
            echo "No active swarm status found"
        fi
        ;;
    clean)
        echo "Cleaning workspace..."
        rm -rf "$SWARM_ROOT/workspace"/*
        rm -rf "$SWARM_ROOT/logs"/*
        echo "Workspace cleaned"
        ;;
    agent)
        shift
        exec "$SCRIPTS/launch-agent.sh" "$@"
        ;;
    help|--help|-h)
        print_usage
        ;;
    *)
        print_usage
        exit 1
        ;;
esac
