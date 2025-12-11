# AI Genesis Framework (AGF)

AI Genesis Framework is a self-expanding, self-documenting project generator that
helps developers translate natural language descriptions into complete, runnable
project skeletons. AGF ships with modular templates, a friendly CLI, and a clear
roadmap for deeper AI/LLM integrations while remaining fully usable offline.

## Features
- 🚀 Scaffold projects from natural language descriptions using built-in templates.
- 📚 Self-documenting structure with architecture notes, quickstarts, and examples.
- 🧩 Extensible template system ready for community-driven growth.
- 🔌 Future-proof hooks for AI-assisted generation without requiring connectivity today.

## Installation

Clone the repository and install in editable mode:

```bash
git clone https://example.com/ai-genesis-framework.git
cd ai-genesis-framework
python -m pip install -e .
```

## Quick Usage

```bash
agf list-templates
agf create my_cli "A simple tool that says hello" --template python_cli_basic
cd my_cli
python main.py --name AGF
```

More guides and architectural notes live in the [docs/](docs) directory.

## License

MIT License © 2024 AI Genesis contributors.
