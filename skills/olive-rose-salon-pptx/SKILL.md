---
name: olive-rose
description: "Reusable fixed-style PPTX generation skill for the Olive Rose Salon visual brand — dark olive-brown background (#372E19), pale pink typography (#FFE1FC), high-fashion art exhibition poster aesthetic, large serif title type, widescreen 16:9 editable .pptx output. Use this skill whenever the user mentions Olive Rose Salon, asks for a presentation or deck in the Olive Rose style, wants an exhibition poster deck, needs a high-fashion poster-led PowerPoint, or mentions the olive-brown/pale-pink color scheme for slides. Also trigger when the user says 'olive rose', 'salon deck', 'poster presentation', or 'fashion deck' in any context."
---

# Olive Rose Salon PPTX Skill

A reusable fixed-style PowerPoint generation skill. It builds on the `pptx` skill's technical capabilities while locking in the Olive Rose Salon visual identity: high-fashion, poster-led, exhibition-grade.

**Core principle — style wins over content volume.** When the user's topic contains more information than the poster format can hold, compress and reinterpret. Do not expand the deck into dense explanations. The user's subject is preserved, but expressed through sparse, editorial, exhibition-like language. Every deck must feel like a sequence of art exhibition posters — not a report, not an explainer, not a generic slide deck. The topic is the subject of an exhibition. The slides are the posters.

---

## Step 1: Gather Inputs (Ask First — Max 3 Questions)

Do **not** start generating immediately. Use the `AskUserQuestion` tool to present interactive questions. Ask all missing questions in a **single** `AskUserQuestion` call (up to 3 questions at once).

Only ask questions the user hasn't already answered in their prompt. If the topic is already clear from their message, skip question 1 and only ask what's still missing.

**Question 1 — Topic** (skip if already provided):
- header: "Topic"
- question: "What is the presentation topic, exhibition title, project title, or brand/product name?"
- options: provide 2–3 example options relevant to context, plus allow Other

**Question 2 — Slide count** (skip if already specified):
- header: "Slides"
- question: "How many slides should the deck include?"
- options: `6 slides`, `8 slides (Recommended)`, `10 slides`, `12 slides`

**Question 3 — Images**:
- header: "Images"
- question: "How should images be handled?"
- options:
  - `Generate with AI` — I'll create botanical abstract illustrations using gpt-image-2
  - `Use my uploaded images` — Insert images I provide
  - `Combine both` — Mix uploaded and AI-generated images

If the user hasn't provided audience, date, venue, speakers, or other details, **infer or use neutral placeholder copy** — do not keep asking. Only follow up if the missing info makes it literally impossible to build the deck.

Once you have the three core answers, proceed directly to generation.

---

## Step 2: Topic Translation — Everything Becomes an Exhibition

Before writing any slide copy, translate the user's topic into an Olive Rose Salon frame. No topic is too technical, strange, or non-botanical. Every subject can be reframed as an atmospheric poster sequence, cultural exhibition, brand mood story, or poetic concept deck — while preserving the user's actual subject.

| User provides | Olive Rose treatment |
|---|---|
| Fragrance brand | Exhibition of scent, memory, and form |
| Tech product launch | A collection. An object. A ritual. |
| The Backrooms | A mysterious cultural exhibition — liminal space as architecture |
| Scientific concept | An atmospheric visual essay |
| Corporate pitch | A manifesto sequence |
| Historical topic | An archival mood installation |
| Any other subject | Atmospheric poster sequence — reframe through the lens of feeling, not fact |

**Do not** create a generic educational report, business explainer, or text-heavy slide deck about the topic. Instead, decide: what is the *exhibition title*? What is the *one-line framing statement*? What is the *3–4 word subtitle*? Write these first. They become the cover slide's primary elements and anchor the visual language of the whole deck.

---

## Step 3: Generate Images (if requested)

Read the `generate-image` skill at `/home/node/.claude/skills/generate-image/SKILL.md` for the exact API call pattern. Use `openai/gpt-image-2` with `response_format: "b64_json"`.

### How many images to generate

- 8-slide deck → 3–4 images
- 10–12 slide deck → 4–5 images
- Fewer than 6 slides → 2–3 images

### Image prompt formula — Olive Rose Salon

All generated images must read as atmospheric, non-literal, and Olive Rose in palette. Even for dark or strange topics, reinterpret through abstract blurred forms — never literal scenes, never people, never readable text.

Base formula:
```
Soft motion-blurred botanical forms, painterly abstract foliage, deep olive green, moss, muted amber, shadow green, very faint pale pink highlights. Long-exposure photography style, atmospheric blurred garden movement, painterly flowers dissolving into color. No text, no logos, no people. Dark olive-brown dominant tone, 16:9 landscape composition.
```

