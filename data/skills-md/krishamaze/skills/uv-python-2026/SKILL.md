---
name: uv-python-2026
description: >
  uv — the 2026 standard Python package manager (replaces pip, venv, pyenv, pip-tools, pipx).
  Use this skill for ALL Python dependency management, virtual environments, Python version
  management, and Docker Python setups. NEVER use bare pip for new projects in 2026.
  Covers uv init, uv add, uv sync, lockfiles, pyproject.toml, Docker integration,
  and migration from pip/Poetry.
---

# uv — Python Package Manager 2026

## Why uv in 2026
uv is the **community consensus default** for new Python projects in 2026:
- Written in Rust — 10–100x faster than pip
- Single binary: replaces pip + pip-tools + pyenv + virtualenv + pipx + Poetry (for apps)
- Global content-addressable cache — packages downloaded once, shared across projects
- Lockfile support (`uv.lock`) — reproducible environments
- Native `pyproject.toml` support (PEP 517/518)

## Installation
```bash
# On any Linux/Mac (VPS, Docker, CI)
# ⚠️  Always pin the version — never pipe an unpinned URL to sh.
curl -LsSf https://astral.sh/uv/0.10.7/install.sh | sh

# Verify
uv --version   # expect 0.10.7
```

> **Security note:** Review the uv [GitHub releases](https://github.com/astral-sh/uv/releases)
> before bumping the pinned version. In CI, prefer downloading the binary and
> verifying its SHA-256 checksum against the published release manifest.

## New Project Setup
```bash
uv init my-project       # creates: pyproject.toml, .python-version, src/, uv.lock
cd my-project
uv python pin 3.12       # pin Python version for this project
```

Generated `pyproject.toml`:
```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []
```

## Add Dependencies
```bash
uv add fastapi           # adds to pyproject.toml + updates uv.lock
uv add camoufox[geoip]   # extras syntax
uv add playwright

# Dev-only dependencies
uv add --dev pytest httpx ruff

# Remove
uv remove requests
```

## Install / Sync Environment
```bash
# Install all deps from lockfile (exact versions — use in CI/Docker)
uv sync

# Install without dev deps (production)
uv sync --no-dev

# Install from lockfile only — never resolve (strict reproducibility)
uv sync --frozen
```

## Run Commands
```bash
# Run script in project environment
uv run python main.py
uv run uvicorn app.main:app --reload
uv run pytest

# No need to activate venv manually
```

## Python Version Management
```bash
# Install specific Python versions
uv python install 3.12 3.13

# Pin version for current project
uv python pin 3.12         # writes .python-version file

# List installed versions
uv python list
```

## Docker Integration (2026 Pattern)
```dockerfile
FROM python:3.12-slim-bookworm

# Copy uv binary from official image — always pin version, never use :latest
COPY --from=ghcr.io/astral-sh/uv:0.10.7 /uv /uvx /bin/

WORKDIR /app

# Copy lockfile and pyproject first (layer caching)
COPY pyproject.toml uv.lock ./

# Install deps only (not the project itself yet)
RUN uv sync --frozen --no-install-project --no-dev

# Copy application code
COPY . .

# Install project
RUN uv sync --frozen --no-dev

# Add venv to PATH
ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "-m", "app.main"]
```

Key Docker rules:
- **Pin the uv image tag** — never use `:latest`; for maximum safety use an immutable SHA digest (e.g., `ghcr.io/astral-sh/uv@sha256:<digest>`)
- Always commit `uv.lock` to version control
- Use `--frozen` in Docker/CI (never auto-resolve in production)
- Use `--no-dev` in production containers
- Copy `pyproject.toml` + `uv.lock` before source code for layer caching

## Pip Compatibility Mode (Migration Path)
```bash
# If you have existing requirements.txt
uv pip install -r requirements.txt   # same as pip, 100x faster
uv pip compile requirements.in -o requirements.txt  # lock deps
uv pip sync requirements.txt         # install exact versions

# Works with existing Dockerfile — just swap pip → uv pip
```

## pyproject.toml Structure (2026 Standard)
```toml
[project]
name = "threads-agent"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.34.0",
    "camoufox[geoip]>=0.4.0",
    "playwright>=1.58.0",
    "pydantic>=2.0.0",
    "python-dotenv>=1.0.0",
]

[dependency-groups]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.25.0",
    "httpx>=0.28.0",
    "ruff>=0.9.0",
]

[tool.ruff]
line-length = 88
target-version = "py312"
```

## Workspace (Monorepo) Support
```bash
# For multi-package projects (e.g., browser-agent + api + frontend tooling)
uv init --workspace
```

```toml
# Root pyproject.toml
[tool.uv.workspace]
members = ["packages/*"]
```

## Anti-Patterns
```bash
# ❌ Never for new projects in 2026
pip install camoufox
pip install -r requirements.txt

# ❌ Never create venv manually
python -m venv .venv

# ❌ Never use requirements.txt as primary dependency spec for new projects
# (use pyproject.toml + uv.lock instead)

# ❌ Never use poetry for automation/app projects in 2026
# (Poetry still valid for library publishing only)
```

## References
- Official docs: https://docs.astral.sh/uv/
- GitHub: https://github.com/astral-sh/uv
