---
name: capy-video-gen-skill
description: Multi-shot AI video generation pipeline with face identity consistency. Converts scripts or ideas into complete videos using character extraction, storyboarding, frame generation, and video assembly. 300 experiments validated, 70% face distance improvement. Use when the user asks to create a video from a script, story, idea, or wants multi-shot video with consistent characters.
allowed-tools: Bash, Read, Write, Edit
---

# Capy Video Gen Skill - Script-to-Video Pipeline

Generate complete multi-shot videos from scripts or ideas with consistent character faces across all scenes. Built for HappyCapy AI Gateway. 300 experiments validated, 70% face distance improvement.

## Overview

ViMax converts text scripts into full videos through an automated pipeline:
1. Extract characters from script with detailed physical features
2. Generate front/side/back character portraits
3. Design shot-by-shot storyboard
4. Decompose each shot into first_frame, last_frame, and motion descriptions
5. Build camera tree for shot relationships
6. Generate frames with reference image selection (face identity as top priority)
7. Generate video clips from frames
8. Concatenate into final video

## Installation Location

The ViMax pipeline code is at: `/home/node/a0/workspace/527fb591-1439-4b5b-ad5d-90f972773f95/workspace/tmp/ViMax/`

All commands must be run from this directory using the venv:
```bash
cd /home/node/a0/workspace/527fb591-1439-4b5b-ad5d-90f972773f95/workspace/tmp/ViMax
```

## Prerequisites

- `AI_GATEWAY_API_KEY` environment variable (auto-configured in HappyCapy)
- Python venv at `.venv/` (already set up)

## Quick Start

### Script-to-Video

Edit the script, requirements, and style in the entry script, then run:

```bash
cd /home/node/a0/workspace/527fb591-1439-4b5b-ad5d-90f972773f95/workspace/tmp/ViMax
.venv/bin/python main_happycapy_script2video.py
```

### Idea-to-Video

For generating from a brief idea (auto-generates script first):

```bash
cd /home/node/a0/workspace/527fb591-1439-4b5b-ad5d-90f972773f95/workspace/tmp/ViMax
.venv/bin/python main_happycapy_idea2video.py
```

## Programmatic Usage

```python
import asyncio
from langchain.chat_models import init_chat_model
from tools.render_backend import RenderBackend
from utils.config_loader import load_config
from pipelines.script2video_pipeline import Script2VideoPipeline

config = load_config("configs/happycapy_script2video.yaml")
chat_model = init_chat_model(**config["chat_model"]["init_args"])
backend = RenderBackend.from_config(config)

pipeline = Script2VideoPipeline(
    chat_model=chat_model,
    image_generator=backend.image_generator,
    video_generator=backend.video_generator,
    working_dir=config["working_dir"],
)

# Run the pipeline
asyncio.run(pipeline(
    script="Your script here...",
    user_requirement="No more than 8 shots total.",
    style="Cinematic, warm lighting"
))
```

## Pipelines

### Script2VideoPipeline
- Input: A formatted screenplay/script with character dialogue and scene descriptions
- Output: Concatenated video at `{working_dir}/final_video.mp4`
- Config: `configs/happycapy_script2video.yaml`

### Idea2VideoPipeline
- Input: A brief idea/concept (1-3 paragraphs)
- Output: Auto-generates a script, then produces video
- Config: `configs/happycapy_idea2video.yaml`

## Configuration

HappyCapy configs at `configs/happycapy_script2video.yaml`:

```yaml
chat_model:
  init_args:
    model: gpt-4.1
    model_provider: openai
    api_key: ${AI_GATEWAY_API_KEY}
    base_url: https://ai-gateway.happycapy.ai/api/v1/openai/v1

image_generator:
  class_path: tools.ImageGeneratorHappyCapyAPI
  init_args:
    api_key: ${AI_GATEWAY_API_KEY}
    model: google/gemini-3.1-flash-image-preview

video_generator:
  class_path: tools.VideoGeneratorHappyCapyAPI
  init_args:
    api_key: ${AI_GATEWAY_API_KEY}
    model: google/veo-3.1-generate-preview

working_dir: .working_dir/script2video
```

## Key Components

### Agents (AI Processing)

