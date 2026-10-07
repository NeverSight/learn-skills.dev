---
name: revenuecat-identify-user
description: Tie RevenueCat identity to your app's auth system. Use when the user asks to log in to RevenueCat, sync a user with RevenueCat, switch RevenueCat user on login, log out of RevenueCat, move a user from anonymous to identified, set appUserID, or handle account switching on iOS, Android, Kotlin Multiplatform, Flutter, or React Native.
---

# revenuecat-identify-user: connect RevenueCat to your auth system

Use this skill when the user wants to call `logIn` / `logOut` on the RevenueCat SDK so that their app users line up with RevenueCat subscribers. This skill does not cover initial SDK setup (see `integrate-revenuecat`), purchases (`revenuecat-purchase-flow`), or gating (`revenuecat-entitlements-gate`).

## 1. Detect the platform

Inspect the working directory and pick the **first** match, from top to bottom:

1. **React Native**: `package.json` has a `react-native-purchases` entry, or `react-native` as a dependency → read `platforms/react-native.md`. If `expo` is also a dependency, note it as an Expo project.
2. **Flutter**: `pubspec.yaml` exists at the project root → read `platforms/flutter.md`.
3. **Kotlin Multiplatform**: `build.gradle.kts` contains a `kotlin { … }` multiplatform source sets block, or depends on `com.revenuecat.purchases:purchases-kmp*` → read `platforms/kmp.md`.
4. **Android (native)**: `build.gradle(.kts)` applies `com.android.application` (and is not KMP) → read `platforms/android.md`.
5. **iOS (native)**: `Package.swift`, `*.xcodeproj`, `*.xcworkspace`, or `Podfile` at the project root → read `platforms/ios.md`.

If several match (e.g. an `ios/` folder inside a Flutter project), pick the **outermost** project, the one that owns the build. If still ambiguous, ask the user which platform they want to configure.

## 2. Shared concepts (all platforms)

- **Anonymous by default.** Before `logIn` is called, RevenueCat assigns a stable anonymous ID prefixed `$RCAnonymousID:`. Purchases made while anonymous are aliased onto the real `appUserID` the first time `logIn` is called with it, so there is no "lost purchase" risk from letting users buy before signing in.
- **Never use email, phone number, or a sequential database id as the appUserID.** Use a stable opaque value such as your backend's user UUID, or a hash of the user id. RevenueCat treats the ID as an opaque string and it is difficult to change later.
- **Call `logIn` after your auth system confirms the session.** Do not call `logIn` speculatively. The typical trigger is your auth state listener firing with a signed in user. `logIn` returns both the user's current `CustomerInfo` and a `created: Boolean` that tells you whether this is a brand new RevenueCat customer.
- **`logOut` only works on identified users.** Calling `logOut` while the SDK is on an anonymous ID throws an error in every SDK (`PurchasesErrorCode.LogOutWithAnonymousUserError` or the iOS equivalent). Gate it behind your own "is signed in" flag.
- **Restore is not login.** `restorePurchases()` asks the store for the current receipt and attaches it to the current RevenueCat user. It does not switch identities. If the user signs in on a new device, call `logIn(appUserID)` first, then `restorePurchases()` only if they also expect to pull a receipt from the current store account.
- **Account switching is `logOut` then `logIn`.** If your app lets a user sign out and sign back in as someone else, call `logOut()` first, wait for it, then `logIn(newId)`. Do not try to swap directly with a second `logIn`, since that will alias the two IDs together.
- **Configure first.** `Purchases.configure(…)` must have run before `logIn` / `logOut`. If it has not, the SDK throws.

## 3. Implementation

Read the platform file that matches detection:

- `platforms/ios.md`
- `platforms/android.md`
- `platforms/kmp.md`
- `platforms/flutter.md`
- `platforms/react-native.md`

Each platform file shows the `logIn` and `logOut` calls wired into a typical auth state observer.

## 4. Verify

Do not claim identity sync works until:

1. In the RevenueCat dashboard, the Customer page for your test user shows the **same** appUserID your backend uses, not the `$RCAnonymousID:` placeholder.
2. Signing out clears the ID back to a fresh anonymous user; signing in as a different account switches to that account's purchases (or shows none if it is a new account).
3. A purchase made while anonymous, followed by `logIn`, remains attached to the signed in user (aliased, not lost).
4. Calling `logOut` while already anonymous is handled, not treated as a crash or a silent success.
