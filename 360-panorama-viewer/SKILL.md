---
name: 360-panorama-viewer
description: >
  Build a fully self-contained 360° equirectangular panorama viewer as a single HTML file.
  The viewer uses Three.js to render immersive spherical panoramas with drag-to-look,
  zoom, auto-rotate, and a scene-switcher sidebar. All panorama images are embedded as
  base64 JPEG — no server needed. Use this skill whenever the user asks to create a 360
  viewer, VR panorama app, immersive scene gallery, equirectangular image viewer, or
  wants to combine multiple AI-generated panoramas into an interactive webpage.
  Also trigger when the user says things like "make a 360 viewer", "VR world gallery",
  "360度全景", "全景查看器", "make scenes I can look around in", etc.
---

# 360° Panorama Viewer Skill

This skill creates a polished, self-contained 360° panorama viewer HTML file.

## What it produces

A single `.html` file (~3–6 MB depending on scene count) that:
- Renders equirectangular panoramas as spherical 360° environments using Three.js
- Supports dragging to look around, scroll to zoom, auto-rotate toggle, fullscreen
- Shows a thumbnail sidebar to switch between multiple scenes
- Works offline — no CDN dependencies, all assets embedded

## Skill assets

| Asset | Purpose |
|---|---|
| `assets/viewer_template.html` | Complete viewer HTML with Three.js inlined; panorama data injected at build time |
| `scripts/build_viewer.py` | Loads images, applies seam fix, base64-encodes, injects into template |

---

## Workflow

### Step 1 — Gather scene specs from the user

Ask (or infer from context) for each scene:
- **Description** of what the panorama should show
- **Title** for the HUD (emoji + name, e.g. `🍄 Mario World`)
- **Thumbnail label** (≤12 chars shown on the sidebar chip)

Typical count: 3–6 scenes. You can also accept user-provided image files directly (skip generation).

### Step 2 — Generate panorama images

For **each scene**, generate a 360° equirectangular panorama image.

**Model choice:**
- **Preferred:** `google/gemini-3.1-flash-image-preview` via AI Gateway — reliable 2:1 output, no safety rejections for fictional themes
- **Alternative:** `gpt-image-2` via AI Gateway at size `1536x1024` — higher quality but may reject branded IP (Mario, Zelda, etc.)

**Generation code (Gemini route):**
```python
import os, requests, base64
from PIL import Image
import io

api_key = os.environ['AI_GATEWAY_API_KEY']

def generate_panorama(prompt: str, save_path: str):
    payload = {
        "model": "google/gemini-3.1-flash-image-preview",
        "prompt": prompt,
        "response_format": "b64_json",
        "n": 1
    }
    resp = requests.post(
        'https://ai-gateway.happycapy.ai/api/v1/images/generations',
        headers={
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
            'Origin': 'https://trickle.so'
        },
        json=payload,
        timeout=180
    )
    resp.raise_for_status()
    img_bytes = base64.b64decode(resp.json()['data'][0]['b64_json'])
    img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
    img.save(save_path)
    return save_path
```

**Prompt formula for good equirectangular panoramas:**
```
360 degree equirectangular panorama of [SCENE DESCRIPTION].
[Key visual elements]. [Style description].
Wide seamless landscape, 2:1 aspect ratio,
left and right edges must tile perfectly for 360 VR viewing.
```

**Example prompts:**
- Mario: `360 degree equirectangular panorama of a colorful cartoon mushroom kingdom platformer world. Bright blue sky, rolling green hills, red mushroom houses, floating brick blocks, gold coins, stone castle. Vibrant cartoon illustration, 2:1 aspect ratio, seamless tiling.`
- Underwater city: `360 degree equirectangular panorama of a futuristic underwater city. Bioluminescent buildings, schools of fish, coral reefs, deep ocean light shafts. Cinematic, 2:1 aspect ratio, seamless tiling.`

Save each generated image to a temp path (e.g. `tmp/scene_N_raw.png`).

### Step 3 — Build the viewer

Run the build script, passing all scenes as a JSON array:

