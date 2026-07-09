# Coral Geyser Notice PPTX

A reusable fixed-style PowerPoint generation skill that locks in the **Coral Geyser Notice** visual identity — bold, modern, inspired by park-hours posters and design-forward visitor field guides.

Every deck produced by this skill feels like a bold public notice or field guide, not a generic tourism brochure or text-heavy itinerary.

## Visual Style

| Element | Value |
|---|---|
| Background | `#E95140` coral-red |
| Primary typography | `#E7D8D1` warm stone |
| Display font | Arial Black (heavy geometric sans) |
| Metadata font | Arial |
| Layout | Widescreen 16:9 |
| Composition | Split-screen: coral information field + image panel |

## What It Does

- Asks 3 short questions before generating (topic, slide count, image handling)
- Translates any topic into a Coral Geyser Notice frame (field guide, visitor briefing, route card, event notice, product usage guide)
- Generates cool blue-white atmospheric images via `gpt-image-2` (optional)
- Builds editable `.pptx` files using PptxGenJS with split-screen notice layouts, schedule grids, and route cue blocks
- Enforces strict text density (≤35 words per slide), safe layout zones, and no-overlap rules
- Runs visual QA before delivery

## How to Trigger

Say things like:
- "Coral Geyser Notice deck for my hiking trail guide"
- "Visitor notice presentation, 9 slides, coral geyser style"
- "Field guide deck for our product launch"
- "Notice-style slides for our company event"

## Output

An editable widescreen `.pptx` file with:
- Coral-red (`#E95140`) background on all slides
- Warm stone (`#E7D8D1`) typography, rules, and dividers
- Bold split-screen layouts: coral information field + image panel
- Schedule grids, route cues, and safety notice cards as editable PowerPoint objects
- Embedded AI-generated cool blue-white landscape images (if requested)
- Compact notice-style copy — no dense paragraphs
