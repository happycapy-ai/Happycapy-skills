"""Structural typing contracts for rendering backends.

Any class that exposes the right method signatures satisfies these
protocols -- no inheritance required. Existing generators (Google,
Yunwu/Doubao, Yunwu/Veo) are already compliant by duck typing.
"""

from typing import List, Protocol, runtime_checkable

from interfaces.image_output import ImageOutput
from interfaces.video_output import VideoOutput


@runtime_checkable
class ImageGenerator(Protocol):
    """Generates a single image from a text prompt and optional reference images."""

    async def generate_single_image(
        self,
        prompt: str,
        reference_image_paths: List[str],
        **kwargs,
    ) -> ImageOutput: ...


@runtime_checkable
class VideoGenerator(Protocol):
    """Generates a single video from a text prompt and optional reference images."""

    async def generate_single_video(
        self,
        prompt: str,
        reference_image_paths: List[str],
        **kwargs,
    ) -> VideoOutput: ...
