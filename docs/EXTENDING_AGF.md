# Extending AGF

AGF is built to grow. Follow this guide to create and share new templates.

## Create a Template with the CLI

```bash
agf new-template my_template
```

This creates:
- `agf/templates/my_template/template_meta.json`
- `agf/templates/my_template/files/README.md.j2`

## Editing template_meta.json

```json
{
  "name": "my_template",
  "label": "My Template",
  "description": "What this template builds",
  "language": "python",
  "type": "service",
  "variables": ["project_name", "project_slug", "description", "author", "year", "template_name"]
}
```

- **name**: unique identifier used by the CLI.
- **label**: human-friendly display name.
- **description**: short summary shown in `list-templates`.
- **language**/**type**: categorization for filtering.
- **variables**: context keys available inside Jinja2 templates.

## Adding Files

Place Jinja2 templates under `files/`. File names end with `.j2` and render to
files without the extension. Example:

```
files/
├── main.py.j2
└── README.md.j2
```

Inside templates, use placeholders such as `{{ project_name }}` or
`{{ description }}`.

## Test Your Template

```bash
agf create demo "Quick demo" --template my_template --output-dir /tmp
```

Inspect the generated folder and iterate on your templates.

## Share and Version

- Commit the new template directory to version control.
- Document usage in `docs/` or `README.md`.
- Propose additions to the official registry via pull requests.
