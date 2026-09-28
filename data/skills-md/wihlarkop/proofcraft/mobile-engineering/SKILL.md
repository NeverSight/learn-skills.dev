---
name: mobile-engineering
description: >-
  Design, implement, test, or review mobile-specific behavior across iOS, Android, Flutter, and
  React Native. Use for app lifecycle/backgrounding, local-first/offline storage and sync,
  conflict resolution, push/deep links, software keyboard/IME, device capabilities, hybrid/WebView
  native boundaries, and mobile-specific verification. Local-first is first-class when product
  behavior requires it, but is never imposed on apps that do not need offline persistence.
license: MIT
compatibility: Portable Agent Skills methodology; no runtime dependency.
metadata:
  suite: proofcraft
  suite-version: "0.1.0"
  skill-version: "0.1.0"
---


# Mobile Engineering

Treat mobile lifecycle, unreliable connectivity, and device constraints as normal operating conditions rather than edge cases.

## Trigger

Use when a task depends on iOS/Android application lifecycle, background execution, local-first/offline behavior, synchronization, device capabilities, push/deep links, software keyboard/IME, native navigation, or mobile WebView/native-shell behavior.

Use ui-engineering alongside this skill for visual layout, accessibility, design-system, or general interaction work.

## Workflow

1. Inspect the existing framework, platform targets, architecture, local storage, backend contracts, and lifecycle behavior. Do not replace an established stack because another framework is familiar.
2. Identify lifecycle boundaries relevant to the feature: foreground/background, process death, restart, connectivity changes, permission changes, or device resource constraints.
3. Classify local state: authoritative, derived, ephemeral, coordination, or cache.
4. If offline/local-first behavior matters, define how local writes persist, how operations are replayed, how remote changes are pulled, and how conflicts are resolved. The network is a synchronization channel, not an implicit prerequisite for locally promised behavior.
5. Define background ownership, cancellation, retries, time limits, restart recovery, progress, and partial failure for background work.
6. Handle mobile input and device surfaces deliberately: safe areas, system back, keyboard/IME, orientation/adaptive layout, deep links, push, permissions, and hardware APIs only when relevant.
7. For WebView/hybrid flows, make native/web ownership and bridge failure behavior explicit.
8. Verify on the strongest available surface: device/emulator when material, otherwise framework/build/static evidence with the gap stated.

## Local-first

Local-first is a supported mobile capability, not a universal default. Activate it when the product promises useful behavior during connectivity loss, delayed sync, or app/process interruption.

## Stop

Stop when mobile-specific lifecycle and failure paths relevant to the feature are explicit and evidenced, without inventing offline/sync complexity the product does not require.
## Reference Guide

Load only the references needed for the current task:

- [adaptive input](references/adaptive-input.md)
- [conflict resolution](references/conflict-resolution.md)
- [lifecycle background](references/lifecycle-background.md)
- [local first](references/local-first.md)
- [mobile testing](references/mobile-testing.md)
- [offline sync](references/offline-sync.md)
- [webview hybrid](references/webview-hybrid.md)
- [principles](references/_shared/constitution/principles.md)
- [decision lock](references/_shared/constitution/decision-lock.md)
- [concerns](references/_shared/orchestration/concerns.md)
- [authority](references/_shared/state/authority.md)
- [lifecycle](references/_shared/state/lifecycle.md)
- [sync](references/_shared/state/sync.md)
- [provider neutrality](references/_shared/engineering/provider-neutrality.md)
- [evidence](references/_shared/verification/evidence.md)
- [risk depth](references/_shared/verification/risk-depth.md)
