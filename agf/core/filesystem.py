"""Filesystem utilities for AGF."""
from __future__ import annotations

from pathlib import Path
from typing import Iterable


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_file(path: Path, content: str) -> None:
    ensure_dir(path.parent)
    path.write_text(content, encoding="utf-8")


def copy_template_path(src: Path, dst: Path) -> None:
    ensure_dir(dst)
    for item in src.iterdir():
        target = dst / item.name
        if item.is_dir():
            copy_template_path(item, target)
        else:
            target.write_bytes(item.read_bytes())


def resolve_output_path(base_dir: Path, project_slug: str) -> Path:
    return base_dir / project_slug


def iter_template_files(files_dir: Path) -> Iterable[Path]:
    for path in files_dir.rglob("*"):
        if path.is_file():
            yield path
