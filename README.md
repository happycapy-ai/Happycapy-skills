# Happycapy Skills

A curated collection of high-quality Claude Code skills to enhance your development workflow.

## About This Repository

This repository contains carefully selected skills that demonstrate best practices and powerful capabilities with Claude's skills system. Each skill is designed to be production-ready, well-documented, and easy to integrate into your workflow.

Browse through these skills to find tools for content creation, presentation design, development workflows, and more. Each skill is self-contained in its own folder with a `SKILL.md` file containing the instructions and metadata that Claude uses.

## Skills

### [3d-web-experience](./skills/3d-web-experience/)
Expert in building 3D experiences for the web using Three.js, React Three Fiber, Spline, and WebGL. Covers product configurators, 3D portfolios, immersive websites, scroll-driven 3D interactions, and performance optimization. Includes guidance on 3D stack selection, model pipeline optimization, and mobile device support.

**Original Source:** [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates/tree/main/cli-tool/components/skills/creative-design/3d-web-experience)

### [happycapy-skill-creator](./skills/happycapy-skill-creator/)
Automated Claude skill creator for HappyCapy environment. Finds and adapts similar skills from anthropics/skills repository using semantic search, LLM-powered adaptation, and auto-fix for compatibility. Creates ready-to-install `.skill` files with 90%+ success rate. Complements the official `/skill-creator` by automating the creation process.

