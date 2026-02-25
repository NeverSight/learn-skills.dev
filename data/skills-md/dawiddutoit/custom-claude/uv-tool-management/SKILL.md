---
name: uv-tool-management
description: |
  Manages Python CLI tools with uv. Learn when to use uvx for temporary execution, uv tool install for persistent tools, and how to differentiate between tool dependencies and project dependencies. Includes version management, listing, cleanup, and scenarios for running tools with specific Python versions.
allowed-tools: Read, Bash, Grep
---

# uv Tool Management

## Purpose

This skill teaches you how to efficiently manage Python command-line tools using uv, including running tools on-demand without installation, installing persistent tools globally, managing versions, and understanding when to use tools versus project dependencies.

## Quick Start

Run any CLI tool without installing it:

```bash
# Run ruff (Python linter) once without installation
uvx ruff check .

# Equivalent longer form
uv tool run ruff check .

# Install a tool permanently for repeated use
uv tool install ruff

# Then run the installed tool
ruff check .
```

## Instructions

### Step 1: Understand the Tool Management Landscape

uv replaces `pipx` for tool management. There are three main approaches:

**uvx (temporary execution)**: Run a tool once without installation
- Tool is fetched, cached, and executed in an isolated environment
- No modification to your system
- Ideal for: occasional use, trying tools, CI/CD where tools aren't needed repeatedly

**uv tool install (persistent installation)**: Install a tool for repeated use
- Tool is installed globally in a dedicated environment
- Available in PATH after installation
- Ideal for: tools you use regularly (linters, formatters, test runners)

**uv run (project environment)**: Run tools that need access to your project
- Tools run within your project's virtual environment
- Can access your project's installed packages
- Ideal for: testing, linting, formatting your project code

### Step 2: Choose Between uvx and uv tool install

**Use `uvx` (ephemeral) when:**
- Running a tool for the first time to test it
- Tool is used rarely or on-demand
- You want no installation footprint
- Running in CI/CD pipelines (cleaner, no persistent state)
- Tool has conflicting dependencies with other tools

```bash
# Try a new tool without committing to it
uvx httpie https://api.github.com/users/github

# Run a tool on-demand in CI
uvx mypy src/

# Run tool from different package
uvx --from httpie http https://example.com
```

**Use `uv tool install` (persistent) when:**
- Tool is part of your regular workflow
- Team uses it consistently (document in README)
- Tool provides utility functions beyond single invocation
- You want faster execution (no download overhead each time)
- Tool is referenced in project docs or scripts

```bash
# Install tools you use daily
uv tool install ruff
uv tool install black
uv tool install mypy

# Then run directly without prefix
ruff check .
black --check src/
mypy src/
```

**Use `uv run` (project environment) when:**
- Running tests, linters, or formatters on your project
- Tool needs access to project dependencies
- Running from within project directory
- Tool is listed in project's dev dependencies

```bash
# Test runner needs access to project (test libraries, modules)
uv run pytest tests/

# Linter running on project code
uv run mypy src/

# Format project code
uv run black src/
```

### Step 3: Run Tools with uvx

**Basic execution without arguments:**
```bash
uvx ruff check .
uvx black --check src/
```

**Specify exact version:**
```bash
# Run specific version of a tool
uvx ruff@0.3.0 check .

# Use version constraint
uvx --from 'ruff>=0.3.0,<0.4.0' ruff check .
```

**Run tools from different packages:**
```bash
# httpie is in package 'httpie', command is 'http'
uvx --from httpie http https://api.github.com

# mkdocs is in 'mkdocs', command is 'mkdocs'
uvx mkdocs serve
```

**Include optional dependencies (extras):**
```bash
# mypy with optional faster caching
uvx --from 'mypy[faster-cache]' mypy src/

# mkdocs with material theme
uvx --with mkdocs-material mkdocs serve
```

**Run with specific Python version:**
```bash
# Run tool with Python 3.10 (useful for compatibility testing)
uvx --python 3.10 ruff check .

# Ensure tool runs on minimum supported version
uvx --python 3.9 pytest tests/
```

**Run from git repository:**
```bash
# Install directly from GitHub
uvx --from git+https://github.com/httpie/cli httpie
```

### Step 4: Install and Manage Persistent Tools

**Install tools:**
```bash
# Install latest version
uv tool install ruff

# Install specific version
uv tool install ruff@0.3.0

# Install with extras
uv tool install 'mypy[faster-cache]'

# Install from git
uv tool install git+https://github.com/user/tool
```

**List installed tools:**
```bash
uv tool list

# Example output:
# black           0.23.11  /Users/user/.local/bin/black
# mypy            1.7.0    /Users/user/.local/bin/mypy
# ruff            0.3.0    /Users/user/.local/bin/ruff
```

**Upgrade tools:**
```bash
# Upgrade specific tool to latest
uv tool upgrade ruff

# Upgrade all tools
uv tool upgrade --all

# Upgrade to specific version
uv tool upgrade ruff@0.4.0
```

**Uninstall tools:**
```bash
# Remove installed tool
uv tool uninstall ruff

# Remove multiple tools
uv tool uninstall ruff black mypy
```

### Step 5: Understand Tool vs Project Dependencies

**Critical distinction for your workflow:**

