---
name: gradient-calendar-pptx
description: "Reusable fixed-style PPTX generation skill for the Gradient Calendar visual brand — pale gray (#F1F3F7) calendar-native productivity aesthetic with near-black oversized numerals, electric lime (#C8FF00) schedule blocks, saturated blue (#0B74FF) vertical labels, and soft cyan-lime-lavender gradient washes, on strict calendar grids, widescreen 16:9 editable .pptx output. Use this skill whenever the user mentions Gradient Calendar, asks for a presentation or deck in the Gradient Calendar style, wants a calendar-native / agenda-poster / schedule-led productivity deck, a planner or roadmap deck with oversized date numerals and lime event blocks, or mentions the pale-gray + electric-lime + blue + gradient-wash look for slides. Also trigger when the user says 'gradient calendar', 'calendar deck', 'agenda poster deck', 'schedule deck', 'planner slides', or 'productivity system presentation' in any context. Display name: Gradient Calendar PPTX."
---

# Gradient Calendar PPTX Skill

A reusable fixed-style PowerPoint generation skill. It builds on the `pptx` skill's technical capabilities while locking in the **Gradient Calendar** visual identity: a polished, calendar-native productivity system — sparse poster-like covers, strict calendar grids, oversized date numerals, electric-lime schedule blocks, and soft gradient washes.

**Core principle — style wins over content volume.** When the user's topic contains more information than the format can hold, compress it into calendar grids, schedule cards, timelines, and extra slides. The deck must feel like a polished calendar-native productivity system for the user's topic — **not** a generic SaaS pitch deck, **not** a cluttered screenshot dump, and **not** a text-heavy product report.

**This skill is topic-agnostic.** It generates Gradient Calendar decks for *any* user-provided topic. Never hardcode a sample topic (productivity apps, SaaS, calendar products, launch plans, specific years, or any brand) into a deck. Any topic-specific wording in this file is an *example only* — replace it at runtime with the user's topic variables.

---

## Step 1: Gather Inputs (Ask First — Max 3 Questions)

Do **not** start generating immediately. Use the `AskUserQuestion` tool to present the missing questions in a **single** call (up to 3 at once). Only ask what the user hasn't already provided in their prompt — if they already gave the topic, slide count, or image choice, skip that question. Do not ask any extra questions unless the deck literally cannot be built without them.

**Question 1 — Topic** (skip if already provided):
- header: "Topic"
- question: "What is the topic or title of the deck?"
- options: 2–3 relevant example topics plus allow Other

**Question 2 — Slide count** (skip if already specified):
- header: "Slides"
- question: "How many slides should the deck include?"
- options: `8 slides`, `10 slides (Recommended)`, `12 slides`, `15 slides`

**Question 3 — Images**:
- header: "Images"
- question: "How should visuals be handled?"
- options:
  - `No generated images` — Editable native grids, cards, and gradient fields only (Recommended)
  - `Generate with gpt-image-2` — Abstract gradient washes + topic-supporting theme images
  - `Use my uploaded / reference images` — Insert images I provide

If the user hasn't provided data, dates, audience, or other details, **infer neutral content or use clearly labeled placeholder figures** (see Content Rules). Do not keep asking. Once you have the three core answers, proceed directly to generation.

---

## Step 2: Topic Translation — Everything Becomes a Calendar-Native System

Before writing any slide copy, translate the user's topic into a Gradient Calendar frame. No topic is too abstract or too far from planning to work. Every subject becomes a schedule, agenda, roadmap, or planning system — while preserving the user's actual subject.

| User provides | Gradient Calendar treatment |
|---|---|
| Product / launch | A rollout calendar: phases, milestones, schedule cards |
| Strategy / plan | A planning grid: quarters, tracks, timeline strips |
| Research / concept | A structured agenda: sections as calendar blocks |
| Team / process | An operating schedule: cadences, roles, weekly grids |
| Event / program | A program calendar: days, tracks, agenda rows |
| Any other subject | Reframe as a schedule-led, calendar-native system |

Decide these **before** writing slides, and use them to anchor the cover and the deck's spine:
- The **hero numeral** (a year, date, index, edition, or time-system number for the cover).
- The **deck title** (bold, black, beneath the numeral).
- The **vertical spine word** (one saturated-blue word running up the right edge — a month, category, or theme word).

---

## Step 3: Generate Images (only if the user chose gpt-image-2)

If the user chose **No generated images** or **uploaded images**, skip generation. For uploads, place their images into black/white photo panels or mockup frames, and leave editable placeholder rects where images are missing.

