---
name: rc-plan-changes
description: Use this skill when implementing subscription upgrades, downgrades, and plan switches via RevenueCat on Android. Covers GoogleProductChangeInfo, picking a Google replacement mode, and letting the SDK manage linkedPurchaseToken chaining.
license: Apache-2.0; see LICENSE
metadata:
  author: RevenueCat
  source: revenuecat-handbook chapter 7
  keywords:
  - android
  - revenuecat
  - upgrade
  - downgrade
  - google-product-change-info
  - replacement-mode
---

# Plan Changes on Android with RevenueCat

You use this skill when a user already has an active Google Play subscription and you need to move them to a different SKU (upgrade, downgrade, cross-grade, or trial conversion). RevenueCat exposes Google's replacement modes through a single `PurchaseParams` builder and resolves the `linkedPurchaseToken` chain server side so you do not write token chaining code.

## Phase 1: Preconditions

Confirm the following before invoking a plan change:

- The user has exactly one active Google Play subscription you intend to replace.
- You have a fresh `CustomerInfo` from `Purchases.sharedInstance.awaitCustomerInfo()` or a cached value from a recent listener callback.
- You have the target `Package` resolved from `offerings.current` (see `fetch-offerings` skill).
- Google Play Billing Library 7+ is on the classpath via the RevenueCat SDK.

Skip this skill if the user has no active subscription. For a fresh purchase, use `make-purchase` instead.

## Phase 2: Plan (pick a replacement mode)

`GoogleReplacementMode` maps one to one onto Google's billing modes. Pick based on the user intent:

| Scenario | Mode | Billing effect |
|---|---|---|
| Standard upgrade (monthly to annual) | `WITH_TIME_PRORATION` | Immediate switch, remaining time credited |
| Upgrade, keep the existing billing date | `CHARGE_PRORATED_PRICE` | Immediate switch, prorated charge now |
| Switch to or from a prepaid plan | `CHARGE_FULL_PRICE` | Immediate switch, full charge now |
| Upgrade during an active free trial | `CHARGE_PRORATED_PRICE` | Immediate switch, prorated charge now |
| Downgrade (annual to monthly) | `DEFERRED` | Switch applies at next renewal |

Do not default to `WITHOUT_PRORATION` for trial upgrades. `WITHOUT_PRORATION` applies the new plan immediately but charges nothing until the next renewal, which gives the user free premium access they did not pay for. Use `CHARGE_PRORATED_PRICE` to charge the upgrade price on the spot.

If you set no mode, `PurchaseParams` defaults to `WITHOUT_PRORATION`. Set the mode explicitly every time.

`DEFERRED` is valid only for downgrades. Google rejects deferred upgrades.

## Phase 3: Execute

Derive `currentProductId` from `CustomerInfo`. Hardcoded SKUs break when a user has migrated between plans.

```kotlin
val customerInfo = Purchases.sharedInstance.awaitCustomerInfo()

// activeSubscriptions entries are "productId:basePlanId", strip the base plan suffix
val currentProductId = customerInfo.activeSubscriptions
    .firstOrNull()
    ?.substringBefore(":")
    ?: return  // nothing active, route to make-purchase instead

val newPackage = offerings.current
    ?.availablePackages
    ?.firstOrNull { it.identifier == "premium_annual_package" }
    ?: return

val params = PurchaseParams.Builder(activity, newPackage)
    .googleProductChangeInfo(
        GoogleProductChangeInfo(
            oldProductId = currentProductId,
            replacementMode = GoogleReplacementMode.WITH_TIME_PRORATION,
        )
    )
    .build()

try {
    val result = Purchases.sharedInstance.awaitPurchase(params)
    // result.customerInfo reflects the new subscription
} catch (e: PurchasesTransactionException) {
    if (!e.userCancelled) showError(e.error.message)
}
```

Notes on `oldProductId`:

- Pass the subscription product ID only. If you pass `"basic_monthly:monthly_plan"`, the SDK strips `:monthly_plan` for you, but the intent is clearer when you slice it yourself.
- `CustomerInfo.activeSubscriptions` uses the `productId:basePlanId` shape. `substringBefore(":")` gives you the correct value.

## Phase 4: Verify

After the suspending call returns, read the updated `CustomerInfo`:

- `customerInfo.activeSubscriptions` now contains the new `productId:basePlanId`.
- `customerInfo.entitlements["pro"]?.isActive` stays `true` across the switch; do not gate UI on the SKU string.
- For `DEFERRED` mode, `activeSubscriptions` still reports the old product until the next renewal. RevenueCat tracks the pending switch server side and flips the entitlement after Google sends the renewal RTDN.

You do not write `linkedPurchaseToken` traversal code. RevenueCat resolves the chain, marks the old token as replaced, and attributes both tokens to the same App User ID. Client code reads entitlements and trusts them.

## Common mistakes

| Mistake | Fix |
|---|---|
| Hardcoding `oldProductId` as a constant | Derive it from `customerInfo.activeSubscriptions.firstOrNull()?.substringBefore(":")` |
| Passing `"productId:basePlanId"` as `oldProductId` | Slice off the base plan with `substringBefore(":")` |
| Using `WITHOUT_PRORATION` for a trial upgrade | Use `CHARGE_PRORATED_PRICE` so the user is charged now |
| Using `DEFERRED` for an upgrade | `DEFERRED` is downgrade only; Google rejects deferred upgrades |
| Writing backend code to follow `linkedPurchaseToken` | RevenueCat does this server side, delete the code |
| Reading the SKU to decide UI state | Read `entitlements[...]?.isActive` instead |

## References

- [Full chapter](https://www.revenuecat.com/guides/revenuecat-android-sdk/subscription-upgrades-and-downgrades)
