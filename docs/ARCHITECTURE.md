# Architecture

AGF is a lightweight Python package composed of clear layers: configuration,
template registry, rendering pipeline, and CLI orchestration. The codebase is
meant to be readable and extendable, leaving space for future plugins.

## Layout

```
ai-genesis-framework/
├── agf/
│   ├── cli.py           # CLI commands
│   ├── config.py        # Simple config loader
│   ├── core/            # Generation utilities
│   │   ├── generator.py # Renders templates into projects
│   │   ├── templates.py # Jinja environment helpers
│   │   ├── filesystem.py# FS helpers
│   │   └── prompts.py   # AI/LLM hooks (stub)
│   └── templates/       # Built-in templates and registry
├── docs/                # Documentation set
├── examples/            # Generated sample outputs
└── scripts/             # Helper scripts
```

## Flow: CLI to Generated Project

```
[user] --click--> cli.py --loads--> config.py
                       |            |
                       |            +--> AGFConfig (from .agf.yaml if present)
                       |
                       +--> registry.TemplateRegistry
                       +--> core.generator.ProjectGenerator
                                 |
                                 +--> core.templates.render_templates (Jinja2)
                                 +--> core.filesystem.write_file
                                 +--> outputs project directory
```

## Template System
- Templates live under `agf/templates/<template_name>/`.
- Each template has `template_meta.json` describing language, type, and variables.
- The `files/` directory contains Jinja2 files (`*.j2`).
- `TemplateRegistry` discovers templates automatically.
- `ProjectGenerator` builds a rendering context and writes rendered files.

## Extensibility Hooks
- `core/prompts.py` outlines how AI prompt builders could provide richer
  scaffolds.
- `cli.py` exposes `new-template` for custom patterns and leaves room for
  plugins to register new commands.

## Error Handling
- Generator raises `GenerationError` for collisions (existing output paths) so
  users do not accidentally overwrite work.
