---
name: flutter-background-execution
description: Implement, debug, or verify Flutter work that must continue or be scheduled after the app leaves the foreground, including OS-scheduled jobs, foreground services, and headless callbacks. Use for persistent background execution; route in-process async or CPU work to dart-concurrency and notification delivery to flutter-notifications.
---

# Flutter Background Execution

Treat background execution as an operating-system contract, not a Dart timer that is guaranteed to keep running. Preserve the project's scheduler or plugin when it satisfies the requirement; inspect `pubspec.yaml`, SDK constraints, target platforms, native capabilities, and existing registration before changing it.

## Define the job

Record the trigger, acceptable delay, maximum duration, survival across process death or reboot, network/power constraints, user visibility, cancellation, and what should happen after sign-out or data deletion. Separate “must eventually run” from “must run at an exact time”; mobile schedulers are commonly opportunistic.

## Choose the owner

- Keep work in `dart-concurrency` when it only needs to run while the app process is alive.
- Use an OS-backed scheduler for deferrable work that must survive the visible app.
- Use a user-visible foreground or continued-processing mode only when the platform permits the use case and its disclosure, permissions, and limits are satisfied.
- Route exact user reminders and notification delivery to `flutter-notifications`.
- Route a custom native scheduler bridge or reusable plugin implementation to `flutter-platform-integration`.

Do not add a scheduling package by default. Verify platform coverage, maintenance, target SDK support, callback model, and the repository's existing dependencies first.

## Load details conditionally

- Read [Android scheduling and services](references/android-scheduling-and-services.md) for WorkManager, foreground services, exact alarms, reboot behavior, or Android permissions.
- Read [Apple background tasks](references/apple-background-tasks.md) for BGTaskScheduler, refresh/processing work, expiration, capabilities, or iOS scheduling expectations.
- Read [headless execution and reliability](references/headless-execution-and-reliability.md) for callback dispatchers, isolates, plugin access, retries, deduplication, or durable progress.

## Verification

Test the job body behind a platform-free boundary, including success, retryable failure, permanent failure, cancellation, duplicate delivery, and stale identity. Then verify the native registration and lifecycle on every supported target: backgrounding, process termination, constraints, expiration or timeout, rescheduling, reboot when promised, and sign-out cleanup. Report actual device and lifecycle evidence; a successful direct function call does not prove OS scheduling.

## Sources

- [Flutter background processes](https://docs.flutter.dev/packages-and-plugins/background-processes)
- [Android persistent work](https://developer.android.com/develop/background-work/background-tasks/persistent)
- [Apple Background Tasks](https://developer.apple.com/documentation/backgroundtasks)
