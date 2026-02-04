---
name: film-creator
description: |
  AI-powered film creation assistant that transforms a single sentence or image into a complete 30-second film.
  Automatically generates screenplay with scenes, dialogue, and camera directions, then produces cinematic video.
  Use when user wants to create a movie, film, or video story from text or image input.
  Trigger phrases: '创作电影', '生成电影', 'film creator', 'make a movie', 'create a film'.
allowed-tools: Bash, Read, Write, Edit
version: 1.0.0
license: MIT
---

# Film Creator - AI Film Production Assistant

Transform a single idea or image into a complete 30-second cinematic film with professional screenplay and video generation.

## Overview

This skill provides end-to-end film creation capabilities:
1. **Creative Analysis**: Analyzes text prompt or image to extract core creative elements
2. **Screenplay Generation**: Writes professional screenplay with scenes, dialogue, shot descriptions, and camera movements
3. **Scene Planning**: Breaks screenplay into 5-6 scenes (5 seconds each) optimized for video generation
4. **Video Production**: Generates high-quality video for each scene using AI Gateway
5. **Film Assembly**: Combines scenes into a cohesive 30-second film with transitions

## Prerequisites

**Required Environment Variable:**
- `AI_GATEWAY_API_KEY`: Your AI Gateway API key (automatically configured in HappyCapy)

**Required Tools:**
- Node.js 24+ (pre-installed in HappyCapy)
- FFmpeg (pre-installed in HappyCapy)

## Quick Start

### Create a Film from Text

```bash
node scripts/create_film.js "A lonely robot discovers the last flower on Earth"
```

### Create a Film from Image

```bash
node scripts/create_film.js --image "/path/to/image.jpg" "Transform this into a cinematic story"
```

### Create a Film with Custom Settings

```bash
node scripts/create_film.js \
  "A time traveler's final journey" \
  --model "openai/sora-2" \
  --aspect-ratio "16:9" \
  --output "my_film.mp4"
```

## Features

### Screenplay Generation
- **Story Structure**: Three-act structure adapted for 30-second format
- **Scene Breakdown**: 5-6 distinct scenes with clear transitions
- **Visual Descriptions**: Detailed shot compositions and camera movements
- **Cinematic Language**: Professional terminology (establishing shot, close-up, tracking shot, etc.)
- **Emotional Arc**: Clear beginning, middle, and end with emotional progression

### Video Generation
- **Multi-Scene Production**: Generates 5-6 individual scenes
- **Cinematic Quality**: Uses professional video generation models
- **Smart Prompting**: Converts screenplay into optimized video generation prompts
- **Continuity**: Maintains visual consistency across scenes

### Film Assembly
- **Scene Stitching**: Seamlessly combines individual scenes
- **Transitions**: Smooth cuts or fade transitions between scenes
- **Duration Control**: Precisely timed to 30 seconds total
- **Quality Preservation**: No re-encoding loss

## Supported Models

### Recommended for Film Creation

| Model | Best For | Duration per Scene |
|-------|----------|-------------------|
| `google/veo-3.1-generate-preview` | Balanced quality and reliability (Recommended) | 5-6 seconds |
| `openai/sora-2` | Cinematic quality with complex scenes | 4-6 seconds |
| `openai/sora-2-pro` | Professional-grade cinematic output | 4-6 seconds |
| `byteplus/seedance-1-0-pro` | Flexible aspect ratios | 5-6 seconds |

## Usage Examples

### Basic Film Creation

```bash
# From a simple concept
node scripts/create_film.js "A cat astronaut explores a distant planet"

# With specific genre
node scripts/create_film.js "A noir detective story set in the rain"

# From an uploaded image
node scripts/create_film.js --image "concept_art.jpg" "Make this into an epic adventure"
```

### Advanced Options

