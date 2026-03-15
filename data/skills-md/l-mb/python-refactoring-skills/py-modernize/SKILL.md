---
name: py-modernize
description: Modernize Python codebases - migrate pip to uv, upgrade syntax to Python 3.13+, replace deprecated patterns, and update tooling to current best practices.
status: stable
---

# Python Codebase Modernization

Upgrade Python projects to use modern tooling, syntax, and patterns following Engineering Charter principles.

## Objectives

1. Migrate from pip to uv for faster dependency management
2. Upgrade Python syntax to 3.13+ modern patterns
3. Replace deprecated APIs and patterns
4. Update tooling to current best practices
5. Ensure pyproject.toml is the single source of configuration

## Required Tools

**Install uv globally** (via package manager): `sudo zypper install uv` or `pip install --user uv`
**Add to `[dependency-groups]` dev**: `"pyupgrade"`, `"ruff"`

- **uv**: Fast package installer (pip replacement)
- **pyupgrade**: Auto-upgrade syntax to newer Python
- **ruff**: Modern linter with UP rules

**Permissions**: Run py-quality-setup first to configure `.claude/settings.local.json` with all needed tool permissions.

## Package Manager: pip → uv

### Why uv?

- **10-100x faster** than pip
- Better dependency resolution
- Improved caching
- Compatible with pip (drop-in replacement)
- Actively developed by Astral (same team as ruff)

### Migration Workflow

```bash
# 1. Verify current setup
cat requirements.txt setup.py setup.cfg pyproject.toml

# 2. Install uv globally (not recommended, ask user to install via package manager)
# curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Replace venv creation
# OLD: python -m venv venv
uv venv

# 4. Replace pip install
# OLD: pip install -e ".[dev]"
uv pip install -e ".[dev]"

# 5. Replace pip install from requirements.txt
# OLD: pip install -r requirements.txt
uv pip install -r requirements.txt

# 6. Compile requirements (faster dependency resolution)
uv pip compile pyproject.toml -o requirements.txt

# 7. Sync environment (install exactly what's in requirements.txt)
uv pip sync requirements.txt
```

### Update CI/CD

```yaml
# .github/workflows/test.yml

# BEFORE
- name: Install dependencies
  run: |
    python -m venv venv
    source venv/bin/activate
    pip install -e ".[dev]"

# AFTER
- name: Install uv
  uses: astral-sh/setup-uv@v1

- name: Install dependencies
  run: |
    uv venv
    source .venv/bin/activate
    uv pip install -e ".[dev]"
```

### Update Documentation

Update README.md:

```markdown
<!-- BEFORE -->
## Development Setup

python -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

<!-- AFTER -->
## Development Setup

# Install uv if not already installed (via package manager preferred)
# sudo zypper install uv  # openSUSE
# or: pip install --user uv

uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

## Python Syntax Modernization

### Target Version

Set target in pyproject.toml:

```toml
[project]
requires-python = ">=3.13"

[tool.pyupgrade]
target-version = "py313"

[tool.ruff]
target-version = "py313"

