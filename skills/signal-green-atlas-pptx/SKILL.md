---
name: signal-green-atlas-pptx
description: "Reusable fixed-style PPTX generation skill for the Signal Green Atlas visual brand — fluorescent green (#0CDA76) dominant background, black (#000000) typography and rules, black-and-white imagery only, bold avant-garde editorial atlas aesthetic, oversized uppercase grotesk headlines, strict two-column information grids, sharp rectangular photo windows, black circular bullets, deliberate asymmetry, widescreen 16:9 editable .pptx output. Use this skill whenever the user mentions Signal Green Atlas, asks for a fluorescent-green editorial presentation, wants an avant-garde atlas or guidebook-style deck, requests a bold black-and-green presentation, or needs a deck using strict information grids and monochrome imagery. Also trigger for 'signal green', 'signal green atlas', 'fluorescent green deck', 'atlas pptx', 'black and green presentation', 'avant-garde atlas deck', 'guidebook style slides', or 'editorial atlas presentation'."
---

# Signal Green Atlas PPTX Skill

A reusable fixed-style PowerPoint generation skill. It builds on the `pptx` skill's technical capabilities while locking in the Signal Green Atlas visual identity: bold, avant-garde, editorial — a fluorescent-green guidebook system with strict typographic grids, sharp rectangular image windows, black-and-white photography, and deliberate asymmetric composition.

**Core principle — style fidelity over content volume.** The atlas visual language originates in European editorial guides and experimental cartography, but it is a design system, not a fixed travel subject. Translate any topic into this visual language without forcing it to become a travel itinerary. The deck must feel bold, sharp, fluorescent, and editorial — never a soft brochure, text-heavy report, or generic corporate presentation.

---

## Step 1: Gather Inputs (Ask First — Max 3 Questions)

Do **not** start generating immediately. Use the `AskUserQuestion` tool to present all questions in a **single** call. Only ask about what the user hasn't already provided.

**Question 1 — Topic** (skip if already provided):
- header: "Topic"
- question: "What is the presentation topic or title?"
- options: 2–3 relevant examples plus allow Other

**Question 2 — Slide count** (skip if already specified):
- header: "Slides"
- question: "How many slides should the deck include? (9 recommended)"
- options: `6 slides`, `9 slides (Recommended)`, `12 slides`, `15 slides`

**Question 3 — Visual assets**:
- header: "Images"
- question: "How should visual assets be provided?"
- options:
  - `Use uploaded images` — Insert images I provide
  - `Generate with gpt-image-2` — AI creates black-and-white editorial imagery
  - `Combine both` — Mix uploaded and AI-generated assets

Infer the audience, narrative structure, sections, labels, and supporting metadata from the user's topic. Do not ask additional questions unless essential information is missing and the presentation cannot be completed without it.

Once you have the three answers, proceed directly to generation.

---

## Step 2: Translate the Topic into Signal Green Atlas Language

Before writing any slide copy, decide how to translate the user's topic into the atlas frame. The visual system originated in route guides and cartographic atlases, but any subject can be reframed as a structured atlas — sections become stops, stages, coordinates, chapters, signals, milestones, sequences, or reference points.

| User provides | Signal Green Atlas treatment |
|---|---|
| Product or brand | Atlas of the product ecosystem — sections, versions, features as stops |
| Strategy or business topic | Strategic atlas — milestones, phases, decision coordinates |
| Research or educational topic | Reference atlas — chapters, findings as entries, index overview |
| Process or workflow | Sequential route — numbered stages, process stops, comparison grid |
| Event or conference | Event atlas — session index, schedule grid, speaker entries |
| Any other subject | Reframe as a bold structured guide — sections, reference points, or field entries |

Preserve the user's topic, terminology, facts, and intended meaning. Do not invent locations, routes, dates, statistics, people, companies, products, claims, or research results.

---

## Step 3: Generate Images (if requested)

Read the `generate-image` skill at `/home/node/.claude/skills/generate-image/SKILL.md` for the exact API call pattern. Use `openai/gpt-image-2` with `response_format: "b64_json"`.

### How many images to generate

