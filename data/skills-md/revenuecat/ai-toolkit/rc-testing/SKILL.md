---
name: rc-testing
description: Use this skill when testing a RevenueCat Android integration. Covers the RevenueCat Test Store (test_ API key prefix, in dialog Success/Fail/Cancel choice), mockk based unit testing with an interface wrapper around Purchases, and a GitHub Actions CI pattern. Avoids Google Play sandbox for day to day test iteration.
license: Apache-2.0; see LICENSE
metadata:
  author: RevenueCat
  source: revenuecat-handbook chapter 16
  keywords:
  - android
  - revenuecat
  - testing
  - test-store
  - mockk
  - github-actions
---

# Testing RevenueCat on Android

Use this skill to stand up a fast test loop for a RevenueCat Android integration. The Test Store replaces the Google Play sandbox for most work, a `BillingService` interface makes `Purchases` mockable, and a small GitHub Actions job runs unit tests on every push.

Full source: see the [full chapter on revenuecat.com](https://www.revenuecat.com/guides/revenuecat-android-sdk/testing).

---

## Phase 1: Discovery

Before changing anything, learn what already exists. Answer each question with a file or a "no".

| Check | Where to look | What you want |
|---|---|---|
| Test API key configured? | `app/build.gradle.kts`, `local.properties`, env | A `test_...` value bound to `BuildConfig.RC_API_KEY` in debug |
| Release key separate? | `build.gradle.kts` release block | A `goog_...` key, never `test_...` |
| Purchases wrapped? | `app/src/main/java/**/*Billing*.kt` | An interface that hides `Purchases.sharedInstance` |
| CI present? | `.github/workflows/*.yml` | A job running `./gradlew testDebugUnitTest` |
| Secret wired? | GitHub repo settings, workflow `env:` | `RC_TEST_STORE_KEY` referenced from `secrets` |
| Test library? | `app/build.gradle.kts` dependencies | `io.mockk:mockk` and `kotlinx-coroutines-test` |

If the project has none of these, start from scratch in Phase 3. If some exist, only fill the gaps.

---

## Phase 2: Plan

Pick the test path per scenario. The Test Store is the default; fall back to Google Play sandbox only when you need store behavior the Test Store does not simulate.

| Scenario | Use |
|---|---|
| Success, failure, cancel paths | Test Store |
| Unit tests of ViewModels | mockk against `BillingService` |
| CI on every push | Test Store + unit tests |
| Subscription renewal cycles | Google Play Sandbox |
| Pending purchase (parental approval) | Google Play Sandbox |
| Full end-to-end payment | Google Play Sandbox |

Write the plan as a short checklist in `tasks/todo.md` before coding. If the app ships subscriptions, keep one Sandbox pass in the pre-ship checklist even if the Test Store covers daily iteration.

---

## Phase 3: Execute

### Step 1: Generate the test API key

In the RevenueCat dashboard, open your app, go to **Apps & providers**, then **Create Test Store**. Copy the `test_...` key. Do not commit it. Put it in `local.properties` or a CI secret.

### Step 2: Wire the key into debug builds

```kotlin
// build.gradle.kts
android {
    buildTypes {
        debug {
            buildConfigField("String", "RC_API_KEY", "\"test_YOUR_KEY\"")
        }
        release {
            buildConfigField("String", "RC_API_KEY", "\"goog_YOUR_KEY\"")
        }
    }
}
```

For CI, read from env so the key never lands in git:

```kotlin
// build.gradle.kts
val testKey = System.getenv("RC_TEST_STORE_KEY") ?: "test_placeholder"
buildConfigField("String", "RC_API_KEY", "\"$testKey\"")
```

### Step 3: Configure Purchases with the build config key

```kotlin
class MyApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        if (BuildConfig.DEBUG) Purchases.logLevel = LogLevel.DEBUG
        Purchases.configure(
            PurchasesConfiguration.Builder(this, BuildConfig.RC_API_KEY).build()
        )
    }
}
```

### Step 4: Trigger the Test Store dialog

Run the app in debug and call `awaitPurchase()` from your paywall. A dialog appears with Success, Fail, and Cancel options. Each choice resolves the same way production would: Success returns a `PurchaseResult` with active entitlements, Fail throws `PurchasesTransactionException` with a payment error, Cancel throws with `userCancelled = true`. Walk every branch of your error handling to verify UI states.

### Step 5: Wrap Purchases in a BillingService

The `Purchases` singleton is not mockable. A thin interface lets you inject a fake in tests and keeps ViewModels free of SDK types.

```kotlin
interface BillingService {
    suspend fun getOfferings(): Offerings
    suspend fun purchase(activity: Activity, pkg: Package): CustomerInfo
    suspend fun getCustomerInfo(): CustomerInfo
}
```

```kotlin
class RevenueCatBillingService : BillingService {
    override suspend fun getOfferings() =
        Purchases.sharedInstance.awaitOfferings()

    override suspend fun purchase(activity: Activity, pkg: Package): CustomerInfo =
        Purchases.sharedInstance.awaitPurchase(
            PurchaseParams.Builder(activity, pkg).build()
        ).customerInfo

    override suspend fun getCustomerInfo() =
        Purchases.sharedInstance.awaitCustomerInfo()
}
```

### Step 6: Write mockk unit tests

```kotlin
class PaywallViewModelTest {
    private val billing = mockk<BillingService>()
    private val viewModel = PaywallViewModel(billing)

    @Test
    fun `purchase success grants access`() = runTest {
        val info = mockk<CustomerInfo> {
            every { entitlements["pro_access"]?.isActive } returns true
        }
        coEvery { billing.purchase(any(), any()) } returns info
        viewModel.purchase(mockActivity, mockPackage)
        assertTrue(viewModel.state.value is PaywallState.Success)
    }
}
```

Add one test per branch: success grants access, failure shows error, cancel stays idle.

### Step 7: Add a minimal GitHub Actions job

```yaml
# .github/workflows/test.yml
name: test
on: [push, pull_request]
jobs:
  unit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: 17
      - name: Run tests
        env:
          RC_TEST_STORE_KEY: ${{ secrets.RC_TEST_STORE_KEY }}
        run: ./gradlew testDebugUnitTest
```

Store the `test_...` key as the `RC_TEST_STORE_KEY` repository secret. The job runs without a device or a Google account.

---

## Verification

After each purchase, open the RevenueCat dashboard, go to **Customers**, pick the user, and confirm the purchase, the entitlement, and the `CustomerInfo` JSON. The **Events** tab shows webhooks fired for the test purchase.

## Pre-Ship Checklist

- [ ] `Purchases.logLevel = LogLevel.DEBUG` gated on `BuildConfig.DEBUG`
- [ ] Release build uses the `goog_` key, not the `test_` key
- [ ] `test_` key is not committed (env var or `local.properties`)
- [ ] Success, failure, and cancel paths exercised through the Test Store dialog
- [ ] At least one end-to-end flow verified in Google Play Sandbox
- [ ] Webhook endpoint receives events for sandbox purchases

## References

- [Full chapter](https://www.revenuecat.com/guides/revenuecat-android-sdk/testing)