If the user chose **gpt-image-2**, read the `generate-image` skill at `/home/node/.claude/skills/generate-image/SKILL.md` for the exact API call pattern. Use `openai/gpt-image-2` with `response_format: "b64_json"` and `aspectRatio` matching the placement (`"16:9"` for washes/dividers). Save each image to `/tmp/gradient-cal-img-N.png`.

Generate **two clearly separated asset types**. Both must contain **no readable text, no logos, no real app/brand marks, and no recognizable real people.**

**Decorative image set** — abstract cyan-lime-lavender gradient washes, used *only* as cover gradient washes, section-divider atmospheres, and non-informational background accents:
```
Abstract smooth gradient wash, calendar-paper light leak, pale blue to electric lime to soft violet haze,
airbrushed luminous background, clean and diffuse, no text, no logos, no people, no UI, no objects.
16:9 composition, soft focus, high-key, non-illustrative.
```

**Theme image set** — topic-specific *supporting* visuals that back the user's subject without embedding any slide content, used on concept/workflow/use-case/performance/roadmap/closing slides:
```
Abstract supporting imagery evoking [TOPIC MOOD WORDS], pale gray and soft gradient palette with cyan,
lime, and lavender light, clean and calm. No readable UI text, no logos, no app branding,
no recognizable real people, no brand marks, no legible numbers. 16:9, atmospheric, non-literal.
```

**Never** use gpt-image-2 to make full-slide screenshots, slide mockups with embedded text, text-heavy graphics, charts with embedded numbers, logos, or anything that should be an editable PowerPoint element. Calendar grids, date numerals, schedule cards, stat cards, charts, and labels are always native PowerPoint — never images.

Count guidance: 8 slides → 2–3 images · 10–12 slides → 3–4 · 15 slides → 4–5. Keep at least half decorative.

---

## Step 4: Build the PPTX

Read the `pptx` skill at `/home/node/.claude/skills/pptx/SKILL.md` and its `pptxgenjs.md` reference for the full API and gotchas. Build with **PptxGenJS** as editable native elements. Output must be an editable widescreen 16:9 `.pptx`. **Do not** create HTML, web presentations, screenshots of slides, or rasterized full-slide images.

### Core style constants — do not deviate

```javascript
const CANVAS   = "F1F3F7"; // main slide canvas (pale gray)
const INK      = "111111"; // large typography, numerals, titles
const LIME     = "C8FF00"; // key schedule / event blocks (electric lime)
const BLUE     = "0B74FF"; // vertical labels, event markers, spine word
const CYAN     = "7FE8F1"; // diffuse gradient wash
const LAVENDER = "B7A5FF"; // diffuse gradient wash
const WHITE    = "FFFFFF"; // inner panels / cards
const CHARCOAL = "1A1D22"; // occasional deep contrast panels

const DISPLAY = "Arial";   // near-black display numerals + headlines (heavy weight)
const SANS    = "Arial";   // labels, body, chart text, metadata
```

Fonts are chosen from the pptx skill's QA-safe list so overflow checks stay trustworthy. Use heavy/bold weight for the oversized numerals and headlines; use regular SANS (often uppercase with `charSpacing`) for vertical labels, agenda rows, metadata, and chart text. PptxGenJS has no true gradient fill — build the cyan-lime-lavender wash from a generated image (Step 3) or by layering 2–3 translucent shapes (`transparency:`), never a baked-alpha hex.

### Typography sizing (strong hierarchy is mandatory)

| Role | Size | Notes |
|------|------|-------|
| Cover hero numeral | 96–150 pt | INK, left side, dominant |
| Cover title | 38–64 pt | INK, bold, beneath numeral |
| Slide headline | 34–56 pt | one per slide |
| Metric numerals | 38–72 pt | stat cards / date numerals |
| Body text | 18–26 pt | fragments, never paragraphs |
| Chart labels | 10–14 pt | axis, data labels, legends |
| Vertical labels / metadata | 10–16 pt | uppercase, `charSpacing: 2–6` |

### Layout — LAYOUT_WIDE (13.3" × 7.5") for a true 16:9 canvas

Set `pres.layout = "LAYOUT_WIDE"` **before** adding slides. All coordinates below assume a 13.3 × 7.5 canvas.

---

## The Cover — Follow This Composition Strictly

The cover is a **sparse full-slide pale-gray agenda poster**, under **14 visible words**. It aligns to this exact recipe. Build every element as an editable native shape/text — never an image of a cover.

```
Canvas: full-slide CANVAS (F1F3F7)
Hero numeral:   one huge INK year/date/index/time numeral on the LEFT (96–150 pt)
Title:          bold INK title directly BENEATH the numeral (38–64 pt)
Subtitle:       one tiny subtitle in the LOWER-LEFT area (12–16 pt)
Gradient wash:  soft cyan-lime-lavender wash across the LOWER HALF
                (generated image, or 2–3 layered translucent CYAN/LIME/LAVENDER shapes)
Lime anchor:    one electric-LIME block anchored to the BOTTOM-LEFT edge
Stripe cluster: 5–7 thin INK vertical stripes near the UPPER-RIGHT
Spine word:     one vertical BLUE word along the RIGHT edge (rotate 90°/270°)
Metadata:       only two or three tiny metadata text blocks
```