- 9-slide deck → 4–5 images
- 12–15 slide deck → 5–6 images
- 6 slides → 3–4 images

### Cover image rule

The cover must include one large topic-relevant black-and-white hero image. Generate or use an uploaded image for this first.

### Signal Green Atlas image prompt formula

Generated images are black-and-white editorial assets — not slide screenshots and never images with embedded text.

```
Black-and-white high-contrast editorial photograph or illustration. [Scene descriptor: sharp architectural lines / industrial surface / structural geometry / stark landscape / editorial still-life / abstract urban form]. Slightly grainy film quality, strong geometric composition, clear primary subject, adequate negative space. [Optional: controlled motion blur]. No readable text, no logos, no brand marks, no watermarks, no recognizable real people, no presentation titles, no charts, no interface elements. Suitable for large rectangular hero window or full-slide monochrome plate.
```

For non-architectural topics, adapt the scene:
```
Black-and-white high-contrast editorial [image type: scientific instrument / object arrangement / abstract form relevant to topic]. Same film quality and no-text rules. Strong geometric structure, sharp edges, negative space.
```

Save each image to `/tmp/signal-green-img-N.png`.

---

## Step 4: Build the PPTX

Read the `pptx` skill at `/home/node/.claude/skills/pptx/SKILL.md` and its `pptxgenjs.md` reference for the full API. Build using PptxGenJS.

### Core style constants — do not deviate

```javascript
const GREEN  = "0CDA76";   // fluorescent green — dominant background, all fields
const BLACK  = "000000";   // primary typography, rules, dividers, bullets, metadata
const WHITE  = "FFFFFF";   // text on black fields or dark image backgrounds only
const SANS   = "Arial Black"; // oversized uppercase headlines, section IDs, cover title
const META   = "Arial";    // labels, metadata, grid content, captions, supporting text
```

If Arial Black is unavailable, substitute `Impact` or `Franklin Gothic Heavy`.

### Layout — LAYOUT_16x9 always (10" × 5.625")

Background is GREEN on every slide by default. Black fields may appear as panel blocks or full-cover sections. Images are always black-and-white and placed in sharp rectangular windows — no rounded corners, no soft frames.

### Typography sizing

| Role | Font | Size | Color |
|------|------|------|-------|
| Cover title | SANS uppercase | 72–110pt | BLACK |
| Slide headline | SANS uppercase | 40–64pt | BLACK |
| Section identifier / index label | SANS uppercase | 32–48pt | BLACK |
| Body / supporting statement | META | 22–30pt | BLACK |
| Grid entries / labels | META | 16–20pt | BLACK |
| Metadata / captions | META | 12–16pt | BLACK |

On black background panels or dark image areas, use WHITE for text.

---

## Signal Green Atlas Visual System Rules

### Rule 1: Style over content volume

The atlas system takes priority over including every detail. Compress, summarise, and choose the one most important idea for each slide. Generous empty green space is a design choice — not wasted space. A mostly-green slide with one oversized headline is correct Signal Green Atlas style.

### Rule 2: One idea per slide. Under 35 words.

Count visible words before finalizing each slide. Most slides must be under 35 words total. Grid content and tiny metadata may be excluded only when it remains compact and legible. No paragraphs, no dense bullets, no long itinerary-style copy.

**Wrong:** "This section provides a comprehensive overview of the four key stages of the product development lifecycle, including discovery, definition, delivery, and deployment phases as practiced by our team."

**Right:**
```
FOUR STAGES

01 DISCOVER
02 DEFINE
03 DELIVER
04 DEPLOY
```

### Rule 3: Varied layouts within the same system

The Signal Green Atlas uses multiple layout types. Plan the slide mix before writing code — do not default to a single repeating composition. The variety is what makes it feel like a real atlas system.

