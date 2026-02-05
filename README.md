# Happycapy Skills

A curated collection of high-quality Claude Code skills to enhance your development workflow.

## About This Repository

This repository contains carefully selected skills that demonstrate best practices and powerful capabilities with Claude's skills system. Each skill is designed to be production-ready, well-documented, and easy to integrate into your workflow.

Browse through these skills to find tools for content creation, presentation design, development workflows, and more. Each skill is self-contained in its own folder with a `SKILL.md` file containing the instructions and metadata that Claude uses.

## Skills

### Anthropic Skills

#### [skill-creator](./skills/skill-creator/)
Guide for creating effective skills. Use when designing, structuring, or packaging skills with scripts, references, and assets. Includes helper scripts for initializing, validating, and packaging skills. Provides comprehensive guidance on skill architecture, progressive disclosure patterns, and best practices for token-efficient skill design.

**Original Source:** [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/skill-creator)

#### [pdf](./skills/pdf/)
Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, and handling forms. When Claude needs to fill in a PDF form or programmatically process, generate, or analyze PDF documents at scale.

**Original Source:** [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/pdf)

#### [canvas-design](./skills/canvas-design/)
Create beautiful visual art in PNG and PDF documents using design philosophy. Use when creating posters, pieces of art, designs, or other static visual pieces. Generates original visual designs through a two-step process: creating a design philosophy (aesthetic movement) and expressing it visually on a canvas.

**Original Source:** [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/canvas-design)

#### [slack-gif-creator](./skills/slack-gif-creator/)
A toolkit for creating animated GIFs optimized for Slack. Provides composable animation primitives, validators for Slack requirements, and utilities for creating custom emoji GIFs (128x128, under 64KB) and message GIFs (480x480, under 2MB).

**Original Source:** [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/slack-gif-creator)

### Vercel Skills

#### [find-skills](./skills/find-skills/)
Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", or express interest in extending capabilities. This skill should be used when the user is looking for functionality that might exist as an installable skill.

