---
name: acid-labels-pptx
description: "Reusable fixed-style PPTX generation skill for the Acid Labels visual brand — bold acid-green (#A9FF7A) operating-guide aesthetic on hard-edged modular panels, deep forest (#3F5E31) plates, black pill labels, white tag chips, oversized italic serif curly-brace title moments, condensed sans labels, data-native charts and dashboards, widescreen 16:9 editable .pptx output. Use this skill whenever the user mentions Acid Labels, asks for a presentation or deck in the Acid Labels style, wants a bold acid-green operating guide / playbook deck, a modular label-driven data deck, or mentions the acid-green + forest-green + black pill-label look for slides. Also trigger when the user says 'acid labels', 'acid green deck', 'operating guide deck', 'playbook slides', or 'label system presentation' in any context. Display name: Acid Labels PPTX."
---

# Acid Labels PPTX Skill

A reusable fixed-style PowerPoint generation skill. It builds on the `pptx` skill's technical capabilities while locking in the **Acid Labels** visual identity: a bold, acid-green professional *operating guide* — modular, label-driven, data-native, and confident.

**Core principle — style wins over content volume.** When the user's topic contains more information than the format can hold, compress and reinterpret into charts, chips, tiles, and extra slides. The deck must feel like a bold acid-green operating guide for the user's topic — **not** a generic report, **not** a copied brand-guidelines deck, and **not** a text-heavy memo. Every slide is a modular panel in a confident operating system.

**This skill is topic-agnostic.** It generates Acid Labels decks for *any* user-provided topic. Never hardcode a sample topic (finance, equities, chips, AI infrastructure, or any other) into a deck. Any topic-specific wording in this file is an *example only* — replace it at runtime with the user's topic variables.

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
  - `No generated images` — Editable native panels and charts only (Recommended)
  - `Generate with gpt-image-2` — Abstract acid-green textures + topic-supporting theme images
  - `Use my uploaded / reference images` — Insert images I provide

If the user hasn't provided data, audience, dates, or other details, **infer neutral content or use clearly labeled placeholder figures** (see Content Rules). Do not keep asking. Once you have the three core answers, proceed directly to generation.

---

## Step 2: Topic Translation — Everything Becomes an Operating Guide

Before writing any slide copy, translate the user's topic into an Acid Labels frame. No topic is too technical, soft, or unusual. Every subject becomes a confident operating guide, playbook, or decision system — while preserving the user's actual subject.

| User provides | Acid Labels treatment |
|---|---|
| Product / launch | Operating guide: how it works, the numbers, the decision |
| Strategy / plan | Playbook: sections, scenarios, checklist |
| Research / concept | Field system: taxonomy labels, data blocks, sources |
| Team / process | Operating manual: roles, workflow, KPIs, risk grid |
| Event / program | Program system: schedule grid, tracks, KPI tiles |
| Any other subject | Reframe as a labeled, data-native operating guide |

Decide these **before** writing slides, and use them as the cover's curly-brace title moment `{TOPIC}` and the deck's spine:
- The **guide title** (the `{TOPIC}` moment).
- The **one-line operating thesis** (what this guide is for).
- The **taxonomy label stack** (2–4 stacked short labels, e.g. category / subject / edition).

---

## Step 3: Generate Images (only if the user chose gpt-image-2)

If the user chose **No generated images** or **uploaded images**, skip this step. For uploads, place their images into forest-green image plates and leave editable placeholder rects where images are missing.

If the user chose **gpt-image-2**, read the `generate-image` skill at `/home/node/.claude/skills/generate-image/SKILL.md` for the exact API call pattern. Use `openai/gpt-image-2` with `response_format: "b64_json"` and `aspectRatio` matching the plate (`"16:9"` for cover/dividers). Save each image to `/tmp/acid-img-N.png`.

Generate **two clearly separated asset types**. Both types must contain **no readable text, no logos, no numbers, no real company/brand marks, and no recognizable real people.**

**Decorative image set** — abstract acid-green guideline textures, used *only* as cover backplates, section-divider image plates, and non-informational background texture:
```
Abstract acid-green guideline texture, shadowy green gradients, diagonal glass-like shadows,
close-cropped abstract panels, acid-green (#A9FF7A) overlays over deep forest green, subtle grain,
high-contrast black and green geometric shapes. No text, no logos, no numbers, no company marks,
no people. 16:9 composition, flat design-system texture, non-illustrative.
```

**Theme image set** — topic-specific *supporting* images that visually back the user's subject without embedding any slide content:
```
Abstract supporting imagery evoking [TOPIC MOOD WORDS], acid-green and deep forest green palette,
soft shadows, matte glass surfaces, high-contrast shapes. No readable text, no logos, no numbers,
no recognizable real people, no brand marks. 16:9, atmospheric, non-literal.
```

**Never** use gpt-image-2 to make full-slide screenshots, slide mockups, text-heavy graphics, charts with embedded numbers, logos, or anything that should be an editable PowerPoint element. Charts, tables, tiles, matrices, labels, and metadata are always native PowerPoint — never images.

Count guidance: 8 slides → 2–3 images · 10–12 slides → 3–4 · 15 slides → 4–5. Keep at least half decorative.

