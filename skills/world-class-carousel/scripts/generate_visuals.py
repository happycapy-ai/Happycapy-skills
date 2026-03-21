#!/usr/bin/env python3
"""
Carousel Visual Generator

Generates AI images for carousel slides based on topic, archetype, and style.
Uses the generate-image skill's API to create:
  - Hook slide backgrounds (dramatic, attention-grabbing)
  - Body slide backgrounds (subtle, text-friendly)
  - Accent illustrations (topic-specific diagrams/icons)
  - Synthesis slide visuals (save-worthy, summary)

Outputs images to a specified directory, named by slide role and ready
for compositing with render_slide.py.

Usage:
    python3 generate_visuals.py --topic "AI Prompting" --style tech --archetype framework --output-dir tmp/carousel/
    python3 generate_visuals.py --topic "Productivity" --style business --archetype tutorial --output-dir tmp/carousel/ --slides hook,body,accent,synthesis
    python3 generate_visuals.py --prompt "custom prompt" --output tmp/carousel/custom.png  (single image mode)
"""

import argparse
import base64
import json
import os
import sys
from pathlib import Path
from urllib import request
from urllib.error import HTTPError, URLError

# === STYLE-TO-PROMPT MAPPINGS ===

STYLE_AESTHETICS = {
    "tech": {
        "bg_mood": "dark, futuristic, deep indigo and purple, subtle geometric patterns, clean and minimal",
        "accent_mood": "neon purple and blue glow, circuit board patterns, clean vector illustration on dark background",
        "palette_desc": "dark navy/indigo/purple tones",
    },
    "business": {
        "bg_mood": "warm amber and orange, painterly oil texture, golden light, rich professional warmth",
        "accent_mood": "warm gold and amber tones, clean flat design, professional and bold on warm background",
        "palette_desc": "warm amber/orange/gold tones",
    },
    "education": {
        "bg_mood": "clean white and pale blue, subtle dotted grid, floating geometric shapes, minimalist modern",
        "accent_mood": "clean blue and white, flat educational diagram style, precise and clear on light background",
        "palette_desc": "clean white/light blue tones",
    },
    "creative": {
        "bg_mood": "dark charcoal and black, scattered pink and gold particle effects, moody film grain texture",
        "accent_mood": "hot pink and gold neon, artistic and expressive, stylized vector on dark background",
        "palette_desc": "dark charcoal with pink/gold accents",
    },
    "mindset": {
        "bg_mood": "warm earthy beige and sage green, natural linen texture, watercolor wash, organic flowing shapes",
        "accent_mood": "earth tones and green, organic natural illustration, hand-drawn feel on beige background",
        "palette_desc": "earthy beige/sage/green tones",
    },
}

# What visuals each slide role needs
SLIDE_ROLE_TEMPLATES = {
    "hook": {
        "type": "background",
        "layout": "full_bg",
        "prompt_template": "Dramatic eye-catching {bg_mood}, abstract background that creates urgency and curiosity about {topic}, no text no objects no people, suitable as background for bold typography overlay, 4:5 portrait aspect ratio",
    },
    "body": {
        "type": "background",
        "layout": "hero_top",
        "prompt_template": "Subtle {bg_mood}, abstract background that supports content about {topic}, very understated and text-friendly, no text no objects no people, 4:5 portrait aspect ratio",
    },
    "accent": {
        "type": "accent",
        "layout": "accent_float",
        "prompt_template": "Minimalist flat illustration representing {topic_concept}, {accent_mood}, centered composition, no text, clean and modern, conceptual diagram or icon style",
    },
    "synthesis": {
        "type": "background",
        "layout": "full_bg",
        "prompt_template": "Visually rich and memorable {bg_mood}, abstract background that feels like a conclusion or achievement related to {topic}, inspiring and save-worthy, no text no objects no people, 4:5 portrait aspect ratio",
    },
    "cta": {
        "type": "background",
        "layout": "full_bg",
        "prompt_template": "Clean and inviting {bg_mood}, soft abstract background with gentle gradient, welcoming and warm, no text no objects no people, suitable for call-to-action text overlay, 4:5 portrait aspect ratio",
    },
}

