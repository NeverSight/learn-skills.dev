---
name: android-ui-home-screen
description: Design Android notifications, live updates, and picture-in-picture experiences outside the main app screen. Use for interruption decisions, notification templates and actions, ongoing progress, and continuity into the app.
license: Apache-2.0
---
# Android system surfaces

Choose a system surface only when it helps the user's current goal. "Home screen" here follows the Android design-guide category; it does not mean the app's first destination.

## Route by surface

- Timely information, permission timing, actions, channels, privacy: [notifications](references/notifications.md).
- Finite, user-initiated tracking or ongoing video: [live updates and PiP](references/live-updates-and-pip.md).
- A persistent glanceable launcher surface: use [widgets](../android-ui-widgets/SKILL.md).

## Specify the experience

Describe why the information belongs outside the app, what initiates it, what the user can do, when it becomes stale, and what ends it. Pick a platform template and define the destination opened by a tap.

Account for user control: disabled notifications, muted channels, denied permission, lock-screen privacy, dismissal, and demotion. Never claim a notification will always sound, appear, or remain visible.

For a continuing task, preserve identity and progress across the system surface and app. Keep timestamps, labels, and state consistent.

## Validate

Inspect collapsed/expanded and relevant locked/unlocked states on supported OS versions. Exercise taps, actions, completion, cancellation, stale cleanup, and return to the app. For PiP, observe actual playback and entry/exit, not just a small video mockup.

Recheck OS/target SDK requirements and current API support before implementation. A design recommendation cannot override foreground-service, permission, or platform eligibility rules.

Source baseline: [Notifications](https://developer.android.com/design/ui/mobile/guides/home-screen/notifications), reviewed 2026-10-04. Additional sources are linked in references.
