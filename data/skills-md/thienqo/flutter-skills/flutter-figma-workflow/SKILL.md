---
name: flutter-figma-workflow
description: Translate an explicit Figma file, frame, component, or node into production Flutter while preserving the app's design system and verifying rendered parity. Use when the request provides or names a Figma source; use flutter-ui-design instead for art direction without Figma.
---

# Flutter Figma Workflow

Treat Figma as design evidence, not generated code. Inspect the target node and the Flutter project before implementation. If Figma access is unavailable, ask for exported screens/specs or work from supplied artifacts and state the limitation; never claim to have inspected a file you could not access.

## Workflow

1. Resolve the exact frame, variants, breakpoints, states, and platform targets.
2. Extract reusable tokens, components, assets, typography, constraints, and interactions.
3. Map them to the existing Flutter theme and components before creating new primitives.
4. Implement semantic, constraint-driven Flutter structure; do not mirror every Figma layer or paste CSS coordinates.
5. Render deterministic fixtures at the reference viewport and relevant responsive sizes.
6. Compare screenshots, correct the largest hierarchy and geometry differences, then verify accessibility and interaction states.

Load [design extraction and mapping](references/design-extraction-and-mapping.md) for Dev Mode, tokens, assets, or Code Connect. Load [Flutter implementation and parity](references/flutter-implementation-and-parity.md) for layout translation and visual verification.

## Boundaries

- Use `flutter-ui-design` when the source is incomplete or the task requires new visual direction.
- Use `flutter-ui-patterns` for component structure without a Figma source.
- Add `flutter-responsive-layout`, `flutter-animation`, or `flutter-accessibility` only when those concerns are explicit.
- Preserve the repository's packages, fonts, icons, theme, and state management unless the design or task proves a change is needed.

## Sources

- [Figma Dev Mode](https://developers.figma.com/docs/plugins/working-in-dev-mode/)
- [Figma Code Connect](https://developers.figma.com/docs/code-connect/)
- [Flutter adaptive and responsive design](https://docs.flutter.dev/ui/adaptive-responsive)
