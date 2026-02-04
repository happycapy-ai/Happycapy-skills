---
name: claude-code-templates
description: CLI tool for configuring and monitoring Claude Code with a comprehensive collection of 600+ AI agents, 200+ custom commands, 55+ external service integrations (MCPs), 60+ settings, 39+ hooks, and 14+ project templates. Use when users need to install or manage Claude Code components, browse available templates, run analytics/health checks, or set up development workflows. Integrates with Claude Code, Cursor, Cline, and 10+ other AI coding platforms.
---

# Claude Code Templates

A comprehensive CLI tool and component library for enhancing your Claude Code development workflow. This skill provides access to a vast ecosystem of ready-to-use configurations, templates, and monitoring tools.

## When to Use This Skill

Use this skill when users need to:
- Install or browse Claude Code components (agents, commands, MCPs, settings, hooks)
- Set up development workflows with pre-configured templates
- Monitor Claude Code sessions with real-time analytics
- Run health checks on Claude Code installations
- Manage Claude Code plugins and permissions
- Access the component marketplace at aitmpl.com

## Core Components

### Available Component Types

1. **Agents (600+)** - AI specialists for specific domains
   - Development teams (frontend, backend, security auditors)
   - Language-specific experts (React, Python, Go, etc.)
   - Role-based specialists (database architects, performance optimizers)

2. **Commands (200+)** - Custom slash commands
   - Testing: `/generate-tests`, `/run-tests`
   - Performance: `/optimize-bundle`, `/analyze-performance`
   - Security: `/check-security`, `/audit-dependencies`

3. **MCPs (55+)** - External service integrations
   - Development: GitHub, GitLab, Bitbucket
   - Databases: PostgreSQL, MongoDB, Redis
   - Cloud Services: AWS, Azure, GCP
   - APIs: Stripe, OpenAI, Anthropic

4. **Settings (60+)** - Claude Code configurations
   - Performance tuning (timeouts, memory limits)
   - Output formatting and styling
   - Workspace configurations

5. **Hooks (39+)** - Automation triggers
   - Pre-commit validation
   - Post-completion actions
   - Continuous integration workflows

6. **Templates (14+)** - Project scaffolding
   - Full-stack applications
   - Microservices architectures
   - API servers

## Installation Commands

### Interactive Mode
```bash
npx claude-code-templates@latest
```
Browse and install components interactively.

### Direct Installation
```bash
# Install a single component
npx claude-code-templates@latest --agent frontend-developer --yes

# Install multiple components at once
npx claude-code-templates@latest --agent security-auditor --command security-audit --mcp github-integration --yes

# Install a complete development stack
npx claude-code-templates@latest --agent development-team/frontend-developer --command testing/generate-tests --mcp development/github-integration --yes
```

### Component Categories
```bash
# Install by category
npx claude-code-templates@latest --agent development-tools/code-reviewer --yes
npx claude-code-templates@latest --command performance/optimize-bundle --yes
npx claude-code-templates@latest --setting performance/mcp-timeouts --yes
npx claude-code-templates@latest --hook git/pre-commit-validation --yes
npx claude-code-templates@latest --mcp database/postgresql-integration --yes
```

## Monitoring Tools

### Analytics Dashboard
```bash
npx claude-code-templates@latest --analytics
```
Real-time monitoring of Claude Code sessions with:
- Live state detection
- Performance metrics
- Session statistics
- Resource usage tracking

### Conversation Monitor
```bash
# Local access
npx claude-code-templates@latest --chats

# Secure remote access via Cloudflare Tunnel
npx claude-code-templates@latest --chats --tunnel
```
Mobile-optimized interface to view Claude responses in real-time.

### Health Check
```bash
npx claude-code-templates@latest --health-check
```
Comprehensive diagnostics including:
- Installation verification
- Configuration validation
- Performance optimization suggestions
- Dependency checks

### Plugin Dashboard
```bash
npx claude-code-templates@latest --plugins
```
Unified interface for:
- Viewing available marketplaces
- Managing installed plugins
- Configuring permissions
- Updating components

## Component Guidelines

All components follow strict standards:
- **Naming**: kebab-case format
- **Paths**: Relative paths only
- **Security**: No hardcoded secrets (use environment variables)
- **Validation**: Automated review before commits
- **Testing**: Comprehensive test coverage

## Security Best Practices

When working with this tool:
1. **Never hardcode API keys or tokens** - Use environment variables
2. **Use .env files** - Add to .gitignore
3. **Validate inputs** - All user inputs are sanitized
4. **Review permissions** - Check MCP permissions before installation

Example secure configuration:
```javascript
// ✅ Good - Using environment variables
const apiKey = process.env.GOOGLE_API_KEY;

// ❌ Bad - Hardcoded secrets
const apiKey = "your-api-key-here";
```

## Web Interface

Browse all components at **[aitmpl.com](https://aitmpl.com)**:
- Interactive catalog of 100+ components
- Search and filter capabilities
- One-click installation commands
- Component documentation and examples

## Documentation

Complete guides and API reference available at **[docs.aitmpl.com](https://docs.aitmpl.com/)**

## Example Workflows

### Setting Up a Frontend Development Environment
```bash
npx claude-code-templates@latest \
  --agent development-team/frontend-developer \
  --agent development-tools/code-reviewer \
  --command testing/generate-tests \
  --command performance/optimize-bundle \
  --mcp development/github-integration \
  --hook git/pre-commit-validation \
  --yes
```

### Security-Focused Setup
```bash
npx claude-code-templates@latest \
  --agent security/security-auditor \
  --command security/check-security \
  --command security/audit-dependencies \
  --hook security/vulnerability-scan \
  --yes
```

### Full-Stack Development Stack
```bash
npx claude-code-templates@latest \
  --agent development-team/frontend-developer \
  --agent development-team/backend-developer \
  --mcp database/postgresql-integration \
  --mcp development/github-integration \
  --setting performance/mcp-timeouts \
  --yes
```

## Component Structure

Components are organized in a hierarchical structure:
```
cli-tool/components/
├── agents/          # AI specialists
├── commands/        # Slash commands
├── mcps/           # External integrations
├── settings/       # Configurations
├── hooks/          # Automation triggers
└── templates/      # Project scaffolds
```

## Version Information

- Current Version: 1.21.14+
- Node.js Required: 14.0.0+
- Compatible with: Claude Code, Cursor, Cline, and 10+ AI coding platforms

## Attribution

This tool includes components from multiple sources:
- K-Dense-AI/claude-scientific-skills (139 scientific skills)
- anthropics/skills (21 official skills)
- obra/superpowers (14 workflow skills)
- Community contributions from various authors

All components maintain their original licenses and attribution.

## Support and Community

- **Repository**: [github.com/davila7/claude-code-templates](https://github.com/davila7/claude-code-templates)
- **Issues**: [GitHub Issues](https://github.com/davila7/claude-code-templates/issues)
- **Discussions**: [GitHub Discussions](https://github.com/davila7/claude-code-templates/discussions)
- **NPM Package**: [claude-code-templates](https://www.npmjs.com/package/claude-code-templates)

## Tips for Users

1. **Start with interactive mode** - Run without flags to explore available components
2. **Use --yes flag** - Skip confirmation prompts for automation
3. **Check health regularly** - Run health checks after updates
4. **Browse the web interface** - Visit aitmpl.com for visual component discovery
5. **Monitor your sessions** - Use analytics to understand Claude Code usage patterns
