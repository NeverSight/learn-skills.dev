---
name: quality-run-linting-formatting
description: |
  Runs ruff linting and formatting with configuration details and common fixes. Use when checking code style, formatting files, fixing lint violations, or before commits. Explains ruff check vs ruff format, --fix flag, configuration in pyproject.toml, and common violation patterns. Works with Python .py files, targets Python 3.12.
allowed-tools:
  - Bash
  - Read
---

# Run Linting and Formatting Workflow

## Table of Contents

**Quick Start** → [Purpose](#purpose) | [When to Use](#when-to-use) | [Quick Start](#quick-start)

**Core Operations** → [Run Linting](#step-1-run-linting-ruff-check) | [Auto-Fix](#step-2-auto-fix-violations) | [Formatting](#step-3-run-formatting-ruff-format)

**Configuration** → [Ruff Config](#step-4-understand-ruff-configuration) | [Violation Codes](#step-5-common-violation-codes) | [Common Fixes](#fixing-common-violations)

**Workflows** → [Common Workflows](#common-workflows) | [Output Interpretation](#interpreting-lint-output) | [Integration](#integration-with-other-skills)

**Help** → [Troubleshooting](#troubleshooting) | [Requirements](#requirements)

---

## Purpose

Master ruff usage for linting (code quality) and formatting (code style) in temet. Understand when to check vs format, how to auto-fix violations, and interpret common error codes.

## When to Use

**Use this skill when:**
- Running code quality checks before commits
- Fixing linting violations
- Formatting code to match project standards
- Understanding ruff error codes (F401, E501, etc.)
- Configuring ruff for project-specific rules

**User trigger phrases:**
- "run linting"
- "format code"
- "fix lint errors"
- "ruff check"
- "what does E501 mean?"

## Quick Start

**Most common workflows:**

```bash
# Check for lint violations (don't modify files)
ruff check src/ tests/

# Auto-fix violations (safe fixes only)
ruff check src/ tests/ --fix

# Format code (modifies files)
ruff format src/ tests/

# Check formatting without modifying
ruff format src/ tests/ --check

# Full workflow (lint + format)
ruff check src/ tests/ --fix && ruff format src/ tests/
```

---

## Instructions

### Understanding Ruff vs Other Tools

**Ruff replaces multiple tools:**

| Tool | What It Did | Ruff Equivalent |
|------|-------------|-----------------|
| `black` | Code formatting | `ruff format` |
| `isort` | Import sorting | `ruff check --select I` |
| `flake8` | Linting | `ruff check` |
| `pylint` | Linting | `ruff check` |
| `pyupgrade` | Python version upgrades | `ruff check --select UP` |
| `autoflake` | Remove unused imports | `ruff check --select F401 --fix` |

**Why ruff:**
- ⚡ **10-100x faster** than other tools (written in Rust)
- 🎯 **One tool** replaces 5-6 tools
- 🔧 **Auto-fix** for most violations
- 📝 **Configurable** (select/ignore rules)

---

### Step 1: Run Linting (ruff check)

**Basic usage:**
```bash
ruff check src/ tests/
```

**Output (success):**
```
All checks passed!
```

**Output (with violations):**
```
src/temet/core/event_bus.py:15:1: F401 [*] `logging` imported but unused
src/temet/core/event_bus.py:42:80: E501 Line too long (102 > 100)
src/temet/plugins/hooks/session_start/plugin.py:23:5: B008 Do not perform function call `dict` in argument defaults
Found 3 errors.
[*] 1 fixable with the `--fix` option.
```

**Understanding output:**
- **File:line:col** - Location of violation
- **Code** - Error code (e.g., F401, E501, B008)
- **[*]** - Fixable with --fix
- **Message** - Description of violation

---

### Step 2: Auto-Fix Violations

**Safe auto-fix (recommended):**
```bash
ruff check src/ tests/ --fix
```

**What gets fixed:**
- ✅ Unused imports removed
- ✅ Imports sorted (isort-compatible)
- ✅ Unnecessary parentheses removed
- ✅ Quoted strings normalized
- ✅ Whitespace issues fixed
- ⚠️ Does NOT fix: Complex violations requiring manual intervention

**Check what would be fixed (dry-run):**
```bash
ruff check src/ tests/ --fix --diff
```

**Unsafe fixes (use with caution):**
```bash
ruff check src/ tests/ --fix --unsafe-fixes
```

**When to use:**
- `--fix`: Before every commit (auto-fix safe issues)
- `--fix --diff`: Preview changes before applying
- `--unsafe-fixes`: Only when you understand the changes

---

### Step 3: Run Formatting (ruff format)

**Format files in-place:**
```bash
ruff format src/ tests/
```

**Output:**
```
3 files reformatted, 244 files left unchanged
```

**Check formatting without modifying:**
```bash
ruff format src/ tests/ --check
```

**Output (violations):**
```
Would reformat: src/temet/core/event_bus.py
Would reformat: src/temet/plugins/hooks/session_start/plugin.py
2 files would be reformatted, 245 files left unchanged
```

**See what would change (dry-run):**
```bash
ruff format src/ tests/ --diff
```

**When to use:**
- `ruff format`: Before commits (format all code)
- `ruff format --check`: In CI/CD (verify formatting)
- `ruff format --diff`: Review formatting changes

---

### Step 4: Understand Ruff Configuration

**temet ruff configuration** (`pyproject.toml`):

```toml
[tool.ruff]
line-length = 100  # Max line length
target-version = "py312"  # Python 3.12

[tool.ruff.lint]
select = ["ALL"]  # Enable ALL rules by default
ignore = [
    "D",        # pydocstyle (docstrings not enforced)
    "COM812",   # Trailing comma (conflicts with formatter)
    "ISC001",   # Single-line implicit concat (conflicts with formatter)
    "T201",     # print() allowed (CLI tool needs print)
    "BLE001",   # Catching Exception allowed (plugin error handling)
    "ARG001",   # Unused function args (test fixtures, protocols)
    "ARG002",   # Unused method args (test fixtures, protocols)
]

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = [
    "S101",     # assert allowed in tests
    "ANN",      # Type annotations optional in tests
]

[tool.ruff.format]
quote-style = "double"  # Use " not '
indent-style = "space"  # 4 spaces (not tabs)
```

**Key rules:**
- **Line length:** 100 characters (not 80)
- **Target:** Python 3.12 (uses modern syntax)
- **Quotes:** Double quotes preferred
- **Indentation:** 4 spaces

---

### Step 5: Common Violation Codes

**Import-related (F):**

| Code | Description | Fix |
|------|-------------|-----|
| F401 | Imported but unused | `ruff check --fix` removes |
| F403 | `from module import *` | Specify imports explicitly |
| F811 | Redefined unused variable | Rename or remove duplicate |

**Code style (E/W):**

| Code | Description | Fix |
|------|-------------|-----|
| E501 | Line too long (> 100) | Break line or shorten |
| E711 | Comparison to None should be `is` | Use `is None` |
| W291 | Trailing whitespace | `ruff check --fix` removes |

**Best practices (B):**

| Code | Description | Fix |
|------|-------------|-----|
| B008 | Function call in argument defaults | Use `default_factory` or None |
| B006 | Mutable default argument | Use `None` and create in function |
| B011 | `assert False` instead of `raise` | Use `raise AssertionError` |

**Type checking (ANN):**

| Code | Description | Fix |
|------|-------------|-----|
| ANN001 | Missing type annotation (arg) | Add type annotation |
| ANN201 | Missing return type | Add `-> ReturnType` |
| ANN401 | `Any` type (too vague) | Use specific type |

**See:** [Ruff rule reference](https://docs.astral.sh/ruff/rules/) for complete list

---

## Common Workflows

### Workflow 1: Pre-Commit (Fix + Format)

```bash
# Fix lint violations + format code
ruff check src/ tests/ --fix && ruff format src/ tests/

# Verify no violations remain
ruff check src/ tests/
ruff format src/ tests/ --check
```

**Time:** 1-2 seconds

---

### Workflow 2: Development (Check Only)

```bash
# Check for violations (don't modify files)
ruff check src/ tests/

# If violations: Fix manually or use --fix
```

**Time:** < 1 second

---

### Workflow 3: CI/CD (Verify Only)

```bash
# In CI pipeline: Verify linting and formatting
ruff check src/ tests/
ruff format src/ tests/ --check

# If violations: Fail CI (developer must fix locally)
```

**Time:** < 1 second (fast feedback)

---

### Workflow 4: Format on Save (IDE Integration)

**VSCode settings.json:**
```json
{
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.organizeImports": true,
      "source.fixAll": true
    }
  }
}
```

**Result:** Auto-fix + format on every file save

---

## Interpreting Lint Output

### Example Output

```
src/temet/core/event_bus.py:15:1: F401 [*] `logging` imported but unused
src/temet/core/event_bus.py:42:80: E501 Line too long (102 > 100)
src/temet/core/event_bus.py:67:5: B006 [*] Do not use mutable data structures for argument defaults
src/temet/plugins/hooks/session_start/plugin.py:23:10: ANN001 Missing type annotation for function argument `event`
Found 4 errors.
[*] 2 fixable with the `--fix` option.
```

**Breakdown:**
1. **F401** - Unused import (fixable) → `ruff check --fix`
2. **E501** - Line too long → Break line manually
3. **B006** - Mutable default (fixable) → `ruff check --fix`
4. **ANN001** - Missing annotation → Add type manually

**Action plan:**
```bash
# 1. Auto-fix what's possible
ruff check src/ tests/ --fix

# 2. Manually fix remaining issues
# - E501: Break long line
# - ANN001: Add type annotation

# 3. Verify all fixed
ruff check src/ tests/
```

---

## Fixing Common Violations

### Violation 1: F401 - Unused Import

**Error:**
```
src/temet/core/event_bus.py:15:1: F401 [*] `logging` imported but unused
```

**Fix (auto):**
```bash
ruff check src/ tests/ --fix
```

**Or manually:**
```python
# ❌ Before
import logging  # Unused
from typing import Any

# ✅ After
from typing import Any  # Removed unused import
```

---

### Violation 2: E501 - Line Too Long

**Error:**
```
src/temet/core/event_bus.py:42:80: E501 Line too long (102 > 100)
```

**Fix (manual):**
```python
# ❌ Before (102 characters)
def process_event(event: Event, handlers: list[Callable], config: dict[str, Any]) -> dict[str, Any]:

# ✅ After (break line)
def process_event(
    event: Event,
    handlers: list[Callable],
    config: dict[str, Any],
) -> dict[str, Any]:
```

---

### Violation 3: B006 - Mutable Default Argument

**Error:**
```
src/temet/core/event_bus.py:67:5: B006 [*] Do not use mutable data structures for argument defaults
```

**Fix (auto or manual):**
```python
# ❌ Before (dangerous - shared mutable default)
def process(data: dict[str, Any] = {}):
    data["key"] = "value"  # Modifies shared default!

# ✅ After (safe - create new dict each call)
def process(data: dict[str, Any] | None = None):
    if data is None:
        data = {}
    data["key"] = "value"
```

---

### Violation 4: ANN001 - Missing Type Annotation

**Error:**
```
src/temet/plugins/hooks/session_start/plugin.py:23:10: ANN001 Missing type annotation for function argument `event`
```

**Fix (manual):**
```python
# ❌ Before
def handle(self, event):
    return event.data

# ✅ After
def handle(self, event: Event) -> dict[str, Any]:
    return event.data
```

---

## Integration with Other Skills

**Before linting:**
- `setup-temet-project` - Ensure ruff installed
- `run-type-checking-workflow` - Fix type errors first (easier to lint)

**After linting:**
- `run-quality-gates` - Run all gates (includes ruff)
- `git-commit-push` - Lint passes as pre-commit requirement

**During development:**
- `interpret-check-all-output` - Understand check_all.sh results (includes ruff)

---

## Troubleshooting

### Issue: `ruff: command not found`

**Solution:**
```bash
# Use uv run prefix
uv run ruff check src/ tests/

# Or ensure ruff installed
uv pip install -e ".[dev]"
```

---

### Issue: Too many violations to fix manually

**Solution:**
```bash
# Auto-fix everything possible
ruff check src/ tests/ --fix

# Then fix remaining violations one file at a time
ruff check src/temet/core/event_bus.py --fix
```

---

### Issue: Conflict between ruff and pyright

**Symptoms:** Ruff suggests one fix, pyright suggests another

**Solution:**
```bash
# 1. Fix pyright errors first (type safety)
pyright src/ tests/

# 2. Then run ruff (code style)
ruff check src/ tests/ --fix
```

**Rationale:** Type safety > code style. Fix types first, style second.

---

### Issue: `--fix` breaks code

**Symptoms:** Auto-fix changes behavior or introduces bugs

**Solution:**
```bash
# 1. Review changes before applying
ruff check src/ tests/ --fix --diff

# 2. If looks wrong, skip auto-fix
# 3. Fix manually with understanding

# 4. If auto-fix is wrong, report bug to ruff
# (Rare - ruff is well-tested)
```

---

### Issue: Want to ignore specific violation

**Solution (per-line ignore):**
```python
# Ignore specific rule on one line
result = some_call()  # noqa: E501
```

**Solution (file-level ignore):**
```toml
# In pyproject.toml
[tool.ruff.lint.per-file-ignores]
"src/temet/legacy/*.py" = ["E501", "F401"]  # Ignore in legacy code
```

**Rule:** Only ignore with justification comment:
```python
# noqa: E501 - API URL cannot be broken
api_url = "https://very-long-api-url.example.com/v1/endpoint/with/many/parameters"
```

---

## Requirements

**Dependencies (auto-installed with `[dev]`):**
- `ruff` - Linter and formatter

**Configuration files:**
- `pyproject.toml` - Ruff configuration (required)
- `.vscode/settings.json` - IDE integration (optional)

**No manual installation needed** - included in `pyproject.toml`.

---

## Expected Output

### Success (No Violations)

```bash
$ ruff check src/ tests/
All checks passed!

$ ruff format src/ tests/ --check
247 files already formatted
```

**✅ Ready to commit**

---

### Violations Found

```bash
$ ruff check src/ tests/
src/temet/core/event_bus.py:15:1: F401 [*] `logging` imported but unused
src/temet/core/event_bus.py:42:80: E501 Line too long (102 > 100)
Found 2 errors.
[*] 1 fixable with the `--fix` option.

$ ruff format src/ tests/ --check
Would reformat: src/temet/core/event_bus.py
1 file would be reformatted, 246 files left unchanged
```

**🔧 Fix with:**
```bash
ruff check src/ tests/ --fix && ruff format src/ tests/
```

