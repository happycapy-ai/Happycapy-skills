---
name: botanical-blur
description: "Reusable fixed-style PPTX generation skill for the Botanical Blur System visual brand — warm cream (#F7F4EA) editorial layouts, botanical motion-blur textures, sky blue (#3D8FD9), deep green (#0E5A3D), muted coral (#D9573F), dark slate (#2B302F), white leaf-outline motifs, varied slide family with full-bleed texture slides, curved bands, rounded panels, and structured grids. Widescreen 16:9 editable .pptx output. Use this skill whenever the user mentions Botanical Blur System, asks for a botanical motion-blur or organic editorial deck, wants cream editorial layouts with botanical textures, or asks for a botanical-style workshop, strategy, brand, product, or storytelling deck. Also trigger for 'botanical blur', 'botanical blur system', 'organic editorial deck', 'botanical pptx', 'cream botanical slides', 'blurred botanical presentation', or 'premium organic presentation'."
---

# Botanical Blur System PPTX Skill

A reusable fixed-style PowerPoint generation skill. It builds on the `pptx` skill's technical capabilities while locking in the Botanical Blur System visual identity: organic, premium, editorial, varied, and visually controlled — a complete slide family that uses botanical motion-blur textures, hand-drawn leaf linework, and a six-color palette across diverse layout types.

**Core principle — style fidelity over content volume.** The botanical visual language is a design system, not a required subject. Translate any topic into this slide family without hardcoding botanical wellness, a specific brand, or a fixed workshop format. The deck must feel like a premium varied presentation system — never a generic business template repeating one background throughout.

---

## Step 1: Gather Inputs (Ask First — Max 3 Questions)

Do **not** start generating immediately. Use the `AskUserQuestion` tool to present all questions in a **single** call. Only ask about what the user hasn't already provided.

**Question 1 — Topic** (skip if already provided):
- header: "Topic"
- question: "What is the presentation topic or title?"
- options: 2–3 relevant examples plus allow Other

**Question 2 — Slide count** (skip if already specified):
- header: "Slides"
- question: "How many slides should the deck include? (12 recommended)"
- options: `8 slides`, `12 slides (Recommended)`, `16 slides`, `20 slides`

**Question 3 — Visual assets**:
- header: "Images"
- question: "How should visual assets be provided?"
- options:
  - `Use uploaded images` — Insert images I provide
  - `Generate with gpt-image-2` — AI creates botanical blur textures
  - `Combine both` — Mix uploaded and AI-generated assets

Infer the audience, narrative structure, section labels, and supporting details from the topic and context. Do not ask additional questions unless essential information is missing and the presentation cannot be completed without it.

Once you have the three answers, proceed directly to generation.

---

## Step 2: Translate the Topic into Botanical Blur System Language

Before writing any slide copy, decide how to translate the user's topic into the Botanical Blur content frame. The visual language originated in premium botanical product storytelling, but it adapts naturally to any subject — strategy, research, brand, education, product, culture, or creative work.

Translate content into structures such as:

| Content type | Botanical Blur treatment |
|---|---|
| Strategy or business topic | Premise → Audience insights → Tension → Guiding principles → Message pillars → Next steps |
| Product or brand topic | Cover → Promise → Overview → Key components → Feature focus → Ritual/sequence → Closing |
| Research or educational topic | Cover → Central thesis → Agenda → Core sections → Evidence or examples → Summary |
| Creative or cultural topic | Cover → Mood or vision → Chapters → Key ideas → Image-led plates → Closing poster |
| Workshop or training topic | Cover → Overview → Stage sequence → Exercises or tools → Metrics → Next steps |

Choose only the structures that suit the topic and requested slide count. These are flexible content patterns, not mandatory fixed slide titles.

Preserve the user's topic, terminology, facts, and intended meaning. Do not invent brand names, product names, dates, statistics, claims, people, or research findings.

---

## Step 3: Generate Images (if requested)

