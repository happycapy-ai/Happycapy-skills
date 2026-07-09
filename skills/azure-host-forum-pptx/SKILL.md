---
name: azure-host
description: "Reusable fixed-style PPTX generation skill for the Azure Host Forum visual brand — sky-blue background (#65AEFF), deep green typography (#07461E), olive side-panel accent (#728E03), cream portrait/detail color (#F1F0EA), bold contemporary industry sharing event aesthetic, oversized condensed grotesk titles, strong left-text / right-speaker-column composition, circular portrait frames, widescreen 16:9 editable .pptx output. Use this skill whenever the user mentions Azure Host Forum, asks for a presentation or deck in the Azure Host Forum style, wants a forum or industry-sharing deck, speaker event deck, expert talk slides, panel presentation, creative industry event deck, founder briefing slides, or any event/forum-style PowerPoint. Also trigger when the user says 'azure host forum', 'forum deck', 'speaker event slides', 'industry sharing presentation', 'host forum pptx', 'panel deck', 'workshop deck', or 'creative industry event slides' in any context."
---

# Azure Host Forum PPTX Skill

A reusable fixed-style PowerPoint generation skill. It builds on the `pptx` skill's technical capabilities while locking in the Azure Host Forum visual identity: bold, contemporary, design-forward, inspired by industry sharing events, speaker forums, and editorial event posters.

**Core principle — style wins over content volume.** When the user's topic contains more information than the format can hold, compress and reinterpret. The deck must feel like a bold contemporary industry forum and speaker event — not a generic webinar deck, not a text-heavy conference agenda, not a business report. Every slide is a bold event panel or editorial speaker card.

---

## Step 1: Gather Inputs (Ask First — Max 3 Questions)

Do **not** start generating immediately. Use the `AskUserQuestion` tool to present all questions in a **single** call. Only ask about what the user hasn't already provided.

**Question 1 — Topic** (skip if already provided):
- header: "Topic"
- question: "What is the presentation topic, event title, forum subject, session theme, project, or brand/product name?"
- options: 2–3 relevant examples plus allow Other

**Question 2 — Slide count** (skip if already specified):
- header: "Slides"
- question: "How many slides should the deck include? (Default is 8 if unsure)"
- options: `6 slides`, `8 slides (Recommended)`, `10 slides`, `12 slides`

**Question 3 — Images**:
- header: "Images"
- question: "How should speaker images be handled?"
- options:
  - `Use uploaded speaker images` — Insert portraits I upload
  - `Generate speaker portraits with gpt-image-2` — AI creates clean editorial headshots
  - `Combine uploaded images and gpt-image-2` — Mix uploaded and AI-generated

If the user hasn't provided host names, speaker names, session details, date, time, location, agenda items, or registration details, **infer reasonable content from the topic or use neutral placeholder copy**. Do not keep asking — only follow up if missing info makes it literally impossible to build the deck.

Once you have the three answers, proceed directly to generation.

---

## Step 2: Topic Translation — Everything Becomes a Forum or Speaker Event

Before writing any slide copy, translate the user's topic into an Azure Host Forum frame. No topic is too technical, too abstract, or too far from UI design or industry sharing to work. Every subject can be reframed as a bold hosted forum, expert talk, live session, design-forward panel, product conversation, founder briefing, workshop, or creative industry event — while preserving the user's actual subject.

| User provides | Azure Host Forum treatment |
|---|---|
| UI/UX or design topic | Industry sharing session — hosts, guests, live critique, portfolio review |
| Tech product or platform | Founder briefing or product forum — live demo, expert Q&A |
| Business or strategy topic | Executive panel or expert roundtable |
| Scientific or research topic | Knowledge forum — expert talk, live discussion |
| Creative or cultural topic | Creative industry exchange — guest portfolio, live session |
| Any other subject | Reframe as a bold hosted live session, expert forum, or workshop event |

Decide the **event title**, the **one-line session premise**, and the **format/location label** before writing any slides. These anchor the cover and the visual language of the whole deck.

---

## Step 3: Generate Images (if requested)

Read the `generate-image` skill at `/home/node/.claude/skills/generate-image/SKILL.md` for the exact API call pattern. Use `openai/gpt-image-2` with `response_format: "b64_json"`.

### Cover portrait rule

The cover slide must include **exactly two speaker/host headshot images** placed in the right olive column, stacked vertically in large circular or softly rounded frames. If the user chose gpt-image-2 or mixed mode and has not uploaded enough portraits, generate two portraits for the cover. Generate additional portraits for individual speaker profile slides as needed.

### How many images to generate

