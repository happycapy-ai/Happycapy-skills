---
name: world-class-carousel
description: "Generate world-class Instagram carousel content on any topic. Produces 7-10 publication-ready slides (1080x1350) with AI-generated visuals, precise typography, Instagram music recommendations, optimized captions, and hashtags. Uses Aristotelian first-principles framework with 7 content archetypes, 6 hook patterns, a mandatory Bullshit Test quality gate, and a comprehensive design system. Fully generalized -- works for ANY topic. Triggers: instagram carousel, create carousel, carousel post, make carousel slides, instagram slides, carousel content, slide deck for instagram, swipeable post"
allowed-tools: Bash, Read, Edit, Write, Glob, Grep, WebFetch
---

# World-Class Instagram Carousel Generator

Generate Instagram carousels that are genuinely world-class: content people save, share, and come back to. Not engagement bait. Not AI slop. Actual value, delivered through precise visual design and narrative structure.

This skill is **fully generalized**. It contains FORM (structure, principles, patterns), not MATTER (specific topics). The user provides the matter (topic); the skill provides the form (archetypes, design system, music matrix, quality gates). Together they produce the carousel. Nothing is hardcoded.

---

## BEFORE YOU START: Read `KNOWN_ISSUES.md`

Before generating ANY carousel, read `/home/node/.claude/skills/world-class-carousel/KNOWN_ISSUES.md`. It contains compressed rules from all previous sessions -- data format gotchas, sizing rules, visual strategy decisions, and quality gates. Ignoring it means repeating solved mistakes.

---

## EXECUTION PIPELINE

When the user requests a carousel, execute these 6 phases in order (Phase 6 runs post-delivery):

### PHASE 1: RESEARCH & STRUCTURING

1. **Analyze the topic** -- What is the core insight? What specific value can this deliver?
2. **Identify the audience** -- What does the target audience NOT already know? What's their current understanding?
3. **Auto-detect content vertical and theme** -- Use the Content Vertical Detection table below
4. **Select the archetype** -- Which of the 7 carousel archetypes (see below) fits best? Use the Archetype Selection Guide below. Auto-select unless the user specifies.
5. **Design the narrative arc** -- Map each archetype role to a renderer slide type using the Role-to-SlideType Mapping below. Ensure each slide creates a curiosity gap that the next slide resolves.
6. **Run the Bullshit Test on the outline** -- Does every slide pass? (See QUALITY GATE below)

#### Content Vertical Detection (Topic -> Theme)

Analyze the topic and auto-select the renderer theme:

| Content Vertical | Keywords/Signals | Renderer Theme | Background Style |
|-----------------|-----------------|----------------|-----------------|
| Tech / AI / Coding | AI, code, developer, API, tools, stack, programming, SaaS, data | `dark` | `gradient` (default) |
| Business / Strategy | growth, revenue, startup, founder, marketing, sales, strategy, scale | `earth` | `gradient` |
| Education / How-To | learn, tutorial, guide, roadmap, beginner, master, course, how to | `clean` | `gradient` |
| Creative / Design | design, UX, brand, visual, aesthetic, portfolio, creative | `dark` | `gradient_mesh` |
| Mindset / Philosophy | mindset, habits, productivity, stoic, growth, mental, philosophy | `warm` | `gradient` |

If the user specifies a brand config with a theme, always use that instead.

#### Content Category Selection (10 Categories, Aristotelian)

Each category has unique visual DNA derived from psychology axioms (Cialdini, cognitive load theory, dual coding, serial position effect). Select based on topic:

| If the topic is about... | Category | Arc Shape | Hook Style | Primary Cialdini |
|--------------------------|----------|-----------|------------|------------------|
| Explaining a research paper | `paper_decoder` | Revelatory | Face + paper panel | Authority |
| Comparing AI tools/models | `tool_showdown` | Divergent | Multi-screenshot face-off | Social Proof |
| Today's AI development | `breaking_news` | Convergent | News-editorial face | Scarcity |
| Step-by-step AI tool how-to | `tool_tutorial` | Linear | Phone-in-hand / device mockup | Reciprocity |
| Controversial opinion | `hot_take` | Confrontational | Bold abstract typography | Authority |
| Copy-paste prompts/templates | `prompt_playbook` | Divergent | Phone screenshot mockup | Reciprocity |
| Complete sector overview | `industry_map` | Divergent | Multi-person face-off | Authority |
| Build [X] with AI project | `build_this` | Linear+Reveal | Multi-device result showcase | Social Proof |
| Funding/business news | `founders_money` | Convergent | Founder portrait + data | Scarcity |
| Future predictions/timeline | `future_scenario` | Revelatory | Abstract cinematic AI imagery | Scarcity |

**Universal Psychology Rules (apply to ALL categories):**
- Max 4 information chunks per slide (Cognitive Load Theory, Sweller)
- Pattern interrupt every 2-3 slides (diagram, comparison, color shift, or layout change)
- Density wave: H-M-H-M-H-H-M (never 3 high-density slides consecutively)
- Synthesis slide = THE save trigger (Serial Position Effect: last items remembered best)
- Dual-code the hardest concept (Paivio: visual + text = 6.5x retention)
- CTA matches save trigger: utility categories → "Save this", social categories → "Share/Comment"

**Category-to-Slide-Sequence Quick Reference:**
- `paper_decoder` (9 slides): hook → body → **diagram** → body → body → **diagram** → body → synthesis → cta
- `tool_showdown` (8 slides): hook → body → **comparison** → body → body → **comparison** → synthesis → cta
- `breaking_news` (8 slides): hook → body → body → body → **diagram** → body → synthesis → cta
- `tool_tutorial` (8 slides): hook → body → **tool** → **tool** → **tool** → body → synthesis → cta
- `hot_take` (7 slides): hook → body → body → body → body → synthesis → cta (text-driven, no diagrams)
- `prompt_playbook` (9 slides): hook → body → body → body → **comparison** → body → body → synthesis → cta
- `industry_map` (9 slides): hook → **diagram** → body → body → body → **comparison** → **diagram** → synthesis → cta
- `build_this` (8 slides): hook → body → **tool** → **tool** → **tool** → body → synthesis → cta
- `founders_money` (7 slides): hook → body → body → body → **diagram** → synthesis → cta
- `future_scenario` (8 slides): hook → body → body → **diagram** → body → body → synthesis → cta

#### Role-to-SlideType Mapping

Map each archetype role to a renderer slide type when building the carousel spec:

| Archetype Role | Renderer Slide Type | Notes |
|---------------|-------------------|-------|
| `hook` | `hook` | Use `title` + `title_highlight` for split title effect |
| `intro`, `context`, `reveal`, `before` | `body` | Use `title_highlight` for the key phrase |
| `step`, `component`, `layer`, `shift`, `evidence`, `action` | `body` | Use `bullets` for key points |
| `item` | `body` | Use `title_highlight` for the item name, `bullets` for details |
| `diagram`, `connection` | `diagram` | Use `diagram_nodes` with `vertical` or `horizontal` layout |
| `contrast`, `reframe` | `comparison` | Use `columns` with opposing views |
| `result`, `after`, `lesson`, `implication` | `body` | Use title highlight to emphasize the key outcome |
| `synthesis` | `synthesis` | Use `points[]` for numbered key takeaways |
| `cta` | `cta` | Use `handle`, `cta_text`, optional `stats[]` |
| `bonus`, `pitfalls`, `prediction` | `body` | Use bullets for listed points |

### PHASE 1.5: VISUAL STRATEGY DECISION (Before Writing Content)

Before writing any content, decide the **visual strategy** for this carousel. You have access to multiple tools -- choose the right ones for the topic.

#### Available Visual Tools Inventory

