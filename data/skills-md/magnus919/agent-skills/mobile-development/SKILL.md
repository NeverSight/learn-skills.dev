---
name: mobile-development
description: Build, test, sign, and ship mobile apps across iOS, Android, Flutter, and React Native — project scaffolding, builds and code signing, device and emulator testing, store submission (App Store and Play Store), app lifecycle and backgrounding, offline and sync, and mobile-specific testing. Use when the task involves creating, building, testing, or shipping a mobile app for iOS or Android, or reasoning about mobile behavior such as background execution, push notifications, offline storage, and data sync. Do not use for web frontend work (that is frontend-engineering), backend services and APIs (that is backend-engineering), or desktop and web platform targets outside the iOS and Android scope.
license: MIT
metadata:
  tags: mobile, ios, android, flutter, react-native, swift, kotlin, xcode, gradle, app-store, play-store
  source_repo: https://github.com/magnus919/hermes-profiles
---

# Mobile Development

One skill for building mobile apps on **iOS** and **Android** — with per-framework
depth for native (Swift/SwiftUI, Kotlin/Jetpack Compose) and cross-platform
(Flutter, React Native) stacks. All four share one agent workflow — scaffold,
build and sign, test on devices and emulators, and ship to stores — so they live
in **ONE family skill** with per-framework references, following the
`frontend-engineering` precedent. Load the shared workflow below, then pull the
reference for the framework you are actually building.

| Framework | Stack | Reference (load on demand) |
|-----------|-------|----------------------------|
| iOS | Swift, SwiftUI/UIKit, Xcode | [references/ios.md](references/ios.md) |
| Android | Kotlin, Jetpack Compose, Gradle | [references/android.md](references/android.md) |
| Flutter | Dart, Flutter SDK | [references/flutter.md](references/flutter.md) |
| React Native | TypeScript/JavaScript, React, Metro | [references/react-native.md](references/react-native.md) |

## When to use

Load this skill when the task involves any part of the mobile lifecycle:

- **Scaffold** — creating a new mobile project for iOS, Android, Flutter, or
  React Native: choosing the framework, initializing the project, and setting up
  the platform toolchains.
- **Build and sign** — compiling a debug or release build, configuring code
  signing (certificates, provisioning profiles, keystores, app signing), or
  producing distributable artifacts (`.ipa`, APK, AAB).
- **Test on devices and emulators** — running and debugging on iOS simulators,
  Android emulators, or physical devices, including device provisioning,
  connectivity, and platform-specific runtime behavior.
- **Ship to stores** — submitting to the App Store (TestFlight, App Store
  Connect) or Google Play (internal/closed/open testing tracks, Play Console),
  and reasoning about store review readiness.
- **Mobile-specific behavior** — app lifecycle and backgrounding, offline
  storage and sync, push notifications, deep links, and mobile testing
  (unit, widget, UI, and device-farm testing).

## When not to use

- **Web frontends** — component architecture, state management, and browser
  behavior belong to [frontend-engineering](../frontend-engineering/SKILL.md);
  this skill covers apps that run on iOS and Android devices.
- **Backend services and APIs** — server-side logic, API design, and data
  persistence on the server belong to
  [backend-engineering](../backend-engineering/SKILL.md). Mobile apps consume
  those APIs; they do not replace them.
- **Desktop or web platform targets** — Flutter for desktop/web and React
  Native for web (React Native Web) have different delivery and testing
  surfaces; this skill is scoped to the iOS and Android app store platforms.
- **Cross-platform web-first development** — if the deliverable is a website or
  PWA, use frontend-engineering instead.

## The Mobile Engineer's Domain

