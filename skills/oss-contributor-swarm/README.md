# Open Source Contributor Swarm v2.0

A continuous, learning multi-agent system that autonomously contributes to open source projects 24/7.

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║   ██████╗ ███████╗███████╗     ██████╗ ██████╗ ███╗   ██╗████████╗        ║
║  ██╔═══██╗██╔════╝██╔════╝    ██╔════╝██╔═══██╗████╗  ██║╚══██╔══╝        ║
║  ██║   ██║███████╗███████╗    ██║     ██║   ██║██╔██╗ ██║   ██║           ║
║  ██║   ██║╚════██║╚════██║    ██║     ██║   ██║██║╚██╗██║   ██║           ║
║  ╚██████╔╝███████║███████║    ╚██████╗╚██████╔╝██║ ╚████║   ██║           ║
║   ╚═════╝ ╚══════╝╚══════╝     ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝           ║
║                                                                            ║
║              🤖 CONTINUOUS CONTRIBUTOR v2.0 🤖                             ║
║                    24/7 Learning Agent Swarm                               ║
║                      Target: 3-5 PRs per day                               ║
║                                                                            ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

## What's New in v2.0

### 1. Continuous Mode
```
┌─────────────────────────────────────────────────────────────┐
│  CONTINUOUS CONTRIBUTOR MODE                                 │
│                                                              │
│  While true:                                                 │
│    1. Scout finds issue → 2. Swarm executes → 3. PR created │
│    4. Monitor PR → 5. Respond to reviews → 6. Loop back     │
│                                                              │
│  Goal: 3-5 contributions per day                            │
└─────────────────────────────────────────────────────────────┘
```

### 2. Agent 0: Repo Qualifier (NEW)
Pre-qualifies repositories before issue selection:
- Checks maintainer responsiveness (avg PR merge time)
- Verifies CONTRIBUTING.md exists
- Detects CLA requirements
- Scores "contribution-friendliness"

### 3. Smarter Issue Selection
Enhanced filtering with quality signals:
```yaml
filters:
  repo_health:
    min_stars: 50          # Active community
    max_stars: 10000       # Not too competitive
    last_commit_days: 30   # Recently maintained

  issue_quality:
    min_body_length: 100
    comments_count: <5     # Not controversial
    age_days: 1-60         # Fresh but not ignored

  maintainer_signals:
    avg_pr_merge_time: <7days
```

### 4. Agent 8: Auto-Reply to Reviews
```
Review Received
      │
      ├── Type: APPROVED → Wait for merge ✓
      │
      └── Type: CHANGES_REQUESTED
          │
          ├── Simple fix? → Auto-fix → Push → "Fixed!" ✓
          ├── Style issue? → Run formatter → Push ✓
          ├── Unclear? → Request clarification
          └── Major rework? → ESCALATE to human
```

### 5. Learning Module
Tracks patterns and improves over time:
```json
{
  "success_patterns": {
    "best_issue_types": ["typo", "documentation"],
    "best_languages": ["Python", "JavaScript"],
    "avoid_repos": ["slow-maintainer/repo"]
  },
  "contribution_history": [...]
}
```

## Architecture v2.0

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ENHANCED EXECUTION FLOW                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Wave 0: [Agent 0: Repo Qualifier] ← NEW!                                   │
│                    │                                                         │
│                    ▼ (qualified repos)                                       │
│  Wave 1: [Agent 1: Issue Scout] ← Enhanced with scoring                     │
│                    │                                                         │
│                    ▼                                                         │
│  Wave 2: [Agent 2: Issue Analyst]                                           │
│                    │                                                         │
│                    ▼                                                         │
│  Wave 3: [Agent 3: Codebase Explorer]                                       │
│                    │                                                         │
│                    ▼                                                         │
│  Wave 4: [Agent 4] ─┬─ [Agent 5] ─┬─ [Agent 6]  (parallel)                 │
│           Code      │    Tests     │    Docs                                │
│                     └──────────────┘                                        │
│                            │                                                 │
│                            ▼                                                 │
│  Wave 5: [Agent 7: PR Creator]                                              │
│                    │                                                         │
│                    ▼                                                         │
│  Wave 6: [Agent 8: Review Responder] ← Enhanced with auto-fix              │
│                    │                                                         │
│                    ▼                                                         │
│              ♻️ CONTINUOUS LOOP                                              │
│                    │                                                         │
│                    ▼                                                         │
│            📚 LEARNING MODULE                                                │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Agents