| Tool | What It Does | When to Use | How to Invoke |
|------|-------------|-------------|---------------|
| **AI Cinematic Images** | HD photorealistic/artistic images (Gemini 3 Pro) | Hook/CTA backgrounds, emotional priming, conceptual anchoring | `generate-image` skill with hyper-detailed prompt (50+ words) |
| **AI Flowcharts/Diagrams** | Production-quality flowcharts with text labels, arrows, boxes | Process flows, pipelines, decision trees -- REPLACES TikZ for better visuals | `generate-image` skill with structural prompt describing boxes + connections |
| **AI Architecture Diagrams** | Blueprint-style system diagrams with components and connections | Microservices, tech stacks, system design | `generate-image` skill with component/connection prompt |
| **AI Infographics/Charts** | Bar charts, data visualizations with accurate labels and proportions | Market data, statistics, comparisons | `generate-image` skill with data + style description |
| **AI Abstract Backgrounds** | Neural networks, geometric patterns, cosmic visuals | Slide backgrounds via `ai_bg` | `generate-image` skill with atmosphere/material prompt |
| **TikZ Diagrams** | Vector flowcharts in LaTeX (basic but reliable) | Simple 3-5 node flows where AI image gen is overkill | Use `diagram` slide type with `diagram_nodes` |
| **Gradient Backgrounds** | TikZ-rendered gradient fills with geometric accents | Default for all text-only slides | Set `bg_style: "gradient"` in slide data |

#### CRITICAL: Slide-Type Visual Rule (Experimentally Verified)

This rule was established through controlled A/B experiments (7 strategies, same content, scored 1-10). It overrides gut instinct:

| Slide Type | Visual Strategy | WHY (Experimental Evidence) |
|-----------|----------------|---------------------------|
| **Hook** | `ai_bg` full-bleed + 0.60-0.68 overlay | Scroll-stopping power. First slide = 80% of engagement. Score: 8.0/10 |
| **Body** | **TEXT-ONLY. No images.** | Images on body slides destroy 40% of content space. Text-only scored 8.3/10 vs 5.7/10 with images |
| **Diagram** | **AI-generated diagram as `ai_bg`** (preferred) OR TikZ fallback | Gemini 3 Pro generates production-quality flowcharts with readable labels, arrows, and boxes. Far more visually striking than basic TikZ. Use `ai_bg` + 0.55-0.65 overlay so text remains readable over the diagram. |
| **Synthesis** | Text-only | Save-worthy reference material. Images would reduce information density. |
| **CTA** | `ai_bg` full-bleed + 0.65-0.70 overlay | Emotional close with visual punch. |

**DO NOT** put AI images on body slides. This was the single biggest quality mistake found in testing.
**DO NOT** use browser screenshots on any slides. They always look terrible embedded in carousel slides.

#### Visual Strategy Decision Matrix (Topic-Level)

For each topic, determine the primary visual mode, background style, and which slide-level visuals to use:

| Topic Type | Background Style | Hook Visual | Body Visuals | Diagram Strategy | Example |
|-----------|-----------------|-------------|-------------|-----------------|---------|
| **Philosophy / Mindset** | `gradient` | AI image: symbolic figure | None (text carries weight) | AI-generated concept map | Stoic principles: marble bust + storm |
| **Tool Review / SaaS** | `gradient` or `gradient_mesh` | AI image: abstract tech glow | None (text-only bullets describe tools) | AI-generated comparison chart | "6 AI Tools": text descriptions + AI chart |
| **News / Current Events** | `gradient` | AI image: dramatic scene | None (text with citations) | AI-generated timeline or power map | "AI War 2025": cinematic + AI power map |
| **Technical Tutorial** | `gradient` (clean) | AI image: conceptual diagram | None (step-by-step text) | AI-generated architecture/flowchart | "Deploy with Docker": AI architecture diagram |
| **Business / Strategy** | `gradient` | AI image: bold abstract | None (text with real data citations) | AI-generated bar chart or funnel | "Growth Hacking": AI infographic |
| **Comparison / Versus** | `gradient_mesh` | AI image: abstract contrast | `comparison` slide type columns | AI-generated side-by-side chart | "React vs Vue": comparison columns + AI chart |
| **Creative / Design** | `gradient_mesh` (dark) | AI image: artistic/gallery quality | None (text-only) | AI-generated process flow | "UX Trends 2025": artistic + AI flow |
| **Framework / Mental Model** | `gradient` | AI image: system metaphor | None (text explains components) | AI-generated flowchart (preferred over TikZ) | "OODA Loop": AI flowchart as `ai_bg` |
| **Data / Research** | `gradient` | AI image: data visualization concept | None (text with specific numbers) | AI-generated bar chart / infographic | "AI Market 2025": AI bar chart |

#### AI Image Generation Best Practices

**Model & Routing**:
- Use `generate-image` skill (uses `AI_GATEWAY_API_KEY`). Nano-banana-pro requires `GEMINI_API_KEY` (often unset) but uses the same underlying model.
- Model: `google/gemini-3-pro-image-preview` (primary). Fallback: `google/gemini-3.1-flash-image-preview`.
- Output: ~1408x768 landscape. Overlay compensates for portrait stretch on slides.

**Gemini 3 Pro Proven Capabilities** (Experimentally Verified):

| Capability | Quality | Best Use in Carousels | Prompt Strategy |
|-----------|---------|----------------------|-----------------|
| **Cinematic portraits** | Excellent | Hook/CTA backgrounds | 50+ words: materials, lighting, composition, colors, atmosphere |
| **Multi-image composition** | Excellent (avg 9.6/10) | Hook slides with real faces + screenshots | Aristotelian axioms below. Send base64 to `/api/v1/images/generations` |
| **Screenshot → device mockup** | Excellent | Tool showcase, product launch slides | "floating laptop/phone mockup, dark studio, reflective surface" |
| **Person + screenshot editorial** | Excellent | News hooks with evidence | "person as SUBJECT, screenshot as floating holographic EVIDENCE panel" |
| **Multi-screenshot dashboard** | Excellent | Comparison/versus slides | "floating panels at varied depths, color-coded edge glows, grid floor" |
| **Flowcharts** | Excellent | Diagram slides as `ai_bg` | Describe boxes, arrows, labels, and connections structurally |
| **Abstract backgrounds** | Excellent | Any slide background | Materials, colors, atmosphere, "no text no words" |

#### The 7 Aristotelian Axioms for Multi-Image Composition (Experimentally Proven)

These irreducible premises govern ALL multi-image prompts. Every prompt must satisfy all 7:

**A1: VISUAL HIERARCHY** -- Eye processes: faces > contrast edges > text > color fields. Composition must respect this order.
**A2: INPUT TYPE DETERMINES ROLE** -- Each input has exactly one role:
- Photo of person → SUBJECT (preserve face, never modify)
- Screenshot/UI → EVIDENCE (float as holographic panel, stylize frame, preserve content)
- Logo/brand → ANCHOR (small, consistent corner placement)
- Abstract/texture → ATMOSPHERE (background only)

**A3: UNIFIED LIGHT SOURCE** -- All elements share one dominant light direction. Mixed lighting = instant "fake" detection.
**A4: DEPTH CREATES DRAMA** -- Foreground sharp (subject), midground recessed (screenshots), background soft (atmosphere). 3 layers minimum.
**A5: NEGATIVE SPACE IS FUNCTIONAL** -- Bottom 30-35% dark for text overlay. Not waste -- it's where the headline goes.
**A6: COLOR TEMPERATURE = STORY** -- Cool blue/teal = innovation. Warm red = urgency. Split red/blue = competition. Mono + accent = editorial.
**A7: NO-TEXT SEAL** -- Always end with "absolutely no text, no words, no letters, no watermarks" (outside screenshots).

#### Proven Scenario Prompt Templates (avg 9.6/10 across 10 tests)

**Person + News Screenshot** (9.5/10): "Image 1 is [person] -- preserve face, place in left 60%, dramatic side lighting. Image 2 is screenshot -- float as glowing translucent panel, tilted 8 degrees, recessed behind subject, cyan edge glow. Dark moody background, cinematic depth of field. Bottom 30% dark. No text outside screenshot."

**Tool Screenshot Showcase** (9/10): "Place screenshot on sleek floating laptop mockup angled 15 degrees. Dark gradient background, ambient teal glow from screen. Glossy reflective surface below. Premium Apple product launch aesthetic. No text outside screenshot."

**Multi-Screenshot Dashboard** (9.5/10): "Arrange as glowing panels floating in dark space, varied depths and angles (5-15 degrees). Largest centered. Color-coded edge glows. Grid floor, particle effects. Digital command center aesthetic. No text outside screenshots."

