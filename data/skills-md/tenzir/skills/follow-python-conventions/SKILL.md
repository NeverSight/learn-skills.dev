---
name: follow-python-conventions
description: >-
  Tenzir Python coding standards and tooling workflow. Use when editing Python
  code, running `uv`, `ruff`, `mypy`, or `pytest`, working with
  `pyproject.toml` or `uv.lock`, or setting up a Tenzir Python project. Also
  use when the user asks how to structure a new Tenzir Python project, set up
  linting, or asks about Python best practices in the Tenzir context.
---

# Follow Python Conventions

Apply the standard Tenzir Python toolchain and coding conventions.

## Required Tools

All Tenzir Python projects use:

- `uv` for dependency management and virtual environments
- `ruff` for linting and formatting
- `mypy` for static type checking
- `pytest` for testing

## Default Libraries

Prefer these libraries unless the repository already establishes a different
stack:

- `pydantic` for models and validation
- `FastAPI` for REST APIs
- `Click` for CLIs

## Quality Gates

Run this sequence before committing or releasing:

```sh
uv run ruff check \
  && uv run ruff format --check \
  && uv run mypy \
  && uv run pytest \
  && uv build
```

## Conventions

- Target Python 3.12 or later.
- Fully type all public surfaces.
- Avoid `Any` unless there is a concrete reason it cannot be removed.
- Keep `__init__.py` files empty.
- Use absolute imports from the package root.
- Use `snake_case` for modules, functions, and variables; `PascalCase` for
  classes; `CONSTANT_CASE` for constants.
- Use kebab-case for CLI flags.

## Reference Files

Load only the configuration reference you need:

- [project structure](references/project-structure.md)
- [pyproject](references/pyproject.md)
- [ruff](references/ruff.md)
- [mypy](references/mypy.md)
- [pytest](references/pytest.md)
- [coverage](references/coverage.md)
- [dev dependencies](references/dev-dependencies.md)
- [upgrading dependencies](references/upgrading-dependencies.md)
