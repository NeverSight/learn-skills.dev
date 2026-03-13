---
name: python-dev
description: Opinionated Python development setup with uv + ty + ruff + pytest + just. Use when creating new Python projects, setting up pyproject.toml, configuring linting, type checking, testing, or build tooling. Triggers on "python project", "uv init", "pyproject.toml", "ruff config", "ty check", "pytest setup", "justfile", "python linting", "python formatting", "type checking python".
metadata:
  version: "0.1.1"
---

# Python Development Setup

Opinionated, production-ready Python development stack. No choices to make - just use this.

## When to Use

- Starting a new Python project
- Modernizing an existing project (migrating from pip/poetry/mypy/black/flake8)
- Setting up linting, formatting, type checking, or testing
- Creating a Justfile for project commands
- Configuring pyproject.toml as the single source of truth

## The Stack

| Tool | Role | Replaces |
|------|------|----------|
| [uv](https://docs.astral.sh/uv/) 0.10+ | Package manager, Python versions, runner | pip, poetry, pyenv, virtualenv |
| [ty](https://github.com/astral-sh/ty) | Type checker (Astral, Rust) | mypy, pyright |
| [ruff](https://docs.astral.sh/ruff/) | Linter + formatter | flake8, black, isort, pyupgrade |
| [pytest](https://docs.pytest.org/) | Testing | unittest |
| [just](https://just.systems/) | Command runner | make |

## Quick Start: New Project

```bash
# 1. Create project with src layout
uv init --package my-project
cd my-project

# 2. Pin Python version
uv python pin 3.13

# 3. Add dev dependencies
uv add --dev ruff ty pytest pytest-asyncio pre-commit

# 4. Create Justfile (see template below)
# 5. Configure pyproject.toml (see template below)
# 6. Run checks
just check
```

## pyproject.toml Template

This is the single config file. Copy this and adjust `[project]` fields.

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "Project description"
readme = "README.md"
requires-python = ">=3.13"
license = {text = "MIT"}
dependencies = []

[project.scripts]
my-project = "my_project:main"

[dependency-groups]
dev = [
    "ruff>=0.7.0",
    "ty>=0.0.1a32",
    "pytest>=8.0.0",
    "pytest-asyncio>=1.0.0",
    "pre-commit>=3.0.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/my_project"]

# =============================================================================
# RUFF - Loose, helpful rules only
# =============================================================================
[tool.ruff]
target-version = "py313"
line-length = 100

[tool.ruff.lint]
select = [
    "E",   # pycodestyle errors - syntax issues
    "F",   # pyflakes - undefined vars, unused imports
    "I",   # isort - import sorting
    "UP",  # pyupgrade - modern Python syntax
]
ignore = [
    "E501",   # line too long - formatter handles it
    "E741",   # ambiguous variable name - sometimes makes sense
    "UP007",  # X | Y unions - Optional[X] is more readable
]
exclude = [".git", ".venv", "__pycache__", "build", "dist"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
line-ending = "lf"

# =============================================================================
# TY - Type Checker
# =============================================================================
[tool.ty.environment]
python-version = "3.13"

[tool.ty.src]
include = ["src"]

# =============================================================================
# PYTEST
# =============================================================================
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
asyncio_mode = "auto"
addopts = [
    "--strict-markers",
    "--strict-config",
    "-ra",
]
```

## Justfile Template

```just
# Check types and lint
check:
    uv run ty check
    uv run ruff check --fix && uv run ruff format

# Run tests
test *ARGS:
    uv run pytest {{ARGS}}

# Run tests with coverage
test-cov:
    uv run pytest --cov=src --cov-report=term-missing

# Auto-fix and format
fix:
    uv run ruff check --fix
    uv run ruff format

# Install/sync all dependencies
install:
    uv sync --all-groups

# Update all dependencies
update:
    uv lock --upgrade
    uv sync --all-groups

# Clean build artifacts
clean:
    rm -rf dist/ build/ .pytest_cache/ .ruff_cache/ htmlcov/
    find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
```

## Pre-commit Config

Create `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: check-added-large-files
        args: ['--maxkb=1000']
        exclude: ^uv\.lock$
      - id: detect-private-key
      - id: check-merge-conflict
      - id: check-yaml
      - id: check-toml
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: mixed-line-ending
        args: ['--fix=lf']

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.4
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

exclude: |
  (?x)^(
    \.venv/.*|
    \.git/.*|
    __pycache__/.*|
    build/.*|
    dist/.*|
    uv\.lock
  )$
```

Then run: `uv run pre-commit install`

## Project Structure

Always use src layout:

```
my-project/
  src/
    my_project/
      __init__.py
      cli.py
      models.py
  tests/
    conftest.py
    test_models.py
  pyproject.toml
  Justfile
  uv.lock
  .python-version
  .pre-commit-config.yaml
  .gitignore
```

## Daily Workflow

```bash
just check          # Type check + lint + format
just test           # Run tests
just test -x        # Stop on first failure
just fix            # Auto-fix lint issues
uv add httpx        # Add a dependency
uv add --dev hypothesis  # Add dev dependency
uv run python -m my_project  # Run the project
```

## Existing Project Migration

```bash
# 1. Install uv if not present
brew install uv

# 2. Convert requirements.txt to pyproject.toml deps
uv add -r requirements.txt

# 3. Replace mypy with ty
uv remove --dev mypy
uv add --dev ty

# 4. Replace black/flake8/isort with ruff
uv remove --dev black flake8 isort
uv add --dev ruff

# 5. Apply pyproject.toml config sections from template above
# 6. Create Justfile from template above
# 7. Run: just check
```

## Reference Docs

Detailed guides for each tool in `references/`:
- **uv-reference.md** - Project init, dependencies, lock/sync, Python versions, build/publish
- **ty-reference.md** - Configuration, rules, CLI flags, known limitations
- **ruff-reference.md** - Rule sets, formatter options, per-file ignores, CI integration
- **pytest-reference.md** - Plugins, fixtures, async testing, conftest patterns
- **justfile-reference.md** - Syntax, variables, parameters, shebang recipes, settings

## Resources

- [uv docs](https://docs.astral.sh/uv/) | [uv GitHub](https://github.com/astral-sh/uv)
- [ty GitHub](https://github.com/astral-sh/ty)
- [ruff docs](https://docs.astral.sh/ruff/) | [ruff GitHub](https://github.com/astral-sh/ruff)
- [pytest docs](https://docs.pytest.org/en/stable/)
- [just manual](https://just.systems/man/en/)
