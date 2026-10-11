---
name: flutter-motion
description: Design and implement purposeful, performant, and accessible motion in Flutter. Use for transitions, micro-interactions, gesture feedback, animated state changes, shared elements, list choreography, reduced-motion behavior, or diagnosing animation quality and performance.
---

# Flutter Motion

Use motion to explain change, causality, continuity, hierarchy, or feedback. Remove motion that communicates none of these.

## Specify

1. Name the event, property change, user value, trigger, interruption behavior, and completion state.
2. Select the least complex Flutter mechanism that satisfies it: implicit animation, `AnimatedSwitcher`, explicit controller, hero transition, custom painter, or physics simulation.
3. Define duration ranges, curve character, sequencing, gesture relationship, and reduced-motion equivalent. Read `references/motion.md`.
   For multi-domain state changes, read `references/connected-product-workflows.md` and animate only the region whose state changed.
4. Check how the motion behaves during rapid taps, navigation interruption, rebuilds, route disposal, low frame budgets, and changed accessibility settings.

## Implement

- Animate transform and opacity before layout-heavy properties when visually equivalent.
- Dispose controllers and avoid duplicated tickers.
- Preserve semantic state throughout transitions.
- Avoid delayed access to core actions.
- Keep list stagger subtle and bounded; never scale delay linearly across large collections.
- Provide immediate or cross-fade alternatives when reduced motion is requested.

## Verify

Test at normal and reduced motion, under interruption, and on the lowest relevant performance tier. Inspect frame behavior when tooling permits. Report unmeasured performance instead of assuming smoothness.
