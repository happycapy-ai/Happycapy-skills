# botanical-blur-system-pptx

A Claude Code skill for generating editable PowerPoint decks in the fixed **Botanical Blur System** visual style — premium organic editorial aesthetic with warm cream layouts, botanical motion-blur textures, a six-color palette, white hand-drawn leaf motifs, and a genuinely varied slide family.

## What This Does

**botanical-blur-system-pptx** produces organic, premium, editorial `.pptx` files that feel coherent through recurring colors, typography, and botanical textures while varying the layout composition across slides. Every text element is a native editable PowerPoint object; botanical blur textures are inserted as image assets.

### Key Features

- **Fixed Six-Color System** — Cream `#F7F4EA`, sky blue `#3D8FD9`, botanical green `#0E5A3D`, coral `#D9573F`, dark slate `#2B302F`, white linework
- **Varied Slide Family** — Cream editorial slides, full-bleed texture slides, curved bands, rounded panels, side blobs, color fields, and information grids — never one repeated background
- **AI Texture Generation** — Optionally generates painterly botanical motion-blur textures using `gpt-image-2`
- **Botanical Linework** — White hand-drawn leaf-outline motifs as decorative atmospheric elements
- **Smart Intake** — Asks 3 focused questions (topic, slide count, image source), then infers all remaining details
- **Topic Translation** — Adapts any subject (strategy, brand, research, storytelling) into the botanical slide language
- **Visual QA** — Inspects every slide for overlaps, text-over-texture readability, and layout variety before delivery

## Installation

```bash
mkdir -p ~/.claude/skills/botanical-blur-system-pptx
cp SKILL.md ~/.claude/skills/botanical-blur-system-pptx/
```

Then use it by mentioning **Botanical Blur System** or asking for an organic editorial deck in Claude Code.

## Usage

```
> "Make a Botanical Blur System deck about our brand strategy"
> "Botanical blur presentation on mindfulness, 12 slides, generate textures"
> "Organic editorial deck for our product workshop"
```

The skill will:
1. Ask up to 3 focused questions (topic, slide count, image handling)
2. Optionally generate botanical motion-blur texture assets with `gpt-image-2`
3. Build the PPTX using PptxGenJS via the `pptx` base skill
4. Run visual QA on every slide
5. Save to `outputs/<topic-slug>.pptx`

## Visual Style

| Element | Value |
|---------|-------|
| Cream editorial bg | `#F7F4EA` |
| Sky blue accent | `#3D8FD9` |
| Botanical green | `#0E5A3D` |
| Muted coral | `#D9573F` |
| Dark slate (text) | `#2B302F` |
| Linework | White |
| Headlines | Clean modern sans-serif |
| Editorial text | Refined serif |

## Slide Type Mix (default 12 slides)

| Type | Count |
|------|-------|
| Cream editorial | 3–4 |
| Full-bleed / color-field | 2–3 |
| Curved band (top or bottom) | 2–3 |
| Rounded panel / side blob | 2 |
| Grid / information map | 1 |

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
`botanical blur` · `botanical blur system` · `organic editorial deck` · `botanical pptx` · `cream botanical slides` · `blurred botanical presentation` · `botanical workshop deck` · `premium organic presentation`
