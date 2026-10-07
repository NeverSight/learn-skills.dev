---
name: revenuecat-troubleshoot
description: Diagnose and resolve RevenueCat integration issues — inspects dashboard configuration through the RevenueCat MCP, walks the SDK debug logs, and covers code-side gotchas. Use when the user says offerings are empty, products not loading, entitlement not active after purchase, paywall won't load, transactions not appearing, customer info shows no entitlements, sandbox purchase not working, or RevenueCat is broken on iOS, Android, Kotlin Multiplatform, Flutter, or React Native.
---

# revenuecat-troubleshoot: diagnose RevenueCat integration problems

Use this skill when the user reports a RevenueCat behavior that does not match expectations: empty offerings, missing products, an entitlement that does not unlock after a successful purchase, a paywall that fails to render, or sandbox transactions that never reach the dashboard.

This skill combines two angles:

1. **Code-side diagnosis** — turn on debug logging, walk a universal checklist, drop into platform specifics.
2. **Dashboard inspection** — use the RevenueCat MCP server or the `rc` CLI (see the `revenuecat-cli` skill) to read the project, apps, products, entitlements, offerings, and webhooks, and offer fixes.

Work them in order. Most reports resolve before you reach the platform specifics.

## 1. Detect the platform

Inspect the working directory and pick the **first** match, from top to bottom:

1. **React Native**: `package.json` has a `react-native-purchases` entry, or `react-native` as a dependency → read `platforms/react-native.md`. If `expo` is also a dependency, note it as an Expo project.
2. **Flutter**: `pubspec.yaml` exists at the project root → read `platforms/flutter.md`.
3. **Kotlin Multiplatform**: `build.gradle.kts` contains a `kotlin { … }` multiplatform source sets block, or depends on `com.revenuecat.purchases:purchases-kmp*` → read `platforms/kmp.md`.
4. **Android (native)**: `build.gradle(.kts)` applies `com.android.application` (and is not KMP) → read `platforms/android.md`.
5. **iOS (native)**: `Package.swift`, `*.xcodeproj`, `*.xcworkspace`, or `Podfile` at the project root → read `platforms/ios.md`.

If several match (e.g. an `ios/` folder inside a Flutter project), pick the **outermost** project, the one that owns the build. If still ambiguous, ask the user which platform the bug reproduces on.

## 2. Universal code-side checklist

Walk these nine items in order. Most reports are resolved by steps 1 through 5.

1. **Turn on debug logging and reproduce.** The SDK narrates what it is doing. Roughly 80% of reports are diagnosable from the log output alone. Each platform file shows how to set `logLevel` to debug.
2. **Verify the API key platform matches the app.** iOS apps must use an `appl_…` public SDK key. Android apps must use `goog_…` (or `amzn_…` for Amazon). A mismatched key produces an authentication error on the first network call. On iOS this surfaces as an `INVALID_CREDENTIALS` error code. On Android it surfaces as `PurchasesErrorCode.InvalidCredentialsError`. Use the `list-app-public-api-keys` RevenueCat MCP tool to list the API keys for the project.
3. **Verify the bundle ID / package name matches the one set up in the RevenueCat project.** 
List the apps using the `list-apps` RevenueCat MCP tool. The `bundle_id` (iOS / App Store) or `package_name` (Android / Play Store / Amazon Appstore) registered there must match the built app exactly, including capitalization. A mismatch causes offerings to come back empty because the app is not recognized.
4. **Verify offerings in the RevenueCat project.** List the project's offerings using the `list-offerings` RevenueCat MCP tool, passing the parameter `expand=items.package.product`. The offering marked with `is_current: true` must have at least one package attached, and each package must reference a store product. An offering with zero packages returns an empty `availablePackages` list even though `getOfferings` succeeds.
5. **Verify store products are live.** Products must be in "Ready to Submit" on App Store Connect or "Active" on Google Play Console. A product in a draft state will not be returned by the store, even in sandbox. If the SDK logs show offerings arriving from RevenueCat but products failing to resolve, this is almost always the cause. Use the `get-product-store-state` RevenueCat MCP tool to understand the state of product in App Store Connect or Google Play Console (field `store_status`). To fix or change the store state (not just read it), follow the `revenuecat-store-state` skill.
6. **Verify the testing account.** iOS: the device must be signed into a Sandbox Apple ID under Settings → App Store → Sandbox Account (set on iOS 14+ after the first sandbox prompt). Android: the tester's Gmail must be added to Google Play Console → Setup → License testing, and the app must be installed via the Internal Testing opt-in link, not sideloaded.
7. **Verify the network.** Corporate VPNs, captive portals, and some DNS filters silently block the RevenueCat API or the store APIs. Try a different network before digging deeper.
8. **Verify the appUserID.** If `logIn(appUserID)` was called with an ID that does not match what the user expects, entitlements appear missing because they are attached to a different RC user. Print `Purchases.shared.appUserID` (iOS) / `Purchases.sharedInstance.appUserID` (Android) and confirm it matches.
9. **Reset and retry.** Uninstall the app, re-sign into the sandbox / tester account, reinstall from the correct channel, relaunch.

