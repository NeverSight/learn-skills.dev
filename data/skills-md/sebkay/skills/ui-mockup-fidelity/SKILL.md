---
name: ui-mockup-fidelity
description: "Implement website UI from mockups with high visual fidelity. Use when building or updating pages/components from mockups where layout, spacing, colors, and section backgrounds must match closely, especially in utility-first CSS workflows such as Tailwind."
---

# UI Mockup Fidelity

Implement mockups with fidelity-first execution and explicit reporting of intentional adaptations.

## Quick Start

1. Read the mockup and list every visible section, component, and state.
2. Identify repeated UI patterns before coding and choose stack-appropriate extraction points (component, partial, include, slot, variant, or primitive).
3. Apply the layout and token contract from [references/layout-token-contract.md](references/layout-token-contract.md).
4. Implement in four passes: structure, extraction, styling, review.
5. Run a manual coverage pass using [references/mockup-coverage-checklist.md](references/mockup-coverage-checklist.md).
6. Report exact matches, extracted components, intentional deviations, and unresolved ambiguities.

## Rule Tiers

Apply these tiers in order.

### Tier 1: Hard constraints

- Use `grid grid-cols-12 gap-(--grid-gap)` for layout grids by default.
- Preserve section hierarchy and component order from the mockup.
- Keep all major layout blocks present; do not drop sections silently.
- Use explicit background treatment for root and major sections.
- Extract repeated UI into reusable front-end components instead of duplicating large HTML and Tailwind blocks.
- When a pattern appears more than once, default to a shared component or variant API unless the repetition is truly incidental.

### Tier 2: Default constraints

- Use project color tokens/classes instead of ad hoc values.
- Match spacing rhythm, alignment, and proportions as closely as possible.
- Match responsive behavior implied by the mockup.
- Match typography hierarchy (size, weight, emphasis, cadence).
- Keep component APIs narrow and composable; prefer props/slots/variants over copy-pasted markup forks.

### Tier 3: Flexible constraints

- Adapt micro-spacing or decorative detail when implementation context requires it.
- Preserve visual intent when exact values are unavailable.
- Leave markup inline only when it is genuinely one-off and unlikely to repeat.

## Component Extraction Protocol

Before styling repeated UI, decide what should become a reusable unit.

- Extract when the same structure, class cluster, or interaction pattern appears in multiple places.
- Extract when a mockup implies a family of elements such as cards, stats, buttons, feature rows, nav items, badges, or section headers.
- Prefer project-native abstractions: React/Vue/Svelte components, Blade partials/components, template includes, or equivalent primitives.
- Avoid "shared" components that merely wrap a single use site; keep unique compositions local.
- If duplication remains, treat it as a deviation and explain why extraction would have been worse.

## Deviation Protocol

Never deviate silently from Tier 1 or Tier 2.

When a deviation is necessary, document it as:

- `Intentional deviation`: what changed
- `Reason`: why strict adherence was not appropriate
- `Replacement`: what was implemented instead

Only deviate when the mockup clearly demands a different approach or when project constraints conflict.

## Four-Pass Implementation

1. Structure pass:
- Build layout skeleton, section wrappers, and grid placement.
- Confirm 12-column baseline usage unless intentionally deviating.

2. Extraction pass:
- Convert repeated patterns into reusable components before finishing markup.
- Define the smallest API that covers current usage without speculative abstraction.

3. Styling pass:
- Apply tokens, backgrounds, typography, spacing, borders, and shadows.
- Match stateful elements (hover/active/focus/disabled) when shown.

4. Fidelity pass:
- Compare implemented UI against the mockup section by section.
- Check that repeated patterns are centralized rather than duplicated inline.
- Complete the coverage checklist before finalizing.

## Output Requirements

Before returning final output, provide:

- `What matches exactly`
- `What components were extracted`
- `What was adapted` (with intentional deviation entries)
- `What needs clarification`

If details are ambiguous and materially affect fidelity, ask for clarification instead of guessing.
