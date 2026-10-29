---
name: ak-ui
description: Integrate, build, extend, or review web interfaces with the brand-adaptive ak-ui design language and CSS foundation. Use when a user asks to install ak-ui, create an Arknights-inspired interface without copying game assets, style native or unstyled headless components such as Reka UI, convert an existing page to ak-ui, or audit whether an implementation follows ak-ui tokens, geometry, interaction states, responsiveness, and accessibility.
---

# ak-ui

Build original interfaces with ak-ui's industrial geometry, tactical information hierarchy, and terminal-like feedback. Treat ak-ui as a design contract and CSS foundation, not as a request to reproduce a specific Arknights screen.

## Read the relevant references

- Always read [references/design-language.md](references/design-language.md) and [references/tokens.md](references/tokens.md) before making visual decisions.
- For the Arknights official website, its navigation/news layouts, or extraction audits, read [references/official-site.md](references/official-site.md). Distinguish observed source values, ak-ui adaptations, and unimplemented patterns.
- For entrance, stagger, count-up, media, or parallax effects, read [references/motion.md](references/motion.md).
- For working component compositions and controller setup, read [references/examples.md](references/examples.md).
- For full-page navigation, mobile menus, archive/media selectors, real resource progress or particle fields in ak-ui >=1.1.0, read [references/site.md](references/site.md). Use the public `/site` controllers or Registry `site`; do not invent an official shader or assume that CSS alone installs interactions.
- Read [references/headless-components.md](references/headless-components.md) when adapting native controls or any unstyled/headless library.
- Also read [references/reka-ui.md](references/reka-ui.md) when the project uses Reka UI or needs a Vue headless primitive.
- Read [references/quality-checklist.md](references/quality-checklist.md) before declaring the work complete.

## Inspect before changing

Determine from the project instead of asking the user when possible:

1. Framework, package manager, styling system, and existing design tokens.
2. Existing accessible primitives, headless library, and ak-ui installation.
3. Components or pages in scope and their interaction states.
4. Existing brand colors, fonts, spacing, and content hierarchy worth preserving.

Ask only when a missing product choice would materially change the result. Do not replace an existing headless library merely to use a documented example.

## Select the style intensity

Honor an explicitly requested mode:

- `accent`: Preserve the current brand and layout; add ak-ui typography, signals, focus, and restrained geometry.
- `system`: Apply the complete design language to surfaces, hierarchy, density, geometry, and states. Use this by default.
- `terminal`: Add immersive composition, asymmetric command planes, telemetry, depth, and stronger motion. Use only when requested or clearly implied because it can change page composition.

Record the chosen mode in the implementation summary. Do not interpret a mode as a color theme.

## Choose the smallest integration path

Use this order:

1. Reuse existing ak-ui CSS classes and components when they fit.
2. For a custom or headless-only surface, import `@yunyoujun/ak-ui/tokens.css` and style the existing behavior with semantic tokens.
3. For a Vue component already available in the ak-ui Registry, prefer the editable Registry adapter.
4. For missing behavior, prefer the project's existing headless primitives, then native browser semantics.
5. Add Reka UI only for Vue interactions that need its accessibility and state machinery. Do not add it for presentation-only elements.

Use the project's package manager. Keep all styling opt-in through `.ak-*`, project-owned component classes, or `data-ak-ui`; do not add global resets or overwrite unrelated elements.

## Implement the design contract

- Preserve the user's brand by mapping existing brand values to semantic `--ak-*` tokens before inventing a new palette.
- Use public ak-ui tokens for repeated decisions. Do not scatter hard-coded colors, spacing, timing, or cut sizes.
- Keep behavior, focus management, keyboard navigation, ARIA, and state in native/headless primitives. Map their rendered parts and state attributes to ak-ui styling.
- Prefer one strong geometric gesture and a clear information hierarchy over decorating every edge.
- Keep status colors functional and distinguishable. Never make color the only state indicator.
- Use original or user-provided imagery. Do not obtain, copy, or imitate game assets, logos, character art, or a specific screen composition.
- Preserve existing public APIs unless the user explicitly requests a breaking redesign.

## Apply the requested workflow

### Integrate

Install the CSS package or Registry adapter, add the narrowest import, render one representative component, and verify the import in the real build.

### Build

Establish hierarchy and responsive layout first. Compose existing primitives, add project content, then apply the selected style intensity. Avoid demo-like placeholder telemetry unless it communicates real product information.

### Extend

Write the component contract before styling: parts, states, keyboard behavior, focus ownership, and responsive constraints. Reuse or wrap existing primitives; keep presentation separate from their behavior.

### Review

Report concrete violations of the design contract, including file locations when available. Fix issues only when the user asks for implementation. Prioritize semantics, interaction loss, token drift, unreadable hierarchy, and mobile overflow over cosmetic differences.

## Verify

Run the project's relevant lint, type-check, build, and tests. When browser tooling is available, inspect desktop and mobile layouts plus keyboard focus, open/closed, selected, disabled, invalid, loading, and reduced-motion states that apply.

Do not claim visual completion from compilation alone. If browser inspection is unavailable, state that limitation and provide the remaining checks from the quality checklist.
