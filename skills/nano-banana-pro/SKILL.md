---
name: nano-banana-pro
description: Generate or edit images via Gemini 3 Pro Image (Nano Banana Pro) with AI Gateway support.
homepage: https://ai.google.dev/
metadata:
  {
    "openclaw":
      {
        "emoji": "🍌",
        "requires": { "bins": [], "env": [] },
        "primaryEnv": "AI_GATEWAY_API_KEY",
      },
  }
---

# Nano Banana Pro (Gemini 3 Pro Image)

Generate or edit images using Gemini 3 Pro Image via AI Gateway or direct API.

## Quick Start

Generate an image:

```bash
python3 {baseDir}/scripts/generate_image.py \
  --prompt "your image description" \
  --filename "output.png" \
  --resolution 1K
```

## Usage Examples

### Generate Image

```bash
python3 {baseDir}/scripts/generate_image.py \
  --prompt "a cute cat sitting on a wooden floor" \
  --filename "cat.png"
```

### Edit Image (requires GEMINI_API_KEY)

**Note**: Image editing currently requires direct Gemini API access.

```bash
export GEMINI_API_KEY="your-gemini-key"
python3 {baseDir}/scripts/generate_image.py \
  --prompt "make it more colorful" \
  --filename "cat-colorful.png" \
  -i "cat.png"
```

### Multi-image Composition (up to 14 images, requires GEMINI_API_KEY)

```bash
python3 {baseDir}/scripts/generate_image.py \
  --prompt "combine these into one scene" \
  --filename "combined.png" \
  -i img1.png -i img2.png -i img3.png
```

## API Key Configuration

The skill automatically detects API keys in this priority order:

1. **`AI_GATEWAY_API_KEY`** (recommended) - Uses AI Gateway
2. **`GEMINI_API_KEY`** - Direct Gemini API access
3. **`--api-key` argument** - Manual key override

### Recommended: AI Gateway (default)

```bash
export AI_GATEWAY_API_KEY="your-gateway-key"  # Usually pre-configured
```

✅ No additional dependencies required
✅ Cost-efficient and unified API management
❌ Image editing not currently supported

### Alternative: Direct Gemini API

```bash
export GEMINI_API_KEY="your-gemini-key"
```

✅ Supports image editing and multi-image composition
❌ Requires `google-genai` package: `pip install google-genai`

## Options

- `--prompt, -p`: Image description (required)
- `--filename, -f`: Output filename (required)
- `--resolution, -r`: Resolution (`1K`, `2K`, `4K`, default: `1K`)
- `--input-image, -i`: Input image(s) for editing (up to 14, requires GEMINI_API_KEY)
- `--api-key, -k`: Manual API key override

## Notes

- Resolutions: `1K` (default), `2K`, `4K`
- Use descriptive filenames with timestamps: `2024-12-31-cat.png`
- The script outputs a `MEDIA:` line for OpenClaw integration
- AI Gateway mode works with standard Python 3, no extra tools needed