---

## Step 4: Build the PPTX

Read the `pptx` skill at `/home/node/.claude/skills/pptx/SKILL.md` and its `pptxgenjs.md` reference for the full API and gotchas. Build with **PptxGenJS** as editable native elements. Output must be an editable widescreen 16:9 `.pptx`. **Do not** create HTML, web presentations, screenshots of slides, or rasterized full-slide images.

### Core style constants — do not deviate

```javascript
const ACID    = "A9FF7A"; // dominant brand system color (acid green)
const FOREST  = "3F5E31"; // deep forest panels / image plates
const BLACK    = "000000"; // titles, chart strokes, pill labels
const WHITE   = "F7F7F1"; // light cards, tag chips
const SKY     = "8BD4F4"; // data blocks / chart fills
const PINK    = "F1AEC0"; // analyst notes
const RED      = "C90D0D"; // risk / warning wedges
const YELLOW  = "FFF34D"; // highlight / emphasis blocks

const SERIF = "Bookman Old Style"; // expressive display serif for {curly-brace} title moments (italic)
const SANS  = "Arial";             // condensed-feel sans for labels + compact chart text
```

Fonts are chosen from the pptx skill's QA-safe list so overflow checks are trustworthy. Use `SERIF` italic for the big `{TOPIC}` moments; use `SANS` (often uppercase with `charSpacing`) for pill labels, tag chips, taxonomy stacks, footer metadata, chart labels, and body.

### Typography sizing (strong hierarchy is mandatory)

| Role | Font | Size | Notes |
|------|------|------|-------|
| Cover title `{TOPIC}` | SERIF italic | 64–104 pt | curly-brace moment, ACID or BLACK |
| Section number | SANS/SERIF | 120–220 pt | oversized, low-contrast or ACID on FOREST |
| Slide headline | SERIF/SANS | 34–58 pt | one per slide |
| Metric numerals | SANS | 36–72 pt | KPI tiles / stat callouts |
| Body text | SANS | 18–26 pt | fragments, never paragraphs |
| Chart labels | SANS | 10–14 pt | axis, data labels, legends |
| Pill / tag / footer metadata | SANS | 10–14 pt | uppercase, `charSpacing: 2–6` |

### Layout — LAYOUT_WIDE (13.3" × 7.5") for a true 16:9 canvas

Set `pres.defineLayout` / `pres.layout = "LAYOUT_WIDE"` **before** adding slides. All coordinates below assume a 13.3 × 7.5 canvas.

### The Acid Labels component kit (all native, all editable)

Build slides from these repeatable modules — repetition of the label system *is* the motif:

- **Black pill label** — `ROUNDED_RECTANGLE`, `fill: BLACK`, high `rectRadius`, white/acid uppercase SANS text inside, `margin: 0`. Used for section names and status tags.
- **Tag chip** — small `ROUNDED_RECTANGLE` in WHITE or ACID with BLACK text; rows of chips for categories/filters.
- **Stacked taxonomy label** — 2–4 short SANS uppercase lines, left-aligned, tight leading, in a corner.
- **Large section number** — 120–220 pt numeral, placed in a FOREST panel or bleeding off one edge, never over a headline.
- **Hard-edged modular panel** — plain `RECTANGLE` blocks (ACID, FOREST, WHITE, SKY) in a strict grid; a rounded outer slide frame is fine, inner data panels are hard-edged.
- **Forest image plate** — FOREST rectangle holding an image or acting as a dark backplate.
- **KPI tile** — small panel: 36–72 pt metric numeral + tiny SANS label + optional delta.
- **Source-note row** — a thin bottom row: `Source: … · data as of [date]` in 10–12 pt.
- **Footer metadata dots** — tiny SANS text + small circle marks along a bottom edge.
- **Rounded slide corners** — outer frame with `rectRadius`; keep it a background frame, never through text.

### Data-native visual forms — choose what fits the topic

Prefer turning dense analysis into visuals rather than prose. Use native `addChart()` / native shapes for: stacked bar, grouped bar, line, pie/donut, waterfall, comparison tables, sensitivity heatmaps (grid of colored cells), probability–impact risk grids, scenario matrices (2×2), dashboards (tile clusters), KPI tiles, source-note rows, and structured decision checklists. **Adapt these to the user's topic — never force finance-specific charts where they don't fit.** Follow the pptx skill's chart gotchas (native charts only; set title/data labels/`chartColors` from the palette above; quiet the axes; stacked labels use `ctr`/`inEnd`/`inBase`, never `outEnd`).

Everything — text, blocks, section numbers, pills, chips, taxonomy stacks, metadata dots, rules, source rows, KPI tiles, tables, charts, matrices, grids, dashboards — must be **editable native PowerPoint elements**.

---

## Acid Labels System Rules — These Override Everything

The most common failure is a text-heavy memo hiding behind acid-green paint, or decorative elements colliding with content. These rules prevent that. When a rule conflicts with fitting more content, the rule wins — compress or split instead.

### Rule 1: Style wins over content volume
Compress dense topics into charts, chips, tiles, and extra slides. Do not shrink fonts below the sizing table or fill a slide with paragraphs.

