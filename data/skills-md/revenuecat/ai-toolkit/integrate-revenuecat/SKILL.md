---
name: integrate-revenuecat
description: End-to-end RevenueCat integration — sets up the dashboard side via the RevenueCat MCP or the `rc` CLI (project, app, public API key) and installs/configures the Purchases SDK in the app. Use when the user asks to add RevenueCat, hook up RevenueCat, add subscriptions or in-app purchases to an app, integrate Purchases, install the RevenueCat SDK, set up a RevenueCat API key, configure Purchases on launch, or set up a brand new RevenueCat integration on iOS, Android, Kotlin Multiplatform, Flutter, or React Native.
---

# integrate-revenuecat: end-to-end RevenueCat integration

Use this skill when the user wants to add RevenueCat to a project for the first time, or to reconfigure the SDK with a public API key. The skill covers two halves:

1. **Dashboard side** — set up the project, register the app, and obtain the public API key, through the RevenueCat MCP server or the `rc` CLI.
2. **App side** — install the Purchases SDK, call `Purchases.configure(…)` at app entry, and verify the configuration banner in the logs.

Once the SDK is configured, settle **how the paywall is built** (Section 5c) before writing any paywall code.

Walk them in order. Most integrations need both halves, even when the user asks "just install the SDK" — the SDK needs an API key from the dashboard.

> If a project + app already exist and the user only wants to wire the SDK into code, jump to **Section 3** below.
> If the user wants to bootstrap a brand new RevenueCat project (apps + products + entitlements + offerings), use the `create-revenuecat-project` skill instead, then come back here for the SDK install.

## Arguments

Available as `$ARGUMENTS` when invoked as a slash command:

- `platform` (optional): One of `ios`, `android`, `kmp`, `flutter`, `react-native`. If omitted, run the detection algorithm in Section 3a.
- `app_identifier` (optional): Bundle ID (iOS) or package name (Android). If omitted, read it from the project files (`Info.plist`, `AndroidManifest.xml`, `app.json`, `pubspec.yaml`).
- `project_name` (optional): Name of the RevenueCat project to use. If omitted, list projects (via MCP or `rc projects list`) and ask the user.

## 1. Understand the status quo

Before touching the dashboard, gather the facts:

- **Platform target**: iOS / Apple App Store, Android / Google Play, or both. Inspect the working directory before asking — the detection algorithm in Section 3 makes this obvious for most projects.
- **Technology**: native iOS (Swift), native Android (Kotlin / Java), React Native, Flutter, Kotlin Multiplatform. SDK list: https://www.revenuecat.com/docs/getting-started/installation.md.
- **App identifier**: bundle ID (iOS), package name (Android). Pull from `Info.plist` / `AndroidManifest.xml` / `app.json` / `pubspec.yaml` rather than asking.

## 2. Dashboard side

Use whichever surface the user has available: the RevenueCat MCP server or the `rc` CLI (see the `revenuecat-cli` skill for CLI discovery and conventions). Both cover the same operations for these steps, and each step below notes the MCP tool and the `rc` command.

### 2a. Get or create the project
- List accessible projects: `list-projects` (MCP) or `rc projects list`. If multiple, ask the user which one matches this app, or offer to create a new one (`create-project` / `rc projects create`).
- If there is no project, hand off to the `create-revenuecat-project` skill, then resume here.
- Store the `project_id` for the rest of the steps.

### 2b. Get or create the app
- Check which apps are already configured in the project (`list-apps` / `rc apps list`). A `test_store` app is always present; `app_store` and `play_store` apps are present only if the user has finished store-side setup.
- Ask the user whether their app is already set up in App Store Connect (iOS) or Google Play Console (Android). Reassure them that store-side setup can come later — the `test_store` app is enough to start integrating.
- If the user confirms store-side setup is done, call `create-app` (or `rc apps create`):
  - **iOS**: `type: "app_store"`, `bundle_id` from Section 1.
  - **Android**: `type: "play_store"`, `package_name` from Section 1.
  - `name` derived from the identifier or asked from the user.

### 2c. Get the public API key
- List public keys for the relevant app ID: `list-public-api-keys` (MCP) or `rc apps keys <app-id>`:
  - `app_store` / `play_store` if the store-side app exists.
  - Otherwise the `test_store` app.
- The returned key is **public** and safe to embed in client app code. iOS keys are prefixed `appl_…`, Android keys `goog_…`, Amazon `amzn_…`.

> **Never use the secret API key in client code.** Secret keys are server-side only.

## 3. App side — install and configure the SDK

### 3a. Detect the platform

Inspect the working directory and pick the **first** match, from top to bottom:

1. **React Native**: `package.json` has a `react-native-purchases` entry, or `react-native` as a dependency → read `platforms/react-native.md`. If `expo` is also a dependency, note it as an Expo project.
2. **Flutter**: `pubspec.yaml` exists at the project root → read `platforms/flutter.md`.
3. **Kotlin Multiplatform**: `build.gradle.kts` contains a `kotlin { … }` multiplatform source sets block, or depends on `com.revenuecat.purchases:purchases-kmp*` → read `platforms/kmp.md`.
4. **Android (native)**: `build.gradle(.kts)` applies `com.android.application` (and is not KMP) → read `platforms/android.md`.
5. **iOS (native)**: `Package.swift`, `*.xcodeproj`, `*.xcworkspace`, or `Podfile` at the project root → read `platforms/ios.md`.

