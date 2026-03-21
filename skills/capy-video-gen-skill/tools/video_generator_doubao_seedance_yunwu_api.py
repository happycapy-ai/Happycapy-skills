import logging
from typing import List, Literal
import asyncio
import aiohttp
from interfaces.video_output import VideoOutput
from utils.image import image_path_to_b64


class VideoGeneratorDoubaoSeedanceYunwuAPI:
    def __init__(
        self,
        api_key: str,
        t2v_model: str = "doubao-seedance-1-0-lite-t2v-250428",
        ff2v_model: str = "doubao-seedance-1-0-lite-i2v-250428",
        flf2v_model: str = "doubao-seedance-1-0-lite-i2v-250428",
    ):
        self.api_key = api_key
        self.t2v_model = t2v_model
        self.ff2v_model = ff2v_model
        self.flf2v_model = flf2v_model


    async def create_video_generation_task(
        self,
        prompt: str,
        reference_image_paths: List[str],
        resolution: Literal["480p", "720p", "1080p"] = "720p",
        aspect_ratio: str = "16:9",
        fps: Literal[16, 24] = 16,
        duration: Literal[5, 10] = 5,
    ) -> str:
        """
        Create a video generation task and return the task ID.
        
        Args:
            prompt: Text prompt for video generation
            reference_image_paths: List of 1 or 2 reference images
            
        Returns:
            Task ID string
        """
        if len(reference_image_paths) == 0:
            model = self.t2v_model
        elif len(reference_image_paths) == 1:
            model = self.ff2v_model
        elif len(reference_image_paths) == 2:
            model = self.flf2v_model
        else:
            raise ValueError("reference_image_paths must contain 1 or 2 images.")

        logging.info(f"Calling {model} to generate video...")

        url = "https://yunwu.ai/volc/v1/contents/generations/tasks"


        content = [
            {
                "type": "text",
                "text": prompt + f" --rs {resolution} --rt {aspect_ratio} --dur {duration}  --fps {fps}  --wm false --seed -1 --cf false"
            }
        ]
        if len(reference_image_paths) >= 1:
            content.append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_path_to_b64(reference_image_paths[0])
                    },
                    "role": "first_frame",
                }
            )
        if len(reference_image_paths) >= 2:
            content.append(
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_path_to_b64(reference_image_paths[1])
                    },
                    "role": "last_frame",
                }
            )

        payload = {
            "model": model,
            "content": content
        }

        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, headers=headers, json=payload) as response:
                        response_json = await response.json()
                        logging.debug(f"Response: {response_json}")
                        task_id = response_json["id"]
            except Exception as e:
                logging.error(f"Error occurred while creating video generation task.\nRetrying in 1 seconds...")
                await asyncio.sleep(1)
                continue
            break

        logging.info(f"Video generation task created successfully. Task ID: {task_id}")
        return task_id

    async def query_video_generation_task(
        self,
        task_id: str,
    ) -> str:
        """
        Query the video generation task until completion and return the video URL.
        
        Args:
            task_id: Task ID to query
            
        Returns:
            Video URL string
        """
        url = f"https://yunwu.ai/volc/v1/contents/generations/tasks/{task_id}"
        headers = {
            'Authorization': f'Bearer {self.api_key}',
        }

        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=headers) as response:
                        response_json = await response.json()

            except Exception as e:
                logging.error(f"Error occurred while querying video generation task: {e}. Retrying in 1 seconds...")
                await asyncio.sleep(1)
                continue

            status = response_json["status"]
            if status == "succeeded":
                video_url = response_json["content"]["video_url"]
                logging.info(f"Video generation completed successfully. Video URL: {video_url}")
                break
            elif status == "failed":
                logging.error(f"Video generation failed. Response: {response_json}")
                raise ValueError("Video generation failed.")
            else:
                logging.info(f"Video generation is still in progress. Checking again in 2 seconds...")
                await asyncio.sleep(2)
                continue

        return video_url

    async def generate_single_video(
        self,
        prompt: str,
        reference_image_paths: List[str],
        resolution: Literal["480p", "720p", "1080p"] = "720p",
        aspect_ratio: str = "16:9",
        fps: Literal[16, 24] = 16,
        duration: Literal[5, 10] = 5,
    ) -> VideoOutput:
        """
        Generate a single video by creating a task and waiting for completion.
        
        Args:
            prompt: Text prompt for video generation
            reference_image_paths: List of 1 or 2 reference images
            resolution: Resolution of the video
            aspect_ratio: Aspect ratio of the video
            fps: Frames per second of the video
            duration: Duration of the video
        Returns:
            VideoOutput containing the video URL
        """
        task_id = await self.create_video_generation_task(prompt, reference_image_paths, resolution, aspect_ratio, fps, duration)
        video_url = await self.query_video_generation_task(task_id)
        return VideoOutput(fmt="url", ext="mp4", data=video_url)

