---
name: rc-subscriptions
description: Use this skill when modeling subscriptions through RevenueCat's object model on Android. Covers Offerings, Packages, StoreProduct, SubscriptionOption, PricingPhase, and how they map to Google Play's Subscription, Base Plan, and Offer hierarchy.
license: Apache-2.0; see LICENSE
metadata:
  author: RevenueCat
  source: revenuecat-handbook chapter 4
  keywords:
  - android
  - revenuecat
  - subscriptions
  - offerings
  - packages
  - subscription-options
  - pricing-phase
---

# Subscriptions on Android with RevenueCat

Google Play exposes subscriptions through a three tier hierarchy: Subscription, Base Plan, and Offer. RevenueCat wraps that hierarchy in a flatter model you configure from the dashboard: Offerings, Packages, and SubscriptionOptions. You fetch an Offering, pick a Package, and in most flows let the SDK choose the right SubscriptionOption for you.

## Phase 1: Understand

The mapping from Google Play to RevenueCat:

| Google Play | RevenueCat |
|---|---|
| Subscription (product ID) | `StoreProduct` |
| Base Plan | `SubscriptionOption` (base plan) |
| Offer | `SubscriptionOption` (offer) |
| Group of base plans grouped in dashboard | `Package` inside an `Offering` |

Key types you will touch:

- `Offering`: a dashboard configured group of `Package` objects. `offerings.current` is the one you show by default.
- `Package`: a purchasable slot (monthly, annual, weekly, custom). Exposes a `product: StoreProduct`.
- `StoreProduct`: the Google Play subscription product. Has `subscriptionOptions: List<SubscriptionOption>?` and a `defaultOption`.
- `SubscriptionOption`: either a base plan or an offer. Has `pricingPhases`, `tags`, and an `id`.
- `PricingPhase`: one billing segment (intro trial, intro price, or recurring). Has `billingPeriod`, `price`, `offerPaymentMode`, and `recurrenceMode`.

