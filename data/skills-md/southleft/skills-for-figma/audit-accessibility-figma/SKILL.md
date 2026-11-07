---
name: audit-accessibility-figma
description: "Deep accessibility scorecard for a single Figma component or component set — state coverage (default/hover/focus/disabled/error/active/loading), focus-indicator quality and contrast, non-color state differentiation, target size, annotation completeness, and color-blind simulation (protanopia/deuteranopia/tritanopia), all rolled into per-category 0–100 scores and prioritized recommendations. Use when the user wants to vet ONE component before shipping it: triggers 'audit this component', 'accessibility score for this button', 'is this component set accessible', 'check the states on this component', 'does my button have a focus state', 'color blind check', 'rate this component for a11y', 'component accessibility scorecard'. Works on ANY Figma plan. For a broad sweep over a whole page/frame use lint-design-figma; for CODE-side (HTML) checks use scan-code-accessibility-figma."
disable-model-invocation: false
---

# audit-accessibility-figma — per-component a11y scorecard

Run a deep accessibility audit on a **single component or component set** and get a weighted 0–100
scorecard with prioritized fixes. Where `lint-design-figma` sweeps a whole tree for many rule
violations, this skill goes deep on one component: it understands variant axes, classifies the
component as interactive vs presentational, and scores each a11y dimension accordingly.

All via `use_figma`, on any plan — it inspects the real variant tree, fills, strokes, effects, and
the component description.

## Skill boundaries
- **`use_figma` rules** — load the official **`figma-use`** skill first; it is the full Figma Plugin API reference. Essentials these scripts rely on: plain JS with top-level `await` + `return` (no IIFE, no `figma.closePlugin()`; `console.log` is not returned), inputs inlined as `const` at the top of each script, colors in 0–1 range, load fonts before any text op, `await figma.getNodeByIdAsync(...)`, and **atomic errors** (a failed script applies nothing — read the error, fix, retry).
- **Tree-wide WCAG + design-system lint** → use `lint-design-figma`.
- **CODE-side a11y** (axe-core over HTML) → use `scan-code-accessibility-figma`.
- **Design-vs-code drift** → use `check-design-parity-figma`.

## Workflow

1. **Target a component.** Set `NODE_ID` to a COMPONENT_SET, COMPONENT, or INSTANCE id (the script
   walks INSTANCE → main component → parent set automatically). Leave it `null` to audit the current
   single selection.
2. **Set the tap-target minimum.** `TARGET_SIZE` defaults to 24 (WCAG 2.5.8 minimum); pass 44 or 48
   for stricter mobile targets.
3. **Run** [`scripts/audit-accessibility.js`](scripts/audit-accessibility.js) via `use_figma`
   (`skillNames: "audit-accessibility-figma"`).
4. **Read the scorecard.** `overallScore` is a classification-weighted blend of the six category
   scores. See [references/audit-categories.md](references/audit-categories.md) for each category, its
   weight, and how to raise it.
5. **Work the recommendations.** `recommendations[]` is already sorted by `priority`
   (`high`/`medium`/`low`) with the WCAG SC named. Fix, then re-run to confirm the score moved.

## Key rules
- **Interactive vs presentational** is auto-detected from the component name and variant axes. It
  changes which categories are scored and their weights — a badge is not penalized for lacking a
  focus state; a button is.
- **Colors are 0–1 floats.** Contrast uses sRGB luminance; color-blind simulation uses
  Brettel/Viénot dichromat matrices.
- **Coverage** means interaction states for interactive components, and variant-axis completeness
  (actual variants ÷ expected combinations) for presentational ones.
- The audit is read-only — apply fixes with `manage-variables-figma` / `figma-use`, then re-audit.
