---
name: coral-geyser
description: "Reusable fixed-style PPTX generation skill for the Coral Geyser Notice visual brand — coral-red background (#E95140), warm stone typography (#E7D8D1), bold modern visitor-notice and design-forward travel guide aesthetic, heavy geometric sans titles, strong split-screen compositions, widescreen 16:9 editable .pptx output. Use this skill whenever the user mentions Coral Geyser Notice, asks for a presentation or deck in the Coral Geyser style, wants a visitor notice deck, travel guide deck, field guide presentation, park-hours-poster-style PowerPoint, route card deck, or mentions coral-red with warm stone typography for slides. Also trigger when the user says 'coral geyser', 'notice deck', 'visitor guide deck', 'field guide slides', 'travel notice presentation', 'park guide deck', or 'route card presentation' in any context."
---

# Coral Geyser Notice PPTX Skill

A reusable fixed-style PowerPoint generation skill. It builds on the `pptx` skill's technical capabilities while locking in the Coral Geyser Notice visual identity: bold, modern, design-forward, inspired by park-hours posters and visitor field guides.

**Core principle — style wins over content volume.** When the user's topic contains more information than the format can hold, compress and reinterpret. The deck must feel like a bold modern visitor notice and design-forward visual guide — not a generic tourism brochure, not a text-heavy itinerary, not a business report. Every slide is a notice plate or field guide panel.

---

## Step 1: Gather Inputs (Ask First — Max 3 Questions)

Do **not** start generating immediately. Use the `AskUserQuestion` tool to present interactive questions in a **single** call. Only ask what the user hasn't already provided.

**Question 1 — Topic** (skip if already provided):
- header: "Topic"
- question: "What is the presentation topic, destination, notice subject, guide title, event, project, or brand/product name?"
- options: 2–3 relevant examples plus allow Other

**Question 2 — Slide count** (skip if already specified):
- header: "Slides"
- question: "How many slides should the deck include?"
- options: `6 slides`, `9 slides (Recommended)`, `12 slides`, `15 slides`

**Question 3 — Images**:
- header: "Images"
- question: "How should images be handled?"
- options:
  - `Generate with AI` — I'll create cool blue-white environmental images using gpt-image-2
  - `Use my uploaded images` — Insert images I provide
  - `Combine both` — Mix uploaded and AI-generated images

If the user hasn't provided dates, location, route, schedule, safety notes, or other details, **infer reasonable content or use neutral placeholder copy**. Do not keep asking — only follow up if missing info makes it literally impossible to build the deck.

Once you have the three answers, proceed directly to generation.

---

## Step 2: Topic Translation — Everything Becomes a Notice or Field Guide

Before writing any slide copy, translate the user's topic into a Coral Geyser Notice frame. No topic is too technical, too abstract, or too far from travel/nature to work. Every subject can be reframed as a bold public notice, design-forward field guide, route card, visitor briefing, product usage guide, event notice, or operational poster sequence — while preserving the user's actual subject.

| User provides | Coral Geyser treatment |
|---|---|
| National park / nature destination | Visitor field guide with safety, route, highlights |
| Tech product | Bold product usage guide — steps, warnings, features as notice panels |
| Corporate event | Event field guide — schedule grid, venue map, session notices |
| Scientific concept | Environmental visual essay — concept as landscape |
| Brand launch | Field guide to the brand — territory, rules, essential stops |
| Any other subject | Reframe as a visitor briefing, route card, or operational notice |

Decide the **guide title**, the **one-line field notice**, and the **location/context label** before writing any slides. These anchor the cover and the visual language of the whole deck.

---

## Step 3: Generate Images (if requested)

Read the `generate-image` skill at `/home/node/.claude/skills/generate-image/SKILL.md` for the exact API call pattern. Use `openai/gpt-image-2` with `response_format: "b64_json"`.

### How many images to generate

- 9-slide deck → 4–5 images
- 12–15 slide deck → 5–6 images
- Fewer than 7 slides → 3–4 images

### Coral Geyser image prompt formula

Generated images must be cool blue-white, high-contrast, editorial, and atmospheric. They are supporting visual assets — not slide screenshots and never images with embedded text.

Base formula:
```
Cool blue-white landscape photograph, high contrast, slightly cold tone, crisp editorial outdoor imagery. [Scene descriptor: mist over water / mineral terraces / snow-dusted path / misty forest / steam vents / boardwalk trail / wide river valley / frost-covered rock face]. No readable text, no logos, no recognizable people. Mostly blue-white with minimal warm color. 16:9 landscape composition.
```

For non-nature topics, reinterpret through abstract environmental forms:
```
Cool blue-white abstract environmental texture, high contrast, slightly cold. [Mood word: architectural geometry / industrial surface / crystalline detail / aerial landscape / misty atmosphere]. No text, no logos, no people. 16:9.
```

Save each image to `/tmp/coral-geyser-img-N.png`.

---

