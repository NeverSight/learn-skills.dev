---
name: figma-context-reader
description: Read and summarize Figma design context for UI/UX implementation, audit, and design-system work. Use this skill when the user provides a Figma URL, selected Figma node, frame, component, Dev Mode context, variables, library, or screenshot and wants structured facts about hierarchy, layout, tokens, components, assets, variants, interaction notes, or implementation constraints without mutating the Figma file.
---

# Figma Context Reader

Use this skill to turn Figma context into an evidence-backed design brief. This is a read-only skill; route mutations to `figma-canvas-editor` or `figma-design-system-sync`.

## Modes

- `frame-brief`: summarize a selected frame or page.
- `component-brief`: summarize components, variants, props, and constraints.
- `token-brief`: summarize variables, styles, color roles, spacing, radius, typography, and effects.
- `audit-input`: collect enough Figma evidence for `ux-audit-skill` or `design-critic-skill`.
- `handoff`: prepare context for implementation specialists.

## Workflow

1. Confirm the input type: Figma URL, selected node, file key, screenshot/export, or connected MCP selection.
2. Apply `../../shared/privacy-policy.md`.
3. If a `use_figma` call is needed, first invoke the installed `figma:figma-use` skill.
4. Read only the needed nodes, variables, components, styles, and assets. Avoid broad file scans unless the user asks for library/system work.
5. Produce a structured context brief with evidence labels. Distinguish direct Figma metadata from visual inference.
6. If MCP access is unavailable, ask for an export, screenshot, node metadata, or manual Figma details as fallback.

## Output Shape

Use [assets/context-brief-template.md](assets/context-brief-template.md).

## Evidence Rules

- `Figma metadata`: node names, type, layout fields, variables, styles, component names, asset references.
- `Visual inference`: hierarchy, attention, density, likely intent, visual polish.
- `Missing`: anything not available from the current Figma context.

Do not claim DOM, runtime behavior, accessibility scan, or implementation evidence from Figma context alone.

## Validation And Eval

- Check that the final brief names the evidence source and privacy mode.
- Check that every implementation claim is traceable to Figma metadata, visual inference, or an explicit missing-context note.
- Use `evals/evals.json` for forward tests that distinguish connected Figma context from screenshot-only input.

## Resources

- Read `$CODEX_SKILLS_DIR/senior-figma-orchestrator/references/figma-mcp-compatibility.md` when tool availability is unclear.
- Use [assets/context-brief-template.md](assets/context-brief-template.md) for reports.
