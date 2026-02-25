---
name: python-best-practices-type-safety
description: |
  Systematic resolution of pyright/mypy type errors with categorization and fix templates.
  Use when pyright fails, type errors are reported, adding type annotations, or enforcing
  type safety. Analyzes Python type errors, categorizes them (missing annotations, incorrect
  types, generic issues, Optional/None handling), and applies fix patterns. Works with .py
  files and pyright output.
allowed-tools:
  - Read
  - Grep
  - Bash
  - Edit
---

# Debug Type Errors

## Purpose
Systematically diagnose and resolve Python type checking errors from pyright/mypy by categorizing error types and applying proven fix patterns.


## When to Use This Skill

Use when fixing type errors with "fix pyright errors", "resolve type mismatch", "add type annotations", or "handle Optional types".

Do NOT use for pytest configuration (use `pytest-configuration`), import validation (use `python-best-practices-fail-fast-imports`), or runtime errors (type checking is static).
## When to Use

Use this skill when:
- Pyright or mypy reports type errors in CI/CD or local checks
- Adding type annotations to untyped code
- Refactoring code and need to maintain type safety
- Debugging "Type X cannot be assigned to Y" errors
- Fixing Optional/None handling issues
- Resolving generic type argument errors
- Converting code to strict type checking mode
- Before committing changes (as part of quality gates)

## Table of Contents

