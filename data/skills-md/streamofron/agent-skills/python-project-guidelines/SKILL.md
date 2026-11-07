---
name: python-project-guidelines
description: Use when starting a new Python project, scaffolding a Python application, or setting up Python project structure with pyproject.toml
---

# Python Project Guidelines

## Overview

**Core principle:** Create Python projects with uv-managed environments, minimal dependencies, modern Python versions, and async-first architecture for web applications.

**Key distinction:** This skill applies to full Python projects with `pyproject.toml`. For standalone single-file scripts, use the `standalone-python-scripts` skill instead.

## When to Use

- Starting a new Python project with multiple modules
- Scaffolding a Python application or library
- Setting up project structure with `pyproject.toml`
- When the project requires multiple files, tests, or complex dependencies

**When NOT to use:**
- Single-file standalone scripts → use `standalone-python-scripts` skill
- Quick utility scripts → use `standalone-python-scripts` skill
- Existing projects without `pyproject.toml` that don't need restructuring

## Standalone Script Check

**Before proceeding:** If the project is a single-file tool or script (not a multi-module application), STOP and use the `standalone-python-scripts` skill instead.

**Decision rule:**
- Single `.py` file for standalone execution → `standalone-python-scripts`
- Multiple modules, tests, or complex structure → continue with this skill

## Environment Management with uv

Use `uv` for Python version management and virtual environment handling.

### Project Initialization

```bash
# Initialize new project
uv init myproject
cd myproject

# Specify Python version (see version policy below)
uv init myproject --python 3.12
```

### Adding Dependencies

```bash
# Add production dependencies
uv add click arrow sqlalchemy

# Add development dependencies
uv add --dev pytest ruff mypy

# Add with version constraints
uv add 'httpx>=0.24,<0.27'
```

### Running Commands

```bash
# Run Python scripts
uv run python myscript.py

# Run installed tools
uv run pytest
uv run ruff check .
```

## Python Version Policy

**Rule:** Never target Python versions that are end-of-life or have less than one year until end-of-life.

**Check current status:** https://devguide.python.org/versions/

**Current safe minimum (as of 2026-08-27):** Python 3.11
- 3.10: EOL 2026-10 (less than 1 year) → DO NOT TARGET
- 3.11: EOL 2027-10 (more than 1 year) → OK
- 3.12+: OK

**In pyproject.toml:**
```toml
[project]
requires-python = ">=3.11"
```

**Verification:** Before setting `requires-python`, check the devguide URL above. If a version's EOL is within 12 months of today, do not use it.

## Dependency Discipline

**Principle:** Take only the minimum necessary external requirements to efficiently accomplish the task.

**Decision process:**
1. Can stdlib handle this? → Use stdlib
2. Is there a well-established, maintained library? → Use it
3. Is the dependency adding significant value over stdlib? → Justify it

**Examples:**
- JSON parsing → stdlib `json` (no external dep needed)
- HTTP client → `httpx` or `requests` (stdlib `urllib` is cumbersome)
- Date/time → `arrow` (per preference table)
- CLI parsing → `click` (per preference table)

## Library Preferences

When external dependencies are needed, prefer these libraries:

| Need | Library | Notes |
|------|---------|-------|
| Argument parsing | **Click** | Decorator-based, clean API |
| Date/time handling | **Arrow** | Better than stdlib `datetime` |
| Database ORM | **SQLAlchemy** | Do not write raw SQL unless absolutely necessary |
| Database migrations | **Alembic** | Works with SQLAlchemy |
| Web (async) | **Quart**, **FastAPI**, or **AioHttp** | Choose based on project needs; prefer async frameworks |

**Web framework selection:**
- **FastAPI**: Best for APIs with automatic OpenAPI docs, type validation
- **Quart**: Async Flask alternative, good for traditional web apps
- **AioHttp**: Lower-level, good for high-performance services

**Database rule:** Use SQLAlchemy ORM. Write raw SQL only when:
- Complex queries that ORM cannot express efficiently
- Performance-critical paths where raw SQL is measurably faster
- Legacy database integration requiring specific SQL features

## Project Structure

```
myproject/
├── pyproject.toml
├── src/
│   └── myproject/
│       ├── __init__.py
│       ├── main.py
│       └── ...
├── tests/
│   └── ...
└── README.md
```

**Key conventions:**
- Use `src/` layout for packages
- Keep tests separate from source
- Use `pyproject.toml` for all project metadata (no `setup.py` or `setup.cfg`)

## Common Mistakes

| Mistake | Correct Pattern |
|---------|-----------------|
| Using `pip` instead of `uv` | Always use `uv` for environment management |
| Targeting Python 3.10 or older | Check devguide; use 3.11+ |
| Writing raw SQL queries | Use SQLAlchemy ORM |
| Using sync web frameworks (Flask, Django) | Use async frameworks (FastAPI, Quart, AioHttp) |
| Using `argparse` for CLI | Use Click |
| Using stdlib `datetime` extensively | Use Arrow |
| Bloated dependencies | Audit and remove unused packages |
| Using `setup.py` | Use `pyproject.toml` only |

## Red Flags - STOP and Check

- [ ] Using Python version with EOL < 1 year away
- [ ] Writing raw SQL instead of using SQLAlchemy
- [ ] Using sync web framework for new project
- [ ] Adding dependencies without justification
- [ ] Using `pip`/`venv` instead of `uv`
- [ ] Missing `requires-python` in `pyproject.toml`
- [ ] Using deprecated packaging tools (`setup.py`, `setup.cfg`)

## Verification

Before completing project setup:

1. **Check Python version:** `uv run python --version` → should be 3.11+
2. **Check dependencies:** `uv tree` → review for unnecessary packages
3. **Verify structure:** `ls src/` → should use src layout
4. **Test run:** `uv run python -m myproject` → should execute without errors

## References

- **Python versions:** https://devguide.python.org/versions/
- **Click:** https://click.palletsprojects.com/
- **Arrow:** https://arrow.readthedocs.io/
- **SQLAlchemy:** https://docs.sqlalchemy.org/
- **Alembic:** https://alembic.sqlalchemy.org/
- **Quart:** https://quart.palletsprojects.com/
- **FastAPI:** https://fastapi.tiangolo.com/
- **AioHttp:** https://docs.aiohttp.org/
- **uv docs:** https://docs.astral.sh/uv/