**Person + Screenshots + Logo** (10/10): "Person as dominant subject center-left, face preserved. Screenshots as holographic panels around them. Logo small in upper corner with glow. Volumetric light rays, 3-layer depth. No text outside screenshots/logo."

**Face-Off + Data** (10/10): "Person A on LEFT in profile facing right, red lighting. Person B on RIGHT facing left, blue lighting. Dashboard between them as floating holographic display. Smoke and sparks in the gap. Competitive energy. No text outside screenshot."

**Phone in Hand** (10/10): "Screenshot on smartphone held in hand from lower-right. Dark background, soft bokeh lights. Screen bright and crisp. Lifestyle photography style. No text outside screenshot."

**5-Image Mega** (10/10): "2 people (main foreground, secondary recessed) + 2 screenshots (holographic panels, color-coded glows) + logo (corner). Volumetric light, split lighting, multiple depth layers. No text outside screenshots/logo."

**Prompt Rules**:
- **HYPER-DETAILED** (50+ words): materials, lighting, composition, colors, atmosphere. Generic = bad.
- **Always end with "absolutely no text, no words, no letters, no watermarks"** -- AI models add unwanted text otherwise.
- **Declare each input's role explicitly** (per A2): "Image 1 is a portrait... Image 2 is a screenshot..."
- **Specify depth map** (per A4): "subject sharp foreground, screenshots floating midground, atmospheric background"
- **Lock light direction** (per A3): "single dominant light from upper-left, rim light on subject"
- For editorial portraits: add "ABSOLUTELY NO TEXT NO LOGOS NO MAGAZINE ELEMENTS" or Gemini creates TIME covers.
- Overlay opacity sweet spot: 0.60-0.68 for hooks, 0.55-0.65 for diagrams, 0.65-0.70 for CTA.

#### Background Style Selection

Set `bg_style` in the carousel spec or per-slide `data` to control the look:

| `bg_style` Value | Visual Result | Best For |
|-----------------|--------------|----------|
| `"gradient"` (default) | Top-to-bottom gradient with subtle accent glow | All themes. Clean, modern, professional |
| `"texture"` | AI-generated paper/fabric texture | AVOID -- produces grey rock look |
| `"gradient_mesh"` | Multi-stop gradient with geometric accent shapes | Creative, premium, high-contrast |
| `"solid"` | Flat theme background color | Clean/education themes, data-heavy content |
| (AI background) | Full-bleed AI image with overlay | Dramatic hooks, artistic carousels |

Set it at the spec level for all slides: `"bg_style": "gradient"` in the spec JSON.
Or per-slide for variation: `"data": {"bg_style": "gradient_mesh", ...}` on specific slides.

#### Screenshot Capture Protocol -- DEPRECATED

**DO NOT use browser screenshots on carousel slides.** They consistently look terrible -- low resolution, poorly framed, and badly integrated with the slide design. This was tested extensively and abandoned.

**Instead**: Use AI-generated images via Gemini 3 Pro for any visual needs:
- Tool/product visuals: Generate an AI illustration or abstract representation
- Data/charts: Generate AI bar charts or infographics (Gemini 3 Pro handles these well)
- Architecture/flows: Generate AI flowcharts or architecture diagrams
- People: Use text descriptions instead of photos

### PHASE 2: CONTENT CREATION

1. **Write the hook** (Slide 1) -- Apply the Hook Taxonomy. This slide determines everything.
2. **Write each slide** -- One idea per slide. No exceptions. Apply the Bullshit Test to each.
3. **Map to renderer data format** -- For each slide, create the JSON data object matching the slide type's required fields (see Data fields by slide type in RENDERING SCRIPTS).
4. **Execute the visual strategy** decided in Phase 1.5:
   - Generate AI images per the 2-3 Rule (hook + 1-2 emotional peaks). State each image's telos.
   - Capture browser screenshots for any real tools/products/news referenced.
   - Set `bg_style` per the Background Style Selection table.
   - Use `diagram` slide type for any process/flow that benefits from a visual.
5. **Select Instagram music** -- Apply the Music Decision Matrix (see MUSIC SELECTION).
6. **Write the caption** -- Front-load value in first 2 lines. Include CTA and hashtags.
7. **Build the carousel spec JSON** -- Assemble all slides into a single spec file for the orchestrator.

### PHASE 3: VISUAL PRODUCTION (LaTeX Pipeline)

Use the **LaTeX-based rendering pipeline** for publication-grade output. This produces slides that match or exceed the quality of accounts with 1M+ followers (Chase AI, Analytics Vidhya, etc.).

The pipeline: **LaTeX (TikZ) -> PDF (pdflatex) -> PNG (pdftoppm at 300 DPI) -> resize to 1080x1350**

#### Why LaTeX (not Pillow/HTML)
- **Knuth-Plass optimal line breaking** -- no ugly word wraps
- **Professional font kerning and ligatures** -- Palatino with microtype
- **Native vector diagrams** -- TikZ flow charts (fallback for simple diagrams)
- **AI image integration** -- full-bleed Gemini 3 Pro images for hook/CTA/diagram backgrounds
- **Gradient backgrounds** -- clean TikZ-rendered gradients for text-only slides
- **Publication-grade output** -- the same engine that typesets academic papers and books

#### Step 3a: Generate AI Images (Hook, CTA, Diagrams)

Generate AI images for hook background, CTA background, and optionally diagram backgrounds:
```bash
# Hook background (cinematic, hyper-detailed 50+ word prompt)
python3 ~/.claude/skills/generate-image/scripts/generate_image.py \
  "Dramatic cinematic split-screen composition: left side dark blue crystalline monolith with electric energy, right side warm golden organic neural network, clash of opposing forces, volumetric lighting, no text no words no letters" \
  --model "google/gemini-3-pro-image-preview" --output tmp/carousel/hook_bg.png

# CTA background (emotional close)
python3 ~/.claude/skills/generate-image/scripts/generate_image.py \
  "Mesmerizing cosmic portal with swirling deep indigo and purple energy, golden light rays, ethereal atmosphere, no text no words" \
  --model "google/gemini-3-pro-image-preview" --output tmp/carousel/cta_bg.png

# Diagram as AI image (optional -- replaces TikZ for better visuals)
python3 ~/.claude/skills/generate-image/scripts/generate_image.py \
  "Professional flowchart: Data Collection box connects to Processing box connects to Output box, clean white background, blue and grey, sharp vector style, readable labels" \
  --model "google/gemini-3-pro-image-preview" --output tmp/carousel/diagram_bg.png
```

#### Step 3b: Render Slides with 7 Slide Types

The LaTeX renderer (`render_latex_slide.py`) supports 7 slide types:

| Type | Description | Best For |
|------|-------------|----------|
| `hook` | Large title + highlighted phrase + subtitle | Cover / first slide |
| `body` | Title + highlighted text + body + bullets | Content-heavy slides, curated list items |
| `comparison` | Multi-column comparison table | Side-by-side analysis |
| `diagram` | Title + TikZ flow diagram (vertical/horizontal) | Architecture, workflows |
| `synthesis` | Styled numbered points with badges | Save-worthy summary |
| `cta` | Centered title + text + handle button | Call to action |

**4 Color Themes**: `warm` (parchment/terracotta), `clean` (white/blue), `dark` (indigo/purple), `earth` (sage/gold)

**Slide 1 (Hook)** -- Title with AI background:
```bash
python3 ~/.claude/skills/world-class-carousel/scripts/render_latex_slide.py \
  --type hook \
  --data tmp/carousel/hook_data.json \
  --output tmp/carousel/slide_01.png \
  --theme dark --brand tmp/carousel/brand.json
```
Where `hook_data.json` contains: `{"title": "6 AI Tools That Will", "title_highlight": "Replace Your Stack", "subtitle": "The tools 10x engineers are switching to.", "callout": "Save this!", "slide_num": 1, "total_slides": 8, "ai_bg": "tmp/carousel/hook_bg.png", "overlay_opacity": 0.63}`

