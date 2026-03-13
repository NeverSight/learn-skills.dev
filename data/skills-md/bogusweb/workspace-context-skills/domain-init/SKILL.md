---
name: domain-init
description: Initializes or refreshes the Domain Registry in CLAUDE.md by scanning the project for library directories. Run this once per project, or after adding new libraries. Creates the registry table that domain-context skill uses for auto-loading.
---

# Domain Registry Initializer

Initialize or refresh the **Domain Registry** in this project's `CLAUDE.md`.

## What This Does

1. Scans the project for library/domain directories
2. Reads each library's metadata (`project.json`, `package.json`, or `ng-package.json`)
3. Writes (or updates) a `## Domain Registry` section in `CLAUDE.md`
4. Adds the auto-load instruction if it's not already present

## Instructions

### Step 1 — Detect Project Structure

Run the detection script to find all library directories:

```bash
bash .claude/skills/domain-init/scripts/scan_domains.sh 2>/dev/null \
  || node .claude/skills/domain-init/scripts/scan_domains.js 2>/dev/null
```

If neither script is available, scan manually:

- Look for directories under `libs/` that contain `project.json` or `package.json`
- For Nx workspaces: read `project.json` → `name` and `targets.build.options.project`
- For plain npm: read `package.json` → `name`
- For Angular libraries: read `ng-package.json` → check parent `package.json` for name

### Step 2 — Build the Registry Table

For each found library, collect:

| Field | Source |
|-------|--------|
| `Path` | Relative directory path from workspace root |
| `Import Path` | `importPath` from `project.json`, or `name` from `package.json` |
| `Description` | First line of existing `README.md` (skip `#` heading), or generate from library name |

Generate description heuristics if no README exists:
- `widget-*` → "Widget: [name] feature module"
- `*-domain` or `domain` → "Domain layer: business logic and state"
- `*-feature` or `feature` → "Feature layer: container components"
- `*-ui` or `ui` → "UI layer: presentational components"
- `*-util` or `util` → "Utilities and helpers"
- `shared/*` → "Shared: [name]"

### Step 3 — Write to CLAUDE.md

Read the current `CLAUDE.md`. Then:

**If `<!-- domain-registry-start -->` already exists:** Replace everything between the start and end markers with the new table.

**If it does not exist:** Append the following block to `CLAUDE.md`:

```markdown

## Domain Registry

> Auto-maintained by domain-init skill. Run `/domain-init` to regenerate.

<!-- domain-registry-start -->
| Path | Import Path | Description |
|------|-------------|-------------|
| <path> | <import-path> | <description> |
<!-- domain-registry-end -->
```

### Step 4 — Add Auto-Load Instruction (if missing)

Check if `CLAUDE.md` already contains the phrase `domain-init skill` or `Domain Registry`. If it does NOT, also append:

```markdown

## Domain Context Loading

The `domain-init` skill is active. Before working on any library listed in the
Domain Registry above, silently read its `README.md` for architecture context.
```

### Step 5 — Report

After writing, output a summary:

```
✓ Domain Registry updated in CLAUDE.md
  Found N domains:
  - libs/widget-chat  →  @scope/widget-chat
  - libs/shared/...   →  @scope/shared/...
  ...

  Domains without README.md (consider running /domain-readme <path>):
  - libs/dashboards-manager
  - libs/widget-map
```

## Arguments

`$ARGUMENTS` — optional scan root path. Defaults to `libs/` if empty.

Examples:
- `/domain-init` — scans `libs/`
- `/domain-init libs/shared` — scans only `libs/shared/`
- `/domain-init packages` — scans a `packages/` monorepo structure

## Re-running

This skill is idempotent. Running it multiple times only updates the registry table, preserving all other content in `CLAUDE.md`.