Layout vocabulary:
- **Cover**: Large black-and-white hero image (full right half or full bleed) + oversized SANS uppercase title left
- **Atlas overview / index**: Numbered list of sections, two-column grid, clean atlas-style index
- **Two-column info grid**: Left column label/index, right column content; thin black rules between rows
- **Full-slide image plate**: Black-and-white image near full bleed, minimal uppercase text overlay
- **Section identifier**: Large oversized section number or name, compact metadata block below
- **Image + metadata**: Left sharp rectangular image panel, right compact metadata cluster
- **Comparison / sequence grid**: Two-column structure comparing stages, options, or entries
- **Closing poster**: Green field, large centered uppercase statement, compact credit metadata

### Rule 4: Sharp geometry only

The Signal Green Atlas style is defined by sharp rectangular image windows, precise grid lines, and exact alignment. No rounded corners on image panels, no decorative cards, no soft shadows, no pill-shaped labels, no ornamental illustration. Corners are sharp. Geometry is precise.

### Rule 5: Safe layout zones — no collisions

Before placing elements, define these non-overlapping zones:

```
HEADLINE ZONE:       y: 0.5"–2.0", left-aligned, x: 0.5"
HERO-IMAGE ZONE:     defined rectangle — text must never overlap it
GRID ZONE:           defined block with row padding — rules never cross entries
SUPPORTING-TEXT ZONE: at least 0.35" below headline bottom
RULE/DIVIDER ZONE:   dedicated whitespace — never within 0.3" of any text
METADATA ZONE:       compact cluster, y: ~4.8"–5.3" or alongside image
FOOTER ZONE:         y: ~5.2"–5.5", minimal META only
```

Conflict resolution order: reduce copy → remove secondary info → shorten grid entries → reduce rows → increase spacing → remove rule → simplify layout → move to another slide.

### Rule 6: Two-column grid discipline

Use two-column grids for index, comparison, and sequence slides. Grid rules:
- Left column: labels, index numbers, section names (META bold, left-aligned)
- Right column: content entries (META, left-aligned)
- Column break at approx. x: 3.0"–3.5"
- Row height: ~0.4"–0.5"
- Thin BLACK rules (LINE, h:0, 0.75–1pt) between row groups — never crossing text
- Internal padding: 0.1"–0.15" above each text row
- Maximum 6–8 rows before splitting to another slide

---

## Layout Patterns

### Cover (hero image + oversized title)
```
Background: GREEN full slide
Hero image (black-and-white): right half, x:4.8, y:0, w:5.2, h:5.625
  — OR full bleed with BLACK overlay rect (transparency: 45%) for text legibility
Left field (x:0.4"–4.4"):
  SANS uppercase title, 72–100pt, BLACK, y: 1.0"–2.8"
  Thin BLACK rule (LINE), w: 3.5", below title + 0.4" gap
  META metadata, 13pt, BLACK, y: ~4.8"
```

### Atlas overview / index slide
```
Background: GREEN full slide
SANS uppercase headline, 44pt, BLACK, x:0.5", y:0.5"
Thin BLACK rule (LINE), full width minus margins, y: below headline + 0.3"
Two-column index:
  Left col (x:0.5"): index numbers, 18pt META bold, BLACK
  Right col (x:1.5"): section names, 18pt META, BLACK
  Row height: 0.45", 5–8 rows
Optional thin rules between groups
META metadata cluster, 13pt, BLACK, bottom-left y:~5.0"
```

### Two-column info grid
```
Background: GREEN full slide
SANS uppercase headline, 40–48pt, BLACK, top
Thin BLACK rule below headline + 0.3" gap
Grid block:
  Left col header, META bold 14pt uppercase, BLACK
  Right col header, META bold 14pt uppercase, BLACK
  Col break x: 3.2"
  Row content, META 16pt, BLACK
  Thin BLACK rules between row groups only
  Row padding: 0.12" above each line
```

### Full-slide monochrome image plate
```
Image: x:0, y:0, w:10, h:5.625 (near full bleed)
BLACK rect overlay where text sits (transparency: 0–25%, just enough for legibility)
SANS uppercase text, 44–64pt, WHITE, left or lower third only
META caption, 13pt, WHITE, bottom edge
Max 12 words total on this slide
```

