---
name: motion-js
description: Build, debug, and optimize Motion animations in vanilla JavaScript. Use when the user asks for Motion/motion.dev or the `motion` package in a non-React, non-Vue context, or explicitly wants vanilla JS animation. Prioritize this skill for complex web animations (staggered reveals, scroll-linked effects, in-view triggers, hover/press gestures, motion values/effects) and migration from GSAP/WAAPI to Motion JS. Do not use for `motion/react` or framework-specific Motion APIs unless the user explicitly requests them.
---

# Motion JS

Implement Motion in plain JavaScript for DOM and SVG animation. Use this skill for `motion` and `motion/mini` APIs only. Do not switch to React APIs unless explicitly requested.

## Workflow

1. Confirm runtime context.
- Identify one of: npm/bundler imports or CMS/embed environment with locally bundled assets.
- Identify target elements and desired behavior: one-shot, gesture-driven, scroll-driven, or continuous.

2. Select the smallest runtime that still meets requirements.
- Use `motion/mini` for lightweight property/keyframe animation.
- Use `motion` (hybrid) when you need scroll/gesture helpers, sequences, SVG-specific control, or value/effect APIs.

3. Implement with the minimum API surface.
- Start with `animate`.
- Add `inView` for viewport-triggered animations.
- Add `scroll` for linked progress/parallax behavior.
- Add `hover`, `press`, or `resize` only when interaction requires it.
- Use `motionValue` pipelines when multiple effects share one source of truth.

4. Harden for production.
- Respect reduced motion preferences.
- Prefer `transform` and `opacity` over layout-heavy properties.
- Keep and call cleanup functions returned by Motion listeners.
- Avoid React-only imports (`motion/react`, `AnimatePresence`, etc.).

5. Verify behavior and constraints.
- Ensure initial styles are set before the first animation frame.
- Validate scroll/in-view targets and offsets.
- Validate keyboard and touch parity for interactive effects.

## API Selection

Use this map when choosing APIs:

- Base animation: `animate`
- Viewport triggers: `inView`
- Scroll-linked effects: `scroll`
- Gesture triggers: `hover`, `press`
- Responsive reactions: `resize`
- Value pipelines: `motionValue`, `mapValue`, `transformValue`, `springValue`
- Render sinks: `styleEffect`, `propEffect`, `attrEffect`, `svgEffect`
- Utility timing/math: `delay`, `stagger`, `spring`, `mix`, `transform`, `wrap`, `frame`

Read deeper only when needed:

- `references/api-index.md`: Full API map + official docs links
- `references/patterns.md`: Reusable vanilla recipes
- `references/performance-accessibility.md`: Performance and reduced-motion guardrails
- `references/integrations-migration.md`: CSS/CMS integrations and GSAP migration

## Motion+ and Advanced APIs

Treat `animateView`, `layout animations`, and `split text` as advanced workflows.

- Implement them when explicitly requested.
- If availability is uncertain, provide a fallback using `animate`, `inView`, and transform/opacity transitions.
- Call out assumptions when suggesting premium-only features.

## Scaffolding

Use `scripts/scaffold-motion-js.sh` to generate a minimal starter:

- `hybrid` profile for broader API surface (`motion`)
- `mini` profile for smallest runtime (`motion/mini`)
