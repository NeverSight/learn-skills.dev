---
name: m3-web-flutter
description: Implement Material Design 3 in Flutter using the built-in material library with M3 theming and dynamic color. Covers theme setup, color schemes, and M3 Expressive packages. Use this when building M3-styled Flutter applications for mobile, web, or desktop.
license: Apache-2.0
---

# Material Design 3 — Flutter

## Overview

Flutter has built-in M3 support since version 3.16. The `material` library provides M3 components, dynamic color, and theming. Full M3 Expressive support is being developed as modular packages (`m3e_design`).

**Keywords**: Material Design 3, M3, Flutter, Dart, cross-platform, dynamic color, Material You, m3e_design, mobile

## When to Use

- Cross-platform mobile, web, and desktop apps using Flutter
- When you want official M3 support from Google
- Projects needing dynamic color (Material You) on Android 12+

## Setup

M3 is built into Flutter — no additional packages needed for baseline:

```dart
MaterialApp(
  theme: ThemeData(
    useMaterial3: true,
    colorSchemeSeed: const Color(0xFF6750A4),
  ),
  darkTheme: ThemeData(
    useMaterial3: true,
    brightness: Brightness.dark,
    colorSchemeSeed: const Color(0xFF6750A4),
  ),
  home: const MyApp(),
);
```

## Dynamic Color (Material You)

On Android 12+, use the device's wallpaper-based dynamic color:

```dart
import 'package:dynamic_color/dynamic_color.dart';

DynamicColorBuilder(
  builder: (ColorScheme? lightDynamic, ColorScheme? darkDynamic) {
    return MaterialApp(
      theme: ThemeData(
        colorScheme: lightDynamic ?? ColorScheme.fromSeed(
          seedColor: const Color(0xFF6750A4),
        ),
        useMaterial3: true,
      ),
      darkTheme: ThemeData(
        colorScheme: darkDynamic ?? ColorScheme.fromSeed(
          seedColor: const Color(0xFF6750A4),
          brightness: Brightness.dark,
        ),
        useMaterial3: true,
      ),
    );
  },
);
```

## Component Examples

### Buttons

```dart
FilledButton(onPressed: () {}, child: const Text('Filled')),
OutlinedButton(onPressed: () {}, child: const Text('Outlined')),
TextButton(onPressed: () {}, child: const Text('Text')),
FilledButton.tonal(onPressed: () {}, child: const Text('Tonal')),
ElevatedButton(onPressed: () {}, child: const Text('Elevated')),
```

### Cards

```dart
Card(
  elevation: 1,
  child: Padding(
    padding: const EdgeInsets.all(16),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Title', style: Theme.of(context).textTheme.titleMedium),
        Text('Content', style: Theme.of(context).textTheme.bodyMedium),
      ],
    ),
  ),
),
```

### Text Fields

```dart
TextField(
  decoration: const InputDecoration(
    labelText: 'Email',
    border: OutlineInputBorder(),
  ),
),
```

### Navigation

```dart
NavigationBar(
  selectedIndex: currentIndex,
  onDestinationSelected: (index) => setState(() => currentIndex = index),
  destinations: const [
    NavigationDestination(icon: Icon(Icons.home), label: 'Home'),
    NavigationDestination(icon: Icon(Icons.search), label: 'Search'),
    NavigationDestination(icon: Icon(Icons.settings), label: 'Settings'),
  ],
),
```

## M3 Expressive Package

```yaml
# pubspec.yaml
dependencies:
  m3e_design: ^latest
```

M3 Expressive adds enhanced shapes, motion, typography, and new components to Flutter's M3 implementation.

## Checklist

- [ ] `useMaterial3: true` set in `ThemeData`
- [ ] `colorSchemeSeed` or `ColorScheme.fromSeed` used for color generation
- [ ] Both light and dark themes defined
- [ ] Dynamic color used on Android 12+ where appropriate
- [ ] Typography uses `Theme.of(context).textTheme` for M3 type scale
- [ ] Components use Material 3 variants (e.g., `FilledButton`, not `RaisedButton`)

## Resources

- Flutter M3 guide: https://docs.flutter.dev/ui/design/material
- M3 for Flutter: https://m3.material.io/develop/flutter
- Dynamic color package: https://pub.dev/packages/dynamic_color
- M3 Expressive tracking: https://github.com/flutter/flutter/issues/168813
