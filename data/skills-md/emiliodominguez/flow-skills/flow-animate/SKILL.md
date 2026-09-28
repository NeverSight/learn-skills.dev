---
name: flow-animate
description: "Interface motion design, tuning and critique. Use when adding transitions or micro-interactions, or when motion feels janky, slow or distracting. Hands off to `flow-styles` or `flow-review`."
metadata:
  stage: build
---

# Animate

Motion serves the interaction. Content stays readable, input responsive, and the final state
correct when animation is reduced, interrupted, replayed or unavailable.

## Select the mode

- **Storyboard:** trigger, sequence, spatial relationship and end state, before code.
- **Dials:** a few development-only parameters when interactive tuning helps.
- **Critique:** name the concrete perceptual or interaction issue in existing motion.

Use the installed animation stack or native CSS/Web Animations. Do not add Motion, a canvas
renderer or a build dependency because a sample uses one. Check actual library versions and
official APIs when uncertain.

## Implement the sequence

1. Define trigger, duration budget, cancellation and final state. Pick a small set of timings,
   easing/spring values and amplitudes. Name reusable constants with units (`durationMs`,
   `durationSeconds`) and convert deliberately; don't abstract every one-off value.
2. Derive stagger from order/count. Use state or lifecycle-aware timelines suited to the UI;
   a single increasing stage counter is not universal.
3. Prefer transform/opacity where suitable, but measure real frame behavior and visual quality.
   Avoid layout thrashing, needless promoted layers and permanent `will-change`.
4. Handle reduced motion explicitly: Motion's supported config or hook, otherwise the media
   preference. Reduced motion still shows content, keeps feedback and completes state
   transitions without relying on an animation event.
5. Cleanup: listeners, observers, animation handles, timers and RAF loops. Handle unmount,
   navigation, rapid repeated input and interruption so stale callbacks cannot mutate new state.

## Development dials

Keep controls out of production UI using the framework/build tool's development mechanism.
In React, mount a separate development component with unconditional Hooks; never wrap Hook
calls in a conditional guard. Write tuned values back to source and remove temporary controls
unless the user wants them.

## Critique and verify

Assess hierarchy, continuity, rhythm and affordance against the intended experience; propose a
concrete before/after or parameter change, not "more polish". Run the page and check initial,
intermediate and final states, representative viewports, keyboard/pointer input, reduced
motion, replay and cancellation. Capture evidence when comparison helps. A passing build does
not prove the animation looks or behaves correctly.

## Anti-patterns

- Decorative movement that obscures reading or delays usable input.
- A hidden initial state that stays hidden if animation never completes.
- Replaying an old timeline after unmount, or assuming reduced motion is on by default.
- Framework-specific dev guards or spring fields copied into an incompatible stack.

## Done when

- Motion expresses the intended behavior and has a valid reduced/static alternative.
- Rendering, cancellation, replay and lifecycle behavior are checked where relevant.
- Tuned values, cleanup and remaining verification limits are clear.

Use `flow-styles` for related layout work or `flow-review` for implementation review.