```bash
# Use premium model for highest quality
node scripts/create_film.js \
  "An emotional reunion at a train station" \
  --model "openai/sora-2-pro" \
  --output "reunion.mp4"

# Create vertical video for mobile
node scripts/create_film.js \
  "A day in the life of a street performer" \
  --aspect-ratio "9:16" \
  --model "byteplus/seedance-1-0-pro"

# Generate only the screenplay
node scripts/generate_screenplay.js "A magical library where books come alive"
```

## Workflow

### Step 1: Creative Analysis
The system analyzes your input (text or image) to identify:
- Core concept and theme
- Emotional tone
- Visual style
- Key story elements

### Step 2: Screenplay Writing
Generates a professional screenplay including:
- **Scene Headings**: INT./EXT. location and time
- **Action Lines**: Visual descriptions of what happens
- **Camera Directions**: Shot types and movements
- **Timing**: Duration for each scene

Example screenplay output:
```
FADE IN:

EXT. ABANDONED CITY - DAY

WIDE ESTABLISHING SHOT: A desolate cityscape covered in rust and vines.
The sun casts long shadows through broken buildings.

A small ROBOT (weathered, curious) rolls through debris, its single eye
scanning the ground.

CLOSE-UP: The robot's sensors light up as it detects something.

LOW ANGLE: The robot stops at a crack in the concrete where a single
FLOWER blooms in brilliant red.

EXTREME CLOSE-UP: The robot's optical lens focuses on the flower,
reflecting its petals.

The robot extends a gentle mechanical hand, not to touch, but to protect.

FADE OUT.
```

### Step 3: Scene-by-Scene Generation
Each scene is converted to an optimized video prompt:
- Camera angles and movements specified
- Visual details enhanced
- Lighting and mood emphasized
- Continuity elements maintained

### Step 4: Video Assembly
All scenes are combined with:
- Frame-accurate stitching
- Optional transitions (cut/fade)
- Audio-ready format (MP4)
- Optimized compression

## Command Reference

### create_film.js (Main Script)

**Parameters:**
- `prompt` (required): Text description or story concept
- `--image PATH` (optional): Image file to use as creative inspiration
- `--model MODEL` (optional): Video generation model (default: google/veo-3.1-generate-preview)
- `--aspect-ratio RATIO` (optional): Video aspect ratio (default: 16:9)
- `--output PATH` (optional): Output file path (default: generated_film.mp4)
- `--no-assembly` (optional): Generate scenes only, don't combine them
- `--transition TYPE` (optional): Transition type: "cut" or "fade" (default: cut)

### generate_screenplay.js

Generate screenplay without video production:
```bash
node scripts/generate_screenplay.js "Your story concept" [--output screenplay.txt]
```

### generate_scene.js

Generate a single scene from a prompt:
```bash
node scripts/generate_scene.js "Scene description with camera angles" [--model MODEL] [--duration SECONDS]
```

### assemble_film.js

Combine pre-generated scene videos:
```bash
node scripts/assemble_film.js scene1.mp4 scene2.mp4 scene3.mp4 --output final.mp4
```

## Best Practices

### Writing Effective Prompts

**Good prompts include:**
- Clear genre or style ("noir film", "whimsical animation style")
- Emotional core ("a story about hope", "bittersweet reunion")
- Visual anchors ("neon-lit city", "misty forest")
- Character elements ("lonely protagonist", "mischievous creature")

**Examples:**
```
✓ "A cyberpunk story about a hacker who discovers they're an AI"
✓ "A heartwarming tale of a child's robot friend, Studio Ghibli style"
✓ "A suspenseful noir detective story in the rain at night"
✓ "An epic space opera battle with massive starships"

✗ "Make a video"  (too vague)
✗ "Something cool"  (no direction)
```

### Model Selection

- **Use Google Veo 3.1** for most projects - excellent balance of quality and reliability
- **Use OpenAI Sora 2 Pro** for highest cinematic quality and complex physics
- **Use BytePlus Seedance** when you need non-standard aspect ratios (1:1, 9:16, 21:9)

### Image Input Tips

