---
name: python
description: Use uv for fast Python project management, script execution, dependency handling, and tool installation. AVOID pip - always use uv commands (uv add, uv sync, uv run) instead.
---
# Python/uv Development Skill

You are a Python development specialist using `uv`, an extremely fast Python package manager and project management tool. This skill provides comprehensive workflows, best practices, and common patterns for Python development with uv.

## Why uv?

`uv` is the modern replacement for pip, virtualenv, poetry, and pyenv combined:
- **Extremely fast**: 10-100x faster than pip
- **All-in-one**: Package management, virtual environments, Python version management
- **Rust-powered**: Built for speed and reliability
- **Compatible**: Works with existing Python projects and tools

## IMPORTANT: Avoid pip

**DO NOT use `pip` commands.** Always use `uv` equivalents:

- **WRONG**: `pip install requests` → **RIGHT**: `uv add requests`
- **WRONG**: `pip install -r requirements.txt` → **RIGHT**: `uv sync`
- **WRONG**: `pip freeze > requirements.txt` → **RIGHT**: `uv lock` (creates uv.lock)
- **WRONG**: `python -m pip install` → **RIGHT**: `uv run` or `uv add`

The only exception is legacy projects that explicitly require pip compatibility, and even then prefer migrating to uv.

## Core Capabilities

1. **Project Management**: init, add, remove, sync, lock
2. **Running Code**: run (scripts and commands)
3. **Python Management**: python (install, list, pin versions)
4. **Tools**: tool (install and run CLI tools)
5. **Environments**: venv (virtual environment creation)
6. **pip-compatible**: pip interface for legacy workflows
7. **Building**: build, publish packages

## Quick Start

### Running a Python Script

The most common use case - just run your script:

```bash
uv run script.py
uv run script.py arg1 arg2
```

**What this does:**
- Automatically creates/uses virtual environment
- Installs dependencies from pyproject.toml if present
- Runs the script with the correct Python version

### Running a Script with Dependencies

```bash
# Run with additional packages
uv run --with requests script.py
uv run --with requests --with pandas analyze.py

# Run with packages from requirements file
uv run --with-requirements requirements.txt script.py
```

### Running a Python Module

```bash
uv run -m module_name
uv run -m pytest tests/
uv run -m black .
```

### One-off Script Execution (No Project)

```bash
# Run a script in isolation
uv run --isolated script.py

# Run with specific Python version
uv run --python 3.11 script.py

# Run with dependencies without a project
uv run --with httpx --with rich my_script.py
```

## Project Management

### Creating a New Project

```bash
# Create application project
uv init my-app
uv init my-app --app

# Create library project
uv init my-lib --lib

# Create script (single file)
uv init my-script --script

# Create in current directory
uv init

# Create without package structure
uv init --bare  # Only creates pyproject.toml
```

**Project types:**
- `--app`: Application (not meant to be imported)
- `--lib`: Library (meant to be published and imported)
- `--script`: Single-file script with inline dependencies

### Managing Dependencies

```bash
# Add dependency
uv add requests
uv add "requests>=2.31.0"
uv add requests pandas numpy

# Add dev dependency
uv add --dev pytest
uv add --dev black ruff mypy

# Add optional dependency (extra)
uv add --extra docs sphinx

# Remove dependency
uv remove requests
uv remove --dev pytest

# Update dependencies
uv lock --upgrade
uv lock --upgrade-package requests
```

### Syncing Environment

```bash
# Sync environment with lockfile
uv sync

# Sync without dev dependencies
uv sync --no-dev

# Sync with all extras
uv sync --all-extras

# Sync specific extra
uv sync --extra docs

# Exact sync (remove extraneous packages)
uv sync --exact
```

### Lockfile Management

```bash
# Update lockfile
uv lock

# Update all packages
uv lock --upgrade

# Update specific package
uv lock --upgrade-package requests

# Lock without touching network (use cache only)
uv lock --offline
```

## Python Version Management

### Installing Python Versions

```bash
# Install specific Python version
uv python install 3.11
uv python install 3.12.1

# Install multiple versions
uv python install 3.11 3.12

# List available Python versions
uv python list

# List installed versions
uv python list --only-installed
```

### Finding and Pinning Python

```bash
# Find Python installation
uv python find
uv python find 3.11

# Pin project to specific Python version
uv python pin 3.11
uv python pin 3.12.1

# This creates/updates .python-version file
```

### Python Version in Projects

When you create a project, uv automatically:
1. Creates `.python-version` file
2. Detects or installs the appropriate Python version
3. Uses it for all `uv run` commands in that project

## Tool Management

### Installing CLI Tools

```bash
# Install a tool globally
uv tool install ruff
uv tool install black
uv tool install httpie

# Install specific version
uv tool install "black==24.1.0"

# Run tool without installing
uv tool run ruff check .
uv tool run black --check .
```

### Managing Installed Tools

```bash
# List installed tools
uv tool list

# Upgrade tools
uv tool upgrade ruff
uv tool upgrade --all

# Uninstall tool
uv tool uninstall ruff

# Show tool directory
uv tool dir
```

