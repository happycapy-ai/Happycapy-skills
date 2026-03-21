#!/usr/bin/env python3
"""
World-Class Carousel Slide Renderer v2

Renders individual Instagram carousel slides at 1080x1350 using Pillow.
Now with advanced AI-image compositing: 6 layout modes that intelligently
integrate AI-generated visuals with typography.

Layout modes:
  gradient_only  -- Pure gradient background (fallback, no image needed)
  full_bg        -- AI image fills entire slide with overlay for text readability
  hero_top       -- AI image in top ~40%, text content below on gradient
  hero_bottom    -- Text content on top, AI image fills bottom ~40%
  accent_center  -- Gradient bg, AI image floats centered between title and body
  accent_float   -- AI image with rounded corners + shadow, text above/below

Usage:
    python3 render_slide.py --title "Title" --body "Text" --style tech --output slide.png
    python3 render_slide.py --title "Hook" --bg-image hero.png --layout full_bg --output slide.png
    python3 render_slide.py --title "Step 1" --bg-image diagram.png --layout hero_top --output slide.png
    python3 render_slide.py --title "Key Insight" --bg-image accent.png --layout accent_float --output slide.png
"""

import argparse
import os
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# === DESIGN SYSTEM CONSTANTS ===

WIDTH = 1080
HEIGHT = 1350
MARGIN = 60
SAFE_TOP = int(HEIGHT * 0.08)
SAFE_BOTTOM = int(HEIGHT * 0.88)
CONTENT_WIDTH = WIDTH - (2 * MARGIN)

# Font paths
FONT_DIR = "/usr/share/fonts/truetype"
FONTS = {
    "title": os.path.join(FONT_DIR, "noto/NotoSerifDisplay-Bold.ttf"),
    "title_regular": os.path.join(FONT_DIR, "noto/NotoSerif-Regular.ttf"),
    "subtitle": os.path.join(FONT_DIR, "noto/NotoSerif-Bold.ttf"),
    "body": os.path.join(FONT_DIR, "noto/NotoSans-Regular.ttf"),
    "body_bold": os.path.join(FONT_DIR, "noto/NotoSans-Bold.ttf"),
    "label": os.path.join(FONT_DIR, "noto/NotoSans-Regular.ttf"),
    "indicator": os.path.join(FONT_DIR, "noto/NotoSans-Regular.ttf"),
}

# Typography sizes
SIZES = {
    "title": 68,
    "subtitle": 36,
    "body": 26,
    "bullet": 24,
    "label": 18,
    "indicator": 16,
}

# Color palettes by style
PALETTES = {
    "tech": {
        "bg": "#0D1117",
        "bg_gradient_end": "#1A1A2E",
        "text_primary": "#E6EDF3",
        "text_secondary": "#8B949E",
        "accent": "#7C3AED",
        "accent_2": "#3B82F6",
        "title_underline": "#7C3AED",
        "bullet_dot": "#7C3AED",
        "indicator": "#6B7280",
    },
    "business": {
        "bg": "#F97316",
        "bg_gradient_end": "#EAB308",
        "text_primary": "#1C1917",
        "text_secondary": "#44403C",
        "accent": "#DC2626",
        "accent_2": "#F59E0B",
        "title_underline": "#1C1917",
        "bullet_dot": "#1C1917",
        "indicator": "#78716C",
    },
    "education": {
        "bg": "#F8FAFC",
        "bg_gradient_end": "#E2E8F0",
        "text_primary": "#0F172A",
        "text_secondary": "#475569",
        "accent": "#2563EB",
        "accent_2": "#0EA5E9",
        "title_underline": "#2563EB",
        "bullet_dot": "#2563EB",
        "indicator": "#64748B",
    },
    "creative": {
        "bg": "#18181B",
        "bg_gradient_end": "#27272A",
        "text_primary": "#FAFAFA",
        "text_secondary": "#A1A1AA",
        "accent": "#EC4899",
        "accent_2": "#F59E0B",
        "title_underline": "#EC4899",
        "bullet_dot": "#EC4899",
        "indicator": "#71717A",
    },
    "mindset": {
        "bg": "#F5F0EB",
        "bg_gradient_end": "#E8DFD5",
        "text_primary": "#2D2416",
        "text_secondary": "#6B5B3E",
        "accent": "#16A34A",
        "accent_2": "#B45309",
        "title_underline": "#16A34A",
        "bullet_dot": "#16A34A",
        "indicator": "#8B7355",
    },
}

