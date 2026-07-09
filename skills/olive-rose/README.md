# Olive Rose Salon PPTX

A reusable fixed-style PowerPoint generation skill that locks in the **Olive Rose Salon** visual identity — high-fashion, poster-led, exhibition-grade.

Every deck produced by this skill feels like a sequence of art exhibition posters, not a report or a generic slide deck.

## Visual Style

| Element | Value |
|---|---|
| Background | `#372E19` dark olive-brown |
| Primary typography | `#FFE1FC` pale pink |
| Secondary typography | `#F5EFE0` warm cream |
| Accents / rules | `#C8A96A` gold |
| Display font | Georgia (serif) |
| Metadata font | Trebuchet MS (sans) |
| Layout | Widescreen 16:9 |

## What It Does

- Asks 3 short questions before generating (topic, slide count, image handling)
- Translates any topic into an Olive Rose Salon exhibition frame
- Generates atmospheric botanical abstract images via `gpt-image-2` (optional)
- Builds editable `.pptx` files using PptxGenJS with poster-hierarchy layouts
- Enforces strict text density (≤25 words per slide), safe layout zones, and no-overlap rules
- Runs visual QA before delivery

## How to Trigger

Say things like:
- "Olive Rose Salon deck for my brand X"
- "Make a poster-style presentation in the olive rose style"
- "Fashion exhibition deck, 8 slides, generate images"

## Output

An editable widescreen `.pptx` file with:
- Dark olive-brown background on every slide
- Pale pink serif headlines
- Poster-style layouts with generous margins
- Embedded AI-generated botanical abstract images (if requested)
- No text-heavy report copy — editorial fragments only
