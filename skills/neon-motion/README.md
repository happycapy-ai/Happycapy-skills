# Neon Motion PPTX

A reusable fixed-style PowerPoint generation skill that locks in the **Neon Motion** visual identity — a premium cinematic pitch built from editorial motion photography and restrained typography: full-bleed motion imagery in electric cyan versus warm orange light, thin geometric sans titles, hairline rules, tiny vertical metadata, and generous empty space.

Every deck produced by this skill feels like a premium cinematic pitch for the user's topic — not a dark SaaS dashboard, an AI report, a cyberpunk poster, a conference deck, a generic startup template, a cluttered product report, or a text-heavy memo. The skill is fully topic-agnostic — no sample topic is ever hardcoded.

## Visual Style

| Element | Value |
|---|---|
| Primary motion light | `#08BFEA` electric cyan |
| Counter motion light | `#FF7317` saturated orange |
| Depth panels / plates | `#07353C` deep petrol |
| Type on light canvases | `#111111` near-black |
| Paper canvas / thin type on images | `#FFFFFF` white |
| Alternate canvas | `#F5F5F3` cool paper gray |
| Display font | Thin/light geometric sans — never heavy bold, never bold on image slides |
| Label / body / chart font | Regular sans, often uppercase with letter-spacing |
| Layout | Widescreen 16:9, restrained editorial rhythm with generous empty space |

## What It Does

- Asks up to 3 short questions before generating (topic, slide count, image handling) and skips any the user already answered
- Translates any topic into a cinematic, photography-led pitch sequence (product pitch, brand film, editorial essay, restrained narrative)
- Builds editable `.pptx` files with PptxGenJS using full-bleed motion plates, thin white one-line titles, hairline separators, tiny vertical metadata, sparse typographic agenda lines, mockup frames, metric moments, typographic comparison columns, and sparse timelines
- Follows a strict motion-poster cover recipe: one full-bleed cinematic cyan-vs-orange motion image (dark wash ≤ 12%), one thin white ~64–76 pt title on a single line, a tiny wordmark, far-left vertical metadata, exactly one small 4:3 thumbnail with a media-glyph row, at most one short hairline — all under 18 visible words
- Keeps every element — text, hairline rules, vertical metadata, charts, metric numerals, mockup frames, timelines, comparison columns, thumbnails — as editable native PowerPoint objects; only photographs are inserted as images (never HTML, screenshots, or rasterized full slides)
- Optionally generates `gpt-image-2` assets in two clearly separated sets — cinematic *decorative* motion plates and restrained *theme* support visuals — never with readable text, logos, brand marks, readable faces, dashboards, UI, lasers, glass shards, cosmic scenes, tunnels, or neon grids
- Uses clearly labeled placeholder / illustrative figures when the user provides no data, and adds a `data as of [date]` note wherever real data is used
- Enforces thin restrained typography, strong hierarchy, generous empty space, no-overlap rules for hairlines and decoration, bright cyan/orange imagery, and runs visual QA before delivery

## How to Trigger

Say things like:
- "Neon Motion deck for our night-run program, 10 slides"
- "Make a cinematic pitch deck about our coffee roastery brand"
- "Motion-poster style slides for our dance season, use my reference photos"
- "Premium cyan-and-orange editorial pitch for our launch"

## Output

An editable widescreen `.pptx` file with:
- Electric cyan (`#08BFEA`) versus saturated orange (`#FF7317`) motion light across the deck, on white / cool-paper-gray canvases and full-bleed motion photos
- A premium motion-poster cover under 18 words with one thin white one-line title following the strict composition recipe
- Thin geometric-sans typography, hairline rules, tiny vertical metadata, and generous empty space — one dominant object per slide
- A few native analytical forms adapted to the topic (one line chart, one before/after comparison, one typographic comparison, one timeline) with `illustrative` and `data as of [date]` notes
- Optional `gpt-image-2` cinematic motion plates and theme support visuals (if requested) — decorative or supporting only, never carrying slide content

Built on top of the [`pptx`](../pptx/) skill foundation.
