# KNOWN ISSUES & PROVEN RULES
# Max 60 lines. Rules only -- no narratives. Replace, never append.
# Last compressed: 2026-03-10 | Sessions distilled: 8

## DATA FORMAT RULES
- Synthesis `points[]` must be FLAT STRINGS, not dicts. Renderer does `escape_latex(pt)` directly.
- Never pass JSON inline in bash. Write to temp file, pass file path.
- Diagram `diagram_nodes[]` must have both `label` and `desc` keys.
- Brand name in header comes from `--brand` config JSON, NOT from `data.brand`. Always pass `--brand`.
- Horizontal diagrams truncate labels at 5+ nodes. Use `vertical` when node count > 4.

## TITLE LENGTH LIMITS
- Hook: 4-6 words main + 2-4 words highlight
- Body: 2-3 words main + 1-3 words highlight
- Diagram: 3-5 words total
- Synthesis: MAX 3-4 words (numbered points ARE the content)
- CTA: 4-7 words

## SIZING RULES
- NEVER use fixed px/cm for content elements. Compute relative to canvas and content count.
- Diagram nodes: width/height derived from card_height, card_width, and node count.
- Body bullets: max 3-4 per slide for readability at mobile size.

## VISUAL STRATEGY (Experimentally Verified)
- Hook slides: `ai_bg` full-bleed + 0.60-0.68 overlay. Use compose_hook.py for viral-style overlays.
- VIRAL HOOK PIPELINE: AI base -> compose_hook.py (PIL gradient+headline+brand+CTA). Prompt by topic type.
- REAL FACES BEST: Base64 multi-image via /api/v1/images/generations (10/10). Sends local photos as data URIs. All 3+ faces in one composition.
- REAL FACES ALT: transform_image.py with CC-licensed Flickr URLs (9.5/10). Limited to URL-accessible photos only.
- Flickr URLs work with Vertex AI; Wikimedia URLs blocked. Use urllib for Wikimedia downloads.
- Base64 data URIs WORK at /api/v1/images/generations (NOT /api/v1/openai/v1/). Correct endpoint is critical.
- Fallback: rembg + PIL composite onto AI background (7/10).
- Body slides: ALWAYS text-only. Images destroy 40% content space for minimal gain.
- CTA slides: `ai_bg` full-bleed + 0.65-0.70 overlay for emotional close.
- Diagram: TikZ or AI-generated flowchart as `ai_bg`. Synthesis: text-only.
- NEVER use texture/paper bg_style or browser screenshots. Default is `gradient`.
- Text-only slides: always use `"bg_style": "gradient"` in data JSON.

## AI IMAGE GENERATION (Gemini 3 Pro via generate-image skill)
- Use `generate-image` skill (AI_GATEWAY_API_KEY). Nano-banana-pro native SDK needs GEMINI_API_KEY (unset; gateway has no Gemini-native endpoint).
- Model: `google/gemini-3-pro-image-preview`. Fallback: `gemini-3.1-flash-image-preview`.
- HYPER-DETAILED prompts (50+ words): materials, lighting, composition, colors, atmosphere. Generic = bad.
- All images output ~1408x768 (landscape). Overlay compensates for portrait stretch on slides.
- PROVEN CAPABILITIES: flowcharts, architecture diagrams, bar charts, infographics, cinematic portraits.
- Gemini 3 Pro renders accurate text labels, arrows, boxes -- can replace TikZ for diagram slides.
- For diagram slides: consider AI-generated diagram image as `ai_bg` instead of TikZ.

## QUALITY GATES
- Every slide must fill its canvas. No half-empty slides. EVER.
- Visually inspect every rendered slide before delivery.
- Body bullets need substance: research citations, specific numbers, actionable advice.
- 125 characters per slide max for mobile readability.

## INSTAGRAM ENGAGEMENT AXIOMS (Research-Backed, 35+ Sources)
- Carousels get 95-114% more saves than static posts
- Educational content = 4.7% avg engagement (highest of any format)
- First slide = 80% of engagement decision (<1.5s scroll-stop test)
- Save rates reach 3.4% for educational carousels
- Text-heavy infographic carousels outperform photo-only carousels

## USER PREFERENCES
- Content must be SAVE-WORTHY -- not just headlines. Every bullet needs substance.
- Aristotelian root-cause analysis over symptom patching.
- Maximum virality: Tier 1 trending music, psychological hooks, specific citations.
- Dark theme + gradient bg for tech/AI content.
- Always provide Instagram music recommendations with carousel.
- 8-slide format: Hook -> 4 content -> Diagram -> Synthesis -> CTA
