---
name: rc-revenuecat-vs-raw-billing
description: Use this skill to decide whether to use RevenueCat or raw Google Play Billing on Android. Provides a side by side reference of what RevenueCat handles versus what remains your responsibility at both client and backend layers.
license: Apache-2.0; see LICENSE
metadata:
  author: RevenueCat
  source: revenuecat-handbook appendix B
  keywords:
  - android
  - revenuecat
  - comparison
  - decision
  - raw-billing
---

# RevenueCat vs Raw Google Play Billing

## Phase 0: Intent

Use this skill when you are choosing between integrating RevenueCat or wiring Google Play Billing Library (PBL) directly, and you need to see which concerns disappear, which shift, and which still land on your team. The decision covers both the Android client and any server side infrastructure that supports subscriptions or one time purchases.

Typical questions this skill answers:

- If I adopt RevenueCat, what client code no longer exists in my app?
- What backend pieces (receipt verification, RTDN, state machine) does RevenueCat replace?
- What do I still own regardless of which path I pick?
- Is there a concern where raw PBL is the only option today?

## Phase 1: Locate the Concern

Before reading the tables, identify what you are actually evaluating. Sort your requirement into one of these buckets and jump to the matching section:

| Bucket | Examples | Go to |
|---|---|---|
| Client purchase plumbing | BillingClient, listeners, acknowledgement, consumption | Client side table |
| Server purchase truth | Token validation, RTDN, entitlement state machine | Server side table |
| Out of scope for either | Auth, your user DB, paywall UI, push | Your responsibility table |

If the concern is split (for example, RevenueCat verifies the token but you still need to gate premium content on your API), you own the integration glue even though the verification itself is handled.

## Phase 2: Side by Side Reference

### Client side

| Concern | Raw PBL | RevenueCat |
|---|---|---|
| BillingClient setup and configuration | You write | Handled internally |
| Connection lifecycle and reconnection | You write | Handled internally |
| PurchasesUpdatedListener | You write | Replaced by purchase callbacks |
| queryProductDetailsAsync() | You write | Replaced by awaitOfferings() / awaitGetProducts() |
| launchBillingFlow() | You write | Called internally by awaitPurchase() |
| Acknowledgement after purchase | You write | Handled automatically |
| Consumption of consumables | You write | Handled automatically (mark product as consumable in dashboard) |
| queryPurchasesAsync() on launch | You write | Handled internally on connection |
| Retry logic for transient errors | You write | Handled internally by SDK |
| BillingResponseCode handling | You write | Abstracted to PurchasesErrorCode |
| In-app payment recovery messages | You write | Automatic (showInAppMessagesAutomatically = true) |
| Subscription option selection for offers | You write | defaultOption selected automatically |

### Server side

| Concern | Raw PBL | RevenueCat |
|---|---|---|
| Google Play Developer API integration | You build | RevenueCat backend |
| Service account credential management | You manage | Configured once in RC dashboard |
| Receipt verification on every purchase | You build | Automatic |
| Purchase token validation and deduplication | You build | RevenueCat backend |
| linkedPurchaseToken chain traversal | You build | RevenueCat backend |
| RTDN processing and dispatch | You build | RevenueCat processes, sends webhooks |
| Cloud Pub/Sub setup | You set up | Not needed |
| Subscription state machine on backend | You build | CustomerInfo computed by RC |
| Entitlement computation across 7 states | You build | isActive computed by RC |
| Grace period / account hold tracking | You build | billingIssueDetectedAt |
| Cancellation with access-until-expiry logic | You build | isActive + unsubscribeDetectedAt |
| Price cohort tracking | You build | RC backend handles |
| Product-to-entitlement mapping | You build | Configured in RC dashboard |

### What remains your responsibility either way

| Concern | Notes |
|---|---|
| User authentication system | You bring your own; pass user ID to RC |
| Your own database of users | RC is not your primary user database |
| Premium content server side | Verify via RC REST API or webhooks |
| Webhook receiver endpoint | You build; RC sends, you receive |
| Play Console product creation | Still done in Play Console |
| Subscription deferral | Direct Google Play API call |
| Subscription revocation | Direct Google Play API call |
| Alternative billing programs | Limited RC support; may need raw PBL |
| App UI (paywalls, onboarding) | You build (RC Paywalls UI optional) |
| Push notifications for payment issues | You build on top of webhook events |

## Phase 3: Recommendation Heuristic

Use these rules to convert the tables into a decision:

1. If your app needs subscription deferral, subscription revocation, or an alternative billing program that RevenueCat does not yet cover, plan to keep a raw PBL path for those specific calls regardless of your main choice.
2. If you would otherwise build a receipt verification service, an RTDN pipeline, and a subscription state machine from scratch, the server side table lists at least eight concerns that RevenueCat removes. Choose RevenueCat unless you have a concrete reason to own that stack.
3. If you already have a mature billing backend with verified tokens and tested state handling, the gain is smaller. Weigh it against RevenueCat's client side simplifications and dashboard driven catalog.
4. Always confirm the "remains your responsibility" row items are staffed. RevenueCat does not replace your auth, your user database, your paywall UI, or your premium content gate. Passing `appUserID` and verifying entitlements server side via the REST API or webhooks is still on you.
5. When in doubt, map every requirement to a row in one of the three tables. Anything that lands in the "remains your responsibility" table costs the same under either option and should not drive the decision.

Quick gate:

```text
need custom RTDN pipeline?      -> raw PBL only if you must own it end to end
need deferral or revocation?    -> keep a raw PBL path for those API calls
need fast time to production?   -> RevenueCat, then add raw PBL escape hatches later
```

## References

- [Full chapter](https://www.revenuecat.com/guides/revenuecat-android-sdk/appendix-what-revenuecat-replaces)
