"""ViMax Idea-to-Video pipeline -- HappyCapy edition.

Uses the HappyCapy AI Gateway for all LLM, image, and video generation.
Run from the ViMax root directory:

    .venv/bin/python main_happycapy_idea2video.py

Environment variables required:
    AI_GATEWAY_API_KEY  -- your HappyCapy gateway key
"""

import asyncio
import logging
import sys

from langchain.chat_models import init_chat_model
from tools.render_backend import RenderBackend
from utils.config_loader import load_config
from pipelines.idea2video_pipeline import Idea2VideoPipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

# ─── Customise your idea here ─────────────────────────────────────────
idea = """\
A lone astronaut discovers a lush hidden garden inside an abandoned space
station orbiting Earth. The garden is overgrown with exotic alien flowers that
glow in the dark. The astronaut carefully touches one of the flowers and it
releases a swarm of tiny glowing butterflies that illuminate the entire room.
"""

user_requirement = """\
Keep it short: no more than 2 scenes, each with at most 4 shots.
"""

style = "Cinematic sci-fi, moody lighting, realistic"
# ─────────────────────────────────────────────────────────────────────


async def main():
    config = load_config("configs/happycapy_idea2video.yaml")

    chat_model = init_chat_model(**config["chat_model"]["init_args"])
    backend = RenderBackend.from_config(config)

    pipeline = Idea2VideoPipeline(
        chat_model=chat_model,
        image_generator=backend.image_generator,
        video_generator=backend.video_generator,
        working_dir=config["working_dir"],
    )

    await pipeline(idea=idea, user_requirement=user_requirement, style=style)
    print("\nDone! Check .working_dir/idea2video/ for results.")


if __name__ == "__main__":
    asyncio.run(main())