**Body slides** -- Content-heavy with bullets (gradient bg, NO texture):
```bash
python3 ~/.claude/skills/world-class-carousel/scripts/render_latex_slide.py \
  --type body \
  --data tmp/carousel/body_data.json \
  --output tmp/carousel/slide_02.png \
  --theme dark --brand tmp/carousel/brand.json
```
Where `body_data.json` contains: `{"title": "Why Most Developers", "title_highlight": "Get This Wrong", "body": "The biggest mistake is...", "bullets": ["Point 1", "Point 2"], "slide_num": 2, "total_slides": 8, "bg_style": "gradient"}`

**NOTE**: Always pass data as a JSON file path, never inline JSON. Always include `"bg_style": "gradient"` for text-only slides. Always pass `--brand`.

**Comparison slide** -- Multi-column:
```bash
python3 ~/.claude/skills/world-class-carousel/scripts/render_latex_slide.py \
  --type comparison \
  --data tmp/carousel/comparison_data.json \
  --output tmp/carousel/slide_04.png \
  --theme warm --brand tmp/carousel/brand.json
```
Where `comparison_data.json` contains: `{"title": "Claude vs GPT", "subtitle": "How they compare", "columns": [{"name": "Claude", "items": [{"label": "Best for", "value": "Complex refactors"}]}, {"name": "GPT-4", "items": [{"label": "Best for", "value": "Quick prototyping"}]}], "slide_num": 4, "total_slides": 9, "bg_style": "gradient"}`

**Diagram slide** -- AI-generated diagram background (preferred) or TikZ fallback:
```bash
python3 ~/.claude/skills/world-class-carousel/scripts/render_latex_slide.py \
  --type diagram \
  --data tmp/carousel/diagram_data.json \
  --output tmp/carousel/slide_07.png \
  --theme dark --brand tmp/carousel/brand.json
```
Where `diagram_data.json` contains: `{"title": "The Architecture", "description": "How the tools connect.", "diagram_nodes": [{"label": "Code", "desc": "Write"}, {"label": "Deploy", "desc": "Ship"}, {"label": "Monitor", "desc": "Track"}], "diagram_type": "vertical", "slide_num": 7, "total_slides": 9, "ai_bg": "tmp/carousel/diagram_bg.png", "overlay_opacity": 0.60, "bg_style": "gradient"}`

**Synthesis slide** -- Save-worthy numbered summary:
```bash
python3 ~/.claude/skills/world-class-carousel/scripts/render_latex_slide.py \
  --type synthesis \
  --data tmp/carousel/synthesis_data.json \
  --output tmp/carousel/slide_08.png \
  --theme dark --brand tmp/carousel/brand.json
```
Where `synthesis_data.json` contains: `{"title": "Your Stack", "points": ["Tool 1 for X", "Tool 2 for Y", "Tool 3 for Z"], "slide_num": 8, "total_slides": 9, "bg_style": "gradient"}`

**CTA slide** -- with AI background for emotional close:
```bash
python3 ~/.claude/skills/world-class-carousel/scripts/render_latex_slide.py \
  --type cta \
  --data tmp/carousel/cta_data.json \
  --output tmp/carousel/slide_09.png \
  --theme dark --brand tmp/carousel/brand.json
```
Where `cta_data.json` contains: `{"title": "Want the full breakdown?", "cta_text": "Follow for daily tips.", "handle": "@yourbrand", "slide_num": 9, "total_slides": 9, "show_nav": false, "ai_bg": "tmp/carousel/cta_bg.png", "overlay_opacity": 0.67}`

#### Step 3d: Full Carousel Generation (Orchestrator)

Generate a complete carousel from a single JSON spec:
```bash
python3 ~/.claude/skills/world-class-carousel/scripts/generate_carousel.py \
  --spec carousel_spec.json \
  --output-dir outputs/carousel/ \
  --brand tmp/carousel/brand.json
```

The spec JSON format:
```json
{
  "topic": "6 AI Tools That Will Replace Your Stack",
  "brand": "AI Builder",
  "theme": "dark",
  "bg_style": "gradient",
  "slides": [
    {"type": "hook", "data": {"title": "...", "title_highlight": "...", "ai_bg": "tmp/hook_bg.png", "overlay_opacity": 0.63}},
    {"type": "body", "data": {"title": "...", "bullets": ["..."], "bg_style": "gradient"}},
    {"type": "diagram", "data": {"title": "...", "diagram_nodes": [{"label": "...", "desc": "..."}], "diagram_type": "vertical", "ai_bg": "tmp/diagram_bg.png", "overlay_opacity": 0.60}},
    {"type": "synthesis", "data": {"title": "...", "points": ["..."], "bg_style": "gradient"}},
    {"type": "cta", "data": {"title": "...", "handle": "@brand", "ai_bg": "tmp/cta_bg.png", "overlay_opacity": 0.67}}
  ]
}
```

**Spec-level `bg_style`** applies to all slides. Per-slide `data.bg_style` overrides it. Options: `"gradient"`, `"gradient_mesh"`, `"solid"`. If omitted, defaults to `"gradient"`. **Never** use `"texture"`.

The orchestrator auto-injects brand name, slide numbering, renders all slides, and creates a preview grid.

#### Brand Configuration System

The design system is fully generalized through brand configs -- JSON files that define visual identity per channel or brand. Pass `--brand brand.json` to any render command.

**Brand config JSON format**:
```json
{
  "name": "TechStack AI",       // Brand name shown in header
  "logo": "path/to/logo.png",   // Optional: logo image replaces text in header
  "theme": "dark",              // Base theme: warm, clean, dark, earth
  "accent_override": "6366F1",  // Optional: override accent hex (no #)
  "font_serif": "newpxtext",    // LaTeX serif font package (default: Palatino)
  "header_style": "bold",       // Header text: italic, bold, or plain
  "nav_style": "circle",        // Navigation arrow: circle, arrow, none
  "divider_style": "line",      // Dividers: line, ornament (diamond), dots, none
  "corner_radius": "6pt"        // Rounded corner radius for labels/badges
}
```

**3 sample brand configs** (in `tmp/brands/`):

| Brand | Theme | Accent | Header | Divider | Character |
|-------|-------|--------|--------|---------|-----------|
| TechStack AI | dark | Indigo `6366F1` | Bold | Line | Modern dev/AI content |
| Growth Academy | earth | Amber `B45309` | Italic | Ornament | Business coaching |
| Code Academy | clean | Blue (default) | Bold | Dots | Educational tutorials |

**Usage with brand config**:
```bash
python3 ~/.claude/skills/world-class-carousel/scripts/render_latex_slide.py \
  --type hook \
  --data hook_data.json \
  --output slide.png \
  --theme dark \
  --brand brands/techstartup.json
```

**AI Image Integration** (Aristotelian Framework): Slides support two AI image zones:
- `ai_image`: Accent illustration placed in a card (hook bottom, body bottom)
- `ai_bg`: Full-bleed background with semi-transparent overlay for text readability
- When no AI image is provided, decorative geometric accents fill empty space automatically

#### AI Image Integration Principles (First-Principles Framework)

Images in carousels must serve a purpose (telos). Before generating any AI image, name its function in one sentence. If you cannot, do not generate it.

**The Three Teloi (Purposes) of Carousel Images**:

| Telos | When to Use | Image Form | Example |
|-------|------------|------------|---------|
| **Emotional Priming** | Create a feeling before text is read | Atmospheric, evocative, human/natural | Marble bust for philosophy, neon cityscape for tech |
| **Conceptual Anchoring** | Give abstract ideas a visual handle | Symbolic, metaphorical, illustrative | Storm figure for "amor fati", network diagram for systems |
| **Authority Signaling** | Establish credibility through proof | Documentary, screenshots, concrete | Product screenshot, data chart, real photo |

**The 2-3 Rule (Golden Mean)**: In an 8-10 slide carousel, use AI images on exactly **2-3 slides**. Always the hook (slide 1) and CTA (last slide). Optionally the diagram slide with an AI-generated diagram as `ai_bg`. Never on body slides -- visual fatigue destroys reading rhythm and costs 40% content space.

**Image Placement Decision Matrix**:

