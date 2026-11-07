---
name: flutter-ui-design
description: Design or visually transform Flutter interfaces with a deliberate art direction, distinctive product identity, coherent tokens, complete states, and rendered visual proof. Use for UI/UX design, redesign, reference-driven parity, or when a screen feels generic or unfinished; route widget architecture and responsive mechanics to their dedicated skills.
---

# Flutter UI Design

Create coherent, platform-aware Flutter interfaces that feel authored for the product rather than assembled from framework defaults.

## Scope

Own art direction, visual ambition, hierarchy, composition, semantic tokens, typography, color, surfaces, shape, state presentation, and rendered visual review.

Route implementation structure, reusable widget APIs, forms, and UI state ownership to `flutter-ui-patterns`. Route constraint mechanics to `flutter-responsive-layout`, motion implementation to `flutter-animation`, advanced blur, refraction, shader, or custom optical rendering to `flutter-visual-effects`, accessibility compliance to `flutter-accessibility`, and navigation behavior to `flutter-navigation`.

## Preflight

Before proposing a redesign:

1. Inspect `pubspec.yaml`, supported platforms, nearby screens, assets, fonts, and any supplied references.
2. Find existing `ThemeData`, `ColorScheme`, `TextTheme`, component themes, `ThemeExtension`s, and design-system widgets.
3. Preserve the established brand and component vocabulary unless the request explicitly authorizes a redesign.
4. Inspect the current screen at a representative viewport when the project is runnable. Source alone is insufficient evidence of its visual baseline.
5. Do not add a UI package, font, icon set, or competing theme merely because it is familiar.

## Design workflow

1. State the screen's primary user task and the visual failure in observable terms.
2. Classify the assignment as preservation, refinement, visible transformation, or reference parity. Match the requested ambition; do not answer a visible-redesign request with a barely changed safe default.
3. Define a concise design signature covering background, surface treatment, type character, accent behavior, shape language, motion, and content voice. Each choice must support the same product idea.
4. Establish or extend semantic tokens before styling individual widgets. Treat the project's existing tokens and shared components as the source of truth; extend them only when the product is missing a stable semantic concept, not to rename or duplicate the current system.
5. Compose a representative populated screen around realistic copy and data, including at least one long-content fixture that exercises wrapping or truncation, then cover the relevant empty, loading, failure, offline, stale, disabled, and interaction states. For every actionable state, choose one primary recovery or progression action; do not leave alternatives such as “retry or dismiss” unresolved in a concrete state matrix. Do not seed production data merely to make a screenshot attractive.
6. Implement through the existing theme and component system. Prefer Flutter core primitives when they can express the direction without a new dependency. Add no second theme system, font, icon pack, or UI dependency unless the brief or inspected project evidence requires it.
7. Render the same fixtures before and after. Critique hierarchy, identity, density, default-widget residue, state quality, and reference gaps, then perform another implementation pass for material issues.

## Design rules

- Use typography, spacing, alignment, and grouping before adding decoration.
- Give each surface one clear primary action. Keep secondary actions visibly subordinate.
- Do not turn every content group into a card; use whitespace and dividers when elevation adds no meaning.
- Distinctive does not mean maximalist. Use gradients, translucency, blur, glow, expressive shape, or depth when they are part of the chosen signature, and keep them subordinate to content.
- Audit the result for framework-default residue. Stock widgets are valid behavior primitives, but their untouched appearance must not dominate a screen whose brief calls for a recognizable visual identity.
- Keep color, type, spacing, shape, iconography, and elevation on a small semantic system.
- Use realistic content; placeholder text often hides hierarchy and overflow problems.
- Pair ambiguous icons with labels or other context.
- Preserve brand identity while adapting controls, gestures, density, and navigation conventions to the target platform.
- When a polished reference or sibling native app is supplied, match its visual ambition and product relationships before adapting platform mechanics. Do not reduce an expressive reference to generic Material merely to avoid imitation.

## Load references conditionally

- Read [art direction](references/art-direction.md) when the request is open-ended, asks for a visible transformation, says the UI feels generic, or supplies a polished reference.
- Read [visual foundations](references/visual-foundations.md) when selecting or extending tokens, typography, color, shape, iconography, or elevation.
- Read [screen composition](references/screen-composition.md) when establishing hierarchy or redesigning a full screen.
- Read [states and feedback](references/states-and-feedback.md) when the interface loads data, accepts input, fails, or needs interaction polish.
- Read [platform adaptation](references/platform-adaptation.md) when targeting more than one platform or translating an iOS, Android, web, or desktop reference.
- Read [visual verification](references/visual-verification.md) before claiming the redesign is complete.

## Verification

Capture stable screenshots or golden fixtures for representative states and form factors. For a visible redesign, include at least one populated primary state and the most important edge state. Define an explicit verification matrix that names light and dark themes, normal and enlarged text scales, actual contrast checks for custom foreground/background pairs, and representative compact and wide form factors; add localization, pointer or keyboard focus, and platform-specific controls where relevant. Do not assume framework defaults make custom combinations accessible. Test behavior separately from appearance.

If the runnable project or required assets are not supplied, define the smallest representative fixture matrix and state what must be rendered later; do not claim visual verification from a design proposal or source text alone.

Do not stop after the first successful render. Compare it with the baseline and any supplied reference, fix material visual gaps, and capture the accepted result. Report observable improvements—such as stronger product identity, clearer action priority, less default-widget residue, intentional density, and complete state coverage—instead of claiming that a screen is simply “beautiful.”

## Sources

- [Material Design for Flutter](https://docs.flutter.dev/ui/design/material)
- [Use themes to share colors and font styles](https://docs.flutter.dev/cookbook/design/themes)
- [Platform adaptations](https://docs.flutter.dev/ui/adaptive-responsive/platform-adaptations)
- [Adaptive and responsive design](https://docs.flutter.dev/ui/adaptive-responsive)
- [Typography](https://docs.flutter.dev/ui/design/text/typography)