- 8-slide deck → 2–3 portraits (cover pair + 1 speaker slide)
- 10–12 slide deck → 3–4 portraits
- 6 slides → 2 portraits minimum (cover pair)

### Azure Host Forum portrait prompt formula

Generated portraits are clean editorial headshots — they are supporting image assets, never full-slide screenshots and never images with embedded text.

```
Clean head-and-shoulders editorial portrait, professional and friendly, white or cream (#F1F0EA) background, soft even studio lighting. [Descriptor: mid-30s person / young professional / senior creative / diverse ethnicity — choose varied diversity across portraits]. No readable text, no logos, no props, no busy environment, no recognizable real person. Suitable for an industry event or speaker forum. High-resolution, editorial photography style.
```

Save each generated portrait to `/tmp/azure-forum-portrait-N.png`.

---

## Step 4: Build the PPTX

Read the `pptx` skill at `/home/node/.claude/skills/pptx/SKILL.md` and its `pptxgenjs.md` reference for the full API. Build using PptxGenJS.

### Core style constants — do not deviate

```javascript
const SKY    = "65AEFF";   // dominant background — all sky-blue fields
const GREEN  = "07461E";   // primary typography — titles, headlines, body
const OLIVE  = "728E03";   // side panel, accent panel, structural anchors
const CREAM  = "F1F0EA";   // portrait frames, detail areas, metadata blocks
const LTBLUE = "7BBFFF";   // subtle organic texture color (slightly lighter than SKY)
const SANS   = "Arial Black"; // oversized condensed titles (heavy grotesk)
const META   = "Arial";    // compact metadata, labels, agenda rows, captions
```

If Arial Black is unavailable, substitute `Impact` or `Trebuchet MS Bold`.

### Layout — LAYOUT_16x9 always (10" × 5.625")

All slides use LAYOUT_16x9. Background is SKY on every slide. The olive panel is a structural vertical band on the right side of speaker slides. Cream areas are used for portrait frames and metadata blocks only — never as a full-slide background.

### Typography sizing

| Role | Font | Size | Color |
|------|------|------|-------|
| Cover hero title | SANS | 72–110pt | GREEN |
| Slide headline | SANS | 40–64pt | GREEN |
| Sub-headline / session premise | META | 24–30pt | GREEN |
| Body / session cue / agenda row | META | 22–28pt | GREEN |
| Speaker name / host label | META uppercase | 16–20pt | CREAM or GREEN |
| Small metadata / location / date | META uppercase | 12–16pt | CREAM or GREEN |

---

## Forum Visual System Rules — These Override Everything

The most common failure mode is a text-heavy report placed on a sky-blue background. These rules prevent that.

### Rule 1: Style wins over content volume

When the topic has more information than the forum format can hold, compress it. Do not add more slides, do not shrink fonts, do not write smaller. Summarise with bold event-language. Pick one idea per slide and discard the rest for that slide. The Azure Host Forum aesthetic takes priority over completeness.

### Rule 2: One idea per slide. Under 35 words.

Count visible words before finalising each slide. Most slides must be under 35 words total — title, body, labels, agenda rows, and metadata combined. Body copy should be one short sentence, a compact speaker note, a short session cue, or a concise agenda row. No paragraphs.

**Wrong:** "This session will explore the fundamental challenges of designing user interfaces for high-stakes enterprise software environments where errors can have serious consequences for end users and organizational outcomes."

**Right:**
```
DESIGNING UNDER PRESSURE
When UI mistakes have real stakes.
Host: [Name] · Guest: [Name]
```

### Rule 3: Left text field + right speaker column is the default layout

The Azure Host Forum style is defined by the split composition: a large sky-blue text field on the left, a strong olive vertical panel on the right containing portrait frames, speaker names, and compact metadata. Use this layout as the default for speaker-led slides. The split does not have to be 50/50 — 60/40 or 65/35 works — but the two zones must be clearly separated and non-overlapping.

### Rule 4: One dominant title, everything else recedes

Every slide has one typographic dominant. Supporting text must be noticeably smaller. Agenda rows, session metadata, and lower-third captions must feel compact and secondary. The hierarchy must be obvious at a glance.

### Rule 5: Write in event language, not report language

Body copy should feel like an event poster, speaker card, or live session notice — short, high-impact, editorial.

Preferred patterns:
- "Live critique. Real work. Honest feedback."
- "Session 1 · Intro · 7:00 PM"
- "Format: Live discussion + open Q&A"
- "Register at [url] before [date]"

Avoid: "This section will cover the important aspects of...", "The following information provides an overview of..."

### Rule 6: Safe layout zones — no collisions

Before placing elements on every slide, define these non-overlapping zones and respect them absolutely:

