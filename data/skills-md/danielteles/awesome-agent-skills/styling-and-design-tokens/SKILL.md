---
name: styling-and-design-tokens
description: >-
  A framework-neutral review lens for CSS architecture and design tokens when
  building or reviewing web UI: cascade layers and flat specificity, a
  primitive/semantic/component token pipeline, theming and dark mode by token
  redefinition, the CSS Modules vs utility vs CSS-in-JS decision, intrinsic
  responsive layout, container queries, and fluid type and spacing. Composes
  with `react`, `angular`, `vue`, and `accessibility`. Use it when the user mentions
  CSS, styling, design tokens, theming, dark mode, a design system, container
  queries, media queries, responsive layout, fluid type, "clamp", Tailwind,
  CSS Modules, CSS-in-JS, cascade layers, or "@layer".
license: CC-BY-4.0
metadata:
  author: danielteles
  version: "1.0"
---

# Styling and Design Tokens — Review Skill

The styling review lens for web UI: how CSS is structured, how visual values are tokenized, and how
layout and type respond to space and user preference. Framework-neutral — the rules hold for plain
CSS, CSS Modules, a utility system, or CSS-in-JS; examples are CSS with a little TSX for where styles
attach.

> **Builds on.** `architecture-and-design` (where the design system sits, the feature boundary)
> and `accessibility` (the perceptual thresholds — contrast, motion, reflow, forced colors), plus
> `react`, `angular`, or `vue` for how styles attach to a component. On a conflict,
> `accessibility` decides the requirement and this skill decides the CSS that meets it. Load a
> sibling only when the task turns on its layer; if it is not loaded, apply that layer from
> general knowledge and do not block.

This SKILL.md is self-sufficient: the **Ruleset** below is the complete, enforceable list. Each
`references/<topic>.md` holds that group's reasoning and `❌ / ✅` code, and
`references/worked-example.md` a full review pass; open them for depth when your runtime allows.

---

## How to Use This Skill

Pick the mode that matches the task. Do the steps in order.

| Mode | Steps |
|---|---|
| **Generate** — write styles for a new component or system | 1. Put every declaration in a cascade layer; keep selectors flat (`architecture`). 2. Read semantic tokens for every color, length, radius, shadow, and z-index (`tokens`). 3. Make it respond to its container, not the viewport (`container-queries`, `responsive-layout`); size type with `clamp()` from the scale (`fluid-type`). 4. Run the Ruleset as a checklist. Fix each fail before you hand off. |
| **Review** — check a pull request or a diff | 1. Run the Ruleset against the diff. 2. Write one finding per fail, in the Output Format below. 3. Order the findings: `must-fix` first, then `consider`. 4. If nothing fails, say so in one line. Do not invent findings. |
| **Migrate** — bring an existing stylesheet up to standard | 1. Introduce `@layer` order and move the reset in; do not reorder rules yet. 2. Extract repeated literals into primitive then semantic tokens, one scale at a time. 3. Replace theme-branching component rules with token redefinition on a theme scope. 4. Swap device-width media queries for container queries on the components that travel. Keep each step a separate commit. |

### Output Format

Write one finding per line:

```
<severity> · <topic> · <file>:<line> — <what is wrong>. <the fix as an action>.
```

- `<severity>` is `must-fix` (breaks a rule in this skill, or the build / a lint rule) or `consider` (safe, but a rule prefers another form).
- `<topic>` is a Ruleset topic slug (`architecture`, `tokens`, `theming`, `methodology`, `responsive-layout`, `container-queries`, `fluid-type`).

### Rules for Every Mode

- Name the Ruleset topic when you enforce a rule.
- A raw value in a component (`#3b82f6`, `16px`, `9999`) is a missing token — say which tier it belongs in, not just "use a variable".
- Contrast, motion, reflow, zoom, and forced-colors are `accessibility` requirements; this skill positions the tokens and queries that satisfy them and defers
  the numbers to that skill.

---

## Ruleset

### architecture → `references/architecture.md`

- [ ] Every declaration sits in a cascade layer; the layer order is declared once, up front (`@layer reset, base, tokens, components, utilities;`). Unlayered
      CSS is reserved for a deliberate last-word override.
- [ ] Specificity stays flat: one class per rule, no `#id` styling, no descendant chain deeper than two, no tag-qualified class (`div.card`).
- [ ] No `!important` outside the utilities layer or a commented third-party override.
- [ ] Component styles are scoped — CSS Modules, `@scope`, shadow DOM, or the framework's scoped styles — never a bare element or global class selector from a
      component file.
- [ ] One reset/normalize, in the `reset` layer, with `box-sizing: border-box` set globally once.
- [ ] A component's styles are colocated with the component, not added to a shared global stylesheet.

### tokens → `references/tokens.md`

- [ ] Three tiers — primitive (`--blue-600`, `--space-4`), semantic (`--color-action`, `--space-inline-sm`), component (`--button-bg`) — and components read
      semantic or component tokens, never primitives.
- [ ] No raw color, length, radius, shadow, duration, or z-index literal in a component rule; each is a `var(--token)`. Allowed literals: `0`, `1px` hairlines,
      `100%`, `50%`.
- [ ] Tokens are defined once as CSS custom properties on `:root` or a theme scope; if a token build source exists (Style Dictionary or equivalent) it is the
      origin and CSS is generated.
