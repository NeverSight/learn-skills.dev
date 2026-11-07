---
name: token-sync
description: "Sync DTCG design tokens to Figma variables and styles. Use when: sync/push/import + tokens/DTCG + Figma, or when updating Figma variables from a token spec file."
---

# Token Sync — DTCG to Figma Sync

Sync DTCG (W3C Design Token Community Group) design tokens to Figma. Creates/updates Variables for atomic tokens (color, spacing, radius) and Styles for composite types (typography, shadow). Idempotent — safe to run multiple times.

## Skill Boundaries

- Use this skill to **sync tokens from DTCG JSON to Figma**.
- If the task is **comparing tokens without syncing**, switch to [spec-compare](../spec-compare/SKILL.md).
- If the task is **exporting Figma variables to DTCG JSON**, use `reverse_sync_tokens` directly after `load_toolset("tokens")`.
- If the task is **creating a full design system** (variables + components), switch to [figcraft-generate-library](../figcraft-generate-library/SKILL.md).

## Workflow

### Step 1: Connect and Get File Path

```
ping                                          → verify plugin connection
```

**If `ping` fails (plugin not connected):** STOP. Do not fall back to other MCP servers. Tell user: open Figma → Plugins → FigCraft → wait for connection, then retry.

Ask the user for the DTCG JSON file path.

### Step 2: Load Token Tools

```
load_toolset("tokens")                        → enable DTCG token tools
```

### Step 3: Preview Tokens

```
list_tokens(filePath: "...")                   → parse and preview what will be synced
```

Show the user a summary: total tokens, types breakdown (color, spacing, typography, shadow, etc.).

### Step 4: Check Current State

```
diff_tokens(filePath: "...", collectionName: "...")  → compare against existing Figma variables
```

Report what will happen:
- New tokens to create
- Existing tokens to update
- Tokens already in-sync (will be skipped)

### Step 5: Sync

```
sync_tokens(filePath: "...", collectionName: "...", modeName: "...")
```

Parameters:
- `filePath` — path to DTCG JSON
- `collectionName` — target Figma collection (default: "Design Tokens")
- `modeName` — target mode (default: first mode)

For multi-mode sync (e.g., Light/Dark):

```
sync_tokens_multi_mode(modes: {
  "Light": "tokens/light.json",
  "Dark": "tokens/dark.json"
}, collectionName: "Color")
```

### Step 6: Report Results

Present sync results:

```
📊 Sync Complete:
- Created: X variables, Y styles
- Updated: Z variables
- Skipped (in-sync): N
- Failed: M (with error details)
```

### Step 7: Verify

Optionally cache tokens for lint integration:

```
cache_tokens(filePath: "...")                  → cache for lint rules to reference
```

This enables lint rules (e.g., `spec-color`, `spec-typography`) to check designs against the synced token spec.

## Key Concepts

- Atomic tokens (color, number, dimension) → Figma Variables
- Composite tokens (typography, shadow) → Figma Styles (Variables don't support compound types)
- Sync is idempotent — running twice produces: created=0, skipped=all
- Aliases are resolved: `{color.primary}` → references the actual variable

## Available Token Tools

| Tool | Purpose |
|------|---------|
| `list_tokens` | Parse and preview DTCG tokens |
| `sync_tokens` | Sync single-mode tokens to Figma |
| `sync_tokens_multi_mode` | Sync multi-mode tokens (Light/Dark) |
| `diff_tokens` | Compare DTCG vs Figma variables |
| `reverse_sync_tokens` | Export Figma variables to DTCG JSON |
| `cache_tokens` | Cache tokens for lint integration |
| `list_cached_tokens` | List cached token entries |
| `delete_cached_tokens` | Remove cached token entry |
| `scan_styles` | Scan local styles (paint, text, effect) |
| `export_tokens` | Export all local variables as DTCG tokens |
| `diff_styles` | Compare DTCG tokens against Figma styles |

## Integration

```
spec-compare → token-sync → design-lint
(audit gap)    (this skill)   (verify compliance)
```

After syncing, run `design-lint` with token category to verify designs comply with the synced tokens.