| Slide Type | AI Image? | Zone | Reasoning |
|------------|-----------|------|-----------|
| `hook` | **Always** | `ai_bg` (full-bleed + 0.60-0.68 overlay) | Scroll-stop power: atmospheric image + typography > typography alone (Axiom 1, 3) |
| `body` | **Never** | -- | Text carries the weight; images destroy 40% content space for minimal gain |
| `diagram` | **Preferred** | `ai_bg` (full-bleed + 0.55-0.65 overlay) | Gemini 3 Pro generates production-quality flowcharts with readable labels, arrows, and boxes -- far more visually striking than basic TikZ. TikZ remains as fallback for simple flows. |
| `synthesis` | **Never** | -- | Numbered points ARE the content; keep text-only with gradient bg |
| `cta` | **Always** | `ai_bg` (full-bleed + 0.65-0.70 overlay) | Emotional close: atmospheric image creates a feeling of resolution |

**Prompt Engineering for Consistency**: All AI images in a single carousel MUST share a consistent style prefix. Build the prefix from the content vertical:

| Content Vertical | Style Prefix for AI Image Prompts |
|-----------------|----------------------------------|
| Mindset/Philosophy | "warm earthy tones, parchment cream, watercolor or classical art style, muted terracotta accents, editorial quality" |
| Tech/AI | "dark indigo and purple tones, subtle geometric patterns, clean digital art, neon accents, futuristic" |
| Business/Strategy | "warm amber and gold tones, bold professional graphics, rich depth, confident and energetic" |
| Education | "clean white and blue tones, flat illustration style, precise and clear, minimal and modern" |
| Creative/Design | "dark charcoal with bold accent colors, artistic and expressive, gallery quality, intentional composition" |

**Text Readability is Inviolable**: If using `ai_bg` (full-bleed), overlay opacity must ensure WCAG AA contrast (4.5:1). Minimum `overlay_opacity: 0.55`. Proven ranges: hook 0.60-0.68, diagram 0.55-0.65, CTA 0.65-0.70.

**What NOT to generate**: Generic stock-photo-style images (people in offices, handshakes, generic landscapes). If the image could illustrate any topic, it fails the Telos Test.

#### AI Visual Generation (via generate-image skill)

Generate AI images for hook backgrounds, CTA backgrounds, and diagram visuals using the `generate-image` skill (requires `AI_GATEWAY_API_KEY`):

```bash
# Hook background -- cinematic, atmospheric, scroll-stopping
python3 ~/.claude/skills/generate-image/scripts/generate_image.py \
  "Dramatic cinematic split-screen composition, glowing neon circuits on dark background, \
  volumetric lighting, deep indigo and electric purple tones, no text, no words, no letters" \
  --model "google/gemini-3-pro-image-preview" --output tmp/carousel/hook_bg.png

# CTA background -- emotional close
python3 ~/.claude/skills/generate-image/scripts/generate_image.py \
  "Abstract convergence of light streams on dark background, warm golden highlights, \
  sense of resolution and completeness, cinematic atmosphere, no text, no words" \
  --model "google/gemini-3-pro-image-preview" --output tmp/carousel/cta_bg.png

# Diagram as AI image (preferred over TikZ for complex flows)
python3 ~/.claude/skills/generate-image/scripts/generate_image.py \
  "Professional flowchart: Data Collection box connects to Processing box connects to Output box, \
  clean white boxes on dark blue background, arrows between nodes, minimal corporate design" \
  --model "google/gemini-3-pro-image-preview" --output tmp/carousel/diagram_bg.png
```

**Key rules**: Always add "no text, no words, no letters" unless the image IS a diagram with labels. Use hyper-detailed prompts (50+ words) for best results.

#### Viral Hook Compositing Pipeline (PIL)

For viral-style hook slides matching accounts like @evolving.ai and @therundownai, use a two-step pipeline:

**Step 1: Generate cinematic base image** with Gemini 3 Pro (topic-specific, dramatic composition):
```bash
# Multi-person composition (best for news/war/rivalry topics)
python3 ~/.claude/skills/generate-image/scripts/generate_image.py \
  "Cinematic photomontage: three powerful figures in dramatic formation, \
  center figure is a humanoid AI robot with glowing eyes, flanking figures \
  are business leaders in dark suits, red and blue dramatic lighting, \
  dark moody background, editorial magazine composition, hyper-detailed" \
  --model "google/gemini-3-pro-image-preview" --output tmp/carousel/hook_base.png

# Single portrait (best for profile/biography/interview topics)
python3 ~/.claude/skills/generate-image/scripts/generate_image.py \
  "Editorial portrait: distinguished elder with glasses, warm ambient lighting, \
  slightly blurred conference background, shallow depth of field, \
  photojournalistic style, natural expression, cinematic color grading" \
  --model "google/gemini-3-pro-image-preview" --output tmp/carousel/hook_base.png

# Face-off composition (best for comparison/versus topics)
python3 ~/.claude/skills/generate-image/scripts/generate_image.py \
  "Dramatic face-off: two opposing figures in profile facing each other, \
  one in cool blue lighting one in warm orange, city skyline between them, \
  energy effects and particles, dark cinematic atmosphere, epic confrontation" \
  --model "google/gemini-3-pro-image-preview" --output tmp/carousel/hook_base.png
```

**Step 2a: News-editorial style** (matches @therundownai -- single person, big headline):
```bash
python3 scripts/compose_news_hook.py \
  --base tmp/carousel/hook_base.png \
  --output tmp/carousel/slide_01_hook.png \
  --headline "OpenAI just hit $13B ARR making it the fastest-growing software company in history" \
  --category "AI NEWS" \
  --brand "@DailyAINews"
```

The `compose_news_hook.py` script (editorial style):
- Subtle bottom gradient (ease-in, configurable start/strength)
- Small category label above headline
- MASSIVE bold headline (Inter Black, auto-sized 42-72px to fill bottom 35%)
- Optional brand mark top-left
- Clean, minimal -- no slide counter, no CTA, no subhead
- Best for: single-person portrait + news headline

**Step 2b: Multi-person viral style** (compose_hook.py -- multi-person, full overlay):
```bash
python3 scripts/compose_hook.py \
  --base tmp/carousel/hook_base.png \
  --output tmp/carousel/slide_01_hook.png \
  --headline "THE AI WAR JUST ESCALATED" \
  --subhead "3 moves that changed everything this week" \
  --brand "YOUR BRAND" \
  --category "AI NEWS"
```

The `compose_hook.py` script (viral style):
- Bottom gradient overlay (0-220 alpha, ease-in curve) for text readability
- Light top gradient for brand area
- Category label (upper-left, e.g., "AI NEWS")
- Brand watermark (centered)
- Word-wrapped bold headline (bottom area, all-caps)
- Optional subheadline
- "SWIPE FOR MORE" CTA with decorative line
- Slide counter (top-right, "1/8")
- Best for: multi-person compositions, face-off style

**Prompt Strategy by Topic Type:**

| Topic Type | Base Image Style | Score |
|---|---|---|
| News/current events | Multi-person photomontage + robot | 8.5/10 |
| Comparison/versus | Face-off composition with opposing energy | 8.5/10 |
| Profile/biography | Single editorial portrait | 8/10 |
| Tools/abstract | Silhouette with holographic/tech backdrop | 7.5/10 |

**For educational/tutorial/framework topics**, AI-generated compositions work excellently (8-8.5/10).

#### Real-Face Hook Pipeline (for news/current events topics)

When the topic involves **specific real people** (Sam Altman, Elon Musk, Jensen Huang, etc.), use web-sourced Creative Commons photos instead of AI generation:

**BEST Approach: Base64 multi-image via AI Gateway (10/10)**

Send local photos as base64 data URIs to `/api/v1/images/generations`. This bypasses URL accessibility issues (Wikimedia blocked, etc.) and supports ALL local images including 3+ people.