| You own | You don't own |
|---------|--------------|
| Mobile app architecture — platform structure, app entry points, navigation, and state management on the device | Backend APIs, data models, and server-side persistence — that's the backend-engineering |
| Framework and toolchain setup — Xcode/Gradle project config, Flutter/React Native scaffolding, dependency management | Web frontend architecture and browser behavior — that's the frontend-engineering |
| Builds and signing — debug/release builds, certificates, provisioning profiles, keystores, app signing, versioning and build numbers | Release orchestration and rollout process for server software — that's the release-engineering |
| Device and emulator testing — simulators, emulators, physical devices, adb/xcrun device workflows | Test strategy, coverage, and quality gates for the whole product — that's the qa-methodology |
| Mobile-specific concerns — lifecycle/backgrounding, offline and sync, push, deep links, mobile performance | User journeys, wireframes, and interaction design — that's the product-design-and-ux |
| Store submission — TestFlight, App Store Connect, Play Console, release tracks, store listing metadata | CI/CD pipeline infrastructure — that's the platform-engineer |

## The Shared Mobile Workflow

Every mobile task follows the same four steps regardless of framework. Deep
framework-specific detail is deferred to the per-framework reference — read it
at the step where it matters.

### 1. Scaffold

Pin down what the app is before generating code:

- **Platform and framework** — native iOS, native Android, Flutter, or React
  Native. Choose based on team skills, target audience, and per-feature needs
  (see Core Principles).
- **Minimum OS versions** — the oldest iOS and Android versions you will
  support; every decision below (APIs, dependencies, testing) flows from this.
- **Project initialization** — generate the project with the framework's
  canonical tool (`xcodebuild`/Xcode template, Android Studio/Gradle, `flutter
  create`, `npx @react-native-community/cli init` or `create-expo-app`), and
  commit the scaffold before adding app code so toolchain upgrades stay
  reviewable.
- **Source of truth** — a single project root that builds both platforms when
  using a cross-platform framework, so the artifact is reproducible from the
  repository.

### 2. Build and sign

A build that only works on your machine is not a build:

- **Build once, in CI** — the release build must reproduce on a clean machine
  or CI runner, not just in your IDE. Pin toolchain versions (Xcode, JDK/Gradle,
  Flutter SDK, Node).
- **Signing is separate from building** — keep signing assets (certificates,
  provisioning profiles, keystores) out of the repository; reference them via
  environment or secure secret storage. See the per-framework reference for
  where each platform expects them.
- **Distinguishable artifacts** — version numbers and build numbers must
  increment per release so testers and crash reports can identify the build.
- **Know your artifact format** — `.ipa` for iOS, APK and AAB for Android,
  and the framework-specific intermediates. Store submission has hard format
  requirements (for example, Google Play requires AAB for new apps).

### 3. Test on devices and emulators

Test where the code runs, not where it is convenient:

- **Emulators/simulators for speed, devices for truth** — simulators and
  emulators are fast and scriptable, but physical devices reveal real
  networking, battery, memory, and sensor behavior. Cover both.
- **Cold install** — test a fresh install (not just a rebuild over the old
  version) to catch first-launch, storage, and migration bugs.
- **Device matrix** — cover the OS versions and screen sizes you declared in
  scope, plus low-memory and low-storage conditions. Use a device farm
  (Firebase Test Lab, BrowserStack, Xcode Cloud) when the matrix outgrows local
  hardware.
- **Debug and release parity** — the debug build and the release build are
  different programs (proguard/minification, stripping, optimization). Smoke
  test the signed release artifact before store submission.

### 4. Ship to stores

Submission is a checklist, not an afterthought:

- **Test track first** — distribute to TestFlight (iOS) and an internal or
  closed testing track (Android) before production; the store will not be your
  first real device feedback loop.
- **Store readiness** — metadata, screenshots, privacy policy, data-collection
  declarations, and privacy nutrition labels must match what the app actually
  does. Review requirements change; re-check them near submission time.
- **Review expectations** — both stores reject apps for missing privacy
  disclosures, misleading metadata, crashes on launch, and broken sign-in or
  in-app purchase flows. Run the app through the platform's review checklist
  before uploading.
