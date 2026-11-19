---
name: figma-apply-effects
description: Create, apply, remove, audit, and bind Figma Effects through MCP or Plugin API-compatible workflows. Use this skill when the user asks for shadows, inner shadows, layer blur, background blur, glow, glassmorphism, noise, texture, glass effects, progressive blur, effect styles, or effect variables/tokens on selected Figma nodes, while handling current Figma effect compatibility, runtime support, variable binding limits, and readback evidence.
---

# Figma Apply Effects

Use this skill for Figma Effects. It replaces the outdated rule that Figma supports only four effect types. Current Figma Plugin typings include shadow, blur, noise, texture, and glass effect families, but MCP/client support can lag behind typings, so advanced effects are runtime-gated.

## Modes

- `apply`: add one or more effects to selected nodes.
- `remove`: remove all effects or selected effect families.
- `style`: apply an existing Effect Style.
- `bind`: bind supported effect fields to variables.
- `audit`: inspect current effects and compatibility.
- `recipe`: translate visual language like glow, glassmorphism, soft elevation, grit, or texture into effect objects.

## Required Workflow

1. Confirm target node(s), visual intent, whether to replace or append effects, and privacy scope.
2. Invoke `figma:figma-use` before any `use_figma` call.
3. Read the selected node metadata first: `effects`, `fills`, style IDs, variable bindings, and current opacity.
4. If the user asks for an existing Effect Style, search/select that style first and apply the style if available.
5. If raw effects are needed, use [references/effect-compatibility.md](references/effect-compatibility.md) to choose the effect family.
6. For `BACKGROUND_BLUR`, check that the node has a visible fill with alpha below `1`; otherwise the blur will be visually hidden.
7. For glow, use a `DROP_SHADOW` recipe: bright color, `offset: { x: 0, y: 0 }`, larger radius, and low-to-medium alpha.
8. For variables, bind only supported fields. Shadow effects support `color`, `radius`, `spread`, `offsetX`, and `offsetY`; blur effects support `radius`; noise, texture, and glass effects currently do not support variable binding in Figma plugin typings.
9. Write the returned bound effect object back to the node's `effects` array.
10. Read metadata back and report exact effects, bindings, skipped fields, and visual caveats.

## Effect Families

Guaranteed core families when the runtime exposes standard Figma effects:

- `DROP_SHADOW`
- `INNER_SHADOW`
- `LAYER_BLUR`
- `BACKGROUND_BLUR`

Extended families to use only after runtime/tool compatibility is confirmed:

- `NOISE`
- `TEXTURE`
- `GLASS`
- Progressive blur variants inside blur effects.

## Safety And Evidence

- Do not claim an effect was applied until readback shows `node.effects` or the applied style ID changed.
- Do not overwrite existing effects unless the user asked to replace them.
- Do not claim variable binding for unsupported extended effect families.
- If MCP cannot express an advanced effect, report a manual Figma step or fall back to a core-effect approximation.

## Validation And Eval

- Verify readback: `node.effects`, style ID, and bound variables where available.
- Confirm that `BACKGROUND_BLUR` has a translucent fill path or report why the effect may not be visible.
- Use `evals/evals.json` to test glow append, glass blur radius binding, and unsupported extended-effect variable binding.

## Output Shape

Use [assets/effects-report-template.md](assets/effects-report-template.md).

## Resources

- Read [references/effect-compatibility.md](references/effect-compatibility.md) for effect fields and binding support.
- Read `$CODEX_SKILLS_DIR/senior-figma-orchestrator/references/figma-mcp-compatibility.md` when current MCP capability is uncertain.