| Agent | File | Purpose |
|-------|------|---------|
| CharacterExtractor | `agents/character_extractor.py` | Extract characters with static/dynamic features from script |
| CharacterPortraitsGenerator | `agents/character_portraits_generator.py` | Generate front/side/back portraits for each character |
| StoryboardArtist | `agents/storyboard_artist.py` | Design shot-by-shot storyboard with first/last frames and motion |
| ReferenceImageSelector | `agents/reference_image_selector.py` | Select best reference images for each frame (face identity #1 priority) |
| CameraImageGenerator | `agents/camera_image_generator.py` | Build camera trees and generate transition videos |
| BestImageSelector | `agents/best_image_selector.py` | Select best generated image from candidates |
| Screenwriter | `agents/screenwriter.py` | Generate scripts from ideas |

### Tools (Generation Backends)

| Tool | File | Purpose |
|------|------|---------|
| ImageGeneratorHappyCapyAPI | `tools/image_generator_happycapy_api.py` | Image generation via HappyCapy Gateway (Gemini) |
| VideoGeneratorHappyCapyAPI | `tools/video_generator_happycapy_api.py` | Video generation via HappyCapy Gateway (Veo) |
| RenderBackend | `tools/render_backend.py` | Factory for instantiating generators from config |

### Interfaces (Data Models)

- `CharacterInScene` - Character with identifier, static_features, dynamic_features
- `ShotDescription` - Shot with ff_desc, lf_desc, motion_desc, variation_type
- `Camera` - Camera with parent-child relationships
- `Frame` - Frame with shot_idx, frame_type, visible characters
- `ImageOutput` / `VideoOutput` - Generation outputs with save methods

## Face Identity Consistency (CRITICAL)

This pipeline includes face identity improvements validated through 257 experiments (70% improvement in face distance, from 0.74 to 0.22):

### Built-In Protections

1. **Reference Image Selector**: Face identity is the #1 priority when selecting reference images. The front-view portrait is always included when a character's face is visible.

2. **Character Portraits**: Enhanced prompts generate identity-critical details (exact nose shape, eye spacing, jawline, distinguishing marks) for cross-scene recognition.

3. **Video Prompt Face Lock**: Every video generation prompt is prepended with a face identity instruction requiring the character's face to remain identical to the starting frame throughout the clip.

### Best Practices When Using ViMax

- **Hyper-detailed character descriptions**: Include ethnicity, age, hair texture/style/color, eye shape, facial hair, glasses, skin tone, build, and distinguishing marks in your script's character introductions
- **Extreme close-up shots**: Include at least one extreme close-up per character to anchor identity
- **Consistent lighting**: Specify similar lighting across scenes to prevent face drift
- **User-provided reference photos**: Place photos in the working directory and pass them as `character_portraits_registry` to skip AI portrait generation

### What Does NOT Work

- Complex prompt engineering (viseme morphing, phoneme anchoring) does not improve face identity
- Simple, direct prompts with detailed physical descriptions outperform clever prompts
- Lip-sync to external audio is NOT possible (Veo generates its own internal audio)

See `FACE_IDENTITY_GUIDE.md` in the ViMax directory for full details.

## Output Structure

After a run, the working directory contains:

```
.working_dir/script2video/
  characters.json                      # Extracted characters
  character_portraits_registry.json    # Portrait paths registry
  character_portraits/                 # Generated portraits
    0_CharacterName/
      front.png
      side.png
      back.png
  storyboard.json                     # Shot descriptions
  camera_tree.json                    # Camera relationships
  shots/
    0/
      shot_description.json
      first_frame.png
      last_frame.png (if medium/large variation)
      video.mp4
    1/
      ...
  final_video.mp4                     # Final concatenated output
```

## Customization

### Using Your Own Reference Photos

To use real photos instead of AI-generated portraits:

```python
# Build a portrait registry pointing to your photos
character_portraits_registry = {
    "Alice": {
        "front": {"path": "/path/to/alice_front.png", "description": "Front view of Alice"},
        "side": {"path": "/path/to/alice_side.png", "description": "Side view of Alice"},
        "back": {"path": "/path/to/alice_back.png", "description": "Back view of Alice"},
    }
}

# Pass to pipeline (skips portrait generation)
await pipeline(
    script=script,
    user_requirement=user_requirement,
    style=style,
    character_portraits_registry=character_portraits_registry,
)
```

### Changing Models

Edit the YAML config to use different models:
- Image: `google/gemini-3.1-flash-image-preview` (recommended for face identity)
- Video: `google/veo-3.1-generate-preview` (recommended) or `openai/sora-2`
- Chat: `gpt-4.1` (recommended) or any OpenAI-compatible model

## Troubleshooting

### "No module named 'tools'" or similar import errors
Run from the ViMax root directory:
```bash
cd /home/node/a0/workspace/527fb591-1439-4b5b-ad5d-90f972773f95/workspace/tmp/ViMax
.venv/bin/python main_happycapy_script2video.py
```

### API rate limit errors
Reduce `max_requests_per_minute` in the YAML config.

### Face identity drift in generated videos
- Add more physical detail to character descriptions in your script
- Use user-provided reference photos instead of AI-generated portraits
- Include extreme close-up shots for important characters
- Keep lighting consistent across scenes
