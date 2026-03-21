#!/usr/bin/env python3
"""
Carousel Orchestrator - End-to-end carousel generation from a slide spec.

Takes a JSON carousel specification (topic, slides, theme) and orchestrates:
  1. Paper texture generation (AI image generation)
  2. Product screenshot capture (browser automation)
  3. Slide-by-slide LaTeX rendering
  4. Preview grid assembly
  5. Final output packaging

Usage:
  python3 generate_carousel.py --spec carousel_spec.json --output-dir outputs/my-carousel/
  python3 generate_carousel.py --spec carousel_spec.json --output-dir outputs/my-carousel/ --texture path/to/texture.png

Spec format (JSON):
{
  "topic": "6 AI Tools That Will Replace Your Tech Stack",
  "brand": "AI Builder",
  "theme": "warm",
  "slides": [
    {"type": "hook", "data": {...}},
    {"type": "tool", "data": {...}},
    ...
  ]
}
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

SCRIPT_DIR = Path(__file__).parent
RENDERER = SCRIPT_DIR / "render_latex_slide.py"
VISUAL_GEN = SCRIPT_DIR / "generate_visuals.py"


def capture_screenshot(url, output_path, wait_seconds=3):
    """Capture a screenshot of a URL using the browser tool.

    Returns True if screenshot was saved successfully.
    Used for: real tool UIs, news articles, public profile photos, dashboards.
    """
    try:
        # Navigate to the URL
        result = subprocess.run(
            ["browser", "navigate", url],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0:
            print(f"  Warning: browser navigate failed for {url}", file=sys.stderr)
            return False

        # Take screenshot
        result = subprocess.run(
            ["browser", "screenshot"],
            capture_output=True, text=True, timeout=15,
        )

        # Find the screenshot file in /tmp/browser-session/
        import glob
        screenshots = sorted(glob.glob("/tmp/browser-session/screenshot-*.png"))
        if screenshots:
            # Copy the latest screenshot to the desired output path
            import shutil
            shutil.copy2(screenshots[-1], output_path)
            return os.path.exists(output_path)

        return False
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"  Warning: Screenshot capture failed: {e}", file=sys.stderr)
        return False


def capture_screenshots_for_spec(slides, output_dir):
    """Pre-capture all browser screenshots referenced in slide specs.

    Scans slides for 'screenshot_url' fields and captures them.
    Sets 'screenshot' in the slide data to the local file path.
    """
    captured = 0
    for i, slide in enumerate(slides):
        data = slide.get("data", {})
        url = data.get("screenshot_url", "")
        if not url:
            continue

        slide_num = str(i + 1).zfill(2)
        filename = f"screenshot_{slide_num}.png"
        local_path = os.path.join(output_dir, filename)

        if os.path.exists(local_path):
            # Already captured (e.g., re-run)
            data["screenshot"] = local_path
            captured += 1
            continue

        print(f"  Capturing screenshot: {url[:60]}...")
        if capture_screenshot(url, local_path):
            data["screenshot"] = local_path
            captured += 1
            print(f"    -> {filename}")
        else:
            print(f"    -> FAILED (slide will render without screenshot)")

    return captured


def generate_paper_texture(output_path, style="warm"):
    """Generate a paper texture using AI image generation."""
    style_prompts = {
        "warm": "Warm aged parchment paper texture, cream and light tan, subtle grain and fiber visible, vintage linen feel, soft lighting, no text no objects, seamless texture, high resolution",
        "clean": "Clean white paper texture with very subtle dot grid pattern, minimal and modern, crisp and bright, no text no objects, seamless texture, high resolution",
        "dark": "Dark charcoal textured paper, deep navy blue-black, subtle fabric weave visible, premium card stock feel, no text no objects, seamless texture, high resolution",
        "earth": "Natural kraft paper texture, warm beige with sage green undertones, organic linen fibers visible, earthy and organic, no text no objects, seamless texture, high resolution",
    }
    prompt = style_prompts.get(style, style_prompts["warm"])

    result = subprocess.run(
        [
            "python3", str(VISUAL_GEN),
            "--prompt", prompt,
            "--output", output_path,
        ],
        capture_output=True, text=True, timeout=120,
    )
    return os.path.exists(output_path)


def render_single_slide(slide_spec, output_path, theme, texture_path, brand_config_path=None):
    """Render a single slide from its spec."""
    slide_type = slide_spec["type"]
    data = slide_spec["data"]

    # Write data to temp JSON
    import tempfile
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(data, f)
        data_path = f.name

    cmd = [
        "python3", str(RENDERER),
        "--type", slide_type,
        "--data", data_path,
        "--output", output_path,
        "--theme", theme,
    ]
    if texture_path and os.path.exists(texture_path):
        cmd.extend(["--texture", texture_path])
    if brand_config_path and os.path.exists(brand_config_path):
        cmd.extend(["--brand", brand_config_path])

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return os.path.exists(output_path), result.stdout + result.stderr
    finally:
        os.unlink(data_path)


def create_preview_grid(slide_dir, output_path):
    """Create a preview grid of all slides."""
    from PIL import Image

    slides = sorted([
        f for f in os.listdir(slide_dir)
        if f.startswith("slide_") and f.endswith(".png")
    ])

    if not slides:
        return False

    n = len(slides)
    cols = min(n, 5)
    rows = (n + cols - 1) // cols

    thumb_w, thumb_h = 360, 450
    padding = 16
    grid_w = cols * thumb_w + (cols + 1) * padding
    grid_h = rows * thumb_h + (rows + 1) * padding

    canvas = Image.new("RGB", (grid_w, grid_h), (240, 235, 228))

    for i, slide_name in enumerate(slides):
        col = i % cols
        row = i // cols
        x = padding + col * (thumb_w + padding)
        y = padding + row * (thumb_h + padding)

        img = Image.open(os.path.join(slide_dir, slide_name))
        img = img.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
        canvas.paste(img, (x, y))

    canvas.save(output_path, "PNG", quality=95)
    return True


def main():
    parser = argparse.ArgumentParser(description="Generate a complete carousel from spec")
    parser.add_argument("--spec", required=True, help="Path to carousel spec JSON")
    parser.add_argument("--output-dir", required=True, help="Output directory for slides")
    parser.add_argument("--texture", help="Path to pre-generated paper texture (skips generation)")
    parser.add_argument("--brand", help="Path to brand config JSON (overrides spec brand name)")
    parser.add_argument("--no-preview", action="store_true", help="Skip preview grid generation")
    parser.add_argument("--parallel", type=int, default=3, help="Max parallel renders (default: 3)")

    args = parser.parse_args()

    # Load spec
    with open(args.spec) as f:
        spec = json.load(f)

    topic = spec.get("topic", "Untitled Carousel")
    brand = spec.get("brand", "Your Brand")
    theme = spec.get("theme", "warm")
    bg_style = spec.get("bg_style", None)  # gradient, gradient_mesh, solid, texture, or None
    slides = spec.get("slides", [])

    if not slides:
        print("Error: No slides in spec", file=sys.stderr)
        sys.exit(1)

    total = len(slides)
    print(f"Carousel: {topic}")
    print(f"Theme: {theme} | Slides: {total} | Brand: {brand}" +
          (f" | BG: {bg_style}" if bg_style else ""))

    os.makedirs(args.output_dir, exist_ok=True)

    # Step 1: Background style (default to gradient -- texture looks like grey rock)
    if bg_style is None:
        bg_style = "gradient"
    texture_path = args.texture
    needs_texture = bg_style == "texture"
    if needs_texture:
        if not texture_path or not os.path.exists(texture_path):
            texture_path = os.path.join(args.output_dir, "paper_texture.png")
            if not os.path.exists(texture_path):
                print(f"\nGenerating paper texture ({theme})...")
                success = generate_paper_texture(texture_path, theme)
                if success:
                    print(f"Texture: {texture_path}")
                else:
                    print("Warning: Texture generation failed, using flat color", file=sys.stderr)
                    texture_path = None
    else:
        print(f"\nBackground style: {bg_style} (skipping texture generation)")
        texture_path = None  # Not needed for gradient/solid/gradient_mesh

    # Step 2: Brand config
    brand_config_path = args.brand
    if not brand_config_path or not os.path.exists(brand_config_path):
        # Auto-create a minimal brand config from the spec
        brand_config_path = os.path.join(args.output_dir, "_brand_config.json")
        brand_config = {"name": brand}
        # Pull optional brand settings from spec
        if "accent_override" in spec:
            brand_config["accent_override"] = spec["accent_override"]
        if "header_style" in spec:
            brand_config["header_style"] = spec["header_style"]
        if "divider_style" in spec:
            brand_config["divider_style"] = spec["divider_style"]
        with open(brand_config_path, "w") as f:
            json.dump(brand_config, f)
        print(f"Brand config: auto-generated for '{brand}'")
    else:
        print(f"Brand config: {brand_config_path}")

    # Step 2b: Capture browser screenshots (for tool reviews, news, etc.)
    has_screenshots = any(s.get("data", {}).get("screenshot_url") for s in slides)
    if has_screenshots:
        print(f"\nCapturing browser screenshots...")
        n_captured = capture_screenshots_for_spec(slides, args.output_dir)
        print(f"Screenshots captured: {n_captured}")

    # Step 3: Inject slide numbering and bg_style into each slide
    for i, slide in enumerate(slides):
        slide["data"].setdefault("slide_num", i + 1)
        slide["data"].setdefault("total_slides", total)
        # Propagate spec-level bg_style to slides that don't have their own override
        if bg_style:
            slide["data"].setdefault("bg_style", bg_style)
        # Last slide typically has no nav arrow
        if i == total - 1:
            slide["data"].setdefault("show_nav", False)

    # Step 4: Render all slides
    print(f"\nRendering {total} slides...")
    results = {}

    for i, slide in enumerate(slides):
        slide_num = str(i + 1).zfill(2)
        slide_type = slide["type"]
        output_path = os.path.join(args.output_dir, f"slide_{slide_num}_{slide_type}.png")

        success, output = render_single_slide(slide, output_path, theme, texture_path, brand_config_path)
        status = "OK" if success else "FAIL"
        print(f"  [{status}] Slide {i+1}/{total}: {slide_type}")
        if not success:
            print(f"    {output[:200]}", file=sys.stderr)
        results[i] = {"path": output_path, "type": slide_type, "success": success}

    # Step 4: Preview grid
    if not args.no_preview:
        preview_path = os.path.join(args.output_dir, "preview_grid.png")
        print(f"\nCreating preview grid...")
        create_preview_grid(args.output_dir, preview_path)
        print(f"Preview: {preview_path}")

    # Step 5: Manifest
    manifest = {
        "topic": topic,
        "brand": brand,
        "theme": theme,
        "bg_style": bg_style or ("texture" if texture_path else "solid"),
        "total_slides": total,
        "slides": results,
        "texture": texture_path,
    }
    manifest_path = os.path.join(args.output_dir, "carousel_manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2, default=str)

    # Summary
    ok = sum(1 for r in results.values() if r["success"])
    print(f"\n=== Complete ===")
    print(f"Rendered: {ok}/{total} slides")
    print(f"Output: {args.output_dir}")
    print(f"Manifest: {manifest_path}")

    if ok < total:
        sys.exit(1)


if __name__ == "__main__":
    main()
