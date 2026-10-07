---
name: revenuecat-customer-center
description: "Add the RevenueCat Customer Center (self service subscription management UI) to an app. Use when the user asks to add a customer center, build a self service subscriptions screen, let users manage subscriptions in app, add a subscription management screen, present CustomerCenterView, call presentCustomerCenter, or wire a 'manage subscription' button to the RevenueCat customer center on iOS, Android, Kotlin Multiplatform, Flutter, or React Native."
---

# revenuecat-customer-center: add the RevenueCat Customer Center

Use this skill when the user wants an out of the box UI that lets their customers manage active subscriptions, request refunds, cancel, restore, or contact support, without shipping custom UI. The UI is configured in the RevenueCat dashboard and rendered by the `RevenueCatUI` SDKs.

Prerequisite: `integrate-revenuecat` has already run. `Purchases.configure(…)` must succeed before the Customer Center can load customer data.

## 1. Detect the platform

Inspect the working directory and pick the **first** match, from top to bottom:

1. **React Native**: `package.json` has a `react-native-purchases` entry, or `react-native` as a dependency. The Customer Center ships in `react-native-purchases-ui`. Read `platforms/react-native.md`. If `expo` is also a dependency, note it as an Expo project.
2. **Flutter**: `pubspec.yaml` exists at the project root. The Customer Center ships in `purchases_ui_flutter`. Read `platforms/flutter.md`.
3. **Kotlin Multiplatform**: `build.gradle.kts` has a `kotlin { … }` multiplatform block, or depends on `com.revenuecat.purchases:purchases-kmp*`. The Customer Center composable is in `purchases-kmp-ui`. Read `platforms/kmp.md`.
4. **Android (native)**: `build.gradle(.kts)` applies `com.android.application` (and is not KMP). The Customer Center composable is in `com.revenuecat.purchases:purchases-ui`. Read `platforms/android.md`.
5. **iOS (native)**: `Package.swift`, `*.xcodeproj`, `*.xcworkspace`, or `Podfile` at the project root. `CustomerCenterView` is in `RevenueCatUI`. Read `platforms/ios.md`.

If several match (e.g. an `ios/` folder inside a Flutter project), pick the **outermost** project, the one that owns the build. If still ambiguous, ask the user which platform they want to configure.

## 2. Shared concepts (all platforms)

- **Customer Center is a dashboard configured UI.** Actions, copy, promotional offers, refund flows, cancel survey options, and support contact details are defined in the RevenueCat dashboard under **Customer Center**. Without configuration, the view renders a minimal default layout; users will see almost nothing useful.
- **It needs an identified user with purchases** to surface anything meaningful. If the user is anonymous and has never bought anything, the Customer Center renders an empty / restore only state. If the app supports login, call `Purchases.logIn(userId)` before opening the Customer Center.
- **Customer Center is separate from paywalls.** The standard pattern: expose a "Manage subscription" row in the settings screen that opens the Customer Center. Paywalls are for new purchases; the Customer Center is for existing subscribers.
- **The UI owns the flow.** Restore, cancel, refund, and promotional offer flows run inside the component. Listen for the lifecycle callbacks (`onRestoreCompleted`, `onRefundRequestStarted`, `onManagementOptionSelected`, `onPromotionalOfferSucceeded`, etc.) to react in app code, not to drive the flow.
- **Platform availability varies.** iOS has had Customer Center longest; Android, KMP, Flutter, and React Native follow. Platform files flag any gaps. Refund requests are an iOS only action because only Apple exposes in app refund requests; on Android, the "Manage subscription" option links out to the Google Play subscriptions screen.
- **If the installed SDK version is older than Customer Center support**, the fallback is a manual subscription management screen: show the user's active entitlements from `Purchases.customerInfo()`, expose a `Purchases.restorePurchases()` button, and link to the store's subscription management URL. Point the user to upgrade the SDK if they want the full Customer Center.

## 3. Implementation

Read the platform file that matches detection:

- `platforms/ios.md`
- `platforms/android.md`
- `platforms/kmp.md`
- `platforms/flutter.md`
- `platforms/react-native.md`

Each platform file is self contained: install command, exact snippet to present the Customer Center, and the callback shape.

## 4. Verify

Do not claim the integration is complete until:

1. The project **builds** on the target platform.
2. Sign into the app with a test user that has **at least one active sandbox subscription**. Trigger the code path that opens the Customer Center. The UI loads and the subscription appears in the list.
3. At least one configured action runs end to end. The simplest check: tap **Restore purchases** and confirm the restore completed callback fires with a non-empty `customerInfo.entitlements.active` map. If the dashboard has Cancel / Refund / Support actions configured, verify the corresponding callback (`onManagementOptionSelected`, `onRefundRequestStarted`, etc.) fires when the user taps through.
4. Dismissing the Customer Center fires the `onDismiss` callback.

If the Customer Center opens but is empty, the signed in user has no purchases, or the dashboard Customer Center section is not configured. Fix in the dashboard, reload, and retry.
