---
name: neon-motion-pptx
description: "Reusable fixed-style PPTX generation skill for the Neon Motion visual brand — a premium cinematic pitch built from editorial motion photography and restrained typography, with electric cyan (#08BFEA) versus saturated orange (#FF7317) light, deep petrol, near-black, white, and cool paper gray, thin geometric sans titles, hairline rules, tiny vertical metadata, and generous empty space, in widescreen 16:9 editable .pptx output. Use this skill whenever the user mentions Neon Motion, asks for a presentation or deck in the Neon Motion style, wants a cinematic / motion-poster / editorial-photography pitch deck, a premium cyan-and-orange motion-lit deck, or a restrained-typography image-led deck. Also trigger when the user says 'neon motion', 'motion poster deck', 'cinematic pitch deck', 'cyan and orange deck', 'editorial motion deck', or 'premium photographic pitch' in any context. Display name: Neon Motion PPTX."
---

# Neon Motion PPTX Skill

A reusable fixed-style PowerPoint generation skill. It builds on the `pptx` skill's technical capabilities while locking in the **Neon Motion** visual identity: a premium cinematic pitch built from editorial motion photography and restrained typography — full-bleed motion imagery in electric cyan versus warm orange light, thin geometric sans titles, hairline rules, and generous empty space.

**Core principle — restraint and cinema win over content volume.** When the user's topic carries more information than the format can hold gracefully, compress it into sparse typographic rows, one compact chart, a timeline, concise metric moments, and extra slides. The deck must feel like a premium cinematic pitch for the user's topic — **not** a dark SaaS dashboard, an AI report, a cyberpunk poster, a conference deck, a generic startup template, a cluttered product report, or a text-heavy memo.

**This skill is topic-agnostic.** It generates Neon Motion decks for *any* user-provided topic. Never hardcode a sample topic (a company name, AI customer intelligence, sales pitches, revenue operations, a specific year, fictional metrics, fixed pricing, or fixed product features) into a deck. Any topic-specific wording in this file is an *example only* — replace it at runtime with the user's topic variables.

---

## Step 1: Gather Inputs (Ask First — Max 3 Questions)

Do **not** start generating immediately. Use the `AskUserQuestion` tool to present the missing questions in a **single** call (up to 3 at once). Only ask what the user hasn't already provided — if they gave the topic, slide count, or image choice, skip that question. Don't ask extra questions unless the deck literally cannot be built without them.

**Question 1 — Topic** (skip if already provided):
- header: "Topic"
- question: "What is the topic, product, company, or title of the deck?"
- options: 2–3 relevant example topics plus allow Other

**Question 2 — Slide count** (skip if already specified):
- header: "Slides"
- question: "How many slides should the deck include?"
- options: `8 slides`, `10 slides (Recommended)`, `12 slides`, `15 slides`

**Question 3 — Images**:
- header: "Images"
- question: "How should visuals be handled?"
- options:
  - `Generate with gpt-image-2` — Cinematic cyan/orange motion photography + topic theme visuals (Recommended)
  - `Use my uploaded / reference images` — Insert images I provide
  - `No generated images` — Native typography, hairlines, and charts only (color-field plates stand in for photos)

If the user hasn't provided data, dates, audience, or other details, **infer neutral content or use clearly labeled placeholder figures** (see Content Rules). Do not keep asking. Once you have the three core answers, proceed to generation.

**Note on the no-images choice:** the Neon Motion style leans heavily on cinematic photography. If the user picks *No generated images*, replace every full-bleed photo with a full-bleed cyan→orange color-field plate (layered translucent CYAN/ORANGE/PETROL shapes) so the motion-lit feel survives — never leave photo zones blank or fall back to a plain dark canvas.

---

## Step 2: Topic Translation — Everything Becomes a Cinematic Pitch

Before writing any slide copy, translate the user's topic into a Neon Motion frame. Every subject becomes a restrained, image-led pitch sequence — while preserving the user's actual subject.

