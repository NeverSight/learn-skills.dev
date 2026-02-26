---
name: pixi
description: Comprehensive guide for using Pixi, a fast and reproducible package management tool for Python, Rust, C/C++, and other languages. Use when (1) Managing Python project dependencies and environments, (2) Setting up reproducible development environments with conda and PyPI packages, (3) Creating cross-platform task runners and build pipelines, (4) Managing multiple isolated environments for testing and development, (5) Installing and managing global CLI tools, (6) Building and packaging conda packages, (7) Working with mixed conda and PyPI dependencies, (8) Setting up CI/CD pipelines with reproducible environments
metadata:
  short-description: Fast and reproducible package management tool
---

# Pixi Package Manager

Pixi is a fast, modern, and reproducible package management tool that combines conda and PyPI package management with built-in task running and environment management.

## Quick Start

### Installation

```bash
# Linux & macOS
curl -fsSL https://pixi.sh/install.sh | sh

# Windows
powershell -ExecutionPolicy Bypass -c "irm -useb https://pixi.sh/install.ps1 | iex"
```

Restart your terminal after installation.

### Create a Project

```bash
# Initialize a new workspace
pixi init my-project
cd my-project

# Add dependencies
pixi add python
pixi add numpy
pixi add --pypi requests

# Run commands
pixi run python -c "import numpy; print(numpy.__version__)"

# Enter environment shell
pixi shell
```

## Core Workflows

### Project Management

**Initialize workspace:**
```bash
pixi init [project-name]
pixi init --format pyproject  # Use pyproject.toml format
```

**Add dependencies:**
```bash
pixi add python ">=3.11"
pixi add numpy pandas
pixi add --pypi requests flask  # Add PyPI packages
pixi add --feature test pytest  # Add to specific feature
pixi add --platform linux-64 glibc  # Platform-specific
```

**Remove dependencies:**
```bash
pixi remove numpy
pixi remove --feature test pytest
```

**Update dependencies:**
```bash
pixi update              # Update within constraints
pixi upgrade             # Upgrade to latest versions
pixi lock                # Regenerate lockfile only
```

**Install environment:**
```bash
pixi install                    # Install default environment
pixi install --environment test # Install specific environment
pixi install --frozen           # Install from lockfile only (no updates)
pixi install --locked           # Install only if lockfile is up-to-date
```

### Running Commands

**Execute tasks or commands:**
```bash
pixi run python script.py
pixi run --environment test pytest
pixi run task-name
pixi run --environment dev task-name
```

**Activate shell:**
```bash
pixi shell
pixi shell --environment test
```

**One-off commands:**
```bash
pixi exec python --version
pixi exec --spec "python=3.12" python --version
```

### Task Management

**Define tasks in `pixi.toml`:**
```toml
[tasks]
# Simple task
hello = "echo Hello World"

# Task with dependencies
build = { cmd = "cargo build", depends-on = ["fmt", "lint"] }

# Task with environment variables
run = { cmd = "python main.py", env = { DEBUG = "true" } }

# Task with caching
compile = { 
    cmd = "gcc -o output input.c", 
    inputs = ["input.c"], 
    outputs = ["output"] 
}

# Task with arguments
greet = { 
    cmd = "echo Hello, {{ name }}!", 
    args = [{ arg = "name", default = "World" }] 
}
```

**Manage tasks:**
```bash
pixi task add build "cargo build"
pixi task add test "pytest" --depends-on build
pixi task add lint "ruff check ." --feature dev
pixi task list
pixi task remove build
```

**Run tasks with arguments:**
```bash
pixi run greet Alice
pixi run build production linux-64
```

### Multiple Environments

**Using features and environments:**
```toml
# Default dependencies
[dependencies]
python = ">=3.11"

# Feature-specific dependencies
[feature.test.dependencies]
pytest = "*"
pytest-cov = "*"

[feature.lint.dependencies]
ruff = "*"
mypy = "*"

[feature.dev.dependencies]
ipython = "*"

# Define environments
[environments]
default = []                    # Just default feature
test = ["test"]                 # default + test
dev = ["test", "lint", "dev"]   # Combine multiple features
```

**Work with environments:**
```bash
pixi add --feature test pytest
pixi run --environment test pytest
pixi shell --environment dev
pixi list --environment test
pixi install --environment prod
```

**Solve groups (ensure shared versions):**
```toml
[environments]
prod = { features = [], solve-group = "prod" }
test-prod = { features = ["test"], solve-group = "prod" }
```

### Global Tools

**Install global CLI tools:**
```bash
pixi global install gh nvim ipython btop ripgrep
pixi global install terraform ansible k9s
```

**Manage global installations:**
```bash
pixi global list
pixi global add nvim ripgrep  # Add to existing global environment
pixi global update
pixi global uninstall gh
pixi global sync  # Sync with global manifest
```

### Manifest Structure

**Basic `pixi.toml`:**
```toml
[project]
name = "my-project"
version = "0.1.0"
channels = ["conda-forge"]
platforms = ["linux-64", "osx-64", "win-64"]

[dependencies]
python = ">=3.11"
numpy = ">=1.21"

[pypi-dependencies]
requests = ">=2.25"
fastapi = { version = ">=0.100", extras = ["all"] }

[tasks]
test = "pytest"
dev = "uvicorn main:app --reload"

[environments]
default = ["test"]
```

