# https://yunwu.apifox.cn/api-347960869

import logging
import aiohttp
from typing import List, Optional
from tenacity import retry, stop_after_attempt
from utils.retry import after_func
from utils.image import image_path_to_b64
from interfaces.image_output import ImageOutput


class ImageGeneratorDoubaoSeedreamYunwuAPI:
    def __init__(
        self,
        api_key: str,
        model: str = "doubao-seedream-4-0-250828",

    ):
        self.api_key = api_key
        self.base_url = "https://yunwu.ai/v1/images/generations"
        self.model = model


    @retry(stop=stop_after_attempt(3), after=after_func)
    async def generate_single_image(
        self,
        prompt: str,
        reference_image_paths: List[str] = [],
        size: Optional[str] = None,
        **kwargs,
    ) -> ImageOutput:
        """
            size: [1024x1024, 4096x4096]
        """

        logging.info(f"Calling {self.model} to generate image...")

        image = [
            image_path_to_b64(path, mime=True) for path in reference_image_paths
        ]

        payload = {
            "model": self.model,
            "prompt": prompt,
            "sequential_image_generation": "disabled",  # "auto" or "disabled"
            # "sequential_image_generation_options": {
            #     "max_images": 1
            # },
            "response_format": "url",
            "size": size if size is not None else "1024x1024",
        }
        if len(image) > 0:
            payload["image"] = image

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.base_url, json=payload, headers=headers) as response:
                    response_json = await response.json()
        except Exception as e:
            logging.error(f"Error occurred while generating image: {e}")
            raise e

        data = response_json['data'][0]['url']
        return ImageOutput(fmt="url", ext="png", data=data)