## 3. Dashboard inspection via the RevenueCat MCP or the `rc` CLI

Use this when steps 3, 4, or 5 above point at dashboard configuration, when the user has no working app yet, or when you need to confirm a fix landed.

**Important:** The API key may have access to multiple projects. Always call `list-projects` first. If multiple projects are returned, ask the user which to inspect.

### Phase A: gather context

1. **Symptom** — "What specifically isn't working? What error messages are you seeing? Which platform (iOS, Android, Web)?"
2. **User state** — "Is this happening for new purchases or existing subscribers? Sandbox or production?"

### Phase B: systematic diagnosis

Work through this checklist via MCP tools or their `rc` CLI equivalents (see the `revenuecat-cli` skill). Each `list-*` tool maps to `rc <noun> list` (e.g. `list-offerings` → `rc offerings list`, `list-apps` → `rc apps list`), `list-app-public-api-keys` → `rc apps keys <app-id>`, and `get-product-store-state` → `rc products show <product-id> --store-state`.

#### Check 1: Project overview
```
list-projects → ask user to select project if multiple
list-apps (with selected project_id)
```
- Verify project exists and apps are present.

#### Check 2: Products
```
list-products
get-product-store-state
```
- [ ] Products exist for each store item.
- [ ] Store identifiers match App Store Connect / Play Console exactly.
- [ ] Product types are correct (subscription vs one-time).
- [ ] Play Store: using `product_id:base_plan_id` format.
- [ ] Store State: `store_status.status` = `ok`.

#### Check 3: Entitlements
```
list-entitlements
get-products-from-entitlement (for each entitlement)
```
- [ ] Entitlements exist for each access level.
- [ ] Products are attached to entitlements.
- [ ] No orphaned products (products not granting any entitlement).

#### Check 4: Offerings
```
list-offerings
list-packages
```
- [ ] At least one offering exists with `is_current: true`.
- [ ] Packages contain products.
- [ ] Package identifiers use standard conventions (`$rc_monthly`, etc.).

#### Check 5: Webhooks (if server-side issues suspected)
```
list-webhook-integrations
```
- [ ] Webhook URL is correct and accessible.
- [ ] Environment matches (production vs sandbox).

### Phase C: report and offer fixes

```
Diagnostic Report
=================
Project: {project_name}

Checks Passed: ✅
  - Project exists and is accessible
  - 2 apps configured (iOS, Android)
  - 4 products found

Issues Found: ⚠️

1. CRITICAL: Product not attached to entitlement
   Product: annual_premium (prod123)
   Fix: Attach this product to an entitlement

2. WARNING: Offering has empty package
   Offering: default / Package: $rc_annual has no products
   Fix: Attach annual_premium to this package

3. INFO: No webhook configured
   Optional but recommended for server-side access control

Recommended Actions:
1. Attach annual_premium to "premium" entitlement
2. Attach annual_premium to $rc_annual package

Would you like me to fix issues #1 and #2 now?
```

For each fixable issue, confirm with the user, then execute via MCP:
- `attach-products-to-entitlement`
- `attach-products-to-package`

## 4. Platform specific step

Read the platform file that matches detection. Each one lists platform specific gotchas not covered above (StoreKit configuration files, Gradle/desugaring, Metro caching, Expo prebuild, etc.).

- `platforms/ios.md`
- `platforms/android.md`
- `platforms/kmp.md`
- `platforms/flutter.md`
- `platforms/react-native.md`

## 5. Verify the fix

Do not declare the issue fixed until:

1. The log that previously showed the error now shows the expected success line (offerings returned with at least one package, purchase completed, entitlement active).
2. The dashboard reflects the change. For a purchase, check the Sandbox view on the Customers page and confirm the transaction is attached to the right `appUserID`.
3. The reproduction steps from the original report now pass.

If the user cannot reproduce locally, have them send the full debug log from app launch to the moment of failure. The SDK's own output is usually enough.

---

## Reference: SDK error codes

### Common errors

