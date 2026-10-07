---
name: revenuecat-entitlements-gate
description: "Check whether a RevenueCat user currently has access to a paid feature via entitlements. Use when the user asks to gate a feature behind premium, check if the user has a pro subscription, read customerInfo active entitlements, show or hide a feature based on subscription status, react to entitlement changes, or 'is the user subscribed' on iOS, Android, Kotlin Multiplatform, Flutter, or React Native."
---

# revenuecat-entitlements-gate: check a RevenueCat entitlement

Use this skill when the user wants to decide whether to show or hide a feature based on an active RevenueCat entitlement. The skill covers the one shot check and the reactive listener; it does not cover purchasing (see `revenuecat-purchase-flow`) or auth (`revenuecat-identify-user`).

## 1. Detect the platform

Inspect the working directory and pick the **first** match, from top to bottom:

1. **React Native**: `package.json` has a `react-native-purchases` entry, or `react-native` as a dependency → read `platforms/react-native.md`. If `expo` is also a dependency, note it as an Expo project.
2. **Flutter**: `pubspec.yaml` exists at the project root → read `platforms/flutter.md`.
3. **Kotlin Multiplatform**: `build.gradle.kts` contains a `kotlin { … }` multiplatform source sets block, or depends on `com.revenuecat.purchases:purchases-kmp*` → read `platforms/kmp.md`.
4. **Android (native)**: `build.gradle(.kts)` applies `com.android.application` (and is not KMP) → read `platforms/android.md`.
5. **iOS (native)**: `Package.swift`, `*.xcodeproj`, `*.xcworkspace`, or `Podfile` at the project root → read `platforms/ios.md`.

If several match (e.g. an `ios/` folder inside a Flutter project), pick the **outermost** project, the one that owns the build. If still ambiguous, ask the user which platform they want to configure.

## 2. Shared concepts (all platforms)

- **Check the entitlement identifier, not the product ID.** The identifier (for example `"premium"`) is configured in the RevenueCat dashboard and mapped to one or more products. Using the entitlement lets you change products, prices, and stores without touching app code.
- **`customerInfo.entitlements.active` is the source of truth.** It is a `Map<String, EntitlementInfo>` keyed by entitlement identifier. Presence in `active` means the user currently has access. Absence means they do not, regardless of past purchases.
- **Do not gate on purchase history.** Expired subscriptions still appear in `customerInfo.entitlements.all` but drop out of `active`. Use `active` only.
- **Fetch once, then subscribe.** The first `customerInfo` call returns a cached value quickly, and the SDK refreshes in the background. Every SDK exposes a listener or stream that fires when entitlements change (after a purchase, restore, renewal, or expiration). Subscribe to that instead of polling.
- **The SDK must be configured first.** If `Purchases.configure(…)` has not run, the entitlement call will fail. Set up the SDK via `integrate-revenuecat` before using this skill.

## 3. Implementation

Read the platform file that matches detection:

- `platforms/ios.md`
- `platforms/android.md`
- `platforms/kmp.md`
- `platforms/flutter.md`
- `platforms/react-native.md`

Each platform file shows the one shot check, the reactive subscription, and where to place each in a typical app.

## 4. Verify

Do not claim the gate works until:

1. A user with an active entitlement sees the gated feature, and a user without it does not.
2. When the entitlement state changes (test with a sandbox purchase or a manual grant in the dashboard), the UI updates without a manual restart, confirming the listener is wired.
3. The entitlement identifier in the code matches an identifier that exists in the RevenueCat dashboard. A typo here silently gates everyone out.
