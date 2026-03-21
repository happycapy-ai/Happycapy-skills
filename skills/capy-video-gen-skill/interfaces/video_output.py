import asyncio
from typing import List, Literal, Optional, Union
from PIL import Image

from utils.video import download_video


class VideoOutput:
    fmt: Literal["url", "bytes"]
    ext: str = "mp4"
    data: Union[str, bytes]

    def __init__(
        self,
        fmt: Literal["url", "bytes"],
        ext: str,
        data: Union[str, bytes],
    ):
        self.fmt = fmt
        self.ext = ext
        self.data = data

    def save_url(self, path: str) -> None:
        """Download and save a video from a URL to the specified path.

        Args:
            path (str): Path where the video will be saved.
        """
        download_video(self.data, path)

    def save_bytes(self, path: str) -> None:
        """Save a bytes object to the specified path.

        Args:
            path (str): Path where the video will be saved.
        """
        with open(path, 'wb') as f:
            f.write(self.data)

    def save(self, path: str) -> None:
        save_func = getattr(self, f"save_{self.fmt}")
        save_func(path)

