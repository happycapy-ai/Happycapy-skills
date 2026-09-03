# Gradient Calendar PPTX

A reusable fixed-style PowerPoint generation skill that locks in the **Gradient Calendar** visual identity — a polished, calendar-native productivity system: sparse poster-like covers, strict calendar grids, oversized date numerals, electric-lime schedule blocks, and soft gradient washes.

Every deck produced by this skill feels like a calendar-native productivity system for the user's topic — not a generic SaaS pitch deck, not a cluttered screenshot dump, and not a text-heavy product report. The skill is fully topic-agnostic — no sample topic is ever hardcoded.

## Visual Style

| Element | Value |
|---|---|
| Slide canvas | `#F1F3F7` pale gray |
| Typography / numerals | `#111111` near-black |
| Key schedule / event blocks | `#C8FF00` electric lime |
| Vertical labels / event markers / spine word | `#0B74FF` saturated blue |
| Gradient wash | `#7FE8F1` cyan + `#B7A5FF` lavender |
| Inner panels / cards | `#FFFFFF` white |
| Deep contrast panels | `#1A1D22` charcoal |
| Display font | Heavy-weight sans for oversized numerals and headlines |
| Label / body / chart font | Regular sans, often uppercase with letter-spacing |
| Layout | Widescreen 16:9, strict calendar grid with generous spacing |

## What It Does

- Asks up to 3 short questions before generating (topic, slide count, image handling) and skips any the user already answered
- Translates any topic into a calendar-native system (rollout calendar, planning grid, structured agenda, operating schedule, program calendar)
- Builds editable `.pptx` files with PptxGenJS using calendar grids, oversized date numerals, electric-lime event blocks, saturated-blue vertical side labels, black/white photo panels, soft gradient gutters, timeline/roadmap strips, mockup frames, and clean stat cards
- Follows a strict sparse-cover recipe: an agenda-poster cover under 14 words — hero numeral, bold title, tiny subtitle, lower-half gradient wash, bottom-left lime anchor, upper-right ink stripes, and one vertical blue spine word
- Keeps every element — text, calendar grids, date numerals, schedule cards, stat cards, charts, gradient fields, mockup frames, vertical labels — as editable native PowerPoint objects (never HTML, screenshots, or rasterized full slides)
- Optionally generates `gpt-image-2` assets in two clearly separated sets — abstract cyan-lime-lavender *gradient-wash* atmospheres and topic-supporting *theme* images — never with readable text, logos, UI, numbers, real people, or brand marks
- Uses clearly labeled placeholder figures when the user provides no data, and adds a `data as of [date]` note wherever real data is used
- Enforces strong typographic hierarchy, strict grid alignment, no-overlap rules for stripes/gutters/washes and decoration, and runs visual QA before delivery

## How to Trigger

Say things like:
- "Gradient Calendar deck for our season plan, 10 slides"
- "Make a calendar-native productivity deck about our annual roadmap"
- "Agenda-poster style slides for our launch schedule, no generated images"
- "Planner slides in the gradient calendar style"

## Output

An editable widescreen `.pptx` file with:
- Pale gray (`#F1F3F7`) canvas and a calendar-native feel across the deck
- Oversized near-black date numerals, electric-lime (`#C8FF00`) schedule blocks, saturated-blue (`#0B74FF`) vertical labels, and soft cyan-lime-lavender gradient washes
- A sparse agenda-poster cover under 14 words following the strict composition recipe
- Native calendar grids, timeline strips, planning grids, comparison cards, and clean stat cards adapted to the topic
- A `data as of [date]` note wherever real data is used
- Optional `gpt-image-2` gradient-wash atmospheres and theme images (if requested) — decorative or supporting only, never carrying slide content

Built on top of the [`pptx`](../pptx/) skill foundation.
