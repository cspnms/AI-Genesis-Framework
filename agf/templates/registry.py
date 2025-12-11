"""Template discovery and metadata management."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List

from agf.core.filesystem import iter_template_files

TEMPLATES_DIR = Path(__file__).resolve().parent


@dataclass
class TemplateDefinition:
    name: str
    label: str
    description: str
    language: str
    type: str
    path: Path
    variables: List[str]

    @property
    def meta_path(self) -> Path:
        return self.path / "template_meta.json"

    @property
    def files_path(self) -> Path:
        return self.path / "files"

    def iter_files(self) -> Iterable[Path]:
        return iter_template_files(self.files_path)


class TemplateRegistry:
    def __init__(self, templates_dir: Path = TEMPLATES_DIR) -> None:
        self.templates_dir = templates_dir
        self._templates: Dict[str, TemplateDefinition] = {}
        self.refresh()

    def refresh(self) -> None:
        self._templates = {}
        for meta_file in self.templates_dir.glob("*/template_meta.json"):
            with meta_file.open("r", encoding="utf-8") as handle:
                meta = json.load(handle)
            name = meta.get("name")
            if not name:
                continue
            self._templates[name] = TemplateDefinition(
                name=name,
                label=meta.get("label", name),
                description=meta.get("description", ""),
                language=meta.get("language", "unknown"),
                type=meta.get("type", "general"),
                path=meta_file.parent,
                variables=meta.get("variables", []),
            )

    def all(self) -> List[TemplateDefinition]:
        return sorted(self._templates.values(), key=lambda t: t.name)

    def get(self, name: str) -> TemplateDefinition:
        if name not in self._templates:
            raise KeyError(f"Template not found: {name}")
        return self._templates[name]

    def describe(self, name: str) -> Dict[str, str]:
        tpl = self.get(name)
        return {
            "name": tpl.name,
            "label": tpl.label,
            "description": tpl.description,
            "language": tpl.language,
            "type": tpl.type,
            "path": str(tpl.path),
            "variables": ", ".join(tpl.variables),
        }
