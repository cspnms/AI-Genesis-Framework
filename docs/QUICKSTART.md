# Quickstart

## Install

```bash
git clone https://example.com/ai-genesis-framework.git
cd ai-genesis-framework
python -m pip install -e .
```

## Basic Usage

List templates:

```bash
agf list-templates
```

Generate a Python CLI:

```bash
agf create my_cli "A simple tool that says hello" --template python_cli_basic
cd my_cli
python main.py --name AGF
```

Generate a Chrome extension:

```bash
agf create my_extension "Shows a banner on every page" --template chrome_extension_basic
```

Inspect a template:

```bash
agf show-template python_cli_basic
```

Create a new template skeleton:

```bash
agf new-template my_company_pattern
```

## Running Examples

The `examples/` directory contains rendered output for reference. Regenerate them
with the helper script:

```bash
bash scripts/bootstrap_example_projects.sh
```