```bash
SKILL_DIR=/home/node/.claude/skills/360-panorama-viewer

python3 "$SKILL_DIR/scripts/build_viewer.py" \
  --template "$SKILL_DIR/assets/viewer_template.html" \
  --output "outputs/360_viewer.html" \
  --scenes '[
    {"title":"🍄 Mario World","thumb_label":"Mario","image_path":"tmp/mario.png","initial_lon":90},
    {"title":"🐚 Underwater City","thumb_label":"Deep City","image_path":"tmp/underwater.png","initial_lon":0}
  ]'
```

The script will:
1. Resize each image to 1774×887 (standard 2:1)
2. Apply a **pure-roll seam fix** — finds the horizontal offset that minimises left/right edge difference, then `np.roll`s the image. No blending. This ensures the 360° seam is as clean as possible without distorting colors.
3. Base64-encode as JPEG quality 90
4. Inject into the template and write the output HTML

### Step 4 — Deliver

Output the file to `outputs/360_viewer.html` (or user-specified path) and attach it as a static HTML deliverable.

---

## Replacing a single scene in an existing viewer

If the user already has a viewer and wants to swap out one scene (e.g. regenerate Mario), do NOT rerun all scenes — just re-encode the new image and replace its `b64` field in the HTML:

```python
import re, base64, io, numpy as np
from PIL import Image

SKILL_DIR = '/home/node/.claude/skills/360-panorama-viewer'

# Load and fix the new image
img = Image.open('new_mario.png').convert('RGB')
img = img.resize((1774, 887), Image.LANCZOS)
arr = np.array(img)
# pure roll seam fix
f = arr.astype(np.float32)
h, w = arr.shape[:2]
best_roll, best_score = 0, float('inf')
for roll in range(w):
    r = np.roll(f, roll, axis=1)
    score = float(np.abs(r[:, :5] - r[:, w-5:]).mean())
    if score < best_score:
        best_score = score
        best_roll = roll
fixed = np.roll(arr, best_roll, axis=1)

buf = io.BytesIO()
Image.fromarray(fixed).save(buf, format='JPEG', quality=90)
new_b64 = base64.b64encode(buf.getvalue()).decode('ascii')

# Replace in HTML by matching scene title
with open('outputs/360_viewer.html') as fh:
    html = fh.read()

# Match the specific scene entry (adjust title keyword as needed)
pattern = r"(title:\s*'[^']*Mario[^']*',\s*initialLon:\s*[\d.]+,\s*b64:\s*')([^']+)(')"
html_new, n = re.subn(pattern, r'\g<1>' + new_b64 + r'\g<3>', html)
assert n == 1, f"Expected 1 replacement, got {n}"

with open('outputs/360_viewer.html', 'w') as fh:
    fh.write(html_new)
print(f'Replaced Mario scene (roll={best_roll})')
```

---

## Seam fix — why pure roll, not blending

Equirectangular panoramas wrap horizontally: x=0 and x=w-1 represent the same physical meridian. AI-generated images rarely place the seam at a natural boundary (e.g. open sky), so the default seam is often visible.

**Pure roll**: shift the whole image left/right to find the position where the 5-pixel columns at both edges are most similar (lowest mean absolute difference). `np.roll()` is a circular shift — no pixels are added or removed, no colors are changed. This is lossless and never creates artifacts.

**Never use blending/color correction** at the seam: it creates a visible "smeared" band where pixel values are artificially averaged, which looks worse than the original seam.

---

## Viewer features reference

The template includes these controls, all functional out of the box:
- **Drag** — look around (mouse or touch)
- **Scroll / pinch** — zoom (FOV 30°–120°, default 75°)
- **Auto Rotate** button — gentle continuous pan
- **Reset** button — return to `initialLon` of current scene
- **Fullscreen** button
- **FOV slider** — right-side vertical range input
- **Thumbnail sidebar** — left-side scene switcher with active highlight

Scene `initialLon` is the starting horizontal angle (0–360). Use it to face an interesting part of the panorama on load (e.g. 90 = face right, 180 = face backwards).

---

## Tips for better panoramas

- Ask for **2:1 aspect ratio** explicitly in every prompt — this is the equirectangular standard
- Mention **"seamless tiling"** and **"left and right edges must connect"** in the prompt
- For fictional/branded themes (Mario, Zelda), describe the visual style without using trademarked names if GPT-Image-2 rejects them: "colorful cartoon platformer mushroom kingdom style" instead of "Mario"
- Gemini rarely rejects prompts and consistently produces good 2:1 panoramas — prefer it for speed
