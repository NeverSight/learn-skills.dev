---
name: figma-canvas-editor
description: Create and edit native Figma canvas objects with MCP when explicitly scoped. Use this skill when the user asks to add or change frames, sections, components, instances, auto layout, variables, styles, FigJam objects, connectors, Slides objects, or selected nodes in Figma, and when the task requires mutation evidence, rollback-aware scope, and design-system consistency.
---

# Figma Canvas Editor

Use this skill for direct Figma mutations. Read-only understanding belongs to `figma-context-reader`; token/library governance belongs to `figma-design-system-sync`.

## Modes

- `create`: add frames, sections, components, objects, or layouts.
- `update`: change selected nodes, layout, styles, variables, text, or component instances.
- `delete`: remove effects, nodes, variants, or obsolete objects only with explicit scope.
- `figjam`: edit FigJam objects, sections, connectors, and shapes.
- `slides`: edit Figma Slides content when the Slides skill is available.

## Workflow

1. Confirm target file/page/frame/node and exact mutation scope.
2. Prefer duplicating important frames before broad changes.
3. Invoke `figma:figma-use` before any `use_figma` call. For FigJam or Slides, invoke the relevant installed Figma skill as well.
4. Read current metadata before editing.
5. Apply changes using native Figma objects, auto layout, components, variables, and styles where possible.
6. Read metadata back after editing and capture screenshot/export evidence when available.
7. Report changed targets, evidence, skipped checks, and rollback path.

## Mutation Boundaries

- Do not make broad destructive changes without explicit approval.
- Do not detach instances, flatten vectors, rasterize editable text, or remove variables/styles unless the user requests that outcome.
- Do not invent node IDs or claim a selected node exists without MCP evidence.
- Keep design-system naming consistent with the existing file when visible.

## Output Shape

Use [assets/canvas-edit-report.md](assets/canvas-edit-report.md).

## Validation And Eval

- Verify that every mutation report includes target, scope, before evidence, after evidence, and skipped checks.
- Treat missing readback as `Skipped` or `Blocked`, not as successful mutation evidence.
- Use `evals/evals.json` to forward-test scoped creation and destructive-delete prompts.