**Do not** put app screenshots, bar charts, dashboards, KPI tiles, feature cards, photo collages, human portraits, icons, or paragraphs on the cover. Keep it minimal — it must read as a quiet agenda poster, not a title slide crammed with proof points. If elements start to crowd, remove metadata blocks first.

---

## Content Slides — From Slide 2 Onward

Build slides from these calendar-native modules (all editable native elements). Vary them across the deck; repetition of the calendar/grid system *is* the motif:

- **Strict calendar grid** — a grid of `RECTANGLE`/`ROUNDED_RECTANGLE` cells with oversized INK date numerals; highlight key days with LIME blocks.
- **Oversized date numeral** — a 38–72 pt INK numeral labeling a day, phase, or step.
- **Electric-lime event block** — a LIME rectangle holding a short event/label; the deck's signature accent (use sparingly for emphasis).
- **Saturated-blue side label** — a vertical BLUE word/label running up a slide edge or column.
- **Black/white photo panel** — a panel holding an uploaded or theme image, desaturated toward black-and-white for calm contrast.
- **Soft gradient gutter** — a narrow cyan-lime-lavender wash between columns or along an edge (decorative, never behind live text).
- **Vertical month/category word** — rotated SANS label as a spine or column marker.
- **Timeline strip / roadmap row** — a horizontal strip of dated markers or phase rows.
- **Concept / product mockup frame** — a clean rounded frame suggesting a screen or artifact, drawn as native shapes (never a real screenshot with embedded text).
- **Clean stat card** — WHITE panel: 38–72 pt metric numeral + tiny SANS label.

### Data forms — use lightly, only where they fit the topic

Prefer calendar grids, schedule cards, and timelines over charts. When data genuinely helps, use native `addChart()` / native shapes for: small bar charts, simple line charts, calendar heatmaps (grid of tinted cells), comparison cards, compact KPI tiles, timeline strips, roadmap rows, planning grids, before/after cards, and schedule-led matrices. **Adapt these to the user's topic — never force product-specific metrics where they don't fit.** Follow the pptx skill's chart gotchas (native charts only; set title/data labels/`chartColors` from the palette; quiet the axes; stacked labels use `ctr`/`inEnd`/`inBase`, never `outEnd`).

Everything — text, layout blocks, calendar grids, date numerals, vertical stripe motifs, gradient fields, schedule cards, app/mockup frames, stat blocks, charts, agenda rows, and callout panels — must be **editable native PowerPoint elements**.

---

## Gradient Calendar System Rules — These Override Everything

The most common failures are a cluttered cover, a text-heavy report behind soft gradients, and decorative elements slicing through text. These rules prevent that. When a rule conflicts with fitting more content, the rule wins — compress or split instead.

### Rule 1: Style wins over content volume
Compress dense topics into calendar grids, schedule cards, timelines, comparison blocks, and extra slides. Do not shrink fonts below the sizing table or fill a slide with paragraphs.

### Rule 2: One idea per slide, most under 35 words
Each content slide carries one primary idea and stays under ~35 visible words. If a second explanatory sentence appears, cut it or move it to its own slide.

### Rule 3: Sparse cover, disciplined density
The cover follows the strict recipe above (under 14 words). Content slides stay calm and gridded — generous whitespace is part of the style, not wasted space.

### Rule 4: Decoration never touches text
Divider lines, vertical stripes, gradient gutters/washes, lime blocks, date numerals, schedule cards, photo panels, and chart elements must sit in safe spacing zones. None may pass through a headline, subtitle, body copy, label, or chart text. The gradient wash sits behind empty canvas areas or under a WHITE/CHARCOAL panel when text must sit over it.

### Rule 5: Strict grid, generous spacing
Align everything to a consistent calendar grid with ≥ 0.4" gutters and ≥ 0.5" slide margins. If content doesn't fit beautifully, split it across additional slides or simplify the copy — never crowd.

### Rule 6: Images are decorative or supporting — never content
Generated/uploaded images are gradient washes, divider atmospheres, black/white photo panels, or theme support. They never carry readable slide text, numbers, charts, logos, or UI, and must not reduce text contrast. If text sits over an image, place a WHITE or CHARCOAL panel behind the text.

### Rule 7: Never expose internals
No `style prompt`, source filenames, implementation notes, generation instructions, or leftover placeholder tokens may appear on a visible slide.

