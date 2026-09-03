# Acid Labels PPTX

A reusable fixed-style PowerPoint generation skill that locks in the **Acid Labels** visual identity — a bold acid-green professional *operating guide*: modular, label-driven, data-native, and confident.

Every deck produced by this skill feels like a bold acid-green operating guide for the user's topic, not a generic report, a copied brand-guidelines deck, or a text-heavy memo. The skill is fully topic-agnostic — no sample topic is ever hardcoded.

## Visual Style

| Element | Value |
|---|---|
| Dominant color | `#A9FF7A` acid green |
| Deep panels | `#3F5E31` forest green |
| Titles / strokes / pills | `#000000` black |
| Light cards / tag chips | `#F7F7F1` white |
| Data blocks | `#8BD4F4` chart sky |
| Analyst notes | `#F1AEC0` pink |
| Risk / warning wedges | `#C90D0D` red |
| Emphasis blocks | `#FFF34D` highlight yellow |
| Display font | Expressive italic serif for `{curly-brace}` title moments |
| Label / chart font | Condensed sans for pills, chips, taxonomy stacks, metadata |
| Layout | Widescreen 16:9, hard-edged modular panels on a strict grid |

## What It Does

- Asks up to 3 short questions before generating (topic, slide count, image handling) and skips any the user already answered
- Translates any topic into an Acid Labels operating guide (playbook, decision system, field system, operating manual)
- Builds editable `.pptx` files with PptxGenJS using black pill labels, tag chips, stacked taxonomy labels, oversized section numbers, forest image plates, KPI tiles, source-note rows, and footer metadata dots
- Renders data as native PowerPoint charts and structures: stacked/grouped bars, line, pie/donut, waterfall, comparison tables, sensitivity heatmaps, probability–impact risk grids, scenario matrices, dashboards, and decision checklists
- Keeps every element — text, panels, section numbers, pills, chips, metadata, rules, tiles, tables, charts, matrices, grids, dashboards — as editable native PowerPoint objects (never HTML, screenshots, or rasterized full slides)
- Optionally generates `gpt-image-2` assets in two clearly separated sets — abstract acid-green *decorative* textures and topic-supporting *theme* images — never with readable text, logos, numbers, real people, or brand marks
- Uses clearly labeled placeholder figures when the user provides no data, and adds a `data as of [date]` note wherever real data is used
- Enforces strong typographic hierarchy, strict grid alignment, no-overlap rules for dividers and decoration, and runs visual QA before delivery

## How to Trigger

Say things like:
- "Acid Labels deck for our product onboarding playbook, 10 slides"
- "Make an acid-green operating guide presentation about our Q3 survey"
- "Playbook slides in the acid labels style, no generated images"
- "Label-system presentation for our launch plan"

## Output

An editable widescreen `.pptx` file with:
- Acid green (`#A9FF7A`) as the dominant brand-system color across the deck
- Deep forest (`#3F5E31`) panels and image plates, black pill labels, white/acid tag chips
- Oversized italic serif `{TOPIC}` cover moment paired with condensed sans labels
- Native charts, KPI tiles, comparison tables, matrices, risk grids, and dashboards adapted to the topic
- Source-note rows with `data as of [date]` wherever real data is used
- Optional `gpt-image-2` decorative textures and theme images (if requested) — decorative or supporting only, never carrying slide content

Built on top of the [`pptx`](../pptx/) skill foundation.
