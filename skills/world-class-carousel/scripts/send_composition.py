#!/usr/bin/env python3
"""Shared helper for sending multi-image compositions to Gemini via AI Gateway."""
import base64, json, os, sys
from pathlib import Path
from urllib import request as req
from urllib.error import HTTPError

API_KEY = os.environ["AI_GATEWAY_API_KEY"]
BASE = "https://ai-gateway.happycapy.ai/api/v1"

def send(image_paths, prompt, output_name):
    images_b64 = []
    for p in image_paths:
        data = base64.b64encode(Path(p).read_bytes()).decode()
        ext = Path(p).suffix.lower()
        mime = "image/png" if ext == ".png" else "image/jpeg"
        images_b64.append(f"data:{mime};base64,{data}")

    payload = {
        "model": "google/gemini-3-pro-image-preview",
        "prompt": prompt,
        "images": images_b64,
        "response_format": "url",
        "n": 1
    }

    r = req.Request(
        f"{BASE}/images/generations",
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
            "Origin": "https://trickle.so",
            "User-Agent": "Mozilla/5.0 (compatible; AI-Gateway-Client/1.0)"
        },
        method="POST"
    )
    try:
        with req.urlopen(r, timeout=180) as resp:
            result = json.loads(resp.read())
            if "data" in result and result["data"]:
                img_url = result["data"][0]["url"]
                dl = req.Request(img_url, headers={"User-Agent": "Mozilla/5.0"})
                with req.urlopen(dl) as dl_resp:
                    Path(output_name).write_bytes(dl_resp.read())
                    kb = Path(output_name).stat().st_size // 1024
                    print(f"OK: {output_name} ({kb}KB)")
                    return True
    except HTTPError as e:
        print(f"FAIL: HTTP {e.code}: {e.read().decode()[:300]}")
    except Exception as e:
        print(f"FAIL: {e}")
    return False

if __name__ == "__main__":
    # CLI: python3 send_composition.py output.png "prompt" img1 img2 ...
    output = sys.argv[1]
    prompt = sys.argv[2]
    images = sys.argv[3:]
    send(images, prompt, output)
