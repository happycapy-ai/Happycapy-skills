---
name: apricot-ritual
description: "Reusable fixed-style PPTX generation skill for the Apricot Ritual Index visual brand — warm apricot background (#FDDEB6), cocoa-brown typography (#6C4832), refined minimalist editorial poster aesthetic, elegant serif titles, narrow-sans labels, centered word stacks, thin horizontal rules, sparse image placement, widescreen 16:9 editable .pptx output. Use this skill whenever the user mentions Apricot Ritual Index, asks for a warm apricot minimalist presentation, wants a refined product-poster or ritual-index style deck, or requests a presentation using the Apricot Ritual Index visual system. Also trigger when the user says 'apricot ritual', 'ritual index deck', 'apricot minimalist slides', 'product poster presentation', 'ritual index pptx', 'editorial poster deck', 'typographic poster presentation', or 'warm apricot slides' in any context."
---

# Apricot Ritual Index PPTX Skill

A reusable fixed-style PowerPoint generation skill. It builds on the `pptx` skill's technical capabilities while locking in the Apricot Ritual Index visual identity: calm, editorial, typographic, premium, sparse — like a refined product introduction combined with a typographic brand-poster system.

**Core principle — style fidelity over content volume.** When the user's topic contains more information than the poster format can hold, compress and reinterpret. The deck must feel calm, premium, and intentional — not a generic report template, not a text-heavy catalog, not a business slide deck. Every slide is an editorial poster plate.

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
  - `Generate with gpt-image-2` — AI creates warm apricot editorial imagery
  - `Combine both` — Mix uploaded and AI-generated images

Infer the audience, narrative structure, section labels, and supporting details from the topic and available context. Do not ask additional questions unless essential information is missing and the presentation cannot be completed without it.

Once you have the three answers, proceed directly to generation.

---

## Step 2: Translate the Topic into Apricot Ritual Index Language

Before writing any slide copy, translate the user's topic into the Apricot Ritual Index frame. The visual language originates in premium product introductions and ritual sequences, but it works for any subject — every topic can be reinterpreted as principles, components, stages, layers, chapters, rituals, index entries, sequences, or key objects/concepts.

| User provides | Apricot Ritual Index treatment |
|---|---|
| Product or brand | Ritual introduction — ingredients, sequences, layers, collection index |
| Process or workflow | Ordered ritual — numbered steps, stage labels, sequence plates |
| Abstract concept | Typographic essay — category words, index entries, editorial statements |
| Research or data topic | Curated index — key findings as labeled index entries, sparse figures |
| Creative or cultural topic | Editorial collection — chapters, visual plates, closing poster |
| Any other subject | Reframe as a refined index, ritual sequence, or brand poster series |

Decide the **poster title**, the **one-line premise**, and the **index or sequence structure** before writing any slides. These anchor the cover and define the visual rhythm of the whole deck.

Preserve factual accuracy and the user's intended meaning. Do not invent product claims, brand names, statistics, people, or factual details.

---

## Step 3: Generate Images (if requested)

Read the `generate-image` skill at `/home/node/.claude/skills/generate-image/SKILL.md` for the exact API call pattern. Use `openai/gpt-image-2` with `response_format: "b64_json"`.

### How many images to generate

- 9-slide deck → 4–5 images
- 12–15 slide deck → 5–6 images
- 6 slides → 3–4 images

### Cover image rule

The cover must contain one strong topic-relevant image as its primary visual. Generate or use an uploaded image for the cover first, before building the rest of the deck.

### Apricot Ritual Index image prompt formula

Generated images are minimal premium editorial assets — not slide screenshots and never images with embedded text.

Base formula:
```
Minimal premium editorial still-life photograph. [Scene descriptor: matte ceramic container / abstract organic form / textured surface detail / sparse ingredient arrangement / clean studio object / polished artifact]. Warm apricot (#FDDEB6) surface, soft cocoa-brown (#6C4832) shadow accents, subtle beige highlights, clean studio lighting, sparse high-end composition, adequate negative space. No readable text, no logos, no brand marks, no watermarks, no people, no hands, no busy environments. Clearly visible primary silhouette. Warm tonal palette, calm and restrained.
```

