from pydantic import BaseModel, Field
from typing import List, Optional, Union, Dict, Tuple, Literal


class Frame(BaseModel):
    shot_idx: int = Field(
        description="The index of the shot in the sequence, starting from 0."
    )

    frame_type: Literal["first", "last"] = Field(
        description="The type of the frame, 'first' for the first frame of the shot, 'last' for the last frame of the shot."
    )

    cam_idx: int = Field(
        description="The index of the camera used for this frame, starting from 0."
    )

    vis_char_idxs: List[int] = Field(
        description="A list of indices of characters that are visible in this frame, corresponding to the character list provided in the input."
    )
