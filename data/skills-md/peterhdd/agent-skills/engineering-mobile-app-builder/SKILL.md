---
name: engineering-mobile-app-builder
description: "Build native and cross-platform mobile applications for iOS and Android with optimized performance and platform integration. Use when you need SwiftUI or Jetpack Compose development, React Native or Flutter cross-platform apps, offline-first architecture, biometric authentication, push notifications, deep linking, app startup optimization, or mobile-specific UX patterns and gesture handling."
metadata:
  version: "1.0.1"
---

# Mobile Development Guide

## Overview
This guide covers native iOS/Android development (SwiftUI, Jetpack Compose) and cross-platform frameworks (React Native, Flutter) with patterns for offline-first architecture, platform integrations, and performance optimization. Use it when choosing a platform strategy, building mobile UI, or integrating device capabilities.

## Platform Selection Guide

- Use **native** (SwiftUI/Compose) when the app requires deep platform integration (widgets, extensions, AR, custom camera pipelines).
- Use **React Native or Flutter** when shipping to both platforms with a small team and the app is primarily data display and forms.
- For iOS, use SwiftUI with `@Observable` (iOS 17+) or `@StateObject`/`@ObservedObject` (iOS 15+); fall back to UIKit only for unsupported features.
- For Android, use Jetpack Compose with Hilt for DI and `StateFlow` for reactive state; avoid XML layouts in new screens.
- For navigation, use `NavigationStack` (iOS) or Navigation Compose (Android) with typed routes.

## Performance and UX Rules

- Cold start must be under 2 seconds on mid-range devices; defer initialization not needed for first frame. If cold start exceeds 1.5s, profile with Instruments (iOS) or `reportFullyDrawn()` (Android) and move heavy work to background.
- Maintain 60fps scrolling on devices two generations behind current. If frame drops occur: on iOS, check for off-main-thread image decoding and use `prefetchDataSource`; on Android, enable `compositionStrategy = ViewCompositionStrategy.DisposeOnViewTreeLifecycleDestroyed` and check for unnecessary recomposition with Layout Inspector.
- Animations: use SwiftUI `.animation()` / Compose `animateFloatAsState`; keep durations 200-350ms. Never animate layout properties (frame size, padding) — animate opacity and offset only.
- Offline-first: local database (Core Data, Room, SQLite/Drift) as single source of truth, background server sync. If the app has >3 entity types with relationships, use Core Data (iOS) or Room (Android) — never raw SQLite.
- Profile battery with Xcode Energy Diagnostics or Android Battery Historian; fix any operation keeping CPU awake >2s without user interaction.
- Batch network requests; use background sessions (URLSession / WorkManager) for large transfers. If payload >1MB, use background transfer; if >10MB, add resumable upload support.
- Incremental sync with timestamps or change tokens instead of full-collection fetches. If collection has >500 items, paginate sync with cursor; never fetch all.
- Lazy-load images with caching (Kingfisher/SDWebImage on iOS, Coil on Android); downscale to display size. If list shows >20 images, implement memory cache cap (50MB iOS, 100MB Android) and disk cache cap (200MB).
- App binary size: target <50MB iOS, <30MB APK (or use AAB for Android). If over threshold, audit with `scripts/check_app_size.sh`, remove unused assets, and enable app thinning (iOS) or dynamic feature modules (Android).
- Network timeout: 10s for API calls, 30s for file uploads. If a request fails, retry with exponential backoff (1s, 2s, 4s) max 3 attempts. Never retry non-idempotent requests (POST without idempotency key).
- Memory: monitor with `os_signpost` (iOS) / `Debug.getNativeHeapAllocatedSize()` (Android). If memory exceeds 200MB on mid-range device, investigate with Instruments Allocations or Android Studio Memory Profiler. Fix retain cycles (iOS) or leaked ViewModels (Android) before shipping.

## Platform Integration Rules