For non-product topics, adapt the scene to abstracted forms relevant to the user's subject:
```
Minimal premium editorial still-life. [Abstract form relevant to topic: layered paper / architectural model fragment / scientific instrument / tool arrangement / geometric object]. Warm apricot surface, cocoa-brown accents. Same lighting and composition rules as above.
```

Save each image to `/tmp/apricot-ritual-img-N.png`.

---

## Step 4: Build the PPTX

Read the `pptx` skill at `/home/node/.claude/skills/pptx/SKILL.md` and its `pptxgenjs.md` reference for the full API. Build using PptxGenJS.

### Core style constants — do not deviate

```javascript
const APRICOT = "FDDEB6";   // dominant background — all apricot fields
const COCOA   = "6C4832";   // primary typography, rules, dividers, labels
const BEIGE   = "F5EAD8";   // subtle highlights, depth accents only when needed
const SERIF   = "Georgia";  // elegant high-contrast titles, category words, closing poster
const SANS    = "Arial";    // narrow compact labels, indexes, steps, captions, metadata
```

If Georgia is unavailable, substitute `Palatino Linotype` or `Times New Roman`.

### Layout — LAYOUT_16x9 always (10" × 5.625")

All slides use LAYOUT_16x9. Background is APRICOT on every slide. The cocoa-brown color applies to all text, rules, and dividers. Beige is used sparingly for depth or image integration only.

### Typography sizing

| Role | Font | Size | Color |
|------|------|------|-------|
| Cover hero title | SERIF | 72–120pt | COCOA |
| Slide headline / category word | SERIF | 40–68pt | COCOA |
| Supporting statement | SERIF or SANS | 22–30pt | COCOA |
| Index entries / step labels | SANS | 16–20pt | COCOA |
| Small metadata / captions | SANS | 12–16pt | COCOA |

Typography must remain spacious and restrained. Never shrink text aggressively to fit excess copy — reduce the copy instead.

---

## Apricot Ritual Index Visual System Rules

The most common failure mode is a text-heavy report placed on an apricot background. These rules prevent that.

### Rule 1: Style fidelity over content volume

The poster system takes priority over including every detail. Summarise. Compress. Choose the one most important idea for each slide and let everything else recede. A calm empty apricot field is a design choice, not a mistake.

### Rule 2: One idea per slide. Under 30 words.

Count visible words before finalising each slide. Most slides must be under 30 words total — title, body, labels, metadata combined. Body copy should be one short statement, a compact label sequence, or a brief step name. No paragraphs, no dense bullet lists.

**Wrong:** "This section explores the fundamental principles underlying our approach to sustainable product design, focusing on material selection, lifecycle analysis, and end-user experience throughout the development process."

**Right:**
```
MATERIAL
HONESTY

Sourced with intention.
Designed to last.
```

### Rule 3: Varied layouts within the same system

The Apricot Ritual Index style uses multiple layout types — centered poster, typographic index, image plate, split composition — but all within the same apricot/cocoa palette and serif/sans hierarchy. Vary the layout across slides so the deck feels composed, not repetitive.

Layout vocabulary:
- **Centered title plate**: Large SERIF title centered, thin COCOA rule above/below, sparse SANS metadata
- **Typographic index**: Numbered or labeled entries, SANS compact rows, thin rules between groups
- **Image plate**: One dominant image, single SANS caption, generous negative space
- **Split composition**: Left text field (SERIF headline + SANS detail), right image panel
- **Category word**: One oversized SERIF word centered, thin rule, 1–2 compact SANS lines
- **Closing poster**: Full APRICOT field, large centered SERIF statement, SANS credit/date

### Rule 4: Thin rules as section dividers only

