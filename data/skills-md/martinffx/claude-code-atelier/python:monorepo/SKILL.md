---
name: python:monorepo
description: Python monorepo architecture with uv workspaces, mise, and apps/packages pattern. Use when setting up project structure, configuring workspaces, managing dependencies across packages, or designing multi-app Python repositories.
user-invocable: false
---

# Python Monorepo with uv Workspaces

Modern Python monorepo architecture using `uv` for workspace management and `mise` for Python version and task orchestration.

## Core Concepts

**Monorepo**: Single repository containing multiple related packages and applications

**uv workspace**: Python's answer to npm/pnpm workspaces
- Single lock file for entire repo
- Shared virtual environment
- Cross-package dependency resolution

## Directory Structure

```
my-monorepo/
├── .mise.toml           # Python version + task runner
├── pyproject.toml       # Root workspace config
├── uv.lock              # Unified lock file
├── apps/                # Deployable applications
│   ├── api/
│   └── worker/
└── packages/            # Shared libraries
    ├── core/
    └── utils/
```

## Workspace Configuration

**Root pyproject.toml:**

```toml
[project]
name = "my-monorepo"
version = "0.1.0"
requires-python = ">=3.12"

[tool.uv.workspace]
members = ["apps/*", "packages/*"]

[tool.uv]
dev-dependencies = [
    "pytest>=8.0.0",
    "ruff>=0.8.0",
    "basedpyright>=1.0.0",
]
```

See `references/workspace-config.md` for detailed configurations.

## Package Linking

Workspace packages reference each other by distribution name:

**packages/utils/pyproject.toml:**
```toml
[project]
name = "my-utils"
dependencies = ["my-core"]
```

**apps/api/pyproject.toml:**
```toml
[project]
name = "my-api"
dependencies = ["my-core", "my-utils", "fastapi>=0.100.0"]
```

## Cross-Package Import

**packages/core/src/my_core/entities.py:**
```python
class User:
    def __init__(self, email: str):
        self.email = email
```

**apps/api/src/my_api/main.py:**
```python
from my_core.entities import User  # Import from workspace package

def run():
    # App code...
```

## Dependency Direction (Critical)

```
apps/ → packages/  (Apps depend on packages)
packages/ ⇏ apps/  (Never the reverse)
```

**Rules:**
- Apps can depend on packages
- Packages can depend on other packages
- Packages NEVER depend on apps
- Avoid circular dependencies

## mise Task Runner

**.mise.toml:**

```toml
[tools]
python = "3.12"

[tasks.check]
depends = ["lint", "typecheck", "test"]

[tasks.lint]
run = "uv run ruff check ."
```

**Usage:** `mise run check`

## Core uv Commands

```bash
uv sync                           # Install all packages
uv add fastapi --package my-api   # Add to specific package
uv add my-core --package my-api   # Add workspace package
uv run pytest                      # Run tests
uv lock --upgrade                 # Update dependencies
```

## Best Practices

1. Single lock file at root
2. Shared dev tools (ruff, pytest) in root dev-dependencies
3. Pin Python version with mise
4. Apps depend on packages only
5. Use namespace packages for logical grouping (optional)

## References

For detailed patterns:
- `references/workspace-config.md` - pyproject.toml patterns, dependencies, versions
- `references/docker.md` - Multi-stage Docker builds
- `references/namespace-packages.md` - PEP 420 namespace packages