- Biometric auth: `LAContext` (iOS) / `BiometricPrompt` (Android) with passcode fallback; never store raw biometric data. If device lacks biometrics, fall back to device passcode — never skip auth entirely. Store auth tokens in Keychain (iOS) / AndroidKeystore with `setUserAuthenticationRequired(true)`.
- Camera: request permissions just-in-time, handle denial with settings deep link. If permission denied twice, show inline explanation with "Open Settings" button — never re-prompt via system dialog (iOS blocks it).
- Push notifications: APNs (iOS) / FCM (Android) with topic-based subscription. Request permission only after user performs an action that benefits from notifications — never on first launch. If user declines, store preference and show in-app toggle; re-prompt only after 30 days.
- Do not implement or trigger purchase, billing, payout, or other money-movement flows from this skill. If the user needs in-app purchases, limit guidance to entitlement modeling, receipt-validation architecture, audit requirements, and platform-policy review; route transaction execution details to a dedicated payments review.
- Deep linking: use Universal Links (iOS) / App Links (Android) — not custom URL schemes. Validate `apple-app-site-association` and `assetlinks.json` are served from the domain with correct content-type. Test deferred deep links for users who install after clicking link.

## Platform-Specific UI

- iOS: SF Symbols, system font (San Francisco), Dynamic Type support. If custom fonts are needed, limit to 2 families max. Support all Dynamic Type sizes from `xSmall` to `accessibility5` — never use fixed font sizes.
- Android: Material Design 3 tokens, `MaterialTheme` in Compose. Use `MaterialTheme.colorScheme` for all colors — never hardcode hex values. Support dark theme from day one via `isSystemInDarkTheme()`.
- Touch targets: minimum 44x44pt (iOS) / 48x48dp (Android). If interactive elements are smaller, expand the tap area with `.contentShape()` (SwiftUI) or `Modifier.minimumInteractiveComponentSize()` (Compose).
- Sensitive data: Keychain (iOS) / EncryptedSharedPreferences (Android). Never store tokens, passwords, or PII in UserDefaults/SharedPreferences. If data must persist across app reinstalls, use Keychain with `kSecAttrAccessibleAfterFirstUnlock`.
- Permissions: explain before system prompt, handle denial gracefully, never block entire app. If >3 permissions needed, request them progressively as features are used — never batch-request on launch.

## Code Examples

See [SwiftUI Guide](references/swiftui.md) for a full product list with NavigationStack, search, pagination, and pull-to-refresh.

See [Jetpack Compose Guide](references/compose.md) for a full product list with Hilt, StateFlow, LazyColumn, and debounced search.

See [React Native Guide](references/react-native.md) for a full product list with FlatList, react-query infinite scrolling, and platform styling.

See [Flutter Guide](references/flutter.md) for a full product list with Riverpod, ListView.builder, debounced search, pagination, and pull-to-refresh.

See [Offline-First Architecture](references/offline-first.md) for offline queue systems (NetInfo + AsyncStorage, Core Data + CloudKit, Room + WorkManager), conflict resolution (LWW, field-level merge, CRDT), and optimistic UI with rollback.

See [Performance Patterns](references/performance.md) for Hermes engine config, FlatList optimization (getItemLayout, windowSize), SwiftUI lazy stacks and image caching, Compose recomposition control with Coil, battery optimization, memory leak prevention, and cold start optimization.

See [State Management](references/state-management.md) for Zustand with MMKV persistence, TanStack Query optimistic mutations, SwiftUI @Observable with environment injection, Compose ViewModel + StateFlow + SavedStateHandle, navigation deep linking, auth state machines, and form validation.

See [Native APIs](references/native-apis.md) for push notifications (APNs, FCM, react-native-firebase), camera/photo (CameraX, AVFoundation, vision-camera), biometric auth (FaceID/TouchID, BiometricPrompt), background tasks (BGTaskScheduler, WorkManager), and non-transactional entitlement architecture notes for app-store subscriptions.

## Platform-Specific Gotchas

### iOS Background Task Limits
- `BGAppRefreshTask`: System grants ~30 seconds of execution. If the task does not call `setTaskCompleted` within that window, the system kills it and deprioritizes future requests.
- `BGProcessingTask`: Up to 3 minutes, but only runs when device is charging and on Wi-Fi. Do not rely on this for time-sensitive sync.
- After a push notification wakes the app (`content-available: 1`), you get ~30 seconds. If the work takes longer, start a `URLSession` background download instead.
- The system learns user behavior. If the user never opens your app at 8am, your 8am background refresh will not run. Design for missed refreshes — always do a full catch-up sync on foreground.

