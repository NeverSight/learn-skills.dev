---
name: poetry-rye-dependency-management
description: Python dependency management with Poetry and Rye -- lockfile-driven workflows, dependency groups, monorepo patterns, and migration paths. Covers pyproject.toml-centric packaging for projects not yet on uv.
version: 2.0.0
category: Languages
agents: [python-pro, developer]
tags: [python, poetry, rye, dependency-management, packaging, pyproject-toml, lockfile]
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Bash, Glob, Grep]
globs: '**/pyproject.toml'
best_practices:
  - Always commit lockfiles (poetry.lock / requirements.lock) for reproducible builds
  - Use dependency groups to separate dev, test, and docs dependencies
  - Pin direct dependencies to compatible ranges; let the solver resolve transitive deps
  - Run lockfile audits regularly to detect known CVEs in dependencies
  - Prefer pyproject.toml over setup.py/setup.cfg for all new projects
error_handling: graceful
streaming: supported
verified: true
lastVerifiedAt: '2026-03-01'
---

# Poetry / Rye Dependency Management Skill

<identity>
Python dependency management specialist for Poetry and Rye workflows. Guides lockfile-driven dependency resolution, virtual environment management, dependency groups, publishing, and migration to modern tooling. Covers the full lifecycle from project initialization through CI/CD integration.
</identity>

<capabilities>
- Initialize new Python projects with Poetry or Rye
- Manage dependency groups (main, dev, test, docs, optional extras)
- Configure lockfile-driven builds for reproducibility
- Set up CI/CD pipelines with cached dependency installation
- Migrate between Poetry, Rye, pip, and uv workflows
- Configure monorepo dependency management with workspaces
- Audit dependencies for security vulnerabilities
- Publish packages to PyPI using Poetry or Rye
</capabilities>

## Overview

Poetry and Rye are Python dependency managers that enforce lockfile-driven, deterministic builds. Both use `pyproject.toml` as the single configuration file. Poetry is the established standard (since 2018); Rye is a newer Astral tool that bridges to uv. For greenfield projects, consider `modern-python` skill (uv-native). This skill covers Poetry/Rye for existing codebases and teams already invested in these tools.

## When to Use

- When maintaining existing Poetry or Rye projects
- When a team has standardized on Poetry and migration to uv is not planned
- When publishing Python packages to PyPI (Poetry has mature publishing support)
- When managing monorepo Python workspaces
- When auditing or upgrading dependency lockfiles

## Iron Laws

1. **ALWAYS** commit the lockfile (`poetry.lock` or `requirements.lock`) -- without it, builds are non-deterministic and CI/CD will resolve different versions than development.
2. **NEVER** use `pip install` in a Poetry/Rye-managed project -- it bypasses the resolver and creates ghost dependencies invisible to the lockfile.
3. **ALWAYS** use `poetry add`/`rye add` to add dependencies -- manual `pyproject.toml` edits without re-locking create stale lockfiles.
4. **NEVER** pin transitive dependencies manually -- let the solver manage the full dependency graph; pinning transitive deps causes resolver conflicts.
5. **ALWAYS** separate runtime and development dependencies into groups -- shipping dev/test dependencies in production images wastes space and expands attack surface.

## Anti-Patterns

| Anti-Pattern                                                | Why It Fails                                                              | Correct Approach                                                                   |
| ----------------------------------------------------------- | ------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Editing `pyproject.toml` deps without running `poetry lock` | Lockfile becomes stale; CI installs different versions than intended      | Always run `poetry lock` or `rye lock` after any dependency change                 |
| Using `poetry install` without `--no-root` in CI            | Installs the project in editable mode unnecessarily; slower CI builds     | Use `poetry install --no-root` for library deps only, `--only main` for production |
| Committing `.venv/` directory to version control            | Bloats repo; virtualenvs are platform-specific and non-portable           | Add `.venv/` to `.gitignore`; recreate with `poetry install` or `rye sync`         |
| Mixing pip and Poetry in the same project                   | Creates two dependency graphs; pip-installed packages invisible to Poetry | Use only `poetry add`/`rye add` for all dependency changes                         |
| Using `*` version constraints for all dependencies          | No upper bound protection; major version bumps break silently             | Use compatible release (`^` in Poetry) or upper-bounded ranges                     |

## Workflow

### Poetry Project Setup

```bash
# Initialize new project
poetry init --name my-project --python ">=3.12"

# Add dependencies by group
poetry add requests httpx
poetry add --group dev ruff pytest pytest-cov
poetry add --group docs sphinx

# Install all groups
poetry install

# Install production only
poetry install --only main
```

### Rye Project Setup

```bash
# Initialize new project
rye init my-project
cd my-project

# Add dependencies
rye add requests httpx
rye add --dev ruff pytest pytest-cov

# Sync (install) dependencies
rye sync
```

### pyproject.toml Configuration (Poetry)

```toml
[tool.poetry]
name = "my-project"
version = "0.1.0"
description = "Project description"
authors = ["Team <team@example.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = ">=3.12"
requests = "^2.31"
httpx = "^0.27"

[tool.poetry.group.dev.dependencies]
ruff = "^0.9"
pytest = "^8.0"
pytest-cov = "^6.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

### CI/CD Integration (GitHub Actions)

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install Poetry
        run: pipx install poetry
      - name: Cache dependencies
        uses: actions/cache@v4
        with:
          path: ~/.cache/pypoetry
          key: poetry-$HASH_OF_LOCKFILE
      - name: Install dependencies
        run: poetry install --no-root
      - name: Lint
        run: poetry run ruff check .
      - name: Test
        run: poetry run pytest --cov
```

### Security Audit

```bash
# Poetry: audit dependencies for known CVEs
poetry audit

# Rye: use pip-audit integration
rye run pip-audit
```

### Migration to uv

When ready to migrate from Poetry/Rye to uv:

```bash
# Export Poetry dependencies
poetry export -f requirements.txt --output requirements.txt

# Initialize uv project
uv init
uv add $(grep -v '^#' requirements.txt | grep -v '^\-' | cut -d'=' -f1)

# Verify
uv sync
uv run pytest
```

See `modern-python` skill for the complete uv workflow.

## Complementary Skills

| Skill                                    | Relationship                                             |
| ---------------------------------------- | -------------------------------------------------------- |
| `modern-python`                          | uv-native workflow (recommended for greenfield projects) |
| `python-backend-expert`                  | Framework-specific patterns (Django, FastAPI, Flask)     |
| `tdd`                                    | Test-driven development methodology                      |
| `comprehensive-unit-testing-with-pytest` | Testing strategies and patterns                          |

## Memory Protocol (MANDATORY)

**Before starting:**

Read `.claude/context/memory/learnings.md` for prior Python packaging decisions.

**After completing:** Record any migration issues, version constraints, or resolver conflicts to `.claude/context/memory/learnings.md`.

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
