#!/usr/bin/env python3
"""
build_viewer.py  —  360° Panorama Viewer builder

Usage:
    python build_viewer.py \
        --scenes '[{"title":"🍄 Mario World","thumb_label":"Mario","image_path":"mario.png","initial_lon":90}]' \
        --output my_viewer.html \
        --template /path/to/viewer_template.html

The --scenes JSON array contains one object per scene:
  - title:        displayed in the top HUD (supports emoji)
  - thumb_label:  short text shown on the sidebar thumbnail chip (≤12 chars)
  - image_path:   path to the equirectangular image (PNG or JPEG, ideally 2:1 ratio)
  - initial_lon:  (optional, default 0) starting horizontal angle in degrees

The script:
  1. Loads each image and applies a pure-roll seam fix (minimises left/right edge diff)
  2. Resizes to 1774×887 if needed
  3. Base64-encodes as JPEG q90
  4. Injects everything into viewer_template.html
  5. Writes the final self-contained HTML to --output
"""

import argparse
import base64
import io
import json
import os
import re
import sys

try:
    import numpy as np
    from PIL import Image
except ImportError:
    print("ERROR: Pillow and numpy are required.  pip install pillow numpy", file=sys.stderr)
    sys.exit(1)

TARGET_W, TARGET_H = 1774, 887
THUMB_W, THUMB_H = 150, 75  # thumbnail preview size


def pure_roll_fix(arr: np.ndarray) -> tuple[np.ndarray, int]:
    """Find the horizontal roll offset that minimises left/right 5-pixel edge MAD."""
    h, w = arr.shape[:2]
    f = arr.astype(np.float32)
    best_roll, best_score = 0, float("inf")
    for roll in range(w):
        r = np.roll(f, roll, axis=1)
        score = float(np.abs(r[:, :5] - r[:, w - 5:]).mean())
        if score < best_score:
            best_score = score
            best_roll = roll
    return np.roll(arr, best_roll, axis=1), best_roll


def image_to_b64_jpeg(arr: np.ndarray, quality: int = 90) -> str:
    buf = io.BytesIO()
    Image.fromarray(arr).save(buf, format="JPEG", quality=quality, optimize=False)
    return base64.b64encode(buf.getvalue()).decode("ascii")


def load_and_prepare(image_path: str, verbose: bool = True) -> tuple[np.ndarray, np.ndarray]:
    """Load image, resize to 2:1, apply seam fix. Returns (fixed_arr, thumb_arr)."""
    img = Image.open(image_path).convert("RGB")
    # Resize to standard panorama size
    if img.size != (TARGET_W, TARGET_H):
        img = img.resize((TARGET_W, TARGET_H), Image.LANCZOS)
    arr = np.array(img)

    # Seam fix
    fixed, roll = pure_roll_fix(arr)
    if verbose:
        h, w = arr.shape[:2]
        f = arr.astype(np.float32)
        before = float(np.abs(f[:, :5] - f[:, w - 5:]).mean())
        fr = fixed.astype(np.float32)
        after = float(np.abs(fr[:, :5] - fr[:, w - 5:]).mean())
        print(f"  seam: {before:.1f} → {after:.2f}  (roll={roll})", flush=True)

    # Thumbnail: center crop to 2:1 at small size
    thumb = Image.fromarray(fixed).resize((THUMB_W, THUMB_H), Image.LANCZOS)
    thumb_arr = np.array(thumb)
    return fixed, thumb_arr


def build_scenes_js(scenes_config: list[dict]) -> str:
    """Build the const SCENES = [...]; JS block."""
    lines = ["const SCENES = ["]
    for i, scene in enumerate(scenes_config):
        comma = "," if i < len(scenes_config) - 1 else ""
        title = scene["title"].replace("'", "\\'")
        lon = scene.get("initial_lon", 0)
        b64 = scene["_b64"]
        lines.append(f"    {{ title: '{title}', initialLon: {lon}, b64: '{b64}' }}{comma}")
    lines.append("];")
    return "\n".join(lines)


def build_thumbnails_html(scenes_config: list[dict]) -> str:
    """Build the scene-switcher inner HTML."""
    parts = []
    for i, scene in enumerate(scenes_config):
        active_class = " active" if i == 0 else ""
        label = scene.get("thumb_label", scene["title"])[:20]
        thumb_b64 = scene["_thumb_b64"]
        parts.append(
            f'  <div class="scene-thumb{active_class}" id="thumb-{i}" onclick="switchScene({i})">'
            f'<img id="thumb-img-{i}" src="data:image/jpeg;base64,{thumb_b64}" alt="{label}" />'
            f'<div class="thumb-label">{label}</div></div>'
        )
    return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser(description="Build a self-contained 360° panorama viewer HTML.")
    parser.add_argument("--scenes", required=True, help="JSON array of scene definitions")
    parser.add_argument("--output", default="360_viewer.html", help="Output HTML file path")
    parser.add_argument("--template", required=True, help="Path to viewer_template.html")
    parser.add_argument("--title", default="360° Panorama Viewer", help="Browser tab title")
    args = parser.parse_args()

    # Load template
    if not os.path.exists(args.template):
        print(f"ERROR: template not found: {args.template}", file=sys.stderr)
        sys.exit(1)
    with open(args.template) as fh:
        template = fh.read()

    # Parse scenes
    scenes = json.loads(args.scenes)
    if not scenes:
        print("ERROR: --scenes must contain at least one scene", file=sys.stderr)
        sys.exit(1)

    print(f"Processing {len(scenes)} scene(s)…", flush=True)
    for i, scene in enumerate(scenes):
        print(f"[{i+1}/{len(scenes)}] {scene['title']} ← {scene['image_path']}", flush=True)
        fixed, thumb = load_and_prepare(scene["image_path"])
        scene["_b64"] = image_to_b64_jpeg(fixed, quality=90)
        scene["_thumb_b64"] = image_to_b64_jpeg(thumb, quality=85)

    # Build JS blocks
    scenes_js = build_scenes_js(scenes)
    thumbs_html = build_thumbnails_html(scenes)
    first_title = scenes[0]["title"].replace("'", "\\'")

    # Inject into template
    html = template
    html = html.replace("/*__SCENES_PLACEHOLDER__*/", scenes_js)
    html = html.replace("__THUMBNAILS_PLACEHOLDER__", thumbs_html)
    html = html.replace("__FIRST_SCENE_TITLE__", scenes[0]["title"])
    html = html.replace("360° Panorama Viewer", args.title)

    # Fix loading count (template has SCENES.length via JS, but loading text string is static)
    html = re.sub(
        r"Loading panoramas… 0 / ' \+ SCENES\.length \+ '",
        f"Loading panoramas… 0 / {len(scenes)}",
        html,
    )

    with open(args.output, "w") as fh:
        fh.write(html)

    size_kb = os.path.getsize(args.output) / 1024
    print(f"\nDone! → {args.output}  ({size_kb:.0f} KB)", flush=True)


if __name__ == "__main__":
    main()