```
TITLE ZONE:         sky-blue left field, y: 0.7"–2.4"
BODY/SESSION ZONE:  below title, at least 0.35" gap from title bottom edge
PORTRAIT ZONE:      olive right column (x: 6.5"–9.8"), two stacked frames
SPEAKER NAME ZONE:  below or alongside portrait frames, in CREAM metadata block
AGENDA/GRID ZONE:   defined grid block, clear top/bottom padding
METADATA ZONE:      y: 4.8"–5.4" bottom strip, or top corner tag
DIVIDER ZONE:       only above title (y < 0.65") or below body (y > 3.9") — never through text
TEXTURE ZONE:       background only — organic line shapes in LTBLUE, never over text
```

No element may cross through or touch another zone's content. Before `pres.writeFile()`, verify each slide:
- No LINE or rule passes through any text box
- No portrait frame edge clips into a text area
- No agenda row overlaps title or body copy
- No metadata label collides with body text
- No organic texture line crosses any readable element

**Conflict resolution order:** reduce copy first → simplify agenda → remove decorative rule or texture → simplify layout. Never shrink the title to make room for more words.

### Rule 7: Portrait frames are circular or softly rounded — always

Portrait images must be placed with `rounding: true` (PptxGenJS circles) or inside a softly rounded container shape. Never place raw rectangular portrait images. Frame diameter: 1.6"–2.2" for the cover column, 1.4"–1.8" for inner slides.

For uploaded images: place with `rounding: true`.
For generated images: place with `rounding: true`.

The olive right panel background rectangle sits behind the portrait frames and labels. The portrait frames sit on top of it with cream `fill` circle shapes beneath them if a background circle is needed for contrast.

### Rule 8: Organic line textures are background decoration only

Subtle organic line shapes in LTBLUE (`7BBFFF`) may be placed as background texture on the sky-blue field — thin elongated oval shapes, curved lines, or abstract organic forms. They must be behind all text boxes, set to transparency 60–75%, and must not cross, touch, or visually compete with any text, portrait, panel, or metadata element.

---

## Suggested Slide Structure

Use this when the user provides no outline. Adapt freely when they do.

| # | Slide type | Words target | Layout |
|---|---|---|---|
| 1 | Cover — two speaker portraits | ≤ 20 | Left title field + right olive portrait column |
| 2 | Session premise / forum theme | ≤ 25 | Full sky-blue, bold premise statement |
| 3 | Host or speaker 1 profile | ≤ 30 | Left bio field + right portrait column |
| 4 | Guest or speaker 2 profile | ≤ 30 | Left bio field + right portrait column |
| 5 | Agenda or session flow | ≤ 35 | Full sky-blue, compact agenda grid |
| 6 | Core themes / discussion pillars | ≤ 35 | Split sky/olive, compact label rows |
| 7 | Live format / Q&A / participation card | ≤ 25 | Full sky-blue, bold format notice |
| 8 | Registration / closing / event poster | ≤ 20 | Cover-style layout, closing message |

---

## Layout Patterns

### Cover (left text field + right olive portrait column)
```
Background: SKY full slide

Left field (x:0.4"–6.0"):
  Event category tag, 12pt META uppercase, GREEN, y: 0.5"
  Large gap
  Hero event title (stacked), 72–100pt SANS, GREEN, y: 1.1"–2.8"
  Session tagline, 22pt META, GREEN
  Date / time / format metadata, 13pt META uppercase, CREAM block near bottom

Right olive column (x:6.5"–9.8", y:0, w:3.3", h:5.625"):
  OLIVE background rectangle
  Portrait 1 (rounding:true), ~1.9" diameter, centered in column, y: 0.5"
  CREAM circle shape behind portrait 1 (subtle frame ring)
  Portrait 2 (rounding:true), ~1.9" diameter, centered in column, y: 2.8"
  CREAM circle shape behind portrait 2
  Speaker name labels (compact META uppercase, 14pt, CREAM), below each portrait
```

### Speaker profile slide (left bio + right portrait column)
```
Background: SKY full slide

Left field (x:0.4"–6.2"):
  Role/host tag, 12pt META uppercase, GREEN, y: 0.5"
  Speaker name, 44–56pt SANS, GREEN, y: 1.0"
  One-line bio / session cue, 22pt META, GREEN
  Optional: 2–3 compact credential tags, 15pt META, GREEN, y: 3.5"+

Right olive column (x:6.5"–9.8"):
  OLIVE background rectangle
  Portrait (rounding:true), ~2.0" diameter, centered at y: 1.2"
  CREAM circle behind portrait
  Compact metadata block (CREAM rect): name, title, social handle
```

