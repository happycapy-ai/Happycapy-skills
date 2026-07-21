#!/usr/bin/env python3
"""Generate a single collage still frame via the local AI Gateway (images/generations).

Unlike scripts/generate_video.py (which talks to Google's API directly with
GEMINI_API_KEY), this talks to the environment's built-in AI_GATEWAY_BASE_URL /
AI_GATEWAY_API_KEY — the same gateway the generate-image / generate-video
skills use. It always requests response_format=url so the hosted URL can be
reused directly as --first-frame-image / --last-frame-image when calling
generate-video's generate_video_sdk.js (Gemini Omni Flash needs http(s) image
URLs, not local paths).

Usage:
  python3 generate_still_gateway.py "<prompt>" --output frames/last-frame-original.png [--model google/gemini-3.1-flash-image]

Prints the hosted URL on the last stdout line and also writes it next to the
output file as "<output>.url.txt".
"""

import argparse
import json
import os
import sys
from pathlib import Path
from urllib import request
from urllib.error import HTTPError, URLError


def check_api_key():
    api_key = os.environ.get("AI_GATEWAY_API_KEY")
    if not api_key:
        print("Error: AI_GATEWAY_API_KEY environment variable is required.", file=sys.stderr)
        sys.exit(1)
    return api_key


def generate_image_url(prompt, model, aspect_ratio):
    api_key = check_api_key()
    api_base = os.environ.get("AI_GATEWAY_BASE_URL", "https://ai-gateway.happycapy.ai").rstrip("/") + "/api/v1"

    payload = {
        "model": model,
        "prompt": prompt,
        "response_format": "url",
        "n": 1,
    }
    if aspect_ratio:
        payload["aspectRatio"] = aspect_ratio

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "Origin": "https://trickle.so",
        "User-Agent": "Mozilla/5.0 (compatible; AI-Gateway-Client/1.0)",
    }

    req = request.Request(
        f"{api_base}/images/generations",
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
    except HTTPError as e:
        print(f"HTTP Error {e.code}: {e.read().decode('utf-8')}", file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"Network Error: {e.reason}", file=sys.stderr)
        sys.exit(1)

    data = result.get("data") or []
    if not data or not data[0].get("url"):
        print(f"Error: no url in response: {result}", file=sys.stderr)
        sys.exit(1)
    return data[0]["url"]


def download(url, output_path):
    req = request.Request(url, headers={"User-Agent": "Mozilla/5.0 (compatible; AI-Gateway-Client/1.0)"})
    with request.urlopen(req) as response:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(response.read())


def main():
    parser = argparse.ArgumentParser(description="Generate a collage still frame via the AI Gateway")
    parser.add_argument("prompt")
    parser.add_argument("--output", required=True)
    parser.add_argument("--model", default="google/gemini-3.1-flash-image")
    parser.add_argument("--aspect-ratio", default="9:16")
    args = parser.parse_args()

    url = generate_image_url(args.prompt, args.model, args.aspect_ratio)
    output_path = Path(args.output)
    download(url, output_path)

    url_sidecar = Path(str(output_path) + ".url.txt")
    url_sidecar.write_text(url + "\n")

    print(f"Saved local copy to: {output_path}")
    print(f"Hosted URL: {url}")


if __name__ == "__main__":
    main()
