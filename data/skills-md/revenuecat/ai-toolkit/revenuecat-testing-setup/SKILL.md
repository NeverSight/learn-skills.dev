---
name: revenuecat-testing-setup
description: Set up a testing environment for RevenueCat purchases without charging real money. Use when the user says test RevenueCat purchases, sandbox setup, StoreKit configuration file, license tester, how do I test purchases without real money, set up sandbox account, internal testing track, or test paywall on iOS, Android, Kotlin Multiplatform, Flutter, or React Native.
---

# revenuecat-testing-setup: set up a testing environment for RevenueCat purchases

Use this skill when the user wants to test purchases against RevenueCat without charging real money. Each store has its own testing channel, and each channel has different fidelity and iteration cost.

## 1. Detect the platform

Inspect the working directory and pick the **first** match, from top to bottom:

1. **React Native**: `package.json` has a `react-native-purchases` entry, or `react-native` as a dependency → read `platforms/react-native.md`. If `expo` is also a dependency, note it as an Expo project.
2. **Flutter**: `pubspec.yaml` exists at the project root → read `platforms/flutter.md`.
3. **Kotlin Multiplatform**: `build.gradle.kts` contains a `kotlin { … }` multiplatform source sets block, or depends on `com.revenuecat.purchases:purchases-kmp*` → read `platforms/kmp.md`.
4. **Android (native)**: `build.gradle(.kts)` applies `com.android.application` (and is not KMP) → read `platforms/android.md`.
5. **iOS (native)**: `Package.swift`, `*.xcodeproj`, `*.xcworkspace`, or `Podfile` at the project root → read `platforms/ios.md`.

If several match (e.g. an `ios/` folder inside a Flutter project), pick the **outermost** project, the one that owns the build. If still ambiguous, ask the user which platform they want to configure.

## 2. Shared concepts (all platforms)

### You cannot charge real money during development

Each store has a dedicated testing channel. Choosing the right channel depends on what you want to test.

### Testing channels by fidelity vs iteration cost

Higher fidelity exercises more of the real purchase pipeline. Lower fidelity iterates faster.

- **RevenueCat Test Store (lowest fidelity, fastest iteration, deterministic).** A synthetic store hosted by RevenueCat. The SDK is configured with a `test_…` API key from the dashboard. Purchases open a Test Store dialog where you pick the outcome by hand: Successful Purchase, Failed Purchase, or Cancel. Purchases trigger entitlements, update `CustomerInfo`, and appear on the dashboard, but no Apple or Google call happens. Best for paywall iteration, integration tests, and CI smoke runs.
- **iOS StoreKit Configuration File (low fidelity, Apple synthetic).** Xcode stubs the store locally. Purchases succeed instantly with no App Store Connect round trip. Useful when you need StoreKit specific behavior. RevenueCat transactions in this mode may or may not appear on the dashboard depending on SDK version and intended routing, so it is not a faithful dashboard test.
- **iOS Sandbox (real sandbox Apple ID) / Android Internal Testing (license tester).** Real store backends, real RevenueCat dashboard ingestion, real receipts. Slower to iterate: build, install, wait for Play propagation or App Store Connect to register the product.
- **TestFlight (iOS) / Closed or Open Testing (Android).** Behaves very close to production. Receipts are production style. Transactions land in the **production** RevenueCat dashboard, not the Sandbox view.
- **Production.** Real money. Do not use for testing.

Start with the lowest fidelity that answers the question, then move up. UI and paywall iteration belongs in the fast channel. "Does my entitlement actually flip?" belongs in sandbox or internal testing.

### Test Store: when to reach for it before sandbox

RevenueCat's Test Store is a synthetic store provider configured per project on the dashboard. It produces real RevenueCat backend records (`CustomerInfo` updates, entitlement transitions, dashboard transactions) without calling App Store or Google Play. The price of that speed is fidelity. Test Store does not simulate Ask to Buy approval flows, region specific pricing, server side receipt validation specifics, store level review or rejection paths, or full subscription renewal cadence (Test Store renews up to five times on a compressed clock).

Use Test Store when you want to iterate on UI quickly, write integration tests with deterministic outcomes, or run CI checks. Move up to App Store Sandbox or Google Play Internal Testing for anything that exercises store side behavior.

**Setup.** In the dashboard, go to **Apps and providers** → _Test configuration_ section → **Test Store** → Create / Enable. The Test Store API key appears under **Project Settings → API keys** with a `test_` prefix. Configure the SDK with the test key in debug builds and the production key (`appl_…` / `goog_…`) in release builds. The platform files show the per platform key swap pattern.

Test Store keys must never ship to production. Gate the key behind your build configuration so release binaries cannot route through Test Store.

### Sandbox transactions appear separately on the dashboard

The RevenueCat dashboard has a toggle between **Sandbox** and **Production** views. Sandbox purchases only appear under Sandbox. If a test transaction does not appear there, the SDK is not reporting it (check API key, `configure` call, and network), or the purchase was against a StoreKit config file that does not hit RevenueCat's backend.

### Accelerated renewal in sandbox

Subscription renewals run on accelerated test clocks in sandbox. This lets you exercise renewal logic in minutes instead of weeks.

- iOS sandbox renewal cadence (per Apple's documentation): daily → every 3 minutes, weekly → every 3 minutes, monthly → every 5 minutes, 2 months → every 10 minutes, 3 months → every 15 minutes, 6 months → every 30 minutes, yearly → every hour. Subscriptions auto-renew a maximum of 6 times then expire.
- Android sandbox renewal cadence is documented in Google Play Console → Subscriptions testing. License tester subscriptions renew on the same accelerated clock.

### Use a fresh test user for first purchase flows

Purchase history is attached to the test account (sandbox Apple ID or license tester Gmail) and persists. Testing "first purchase" logic, introductory offers, or free trials against an account that has already used them produces misleading results. Create a new sandbox tester for clean first purchase scenarios.

### Confirm against the dashboard, not the device

A purchase succeeding on the device is not the same as RevenueCat recording it. Always confirm:

1. The transaction appears on the RevenueCat dashboard (Sandbox view).
2. The expected appUserID owns the transaction.
3. The expected entitlement is now active on that user.

If the device shows success but the dashboard shows nothing, something is wrong in the configuration path, not the store.

## 3. Implementation

Read the platform file that matches detection:

- `platforms/ios.md`
- `platforms/android.md`
- `platforms/kmp.md`
- `platforms/flutter.md`
- `platforms/react-native.md`

## 4. Verify

Your testing environment is set up once:

1. A test purchase succeeds end to end from a test user.
2. The transaction appears on the RevenueCat dashboard Sandbox view, attached to the appUserID you logged in with.
3. The expected entitlement is active on `customerInfo` after the purchase completes.
4. Restoring purchases on a fresh install of the app restores the entitlement to the same test user.

If any of those four steps fails, the environment is not ready. The `revenuecat-troubleshoot` skill covers the usual root causes.