### Core Sections
- [Purpose](#purpose) - Systematic type error diagnosis and resolution
- [Quick Start](#quick-start) - Fastest way to fix type errors with automation
- [Instructions](#instructions) - Complete implementation guide
  - [Step 1: Run Type Checker and Capture Output](#step-1-run-type-checker-and-capture-output) - Pyright execution and error capture
  - [Step 2: Categorize Errors](#step-2-categorize-errors) - 6 error categories with patterns
  - [Step 3: Apply Fix Patterns](#step-3-apply-fix-patterns) - Category-specific fix templates
  - [Step 4: Use MultiEdit for Batch Fixes](#step-4-use-multiedit-for-batch-fixes) - Token-efficient batch fixes
  - [Step 5: Verify Fixes](#step-5-verify-fixes) - Post-fix validation
- [Examples](#examples) - Real-world error fixes
  - [Example 1: Missing Return Type Annotation](#example-1-missing-return-type-annotation)
  - [Example 2: Optional Parameter Handling](#example-2-optional-parameter-handling)
  - [Example 3: Generic Type Arguments](#example-3-generic-type-arguments)
- [Common Error Patterns](#common-error-patterns) - Quick reference table
- [Project-Specific Rules](#project-specific-rules) - Strict type checking rules
- [Requirements](#requirements) - Python 3.11+, pyright, pyrightconfig.json
- [Automation Scripts](#automation-scripts) - Parser, annotation fixer, Optional handler

### Supporting Resources
- [scripts/README.md](./scripts/README.md) - Automation scripts and workflows
- [references/reference.md](./references/reference.md) - Complete error pattern catalog
- [CLAUDE.md](../../../CLAUDE.md) - Project type safety rules
- [../apply-code-template/references/code-templates.md](../../docs/code-templates.md) - Type-safe code templates

### Python Scripts
- [Parse Pyright Errors](./scripts/parse_pyright_errors.py) - Categorize and analyze pyright type checking errors
- [Fix Missing Annotations](./scripts/fix_missing_annotations.py) - Automatically add type hints to Python files
- [Fix Optional Handling](./scripts/fix_optional_handling.py) - Add None checks for Optional types

## Quick Start

**Using Automation Scripts (Recommended):**
```bash
# Parse and categorize errors
uv run pyright src/ | python .claude/skills/debug-type-errors/scripts/parse_pyright_errors.py

# Auto-fix missing annotations
python .claude/skills/debug-type-errors/scripts/fix_missing_annotations.py src/file.py --all --dry-run

# Auto-fix Optional handling
python .claude/skills/debug-type-errors/scripts/fix_optional_handling.py src/file.py --dry-run
```

**Manual Analysis:**
```bash
# Run pyright and capture errors
uv run pyright src/ > type_errors.txt

# Analyze errors by category
grep "is not assignable" type_errors.txt
grep "Cannot access member" type_errors.txt
grep "is not defined" type_errors.txt

# Fix using MultiEdit for multiple errors in same file
```

**See:** [scripts/README.md](./scripts/README.md) for complete automation workflow.

## Instructions

### Step 1: Run Type Checker and Capture Output

Run pyright with verbose output to get detailed error information:

```bash
# Project-wide check
uv run pyright src/ --verbose > type_errors.txt

# Specific file check
uv run pyright src/path/to/file.py --verbose

# Check with stats
uv run pyright src/ --stats
```

**Key flags:**
- `--verbose` - Shows full error context
- `--stats` - Displays error count by category
- No flags - Standard output (recommended for parsing)

### Step 2: Categorize Errors

Parse pyright output and group errors by category:

**Category 1: Missing Type Annotations**
```
error: Type of "variable" is unknown
error: Return type of function is unknown
error: Parameter "param" type is unknown
```

**Category 2: Type Mismatch (Assignment)**
```
error: Argument of type "X" cannot be assigned to parameter "Y"
error: Expression of type "X" cannot be assigned to declared type "Y"
error: Type "X" is not assignable to type "Y"
```

**Category 3: Optional/None Handling**
```
error: "None" is not assignable to "X"
error: Argument of type "X | None" cannot be assigned to parameter "X"
error: Object of type "None" cannot be used as iterable value
```

**Category 4: Generic Type Errors**
```
error: Type argument "X" is missing
error: Expected 1 type argument
error: Type "X[Y]" is incompatible with "X[Z]"
```

**Category 5: Attribute/Method Errors**
```
error: Cannot access member "X" for type "Y"
error: "X" is not a known member of "Y"
```

**Category 6: Import/Module Errors**
```
error: Import "X" could not be resolved
error: Stub file not found for "X"
```

### Step 3: Apply Fix Patterns

Use category-specific fix patterns (see `references/reference.md` for detailed examples):

**Pattern 1: Add Type Annotations**
```python
# Before
def process_data(data):
    return data.strip()

# After
def process_data(data: str) -> str:
    return data.strip()
```

**Pattern 2: Fix Type Mismatches**
```python
# Before
result: ServiceResult[bool] = service.get_data()  # Returns ServiceResult[dict]

# After
result: ServiceResult[dict] = service.get_data()
```

**Pattern 3: Handle Optional Types**
```python
# Before
def get_value(config: Settings | None) -> str:
    return config.value  # Error: config might be None

# After
def get_value(config: Settings | None) -> str:
    if not config:
        raise ValueError("Config required")
    return config.value
```

**Pattern 4: Fix Generic Types**
```python
# Before
items: list = []  # Missing type argument

# After
items: list[str] = []
```

### Step 4: Use MultiEdit for Batch Fixes

When fixing multiple errors in the same file, ALWAYS use MultiEdit:

```python
# ❌ WRONG - Sequential edits (wastes tokens)
Edit("file.py", old1, new1)
Edit("file.py", old2, new2)

# ✅ CORRECT - Single MultiEdit operation
MultiEdit("file.py", [
    {"old_string": old1, "new_string": new1},
    {"old_string": old2, "new_string": new2}
])
```

### Step 5: Verify Fixes

After applying fixes, verify the changes:

```bash
# Run pyright on specific file
uv run pyright src/path/to/file.py

# Run full type check
uv run pyright src/

# Run quality gates
./scripts/check_all.sh
```

## Examples

### Example 1: Missing Return Type Annotation

**Error:**
```
src/application/services/indexing_service.py:45:5 - error: Return type of "process" is unknown
```

**Fix:**
```python
# Before
def process(self, data: dict):
    return ServiceResult.success(data)

# After
def process(self, data: dict) -> ServiceResult[dict]:
    return ServiceResult.success(data)
```

### Example 2: Optional Parameter Handling

**Error:**
```
src/infrastructure/neo4j_repository.py:23:9 - error: Argument of type "Settings | None" cannot be assigned to parameter "settings" of type "Settings"
```

**Fix:**
```python
# Before
def __init__(self, settings: Settings | None = None):
    self.settings = settings

# After
def __init__(self, settings: Settings):
    if not settings:
        raise ValueError("Settings required")
    self.settings = settings
```

### Example 3: Generic Type Arguments

**Error:**
```
src/domain/entities/chunk.py:12:5 - error: Type argument for "list" is missing
```

**Fix:**
```python
# Before
class Chunk:
    entities: list

# After
class Chunk:
    entities: list[str]
```

## Common Error Patterns

See `references/reference.md` for comprehensive error pattern catalog.

**Quick Reference:**

| Error Pattern | Fix Template |
|---------------|--------------|
| `Type of "X" is unknown` | Add type annotation |
| `"X \| None" cannot be assigned to "X"` | Add None check with fail-fast |
| `Type argument is missing` | Add generic type parameter |
| `Cannot access member "X"` | Check type narrowing/guards |
| `Import "X" could not be resolved` | Install stub package or add type: ignore |

## Project-Specific Rules

This project enforces **strict type checking** with the following rules:

1. **No Optional Config Parameters** - Use `Settings`, not `Settings | None`
2. **Fail Fast on None** - Check and raise ValueError immediately
3. **ServiceResult Returns** - All service methods return `ServiceResult[T]`
4. **No Bare None Returns** - Use `ServiceResult.failure()` instead
5. **Generic Types Required** - Always specify type arguments: `list[str]`, not `list`

## Requirements

- Python 3.11+
- pyright (installed via uv): `uv pip install pyright`
- Project type checking config in `pyrightconfig.json`

## Automation Scripts

This skill includes powerful automation utilities in `scripts/`:

1. **parse_pyright_errors.py** - Parse and categorize pyright errors
   - Categorizes errors by type (missing annotations, type mismatch, etc.)
   - Groups by file and severity
   - Provides fix templates and quick wins

2. **fix_missing_annotations.py** - Auto-add type hints
   - Infers return types from return statements
   - Detects ServiceResult[T] patterns
   - Suggests parameter types from usage

3. **fix_optional_handling.py** - Fix Optional/None handling
   - Detects Optional parameters without None checks
   - Adds fail-fast validation
   - Follows project pattern: `if not param: raise ValueError()`

**See:** [scripts/README.md](./scripts/README.md) for usage examples and workflow integration.

## See Also

- [scripts/README.md](./scripts/README.md) - Automation scripts and workflows
- [references/reference.md](./references/reference.md) - Complete error pattern catalog
- [CLAUDE.md](../../../CLAUDE.md) - Project type safety rules
- [../apply-code-template/references/code-templates.md](../../docs/code-templates.md) - Type-safe code templates
