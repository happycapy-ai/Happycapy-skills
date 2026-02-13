#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-genai>=1.0.0",
#     "pillow>=10.0.0",
#     "requests>=2.31.0",
# ]
# ///
"""
Generate images using Google's Nano Banana Pro (Gemini 3 Pro Image) API.

Usage:
    python3 generate_image.py --prompt "your image description" --filename "output.png" [--resolution 1K|2K|4K] [--api-key KEY]

Multi-image editing (up to 14 images):
    python3 generate_image.py --prompt "combine these images" --filename "output.png" -i img1.png -i img2.png -i img3.png
"""

import argparse
import os
import sys
from pathlib import Path


def get_api_key(provided_key: str | None) -> tuple[str | None, bool]:
    """
    Get API key with priority order.
    Returns: (api_key, use_ai_gateway)

    Priority:
    1. AI_GATEWAY_API_KEY env var -> (key, True)
    2. --api-key argument -> (key, False)
    3. GEMINI_API_KEY env var -> (key, False)
    """
    # Check AI Gateway first (highest priority)
    ai_gateway_key = os.environ.get("AI_GATEWAY_API_KEY")
    if ai_gateway_key:
        return (ai_gateway_key, True)

    # Check command-line argument
    if provided_key:
        return (provided_key, False)

    # Check direct Gemini API key (lowest priority)
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if gemini_key:
        return (gemini_key, False)

    return (None, False)