See the [Subscriptions chapter on revenuecat.com](https://www.revenuecat.com/guides/revenuecat-android-sdk/subscriptions-with-revenuecat) for the object model diagram showing the full Offerings hierarchy alongside the CustomerInfo hierarchy used for entitlement checks.

## Phase 2: Plan

Before you write code, map your paywall to the object model. Answer these three questions.

### 2.1 Which Offering drives the paywall?

- Default paywall: use `offerings.current`. This is the Offering marked current in the dashboard and is the standard choice.
- Experiment or segment specific paywall: fetch `offerings.all["experiment-a"]`. You keep the dashboard in charge of which products appear, so no app update ships when the catalog changes.

### 2.2 Which Packages do you show?

Two access patterns, pick the one that matches your layout:

| Pattern | API | When to use |
|---|---|---|
| Named slots | `offering.monthly`, `offering.annual`, `offering.weekly` | Fixed paywall with known durations |
| Iteration | `offering.availablePackages` | Dynamic layout, unknown durations, or custom package types |

Standard `PackageType` values: `MONTHLY`, `ANNUAL`, `WEEKLY`, `TWO_MONTH`, `THREE_MONTH`, `SIX_MONTH`, `LIFETIME`. Anything else is `PackageType.CUSTOM`.

### 2.3 Does the paywall need a specific offer, or is the default fine?

| Situation | What to pass to `PurchaseParams` |
|---|---|
| Standard paywall, user gets best eligible offer automatically | `Package` |
| You need a specific offer (win back, promo, tag selected) | `SubscriptionOption` |

The SDK's `defaultOption` logic:

1. Filters out options tagged `"rc-ignore-offer"` or `"rc-customer-center"`.
2. Picks the option with the longest free trial or the cheapest first phase.
3. Falls back to the base plan if no offer qualifies.

Trial eligibility is not filtered by the SDK. Google Play only returns offers the user is eligible for, so if a user already consumed a free trial, that option simply will not appear in `subscriptionOptions` and the base plan becomes the default.

## Phase 3: Execute

### 3.1 Pull Offerings and pick a Package

```kotlin
val offerings = Purchases.sharedInstance.awaitOfferings()
val offering = offerings.current ?: return
val monthly = offering.monthly ?: return
val product = monthly.product
val price = product.price.formatted
val period = product.period?.iso8601 // "P1M", "P1Y", null for one time
```

For a dynamic list:

```kotlin
for (pkg in offering.availablePackages) {
    render(pkg.product.title, pkg.product.price.formatted, pkg.packageType)
}
```

### 3.2 Purchase with the default option

When the paywall shows a Package and you want the SDK to pick the best offer, pass the Package directly.

```kotlin
val params = PurchaseParams.Builder(activity, monthly).build()
val result = Purchases.sharedInstance.awaitPurchase(params)
```

### 3.3 Drill into `subscriptionOptions` for a specific offer

Use this when the paywall targets an offer by tag or offer ID, for example a win back offer.

```kotlin
val product = offering.monthly?.product ?: return
val winBack = product.subscriptionOptions
    ?.firstOrNull { it.tags.contains("win-back") }
val option = winBack ?: product.defaultOption ?: return
val params = PurchaseParams.Builder(activity, option).build()
```

Always fall back to `defaultOption` so the paywall still works when the targeted offer is absent (for example, the user is not eligible).

### 3.4 Render trial and intro pricing from `pricingPhases`

The first `PricingPhase` is the trial or intro price when present. Use `offerPaymentMode` for trial detection.

```kotlin
val option = pkg.product.defaultOption ?: return
val first = option.pricingPhases.first()
val isTrial = first.offerPaymentMode == OfferPaymentMode.FREE_TRIAL
```

`billingPeriod.value` is the count in the period's unit, not days. A `P1W` period gives `value = 1`, `unit = WEEK`. Build labels off both fields:

```kotlin
val p = first.billingPeriod
val label = when (p.unit) {
    Period.Unit.DAY -> "${p.value} day"
    Period.Unit.WEEK -> "${p.value} week"
    Period.Unit.MONTH -> "${p.value} month"
    Period.Unit.YEAR -> "${p.value} year"
    else -> p.iso8601
}
```

### 3.5 Prepaid plans

Prepaid base plans use the same `SubscriptionOption` API. Their `pricingPhases` report `RecurrenceMode.NON_RECURRING`. To accept pending purchases for prepaid plans, enable the flag at configuration time.

```kotlin
PurchasesConfiguration.Builder(context, apiKey)
    .pendingTransactionsForPrepaidPlansEnabled(true)
    .build()
```

### 3.6 Check access after purchase

Prefer entitlements. They reflect server computed access state including grace period, account hold, and cancellation with remaining time.

```kotlin
val info = result.customerInfo
val isPro = info.entitlements["pro"]?.isActive == true
```

If you need the raw product ID, use `customerInfo.activeSubscriptions`. It returns a `Set<String>` of `"subscriptionId:basePlanId"` entries.

## Decision summary

| Question | Answer |
|---|---|
| How do I fetch products? | `Purchases.sharedInstance.awaitOfferings()` then `offerings.current`. |
| How do I present durations? | `offering.monthly`/`annual`/`weekly` or iterate `availablePackages`. |
| How do I purchase? | Pass the `Package` to `PurchaseParams` and let `defaultOption` apply. |
| How do I target a specific offer? | Filter `product.subscriptionOptions` by tag or ID, pass the `SubscriptionOption`. |
| How do I detect a free trial? | `pricingPhases.first().offerPaymentMode == OfferPaymentMode.FREE_TRIAL`. |
| How do I check access? | `customerInfo.entitlements["<id>"]?.isActive`. |

## References

- [Full chapter](https://www.revenuecat.com/guides/revenuecat-android-sdk/subscriptions-with-revenuecat)
