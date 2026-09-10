---
name: rc-configuring-the-sdk
description: Use this skill when adding and configuring the RevenueCat Android SDK (purchases-kt/purchases) in an app. Covers the Gradle dependency, Purchases.configure with PurchasesConfiguration, initial app user id strategy, and log level.
license: Apache-2.0; see LICENSE
metadata:
  author: RevenueCat
  source: revenuecat-handbook chapter 5
  keywords:
  - android
  - revenuecat
  - configure
  - purchases-configuration
  - app-user-id
  - sdk
---

# Configuring the RevenueCat Android SDK

Use this skill to add and configure RevenueCat (`purchases-kt`) in an Android app. A single `Purchases.configure` call replaces `BillingClient` setup, connection lifecycle management, reconnection handling, and launch-time purchase queries.

Work through the phases in order. The [full chapter on revenuecat.com](https://www.revenuecat.com/guides/revenuecat-android-sdk/configuring-the-sdk) has the complete reference text.

## Phase 1: Discovery

Find out whether RevenueCat is already wired up and where billing code currently lives.

1. Search for an existing configure call and prior SDK version.

   ```bash
   rg -n "Purchases\.configure|PurchasesConfiguration" --type kotlin --type java
   rg -n "com\.revenuecat\.purchases" -g '*.gradle*' -g '*.toml'
   ```

2. Search for the existing billing surface you may be replacing.

   ```bash
   rg -n "BillingClient|PurchasesUpdatedListener|startConnection" --type kotlin --type java
   ```

3. Record answers before moving on.

| Question | Where to look |
| --- | --- |
| Is `Purchases.configure` already called? | App startup, `Application.onCreate`, main `Activity.onCreate` |
| Which module owns billing today? | `app/build.gradle(.kts)`, any `:billing` module |
| Is there an auth system with a stable user id? | Login flow, session store |
| Debug vs release build detection available? | `BuildConfig.DEBUG` |

If `Purchases.configure` already runs, stop and confirm with the user before changing it. Configuration runs once per process.

## Phase 2: Plan

Decide three things before writing code.

### 2.1 Where to call configure

| Location | When to choose |
| --- | --- |
| `Application.onCreate` | Default. Ensures the SDK is ready before any `Activity` or background work touches purchases. |
| First `Activity.onCreate` | Only if the app has no custom `Application` class and you are not willing to add one. |

Call `configure` exactly once per process. Calling it from an `Activity` risks re-running it on configuration changes if you are not careful; the `Application` path avoids that.

### 2.2 App user id strategy

| Strategy | Pass to `appUserID` | Use when |
| --- | --- | --- |
| Anonymous | `null` | Users can purchase before signing in, or you have no auth. Later call `Purchases.sharedInstance.logIn(id)` to merge history. |
| Known user | Your stable backend id (for example `"user_12345"`) | Users are always authenticated before purchase. |

Do not pass device ids, email addresses, or values that can change. If you do not have the id at startup, configure anonymously and call `logIn` after authentication.

### 2.3 Log level

| Build | Log level |
| --- | --- |
| Debug | `LogLevel.DEBUG` or `VERBOSE` while integrating |
| Release | `LogLevel.INFO` (default) or `WARN` |

Switch on `BuildConfig.DEBUG` so production builds stay quiet.

## Phase 3: Execute

### 3.1 Add the Gradle dependency

In the app module `build.gradle.kts`:

```kotlin
dependencies {
    implementation("com.revenuecat.purchases:purchases:<latest>")
}
```

Replace `<latest>` with the current published version. If the project uses a Groovy `build.gradle`, use `implementation 'com.revenuecat.purchases:purchases:<latest>'`. Sync Gradle after the change.

### 3.2 Call configure at startup

In your `Application` subclass:

```kotlin
class App : Application() {
    override fun onCreate() {
        super.onCreate()
        Purchases.logLevel =
            if (BuildConfig.DEBUG) LogLevel.DEBUG else LogLevel.INFO
        Purchases.configure(
            PurchasesConfiguration.Builder(this, BuildConfig.RC_API_KEY)
                .appUserID(null) // or your stable user id
                .build()
        )
    }
}
```

Register the class in `AndroidManifest.xml` with `android:name=".App"` on `<application>`. Keep the public Android SDK key out of source; inject it through `BuildConfig` or a secret manager.

### 3.3 Confirm the wiring with a minimal offerings fetch

From any coroutine scope after `configure` has run:

```kotlin
lifecycleScope.launch {
    val offerings = Purchases.sharedInstance.awaitOfferings()
    Log.d("RC", "current=${offerings.current?.identifier}")
}
```

A non-null `offerings.current` identifier means the API key, package name, and network path are working. If you see `null`, check the dashboard offering setup and the package name match before touching code.

## What the SDK handles for you

Once configured, you do not need to:

- Create or close a `BillingClient`
- Call `startConnection` or `endConnection`
- Check `isReady` or write reconnection logic for `SERVICE_DISCONNECTED`
- Call `queryPurchasesAsync` at launch; the SDK posts unfinished transactions automatically

## Common pitfalls

| Symptom | Likely cause |
| --- | --- |
| `IllegalStateException: There is no singleton instance` | Code touched `Purchases.sharedInstance` before `configure` ran. Move `configure` to `Application.onCreate`. |
| Offerings always `null` | Package name mismatch between Play Console and dashboard, or offering not marked current. |
| Duplicate anonymous users | `configure` called more than once per process, or an unstable id passed as `appUserID`. |
| Verbose logs in production | Log level not gated on `BuildConfig.DEBUG`. |

## References

- [Full chapter](https://www.revenuecat.com/guides/revenuecat-android-sdk/configuring-the-sdk)
