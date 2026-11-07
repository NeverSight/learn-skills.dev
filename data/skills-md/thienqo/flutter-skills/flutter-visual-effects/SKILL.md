---
name: flutter-visual-effects
description: Implement or review advanced Flutter visual rendering such as frosted or liquid glass, backdrop blur, refraction, shaders, custom painting, glow, masks, and effect fallbacks. Use when the request explicitly needs a nontrivial visual effect; route art direction, ordinary styling, animation timing, and evidence-based performance diagnosis to their dedicated skills.
---

# Flutter Visual Effects

Translate an intended material or optical behavior into a maintainable Flutter rendering stack without treating an effect package as a design system.

## Scope

Own effect fidelity, layer composition, blur and refraction implementation, shader or `CustomPainter` selection, effect grouping, platform/backend fallbacks, and rendered effect verification.

Route whether the product should use the effect to `flutter-ui-design`. Route timing, choreography, springs, Hero, and interruption behavior to `flutter-animation`; measured jank diagnosis to `flutter-performance`; and native views or platform channels to `flutter-platform-integration`.

## Preflight

1. Inspect `pubspec.yaml`, Flutter/Dart constraints, enabled platforms, existing graphics packages, and the rendering code around the target surface.
2. Inspect the supplied reference at equivalent content, background, state, and viewport. An isolated translucent rectangle is not enough evidence for a backdrop-dependent effect.
3. State the optical behavior that matters: blur, tint, edge highlight, depth, refraction, shape blending, glow, noise, or responsive deformation.
4. Establish required platform coverage, acceptable fidelity loss, accessibility fallbacks, and whether representative hardware can be profiled.
5. Start from the project's current rendering solution and dependencies. Preserve an adequate existing effect implementation; do not replace it with core code or another package merely for stylistic preference.

## Choose by evidence, not ideology

1. Reuse an adequate solution or package already in the project, including its theme and fallback behavior.
2. Use decoration, gradients, masks, shadows, `CustomPainter`, or a clipped `BackdropFilter` for simple effects that Flutter core expresses clearly. Use `ImageFiltered` when filtering one known child rather than the existing backdrop.
3. Use a maintained package for a complex, common capability when it materially reduces implementation risk and meets the project's SDK, renderer, platform, license, maintenance, and performance constraints.
4. Use a custom fragment shader or renderer when the effect is product-specific, the accepted package cannot meet fidelity or platform requirements, or measured control is worth the maintenance cost.
5. Use native integration only when native rendering itself is a requirement; preserve a defined behavior for every other supported target.

The decision record must name the existing solution checked, why core/package/custom/native is the smallest faithful choice, and what evidence would reverse that choice. Do not add a package merely because its demo resembles the reference, and do not hand-roll mature infrastructure that an adequate maintained dependency already provides.

When an effect package or shared renderer already exists, explicitly inspect its `pubspec`/lockfile entry, source usage, theme contract, supported targets, and fallback before proposing code. Preserve a stable before fixture, compare the same content and viewport after the change, and label screenshots or profile measurements as planned versus observed. A package that is adequate on inspection should be extended in place, not replaced by a parallel renderer.

For an ordinary core-material implementation, make the decision record explicit: `BackdropFilter` samples already painted content behind the surface, `ImageFiltered` filters one owned child, no effect package is being added, and decorative layers expose neither semantics nor press, hover, or focus affordances.

## Implementation invariants

- Clip filters to the smallest useful bounds; an unbounded backdrop filter can process far more of the scene than the visible surface.
- Build glass as layers: sampled backdrop, controlled blur or refraction, tint, border/highlight, then readable content. Opacity alone is not glass.
- Keep optical effects behind semantics and hit testing. Decorative or read-only layers must not expose press, hover, focus, or interactive-glow affordances; only real controls receive them.
- Reuse or group shared effect layers where the SDK and composition allow it. Do not place an independent live blur or shader behind every scrolling row.
- Keep effect configuration semantic and centralized, with opaque or lower-cost alternatives for unsupported renderers, reduced transparency, high contrast, and constrained hardware.
- Preserve stable identity while shapes morph. The animation owner controls time; the effect layer derives its geometry and uniforms from that state.
- Never claim pixel parity with an Apple-native material. Report which transferable properties were reproduced and which native optical behaviors were approximated.

## Conditional references

- Read [iOS effect translation](references/ios-effect-translation.md) when a SwiftUI, Liquid Glass, Material, PhaseAnimator, or matched-geometry reference must be reproduced in Flutter.
- Read [shaders, packages, and performance](references/shaders-packages-performance.md) when custom GLSL, `FragmentProgram`, backdrop distortion, an effect package, renderer compatibility, or GPU cost is in scope.

## Verification

Render the effect over representative quiet and busy backgrounds in light and dark themes. Keep viewport, content, effect geometry, and interaction state equal when comparing normal, high-contrast, and opaque or low-cost fallback fixtures. Capture the interactive or morphed state where relevant. Check legibility, clipping, edge artifacts, scroll behavior, text scaling, high contrast, reduced motion, and the available reduced-transparency path.

Golden tests can lock deterministic geometry and paint output, but device screenshots are required for claims involving platform compositing, system chrome, or backend-specific shaders. Profile nontrivial blur, shader, or continuously animated effects in profile mode on representative hardware; report the tested renderer, device class, scene, and fallback rather than generalizing from debug mode.

## Sources

- [Custom drawing and graphics](https://docs.flutter.dev/ui/design/graphics)
- [Writing and using fragment shaders](https://docs.flutter.dev/ui/design/graphics/fragment-shaders)
- [BackdropFilter](https://api.flutter.dev/flutter/widgets/BackdropFilter-class.html)
- [ImageFilter](https://api.flutter.dev/flutter/dart-ui/ImageFilter-class.html)
