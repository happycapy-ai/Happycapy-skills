# HappyCapy Skill Creator

**Automated Claude skill creator for HappyCapy environment**

[![Download Latest Release](https://img.shields.io/github/v/release/Y1fe1-Yang/happycapy-skill-creator?label=Download&style=flat-square)](https://github.com/Y1fe1-Yang/happycapy-skill-creator/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## What is This?

**HappyCapy Skill Creator** is an automation tool that creates Claude skills by finding and adapting similar skills from the [anthropics/skills](https://github.com/anthropics/skills) repository. Instead of building from scratch, it intelligently clones, modifies, and packages skills tailored for the HappyCapy environment.

### How is This Different from Official `/skill-creator`?

| Aspect | Official `/skill-creator` | HappyCapy Skill Creator |
|--------|--------------------------|-------------------------|
| **Type** | Educational Guide | Automation Tool |
| **Purpose** | Teaches you **how** to create skills | **Automatically** creates skills |
| **Target Users** | Developers who want to learn | Anyone who needs a skill quickly |
| **Usage** | Read, understand, then create manually | Run one command, get a skill |

**Think of it this way:**
- **Official skill-creator** = Your **teacher** who explains principles
- **HappyCapy Skill Creator** = Your **assistant** who does the work

**They complement each other!** Learn principles from the official guide, then use this tool to create skills quickly.

## Key Features

- **Semantic Search** - Uses LLM to find similar skills from anthropics/skills
- **Smart Adaptation** - Clones and modifies skills with LLM fine-tuning
- **Auto-Fix** - Automatically removes Docker dependencies and adapts for HappyCapy
- **One-Click Package** - Creates ready-to-install `.skill` files
- **Environment Aware** - Handles HappyCapy constraints (Python 3.11, Node.js 24, no Docker)

## Installation

### Option 1: Download Pre-packaged Skill (Recommended)

1. Download from [GitHub Releases](https://github.com/Y1fe1-Yang/happycapy-skill-creator/releases/latest)
2. In HappyCapy environment:
   ```bash
   /install happycapy-skill-creator-v1.2.0.skill
   ```

### Option 2: Clone Repository

```bash
git clone https://github.com/Y1fe1-Yang/happycapy-skill-creator.git
cd happycapy-skill-creator
git checkout main
python scripts/create_skill.py "Your requirement" --name skill-name
```

## Usage

Once installed, trigger the skill with phrases like:
- "Create a skill for compressing PDFs"
- "I need a skill to handle image processing"
- "Build a skill that converts markdown to HTML"

The skill will:
1. Search for similar skills in anthropics/skills
2. Clone the most relevant skill
3. Adapt it with your new requirements
4. Fix compatibility issues for HappyCapy
5. Package it as a `.skill` file

## Performance

- **Context Usage**: -55% compared to original (950 words vs 2,100 words)
- **SKILL.md Size**: -62% smaller (94 lines vs 247 lines)
- **Success Rate**: 90%+ for skills with similar base in anthropics/skills
- **Compliance**: 100% aligned with official skill-creator guidelines

## Requirements

- Python 3.11+
- `AI_GATEWAY_API_KEY` environment variable (auto-configured in HappyCapy)
- Internet connection (to clone from anthropics/skills)

## Best Practices

**Recommended Workflow:**

1. Read official `/skill-creator` to learn principles
2. Use HappyCapy Skill Creator to generate quickly
3. Refine based on official guidelines
4. Test and iterate

## Documentation

- **Full Documentation**: [GitHub Repository](https://github.com/Y1fe1-Yang/happycapy-skill-creator)
- **SKILL.md**: Core workflow and usage
- **CHANGELOG**: Version history
- **CONTRIBUTING**: How to contribute

## Version

**Current**: v1.2.0 - Optimized Structure

### What's New in v1.2.0
- Simplified SKILL.md from 247 to 94 lines (-62%)
- Removed 9 unnecessary documentation files
- Improved triggering with specific use cases
- Applied progressive disclosure design pattern
- 100% aligned with official skill-creator guidelines

## Links

- **Repository**: https://github.com/Y1fe1-Yang/happycapy-skill-creator
- **Releases**: https://github.com/Y1fe1-Yang/happycapy-skill-creator/releases
- **Issues**: https://github.com/Y1fe1-Yang/happycapy-skill-creator/issues

## License

MIT License - See repository for details.

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](https://github.com/Y1fe1-Yang/happycapy-skill-creator/blob/main/CONTRIBUTING.md) for guidelines.

---

**Made with ❤️ for the HappyCapy community**
