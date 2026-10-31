---
name: lint-design-figma
description: "Lint a Figma node tree for WCAG 2.2 accessibility AND design-system quality — contrast, target size, focus indicators, color-only signaling, hardcoded colors, missing text styles, detached components, and more. Use when the user wants a design-side audit BEFORE handoff: triggers 'lint this frame', 'check accessibility', 'WCAG audit', 'is my design accessible', 'find contrast issues', 'check color contrast', 'find hardcoded colors', 'are my components using tokens', 'design QA', 'a11y check on this page', 'audit my design for issues'. Walks the tree from a node (or the whole page) and returns findings with severity (critical/warning/info) and WCAG level (A/AA/AAA/best-practice). The native Figma MCP has NO design-side linting — this is unique to this collection. For the deep per-component a11y scorecard use audit-accessibility-figma; for CODE-side (HTML) checks use scan-code-accessibility-figma."
disable-model-invocation: false
---

# lint-design-figma — WCAG 2.2 + design-system lint over a node tree

Walk a Figma node (or the whole current page) and report accessibility and design-quality problems
in one pass. Runs entirely through `use_figma`, so it works on **any Figma plan** and inspects the
real design (true colors, real auto-layout, actual variant names) rather than generated code.

**Why this is unique:** the native Figma MCP (`get_design_context`, `get_metadata`, etc.) reads
designs for code generation but does **not** lint them. There is no built-in "is this accessible /
token-clean?" check on the design side. This skill fills that gap with a faithful port of 14 WCAG 2.2
rules plus 6 design-system/layout rules.

## Skill boundaries
- **`use_figma` rules** — load the official **`figma-use`** skill first; it is the full Figma Plugin API reference. Essentials these scripts rely on: plain JS with top-level `await` + `return` (no IIFE, no `figma.closePlugin()`; `console.log` is not returned), inputs inlined as `const` at the top of each script, colors in 0–1 range, load fonts before any text op, `await figma.getNodeByIdAsync(...)`, and **atomic errors** (a failed script applies nothing — read the error, fix, retry).
- **Per-component deep scorecard** (state coverage, color-blind sim, 0–100 scores) → use
  `audit-accessibility-figma`.
- **CODE-side a11y** (axe-core over generated HTML) → use `scan-code-accessibility-figma`.
- **Design-vs-code drift** → use `check-design-parity-figma`.

## Workflow

1. **Pick the scope.** Get the target `NODE_ID` (a frame, component set, or screen) from the user's
   selection or a URL. Leave it `null` to lint the entire current page.
2. **Pick the rules.** `RULES` defaults to `['all']`. Narrow it to a group (`'wcag'`,
   `'design-system'`, `'layout'`) or a specific rule id (e.g. `'wcag-contrast'`) to cut noise. The
   full catalog is in [references/lint-rules.md](references/lint-rules.md).
3. **Run** [`scripts/lint-design.js`](scripts/lint-design.js) via `use_figma`
   (`skillNames: "lint-design-figma"`). Edit the `const` inputs at the top first.
4. **Triage by severity.** The result groups findings by rule, each carrying `severity`
   (`critical`/`warning`/`info`) and `wcagLevel` (`a`/`aa`/`aaa`/`best-practice`/`design-system`).
   Lead with `critical` (contrast, target size, focus, color-only).
5. **Fix + re-lint.** Apply fixes (via `manage-variables-figma`, `figma-use`, etc.) and re-run the
   same scope to confirm `summary.total` dropped. Each finding includes the offending `node.id` so
   you can jump straight to it.

## Key rules
- **Colors are 0–1 floats.** Contrast math uses sRGB linearization + relative luminance; the script
  ships its own helpers (no hex needed for input).
- **Background is inferred** by walking ancestors for the nearest solid fill (defaults to white).
  Contrast on semi-transparent fills is flagged `approximate: true`.
- **`MAX_DEPTH`** (default 10) and **`MAX_FINDINGS`** (default 100) bound the walk. If `truncated` is
  set, narrow the scope or raise the cap.
- **WCAG-honest severity:** some rules (text size, line height, letter/paragraph spacing) are labelled
  `best-practice`, not a hard WCAG failure — see lint-rules.md for the exact reasoning per rule.
- Findings are descriptive, not auto-fixed. Confirm intent before bulk-editing a design.