Read the `generate-image` skill at `/home/node/.claude/skills/generate-image/SKILL.md` for the exact API call pattern. Use `openai/gpt-image-2` with `response_format: "b64_json"`.

### How many images to generate

- 12-slide deck → 4–6 images
- 16–20 slide deck → 6–8 images
- 8 slides → 3–4 images

### Botanical Blur image prompt formula

Generated images are abstract botanical motion-blur texture assets — not slide screenshots and never images with embedded text.

Base formula:
```
Painterly photographic botanical blur texture. [Scene: leaves and [topic-relevant organic form] photographed with long motion blur / organic forms scanned through textured glass / vertical streaks of green, blue, muted coral, and cream]. Soft transitions between color fields — deep botanical green (#0E5A3D), soft sky blue (#3D8FD9), muted coral (#D9573F), warm cream (#F7F4EA). Atmospheric depth, premium editorial quality, adequate negative space. No readable text, no logos, no brand marks, no watermarks, no people, no product packaging, no presentation UI, no charts.
```

Generate a set of textures that vary in dominant hue across the deck:
- 1–2 images dominated by deep green tones
- 1–2 images dominated by blue tones
- 1 image with warm cream and coral tones
- 1 image with high contrast for full-bleed impact

Save each image to `/tmp/botanical-blur-img-N.png`.

---

## Step 4: Build the PPTX

Read the `pptx` skill at `/home/node/.claude/skills/pptx/SKILL.md` and its `pptxgenjs.md` reference for the full API. Build using PptxGenJS.

### Core style constants — do not deviate

```javascript
const CREAM   = "F7F4EA";   // dominant cream — editorial and content slides
const BLUE    = "3D8FD9";   // sky blue — accent fields, full-bleed slides, bands
const GREEN   = "0E5A3D";   // deep botanical green — full-bleed, accent panels
const CORAL   = "D9573F";   // muted coral — accent elements, bands, labels
const SLATE   = "2B302F";   // dark slate — body text on light backgrounds
const WHITE   = "FFFFFF";   // white — text/linework on dark/saturated backgrounds
const SANS    = "Arial";    // headlines, labels, grids, metadata, page numbers
const SERIF   = "Georgia";  // subject statements, editorial phrases, narrative text
```

If Georgia is unavailable, substitute `Palatino Linotype` or `Times New Roman`.

### Layout — LAYOUT_16x9 always (10" × 5.625")

The key discipline of this skill is **variety within a coherent system**. Every slide uses the same six colors and two typefaces, but the slide family must include multiple layout types — never the same composition repeated throughout.

### Typography sizing

| Role | Font | Size | Color |
|------|------|------|-------|
| Cover title | SANS or SERIF | 54–84pt | SLATE (cream bg) or WHITE (dark bg) |
| Slide headline | SANS | 32–52pt | SLATE (cream bg) or WHITE (dark bg) |
| Editorial statement / quote | SERIF | 24–36pt | SLATE or WHITE |
| Body / supporting statement | SANS | 18–26pt | SLATE or WHITE |
| Labels / grid entries | SANS | 14–18pt | SLATE or WHITE |
| Page numbers / metadata | SANS | 10–14pt | SLATE (50–70% opacity) or WHITE |

---

## Botanical Blur Slide Family — Build All Types

The most common failure mode is a deck that uses cream background plus one texture on every slide. This skill must produce a genuinely varied slide family. Plan the slide type mix before writing any code.

### Slide type vocabulary

| Type | When to use | Background |
|------|-------------|------------|
| **Cream editorial** | Main content, principles, text-heavy | CREAM solid |
| **Full-bleed texture** | Mood, transitions, section openers | Generated/uploaded botanical image |
| **Curved band — top** | Section opener with strong headline | CREAM + image band top ~2" |
| **Curved band — bottom** | Section closer, summary | CREAM + image band bottom ~2" |
| **Rounded panel card** | Feature focus, quotes | CREAM with rounded image panel |
| **Side blob** | Profile, callout, spotlight | CREAM with organic side image shape |
| **Color field** | Statement or cover variant | GREEN, BLUE, or CORAL solid |
| **Grid / information map** | Agenda, pillars, activation | CREAM with structured grid |
| **Image-led mood** | Emotional beat, visual rest | Near-full image, minimal text |