| User provides | Neon Motion treatment |
|---|---|
| Product / launch | A cinematic product pitch: motion cover, one mockup frame, one proof metric |
| Strategy / plan | A restrained narrative: challenge rows, one timeline, one closing ask |
| Research / concept | An editorial essay: statement plates, one chart, sparse agenda lines |
| Service / brand | A premium brand film: motion plates, one claim per slide, quote plates |
| Any other subject | Reframe as a cinematic, photography-led pitch with restrained type |

Decide these **before** writing slides:
- The **motion energy** for the imagery (what kind of anonymous human/topic motion moves through cyan-and-orange light).
- The **one-line cover title** (thin white sans, no tagline).
- The **wordmark** (a product/company name, if any — placed tiny, never merged into the big title unless the user asks).

---

## Step 3: Generate Images (only if the user chose gpt-image-2)

If the user chose **No generated images**, skip generation and use color-field plates (Step 1 note). For **uploaded images**, place them full-bleed or in small crops/mockup frames, and use color-field plates where an image is missing.

If the user chose **gpt-image-2**, read the `generate-image` skill at `/home/node/.claude/skills/generate-image/SKILL.md` for the exact API call pattern. Use `openai/gpt-image-2` with `response_format: "b64_json"` and `aspectRatio` matching placement (`"16:9"` full-bleed, `"4:3"` thumbnails/mockups). Save each image to `/tmp/neon-motion-img-N.png`.

Generate **two clearly separated asset types** (these labels are production notes only — never printed on a slide). Both must contain **no readable text, no logos, no brand marks, no readable faces.**

**Decorative image set** — editorial long-exposure / cinematic motion photographs for the cover, full-bleed section plates, quote plates, and closing:
```
Cinematic editorial long-exposure photograph, anonymous people (or [TOPIC-RELEVANT SUBJECTS]) moving laterally
through electric cyan and warm orange light, blurred silhouettes and motion energy, natural cinematic lighting,
soft reflections, strong spatial depth, bright and vivid. No text, no logos, no readable faces, no dashboards,
no product UI, no lasers, no glass shards, no cosmic scenes, no tunnels, no neon grids, no empty interiors. 16:9.
```

**Theme image set** — restrained topic-support visuals for content slides (fictional interface mockups, minimal product-support scenes, anonymous team/workspace photography, other topic-specific support):
```
Restrained topic-support visual for [TOPIC], cinematic cyan-and-orange palette, calm and premium, anonymous
subjects only, natural lighting. No readable UI text, no logos, no brand marks, no readable faces, no legible
numbers, no charts. 4:3 or 16:9, editorial, non-literal.
```

Theme assets **support** the story; they never replace native editable charts, text, or structured content. **Never** use gpt-image-2 for full-slide screenshots, slide mockups with embedded text, text-heavy graphics, charts with embedded numbers, logos, or brand marks — those are always native PowerPoint.

Count guidance: 8 slides → 3–4 images · 10–12 slides → 4–6 · 15 slides → 6–8. Keep most of them decorative motion plates.

---

## Step 4: Build the PPTX

Read the `pptx` skill at `/home/node/.claude/skills/pptx/SKILL.md` and its `pptxgenjs.md` reference for the full API and gotchas. Build with **PptxGenJS** as editable native elements. Output must be an editable widescreen 16:9 `.pptx`. **Do not** create HTML, web presentations, screenshots of slides, or rasterized full-slide composites. Generated images may be inserted only as supporting photographic/visual assets.

### Core style constants — do not deviate

```javascript
const CYAN   = "08BFEA"; // electric cyan — primary motion light
const ORANGE = "FF7317"; // saturated orange — counter motion light
const PETROL = "07353C"; // deep petrol — depth panels / plates
const INK    = "111111"; // near-black — type on light canvases
const WHITE  = "FFFFFF"; // paper canvas + thin type on images
const PAPER  = "F5F5F3"; // cool paper gray — alternate canvas

const DISPLAY = "Arial";  // geometric sans display titles — LIGHT / regular weight only
const SANS    = "Arial";  // labels, body, metadata, chart text
```

