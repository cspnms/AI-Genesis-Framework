"""Configuration handling for AI Genesis Framework.

This module defines default values and provides a light-weight mechanism for
reading user overrides from a local ``.agf.yaml`` file when present. The intent
is to keep configuration simple and transparent while enabling gradual
extensibility.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

try:  # Optional dependency for minimal environments
    import yaml
except ImportError:  # pragma: no cover - fallback
    yaml = None


DEFAULT_OUTPUT_DIR = Path.cwd()
CONFIG_FILE_NAME = ".agf.yaml"


def _load_yaml_config(path: Path) -> Dict[str, Any]:
    if yaml is None:
        return {}
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        return {}
    return data


@dataclass
class AGFConfig:
    """Runtime configuration for AGF."""

    output_dir: Path = DEFAULT_OUTPUT_DIR
    author: str = "Your Name"

    @classmethod
    def from_file(cls, search_dir: Optional[Path] = None) -> "AGFConfig":
        search_dir = search_dir or Path.cwd()
        config_path = search_dir / CONFIG_FILE_NAME
        data = _load_yaml_config(config_path)
        output_dir = Path(data.get("output_dir", DEFAULT_OUTPUT_DIR))
        author = str(data.get("author", "Your Name"))
        return cls(output_dir=output_dir, author=author)

    def to_dict(self) -> Dict[str, Any]:
        return {"output_dir": str(self.output_dir), "author": self.author}