# Archetype-specific concept keywords for accent images
ARCHETYPE_CONCEPTS = {
    "tutorial": "step-by-step process, workflow diagram, connected steps",
    "framework": "interconnected system, framework diagram, interlocking components",
    "myth_buster": "broken chain or shattered glass, revealing truth behind illusion",
    "case_study": "growth chart, transformation before and after, measurable results",
    "curated_list": "organized collection, curated grid of items, catalog",
    "deep_dive": "magnifying glass revealing layers, deep ocean exploration, cross-section",
    "transformation": "butterfly emerging from cocoon, metamorphosis, dramatic change",
}


def generate_image_api(prompt, output_path, model="google/gemini-3.1-flash-image-preview"):
    """Call the AI Gateway API to generate an image."""
    api_key = os.environ.get("AI_GATEWAY_API_KEY")
    if not api_key:
        print("Error: AI_GATEWAY_API_KEY environment variable is required.", file=sys.stderr)
        return False

    payload = {
        "model": model,
        "prompt": prompt,
        "response_format": "b64_json",
        "n": 1,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "Origin": "https://trickle.so",
        "User-Agent": "Mozilla/5.0 (compatible; AI-Gateway-Client/1.0)",
    }

    try:
        req = request.Request(
            "https://ai-gateway.happycapy.ai/api/v1/images/generations",
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )

        with request.urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))

        if "data" not in result or not result["data"]:
            print("Error: No image data in response", file=sys.stderr)
            return False

        b64_data = result["data"][0].get("b64_json")
        if not b64_data:
            print("Error: No base64 data in response", file=sys.stderr)
            return False

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(b64_data))

        return True

    except HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"HTTP Error {e.code}: {error_body}", file=sys.stderr)
        return False
    except URLError as e:
        print(f"Network Error: {e.reason}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return False


def build_prompt(role, topic, style, topic_concept=None):
    """Build a generation prompt for a specific slide role, topic, and style."""
    aesthetics = STYLE_AESTHETICS.get(style, STYLE_AESTHETICS["tech"])
    template = SLIDE_ROLE_TEMPLATES.get(role, SLIDE_ROLE_TEMPLATES["body"])

    prompt = template["prompt_template"].format(
        topic=topic,
        topic_concept=topic_concept or topic,
        bg_mood=aesthetics["bg_mood"],
        accent_mood=aesthetics["accent_mood"],
        palette_desc=aesthetics["palette_desc"],
    )

    return prompt


def get_template_fallback(role, style):
    """Return path to a pre-generated template image as fallback."""
    template_dir = Path(__file__).parent.parent / "templates" / "images"

    if role in ("hook", "body", "synthesis", "cta"):
        fallback = template_dir / f"bg_{style}.png"
    else:
        # accent images -- pick based on common themes
        fallback = template_dir / "accent_idea.png"

    if fallback.exists():
        return str(fallback)
    return None


def generate_carousel_visuals(topic, style, archetype, output_dir, slides=None, model=None):
    """Generate all visual assets for a carousel.

    Args:
        topic: The carousel topic (e.g., "AI Prompting Techniques")
        style: Visual style (tech, business, education, creative, mindset)
        archetype: Content archetype (tutorial, framework, myth_buster, etc.)
        output_dir: Directory to save generated images
        slides: Comma-separated list of slide roles to generate (default: hook,body,accent,synthesis)
        model: AI model to use (default: google/gemini-3.1-flash-image-preview)

    Returns:
        dict: Mapping of slide role -> {"path": str, "layout": str, "source": "generated"|"template"}
    """
    if model is None:
        model = "google/gemini-3.1-flash-image-preview"

    if slides is None:
        slides = ["hook", "body", "accent", "synthesis"]
    elif isinstance(slides, str):
        slides = [s.strip() for s in slides.split(",")]

    os.makedirs(output_dir, exist_ok=True)

    # Get archetype-specific concept for accent images
    concept = ARCHETYPE_CONCEPTS.get(archetype, topic)

    results = {}

    for role in slides:
        output_path = os.path.join(output_dir, f"visual_{role}.png")
        prompt = build_prompt(role, topic, style, topic_concept=concept)
        layout = SLIDE_ROLE_TEMPLATES.get(role, {}).get("layout", "gradient_only")

        print(f"\n--- Generating: {role} ({layout}) ---")
        print(f"Prompt: {prompt[:120]}...")

        success = generate_image_api(prompt, output_path, model=model)

        if success:
            file_size = os.path.getsize(output_path) // 1024
            print(f"Generated: {output_path} ({file_size}KB)")
            results[role] = {"path": output_path, "layout": layout, "source": "generated"}
        else:
            # Fall back to template image
            fallback = get_template_fallback(role, style)
            if fallback:
                print(f"Using template fallback: {fallback}")
                results[role] = {"path": fallback, "layout": layout, "source": "template"}
            else:
                print(f"Warning: No image available for {role}", file=sys.stderr)
                results[role] = {"path": None, "layout": "gradient_only", "source": "none"}

    # Save manifest
    manifest_path = os.path.join(output_dir, "visuals_manifest.json")
    with open(manifest_path, "w") as f:
        json.dump({
            "topic": topic,
            "style": style,
            "archetype": archetype,
            "model": model,
            "visuals": results,
        }, f, indent=2)
    print(f"\nManifest: {manifest_path}")

    return results


def main():
    parser = argparse.ArgumentParser(description="Generate AI visuals for carousel slides")

    # Full carousel mode
    parser.add_argument("--topic", type=str, help="Carousel topic")
    parser.add_argument("--style", type=str, default="tech",
                        choices=list(STYLE_AESTHETICS.keys()), help="Visual style")
    parser.add_argument("--archetype", type=str, default="framework",
                        choices=list(ARCHETYPE_CONCEPTS.keys()), help="Content archetype")
    parser.add_argument("--output-dir", type=str, help="Output directory for generated images")
    parser.add_argument("--slides", type=str, default="hook,body,accent,synthesis",
                        help="Comma-separated slide roles to generate (default: hook,body,accent,synthesis)")
    parser.add_argument("--model", type=str, default="google/gemini-3.1-flash-image-preview",
                        help="AI model for image generation")

    # Single image mode
    parser.add_argument("--prompt", type=str, help="Custom prompt for single image generation")
    parser.add_argument("--output", type=str, help="Output path for single image")

    args = parser.parse_args()

    if args.prompt and args.output:
        # Single image mode
        print(f"Generating single image...")
        print(f"Prompt: {args.prompt[:120]}...")
        success = generate_image_api(args.prompt, args.output, model=args.model)
        if success:
            print(f"Saved: {args.output}")
        else:
            print("Failed to generate image.", file=sys.stderr)
            sys.exit(1)

    elif args.topic and args.output_dir:
        # Full carousel mode
        print(f"Generating carousel visuals for: {args.topic}")
        print(f"Style: {args.style} | Archetype: {args.archetype}")
        print(f"Slides: {args.slides}")
        print(f"Model: {args.model}")

        results = generate_carousel_visuals(
            topic=args.topic,
            style=args.style,
            archetype=args.archetype,
            output_dir=args.output_dir,
            slides=args.slides,
            model=args.model,
        )

        # Summary
        print(f"\n=== Summary ===")
        generated = sum(1 for v in results.values() if v["source"] == "generated")
        templates = sum(1 for v in results.values() if v["source"] == "template")
        print(f"Generated: {generated} | Template fallbacks: {templates}")
        for role, info in results.items():
            src = info["source"]
            layout = info["layout"]
            path = info["path"] or "(none)"
            print(f"  {role}: {layout} [{src}] -> {path}")

    else:
        parser.print_help()
        print("\nExamples:")
        print('  python3 generate_visuals.py --topic "AI Prompting" --style tech --archetype framework --output-dir tmp/carousel/')
        print('  python3 generate_visuals.py --prompt "abstract dark gradient" --output tmp/bg.png')
        sys.exit(1)


if __name__ == "__main__":
    main()
