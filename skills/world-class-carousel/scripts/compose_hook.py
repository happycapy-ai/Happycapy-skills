#!/usr/bin/env python3
"""
Compose a viral-style hook slide from an AI-generated base image.
Adds: gradient overlay, headline text, brand watermark, swipe CTA.
Mirrors the visual style of @evolving.ai and @therundownai hooks.

Usage:
    python3 compose_hook.py --base base.png --output hook.png \
        --headline "AI IS MOVING FASTER THAN EVER" \
        --subhead "Here's what happened this week" \
        --brand "YOUR BRAND" \
        --category "AI NEWS"
"""
import argparse
from PIL import Image, ImageDraw, ImageFont
import os

# Instagram carousel dimensions
CANVAS_W, CANVAS_H = 1080, 1350


def load_font(size, bold=False):
    """Try to load a good font, fall back gracefully."""
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap_text(text, font, max_width, draw):
    """Word-wrap text to fit within max_width."""
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
    return lines


def compose_hook(base_path, output_path, headline, subhead=None, brand=None, category=None):
    """Compose a viral hook slide from base image + text overlays."""

    # Load and resize base image to fill canvas
    base = Image.open(base_path).convert('RGB')

    # Resize to fill canvas (crop to aspect ratio first)
    base_ratio = base.width / base.height
    canvas_ratio = CANVAS_W / CANVAS_H

    if base_ratio > canvas_ratio:
        # Image is wider -- crop sides
        new_h = base.height
        new_w = int(new_h * canvas_ratio)
        left = (base.width - new_w) // 2
        base = base.crop((left, 0, left + new_w, new_h))
    else:
        # Image is taller -- crop top/bottom
        new_w = base.width
        new_h = int(new_w / canvas_ratio)
        top = (base.height - new_h) // 2
        base = base.crop((0, top, new_w, top + new_h))

    base = base.resize((CANVAS_W, CANVAS_H), Image.LANCZOS)

    # Create overlay layer
    overlay = Image.new('RGBA', (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Bottom gradient overlay (heavier at bottom for text readability)
    for y in range(CANVAS_H // 3, CANVAS_H):
        progress = (y - CANVAS_H // 3) / (CANVAS_H - CANVAS_H // 3)
        # Ease-in curve for more natural gradient
        alpha = int(220 * (progress ** 1.5))
        alpha = min(alpha, 220)
        draw.rectangle([(0, y), (CANVAS_W, y + 1)], fill=(0, 0, 0, alpha))

    # Light top gradient for brand area
    for y in range(0, CANVAS_H // 6):
        progress = 1.0 - (y / (CANVAS_H // 6))
        alpha = int(100 * (progress ** 2))
        draw.rectangle([(0, y), (CANVAS_W, y + 1)], fill=(0, 0, 0, alpha))

    # Composite overlay onto base
    canvas = base.convert('RGBA')
    canvas = Image.alpha_composite(canvas, overlay)

    # Now draw text elements
    draw = ImageDraw.Draw(canvas)
    margin = 60

    # Category label (e.g., "AI NEWS") -- top area if provided
    if category:
        cat_font = load_font(28, bold=False)
        cat_y = CANVAS_H - 380
        draw.text((margin, cat_y), category.upper(), font=cat_font, fill=(200, 200, 200, 230))

    # Brand watermark -- center, above headline
    if brand:
        brand_font = load_font(22, bold=True)
        bbox = draw.textbbox((0, 0), brand.upper(), font=brand_font)
        brand_w = bbox[2] - bbox[0]
        brand_x = (CANVAS_W - brand_w) // 2
        brand_y = CANVAS_H - 400 if category else CANVAS_H - 370
        draw.text((brand_x, brand_y), brand.upper(), font=brand_font, fill=(255, 255, 255, 180))

    # Main headline -- bold, large, bottom area
    headline_font = load_font(56, bold=True)
    headline_lines = wrap_text(headline.upper(), headline_font, CANVAS_W - margin * 2, draw)

    # Position headline from bottom up
    line_height = 68
    total_headline_h = len(headline_lines) * line_height
    headline_start_y = CANVAS_H - 140 - total_headline_h

    for i, line in enumerate(headline_lines):
        y = headline_start_y + i * line_height
        draw.text((margin, y), line, font=headline_font, fill=(255, 255, 255, 255))

    # Subhead if provided
    if subhead:
        sub_font = load_font(30, bold=False)
        sub_y = headline_start_y - 50
        draw.text((margin, sub_y), subhead, font=sub_font, fill=(220, 220, 220, 200))

    # "SWIPE FOR MORE" CTA at bottom
    cta_font = load_font(20, bold=False)
    cta_text = "SWIPE FOR MORE"
    bbox = draw.textbbox((0, 0), cta_text, font=cta_font)
    cta_w = bbox[2] - bbox[0]
    cta_x = (CANVAS_W - cta_w) // 2
    cta_y = CANVAS_H - 60

    # Draw subtle line above CTA
    line_w = 80
    line_y = cta_y - 15
    draw.rectangle([(CANVAS_W//2 - line_w, line_y), (CANVAS_W//2 + line_w, line_y + 1)], fill=(255, 255, 255, 100))
    draw.text((cta_x, cta_y), cta_text, font=cta_font, fill=(200, 200, 200, 160))

    # Slide counter (top right)
    counter_font = load_font(24, bold=True)
    draw.text((CANVAS_W - 120, 30), "1/8", font=counter_font, fill=(255, 255, 255, 180))

    # Convert back to RGB and save
    final = canvas.convert('RGB')
    final.save(output_path, 'PNG', quality=95)
    print(f"Hook slide saved: {output_path}")
    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compose viral hook slide")
    parser.add_argument("--base", required=True, help="Base AI image path")
    parser.add_argument("--output", required=True, help="Output path")
    parser.add_argument("--headline", required=True, help="Main headline text")
    parser.add_argument("--subhead", default=None, help="Subheadline text")
    parser.add_argument("--brand", default=None, help="Brand watermark text")
    parser.add_argument("--category", default=None, help="Category label (e.g., AI NEWS)")
    args = parser.parse_args()

    compose_hook(args.base, args.output, args.headline, args.subhead, args.brand, args.category)
