---
name: quality-run-type-checking
description: |
  Runs dual type checking with pyright (fast, development) and mypy (thorough, CI/CD). Use when checking types, before commits, debugging type errors, or validating type annotations. Explains why both tools required, configuration differences, and when to use each. Works with Python .py files, pyproject.toml, strict mode enabled.
allowed-tools:
  - Bash
  - Read
---

# Run Type Checking Workflow

## Table of Contents

**Quick Start** → [Purpose](#purpose) | [When to Use](#when-to-use) | [Why Dual Checking](#why-dual-type-checking) | [Quick Start](#quick-start)

**Operations** → [Run Pyright](#step-1-run-pyright-fast-development-feedback) | [Run Mypy](#step-2-run-mypy-thorough-pre-commit-check) | [Configuration](#step-3-understand-configuration-differences)

**Error Handling** → [Interpret Errors](#step-4-interpret-type-errors) | [Fix Systematically](#step-5-fix-type-errors-systematically) | [Common Fixes](#common-workflows)

**Help** → [Integration](#integration-with-other-skills) | [Troubleshooting](#troubleshooting) | [Requirements](#requirements)

---

## Purpose

Understand and execute temet's dual type checking strategy using both pyright (fast iteration) and mypy (comprehensive validation). Learn when to use each tool, how to interpret errors, and why both are required.

## When to Use

**Use this skill when:**
- Running type checks during development (pyright for fast feedback)
- Pre-commit validation (both pyright and mypy)
- Debugging type errors
- Understanding why both type checkers are required
- Configuring type checking in pyproject.toml

**User trigger phrases:**
- "run type checking"
- "check types"
- "pyright errors"
- "mypy failing"
- "fix type errors"

## Quick Start

**Daily development (fast feedback):**
```bash
pyright src/ tests/
# or with uv run prefix
uv run pyright src/ tests/
```

**Pre-commit validation (thorough check):**
```bash
# Run both type checkers (required before commit)
pyright src/ tests/ && mypy src/ tests/
```

**Full quality gates (includes both):**
```bash
./scripts/check_all.sh
```

---

## Why Dual Type Checking?

temet requires **BOTH** pyright and mypy because they complement each other:

| Aspect | Pyright | Mypy | Why Both? |
|--------|---------|------|-----------|
| **Speed** | ⚡ Fast (< 2s) | 🐌 Slower (3-5s) | Fast feedback + thorough validation |
| **Editor integration** | ✅ Excellent (VSCode/Pylance) | ⚠️ Limited | Real-time feedback in IDE |
| **Error detection** | ✅ Strict mode, modern Python | ✅ Mature, comprehensive | Catch different error classes |
| **Pydantic support** | ⚠️ Basic | ✅ Plugin support | Model validation requires mypy |
| **Type narrowing** | ✅ Advanced | ✅ Good | Both handle `isinstance()` guards |
| **CI/CD** | ✅ Fast | ✅ Authoritative | Pyright for speed, mypy for final check |

**Bottom line:** Pyright catches 90% of issues in 2s (dev workflow). Mypy catches the remaining 10% in 5s (pre-commit/CI).

---

## Instructions

### Step 1: Run Pyright (Fast Development Feedback)

**Basic usage:**
```bash
pyright src/ tests/
```

**Output (success):**
```
Found 1247 source files
0 errors, 0 warnings, 0 informations
Completed in 1.8sec
```

**Output (with errors):**
```
/Users/dev/temet/src/temet/core/event_bus.py
  /Users/dev/temet/src/temet/core/event_bus.py:45:16 - error: Type "None" is not assignable to return type "dict[str, Any]"
    Expected type is "dict[str, Any]"
    Received type is "None" (reportGeneralTypeIssues)
  /Users/dev/temet/src/temet/plugins/hooks/session_start/plugin.py:67:21 - error: Argument of type "str | None" cannot be assigned to parameter of type "str" (reportArgumentType)

2 errors, 0 warnings, 0 informations
Completed in 1.9sec
```

**When to use:**
- After every code change (fast feedback)
- In IDE (automatic via Pylance extension)
- Quick validation before deeper work

**Typical workflow:**
```bash
# 1. Make code change
# 2. Run pyright
pyright src/ tests/

# 3. If errors: Fix immediately (fast iteration)
# 4. If pass: Continue development
```

---

### Step 2: Run Mypy (Thorough Pre-Commit Check)

**Basic usage:**
```bash
mypy src/ tests/
```

**Output (success):**
```
Success: no issues found in 247 source files
```

**Output (with errors):**
```
src/temet/plugins/hooks/session_start/plugin.py:67: error: Argument 1 to "process_workspace" has incompatible type "str | None"; expected "str"  [arg-type]
src/temet/core/event_bus.py:45: error: Incompatible return value type (got "None", expected "dict[str, Any]")  [return-value]
Found 2 errors in 2 files (checked 247 source files)
```

**When to use:**
- Before committing (part of quality gates)
- After major refactoring
- When pyright passes but unsure about Pydantic models
- In CI/CD pipeline (final validation)

**Typical workflow:**
```bash
# Before commit
./scripts/check_all.sh  # Includes mypy

# Or manually
pyright src/ tests/ && mypy src/ tests/
```

---

### Step 3: Understand Configuration Differences

**Pyright configuration** (`pyproject.toml`):
```toml
[tool.pyright]
include = ["src", "tests"]
exclude = [
    "**/__pycache__",
    "**/node_modules",
    ".venv",
]
typeCheckingMode = "strict"  # Strictest mode
reportMissingTypeStubs = false
pythonVersion = "3.12"
```

**Mypy configuration** (`pyproject.toml`):
```toml
[tool.mypy]
python_version = "3.12"
strict = true  # Enable all strict checks
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
plugins = ["pydantic.mypy"]  # Critical for Pydantic models

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false  # Relax for test files
```

**Key differences:**
1. **Pydantic plugin:** Mypy has it, pyright doesn't (Pydantic models validated by mypy)
2. **Strict mode:** Both use strict, but implement differently
3. **Speed:** Pyright optimized for speed, mypy for thoroughness
4. **Test files:** Mypy relaxes rules for tests (less boilerplate)

---

### Step 4: Interpret Type Errors

**Common error types and solutions:**

#### Error 1: `Type "None" is not assignable`

**Pyright:**
```
error: Type "None" is not assignable to return type "dict[str, Any]"
```

**Mypy:**
```
error: Incompatible return value type (got "None", expected "dict[str, Any]")
```

**Solution:**
```python
# ❌ Wrong
def handle(self, event: Event) -> dict[str, Any]:
    if event.type != "my_event":
        return None  # Error: None not allowed

# ✅ Correct (return type allows None)
def handle(self, event: Event) -> dict[str, Any] | None:
    if event.type != "my_event":
        return None  # OK

# ✅ Or fail-fast (always return dict)
def handle(self, event: Event) -> dict[str, Any]:
    if event.type != "my_event":
        return {}  # Return empty dict instead
```

---

#### Error 2: `Argument has incompatible type`

**Pyright:**
```
error: Argument of type "str | None" cannot be assigned to parameter of type "str"
```

**Mypy:**
```
error: Argument 1 to "process_workspace" has incompatible type "str | None"; expected "str"
```

**Solution:**
```python
# ❌ Wrong
workspace_path: str | None = get_workspace()
process_workspace(workspace_path)  # Error: might be None

# ✅ Correct (guard with None check)
workspace_path: str | None = get_workspace()
if workspace_path is not None:
    process_workspace(workspace_path)  # OK: narrowed to str

# ✅ Or with default
workspace_path = get_workspace() or "/default/path"
process_workspace(workspace_path)  # OK: always str
```

---

#### Error 3: `Untyped function definition`

**Mypy only:**
```
error: Function is missing a type annotation
```

**Solution:**
```python
# ❌ Wrong
def process_event(event):
    return event.data

# ✅ Correct (add type annotations)
def process_event(event: Event) -> dict[str, Any]:
    return event.data
```

---

#### Error 4: `Pydantic model validation`

**Mypy only (requires Pydantic plugin):**
```
error: "SessionWorkspace" has incompatible type
```

**Solution:**
```python
# Ensure Pydantic plugin enabled in pyproject.toml
[tool.mypy]
plugins = ["pydantic.mypy"]

# Then mypy validates Pydantic models correctly
class SessionWorkspace(BaseModel):
    date: str
    path: Path  # Validated by Pydantic plugin
```

---

### Step 5: Fix Type Errors Systematically

**Workflow:**
```bash
# 1. Run pyright (fast)
pyright src/ tests/

# 2. Fix pyright errors (most common issues)
# 3. Re-run pyright until clean

# 4. Run mypy (Pydantic + edge cases)
mypy src/ tests/

# 5. Fix mypy-specific errors
# 6. Re-run both to confirm

pyright src/ tests/ && mypy src/ tests/
```

**See also:** `debug-type-errors` skill for systematic error debugging

---

## Common Workflows

### Workflow 1: Development (Fast Iteration)

```bash
# After code change: Run pyright only
pyright src/ tests/

# If pass: Continue development
# If fail: Fix type errors, re-run
```

**Time:** 1-2 seconds

---

### Workflow 2: Pre-Commit (Full Validation)

```bash
# Before commit: Run both type checkers
pyright src/ tests/ && mypy src/ tests/

# If both pass: Ready to commit
# If either fails: Fix and re-run
```

**Time:** 4-6 seconds

---

### Workflow 3: CI/CD (Automated Validation)

```bash
# In CI pipeline: Run as part of check_all.sh
./scripts/check_all.sh

# Includes:
# - pyright (fast check)
# - mypy (thorough check)
# - other quality gates
```

**Time:** 8 seconds (all gates in parallel)

---

### Workflow 4: Pydantic Model Changes

```bash
# After modifying Pydantic models: Run mypy specifically
mypy src/ tests/

# Mypy's Pydantic plugin validates:
# - Field types
# - Default values
# - Validators
# - Config options
```

---

## Configuration

### Strict Mode (Required)

Both tools use strict mode to catch maximum errors:

**What strict mode enables:**
- No implicit `Any` types
- No untyped function definitions
- No untyped calls
- Enforce `Optional` handling
- Warn on unused ignores

**Example violations caught:**
```python
# ❌ Strict mode violations
def process(data):  # Error: Untyped function
    pass

result: dict = get_data()  # Error: Need dict[str, Any]

value = data.get("key")  # Error: Need type annotation
```

**Correct in strict mode:**
```python
# ✅ Strict mode compliant
def process(data: dict[str, Any]) -> None:
    pass

result: dict[str, Any] = get_data()

value: str | None = data.get("key")
```

---

### Type Stubs

**When type stubs missing:**
```
error: Library stubs not installed for "some_package"
hint: Try `python -m pip install types-some-package`
```

**Solution:**
```bash
# Install type stubs
uv pip install types-some-package

# Common stubs for temet
uv pip install types-pyyaml types-toml
```

---

## Integration with Other Skills

**Before type checking:**
- `setup-temet-project` - Ensure environment configured
- `run-linting-formatting-workflow` - Format code first (easier to read errors)

**After type errors:**
- `debug-type-errors` - Systematic type error debugging
- `create-value-object` - Use NamedTuple for type-safe returns

**During development:**
- `run-quality-gates` - Run all gates (includes both type checkers)
- `interpret-check-all-output` - Understand check_all.sh results

---

## Troubleshooting

### Issue: `pyright: command not found`

**Solution:**
```bash
# Use uv run prefix
uv run pyright src/ tests/

# Or ensure pyright installed
uv pip install -e ".[dev]"
```

---

### Issue: `mypy: command not found`

**Solution:**
```bash
# Use uv run prefix
uv run mypy src/ tests/

# Or ensure mypy installed
uv pip install -e ".[dev]"
```

---

### Issue: Pyright passes, mypy fails (Pydantic models)

**Symptoms:** Pyright shows no errors, but mypy reports Pydantic model issues

**Solution:**
```bash
# Ensure Pydantic plugin enabled
cat pyproject.toml | grep -A 5 "tool.mypy"
# Should show: plugins = ["pydantic.mypy"]

# If missing, add to pyproject.toml
[tool.mypy]
plugins = ["pydantic.mypy"]
```

---

### Issue: Type errors in test files

**Symptoms:** Mypy complains about untyped test functions

**Solution:**
```toml
# Relax mypy rules for tests in pyproject.toml
[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
```

**Rationale:** Test files benefit from less strict typing (less boilerplate, focus on test logic).

---

### Issue: Too many `type: ignore` comments

**Symptoms:** Code littered with `# type: ignore`

**Solution:**
```python
# ❌ Wrong (hiding real issues)
result = process_data()  # type: ignore

# ✅ Correct (fix the type error)
result: dict[str, Any] = process_data()

# ✅ Or narrow the ignore
result = process_data()  # type: ignore[return-value]
```

**Rule:** `# type: ignore` requires justification comment:
```python
# type: ignore[return-value]  # OK: External library has wrong type stubs
```

---

## Requirements

**Dependencies (auto-installed with `[dev]`):**
- `pyright` - Fast type checker (VSCode/Pylance backend)
- `mypy` - Thorough type checker (CI/CD standard)
- `pydantic` - Model validation (required for mypy plugin)

**Configuration files:**
- `pyproject.toml` - Both pyright and mypy configuration
- `.vscode/settings.json` - VSCode integration (optional)

**No manual installation needed** - included in `pyproject.toml`.

---

## Expected Output

### Both Passing (Success)

```bash
$ pyright src/ tests/
Found 1247 source files
0 errors, 0 warnings, 0 informations
Completed in 1.8sec

$ mypy src/ tests/
Success: no issues found in 247 source files
```

**✅ Ready to commit**

---

### Pyright Passing, Mypy Failing

```bash
$ pyright src/ tests/
Found 1247 source files
0 errors, 0 warnings, 0 informations
Completed in 1.8sec

$ mypy src/ tests/
src/temet/models/workspace.py:15: error: "Path" has no attribute "mkdir"
Found 1 error in 1 file (checked 247 source files)
```

**⚠️ Pydantic model issue - fix before commit**

---

### Both Failing

```bash
$ pyright src/ tests/
/Users/dev/temet/src/temet/core/event_bus.py:45:16 - error: Type "None" is not assignable to return type "dict[str, Any]"
1 error, 0 warnings, 0 informations
Completed in 1.9sec

$ mypy src/ tests/
src/temet/core/event_bus.py:45: error: Incompatible return value type (got "None", expected "dict[str, Any]")
Found 1 error in 1 file (checked 247 source files)
```

**❌ Fix type errors before committing**

---