def call_ai_gateway(api_key: str, prompt: str, input_images: list, resolution: str) -> bytes:
    """
    Call AI Gateway endpoint for image generation.
    Uses the HappyCapy AI Gateway format (compatible with OpenAI images API).
    Returns the generated image as bytes.
    """
    import requests
    import base64
    from io import BytesIO

    # HappyCapy AI Gateway - use clean base URL, not the OpenAI-specific one
    api_base = "https://ai-gateway.happycapy.ai/api/v1"
    gateway_url = f"{api_base}/images/generations"

    # Prepare the request payload - try with response_format: url (like generate-image does)
    payload = {
        "model": "google/gemini-3-pro-image-preview",  # Model with provider prefix
        "prompt": prompt,
        "response_format": "url",  # Request URL instead of base64
        "n": 1
    }

    # Note: AI Gateway's images/generations endpoint doesn't support input_images
    # For image-to-image, we would need a different endpoint or approach
    if input_images:
        print(f"Warning: AI Gateway images/generations endpoint doesn't support input images.")
        print(f"Ignoring {len(input_images)} input image(s) and generating from text only.")

    # Request headers (include Origin header as required by AI Gateway)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "Origin": "https://trickle.so",  # Required by AI Gateway
        "User-Agent": "Mozilla/5.0 (compatible; Nano-Banana-Pro/1.0)"
    }

    print(f"Calling AI Gateway at: {gateway_url}")
    print(f"Using model: google/gemini-3-pro-image-preview")

    response = requests.post(gateway_url, json=payload, headers=headers, timeout=120)

    if response.status_code != 200:
        raise Exception(f"AI Gateway request failed with status {response.status_code}: {response.text}")

    # Parse response (OpenAI-compatible format)
    result = response.json()

    # Extract image data from response
    # Expected format: {"data": [{"b64_json": "base64_encoded_image_data"}]} or {"data": [{"url": "..."}]}
    if "data" not in result or not result["data"]:
        raise Exception(f"No image data in AI Gateway response: {result}")

    image_data = result["data"][0]

    if "b64_json" in image_data:
        # Decode base64 image data
        b64_data = image_data["b64_json"]
        return base64.b64decode(b64_data)
    elif "url" in image_data:
        # If response contains URL instead, download it
        image_url = image_data["url"]
        print(f"Downloading image from: {image_url}")
        img_response = requests.get(image_url, timeout=60)
        if img_response.status_code == 200:
            return img_response.content
        else:
            raise Exception(f"Failed to download image from URL: {img_response.status_code}")
    else:
        raise Exception(f"No 'b64_json' or 'url' in response data: {image_data}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Nano Banana Pro (Gemini 3 Pro Image)"
    )
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Image description/prompt"
    )
    parser.add_argument(
        "--filename", "-f",
        required=True,
        help="Output filename (e.g., sunset-mountains.png)"
    )
    parser.add_argument(
        "--input-image", "-i",
        action="append",
        dest="input_images",
        metavar="IMAGE",
        help="Input image path(s) for editing/composition. Can be specified multiple times (up to 14 images)."
    )
    parser.add_argument(
        "--resolution", "-r",
        choices=["1K", "2K", "4K"],
        default="1K",
        help="Output resolution: 1K (default), 2K, or 4K"
    )
    parser.add_argument(
        "--api-key", "-k",
        help="Gemini API key (overrides GEMINI_API_KEY env var)"
    )

    args = parser.parse_args()

    # Get API key and determine method
    api_key, use_ai_gateway = get_api_key(args.api_key)
    if not api_key:
        print("Error: No API key provided.", file=sys.stderr)
        print("Please either:", file=sys.stderr)
        print("  1. Set AI_GATEWAY_API_KEY environment variable (for AI Gateway)", file=sys.stderr)
        print("  2. Provide --api-key argument (for direct Gemini API)", file=sys.stderr)
        print("  3. Set GEMINI_API_KEY environment variable (for direct Gemini API)", file=sys.stderr)
        sys.exit(1)

    # Debug output showing which method is being used
    if use_ai_gateway:
        print(f"Using AI Gateway (API key from AI_GATEWAY_API_KEY)")
    else:
        print(f"Using direct Gemini API")

    # Import PIL here to avoid slow import on error
    from PIL import Image as PILImage

    # Only initialize Gemini client if not using AI Gateway
    client = None
    if not use_ai_gateway:
        from google import genai
        from google.genai import types
        client = genai.Client(api_key=api_key)

    # Set up output path
    output_path = Path(args.filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Load input images if provided (up to 14 supported by Nano Banana Pro)
    input_images = []
    output_resolution = args.resolution
    if args.input_images:
        if len(args.input_images) > 14:
            print(f"Error: Too many input images ({len(args.input_images)}). Maximum is 14.", file=sys.stderr)
            sys.exit(1)

        max_input_dim = 0
        for img_path in args.input_images:
            try:
                img = PILImage.open(img_path)
                input_images.append(img)
                print(f"Loaded input image: {img_path}")

                # Track largest dimension for auto-resolution
                width, height = img.size
                max_input_dim = max(max_input_dim, width, height)
            except Exception as e:
                print(f"Error loading input image '{img_path}': {e}", file=sys.stderr)
                sys.exit(1)

        # Auto-detect resolution from largest input if not explicitly set
        if args.resolution == "1K" and max_input_dim > 0:  # Default value
            if max_input_dim >= 3000:
                output_resolution = "4K"
            elif max_input_dim >= 1500:
                output_resolution = "2K"
            else:
                output_resolution = "1K"
            print(f"Auto-detected resolution: {output_resolution} (from max input dimension {max_input_dim})")

    # Build contents (images first if editing, prompt only if generating)
    if input_images:
        contents = [*input_images, args.prompt]
        img_count = len(input_images)
        print(f"Processing {img_count} image{'s' if img_count > 1 else ''} with resolution {output_resolution}...")
    else:
        contents = args.prompt
        print(f"Generating image with resolution {output_resolution}...")

    try:
        if use_ai_gateway:
            # Use AI Gateway
            image_data = call_ai_gateway(api_key, args.prompt, input_images, output_resolution)

            # Convert to PIL Image and save
            from io import BytesIO
            image = PILImage.open(BytesIO(image_data))

            # Ensure RGB mode for PNG
            if image.mode == 'RGBA':
                rgb_image = PILImage.new('RGB', image.size, (255, 255, 255))
                rgb_image.paste(image, mask=image.split()[3])
                rgb_image.save(str(output_path), 'PNG')
            elif image.mode == 'RGB':
                image.save(str(output_path), 'PNG')
            else:
                image.convert('RGB').save(str(output_path), 'PNG')

            full_path = output_path.resolve()
            print(f"\nImage saved: {full_path}")
            print(f"MEDIA: {full_path}")

        else:
            # Use direct Gemini API
            from google.genai import types

            response = client.models.generate_content(
                model="gemini-3-pro-image-preview",
                contents=contents,
                config=types.GenerateContentConfig(
                    response_modalities=["TEXT", "IMAGE"],
                    image_config=types.ImageConfig(
                        image_size=output_resolution
                    )
                )
            )

            # Process response and convert to PNG
            image_saved = False
            for part in response.parts:
                if part.text is not None:
                    print(f"Model response: {part.text}")
                elif part.inline_data is not None:
                    # Convert inline data to PIL Image and save as PNG
                    from io import BytesIO

                    # inline_data.data is already bytes, not base64
                    image_data = part.inline_data.data
                    if isinstance(image_data, str):
                        # If it's a string, it might be base64
                        import base64
                        image_data = base64.b64decode(image_data)

                    image = PILImage.open(BytesIO(image_data))

                    # Ensure RGB mode for PNG (convert RGBA to RGB with white background if needed)
                    if image.mode == 'RGBA':
                        rgb_image = PILImage.new('RGB', image.size, (255, 255, 255))
                        rgb_image.paste(image, mask=image.split()[3])
                        rgb_image.save(str(output_path), 'PNG')
                    elif image.mode == 'RGB':
                        image.save(str(output_path), 'PNG')
                    else:
                        image.convert('RGB').save(str(output_path), 'PNG')
                    image_saved = True

            if image_saved:
                full_path = output_path.resolve()
                print(f"\nImage saved: {full_path}")
                # OpenClaw parses MEDIA tokens and will attach the file on supported providers.
                print(f"MEDIA: {full_path}")
            else:
                print("Error: No image was generated in the response.", file=sys.stderr)
                sys.exit(1)

    except Exception as e:
        print(f"Error generating image: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
