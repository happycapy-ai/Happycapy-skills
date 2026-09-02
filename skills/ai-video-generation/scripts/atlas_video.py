#!/usr/bin/env python3
"""Generate one text-to-video clip through the optional Atlas Cloud provider."""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Callable, Optional
from urllib import error as url_error
from urllib import request as url_request
from urllib.parse import urlparse


API_ROOT = "https://api.atlascloud.ai"
CATALOG_URL = f"{API_ROOT}/api/v1/models"
DEFAULT_MODEL = "bytedance/seedance-v1-pro-fast/text-to-video"
SUCCESS_STATUSES = {"completed", "succeeded", "success"}
FAILURE_STATUSES = {"failed", "canceled", "cancelled", "error"}


class ConfirmationRequired(RuntimeError):
    """Raised when live preflight succeeds but a billable run is unconfirmed."""


def read_json(url: str, *, api_key: Optional[str] = None) -> dict[str, Any]:
    headers = {"Accept": "application/json", "User-Agent": "happycapy-atlas-video/1"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    req = url_request.Request(url, headers=headers, method="GET")
    with url_request.urlopen(req, timeout=60) as response:
        value = json.loads(response.read().decode("utf-8"))
    if not isinstance(value, dict):
        raise ValueError("Atlas GET returned a non-object response")
    return value


def post_json_once(
    url: str, *, api_key: str, payload: dict[str, Any]
) -> dict[str, Any]:
    """Submit exactly one generation POST, with no automatic retry."""
    req = url_request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "happycapy-atlas-video/1",
        },
        method="POST",
    )
    try:
        with url_request.urlopen(req, timeout=120) as response:
            value = json.loads(response.read().decode("utf-8"))
    except url_error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"Atlas submit failed ({exc.code}): {detail}") from exc
    if not isinstance(value, dict):
        raise ValueError("Atlas POST returned a non-object response")
    return value


