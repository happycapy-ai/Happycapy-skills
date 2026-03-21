import logging
import os
import asyncio
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.chat_models.base import BaseChatModel
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from tenacity import retry, stop_after_attempt
from interfaces import CharacterInScene, ImageOutput
from langchain_core.messages import HumanMessage, SystemMessage
from utils.retry import after_func



prompt_template_front = \
"""
Generate a full-body, front-view portrait of character {identifier} based on the following description, with a pure white background. The character should be centered in the image, occupying most of the frame. Gazing straight ahead. Standing with arms relaxed at sides. Natural expression.

CRITICAL - Face Identity: Generate this EXACT person with precise facial features. Every detail matters for identity consistency across scenes: exact nose shape, eye shape and spacing, jawline contour, skin tone, hair texture/style/color, and any distinguishing marks (glasses, facial hair, scars, moles). The face must be photorealistic and detailed enough to be recognizable as the same person in every subsequent frame.

Features: {features}
Style: {style}
"""

prompt_template_side = \
"""
Generate a full-body, side-view portrait of character {identifier} based on the provided front-view portrait, with a pure white background. The character should be centered in the image, occupying most of the frame. Facing left. Standing with arms relaxed at sides.
"""

prompt_template_back = \
"""
Generate a full-body, back-view portrait of character {identifier} based on the provided front-view portrait, with a pure white background. The character should be centered in the image, occupying most of the frame. No facial features should be visible.
"""


class CharacterPortraitsGenerator:
    def __init__(
        self,
        image_generator,
    ):
        self.image_generator = image_generator


    @retry(stop=stop_after_attempt(3), after=after_func, reraise=True)
    async def generate_front_portrait(
        self,
        character: CharacterInScene,
        style: str,
    ) -> ImageOutput:
        features = "(static) " + character.static_features + "; (dynamic) " + character.dynamic_features
        prompt = prompt_template_front.format(
            identifier=character.identifier_in_scene,
            features=features,
            style=style,
        )
        image_output = await self.image_generator.generate_single_image(
            prompt=prompt,
            # size="512x512",
        )
        return image_output

    @retry(stop=stop_after_attempt(3), after=after_func, reraise=True)
    async def generate_side_portrait(
        self,
        character: CharacterInScene,
        front_image_path: str,
    ) -> ImageOutput:
        prompt = prompt_template_side.format(
            identifier=character.identifier_in_scene,
        )
        image_output = await self.image_generator.generate_single_image(
            prompt=prompt,
            reference_image_paths=[front_image_path],
            # size="1024x1024",
        )
        return image_output


    @retry(stop=stop_after_attempt(3), after=after_func, reraise=True)
    async def generate_back_portrait(
        self,
        character: CharacterInScene,
        front_image_path: str,
    ) -> ImageOutput:
        prompt = prompt_template_back.format(
            identifier=character.identifier_in_scene,
        )
        image_output = await self.image_generator.generate_single_image(
            prompt=prompt,
            reference_image_paths=[front_image_path],
            # size="512x512",
        )
        return image_output