"""YAML config loader with environment variable expansion.

Supports ``${VAR_NAME}`` syntax in YAML values, expanding them from
``os.environ`` at load time.
"""

import os
import re
import yaml


_ENV_RE = re.compile(r"\$\{(\w+)\}")


def _expand_env(value):
    """Recursively expand ${VAR} references in strings, dicts, and lists."""
    if isinstance(value, str):
        return _ENV_RE.sub(lambda m: os.environ.get(m.group(1), ""), value)
    if isinstance(value, dict):
        return {k: _expand_env(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_expand_env(item) for item in value]
    return value


def load_config(path: str) -> dict:
    """Load a YAML config file with environment variable expansion."""
    with open(path, "r") as f:
        raw = yaml.safe_load(f)
    return _expand_env(raw)
