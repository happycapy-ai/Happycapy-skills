#!/usr/bin/env python3
import argparse
import json
import os
import shutil
import subprocess
import time
from pathlib import Path

from google import genai
from google.genai import types


def image_from_path(path: str):
    resolved = Path(path).resolve()
    mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg"}[
        resolved.suffix.lower()
    ]
    return resolved, types.Image(image_bytes=resolved.read_bytes(), mime_type=mime)


def run_ffmpeg(args):
    if shutil.which("ffmpeg"):
        subprocess.run(["ffmpeg", "-y", *args], check=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--first-frame", required=True)
    parser.add_argument("--last-frame", required=True)
    parser.add_argument("--prompt-file", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--gcs-uri", required=True)
    parser.add_argument("--model", default="veo-3.1-fast-generate-001")
    parser.add_argument("--native-duration", type=int, default=8)
    parser.add_argument("--final-duration", type=int, default=10)
    parser.add_argument("--aspect-ratio", default="9:16")
    parser.add_argument("--resolution", default="720p")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    first_path, first = image_from_path(args.first_frame)
    last_path, last = image_from_path(args.last_frame)
    prompt = Path(args.prompt_file).read_text()
    output = Path(args.output_dir).resolve()
    output.mkdir(parents=True, exist_ok=True)

    request = {
        "model": args.model,
        "first_frame": str(first_path),
        "last_frame": str(last_path),
        "prompt": prompt,
        "native_duration_seconds": args.native_duration,
        "final_duration_seconds": args.final_duration,
        "aspect_ratio": args.aspect_ratio,
        "resolution": args.resolution,
        "output_gcs_uri": args.gcs_uri,
    }
    (output / "request.json").write_text(json.dumps(request, ensure_ascii=False, indent=2))
    if args.dry_run:
        print(json.dumps(request, ensure_ascii=False, indent=2))
        return

    client = genai.Client(
        vertexai=True,
        project=os.environ["GOOGLE_CLOUD_PROJECT"],
        location=os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1"),
    )
    operation = client.models.generate_videos(
        model=args.model,
        prompt=prompt,
        image=first,
        config=types.GenerateVideosConfig(
            number_of_videos=1,
            duration_seconds=args.native_duration,
            aspect_ratio=args.aspect_ratio,
            resolution=args.resolution,
            output_gcs_uri=args.gcs_uri,
            generate_audio=False,
            last_frame=last,
        ),
    )
    (output / "operation.json").write_text(json.dumps({"name": operation.name}, indent=2))
    print(f"Submitted: {operation.name}", flush=True)
    while not operation.done:
        time.sleep(15)
        operation = client.operations.get(operation)
        print(f"done={operation.done}", flush=True)

    (output / "result.txt").write_text(str(operation))
    if operation.error:
        raise SystemExit(f"Veo failed: {operation.error}")

    uri = operation.result.generated_videos[0].video.uri
    native_video = output / f"veo-native-{args.native_duration}s.mp4"
    final_video = output / f"final-{args.final_duration}s.mp4"
    subprocess.run(["gcloud", "storage", "cp", uri, str(native_video)], check=True)

    if args.final_duration > args.native_duration:
        pad = args.final_duration - args.native_duration
        run_ffmpeg(
            [
                "-i",
                str(native_video),
                "-filter_complex",
                f"[0:v]tpad=stop_mode=clone:stop_duration={pad}[v]",
                "-map",
                "[v]",
                "-an",
                "-t",
                str(args.final_duration),
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                str(final_video),
            ]
        )
    else:
        shutil.copy2(native_video, final_video)

    last_frame_index = max(args.final_duration * 24 - 1, 1)
    sample_frames = [
        0,
        round(last_frame_index * 0.2),
        round(last_frame_index * 0.4),
        round(last_frame_index * 0.6),
        last_frame_index,
    ]
    select = "+".join(f"eq(n,{frame})" for frame in sample_frames)
    run_ffmpeg(
        [
            "-i",
            str(final_video),
            "-vf",
            f"select='{select}',scale=144:256,tile=5x1",
            "-frames:v",
            "1",
            str(output / "contact-sheet.png"),
        ]
    )


if __name__ == "__main__":
    main()