```python
import base64, json, os
from pathlib import Path
from urllib import request

API_KEY = os.environ["AI_GATEWAY_API_KEY"]
BASE = "https://ai-gateway.happycapy.ai/api/v1"  # NOT /openai/v1 !

# Load photos as base64 data URIs
images_b64 = []
for photo in ["elon_musk.jpg", "jensen_huang.jpg", "sam_altman.jpg"]:
    data = base64.b64encode(Path(photo).read_bytes()).decode()
    images_b64.append(f"data:image/jpeg;base64,{data}")

payload = {
    "model": "google/gemini-3-pro-image-preview",
    "prompt": "Create a dramatic face-off style composition with these three tech leaders. "
              "Confrontational layout, intense red vs blue split lighting, dark background "
              "with smoke/particle effects. Faces must remain photorealistic and recognizable.",
    "images": images_b64,
    "response_format": "url",
    "n": 1
}

req = request.Request(
    f"{BASE}/images/generations",
    data=json.dumps(payload).encode(),
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
        "Origin": "https://trickle.so"
    },
    method="POST"
)
with request.urlopen(req, timeout=180) as resp:
    result = json.loads(resp.read())
    img_url = result["data"][0]["url"]
    # Download and save...
```

CRITICAL: Use `/api/v1/images/generations` (NOT `/api/v1/openai/v1/images/generations`). The OpenAI-prefixed endpoint rejects the `images` parameter.

**Alternative: transform_image.py with Flickr URLs (9.5/10)**

When photos are available at Flickr URLs (directly accessible by Vertex AI):

```bash
python3 ~/.claude/skills/generate-image/scripts/transform_image.py \
  "Create a dramatic cinematic photomontage combining these tech leaders. \
  Dark dramatic background with blue and red lighting. Keep faces EXACTLY as they appear." \
  "https://live.staticflickr.com/7832/33377877458_d1a3774615_b.jpg" \
  "https://live.staticflickr.com/5767/30796823531_85932ecaa0_b.jpg" \
  --model "google/gemini-3-pro-image-preview" \
  --output tmp/carousel/hook_base.png
```

**Photo sourcing rules:**
- Use Creative Commons (CC BY 2.0+) photos from Flickr, Wikimedia Commons
- Flickr URLs accessible by Vertex AI; Wikimedia URLs often blocked
- Use `urllib.request` with browser User-Agent for Wikimedia downloads to local files
- For local-only files (Wikimedia downloads), use the base64 approach above
- Include CC attribution in carousel caption

**Fallback: PIL rembg composite (7/10)**
```bash
pip install rembg  # One-time setup
# Remove backgrounds, composite onto AI background, apply compose_hook.py overlay
```

**nano-banana-pro status:** The native google-genai SDK requires GEMINI_API_KEY (not set). The AI Gateway has no Gemini-native endpoint, so routing the SDK through the gateway fails (404). The base64 approach above achieves the same multi-image composition capability via the AI Gateway's image generation endpoint.

### PHASE 4: MUSIC SELECTION

Select from Instagram's available music library. Do NOT generate music. Apply the Music Decision Matrix to recommend 2-3 specific tracks the user can search for on Instagram.

### PHASE 5: QUALITY REVIEW & EXPORT

Run the final checklist (see APPENDIX) against every slide. Re-render any slide that fails. Output:
- 7-10 slide PNG images at 1080x1350
- Caption text with hashtags
- Music recommendation (Instagram track names + artists)
- Posting notes (best time, engagement strategy)

---

## THE 6 FOUNDATIONAL AXIOMS

Every decision in this skill traces back to these irreducible premises:

### AXIOM 1: Attention is Finite and Contested
A human scrolling Instagram makes a stay-or-leave decision in ~1.3 seconds. The first slide is a survival test. Visual pattern interrupts trigger involuntary attention. Cognitive curiosity gaps (Zeigarnik effect) create forward momentum. The cost of starting to swipe is high; the cost of continuing is near-zero.

### AXIOM 2: Value is the Only Sustainable Currency
Content that does not leave the viewer materially better off is noise. Save rate is the purest signal of value. Share rate = social currency. "Useful" is domain-specific.

### AXIOM 3: Visual Cognition Precedes Textual Cognition
The brain processes visual information 60,000x faster than text. Color communicates emotion before words. Spatial hierarchy dictates reading order. Consistency creates cognitive fluency. One dominant visual per slide.

### AXIOM 4: Narrative Arc is Hardwired
Content structured as narrative is retained 22x better than lists. Each slide must resolve the previous curiosity gap AND create the next one. The arc must reach genuine resolution.

### AXIOM 5: The Medium Constrains and Enables
1080x1350 canvas on a 6-inch screen in half-attention. Minimum readable font = 24px. Bottom ~15% occluded by UI. Portrait (4:5) occupies maximum screen real estate.

### AXIOM 6: Audio Creates Emotional Context
Music activates the limbic system independently. Instagram's algorithm rewards music usage with 15-30% more reach. Genre signals tribal identity. Trending audio boosts discovery if it genuinely fits.

---

## THE 7 CAROUSEL ARCHETYPES

Auto-select the best archetype based on the topic. Each archetype has a specific slide structure, value test, and music profile.

### 1. TUTORIAL (How-To)
```
Slide 1: Problem statement (hook)
Slide 2: Tool/method introduction
Slide 3: Step 1 (with visual)
Slide 4: Step 2
Slide 5: Step 3
Slide 6: Step 4 (if needed)
Slide 7: Result / proof it works
Slide 8: Common mistakes to avoid
Slide 9: Quick-reference summary (save-worthy)
Slide 10: CTA
```
**Value Test**: Can the reader DO the thing after reading?
**Music Profile**: Lo-fi/chillhop, 70-85 BPM, instrumental

### 2. FRAMEWORK (Mental Model)
```
Slide 1: Common problem everyone faces (hook)
Slide 2: Why existing approaches fail
Slide 3: The framework name + overview
Slide 4: Component 1 explained
Slide 5: Component 2 explained
Slide 6: Component 3 explained
Slide 7: How the components connect (diagram)
Slide 8: Practical application example
Slide 9: The complete framework visual (save-worthy)
Slide 10: CTA
```
**Value Test**: Does the reader now have a reusable thinking tool?
**Music Profile**: Minimal electronic, 90-110 BPM, instrumental

### 3. MYTH-BUSTER (Contrarian Insight)
```
Slide 1: "Everyone thinks X" (hook)
Slide 2: "Here's what's actually happening"
Slide 3: Evidence 1
Slide 4: Evidence 2
Slide 5: Evidence 3
Slide 6: The real framework / truth
Slide 7: Implications
Slide 8: What to do instead
Slide 9: The mental model shift (save-worthy)
Slide 10: CTA
```
**Value Test**: Has the reader's mental model shifted?
**Music Profile**: Trip-hop/downtempo, 85-100 BPM, instrumental

### 4. CASE STUDY (Proof-Based)
```
Slide 1: The result / shocking metric (hook)
Slide 2: The context / starting point
Slide 3: What was done (overview)
Slide 4: Step 1 of the process
Slide 5: Step 2
Slide 6: Step 3
Slide 7: The data / proof
Slide 8: Key insight
Slide 9: How you can replicate it (save-worthy)
Slide 10: CTA
```
**Value Test**: Is the specific mechanism replicable?
**Music Profile**: Upbeat electronic, 110-120 BPM, light vocals OK

### 5. CURATED LIST (Resource Compilation)
```
Slide 1: "X Tools/Resources for Y" (hook)
Slide 2: Item 1 + why it's valuable
Slide 3: Item 2 + why
Slide 4: Item 3 + why
Slide 5: Item 4 + why
Slide 6: Item 5 + why
Slide 7: Item 6 + why (if needed)
Slide 8: Item 7 + why (if needed)
Slide 9: Comparison / selection guide (save-worthy)
Slide 10: CTA
```
**Value Test**: Can the reader immediately use at least 3 of these?
**Music Profile**: Chill beats/lo-fi, 75-90 BPM, instrumental

### 6. DEEP DIVE (Technical Explanation)
```
Slide 1: The concept + why it matters (hook)
Slide 2: What most people get wrong
Slide 3: How it actually works (simplified)
Slide 4: Visual diagram / mechanism
Slide 5: Practical example 1
Slide 6: Practical example 2
Slide 7: Common mistakes
Slide 8: Pro tips
Slide 9: The complete mental model (save-worthy)
Slide 10: CTA
```
**Value Test**: Does the reader understand the mechanism, not just the surface?
**Music Profile**: Ambient/atmospheric, 60-80 BPM, instrumental only

