---
name: design-guardian
description: "Library mode design rules: token priority, typography, spacing, elevation, dark mode, conflict resolution. Extends ui-ux-fundamentals."
---

# Design Guardian — Library Mode Rules

Prefer library styles and tokens. Use what exists, skip what doesn't — never let incomplete specs limit design quality.

> Extends UI/UX Fundamentals (loaded separately).
> **Scope**: Library-specific design direction only.
> Layout structure, sizing defaults, auto-layout rules are handled by Quality Engine lint.

## Skill Boundaries

- Use this skill for **library mode design decisions** (token priority, component instances, dark mode).
- Only loaded when a library is selected. If no library, use [design-creator](../design-creator/SKILL.md) instead.
- Extends [ui-ux-fundamentals](../ui-ux-fundamentals/SKILL.md) — that skill must also be loaded.

## Spec Priority

- MUST use component instances (`type:"instance"`) when a matching component exists; hand-built frame+text is only acceptable when no matching component is found
  - **Library mode**: use `componentKey`/`componentSetKey` from `libraryComponents`
  - **Local mode**: use `componentId` (node ID) from `localComponents`
- MUST match colors/fonts/spacing/radii to Style/Variable first; when no match exists, skip binding and choose freely
- SHOULD use primary for focal points, secondary for supporting, tertiary for background; exercise restraint — don't use every available token
- When selecting components, check `containingFrame` to verify category (e.g., "Forms" vs "Avatars") — property names like "Placeholder"/"Size" appear across unrelated component types

## Typography (Library Addendum)

- MUST use library text styles for heading/body distinction

## Spacing (Library Addendum)

- MUST use library spacing tokens when available; fall back to 4px-grid spacing scale

## Elevation (Library Addendum)

- SHOULD prefer library effect styles when available

## Dark Mode (Library Addendum)

- When library has light/dark mode variable collections, MUST bind color fills to mode-aware variables (not hardcoded hex)
- SHOULD verify both modes produce adequate contrast (≥ 4.5:1) by checking light AND dark values
- NEVER hardcode colors that only work in one mode — always use variables that resolve per-mode

## Conflict Resolution

When user request conflicts with library tokens:
1. **Library token wins** for color, typography, spacing, radius — use the closest available token
2. **User intent wins** for layout, content, tone — these are not constrained by tokens
3. If no token matches at all, create without binding and add a note: "No matching library token — hardcoded value used"
