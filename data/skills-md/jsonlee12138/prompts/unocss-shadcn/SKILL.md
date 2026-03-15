---
name: unocss-shadcn
description: Configure UnoCSS with unocss-preset-shadcn using a semi-automatic, framework-agnostic workflow. Use when setting up or updating UnoCSS + shadcn integration, deciding monorepo vs single-project component destinations, enforcing peerDependencies in monorepos, and requiring shadcn MCP + manual component creation mode.
---

# unocss-shadcn

## Overview
Apply a deterministic setup flow for UnoCSS and `unocss-preset-shadcn` without running automatic installers. Detect monorepo strictly, route component targets by project shape, and enforce shadcn MCP plus manual-mode component creation.

## Core Rules
1. Run in semi-automatic mode only: propose commands and file edits, but do not auto-install dependencies.
2. Detect monorepo only when one of these is true:
- `pnpm-workspace.yaml` exists at repo root.
- Root `package.json` contains `workspaces`.
3. Use destination policy:
- Monorepo: `packages/shadcn-ui`
- Single project: `src/components`
4. UnoCSS config location policy:
- Monorepo: configure in each `apps/<app>/uno.config.*` (NOT at repo root or in packages).
- Single project: configure at project root `uno.config.*`.
5. Default to `presetWind4` unless the user explicitly requests a different version (e.g. `presetWind3`).
6. For monorepo component package dependencies, write shadcn-related runtime items to `peerDependencies`.
7. Use shadcn MCP before any component usage or creation.
8. Create shadcn components in manual mode only (do not use Tailwind-oriented auto init flow).
9. If shadcn MCP is unavailable, block the component step and return an explicit error.

## Workflow
1. Inspect project files:
- `package.json`
- `pnpm-workspace.yaml`
- `uno.config.*` or `unocss.config.*`
- `components.json` if present
2. Decide branch using strict monorepo detection.
3. Update UnoCSS config to include `unocss-preset-shadcn` in `presets`.
4. Generate destination-specific instructions from references:
- Monorepo path: `references/monorepo.md`
- Single-project path: `references/single-project.md`
5. Enforce shadcn MCP chain and manual creation mode.
6. Verify with `references/checklist.md` before claiming completion.

## Required MCP Chain (shadcn)
Run these in order before component operations:
1. `get_project_registries`
2. `search_items_in_registries` or `list_items_in_registries`
3. `get_item_examples_from_registries`
4. Optional reference only: `get_add_command_for_items`

Use MCP outputs as the source of truth for component API, file content, and dependency hints.

## References
- `references/monorepo.md`: monorepo branch instructions and templates
- `references/single-project.md`: single-project branch instructions and templates
- `references/checklist.md`: validation checklist and remediation matrix