### Session premise / full sky-blue slide
```
Background: SKY full slide
Optional organic texture lines: LTBLUE, transparency: 65%, background layer only

Section tag, 12pt META uppercase, GREEN, y: 0.5", x: 0.6"
Headline / premise statement, 52–64pt SANS, GREEN, y: 1.4"
Optional short supporting line, 22pt META, GREEN, at least 0.4" below headline
Optional thin OLIVE rule (LINE), w: 3.5", placed below body with 0.4"+ gap from any text
Bottom metadata if needed: 13pt META, GREEN or CREAM, y: ~5.0"
```

### Agenda / session flow slide
```
Background: SKY full slide

Headline, 44pt SANS, GREEN, top
Grid of rows (2 columns): LEFT = time/session label (GREEN, 15pt bold), RIGHT = descriptor (GREEN, 15pt normal)
Row height: ~0.42", evenly spaced
No bullets. Clear left margin x: 0.6", column break at x: 3.5"
Thin OLIVE line between headline and rows (if space allows, with 0.4"+ gap)
Bottom tag: format / location, 13pt META, y: ~5.0"
```

### Closing / registration slide
```
Similar to Cover but without portraits or with a single centered portrait
Dominant closing headline, 64–80pt SANS, GREEN
Registration CTA or URL, 18pt META, GREEN
Date / format / host credit, 13pt META uppercase, CREAM block, lower area
```

---

## PptxGenJS Critical Reminders

- Never `#` in hex: `"65AEFF"` not `"#65AEFF"`
- Never 8-char hex for opacity — use `opacity:` property separately
- Fresh option objects per shape — PptxGenJS mutates in place
- `margin: 0` on text boxes aligned to shapes or panel edges
- `charSpacing: 3–6` on uppercase META labels for forum notice feel
- `rounding: true` on ALL portrait images — never raw rectangles
- LINE shapes: always verify `y` coordinate does not intersect any text box `y` range
- Olive column rectangles: set `x` to the split boundary exactly; never overlap the sky-blue text field
- Portrait `rounding: true` produces a circle crop in PptxGenJS — use square dimensions (equal `w` and `h`)

---

## Step 5: Visual QA — Required Before Delivery

```bash
python -m markitdown output.pptx
python /home/node/.claude/skills/pptx/scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

Use a subagent for visual inspection — you have been staring at the code and will miss obvious issues. Pass this prompt to the subagent:

```
Visually inspect these Azure Host Forum slides. Assume there are issues — find them.

Look for:
- Any rule, line, panel edge, or portrait frame overlapping or touching title text, body text, speaker names, labels, or metadata
- Text overflow or cut off at box boundaries or slide edges
- Portrait images that are rectangular instead of circular
- Olive right column not cleanly separated from the sky-blue text field
- Agenda rows or metadata blocks colliding with titles
- Organic texture lines crossing over readable text
- Slides with more than 35 words total
- Slides lacking a clear dominant headline
- Low-contrast text (e.g., cream text on light backgrounds)
- Any slide that still reads like a generic report or webinar deck rather than a bold forum event

For each slide, list issues. Report ALL issues, including minor ones.

Images:
1. /path/to/slide-01.jpg (Cover with portrait column)
2. /path/to/slide-02.jpg ...
```

### Forum QA checklist — check every slide

- [ ] Under 35 words on most slides (count them)
- [ ] No rule, line, divider, or panel edge passes through or touches any text
- [ ] No portrait frame edge collides with a text area
- [ ] No agenda row or metadata block overlaps title or body
- [ ] Title/headline is clearly the dominant element
- [ ] Body is compact — event language, not paragraphs
- [ ] Speaker-led slides: text on sky-blue left field, portraits in olive right column
- [ ] Portrait images are circular (rounding:true), not rectangular
- [ ] Cover has exactly two portrait frames stacked in the right olive column
- [ ] Sky-blue (#65AEFF) on all background fields
- [ ] Deep green (#07461E) on all primary text
- [ ] Olive (#728E03) on all structural panel backgrounds
- [ ] Cream (#F1F0EA) on portrait frame backing, metadata blocks, and speaker labels
- [ ] Deck reads as a bold contemporary industry forum, not a generic presentation

If any slide fails: fix, re-render, verify. If fixing requires removing copy, remove the copy. Deliver only after a clean pass.

---

## Step 6: Deliver

Save to `./outputs/[topic-slug].pptx`. Confirm: slide count, image approach, QA passed.

Do **not** show internal labels — no skill instructions, no source filenames, no implementation notes, no QA checklist text — on any visible slide.