Fonts are chosen from the pptx skill's QA-safe list so overflow checks stay trustworthy. Evoke the clean geometric-sans feel through **light/regular weight and letter-spacing** (`charSpacing`), never heavy bold — **never place a heavy bold title on an image slide.** PptxGenJS has no true gradient fill; build any cyan→orange color-field plate from a generated/uploaded image or by layering 2–3 translucent shapes (`transparency:`), never a baked-alpha hex.

### Typography sizing (strong hierarchy, generous space)

| Role | Size | Notes |
|------|------|-------|
| Cover title | 64–76 pt | one thin white line, never bold |
| Slide headline | 34–54 pt | one per slide |
| Metric numerals | 42–64 pt | proof moments |
| Body copy | 18–22 pt | fragments, never paragraphs |
| Metadata / vertical labels | 9–12 pt | uppercase, `charSpacing: 2–6` |
| Chart labels | 10–14 pt | axis, data labels, legends |

### Layout — LAYOUT_WIDE (13.3" × 7.5") for a true 16:9 canvas

Set `pres.layout = "LAYOUT_WIDE"` **before** adding slides. All coordinates below assume a 13.3 × 7.5 canvas.

---

## The Cover — Follow This Composition Strictly

A **premium motion-poster cover**. Build every text/rule/thumbnail element as editable native shapes/text over the background image — never an image of a finished cover.

```
Background:  ONE full-bleed 16:9 cinematic editorial image, cropped to all four edges.
             Reads immediately as electric CYAN vs warm ORANGE motion (anonymous human/topic motion,
             lateral movement, blurred silhouettes). Dark wash no stronger than 12% — keep cyan/orange bright.
             NOT an empty hallway, architecture-only, cosmic, data tunnel, gradient, single portrait,
             dashboard, product UI, sci-fi laser, neon grid, glass shards, or readable faces/text/logos.
Title:       ONE large thin WHITE sans title on ONE line, ~64–76 pt, centered near 42% slide width / 36% height.
             Do NOT merge the product/company name into it (unless the user asks for that exact title).
Wordmark:    product/company name (if any) as a TINY wordmark, top-right or another subtle metadata spot.
Vertical meta: small vertical year/index/metadata near the FAR-LEFT edge, ~12% of slide height.
Thumbnail:   exactly ONE small floating 4:3 thumbnail below & slightly left of the title, ~12–14% slide width,
             a tight cyan-orange crop; subtle translucent backing, no thick frame.
Glyph row:   one tiny row of media-control-style glyphs beside the thumbnail.
Descriptor:  one short two-line descriptor below the thumbnail.
Context:     tiny contact/context details at bottom-left when appropriate.
Hairline:    at most ONE short hairline — never a long rule across the whole slide.
```

Keep all cover copy **under 18 visible words** (excluding contact/context details). **Do not** put a subtitle, tagline, email-as-headline, agenda, metrics, product screenshot, portrait card, KPI, chart, panel, border, or explanatory paragraph on the cover. If elements start to crowd, remove the descriptor or glyph row first.

---

## Content Slides — From Slide 2 Onward

Use a restrained editorial rhythm: **alternate** white / cool-paper-gray canvas slides with full-bleed motion-photo slides. Build from these modules (all editable native elements except the photos themselves), varying them across the deck:

- **White agenda slide** — one square cyan/orange crop + a large two-line title + sparse typographic agenda lines separated by hairlines.
- **Full-bleed motion image** — one short claim (thin white type) + a few tiny bullets; keep text off the busiest part of the image (add a small translucent PETROL/INK pad only where legibility needs it).
- **Challenge rows** — short rows separated by thin hairlines on a white canvas, with one tall portrait or motion crop beside them.
- **Statement plate** — full-bleed image with one large thin statement + a miniature media tile.
- **Experience slide** — one product/concept mockup frame (native rounded shapes, never a real screenshot with embedded text) + one restrained chart.
- **Proof slide** — one or two large metric numerals + a single simple line chart, with an `illustrative` / `data as of` note.
- **Commercial / comparison slide** — typographic columns (no heavy cards) for pricing or comparison.
- **Pilot / roadmap / sequence slide** — a sparse horizontal timeline.
- **Closing slide** — full-bleed cyan-orange human-silhouette or topic-appropriate motion image + one concise ask.