**Original Source:** [vercel-labs/skills](https://github.com/vercel-labs/skills/tree/main/skills/find-skills)

#### [next-best-practices](./skills/next-best-practices/)
Next.js best practices covering file conventions, RSC boundaries, data patterns, async APIs, metadata, error handling, route handlers, image/font optimization, and bundling. Use when writing or reviewing Next.js code to ensure optimal patterns.

**Original Source:** [vercel-labs/next-skills](https://github.com/vercel-labs/next-skills)

### Inference.sh Skills

#### [ai-image-generation](./skills/ai-image-generation/)
Generate AI images with FLUX, Gemini, Grok, Seedream, Reve and 50+ models via inference.sh CLI. Capabilities include text-to-image, image-to-image, inpainting, LoRA, image editing, upscaling, and text rendering. Use for AI art, product mockups, concept art, social media graphics, and marketing visuals.

**Original Source:** [inference-sh/skills](https://github.com/inference-sh/skills)

#### [ai-video-generation](./skills/ai-video-generation/)
Generate AI videos with Google Veo, Seedance, Wan, Grok and 40+ models via inference.sh CLI. Capabilities include text-to-video, image-to-video, lipsync, avatar animation, video upscaling, and foley sound. Use for social media videos, marketing content, explainer videos, and product demos.

**Original Source:** [inference-sh/skills](https://github.com/inference-sh/skills)

### Supabase Skills

#### [supabase-postgres-best-practices](./skills/supabase-postgres-best-practices/)
Postgres performance optimization and best practices for Supabase. Covers query optimization, indexing strategies, connection pooling, data patterns, security best practices, and monitoring. Use when optimizing slow queries or improving database design.

**Original Source:** [supabase/agent-skills](https://github.com/supabase/agent-skills)

### Community Skills

#### [3d-web-experience](./skills/3d-web-experience/)
Expert in building 3D experiences for the web using Three.js, React Three Fiber, Spline, and WebGL. Covers product configurators, 3D portfolios, immersive websites, scroll-driven 3D interactions, and performance optimization.

**Original Source:** [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates/tree/main/cli-tool/components/skills/creative-design/3d-web-experience)

#### [happycapy-skill-creator](./skills/happycapy-skill-creator/)
Automated Claude skill creator for HappyCapy environment. Finds and adapts similar skills from anthropics/skills repository using semantic search, LLM-powered adaptation, and auto-fix for compatibility.

**Original Source:** [Y1fe1-Yang/happycapy-skill-creator](https://github.com/Y1fe1-Yang/happycapy-skill-creator)

#### [reddit-post-writer](./skills/reddit-post-writer/)
Generate authentic Reddit posts that sound human, avoid AI detection, and spark engagement across 25+ subreddits. Includes 7-persona committee review system and subreddit-specific guidelines.

**Original Source:** [niveshdandyan/reddit-post-skill](https://github.com/niveshdandyan/reddit-post-skill)

#### [frontend-slides](./skills/frontend-slides/)
Create stunning, animation-rich HTML presentations from scratch or convert PowerPoint files to web format. Zero dependencies, 12 distinctive design presets, fully responsive and viewport-fitted.

**Original Source:** [zarazhangrui/frontend-slides](https://github.com/zarazhangrui/frontend-slides)

#### [treatment-plans](./skills/treatment-plans/)
Generate concise (3-4 page), focused medical treatment plans in LaTeX/PDF format for all clinical specialties. Includes SMART goal frameworks, evidence-based interventions, regulatory compliance (HIPAA), and professional formatting.

**Original Source:** [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates/tree/main/cli-tool/components/skills/scientific/treatment-plans)

#### [writing-clearly-and-concisely](./skills/writing-clearly-and-concisely/)
Write with clarity and force using William Strunk Jr.'s timeless principles from The Elements of Style. Use when writing documentation, commit messages, error messages, reports, or any prose for human readers.

**Original Source:** [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates/tree/main/cli-tool/components/skills/enterprise-communication/writing-clearly-and-concisely)

#### [goplaces](./skills/goplaces/)
Query Google Places API (New) via the goplaces CLI for text search, place details, resolve, and reviews. Modern CLI with human-friendly output by default and JSON format for scripting.

**Original Source:** [steipete/goplaces](https://github.com/steipete/goplaces) via [openclaw/skills](https://github.com/openclaw/skills/tree/main/skills/steipete/goplaces)

#### [image-enhancer](./skills/image-enhancer/)
Improves the quality of images, especially screenshots, by enhancing resolution, sharpness, and clarity. Perfect for preparing images for presentations, documentation, or social media posts.

**Original Source:** [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills/tree/master/image-enhancer)

#### [video-downloader](./skills/video-downloader/)
Downloads videos from YouTube and other platforms for offline viewing, editing, or archival. Handles various formats and quality options. Includes copyright and fair use guidelines.

**Original Source:** [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates/tree/main/cli-tool/components/skills/media/video-downloader)

#### [xiaohongshu-recruiter](./skills/xiaohongshu-recruiter/)
Publish high-quality AI job recruitment posts on Xiaohongshu (Little Red Book). Automatically generates geek-style recruitment cover images and detail images, with automated publishing scripts.

**Original Source:** [iOfficeAI/AionUi](https://github.com/iOfficeAI/AionUi/tree/main/skills/xiaohongshu-recruiter)

#### [youtube-music](./skills/youtube-music/)
Search and play music tracks on YouTube Music through MCP integration. Enables AI assistants to search for songs by title or artist name and play them directly in your default web browser.

**Original Source:** [instructa/mcp-youtube-music](https://github.com/instructa/mcp-youtube-music)

#### [nano-banana-pro](./skills/nano-banana-pro/)
Generate or edit images using Google's Gemini 3 Pro Image API (Nano Banana Pro). Create images from text descriptions, edit existing images with natural language instructions, or combine up to 14 images into composite scenes.

**Original Source:** [openclaw/openclaw](https://github.com/openclaw/openclaw/tree/main/skills/nano-banana-pro)

#### [video-frames](./skills/video-frames/)
Extract single frames or create quick thumbnails from videos using ffmpeg. Perfect for video analysis, creating thumbnails, inspecting specific moments, or extracting UI frames.

**Original Source:** [clawdbot/clawdbot](https://github.com/clawdbot/clawdbot/tree/main/skills/video-frames)

#### [claude-code-templates](./skills/claude-code-templates/)
CLI tool for configuring and monitoring Claude Code with a comprehensive collection of 600+ AI agents, 200+ custom commands, 55+ external service integrations (MCPs), 60+ settings, 39+ hooks, and 14+ project templates.

**Original Source:** [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates)

#### [data-storytelling](./skills/data-storytelling/)
Transform data into compelling narratives using visualization, context, and persuasive structure. Use when presenting analytics to stakeholders, creating data reports, or building executive presentations.

**Original Source:** [wshobson/agents](https://github.com/wshobson/agents/tree/main/plugins/business-analytics/skills/data-storytelling)

#### [redbook-creator-publish](./skills/redbook-creator-publish/)
Xiaohongshu (Little Red Book) post creation and publishing skill. Generate Xiaohongshu-style post content, related post images, and auto-upload to creator platform.

**Original Source:** [NeverSight/skills_feed](https://github.com/NeverSight/skills_feed/tree/main/data/skills-md/yanquankun/redbook-creator-publish/redbook-creator-publish)

#### [mobile-design](./skills/mobile-design/)
Mobile-first design thinking and decision-making for iOS and Android apps. Touch interaction, performance patterns, platform conventions. Use when building React Native, Flutter, or native mobile apps.

**Original Source:** [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates/tree/main/cli-tool/components/skills/creative-design/mobile-design)

#### [resume-assistant](./skills/resume-assistant/)
Intelligent resume assistant powered by five specialized AI agents for end-to-end job search support. Supports PDF/DOCX/HTML/Excel multi-format output with built-in Chinese fonts.

**Original Source:** [Y1fe1-Yang/resume-assistant-skill](https://github.com/Y1fe1-Yang/resume-assistant-skill)

#### [film-creator](./skills/film-creator/)
AI-powered film creation assistant that transforms a single sentence or image into a complete 30-second cinematic film. Automatically generates professional screenplay and creates high-quality video.

**Original Source:** [Y1fe1-Yang/film-creator-skill](https://github.com/Y1fe1-Yang/film-creator-skill)

#### [weather](./skills/weather/)
Get current weather and forecasts using free services without requiring API keys. Uses wttr.in for rich terminal weather displays and Open-Meteo for JSON API responses.

**Original Source:** [openclaw/openclaw](https://github.com/openclaw/openclaw/tree/main/skills/weather)

---

## Installation

### For Claude Code Users

Clone this repository and install individual skills:

```bash
# Clone the repository
git clone https://github.com/happycapy-ai/Happycapy-skills.git
cd Happycapy-skills

# Install a specific skill
mkdir -p ~/.claude/skills
cp -r skills/skill-creator ~/.claude/skills/
cp -r skills/pdf ~/.claude/skills/
cp -r skills/find-skills ~/.claude/skills/
cp -r skills/next-best-practices ~/.claude/skills/
cp -r skills/ai-image-generation ~/.claude/skills/
cp -r skills/ai-video-generation ~/.claude/skills/
cp -r skills/supabase-postgres-best-practices ~/.claude/skills/

# Or install all skills at once
cp -r skills/* ~/.claude/skills/
```

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

**Repository:** [github.com/happycapy-ai/Happycapy-skills](https://github.com/happycapy-ai/Happycapy-skills)

**Maintained by:** [Happycapy AI](https://github.com/happycapy-ai)

## Related Resources

- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)
- [Using skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [Agent Skills Standard](http://agentskills.io)
- [Anthropic's Official Skills Repository](https://github.com/anthropics/skills)
- [Vercel Agent Skills](https://github.com/vercel-labs/agent-skills)
- [Inference.sh Skills](https://github.com/inference-sh/skills)
- [Supabase Agent Skills](https://github.com/supabase/agent-skills)
