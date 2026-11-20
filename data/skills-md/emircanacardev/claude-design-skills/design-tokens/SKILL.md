---
name: design-tokens
description: Designs a design token architecture with primitive, semantic and component tiers, consistent naming and modes for light, dark and density, then exports it as CSS custom properties, W3C Design Tokens Community Group JSON using $value and $type, and an optional Tailwind theme mapping. Use when asked to set up tokens or theme variables, create a token JSON, or tokenize hard-coded styles. Not for choosing the colors themselves; use color-system.
---

# Design Tokens

Produces a three-tier token system (primitive, semantic, component) with mode support, delivered as DTCG JSON and CSS custom properties so design files and code share one source of truth.

## When to use
- Starting a design system or theming layer
- Replacing hard-coded hex, px and shadow values in a codebase with tokens
- Adding dark mode or a compact density to an existing token set
- Syncing Figma variables with code or preparing input for a token build tool
- Auditing a token set for naming drift, duplicates or broken aliases

## Workflow
1. Inventory: collect existing values (hex, rgb, px, rem, radii, shadows, durations, z-index) from code or spec. Count unique values per category and flag near-duplicates such as #1F2937 and #1E2937.
2. Define primitives as context-free scales: colors from color-system, spacing from layout-spacing, type from typography-system, plus radius, shadow, duration, easing and z-index.
3. Define semantic tokens: role-based aliases that reference primitives (color.bg.default, color.text.muted, color.border.subtle, color.action.primary.bg, space.inset.md).
4. Add component tokens only where a component must be themed independently (button.primary.bg referencing color.action.primary.bg).
5. Define modes: light and dark swap semantic references; density swaps spacing and sizing semantics.
6. Export DTCG JSON, CSS custom properties, and a Tailwind mapping if the project uses Tailwind.
7. Migrate: replace hard-coded values with semantic tokens, worst offenders first.

## Rules
**Architecture**
- Three tiers maximum. Code references semantic or component tokens, never primitives.
- Primitive names describe the scale (color.blue.600, space.4, radius.md); semantic names describe the role (color.text.danger, not color.text.red).
- Modes change semantic aliases only; primitive values are identical across modes.
- Every text color token documents its intended background and meets 4.5:1 there (3:1 for large text, borders and icons) in every mode.
- A value used once is not a token yet; promote it on second use.

**Naming**
- Order general to specific: category.role.variant.state, e.g. color.action.primary.bg.hover.
- JSON uses dot paths; CSS uses kebab-case with an optional namespace: --ds-color-action-primary-bg-hover.
- One state vocabulary everywhere: default, hover, active, focus, disabled, selected.
- Numeric steps for primitives (space.4, blue.600); t-shirt sizes (xs–2xl) for semantic spacing and radius.
- No raw values or vague qualifiers in names (space.16px, gray-dark-2).

**Formats**
- DTCG: every token has $value; $type is set on the token or inherited from its group (color, dimension, fontFamily, fontWeight, duration, cubicBezier, number, shadow, typography). Aliases use curly-brace references such as {color.blue.600}. Add $description to semantic tokens.
- The DTCG 2025.10 stable spec uses object values: color as colorSpace + components (optional hex), dimension and duration as value + unit. Some tools still expect strings (#2563eb, 16px). Match the project's toolchain and stay consistent.
- DTCG has no per-token mode field: keep each mode in its own file (semantic.light.json, semantic.dark.json).
- CSS output: font sizes and spacing in rem (1rem = 16px), borders in px, durations in ms, easings as cubic-bezier().
- Light values on :root; dark under :root[data-theme="dark"] and inside @media (prefers-color-scheme: dark) on :root:not([data-theme="light"]). Set color-scheme per mode. See dark-mode.

## Output
- tokens/primitives.json, tokens/semantic.light.json, tokens/semantic.dark.json (plus component.json if needed) in DTCG format.
- tokens.css with :root, dark-mode and [data-density="compact"] blocks.
- Optional Tailwind mapping: a v4 @theme block, or v3 theme.extend values pointing at var(--token).
- Migration table: hard-coded value → token, with file locations for the top offenders.

```json
{
  "color": {
    "$type": "color",
    "blue": { "600": { "$value": { "colorSpace": "srgb", "components": [0.145, 0.388, 0.922], "hex": "#2563eb" } } },
    "action": { "primary": { "bg": {
      "$value": "{color.blue.600}",
      "$description": "Primary buttons and active controls on light surfaces"
    } } }
  },
  "space": { "$type": "dimension", "4": { "$value": { "value": 1, "unit": "rem" } } }
}
```

## Avoid
- Semantic names that encode appearance (color.text.gray, button-blue)
- Components referencing primitives directly, which breaks theming
- Separate dark primitive ramps instead of swapping semantic aliases
- Four or more tiers or deep nesting (color.brand.primary.default.base.light)
- Tokens for one-off values, or duplicates with identical value and role
- px font sizes that ignore user font-size preferences
- Alias cycles or references to tokens that do not exist

## Final check
- [ ] Every in-scope hard-coded value maps to a token or is documented as an exception
- [ ] No component or stylesheet references a primitive directly
- [ ] All aliases resolve; no cycles
- [ ] Light and dark files define the same semantic token set
- [ ] Text and background pairs meet 4.5:1 in every mode
- [ ] Every token has $value and a resolvable $type
- [ ] Naming pattern and state vocabulary consistent across categories