Adapt this rhythm to the requested slide count and topic — do not force a fixed 10-slide structure.

### Data forms — use sparingly

Across a typical short deck, use only a **few** native analytical forms, adapted to the topic: **one** line chart, **one** before/after metric comparison, **one** typographic comparison or pricing layout, and **one** implementation timeline. Prefer restraint over dashboards. Follow the pptx skill's chart gotchas (native `addChart` only; set title/data labels/`chartColors` from the palette — cyan & orange primary; quiet the axes; stacked labels use `ctr`/`inEnd`/`inBase`, never `outEnd`).

Everything — text, hairline rules, vertical metadata, agenda lines, charts, metric numerals, mockup frames, timelines, comparison columns, thumbnails, and callouts — must be **editable native PowerPoint elements**. Only photographs are inserted images.

---

## Neon Motion System Rules — These Override Everything

The most common failures are a crowded cover, a dark-SaaS-dashboard feel, decoration slicing through text, a muddy/too-dark image, and a cover that reads as an empty room or generic AI software. These rules prevent that. When a rule conflicts with fitting more content, the rule wins — compress or split instead.

### Rule 1: Restraint and cinema win over content volume
Compress dense topics into sparse typographic rows, one compact chart, a timeline, metric moments, and extra slides. Never shrink fonts below the sizing table or fill a slide with paragraphs or stacks of cards.

### Rule 2: One dominant object, one idea, under ~30 words
Each content slide carries one dominant content object and one primary idea, and stays under ~30 visible words. A second explanatory sentence gets cut or moved to its own slide.

### Rule 3: Thin type, never heavy — especially on images
Titles are thin/light geometric sans. **Never** a heavy bold title on an image slide. Let letter-spacing and empty space do the work.

### Rule 4: Decoration never touches text
Hairline rules, thumbnails, media glyphs, vertical metadata, charts, image crops, mockup frames, and any decorative element must sit in safe spacing zones. None may pass through a headline, body copy, metadata, label, or chart text. Where text sits over a busy image, place a small translucent PETROL/INK pad behind just that text — never a full dark wash over the whole slide.

### Rule 5: Keep the cyan and orange bright
Full-bleed images must read immediately as cyan-versus-orange motion. Dark overlays stay ≤ 12%. Reject/regenerate any image that is muddy, too dark, or reads as an empty room, hallway, gradient, cosmic/data tunnel, or generic AI software.