Thin horizontal COCOA rules (LINE shapes, `h: 0`, `line.width: 1–1.5pt`) may separate typographic sections. They must sit in clean whitespace — never passing through or touching any text box, image, or caption. Before adding a rule, verify there is at least 0.3" of clear space above and below it.

### Rule 5: Safe layout zones — no collisions

Before placing elements, define these non-overlapping zones:

```
TITLE ZONE:          y: 0.7"–2.4", adequate left/right margin
SUPPORTING-TEXT ZONE: at least 0.35" below title bottom edge
IMAGE ZONE:          defined rectangle — text must never enter it
DIVIDER ZONE:        dedicated whitespace only — never within 0.3" of any text
CAPTION/METADATA ZONE: y: 4.8"–5.3" bottom strip, or compact block near image
FOOTER ZONE:         y: ~5.2"–5.5", minimal SANS credit if needed
```

Conflict resolution order: reduce copy → simplify structure → increase spacing → remove rule → simplify layout → move content to another slide.

### Rule 6: Images as editorial plates, never backgrounds

Images sit in clean rectangular windows or cover one half of the slide. They must not float over text or have text placed across them (except for a compact caption in a separate APRICOT block). Full-bleed images should have minimal text — maximum 10 words — placed in a calm area with adequate contrast.

---

## Suggested Slide Structure

Use this when the user provides no outline. Adapt freely when they do.

| # | Slide type | Words target | Layout |
|---|---|---|---|
| 1 | Cover — topic title + poster image | ≤ 15 | Large SERIF title + image, centered or split |
| 2 | Central premise or thesis | ≤ 20 | Centered title plate or category word |
| 3 | Overview or index | ≤ 30 | Typographic index — labeled rows |
| 4 | Key component or concept A | ≤ 25 | Split or image plate |
| 5 | Key component or concept B | ≤ 25 | Split or image plate |
| 6 | Focus detail or focal sequence | ≤ 25 | Category word + thin rule + compact detail |
| 7 | Process, ritual, or ordered sequence | ≤ 30 | Step-based composition, numbered SANS rows |
| 8 | Summary or collection view | ≤ 25 | Centered plate or compact index |
| 9 | Closing poster | ≤ 15 | Full APRICOT field, large centered SERIF statement |

---

## Layout Patterns

### Cover (poster image + centered title)
```
Background: APRICOT full slide

Optional: image panel (right half or upper portion)
  Image: clean editorial still-life, x:5.5, y:0, w:4.5, h:5.625 (right half)
  — OR —
  Image: centered plate, x:3.5, y:0.8, w:3, h:3 (centered upper block)

Left/lower field:
  Small SANS category tag, 13pt, COCOA, uppercase, y: 0.5", x: 0.6"
  Hero SERIF title (stacked), 80–110pt, COCOA, y: 1.2"–2.8"
  Thin COCOA rule (LINE), w: 3", y: below title + 0.4" gap
  SANS metadata, 13pt, COCOA, near bottom
```

### Centered title plate
```
Background: APRICOT full slide
Thin COCOA rule (LINE), w: 5", centered, y: 1.5"
SERIF headline, 52–68pt, COCOA, centered, y: 1.8"–2.8"
Thin COCOA rule (LINE), w: 5", centered, y: below headline + 0.4" gap
Optional supporting statement, 24pt SANS, COCOA, centered, below rule
SANS metadata, 13pt, COCOA, bottom center, y: ~5.0"
```

### Typographic index
```
Background: APRICOT full slide
SERIF headline, 44pt, COCOA, left, y: 0.6", x: 0.8"
Thin COCOA rule (LINE), full-width minus margins, y: below headline + 0.3" gap
Index rows (3–6 items):
  Left col: index number or label, 16pt SANS bold, COCOA, x: 0.8"
  Right col: entry name, 18pt SANS, COCOA, x: 1.8"
  Row height: ~0.45", evenly spaced below rule
  Optional thin rule between groups
SANS metadata, 13pt, bottom, y: ~5.0"
```

