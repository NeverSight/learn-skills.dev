---
name: react-native-expo
description: Build and maintain React Native apps with Expo SDK, EAS Build, EAS Update, and Continuous Native Generation. Use when configuring Expo projects, adding native modules, building binaries, or shipping over-the-air updates.
metadata:
  author: Hairy
  version: "2026-02-26"
  source: Generated from https://github.com/expo/expo, scripts located at https://github.com/hairyf/skills
---

> The skill is based on Expo SDK (docs from expo/expo repo), generated at 2026-02-26.

Expo provides tooling and services for React Native: app config and Prebuild (Continuous Native Generation), Expo SDK packages, development builds, EAS Build (cloud builds and internal distribution), and EAS Update (over-the-air JS updates). Use development builds for production apps; Expo Go is a limited playground.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| App config | app.json, app.config.js/ts, dynamic config, reading in app | [core-config](references/core-config.md) |
| Development workflow | Dev loop, development builds vs Expo Go, when to rebuild | [core-development-workflow](references/core-development-workflow.md) |
| Development and production modes | __DEV__, --no-dev --minify, when to use each | [core-development-mode](references/core-development-mode.md) |
| Metro | metro.config.js, resolver, transformer, cache, env vars | [core-metro](references/core-metro.md) |
| Logging | Console in terminal, native logs, log-android / log-ios | [core-logging](references/core-logging.md) |
| CNG and Prebuild | npx expo prebuild, --clean, EAS Build and native dirs | [core-continuous-native-generation](references/core-continuous-native-generation.md) |

## Features

### Expo SDK and native code

| Topic | Description | Reference |
|-------|-------------|-----------|
| Expo SDK and third-party libs | Install with npx expo install, compatibility, config plugins | [features-expo-modules](references/features-expo-modules.md) |
| expo-constants | App manifest, build info, system constants, extra/env at runtime | [features-sdk-constants](references/features-sdk-constants.md) |
| expo-image | Performant image component, caching, BlurHash/ThumbHash, contentFit | [features-sdk-image](references/features-sdk-image.md) |
| expo-file-system | File and directory API, Paths.cache/document, read/write, download | [features-sdk-filesystem](references/features-sdk-filesystem.md) |
| expo-secure-store | Encrypted key-value store, optional biometric auth | [features-sdk-secure-store](references/features-sdk-secure-store.md) |
| Config plugins | Use and write plugins to modify AndroidManifest, Info.plist during prebuild | [features-config-plugins](references/features-config-plugins.md) |
| Native modules | Expo Modules API, local module, config plugin for native config, lifecycle | [features-native-modules](references/features-native-modules.md) |

### EAS Build and Submit

| Topic | Description | Reference |
|-------|-------------|-----------|
| EAS Build | Cloud builds, eas.json profiles, development/preview/production | [features-eas](references/features-eas.md) |
| EAS Submit | Submit to Google Play and App Store (TestFlight), eas.json, CI | [features-eas-submit](references/features-eas-submit.md) |

### Development experience

| Topic | Description | Reference |
|-------|-------------|-----------|
| iOS Simulator and Android emulator | Setup, npx expo start + i/a, limitations, troubleshooting | [features-simulators-emulators](references/features-simulators-emulators.md) |

### Updates and versioning

| Topic | Description | Reference |
|-------|-------------|-----------|
| expo-updates and EAS Update | OTA updates, runtime version, channels | [features-updates](references/features-updates.md) |
| Upgrading Expo SDK | Incremental upgrade, npx expo install --fix, expo-doctor | [features-versioning](references/features-versioning.md) |

## Best practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Debugging | Dev vs production errors, native logs, reproducing crashes | [best-practices-debugging](references/best-practices-debugging.md) |
| Common development errors | Metro, AppRegistry, SDK version, version mismatch, caches | [best-practices-common-errors](references/best-practices-common-errors.md) |
