---
name: rc-revenuecat-api-quick-reference
description: Use this skill as a quick reference for the RevenueCat Android SDK 10.x and REST API. Covers SDK init, common Purchases calls, CustomerInfo / Offerings access patterns, and the most used REST endpoints.
license: Apache-2.0; see LICENSE
metadata:
  author: RevenueCat
  source: revenuecat-handbook appendix A
  keywords:
  - android
  - revenuecat
  - sdk-reference
  - rest-reference
---

# RevenueCat API Quick Reference

## Phase 0: Intent

Use this skill when you need a fast lookup of a RevenueCat API surface while writing Android code or server logic. Typical questions you answer from here:

- Which builder option controls a given `Purchases.configure` behavior?
- What is the return type and signature of `awaitPurchase`, `awaitOfferings`, `awaitCustomerInfo`, `awaitRestore`, `awaitLogIn`, `awaitLogOut`?
- How do I read offering, package, product, entitlement fields?
- Which `PurchasesErrorCode` should I branch on?
- Which listener callback do I register for customer info updates?

Do not use this skill as a deep tutorial. Reach for the feature-specific skills (purchase flow, configuring the SDK, error handling, subscription states) when you need step-by-step guidance or design rationale.

## Phase 1: Locate

Decide SDK surface vs REST surface before you search the tables.

Route to the SDK (client side, Android app code):

- Code runs inside the Android app, in an `Activity`, `ViewModel`, or background worker bundled with your app.
- You need to launch a purchase, restore purchases, read cached `CustomerInfo`, fetch `Offerings`, identify or log out a user, or listen for updates.
- You want entitlement gating in the UI.

Route to the REST API (server side):

- Code runs on your backend, in a webhook handler, in an admin tool, or in a scheduled job.
- You need to grant or revoke a promotional entitlement, override a subscription, look up a subscriber from another service, refund, or deliver events to another system.
- You are integrating with a system that cannot embed the SDK.