## Step 4: Build the PPTX

Read the `pptx` skill at `/home/node/.claude/skills/pptx/SKILL.md` and its `pptxgenjs.md` reference for the full API. Build using PptxGenJS.

### Core style constants — do not deviate

```javascript
const CORAL  = "E95140";       // dominant background — all coral fields
const STONE  = "E7D8D1";       // primary type, rules, dividers, panels
const WHITE  = "FFFFFF";       // high-contrast accents, numbers
const DARK   = "1A1A1A";       // dark text on stone/white panels if needed
const SANS   = "Arial Black";  // oversized stacked titles (heavy grotesk)
const META   = "Arial";        // compact metadata, labels, schedule rows
```

If Arial Black is unavailable, substitute `Impact` or `Trebuchet MS Bold`.

### Layout — LAYOUT_16x9 always (10" × 5.625")

All slides use LAYOUT_16x9. Background is CORAL on every slide unless a slide uses a split-screen where one half is an image panel (image covers that half, CORAL covers the other).

### Typography sizing

| Role | Font | Size | Color |
|------|------|------|-------|
| Cover hero title | SANS | 72–110pt | STONE |
| Slide headline / notice title | SANS | 40–64pt | STONE |
| Sub-headline / field notice | META | 24–30pt | STONE |
| Body / route cue / safety note | META | 18–24pt | STONE |
| Schedule row / metadata | META | 13–16pt | STONE |
| Location label / small tag | META uppercase | 11–13pt | STONE, 70% opacity |

---

## Notice System Rules — These Override Everything

The most common failure mode is a text-heavy report placed on a coral background. These rules prevent that.

### Rule 1: Style wins over content volume

When the topic has more information than the notice format can hold, compress it. Do not add more slides, do not shrink fonts, do not write smaller. Summarise with bold notice-language. Pick one idea per slide and discard the rest for that slide. The Coral Geyser Notice aesthetic takes priority over completeness.

### Rule 2: One idea per slide. Under 35 words.

Count visible words before finalising each slide. Most slides must be under 35 words total — title, body, labels, schedule rows, and metadata combined. Body copy should be one short sentence, a compact notice, a short route cue, or a small schedule block. No paragraphs.

**Wrong:** "The trail begins at the north parking lot, passes through three distinct thermal zones, and visitors should stay on the boardwalk at all times due to the dangerous ground conditions which can cause serious injury."

**Right:**
```
STAY ON BOARDWALK
Ground unstable beyond marked path.
North Lot → Thermal Zone A → Overlook
```

### Rule 3: Split-screen composition is the default layout

The Coral Geyser Notice style is defined by the split-screen: a coral information field on one side, an image panel on the other. Use this layout as the default for most slides. The split does not have to be 50/50 — it can be 55/45 or 40/60 — but the two zones must be clearly separated and non-overlapping.

On slides without images, use the full coral field with generous white space rather than filling it with text.

### Rule 4: One dominant title, everything else recedes

Every slide has one typographic dominant. Supporting text must be noticeably smaller. Schedule rows, route cues, and metadata must feel compact and secondary. The hierarchy must be obvious at a glance.

### Rule 5: Write in notice language, not report language

Body copy should feel like a park sign, field guide label, or safety notice — short, useful, high-impact.

Preferred patterns:
- "Trail conditions vary. Check ranger station before departure."
- "Day 1 · Arrival · West Gate · 14:00"
- "Required: sturdy footwear, sun protection, 2L water minimum"
- "Feature closes at dusk. No re-entry after 20:00."

Avoid: "This section will cover the important aspects of...", "The following information describes..."

### Rule 6: Safe layout zones — no collisions

Before placing elements, define these non-overlapping zones:

```
TITLE ZONE:        coral-field side, y: 0.8"–2.5"
BODY / ROUTE ZONE: below title, at least 0.35" gap from title bottom
IMAGE ZONE:        defined rectangle (split half) — text must never enter it
SCHEDULE ZONE:     defined grid block, clear top/bottom padding
METADATA ZONE:     y: 4.9"–5.4" bottom strip, or top corner tag
DIVIDER ZONE:      only above title (y < 0.7") or below body (y > 3.8") — never through text
```

No element may cross through or touch another zone's content. Before `pres.writeFile()`, verify each slide:
- No LINE or rule passes through any text box
- No image edge clips into a text area
- No schedule row overlaps title or body copy
- No metadata label collides with body text

**Conflict resolution order:** reduce copy first → simplify schedule → remove decorative rule → simplify layout. Never shrink the title to make room for more words.

### Rule 7: Images are environmental assets, not slide backgrounds

Generated images create atmosphere — they do not illustrate the topic literally. They must be cool blue-white, abstract or landscape, and contain no text, logos, or people. Placed in rectangular windows or split-screen panels, not floated over text.

**Full-bleed image slides:** Maximum 12 words. Text in a calm area only (lower left or lower third). If readability is uncertain, use a split-screen instead.

