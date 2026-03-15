---
name: animator
description: Create beautiful, performant, and accessible web animations with Motion One (motion.dev). Use when requests mention Motion One, motion.dev, WAAPI-based animation, UI micro-interactions, scroll-linked motion, staggered reveals, easing/timing tuning, animation performance optimization, or reduced-motion accessibility in vanilla JS/React/Vue apps.
---

# Animator

## Overview

Design and implement Motion One animations that feel polished, stay fast on real devices, and support accessibility constraints. Keep animations purposeful, subtle, and consistent with product intent.

Read `references/motion-one-playbook.md` for concrete patterns, timing/easing defaults, anti-patterns, and code examples.

## Workflow

1. Define animation intent and scope.
2. Choose the simplest Motion One primitive.
3. Implement with transform/opacity first.
4. Tune easing, duration, and sequencing.
5. Validate performance and accessibility.
6. Iterate on feel, then finalize.

## 1) Define Intent And Scope

State the UX purpose before writing code:
- Guide attention.
- Confirm user actions.
- Explain state change.
- Reveal hierarchy progressively.

If the animation does not support one of these goals, remove it.

## 2) Choose The Simplest Primitive

Prefer this order:
1. `animate()` for direct property transitions.
2. `stagger()` for list/sequence reveals.
3. `scroll` options for scroll-linked effects.

Avoid introducing extra tooling unless Motion One cannot cover the use case.

## 3) Implement With Compositor-Friendly Properties

Default to these properties:
- `transform` (`x`, `y`, `scale`, `rotate`)
- `opacity`

Avoid animating layout-triggering properties (`width`, `height`, `top`, `left`) unless required.

## 4) Tune Feel

Start with practical defaults:
- Interaction duration: 0.2s to 0.5s.
- Entrance: faster than exit.
- Easing: natural curves or spring behavior.
- Sequences: small stagger offsets for hierarchy.

Do not animate from `scale(0)`. Start from ~`0.95` plus opacity.
Set `transform-origin` to match perceived motion direction.

## 5) Validate Performance And Accessibility

Performance checks:
- Confirm smoothness around 60fps on representative devices.
- Inspect frame drops and long tasks with browser dev tools.
- Use `will-change` selectively for high-value elements.

Accessibility checks:
- Respect `prefers-reduced-motion`.
- Reduce duration/intensity or disable non-essential motion.
- Never rely on animation alone to convey critical information.

## 6) Finalize With Consistency

Align motion system-wide:
- Reuse a small set of easings and durations.
- Keep decorative motion secondary to functional motion.
- Limit simultaneous animated elements per viewport.

## Output Expectations

When delivering animation work, provide:
- A short rationale tying each animation to UX purpose.
- Motion One implementation snippet(s).
- Performance + reduced-motion handling notes.
- Any assumptions or device constraints.

## Reference

- `references/motion-one-playbook.md`: installation, API patterns, defaults, anti-patterns, advanced examples, and source links.
