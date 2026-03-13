---
name: custom-quality-check
description: Project-specific code quality checks. Runs Ruff linting on modified Python files for claudecode_webui.
---

# Custom Quality Check

## Purpose

This is a **project-specific custom skill** called by the Builder workflow to enforce code quality standards.
It runs linting and quality checks specific to this project (claudecode_webui).

Generic workflow skills invoke this skill if it exists; if absent, the quality check step is skipped.

## When Called

The Builder invokes this skill from its working directory (the worktree) after implementation, providing the list of changed files.

## Input

- `changed_files`: List of files modified (from `git diff --name-only`)

## Quality Checks

### Ruff Linting (Python files)

Run Ruff on modified Python files only:
```bash
# Get changed Python files
CHANGED_PY=$(git diff --name-only --diff-filter=AM | grep '\.py$')

# Run Ruff with auto-fix on changed files
if [ -n "$CHANGED_PY" ]; then
    uv run ruff check --fix $CHANGED_PY
fi
```

### Rules

- New code MUST NOT introduce new violations
- Changed code SHOULD fix existing violations when touched
- Auto-fix safe violations in modified files
- Line length: 100 characters
- Target Python: 3.11+

### Important

- Do NOT run `uv run ruff check --fix src/` on the entire codebase
- Only lint files that were actually modified to avoid unrelated changes

## Usage by Generic Skills

The Builder workflow calls this skill like:

```
Invoke custom-quality-check skill with changed_files
```

The skill runs project-specific quality checks in the Builder's working directory.
If this skill does not exist, the generic workflow skips the quality check step.