def _walk(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from _walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from _walk(child)


def find_model(catalog: dict[str, Any], model: str) -> dict[str, Any]:
    matches = [
        item
        for item in _walk(catalog)
        if item.get("model") == model
        and item.get("type") == "Video"
        and item.get("display_console") is True
    ]
    if len(matches) != 1:
        raise ValueError(f"Atlas video model is unavailable or ambiguous: {model}")
    return matches[0]


def validate_payload(schema: dict[str, Any], payload: dict[str, Any]) -> None:
    input_schema = schema.get("components", {}).get("schemas", {}).get("Input", {})
    properties = input_schema.get("properties")
    if not isinstance(properties, dict):
        raise ValueError("Atlas model schema is missing Input.properties")
    missing = sorted(set(input_schema.get("required", [])).difference(payload))
    if missing:
        raise ValueError(f"Atlas request is missing required fields: {', '.join(missing)}")
    unknown = sorted(set(payload).difference(properties))
    if unknown:
        raise ValueError(f"Atlas request contains unsupported fields: {', '.join(unknown)}")
    for name, value in payload.items():
        choices = properties.get(name, {}).get("enum")
        if choices and value not in choices:
            raise ValueError(f"Atlas {name} must be one of: {', '.join(map(str, choices))}")


def _unwrap(response: dict[str, Any]) -> dict[str, Any]:
    if "code" in response and str(response.get("code")) != "200":
        raise RuntimeError(
            f"Atlas API returned code {response.get('code')}: {response.get('message')}"
        )
    payload = response.get("data", response)
    if not isinstance(payload, dict):
        raise ValueError("Atlas response is missing an object payload")
    return payload


def result_path(schema: dict[str, Any]) -> str:
    for path, operations in schema.get("paths", {}).items():
        if "{request_id}" in path and isinstance(operations, dict) and "get" in operations:
            return path
    return "/api/v1/model/prediction/{request_id}"


def unit_price(model: dict[str, Any]) -> str:
    return str(model.get("price", {}).get("actual", {}).get("base_price", "unknown"))


def generate(
    *,
    api_key: str,
    payload: dict[str, Any],
    output: Path,
    confirmed: bool,
    poll_attempts: int = 45,
    get_json: Callable[..., dict[str, Any]] = read_json,
    post_json: Callable[..., dict[str, Any]] = post_json_once,
    get_bytes: Optional[Callable[[str], bytes]] = None,
    sleep_fn: Callable[[float], None] = time.sleep,
) -> dict[str, Any]:
    """Preflight live metadata, submit once, then poll with bounded GET retry."""
    catalog = get_json(CATALOG_URL, api_key=api_key)
    model_entry = find_model(catalog, payload["model"])
    schema_url = model_entry.get("schema")
    if not isinstance(schema_url, str) or urlparse(schema_url).scheme != "https":
        raise ValueError("Atlas model catalog is missing an HTTPS schema URL")
    schema = get_json(schema_url)
    validate_payload(schema, payload)

    price = unit_price(model_entry)
    print(
        f"Atlas plan: model={payload['model']} duration={payload.get('duration')} "
        f"resolution={payload.get('resolution')} unit_price={price}",
        flush=True,
    )
    if not confirmed:
        raise ConfirmationRequired(
            "Atlas generation is billable. Review the plan and rerun with --yes."
        )

    submitted = _unwrap(
        post_json(
            f"{API_ROOT}/api/v1/model/generateVideo",
            api_key=api_key,
            payload=payload,
        )
    )
    prediction_id = submitted.get("id") or submitted.get("prediction_id")
    if not isinstance(prediction_id, str) or not prediction_id:
        raise ValueError("Atlas submit response is missing a prediction id")

    url = f"{API_ROOT}{result_path(schema).replace('{request_id}', prediction_id)}"
    completed: Optional[dict[str, Any]] = None
    for poll_index in range(poll_attempts):
        last_error: Optional[Exception] = None
        for retry_index in range(4):
            try:
                prediction = _unwrap(get_json(url, api_key=api_key))
                last_error = None
                break
            except (OSError, RuntimeError, ValueError, url_error.URLError) as exc:
                last_error = exc
                if retry_index < 3:
                    sleep_fn(float(2**retry_index))
        if last_error is not None:
            raise RuntimeError(f"Atlas prediction GET failed after 4 attempts: {last_error}")
        status = str(prediction.get("status", "")).lower()
        if status in SUCCESS_STATUSES:
            completed = prediction
            break
        if status in FAILURE_STATUSES:
            raise RuntimeError(f"Atlas prediction {status}: {prediction.get('error', 'no detail')}")
        if poll_index + 1 < poll_attempts:
            sleep_fn(float(min(2**poll_index, 8)))
    if completed is None:
        raise TimeoutError(f"Atlas prediction did not finish after {poll_attempts} polls")

    outputs = completed.get("outputs") or completed.get("output")
    if isinstance(outputs, str):
        outputs = [outputs]
    if not isinstance(outputs, list) or not outputs or not isinstance(outputs[0], str):
        raise ValueError("Atlas prediction completed without a video URL")
    video_url = outputs[0]
    parsed_video_url = urlparse(video_url)
    if parsed_video_url.scheme != "https":
        raise ValueError("Atlas output URL must use HTTPS")

    if get_bytes is None:
        def get_bytes(download_url: str) -> bytes:
            req = url_request.Request(
                download_url,
                headers={"User-Agent": "happycapy-atlas-video/1"},
                method="GET",
            )
            with url_request.urlopen(req, timeout=300) as response:
                return response.read()

    content = get_bytes(video_url)
    if len(content) < 1024:
        raise ValueError("Atlas video output is unexpectedly small")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(content)
    metadata = {
        "gateway": "atlas-cloud",
        "model": payload["model"],
        "prediction_id": prediction_id,
        "unit_price": price,
        "request": payload,
        "output_url": parsed_video_url._replace(query="", fragment="").geturl(),
        "bytes": len(content),
    }
    Path(str(output) + ".meta.json").write_text(
        json.dumps(metadata, indent=2), encoding="utf-8"
    )
    return metadata


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--duration", type=int, default=4)
    parser.add_argument("--resolution", default="480p")
    parser.add_argument("--aspect-ratio", default="16:9")
    parser.add_argument("--camera-fixed", action="store_true")
    parser.add_argument("--seed", type=int, default=-1)
    parser.add_argument("--yes", action="store_true")
    args = parser.parse_args()

    api_key = os.environ.get("ATLASCLOUD_API_KEY") or os.environ.get("ATLAS_CLOUD_API_KEY")
    if not api_key:
        sys.exit("ERROR: ATLASCLOUD_API_KEY is required")
    try:
        generate(
            api_key=api_key,
            payload={
                "model": args.model,
                "prompt": args.prompt,
                "duration": args.duration,
                "resolution": args.resolution,
                "aspect_ratio": args.aspect_ratio,
                "camera_fixed": args.camera_fixed,
                "seed": args.seed,
            },
            output=args.output,
            confirmed=args.yes,
        )
    except ConfirmationRequired as exc:
        sys.exit(f"ERROR: {exc}")
    print(f"Saved video to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