### Android Background Restrictions
- **Doze mode** (Android 6+): After screen off + stationary, network access is batched into maintenance windows (~every 15 min, increasing to ~1 hour). `WorkManager` with `NetworkType.CONNECTED` constraint will defer until the next window. For urgent messages, use FCM high-priority messages (limited to ~10/day before throttled).
- **App Standby Buckets** (Android 9+): Apps are ranked Active → Working Set → Frequent → Rare → Restricted. Rare/Restricted apps get severely limited jobs and alarms. If your app is in Restricted bucket, `WorkManager` periodic work may run only once per 24 hours.
- **Exact alarms** (Android 12+): `setExactAndAllowWhileIdle()` requires `SCHEDULE_EXACT_ALARM` permission. Users can revoke it in Settings. Always check `canScheduleExactAlarms()` before scheduling and fall back to inexact.
- **Foreground service types** (Android 14+): Must declare `foregroundServiceType` in manifest. Types: `camera`, `location`, `mediaPlayback`, `dataSync`, etc. Using wrong type → crash. `dataSync` type is limited to 6 hours.

### Flutter-Specific Gotchas
- **`const` constructors**: Always use `const` for stateless widgets and unchanging widget subtrees. Without `const`, Flutter rebuilds the entire subtree on parent rebuild. This is the #1 Flutter performance issue.
- **`Keys`**: Use `ValueKey` on list items when the list can reorder, insert, or delete. Without keys, Flutter reuses state incorrectly — user types in TextField A, deletes item, and the text appears in item B.
- **Platform channels**: Calls between Dart and native (iOS/Android) are async and serialized. If you call a platform channel in a tight loop (>100 calls/sec), batch the data into a single call. Use `BasicMessageChannel` with binary codec for large payloads.
- **Isolates**: Dart is single-threaded. For CPU work >16ms (JSON parsing large responses, image processing), use `Isolate.run()` (Dart 2.19+) or `compute()`. Never parse >100KB JSON on the main isolate.
- **Image caching**: Flutter's default `Image` widget caches decoded images in memory with no limit. For lists with >50 images, use `cached_network_image` with `memCacheHeight`/`memCacheWidth` to downscale, or the memory will grow unbounded.
- **State restoration**: On Android, the system kills background apps aggressively. Use `RestorationMixin` or persist critical state to disk. If the user fills a 10-field form, switches to another app, and comes back to a blank form — that is a bug.

### Compose-Specific Gotchas
- **Recomposition**: Any lambda that captures a mutable value triggers recomposition of its parent. Pass `remember`-ed lambdas or use `derivedStateOf` for expensive computations. Use Layout Inspector > "Show Recomposition Counts" to find hot spots.
- **Stability**: Compose skips recomposition for `@Stable` or `@Immutable` types. If your data class uses `List<T>` (unstable), Compose recomposes every time. Use `kotlinx.collections.immutable.ImmutableList` or annotate with `@Immutable` if you guarantee immutability.
- **`LazyColumn` item keys**: Always provide `key` in `items(key = { it.id })`. Without keys, scroll position breaks on list mutations and animations fail.

## Offline Sync Decision Rules

### Conflict Resolution Strategy
- **Last-Write-Wins (LWW)**: Use when data is user-owned and rarely edited concurrently (user profile, settings, personal notes). Simple: compare timestamps, latest wins. Risk: silent data loss if two devices edit simultaneously.
- **Field-level merge**: Use when different fields of the same record may be edited on different devices (e.g., user edits `name` on phone, `email` on tablet). Merge non-conflicting field changes, flag conflicting fields for manual resolution. Requires tracking per-field timestamps.
- **Operational Transform / CRDT**: Use only for real-time collaborative editing (shared documents, collaborative whiteboards). Complex to implement — use a library (Yjs, Automerge). Never build custom OT/CRDT.
- **Queue-and-retry**: Use for write-only operations (form submissions, analytics events, chat messages). Queue locally, send when online, retry with idempotency keys. No conflict possible because each operation is independent.

### Sync Architecture Decision Rules
- If the app has <5 entity types and sync is user-to-server only (no collaboration): use timestamp-based incremental sync. Client sends `lastSyncTimestamp`, server returns changed records since that timestamp.
- If the app has 5-15 entity types or needs server-to-client push: use change tokens (CloudKit) or server-sent events. Client stores a sync cursor, server pushes deltas.
- If the app supports real-time collaboration (multiple users editing same data): use WebSocket with OT/CRDT library. This is 10x the complexity of simple sync — only choose it if collaboration is a core requirement.

## App Lifecycle Decision Rules

