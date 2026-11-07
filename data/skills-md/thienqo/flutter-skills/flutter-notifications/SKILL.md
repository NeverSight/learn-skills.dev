---
name: flutter-notifications
description: Implement or repair Flutter local notifications and remote push delivery across permission, scheduling, token, lifecycle, payload, interaction, and reconciliation flows. Use for notification behavior; route ordinary API transport, navigation, persistence, and custom native bridge work to their specialists.
---

# Flutter Notifications

Deliver notifications as a lifecycle, not as a single plugin call. Preserve the project's provider, notification package, architecture, and route ownership unless migration is explicitly requested.

## Preflight

Read `pubspec.yaml`, SDK constraints, enabled platforms, native manifests and capabilities, and the complete existing notification/provider wiring before prescribing initialization, listeners, or native changes: initialization, listener registration, permission flow, service files, payload parsing, backend contract, route handoff, persistence, flavors, and tests. Identify the demonstrated gap and whether the task concerns local scheduling, remote push, or both. When repository evidence is unavailable, state that inspection is still required and keep proposed changes conditional instead of assuming the wiring is missing. Do not add Firebase, OneSignal, a local notification package, or a state-management package by default.

## Establish one delivery contract

Define stable notification IDs, payload version/type, allowed fields, destination intent, deduplication key, timestamps, and fallback behavior for unknown or stale payloads. Notification payloads and logs must exclude secrets and sensitive user, message, health, payment, or authentication content; send opaque identifiers and fetch authorized domain data when needed. Treat a notification tap as untrusted external input: validate it before handing a typed intent to the app's navigation owner.

Model permission as user-controlled state. Ask in context after explaining value, distinguish not-determined, provisional, denied, and granted where the platform exposes them, and provide a useful disabled state. Never loop permission prompts or imply delivery is guaranteed.

## Route the mode

- For device-scheduled reminders, calendars, time zones, recurrence, cancellation, or reconciliation, read [local notifications](references/local-notifications.md).
- For provider registration, token lifecycle, foreground/background/terminated delivery, taps, or silent/data messages, read [remote push notifications](references/remote-push-notifications.md).
- For Android/iOS/web constraints, permissions, capabilities, or device verification, read [platform delivery](references/platform-delivery.md).

Load only the references required by the current task.

## Boundaries

- `flutter-networking` owns ordinary backend transport and retry mechanics; this skill owns the notification registration and payload lifecycle contract.
- `flutter-persistence` owns the storage implementation; this skill defines notification reconciliation and idempotency needs.
- `flutter-navigation` owns route graphs and back-stack behavior; this skill produces a validated destination intent.
- `flutter-platform-integration` owns a custom plugin or native bridge when the existing package cannot expose a required capability.
- `flutter-security` owns a broader threat review; this skill still redacts payloads, tokens, and delivery telemetry by default.

## Verification

Test deterministic contract, permission, schedule/reconcile, token-change, deduplication, and tap-routing logic without the platform plugin where possible. Then verify supported lifecycle paths on real platform surfaces: foreground, background, terminated launch, denied permission, restart, time-zone change when relevant, and malformed or duplicate payloads. Flutter widget/integration tests alone do not prove OS notification delivery.

Report the platforms and lifecycle states actually exercised, provider/backend dependencies, and remaining device-only gaps.

## Sources

- [Firebase Cloud Messaging: receive messages in Flutter](https://firebase.google.com/docs/cloud-messaging/flutter/receive-messages)
- [Apple UserNotifications](https://developer.apple.com/documentation/usernotifications)
- [Android notification runtime permission](https://developer.android.com/develop/ui/views/notifications/notification-permission)