```toml
# pyproject.toml

[project]
# Main project dependencies - needed to run your application
dependencies = [
    "fastapi>=0.104.0",
    "httpx>=0.27.0",
]

[project.optional-dependencies]
# Optional features for your application (not development tools)
aws = ["boto3>=1.34.0"]
database = ["sqlalchemy>=2.0.0"]

[dependency-groups]
# Development tools - only needed while developing
test = [
    "pytest>=8.0.0",
    "pytest-cov>=4.1.0",
]
lint = [
    "ruff>=0.1.0",
    "mypy>=1.7.0",
]
format = [
    "black>=23.11.0",
]
```

**Decision matrix:**

| Use Case | Tool | Command | Where |
|----------|------|---------|-------|
| Try a new linter | uvx | `uvx flake8 .` | Any directory |
| Lint project code regularly | uv run | `uv run ruff check .` | Project directory |
| Lint tool used across projects | uv tool install | `ruff check .` | Any directory |
| Test code | uv run | `uv run pytest` | Project directory |
| Build documentation | uv tool install | `uv tool install mkdocs` | Global install |
| One-time script execution | uvx | `uvx httpie` | Any directory |
| Format code | uv run | `uv run black src/` | Project directory |

### Step 6: Manage Tool Versions and Upgrades

**Check installed version:**
```bash
# Show version of installed tool
ruff --version

# Or via uv
uv tool list | grep ruff
```

**Upgrade specific tool:**
```bash
# Upgrade to latest
uv tool upgrade ruff

# Keep all tools up to date
uv tool upgrade --all
```

**Pin tool version:**
```bash
# Use specific version (best practice for team consistency)
uv tool install ruff@0.3.0

# Override installed version
uv tool install ruff@0.4.0
```

**Clean up old tools:**
```bash
# Uninstall unused tools
uv tool uninstall old-tool

# Check what's installed
uv tool list

# Free up disk space
uv cache prune
```

### Step 7: Handle Tool Dependencies and Conflicts

**Tools with conflicting dependencies:**
```bash
# These tools both depend on different versions of a library
# uvx creates isolated environments, avoiding conflicts
uvx tool-a
uvx tool-b

# Both run in separate, isolated environments
# No dependency conflicts
```

**Tools requiring additional packages:**
```bash
# Add extra packages to tool execution
uvx --with mkdocs-material mkdocs serve

# Tool runs with mkdocs + mkdocs-material installed
```

**Specific Python version for tool:**
```bash
# Some tools require specific Python versions
# Ensure compatibility
uvx --python 3.9 older-tool

# Run with minimum supported Python
uvx --python 3.10 modern-tool
```

## Examples

### Example 1: One-Time Tool Usage (uvx)

You need to check code quality but don't use ruff regularly:

```bash
# Run ruff once to check your code
uvx ruff check .

# Output analysis but don't install anything
# After execution, no system changes
# Next time you run it, it's fetched again (but cached locally)
```

### Example 2: Regular Linting in Project (uv run)

Your project uses ruff as a dev dependency:

```bash
# In your project directory
cd my-project

# Edit pyproject.toml to add ruff to dev dependencies
# [dependency-groups]
# lint = ["ruff>=0.1.0"]

# Sync environment
uv sync --group lint

# Run linter from project environment
uv run ruff check .

# Everyone on team uses same ruff version (from uv.lock)
```

### Example 3: Global Tool Installation (uv tool install)

You use ruff across multiple projects:

```bash
# Install once globally
uv tool install ruff

# Use in any directory
cd project-a && ruff check .
cd ../project-b && ruff check .

# No project setup needed
# Tool always available in PATH
```

### Example 4: Test Different Python Versions

You need to verify code works on Python 3.10 and 3.12:

```bash
# Run with Python 3.10
uvx --python 3.10 pytest tests/

# Run with Python 3.12
uvx --python 3.12 pytest tests/

# Each uses different Python version
# No installation overhead
```

### Example 5: Tool with Extras

mypy runs faster with optional faster-cache feature:

```bash
# Via uvx (temporary)
uvx --from 'mypy[faster-cache]' mypy src/

# Via uv tool install (persistent)
uv tool install 'mypy[faster-cache]'
mypy src/
```

### Example 6: CI/CD Pipeline

Your CI uses different tools without installation:

```bash
# .github/workflows/ci.yml
- name: Lint code
  run: uvx ruff check .

- name: Type check
  run: uvx mypy src/

- name: Format check
  run: uvx black --check .

- name: Test
  run: |
    uv sync --group test
    uv run pytest tests/
```

Each step is clean, isolated, no tool installation overhead.

### Example 7: Cleanup and Maintenance

Remove old tools and free disk space:

```bash
# See what's installed
uv tool list

# Remove tool you no longer use
uv tool uninstall old-formatter

# Prune cache of unused packages
uv cache prune

# Check cache location and size
uv cache dir
```

## Requirements

- uv installed (install via: `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- Python 3.8+ available (for running tools)
- Understanding of your project's dependency structure

## See Also

- [references/tool-comparison.md](./references/tool-comparison.md) - Detailed comparison of uvx vs uv tool vs uv run
- [references/common-workflows.md](./references/common-workflows.md) - Copy-paste ready tool usage patterns
- [examples/tool-scenarios.md](./examples/tool-scenarios.md) - Real-world tool management examples
- [uv Documentation](https://docs.astral.sh/uv/tools/) - Official tool management guide
