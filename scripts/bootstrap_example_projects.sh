#!/usr/bin/env bash
set -euo pipefail

# This helper demonstrates how to regenerate the example projects using AGF.
# Run from repository root.

# Example: regenerate Python CLI sample
# agf create python_cli_hello "Example generated CLI that greets users." --template python_cli_basic --output-dir examples

# Example: regenerate Chrome extension sample
# agf create chrome_extension_hello "Example extension that shows a banner." --template chrome_extension_basic --output-dir examples

# Feel free to adjust descriptions or inject extra variables:
# agf create custom "My custom app" --template python_cli_basic --var author="ACME" --var year="2024"

# No automatic commands are executed to keep this script safe by default.