---

## Suggested Slide Structure

Use when the user gives no outline; adapt freely when they do.

| # | Slide type | Notes |
|---|---|---|
| 1 | Cover | Strict agenda-poster recipe (hero numeral, title, spine word, wash, lime anchor, stripes) |
| 2 | Agenda / calendar overview | Calendar grid or agenda rows mapping the deck |
| 3 | Section divider | Gradient-wash atmosphere + oversized numeral + one line |
| 4 | Concept / framing | One idea, supporting fragments, optional theme image |
| 5 | Timeline / roadmap | Horizontal timeline strip or roadmap rows |
| 6 | Planning grid | Calendar/planning grid with lime event blocks |
| 7 | Data / stat cards | Clean stat cards or a small chart with source note |
| 8 | Comparison / before-after | Comparison cards or before/after panels |
| 9 | Use case / workflow | Mockup frames or workflow steps as calendar blocks |
| 10 | Closing | Recap + next-step schedule cards + spine word reprise |

Scale sections up or down to match the requested slide count; keep dividers between major sections.

---

## Content Rules

- **Use the user's data when provided.** When they don't, use **clearly labeled placeholder figures** and sample chart structures (e.g. "Metric A", "Phase 1–4", "Week 1"). Do **not** invent real customer numbers, business metrics, financial figures, dates, forecasts, or other time-sensitive facts.
- Add a small `data as of [date]` note wherever real data is used (use the current date, 2026-09-03, unless the user gives one).
- Keep each slide to one idea; turn density into calendar grids, schedule cards, timelines, comparison blocks, charts, or extra slides rather than shrinking text.

---

## PptxGenJS Critical Reminders (from the pptx skill)

- Set `pres.layout = "LAYOUT_WIDE"` before adding slides.
- Hex colors: never `#`, never 8-digit alpha — `color: "C8FF00"`. Use `transparency:` for translucent gradient layers, not baked alpha.
- No native gradient fill — build the wash from a generated image or layered translucent shapes.
- Build a fresh options/shadow object per shape — PptxGenJS mutates in place.
- `rectRadius` only works on `ROUNDED_RECTANGLE` (cards, frames, chips).
- `margin: 0` on any text box that must align to a grid cell, block, panel edge, or chart.
- Rotate vertical spine words with `rotate: 270` (or `90`); verify the rotated bounding box stays clear of other elements.
- Keep charts native (`addChart`); set `showTitle`+`title`, `showValue`+`dataLabelPosition`, `chartColors` from the palette, quiet the axes.
- Verify every LINE/stripe/gutter `y`/`x` range does not intersect any text box — Rule 4.
- After `writeFile()`, run `python /home/node/.claude/skills/pptx/scripts/office/validate.py output.pptx` and fix reported faults in the generator.

---

## Step 5: Visual QA — Required Before Delivery

Convert slides to images and inspect **every** slide. Not optional.

```bash
python -m markitdown output.pptx
python /home/node/.claude/skills/pptx/scripts/office/soffice.py --headless --convert-to pdf output.pptx
rm -f slide-*.jpg
pdftoppm -jpeg -r 150 output.pdf slide
python /home/node/.claude/skills/pptx/scripts/office/validate.py output.pptx
```

Inspect the rendered images fresh (a subagent works well) and fix before delivery:

- [ ] Text overflow or text cut off at any box/slide boundary (check first)
- [ ] Crowded layouts / overly dense body copy — split or compress
- [ ] Overlapping text and decorative elements; vertical stripes, gutters, washes, lime blocks, numerals, cards, or photo panels colliding with content (Rule 4)
- [ ] Cover has too many elements — trim to the strict recipe, under 14 words
- [ ] Unreadable chart labels (contrast + size 10–14 pt)
- [ ] Image assets reducing text contrast — add WHITE/CHARCOAL panel behind text
- [ ] Strong hierarchy present: one dominant element per slide; calendar grids aligned
- [ ] Strict grid alignment, ≥ 0.5" margins, ≥ 0.4" gutters
- [ ] Pale-gray canvas and calendar-native feel hold across the deck
- [ ] All grids/cards/charts/numerals are editable native elements (no rasterized full slides)
- [ ] No internal labels, filenames, notes, or leftover instruction tokens visible
- [ ] `data as of [date]` note present wherever real data is used

If any slide fails: fix it, re-render only the changed slides, verify again. If resolving a collision needs less copy, remove copy. Deliver only after a clean pass.

---

## Step 6: Deliver

Save to `./outputs/[topic-slug]-gradient-calendar.pptx`. Confirm to the user: slide count, image approach, and that QA passed. Do not show any internal skill instructions, source filenames, or implementation notes on any visible slide or in the delivered file.
