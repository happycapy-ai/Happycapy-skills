# Happycapy Skills

A curated collection of high-quality Claude Code skills to enhance your development workflow.

## About This Repository

This repository contains carefully selected skills that demonstrate best practices and powerful capabilities with Claude's skills system. Each skill is designed to be production-ready, well-documented, and easy to integrate into your workflow.

Browse through these skills to find tools for content creation, presentation design, development workflows, and more. Each skill is self-contained in its own folder with a `SKILL.md` file containing the instructions and metadata that Claude uses.

## Skills

### [reddit-post-writer](./skills/reddit-post-writer/)
Generate authentic Reddit posts that sound human, avoid AI detection, and spark engagement across 25+ subreddits. Includes 7-persona committee review system and subreddit-specific guidelines for different communities.

**Original Source:** [niveshdandyan/reddit-post-skill](https://github.com/niveshdandyan/reddit-post-skill)

### [frontend-slides](./skills/frontend-slides/)
Create stunning, animation-rich HTML presentations from scratch or convert PowerPoint files to web format. Zero dependencies, 12 distinctive design presets, fully responsive and viewport-fitted. Perfect for pitch decks, conference talks, and teaching.

**Original Source:** [zarazhangrui/frontend-slides](https://github.com/zarazhangrui/frontend-slides)

### [treatment-plans](./skills/treatment-plans/)
Generate concise (3-4 page), focused medical treatment plans in LaTeX/PDF format for all clinical specialties. Supports general medical treatment, rehabilitation therapy, mental health care, chronic disease management, perioperative care, and pain management. Includes SMART goal frameworks, evidence-based interventions with minimal text citations, regulatory compliance (HIPAA), and professional formatting. Prioritizes brevity and clinical actionability.

**Original Source:** [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates/tree/main/cli-tool/components/skills/scientific/treatment-plans)

### [goplaces](./skills/goplaces/)
Query Google Places API (New) via the goplaces CLI for text search, place details, resolve, and reviews. Modern CLI with human-friendly output by default and JSON format for scripting. Includes advanced filters like open now, minimum rating, location bias, and radius search.

**Original Source:** [steipete/goplaces](https://github.com/steipete/goplaces) via [openclaw/skills](https://github.com/openclaw/skills/tree/main/skills/steipete/goplaces)

---

## Installation

### For Claude Code Users

Clone this repository and install individual skills:

```bash
# Clone the repository
git clone https://github.com/trickleai/Happycapy-skills.git
cd Happycapy-skills

# Install a specific skill
mkdir -p ~/.claude/skills
cp -r skills/reddit-post-writer ~/.claude/skills/
cp -r skills/frontend-slides ~/.claude/skills/
cp -r skills/treatment-plans ~/.claude/skills/
cp -r skills/goplaces ~/.claude/skills/

# Or install all skills at once
cp -r skills/* ~/.claude/skills/
```

### Repository Structure

```
Happycapy-skills/
├── README.md
├── LICENSE
└── skills/
    ├── reddit-post-writer/
    │   ├── SKILL.md
    │   ├── references/
    │   └── LICENSE
    ├── frontend-slides/
    │   ├── SKILL.md
    │   ├── STYLE_PRESETS.md
    │   └── LICENSE
    ├── treatment-plans/
    │   ├── SKILL.md
    │   ├── README.md
    │   ├── assets/
    │   ├── scripts/
    │   └── references/
    └── goplaces/
        ├── SKILL.md
        └── README.md
```

Each skill follows the standard Claude Code skill structure with a `SKILL.md` file and any necessary reference materials.

---

## Creating a Custom Skill

Skills are simple to create - just a folder with a `SKILL.md` file containing YAML frontmatter and instructions:

```markdown
---
name: my-skill-name
description: A clear description of what this skill does and when to use it
---

# My Skill Name

[Add your instructions here that Claude will follow when this skill is active]

## Examples
- Example usage 1
- Example usage 2

## Guidelines
- Guideline 1
- Guideline 2
```

The frontmatter requires:
- `name` - A unique identifier for your skill (lowercase, hyphens for spaces)
- `description` - A complete description of what the skill does and when to use it

For more details, see [How to create custom skills](https://support.claude.com/en/articles/12512198-creating-custom-skills).

---

## Contributing

We welcome contributions! If you have a skill you'd like to add to this collection:

1. Fork this repository
2. Create a new folder under `skills/` with your skill name
3. Add a `SKILL.md` file with proper frontmatter and instructions
4. Include any necessary reference materials
5. Add a LICENSE file if different from the repository license
6. Update this README to list your skill
7. Submit a pull request

Please ensure your skill:
- Has a clear, descriptive name
- Includes comprehensive documentation
- Follows Claude Code best practices
- Works reliably and is production-ready
- Includes proper attribution if derived from other work

---

## License

Each skill in this collection maintains its original license. Please refer to individual skill directories for specific license information.

The repository itself is licensed under MIT License - see [LICENSE](LICENSE) for details.

---

**Repository:** [github.com/trickleai/Happycapy-skills](https://github.com/trickleai/Happycapy-skills)

**Maintained by:** [Trickle AI](https://github.com/trickleai)

## Related Resources

- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)
- [Using skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [Agent Skills Standard](http://agentskills.io)
- [Anthropic's Official Skills Repository](https://github.com/anthropics/skills)
