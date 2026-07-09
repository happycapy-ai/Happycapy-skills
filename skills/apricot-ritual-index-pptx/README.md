# apricot-ritual-index-pptx

A Claude Code skill for generating editable PowerPoint decks in the fixed **Apricot Ritual Index** visual style — refined minimalist editorial poster aesthetic with warm apricot backgrounds, cocoa-brown typography, centered word stacks, thin horizontal rules, and sparse image placement.

## What This Does

**apricot-ritual-index-pptx** produces calm, premium, typographic `.pptx` files that feel like a refined product introduction combined with a brand-poster system. Every element — titles, dividers, index rows, captions, metadata — is a native editable PowerPoint object.

### Key Features

- **Fixed Visual Brand** — Warm apricot `#FDDEB6` background, cocoa-brown `#6C4832` typography and rules
- **Editorial Poster Layouts** — Centered word stacks, thin rules, sparse image placement, generous whitespace
- **AI Image Generation** — Optionally generates minimal premium still-life assets using `gpt-image-2`
- **Smart Intake** — Asks 3 focused questions (topic, slide count, image source), then infers all remaining details
- **Topic Translation** — Reframes any subject (products, research, strategy, creative work) as a ritual index, collection, or ordered sequence
- **Visual QA** — Inspects every slide for overlaps, collisions, and density violations before delivery

## Installation

```bash
mkdir -p ~/.claude/skills/apricot-ritual-index-pptx
cp SKILL.md ~/.claude/skills/apricot-ritual-index-pptx/
```

Then use it by mentioning **Apricot Ritual Index** or asking for a warm apricot minimalist deck in Claude Code.

## Usage

```
> "Make an Apricot Ritual Index deck about skincare ingredients"
> "Ritual index style presentation on our product launch, 9 slides"
> "Warm apricot minimalist slides for our brand strategy"
```

The skill will:
1. Ask up to 3 focused questions (topic, slide count, image handling)
2. Optionally generate still-life editorial images with `gpt-image-2`
3. Build the PPTX using PptxGenJS via the `pptx` base skill
4. Run visual QA on every slide
5. Save to `outputs/<topic-slug>.pptx`

## Visual Style

| Element | Value |
|---------|-------|
| Background | Warm apricot `#FDDEB6` |
| Typography & rules | Cocoa-brown `#6C4832` |
| Depth highlights | Subtle beige `#F5EAD8` |
| Cover title | 72–120 pt elegant serif |
| Slide headlines | 40–68 pt serif |
| Body text | 22–30 pt |
| Labels & metadata | 12–16 pt narrow sans |

## Slide Structure (default 9 slides)

1. Cover — strong poster image + hero serif title
2. Central promise or thesis
3. Overview or index
4. Key component / concept A
5. Key component / concept B
6. Focus detail or focal sequence
7. Process or ritual order
8. Summary or collection view
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
`apricot ritual` · `ritual index deck` · `apricot minimalist slides` · `product poster presentation` · `ritual index pptx` · `editorial poster deck` · `typographic poster presentation` · `warm apricot slides`
