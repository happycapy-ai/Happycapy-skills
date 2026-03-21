import asyncio
from pipelines.script2video_pipeline import Script2VideoPipeline


# SET YOUR OWN SCRIPT, USER REQUIREMENT, AND STYLE HERE
script = \
"""
EXT. SCHOOL GYM - DAY
A group of students are practicing basketball in the gym. The gym is large and open, with a basketball hoop at one end and a large crowd of spectators at the other end. John (18, male, tall, athletic) is the star player, and he is practicing his dribble and shot. Jane (17, female, short, athletic) is the assistant coach, and she is helping John with his practice. The other students are watching the practice and cheering for John.
John: (dribbling the ball) I'm going to score a basket!
Jane: (smiling) Good job, John!
John: (shooting the ball) Yes!
John:(The shot misses. He seems frustrated.) Argh! My follow-through feels off today.
Jane:(Walks over, analytical.) Your elbow is drifting out. Remember, straight as an arrow.
John:(Nods, taking the ball again.) Straight as an arrow... Let me try again.
(John takes another shot. This time, the ball swishes through the net perfectly.)
Jane:(Clapping.) There it is! Perfect form! That's the shot we need for the championship.
John:(Retrieving the ball, smiling with renewed confidence.) Thanks, Coach Jane. I just needed you to point it out. One more time?
"""
user_requirement = \
"""
Fast-paced with no more than 15 shots.
"""
style = "Anime Style"



async def main():
    pipeline = Script2VideoPipeline.init_from_config(config_path="configs/script2video.yaml")
    await pipeline(script=script, user_requirement=user_requirement, style=style)


if __name__ == "__main__":
    asyncio.run(main())
