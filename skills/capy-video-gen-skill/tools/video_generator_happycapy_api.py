"""Video generator backend using the HappyCapy AI Gateway API.

Implements the ViMax VideoGenerator protocol by calling the AI Gateway's
video generation endpoints. Supports:
  - Text-to-video (T2V): no reference images
  - First-frame-to-video (FF2V): one reference image as first frame
  - First+last-frame-to-video (FLF2V): two reference images

The gateway exposes an async workflow: submit -> poll -> download.

Usage in config::

    video_generator:
      class_path: tools.VideoGeneratorHappyCapyAPI
      init_args:
        api_key: ${AI_GATEWAY_API_KEY}
        model: google/veo-3.1-generate-preview
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

from interfaces.video_output import VideoOutput
from utils.rate_limiter import RateLimiter


class VideoGeneratorHappyCapyAPI:
    """Generate videos via the HappyCapy AI Gateway."""

    GATEWAY_BASE = "https://ai-gateway.trickle-lab.tech"

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "google/veo-3.1-generate-preview",
        rate_limiter: Optional[RateLimiter] = None,
        poll_interval: int = 10,
        poll_timeout: int = 600,
    ):
        self.api_key = api_key or os.environ.get("AI_GATEWAY_API_KEY", "")
        self.model = model
        self.rate_limiter = rate_limiter
        self.poll_interval = poll_interval
        self.poll_timeout = poll_timeout

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

    def _headers(self) -> dict:
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "Origin": "https://trickle.so",
            "User-Agent": "ViMax-HappyCapy/1.0",
        }

    async def generate_single_video(
        self,
        prompt: str,
        reference_image_paths: Optional[List[str]] = None,
        resolution: str = "720p",
        aspect_ratio: str = "16:9",
        duration: int = 8,
        **kwargs,
    ) -> VideoOutput:
        """Generate a single video, optionally with first/last frame guidance.

        Args:
            prompt: Text description of the desired video.
            reference_image_paths: 0, 1, or 2 local image paths.
                [0] = first frame, [1] = last frame.
            resolution: "720p" or "1080p".
            aspect_ratio: e.g. "16:9".
            duration: Duration in seconds.

        Returns:
            VideoOutput with the raw video bytes.
        """
        if reference_image_paths is None:
            reference_image_paths = []

        if len(reference_image_paths) > 2:
            raise ValueError("At most 2 reference images (first_frame, last_frame)")

        if self.rate_limiter:
            await self.rate_limiter.acquire()

        mode = "T2V"
        if len(reference_image_paths) == 1:
            mode = "FF2V"
        elif len(reference_image_paths) == 2:
            mode = "FLF2V"

        logging.info(
            "Calling HappyCapy AI Gateway (%s) for video generation [%s], duration=%ds...",
            self.model,
            mode,
            duration,
        )

        # Build payload
        payload = {
            "model": self.model,
            "prompt": prompt,
            "duration": duration,
            "aspectRatio": aspect_ratio,
        }

        if resolution:
            payload["size"] = resolution

        if len(reference_image_paths) >= 1:
            payload["first_frame"] = self._image_path_to_data_uri(
                reference_image_paths[0]
            )
        if len(reference_image_paths) >= 2:
            payload["last_frame"] = self._image_path_to_data_uri(
                reference_image_paths[1]
            )

        # Step 1: Submit generation request
        max_retries = 3
        retry_delay = 10

        for attempt in range(max_retries):
            try:
                submit_resp = await asyncio.get_event_loop().run_in_executor(
                    None,
                    self._sync_post,
                    f"{self.GATEWAY_BASE}/api/v1/videos",
                    payload,
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
                    error_body = ""
                    try:
                        error_body = e.read().decode("utf-8")
                    except Exception:
                        pass
                    logging.error("Video submission failed: %s %s", e.code, error_body)
                    raise

        video_id = submit_resp.get("id")
        if not video_id:
            raise RuntimeError(f"No video ID in response: {submit_resp}")

        logging.info("Video generation submitted, id=%s. Polling for completion...", video_id)

        # Step 2: Poll until completion
        elapsed = 0
        initial_delay = 35  # seconds before first poll
        await asyncio.sleep(initial_delay)
        elapsed += initial_delay

        while elapsed < self.poll_timeout:
            status_resp = await asyncio.get_event_loop().run_in_executor(
                None,
                self._sync_get,
                f"{self.GATEWAY_BASE}/api/v1/videos/{video_id}",
            )

            status = status_resp.get("status", "unknown")
            logging.info(
                "Video %s status: %s (elapsed: %ds)", video_id, status, elapsed
            )

            if status == "succeeded":
                video_url = status_resp.get("url")
                if not video_url:
                    raise RuntimeError("Video succeeded but no URL returned")

                # Download the video
                logging.info("Downloading video from %s...", video_url)
                video_bytes = await asyncio.get_event_loop().run_in_executor(
                    None, self._download_bytes, video_url
                )
                return VideoOutput(fmt="bytes", ext="mp4", data=video_bytes)

            elif status == "failed":
                error_msg = status_resp.get("error", "Unknown error")
                raise RuntimeError(f"Video generation failed: {error_msg}")

            await asyncio.sleep(self.poll_interval)
            elapsed += self.poll_interval

        raise TimeoutError(
            f"Video generation timed out after {self.poll_timeout}s (id={video_id})"
        )

    def _sync_post(self, url: str, payload: dict) -> dict:
        """Synchronous POST request."""
        req = urllib_request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=self._headers(),
            method="POST",
        )
        with urllib_request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def _sync_get(self, url: str) -> dict:
        """Synchronous GET request."""
        req = urllib_request.Request(url, headers=self._headers(), method="GET")
        with urllib_request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def _download_bytes(self, url: str) -> bytes:
        """Download raw bytes from a URL."""
        req = urllib_request.Request(
            url,
            headers={"User-Agent": "ViMax-HappyCapy/1.0"},
        )
        with urllib_request.urlopen(req, timeout=300) as resp:
            return resp.read()
