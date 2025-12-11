"""Command line interface for AI Genesis Framework."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import click

try:
    from rich.console import Console
    from rich.table import Table
except ImportError:  # pragma: no cover - fallback for minimal environments
    class _PlainTable:
        def __init__(self, title: str | None = None) -> None:
            self.title = title
            self.rows = []

        def add_column(self, *_: object, **__: object) -> None:
            return None

        def add_row(self, *args: str) -> None:
            self.rows.append(args)

        def __rich_console__(self, *_: object, **__: object):
            yield from []

    class _PlainConsole:
        def print(self, message: object = "", **_: object) -> None:
            if isinstance(message, _PlainTable):
                if message.title:
                    click.echo(message.title)
                for row in message.rows:
                    click.echo(" | ".join(row))
            else:
                click.echo(message)

        def rule(self, text: str) -> None:
            click.echo(f"--- {text} ---")

    Console = _PlainConsole  # type: ignore
    Table = _PlainTable  # type: ignore

from agf import __version__
from agf.config import AGFConfig
from agf.core.generator import GenerationError, ProjectGenerator
from agf.templates.registry import TemplateRegistry

console = Console()


@click.group()
@click.version_option(__version__, prog_name="AI Genesis Framework")
@click.pass_context
def cli(ctx: click.Context) -> None:
    ctx.ensure_object(dict)
    ctx.obj["config"] = AGFConfig.from_file()


def _render_template_table(registry: TemplateRegistry) -> None:
    table = Table(title="Available Templates")
    table.add_column("Name", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")
    table.add_column("Language", style="green")
    table.add_column("Type", style="magenta")
    for tpl in registry.all():
        table.add_row(tpl.name, tpl.description, tpl.language, tpl.type)
    console.print(table)


@cli.command("list-templates")
def list_templates() -> None:
    """List all available templates."""
    registry = TemplateRegistry()
    _render_template_table(registry)


@cli.command("show-template")
@click.argument("template_name")
def show_template(template_name: str) -> None:
    """Show template metadata and files."""
    registry = TemplateRegistry()
    try:
        template = registry.get(template_name)
    except KeyError as exc:
        raise click.ClickException(str(exc))

    console.rule(f"Template: {template.label}")
    console.print(f"[bold]Name:[/bold] {template.name}")
    console.print(f"[bold]Description:[/bold] {template.description}")
    console.print(f"[bold]Language:[/bold] {template.language}")
    console.print(f"[bold]Type:[/bold] {template.type}")
    console.print(f"[bold]Path:[/bold] {template.path}")
    console.print(f"[bold]Variables:[/bold] {', '.join(template.variables)}")

    console.print("\n[bold]Files:[/bold]")
    for path in template.iter_files():
        console.print(f"- {path.relative_to(template.path)}")


@cli.command("create")
@click.argument("project_slug")
@click.argument("description")
@click.option("--template", "template_name", required=True, help="Template name to use")
@click.option("--output-dir", type=click.Path(file_okay=False, dir_okay=True, path_type=Path))
@click.option("--var", "extra_vars", multiple=True, help="Extra variables as key=value")
@click.pass_context
def create_project(
    ctx: click.Context,
    project_slug: str,
    description: str,
    template_name: str,
    output_dir: Optional[Path],
    extra_vars: tuple[str, ...],
) -> None:
    """Create a new project from a template."""
    config: AGFConfig = ctx.obj["config"]
    generator = ProjectGenerator(config=config)

    extra_context = {}
    for item in extra_vars:
        if "=" not in item:
            raise click.ClickException("Extra variables must be in key=value format")
        key, value = item.split("=", 1)
        extra_context[key] = value

    try:
        project_path = generator.generate(
            template_name=template_name,
            project_slug=project_slug,
            description=description,
            output_dir=output_dir,
            extra_vars=extra_context,
        )
    except (GenerationError, KeyError) as exc:
        raise click.ClickException(str(exc))

    console.print(f"\n[bold green]Project created at[/bold green] {project_path}")


@cli.command("new-template")
@click.argument("template_name")
def new_template(template_name: str) -> None:
    """Scaffold a new template directory."""
    target_dir = Path(__file__).resolve().parent / "templates" / template_name
    if target_dir.exists():
        raise click.ClickException(f"Template already exists at {target_dir}")

    files_dir = target_dir / "files"
    files_dir.mkdir(parents=True, exist_ok=True)

    meta = {
        "name": template_name,
        "label": template_name.replace("_", " ").title(),
        "description": "Describe your template here.",
        "language": "python",
        "type": "custom",
        "variables": ["project_name", "project_slug", "description", "author", "year", "template_name"],
    }
    (target_dir / "template_meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

    sample_file = files_dir / "README.md.j2"
    sample_file.write_text(
        "# {{ project_name }}\n\nGenerated with custom template '{{ template_name }}'.\n",
        encoding="utf-8",
    )

    console.print(f"[green]New template scaffolded at[/green] {target_dir}")


def main() -> None:
    cli()


if __name__ == "__main__":
    main()
