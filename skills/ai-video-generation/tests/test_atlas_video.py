import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from urllib.error import URLError


SCRIPT = Path(__file__).parents[1] / "scripts" / "atlas_video.py"
SPEC = importlib.util.spec_from_file_location("atlas_video", SCRIPT)
atlas_video = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(atlas_video)


def catalog():
    return {
        "data": [
            {
                "model": atlas_video.DEFAULT_MODEL,
                "type": "Video",
                "display_console": True,
                "schema": "https://static.atlascloud.ai/model/schema/video.json",
                "price": {"actual": {"base_price": "0.009"}},
            }
        ]
    }


def schema():
    return {
        "components": {
            "schemas": {
                "Input": {
                    "required": ["model", "prompt"],
                    "properties": {
                        "model": {"type": "string"},
                        "prompt": {"type": "string"},
                        "duration": {"enum": [2, 4]},
                        "resolution": {"enum": ["480p", "720p"]},
                        "aspect_ratio": {"enum": ["16:9", "9:16"]},
                        "camera_fixed": {"type": "boolean"},
                        "seed": {"type": "integer"},
                    },
                }
            }
        },
        "paths": {"/api/v1/model/result/{request_id}": {"get": {}}},
    }


def request_payload():
    return {
        "model": atlas_video.DEFAULT_MODEL,
        "prompt": "A paper boat crossing a quiet pond",
        "duration": 4,
        "resolution": "480p",
        "aspect_ratio": "16:9",
        "camera_fixed": False,
        "seed": -1,
    }


class AtlasVideoTests(unittest.TestCase):
    def test_finds_exact_visible_video_model_and_price(self):
        entry = atlas_video.find_model(catalog(), atlas_video.DEFAULT_MODEL)
        self.assertEqual(atlas_video.unit_price(entry), "0.009")

    def test_rejects_value_outside_live_schema_enum(self):
        payload = request_payload()
        payload["resolution"] = "4k"
        with self.assertRaisesRegex(ValueError, "resolution must be one of"):
            atlas_video.validate_payload(schema(), payload)

    def test_unconfirmed_preflight_never_submits(self):
        post_calls = []

        def get_json(url, **_kwargs):
            return catalog() if url == atlas_video.CATALOG_URL else schema()

        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(atlas_video.ConfirmationRequired):
                atlas_video.generate(
                    api_key="test-key",
                    payload=request_payload(),
                    output=Path(directory) / "clip.mp4",
                    confirmed=False,
                    get_json=get_json,
                    post_json=lambda *args, **kwargs: post_calls.append((args, kwargs)),
                )
        self.assertEqual(post_calls, [])

    def test_confirmed_generation_posts_once_and_saves_metadata(self):
        post_calls = []
        prediction_calls = []

        def get_json(url, **_kwargs):
            if url == atlas_video.CATALOG_URL:
                return catalog()
            if url.endswith("video.json"):
                return schema()
            prediction_calls.append(url)
            return {"data": {"status": "completed", "outputs": ["https://cdn.example/clip.mp4"]}}

        def post_json(url, **kwargs):
            post_calls.append((url, kwargs))
            return {"data": {"id": "prediction-1"}}

        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "clip.mp4"
            metadata = atlas_video.generate(
                api_key="test-key",
                payload=request_payload(),
                output=output,
                confirmed=True,
                get_json=get_json,
                post_json=post_json,
                get_bytes=lambda _url: b"v" * 2048,
                sleep_fn=lambda _seconds: None,
            )
            self.assertEqual(output.read_bytes(), b"v" * 2048)
            saved = json.loads(Path(str(output) + ".meta.json").read_text())

        self.assertEqual(len(post_calls), 1)
        self.assertEqual(
            post_calls[0][0],
            "https://api.atlascloud.ai/api/v1/model/generateVideo",
        )
        self.assertEqual(
            prediction_calls,
            ["https://api.atlascloud.ai/api/v1/model/result/prediction-1"],
        )
        self.assertEqual(metadata["prediction_id"], "prediction-1")
        self.assertEqual(metadata["output_url"], "https://cdn.example/clip.mp4")
        self.assertEqual(saved["unit_price"], "0.009")

    def test_prediction_get_retries_without_resubmitting(self):
        post_calls = []
        prediction_attempts = []

        def get_json(url, **_kwargs):
            if url == atlas_video.CATALOG_URL:
                return catalog()
            if url.endswith("video.json"):
                return schema()
            prediction_attempts.append(url)
            if len(prediction_attempts) < 3:
                raise URLError("temporary")
            return {"data": {"status": "completed", "outputs": ["https://cdn.example/clip.mp4"]}}

        def post_json(_url, **_kwargs):
            post_calls.append(True)
            return {"data": {"id": "prediction-2"}}

        with tempfile.TemporaryDirectory() as directory:
            atlas_video.generate(
                api_key="test-key",
                payload=request_payload(),
                output=Path(directory) / "clip.mp4",
                confirmed=True,
                get_json=get_json,
                post_json=post_json,
                get_bytes=lambda _url: b"v" * 2048,
                sleep_fn=lambda _seconds: None,
            )

        self.assertEqual(len(post_calls), 1)
        self.assertEqual(len(prediction_attempts), 3)

    def test_signed_output_query_is_not_written_to_metadata(self):
        def get_json(url, **_kwargs):
            if url == atlas_video.CATALOG_URL:
                return catalog()
            if url.endswith("video.json"):
                return schema()
            return {
                "data": {
                    "status": "completed",
                    "outputs": ["https://cdn.example/clip.mp4?signature=secret"],
                }
            }

        with tempfile.TemporaryDirectory() as directory:
            metadata = atlas_video.generate(
                api_key="test-key",
                payload=request_payload(),
                output=Path(directory) / "clip.mp4",
                confirmed=True,
                get_json=get_json,
                post_json=lambda _url, **_kwargs: {"data": {"id": "prediction-3"}},
                get_bytes=lambda _url: b"v" * 2048,
                sleep_fn=lambda _seconds: None,
            )

        self.assertEqual(metadata["output_url"], "https://cdn.example/clip.mp4")


if __name__ == "__main__":
    unittest.main()
