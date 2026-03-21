"""Image generator backend using the HappyCapy AI Gateway API.

Implements the ViMax ImageGenerator protocol by calling the AI Gateway's
``/images/generations`` endpoint. Supports text-to-image and image-to-image
(with reference images passed as base64 data URIs).

Usage in config::

    image_generator:
      class_path: tools.ImageGeneratorHappyCapyAPI
      init_args:
        api_key: ${AI_GATEWAY_API_KEY}
        model: google/gemini-3.1-flash-image-preview
"""

import asyncio
import base64
import json
import logging
import mimetypes
import os
from typing import List, Optional
from urllib import request as urllib_request
from urllib.error import HTTPError

from interfaces.image_output import ImageOutput
from utils.rate_limiter import RateLimiter


class ImageGeneratorHappyCapyAPI:
    """Generate images via the HappyCapy AI Gateway (OpenAI-compatible)."""

    GATEWAY_URL = "https://ai-gateway.happycapy.ai/api/v1/images/generations"

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "google/gemini-3.1-flash-image-preview",
        rate_limiter: Optional[RateLimiter] = None,
    ):
        self.api_key = api_key or os.environ.get("AI_GATEWAY_API_KEY", "")
        self.model = model
        self.rate_limiter = rate_limiter

        if not self.api_key:
            raise ValueError(
                "AI_GATEWAY_API_KEY is required. Set it in config or as an env var."
            )

    def _image_path_to_data_uri(self, path: str) -> str:
        """Convert a local image file to a base64 data URI."""
        mime_type, _ = mimetypes.guess_type(path)
        if mime_type is None:
            mime_type = "image/png"
        with open(path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")
        return f"data:{mime_type};base64,{b64}"

    async def generate_single_image(
        self,
        prompt: str,
        reference_image_paths: Optional[List[str]] = None,
        aspect_ratio: Optional[str] = "16:9",
        size: Optional[str] = None,
        **kwargs,
    ) -> ImageOutput:
        """Generate a single image, optionally using reference images.

        Args:
            prompt: Text description of the desired image.
            reference_image_paths: Local file paths to reference images.
            aspect_ratio: Desired aspect ratio (e.g. "16:9", "1:1").
            size: Desired image size (e.g. "1600x900", "1024x1024").

        Returns:
            ImageOutput with format "b64" and extension "png".
        """
        if reference_image_paths is None:
            reference_image_paths = []

        if self.rate_limiter:
            await self.rate_limiter.acquire()

        logging.info(
            "Calling HappyCapy AI Gateway (%s) to generate image with %d reference(s)...",
            self.model,
            len(reference_image_paths),
        )

        # Build the payload
        payload = {
            "model": self.model,
            "prompt": prompt,
            "response_format": "b64_json",
            "n": 1,
        }

        # The API uses aspectRatio (not arbitrary pixel sizes).
        # Convert size like "1600x900" to an aspect ratio.
        effective_ratio = aspect_ratio
        if size:
            try:
                w, h = map(int, size.lower().split("x"))
                from math import gcd
                g = gcd(w, h)
                effective_ratio = f"{w // g}:{h // g}"
            except (ValueError, AttributeError):
                pass  # fall through to default aspect_ratio

        if effective_ratio:
            payload["aspectRatio"] = effective_ratio

        # Attach reference images as data URIs
        if reference_image_paths:
            payload["images"] = [
                self._image_path_to_data_uri(p) for p in reference_image_paths
            ]

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "Origin": "https://trickle.so",
            "User-Agent": "ViMax-HappyCapy/1.0",
        }

        # Retry logic
        max_retries = 3
        retry_delay = 5

        for attempt in range(max_retries):
            try:
                response_data = await asyncio.get_event_loop().run_in_executor(
                    None, self._sync_request, payload, headers
                )
                break
            except HTTPError as e:
                if e.code == 429 and attempt < max_retries - 1:
                    wait_time = retry_delay * (2 ** attempt)
                    logging.warning(
                        "Rate limit hit (429), retrying in %ds... (attempt %d/%d)",
                        wait_time,
                        attempt + 1,
                        max_retries,
                    )
                    await asyncio.sleep(wait_time)
                else:
                    error_body = e.read().decode("utf-8") if hasattr(e, "read") else str(e)
                    logging.error("Image generation failed: %s", error_body)
                    raise

        # Parse response
        data_list = response_data.get("data", [])
        if not data_list:
            raise ValueError("No image data in API response")

        b64_data = data_list[0].get("b64_json")
        if b64_data:
            return ImageOutput(fmt="b64", ext="png", data=b64_data)

        url = data_list[0].get("url")
        if url:
            return ImageOutput(fmt="url", ext="png", data=url)

        raise ValueError("Response contained neither b64_json nor url")

    def _sync_request(self, payload: dict, headers: dict) -> dict:
        """Perform a synchronous HTTP request (run from executor)."""
        req = urllib_request.Request(
            self.GATEWAY_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers=headers,
            method="POST",
        )
        with urllib_request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))
