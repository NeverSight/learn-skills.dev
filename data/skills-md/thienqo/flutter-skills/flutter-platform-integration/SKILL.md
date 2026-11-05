---
name: flutter-platform-integration
description: Implement or review Flutter platform channels, Pigeon APIs, FFI and build hooks, native plugin implementations, platform views, add-to-app boundaries, web interop, and native lifecycle integration. Use when Dart must communicate with native platforms; route reusable package APIs, federation, and publication readiness to flutter-package-development.
---

# Flutter Platform Integration

Prefer an existing maintained plugin when it meets the requirement. Write platform code when the capability is unavailable, product-specific, or requires a controlled native contract.

When asked to replace an adequate plugin the project already uses with custom native code, do not write the native code yet. Name what the current plugin already covers, ask which concrete requirement it fails (missing API, platform, behavior, license, or size), and recommend keeping it until that gap is known. When the gap is real, close it with the smallest change: a Dart wrapper, an upstream fix, or a narrow channel for the missing part only.

## Choose the boundary

- Use a package API for established cross-platform capabilities.
- Use Pigeon or another typed generated contract when a multi-method channel benefits from compile-time structure.
- Use a basic method/event channel for small, stable request/response or event surfaces.
- Use FFI for suitable native C-compatible libraries and performance-sensitive calls.
- Use platform views only when native view embedding is required and account for composition, gestures, accessibility, and performance.

Keep domain models outside the channel contract. Version or evolve messages compatibly, validate all values at the boundary, and map platform failures into actionable Dart errors.

## Load references conditionally

- Read [integration strategy](references/integration-strategy.md) when choosing among an existing package, channels or Pigeon, FFI, JS interop, and platform views.
- Read [plugin development](references/plugin-development.md) when creating or evolving a reusable plugin package, federated implementation, platform interface, or multi-platform native API.

`flutter-package-development` owns reusable public APIs, package shape, compatibility, federation decisions, consumer quality, and publication readiness. Use both skills when package design and native implementation are material.

## Lifecycle and platforms

Handle engine/activity/view-controller attachment, background/foreground changes, permission flow, cancellation, and multiple engine instances where applicable. Provide an explicit unsupported-platform behavior rather than a late missing-plugin crash.

## Verification

Test the Dart adapter with fakes and the native implementation on every supported target. Verify error mapping, lifecycle reattachment, permissions, background behavior, and accessibility for embedded views.

## Sources

- [Flutter platform integration](https://docs.flutter.dev/platform-integration)
- [Platform channels](https://docs.flutter.dev/platform-integration/platform-channels)
- [Bind to native code using FFI](https://docs.flutter.dev/platform-integration/bind-native-code)
- [Developing packages and plugins](https://docs.flutter.dev/packages-and-plugins/developing-packages)
