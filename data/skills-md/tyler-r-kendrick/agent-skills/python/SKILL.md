---
name: python
description: |
  Guidance for Python software development across the ecosystem. Covers project configuration, package management, CLI development, and popular libraries.
  USE FOR: Python project setup, choosing Python tools, understanding Python language features, virtual environments, type hints, async programming, packaging strategy
  DO NOT USE FOR: specific tool deep-dives (use the sub-skills: project-system, package-management, cli, packages)
license: MIT
metadata:
  displayName: "Python"
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
  tags:
    - python
    - pip
    - uv
    - poetry
    - pyproject
    - cli
compatibility: claude, copilot, cursor
references:
  - title: "Python Official Documentation"
    url: "https://docs.python.org/3/"
  - title: "CPython GitHub Repository"
    url: "https://github.com/python/cpython"
  - title: "Python Packaging User Guide"
    url: "https://packaging.python.org/en/latest/"
---

# Python Skills

A comprehensive collection of guidance for Python software development, covering project configuration, dependency management, CLI tooling, and best practices across the modern Python ecosystem.

## Overview

Python is one of the most widely-used programming languages, powering web backends, data science, machine learning, DevOps automation, CLI tools, and scripting. The Python ecosystem has undergone significant modernization in recent years with `pyproject.toml` replacing `setup.py`, type hints becoming standard, and new high-performance tooling like `uv` transforming the developer experience.

This skill tree provides structured guidance for navigating the Python ecosystem effectively.

## Knowledge Map

```
python/
  project-system/       pyproject.toml, build backends, setuptools, hatch, flit, maturin
  package-management/   pip, uv, poetry, pdm, conda, pipx, virtual environments
  cli/                  argparse, click, typer, rich, textual
  packages/             Popular libraries and frameworks (Flask, FastAPI, Django, pytest, etc.)
```

## Sub-Skill Categories

| Category | Sub-Skill | What It Covers |
|----------|-----------|----------------|
| **Project System** | `project-system` | `pyproject.toml` anatomy, build backends (setuptools, hatchling, flit-core, maturin), PEP 517/518/621/660, entry points, versioning, publishing |
| **Package Management** | `package-management` | pip, uv, poetry, pdm, conda, pipx, virtual environments, lockfiles, private indexes |
| **CLI Development** | `cli` | argparse, click, typer, rich, textual, output formatting, testing CLI apps |
| **Packages** | `packages` | Popular Python libraries and frameworks for web, data, testing, and more |

## Choosing Guide

| I need to... | Use this sub-skill |
|---|---|
| Set up a new Python project with `pyproject.toml` | `project-system` |
| Choose between setuptools, hatch, flit, or poetry for building | `project-system` |
| Configure entry points or console scripts | `project-system` |
| Publish a package to PyPI | `project-system` |
| Install dependencies or manage a lockfile | `package-management` |
| Choose between pip, uv, poetry, pdm, or conda | `package-management` |
| Set up virtual environments | `package-management` |
| Configure private package indexes | `package-management` |
| Build a command-line application | `cli` |
| Add rich terminal output (colors, tables, progress bars) | `cli` |
| Build a terminal UI (TUI) | `cli` |
| Choose between argparse, click, and typer | `cli` |

## Python Version Landscape

| Version | Status | Key Features |
|---------|--------|--------------|
| **3.9** | Security fixes | Dict union operators (`\|`, `\|=`), `str.removeprefix()`/`removesuffix()`, type hinting generics in standard collections |
| **3.10** | Security fixes | Structural pattern matching (`match`/`case`), parenthesized context managers, `TypeAlias`, better error messages |
| **3.11** | Maintained | Exception groups and `except*`, `tomllib` in stdlib, significant performance improvements (10-60% faster), `TaskGroup` for asyncio |
| **3.12** | Maintained | Type parameter syntax (`type X = ...`), f-string improvements, per-interpreter GIL (subinterpreters), `pathlib` improvements |
| **3.13** | Latest stable | Free-threaded mode (experimental, no GIL), JIT compiler (experimental), improved `typing` module, better REPL |
| **3.14+** | In development | Deferred evaluation of annotations (PEP 649), further JIT/free-threading improvements |

**Recommendation**: Target Python 3.11+ for new projects. Use 3.12+ if you need the new type parameter syntax. Use 3.13 to experiment with free-threaded mode.

## Core Language Features Quick Reference

### Type Hints (PEP 484, 526, 604, 612, 695)

```python
# Basic type annotations
def greet(name: str) -> str:
    return f"Hello, {name}"

# Generic collections (3.9+ -- no need for typing.List, typing.Dict)
def process(items: list[int]) -> dict[str, int]:
    return {str(i): i for i in items}

# Union types (3.10+ -- use | instead of Union)
def parse(value: str | int) -> str:
    return str(value)

# Optional is shorthand for X | None
def find(key: str) -> str | None:
    ...

# TypeVar and generics (3.12+ type parameter syntax)
type Comparable = int | float | str

def maximum[T: Comparable](a: T, b: T) -> T:
    return a if a >= b else b

# TypedDict for structured dictionaries
from typing import TypedDict

class UserConfig(TypedDict):
    name: str
    age: int
    email: str | None
```