### Rule 6: Generous empty space and precise alignment
Maintain wide margins (≥ 0.5"), clear reading order, and precise alignment. Empty space is the premium signal — do not fill it. If content doesn't fit beautifully, split it or simplify the copy.

### Rule 7: Images support, never carry content
Generated/uploaded images are cover/section/quote/closing plates, small crops, or topic support. They never carry readable slide text, numbers, charts, logos, or UI, and must not reduce text contrast.

### Rule 8: Never expose internals
No `style prompt`, `decorative image set` / `theme image set` labels, source filenames, model instructions, production notes, or leftover placeholder tokens may appear on a visible slide.

---

## Suggested Slide Structure

Use when the user gives no outline; adapt freely when they do.

| # | Slide type | Notes |
|---|---|---|
| 1 | Cover | Strict motion-poster recipe (full-bleed motion image, one thin title, thumbnail, vertical meta) |
| 2 | White agenda | Square cyan/orange crop + two-line title + sparse agenda lines |
| 3 | Statement plate | Full-bleed motion image + one large thin statement + miniature tile |
| 4 | Challenge rows | Hairline-separated rows + one tall motion crop |
| 5 | Concept / experience | One mockup frame + one restrained chart |
| 6 | Proof | One or two metric numerals + one simple line chart (illustrative note) |
| 7 | Commercial / comparison | Typographic columns, no heavy cards |
| 8 | Roadmap / pilot | Sparse horizontal timeline |
| 9 | Full-bleed claim | Motion image + one short claim + tiny bullets |
| 10 | Closing | Full-bleed silhouette/motion image + one concise ask |

Scale sections up or down to match the requested slide count; alternate white/paper canvases with full-bleed image slides throughout.

---

## Content Rules

- **Use the user's data when provided.** When they don't, use **clearly labeled placeholder / illustrative figures** and sample chart structures (e.g. "Metric A", "Phase 1–4", "Before / After"). Do **not** invent real customer numbers, financial figures, dates, forecasts, prices, or other time-sensitive facts.
- Label sample results as `illustrative`, and add a small `data as of [date]` note wherever real data is used (use the current date, 2026-09-03, unless the user gives one).
- Keep each slide to one idea; turn density into extra slides, sparse rows, one compact chart, a timeline, or metric moments rather than shrinking text.

---

## PptxGenJS Critical Reminders (from the pptx skill)

- Set `pres.layout = "LAYOUT_WIDE"` before adding slides.
- Hex colors: never `#`, never 8-digit alpha — `color: "08BFEA"`. Use `transparency:` for translucent pads / color-field layers, not baked alpha.
- No native gradient fill — build cyan→orange plates from an image or layered translucent shapes.
- Insert full-bleed photos at `x:0, y:0, w:13.3, h:7.5`; crops/thumbnails sized per the recipe.
- Build a fresh options/shadow object per shape — PptxGenJS mutates in place.
- `rectRadius` only works on `ROUNDED_RECTANGLE` (mockup frames, thumbnails, pads).
- `margin: 0` on any text box that must align to a title, column, grid, or chart edge.
- Rotate vertical metadata with `rotate: 270` (or `90`); verify the rotated bounding box stays clear of other elements.
- Keep charts native (`addChart`); set `showTitle`+`title`, `showValue`+`dataLabelPosition`, `chartColors` from the palette, quiet the axes.
- Verify every hairline/rule `y`/`x` range does not intersect any text box — Rule 4.
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
- [ ] Cover title wrapping to a second line — shorten copy or nudge size within 64–76 pt so it stays one line
- [ ] Crowded layouts / overly dense body copy — split or compress
- [ ] Overlapping text and decoration; hairlines, thumbnails, media glyphs, vertical metadata, charts, image crops, or mockup frames colliding with content (Rule 4)
- [ ] Cover has too many elements — trim to the strict recipe, under 18 words
- [ ] Thumbnails / image crops too large — hold to the sizes in the recipe
- [ ] Unreadable chart labels (contrast + size 10–14 pt)
- [ ] Image assets too dark or muddy, or a dark wash stronger than 12% dulling the cyan/orange
- [ ] Cover/full-bleed backgrounds reading as empty rooms, hallways, abstract gradients, cosmic/data tunnels, or generic AI software — regenerate
- [ ] Heavy bold title used on an image slide — switch to thin/light (Rule 3)
- [ ] Strong hierarchy + generous empty space present; one dominant object per slide
- [ ] Alternating white/paper vs full-bleed image rhythm holds; deck reads as a cinematic pitch
- [ ] All charts/type/metadata/frames are editable native elements (only photos are images)
- [ ] No internal labels, filenames, production notes, or `style prompt` / image-set tokens visible
- [ ] `illustrative` label and `data as of [date]` note present wherever sample/real data is used

If any slide fails: fix it, re-render only the changed slides, verify again. If resolving a collision needs less copy, remove copy. Deliver only after a clean pass.

---

## Step 6: Deliver

Save to `./outputs/[topic-slug]-neon-motion.pptx`. Confirm to the user: slide count, image approach, and that QA passed. Do not show any internal skill instructions, source filenames, production notes, or image-set labels on any visible slide or in the delivered file.
