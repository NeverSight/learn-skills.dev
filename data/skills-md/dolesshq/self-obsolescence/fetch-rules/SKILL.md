---
name: fetch-rules
description: Fetch and apply Cursor-style workspace rules supporting all rule formats (.cursor/rules/*.md, *.mdc, AGENTS.md, and legacy .cursorrules).
metadata:
  short-description: Select and print relevant Cursor rules for the task.
---

# Fetch Rules 

## Purpose

This skill emulates Cursor's rule selection behavior for AI agents.

It discovers and selects rules from:

- **Project Rules** (`.cursor/rules/`)
  - `.mdc` files with frontmatter (`description`, `globs`, `alwaysApply`)
  - `.md` files without frontmatter (treated as always-apply)
- **AGENTS.md** files (root and nested subdirectories)
- **Legacy `.cursorrules`** at repo root (deprecated but still supported)

### Rule Selection Semantics

| Rule Type | Selection Behavior |
|---|---|
| `alwaysApply: true` | Always included |
| Simple `.md` (no frontmatter) | Always included |
| `globs: ...` | Included when any candidate file matches |
| `description: ...` | Included when prompt overlaps with description keywords |
| No metadata (`.mdc` only) | Included only when explicitly referenced |
| `AGENTS.md` | Always included when in scope (directory hierarchy) |

Candidate files come from `--files`, `--use-git-diff`, and file-like paths found in `--prompt`.

## Requirements

- `bash` (macOS / Linux default)
- `git` optional (only if you use `--use-git-diff`)

No Python, Node, or jq required.

## Usage

Run commands from this skill directory (the directory containing this `SKILL.md`). Do not hardcode agent install paths.

```bash
bash scripts/fetch_rules.sh --prompt "<your request>"
```

Optional file hints:

```bash
bash scripts/fetch_rules.sh --prompt "<request>" --files path/to/a.ts path/to/b.sql
bash scripts/fetch_rules.sh --prompt "<request>" --use-git-diff
```

Force-include a rule by filename:

```bash
bash scripts/fetch_rules.sh --prompt "<request>" --explicit global.mdc
bash scripts/fetch_rules.sh --prompt "<request>" --explicit react-patterns.md
```

## Supported Formats

| Format | Location | Description |
|---|---|---|
| `.mdc` | `.cursor/rules/` | Rules with YAML frontmatter for fine-grained control |
| `.md` | `.cursor/rules/` | Simple markdown rules (always applied) |
| `AGENTS.md` | Root or subdirs | Simple agent instructions (always applied in scope) |
| `.cursorrules` | Root only | Legacy format (deprecated, will be removed) |

## Notes

- If multiple rules share the same filename, the rule in the closest scoped directory wins (deepest scope).
- Glob matching uses bash pattern matching (`[[ file == pattern ]]`). Cursor-style `**` works effectively as `*` in this matcher.
- `AGENTS.md` files are combined hierarchically—parent directories' instructions apply alongside more specific subdirectory instructions.
