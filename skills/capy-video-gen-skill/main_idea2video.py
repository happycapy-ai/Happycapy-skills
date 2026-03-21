import asyncio
from pipelines.idea2video_pipeline import Idea2VideoPipeline


# SET YOUR OWN IDEA, USER REQUIREMENT, AND STYLE HERE
idea = \
    """
A beaufitul fit woman with black hair, great butt and thigs is exercising in a
gym surrounded by glass windows with a beautiful beach view on the outside.
She is performing glute exercises that highlight her beautiful back and sexy outfit
and showing the audience the proper form. Between the 3 different exercises she looks
at the camera with a gorgeous look asking the viewer understood the proper form.
"""
user_requirement = \
    """
For adults, do not exceed 3 scenes. Each scene should be no more than 5 shots.
"""
style = "Realistic, warm feel"


async def main():
    pipeline = Idea2VideoPipeline.init_from_config(
        config_path="configs/idea2video.yaml")
    await pipeline(idea=idea, user_requirement=user_requirement, style=style)

if __name__ == "__main__":
    asyncio.run(main())