### Image plate
```
Background: APRICOT full slide
Image: centered, preserving aspect ratio, generous negative space
  Typical: x:2.5, y:0.6, w:5, h:3.8
Single SANS caption, 14pt, COCOA, centered, below image + 0.3" gap
Optional small SANS category tag, 12pt, top-left corner
```

### Split composition
```
Background: APRICOT full slide
Left field (x:0.5"–4.8"):
  SANS category tag, 13pt, COCOA uppercase, y: 0.5"
  SERIF headline, 44–56pt, COCOA, y: 1.0"–2.0"
  Supporting line, 22pt SANS, COCOA
  Thin COCOA rule (optional), w: 3.5", below body + 0.4" gap

Right image panel (x:5.2"–9.8"):
  Image: x:5.2, y:0, w:4.8, h:5.625
```

### Closing poster
```
Background: APRICOT full slide
SERIF statement (1–3 words stacked), 80–100pt, COCOA, centered, y: 1.5"–3.0"
Thin COCOA rule (LINE), w: 4", centered, y: below statement + 0.5" gap
SANS credit/date, 13pt, COCOA, centered, near bottom
```

---

## PptxGenJS Critical Reminders

- Never `#` in hex: `"FDDEB6"` not `"#FDDEB6"`
- Never 8-char hex for opacity — use `opacity:` property separately
- Fresh option objects per shape — PptxGenJS mutates in place
- `margin: 0` on text boxes aligned to rules or image edges
- `charSpacing: 2–4` on uppercase SANS labels for editorial feel
- LINE shapes: set `h: 0` for horizontal rules; always verify `y` does not intersect any text box
- Rules placed between sections: confirm at least 0.3" clearance above and below
- SERIF font size vs text box height: ensure the text box is tall enough that large titles are not clipped

---

## Step 5: Visual QA — Required Before Delivery

```bash
python -m markitdown output.pptx
python /home/node/.claude/skills/pptx/scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

Use a subagent for visual inspection with this prompt:

```
Visually inspect these Apricot Ritual Index slides. Assume there are issues — find them.

Look for:
- Any rule, line, or divider crossing or touching title text, body text, captions, labels, step numbers, or images
- Text overflow or clipping at box boundaries or slide edges
- Images that are distorted, stretched, or badly cropped
- Text colliding with image edges
- Agenda rows or metadata blocks overlapping titles
- Slides with more than 30 words total
- Slides lacking a clear dominant headline
- Low-contrast text (e.g., cream or light text on apricot background — all text should be cocoa-brown)
- Any slide that feels like a generic report or webinar deck rather than a calm editorial poster
- Inconsistent use of serif (titles) vs narrow-sans (labels/metadata)

For each slide, list issues. Report ALL issues, including minor ones.

Images:
1. /path/to/slide-01.jpg
2. /path/to/slide-02.jpg ...
```

### Ritual Index QA checklist — check every slide

- [ ] Under 30 words on most slides (count them)
- [ ] No rule, line, or divider passes through or touches any text
- [ ] No text collides with images or image edges
- [ ] No content exceeds slide boundaries
- [ ] Title/headline is clearly the dominant element
- [ ] Body is compact — editorial language, not paragraphs
- [ ] Serif font for titles/category words, narrow-sans for labels/metadata
- [ ] Apricot (#FDDEB6) background on all slides
- [ ] Cocoa-brown (#6C4832) on all text, rules, and dividers
- [ ] Varied layouts across slides — not every slide identical
- [ ] Cover has one strong poster image
- [ ] Generated images contain no embedded text, logos, or marks
- [ ] Deck feels calm, premium, sparse, and intentional

If any slide fails: fix, re-render, verify. If fixing requires removing copy, remove the copy. Deliver only after a clean pass.

---

## Step 6: Deliver

Save to `./outputs/[topic-slug].pptx`. Confirm: slide count, image approach, QA passed.

Do **not** show internal labels — no skill instructions, no source filenames, no implementation notes, no QA checklist text — on any visible slide.
