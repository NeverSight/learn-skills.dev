---
name: python-conventions
description: >-
  Python tooling conventions. Use when working on .py files, pyproject.toml,
  or Python projects. Enforce uv for package management, ty for type checking.
  NOT for JavaScript/TypeScript projects or shell scripts.
user-invocable: false
disable-model-invocation: false
license: MIT
metadata:
  author: wyattowalsh
  version: "1.0.0"
---

# Python Conventions

Apply these conventions when working on Python files or projects.

## Dispatch

| $ARGUMENTS | Action |
|------------|--------|
| Active (auto-invoked when working on Python files) | Apply all conventions below |
| Empty | Display convention summary |
| `check` | Verify tooling compliance only |

## References

| File | Purpose |
|------|---------|
| `references/exceptions.md` | When to break conventions (legacy, corporate) |

## Tooling

- **Package manager**: `uv` for all Python operations (`uv run python ...` instead of `python`, `uv add` instead of `pip install`)
- **Project config**: `pyproject.toml` with `uv add <pkg>` (never `uv pip install` or `pip install`)
- **Type checking**: `ty` (not mypy)
- **Linting**: `ruff check` and `ruff format`
- **Testing**: `uv run pytest`
- **Task running**: `uv run <command>` for all script execution

### Virtual Environments

- Let `uv` manage virtual environments automatically
- Never manually create or activate `.venv` directories
- Use `uv run` to execute within the project environment

## Preferred Libraries

When applicable, prefer these libraries over alternatives:

| Purpose | Library | Instead of |
|---------|---------|------------|
| Logging | `loguru` | `logging` |
| Retries | `tenacity` | manual retry loops |
| Progress bars | `tqdm` | print statements |
| Web APIs | `fastapi` | flask |
| CLI tools | `typer` | argparse, click |
| DB migrations | `alembic` | manual SQL |
| DB ORM | `sqlmodel` | sqlalchemy raw |
| UI/demos | `gradio` | streamlit |
| Numerics | `numpy` | manual math |
| MCP servers | `fastmcp` | raw MCP protocol |

## Project Structure

- Use `pyproject.toml` for all project metadata and dependencies
- Place source code in a package directory matching the project name
- Use `uv` workspace members for monorepo sub-packages
- Run `ruff check` and `ruff format` before committing

## Critical Rules

1. Always use `uv` for package management -- never `pip install` or `pip`
2. Use `uv add` to add dependencies -- never `uv pip install`
3. Use `ty` for type checking -- never `mypy`
4. Run `uv run pytest` before committing any Python changes
5. Run `uv run ruff check` to lint before committing
6. Check `references/exceptions.md` before breaking any convention
7. Prefer libraries from the preferred table over their alternatives

**Canonical terms** (use these exactly):
- `uv` -- the required package manager and task runner
- `ty` -- the required type checker (not mypy)
- `ruff` -- the required linter and formatter
- `pyproject.toml` -- the single source of project configuration
- `uv run` -- prefix for all Python command execution
