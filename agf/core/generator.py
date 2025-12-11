"""Project generation logic for AGF."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Dict

from agf.config import AGFConfig
from agf.core.filesystem import resolve_output_path, write_file
from agf.core.templates import render_templates, resolve_template


class GenerationError(Exception):
    """Raised when project generation fails."""


class ProjectGenerator:
    def __init__(self, config: AGFConfig | None = None) -> None:
        self.config = config or AGFConfig.from_file()

    def build_context(
        self,
        template_name: str,
        project_slug: str,
        description: str,
        extra_vars: Dict[str, str] | None = None,
    ) -> Dict[str, str]:
        now = datetime.utcnow()
        template = resolve_template(template_name)
        context = {
            "project_name": project_slug.replace("-", " ").title(),
            "project_slug": project_slug,
            "description": description,
            "author": self.config.author,
            "year": str(now.year),
            "template_name": template.name,
        }
        if extra_vars:
            context.update(extra_vars)
        return context

    def generate(
        self,
        template_name: str,
        project_slug: str,
        description: str,
        output_dir: Path | None = None,
        extra_vars: Dict[str, str] | None = None,
    ) -> Path:
        template = resolve_template(template_name)
        context = self.build_context(template_name, project_slug, description, extra_vars)
        base_dir = output_dir or self.config.output_dir
        project_path = resolve_output_path(base_dir, project_slug)
        if project_path.exists():
            raise GenerationError(f"Target directory already exists: {project_path}")

        for relative_path, rendered in render_templates(template, context):
            write_file(project_path / relative_path, rendered)
        return project_path