If several match (e.g. an `ios/` folder inside a Flutter project), pick the **outermost** project, the one that owns the build. If still ambiguous, ask the user which platform they want to configure.

### 3b. Shared concepts (all platforms)

- **Public SDK key, not secret key.** RevenueCat issues a separate public SDK key per store/platform. iOS apps use an `appl_…` key, Android apps use a `goog_…` key (Amazon uses `amzn_…`). Server-side secret keys must never appear in client apps.
- **Configure once per app launch.** Call `Purchases.configure(…)` exactly once, as early as possible (app entry point). Later calls no-op or warn.
- **Anonymous users by default.** If you don't pass an `appUserID`, RevenueCat creates a stable anonymous ID. Only pass `appUserID` if you already have an authenticated user at launch; otherwise call `logIn(…)` later (see the `revenuecat-identify-user` skill).
- **Enable debug logging during integration.** Each platform file shows how. Turn it off for release builds.
- **Keep keys out of source control.** Recommend `.env` (RN), `xcconfig` (iOS), `local.properties` / `gradle.properties` (Android), or dart-define (Flutter) when the user asks about secret management.

### 3c. Implementation

Read the platform file that matches detection:

- `platforms/ios.md`
- `platforms/android.md`
- `platforms/kmp.md`
- `platforms/flutter.md`
- `platforms/react-native.md`

Each platform file is self-contained: install command, exact `configure` snippet, and where to place it in the app entry point.

## 4. Verify

Do not claim setup is complete until:

1. The project **builds** (Xcode build, `./gradlew assembleDebug`, `flutter run`, `npx react-native run-ios`, or the KMP equivalent).
2. The app launches and the RevenueCat SDK logs a configuration banner in the console / logcat / Metro output (each platform file describes the expected log line).
3. No authentication errors appear on the first SDK network call. A wrong API key surfaces as an auth error log as soon as the app fetches offerings.

If the user only asked to "install" without running the app, tell them what to look for in the logs when they do run it.

## 5. Next steps

### 5a. Products, entitlements, offerings
Check whether products, entitlements, and offerings are already set up in the project. If not, offer to help via the `create-revenuecat-project` skill.

### 5b. Store-side setup

**iOS (App Store Connect)**

1. **In-App Purchase Key (recommended for StoreKit 2)** — App Store Connect → Users and Access → Integrations → In-App Purchase. Generate key, download the `.p8` file. Note the Key ID and Issuer ID.
2. **Shared Secret (legacy StoreKit 1)** — App Store Connect → App → App Information → App-Specific Shared Secret.
3. If the user provides this information, register it on the RevenueCat side via `create-app` / `update-app`.

**Android (Google Play Console)**

1. **Service account credentials** — Create a service account in Google Cloud Console. Grant "Service Account User" role. Create a JSON key. In Play Console, grant the service account access with "View financial data" permission.
2. **Real-time Developer Notifications (RTDN)** — Set up a Cloud Pub/Sub topic. Configure in Play Console → Monetization setup.
3. If the user provides this information, register it via `create-app` / `update-app`.

### 5c. Choose how the paywall is built

The app still needs a paywall, and there are two ways to build one. This is a product decision, not an implementation detail, so settle it before writing any paywall code.

- **RevenueCat Paywall (recommended default).** Hosted by RevenueCat and rendered by RevenueCatUI. You create it yourself: load the `revenuecat-paywall-design` skill and follow its creating workflow (`create-paywall-ai` via MCP or `rc paywalls generate` via CLI, attached to the current offering and informed by the app's codebase), then present it with `revenuecat-paywall`. The user does not have to design anything in the dashboard; they can refine it later in the paywall builder. Design, copy, and packages change without an app release, and paywall variants can be A/B tested with RevenueCat Experiments.
- **Custom paywall in code.** The app's own UI, with packages and prices from `getOfferings()` and the purchase handled by `revenuecat-purchase-flow`. Full visual control, but every design change ships in an app release and the paywall design cannot be A/B tested. Price and offering tests still work, because packages come from the offering.

Pick the path:

1. **The user already said which one.** Use it.
2. **The app has no paywall screen yet.** Recommend a RevenueCat Paywall.
3. **The app already has a paywall or subscription screen** (a screen listing plans or prices, a subscribe or upgrade button, hardcoded prices or product IDs). The user most likely wants that screen wired to offerings. Recommend keeping it, and mention that a RevenueCat Paywall could replace it.

If you can ask the user, ask one question with both options, the recommended one first, each with a one-line trade-off. If you cannot ask (for example, you are running non-interactively), do not stop: take the recommendation above, and in your summary say which path you took and how to switch to the other.

Do not hand-code a paywall screen by default just because it keeps the work in code. A new RevenueCat Paywall is an unpublished draft: tell the user to review it in the paywall builder, and publish it only when they ask, because the app renders the default fallback layout until a paywall is published and attached to the offering.

### 5d. Subsequent skills

Common follow-ups after `integrate-revenuecat`:

- `revenuecat-paywall-design` — create or edit the dashboard paywall.
- `revenuecat-paywall` — display a dashboard-configured paywall.
- `revenuecat-purchase-flow` — implement purchase + restore for a custom paywall.
- `revenuecat-entitlements-gate` — gate features behind active entitlements.
- `revenuecat-identify-user` — wire `logIn` / `logOut` to the app's auth system.
- `revenuecat-testing-setup` — set up a sandbox testing channel.
- `revenuecat-troubleshoot` — diagnose offerings / products / entitlement bugs.
