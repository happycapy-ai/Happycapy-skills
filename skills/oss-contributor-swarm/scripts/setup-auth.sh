#!/bin/bash
#
# GitHub Authentication Setup for OSS Contributor Swarm
#

set -euo pipefail

CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║         GitHub Authentication Setup                            ║${NC}"
echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check current auth status
if gh auth status &>/dev/null; then
    echo -e "${GREEN}✓ Already authenticated with GitHub${NC}"
    gh auth status
    exit 0
fi

echo -e "${YELLOW}GitHub CLI is not authenticated.${NC}"
echo ""
echo "To authenticate, you need a Personal Access Token (PAT)."
echo ""
echo -e "${CYAN}To create a PAT:${NC}"
echo "  1. Go to: https://github.com/settings/tokens"
echo "  2. Click 'Generate new token (classic)'"
echo "  3. Give it a name like 'oss-contributor-swarm'"
echo "  4. Select these scopes:"
echo "     - repo (Full control of private repositories)"
echo "     - read:org (Read org membership)"
echo "     - workflow (Update GitHub Action workflows)"
echo "  5. Click 'Generate token' and copy it"
echo ""
echo -e "${YELLOW}Paste your token below (it won't be displayed):${NC}"
echo ""

read -s -p "GitHub Token: " token
echo ""

if [[ -z "$token" ]]; then
    echo -e "${RED}No token provided. Exiting.${NC}"
    exit 1
fi

echo ""
echo "Authenticating..."

if echo "$token" | gh auth login --with-token; then
    echo ""
    echo -e "${GREEN}✓ Successfully authenticated!${NC}"
    echo ""
    gh auth status
else
    echo ""
    echo -e "${RED}✗ Authentication failed. Please check your token.${NC}"
    exit 1
fi

# Configure git to use gh for credentials
gh auth setup-git

echo ""
echo -e "${GREEN}✓ Git configured to use GitHub CLI for authentication${NC}"
echo ""
echo -e "${CYAN}You're all set! Run the swarm with:${NC}"
echo "  ./scripts/run-swarm.sh start"
