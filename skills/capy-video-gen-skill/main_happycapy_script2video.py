"""ViMax Script-to-Video pipeline -- HappyCapy edition.

Uses the HappyCapy AI Gateway for all LLM, image, and video generation.
Run from the ViMax root directory:

    .venv/bin/python main_happycapy_script2video.py

Environment variables required:
    AI_GATEWAY_API_KEY  -- your HappyCapy gateway key
"""

import asyncio
import logging

from langchain.chat_models import init_chat_model
from tools.render_backend import RenderBackend
from utils.config_loader import load_config
from pipelines.script2video_pipeline import Script2VideoPipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

# ─── Customise your script here ──────────────────────────────────────
script = """\
EXT. ROOFTOP CAFE - SUNSET

A small rooftop cafe overlooks a European city at golden hour. The warm
light casts long shadows between the tables. EMMA (28, creative, bright
red scarf) sits alone sketching in a notebook. MARCUS (30, charming,
leather jacket) approaches with two espressos.

MARCUS: (setting down the cups) I thought you could use a refuel.

EMMA: (looking up, surprised) Marcus? I didn't know you were in town!

MARCUS: (sitting down) Surprise visit. Couldn't miss the festival.
(gestures at her notebook) Still drawing the city?

EMMA: (smiling, turning the notebook) Always. Look -- I finally captured
that bell tower perfectly.

MARCUS: (leaning in, impressed) That's beautiful. You should exhibit these.

EMMA: (laughing softly) One day, maybe. For now, the coffee and the
sunset are enough.

(They both turn to watch the sun dip below the rooftops, the city
glowing in amber light.)
"""

user_requirement = """\
Warm, romantic tone. No more than 8 shots total.
"""

style = "Warm European cinema, golden hour lighting, shallow depth of field"
# ─────────────────────────────────────────────────────────────────────


async def main():
    config = load_config("configs/happycapy_script2video.yaml")

    chat_model = init_chat_model(**config["chat_model"]["init_args"])
    backend = RenderBackend.from_config(config)

    pipeline = Script2VideoPipeline(
        chat_model=chat_model,
        image_generator=backend.image_generator,
        video_generator=backend.video_generator,
        working_dir=config["working_dir"],
    )

    await pipeline(script=script, user_requirement=user_requirement, style=style)
    print("\nDone! Check .working_dir/script2video/ for results.")


if __name__ == "__main__":
    asyncio.run(main())
