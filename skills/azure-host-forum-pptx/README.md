# azure-host-forum-pptx

A Claude Code skill for generating editable PowerPoint decks in the fixed **Azure Host Forum** visual style — bold contemporary industry sharing event aesthetic with sky-blue backgrounds, deep green typography, olive speaker columns, and circular portrait frames.

## What This Does

**azure-host-forum-pptx** produces polished, editable `.pptx` files that look and feel like a premium industry forum or speaker event poster system. Every element — titles, panels, portrait frames, agenda rows, metadata blocks — is a native editable PowerPoint object.

### Key Features

- **Fixed Visual Brand** — Sky-blue `#65AEFF` background, deep green `#07461E` typography, olive `#728E03` side panels, cream `#F1F0EA` portrait details
- **Speaker Column Layout** — Large left text field with strong right olive column for circular speaker portraits
- **AI Portrait Generation** — Optionally generates clean editorial speaker headshots using `gpt-image-2`
- **Smart Intake** — Asks 3 focused questions (topic, slide count, image source), then infers all remaining details
- **Event Language** — Rewrites any topic as a bold hosted forum, expert talk, panel, or creative industry event
- **Visual QA** — Inspects every slide for overlaps, collisions, and word-count violations before delivery

## Installation

```bash
mkdir -p ~/.claude/skills/azure-host-forum-pptx
cp SKILL.md ~/.claude/skills/azure-host-forum-pptx/
```

Then use it by mentioning **Azure Host Forum** or asking for a forum/speaker-event style deck in Claude Code.

## Usage

```
> "Make an Azure Host Forum deck about product design"
> "Create a forum deck for our AI workshop, 8 slides, generate speaker portraits"
> "Azure host forum style presentation on fintech trends"
```

The skill will:
1. Ask up to 3 focused questions (topic, slide count, image handling)
2. Optionally generate speaker portraits with `gpt-image-2`
3. Build the PPTX using PptxGenJS via the `pptx` base skill
4. Run visual QA on every slide
5. Save to `outputs/<topic-slug>.pptx`

## Visual Style

| Element | Value |
|---------|-------|
| Background | Sky-blue `#65AEFF` |
| Primary text | Deep green `#07461E` |
| Side panels | Olive `#728E03` |
| Portrait details | Cream `#F1F0EA` |
| Cover title | 72–110 pt condensed bold sans |
| Slide headlines | 40–64 pt |
| Body text | 22–30 pt |
| Metadata | 12–16 pt |

## Slide Structure (default 8 slides)

1. Cover — two speaker portraits in right olive column
2. Session premise or forum theme
3. Host / speaker 1 profile
4. Guest / speaker 2 profile
5. Agenda or session flow
6. Core themes or discussion pillars
7. Live format / Q&A / participation card
8. Registration, closing, or event poster

## Output Format

- **File format:** PowerPoint (`.pptx`)
- **Slide size:** 16:9 widescreen
- **All text:** Editable native PowerPoint elements
- **Location:** `outputs/<topic-slug>.pptx`

## Requirements

- [Claude Code](https://claude.ai/claude-code) CLI
- `pptx` base skill installed
- Node.js + `pptxgenjs` (`npm install -g pptxgenjs`)
- Python 3 + `markitdown[pptx]`, LibreOffice, Poppler (for QA)

## Trigger Phrases

This skill activates when you mention:
`azure host forum` · `forum deck` · `speaker event slides` · `industry sharing presentation` · `panel deck` · `workshop deck` · `creative industry event slides` · `host forum pptx`
