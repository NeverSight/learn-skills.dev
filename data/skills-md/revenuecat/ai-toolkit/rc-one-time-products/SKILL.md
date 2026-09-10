---
name: rc-one-time-products
description: Use this skill when selling one time products on Android with RevenueCat. Covers fetching offerings, running awaitPurchase on a non subscription package, and relying on the SDK to acknowledge or consume automatically.
license: Apache-2.0; see LICENSE
metadata:
  author: RevenueCat
  source: revenuecat-handbook chapter 3
  keywords:
  - android
  - revenuecat
  - one-time-products
  - awaitpurchase
  - consumable
  - non-consumable
---

# One Time Products with RevenueCat

Sell one time products on Android without writing BillingClient glue. The RevenueCat SDK fetches products, launches the purchase, verifies the receipt, and acknowledges or consumes the token for you.

## Phase 1: Scope

Answer these before touching code.

| Question | Decision |
|---|---|
| Is the product consumable or non consumable? | Mark consumables in the RevenueCat dashboard so the SDK calls `consumeAsync` for you. |
| Do you read access through entitlements or transactions? | Prefer entitlements so access logic stays decoupled from product IDs. |
| Do you need server notification of the purchase? | Use RevenueCat webhooks. The `INITIAL_PURCHASE` event fires for every new non subscription purchase. |

Do not call `BillingClient.queryProductDetailsAsync`, `acknowledgePurchase`, or `consumeAsync` yourself once RevenueCat is integrated. The SDK owns the `BillingClient` instance.

## Phase 2: Prepare

- Configure the product in Google Play Console as a one time product.
- In the RevenueCat dashboard, attach the product to an offering and package, and flag it as consumable if it should be consumed on purchase.
- Confirm `Purchases.configure` runs once on app start with your Android API key and the current App User ID.

## Phase 3: Execute

Fetch offerings, launch the purchase, then read the result off `CustomerInfo`.

```kotlin
val offerings = Purchases.sharedInstance.awaitOfferings()
val pkg = offerings.current?.availablePackages?.first() ?: return
```

Launch the purchase with `awaitPurchase`. It suspends until the RevenueCat backend verifies the token.

```kotlin
val result = Purchases.sharedInstance.awaitPurchase(
    PurchaseParams.Builder(activity, pkg).build()
)
val info = result.customerInfo
```

Read access through entitlements, or fall back to the non subscription transactions list.

```kotlin
val hasAccess = info.entitlements["lifetime_access"]?.isActive == true
val owned = info.nonSubscriptionTransactions
    .any { it.productIdentifier == "lifetime_product_id" }
```

The SDK acknowledges non consumables and consumes consumables automatically once the backend verifies the purchase. You do not call `acknowledgePurchase` or `consumeAsync`.

## Phase 4: Handle Edge Cases

Wrap `awaitPurchase` to separate cancellation, pending payments, and real errors.

```kotlin
try { /* awaitPurchase */ } catch (e: PurchasesTransactionException) {
    when {
        e.error.code == PurchasesErrorCode.PaymentPendingError -> showPending()
        e.userCancelled -> Unit
        else -> showError(e.error.message)
    }
}
```

| Outcome | SDK signal | Action |
|---|---|---|
| Success | `awaitPurchase` returns with updated `CustomerInfo` | Grant access from `entitlements` or `nonSubscriptionTransactions`. |
| User cancel | `PurchasesTransactionException`, `userCancelled == true` | Swallow silently. |
| Pending payment | `PurchasesTransactionException`, `PaymentPendingError` | Show a pending message. The SDK updates the entitlement later through `UpdatedCustomerInfoListener`. |
| Other error | `PurchasesTransactionException`, other codes | Surface `e.error.message` to you. |

## Phase 5: Verify

- Trust `result.customerInfo` from `awaitPurchase`. Do not grant access from optimistic local state.
- Pending purchases do not grant entitlements. Register an `UpdatedCustomerInfoListener` so you react when the payment completes.
- For server side provisioning, subscribe to the RevenueCat `INITIAL_PURCHASE` webhook. Do not reimplement Google Play Developer API verification.

## References

- [Full chapter](https://www.revenuecat.com/guides/revenuecat-android-sdk/one-time-products-with-revenuecat)