### Section identifier
```
Background: GREEN full slide
Large SANS uppercase section number or name, 80–100pt, BLACK, centered or left, y:1.2"
Thin BLACK rule (LINE), w:6", below identifier + 0.5" gap
META supporting lines (2–3 max), 20pt, BLACK, below rule
META metadata, 13pt, BLACK, bottom
```

### Image + metadata composition
```
Background: GREEN full slide
Sharp rectangular image panel: x:0.4, y:0.5, w:4.2, h:4.4 (no rounded corners)
Right metadata cluster (x:5.2"–9.5"):
  SANS uppercase section label, 14pt, BLACK
  SANS uppercase headline, 36–44pt, BLACK
  Thin BLACK rule, w:3.5", below headline
  META entries (3–5 short lines), 18pt, BLACK
  META small metadata, 13pt, BLACK, bottom
```

### Closing poster
```
Background: GREEN full slide
  — OR: BLACK full slide with WHITE text
SANS uppercase statement (1–4 words stacked), 72–96pt, BLACK or WHITE, centered
Thin BLACK (or WHITE) rule, w:5", centered, below statement + 0.5" gap
META credit / topic label, 13pt, BLACK or WHITE, centered, near bottom
```

---

## PptxGenJS Critical Reminders

- Never `#` in hex: `"0CDA76"` not `"#0CDA76"`
- Never 8-char hex for opacity — use `opacity:` property separately
- Fresh option objects per shape — PptxGenJS mutates in place
- `margin: 0` on text boxes aligned to image edges or grid columns
- LINE shapes for rules: set `h: 0`, `line.width: 0.75–1pt`; verify `y` clears all text by 0.3"+
- Images: never use `rounding: true` — all image windows are sharp rectangles
- Grid column alignment: use exact `x` coordinates for both columns, consistent across all rows

---

## Step 5: Visual QA — Required Before Delivery

```bash
python -m markitdown output.pptx
python /home/node/.claude/skills/pptx/scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

Use a subagent for visual inspection with this prompt:

```
Visually inspect these Signal Green Atlas slides. Assume there are issues — find them.

Look for:
- Any text overlapping other text, image edges, rules, bullets, grid lines, metadata, or slide edges
- Titles or text that are clipped or cut off at boundaries
- Images that are not black-and-white, or are stretched or distorted
- Rounded image corners — all image windows must be sharp rectangles
- Rules or dividers crossing or touching text, grid entries, or labels
- Grid columns that are misaligned or have inconsistent row spacing
- Slides that all use the same composition — the deck must show varied layout types
- Fluorescent green (#0CDA76) not used as the dominant background
- Typography that is not bold uppercase for headlines
- Slides with more than 35 words total
- Any slide that looks like a soft brochure or generic corporate template
- Hardcoded sample routes, cities, dates, products, or placeholder content
- Generated images containing text, logos, or recognizable real people

For each slide, list issues. Report ALL issues, including minor ones.

Images:
1. /path/to/slide-01.jpg
2. /path/to/slide-02.jpg ...
```

### Signal Green Atlas QA checklist — check every slide

- [ ] Under 35 words on most slides (count them)
- [ ] No text overlaps text, images, rules, grid lines, bullets, or slide edges
- [ ] No rule crosses or touches text
- [ ] No title is clipped
- [ ] All images are black-and-white — no color
- [ ] All image windows are sharp rectangles — no rounded corners
- [ ] Fluorescent green (#0CDA76) is the dominant background throughout
- [ ] Black (#000000) is the primary text and line color
- [ ] Headlines use bold uppercase grotesk (Arial Black or equivalent)
- [ ] Two-column grids have consistent alignment and row spacing
- [ ] Layouts vary across slides — not one repeated composition
- [ ] No hardcoded sample content appears
- [ ] Generated images contain no text, logos, or recognizable real people
- [ ] Result feels bold, fluorescent, editorial, and avant-garde — not a soft brochure

If any slide fails: fix, re-render, verify. Deliver only after a clean pass.

---

## Step 6: Deliver

Save to `./outputs/[topic-slug].pptx`. Confirm: slide count, image approach, slide types used, QA passed.

Do **not** show internal labels — no skill instructions, no source filenames, no implementation notes, no QA checklist text — on any visible slide.