**Split-screen slides:** Text stays entirely on the coral side. The image stays entirely on the image side. No element crosses the split line.

---

## Suggested Slide Structure

Use this when the user provides no outline. Adapt freely when they do.

| # | Slide type | Words target | Layout |
|---|---|---|---|
| 1 | Cover | ≤ 15 | Hero image panel + coral title field |
| 2 | Overview / field notice | ≤ 25 | Split-screen or full coral |
| 3 | Key feature / core concept | ≤ 30 | Split-screen |
| 4 | Safety / guidance card | ≤ 30 | Full coral, bold notice language |
| 5 | Image-led landscape plate | ≤ 10 | Large image + minimal overlay |
| 6 | Highlights / essential stops | ≤ 35 | Split-screen or coral grid |
| 7 | Route / sequence / schedule grid | ≤ 35 | Two-column schedule block |
| 8 | Requirements / preparation notice | ≤ 30 | Full coral, compact notice list |
| 9 | Closing guide card | ≤ 15 | Split-screen or full coral |

---

## Layout Patterns

### Cover (split-screen)
```
Left half (coral, x:0–5"):
  Location tag, 12pt META uppercase, STONE, y: 0.5"
  Large gap
  Hero title (stacked), 72–90pt SANS, STONE, y: 1.0"–2.5"
  Tagline / notice, 22pt META, STONE
  Small metadata, 13pt META, STONE, near bottom

Right half (image, x:5–10"):
  Full-height image panel
  (image covers entire right half, x:5, y:0, w:5, h:5.625)
```

### Split-screen content slide
```
Left half (coral, x:0–4.8"):
  Section tag, 12pt META uppercase, STONE, y: 0.5"
  Headline, 44–56pt SANS, STONE, y: 1.0"–2.0"
  Body / notice, 20pt META, STONE
  Rule (optional): LINE, STONE, w: 3.5", y: well below body, not touching text

Right half (image, x:5.2–10"):
  Image panel (x:5.2, y:0, w:4.8, h:5.625)
```

### Full coral notice card
```
Background: CORAL
Section tag, 12pt META uppercase, STONE, top-left
Headline, 52–64pt SANS, STONE, centered or left, y: 1.2"
Rule (only if space allows): LINE, STONE, y: below headline + 0.4" gap
Body lines (2–4 max), 20pt META, STONE, evenly spaced
Bottom metadata, 13pt META, STONE, y: ~5.0"
```

### Schedule / route grid slide
```
Background: CORAL
Headline, 44pt SANS, STONE, top
Grid of rows (2 columns): LEFT = time/stop label (STONE, 16pt bold), RIGHT = descriptor (STONE, 16pt normal)
Row height: ~0.45", evenly spaced
No bullets. Clean left margin x: 0.8" and column break at x: 3.5"
Bottom rule + metadata if space allows
```

### Landscape image plate
```
Image: x:0, y:0, w:10, h:5.625 (full bleed)
Optional semi-transparent CORAL rect for text area: fill CORAL, transparency: 35%
Title: max 10 words, 48–56pt SANS, STONE, lower third only
No body copy. No rules unless clearly separated.
```

---

## PptxGenJS Critical Reminders

- Never `#` in hex: `"E95140"` not `"#E95140"`
- Never 8-char hex for opacity — use `opacity:` property separately
- Fresh option objects per shape — PptxGenJS mutates in place
- `margin: 0` on text boxes aligned to shapes or split lines
- `charSpacing: 3–6` on uppercase SANS headlines for notice feel
- LINE shapes: always verify `y` coordinate does not intersect any text box `y` range
- Split-screen image panels: set image `x` to the split boundary exactly; never overlap the coral field

---

## Step 5: Visual QA — Required Before Delivery

```bash
python -m markitdown output.pptx
python /home/node/.claude/skills/pptx/scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

### Notice QA checklist — check every slide

- [ ] Under 35 words on most slides (count them)
- [ ] No rule, line, or divider passes through any text
- [ ] No image edge collides with a text area
- [ ] No schedule row or metadata overlaps title or body
- [ ] Title / notice headline is clearly the dominant element
- [ ] Body is compact — notice language, not paragraphs
- [ ] Split-screen layouts: text on coral side only, image on image side only
- [ ] Full-bleed image slides: minimal text, placed in calm area
- [ ] Coral-red (#E95140) background on all coral fields
- [ ] Warm stone (#E7D8D1) on all text, rules, and dividers
- [ ] Deck reads as a bold modern notice and visual guide, not a generic presentation

If any slide fails: fix, re-render, verify. If fixing requires removing copy, remove the copy. Deliver only after a clean pass.

---

## Step 6: Deliver

Save to `./outputs/[topic-slug].pptx`. Confirm: slide count, image approach, QA passed.

Do **not** show internal labels — no skill instructions, no source filenames, no implementation notes, no QA checklist text — on any visible slide.