- [ ] Spacing, font size, radius, and z-index each come from a named scale, not hand-picked values.
- [ ] A token is named for its role, not its value — `--color-danger`, not `--color-red`.
- [ ] Stacking uses a small named z-index scale (`--z-dropdown`, `--z-modal`, `--z-toast`); no ad-hoc `z-index: 9999`.

### theming → `references/theming.md`

- [ ] A theme (dark mode, brand, density) changes only token values, redefined on a scope (`:root`, `[data-theme="dark"]`,
      `@media (prefers-color-scheme: dark)`); component rules never branch on the theme.
- [ ] `color-scheme` is declared on every theme scope.
- [ ] Both an automatic path (`prefers-color-scheme`) and a persisted user override (an attribute on `<html>`) exist, and the override wins in both directions.
- [ ] Where the theme axis is only light / dark, each token is one `light-dark()` declaration under `color-scheme: light dark`, and the user override sets
      `color-scheme` on the root scope instead of redefining tokens.
- [ ] The active theme is applied before first paint — an inline script or an SSR attribute.
- [ ] Forced-colors mode is handled: no meaning carried only by `background-image`, `forced-color-adjust` used deliberately, checked under
      `@media (forced-colors: active)` (thresholds: `accessibility`, perceivable).
- [ ] Every foreground/background token pair meets the contrast `accessibility` requires, in every theme.

### methodology → `references/methodology.md`

- [ ] The approach — scoped CSS / CSS Modules, a utility system, or CSS-in-JS — is chosen once for the project and written down; a component does not mix all
      three.
- [ ] Styling carries zero or build-time runtime cost: no per-render style recalculation, and no runtime CSS-in-JS in a Server Component or a long list.
- [ ] Utilities and arbitrary values express tokens (`p-4`, not `p-[13px]`); an arbitrary value is a missing token.
- [ ] Unused CSS is eliminated at build (module scoping, utility JIT, or coverage).
- [ ] A one-off style is a local scoped rule or a token-backed utility, not an inline `style` attribute with a literal value.

### responsive-layout → `references/responsive-layout.md`

- [ ] Layout is intrinsic — flex/grid with wrapping, `minmax()`, `auto-fit`/`auto-fill`, and `min()`/`max()`/`clamp()` sizing — not device-width
      breakpoints.
- [ ] No fixed `px` width or height on a content container; use `max-width` in `rem`/`ch` with `width: 100%`.
- [ ] Space between siblings is `gap`, not margins on the children.
- [ ] Flow-relative logical properties (`margin-inline`, `padding-block`, `inset`, `border-start-start-radius`) instead of physical
      `left`/`right`/`top`/`bottom`, so writing-direction changes need no overrides.
- [ ] Media queries are `min-width` in `em`/`rem`, few in number, and tied to where the layout breaks — not one per device.
- [ ] A component that must adapt to the space it is placed in uses a container query, not a media query (see `container-queries`).

### container-queries → `references/container-queries.md`

- [ ] A component that appears in more than one column width adapts via `@container`, not `@media`.
- [ ] The wrapper sets `container-type` (usually `inline-size`), and `container-name` when containers nest.
- [ ] `@container` rules name the container they query.
- [ ] Values that should scale with the container use container units (`cqi`, `cqw`), not viewport units (`vw`).
- [ ] Before adding `container-type`, its containment side effects (layout, and `size` containment needing an explicit height) are checked.

### fluid-type → `references/fluid-type.md`

- [ ] Font sizes and the major spacing steps use `clamp()` from a documented scale, not a fixed `px` value re-set at each breakpoint.
- [ ] Font sizes are `rem` (spacing may be `rem` or `em`); no `px` font size.
- [ ] `line-height` is unitless.
- [ ] Body text is at least `1rem`, the `clamp()` minimum never resolves below ~16px, and line length is capped near `66ch` via `max-width` in `ch`.
- [ ] The `clamp()` expression includes a `rem` term, not only `vw` (reflow: `accessibility`, perceivable).
- [ ] Query breakpoints are in `em`/`rem`, not `px`.

---

## Limits

This skill is CSS architecture and design tokens. It does not cover:

- The visual design itself — palettes, type pairings, brand. This skill positions tokens; it does not choose their values.
- Contrast ratios, motion thresholds, reflow and zoom targets, and forced-colors requirements — those are set by `accessibility`. This skill wires the tokens
  and queries that meet them.
- Component API, composition, and where the design system lives — `architecture-and-design` and the framework skills.
- Animation choreography, JS animation libraries, SVG authoring, and icon-system design.
- The internals of a specific CSS framework or CSS-in-JS library — the choice between approaches is here; each library's API is its own.
- CSS build tooling (PostCSS plugins, bundler config) beyond the `@layer` and token setup.
- CSS delivery cost — critical CSS, unused CSS, `font-display`, and font loading — `web-performance`; `methodology` only asks that unused CSS is removable
  at build.

This skill states how the CSS is organized. It is not a substitute for viewing the rendered result at real widths, themes, and zoom levels.

---

## References

This skill composes with:

- **`architecture-and-design`** — owns where the design system and its tokens live and the feature boundary; this skill owns the CSS inside it.
- **`accessibility`** — owns the perceptual thresholds (contrast, motion, reflow, forced colors). This skill positions the tokens and queries; on a conflict
  `accessibility` decides the requirement.
- **`react`** / **`angular`** / **`vue`** — how styles attach to a component (CSS Modules, `styleUrls`, `<style scoped>`, the `class` / `style` binding) and
  the Server Component runtime constraint on CSS-in-JS.