### 7. TRANSFORMATION (Before/After)
```
Slide 1: The "after" result (hook)
Slide 2: The "before" state / the pain
Slide 3: The discovery / turning point
Slide 4: The change in approach
Slide 5: Step 1 of the new way
Slide 6: Step 2
Slide 7: Step 3
Slide 8: The complete "after" state with proof
Slide 9: How to start your transformation (save-worthy)
Slide 10: CTA
```
**Value Test**: Can the reader see themselves in the transformation?
**Music Profile**: Progressive/building, 80-120 BPM arc, light vocals OK

---

## THE 6 HOOK PATTERNS

The first slide determines everything. Select the best hook pattern for the topic:

### 1. The Curiosity Gap
> "Claude Code has a memory problem. Here's how to fix it for free."

States a problem the audience recognizes + promises a solution. Optionally removes an objection ("for free", "in 5 minutes").

### 2. The Contrarian Statement
> "Stop using RAG. There's a better way."

Contradicts a common belief. Creates cognitive dissonance that demands resolution.

### 3. The Specific Result
> "This setup saved me 4 hours per week of prompt debugging."

Concrete numbers bypass the vague-promise filter. Specificity = credibility.

### 4. The Analogy Bridge
> "Your AI agent's memory works like a messy desk. Here's how to organize it."

Maps unfamiliar onto familiar. Creates instant comprehension.

### 5. The "You're Doing It Wrong"
> "90% of developers use Claude Code wrong. Are you one of them?"

Identity-based challenge. Use sparingly -- dangerous if overused.

### 6. The Stack / Combination
> "Obsidian + Claude Code = unlimited AI memory"

Two known things combined unexpectedly. The "+" implies synergy.

---

## THE BULLSHIT TEST (Mandatory Quality Gate)

**Every single slide must pass ALL 3 conditions before rendering. No exceptions.**

### Condition 1: SPECIFICITY
Does this contain a concrete, actionable insight that could NOT be guessed by someone with zero domain knowledge?
- FAIL: "Use the right tools for the job"
- PASS: "Obsidian's graph view lets Claude Code traverse 10x more documents by following wiki-links between markdown files"

### Condition 2: NOVELTY
Does this present a connection, framework, or technique the viewer has likely NOT encountered before?
- FAIL: "AI is changing the world"
- PASS: "By creating bidirectional links between your docs, you turn Claude Code's context window into a navigation system instead of a storage container"

### Condition 3: DENSITY
Could the same information be compressed further without loss of meaning? If yes, it is padded and needs to be tightened.
- FAIL: "There are many benefits to using this approach, including several key advantages that make it worthwhile"
- PASS: "3 benefits: 10x doc navigation, auto-linked memory, zero-config setup"

**If a slide fails any condition, rewrite it before rendering.**

---

## VISUAL DESIGN SYSTEM

### Typography Hierarchy

| Element | Size | Weight | Font Type |
|---------|------|--------|-----------|
| Slide Title | 64-80px | Bold/Black (700-900) | Strong serif OR geometric sans |
| Subtitle / Hook | 32-40px | SemiBold (600) | Same family as title |
| Body Text | 24-28px | Regular (400) | Clean sans-serif |
| Bullet Points | 22-26px | Regular (400) | Same as body |
| Labels / Citations | 16-20px | Light (300) | Same as body |
| Slide Indicator | 14-16px | Light (300) | Sans-serif |

**Rules**:
- Maximum 2 fonts per carousel
- Title font and body font must pair well
- NEVER go below 24px for any text the reader must understand
- Consistent across ALL slides

### Color Palettes by Content Vertical

**Tech / AI / Coding**:
- Background: `#0D1117` (deep dark) or `#1A1A2E` (midnight blue)
- Primary text: `#E6EDF3` (near-white) or `#F0F6FC`
- Accent: `#7C3AED` (electric purple) or `#3B82F6` (bright blue)
- Secondary: `#6B7280` (muted gray)

**Business / Strategy**:
- Background: Linear gradient `#F97316` to `#EAB308` (warm amber) or `#FFF7ED` (cream)
- Primary text: `#1C1917` (near-black)
- Accent: `#DC2626` (confident red) or `#F59E0B` (gold)
- Secondary: `#78716C` (warm gray)

**Education / How-To**:
- Background: `#FFFFFF` (clean white) or `#F8FAFC` (cool off-white)
- Primary text: `#0F172A` (dark slate)
- Accent: `#2563EB` (trust blue) or `#0EA5E9` (sky blue)
- Secondary: `#64748B` (slate gray)

**Design / Creative**:
- Background: `#18181B` (charcoal) or `#FAFAFA` (near-white)
- Primary text: Inverse of background
- Accent: ONE bold color (`#EC4899` magenta, `#10B981` emerald, or `#F59E0B` amber)
- Secondary: `#71717A` (zinc)

**Mindset / Growth**:
- Background: `#F5F0EB` (warm neutral) or `#1B3A2D` (forest dark)
- Primary text: `#2D2416` (earth brown) or `#E8E0D5` (warm light)
- Accent: `#16A34A` (forest green) or `#B45309` (amber earth)
- Secondary: `#8B7355` (warm mid-tone)

### Layout Rules

1. **Canvas**: 1080 x 1350 px (4:5 portrait) -- ALWAYS
2. **Margins**: 60px minimum on all sides
3. **Safe Zone**: Center 80% (top/bottom 10% may be occluded by Instagram UI)
4. **One idea per slide**: If a slide has two ideas, split it into two slides
5. **Visual anchor**: Every slide needs ONE dominant visual element
6. **Breathing room**: Content should never feel cramped -- generous whitespace signals quality

---

## MUSIC SELECTION (Instagram Library)

Do NOT generate music. Recommend specific tracks available on Instagram's music library.

### Music Decision Matrix

| Content Type | Search Keywords on Instagram | BPM Range | Vocals | Example Tracks to Search |
|-------------|----------------------------|-----------|--------|------------------------|
| **Tech / AI** | "lo-fi", "chill beats", "trip-hop" | 70-90 | No | DJ Shadow - Six Days, Nujabes - Aruarian Dance, Tycho - A Walk, Bonobo - Kerala |
| **Business** | "indie electronic", "future bass" | 100-120 | Minimal | ODESZA - A Moment Apart, Rufus Du Sol - Innerbloom, Bicep - Glue |
| **Tutorial** | "study beats", "chillhop", "acoustic" | 75-95 | No | Idealism - Lovely Day, Jinsang - Solitude, Tomppabeats - Monday Loop |
| **Motivational** | "epic", "cinematic", "uplifting" | 110-130 | Optional | M83 - Midnight City, Hans Zimmer - Time, Illenium - Good Things Fall Apart |
| **Creative** | "minimal techno", "ambient", "art" | 90-115 | No | Four Tet - Two Thousand and Seventeen, Jon Hopkins - Emerald Rush, Kiasmos - Blurred |
| **Myth-Buster** | "dark ambient", "post-rock", "mysterious" | 80-100 | No | Massive Attack - Teardrop, Radiohead - Everything In Its Right Place, Portishead - Wandering Star |
| **Case Study** | "upbeat", "indie pop", "electronic" | 110-125 | Light | Washed Out - Feel It All Around, Toro y Moi - So Many Details, M83 - Wait |

### Music Selection Rules

1. **Text-heavy carousels**: ALWAYS instrumental only (vocals compete with reading)
2. **Visual-heavy carousels**: Vocals acceptable (separate processing channels)
3. **Trending audio**: Use ONLY if it genuinely fits the content type. Mismatched trending sounds damage authenticity
4. **Trending audio lifecycle**: Discovery (Day 0-3, max boost) -> Growth (Day 3-14, good) -> Peak (Day 14-30, OK) -> Saturation (Day 30+, skip)
5. **Output format**: Provide 2-3 track recommendations with artist name, track name, and why it fits

---

## CAPTION TEMPLATE