### Common Tools to Install

```bash
# Linters and formatters
uv tool install ruff      # Fast linter and formatter
uv tool install black     # Code formatter
uv tool install mypy      # Type checker

# Testing
uv tool install pytest    # Test framework
uv tool install tox       # Test automation

# Utilities
uv tool install httpie    # HTTP client
uv tool install rich-cli  # Pretty terminal output
uv tool install pipx      # Legacy tool installer
```

## Virtual Environments

### Creating Virtual Environments

```bash
# Create venv in current directory
uv venv

# Create with specific Python version
uv venv --python 3.11

# Create in specific location
uv venv path/to/venv

# Create with specific name
uv venv .venv-dev
```

### Using Virtual Environments

```bash
# Activate (traditional way)
source .venv/bin/activate

# Or just use uv run (recommended)
uv run python script.py
uv run pytest
```

**Best Practice**: With uv, you rarely need to manually activate environments. Just use `uv run`.

## Legacy pip Interface (AVOID - Use Native uv Commands Instead)

**WARNING**: This interface exists only for legacy compatibility. **Prefer native uv commands** (`uv add`, `uv sync`, `uv lock`) over `uv pip` commands.

Only use `uv pip` when:
- Working with a legacy project that cannot be migrated yet
- Maintaining compatibility with existing CI/CD that expects pip commands
- As a temporary bridge during migration

**Better alternatives:**
- `uv pip install requests` → Use `uv add requests` instead
- `uv pip install -r requirements.txt` → Use `uv sync` instead
- `uv pip freeze` → Use `uv lock` instead

```bash
# Legacy pip-compatible commands (avoid if possible)
uv pip install requests              # Better: uv add requests
uv pip install -r requirements.txt   # Better: uv sync
uv pip list                          # Better: uv tree
uv pip show requests                 # Better: uv tree --package requests
uv pip freeze > requirements.txt     # Better: uv lock
uv pip uninstall requests            # Better: uv remove requests
```

## Common Workflows

### Workflow 1: New Python Project

```bash
# 1. Create project
uv init my-project --app
cd my-project

# 2. Add dependencies
uv add requests httpx rich

# 3. Add dev dependencies
uv add --dev pytest black ruff

# 4. Run your code
uv run python main.py

# 5. Run tests
uv run pytest
```

### Workflow 2: Working with Existing Project

```bash
# 1. Clone repository
git clone <repo>
cd <repo>

# 2. Sync dependencies (reads pyproject.toml)
uv sync

# 3. Run the application
uv run python main.py

# 4. Run tests
uv run pytest
```

### Workflow 3: Quick Script with Dependencies

```bash
# Option 1: Inline dependencies in script
cat > script.py << 'EOF'
# /// script
# dependencies = ["requests", "rich"]
# ///

import requests
from rich import print

response = requests.get("https://api.github.com")
print(response.json())
EOF

uv run --script script.py

# Option 2: Command-line dependencies
uv run --with requests --with rich script.py
```

### Workflow 4: Testing and Linting

```bash
# Run tests
uv run pytest
uv run pytest tests/
uv run pytest -v --cov

# Format code
uv run black .
uv run ruff format .

# Lint code
uv run ruff check .
uv run ruff check --fix .

# Type check
uv run mypy .
```

### Workflow 5: Dependency Updates

```bash
# 1. Check current dependencies
uv tree

# 2. Update all dependencies
uv lock --upgrade

# 3. Update specific package
uv lock --upgrade-package requests

# 4. Sync environment
uv sync

# 5. Run tests to verify
uv run pytest
```

### Workflow 6: Building and Publishing

```bash
# Build package
uv build

# Publish to PyPI
uv publish

# Publish to test PyPI
uv publish --index https://test.pypi.org/simple/
```

## Best Practices

### 1. Always Use uv run

Instead of:
```bash
# Don't do this
source .venv/bin/activate
python script.py
```

Do this:
```bash
# Do this
uv run script.py
```

**Benefits:**
- Automatic environment management
- Ensures dependencies are synced
- Works consistently across systems

### 2. Pin Python Versions

Always create `.python-version` file:
```bash
uv python pin 3.11
```

This ensures everyone on the team uses the same Python version.

### 3. Use Lockfiles

Commit `uv.lock` to version control:
- Ensures reproducible builds
- Locks transitive dependencies
- Faster installs for teammates

### 4. Separate Dev Dependencies

```bash
uv add --dev pytest black ruff mypy
```

This keeps production dependencies clean.

### 5. Use Scripts Section

In `pyproject.toml`:
```toml
[project.scripts]
my-cli = "my_package.cli:main"

[tool.uv]
dev-dependencies = [
    "pytest>=7.0.0",
    "black>=24.0.0",
]
```

Then run:
```bash
uv run my-cli
```

## Project Structure

### Typical uv Project Layout

```
my-project/
├── .python-version      # Python version (e.g., "3.11")
├── pyproject.toml       # Project config and dependencies
├── uv.lock             # Lockfile (commit this!)
├── .venv/              # Virtual environment (don't commit)
├── src/
│   └── my_package/
│       ├── __init__.py
│       └── main.py
└── tests/
    └── test_main.py
```

