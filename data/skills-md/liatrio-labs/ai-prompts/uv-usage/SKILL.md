---
name: uv-usage
description: Provides concise guidance for using uv (Python package manager), including project workflows, pip-compatible commands, Python version management, and PEP 723 inline script dependencies. Use when users mention uv, uv run, inline dependencies, PEP 723, or Python dependency/project management.
---

# uv Usage

## Quick start

Use uv as a fast, unified tool for Python projects:

1. Initialize a project: `uv init`
2. Add deps: `uv add <package>`
3. Sync env: `uv sync`
4. Run commands: `uv run <cmd>`

`uv add` updates `uv.lock` automatically; use `uv lock` when you need to re-lock after manual `pyproject.toml` edits.

## Inline dependencies (PEP 723 scripts)

Use inline metadata so a script runs standalone with `uv run <script-file>`.

### Steps

1. Add a `# /// script` block at the top of the file.
2. Set `requires-python` and `dependencies`.
3. Run the script with `uv run <script-file>`.
4. Add or remove inline deps with `uv add --script` and `uv remove --script`.

### Template

```python
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "requests>=2.31",
#   "rich>=13.0",
# ]
# ///

import requests
from rich import print

print(requests.get("https://api.github.com/repos/astral-sh/uv").status_code)
```

### Commands

```bash
uv run script.py
uv add --script script.py beautifulsoup4
uv remove --script script.py rich
```

## Pip-compatible commands

Use these for drop-in workflows or legacy projects:

```bash
uv pip install <package>
uv pip install -r requirements.txt
uv pip compile requirements.in -o requirements.txt
uv pip sync requirements.txt
```

## Python versions and environments

```bash
uv python install 3.12
uv python pin 3.12
uv venv --python 3.12
uv run --python 3.12 -- python -V
```

## Examples

### New project

```bash
uv init demo
cd demo
uv add ruff
uv run ruff check .
```

### Standalone script with inline deps

```bash
uv run script.py
```

## Notes

- uv offers pip-compatible commands, but behavior can differ in edge cases.
- Use `uvx <tool>` (alias for `uv tool run`) to run tools ephemerally without installing them globally.
- Prefer project workflow (`uv add`, `uv sync`) for new work, and run `uv lock` when re-locking after manual `pyproject.toml` changes.
