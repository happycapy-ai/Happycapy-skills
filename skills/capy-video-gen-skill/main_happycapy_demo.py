"""ViMax Demo -- Custom video with user's real photos as character portraits.

Bypasses the portrait generation step and uses the user's actual photos
as character reference images for maximum likeness accuracy.
"""

import asyncio
import json
import logging
import os
import shutil

from langchain.chat_models import init_chat_model
from tools.render_backend import RenderBackend
from utils.config_loader import load_config
from pipelines.script2video_pipeline import Script2VideoPipeline
from interfaces import CharacterInScene

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

WORKING_DIR = ".working_dir/demo_video"

# ─── Script featuring the user as hero ────────────────────────────────
SCRIPT = """\
EXT. FUTURISTIC CITY ROOFTOP - NIGHT

A breathtaking cityscape stretches across the horizon, neon lights
reflecting off glass skyscrapers. <Arjun> stands at the edge of a
rooftop, looking out over the city. The wind gently moves his curly
dark hair. He wears round glasses, a casual light-colored t-shirt,
and has a backpack slung over one shoulder. He holds a glowing
holographic tablet that projects a 3D map of the city.

ARJUN: (to himself, determined) The signal is coming from the old
tech district. If I can trace it back, I can stop the override
before midnight.

He swipes through the holographic display, zooming into a section
of the city map. The neon glow from the buildings below illuminates
his face.

EXT. NEON-LIT ALLEY - NIGHT

<Arjun> walks through a narrow alley lined with flickering neon signs
and holographic advertisements. Steam rises from vents in the ground.
He checks his tablet as he moves quickly, the blue glow of the screen
reflecting off his glasses.

He pauses, noticing a hidden door behind a holographic sign. He pushes
through it cautiously.

INT. UNDERGROUND TECH LAB - NIGHT

<Arjun> enters a vast underground laboratory filled with servers and
floating holographic screens. Banks of quantum computers hum with
energy. He approaches the central terminal, a massive curved display.

ARJUN: (placing his hands on the terminal, focused) There you are.
Let's see what you're really up to.

He begins typing rapidly. Lines of code cascade across the screens.
A countdown timer appears: 00:03:42. His expression shifts from
concentration to urgency.

ARJUN: (muttering) Three minutes. That's tight, but doable.

He pulls up a decryption algorithm and launches it. The screens flash
with green confirmation signals as each firewall is breached.

EXT. FUTURISTIC CITY ROOFTOP - DAWN

<Arjun> is back on the rooftop. The first rays of dawn paint the sky
in orange and gold. He looks exhausted but triumphant. His tablet
displays "OVERRIDE NEUTRALIZED" in bold green text.

ARJUN: (smiling, relieved) City's safe for another day.

He puts the tablet away and watches the sunrise, the city slowly
coming to life below him. The camera pulls back to reveal the full
magnificent cityscape bathed in golden morning light.
"""

USER_REQUIREMENT = """\
Cinematic sci-fi thriller tone. Keep it to 3 scenes with no more than
12 shots total. Each shot should be visually striking with dramatic
lighting. The main character should appear in most shots.
"""

STYLE = "Cinematic sci-fi, dramatic neon lighting, Blade Runner aesthetic, photorealistic"


def setup_character_portraits():
    """Pre-populate the character portrait registry with the user's actual photos."""
    photo_dir = ".working_dir/user_photos"
    portrait_dir = os.path.join(WORKING_DIR, "character_portraits", "0_Arjun")
    os.makedirs(portrait_dir, exist_ok=True)

    # Map user photos to portrait views:
    # photo1.png = full body front view (park photo)
    # photo3.png = front face close-up (office/building photo)
    # photo2.png = close-up selfie angle (garden selfie)
    shutil.copy(f"{photo_dir}/photo1.png", f"{portrait_dir}/front.png")
    shutil.copy(f"{photo_dir}/photo3.png", f"{portrait_dir}/side.png")
    shutil.copy(f"{photo_dir}/photo2.png", f"{portrait_dir}/back.png")

    # Create the character portrait registry JSON
    registry = {
        "Arjun": {
            "front": {
                "path": os.path.abspath(f"{portrait_dir}/front.png"),
                "description": "A front full-body view of Arjun -- a young South Asian man with curly dark hair, round glasses, light mustache, wearing a light blue casual t-shirt and white pants.",
            },
            "side": {
                "path": os.path.abspath(f"{portrait_dir}/side.png"),
                "description": "A front close-up view of Arjun -- a young South Asian man with curly dark hair, round glasses, light mustache, wearing a striped light shirt with a backpack and lanyard.",
            },
            "back": {
                "path": os.path.abspath(f"{portrait_dir}/back.png"),
                "description": "A close-up selfie of Arjun -- a young South Asian man with curly dark hair, round glasses, light mustache, wearing a rust-brown sweater.",
            },
        }
    }

    registry_path = os.path.join(WORKING_DIR, "character_portraits_registry.json")
    with open(registry_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=4)

    print(f"Character portrait registry created at {registry_path}")
    return registry


def setup_characters():
    """Create the character definition and save it."""
    characters = [
        CharacterInScene(
            idx=0,
            identifier_in_scene="Arjun",
            static_features="Young South Asian man in his early 20s, curly dark hair, round glasses, light mustache, medium build",
            dynamic_features="Wears a casual light-colored t-shirt, sometimes with a backpack slung over one shoulder. Carries a glowing holographic tablet.",
            is_visible=True,
        )
    ]

    characters_path = os.path.join(WORKING_DIR, "characters.json")
    with open(characters_path, "w", encoding="utf-8") as f:
        json.dump([c.model_dump() for c in characters], f, ensure_ascii=False, indent=4)

    print(f"Characters saved to {characters_path}")
    return characters


async def main():
    os.makedirs(WORKING_DIR, exist_ok=True)

    config = load_config("configs/happycapy_script2video.yaml")

    # Override working dir
    config["working_dir"] = WORKING_DIR

    chat_model = init_chat_model(**config["chat_model"]["init_args"])
    backend = RenderBackend.from_config(config)

    pipeline = Script2VideoPipeline(
        chat_model=chat_model,
        image_generator=backend.image_generator,
        video_generator=backend.video_generator,
        working_dir=WORKING_DIR,
    )

    # Pre-populate characters and portraits (skip AI generation)
    characters = setup_characters()
    portrait_registry = setup_character_portraits()

    print("\n" + "=" * 60)
    print("Starting ViMax Script2Video Pipeline")
    print("=" * 60)
    print(f"Working dir: {WORKING_DIR}")
    print(f"Characters: {[c.identifier_in_scene for c in characters]}")
    print(f"Style: {STYLE}")
    print("=" * 60 + "\n")

    # Run the full pipeline with pre-populated characters and portraits
    final_video_path = await pipeline(
        script=SCRIPT,
        user_requirement=USER_REQUIREMENT,
        style=STYLE,
        characters=characters,
        character_portraits_registry=portrait_registry,
    )

    print(f"\nFinal video: {final_video_path}")


if __name__ == "__main__":
    asyncio.run(main())
