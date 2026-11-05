---
name: migration-assistant
description: "Assist design system version migration — token mapping, component swapping, variable renaming. Use when: migrate/upgrade/update + design system/tokens/components/version, or when transitioning between design system versions."
---

# Migration Assistant — Design System Version Migration

Assist with migrating a Figma design system between versions: map old tokens to new ones, swap deprecated components, rename variables, and verify migration completeness. Works incrementally with user checkpoints.

## Skill Boundaries

- Use this skill to **migrate between design system versions**.
- If the task is **building a new design system from scratch**, switch to [figcraft-generate-library](../figcraft-generate-library/SKILL.md).
- If the task is **auditing current system health**, switch to [design-system-audit](../design-system-audit/SKILL.md).
- If the task is **syncing tokens from a spec**, switch to [token-sync](../token-sync/SKILL.md).

## Workflow

### Step 1: Connect and Load Tools

```
ping                                          → verify plugin connection
load_toolset("variables")                     → variable management
load_toolset("tokens")                        → token diff/sync
load_toolset("components-advanced")           → component swapping
```

**If `ping` fails (plugin not connected):** STOP. Do not fall back to other MCP servers. Tell user: open Figma → Plugins → FigCraft → wait for connection, then retry.

### Step 2: Discover Current State

Inventory the existing design system:

```
variables_ep(method: "list")                  → all current variables
variables_ep(method: "list_collections")      → collection structure
components(method: "list")                    → all components
scan_styles                                   → all styles
```

### Step 3: Define Migration Map

Work with the user to define the mapping between old and new:

```markdown
## Token Migration Map

| Old Token | New Token | Action |
|-----------|-----------|--------|
| color/primary | color/brand/primary | rename |
| color/bg | color/surface/default | rename + remap |
| spacing/sm | space/200 | rename |
| — | color/surface/elevated | create new |
| color/accent | — | deprecate |

## Component Migration Map

| Old Component | New Component | Action |
|---------------|---------------|--------|
| Button/Primary | Button (variant=filled) | swap variant |
| Card/Basic | Card (variant=elevated) | swap + update props |
| OldInput | TextField | swap component |
| DeprecatedBadge | — | remove |
```

⛔ WAIT for user confirmation before proceeding.

### Step 4: Migrate Variables

For each variable in the migration map:

Rename:
```
variables_ep(method: "update", variableId: "...", name: "new/name")
```

Create new:
```
variables_ep(method: "create", name: "...", collectionId: "...", resolvedType: "...")
```

Create alias (semantic → primitive):
```
create_variable_alias(variableId: "...", targetVariableId: "...")
```

Update scopes:
```
variables_ep(method: "update", variableId: "...", scopes: [...])
```

After each batch, verify:
```
variables_ep(method: "list")                  → confirm changes applied
```

### Step 5: Migrate Components

For each component swap:

```
swap_instance(instanceId: "...", componentKey: "new-component-key")
```

For property updates after swap:
```
nodes(method: "update", patches: [{ nodeId: "...", props: { ... } }])
```

### Step 6: Migrate Styles

For text/paint/effect style changes, update or create new styles and rebind:

```
load_toolset("styles")
styles_ep(method: "update_text", ...)
styles_ep(method: "update_paint", ...)
```

### Step 7: Verify Migration

Run a comprehensive check:

```
lint_fix_all                                  → catch broken bindings or layout issues
```

Additionally verify:
- No references to old/deprecated variable names
- All component instances point to new components
- No hardcoded values where new tokens exist
- Visual regression check with `export_image` on key screens

### Step 8: Cleanup

After verification and user approval:
- Delete deprecated variables (if confirmed)
- Remove deprecated component pages
- Update documentation pages

⛔ WAIT for user confirmation before any destructive operations.

## Migration Strategies

### Token Rename (Non-Breaking)
1. Create new variable with new name
2. Alias old variable → new variable
3. Gradually update bindings to use new name
4. Delete old variable when no references remain

### Token Value Change
1. Update variable value directly
2. Verify all bound nodes reflect the change
3. Check contrast ratios if color changed

### Component Swap
1. Identify all instances of old component
2. Swap to new component
3. Re-apply property overrides that map to new properties
4. Verify visual correctness

### Breaking Migration (Major Version)
1. Create new collection/components alongside old
2. Migrate screen by screen
3. Verify each screen before proceeding
4. Remove old system only after full migration

## Safety Rules

- NEVER delete variables or components without explicit user confirmation
- ALWAYS create before deleting — new tokens exist before old ones are removed
- ALWAYS verify visually after each migration step
- Keep a migration log of all changes for rollback reference
- Use `save_version_history` before starting migration for easy rollback