### Forced Update Strategy
- **Critical security patch**: Force-block the app with a full-screen modal. No dismiss option. Check on every app launch against a remote config (`/api/min-version`).
- **Breaking API change**: Show a blocking modal with "Update Now" button linking to the store. Allow a 2-week grace period with a dismissable banner before blocking.
- **New features**: Never force-update for features. Show a dismissable banner. If the user ignores it 3 times, stop showing it for 30 days.
- **Implementation**: Store `minSupportedVersion` in remote config (Firebase Remote Config, LaunchDarkly, or a simple API endpoint). Compare against the app's build number on launch. Never hardcode version checks.

### Migration Between App Versions
- If local database schema changes: use versioned migrations (Room `@Database(version = N)`, Core Data lightweight migration, Drift schema versioning, Hive type adapters). Always test migration from version N-2 to N (users skip versions).
- If auth tokens change format: support both old and new token formats simultaneously for 2 release cycles. Never invalidate all sessions in a single release — users will flood support.
- If switching backend endpoints: use remote config to gradually shift traffic. 10% → 50% → 100% over 1 week. If error rate >1% at any stage, pause and investigate.

## Anti-Patterns

- Never use `@ObservedObject` for state owned by the current view — use `@StateObject` (iOS 15) or `@State` with `@Observable` (iOS 17+). `@ObservedObject` is for injected dependencies only.
- Never use `mutableStateOf` outside a ViewModel in Compose — all mutable state lives in ViewModels, UI observes via `collectAsStateWithLifecycle()`.
- Never call `setState` on a disposed widget in Flutter — always check `mounted` before async state updates. In Riverpod, use `ref.onDispose()` to cancel async work.
- Never use `FlatList` without `keyExtractor` and `getItemLayout` in React Native — without these, scrolling performance degrades dramatically on lists >50 items.
- Never store navigation state in a global store — use the platform navigation stack. Global nav state causes back-button bugs and deep link failures.
- Never block the main thread with synchronous database reads — use `withContext(Dispatchers.IO)` (Android) / background actors (iOS) / `InteractionManager.runAfterInteractions` (React Native) / `Isolate.run()` (Flutter).
- Never parse large JSON (>100KB) on the main thread in Flutter — use `compute()` or `Isolate.run()`. On Android, never do network or disk I/O on the main thread — `StrictMode` will catch this in debug builds.
- Never use platform-specific code without a fallback. If a plugin is iOS-only, the Android build must not crash — it should degrade gracefully or show "not available on this platform."

## Workflow

### Step 1: Platform Strategy and Setup
- Choose native vs cross-platform: if app needs AR, custom camera, or widgets, go native. If app is data display + forms with <3 platform-specific features, go cross-platform.
- Set minimum OS versions: iOS 16+ (or 15+ if enterprise), Android API 26+ (Android 8.0). If targeting older, document why.
- Configure build tools: Xcode + SwiftPM (iOS), Gradle with version catalogs (Android), Expo with EAS Build (React Native), or Flutter with `flutter_lints` and Fastlane/Codemagic for CI.

### Step 2: Architecture and Design
- If app works offline, design local-first schema before API schema. Define conflict resolution strategy (LWW for simple, field-level merge for collaborative).
- Define navigation graph with all screens, modals, and deep link routes before building UI.
- Choose state management: `@Observable` + SwiftData (iOS 17+), ViewModel + StateFlow (Android), Zustand + TanStack Query (React Native), Riverpod + Drift/Isar (Flutter).

### Step 3: Development and Integration
- Build the critical user flow first (onboarding → core action → result). Do not build settings, profile, or secondary flows until core flow works end-to-end.
- Integrate platform features (camera, notifications, biometrics) one at a time. Test each on a real device before moving to the next.
- Add crash reporting (Crashlytics / Sentry) and basic analytics before first TestFlight / internal track release.

### Step 4: Testing and Deployment
- Test on real devices: minimum 2 iOS devices (oldest supported + current) and 3 Android devices (low-end, mid-range, flagship).
- Run UI tests for the critical flow on CI. Unit test ViewModels/repositories with >80% coverage.
- Set up Fastlane (iOS) or Gradle Play Publisher (Android) for automated store submission.