- **Rollout** — prefer staged rollouts (phased release on Play, gradual
  release on App Store Connect) so a regression reaches few users before it
  reaches everyone.

## Mobile-Specific Concerns

These concerns are where mobile engineering differs from web and desktop work.

### App lifecycle and backgrounding

Mobile OSes kill and suspend apps aggressively; the lifecycle is not optional:

- **Lifecycle states** — iOS (foreground/background/inactive, scene-based
  lifecycle) and Android (activity/fragment states, process death). State that
  is not persisted across these transitions is lost.
- **Background execution is a privilege** — both platforms restrict background
  work. Use the platform's sanctioned mechanisms (background modes, `WorkManager`,
  background fetch, push-driven wakeups) instead of fighting the OS.
- **Process death** — the OS can kill the app at any time. Save in-progress
  state, and restore UI state from storage on relaunch, not from memory.

### Offline and sync

Mobile networks are unreliable; offline is a first-class mode:

- **Offline-first storage** — local persistence (Core Data, Room, SQLite-based
  stores, or key-value stores) is the source of truth while disconnected;
  the network is a sync channel, not a dependency.
- **Sync semantics** — define conflict resolution (last-write-wins, per-field
  merge, or explicit conflict UI), idempotent writes, and retry with backoff.
  Never blindly overwrite newer remote data with stale local data.
- **Queue mutations** — writes made offline must be queued and replayed in
  order when connectivity returns, with a clear sync state surfaced to the user.

### Mobile-specific testing

Beyond unit tests, mobile code needs platform-aware testing:

- **Unit and widget/component tests** — framework-level logic, reducers, and
  state without a device (XCTest, JUnit, Flutter widget tests, Jest).
- **UI/instrumentation tests** — drive the real UI on a device or emulator
  (XCUITest, Espresso/Compose UI tests, Flutter `integration_test`, Detox).
- **Device-farm coverage** — run the UI suite across the device matrix on a
  farm; a test that passes on one device is not a guarantee.
- **Performance and battery** — measure launch time, frame rate, memory, and
  network on device, not just functionality.

## Core Principles

**Pick the framework by the constraints, not the hype** — native iOS and
Android give the deepest platform integration; Flutter and React Native give
shared code across platforms. The right choice depends on team skills, the
device APIs the app needs, and how much per-platform work is acceptable. Match
the decision to the app's actual requirements.

**The OS lifecycle is part of the contract** — mobile apps are suspended,
killed, and backgrounded constantly. Any feature that assumes the app is always
alive and online will break. Design for process death and disconnection from
the first commit.

**Signing and builds are release engineering, not CI garnish** — an app that
cannot be reproducibly built and signed cannot be released, patched, or
audited. Keep signing assets secret, pinned, and scriptable, and treat the
release pipeline as production infrastructure.

**Test the artifact you ship** — the signed release build, not the debug build,
is what users and reviewers see. Smoke-test it on a real device before it
reaches TestFlight, Play, or the App Review team.

**Store requirements are moving targets** — privacy declarations, target API
levels, and submission formats change every year. Verify requirements against
the current store documentation near submission time rather than relying on
remembered rules.

## Related skills

- [frontend-engineering](../frontend-engineering/SKILL.md) — web frontend
  methodology; the sibling family-skill precedent this skill mirrors, and the
  routing target for browser-based UI work.
- [backend-engineering](../backend-engineering/SKILL.md) — the APIs and
  services mobile apps consume; the routing target for server-side work.
- [release-engineering](../release-engineering/SKILL.md) — release
  orchestration, versioning, and rollout methodology; store releases are one
  instance of the discipline.
- [qa-methodology](../qa-methodology/SKILL.md) — test strategy and quality
  gates; the routing target for product-wide test planning.
- [platform-engineering](../platform-engineering/SKILL.md) — CI/CD pipelines
  and build infrastructure for shipping mobile builds at scale.
