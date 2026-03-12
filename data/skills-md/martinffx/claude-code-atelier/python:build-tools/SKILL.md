---
name: python:build-tools
description: Python project tooling with uv, mise, ruff, basedpyright, and pytest. Use when setting up pyproject.toml, running builds, typechecking, configuring tests, linting, formatting, or managing Python environments.
user-invocable: false
---

# Python Build Tools

Modern Python development tooling using uv, mise, ruff, basedpyright, and pytest.

## Quick Start

### Minimal pyproject.toml

```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["fastapi", "pydantic"]

[project.optional-dependencies]
dev = ["pytest>=8.0.0", "ruff>=0.8.0", "basedpyright>=1.0.0"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "UP", "RUF"]

[tool.basedpyright]
typeCheckingMode = "strict"

[tool.pytest.ini_options]
testpaths = ["tests"]
```

### Setup Project

```bash
uv init my-project && cd my-project
uv sync
uv add fastapi pydantic
uv add --dev pytest ruff basedpyright
```

## Tool Overview

| Tool | Purpose | Replaces |
|------|---------|----------|
| **uv** | Package management | pip, virtualenv |
| **mise** | Version & tasks | pyenv, asdf |
| **ruff** | Lint & format | black, isort, flake8 |
| **basedpyright** | Type checking | mypy |
| **pytest** | Testing | unittest |

## Common Commands

### Lint and Format

```bash
uv run ruff check --fix .
uv run ruff format .
```

### Type Check

```bash
uv run basedpyright
uv run basedpyright src/main.py
```

### Test

```bash
uv run pytest
uv run pytest --cov=src --cov-report=html
```

### Manage Dependencies

```bash
uv add fastapi
uv add --dev pytest
uv lock --upgrade
uv tree
```

## Mise Configuration

Create `.mise.toml` for consistent development:

```toml
[tools]
python = "3.12"

[tasks.lint]
run = "uv run ruff check --fix ."

[tasks.format]
run = "uv run ruff format ."

[tasks.typecheck]
run = "uv run basedpyright"

[tasks.test]
run = "uv run pytest"

[tasks.check]
depends = ["lint", "format", "typecheck", "test"]
```

Usage:

```bash
mise install
mise run check
```

## Type Hints Example

```python
from decimal import Decimal
from typing import Optional

def calculate_discount(
    total: Decimal,
    rate: Optional[Decimal] = None
) -> Decimal:
    if rate is None:
        rate = Decimal("0.1")
    return total * rate
```

## Best Practices

1. Use uv for all package management (faster, reliable)
2. Pin Python version with mise
3. Configure tools in pyproject.toml
4. Enable strict type checking
5. Run checks before commit

## References

For detailed configuration and advanced patterns:

- **[references/uv.md](references/uv.md)** - Workspaces, scripts, dependency management
- **[references/ruff.md](references/ruff.md)** - Rules, per-file ignores, pre-commit integration
- **[references/basedpyright.md](references/basedpyright.md)** - Type patterns, generics, protocols