### Rule 2: One idea per slide
Each slide carries exactly one primary question, claim, or idea. Keep prose concise; if a second explanatory sentence appears, cut it or move it to its own slide.

### Rule 3: Bold hierarchy, always
Every slide has one dominant element (headline, section number, or hero metric). Labels, chips, and metadata stay small and peripheral. The reading order must be obvious at a glance.

### Rule 4: Dividers and decoration never touch text
Rules, decorative bars, image plates, tag chips, section numbers, and chart elements must sit in safe spacing zones. No divider may pass through a headline, subtitle, body copy, or chart label. Section numbers bleed off edges or sit in their own panel — never behind live text at the same coordinates.

### Rule 5: Strict grid, generous spacing
Align everything to a consistent grid with ≥ 0.4" gutters and ≥ 0.5" slide margins. If content doesn't fit beautifully, split it across additional slides or simplify the copy — never crowd.

### Rule 6: Images are decorative or supporting — never content
Generated/uploaded images are cover backplates, divider plates, forest-plate supports, or texture. They never carry readable slide text, numbers, charts, or logos, and must not reduce text contrast. If text sits over an image, use a FOREST or BLACK overlay panel behind the text.

### Rule 7: Never expose internals
No `style prompt`, source filenames, implementation notes, generation instructions, or placeholder labels like `{TOPIC}` literal braces-as-instruction may appear on a visible slide. The `{ }` treatment is a *design* flourish around the real title text, not a leftover token.

---

## Suggested Slide Structure

Use when the user gives no outline; adapt freely when they do.

| # | Slide type | Notes |
|---|---|---|
| 1 | Cover | `{TOPIC}` serif moment, taxonomy label stack, footer metadata, decorative backplate |
| 2 | Contents / operating map | Numbered sections as pill labels in a grid |
| 3 | Section divider | Oversized section number + FOREST/image plate + one line |
| 4 | Framing / thesis | One claim, 2–3 supporting fragments as chips |
| 5 | Data block | Primary chart (bar/line/stacked) with source-note row |
| 6 | Comparison / matrix | Comparison table or 2×2 scenario matrix |
| 7 | KPI dashboard | Row/grid of KPI tiles + one supporting chart |
| 8 | Risk / sensitivity | Probability–impact grid or sensitivity heatmap (RED wedges) |
| 9 | Decision checklist | Structured checklist as native rows/checkboxes |
| 10 | Closing | Recap thesis + next-step pill labels + footer metadata |

Scale sections up or down to match the requested slide count; keep dividers between major sections.

---

## Content Rules

- **Use the user's data when provided.** When they don't, use **clearly labeled placeholder figures**, sample chart structures, and neutral axis labels (e.g. "Metric A", "Q1–Q4", "Segment 1"). Do **not** invent real current facts, prices, financial figures, forecasts, market caps, or other time-sensitive data.
- Add a small `data as of [date]` note in the source-note row **wherever real data is used** (use the current date, 2026-09-03, unless the user gives one).
- Keep each slide to one idea; turn density into charts, tables, chips, diagrams, or extra slides rather than shrinking text.

---

## PptxGenJS Critical Reminders (from the pptx skill)

- Set `pres.layout = "LAYOUT_WIDE"` before adding slides.
- Hex colors: never `#`, never 8-digit alpha — `color: "A9FF7A"`. Use `transparency:` for translucent fills, not baked alpha.
- Build a fresh options/shadow object per shape — PptxGenJS mutates in place.
- `rectRadius` only works on `ROUNDED_RECTANGLE`; use it for pills/chips/outer frame.
- `margin: 0` on any text box that must align to a pill, chip, panel edge, or chart.
- Keep charts native (`addChart`); set `showTitle`+`title`, `showValue`+`dataLabelPosition`, `chartColors` from the palette, quiet the axes. Stacked labels: `ctr`/`inEnd`/`inBase` only.
- Verify every LINE/rule `y` range does not intersect any text box — Rule 4.
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
- [ ] Overlapping text and dividers; decorative bars, plates, chips, or section numbers colliding with content (Rule 4)
- [ ] Unreadable chart labels (contrast + size 10–14 pt)
- [ ] Image assets reducing text contrast — add FOREST/BLACK overlay
- [ ] Strong hierarchy present: one dominant element per slide
- [ ] Strict grid alignment, ≥ 0.5" margins, ≥ 0.4" gutters
- [ ] Acid green reads as the dominant system color across the deck
- [ ] All labels/charts/tables/tiles are editable native elements (no rasterized full slides)
- [ ] No internal labels, filenames, notes, or leftover `{TOPIC}` instruction tokens visible
- [ ] `data as of [date]` note present wherever real data is used

If any slide fails: fix it, re-render only the changed slides, verify again. If resolving a collision needs less copy, remove copy. Deliver only after a clean pass.

---

## Step 6: Deliver

Save to `./outputs/[topic-slug]-acid-labels.pptx`. Confirm to the user: slide count, image approach, and that QA passed. Do not show any internal skill instructions, source filenames, or implementation notes on any visible slide or in the delivered file.