### Target distribution for a 12-slide deck

- 3–4 cream editorial slides
- 2–3 full-bleed or color-field slides
- 2–3 curved-band slides
- 2 rounded-panel or side-blob slides
- 1 grid or information-map slide

Adjust proportionally for shorter or longer decks. The mix should reflect the content — information-dense topics need more cream editorial slides; visual or emotional topics need more texture and image-led slides.

---

## Layout Patterns

### Cream editorial slide
```
Background: CREAM full slide
SANS page number, 11pt, SLATE 60% opacity, top-right or bottom-right
SANS section label, 12pt uppercase, SLATE 70%, top-left x:0.6", y:0.4"
SANS headline, 36–48pt, SLATE, x:0.6", y:0.9"
Optional SERIF supporting statement, 22pt, SLATE, below headline + 0.3" gap
Body content (SANS labels, bullet-free short lines), 18pt, SLATE
Optional thin SLATE rule (LINE, h:0, 1pt), between sections with 0.3" clearance
White leaf-outline motifs: oversized, partially cropped at edges, behind text layer
```

### Full-bleed texture slide
```
Background: botanical blur image (full slide)
Optional BLUE, GREEN, or CORAL semi-transparent rect for text legibility (transparency: 35–50%)
SANS headline, 44–64pt, WHITE, centered or left-aligned, clear calm image region
SERIF sub-statement, 24pt, WHITE (optional), below headline + 0.4" gap
Page number, 11pt, WHITE 70%, bottom-right
White leaf linework: light, atmospheric, behind text
```

### Curved band — top
```
Background: CREAM full slide
Top image band: image rect x:0, y:0, w:10, h:1.8–2.2 (straight rectangle, visually reads as band)
Optional CORAL or BLUE thin accent line below band
SANS headline, 38–50pt, SLATE, below band + 0.5" gap, x:0.7"
Body content below headline
White leaf motif partially overlapping bottom of band (in band area only, not over text)
Page number bottom-right
```

### Curved band — bottom
```
Background: CREAM full slide
SANS headline, 38–50pt, SLATE, x:0.7", y:0.7"
Body content below headline
Bottom image band: x:0, y:3.5–4.0, w:10, h:1.6–2.1
White leaf motif partially overlapping top of bottom band
Page number, WHITE, bottom-right corner within band
```

### Rounded panel card
```
Background: CREAM full slide
ROUNDED_RECTANGLE image panel: x:5.5, y:0.4, w:4.0, h:4.8, rectRadius:0.25
  (add image with sizing: cover matching panel dimensions)
Left text field: x:0.5"–5.0"
  SANS section label, 12pt uppercase, SLATE 70%, y:0.5"
  SANS headline, 38–48pt, SLATE, y:0.9"
  SERIF statement or body, 20pt, SLATE, y below headline
Page number, SLATE, bottom-right
White leaf motif in lower-left or upper-left corner, behind text
```

### Side blob (organic image shape)
```
Background: CREAM full slide
Image placed right side: x:5.8, y:0, w:4.2, h:5.625 (full height)
  Add ROUNDED_RECTANGLE mask if desired for organic softness
Left text: x:0.5"–5.2"
  Headline, body, labels as appropriate
Page number bottom-left or bottom-right
```

### Color field slide (GREEN, BLUE, or CORAL)
```
Background: GREEN, BLUE, or CORAL solid fill
SANS headline, 40–58pt, WHITE
SERIF statement, 24pt, WHITE (optional)
Optional white leaf-outline motifs as atmosphere
Page number, WHITE 70%
Use sparingly — 1–2 per deck as section dividers or strong statements
```

