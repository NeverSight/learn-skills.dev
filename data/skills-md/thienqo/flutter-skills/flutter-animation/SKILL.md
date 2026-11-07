---
name: flutter-animation
description: Implement or diagnose Flutter motion with implicit, explicit, route, Hero, staggered, and physics-based animations. Use when timing, transition, or motion behavior is requested or broken; route optical materials, shaders, general layout, and performance profiling to their specialists.
---

# Flutter Animation

Use motion to explain state change, hierarchy, or continuity. Keep it interruptible and accessible.

Own timing, interpolation, sequencing, stable identity, and interruption. Route blur, glass, refraction, shader uniforms, and optical layer composition to `flutter-visual-effects`; when both apply, animation state drives the effect rather than duplicating controller ownership inside the renderer.

## Choose the mechanism

- Use implicit animation for a small number of property changes controlled by state.
- Use an `AnimationController` when timing, sequencing, repetition, interruption, or multiple values require explicit ownership.
- Use `Hero` only when the same conceptual element persists across routes and tags remain unique.
- Use custom painters or lower-level animation only when widget composition cannot express the result efficiently.
- Preserve animation controllers in the state lifecycle that owns them and dispose them correctly.

Do not animate layout-heavy properties across large subtrees without profiling. Avoid stacking unrelated implicit animations that make timing hard to reason about.

## Reduced motion

Read platform accessibility preferences through the project-compatible Flutter API. Replace nonessential motion with an immediate or low-motion transition while preserving meaning and task completion.

## Verification

Test initial, in-progress, completed, reversed, interrupted, and reduced-motion states where relevant. Check for ticker leaks and profile complex motion in profile mode on a representative device.

When motion patterns or reduced motion is in scope, follow the [motion patterns and reduced motion reference](references/motion-patterns-and-reduced-motion.md).

## Sources

- [Flutter animations](https://docs.flutter.dev/ui/animations)
- [Animation accessibility](https://docs.flutter.dev/ui/accessibility)
