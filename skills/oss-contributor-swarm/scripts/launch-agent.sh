#!/bin/bash
#
# Launch a single agent with Claude Code
# Usage: ./launch-agent.sh <agent-number> [--background]
#

set -euo pipefail

SWARM_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
AGENTS_DIR="$SWARM_ROOT/agents"
WORKSPACE="$SWARM_ROOT/workspace"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

agent_num="${1:-}"
background="${2:-}"

if [[ -z "$agent_num" ]]; then
    echo "Usage: $0 <agent-number> [--background]"
    echo ""
    echo "Available agents:"
    echo "  1 - Issue Scout"
    echo "  2 - Issue Analyst"
    echo "  3 - Codebase Explorer"
    echo "  4 - Code Writer"
    echo "  5 - Test Writer"
    echo "  6 - Documentation Writer"
    echo "  7 - PR Creator"
    echo "  8 - Review Responder"
    exit 1
fi

# Map agent number to file
case $agent_num in
    1) agent_file="agent-1-issue-scout.md"; agent_name="Issue Scout" ;;
    2) agent_file="agent-2-issue-analyst.md"; agent_name="Issue Analyst" ;;
    3) agent_file="agent-3-codebase-explorer.md"; agent_name="Codebase Explorer" ;;
    4) agent_file="agent-4-code-writer.md"; agent_name="Code Writer" ;;
    5) agent_file="agent-5-test-writer.md"; agent_name="Test Writer" ;;
    6) agent_file="agent-6-docs-writer.md"; agent_name="Documentation Writer" ;;
    7) agent_file="agent-7-pr-creator.md"; agent_name="PR Creator" ;;
    8) agent_file="agent-8-review-responder.md"; agent_name="Review Responder" ;;
    *)
        echo "Invalid agent number: $agent_num"
        exit 1
        ;;
esac

agent_prompt_file="$AGENTS_DIR/$agent_file"

if [[ ! -f "$agent_prompt_file" ]]; then
    echo "Agent prompt file not found: $agent_prompt_file"
    exit 1
fi

echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Launching Agent $agent_num: $agent_name${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"

# Read agent prompt
agent_prompt=$(cat "$agent_prompt_file")

# Add context from previous agents
context=""

case $agent_num in
    2)
        if [[ -f "$WORKSPACE/current-issue.json" ]]; then
            context="

## Previous Agent Output (Agent 1 - Issue Scout)

$(cat "$WORKSPACE/current-issue.json")
"
        fi
        ;;
    3)
        if [[ -f "$WORKSPACE/issue-analysis.json" ]]; then
            context="

## Previous Agent Output (Agent 2 - Issue Analyst)

$(cat "$WORKSPACE/issue-analysis.json")
"
        fi
        ;;
    4|5|6)
        if [[ -f "$WORKSPACE/codebase-map.json" ]]; then
            context="

## Previous Agent Output (Agent 3 - Codebase Explorer)

$(cat "$WORKSPACE/codebase-map.json")
"
        fi
        if [[ -f "$WORKSPACE/issue-analysis.json" ]]; then
            context+="

## Issue Analysis (Agent 2)

$(cat "$WORKSPACE/issue-analysis.json")
"
        fi
        ;;
    7)
        for file in code-changes.json test-changes.json docs-changes.json; do
            if [[ -f "$WORKSPACE/$file" ]]; then
                context+="

## $file

$(cat "$WORKSPACE/$file")
"
            fi
        done
        ;;
    8)
        if [[ -f "$WORKSPACE/pr-created.json" ]]; then
            context="

## PR Information (Agent 7)

$(cat "$WORKSPACE/pr-created.json")
"
        fi
        ;;
esac

# Construct full prompt
full_prompt="${agent_prompt}${context}

---

Execute your mission now. Write your output to the specified JSON file when complete."

# Launch with Claude Code
if [[ "$background" == "--background" ]]; then
    echo -e "${YELLOW}Running in background...${NC}"
    nohup claude --print "$full_prompt" > "$SWARM_ROOT/logs/agent-$agent_num.log" 2>&1 &
    echo "PID: $!"
else
    echo -e "${YELLOW}Running in foreground...${NC}"
    claude --print "$full_prompt"
fi

echo -e "${GREEN}Agent $agent_num launched${NC}"
