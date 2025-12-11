"""Template loading and rendering utilities."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable

try:  # Optional import for environments without dependencies installed
    from jinja2 import Environment, FileSystemLoader, select_autoescape
except ImportError as exc:  # pragma: no cover - runtime guard
    Environment = FileSystemLoader = select_autoescape = None  # type: ignore
    _JINJA_IMPORT_ERROR = exc
else:
    _JINJA_IMPORT_ERROR = None

from agf.templates.registry import TemplateRegistry, TemplateDefinition


@dataclass
class RenderContext:
    template: TemplateDefinition
    variables: Dict[str, str]


def build_environment(template_path: Path) -> "Environment":
    if _JINJA_IMPORT_ERROR is not None:
        raise RuntimeError(
            "Jinja2 is required to render templates. Install dependencies via pip."
        ) from _JINJA_IMPORT_ERROR
    loader = FileSystemLoader(str(template_path))
    return Environment(loader=loader, autoescape=select_autoescape())


def render_templates(template: TemplateDefinition, context: Dict[str, str]) -> Iterable[tuple[Path, str]]:
    env = build_environment(template.files_path)
    for template_file in template.iter_files():
        relative = template_file.relative_to(template.files_path)
        target_path = Path(relative.with_suffix(""))
        tpl = env.get_template(str(relative))
        yield target_path, tpl.render(**context)


def resolve_template(name: str) -> TemplateDefinition:
    registry = TemplateRegistry()
    return registry.get(name)