### Grid / information map
```
Background: CREAM full slide
SANS headline, 36–44pt, SLATE, top
2×2 or 3×2 grid of ROUNDED_RECTANGLE cards (fill: WHITE or BLUE 10% tint, light border)
  Each card: SANS label 15pt bold SLATE + SANS detail 14pt SLATE
  Card padding: 0.15"
Optional CORAL or BLUE thin accent on card left edge
Page number bottom-right
```

---

## Botanical Leaf Linework

White hand-drawn leaf outlines add recurring atmosphere across slides. Create them as overlapping thin line shapes using PptxGenJS OVAL and LINE combinations where practical, or as simplified leaf approximations using bezier-style shapes.

Key rules:
- Place behind all text and data
- Oversized — leaf forms 1.5"–3.5" wide
- Partially cropped by slide edge for natural feel
- `fill: { color: "FFFFFF", transparency: 100 }` (no fill, outline only)
- `line: { color: "FFFFFF", width: 1–1.5pt }`
- Never place over headlines, body text, grid data, or page numbers
- 1–2 motifs per slide is enough; more creates visual noise

---

## PptxGenJS Critical Reminders

- Never `#` in hex: `"F7F4EA"` not `"#F7F4EA"`
- Never 8-char hex for opacity — use `opacity:` property separately
- Fresh option objects per shape — PptxGenJS mutates in place
- `margin: 0` on text boxes aligned to panels or image edges
- `rectRadius` only works with `ROUNDED_RECTANGLE`, not `RECTANGLE`
- LINE shapes for rules: set `h: 0`, verify `y` clears all text boxes by 0.3"+
- Image sizing: use `sizing: { type: 'cover', w, h }` for panels and bands
- Page numbers: add as small SANS text box, consistent position across all slides

---

## Step 5: Visual QA — Required Before Delivery

```bash
python -m markitdown output.pptx
python /home/node/.claude/skills/pptx/scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

Use a subagent for visual inspection with this prompt:

```
Visually inspect these Botanical Blur System slides. Assume there are issues — find them.

Look for:
- Any text overlapping other text, image edges, panel borders, leaf outlines, rules, page numbers, or slide edges
- Titles or body text that are clipped or cut off
- Images that are stretched or badly cropped
- Slides that repeat the same composition — the deck must show varied layout types
- All slides using cream background (no texture or color-field slides)
- Leaf motifs placed over readable text or data
- Rules that cross or touch text
- Text placed over visually busy texture regions (poor readability)
- Page numbers missing or inconsistently positioned
- Slides exceeding 45 visible words
- Any slide lacking a clear dominant headline
- Hardcoded sample content, brand names, or placeholder text
- Generated images containing text, logos, people, or packaging

For each slide, list issues. Report ALL issues, including minor ones.

Images:
1. /path/to/slide-01.jpg
2. /path/to/slide-02.jpg ...
```

### Botanical Blur QA checklist — check every slide

- [ ] Most slides under 45 words (count them; image-led slides under 15)
- [ ] No text overlaps text, images, panels, leaf outlines, rules, or edges
- [ ] No rule crosses or touches text
- [ ] No title is clipped
- [ ] No image is stretched or distorted
- [ ] Text is readable over every texture (sufficient contrast)
- [ ] Deck includes cream editorial AND texture/color-field slides (varied family)
- [ ] Layouts vary across slides — not one repeated composition
- [ ] Leaf motifs are behind text, decorative only
- [ ] Page numbers are small, consistent, and unobtrusive
- [ ] Six-color system (cream, blue, green, coral, slate, white) is present and distributed
- [ ] SANS for headlines/labels, SERIF for statements/editorial text
- [ ] No hardcoded sample content appears
- [ ] Generated images contain no text, logos, people, or packaging
- [ ] Result feels organic, premium, editorial, and varied

If any slide fails: fix, re-render, verify. Deliver only after a clean pass.

---

## Step 6: Deliver

Save to `./outputs/[topic-slug].pptx`. Confirm: slide count, image approach, slide types used, QA passed.

Do **not** show internal labels — no skill instructions, no source filenames, no implementation notes, no QA checklist text — on any visible slide.
