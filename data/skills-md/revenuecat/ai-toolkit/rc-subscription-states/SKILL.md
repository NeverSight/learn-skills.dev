---
name: rc-subscription-states
description: Use this skill when gating access based on RevenueCat subscription state on Android. Covers reading CustomerInfo, checking entitlement.isActive as the single source of truth for access, and drilling into willRenew, periodType, and expirationDate when deeper logic is needed.
license: Apache-2.0; see LICENSE
metadata:
  author: RevenueCat
  source: revenuecat-handbook chapter 11
  keywords:
  - android
  - revenuecat
  - customerinfo
  - entitlement
  - is-active
  - will-renew
---

# Subscription States

Decide whether a user has access, and drive state aware UI, using `CustomerInfo` and `EntitlementInfo` on Android.

## Phase 1: Discover

Confirm what you are actually checking before you write code.

- Which entitlement identifier gates the feature? (for example `pro_access`)
- Do you need a plain access boolean, or do you also need to explain *why* the user has or lacks access (billing issue, canceled but still paid, paused)?
- Do you need the cached value (fast, possibly stale) or a freshly fetched value (server authoritative)?
- Are you refreshing UI once on launch, or reacting to live changes (purchase, restore, background refresh)?

If you only need access on/off, you only need `isActive`. Everything else is optional context.

## Phase 2: Plan

### Google's seven states versus RevenueCat's boolean

Rolling your own tracker with the Google Play Developer API means mapping seven subscription states and deciding which grant access.

| Google state | Grants access? |
|---|---|
| ACTIVE | yes |
| IN_GRACE_PERIOD | yes |
| CANCELED (before `expirationDate`) | yes |
| ON_HOLD | no |
| PAUSED | no |
| EXPIRED | no |
| PENDING | no |

RevenueCat computes this on the backend from the Google `SubscriptionPurchaseV2` resource and exposes the result as one field: `EntitlementInfo.isActive`. You read a boolean instead of implementing the state machine.

### What to read, and when

| Need | Field |
|---|---|
| Does the user have access right now? | `entitlement.isActive` |
| Will the subscription renew at period end? | `entitlement.willRenew` |
| When does paid access end? | `entitlement.expirationDate` |
| Is this a trial, intro, prepaid, or normal period? | `entitlement.periodType` |
| Is there a payment problem? | `entitlement.billingIssueDetectedAt` |
| Has the user canceled but still has time left? | `entitlement.unsubscribeDetectedAt` |
| Which store issued the entitlement? | `entitlement.store` |

### Decision rules

- Gate features on `isActive == true`. Nothing else.
- Use `billingIssueDetectedAt != null` to show a fix payment prompt.
- Use `unsubscribeDetectedAt != null` with `expirationDate` to show a renewal reminder while access is still valid.
- Use `!willRenew` (when no billing issue and no explicit cancel timestamp) to show a non renewing notice.

## Phase 3: Execute

### Read CustomerInfo and check access

```kotlin
val customerInfo = Purchases.sharedInstance.awaitCustomerInfo()
val hasAccess = customerInfo.entitlements["pro_access"]?.isActive == true
```

`awaitCustomerInfo()` returns the disk cache immediately, then refreshes from the network in the background. Entitlement checks stay fast, even offline.

### Force a fresh fetch when you must

Use this after a server side grant (for example, a support agent issued a promo).

```kotlin
val fresh = Purchases.sharedInstance.awaitCustomerInfo(
    fetchPolicy = CacheFetchPolicy.FETCH_CURRENT
)
```

### Drive state aware UI

`isActive` gates access; the other fields explain context.

```kotlin
fun updateUI(entitlement: EntitlementInfo?) {
    if (entitlement == null || !entitlement.isActive) {
        showSubscribeScreen(); return
    }
    showPremiumContent()
    when {
        entitlement.billingIssueDetectedAt != null -> showBillingIssueWarning()
        entitlement.unsubscribeDetectedAt != null ->
            entitlement.expirationDate?.let { showExpiryNotice(it) }
        !entitlement.willRenew -> showNonRenewingNotice()
    }
}
```

### Messaging guide by signal

| Signal on an active entitlement | Message to show |
|---|---|
| `billingIssueDetectedAt != null` | Payment problem, update method |
| `unsubscribeDetectedAt != null` | Access ends on `expirationDate` |
| `willRenew == false` (no other signal) | Will not renew this period |
| `periodType == TRIAL` or `INTRO` | Trial or intro pricing in effect |

### Identify the user for multi device

```kotlin
val result = Purchases.sharedInstance.awaitLogIn("your_user_id")
val customerInfo = result.customerInfo
val createdNewUser = result.created
```

`awaitLogIn()` merges anonymous purchases with the identified user. `logOut()` starts a fresh anonymous session.

## Phase 4: Verify

### Listen for CustomerInfo updates

Register a listener so UI reacts to purchases, restores, and background refreshes without manual polling.

```kotlin
Purchases.sharedInstance.updatedCustomerInfoListener =
    UpdatedCustomerInfoListener { info ->
        val active = info.entitlements["pro_access"]?.isActive == true
        updateAccessGate(active)
    }
```

The listener does not fire when the SDK starts with a cache hit and nothing changed. Always call `awaitCustomerInfo()` on launch in addition to setting the listener.

### Test matrix

Walk through each case and confirm the UI responds correctly.

| Case | Expected `isActive` | Expected UI |
|---|---|---|
| Fresh purchase | true | Premium content |
| Grace period (billing issue, still granted) | true | Premium + billing warning |
| Canceled, still before `expirationDate` | true | Premium + expiry notice |
| On hold | false | Subscribe screen |
| Paused | false | Subscribe screen |
| Expired | false | Subscribe screen |
| Pending (no payment yet) | false | Subscribe screen |

### Sanity checks

- Access gate flips correctly when the listener fires after a purchase.
- `FETCH_CURRENT` updates `CustomerInfo` after a backend grant (promo, refund, support action).
- After `logOut()`, `CustomerInfo` reflects an anonymous user and `isActive` resets accordingly.
- Offline launch still returns cached `CustomerInfo` and gates access without a network call.

## References

- [Full chapter](https://www.revenuecat.com/guides/revenuecat-android-sdk/subscription-states)