For darker topics (e.g., liminal space, industrial, dystopian), adapt the mood while keeping the Olive Rose palette:
```
Abstract blurred forms suggesting [mood word — shadows, corridors, silence, depth], deep olive and moss tones, motion blur, painterly dissolution. No readable text, no logos, no people. Dark olive-brown dominant. 16:9.
```

Save each image to `/tmp/olive-rose-img-N.png`.

---

## Step 4: Build the PPTX

Read the `pptx` skill at `/home/node/.claude/skills/pptx/SKILL.md` and its `pptxgenjs.md` reference for the full API. Build using PptxGenJS.

### Core style constants — do not deviate

```javascript
const BG    = "372E19";        // all slide backgrounds
const PINK  = "FFE1FC";        // primary type — titles, headlines
const CREAM = "F5EFE0";        // secondary — body, taglines
const GOLD  = "C8A96A";        // rules, dividers, labels, metadata
const SERIF = "Georgia";       // all poster/display type
const SANS  = "Trebuchet MS";  // all small metadata and labels
```

### Typography sizing

| Role | Font | Size | Color |
|------|------|------|-------|
| Hero title (cover) | SERIF | 80–100pt | PINK |
| Slide headline | SERIF | 44–60pt | PINK |
| Sub-headline / tagline | SERIF italic | 26–34pt | CREAM |
| Short body fragment | SANS | 18–22pt | CREAM |
| Metadata / labels | SANS | 12–14pt | GOLD |
| Decorative ghost word | SERIF | 90–120pt, 15–20% opacity | PINK |

### Layout — LAYOUT_16x9 always (10" × 5.625")

---

## Poster System Rules — These Override Everything

The most common failure mode is a text-heavy report placed on a dark background. These rules prevent that. When any rule conflicts with fitting more content onto a slide, the rule wins — compress the content instead.

### Rule 1: Style wins over content volume

When the topic has more information than the poster format can hold, compress it. Do not add more slides, do not shrink the font, do not write smaller. Summarise poetically. Pick the single most important idea per slide and discard the rest. The Olive Rose Salon aesthetic takes priority over completeness of information.

### Rule 2: One idea per slide. Under 25 words.

Count the visible words before finalising each slide. Most slides must be under 25 words total — title, body, labels, and metadata combined. If you find yourself writing a second sentence to explain the first, delete the second sentence and make the first more precise.

**Wrong:** "The Backrooms is an internet phenomenon originating from a 2019 4chan post, describing a liminal space of infinite yellow rooms with buzzing fluorescent lights and damp carpet."

**Right:**
```
THE BACKROOMS
An internet myth becomes architecture.
```

### Rule 3: One dominant title, everything else recedes

Every slide has exactly one typographic dominant: the title. It must be large, elegant, and visually primary. Supporting text must be noticeably smaller. Metadata — date, venue, section label — must stay small and peripheral, never competing with the title. The hierarchy must be obvious at a glance.

### Rule 4: Write in editorial fragments, not explanatory sentences

Body copy should feel like art wall text, not a report. Prefer poetic compression:

- "Familiar rooms, made unstable."
- "Thresholds, loops, fluorescent memory."
- "A ritual of light and wax."
- "Sourced. Slow. Intentional."

Avoid: "This slide covers...", "The following section explains...", "X is a Y that does Z."

Only use full explanatory sentences if the user has explicitly asked for a text-heavy informational deck.

### Rule 5: Safe layout zones — no collisions

Before placing elements on each slide, define five non-overlapping zones:

```
TITLE ZONE:      y: 1.2"–2.8" (centered poster composition)
BODY ZONE:       below title, at least 0.4" gap from title bottom
IMAGE ZONE:      defined rectangle or full-bleed — text must not enter it
METADATA ZONE:   y: 4.8"–5.3" bottom strip, or top-left corner label
DIVIDER ZONE:    above title (y < 1.0") OR below body (y > 3.5") — never through text
```

No element may cross through or touch another zone's content. Before calling `pres.writeFile()`, verify every slide:
- No LINE or rule shape passes through any text box
- No image edge clips into a text area
- No metadata label overlaps body copy or title
- No decorative ghost word sits at the same y-coordinates as real title text

**When space is tight, resolve conflicts in this order:** reduce copy first → remove the divider → simplify the layout. Never shrink the title to make room for more words.

### Rule 6: Images are atmospheric assets, not slide backgrounds

Generated images must be abstract, non-literal, and palette-aligned. They set mood — they are not illustrations of the topic and must not contain readable text, logos, or people. Always use the Olive Rose image prompt formula (see Step 3). For non-botanical topics, reinterpret the mood through abstract blurred forms rather than literal scenes.

