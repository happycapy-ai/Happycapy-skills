from pipelines.base import BasePipeline
import os
import logging


class Idea2SVideoPipeline(BasePipeline):

    async def __call__(
        self,
        idea: str,
        style: str,
    ):
        script = await self.idea2script_pipeline(idea=idea)
        await self.script2video_pipeline(script=script, style=style)

        pass

