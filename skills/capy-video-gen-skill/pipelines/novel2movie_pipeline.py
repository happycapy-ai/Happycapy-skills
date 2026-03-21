# TODO: NOT IMPLEMENTED YET

import os
import shutil
import yaml
import json
import importlib
import asyncio
from typing import List, Dict
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from PIL import Image

from components.event import Event
from components.scene import Scene
from components.character import CharacterInScene, CharacterInNovel, CharacterInEvent
from pipelines.base import BasePipeline
from tenacity import retry

class Novel2MoviePipeline(BasePipeline):

    async def __call__(
        self,
        novel_text: str,
        style: str,
    ):
        print("🎬 Novel to Movie Pipeline Started".center(80, "="))

        # Step 1: Compress the novel text
        print()
        print("📋 Step 1: Compress the novel text".center(80, "-"))

        working_dir_novel_compressor = os.path.join(self.working_dir, "novel")
        os.makedirs(working_dir_novel_compressor, exist_ok=True)
        with open(os.path.join(working_dir_novel_compressor, "novel.txt"), "w", encoding="utf-8") as f:
            f.write(novel_text)
        print(f"🗂️ Working directory: {working_dir_novel_compressor}")

        print("🔖 Splitting the novel into chunks...")
        novel_chunks = self.novel_compressor.split(novel_text)
        for idx, novel_chunk in enumerate(novel_chunks):
            with open(os.path.join(working_dir_novel_compressor, f"novel_chunk_{idx}.txt"), "w", encoding="utf-8") as f:
                f.write(novel_chunk)
        print(f"🔖 Split the novel into {len(novel_chunks)} chunks, all saved to {working_dir_novel_compressor}.")


        print()
        print("🔖 Compressing the novel chunks...")
        compressed_novel_chunks = [None] * len(novel_chunks)
        index_chunk_pairs_unfinished = []
        for index, novel_chunk in enumerate(novel_chunks):
            path = os.path.join(working_dir_novel_compressor, f"novel_chunk_{index}_compressed.txt")
            if os.path.exists(path):
                compressed_novel_chunks[index] = open(path, "r", encoding="utf-8").read()
                print(f"⏭️ Skipping compression for chunk {index} as it already exists.")
            else:
                index_chunk_pairs_unfinished.append((index, novel_chunk))

        sem = asyncio.Semaphore(5)
        tasks = [
            self.novel_compressor.compress_single_novel_chunk(sem, index, novel_chunk)
            for index, novel_chunk in index_chunk_pairs_unfinished
        ]
        task_outputs = await asyncio.gather(*tasks)
        for index, novel_chunk_compressed in task_outputs:
            save_path = os.path.join(working_dir_novel_compressor, f"novel_chunk_{index}_compressed.txt")
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(novel_chunk_compressed)
            print(f"✅ Compressed chunk {index}, saved to {save_path}")
            compressed_novel_chunks[index] = novel_chunk_compressed
        print("🔖 Compressed all novel chunks.")


        print()
        print("🔖 Merging the compressed novel chunks...")
        path = os.path.join(working_dir_novel_compressor, "novel_compressed.txt")
        if os.path.exists(path):
            compressed_novel = open(path, "r", encoding="utf-8").read()
            print(f"⏭️ Skipping merging as {path} already exists.")
        else:
            compressed_novel = self.novel_compressor.aggregate(compressed_novel_chunks)
            with open(path, "w", encoding="utf-8") as f:
                f.write(compressed_novel)
            print(f"✅ Merged the compressed novel chunks, saved to {path}")
        print(f"🔖 Merging completed.")

        # summary
        print()
        print("📌 Summary:")
        print(f"📌 Before Compression: {len(novel_text)} characters")
        print(f"📌 After Compression: {len(compressed_novel)} characters")
        print(f"📌 Compression Ratio: {len(compressed_novel) / len(novel_text):.2%}")

        print("📋 Step 1: Compress the novel text".center(80, "-"))


        # Step 2: Extract events from the compressed novel
        print()
        print("📋 Step 2: Extract events from the compressed novel".center(80, "-"))
        working_dir_event_extractor = os.path.join(self.working_dir, "events")
        os.makedirs(working_dir_event_extractor, exist_ok=True)
        print(f"🗂️ Working directory: {working_dir_event_extractor}")

        extracted_events = []
        for event_json_fname in sorted(os.listdir(working_dir_event_extractor), key=lambda x: int(x.split('_')[1].split('.')[0])):
            event_json_path = os.path.join(working_dir_event_extractor, event_json_fname)
            if os.path.exists(event_json_path):
                with open(event_json_path, "r", encoding="utf-8") as f:
                    event_data = json.load(f)
                event: Event = Event.model_validate(event_data)
                extracted_events.append(event)

        if len(extracted_events) > 0:
            if extracted_events[-1].is_last:
                print(f"⏭️ Skipping event extraction as all events already exist in {working_dir_event_extractor}.")
            else:
                print(f"🔖 Continuing event extraction from {len(extracted_events)} existing events...")
        else:
            print("🔖 Starting event extraction ...")

        while len(extracted_events) == 0 or not extracted_events[-1].is_last:
            next_event = self.event_extractor.extract_next_event(
                novel_text=compressed_novel,
                extracted_events=extracted_events,
            )
            event_json_path = os.path.join(working_dir_event_extractor, f"event_{len(extracted_events)}.json")
            with open(event_json_path, "w", encoding="utf-8") as f:
                json.dump(next_event.model_dump(), f, ensure_ascii=False, indent=4)
            print(f"✅ Extracted event {next_event.index}, saved to {event_json_path}")

            extracted_events.append(next_event)

        # summary
        print()
        print("📌 Summary:")
        print(f"📌 Extracted a total of {len(extracted_events)} events.")

        print("📋 Step 2: Extract events from the compressed novel".center(80, "-"))


        # Step 3:  Extract relevant chunks for each event
        print()
        print("📋 Step 3: Retrieve relevant chunks for each event".center(80, "-"))
        working_dir_knowledge_base = os.path.join(self.working_dir, "knowledge_base")
        working_dir_retrieve = os.path.join(self.working_dir, "relevant_chunks")
        os.makedirs(working_dir_knowledge_base, exist_ok=True)
        os.makedirs(working_dir_retrieve, exist_ok=True)
        print(f"🗂️ Working directory: {working_dir_knowledge_base} and {working_dir_retrieve}")

        print("🔖 Constructing knowledge base from the raw novel text...")
        embeddings = CacheBackedEmbeddings.from_bytes_store(
            underlying_embeddings=self.embeddings,
            document_embedding_cache=LocalFileStore(
                root_path=working_dir_knowledge_base,
            ),
            namespace=self.embeddings.model,
            key_encoder="sha256",
        )
        novel_splitter = RecursiveCharacterTextSplitter(
            chunk_size=512,
            chunk_overlap=128,
        )
        novel_chunks = novel_splitter.split_text(novel_text)
        knowledge_base = FAISS.from_texts(texts=novel_chunks, embedding=embeddings)
        print(f"🔖 Constructed knowledge base with {len(novel_chunks)} chunks, saved to {working_dir_knowledge_base}")


        print("🔖 Retrieving relevant chunks for each event...")
        async def retrieve_relevant_chunks(sem, knowledge_base, event):
            async with sem:
                relevant_chunk_score_dict = {}
                for process in event.process_chain:
                    chunks = knowledge_base.similarity_search(process, k=10)
                    chunks = [chunk.page_content for chunk in chunks if chunk.page_content not in relevant_chunk_score_dict]

                    chunk_score_pairs = await self.rerank_model(
                        documents=chunks,
                        query=process,
                        top_n=10,
                    )

                    threshold = 0.7
                    for chunk, score in chunk_score_pairs:
                        if score >= threshold:
                            if chunk not in relevant_chunk_score_dict:
                                relevant_chunk_score_dict[chunk] = score
                            else:
                                relevant_chunk_score_dict[chunk] += score

            return event.index, relevant_chunk_score_dict

        event_idx_to_relevant_chunk_score_dict = {}

        sem = asyncio.Semaphore(10)
        tasks = []
        for event in extracted_events:
            chunks_dir = os.path.join(working_dir_retrieve, f"event_{event.index}")
            if os.path.exists(chunks_dir) and len(os.listdir(chunks_dir)) > 0:
                relevant_chunk_score_dict = {}
                for chunk_fname in os.listdir(chunks_dir):
                    chunk_path = os.path.join(chunks_dir, chunk_fname)
                    score = float(chunk_fname.split('-score_')[1].split('.txt')[0])
                    with open(chunk_path, "r", encoding="utf-8") as f:
                        chunk = f.read()
                    relevant_chunk_score_dict[chunk] = score
                event_idx_to_relevant_chunk_score_dict[event.index] = relevant_chunk_score_dict
                print(f"⏭️ Skipping retrieval for event {event.index} as it already exists.")
            else:
                tasks.append(retrieve_relevant_chunks(sem, knowledge_base, event))

        if len(tasks) > 0:
            for task in asyncio.as_completed(tasks):
                event_index, relevant_chunk_score_dict = await task
                chunks_dir = os.path.join(working_dir_retrieve, f"event_{event_index}")
                os.makedirs(chunks_dir, exist_ok=True)
                for idx, (chunk, score) in enumerate(relevant_chunk_score_dict.items()):
                    chunk_path = os.path.join(chunks_dir, f"chunk_{idx}-score_{score:.2f}.txt")
                    with open(chunk_path, "w", encoding="utf-8") as f:
                        f.write(chunk)
                event_idx_to_relevant_chunk_score_dict[event_index] = relevant_chunk_score_dict
                print(f"✅ Retrieved {len(relevant_chunk_score_dict)} relevant chunks for event {event_index}, saved to {chunks_dir}")

        print("🔖 Retrieved relevant chunks for all events.")
        print("📋 Step 3: Retrieve relevant chunks for each event".center(80, "-"))



        # Step 4: Extract scenes for each event, design the script for each scene
        print()
        print("📋 Step 4: Extract scenes for each event, design the script for each scene".center(80, "-"))
        working_dir_scene_extractor = os.path.join(self.working_dir, "scenes")
        os.makedirs(working_dir_scene_extractor, exist_ok=True)
        print(f"🗂️ Working directory: {working_dir_scene_extractor}")


        unfinished_event_indices = []
        event_idx_to_scenes = {event.index: [] for event in extracted_events}
        for event in extracted_events:
            scenes_dir = os.path.join(working_dir_scene_extractor, f"event_{event.index}")
            if os.path.exists(scenes_dir):
                for scene_json_fname in sorted(os.listdir(scenes_dir), key=lambda x: int(x.split('_')[1].split('.')[0])):
                    scene_json_path = os.path.join(scenes_dir, scene_json_fname)
                    with open(scene_json_path, "r", encoding="utf-8") as f:
                        scene_data = json.load(f)
                    scene = Scene.model_validate(scene_data)
                    event_idx_to_scenes[event.index].append(scene)

            if len(event_idx_to_scenes[event.index]) > 0 and event_idx_to_scenes[event.index][-1].is_last:
                print(f"⏭️ Skipping scene extraction for event {event.index} as all scenes already exist in {scenes_dir}.")
            else:
                unfinished_event_indices.append(event.index)

        if len(unfinished_event_indices) > 0:
            if len(unfinished_event_indices) == len(extracted_events):
                print(f"🔖 Starting scene extraction for all events...")
            else:
                print(f"🔖 Continuing scene extraction for events: {unfinished_event_indices}")


        async def extract_scenes_for_event(sem, relevant_chunks, event, previous_scenes):
            async with sem:
                os.makedirs(os.path.join(working_dir_scene_extractor, f"event_{event.index}"), exist_ok=True)

                while len(previous_scenes) == 0 or not previous_scenes[-1].is_last:
                    next_scene = await self.scene_extractor.get_next_scene(
                        relevant_chunks=relevant_chunks,
                        event=event,
                        previous_scenes=previous_scenes,
                    )
                    scene_json_path = os.path.join(working_dir_scene_extractor, f"event_{event.index}", f"scene_{len(previous_scenes)}.json")
                    with open(scene_json_path, "w", encoding="utf-8") as f:
                        json.dump(next_scene.model_dump(), f, ensure_ascii=False, indent=4)
                    print(f"✔️​ Extracted scene {next_scene.idx} for event {event.index}, saved to {scene_json_path}")
                    previous_scenes.append(next_scene)

            print(f"✅ Extracted all {len(previous_scenes)} scenes for event {event.index}.")
            return event.index, previous_scenes


        sem = asyncio.Semaphore(8)
        for event_index in unfinished_event_indices:
            relevant_chunks = list(event_idx_to_relevant_chunk_score_dict[event_index].keys())
            tasks.append(extract_scenes_for_event(sem, relevant_chunks, extracted_events[event_index], event_idx_to_scenes[event_index]))

        task_outputs = await asyncio.gather(*tasks)
        for event_index, previous_scenes in task_outputs:
            event_idx_to_scenes[event_index] = previous_scenes

        print("🔖 Extracted scenes for all events.")
        print("📋 Step 4: Extract scenes for each event, design the script for each scene".center(80, "-"))



        # Step 5: Merge characters from scene-level to event-level, then to novel-level
        print()
        print("📋 Step 5: Merge characters from scene-level to novel-level".center(80, "-"))
        working_dir_global_information_planner = os.path.join(self.working_dir, "global_information")
        os.makedirs(working_dir_global_information_planner, exist_ok=True)
        print(f"🗂️ Working directory: {working_dir_global_information_planner}")

        # Step 5.1: Merge characters from scene-level to event-level
        print("🔖 Merging characters across scenes in each event...")
        working_dir_characters = os.path.join(working_dir_global_information_planner, "characters")
        os.makedirs(working_dir_characters, exist_ok=True)

        async def merge_characters_across_scenes_in_event(sem, event_idx, scenes):
            async with sem:
                merged_characters = await self.global_information_planner.merge_characters_across_scenes_in_event(
                    event_idx=event_idx,
                    scenes=scenes,
                )
                path = os.path.join(working_dir_characters, "event_level", f"event_{event_idx}_characters.json")
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as f:
                    json.dump([char.model_dump() for char in merged_characters], f, ensure_ascii=False, indent=4)
                print(f"✅ Merged characters for event {event_idx}, saved to {path}")

            return event_idx, merged_characters


        event_idx_to_characters_in_event = {}

        sem = asyncio.Semaphore(8)
        tasks = []
        for event in extracted_events:
            path = os.path.join(working_dir_characters, "event_level", f"event_{event.index}_characters.json")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    character_data = json.load(f)
                characters = [CharacterInEvent.model_validate(char) for char in character_data]
                event_idx_to_characters_in_event[event.index] = characters
                print(f"⏭️ Skipping character merging for event {event.index} as it already exists.")
            else:
                tasks.append(merge_characters_across_scenes_in_event(sem, event.index, event_idx_to_scenes[event.index]))

        task_outputs = await asyncio.gather(*tasks)
        for event_index, merged_characters in task_outputs:
            event_idx_to_characters_in_event[event_index] = merged_characters

        print("🔖 Merged characters across scenes in each event.")

        # Step 5.2: Merge characters from event-level to novel-level
        print("🔖 Merging characters across events in the novel...")

        working_dir_characters_novel = os.path.join(working_dir_characters, f"novel_level")
        os.makedirs(working_dir_characters_novel, exist_ok=True)

        fnames = os.listdir(working_dir_characters_novel)
        existing_characters_in_novel = []
        if len(fnames) > 0:
            fname = max(fnames, key=lambda x: int(x.split('_')[-1].split('.json')[0]))
            start_event_idx = int(fname.split('_')[-1].split('.json')[0]) + 1
            path = os.path.join(working_dir_characters_novel, fname)
            with open(path, "r", encoding="utf-8") as f:
                character_data = json.load(f)
            existing_characters_in_novel = [CharacterInNovel.model_validate(char) for char in character_data]
            
            if start_event_idx == len(extracted_events):
                print(f"⏭️ Skipping merging as all events already merged to novel-level in {working_dir_characters_novel}.")
            else:
                print(f"🔖 Continuing merging from event {start_event_idx}, currently {len(existing_characters_in_novel)} characters in novel.")

        else:
            existing_characters_in_novel = []
            start_event_idx = 0

        for event in extracted_events[start_event_idx:]:
            characters_in_event = event_idx_to_characters_in_event[event.index]
            path = os.path.join(working_dir_characters_novel, f"novel_characters_after_event_{event.index}.json")
            existing_characters_in_novel = self.global_information_planner.merge_characters_to_existing_characters_in_novel(
                event_idx=event.index,
                existing_characters_in_novel=existing_characters_in_novel,
                characters_in_event=characters_in_event,
            )
            with open(path, "w", encoding="utf-8") as f:
                json.dump([char.model_dump() for char in existing_characters_in_novel], f, ensure_ascii=False, indent=4)
            print(f"✅ Merged characters from event {event.index} to novel-level, now {len(existing_characters_in_novel)} characters in novel, saved to {path}")

        print("🔖 Merged characters across events in the novel.")

        characters_in_novel = existing_characters_in_novel

        print("📋 Step 5: Merge characters from scene-level to novel-level".center(80, "-"))




        # Step 6: Generate the portrait for all characters in the novel
        print()
        print("📋 Step 6: Generate the reference images for all characters in the specific scene")

        working_dir_character_portrait = os.path.join(self.working_dir, "character_portraits")
        os.makedirs(working_dir_character_portrait, exist_ok=True)
        print(f"🗂️ Working directory: {working_dir_character_portrait}")

        print("🔖 Generating character portraits based on static features ...")
        base_character_portrait_dir = os.path.join(working_dir_character_portrait, "base")
        os.makedirs(base_character_portrait_dir, exist_ok=True)

        async def generate_portrait_for_character(sem, character: CharacterInNovel):
            async with sem:
                image_path = os.path.join(base_character_portrait_dir, f"character_{character.index}_{character.identifier_in_novel}.png")
                
                if os.path.exists(image_path):
                    print(f"⏭️ Skipping portrait generation for character {character.index} as it already exists.")
                    return

                prompt = f"Generate a full-body, front-view portrait based on the following description, in the style of {style}:"
                prompt += f"\nCharacter Identifier: {character.identifier_in_novel}"
                prompt += f"\nFeatures: {character.static_features}"
                prompt += f"\nThe character should be centered in the image, occupying most of the frame. Gazing straight ahead. Standing with arms relaxed at sides. Natural expression. The background should be plain white."

                image = await self.image_generator.generate_single_image(
                    prompt=prompt,
                    size="512x512",
                )
                image.save(image_path)
                print(f"✅ Generated portrait for character {character.index} ({character.identifier_in_novel}), saved to {image_path}")


        sem = asyncio.Semaphore(5)
        tasks = [
            generate_portrait_for_character(sem, character)
            for character in characters_in_novel
        ]

        await asyncio.gather(*tasks)
        print("🔖 Generated character portraits based on static features.")


        print("🔖 Generating character portraits based on dynamic features in the specific scene")

        async def generate_portrait_for_character_in_scene(
            sem,
            base_character_image_path: str,
            character: CharacterInScene,
            event_idx: int,
            scene_idx: int,
        ):
            async with sem:
                image_path = os.path.join(
                    working_dir_character_portrait,
                    f"event_{event_idx}",
                    f"scene_{scene_idx}",
                    f"character_{character.index}_{character.identifier_in_scene}.png",
                )
                os.makedirs(os.path.dirname(image_path), exist_ok=True)

                if os.path.exists(image_path):
                    print(f"⏭️ Skipping portrait generation for event {event_idx}, scene {scene_idx}, character {character.index} as it already exists.")
                    return

                if not character.is_visible:
                    shutil.copy(base_character_image_path, image_path)
                    print(f"⏭️ For event {event_idx}, scene {scene_idx}, character {character.index} ({character.identifier_in_scene}) is not visible, copied base portrait to {image_path}")
                    return

                if character.dynamic_features is None:
                    shutil.copy(base_character_image_path, image_path)
                    print(f"⏭️ For event {event_idx}, scene {scene_idx}, character {character.index} ({character.identifier_in_scene}) has no dynamic features, copied base portrait to {image_path}")
                    return

                prompt = f"Generate a full-body, front-view portrait based on the provided base image. Modify the base image according to the following dynamic features, in the style of {style}. Keep the character's identity consistent with the base image:"
                prompt += f"\nCharacter Identifier: {character.identifier_in_scene}"
                prompt += f"\nDynamic Features: {character.dynamic_features}"
                prompt += f"\nThe character should be centered in the image, occupying most of the frame. Gazing straight ahead. Standing with arms relaxed at sides. Natural expression. The background should be plain white."

                prompt = await self.rewriter(prompt)


                image = await self.image_generator.generate_single_image(
                    prompt=prompt,
                    reference_image_paths=[base_character_image_path],
                    size="512x512",
                )
                image.save(image_path)
                print(f"✅ For event {event_idx}, scene {scene_idx}, generated portrait for character {character.index} ({character.identifier_in_scene}), saved to {image_path}")


        sem = asyncio.Semaphore(3)
        tasks = []
        for character in characters_in_novel:
            character_base_image_path = os.path.join(base_character_portrait_dir, f"character_{character.index}_{character.identifier_in_novel}.png")
            for event_idx, identifier_in_event in character.active_events.items():
                characters_in_event: List[CharacterInEvent] = event_idx_to_characters_in_event[event_idx]
                character_in_event = [char for char in characters_in_event if char.identifier_in_event == identifier_in_event][0]  # TODO: 这里的数据结构没有做好，居然还要遍历查找。。。
                for scene_idx, identifier_in_scene in character_in_event.active_scenes.items():
                    scene = event_idx_to_scenes[event_idx][scene_idx]
                    character_in_scene: CharacterInScene = [char for char in scene.characters if char.identifier_in_scene == identifier_in_scene][0]  # TODO: 这里的数据结构也没有做好
                    tasks.append(
                        generate_portrait_for_character_in_scene(
                            sem,
                            character_base_image_path,
                            character_in_scene,
                            event_idx,
                            scene_idx,
                        )
                    )
        await asyncio.gather(*tasks)
        print("🔖 Generated character portraits based on dynamic features in the specific scene")

        print("📋 Step 6: Generate the reference images for all characters in the specific scene".center(80, "-"))



        # Step 7: Generate video for each scene
        print("📋 Step 7: Generate the video for each scene".center(80, "-"))
        working_dir_scene_videos = os.path.join(self.working_dir, "videos")
        os.makedirs(working_dir_scene_videos, exist_ok=True)

        for event in extracted_events:
            scenes: List[Scene] = event_idx_to_scenes[event.index]
            for scene in scenes:
                scene_video_dir = os.path.join(working_dir_scene_videos, f"event_{event.index}", f"scene_{scene.idx}")
                os.makedirs(scene_video_dir, exist_ok=True)

                self.script2video_pipeline.working_dir = scene_video_dir
                script = scene.script
                style = "realistic movie style"
                character_registry = {}
                for character in scene.characters:
                    character_registry[character.identifier_in_scene] = [
                        {
                            "path": os.path.join(
                                working_dir_character_portrait,
                                f"event_{event.index}",
                                f"scene_{scene.idx}",
                                f"character_{character.index}_{character.identifier_in_scene}.png",
                            ),
                            "description": f"A portrait of {character.identifier_in_scene}",
                        }
                    ]
                await self.script2video_pipeline(
                    script=script,
                    style=style,
                    character_registry=character_registry
                )
                print(f"✅ Generated video for event {event.index}, scene {scene.idx}, saved to {scene_video_dir}")
        print("📋 Step 7: Generate the video for each scene".center(80, "-"))