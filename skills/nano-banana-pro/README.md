# Nano Banana Pro

Generate or edit images using Google's Gemini 3 Pro Image API (Nano Banana Pro).

## Features

- **Text-to-Image Generation**: Create images from text descriptions
- **Image Editing**: Modify existing images with natural language instructions
- **Multi-Image Composition**: Combine up to 14 images into a single scene
- **Flexible Resolutions**: Support for 1K, 2K, and 4K output

## Requirements

- `uv` package manager (install via Homebrew: `brew install uv`)
- `GEMINI_API_KEY` environment variable with your Google API key

## Usage

### Generate a new image

```bash
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "a serene mountain landscape at sunset" \
  --filename "sunset-mountains.png" \
  --resolution 2K
```

### Edit an existing image

```bash
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "add northern lights to the sky" \
  --filename "edited-mountains.png" \
  --input-image sunset-mountains.png \
  --resolution 2K
```

### Combine multiple images

```bash
uv run ~/.claude/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "create a collage of these vacation photos" \
  --filename "vacation-collage.png" \
  -i photo1.png -i photo2.png -i photo3.png
```

## Configuration

Set your API key via environment variable:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

Or configure it in OpenClaw's config file at `~/.openclaw/openclaw.json`:

```json
{
  "skills": {
    "nano-banana-pro": {
      "apiKey": "your-api-key-here"
    }
  }
}
```

## Installation

```bash
# Install to Claude Code skills directory
mkdir -p ~/.claude/skills
cp -r nano-banana-pro ~/.claude/skills/
```

## Notes

- Supported resolutions: `1K` (default), `2K`, `4K`
- Use timestamp-based filenames for organization: `2026-02-04-14-30-00-description.png`
- The script automatically handles image format conversion to PNG
- On supported platforms, generated images are automatically attached to the chat

## Original Source

[openclaw/openclaw](https://github.com/openclaw/openclaw/tree/main/skills/nano-banana-pro)