[tool.ruff.lint]
select = ["UP"]  # Enable pyupgrade rules
```

### Run Syntax Upgrades

```bash
# Using pyupgrade directly (modifies files in-place)
pyupgrade --py313-plus **/*.py

# Using ruff (shows what would change)
ruff check . --select UP
ruff check . --select UP --fix  # Apply fixes

# Verify changes
git diff

# Run tests to ensure functionality preserved
pytest
```

### Common Modernizations

Run `pyupgrade --py313-plus .` or `ruff check . --select UP` to auto-upgrade:

- **Type hints**: `List[str]` → `list[str]`, `Optional[int]` → `int | None`
- **Remove `__future__`**: imports (built-in 3.11+)
- **String formatting**: `%` or `.format()` → f-strings
- **Type unions**: `Union[int, str]` → `int | str`
- **Walrus operator**: `if x := func():` (reduce temp variables)
- **Match statements**: Replace long if/elif chains (3.10+)
- **Pathlib**: Replace `os.path` with `Path` objects
- **Dataclasses**: Replace manual `__init__` with `@dataclass`


## Configuration Modernization

Consolidate setup.py/setup.cfg/requirements.txt → pyproject.toml.

**Note**: For complete pyproject.toml configuration including ruff, mypy, and basedpyright, see **py-quality-setup**.

Basic structure:

```toml
[project]
name = "myproject"
version = "1.0.0"
requires-python = ">=3.13"
dependencies = ["requests", "pydantic"]

[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"
```

After: `rm setup.py setup.cfg; uv pip install -e .; pytest`

## Deprecated Pattern Updates

Common deprecations to fix:

- `collections.Iterable` → `collections.abc.Iterable` (deprecated 3.3, removed 3.10)
- `datetime.utcnow()` → `datetime.now(UTC)` (deprecated 3.12)
- `datetime.utcfromtimestamp()` → `datetime.fromtimestamp(ts, UTC)` (deprecated 3.12)
- `imp` module → `importlib` (removed 3.12)
- `typing.List`, `typing.Dict` → `list`, `dict` (3.9+)
- `typing.Optional[X]` → `X | None` (3.10+)
- `typing.Union[X, Y]` → `X | Y` (3.10+)

Search for deprecated patterns:
```bash
# Find deprecated datetime usage
grep -rn "datetime.utcnow\|datetime.utcfromtimestamp" --include="*.py" .

# Find old typing imports
grep -rn "from typing import.*List\|from typing import.*Dict\|from typing import.*Optional" --include="*.py" .

# Find old collections imports
grep -rn "from collections import.*Callable\|from collections import.*Iterable" --include="*.py" .
```

## Verification Checklist

- [ ] `uv` is used for venv creation and package installation
- [ ] `pyproject.toml` is the single configuration source (no setup.py/setup.cfg)
- [ ] `requires-python = ">=3.13"` is set in pyproject.toml
- [ ] `ruff check . --select UP` reports no issues (or only accepted exceptions)
- [ ] No deprecated `datetime.utcnow()` or `datetime.utcfromtimestamp()` usage
- [ ] No old-style typing imports (`List`, `Dict`, `Optional`, `Union`)
- [ ] CI/CD updated to use uv
- [ ] README.md reflects uv-based setup instructions
- [ ] All tests pass after modernization

## Examples

**Example: Migrate pip to uv**
```
1. Check current setup:
   - ls -la | grep -E "setup.py|requirements.txt|pyproject.toml"
   - cat pyproject.toml

2. Install uv (if not already installed):
   - Via package manager: sudo zypper install uv  # openSUSE
   - Or as user package: pip install --user uv

3. Test uv with current project:
   - uv venv
   - source .venv/bin/activate
   - uv pip install -e ".[dev]"
   - pytest (verify all tests pass)

4. Update CI/CD:
   - Edit .github/workflows/test.yml
   - Replace pip commands with uv

5. Update README:
   - Replace pip instructions with uv

6. Commit: "Migrate from pip to uv for dependency management"
```

**Example: Modernize syntax to Python 3.13**
```
1. Update pyproject.toml:
   [project]
   requires-python = ">=3.13"

2. Run pyupgrade:
   pyupgrade --py313-plus **/*.py

3. Review changes:
   git diff
   # Check: List[X] → list[X], Union[X, Y] → X | Y, etc.

4. Run ruff for additional upgrades:
   ruff check . --select UP --fix

5. Verify type checking still works:
   mypy .
   basedpyright .

6. Run tests:
   pytest

7. Commit: "Modernize syntax to Python 3.13+"
```

**Example: Complete modernization**
```
1. Migrate to uv (see Example 1)

2. Consolidate configuration:
   - Read setup.py and setup.cfg
   - Migrate all config to pyproject.toml
   - Remove setup.py and setup.cfg
   - Verify: uv pip install -e ".[dev]"

3. Modernize syntax (see Example 2)

4. Update deprecated APIs:
   - grep -r "from collections import.*Iterable" .
   - Replace with collections.abc
   - grep -r "datetime.utcnow" .
   - Replace with datetime.now(UTC)

5. Final validation:
   - ruff check . --select UP (clean)
   - pytest (all pass)
   - mypy . && basedpyright . (no errors)

6. Update documentation:
   - README reflects uv usage
   - CONTRIBUTING.md updated

7. Commit: "Modernize codebase: uv, Python 3.13 syntax, pyproject.toml"
```

## Related Skills

- **Prerequisites**: py-quality-setup (tool configuration), py-test-quality (safety net before syntax changes)
- **Enforcement**: py-git-hooks (enforce modern syntax via ruff UP rules)
- **See also**: py-complexity (modernization often enables simplification)
