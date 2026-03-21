#!/usr/bin/env python3
"""
World-Class Carousel Assembly Script

Assembles individual carousel slide PNGs into a final package:
- Validates all slides are 1080x1350
- Optimizes file sizes
- Generates a preview grid
- Copies slides with sequential naming
- Creates a metadata summary

Usage:
    python3 assemble_carousel.py --input-dir tmp/carousel/ --output-dir outputs/carousel/ --optimize
"""

import argparse
import glob
import os
import shutil
import json
from datetime import datetime
from PIL import Image


def validate_slide(filepath, expected_width=1080, expected_height=1350):
    """Validate a slide image meets specifications."""
    try:
        img = Image.open(filepath)
        w, h = img.size
        if w != expected_width or h != expected_height:
            return False, f"Wrong dimensions: {w}x{h} (expected {expected_width}x{expected_height})"
        return True, "OK"
    except Exception as e:
        return False, str(e)


def optimize_png(filepath, quality=85):
    """Optimize PNG file size while maintaining quality."""
    img = Image.open(filepath)
    # Convert to RGB if RGBA (Instagram doesn't need alpha)
    if img.mode == "RGBA":
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        img = bg
    elif img.mode != "RGB":
        img = img.convert("RGB")
    img.save(filepath, "PNG", optimize=True)
    return os.path.getsize(filepath)


def create_preview_grid(slide_paths, output_path, cols=5):
    """Create a preview grid of all slides."""
    if not slide_paths:
        return

    # Thumbnail size
    thumb_w, thumb_h = 216, 270  # 1/5 of original

    rows = (len(slide_paths) + cols - 1) // cols
    grid_w = cols * thumb_w + (cols + 1) * 10
    grid_h = rows * thumb_h + (rows + 1) * 10

    grid = Image.new("RGB", (grid_w, grid_h), (30, 30, 30))

    for i, path in enumerate(slide_paths):
        row = i // cols
        col = i % cols
        x = 10 + col * (thumb_w + 10)
        y = 10 + row * (thumb_h + 10)

        try:
            thumb = Image.open(path)
            thumb = thumb.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
            grid.paste(thumb, (x, y))
        except Exception:
            pass

    grid.save(output_path, "PNG")
    print(f"Preview grid: {output_path}")


def assemble(input_dir, output_dir, optimize=True, caption_file=None, music_file=None):
    """Assemble carousel from individual slides."""

    # Find all PNG slides in input directory
    patterns = [
        os.path.join(input_dir, "slide_*.png"),
        os.path.join(input_dir, "slide*.png"),
        os.path.join(input_dir, "*.png"),
    ]

    slide_paths = []
    for pattern in patterns:
        found = sorted(glob.glob(pattern))
        if found:
            slide_paths = found
            break

    if not slide_paths:
        print(f"ERROR: No PNG slides found in {input_dir}")
        return False

    print(f"Found {len(slide_paths)} slides")

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Validate and copy slides
    valid_slides = []
    for i, src in enumerate(slide_paths):
        is_valid, msg = validate_slide(src)
        slide_num = i + 1
        dst = os.path.join(output_dir, f"slide_{slide_num:02d}.png")

        if not is_valid:
            print(f"  WARNING: Slide {slide_num} ({os.path.basename(src)}): {msg}")
            # Copy anyway but warn

        shutil.copy2(src, dst)

        if optimize:
            size = optimize_png(dst)
            print(f"  Slide {slide_num}: {os.path.basename(src)} -> {dst} ({size // 1024}KB)")
        else:
            size = os.path.getsize(dst)
            print(f"  Slide {slide_num}: {os.path.basename(src)} -> {dst} ({size // 1024}KB)")

        valid_slides.append(dst)

    # Create preview grid
    grid_path = os.path.join(output_dir, "preview_grid.png")
    create_preview_grid(valid_slides, grid_path)

    # Copy caption if provided
    if caption_file and os.path.exists(caption_file):
        shutil.copy2(caption_file, os.path.join(output_dir, "caption.txt"))
        print(f"  Caption: {caption_file}")

    # Copy music recommendation if provided
    if music_file and os.path.exists(music_file):
        shutil.copy2(music_file, os.path.join(output_dir, "music_recommendation.txt"))
        print(f"  Music: {music_file}")

    # Generate metadata
    metadata = {
        "created": datetime.now().isoformat(),
        "total_slides": len(valid_slides),
        "dimensions": "1080x1350",
        "aspect_ratio": "4:5",
        "format": "PNG",
        "slides": [os.path.basename(s) for s in valid_slides],
        "total_size_kb": sum(os.path.getsize(s) for s in valid_slides) // 1024,
    }

    meta_path = os.path.join(output_dir, "metadata.json")
    with open(meta_path, "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"\nCarousel assembled: {len(valid_slides)} slides in {output_dir}")
    print(f"Total size: {metadata['total_size_kb']}KB")
    print(f"Preview: {grid_path}")
    print(f"Metadata: {meta_path}")

    return True


def main():
    parser = argparse.ArgumentParser(description="Assemble carousel slides into final package")
    parser.add_argument("--input-dir", type=str, required=True, help="Directory containing slide PNGs")
    parser.add_argument("--output-dir", type=str, required=True, help="Output directory for assembled carousel")
    parser.add_argument("--optimize", action="store_true", help="Optimize PNG file sizes")
    parser.add_argument("--caption", type=str, help="Path to caption text file")
    parser.add_argument("--music-rec", type=str, help="Path to music recommendation file")

    args = parser.parse_args()

    assemble(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        optimize=args.optimize,
        caption_file=args.caption,
        music_file=args.music_rec,
    )


if __name__ == "__main__":
    main()
