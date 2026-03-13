---
name: safe-delete
description: Stage deletions with `scripts/safe-delete` (script-first, no MCP tool calls). Moves paths to `/tmp/safe-delete` with collision-safe names. [skill-hash:71d8a0c]
---

# Safe Delete

Use this skill whenever you need to remove files/directories without permanent deletion.

## Required Path

- Run: `~/.codex/skills/safe-delete/scripts/safe-delete <path...>`
- Do not call MCP safe-delete tools.
- Do not run raw `rm` unless user explicitly asks for hard delete.

## Behavior

- Creates `/tmp/safe-delete` if missing.
- Moves each provided path to `/tmp/safe-delete/<name>-<timestamp>-<rand>`.
- Prints one mapping line per moved path.
