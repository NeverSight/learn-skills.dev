---
name: code-navigation
description: Rapid, focused navigation to locate definitions/usages and map the impact of proposed changes.
license: MIT
metadata:
  mode: read-only
  purpose: navigation
---

# Code Navigation

## When to Use

- You need the authoritative locations and immediate impact surface for a symbol, endpoint, or config key before making changes.

## Responsibilities

- Find definitions, primary usages, and obvious entry points.
- Produce a short impact map (who calls it, where it is exported, related tests).
- Keep reads minimal (prefer 1-5 files).

## Rules

- Read-only; do not modify files or run shell commands.
- Use `grep` first, then targeted `read` for the top matches.
- Provide `path:line` citations for all claims.

## Workflow

1. Clarify the exact symbol or endpoint.
2. Narrow candidates via glob and grep.
3. Read 1-3 highest-confidence files.
4. Report: primary locations, secondary references, change impact.

## Output

- **Locations:** `path:line` entries.
- **Impact:** 1-3 bullets describing callers, dependents, and test coverage.
- **Next:** suggested file to open if deeper context is required.

## Examples

- "Where is JWT issued and validated?" - definition + callers + tests.
- "Which packages import `database.GetDB()`?" - list of usages.

## Related Skills

- `source-search` (broad grep), `file-reader` (detailed read), `ast-introspection` (structure-aware)
