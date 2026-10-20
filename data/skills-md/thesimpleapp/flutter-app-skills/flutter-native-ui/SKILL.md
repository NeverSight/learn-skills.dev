---
name: flutter-native-ui
description: >
  Build native-feeling Flutter screens with Material 3 and Cupertino. Covers
  theming, adaptive controls, go_router, SafeArea/MediaQuery, slivers, sheets,
  animations, icons, and platform conventions grounded in current Flutter
  stable docs (3.47+ / Dart 3.13+). Use when building Flutter UI, widgets,
  themes, navigation, screens, lists, forms, dialogs, or sheets; when making
  an app feel native on iOS or Android; or when the user runs /flutter-native-ui.
  If the project already has a custom ThemeExtension / house Pressable / branded
  token file, use flutter-custom-design-system instead of restyling to Material.
license: MIT
metadata:
  version: 1.0.0
  openclaw:
    requires:
      bins: ["flutter", "dart"]
---

# Flutter Native UI

Ground every UI choice in current Flutter and Dart docs, not React Native or Expo patterns. Check `flutter --version`. Official sources: [docs.flutter.dev](https://docs.flutter.dev), [api.flutter.dev](https://api.flutter.dev), [dart.dev](https://dart.dev), [m3.material.io](https://m3.material.io), [pub.dev](https://pub.dev) packages from `flutter.dev`.

If the project already has a design system, tokens, or router, extend those. Do not invent a second theme or a second navigator.

If widgets read a house `ThemeExtension`, a branded token file, or a `*Pressable` instead of Material ink, stop and follow `flutter-custom-design-system`. Do not "fix" that app toward stock Material 3.

## References

Read only the file you need:

```
references/
  navigation.md      go_router, tabs, sheets, dialogs, transitions
  theming.md         ColorScheme, TextTheme, light/dark, Cupertino
  layout.md          SafeArea, MediaQuery.*Of, breakpoints, slivers
  controls.md        Adaptive constructors, buttons, fields, pickers
  animations.md      Implicit first, Hero, M3 motion, lists
  icons-and-media.md Icons.adaptive, images, camera, audio, video
  visual-effects.md  Elevation, blur, gradients
  storage.md         Preferences, secure storage, files, SQL
```

## Design system

Pick one app chrome and stay on it.

| Product | Root | Chrome |
| --- | --- | --- |
| Cross-platform (default) | `MaterialApp` / `MaterialApp.router` | Material 3 + `.adaptive()` controls |
| iOS-first | `CupertinoApp` / `CupertinoApp.router` | Cupertino widgets + HIG spacing |
| Existing app | Whatever it already uses | Do not restyle the whole app to prove a point |

Flutter auto-adapts **OS behavior** (scroll physics, back gesture, text editing, haptics). It does **not** auto-swap tab bars, app bars, or information architecture. That is an explicit choice. See [platform adaptations](https://docs.flutter.dev/ui/adaptive-responsive/platform-adaptations).

Do not mix Material and Cupertino widgets on the same surface except `.adaptive()` constructors and `Icons.adaptive`.

Material 3 is the default since Flutter 3.16. Never set `useMaterial3: false`. Never pass `useMaterial3: true` as if it were an opt-in.

## Imports (Flutter 3.47+)

Material and Cupertino shipped as standalone 1.0 packages: `material_ui` and `cupertino_ui`. The SDK copies still work in 3.47 and are scheduled for deprecation in the Fall 2026 stable.

- **Existing project:** keep the import style already in the tree.
- **New 3.47+ app, or when asked to migrate:**

```bash
flutter pub add material_ui
# only if you build Cupertino chrome:
flutter pub add cupertino_ui
dart fix --apply --code=migrate_design_widgets
```

That rewrites `package:flutter/material.dart` → `package:material_ui/material_ui.dart` and `package:flutter/cupertino.dart` → `package:cupertino_ui/cupertino_ui.dart`.

If `pubspec.yaml` does not update, run `flutter pub add material_ui` (and `cupertino_ui`) then `dart fix --apply` again.

Legacy package widgets that still import the SDK libraries need a bridge:

```dart
MaterialApp(
  builder: (context, child) => MaterialUiCompatibilityBridge(child: child!),
)
```

Localizations: `localizationsDelegates: GlobalMaterialLocalizations.delegates` from `material_ui` (includes Cupertino + Widgets). Do not keep `flutter_localizations` `GlobalMaterialLocalizations` / `GlobalCupertinoLocalizations` after migrating.

## Build a screen

1. Read the existing theme, router, and a nearby screen. Copy those conventions.
2. Choose the scaffold: `Scaffold` + `AppBar` / `SliverAppBar` (Material) or `CupertinoPageScaffold` + `CupertinoNavigationBar` / `CupertinoSliverNavigationBar` (Cupertino).
3. Put the **page title in the app/nav bar**, not a custom `Text` at the top of the body.
4. Inset content with `SafeArea` around the **body**, not the whole `Scaffold` (`AppBar` already draws under the status bar). Nested `SafeArea`s collapse; do not add padding by reading `MediaQuery.padding` yourself.
5. Scrollable pages: `CustomScrollView` + slivers, or `ListView.builder`. Forms: `ListView` / `CustomScrollView`, not a bare `Column` that overflows.
6. Color and type come from `ColorScheme.of(context)` and `TextTheme.of(context)`. No raw `Colors.blue`, no one-off `fontSize: 13`.
7. Interactive controls get `const ValueKey<String>('kebab-name')`.
8. After edits: hot reload, then verify (see Verify).

## Hard rules

**Theme and color**
- Build schemes with `ColorScheme.fromSeed`. Pair `theme` + `darkTheme` + `themeMode`.
- Read tokens via `ColorScheme.of(context)` and `TextTheme.of(context)` (same as `Theme.of(context).colorScheme` / `.textTheme`).
- Use M3 roles: `primary`/`onPrimary`, `surface`/`onSurface`, `surfaceContainer*`, `outline`, `error`. Not `primarySwatch`, not `accentColor`.
- Cupertino color is `CupertinoColors` / `CupertinoDynamicColor`, resolved with `CupertinoDynamicColor.resolve(color, context)`.

**Layout**
- `MediaQuery.sizeOf` / `paddingOf` / `viewInsetsOf` / `viewPaddingOf` / `textScalerOf` / `platformBrightnessOf` / `highContrastOf` / `accessibleNavigationOf`. Never `MediaQuery.of(context).size` (rebuilds on every MediaQuery change).
- `Row`/`Column`/`Flex` `spacing` for gaps. `Wrap` `spacing` + `runSpacing`. Do not sprinkle `SizedBox` between every child.
- Window size, not device type. Never `Platform.isIOS` to pick a phone vs tablet layout. Never `OrientationBuilder` at the app root. Breakpoints: compact `<600`, medium `600–839`, expanded `≥840` ([M3 window size classes](https://m3.material.io/foundations/layout/applying-layout/window-size-classes)).
- Do not lock orientation. Do not use `flutter_screenutil` or design-px scalers.

**Widgets (new code)**

| Use | Do not use |
| --- | --- |
| `FilledButton`, `FilledButton.tonal`, `OutlinedButton`, `TextButton` | `ElevatedButton` as the primary action, `RaisedButton`, `FlatButton` |
| `NavigationBar` + `NavigationDestination` | `BottomNavigationBar` |
| `NavigationRail` / `NavigationDrawer` on large widths | A stretched phone nav bar on desktop |
| `SegmentedButton` | `ToggleButtons` |
| `DropdownMenu` | `DropdownButton` / `DropdownButtonFormField` |
| `MenuAnchor` / `MenuBar` | `PopupMenuButton` for new menus |
| `SearchAnchor` / `SearchBar` | A homemade search `TextField` in the app bar |
| `Card.filled` / `Card.outlined` | Random `Container` + `BoxShadow` cards |
| `ListView.builder` / slivers | `ListView(children: hugeList)` |
| `Switch.adaptive`, `Slider.adaptive`, `Checkbox.adaptive`, `Radio.adaptive`, `CircularProgressIndicator.adaptive`, `RefreshIndicator.adaptive`, `AlertDialog.adaptive`, `showAdaptiveDialog` | Platform-blind Material controls for those OS-native affordances |

**Navigation**
- New multi-screen apps: `go_router` + `MaterialApp.router` / `CupertinoApp.router`. Official docs do **not** recommend `MaterialApp.routes` named routes.
- Existing `Navigator.push` apps: keep `Navigator` unless asked to migrate.
- Tabs that must keep per-tab stacks: `StatefulShellRoute.indexedStack`.
- Sheets and dialogs stay pageless (`showModalBottomSheet`, `showAdaptiveDialog`). Do not make every popup a GoRoute unless it must be deep-linkable.
- Full-screen modal: `fullscreenDialog: true` (iOS present) or a `GoRoute` with that page flag.

**Dart / widgets**
- `const` constructors. Small widgets over one 400-line `build`.
- File names `snake_case.dart`. Types `PascalCase`. Interactive keys kebab-case strings.
- `SelectableText`, or a `SelectionArea` ancestor, for values the user may copy.
- Tabular numbers: `fontFeatures: const [FontFeature.tabularFigures()]`.
- Debug-only jump chips and prefills stay behind `kDebugMode` and still go through the real auth path.
- Do not add GetX, `flutter_screenutil`, FontAwesome-for-chrome, or a new state-management package to ship a screen.

**Do not copy Expo/RN habits**
- No `StyleSheet`, `process.env.EXPO_OS`, `SafeAreaView`, CSS `boxShadow`, or kebab-case source files.
- No `flex: 1` style maps — use `Expanded` / `Flexible`.
- No SF Symbols via `expo-image`. Use `Icons.adaptive` / `CupertinoIcons`.

## Verify

UI work is not done when the edit applies.

1. Analyzer clean on the files you touched (`dart analyze` / `flutter analyze`).
2. Hot reload the running app. Hot restart if you changed `main`, routes, or global theme.
3. Look at the running frame (screenshot, widget preview, or the project's visual loop). A stale frame is not evidence.
4. Isolated widgets: `@Preview` from `package:flutter/widget_previews.dart` (stable in 3.47). See [Widget Previewer](https://docs.flutter.dev/tools/widget-previewer).
5. Check the empty, loading, error, and keyboard-open states of the screen you changed — and any other route that reads the same state.