### pyproject.toml Example

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "My awesome project"
requires-python = ">=3.11"
dependencies = [
    "requests>=2.31.0",
    "rich>=13.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "black>=24.0.0",
    "ruff>=0.1.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
dev-dependencies = [
    "pytest>=7.0.0",
    "black>=24.0.0",
]
```

## Advanced Features

### Running with Extras

```bash
# Run with optional dependencies
uv run --extra docs sphinx-build
uv run --all-extras pytest
```

### Dependency Groups

```bash
# Add to specific group
uv add --group test pytest

# Run with specific group
uv run --group test pytest

# Sync specific group
uv sync --group test
```

### Environment Variables

```bash
# Use .env file
uv run --env-file .env script.py

# Override env file
uv run --no-env-file script.py
```

### Offline Mode

```bash
# Work without network
uv run --offline script.py
uv sync --offline
uv lock --offline
```

### Custom Indexes

```bash
# Use custom PyPI index
uv add requests --index https://my-pypi.org/simple/

# Use multiple indexes
uv add package --index https://index1.org/simple/ --index https://index2.org/simple/
```

## Troubleshooting

### Issue: Command not found after uv tool install

**Solution**: Update shell PATH
```bash
uv tool update-shell
# Then restart shell or source config
```

### Issue: Python version not found

**Solution**: Install Python with uv
```bash
uv python install 3.11
uv python pin 3.11
```

### Issue: Dependencies not syncing

**Solution**: Force sync
```bash
uv sync --reinstall
uv sync --exact
```

### Issue: Cache issues

**Solution**: Clear cache
```bash
uv cache clean
uv run --no-cache script.py
```

### Issue: Lock file out of sync

**Solution**: Regenerate lock
```bash
uv lock --upgrade
uv sync
```

## Performance Tips

### 1. Use --frozen for CI/CD

```bash
# Skip lockfile updates in CI
uv sync --frozen
uv run --frozen pytest
```

### 2. Leverage Cache

uv automatically caches packages. To see cache:
```bash
uv cache dir
```

### 3. Parallel Operations

uv automatically parallelizes operations. No configuration needed.

## Migration from Other Tools

### From pip + virtualenv

```bash
# Old way
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python script.py

# New way
uv run script.py  # That's it!
```

### From Poetry

```bash
# Old: poetry install && poetry run python script.py
# New:
uv sync && uv run python script.py
```

### From Pipenv

```bash
# Old: pipenv install && pipenv run python script.py
# New:
uv sync && uv run python script.py
```

## Integration with Other Tools

### pytest

```bash
uv run pytest
uv run pytest --cov --cov-report=html
```

### black/ruff

```bash
uv run black .
uv run ruff check --fix .
```

### mypy

```bash
uv run mypy src/
```

### jupyter

```bash
uv add --dev jupyter
uv run jupyter notebook
```

## Quick Reference

```bash
# Run script
uv run script.py

# Run with dependencies
uv run --with requests script.py

# Project setup
uv init my-project
uv add package-name
uv add --dev pytest

# Environment management
uv sync
uv lock --upgrade

# Python management
uv python install 3.11
uv python pin 3.11

# Tools
uv tool install ruff
uv tool run black .

# Legacy compatibility (AVOID - use uv add/sync instead)
uv pip install package              # DON'T USE - use: uv add package
uv pip install -r requirements.txt  # DON'T USE - use: uv sync

# Testing and quality
uv run pytest
uv run black .
uv run ruff check .
```

## Key Differences from pip/virtualenv

| Task | Old Way | uv Way |
|------|---------|--------|
| Create venv | `python -m venv .venv` | `uv venv` (or automatic) |
| Activate | `source .venv/bin/activate` | Not needed with `uv run` |
| Install deps | `pip install -r requirements.txt` | `uv sync` |
| Run script | `python script.py` | `uv run script.py` |
| Add package | `pip install requests` | `uv add requests` |
| Global tool | `pip install black` | `uv tool install black` |

## Common Patterns

### Pattern 1: Quick Data Analysis Script

```bash
uv run --with pandas --with matplotlib analyze.py
```

### Pattern 2: Testing Before Commit

```bash
uv run pytest && uv run black --check . && uv run ruff check .
```

### Pattern 3: Update All Dependencies

```bash
uv lock --upgrade && uv sync && uv run pytest
```

### Pattern 4: Run with Specific Python

```bash
uv run --python 3.11 script.py
```

### Pattern 5: Install and Run Tool

```bash
uv tool run ruff check .  # Installs if needed, then runs
```

## Summary

**Primary directive**: Use `uv run` for executing Python scripts and commands.

**Key advantages:**
- No manual environment activation needed
- Automatic dependency management
- Extremely fast operations
- Single tool for all Python workflows

**Most common commands:**
- `uv run script.py` - Run anything
- `uv add package` - Add dependency
- `uv sync` - Sync environment
- `uv python pin 3.11` - Set Python version
