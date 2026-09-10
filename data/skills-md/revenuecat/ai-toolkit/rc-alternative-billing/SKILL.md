---
name: rc-alternative-billing
description: Use this skill when scoping Google Play alternative billing work with RevenueCat Android SDK 10.x. Documents the current support status, which flows RevenueCat abstracts and which require direct integration at the time the chapter was written.
license: Apache-2.0; see LICENSE
metadata:
  author: RevenueCat
  source: revenuecat-handbook chapter 18
  keywords:
  - android
  - revenuecat
  - alternative-billing
  - sdk8
  - user-choice-billing
---

# Alternative Billing Programs

Google runs several programs that let you collect payment outside standard Play Store billing. This skill tells you which pieces the RevenueCat Android SDK covers today and which ones you implement yourself against the Play Billing Library.

Per the handbook chapter, RevenueCat has limited support for these programs as of SDK 9.x. Treat that as the status of record; check the RevenueCat changelog for any newer SDK releases before you start work.

## Phase 1: Discovery

Answer these before writing any code.

| Question | Why it matters |
|---|---|
| Which program are you targeting? | User Choice Billing, Alternative Billing Only, External Offers, and External Payment Links each have different Play requirements. |
| Is your app eligible in the target region? | Google gates these programs by country and app category. You enroll through Play Console, not through RevenueCat. |
| Are you using RevenueCat Web Billing instead? | RevenueCat's web checkout is a separate product from Google's alternative billing. Do not conflate the two. |
| Which RevenueCat SDK version are you on? | Support evolves per release. What is unsupported in SDK 9.x may land later. |

If you actually want to sell subscriptions via a RevenueCat-hosted web checkout, that is not one of Google's alternative billing programs. Use `Offering.webCheckoutURL` or `Package.webCheckoutURL`:

```kotlin
val pkg = offerings.current?.monthly
pkg?.webCheckoutURL?.let { url ->
    startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url.toString())))
}
```

After the user completes that purchase on the web, they redeem it in-app via deep link handling.

## Phase 2: Plan

Decide which of the two paths fits.

**Path A: Wait for SDK support.** If your launch timeline is flexible, watch the RevenueCat changelog and docs for first-class support of the specific program you need. This avoids running raw Play Billing Library code alongside RevenueCat.

**Path B: Hand roll the integration.** If you must ship now, implement the Play Billing Library APIs for the target program directly. The RevenueCat SDK owns the `BillingClient` instance, so running raw `BillingClient` calls alongside it needs care.

For Path B, set completion ownership so RevenueCat does not interfere with acknowledgement of purchases you are managing:

```kotlin
Purchases.configure(
    PurchasesConfiguration.Builder(context, apiKey)
        .purchasesAreCompletedBy(PurchasesAreCompletedBy.MY_APP)
        .build()
)
```

Planning checklist:

- [ ] Confirmed the Play program and regional eligibility in Play Console.
- [ ] Read the current RevenueCat docs and changelog for the SDK version you ship.
- [ ] Chose Path A or Path B with a clear reason.
- [ ] If Path B, identified which flows RevenueCat still drives and which you drive.

## Phase 3: Execute

What RevenueCat's SDK currently supports in this space, per the chapter:

| Flow | SDK coverage |
|---|---|
| RevenueCat Web Billing via `Offering.webCheckoutURL` / `Package.webCheckoutURL` | Supported. Not a Google alternative billing program. |
| User Choice Billing | No dedicated SDK APIs. Implement via Play Billing Library alongside RevenueCat. |
| Alternative Billing Only | No dedicated SDK APIs. Implement via Play Billing Library alongside RevenueCat. |
| External Offers | No dedicated SDK APIs. Implement via Play Billing Library alongside RevenueCat. |
| External Payment Links | No dedicated SDK APIs. Implement via Play Billing Library alongside RevenueCat. |

When you ship Path B, use `PurchasesAreCompletedBy.MY_APP` so acknowledgement stays in your hands for the purchases you manage, and leave the standard Play Store purchases to the RevenueCat SDK.

Verification steps:

- [ ] Standard Play Store purchases still flow through RevenueCat and appear in the dashboard.
- [ ] Purchases made through the alternative billing path reach your backend and are reconciled with RevenueCat subscriber state.
- [ ] Acknowledgement happens exactly once per purchase, with no double-handling between your code and the SDK.

## References

- [Full chapter](https://www.revenuecat.com/guides/revenuecat-android-sdk/alternative-billing-programs)

- RevenueCat Docs: https://www.revenuecat.com/docs/
- RevenueCat Codelabs: https://revenuecat.github.io/
