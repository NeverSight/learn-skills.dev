---
name: uv-ruff-python-tools
description: Modern Python development with uv (10-100x faster package manager) and ruff (extremely fast linter/formatter). Use when managing Python projects, dependencies, virtual environments, installing packages, linting code, or formatting Python files. Triggers on phrases like "uv install", "ruff check", "python package manager", "format python code", or working with pyproject.toml files.
---

# UV & Ruff: Modern Python Development Tools

Supercharge your Python development with Astral's blazing-fast tooling suite - uv for package management and ruff for code quality.

## When to Use This Skill

Use this skill when you need to:
- **Package Management**: Install, update, or manage Python dependencies 10-100x faster than pip
- **Project Setup**: Initialize new Python projects with modern standards
- **Python Versions**: Install and manage multiple Python versions
- **Code Linting**: Check Python code for errors and style issues
- **Code Formatting**: Auto-format Python code to consistent style
- **Virtual Environments**: Create and manage isolated Python environments
- **Migration**: Move from pip, conda, poetry, or pipx to modern tooling

## Quick Start

### Installing UV

```bash
# macOS/Linux - standalone installer
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows - PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# With Homebrew
brew install uv

# With pipx
pipx install uv

# Verify installation
uv version
```

### Installing Ruff

```bash
# With uv (recommended)
uv tool install ruff

# With pip
pip install ruff

# With Homebrew
brew install ruff

# Verify installation
ruff version
```

## Common Workflows

### Project Management with UV

```bash
# Create a new project
uv init my-project
cd my-project

# Add dependencies
uv add requests pandas numpy

# Add development dependencies
uv add --dev pytest black ruff

# Install all dependencies
uv sync

# Run a script in the project environment
uv run python main.py

# Run a tool (like pytest)
uv run pytest

# Update dependencies
uv lock --upgrade
uv sync
```

### Code Quality with Ruff

```bash
# Check for linting errors
ruff check .

# Auto-fix linting errors
ruff check --fix .

# Format code
ruff format .

# Check formatting without changes
ruff format --check .

# Watch mode (continuous linting)
ruff check --watch

# Lint and format in one command
ruff check --fix . && ruff format .
```

### Python Version Management

```bash
# Install Python versions
uv python install 3.11 3.12 3.13

# List installed Python versions
uv python list

# Pin Python version for project
uv python pin 3.12

# Use specific Python version
uv run --python 3.11 python script.py
```

## Key Features

### UV Features

**🚀 Speed**: 10-100x faster than pip for package installation
- Parallel downloads and caching
- Rust-powered dependency resolution
- Global package cache for deduplication

**📦 All-in-One Tool**: Replaces multiple tools
- `pip` - Package installation
- `pip-tools` - Dependency locking
- `pipx` - Tool installation
- `poetry` - Project management
- `pyenv` - Python version management
- `virtualenv` - Environment creation

**🔒 Reproducible Environments**:
- Universal lockfiles (`uv.lock`)
- Platform-independent resolution
- Version pinning

### Ruff Features

**⚡ Extreme Speed**: 10-100x faster than existing linters
- Written in Rust for maximum performance
- Processes entire codebases in milliseconds

**🔧 Unified Tool**: Replaces multiple tools
- `Flake8` - Linting
- `Black` - Formatting
- `isort` - Import sorting
- `pyupgrade` - Modern Python syntax
- `autoflake` - Unused code removal

**📏 800+ Rules**: Comprehensive code quality
- Pyflakes error detection
- pycodestyle (PEP 8) compliance
- flake8-bugbear best practices
- Many popular Flake8 plugins built-in

## Common Patterns

### UV Patterns

```bash
# Quick tool execution (like npx or pipx)
uvx ruff check .
uvx black .
uvx pytest

# Build and publish packages
uv build
uv publish

# Pip-compatible interface (drop-in replacement)
uv pip install requests
uv pip freeze > requirements.txt
uv pip compile requirements.in
uv pip sync requirements.txt

# Create virtual environment
uv venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Run scripts with inline dependencies
uv add --script my_script.py requests
uv run my_script.py
```