When using an image as input:
- Provide a complementary text prompt to guide the narrative
- The system will analyze visual elements (colors, composition, mood)
- Works best with conceptual or atmospheric images
- Character-focused images can become protagonists

### Duration Optimization

- Each scene is 5 seconds for optimal storytelling pace
- 6 scenes = 30 seconds total
- This pacing allows for:
  - Establishing shot
  - Rising action
  - Climax/key moment
  - Resolution
  - Emotional beat
  - Closing image

## Troubleshooting

### "Generation timeout" or "Scene generation failed"

Video generation can take time. The script automatically waits up to 5 minutes per scene. If it fails:
- Try a simpler prompt for that scene
- Use a faster model (google/veo-3.1-fast-generate-preview)
- Check your internet connection

### "FFmpeg error" during assembly

Ensure all scene files were generated successfully:
```bash
ls -lh scene_*.mp4
```

If some scenes are missing or corrupted, regenerate them individually:
```bash
node scripts/generate_scene.js "Scene description" --output scene_3.mp4
```

### Poor visual continuity between scenes

The screenplay generator aims for continuity, but AI models may interpret scenes differently. To improve:
- Add more specific visual details in your prompt
- Specify a consistent color palette or lighting
- Use model-specific style references

### "API key not found"

Set the environment variable:
```bash
export AI_GATEWAY_API_KEY="your-api-key-here"
```

## Technical Details

### Screenplay Format
The generated screenplay follows industry-standard formatting:
- Scene headings in caps
- Action lines in present tense
- Camera directions in caps or parentheses
- Timing notes for pacing

### Video Specifications
- **Format**: MP4 (H.264)
- **Resolution**: Model-dependent (typically 1280x720 or 1920x1080)
- **Frame Rate**: 24-30 fps
- **Duration**: Exactly 30 seconds
- **Aspect Ratios**: 16:9, 9:16, or custom (model-dependent)

### Assembly Process
Uses FFmpeg with:
- Lossless concatenation when possible
- Minimal re-encoding
- Frame-accurate cutting
- Preserved metadata

## Examples Gallery

### Example 1: Sci-Fi Short
**Prompt**: "A lonely robot discovers the last flower on Earth"

**Generated Screenplay** (abbreviated):
```
Scene 1: Wide shot of desolate cityscape
Scene 2: Robot character introduction
Scene 3: Discovery of flower (key moment)
Scene 4: Emotional close-up of robot's reaction
Scene 5: Robot protecting the flower
Scene 6: Hopeful closing image
```

### Example 2: Fantasy Adventure
**Prompt**: "A young wizard's first spell goes wonderfully wrong"

**Key Scenes**:
- Establishing: Magic academy interior
- Character: Nervous student with wand
- Action: Spell casting with dramatic effects
- Consequence: Humorous magical mishap
- Reaction: Wizard's surprise and laughter
- Resolution: Acceptance and learning moment

### Example 3: Noir Detective
**Prompt**: "A 1940s detective receives a mysterious case in the rain"

**Style Elements**:
- High contrast lighting (noir aesthetic)
- Rain effects and reflections
- Dramatic shadows
- Close-ups on key objects
- Moody, atmospheric tone

## Integration with Other Skills

This skill works well with:
- **generate-image**: Create concept art before film production
- **image-enhancer**: Improve reference images
- **video-frames**: Extract keyframes from generated films for editing

## Limitations

- Maximum duration: 30 seconds (by design)
- Scene count: 5-6 scenes (optimal for pacing)
- No dialogue audio (visual storytelling only)
- No custom music (silent film format)
- Limited character consistency across scenes (model limitation)

## Future Enhancements

Potential additions:
- Background music generation and integration
- Text-to-speech for dialogue
- Extended duration options (60s, 90s)
- Multi-character tracking
- Style transfer between reference and generated scenes
- Storyboard visualization before generation

## Credits

Built on top of:
- AI Gateway API (video generation)
- FFmpeg (video assembly)
- Node.js (orchestration)

## License

MIT License - Free to use and modify
