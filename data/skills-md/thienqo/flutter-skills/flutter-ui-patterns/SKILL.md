---
name: flutter-ui-patterns
description: Build and refactor Flutter widgets, forms with stale-safe asynchronous validation and duplicate-submit handling, widget previews, component APIs, and UI state boundaries. Use alone for form behavior over existing services; add networking or concurrency only when their infrastructure changes, and route visual polish, responsive layout, navigation, animation, and performance to their specialists.
---

# Flutter UI Patterns

Build declarative interfaces whose widget tree reflects state clearly and remains easy to test.

Visual hierarchy, token selection, typography, color, surfaces, and aesthetic direction belong to `flutter-ui-design`. This skill owns implementing those decisions with maintainable widgets.

## Composition

- Extract widgets around cohesive UI concepts, reuse, isolated state, or test value—not arbitrary file length.
- Split files by responsibility, not one public widget per file. Keep small private (`_`-prefixed) widgets that only serve one screen or feature in that screen's file; give a widget its own file when it is reused, has isolated state, or is tested alone.
- Prefer immutable widget configuration and `const` constructors where valid.
- Keep side effects out of `build`; trigger them from lifecycle-safe controllers, state objects, or explicit callbacks.
- Use the project theme and semantic design tokens instead of scattered literal styles.
- Preserve platform conventions where Material and Cupertino behavior should differ.
- Give forms explicit validation, focus, submission, and error behavior.
- Keep keys stable and purposeful; do not use random or changing keys to force rebuilds.

## State boundaries

Own controllers, focus nodes, and animation controllers in the lifecycle that creates them, and dispose them there. Hoist state only when another component must coordinate it.

## Load references conditionally

- Read [forms and input](references/forms-and-input.md) when implementing validation, focus traversal, autofill, asynchronous submission, or field-error behavior.
- Read [widget previews](references/widget-previews.md) when adding or repairing Flutter Widget Previewer annotations and fixtures.

## Verification

Test meaningful rendered states and interactions. Check text scaling, keyboard input where supported, light/dark themes, and at least the smallest and largest intended form factors.

## Sources

- [Flutter UI](https://docs.flutter.dev/ui)
- [Widget catalog](https://docs.flutter.dev/ui/widgets)
- [Flutter forms cookbook](https://docs.flutter.dev/cookbook/forms)
- [Flutter Widget Previewer](https://docs.flutter.dev/tools/widget-previewer)