```
[Hook line -- front-load value, must be compelling in first 2 lines before "...more"]

[2-3 sentences expanding the core value proposition]

[Key points:]
- Point 1 (specific, not vague)
- Point 2
- Point 3

[Specific CTA -- NOT "What do you think?" but rather a specific question or action]

[5-15 hashtags with distribution:]
[2-3 broad (100K-1M posts)] [3-5 niche (10K-100K)] [2-3 community (1K-10K)] [1-2 branded]
```

---

## INSTAGRAM ALGORITHM OPTIMIZATION

- **Save Rate** is the #1 signal. Design every carousel to be save-worthy. Include a synthesis/mental-model slide.
- **10-slide carousels** outperform shorter ones by ~30% in save rate
- **Dwell time**: More slides = more time on post = algorithm reward
- **Music** adds ~15-30% reach boost
- **Re-engagement**: Instagram re-shows carousels to users who did not swipe all the way through
- **First hour**: Posts saved within the first hour get exponential distribution
- **Hashtags**: Put in caption (not first comment). 5-15 total.

---

## RENDERING SCRIPTS

### render_latex_slide.py (PRIMARY RENDERER)

Publication-grade LaTeX slide renderer. Produces 1080x1350 PNG slides using pdflatex + pdftoppm.

**6 slide types**: `hook`, `body`, `comparison`, `diagram`, `synthesis`, `cta`
**4 themes**: `warm`, `clean`, `dark`, `earth`

```bash
python3 ~/.claude/skills/world-class-carousel/scripts/render_latex_slide.py \
  --type body \
  --data body_data.json \
  --output slide.png \
  --theme dark \
  --brand brand_config.json
```

**Data fields by slide type**:
- **hook**: `title`, `title_highlight`, `subtitle`, `callout`, `ai_bg`, `overlay_opacity`, `logos[]`
- **body**: `title`, `title_highlight`, `body`, `bullets[]`, `bg_style`
- **comparison**: `title`, `subtitle`, `columns[{name, items[{label, value}]}]`, `bg_style`
- **diagram**: `title`, `description`, `diagram_nodes[{label, desc}]`, `diagram_type` (vertical/horizontal), `ai_bg`, `overlay_opacity`
- **synthesis**: `title`, `points[]`, `bg_style`
- **cta**: `title`, `cta_text`, `handle`, `stats[]`, `ai_bg`, `overlay_opacity`
- **All types**: `slide_num`, `total_slides`, `show_nav`, `ai_bg` (full-bleed background), `overlay_opacity`, `bg_style`

### generate_carousel.py (ORCHESTRATOR)

End-to-end carousel generation from a JSON spec. Handles slide numbering, rendering, and preview grid assembly.

```bash
python3 ~/.claude/skills/world-class-carousel/scripts/generate_carousel.py \
  --spec carousel_spec.json \
  --output-dir outputs/carousel/ \
  --brand brand_config.json
```

### AI Image Generation (via generate-image skill)

Use the `generate-image` skill for all AI images (hook bg, CTA bg, diagram bg). See "AI Visual Generation" section above for examples.

```bash
python3 ~/.claude/skills/generate-image/scripts/generate_image.py \
  "Your detailed prompt here, 50+ words, no text no words no letters" \
  --model "google/gemini-3-pro-image-preview" --output tmp/carousel/image.png
```

### assemble_carousel.py (ASSEMBLY)

Validates 1080x1350, optimizes PNGs, creates preview grid, generates metadata JSON.

```bash
python3 ~/.claude/skills/world-class-carousel/scripts/assemble_carousel.py \
  --input-dir tmp/carousel/ --output-dir outputs/carousel/ --optimize
```

### render_slide.py (LEGACY - Pillow-based)

Pillow-based renderer with 6 layout modes. Superseded by `render_latex_slide.py` for production use. Still available for quick prototyping without LaTeX dependencies.

---

## 10 WORLD-CLASS DIFFERENTIATORS

Apply these to elevate from "good" to "world-class":

1. **Intellectual Density**: One INSIGHT per slide, not just one idea (insight = non-obvious connection between two known things)
2. **Visual Craftsmanship**: Every pixel intentional. Margins mathematical. Colors from a system.
3. **Hook Specificity**: "I tested 1,247 prompts across 6 models" not "5 Tips for Better Prompts"
4. **Narrative Completeness**: Each slide creates a question the next answers. Final slide ties back to hook.
5. **Proof Over Claims**: Screenshots, before/after comparisons, specific metrics -- not "this is great"
6. **Typography as Design**: The way words are sized, spaced, and placed tells the story VISUALLY
7. **Strategic Restraint**: Know what to leave OUT. Negative space is a design choice.
8. **Music-Content Resonance**: BPM matches reading pace. Genre signals the tribe.
9. **Save-Worthy Synthesis**: Last content slide is a mental model / framework diagram worth saving
10. **Authentic Voice**: Written as one expert talking to a colleague. Never "content creator voice."

---

## FINAL CHECKLIST

Before delivering any carousel, verify ALL of these:

- [ ] First slide passes the 1.3-second scroll-stop test
- [ ] Every slide passes the Bullshit Test (Specific, Novel, Dense)
- [ ] One idea per slide, no exceptions
- [ ] Typography readable at mobile size (24px+ body text)
- [ ] Color palette consistent across all slides
- [ ] Narrative arc complete (tension -> resolution)
- [ ] Each slide creates curiosity for the next
- [ ] Last content slide has a save-worthy synthesis (mental model, framework, diagram)
- [ ] CTA slide is clear and specific
- [ ] Music recommendation matches content type and audience
- [ ] Aspect ratio is 1080x1350 (4:5)
- [ ] All content within safe zone (not occluded by UI)
- [ ] Caption front-loads value in first 2 lines
- [ ] 5-15 hashtags with proper distribution (broad + niche + community + branded)
- [ ] Alt-text provided for accessibility
- [ ] Every rendered slide visually inspected (no half-empty slides)
- [ ] Synthesis title < 4 words
- [ ] Synthesis points are flat strings, not dicts
- [ ] JSON data passed via temp files, not inline in bash
- [ ] Hook/CTA slides use `ai_bg` for visual topics; body slides stay text-only
- [ ] AI images prompted with "no text" to prevent unwanted labels
- [ ] Overlay opacity 0.60-0.68 for hooks, 0.65-0.70 for CTA
- [ ] All KNOWN_ISSUES.md rules checked before delivery

---

## PHASE 6: LEARNING PROTOCOL (Post-Delivery)

After every carousel delivery, update the skill's knowledge base. This system prevents repeating mistakes while staying compact.

### Two-Tier Memory Architecture

**Tier 1: `KNOWN_ISSUES.md`** (in this skill directory)
- MAX 60 lines. Contains ONLY compressed, actionable rules.
- Format: one-line rules grouped by category. No narratives, no session history.
- When adding a new rule: check if it supersedes an existing rule. If yes, REPLACE the old rule. Never append duplicates.
- Read this file at the START of every carousel session to avoid known pitfalls.

**Tier 2: `session-archives/` directory** (in this skill directory)
- Verbose session logs go here as timestamped files: `session-archives/YYYY-MM-DD-topic.md`
- Include: full experiment data, scoring matrices, debug traces, before/after comparisons.
- These files are NEVER loaded into context unless explicitly requested by the user.
- They exist as raw data for future deep-dives, not as operational knowledge.

### After Every Session

1. **Check KNOWN_ISSUES.md** -- Does this session reveal a new rule? Add it (max 1 line). Does it supersede an old rule? Replace it.
2. **Archive verbose data** -- If the session involved experiments, debugging, or research, write a session archive file.
3. **Compress, don't accumulate** -- The goal is a fixed-size knowledge base that gets BETTER over time, not BIGGER.

### The Compression Principle

Every piece of learning must be compressed to its irreducible form before entering Tier 1:
- BAD: "In session on March 10, we discovered that passing synthesis points as dicts causes an AttributeError because the renderer at line 870 does escape_latex(pt) directly on each point" (38 words)
- GOOD: "Synthesis `points[]` must be FLAT STRINGS, not dicts. Renderer does `escape_latex(pt)` directly." (12 words)

If you can't compress it to one line, it belongs in Tier 2 (session archive), not Tier 1.