| Error code                       | Likely cause                                | Solution                                                                |
| -------------------------------- | ------------------------------------------- | ----------------------------------------------------------------------- |
| `INVALID_APP_USER_ID`            | Reserved characters or empty string         | Use alphanumeric IDs, underscores, hyphens only                         |
| `INVALID_CREDENTIALS`            | Wrong API key or bundle ID mismatch         | Verify API key matches app                                              |
| `NETWORK_ERROR`                  | No connectivity or firewall                 | Check network, verify RevenueCat domains allowed                        |
| `STORE_PROBLEM`                  | Store downtime, config issue, iOS 18.x bug  | Check store status, verify config, see Known iOS Issues below           |
| `SIGNATURE_VERIFICATION_FAILED`  | Tampered receipt or config error            | Verify In-App Purchase Key (iOS) or service credentials                 |

### Purchase errors

| Error code                            | Solution                                                          |
| ------------------------------------- | ----------------------------------------------------------------- |
| `RECEIPT_ALREADY_IN_USE`              | Call `restorePurchases()` or sync customer                        |
| `PRODUCT_NOT_AVAILABLE_FOR_PURCHASE`  | Verify product status in App Store Connect / Play Console         |
| `PURCHASE_NOT_ALLOWED`                | Check parental controls, payment method                           |
| `PRODUCT_ALREADY_PURCHASED`           | Call `restorePurchases()` to sync                                 |

## Reference: debug log interpretation

Ask the developer to enable debug logging:
- iOS: `Purchases.logLevel = .debug`
- Android: `Purchases.logLevel = LogLevel.DEBUG`

Log emoji indicators: 🍎 Apple/StoreKit · 🤖 Google Play · 📦 Amazon · 😿 RevenueCat backend.

## Reference: known platform issues

### iOS

**iOS 18.0–18.3.2: StoreKit Daemon Connection Failure**
- Symptom: `STORE_PROBLEM` (NSCocoaErrorDomain Code 4097) on ~25% of purchases on physical devices.
- Fix: Upgrade to iOS 18.4+.

**iOS 18.4–18.5 Simulator: Products Don't Load**
- Symptom: Products return empty in simulator with sandbox.
- Affected: Simulator only — physical devices and production unaffected.
- Fix: Test on physical device, or use Xcode 26+ with iOS 26+ simulators.

### Android

**ProxyBillingActivity NullPointerException**
- Typically from automated testing or Play Store pre-launch reports on LG Nexus 5X / rooted devices.
- Safe to ignore/silence in crash reporting tools.

**NoCoreLibraryDesugaringException / NoClassDefFoundError**
- Fix: Enable core library desugaring in `build.gradle` or raise `minSdk`.

## Reference: platform configuration checklists

### iOS

- [ ] Paid Applications agreement signed in App Store Connect.
- [ ] In-App Purchase Key uploaded to RevenueCat (StoreKit 2 / SDK 5.x+).
- [ ] Products show "Ready to Submit" or "Approved" status.
- [ ] Bundle ID matches exactly in Xcode, App Store Connect, and RevenueCat.
- [ ] New products: wait 24h for propagation.

### Android

- [ ] App published to at least closed testing track (internal testing won't work).
- [ ] Test account added as licensed tester in Play Console.
- [ ] Service account credentials (JSON) uploaded to RevenueCat with Finance permissions.
- [ ] Subscriptions use `product_id:base_plan_id` format.
- [ ] New products: wait 24h for propagation.

## Reference: App Store rejection troubleshooting

**"Issues fetching products"** — Products must be submitted for review with the app on first submission. Create products in App Store Connect, then submit app and products together.

**"Error during purchase" (Sandbox)** — Apple sandbox downtime. Inform reviewer, provide RevenueCat sandbox dashboard screenshot showing test purchases work, ask to retry.

**"Content not unlocked after purchase"** — Verify product → entitlement connection in RevenueCat. Ensure app calls `getCustomerInfo()` after purchase.

## Reference: common issues

**User purchased but has no entitlement** — Check product → entitlement attachment and verify store identifier matches exactly.

**Offering returns empty** — Verify a `current` offering exists, packages have products attached, and products exist in the app's store.

**Webhook not receiving events** — Verify URL is internet-accessible and returns 200 OK. Test with webhook.site.

**Subscription status out of sync** — SDK caches `CustomerInfo` for 5 min (foreground). Force refresh:
```swift
// iOS
Purchases.shared.getCustomerInfo(fetchPolicy: .fetchCurrent) { ... }
```
```kotlin
// Android
Purchases.sharedInstance.getCustomerInfoWith(CacheFetchPolicy.FETCH_CURRENT) { ... }
```

**SDK crashes on launch (iOS / Xcode 26)** — Initialize RevenueCat before other networking libraries.

**SDK crashes on launch (Android)** — Enable core library desugaring or raise `minSdk` to 24+.
