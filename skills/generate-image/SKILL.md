---
name: generate-image
description: Generate and transform images using AI Gateway API. Use when the user asks to create, generate, produce, or transform images, or work with image generation.
allowed-tools: Bash, Read
---

# Image Generation Skill

Generate images from text prompts and transform existing images using the AI Gateway API with support for multiple AI models including Google Gemini, Byteplus Seedream, and OpenAI GPT-Image.

## Overview

This Skill enables Claude to generate images from text descriptions and transform existing images with AI-powered modifications. It uses the AI Gateway API which routes requests to appropriate providers based on the model selected.

## Prerequisites

**Required Environment Variable:**
- `AI_GATEWAY_API_KEY`: Your AI Gateway API key

If this environment variable is not set, the scripts will fail with an error message asking you to provide it.

## Quick Start

### Generate an Image from Text

Use the bundled script to generate images from text descriptions:

```bash
python3 scripts/generate_image.py "A serene landscape with mountains and a lake at sunset, photorealistic style"
```

### Transform an Existing Image

Apply transformations to existing images using reference URLs:

```bash
python3 scripts/transform_image.py "Make this image more vibrant and add dramatic lighting" "https://example.com/image.jpg"
```

## Supported Models

### Image Generation Models

| Model | Provider | Best For |
|-------|----------|----------|
| `google/gemini-3.1-flash-image-preview` | Google Vertex AI | Latest fast image generation with improved quality |
| `google/gemini-3-pro-image-preview` | Google Vertex AI | High-quality photorealistic images |
| `google/gemini-2.5-flash-image` | Google Vertex AI | Fast image generation |
| `byteplus/seedream-4-5` | Byteplus Seedream | Creative artistic styles |
| `byteplus/seedream-4-0` | Byteplus Seedream | General purpose image generation |
| `openai/gpt-image-1` | OpenAI | Advanced image synthesis |
| `openai/gpt-image-1-mini` | OpenAI | Quick image generation |
| `openai/gpt-image-1.5` | OpenAI | Enhanced image synthesis |
| `openai/gpt-image-2` | OpenAI | Latest generation, multi-aspect ratio support |

## API Parameters

### Image Generation

- `prompt` (required): Text description of the desired image
- `model` (required): Model to use for generation
- `images` (optional): Array of reference image URLs for image-to-image transformation
- `response_format` (optional): "url" (default) or "b64_json"
- `n` (optional): Number of images to generate (default: 1)
- `size` (optional): Image dimensions (e.g., "1024x1024", "1792x1024", "1024x1792", "1536x1024", "1024x1536")
- `aspectRatio` (optional): Aspect ratio — alternative to `size`. Supported values: `"1:1"`, `"16:9"`, `"9:16"`, `"3:2"`, `"2:3"`, `"4:3"`, `"3:4"`, `"3:1"`, `"1:3"`
- `background` (optional, OpenAI models only): `"transparent"` | `"opaque"` | `"auto"` — controls background transparency
- `user` (optional): User identifier for tracking

### OpenAI gpt-image-2 / gpt-image-1.5 Parameters

These models support the full parameter set above. Key notes:
- Supports all aspect ratios via `aspectRatio` field
- Supports `background: "transparent"` for PNG output with transparency
- Use `response_format: "b64_json"` to receive raw image data; use `"url"` for a hosted URL
- Image editing (passing `images`) routes to the `/images/edits` endpoint automatically

## Bundled Scripts

### 1. generate_image.py

Generate images from text prompts with customizable parameters.

**Usage:**
```bash
python3 scripts/generate_image.py "prompt" [--model MODEL] [--output OUTPUT] [--format FORMAT]
```

**Options:**
- `--model`: Model to use (default: google/gemini-3.1-flash-image-preview)
- `--output`: Output file path (default: generated_image.png)
- `--format`: Response format - "url" or "b64_json" (default: b64_json)

**Example:**
```bash
python3 scripts/generate_image.py \
  "A futuristic city with flying cars at night, cyberpunk style" \
  --model "google/gemini-3.1-flash-image-preview" \
  --output "city.png"
```

### 2. transform_image.py

Transform existing images using AI with text instructions.

**Usage:**
```bash
python3 scripts/transform_image.py "prompt" "image_url" [--model MODEL] [--output OUTPUT]
```

**Example:**
```bash
python3 scripts/transform_image.py \
  "Make this image more vibrant and add dramatic sunset lighting" \
  "https://example.com/original.jpg" \
  --output "enhanced.png"
```

### 3. batch_generate.py

Generate multiple images in batch.

**Usage:**
```bash
python3 scripts/batch_generate.py prompts.txt [--model MODEL]
```

**Example prompts.txt:**
```
A sunset over the ocean
A mountain landscape at dawn
A bustling city street at night
```

## Implementation Notes

**When implementing image generation tasks:**

1. **Always use JavaScript for API calls** when writing custom code
2. **Check for API Key** at the start:
   ```javascript
   const apiKey = process.env.AI_GATEWAY_API_KEY;
   if (!apiKey) {
     throw new Error('AI_GATEWAY_API_KEY environment variable is required. Please set it with your AI Gateway API key.');
   }
   ```

3. **Use the bundled Python scripts** for quick generation tasks rather than writing custom code

4. **Include Origin header** in all API requests: Set `Origin: https://trickle.so` header for proper request routing

5. **Handle both streaming and non-streaming responses** appropriately

6. **Save generated images** to appropriate file paths and inform the user

## JavaScript Implementation Template

When you need to write custom JavaScript code for image generation:

```javascript
const apiKey = process.env.AI_GATEWAY_API_KEY;
if (!apiKey) {
  throw new Error('AI_GATEWAY_API_KEY environment variable is required. Please set it with your AI Gateway API key.');
}

const API_BASE = `${process.env.AI_GATEWAY_BASE_URL}/api/v1`;

async function generateImage(prompt, model = 'google/gemini-3.1-flash-image-preview') {
  const response = await fetch(`${API_BASE}/images/generations`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`,
      'Origin': 'https://trickle.so'
    },
    body: JSON.stringify({
      model,
      prompt,
      response_format: 'url'
    })
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status} ${response.statusText}`);
  }

  return await response.json();
}

// Use the function
const result = await generateImage('A beautiful sunset over mountains');
console.log('Generated image URL:', result.data[0].url);
```

## Error Handling

All scripts include comprehensive error handling for:
- Missing API key
- Network failures
- Invalid responses
- File I/O errors

Errors will include helpful messages to guide troubleshooting.

## Best Practices

1. **Be Specific in Prompts**: Include style, mood, lighting, and composition details
2. **Use Appropriate Models**: Choose models based on your quality vs. speed requirements
3. **Reference Images**: Use image-to-image transformation for style transfer or modifications
4. **Batch Processing**: Use the batch script for multiple generations to save time
5. **Save Outputs**: Always specify meaningful output file names for organization

## Troubleshooting

### "AI_GATEWAY_API_KEY environment variable is required"
Set the environment variable before running scripts:
```bash
export AI_GATEWAY_API_KEY="your-api-key-here"
```

### Network Errors
Check your internet connection and verify the API Gateway is accessible.

### Invalid Model Errors
Ensure you're using a valid model name from the supported models list above.

## Additional Resources

For more details on API parameters and response formats, see the API documentation at the AI Gateway repository.
