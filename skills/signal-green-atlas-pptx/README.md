# signal-green-atlas-pptx

A Claude Code skill for generating editable PowerPoint decks in the fixed **Signal Green Atlas** visual style — bold avant-garde editorial atlas aesthetic with fluorescent green backgrounds, black typography, black-and-white imagery, oversized uppercase headlines, and strict two-column information grids.

## What This Does

**signal-green-atlas-pptx** produces sharp, fluorescent, editorial `.pptx` files that feel like a bold European guidebook or experimental atlas system. Every text element — headlines, grid entries, metadata, captions — is a native editable PowerPoint object. Images are always black-and-white; image windows are always sharp rectangles.

### Key Features

- **Fixed Two-Color System** — Fluorescent green `#0CDA76` dominant background, black `#000000` for all typography, rules, and dividers
- **Black-and-White Imagery Only** — All image assets (uploaded or generated) must be high-contrast monochrome
- **AI Editorial Photography** — Optionally generates black-and-white high-contrast editorial images using `gpt-image-2`
- **Sharp Geometry** — No rounded corners, no soft shadows, no decorative cards — precise rectangular windows and grid alignment throughout
- **Strict Grid Discipline** — Two-column information grids with consistent row spacing, column alignment, and thin rules
- **Smart Intake** — Asks 3 focused questions (topic, slide count, image source), then infers all remaining details
- **Topic Translation** — Reframes any subject as a structured atlas — sections, stops, stages, milestones, reference points
- **Visual QA** — Inspects every slide for overlaps, grid integrity, image color, and density violations before delivery

## Installation

```bash
mkdir -p ~/.claude/skills/signal-green-atlas-pptx
cp SKILL.md ~/.claude/skills/signal-green-atlas-pptx/
```

Then use it by mentioning **Signal Green Atlas** or asking for a fluorescent-green editorial atlas deck in Claude Code.

## Usage

```
> "Make a Signal Green Atlas deck about our product roadmap"
> "Fluorescent green editorial presentation on climate data, 9 slides"
> "Atlas-style guidebook deck for our research findings"
```

The skill will:
1. Ask up to 3 focused questions (topic, slide count, image handling)
2. Optionally generate black-and-white editorial images with `gpt-image-2`
3. Build the PPTX using PptxGenJS via the `pptx` base skill
4. Run visual QA on every slide
5. Save to `outputs/<topic-slug>.pptx`

## Visual Style

| Element | Value |
|---------|-------|
| Background | Fluorescent green `#0CDA76` |
| Typography & rules | Black `#000000` |
| Images | Black-and-white only |
| Image windows | Sharp rectangles (no rounding) |
| Cover title | 72–110 pt bold uppercase grotesk |
| Slide headlines | 40–64 pt bold uppercase |
| Body text | 22–30 pt |
| Grid & metadata | 12–20 pt precise sans |

## Slide Structure (default 9 slides)

1. Cover — monochrome hero image + oversized uppercase title
2. Topic snapshot or atlas overview
3. Key sections or stops (index)
4. Focus slide A
5. Focus slide B
6. Two-column information grid
7. Sequence, route, or comparison grid
8. Image + metadata composition
9. Closing poster

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
`signal green` · `signal green atlas` · `fluorescent green deck` · `atlas pptx` · `black and green presentation` · `avant-garde atlas deck` · `guidebook style slides` · `editorial atlas presentation`
