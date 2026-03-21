#!/usr/bin/env python3
"""
Generalized News Hook Slide Compositor
Matches @therundownai editorial style:
  - Real photo fills entire canvas
  - Subtle gradient at bottom for text
  - Small category label above headline
  - MASSIVE bold headline text
  - Optional brand mark top-left

Usage:
  python3 compose_news_hook.py \
    --base photo.png \
    --output hook.png \
    --headline "Turing Award winner credits Claude AI for solving a problem he had been stuck on for weeks" \
    --category "AI NEWS" \
    --brand "@DailyAINews"
"""

import argparse
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# === CONSTANTS ===
CANVAS_W = 1080
CANVAS_H = 1350

# Font paths (priority order)
FONT_PATHS = {
    "headline": [
        "/home/node/.local/share/fonts/Inter-Black.ttf",
        "/tmp/inter/extras/ttf/Inter-Black.ttf",
        "/home/node/.local/share/fonts/InterDisplay-ExtraBold.ttf",
        "/tmp/inter/extras/ttf/InterDisplay-ExtraBold.ttf",
        "/usr/share/fonts/opentype/cantarell/Cantarell-ExtraBold.otf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ],
    "category": [
        "/tmp/inter/extras/ttf/Inter-Bold.ttf",
        "/usr/share/fonts/opentype/inter/Inter-Bold.otf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ],
    "brand": [
        "/tmp/inter/extras/ttf/Inter-SemiBold.ttf",
        "/usr/share/fonts/opentype/inter/Inter-Bold.otf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ],
}


def find_font(role, size):
    """Find first available font for a given role."""
    for path in FONT_PATHS.get(role, []):
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def wrap_text(draw, text, font, max_width):
    """Word-wrap text to fit within max_width pixels."""
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


def find_optimal_font_size(draw, text, max_width, max_height, role="headline", min_size=40, max_size=80):
    """Find the largest font size that fits the text within bounds."""
    best_size = min_size

    for size in range(max_size, min_size - 1, -2):
        font = find_font(role, size)
        lines = wrap_text(draw, text, font, max_width)

        # Calculate total height
        line_height = int(size * 1.15)
        total_height = len(lines) * line_height

        if total_height <= max_height:
            return size, lines, font

    # Fallback to min size
    font = find_font(role, min_size)
    lines = wrap_text(draw, text, font, max_width)
    return min_size, lines, font


def compose_news_hook(
    base_path,
    output_path,
    headline,
    category="AI NEWS",
    brand=None,
    gradient_strength=0.85,
    gradient_start=0.40,
):
    """
    Compose a news hook slide in @therundownai editorial style.

    Args:
        base_path: Path to the base photo
        output_path: Path to save the composed slide
        headline: The headline text (will be auto-wrapped and auto-sized)
        category: Small category label above headline (e.g., "AI NEWS")
        brand: Optional brand/handle text for top-left
        gradient_strength: Max opacity of bottom gradient (0-1)
        gradient_start: Where gradient starts (0=top, 1=bottom)
    """
    # Load and resize base image to fill canvas
    base = Image.open(base_path).convert("RGBA")

    # Smart crop/resize to fill canvas
    base_ratio = base.width / base.height
    canvas_ratio = CANVAS_W / CANVAS_H

    if base_ratio > canvas_ratio:
        # Image is wider - fit height, crop width
        new_h = CANVAS_H
        new_w = int(CANVAS_H * base_ratio)
    else:
        # Image is taller - fit width, crop height
        new_w = CANVAS_W
        new_h = int(CANVAS_W / base_ratio)

    base = base.resize((new_w, new_h), Image.LANCZOS)

    # Center crop
    left = (new_w - CANVAS_W) // 2
    top = (new_h - CANVAS_H) // 2
    base = base.crop((left, top, left + CANVAS_W, top + CANVAS_H))

    canvas = base.copy()
    draw = ImageDraw.Draw(canvas)

    # === GRADIENT OVERLAY ===
    gradient = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    grad_draw = ImageDraw.Draw(gradient)

    gradient_start_y = int(CANVAS_H * gradient_start)
    gradient_end_y = CANVAS_H
    gradient_range = gradient_end_y - gradient_start_y

    for y in range(gradient_start_y, gradient_end_y):
        progress = (y - gradient_start_y) / gradient_range
        # Ease-in curve for natural gradient
        alpha = int(255 * gradient_strength * (progress ** 1.5))
        alpha = min(255, alpha)
        grad_draw.line([(0, y), (CANVAS_W, y)], fill=(0, 0, 0, alpha))

    canvas = Image.alpha_composite(canvas, gradient)
    draw = ImageDraw.Draw(canvas)

    # === TEXT LAYOUT ===
    margin_x = 60
    text_max_w = CANVAS_W - 2 * margin_x
    bottom_margin = 65

    # 1. Find optimal headline size
    # Headline should fill bottom 30-40% of canvas
    max_headline_h = int(CANVAS_H * 0.35)
    headline_size, headline_lines, headline_font = find_optimal_font_size(
        draw, headline, text_max_w, max_headline_h,
        role="headline", min_size=42, max_size=72
    )

    headline_line_h = int(headline_size * 1.15)
    total_headline_h = len(headline_lines) * headline_line_h

    # 2. Category label
    cat_font = find_font("category", 22)
    cat_h = 30
    gap_cat_headline = 16

    # 3. Calculate positions (bottom-anchored)
    headline_bottom = CANVAS_H - bottom_margin
    headline_top = headline_bottom - total_headline_h
    cat_y = headline_top - gap_cat_headline - cat_h

    # === DRAW TEXT ===

    # Category label
    if category:
        draw.text(
            (margin_x, cat_y),
            category.upper(),
            fill=(200, 200, 210),
            font=cat_font,
        )

    # Headline with text shadow
    for i, line in enumerate(headline_lines):
        y = headline_top + i * headline_line_h

        # Shadow (2px offset, dark)
        draw.text((margin_x + 2, y + 2), line, fill=(0, 0, 0, 180), font=headline_font)
        # Main text
        draw.text((margin_x, y), line, fill=(255, 255, 255), font=headline_font)

    # Brand mark (top-left)
    if brand:
        brand_font = find_font("brand", 20)
        draw.text((margin_x, 50), brand, fill=(220, 220, 225, 200), font=brand_font)

    # === SAVE ===
    final = canvas.convert("RGB")
    final.save(str(output_path), "PNG", quality=95)
    print(f"News hook saved: {output_path} ({Path(output_path).stat().st_size // 1024}KB)")
    return output_path


def main():
    parser = argparse.ArgumentParser(description="Compose news hook slide in editorial style")
    parser.add_argument("--base", required=True, help="Path to base photo")
    parser.add_argument("--output", required=True, help="Output PNG path")
    parser.add_argument("--headline", required=True, help="Headline text")
    parser.add_argument("--category", default="AI NEWS", help="Category label")
    parser.add_argument("--brand", default=None, help="Brand/handle text")
    parser.add_argument("--gradient-strength", type=float, default=0.85)
    parser.add_argument("--gradient-start", type=float, default=0.40)

    args = parser.parse_args()
    compose_news_hook(
        args.base, args.output, args.headline,
        category=args.category, brand=args.brand,
        gradient_strength=args.gradient_strength,
        gradient_start=args.gradient_start,
    )


if __name__ == "__main__":
    main()