**Package specifications:**
```toml
# Version constraints
python = ">=3.11,<3.13"     # Range
numpy = "==1.21.0"          # Exact
pytorch = "2.0.*"           # Wildcard

# Channel specification
pytorch = { version = "2.0.*", channel = "pytorch" }

# Build string
numpy = { version = ">=1.21", build = "py311*" }

# PyPI with extras
pandas = { version = ">=1.0", extras = ["dataframe", "sql"] }

# Git dependencies
package = { git = "https://github.com/user/repo.git", rev = "abc123" }

# Local editable
my-pkg = { path = ".", editable = true }
```

### Configuration

**Project configuration (`.pixi/config.toml`):**
```toml
# Pin strategy
pinning-strategy = "semver"  # or "exact-version", "major", "minor", "latest-up"

# Shell behavior
[shell]
change-ps1 = true
```

**Global configuration (`~/.pixi/config.toml`):**
```toml
# Default channels for new projects
default-channels = ["conda-forge"]

# PyPI configuration
[pypi-config]
index-url = "https://pypi.org/simple"
extra-index-urls = ["https://custom-index.com/simple"]

# Proxy configuration
[proxy-config]
https = "http://proxy.example.com:8080"
```

**Configure via CLI:**
```bash
pixi config set pinning-strategy semver
pixi config set shell.change-ps1 false
pixi config list
pixi config edit
```

### Lockfile Management

**Understanding lockfiles:**
- `pixi.lock` ensures reproducible environments
- Contains exact package versions and build info
- Should be committed to version control
- Automatically updated when dependencies change

**Lockfile commands:**
```bash
pixi lock                    # Generate/update lockfile
pixi install --frozen        # Use lockfile as-is (no updates)
pixi install --locked        # Install only if lockfile matches manifest
```

## Common Patterns

### Python Project Setup

```toml
[project]
channels = ["conda-forge"]
platforms = ["linux-64", "osx-64", "win-64"]

[dependencies]
python = ">=3.11"

[pypi-dependencies]
fastapi = "*"
uvicorn = { extras = ["standard"], version = "*" }
# Editable install
my-package = { path = ".", editable = true }

[feature.test.dependencies]
pytest = "*"
pytest-asyncio = "*"

[tasks]
dev = "uvicorn main:app --reload"
test = "pytest"
lint = "ruff check . && mypy ."

[environments]
default = ["test", "lint"]
```

### C/C++ Project

```toml
[dependencies]
cmake = "*"
ninja = "*"

[target.linux-64.dependencies]
gcc_linux-64 = "*"

[target.osx-64.dependencies]
clang_osx-64 = "*"

[tasks]
configure = "cmake -S . -B build -G Ninja"
build = { cmd = "cmake --build build", depends-on = ["configure"] }
test = { cmd = "ctest --test-dir build", depends-on = ["build"] }
```

### Multi-Version Testing

```toml
[feature.py39.dependencies]
python = "3.9.*"
[feature.py310.dependencies]
python = "3.10.*"
[feature.py311.dependencies]
python = "3.11.*"

[environments]
py39 = ["py39", "test"]
py310 = ["py310", "test"]
py311 = ["py311", "test"]
```

## Platform-Specific Configuration

```toml
[target.linux-64.dependencies]
glibc = "2.28"

[target.osx-arm64.dependencies]
mlx = "*"

[target.win-64.dependencies]
msmpi = "~=10.1.1"

[target.unix.tasks]
clean = "rm -rf build/"

[target.win.tasks]
clean = "rmdir /s /q build"
```

## Environment Activation

**Activation scripts:**
```toml
[activation]
scripts = ["setup.sh"]
env = { 
    MY_VAR = "value",
    PATH = "$PIXI_PROJECT_ROOT/bin:$PATH"
}

[target.win-64.activation]
scripts = ["setup.bat"]
```

**In shell:**
```bash
pixi shell
# Environment is automatically activated
# Type 'exit' to leave
```

## Utility Commands

```bash
# Information
pixi info                    # Show workspace info
pixi list                    # List installed packages
pixi list --environment test # List packages in environment
pixi tree                    # Show dependency tree
pixi tree --invert package   # Show reverse dependencies

# Search
pixi search numpy            # Search for packages

# Cleanup
pixi clean                   # Remove environments
pixi clean --environment test
pixi clean cache             # Clear package cache

# Authentication
pixi auth login              # Login to private channels
pixi auth logout

# Completion
pixi completion --shell bash > ~/.bash_completion
pixi completion --shell zsh > ~/.zsh_completion
```

## Troubleshooting

**Environment out of sync:**
```bash
pixi install  # Automatically fixes and updates
pixi reinstall  # Force reinstall
```

**Lockfile issues:**
```bash
rm pixi.lock  # Delete and regenerate
pixi lock     # Regenerate lockfile
```

**Clear cache:**
```bash
pixi clean cache
```

**Check configuration:**
```bash
pixi info -vvv  # Show all configuration locations
pixi config list
```

## Best Practices

1. **Commit lockfiles**: Always commit `pixi.lock` to version control
2. **Use features**: Organize dependencies by purpose (test, lint, dev)
3. **Use solve-groups**: When environments need shared versions
4. **Task caching**: Specify `inputs` and `outputs` for faster rebuilds
5. **Platform-specific**: Use `target` tables for cross-platform differences
6. **Prefer conda**: Use conda packages when available (more stable, binary deps)
7. **Editable installs**: Use `editable = true` for local packages

## References

For detailed information, see:
- [manifest.md](references/manifest.md) - Complete manifest reference
- [commands.md](references/commands.md) - Full command reference
- [advanced.md](references/advanced.md) - Advanced features and patterns