### Async/Await (PEP 492)

```python
import asyncio

async def fetch_data(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# TaskGroup (3.11+) -- structured concurrency
async def fetch_all(urls: list[str]) -> list[dict]:
    results = []
    async with asyncio.TaskGroup() as tg:
        for url in urls:
            tg.create_task(fetch_data(url))
    return results

# Async generators
async def stream_lines(path: str):
    async with aiofiles.open(path) as f:
        async for line in f:
            yield line.strip()
```

### Dataclasses (PEP 557)

```python
from dataclasses import dataclass, field

@dataclass
class Config:
    host: str = "localhost"
    port: int = 8080
    tags: list[str] = field(default_factory=list)

# Frozen (immutable) dataclass
@dataclass(frozen=True)
class Point:
    x: float
    y: float

# Slots for memory efficiency (3.10+)
@dataclass(slots=True)
class Measurement:
    timestamp: float
    value: float
    unit: str
```

### Pattern Matching (PEP 634, 3.10+)

```python
def handle_command(command: dict) -> str:
    match command:
        case {"action": "quit"}:
            return "Goodbye"
        case {"action": "greet", "name": str(name)}:
            return f"Hello, {name}"
        case {"action": "move", "x": int(x), "y": int(y)} if x > 0:
            return f"Moving right to ({x}, {y})"
        case _:
            return "Unknown command"
```

### Exception Groups (PEP 654, 3.11+)

```python
# Raising multiple exceptions
def validate(data: dict) -> None:
    errors = []
    if "name" not in data:
        errors.append(ValueError("Missing name"))
    if "age" not in data:
        errors.append(ValueError("Missing age"))
    if errors:
        raise ExceptionGroup("Validation failed", errors)

# Handling exception groups
try:
    validate({})
except* ValueError as eg:
    for exc in eg.exceptions:
        print(f"Validation error: {exc}")
except* TypeError as eg:
    for exc in eg.exceptions:
        print(f"Type error: {exc}")
```

### Context Managers

```python
from contextlib import contextmanager, asynccontextmanager

@contextmanager
def managed_resource(name: str):
    print(f"Acquiring {name}")
    try:
        yield name
    finally:
        print(f"Releasing {name}")

# Parenthesized context managers (3.10+)
with (
    open("input.txt") as fin,
    open("output.txt", "w") as fout,
):
    fout.write(fin.read())
```

## Best Practices

### Always Use Virtual Environments

Never install project dependencies into the system Python. Use `venv`, `uv venv`, or let your package manager (poetry, pdm) handle environment creation.

```bash
# Standard library
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\Scripts\activate      # Windows

# Using uv (faster)
uv venv
source .venv/bin/activate
```

### Adopt Type Annotations

Use type hints throughout your codebase. They improve readability, enable IDE support, and catch bugs early with `mypy` or `pyright`.

```bash
# Type checking with mypy
pip install mypy
mypy src/

# Type checking with pyright (faster, used by Pylance in VS Code)
pip install pyright
pyright src/
```

### Format and Lint with Ruff

Ruff is an extremely fast Python linter and formatter written in Rust. It replaces flake8, isort, black, and many other tools.

```bash
# Install
pip install ruff

# Lint
ruff check src/

# Format (replaces black)
ruff format src/

# Fix auto-fixable issues
ruff check --fix src/
```

Minimal `ruff` configuration in `pyproject.toml`:

```toml
[tool.ruff]
target-version = "py311"
line-length = 88

[tool.ruff.lint]
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # pyflakes
    "I",    # isort
    "UP",   # pyupgrade
    "B",    # flake8-bugbear
    "SIM",  # flake8-simplify
    "TCH",  # flake8-type-checking
]

[tool.ruff.lint.isort]
known-first-party = ["mypackage"]
```

### Use `pyproject.toml` for All Configuration

Consolidate tool configuration in `pyproject.toml` instead of scattering it across `setup.cfg`, `tox.ini`, `.flake8`, etc.

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra -q"

[tool.mypy]
python_version = "3.11"
strict = true

[tool.coverage.run]
source = ["src"]
branch = true
```

### Write Tests with pytest

Use `pytest` as your test runner. It is the de facto standard in the Python ecosystem.

```bash
pip install pytest pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=src --cov-report=term-missing
```

### Use `__all__` for Public API Control

Define `__all__` in `__init__.py` files to make your public API explicit:

```python
# src/mypackage/__init__.py
__all__ = ["Client", "Config", "process_data"]

from .client import Client
from .config import Config
from .processing import process_data
```
