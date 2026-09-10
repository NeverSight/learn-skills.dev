---
name: rc-purchase-flow
description: Use this skill when implementing a RevenueCat purchase on Android. Covers awaitPurchase, PurchasesTransactionException, reading CustomerInfo entitlements to grant access, restoring purchases, and the six SDK managed steps that happen inside a single call.
license: Apache-2.0; see LICENSE
metadata:
  author: RevenueCat
  source: revenuecat-handbook chapter 6
  keywords:
  - android
  - revenuecat
  - purchase-flow
  - awaitpurchase
  - purchases-transaction-exception
  - customerinfo
  - entitlements
---

# Purchase Flow

A RevenueCat purchase on Android is two lines of code. The SDK handles the billing params, the Play sheet, the purchase token round trip, server side verification, and acknowledgment. You decide which package to pass in and what to do with the returned entitlements.

## Phase 1: Understand what awaitPurchase() does

One call to `Purchases.sharedInstance.awaitPurchase(params)` runs six steps under the hood. You do not write any of this.

| Step | What happens |
|------|--------------|
| 1 | Builds `BillingFlowParams` with the correct `ProductDetailsParams` from your `Package` |
| 2 | Calls `BillingClient.launchBillingFlow()` against the activity you passed |
| 3 | Suspends until the `PurchasesUpdatedListener` result arrives |
| 4 | If `OK`, posts the Play purchase token to the RevenueCat backend |
| 5 | Backend verifies via `purchases.subscriptionsv2.get` or `purchases.products.get` |
| 6 | SDK acknowledges (subs or non-consumables) or consumes (consumables) within the 3 day Google window |

The call returns `PurchaseResult(storeTransaction, customerInfo)`. Retriable failures are retried automatically.

See the [Purchase Flow chapter on revenuecat.com](https://www.revenuecat.com/guides/revenuecat-android-sdk/the-purchase-flow) for the six-step diagram and the full picture.

## Phase 2: Prepare the package

You need a `Package` from offerings before you can purchase. Fetch offerings, let your UI pick one, and hold the activity.

```kotlin
val offerings = Purchases.sharedInstance.awaitOfferings()
val pkg = offerings.current?.monthly ?: return
```

If you need a specific offer instead of the default, resolve a `SubscriptionOption` and pass that to `PurchaseParams.Builder` instead of the package.

```kotlin
val option = pkg.product.subscriptionOptions
    ?.firstOrNull { it.tags.contains("promo_50_off") }
    ?: pkg.product.defaultOption
    ?: return
```

For EU personalized pricing, chain `.isPersonalizedPrice(true)` on the builder so Play shows the customized price notice.

## Phase 3: Execute the purchase

Build the params, await the purchase, read `customerInfo` to gate access, and handle the two expected error branches.

```kotlin
try {
    val result = Purchases.sharedInstance.awaitPurchase(
        PurchaseParams.Builder(activity, pkg).build()
    )
    val customerInfo = result.customerInfo
    if (customerInfo.entitlements["pro"]?.isActive == true) {
        navigateToApp()
    }
} catch (e: PurchasesTransactionException) {
    when {
        e.userCancelled -> { /* backed out, do nothing */ }
        e.error.code == PurchasesErrorCode.ProductAlreadyPurchasedError ->
            showMessage("You already have this subscription")
        else -> showError(e.error.message)
    }
}
```

Rules for this block:

- `PurchaseResult` is `@Poko`. Access fields as `result.customerInfo` and `result.storeTransaction`. Do not destructure with `val (transaction, customerInfo) = result`.
- `customerInfo.entitlements["<id>"]?.isActive == true` is the gate. Do not check `storeTransaction` to decide access.
- `PurchasesTransactionException` is the only exception type thrown by `awaitPurchase`. Catch it, branch on `userCancelled` first, then on `e.error.code`.
- User cancellation is not an error to surface. Swallow it.

If you prefer callbacks over coroutines, `purchaseWith(params, onError, onSuccess)` is the equivalent entry point.

## Phase 4: Inspect StoreTransaction only if you need it

`result.storeTransaction` is available but usually unused. `customerInfo` is the source of truth for entitlements. If you need transaction level data for logging or your own backend:

| Field | Type | Notes |
|-------|------|-------|
| `orderId` | `String?` | Null for restored purchases |
| `purchaseToken` | `String` | Raw Play purchase token |
| `productIds` | `List<String>` | Product IDs in the transaction |
| `purchaseTime` | `Long` | Epoch millis |
| `type` | `ProductType` | `SUBS` or `INAPP` |

## Phase 5: Restore on reinstall or device switch

Restore runs `queryPurchasesAsync()`, posts everything found to RevenueCat, and returns the fresh `CustomerInfo`. Gate access the same way you do after a purchase.

```kotlin
try {
    val customerInfo = Purchases.sharedInstance.awaitRestore()
    if (customerInfo.entitlements["pro"]?.isActive == true) {
        navigateToApp()
    } else {
        showMessage("No active purchases found")
    }
} catch (e: PurchasesException) {
    showError(e.error.message)
}
```

Note the exception type. `awaitRestore()` throws `PurchasesException`, not `PurchasesTransactionException`. There is no `userCancelled` flag to check because no billing sheet is shown.

## Exception types at a glance

| Call | Thrown exception | Has `userCancelled`? |
|------|------------------|----------------------|
| `awaitPurchase(params)` | `PurchasesTransactionException` | Yes |
| `awaitRestore()` | `PurchasesException` | No |

## References

- [Full chapter](https://www.revenuecat.com/guides/revenuecat-android-sdk/the-purchase-flow)