**Full-bleed image slides:** Maximum 10–12 words. Text in a calm, low-detail area (lower third preferred). If readability is uncertain, add a semi-transparent overlay rect (`fill: { color: "372E19", transparency: 40 }`) behind the text.

**Image window slides:** All text stays on the solid `BG`-colored area. Text never enters the image rectangle.

Never place a dense paragraph over a full-bleed image.

---

## Suggested Slide Structure

Use this when the user provides no outline. Adapt freely when they do.

| # | Slide type | Words target | Notes |
|---|---|---|---|
| 1 | Poster cover | ≤ 12 | Exhibition title + 3-word subtitle + small metadata |
| 2 | Framing statement | ≤ 18 | One positioning line + 1–2 fragments |
| 3 | Mood / image plate | ≤ 8 | Full-bleed or large window image, minimal overlay |
| 4 | Key statement | ≤ 15 | One bold headline, 1–2 fragments |
| 5 | Second image plate | ≤ 8 | Second image, short title overlay |
| 6 | Detail / context card | ≤ 25 | Date, venue, offer, or collection descriptor |
| 7 | Program / sequence | ≤ 25 | 3–5 items, names only — no descriptions |
| 8 | Closing poster | ≤ 12 | Invitation line + brand name reprise |

---

## Layout Patterns

### Poster cover
```
Background: BG (solid)
Decorative ghost word, centered, 100pt, 18% opacity, PINK   ← behind title, not overlapping
Main title, centered, 80–90pt SERIF, PINK
  gap: at least 0.3"
Tagline, 26pt SERIF italic, CREAM
  gap: at least 0.4"
Thin horizontal rule: LINE shape, GOLD, w: 5", y: well below tagline
  gap: at least 0.25"
Metadata, 13pt SANS, GOLD, centered
```

### Statement slide (no image)
```
Background: BG
Section label, 12pt SANS uppercase, GOLD, y: 0.5" (top area)
  large gap
Headline, centered, 50–60pt SERIF, PINK, y: 1.4"–2.0"
  gap: at least 0.5"
1–2 short fragments, 20pt SANS, CREAM
  (optional) thin rule BELOW this block, y > 3.8"
```

### Image window slide
```
Background: BG
Image rect (x: 0.6, y: 0.8, w: 5.0, h: 3.8) — left or right
Text block on opposite side:
  Section label, 12pt GOLD
  Headline, 40pt SERIF PINK
  1 fragment, 20pt SANS CREAM
Keep all text inside the BG-colored side — never enter the image rect
```

### Full-bleed image plate
```
Image: x:0, y:0, w:10, h:5.625 (full slide)
Optional dark overlay rect if needed for readability
Title: max 8 words, 48–56pt SERIF PINK, placed in calm area (lower third preferred)
No body copy. No rule. No metadata unless essential.
```

### Details / program card
```
Background: BG
Section label, 12pt SANS uppercase, GOLD, top
Items: each item = PINK 24pt name + CREAM 16pt short descriptor (optional)
Even spacing, no bullets, generous left margin (x: 1.2")
Rule only if there is clear space above AND below it — otherwise omit
```

---

## PptxGenJS Critical Reminders

- Never `#` in hex: `"FFE1FC"` not `"#FFE1FC"`
- Never 8-char hex for opacity — use `opacity:` property
- Fresh option objects per shape — PptxGenJS mutates in place
- `margin: 0` on text boxes aligned to shapes
- `charSpacing: 4–8` on uppercase serif titles for poster feel
- LINE shapes: always verify `y` coordinate does not intersect any text box `y` range

---

## Step 5: Visual QA — Required Before Delivery

Convert slides to images and inspect every slide. This is not optional.

```bash
python -m markitdown output.pptx
python /home/node/.claude/skills/pptx/scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

### Poster QA checklist — check every slide

- [ ] Under 25 words on most slides (count them)
- [ ] No rule, line, or divider passes through any text
- [ ] No image edge collides with a text box
- [ ] No metadata or label overlaps body copy or title
- [ ] Title is clearly the dominant typographic element — largest, most prominent element
- [ ] Body text is sparse — fragments only, not paragraphs
- [ ] No full-bleed image slide has a dense paragraph placed over it
- [ ] Dark olive-brown background on every slide
- [ ] Pale pink on all headlines
- [ ] The deck reads as a poster sequence, not a generic topic presentation

If any slide fails: fix it, re-render, verify again. If fixing a layout conflict requires removing copy, remove the copy. Deliver only after a clean pass.

---

## Step 6: Deliver

Save to `./outputs/[topic-slug].pptx`. Confirm to the user: slide count, image approach, and that QA passed.

Do **not** show any internal labels — no skill instructions, no source filenames, no implementation notes — on any visible slide.