### Ruff Patterns

```bash
# Enable specific rule sets
ruff check --select E,W,F,I .

# Ignore specific rules
ruff check --ignore E501 .

# Show fixes that will be applied
ruff check --diff .

# Format with preview features
ruff format --preview .

# Check specific files
ruff check src/main.py tests/test_main.py

# Output formats
ruff check --output-format json .
ruff check --output-format github .
```

## Configuration

### UV Configuration (pyproject.toml)

```toml
[project]
name = "my-project"
version = "0.1.0"
description = "My Python project"
requires-python = ">=3.11"
dependencies = [
    "requests>=2.31.0",
    "pandas>=2.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "ruff>=0.1.0",
]

[tool.uv]
dev-dependencies = [
    "pytest>=7.0.0",
    "ruff>=0.1.0",
]

[tool.uv.sources]
# Use specific package sources if needed
```

### Ruff Configuration (pyproject.toml)

```toml
[tool.ruff]
# Set line length
line-length = 88
indent-width = 4
target-version = "py311"

# Exclude directories
exclude = [
    ".git",
    ".venv",
    "__pycache__",
    "build",
    "dist",
]

[tool.ruff.lint]
# Enable rule sets
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # Pyflakes
    "I",   # isort
    "B",   # flake8-bugbear
    "UP",  # pyupgrade
]

# Ignore specific rules
ignore = [
    "E501",  # line too long (handled by formatter)
]

# Allow auto-fix for all enabled rules
fixable = ["ALL"]
unfixable = []

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]  # Allow unused imports
"tests/*" = ["S101"]      # Allow assert statements

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
line-ending = "auto"
```

## Integration with Development Tools

### Pre-commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.12.8
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

### CI/CD (GitHub Actions)

```yaml
name: Lint and Test

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh

      - name: Install dependencies
        run: uv sync

      - name: Lint with ruff
        run: uv run ruff check .

      - name: Format check with ruff
        run: uv run ruff format --check .

      - name: Run tests
        run: uv run pytest
```

## Detailed Documentation

For comprehensive guides and advanced usage, see the reference files:

- **references/uv-guide.md** - Complete uv documentation
  - Project management workflows
  - Python version management
  - Package building and publishing
  - Migration from other tools

- **references/ruff-guide.md** - Complete ruff documentation
  - All 800+ linting rules
  - Formatting options
  - Rule configuration
  - Editor integration

- **references/migration.md** - Migration guides
  - From pip + virtualenv
  - From conda
  - From poetry
  - From pipx

- **references/workflows.md** - Advanced workflows
  - Monorepo management
  - Docker integration
  - Production deployments

## Resources

**Official Documentation:**
- [uv Documentation](https://docs.astral.sh/uv/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Astral (Parent Company)](https://astral.sh)

**GitHub Repositories:**
- [astral-sh/uv](https://github.com/astral-sh/uv)
- [astral-sh/ruff](https://github.com/astral-sh/ruff)

**Community:**
- [Ruff Discord](https://discord.gg/astral-sh)
- [GitHub Discussions](https://github.com/astral-sh/uv/discussions)

## Troubleshooting

**UV Issues:**
```bash
# Clear cache
uv cache clean

# Reinstall Python
rm -r "$(uv python dir)"
uv python install 3.12

# Reset lockfile
rm uv.lock
uv lock
```

**Ruff Issues:**
```bash
# Clear cache
ruff clean

# Show current settings
ruff check --show-settings

# List all available rules
ruff rule --all

# Explain a specific rule
ruff rule E501
```

## Notes

- UV and Ruff are both built by Astral and designed to work together seamlessly
- UV automatically creates and manages virtual environments - no manual activation needed
- Ruff can replace Black, isort, Flake8, and more with a single tool
- Both tools are written in Rust for maximum performance
- UV's lockfile format is becoming a Python standard (PEP 751 proposal)
- Ruff is compatible with Black formatting by default
