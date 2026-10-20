---
name: flutter-improving-accessibility
description: >
  Make Flutter UIs work with TalkBack, VoiceOver, JAWS/NVDA, large text, high
  contrast, and reduced motion. Covers Semantics, MergeSemantics,
  ExcludeSemantics, BlockSemantics, 48×48 tap targets, icon-only tooltips,
  TextScaler, MediaQuery a11y *Of getters, sort keys vs keyboard focus,
  contrast, and guideline tests. Use when the user mentions accessibility,
  a11y, semantics, TalkBack, VoiceOver, screen reader, tap target, tooltip,
  text scale, high contrast, reduce motion, or runs
  /flutter-improving-accessibility.
license: MIT
metadata:
  version: 1.0.0
  openclaw:
    requires:
      bins: ["flutter", "dart"]
---

# Flutter accessibility

Prefer built-in Material and Cupertino widgets — they already emit a TalkBack / VoiceOver / JAWS / NVDA tree. Add `Semantics` (or `Semantics.fromProperties`) only on custom painted or gestured widgets.

If this repo already has a Semantics helper, a11y test harness, labeled-control convention, or a pressable with `semanticLabel`, **extend that**. Do not wrap it in a second `Semantics(label:)` that repeats visible text.

Official: [Accessibility](https://docs.flutter.dev/ui/accessibility), [assistive technologies](https://docs.flutter.dev/ui/accessibility/assistive-technologies), [UI design and styling](https://docs.flutter.dev/ui/accessibility/ui-design-and-styling), [accessibility testing](https://docs.flutter.dev/ui/accessibility/accessibility-testing).

## References

Read `references/recipes.md` when implementing a custom control, merge/exclude/block, MediaQuery wiring, or the guideline test.

## Detect first

Search the repo for `Semantics(`, `MergeSemantics`, `ExcludeSemantics`, `BlockSemantics`, `semanticLabel`, `excludeFromSemantics`, `tooltip:`, `meetsGuideline(`, `ensureSemantics(`, `highContrastTheme`, `accessibleNavigationOf`, `textScalerOf`. Open a nearby production screen and copy that pattern.

## Hard rules

**Semantics**
- Custom paint / `GestureDetector` / `InkWell`: set `label`, a role flag (`button`, `slider`, `textField`), `tooltip` / `hint`, and `onTap` so the node is announced as a control.
- Role is a flag: `Semantics(button: true, label: 'Submit')`. Never put "button" in the label. `label` / `hint` / `tooltip` require an ambient `Directionality` or an explicit `textDirection`. Transient status: `liveRegion: true`.
- `container: true` introduces a `SemanticsNode` — use it for a distinct TalkBack/VoiceOver focus stop.

**Merge, exclude, block**
- One control + its visible `Text`: wrap both in `MergeSemantics`. Never merge two checkboxes, two tappable children, or conflicting `selected` / `checked` values.
- `ExcludeSemantics` only for decorative or redundant descendants. `Semantics(excludeSemantics: true)` replaces all child semantics with this node. Hide widgets painted behind a modal or `Drawer` with `BlockSemantics` on the overlay, not `ExcludeSemantics` on the overlay child.

**Hit targets and names**
- Every tappable target ≥ 48×48 logical pixels (`kMinInteractiveDimension`). Cupertino floor is `kMinInteractiveDimensionCupertino` (44.0). Prefer `IconButton` so the hit region stays 48 regardless of `iconSize`. Do not pass `IconButton.constraints` or compact `VisualDensity` that shrinks below 48.
- Icon-only `IconButton` / FAB: `tooltip` is a short action name. Custom icon taps: `Semantics(label: ..., button: true)`. Decorative `Icon`: `semanticLabel`. Meaningful `Image`: `semanticLabel`. Decorative `Image`: `excludeFromSemantics: true`.

**Text scale**
- Read with `MediaQuery.textScalerOf(context)` and compute sizes with `textScaler.scale(fontSize)`. Never `textScaleFactor` — deprecated and cannot represent Android 14 nonlinear scaling.
- `Text` already honors the OS font-size setting. Test every screen on a small device at the largest OS text size. `MediaQuery.withNoTextScaling` only to stop icon fonts from scaling. Never disable scaling at the `MaterialApp` root.

**MediaQuery flags**
- Call `MediaQuery.accessibleNavigationOf`, `highContrastOf`, `disableAnimationsOf`, and `textScalerOf` — not `MediaQuery.of`.
- When `accessibleNavigationOf` is true, disable timeouts or raise their minimum duration.
- When `highContrastOf` is true, set `MaterialApp.highContrastTheme` and `highContrastDarkTheme`. Wrapping a subtree in `MediaQuery(data: copyWith(highContrast: true))` does not switch those themes.
- `disableAnimationsOf` is Android Remove animations. `AnimationController` already honors `SemanticsBinding.disableAnimations`. Custom explicit animations must still read `disableAnimationsOf`. iOS Reduce Motion is `AccessibilityFeatures.reduceMotion` and does **not** set `disableAnimations`.

**Traversal**
- TalkBack/VoiceOver sibling order: `Semantics(sortKey: OrdinalSortKey(n))`. Keyboard/Tab order is a different tree: `FocusTraversalGroup` / `FocusTraversalOrder`. Do not use `sortKey` to fix Tab order.

**Contrast**
- At least 4.5:1 between text/controls and background (except disabled). 3.0:1 for large text (18pt+ regular or 14pt+ bold). Do not convey state by color alone.

**Tests and devices**
- `tester.ensureSemantics()`, then `expectLater(tester, meetsGuideline(...))`, then `handle.dispose()`. Guidelines: `androidTapTargetGuideline`, `iOSTapTargetGuideline`, `labeledTapTargetGuideline`, `textContrastGuideline`.
- Walk every changed screen with TalkBack and VoiceOver. Flutter web: `SemanticsBinding.instance.ensureSemantics()` in `main()`. Debug with `showSemanticsDebugger` or `flutter run -d chrome --profile --dart-define=FLUTTER_WEB_DEBUG_SHOW_SEMANTICS=true`.

### Samples

```dart
Semantics(
  button: true,
  label: 'Submit',
  hint: 'Sends the form',
  onTap: onSubmit,
  child: CustomPaint(painter: SubmitPainter()),
)

IconButton(
  tooltip: 'Search',
  icon: const Icon(Icons.search),
  onPressed: onSearch,
)

final TextScaler scaler = MediaQuery.textScalerOf(context);
final bool screenReader = MediaQuery.accessibleNavigationOf(context);
```

## Do not

- Wrap an already-semantic Material/Cupertino widget in `Semantics(label:)` that repeats visible text.
- Put `ExcludeSemantics` around interactive content, or use it instead of `BlockSemantics` to hide widgets behind a dialog.
- `MergeSemantics` over two checkboxes or two tappable children.
- Icon-only control with no `tooltip`, no `Semantics.label`, and no `Icon.semanticLabel`.
- `MediaQuery.of(context).textScaleFactor` or `Text(textScaleFactor:)`.
- Disable text scaling at the app root, or shrink `IconButton` below 48.
- Assume `MediaQuery(data: copyWith(disableAnimations: true))` stops `AnimationController`.
- Write the role into the label (`label: 'Submit button'`).
- Use `Semantics.sortKey` to fix keyboard Tab order.

## Fix a screen

1. Detect the existing a11y convention and reuse it.
2. Leave stock Material/Cupertino widgets unlabeled unless they are custom-painted or icon-only.
3. Give every icon-only control a `tooltip` or `Semantics(label:, button: true)`. Pad the hit target to 48, not the glyph.
4. Read `MediaQuery.*Of`. Honor largest text, high-contrast themes, screen-reader timeouts, and reduced motion.
5. Add the guideline test. Walk TalkBack and VoiceOver.

## Verify

1. `tester.ensureSemantics()` + the four `meetsGuideline` checks + `handle.dispose()` on the screen you touched.
2. Layout still fits at the OS largest text size on a small device.
3. Contrast ≥ 4.5:1 (3:1 large text); state is not color-only.
4. TalkBack and VoiceOver: every control has an intelligible name and the right role.
5. Web: semantics enabled from `main()`.