**Original Source:** [Y1fe1-Yang/happycapy-skill-creator](https://github.com/Y1fe1-Yang/happycapy-skill-creator)

### [reddit-post-writer](./skills/reddit-post-writer/)
Generate authentic Reddit posts that sound human, avoid AI detection, and spark engagement across 25+ subreddits. Includes 7-persona committee review system and subreddit-specific guidelines for different communities.

**Original Source:** [niveshdandyan/reddit-post-skill](https://github.com/niveshdandyan/reddit-post-skill)

### [frontend-slides](./skills/frontend-slides/)
Create stunning, animation-rich HTML presentations from scratch or convert PowerPoint files to web format. Zero dependencies, 12 distinctive design presets, fully responsive and viewport-fitted. Perfect for pitch decks, conference talks, and teaching.

**Original Source:** [zarazhangrui/frontend-slides](https://github.com/zarazhangrui/frontend-slides)

### [treatment-plans](./skills/treatment-plans/)
Generate concise (3-4 page), focused medical treatment plans in LaTeX/PDF format for all clinical specialties. Supports general medical treatment, rehabilitation therapy, mental health care, chronic disease management, perioperative care, and pain management. Includes SMART goal frameworks, evidence-based interventions with minimal text citations, regulatory compliance (HIPAA), and professional formatting. Prioritizes brevity and clinical actionability.

**Original Source:** [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates/tree/main/cli-tool/components/skills/scientific/treatment-plans)

### [writing-clearly-and-concisely](./skills/writing-clearly-and-concisely/)
Write with clarity and force using William Strunk Jr.'s timeless principles from The Elements of Style. Applies proven rules for clear, strong, professional writing while avoiding common AI writing patterns. Use when writing documentation, commit messages, error messages, reports, or any prose for human readers. Emphasizes active voice, concrete language, and cutting needless words.

**Original Source:** [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates/tree/main/cli-tool/components/skills/enterprise-communication/writing-clearly-and-concisely)

### [goplaces](./skills/goplaces/)
Query Google Places API (New) via the goplaces CLI for text search, place details, resolve, and reviews. Modern CLI with human-friendly output by default and JSON format for scripting. Includes advanced filters like open now, minimum rating, location bias, and radius search.

**Original Source:** [steipete/goplaces](https://github.com/steipete/goplaces) via [openclaw/skills](https://github.com/openclaw/skills/tree/main/skills/steipete/goplaces)

### [image-enhancer](./skills/image-enhancer/)
Improves the quality of images, especially screenshots, by enhancing resolution, sharpness, and clarity. Perfect for preparing images for presentations, documentation, or social media posts. Analyzes image quality, enhances resolution, improves sharpness, reduces artifacts, and optimizes for different use cases. Supports batch processing and keeps original files as backup.

**Original Source:** [ComposioHQ/awesome-claude-skills - image-enhancer](https://github.com/ComposioHQ/awesome-claude-skills/tree/master/image-enhancer)

### [video-downloader](./skills/video-downloader/)
Downloads videos from YouTube and other platforms for offline viewing, editing, or archival. Handles various formats (MP4, WebM, audio-only) and quality options (480p to 4K). Supports batch downloads, playlists, and metadata preservation. Perfect for saving educational content, archiving important videos, or downloading your own content from platforms. Includes copyright and fair use guidelines.

**Original Source:** [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates/tree/main/cli-tool/components/skills/media/video-downloader)

### [xiaohongshu-recruiter](./skills/xiaohongshu-recruiter/)
Publish high-quality AI job recruitment posts on Xiaohongshu (Little Red Book). Automatically generates geek-style recruitment cover images and detail images, with automated publishing scripts. Built with Systemic Flux design philosophy, supports one-click publishing workflow.

**Original Source:** [iOfficeAI/AionUi](https://github.com/iOfficeAI/AionUi/tree/main/skills/xiaohongshu-recruiter)

### [youtube-music](./skills/youtube-music/)
Search and play music tracks on YouTube Music through MCP integration. Enables AI assistants to search for songs by title or artist name and play them directly in your default web browser. Requires a Google YouTube API key for operation.

**Original Source:** [instructa/mcp-youtube-music](https://github.com/instructa/mcp-youtube-music)

### [nano-banana-pro](./skills/nano-banana-pro/)
Generate or edit images using Google's Gemini 3 Pro Image API (Nano Banana Pro). Create images from text descriptions, edit existing images with natural language instructions, or combine up to 14 images into composite scenes. Supports 1K, 2K, and 4K resolutions. Requires uv package manager and GEMINI_API_KEY.

**Original Source:** [openclaw/openclaw](https://github.com/openclaw/openclaw/tree/main/skills/nano-banana-pro)

### [video-frames](./skills/video-frames/)
Extract single frames or create quick thumbnails from videos using ffmpeg. Supports extracting frames by timestamp, frame index, or first frame. Perfect for video analysis, creating thumbnails, inspecting specific moments, or extracting UI frames. Outputs to JPG for quick sharing or PNG for crisp quality.

**Original Source:** [clawdbot/clawdbot](https://github.com/clawdbot/clawdbot/tree/main/skills/video-frames)

### [canvas-design](./skills/canvas-design/)
Create beautiful visual art in PNG and PDF documents using design philosophy. Use when creating posters, pieces of art, designs, or other static visual pieces. Generates original visual designs through a two-step process: creating a design philosophy (aesthetic movement) and expressing it visually on a canvas. Emphasizes master-level craftsmanship with minimal text and visual-first communication.

**Original Source:** [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/canvas-design)

### [claude-code-templates](./skills/claude-code-templates/)
CLI tool for configuring and monitoring Claude Code with a comprehensive collection of 600+ AI agents, 200+ custom commands, 55+ external service integrations (MCPs), 60+ settings, 39+ hooks, and 14+ project templates. Use when users need to install or manage Claude Code components, browse available templates at aitmpl.com, run analytics/health checks, or set up development workflows. Integrates with Claude Code, Cursor, Cline, and 10+ other AI coding platforms.

**Original Source:** [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates)

### [slack-gif-creator](./skills/slack-gif-creator/)
A toolkit for creating animated GIFs optimized for Slack. Provides composable animation primitives, validators for Slack requirements, and utilities for creating custom emoji GIFs (128x128, under 64KB) and message GIFs (480x480, under 2MB). Includes easing functions, frame helpers, and support for animations like shake, pulse, bounce, spin, fade, and more. Draw graphics from scratch using PIL primitives.

**Original Source:** [anthropics/skills - slack-gif-creator](https://github.com/anthropics/skills/tree/main/skills/slack-gif-creator)

### [data-storytelling](./skills/data-storytelling/)
Transform data into compelling narratives using visualization, context, and persuasive structure. Use when presenting analytics to stakeholders, creating data reports, or building executive presentations. Includes story frameworks (problem-solution, trend, comparison), visualization techniques, presentation templates, and best practices for writing headlines and handling uncertainty.

**Original Source:** [wshobson/agents](https://github.com/wshobson/agents/tree/main/plugins/business-analytics/skills/data-storytelling)

### [redbook-creator-publish](./skills/redbook-creator-publish/)
Xiaohongshu (Little Red Book) post creation and publishing skill. Features: (1) Generate Xiaohongshu-style post content (title + body + tags), (2) Generate related post images, (3) Auto-upload to Xiaohongshu creator platform (default auto-upload, manual guidance on failure), (4) Generate local preview HTML files. Uses Playwright for Python for browser automation, supports deep topic search, images in PNG/JPG format (9:16 vertical ratio).

**Original Source:** [NeverSight/skills_feed - yanquankun/redbook-creator-publish](https://github.com/NeverSight/skills_feed/tree/main/data/skills-md/yanquankun/redbook-creator-publish/redbook-creator-publish)

### [skill-creator](./skills/skill-creator/)
Guide for creating effective skills. Use when designing, structuring, or packaging skills with scripts, references, and assets. Includes helper scripts for initializing, validating, and packaging skills. Provides comprehensive guidance on skill architecture, progressive disclosure patterns, and best practices for token-efficient skill design. Features bundled scripts: init_skill.py (generate skill structure), package_skill.py (validate and package), and quick_validate.py (validation).

**Original Source:** [openclaw/openclaw](https://github.com/openclaw/openclaw/tree/main/skills/skill-creator)

### [mobile-design](./skills/mobile-design/)
Mobile-first design thinking and decision-making for iOS and Android apps. Touch interaction, performance patterns, platform conventions. Teaches principles, not fixed values. Use when building React Native, Flutter, or native mobile apps. Includes comprehensive guidance on touch psychology, Fitts' Law, thumb zones, mobile performance optimization, platform-specific design patterns (iOS HIG & Material Design 3), navigation patterns, and framework selection. Features 13 detailed reference files, decision trees, and a mobile UX audit script.

**Original Source:** [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates/tree/main/cli-tool/components/skills/creative-design/mobile-design)

### [resume-assistant](./skills/resume-assistant/)
Intelligent resume assistant powered by five specialized AI agents for end-to-end job search support: (1) Story Mining - discover experience highlights, (2) Job Matching - recommend suitable positions, (3) Resume Optimization - customize content for job descriptions, (4) Mock Interviews - practice with feedback, (5) Skill Development - gap analysis and improvement plans. Supports PDF/DOCX/HTML/Excel multi-format output with built-in Chinese fonts, ready to use out of the box.

**Original Source:** [Y1fe1-Yang/resume-assistant-skill](https://github.com/Y1fe1-Yang/resume-assistant-skill)

### [film-creator](./skills/film-creator/)
AI-powered film creation assistant that transforms a single sentence or image into a complete 30-second cinematic film. Automatically generates professional screenplay with 5-scene structure, creates high-quality video for each scene using AI models (Google Veo, OpenAI Sora, BytePlus Seedance), and assembles them into a polished film with FFmpeg. Perfect for social media content, marketing videos, and rapid film prototyping.

**Original Source:** [Y1fe1-Yang/film-creator-skill](https://github.com/Y1fe1-Yang/film-creator-skill)

### [weather](./skills/weather/)
Get current weather and forecasts using free services without requiring API keys. Uses wttr.in for rich terminal weather displays with ASCII art and Open-Meteo for JSON API responses. Supports multiple output formats (text, PNG images), cities, airport codes, and coordinates. Perfect for quick weather checks in the terminal or programmatic weather data access.

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
cp -r skills/3d-web-experience ~/.claude/skills/
cp -r skills/happycapy-skill-creator ~/.claude/skills/
cp -r skills/reddit-post-writer ~/.claude/skills/
cp -r skills/frontend-slides ~/.claude/skills/
cp -r skills/treatment-plans ~/.claude/skills/
cp -r skills/writing-clearly-and-concisely ~/.claude/skills/
cp -r skills/goplaces ~/.claude/skills/
cp -r skills/image-enhancer ~/.claude/skills/
cp -r skills/video-downloader ~/.claude/skills/
cp -r skills/xiaohongshu-recruiter ~/.claude/skills/
cp -r skills/youtube-music ~/.claude/skills/
cp -r skills/nano-banana-pro ~/.claude/skills/
cp -r skills/video-frames ~/.claude/skills/
cp -r skills/canvas-design ~/.claude/skills/
cp -r skills/claude-code-templates ~/.claude/skills/
cp -r skills/slack-gif-creator ~/.claude/skills/
cp -r skills/data-storytelling ~/.claude/skills/
cp -r skills/redbook-creator-publish ~/.claude/skills/
cp -r skills/skill-creator ~/.claude/skills/
cp -r skills/mobile-design ~/.claude/skills/
cp -r skills/resume-assistant ~/.claude/skills/
cp -r skills/film-creator ~/.claude/skills/
cp -r skills/weather ~/.claude/skills/

# Or install all skills at once
cp -r skills/* ~/.claude/skills/
```

### Repository Structure

```
Happycapy-skills/
├── README.md
├── LICENSE
└── skills/
    ├── 3d-web-experience/
    │   ├── SKILL.md
    │   └── README.md
    ├── happycapy-skill-creator/
    │   ├── SKILL.md
    │   └── README.md
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
    ├── writing-clearly-and-concisely/
    │   ├── SKILL.md
    │   ├── README.md
    │   ├── signs-of-ai-writing.md
    │   └── elements-of-style/
    │       ├── 01-introductory.md
    │       ├── 02-elementary-rules-of-usage.md
    │       ├── 03-elementary-principles-of-composition.md
    │       ├── 04-a-few-matters-of-form.md
    │       └── 05-words-and-expressions-commonly-misused.md
    ├── goplaces/
    │   ├── SKILL.md
    │   └── README.md
    ├── image-enhancer/
    │   ├── SKILL.md
    │   └── README.md
    ├── video-downloader/
    │   ├── SKILL.md
    │   └── README.md
    ├── xiaohongshu-recruiter/
    │   ├── SKILL.md
    │   ├── README.md
    │   ├── assets/
    │   ├── scripts/
    │   └── references/
    ├── youtube-music/
    │   ├── SKILL.md
    │   └── README.md
    ├── nano-banana-pro/
    │   ├── SKILL.md
    │   ├── README.md
    │   └── scripts/
    │       └── generate_image.py
    ├── video-frames/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── frame.sh
    ├── canvas-design/
    │   ├── SKILL.md
    │   └── README.md
    ├── claude-code-templates/
    │   ├── SKILL.md
    │   └── README.md
    ├── slack-gif-creator/
    │   ├── SKILL.md
    │   ├── README.md
    │   ├── LICENSE.txt
    │   ├── requirements.txt
    │   └── core/
    │       ├── easing.py
    │       ├── frame_composer.py
    │       ├── gif_builder.py
    │       └── validators.py
    ├── data-storytelling/
    │   ├── SKILL.md
    │   └── README.md
    ├── redbook-creator-publish/
    │   ├── SKILL.md
    │   └── README.md
    ├── skill-creator/
    │   ├── SKILL.md
    │   ├── README.md
    │   ├── license.txt
    │   └── scripts/
    │       ├── init_skill.py
    │       ├── package_skill.py
    │       └── quick_validate.py
    ├── mobile-design/
    │   ├── SKILL.md
    │   ├── README.md
    │   ├── decision-trees.md
    │   ├── mobile-backend.md
    │   ├── mobile-color-system.md
    │   ├── mobile-debugging.md
    │   ├── mobile-design-thinking.md
    │   ├── mobile-navigation.md
    │   ├── mobile-performance.md
    │   ├── mobile-testing.md
    │   ├── mobile-typography.md
    │   ├── platform-android.md
    │   ├── platform-ios.md
    │   ├── touch-psychology.md
    │   └── scripts/
    │       └── mobile_audit.py
    ├── resume-assistant/
    │   ├── SKILL.md
    │   └── README.md
    ├── film-creator/
    │   ├── SKILL.md
    │   └── README.md
    └── weather/
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

**Repository:** [github.com/happycapy-ai/Happycapy-skills](https://github.com/happycapy-ai/Happycapy-skills)

**Maintained by:** [Happycapy AI](https://github.com/happycapy-ai)

## Related Resources

- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)
- [Using skills in Claude](https://support.claude.com/en/articles/12512180-using-skills-in-claude)
- [Agent Skills Standard](http://agentskills.io)
- [Anthropic's Official Skills Repository](https://github.com/anthropics/skills)
