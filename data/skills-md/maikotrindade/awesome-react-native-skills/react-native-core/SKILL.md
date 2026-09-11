---
name: react-native-core
description: React Native core components, layout, styling, animations, lists, platform APIs, and best practices. Use when building iOS/Android UIs with native components.
metadata:
  author: maikotrindade
  version: "2026.5.0"
---

# React Native Core

> Based on React Native docs as of 2026.
>
> **See also:**
> - Ecosystem libraries (navigation, state, TanStack Query, Reanimated) → `react-native-ecosystem`
> - Expo SDK and EAS tooling → `react-native-expo`
> - Deep performance work (FPS, bundle, TTI, memory, native) → `react-native-performance`
> - React Native Testing Library deep dive → `react-native-testing`

React Native lets you build mobile apps using only JavaScript. It uses the same design as React, letting you compose a rich mobile UI from declarative components. With React Native, you build a real mobile app that's indistinguishable from an app built using Objective-C or Java.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Core Components | View, Text, Image, TextInput, ScrollView — fundamental UI building blocks | [core-components](references/core-components.md) |
| Layout with Flexbox | Flexbox layout system for positioning and aligning components | [core-layout](references/core-layout.md) |
| Styling | StyleSheet API for creating and organizing component styles | [core-styling](references/core-styling.md) |

## Features

### Animations

| Topic | Description | Reference |
|-------|-------------|-----------|
| Animated API | Built-in Animated API — timing, spring, composition (use Reanimated v3 for complex cases) | [features-animations](references/features-animations.md) |
| Easing Functions | Easing functions for custom animation curves and natural motion | [features-easing](references/features-easing.md) |

### User Interactions

| Topic | Description | Reference |
|-------|-------------|-----------|
| Touch Handling | Pressable, Touchable components, and gesture responders for handling user input | [features-touch-handling](references/features-touch-handling.md) |
| Keyboard | Keyboard API for handling keyboard events, dismissing keyboard, and KeyboardAvoidingView | [features-keyboard](references/features-keyboard.md) |

### UI Components

| Topic | Description | Reference |
|-------|-------------|-----------|
| Additional Components | Modal, Switch, ActivityIndicator, RefreshControl for dialogs, toggles, loading states | [components-ui](references/components-ui.md) |

### Data Display

| Topic | Description | Reference |
|-------|-------------|-----------|
| Lists | FlatList and SectionList for efficiently rendering large, scrollable lists | [features-lists](references/features-lists.md) |

### Styling and Theming

| Topic | Description | Reference |
|-------|-------------|-----------|
| Colors and Theming | Colors, PlatformColor, Appearance API for theming and dark mode support | [features-colors-theming](references/features-colors-theming.md) |

### Platform Integration

| Topic | Description | Reference |
|-------|-------------|-----------|
| Platform APIs | Linking, Dimensions, Platform detection, AppState, and native integrations | [features-platform-apis](references/features-platform-apis.md) |
| Network | Fetch API for HTTP requests (production apps: Axios + TanStack Query) | [features-network](references/features-network.md) |
| StatusBar | Control status bar appearance, style, and visibility | [features-statusbar](references/features-statusbar.md) |
| Share & Vibration | Native share dialog and device vibration for haptic feedback | [features-share-vibration](references/features-share-vibration.md) |
| Timers | setTimeout, setInterval, requestAnimationFrame for scheduling and delays | [features-timers](references/features-timers.md) |
| Platform-Specific APIs | Android (ToastAndroid, DrawerLayoutAndroid) and iOS (ActionSheetIOS) native patterns | [features-platform-specific](references/features-platform-specific.md) |

### Accessibility

| Topic | Description | Reference |
|-------|-------------|-----------|
| Accessibility | Screen reader support, accessibility labels, roles, and states | [features-accessibility](references/features-accessibility.md) |

### Advanced Styling

| Topic | Description | Reference |
|-------|-------------|-----------|
| Transforms | 2D and 3D transforms for rotation, scale, translation, and skew | [features-transforms](references/features-transforms.md) |

### Architecture

| Topic | Description | Reference |
|-------|-------------|-----------|
| New Architecture | Fabric, JSI, TurboModules — default since RN 0.76, what it means for your code | [features-new-architecture](references/features-new-architecture.md) |

### Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Debugging | React Native DevTools, LogBox, Dev Menu, and debugging techniques | [best-practices-debugging](references/best-practices-debugging.md) |

## Key Recommendations

- **Use `StyleSheet.create()`** for all styles instead of inline objects
- **Use FlatList** instead of ScrollView for long lists
- **Use Pressable** for new touch interactions (preferred over deprecated Touchable components)
- **Animations**: the built-in `Animated` API suffices for simple cases; use Reanimated v3 for complex or gesture-driven animations
- **Permissions**: use `react-native-permissions` for cross-platform permission handling instead of the low-level `PermissionsAndroid`
- **Handle platform differences** with `Platform.select()` and `Platform.OS`
- **Test on real devices** — simulator behavior may differ from actual devices
- **Use TypeScript** for better type safety and developer experience
- **New Architecture is default** in RN 0.76+ — Fabric, JSI, and TurboModules are active; check library compatibility
