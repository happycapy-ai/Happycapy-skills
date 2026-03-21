from pydantic import BaseModel, Field
from typing import List, Optional, Union, Dict
from PIL import Image



class EnvironmentInScene(BaseModel):
    slugline: str = Field(
        description="The slugline of the scene, indicating the location and time of day",
        examples=[
            "INT. COFFEE SHOP - NIGHT",
            "EXT. PARK - DAY",
        ]
    )
    description: str = Field(
        description="A detailed description of the environment in the specific scene. Don't describe any characters or actions here, just the setting.",
        examples=[
            "The warm yellow light glowed against the mottled brick wall, while raindrops streaked the glass window with blurred neon reflections. Among the empty booths sat a lone half-finished iced latte—its foam collapsed, a faint lipstick mark on the rim. beads of condensation gleamed on the stainless steel espresso machine, and the record player's turntable rotated slowly in the shadows. A patch of wet floor shimmered with hazy reflected light.",
        ]
    )

    def __str__(self):
        s = f"{self.slugline} -- {self.description}"
        return s


