---
name: react-native
description: |
  React Native with Expo framework for building native mobile apps on Android, iOS, and web from a single TypeScript codebase. Covers Expo Router file-based navigation (stack, tabs, drawer), EAS Build/Submit/Update for CI/CD and OTA updates, expo-dev-client for custom development builds, Expo Modules API for native Swift/Kotlin modules, core RN patterns (StyleSheet, FlatList, Platform-specific code), native device APIs (camera, notifications, haptics), and NativeWind for Tailwind CSS styling.

  Use when building React Native apps with Expo, configuring Expo Router navigation, setting up EAS Build pipelines, implementing OTA updates, creating native modules, or integrating device APIs like camera and push notifications.
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://docs.expo.dev'
user-invocable: false
---

# React Native with Expo

## Overview

Expo is an open-source framework for building universal native apps with React Native from a single TypeScript codebase. It provides file-based routing (Expo Router), cloud build services (EAS Build/Submit/Update), and a rich set of native modules for device APIs.

**When to use:** Mobile apps targeting iOS and Android, universal apps with web support, projects needing OTA updates, apps requiring native device APIs (camera, notifications, haptics), teams preferring managed infrastructure over bare React Native.

**When NOT to use:** Apps requiring heavy custom native code incompatible with Expo Modules API, brownfield integration into existing native apps, apps with native-only CI/CD requirements.

## Quick Reference

| Pattern           | API                                  | Key Points                                  |
| ----------------- | ------------------------------------ | ------------------------------------------- |
| Stack navigation  | `<Stack>` from `expo-router`         | File-based, `_layout.tsx` defines navigator |
| Tab navigation    | `<Tabs>` from `expo-router`          | `(tabs)` directory group with `_layout.tsx` |
| Drawer navigation | `<Drawer>` from `expo-router/drawer` | Requires `@react-navigation/drawer`         |
| Typed routes      | `href` with `/(group)/route`         | Enable `typed-routes` in `app.json`         |
| Dev build         | `expo-dev-client`                    | Custom native code + dev tools              |
| EAS Build         | `eas build --profile production`     | Cloud builds for app stores                 |
| EAS Submit        | `eas submit -p ios` / `-p android`   | Automated store submission                  |
| OTA Update        | `eas update --branch production`     | JS-only updates, no rebuild needed          |
| Native module     | Expo Modules API                     | Swift/Kotlin with `expo-module.config.json` |
| Platform code     | `Platform.select()` / `.ios.tsx`     | Per-platform logic or entire files          |
| Styled lists      | `FlatList` / `FlashList`             | Virtualized, `keyExtractor` required        |
| Camera            | `expo-camera`                        | Permissions via `useCameraPermissions()`    |
| Notifications     | `expo-notifications`                 | Push tokens via `getExpoPushTokenAsync()`   |
| Haptics           | `expo-haptics`                       | `impactAsync`, `notificationAsync`          |
| Tailwind (RN)     | NativeWind v4                        | `className` prop, Tailwind CSS in RN        |

## Common Mistakes

| Mistake                                                  | Correct Pattern                                               |
| -------------------------------------------------------- | ------------------------------------------------------------- |
| Using `react-navigation` directly instead of Expo Router | Expo Router wraps React Navigation with file-based routing    |
| Forgetting `_layout.tsx` in route directories            | Every directory with routes needs a layout file               |
| Using `expo start` for custom native code                | Use `expo start --dev-client` with `expo-dev-client`          |
| Running `eas update` after native dependency changes     | Native changes require `eas build`, OTA is JS-only            |
| Hardcoding platform checks with `if`                     | Use `Platform.select()` or platform-specific file extensions  |
| Not requesting permissions before accessing device APIs  | Always check/request permissions before camera, notifications |
| Using `ScrollView` for long lists                        | Use `FlatList` or `FlashList` for virtualized rendering       |
| Inline styles in render functions                        | Define styles with `StyleSheet.create()` outside component    |
| Missing `keyExtractor` on `FlatList`                     | Always provide `keyExtractor` for stable list rendering       |
| Importing from `react-native` for Expo-provided APIs     | Prefer `expo-*` packages over `react-native` equivalents      |

## Delegation

- **Pattern discovery**: Use `Explore` agent
- **Build/deployment review**: Use `Task` agent
- **Code review**: Delegate to `code-reviewer` agent

> If the `react-patterns` skill is available, delegate React component patterns and hooks to it.
> If the `tanstack-query` skill is available, delegate data fetching and caching to it.
> If the `zustand` skill is available, delegate client-side state management to it.
> If the `vitest-testing` skill is available, delegate unit and component testing patterns to it.
> If the `tailwind` skill is available, delegate Tailwind CSS utility patterns to it (NativeWind uses Tailwind CSS syntax).
> If the `accessibility` skill is available, delegate mobile accessibility patterns to it.

## References

- [Core patterns: StyleSheet, FlatList, Platform-specific code](references/core-patterns.md)
- [Expo Router navigation: stack, tabs, drawer, typed routes](references/expo-router.md)
- [EAS Build, Submit, and Update workflows](references/eas-workflows.md)
- [Dev client and native modules with Expo Modules API](references/native-modules.md)
- [Device APIs: camera, notifications, haptics](references/device-apis.md)
- [NativeWind Tailwind CSS integration](references/nativewind.md)
- [App configuration and environment setup](references/app-configuration.md)
- [Performance optimization patterns](references/performance-patterns.md)