LAYOUTS = ["gradient_only", "full_bg", "hero_top", "hero_bottom", "accent_center", "accent_float"]


# === IMAGE PROCESSING HELPERS ===

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple."""
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def smart_crop(img, target_w, target_h):
    """Center-crop an image to target aspect ratio, then resize.
    Handles landscape-to-portrait conversion gracefully."""
    src_w, src_h = img.size
    target_ratio = target_w / target_h
    src_ratio = src_w / src_h

    if src_ratio > target_ratio:
        # Source is wider -- crop sides
        new_w = int(src_h * target_ratio)
        left = (src_w - new_w) // 2
        img = img.crop((left, 0, left + new_w, src_h))
    elif src_ratio < target_ratio:
        # Source is taller -- crop top/bottom
        new_h = int(src_w / target_ratio)
        top = (src_h - new_h) // 2
        img = img.crop((0, top, src_w, top + new_h))

    return img.resize((target_w, target_h), Image.Resampling.LANCZOS)


def create_gradient(width, height, color1, color2, direction="vertical"):
    """Create a gradient background image."""
    img = Image.new("RGB", (width, height))
    draw = ImageDraw.Draw(img)
    r1, g1, b1 = hex_to_rgb(color1)
    r2, g2, b2 = hex_to_rgb(color2)

    if direction == "vertical":
        for y in range(height):
            ratio = y / height
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
    else:
        for x in range(width):
            ratio = x / width
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            draw.line([(x, 0), (x, height)], fill=(r, g, b))

    return img


def apply_overlay(img, color_hex, opacity):
    """Apply a semi-transparent color overlay to an image."""
    rgba = img.convert("RGBA")
    overlay = Image.new("RGBA", img.size, hex_to_rgb(color_hex) + (int(opacity * 255),))
    composited = Image.alpha_composite(rgba, overlay)
    return composited.convert("RGB")


def create_vertical_fade(width, height, color_hex, fade_from_top=True):
    """Create a vertical fade mask -- from transparent to solid color.
    Used to blend image regions into gradient backgrounds."""
    fade = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    r, g, b = hex_to_rgb(color_hex)

    for y in range(height):
        if fade_from_top:
            alpha = int(255 * (y / height))
        else:
            alpha = int(255 * (1 - y / height))
        for x in range(width):
            fade.putpixel((x, y), (r, g, b, alpha))

    return fade


def create_vertical_fade_fast(width, height, color_hex, fade_from_top=True):
    """Fast vertical fade using line drawing instead of putpixel."""
    fade = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(fade)
    r, g, b = hex_to_rgb(color_hex)

    for y in range(height):
        if fade_from_top:
            alpha = int(255 * (y / height) ** 1.5)  # ease-in curve
        else:
            alpha = int(255 * (1 - y / height) ** 1.5)
        draw.line([(0, y), (width, y)], fill=(r, g, b, alpha))

    return fade


def round_corners(img, radius):
    """Apply rounded corners to an image."""
    img = img.convert("RGBA")
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), img.size], radius=radius, fill=255)
    img.putalpha(mask)
    return img


def add_drop_shadow(img, offset=(8, 8), blur_radius=15, shadow_color=(0, 0, 0, 100)):
    """Add a drop shadow behind an image (must be RGBA)."""
    img = img.convert("RGBA")
    # Create shadow canvas (larger to accommodate blur)
    pad = blur_radius * 2
    shadow_canvas = Image.new("RGBA",
        (img.width + pad * 2, img.height + pad * 2), (0, 0, 0, 0))

    # Create shadow from alpha channel
    shadow = Image.new("RGBA", img.size, shadow_color)
    shadow.putalpha(img.split()[3])  # use source alpha as shadow shape

    # Paste shadow offset
    shadow_canvas.paste(shadow, (pad + offset[0], pad + offset[1]))
    shadow_canvas = shadow_canvas.filter(ImageFilter.GaussianBlur(blur_radius))

    # Paste original on top
    shadow_canvas.paste(img, (pad, pad), img)

    return shadow_canvas, pad  # return pad so caller knows the extra margin


# === LAYOUT COMPOSERS ===

def compose_gradient_only(width, height, palette):
    """Pure gradient background. No image."""
    return create_gradient(width, height, palette["bg"], palette["bg_gradient_end"])


def compose_full_bg(width, height, palette, bg_img):
    """AI image fills entire canvas. Semi-transparent overlay + bottom fade for text."""
    img = smart_crop(bg_img.convert("RGB"), width, height)

    # Darken overlay -- lighter for light palettes, heavier for dark
    bg_brightness = sum(hex_to_rgb(palette["bg"])) / 3
    if bg_brightness > 128:
        # Light palette: lighter overlay
        img = apply_overlay(img, palette["bg"], 0.35)
    else:
        # Dark palette: medium overlay
        img = apply_overlay(img, palette["bg"], 0.45)

    # Bottom gradient fade to solid bg color for text readability
    fade_height = height // 3
    fade = create_vertical_fade_fast(width, fade_height, palette["bg_gradient_end"], fade_from_top=True)
    img_rgba = img.convert("RGBA")
    img_rgba.paste(fade, (0, height - fade_height), fade)
    return img_rgba.convert("RGB")


def compose_hero_top(width, height, palette, bg_img):
    """AI image fills top portion, gradient background below for text."""
    # Image region: top 42% of canvas
    img_region_h = int(height * 0.42)
    text_region_h = height - img_region_h

    # Smart crop image to fill the top region
    cropped = smart_crop(bg_img.convert("RGB"), width, img_region_h)

    # Create gradient for bottom text area
    gradient = create_gradient(width, text_region_h, palette["bg"], palette["bg_gradient_end"])

    # Assemble
    canvas = Image.new("RGB", (width, height))
    canvas.paste(cropped, (0, 0))
    canvas.paste(gradient, (0, img_region_h))

    # Smooth blend zone between image and gradient (60px fade)
    blend_h = 80
    blend_zone = create_vertical_fade_fast(width, blend_h, palette["bg"], fade_from_top=True)
    canvas_rgba = canvas.convert("RGBA")
    canvas_rgba.paste(blend_zone, (0, img_region_h - blend_h // 2), blend_zone)

    return canvas_rgba.convert("RGB")


def compose_hero_bottom(width, height, palette, bg_img):
    """Text content on top on gradient, AI image fills bottom portion."""
    # Text region: top 55%, image: bottom 45%
    text_region_h = int(height * 0.55)
    img_region_h = height - text_region_h

    # Gradient for top text area
    gradient = create_gradient(width, text_region_h, palette["bg"], palette["bg_gradient_end"])

    # Smart crop image for bottom
    cropped = smart_crop(bg_img.convert("RGB"), width, img_region_h)

    # Assemble
    canvas = Image.new("RGB", (width, height))
    canvas.paste(gradient, (0, 0))
    canvas.paste(cropped, (0, text_region_h))

    # Blend zone
    blend_h = 80
    blend_zone = create_vertical_fade_fast(width, blend_h, palette["bg_gradient_end"], fade_from_top=False)
    canvas_rgba = canvas.convert("RGBA")
    canvas_rgba.paste(blend_zone, (0, text_region_h - blend_h // 3), blend_zone)

    return canvas_rgba.convert("RGB")


def compose_accent_center(width, height, palette, bg_img):
    """Gradient background with AI image placed as a centered accent block."""
    canvas = create_gradient(width, height, palette["bg"], palette["bg_gradient_end"])

    # Scale image to fit within accent area (max 700px wide, 400px tall)
    max_w, max_h = 700, 400
    img = bg_img.convert("RGB")
    scale = min(max_w / img.width, max_h / img.height, 1.0)
    new_size = (int(img.width * scale), int(img.height * scale))
    img = img.resize(new_size, Image.Resampling.LANCZOS)

    # Center horizontally, place in middle third vertically
    x = (width - new_size[0]) // 2
    y = int(height * 0.35)

    # Add subtle border using accent color
    border_w = 3
    draw = ImageDraw.Draw(canvas)
    draw.rectangle(
        [x - border_w, y - border_w, x + new_size[0] + border_w, y + new_size[1] + border_w],
        fill=hex_to_rgb(palette["accent"]),
    )
    canvas.paste(img, (x, y))

    return canvas


def compose_accent_float(width, height, palette, bg_img):
    """Gradient background with AI image floating with rounded corners + shadow."""
    canvas = create_gradient(width, height, palette["bg"], palette["bg_gradient_end"])

    # Scale image to fit nicely (max 800px wide, 450px tall)
    max_w, max_h = 800, 450
    img = bg_img.convert("RGBA")
    scale = min(max_w / img.width, max_h / img.height, 1.0)
    new_size = (int(img.width * scale), int(img.height * scale))
    img = img.resize(new_size, Image.Resampling.LANCZOS)

    # Round corners
    img = round_corners(img, 24)

    # Add drop shadow
    shadowed, pad = add_drop_shadow(img, offset=(6, 6), blur_radius=20, shadow_color=(0, 0, 0, 80))

    # Center horizontally, place in middle zone
    x = (width - shadowed.width) // 2
    y = int(height * 0.33)

    canvas_rgba = canvas.convert("RGBA")
    canvas_rgba.paste(shadowed, (x, y), shadowed)

    return canvas_rgba.convert("RGB")


# === TYPOGRAPHY AND CONTENT DRAWING ===

def load_font(font_key, size):
    """Load a font, falling back to default if not found."""
    try:
        return ImageFont.truetype(FONTS[font_key], size)
    except (OSError, KeyError):
        fallbacks = [
            os.path.join(FONT_DIR, "liberation/LiberationSerif-Bold.ttf"),
            os.path.join(FONT_DIR, "liberation/LiberationSans-Regular.ttf"),
            os.path.join(FONT_DIR, "dejavu/DejaVuSans.ttf"),
        ]
        for fb in fallbacks:
            try:
                return ImageFont.truetype(fb, size)
            except OSError:
                continue
        return ImageFont.load_default()


def wrap_text(text, font, max_width, draw):
    """Word-wrap text to fit within max_width."""
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


def draw_text_block(draw, text, font, color, x, y, max_width, line_spacing=1.4):
    """Draw wrapped text block, return the y position after the block."""
    lines = wrap_text(text, font, max_width, draw)
    current_y = y

    for line in lines:
        draw.text((x, current_y), line, font=font, fill=hex_to_rgb(color))
        bbox = draw.textbbox((0, 0), line, font=font)
        line_height = (bbox[3] - bbox[1]) * line_spacing
        current_y += line_height

    return current_y


# === MAIN RENDER FUNCTION ===

def render_slide(
    title=None,
    subtitle=None,
    body=None,
    bullets=None,
    slide_number=None,
    total_slides=None,
    style="tech",
    layout="gradient_only",
    bg_image=None,
    icon=None,
    output="slide.png",
    width=WIDTH,
    height=HEIGHT,
    cta_text=None,
    overlay_strength=None,
):
    """Render a single carousel slide with AI-image compositing.

    Args:
        title: Slide title text
        subtitle: Optional subtitle
        body: Body paragraph text
        bullets: Pipe-separated bullet points or list
        slide_number: Current slide number
        total_slides: Total slides count
        style: Visual style (tech, business, education, creative, mindset)
        layout: Compositing layout (gradient_only, full_bg, hero_top, hero_bottom, accent_center, accent_float)
        bg_image: Path to AI-generated image for compositing
        icon: Path to small icon/image overlay
        output: Output PNG path
        width: Canvas width (default 1080)
        height: Canvas height (default 1350)
        cta_text: Call-to-action text
        overlay_strength: Override overlay opacity (0.0-1.0) for full_bg layout
    """
    palette = PALETTES.get(style, PALETTES["tech"])

    # Load background image if provided
    src_img = None
    if bg_image and os.path.exists(bg_image):
        try:
            src_img = Image.open(bg_image)
        except Exception as e:
            print(f"Warning: Could not load bg_image '{bg_image}': {e}", file=sys.stderr)

    # If layout needs an image but none provided, fall back to gradient_only
    if layout != "gradient_only" and src_img is None:
        print(f"Note: Layout '{layout}' requires --bg-image. Falling back to gradient_only.", file=sys.stderr)
        layout = "gradient_only"

    # Compose background based on layout
    if layout == "full_bg":
        img = compose_full_bg(width, height, palette, src_img)
        if overlay_strength is not None:
            # Allow manual override of overlay
            img = smart_crop(src_img.convert("RGB"), width, height)
            img = apply_overlay(img, palette["bg"], overlay_strength)
    elif layout == "hero_top":
        img = compose_hero_top(width, height, palette, src_img)
    elif layout == "hero_bottom":
        img = compose_hero_bottom(width, height, palette, src_img)
    elif layout == "accent_center":
        img = compose_accent_center(width, height, palette, src_img)
    elif layout == "accent_float":
        img = compose_accent_float(width, height, palette, src_img)
    else:
        img = compose_gradient_only(width, height, palette)

    draw = ImageDraw.Draw(img)

    # Load fonts
    font_title = load_font("title", SIZES["title"])
    font_subtitle = load_font("subtitle", SIZES["subtitle"])
    font_body = load_font("body", SIZES["body"])
    font_body_bold = load_font("body_bold", SIZES["body"])
    font_bullet = load_font("body", SIZES["bullet"])
    font_indicator = load_font("indicator", SIZES["indicator"])

    # Determine text start position based on layout
    if layout == "hero_top":
        # Text starts below the image region
        y_cursor = int(height * 0.44) + MARGIN // 2
    elif layout == "hero_bottom":
        # Text starts at normal top position
        y_cursor = SAFE_TOP + MARGIN
    elif layout == "accent_center":
        # Title at top, image in middle, body below image
        y_cursor = SAFE_TOP + MARGIN
    elif layout == "accent_float":
        # Title at top, image in middle, body below image
        y_cursor = SAFE_TOP + MARGIN
    else:
        y_cursor = SAFE_TOP + MARGIN

    # Draw slide indicator (top-right)
    if slide_number is not None and total_slides is not None:
        indicator_text = f"{slide_number}/{total_slides}"
        ind_bbox = draw.textbbox((0, 0), indicator_text, font=font_indicator)
        ind_width = ind_bbox[2] - ind_bbox[0]
        pill_x = width - MARGIN - ind_width - 20
        pill_y = SAFE_TOP + 10
        pill_w = ind_width + 20
        pill_h = (ind_bbox[3] - ind_bbox[1]) + 12

        # Semi-transparent pill background
        pill_img = Image.new("RGBA", (pill_w, pill_h), (0, 0, 0, 0))
        pill_draw = ImageDraw.Draw(pill_img)
        pill_draw.rounded_rectangle(
            [0, 0, pill_w, pill_h],
            radius=pill_h // 2,
            fill=hex_to_rgb(palette["accent"]) + (200,),
        )
        img_rgba = img.convert("RGBA")
        img_rgba.paste(pill_img, (pill_x, pill_y), pill_img)
        img = img_rgba.convert("RGB")
        draw = ImageDraw.Draw(img)  # refresh draw object

        draw.text(
            (pill_x + 10, pill_y + 4),
            indicator_text,
            font=font_indicator,
            fill=(255, 255, 255),
        )

    # Draw title
    if title:
        y_cursor += 20
        title_lines = wrap_text(title, font_title, CONTENT_WIDTH, draw)
        for line in title_lines:
            draw.text((MARGIN, y_cursor), line, font=font_title, fill=hex_to_rgb(palette["text_primary"]))
            bbox = draw.textbbox((0, 0), line, font=font_title)
            y_cursor += (bbox[3] - bbox[1]) * 1.2

        # Underline accent
        underline_y = y_cursor + 5
        if title_lines:
            last_bbox = draw.textbbox((0, 0), title_lines[-1], font=font_title)
            underline_width = min(last_bbox[2] - last_bbox[0], CONTENT_WIDTH * 0.6)
        else:
            underline_width = CONTENT_WIDTH * 0.4
        draw.rectangle(
            [MARGIN, underline_y, MARGIN + underline_width, underline_y + 4],
            fill=hex_to_rgb(palette["title_underline"]),
        )
        y_cursor = underline_y + 30

    # Draw subtitle
    if subtitle:
        y_cursor = draw_text_block(
            draw, subtitle, font_subtitle, palette["text_secondary"], MARGIN, y_cursor, CONTENT_WIDTH
        )
        y_cursor += 20

    # For accent layouts, skip past the image zone before drawing body/bullets
    if layout in ("accent_center", "accent_float") and src_img is not None:
        # Image is placed around y=0.33*height, estimate its bottom
        max_w, max_h = (700, 400) if layout == "accent_center" else (800, 450)
        scale = min(max_w / src_img.width, max_h / src_img.height, 1.0)
        img_h = int(src_img.height * scale)
        img_bottom = int(height * 0.35 if layout == "accent_center" else height * 0.33) + img_h
        if layout == "accent_float":
            img_bottom += 40  # account for shadow
        y_cursor = max(y_cursor, img_bottom + 30)

    # Draw body text
    if body:
        y_cursor = draw_text_block(
            draw, body, font_body, palette["text_primary"], MARGIN, y_cursor, CONTENT_WIDTH
        )
        y_cursor += 25

    # Draw bullet points
    if bullets:
        bullet_list = bullets.split("|") if isinstance(bullets, str) else bullets
        for bullet in bullet_list:
            bullet = bullet.strip()
            if not bullet:
                continue

            dot_y = y_cursor + SIZES["bullet"] // 2 - 4
            draw.ellipse(
                [MARGIN + 5, dot_y, MARGIN + 13, dot_y + 8],
                fill=hex_to_rgb(palette["bullet_dot"]),
            )

            bullet_x = MARGIN + 28
            bullet_width = CONTENT_WIDTH - 28
            y_cursor = draw_text_block(
                draw, bullet, font_bullet, palette["text_primary"], bullet_x, y_cursor, bullet_width
            )
            y_cursor += 8

    # Draw CTA text (centered, at bottom of safe zone)
    if cta_text:
        font_cta = load_font("body_bold", 30)
        cta_lines = wrap_text(cta_text, font_cta, CONTENT_WIDTH - 40, draw)
        cta_y = SAFE_BOTTOM - 80
        for line in cta_lines:
            cta_bbox = draw.textbbox((0, 0), line, font=font_cta)
            cta_w = cta_bbox[2] - cta_bbox[0]
            cta_x = (width - cta_w) // 2
            draw.text((cta_x, cta_y), line, font=font_cta, fill=hex_to_rgb(palette["accent"]))
            cta_y += (cta_bbox[3] - cta_bbox[1]) * 1.3

    # Draw icon overlay if provided
    if icon and os.path.exists(icon):
        try:
            icon_img = Image.open(icon).convert("RGBA")
            max_icon_size = 200
            icon_ratio = min(max_icon_size / icon_img.width, max_icon_size / icon_img.height)
            icon_size = (int(icon_img.width * icon_ratio), int(icon_img.height * icon_ratio))
            icon_img = icon_img.resize(icon_size, Image.Resampling.LANCZOS)

            icon_x = (width - icon_size[0]) // 2
            icon_y = max(y_cursor + 30, SAFE_BOTTOM - icon_size[1] - 60)

            img_rgba = img.convert("RGBA")
            img_rgba.paste(icon_img, (icon_x, icon_y), icon_img)
            img = img_rgba.convert("RGB")
        except Exception as e:
            print(f"Warning: Could not load icon: {e}", file=sys.stderr)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(os.path.abspath(output)), exist_ok=True)

    # Save
    img.save(output, "PNG", quality=95)
    print(f"Rendered slide: {output} ({width}x{height}, style={style}, layout={layout})")
    return output


def main():
    parser = argparse.ArgumentParser(description="Render a world-class Instagram carousel slide")
    parser.add_argument("--title", type=str, help="Slide title text")
    parser.add_argument("--subtitle", type=str, help="Subtitle text")
    parser.add_argument("--body", type=str, help="Body paragraph text")
    parser.add_argument("--bullets", type=str, help="Pipe-separated bullet points")
    parser.add_argument("--slide-number", type=int, help="Current slide number")
    parser.add_argument("--total-slides", type=int, help="Total number of slides")
    parser.add_argument("--style", type=str, default="tech", choices=list(PALETTES.keys()), help="Visual style")
    parser.add_argument("--layout", type=str, default="gradient_only", choices=LAYOUTS,
                        help="Image compositing layout (default: gradient_only)")
    parser.add_argument("--bg-image", type=str, help="AI-generated image path for compositing")
    parser.add_argument("--icon", type=str, help="Icon/image to overlay")
    parser.add_argument("--output", type=str, default="slide.png", help="Output file path")
    parser.add_argument("--width", type=int, default=WIDTH, help="Canvas width")
    parser.add_argument("--height", type=int, default=HEIGHT, help="Canvas height")
    parser.add_argument("--cta", type=str, help="Call-to-action text (centered at bottom)")
    parser.add_argument("--overlay-strength", type=float, help="Override overlay opacity for full_bg (0.0-1.0)")

    args = parser.parse_args()

    render_slide(
        title=args.title,
        subtitle=args.subtitle,
        body=args.body,
        bullets=args.bullets,
        slide_number=args.slide_number,
        total_slides=args.total_slides,
        style=args.style,
        layout=args.layout,
        bg_image=args.bg_image,
        icon=args.icon,
        output=args.output,
        width=args.width,
        height=args.height,
        cta_text=args.cta,
        overlay_strength=args.overlay_strength,
    )


if __name__ == "__main__":
    main()
