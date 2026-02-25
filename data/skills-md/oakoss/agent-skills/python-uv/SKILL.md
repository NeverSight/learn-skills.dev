---
name: python-uv
description: |
  Modern Python development with uv, the fast Python package and project manager. Covers project management (uv init, uv add, uv sync, uv lock), virtual environments, Python version management (uv python install/pin), script runners (uv run), tool management (uvx), workspace support for monorepos, and publishing to PyPI. Includes Python patterns for FastAPI, Pydantic, async/await, type checking, pytest, structlog, and CLI tools.

  Use when initializing Python projects, managing dependencies with uv, configuring pyproject.toml, setting up virtual environments, running scripts, managing Python versions, building monorepos with workspaces, containerizing Python apps, or writing modern Python with type hints.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://docs.astral.sh/uv/'
user-invocable: false
---

# Python uv

## Overview

uv is an extremely fast Python package and project manager written in Rust, designed to replace pip, pip-tools, pipx, poetry, pyenv, and virtualenv. It provides unified project management, dependency resolution, Python version management, and tool execution with 10-100x speed improvements over traditional tools.

**Key capabilities:** Project initialization, dependency locking and syncing, Python version management, PEP 723 inline script dependencies, ephemeral tool execution via `uvx`, monorepo workspaces with shared lockfiles, and package building/publishing.

**When to use:** Python project initialization, dependency management, virtual environments, Python version pinning, running scripts with inline dependencies, monorepo workspaces, tool execution, publishing packages.

**When NOT to use:** Non-Python projects, conda-managed scientific computing environments with system-level binary dependencies, projects locked to legacy `setup.py`-only workflows.

## Quick Reference

| Pattern              | Command / API                         | Key Points                                     |
| -------------------- | ------------------------------------- | ---------------------------------------------- |
| Init project         | `uv init`                             | Creates `pyproject.toml` and `.python-version` |
| Init library         | `uv init --lib`                       | Creates `src/` layout with `py.typed`          |
| Init script          | `uv init --script example.py`         | PEP 723 inline metadata script                 |
| Add dependency       | `uv add requests`                     | Adds to `pyproject.toml`, updates lockfile     |
| Add dev dependency   | `uv add --dev pytest`                 | Adds to `[dependency-groups]` dev group        |
| Add group dependency | `uv add --group docs mkdocs`          | Custom dependency groups                       |
| Add optional         | `uv add --optional postgres psycopg`  | Optional extras for libraries                  |
| Remove dependency    | `uv remove requests`                  | Removes from `pyproject.toml` and lockfile     |
| Lock dependencies    | `uv lock`                             | Creates/updates `uv.lock`                      |
| Upgrade in lockfile  | `uv lock --upgrade-package requests`  | Targeted dependency upgrade                    |
| Sync environment     | `uv sync`                             | Installs locked dependencies into `.venv`      |
| Sync for CI          | `uv sync --locked`                    | Fails if lockfile is stale                     |
| Sync frozen          | `uv sync --frozen`                    | Skips lockfile verification                    |
| Run command          | `uv run python app.py`                | Runs in project virtual environment            |
| Run script           | `uv run script.py`                    | Supports PEP 723 inline dependencies           |
| Run in package       | `uv run --package api pytest`         | Workspace-specific execution                   |
| Install Python       | `uv python install 3.13`              | Downloads and manages Python versions          |
| Pin Python           | `uv python pin 3.12`                  | Writes `.python-version` file                  |
| List Pythons         | `uv python list`                      | Shows available and installed versions         |
| Run tool             | `uvx ruff check .`                    | Ephemeral tool execution                       |
| Tool with plugins    | `uvx --with mkdocs-material mkdocs`   | Ephemeral tool with extra packages             |
| Install tool         | `uv tool install ruff`                | Persistent global tool install                 |
| Workspace            | `[tool.uv.workspace]`                 | Monorepo multi-package support                 |
| Build package        | `uv build`                            | Creates sdist and wheel in `dist/`             |
| Publish              | `uv publish`                          | Uploads to PyPI with trusted publishing        |
| Export deps          | `uv export --format requirements-txt` | Generate requirements.txt from lockfile        |

## Common Mistakes

| Mistake                                     | Correct Pattern                                                          |
| ------------------------------------------- | ------------------------------------------------------------------------ |
| Using `pip install` inside uv project       | `uv add` to manage via `pyproject.toml`                                  |
| Activating venv manually before `uv run`    | `uv run` handles venv activation automatically                           |
| Committing `.venv/` to version control      | Add `.venv/` to `.gitignore`, commit `uv.lock`                           |
| Not committing `uv.lock`                    | Always commit `uv.lock` for reproducible builds                          |
| Using `uv sync` without `--locked` in CI    | `uv sync --locked` ensures lockfile matches `pyproject.toml`             |
| Running `uv lock --upgrade` routinely       | Only upgrade intentionally, use `--upgrade-package` for targeted updates |
| Mixing `pip` and `uv` dependency management | Choose one tool for the project consistently                             |
| Using `uv pip install` for project deps     | Use `uv add`/`uv sync` for managed projects                              |
| Forgetting `--frozen` for Docker builds     | `uv sync --frozen` skips lockfile verification for faster builds         |
| Creating venv manually in uv project        | `uv sync` creates and manages `.venv` automatically                      |
| Using `setup.py` for new projects           | Use `pyproject.toml` with a modern build backend                         |
| Not using `py.typed` in libraries           | `uv init --lib` includes it, required for typed packages                 |

## Delegation

- **Project scaffolding**: Use `Explore` agent
- **Dependency audit**: Use `Task` agent
- **Code review**: Delegate to `code-reviewer` agent

> If the `docker` skill is available, delegate containerization patterns to it.
> If the `github-actions` skill is available, delegate CI/CD pipeline configuration to it.
> If the `api-testing` skill is available, delegate API testing patterns to it.
> If the `sentry-setup-logging` skill is available, delegate error monitoring setup to it.
> If the `pino-logging` skill is available, delegate Node.js logging patterns to it (Python equivalent covered here with structlog).

## References

- [Project management and pyproject.toml configuration](references/project-management.md)
- [Dependency management, lockfiles, and groups](references/dependency-management.md)
- [Python version management and virtual environments](references/python-environments.md)
- [Scripts, inline dependencies, and tool management](references/scripts-and-tools.md)
- [Workspace support for monorepos](references/workspaces.md)
- [FastAPI web framework patterns](references/fastapi-patterns.md)
- [Pydantic validation and data modeling](references/pydantic-validation.md)
- [Async patterns with asyncio](references/async-patterns.md)
- [Type checking with mypy and pyright](references/type-checking.md)
- [Testing with pytest](references/testing-patterns.md)
- [Logging with structlog](references/structlog-logging.md)
- [CLI applications with typer](references/cli-applications.md)
- [Docker integration and publishing](references/docker-and-publishing.md)
