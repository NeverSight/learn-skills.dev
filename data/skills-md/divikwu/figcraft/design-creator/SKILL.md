---
name: design-creator
description: "No-library mode design rules: intentional design thinking, color, typography, iconography. Extends ui-ux-fundamentals."
---

# Design Creator — No-Library Mode Rules

Every design choice must be intentional. Never rely on AI defaults.

> Extends UI/UX Fundamentals (loaded separately).
> **Scope**: No-library design decisions only.
> Layout structure, sizing defaults, auto-layout rules are handled by Quality Engine lint.

## Skill Boundaries

- Use this skill for **no-library mode design decisions** (intentional color, typography, iconography choices).
- Only loaded when no library is selected. If library is selected, use [design-guardian](../design-guardian/SKILL.md) instead.
- Extends [ui-ux-fundamentals](../ui-ux-fundamentals/SKILL.md) — that skill must also be loaded.

## Anti-Defaults

- Inter + blue + centered symmetry is the AI safe zone — if you choose it, have a reason
- Design preflight checklist (purpose/platform/language/density/tone) is enforced by `_workflow` — do not skip it

## Color

- MUST choose 1 dominant + 1 accent, total colors ≤ 5, serving the Tone
- SHOULD dominant color at 60%+, accent for key focal points
- MUST use #6B7280 (gray-500) or darker for secondary text on light backgrounds — #9CA3AF (gray-400) fails WCAG 4.5:1
- Placeholder/hint text: #9CA3AF or darker on light backgrounds (large text exception at 3:1)
- NEVER purple gradient on white background

## Typography (Creator Addendum)

- NEVER use only Inter without justification

## Iconography (Creator Addendum — no-library mode)

- NEVER use decorative icons without functional meaning
- MUST use icon_search + icon_create for all interactive indicators (chevrons, share, notifications, social logos)
- NEVER use text characters as icon placeholders (">" for chevron, "..." for more, "←" for back)
- SHOULD use a single icon set consistently (e.g., all Lucide outline)