| # | Agent | Role | New in v2.0 |
|---|-------|------|-------------|
| 0 | Repo Qualifier | Pre-qualify repos | **NEW** |
| 1 | Issue Scout | Find issues | Scoring algorithm |
| 2 | Issue Analyst | Analyze requirements | - |
| 3 | Codebase Explorer | Clone & understand | - |
| 4 | Code Writer | Implement fix | - |
| 5 | Test Writer | Write tests | - |
| 6 | Documentation | Update docs | - |
| 7 | PR Creator | Submit PR | - |
| 8 | Review Responder | Handle feedback | **Auto-fix** |

## Quick Start

### Prerequisites

- GitHub CLI (`gh`) - authenticated
- Claude Code (`claude`) CLI
- `jq` for JSON processing
- `git`

### Installation

```bash
cd oss-contributor-swarm
chmod +x scripts/*.sh
```

### Run Continuous Mode

```bash
# Start 24/7 continuous contribution
./scripts/continuous-orchestrator.sh

# Or use the run script
./scripts/run-swarm.sh start
```

### Run Single Cycle

```bash
./scripts/run-swarm.sh single
```

## Configuration

Edit `config/swarm-config.json`:

```json
{
  "continuous": {
    "enabled": true,
    "target_daily_prs": {"min": 3, "max": 5},
    "max_concurrent_prs": 3,
    "daily_pr_limit": 10
  },
  "repo_qualification": {
    "min_stars": 50,
    "max_stars": 10000,
    "max_days_since_commit": 30
  },
  "learning": {
    "enabled": true,
    "boost_successful_repos": 15,
    "auto_avoid_threshold": 3
  }
}
```

## Directory Structure

```
oss-contributor-swarm/
├── agents/
│   ├── agent-0-repo-qualifier.md   # NEW - Pre-qualifies repos
│   ├── agent-1-issue-scout.md      # Enhanced with scoring
│   ├── agent-2-issue-analyst.md
│   ├── agent-3-codebase-explorer.md
│   ├── agent-4-code-writer.md
│   ├── agent-5-test-writer.md
│   ├── agent-6-docs-writer.md
│   ├── agent-7-pr-creator.md
│   └── agent-8-review-responder.md # Enhanced with auto-fix
├── config/
│   └── swarm-config.json           # v2.0 config with all options
├── scripts/
│   ├── continuous-orchestrator.sh  # NEW - 24/7 loop
│   ├── orchestrator.sh
│   ├── run-swarm.sh
│   └── launch-agent.sh
├── shared/
│   ├── interfaces.md
│   ├── contribution-history.json   # NEW - Learning data
│   └── learning-module.md          # NEW - Learning docs
└── workspace/
```

## Learning System

The swarm learns from every contribution:

### Success Patterns Tracked
- Best issue types (typo > docs > tests > bugs)
- Best languages (Python, JavaScript, TypeScript)
- Best repo size range (50-5000 stars)
- Optimal issue age (1-30 days)

### Repository Memory
- Successful repos get score boost (+15)
- Failed repos get penalized
- After 3 failures, repos are auto-avoided

### Maintainer Patterns
- Response time tracked
- Preferences learned (quote style, commit format)
- Slow maintainers flagged

## Auto-Fix Capabilities

Agent 8 can automatically fix these review requests:

| Fix Type | Example | Auto-Fix? |
|----------|---------|-----------|
| Typo | "Change teh to the" | Yes |
| Style | "Use single quotes" | Yes |
| Formatting | "Run prettier" | Yes |
| Add comment | "Add explanation" | Yes |
| Logic change | "Use different algorithm" | **No - Escalate** |
| Architecture | "Refactor this module" | **No - Escalate** |

## Safety Features

- Never force push
- Max 5 files per PR
- Max 100 lines changed
- Respects CONTRIBUTING.md
- Checks for secrets before commit
- Human approval required for security/deps

## Monitoring Dashboard

```
═══════════════════ CONTINUOUS MODE STATUS ═══════════════════

  Mode: CONTINUOUS  |  Uptime: 48h
  Cycle: #127  |  Daily PRs: 4/10
  Active PRs: 2/3

─────────────────── Active PRs ───────────────────
  • https://github.com/org/repo/pull/123
  • https://github.com/org/repo2/pull/456

─────────────────── Learning Stats ───────────────────
  Total contributions: 127
  PRs merged: 98
  Success rate: 77%

═══════════════════════════════════════════════════════════════
```

## License

MIT

---

*Built with the Agent Architect skill - v2.0 with Learning*