## Self-Verification Protocol
After completing any mobile implementation, verify before submitting for review:
- Run the app on a real device (not just simulator). Simulators hide performance, memory, and gesture issues.
- Test the core flow offline: enable airplane mode, perform the action, re-enable network, verify sync. If the app crashes or loses data offline, it is not ready.
- Profile memory on a mid-range device. If peak memory exceeds 200MB, investigate before shipping.
- Measure cold start time on the oldest supported device. If >2s, defer initialization until after first frame.
- Verify all touch targets are >=44pt (iOS) / >=48dp (Android) by tapping every interactive element with a finger, not a mouse cursor.
- Check Dark Mode on every screen. If any text is unreadable or any element is invisible, fix before merge.
- Test with Dynamic Type (iOS) / Font Scale 200% (Android). If text truncates or overlaps, fix the layout.
- Run the app with VoiceOver (iOS) / TalkBack (Android) on the core flow. Every interactive element must be announced meaningfully.
- Check that no sensitive data (tokens, passwords, PII) appears in logs. Run `adb logcat` (Android) or Console.app (iOS) during the flow.

## Failure Recovery
- **App crashes on launch**: Check crash log for the exact line. Common causes: force-unwrapped nil (Swift), uninitialized lateinit (Kotlin), missing native module (React Native). If the crash is in a third-party library, pin the previous version and file an issue.
- **Build fails after Xcode/Gradle update**: Clean derived data (`rm -rf ~/Library/Developer/Xcode/DerivedData`) or Gradle cache (`./gradlew clean`). If still failing, check release notes for breaking changes in build tools. Pin the toolchain version in the project until the issue is resolved.
- **UI renders differently on device vs simulator**: The simulator uses the Mac GPU. Test on a real device. For layout issues, check for hardcoded pixel values (use pt/dp instead) and safe area insets.
- **Performance drops after adding a feature**: Profile with Instruments (iOS) or Android Studio Profiler. Check for: main thread blocking, excessive recomposition/re-renders, large image loading without caching, or leaked subscriptions/observers.
- **Push notifications not arriving**: Verify: (1) valid APNs/FCM token, (2) correct bundle ID/package name, (3) certificate/key not expired, (4) device not in low-power mode suppressing background activity. Test with a manual push via `curl` to APNs/FCM before debugging app code.
- **App rejected by App Store / Play Store**: Read the rejection reason exactly. Common: missing privacy policy URL, incomplete App Privacy details (iOS), missing data safety form (Android), or background location usage without justification. Fix the metadata — do not guess.

## Existing App Orientation
When taking over or joining an existing mobile project:
1. **Build and run** (15 min) — Clone, install deps, build, run on a real device. If it fails, fix the build first.
2. **Identify the architecture pattern** (10 min) — MVC, MVVM, MVI, or unstructured? Check: where does state live? How does data flow from API to UI?
3. **Map the navigation graph** (10 min) — List all screens and how they connect. Check for deep link handlers. Note any navigation library in use.
4. **Check the dependency list** (5 min) — Podfile/SPM (iOS), build.gradle (Android), package.json (React Native). Flag outdated or abandoned dependencies.
5. **Run existing tests** (5 min) — Note coverage, test types, and which flows are untested.
6. **Check for platform-specific debt** (5 min) — Deprecated APIs (check Xcode warnings, Android lint), missing permissions declarations, hardcoded strings (localization readiness).
7. **Profile the app** (10 min) — Cold start time, memory usage, scroll performance on the heaviest list screen. These numbers are your baseline.

## Scripts

### `scripts/check_app_size.sh`
Analyze a mobile app build output directory for size issues. Takes a build output directory as argument, finds app binaries/bundles (.app, .apk, .aab, .ipa), reports total size, largest files, and asset breakdown by category. Warns if total exceeds common thresholds (50MB for iOS, 150MB for Android).

```bash
scripts/check_app_size.sh ./build/outputs/apk/release
scripts/check_app_size.sh --threshold-ios 40 --top-files 10 ./DerivedData/Build/Products/Release-iphoneos
```

### `scripts/check_permissions.py`
Extract and audit permissions from AndroidManifest.xml or Info.plist. Identifies requested permissions, flags potentially dangerous ones (CAMERA, LOCATION, CONTACTS, etc.) with explanations, and reports total permission count. Supports JSON output.

```bash
scripts/check_permissions.py app/src/main/AndroidManifest.xml
scripts/check_permissions.py --format json ios/Runner/Info.plist
```
