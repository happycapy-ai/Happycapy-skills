# Claude Code Templates

CLI tool for configuring and monitoring Claude Code with a comprehensive collection of AI agents, custom commands, external service integrations (MCPs), settings, hooks, and project templates.

## Description

Claude Code Templates is a powerful CLI tool and component library that enhances your Claude Code development workflow. It provides access to over 600 AI agents, 200+ custom commands, 55+ MCPs, 60+ settings, 39+ hooks, and 14+ project templates.

The tool integrates seamlessly with Claude Code, Cursor, Cline, and over 10 other AI coding platforms, making it a versatile solution for any AI-powered development environment.

## Key Features

### Component Library
- **600+ AI Agents** - Domain-specific AI specialists (frontend, backend, security, database, etc.)
- **200+ Custom Commands** - Slash commands for testing, performance, security, and more
- **55+ MCPs** - External service integrations (GitHub, PostgreSQL, Stripe, AWS, OpenAI, etc.)
- **60+ Settings** - Configuration options for performance tuning and customization
- **39+ Hooks** - Automation triggers for git workflows and CI/CD
- **14+ Templates** - Project scaffolding for common architectures

### Monitoring Tools
- **Analytics Dashboard** - Real-time session monitoring with performance metrics
- **Conversation Monitor** - Mobile-optimized interface for viewing Claude responses
- **Health Check** - Comprehensive diagnostics for installation validation
- **Plugin Dashboard** - Unified interface for managing plugins and permissions

### Web Interface
Browse and explore all components at [aitmpl.com](https://aitmpl.com) with an interactive catalog, search functionality, and one-click installation commands.

## Installation

### Quick Start

```bash
# Interactive mode - browse and install components
npx claude-code-templates@latest

# Install specific components
npx claude-code-templates@latest --agent frontend-developer --yes
npx claude-code-templates@latest --command generate-tests --yes
npx claude-code-templates@latest --mcp github-integration --yes
```

### Common Workflows

#### Frontend Development Setup
```bash
npx claude-code-templates@latest \
  --agent development-team/frontend-developer \
  --command testing/generate-tests \
  --command performance/optimize-bundle \
  --mcp development/github-integration \
  --hook git/pre-commit-validation \
  --yes
```

#### Security Auditing Setup
```bash
npx claude-code-templates@latest \
  --agent security/security-auditor \
  --command security/check-security \
  --command security/audit-dependencies \
  --yes
```

## Usage

### Component Installation
Install components by category and name:
- `--agent category/name` - Install an AI agent
- `--command category/name` - Install a custom command
- `--mcp category/name` - Install an MCP integration
- `--setting category/name` - Install a configuration setting
- `--hook category/name` - Install an automation hook
- `--yes` - Skip confirmation prompts

### Monitoring Commands
- `--analytics` - Launch the analytics dashboard
- `--chats` - Start the conversation monitor
- `--chats --tunnel` - Start conversation monitor with remote access
- `--health-check` - Run comprehensive diagnostics
- `--plugins` - Open the plugin dashboard

## Use Cases

Use this skill when you need to:
- Set up a new Claude Code development environment
- Install pre-configured AI agents for specific tasks
- Add custom commands to streamline workflows
- Integrate external services (GitHub, databases, APIs)
- Monitor Claude Code session performance
- Diagnose installation or configuration issues
- Manage Claude Code plugins and permissions

## Security Considerations

The tool enforces security best practices:
- No hardcoded API keys or secrets in components
- All sensitive data uses environment variables
- Automated validation before component installation
- .env files are automatically added to .gitignore

## Documentation

- **Full Documentation**: [docs.aitmpl.com](https://docs.aitmpl.com/)
- **Web Catalog**: [aitmpl.com](https://aitmpl.com)
- **GitHub Repository**: [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates)

## Requirements

- Node.js 14.0.0 or higher
- npm or npx
- Compatible with Claude Code, Cursor, Cline, and 10+ AI coding platforms

## Attribution

This tool includes components from multiple sources:
- **K-Dense-AI/claude-scientific-skills** - MIT License (139 scientific skills)
- **anthropics/skills** - Official Anthropic skills (21 skills)
- **anthropics/claude-code** - Development guides (10 skills)
- **obra/superpowers** - MIT License (14 workflow skills)
- **alirezarezvani/claude-skills** - MIT License (36 professional role skills)
- **wshobson/agents** - MIT License (48 agents)
- **NerdyChefsAI Skills** - MIT License (specialized enterprise skills)
- **awesome-claude-code** - CC0 1.0 Universal (21 commands)
- **awesome-claude-skills** - Apache 2.0 (community skills)

Each component retains its original license and attribution.

## Support

- **Issues**: [GitHub Issues](https://github.com/davila7/claude-code-templates/issues)
- **Discussions**: [GitHub Discussions](https://github.com/davila7/claude-code-templates/discussions)
- **NPM Package**: [claude-code-templates](https://www.npmjs.com/package/claude-code-templates)

## Version

Current version: 1.21.14+

## License

MIT License - See the [original repository](https://github.com/davila7/claude-code-templates) for complete license details.

## Original Source

**Original Source:** [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates)

**License:** MIT License
