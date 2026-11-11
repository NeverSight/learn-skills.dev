---
name: dhtmlx-angular-gantt
description: >
  Builds and integrates DHTMLX Angular Gantt into Angular applications. Covers setup,
  inputs, templates, themes, data.save, data.batchSave, resources, calendars, undo/redo,
  row reorder, sortorder, and Angular wrapper integration patterns for
  @dhtmlx/trial-angular-gantt and @dhx/angular-gantt. Applies when working with gantt charts,
  project timelines, task dependencies, task CRUD, resource panels, working calendars,
  lightboxes, or weekend highlighting in Angular — regardless of whether "DHTMLX" is
  mentioned by name. Provides verified API guidance rather than guessing Angular Gantt APIs.
---

## Source Of Truth

Use only:
1. The current project's files, structure, and established patterns
2. DHTMLX MCP for Angular Gantt API details: https://docs.dhtmlx.com/mcp
3. Official DHTMLX Angular Gantt docs as fallback: https://docs.dhtmlx.com/gantt/integrations/angular/

Never invent inputs, template signatures, callback contracts, event names, or backend behavior.

If any Angular Gantt API detail is unclear, resolve it through DHTMLX MCP before writing code.

## Preflight

Before writing code, identify:
- **package**: `@dhtmlx/trial-angular-gantt` or `@dhx/angular-gantt` — check `package.json`, imports, lockfiles
- **runtime**: Angular standalone components or NgModule setup
- **ownership model**: Angular state/store as source of truth (recommended) or Gantt as source of truth (performance-focused)
- **persistence**: local only, `data.save` (default), or `data.batchSave` (bulk sync)

## Workflow

1. Confirm installed Angular Gantt package and matching import path.
2. Confirm wrapper CSS is imported and chart height chain is explicit.
3. Decide the state ownership model before implementing features, and keep one model per page/feature area.
4. Read only the reference file needed for the task:
   - Angular wrapper integration/setup: [references/angular-integration.md](references/angular-integration.md)
   - CRUD, state, persistence, wrapper task types, and v9 -> v10 migration: [references/data-and-crud.md](references/data-and-crud.md)
   - Failure cases and guardrails: [references/known-failures.md](references/known-failures.md)
   - Advanced patterns (reorder, resources, undo/redo, schema): [references/advanced-patterns.md](references/advanced-patterns.md)
   - Styling, theming, templates, and override strategy: [references/styling-and-theming.md](references/styling-and-theming.md)
5. Use DHTMLX MCP before relying on advanced or unfamiliar APIs.
6. Implement with documented APIs only.

## MCP Server

This skill relies on DHTMLX MCP for API verification. If the `dhtmlx-mcp` tool is not available, ask the user to add it:

Claude Code:
```bash
claude mcp add --transport http dhtmlx-mcp https://docs.dhtmlx.com/mcp
```

Codex:
```bash
codex mcp add dhtmlx-mcp --url https://docs.dhtmlx.com/mcp
```

If MCP is not available, use the official docs at https://docs.dhtmlx.com/gantt/integrations/angular/ as fallback.

## Consult MCP First For

Consult DHTMLX MCP before using or changing:
- template callbacks you have not already verified
- advanced inputs such as `batchSave`, `customLightbox`, `groupTasks`, or `resourceFilter`
- `events` callback signatures beyond commonly used handlers
- theme/skin names beyond known project usage
- complex layout/resource panel definitions (`resourceGrid`, `resourceTimeline`, shared scroll)
- workload cell template callbacks and overload logic

## Hard Rules

- Use wrapper path (`<dhx-gantt>`) by default for Angular tasks.
- The Gantt container must have explicit height through the parent chain.
- Use app theme as single source of truth; map it to Gantt theme.
- Prefer CSS variables and documented templates before selector-heavy overrides.
- Keep tasks/links in Angular state/store when surrounding UI depends on chart state.
- Normalize date values before persistence.
- Build backend payloads explicitly from normalized app task/link models.
- If mutating through `instance`, keep Angular state synchronized immediately.
- Do not mix wrapper-driven inputs and imperative instance mutations without intentional synchronization.

## Quick Checklist

- [ ] Correct package identified
- [ ] Matching wrapper CSS import used
- [ ] Explicit height chain provided
- [ ] State ownership model chosen
- [ ] Dates normalized before persistence
- [ ] Advanced APIs verified with MCP
