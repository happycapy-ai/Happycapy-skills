---
name: happycapy-skill-creator
description: Create HappyCapy skills by finding and adapting similar skills from anthropics/skills repository. Use when the user wants to: (1) Create a new skill for a specific task or domain, (2) Adapt an existing skill with new features, (3) Build a skill that needs to work within HappyCapy constraints (Python 3.11, Node.js 24, no Docker). Triggers include requests like "create a skill for X", "build a skill that does Y", "I need a skill to handle Z", or when discussing skill development for HappyCapy environment.
---

# HappyCapy Skill Creator

Automate skill creation through **adaptation** rather than building from scratch.

## Workflow

```bash
python scripts/create_skill.py "Your requirement here" --name skill-name
```

**Process:**
1. Search anthropics/skills for similar skills (semantic + LLM)
2. Clone the closest match
3. Add requested features using LLM
4. Auto-fix HappyCapy compatibility (remove Docker, adapt dependencies)
5. Package as `.skill` file

## Core Scripts

### create_skill.py
Main orchestrator - runs full workflow end-to-end

### semantic_search.py
LLM-powered semantic search of anthropics/skills repository

### clone_skill.py
Clone skill from GitHub (anthropics/skills)

### integrate_feature.py
Add new features using LLM fine-tuning

### check_compatibility.py
Scan for HappyCapy incompatibilities (Docker, unsupported runtimes, memory issues)

### auto_fix.py
Auto-fix compatibility issues with LLM rewrites

### package_skill.py
Create distributable .skill file (zip format)

## Examples

**Compress PDFs:**
```bash
python scripts/create_skill.py "I need to compress PDF files"
# Finds pdf skill → Clones → Adds compress function → Packages
```

**Extract video frames:**
```bash
python scripts/create_skill.py "Extract frames from videos every second"
# Finds video-frames skill → Clones → Adds interval parameter → Packages
```

## Environment Constraints

HappyCapy provides:
- ✅ Python 3.11, Node.js 24
- ✅ pandoc, ImageMagick, jq
- ✅ 4GB RAM, 2 CPU cores

HappyCapy does NOT support:
- ❌ Docker, Java, Ruby, Go

The tool automatically fixes incompatibilities.

## Requirements

- Python 3.11+
- `AI_GATEWAY_API_KEY` environment variable (auto-configured in HappyCapy)
- Internet connection (to clone from anthropics/skills)

## Advanced

**Use improved auto-fix with batching:**
```python
from scripts.auto_fix_improved import fix_compatibility_issues

fix_compatibility_issues(
    skill_path=path,
    issues=issues,
    batch_size=5,      # Process 5 issues per batch
    max_retries=2      # Retry failed fixes up to 2 times
)
```

**Troubleshooting:** See `references/bugfixes.md` for known issues and solutions

**Environment details:** See `references/happycapy-environment.md`
