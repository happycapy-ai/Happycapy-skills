# Face Identity Consistency Guide for ViMax Pipeline

Validated through 257 experiments. Reduces face distance from 0.74 to 0.22 (70% improvement).

## The Problem

When generating multi-shot videos, AI video models (Veo, Sora, Seedance) suffer from severe face identity drift:
- Only the first frame preserves the character's face from the reference image
- Subsequent frames progressively lose identity (different nose, jawline, hair, etc.)
- By mid-clip, the generated person looks completely different

## Solution: Two-Stage Pipeline

### Stage 1: Generate Identity-Accurate First Frame (Gemini Image Gen)

Use `google/gemini-3.1-flash-image-preview` with the character's reference photos as input to generate each shot's first frame. This gives precise control over facial features.

### Stage 2: Generate Video Anchored to First Frame (Veo)

Pass the Stage 1 output as `first_frame` to Veo. Always prepend this face-lock instruction to the video prompt:

```
CRITICAL: The character's face in every frame of this video MUST remain identical
to the face shown in the starting frame image. Maintain the exact same facial
structure, features, skin tone, hair, glasses, and all distinguishing marks
throughout the entire clip. The face must match the starting frame exactly.
```

## Key Techniques

### 1. Hyper-Detailed Physical Descriptions (in EVERY prompt)

Never rely on the model "remembering" a character. Include exhaustive descriptions every time:

- Ethnicity and age
- Hair: texture, style, color, length
- Face: nose shape, eye shape/spacing, jawline contour
- Skin tone
- Distinguishing marks: glasses type, facial hair, scars, moles
- Body build

Example: "A young South Asian man with curly dark hair, round glasses, light mustache, medium build, early 20s"

### 2. Extreme Close-Up Framing

For shots where face identity matters most, use close-up framing to force the model to focus on facial details.

### 3. Consistent Scene Lighting

Use the same lighting setup across shots. Dramatic lighting changes cause the model to alter facial features.

### 4. Front-View Portrait as Primary Reference

The character's front-view portrait should ALWAYS be included as a reference image when their face is visible.

## What Does NOT Work

- Complex prompt engineering (viseme morphing, phoneme anchoring, etc.)
- LLM-suggested "creative" experiments averaged worse than simple direct prompts
- Lip-sync to external audio (Veo generates its own internal audio)

## Files Modified

- `agents/reference_image_selector.py` - Face identity added as highest priority in reference selection
- `agents/character_portraits_generator.py` - Enhanced portrait prompts with identity-critical details
- `pipelines/script2video_pipeline.py` - Face-lock instruction prepended to all video prompts
- `~/.claude/skills/generate-video/SKILL.md` - Best practices documented for standalone video generation

## Metrics

| Metric | Baseline | After Changes |
|--------|----------|--------------|
| Face Distance (avg) | 0.740 | 0.221 |
| Verification Rate | 5% | 100% |
| Pass Rate (<0.40) | 0% | 85% |
