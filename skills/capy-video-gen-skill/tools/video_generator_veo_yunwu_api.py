import logging
from typing import List, Optional
from PIL import Image
import asyncio
import aiohttp
from interfaces.video_output import VideoOutput
from utils.image import image_path_to_b64


class VideoGeneratorVeoYunwuAPI:
    def __init__(
        self,
        api_key: str,
        t2v_model: str = "veo3.1-fast",  # text to video
        ff2v_model: str = "veo3.1-fast",   # first frame to video
        flf2v_model: str = "veo2-fast-frames",  # first and last frame to video
    ):
        """
        all models:
            veo2
            veo2-fast
            veo2-fast-frames
            veo2-fast-components
            veo2-pro
            veo3
            veo3-fast
            veo3-pro
            veo3-pro-frames
            veo3-fast-frames
            veo3-frames

        NOTE: veo3 does not support first and last frame to video generation.
        """
        self.base_url = "https://yunwu.ai"
        self.api_key = api_key
        self.t2v_model = t2v_model
        self.ff2v_model = ff2v_model
        self.flf2v_model = flf2v_model

    async def generate_single_video(
        self,
        prompt: str = "",
        reference_image_paths: List[Image.Image] = [],
        aspect_ratio: str = "16:9",
        **kwargs,
    ) -> VideoOutput:
        if len(reference_image_paths) == 0:
            model = self.t2v_model
        elif len(reference_image_paths) == 1:
            model = self.ff2v_model
        elif len(reference_image_paths) == 2:
            model = self.flf2v_model
        else:
            raise ValueError("The number of reference images must be no more than 2")

        logging.info(f"Calling {model} to generate video...")

        # 1. Create video generation task
        payload = {
            "prompt": prompt,
            "model": model,
            "images": [image_path_to_b64(image_path, mime=True) for image_path in reference_image_paths],
            "enhance_prompt": True,
        }
        # only veo3 supports aspect ratio setting
        if model.startswith("veo3"):
            payload["aspect_ratio"] = aspect_ratio

        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }


        url = f"https://yunwu.ai/v1/video/create"
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, headers=headers, json=payload) as response:
                        response = await response.json()
                        logging.debug(f"Response: {response}")
                        task_id = response["id"]
                        logging.info(f"Video generation task created successfully. Task ID: {task_id}")
            except Exception as e:
                logging.error(f"Error occurred while creating video generation task: {e}. Retrying in 1 second...")
                await asyncio.sleep(1)
                continue
            break


        # 2. Query the video generation task until the video generation is completed
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.api_key}',
        }

        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"{self.base_url}/v1/video/query?id={task_id}", headers=headers) as response:
                        payload = await response.json()
                        logging.debug(f"Response: {payload}")
                        status = payload["status"]
            except Exception as e:
                logging.error(f"Error occurred while querying video generation task: {e}. Retrying in 1 second...")
                await asyncio.sleep(1)
                continue

            if status == "completed":
                logging.info(f"Video generation completed successfully")
                video_url = payload["video_url"]
                return VideoOutput(fmt="url", ext="mp4", data=video_url)
            elif status == "failed":
                logging.error(f"Video generation failed: \n{payload}")
                break
            else:
                logging.info(f"Video generation status: {status}, waiting 1 second...")
                await asyncio.sleep(1)
                continue
