---
name: flutter-custom-design-system
description: >
  Implement Flutter UI against a project-owned design system instead of stock
  Material 3 / Cupertino chrome. Covers ThemeExtension tokens, 1:1 token
  discipline, a house Pressable that replaces ink ripples, branded type/spacing,
  and detecting an existing system before inventing a new one. Use when the app
  has custom tokens, a *Pressable, a ThemeExtension, Figma/CSS token files, or
  the user says custom design system, branded UI, no Material look, no ripple;
  or when they run /flutter-custom-design-system.
license: MIT
metadata:
  version: 1.0.0
  openclaw:
    requires:
      bins: ["flutter", "dart"]
---

# Flutter custom design system

Stock Material/Cupertino skills are the wrong default here. If this repo already named colors, type, radius, motion, or a pressable, **use those names and values**. Do not restyle the app toward `FilledButton` / `NavigationBar` / `ColorScheme.fromSeed` unless the user asked to throw the system away.

Companion skill: `flutter-native-ui` — only for apps that actually want Material 3 or Cupertino chrome.

## References

```
references/
  tokens.md      ThemeExtension mount, context accessor, 1:1 rule
  pressable.md   Scale/sink press, NoSplash, focus ring, semantics
```

## Detect the system first

Before writing a widget, search the repo for:

- `ThemeExtension<`
- `extension <Name> on BuildContext` that returns colors/tokens
- files named `*tokens*`, `*semantics*`, `*theme*`, `WIDGETS.md`, `DESIGN-SYSTEM.md`
- a widget named `*Pressable`
- `NoSplash.splashFactory` / `splashFactory: NoSplash`

Then open a nearby production screen and copy its accessor (`context.pt`, `St6Theme.of(context)`, `context.colors`, …). Product code must use that accessor, not a new one.

No system yet, and the user wants one: install the pattern in `references/tokens.md` and `references/pressable.md`. One token module, one extension, one pressable. Do not add a third-party UI kit.

## Hard rules

**Tokens**
- Values live in **one** source (Dart token file, generated from CSS/JSON, or a signed-off `tokens.dart`). Widgets never contain raw hex, magic radii, or ad-hoc durations.
- Runtime mount is a `ThemeExtension<T>` on `ThemeData.extensions`, plus a single context accessor. Do not import a `FooColors` class into random widgets beside the extension.
- 1:1 with the system file. If the handoff says `#C9A24B`, the token is `#C9A24B`. Do not “improve” contrast, invent a light theme, or add roles the system does not name.
- Missing role: add it to the token source and the extension together, or ask. Never `#hex` in the widget as a shortcut.
- Dark mode only exists if the system shipped it. Do not invent a dark palette.

**Chrome**
- A stranger should not be able to tell the app is default Flutter Material. No ink ripples, no M3 primary-container pills, no stock `NavigationBar` indicator, unless the system specifies them.
- Every tap goes through the house `Pressable` (create it if the repo has none). Press = scale and/or sink. `splashFactory: NoSplash.splashFactory` and transparent overlays on the theme and on the pressable.
- Do not wrap branded controls in `FilledButton` / `ElevatedButton` / `InkWell` “to get accessibility for free” and then fight the splash. Put semantics on the pressable.
- Use Material **behavior** (focus, media query, text scaler, `Shortcuts`) without Material **look**.

**Type and space**
- Type roles come from the system (or the extension’s text styles), not `TextTheme.of(context).titleLarge` unless the system mapped onto `TextTheme`.
- Spacing, radius, and motion come from token numbers (`space200`, `radiusControl`, `durationPress`). No `EdgeInsets.all(13)` and no `Duration(milliseconds: 180)` invented at the call site.

**Keys and debug**
- Interactive controls: `const ValueKey<String>('kebab-name')` so tests can `find.byKey`.
- God-mode, galleries, prefills, jump chips: `kDebugMode` only, and they still go through the real auth/session path. No release backdoors.

**Do not**
- Add `google_fonts` if the system already vendors faces. If goldens matter, load those faces with `FontLoader` — Roboto goldens are not the product.
- Add `flutter_screenutil`, GetX, or a second design package.
- Mix stock M3 components onto a branded surface “just this once.”

## Build a screen

1. Read the token file, the extension, the pressable, and one existing screen.
2. Scaffold with the project’s shell (custom app bar / tab bar), not a fresh `AppBar` + `NavigationBar`.
3. Color, type, space, radius, motion: extension/tokens only.
4. Taps: house pressable. Icons: the system’s icon set, not `Icons.favorite` unless that is the system.
5. Safe area and keyboard: `SafeArea` on content, `MediaQuery.sizeOf` / `viewInsetsOf` / `textScalerOf`. Window width breakpoints if the system defines them; otherwise keep the existing shell’s rule.
6. Verify with the project’s analyzer and a running frame.

## When to refuse Material defaults

Refuse these on a branded surface unless the system’s widget inventory lists them:

`FilledButton`, `NavigationBar`, `NavigationRail`, `NavigationDrawer`, `SnackBar` (if the system has a toast), `FloatingActionButton`, `Chip`, `Card`, `Material` with elevation tint, `InkWell` with default splash.

OS-native affordances that are not chrome may still use `.adaptive()` (`Switch.adaptive`, `Checkbox.adaptive`) when the system does not specify a replacement.

## Verify

1. `grep` the files you touched for `Color(0x` / `Color.from` / `#`. Hits belong in the token file, not the widget.
2. Every new tap target goes through the house pressable.
3. Analyzer clean. Hot reload. Confirm the running frame against a nearby branded screen, not against Material 3 gallery memory.
4. Widget tests use `find.byKey`, not visible copy, when a key exists.
