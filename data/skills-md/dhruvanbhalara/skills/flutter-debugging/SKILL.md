---
name: flutter-debugging
description: Flutter DevTools, Profiling, Logging & Memory Management
metadata:
    platforms: "flutter"
    languages: "dart"
    category: "tooling"
---

# Logging

-   Use a centralized `AppLogger` class for all logging — NEVER use `print()` or raw `debugPrint()`
-   Define log levels: `verbose`, `debug`, `info`, `warning`, `error`, `fatal`
-   In dev flavor: log everything (verbose and above)
-   In staging: log info and above
-   In production: log warning and above only, route to Crashlytics
-   Include context in logs: `AppLogger.error('Failed to fetch user', error: e, stackTrace: st)`
-   NEVER log sensitive data (passwords, tokens, PII) at any level

# Flutter DevTools

-   Use **Widget Inspector** to debug layout issues and identify unnecessary rebuilds
-   Use **Performance Overlay** (`showPerformanceOverlay: true`) to monitor frame rates
-   Use **Timeline View** to identify jank — target 16ms per frame (60fps)
-   Use **Memory View** to detect memory leaks and monitor allocation patterns
-   Use **Network Profiler** to inspect Dio requests/responses during development

# Debugging Strategies

-   **Layout Issues**: Use `debugPaintSizeEnabled = true` to visualize widget boundaries
-   **Overflow Errors**: Check `RenderFlex overflowed` — use `Expanded`, `Flexible`, or constrain dimensions
-   **Unbounded Height**: Wrap `ListView` in `SizedBox` or use `shrinkWrap: true` with `NeverScrollableScrollPhysics`
-   **Rebuild Tracking**: Add `debugPrint('$runtimeType rebuild')` temporarily to identify excessive rebuilds — remove before commit
-   **Async Errors**: Always catch and log errors in `try-catch` blocks with stack traces
-   Use `assert()` for development-time invariant checks that are stripped in release builds

# Memory Management

-   Dispose ALL controllers, subscriptions, `Timer`, and `AnimationController` in `dispose()`
-   Use `late` initialization in `initState()` — never inline-initialize disposable objects
-   Use `WeakReference` for caches that should not prevent garbage collection
-   Profile memory with DevTools Memory tab — watch for monotonically increasing allocations
-   Watch for common leaks: undisposed listeners, closures capturing `BuildContext`, global streams without cancellation

# Performance Profiling

-   Always profile with `--profile` mode (not debug): `flutter run --profile --flavor dev -t lib/main_dev.dart`
-   Use `Timeline.startSync` / `Timeline.finishSync` for custom performance tracing of critical paths
-   Monitor shader compilation jank on first run — use `--cache-sksl` for warmup:
    ```bash
    flutter run --profile --cache-sksl --purge-persistent-cache
    ```
-   Target metrics: < 16ms frame build time, < 100ms screen transition, < 2s cold start

# Error Boundaries

-   Route errors to Crashlytics in staging/prod (`FlutterError.onError = FirebaseCrashlytics.instance.recordFlutterFatalError`)
-   Set `FlutterError.onError` and `PlatformDispatcher.instance.onError` to catch framework and async errors
-   Wrap critical widget subtrees in custom error boundary widgets that show fallback UI instead of red screens
-   In release mode: NEVER show stack traces to users — show user-friendly error messages only