The tables in this skill cover the Android SDK 10.x surface from appendix A verbatim. For REST endpoint paths, authentication, and payloads, see the [full appendix on revenuecat.com](https://www.revenuecat.com/guides/revenuecat-android-sdk/appendix-revenuecat-api-quick-reference) together with the backend and webhooks skills, and treat this file as the SDK index.

## Phase 2: Reference Tables

### SDK Initialization

```kotlin
// Minimum setup
Purchases.configure(
    PurchasesConfiguration.Builder(context, "api_key").build()
)

// Full options
Purchases.configure(
    PurchasesConfiguration.Builder(context, "api_key")
        .appUserID("user_id")                    // null for anonymous
        .showInAppMessagesAutomatically(true)    // default: true
        .purchasesAreCompletedBy(PurchasesAreCompletedBy.REVENUECAT) // default
        .entitlementVerificationMode(EntitlementVerificationMode.INFORMATIONAL)
        .diagnosticsEnabled(false)               // default: false
        .pendingTransactionsForPrepaidPlansEnabled(false) // default: false
        .build()
)

Purchases.logLevel = LogLevel.DEBUG // before configure()
```

### Core Operations (Coroutine)

```kotlin
// Fetch offerings
val offerings: Offerings = Purchases.sharedInstance.awaitOfferings()

// Fetch specific products
val products: List<StoreProduct> = Purchases.sharedInstance.awaitGetProducts(
    listOf("product_id"),
    type = ProductType.INAPP // or SUBS, or null for all
)
```

```kotlin
// Purchase
val result: PurchaseResult = Purchases.sharedInstance.awaitPurchase(
    PurchaseParams.Builder(activity, packageOrStoreProductOrSubscriptionOption).build()
)

// Purchase upgrade/downgrade
val result = Purchases.sharedInstance.awaitPurchase(
    PurchaseParams.Builder(activity, newPackage)
        .oldProductId("old_product_id")
        .googleReplacementMode(GoogleReplacementMode.WITH_TIME_PRORATION)
        .build()
)
```

```kotlin
// Get customer info
val customerInfo: CustomerInfo = Purchases.sharedInstance.awaitCustomerInfo()
val fresh: CustomerInfo = Purchases.sharedInstance.awaitCustomerInfo(
    fetchPolicy = CacheFetchPolicy.FETCH_CURRENT
)

// Restore
val customerInfo: CustomerInfo = Purchases.sharedInstance.awaitRestore()

// Log in / log out
val loginResult: LogInResult = Purchases.sharedInstance.awaitLogIn("user_id")
// loginResult.customerInfo, loginResult.created (Boolean)
val customerInfo: CustomerInfo = Purchases.sharedInstance.awaitLogOut()
```

### Offerings Structure

```kotlin
val offerings: Offerings
offerings.current          // current Offering
offerings.all              // Map<String, Offering>
offerings["my_offering"]   // by identifier
offerings.getCurrentOfferingForPlacement("placement_id") // targeting
```

```kotlin
val offering: Offering
offering.identifier
offering.monthly           // Package? (shortcut)
offering.annual            // Package?
offering.weekly            // Package?
offering.availablePackages // List<Package>
offering.metadata          // Map<String, Any>
```

```kotlin
val pkg: Package
pkg.identifier             // "$rc_monthly", "$rc_annual", custom
pkg.packageType            // PackageType enum
pkg.product                // StoreProduct
pkg.webCheckoutURL         // URL? (RevenueCat web billing)
```

```kotlin
val product: StoreProduct
product.productId
product.title
product.description
product.price.formatted    // "$4.99"
product.price.amountMicros
product.price.currencyCode
product.period             // Period? (null for INAPP); use period.iso8601 for "P1M", "P1Y", etc.
product.subscriptionOptions // List<SubscriptionOption>? (null for INAPP)
product.defaultOption       // SubscriptionOption? best available offer
```

### Entitlements

```kotlin
val customerInfo: CustomerInfo
customerInfo.entitlements.active         // Map<String, EntitlementInfo> (active only)
customerInfo.entitlements.all            // Map<String, EntitlementInfo> (all)
customerInfo.entitlements["pro_access"]  // EntitlementInfo?
customerInfo.activeSubscriptions         // Set<String> of "productId:basePlanId"
customerInfo.nonSubscriptionTransactions // List<Transaction>
customerInfo.managementURL               // Uri? to Play Store management
```

```kotlin
val entitlement: EntitlementInfo
entitlement.isActive                     // Boolean, the main access gate
entitlement.willRenew                    // false if canceled
entitlement.expirationDate               // Date? (null for lifetime)
entitlement.periodType                   // NORMAL, TRIAL, INTRO, PREPAID
entitlement.billingIssueDetectedAt       // Date? (non-null = grace/hold)
entitlement.unsubscribeDetectedAt        // Date? (non-null = canceled)
entitlement.store                        // PLAY_STORE, APP_STORE, etc.
entitlement.productIdentifier            // subscription product ID
entitlement.productPlanIdentifier        // base plan ID (Google only)
entitlement.verification                 // VerificationResult
```

### Error Handling

```kotlin
// Purchase errors
try {
    Purchases.sharedInstance.awaitPurchase(params)
} catch (e: PurchasesTransactionException) {
    e.userCancelled     // Boolean
    e.error.code        // PurchasesErrorCode
    e.error.message     // description string
}

// Other errors
try {
    Purchases.sharedInstance.awaitOfferings()
} catch (e: PurchasesException) {
    e.error.code        // PurchasesErrorCode
}
```

```kotlin
// Key error codes
PurchasesErrorCode.PurchaseCancelledError
PurchasesErrorCode.ProductAlreadyPurchasedError
PurchasesErrorCode.PaymentPendingError
PurchasesErrorCode.NetworkError
PurchasesErrorCode.StoreProblemError
PurchasesErrorCode.IneligibleError
PurchasesErrorCode.ConfigurationError
```

### Listeners

```kotlin
// CustomerInfo updates
Purchases.sharedInstance.updatedCustomerInfoListener =
    UpdatedCustomerInfoListener { customerInfo -> }

// Show in-app messages manually
Purchases.sharedInstance.showInAppMessagesIfNeeded(activity)
```

## Phase 3: Typical Snippets

Gate a feature on an entitlement.

```kotlin
val info = Purchases.sharedInstance.awaitCustomerInfo()
val hasPro = info.entitlements["pro_access"]?.isActive == true
if (hasPro) unlockFeature() else showPaywall()
```

Buy the monthly package from the current offering.

```kotlin
val current = Purchases.sharedInstance.awaitOfferings().current ?: return
val monthly = current.monthly ?: return
val result = Purchases.sharedInstance.awaitPurchase(
    PurchaseParams.Builder(activity, monthly).build()
)
```

Handle cancel vs real failure.

```kotlin
try {
    Purchases.sharedInstance.awaitPurchase(params)
} catch (e: PurchasesTransactionException) {
    if (e.userCancelled) return
    when (e.error.code) {
        PurchasesErrorCode.PaymentPendingError -> showPendingUi()
        PurchasesErrorCode.NetworkError -> showRetry()
        else -> showGenericError(e.error.message)
    }
}
```

Force a fresh CustomerInfo fetch after a server side grant.

```kotlin
val fresh = Purchases.sharedInstance.awaitCustomerInfo(
    fetchPolicy = CacheFetchPolicy.FETCH_CURRENT
)
```

Log in an identified user and detect first login.

```kotlin
val login = Purchases.sharedInstance.awaitLogIn("user_123")
val isNewAlias = login.created
val info = login.customerInfo
```

React to background entitlement changes.

```kotlin
Purchases.sharedInstance.updatedCustomerInfoListener =
    UpdatedCustomerInfoListener { info ->
        val active = info.entitlements["pro_access"]?.isActive == true
        uiState.update { it.copy(hasPro = active) }
    }
```

## References

- [Full chapter](https://www.revenuecat.com/guides/revenuecat-android-sdk/appendix-revenuecat-api-quick-reference)

- Related skills in this repo: [rc-configuring-the-sdk](../rc-configuring-the-sdk/), [rc-purchase-flow](../rc-purchase-flow/), [rc-error-handling](../rc-error-handling/), [rc-subscription-states](../rc-subscription-states/), [rc-backend](../rc-backend/), [rc-webhooks](../rc-webhooks/).
