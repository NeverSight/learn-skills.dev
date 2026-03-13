---
name: maui-platform-apis
description: Provides cross-platform patterns and best practices for using device capabilities in .NET MAUI apps.
---

# .NET MAUI — Platform APIs Skill

## Purpose

This skill provides agents with best practices, patterns, and cross-platform abstractions for using device capabilities in .NET MAUI applications. It covers permissions, sensors, file pickers, geolocation, camera access, notifications, and platform-specific APIs.

The goal is to ensure that all platform API usage is safe, consistent, and aligned with MAUI’s cross-platform architecture.

## Core Principles

1. **Permission-first design**
   Always request and check permissions before accessing device capabilities.
2. **Cross-platform abstractions**
   Use MAUI Essentials APIs whenever possible.
3. **Graceful degradation**
   If a capability is unavailable on a platform, handle it cleanly.
4. **Separation of concerns**
   Wrap platform API calls in services and interfaces.
5. **User transparency**
   Provide clear explanations when requesting permissions.

## Supported Platform Capabilities

- Geolocation
- Camera & Media Picker
- File Picker
- Clipboard
- Vibration
- Flashlight
- Connectivity
- Sensors (accelerometer, compass, gyroscope)
- Notifications (local)
- Permissions

## Recommended Folder Structure

```text
Services
└─ Platform
   ├─ Implementations
   └─ Interfaces
```

## Agent Usage Guidelines

- When generating code that uses device capabilities:
  - Always check permissions first.
  - Use `Permissions.RequestAsync<T>()`.
  - Use MAUI Essentials APIs (e.g., Geolocation, MediaPicker).
  - Wrap logic in a service (e.g., `IGeolocationService`).
- When asked to “access the camera,” generate:
  - A service abstraction
  - A platform-safe implementation
  - Permission checks
- When asked to “get the user’s location,” apply:
  - Permission checks
  - Fallback handling
  - Cancellation tokens

## Out of Scope

- Authentication (covered in `maui-authentication`)
- UI layout (covered in `maui-ui-best-practices`)
- Database storage (covered in `maui-data-storage`)
