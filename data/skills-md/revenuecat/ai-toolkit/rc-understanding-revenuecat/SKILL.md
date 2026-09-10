---
name: rc-understanding-revenuecat
description: Use this skill to orient an agent to the RevenueCat Android SDK (10.x) architecture. Covers how RevenueCat reorganizes BillingClient, Google Play Developer API, and RTDN into a single SDK, and how Products, Packages, Offerings, Entitlements, and CustomerInfo connect.
license: Apache-2.0; see LICENSE
metadata:
  author: RevenueCat
  source: revenuecat-handbook chapter 1
  keywords:
  - android
  - revenuecat
  - sdk
  - architecture
  - offerings
  - entitlements
  - customerinfo
---

# Understanding RevenueCat

## Phase 0: Intent

Use this skill before writing any RevenueCat code. It gives you the vocabulary and mental model you need so that downstream skills (setup, configuration, purchase flow, entitlements) make sense.

Start here if any of these apply:

- You are new to RevenueCat or coming from a raw Play Billing integration.
- You are unsure which concept maps to which dashboard object.
- You need to decide which downstream skill to invoke for a specific user goal.

Skip this skill if you already know the difference between an Offering, a Package, a Product, and an Entitlement, and you already know that `Purchases.sharedInstance` is the single entry point.

## Phase 1: Orient

Raw Android in-app purchases require three separate systems. RevenueCat folds all three into one SDK plus one dashboard.

| Raw Google Play stack | RevenueCat replacement | Where it lives |
|---|---|---|
| `BillingClient` on the client | `Purchases` SDK | Your Android app |
| Google Play Developer API on your server | RevenueCat backend | RevenueCat managed |
| Real Time Developer Notifications via Cloud Pub/Sub | RevenueCat webhooks | RevenueCat managed, delivered to your server |

The call path is:

```text
Your App
  -> Purchases SDK
  -> RevenueCat Backend
  -> Google Play Developer API
  -> Google Play
```

Your app talks to the `Purchases` SDK. The SDK talks to Google Play for the purchase UI and to the RevenueCat backend for verification and entitlement storage. Your server side code talks to the RevenueCat backend, not to Google Play directly.

One consequence: RevenueCat sits in the purchase verification path. After a user completes a purchase, the SDK posts the token to RevenueCat before your app sees confirmation. You trade a network round trip for not having to build server side verification yourself.

### The four concepts you must know

| Concept | What it is | Where you define it |
|---|---|---|
| Product | A subscription, base plan, or one time purchase | Google Play Console |
| Package | A Product wrapped with a type label (Monthly, Annual, Lifetime, custom). The unit your paywall displays | RevenueCat dashboard |
| Offering | A group of Packages. One Offering is marked Current and returned by `offerings.current` | RevenueCat dashboard |
| Entitlement | A logical access level your app checks, such as `"pro_access"`. Products are attached to Entitlements | RevenueCat dashboard |

`CustomerInfo` is the runtime snapshot of the user's purchase history and active Entitlements, computed and cached by RevenueCat.

### The only two reads you need most of the time

```kotlin
val offerings = Purchases.sharedInstance.awaitOfferings()
val monthly = offerings.current?.monthly
```

```kotlin
val customerInfo = Purchases.sharedInstance.awaitCustomerInfo()
val hasPro = customerInfo.entitlements["pro_access"]?.isActive == true
```

`isActive` already resolves the seven Play subscription states (ACTIVE, IN_GRACE_PERIOD, ON_HOLD, PAUSED, CANCELED, EXPIRED, PENDING) on the server side. You do not reimplement that logic on the client.

### The singleton

`Purchases.sharedInstance` is the single entry point. You configure it once at app startup:

```kotlin
Purchases.configure(
    PurchasesConfiguration.Builder(context, "your_api_key")
        .appUserID("optional_user_id")
        .build()
)
```

Unlike `BillingClient`, the singleton does not require you to manage connection state. It reconnects and queues calls for you.

### What RevenueCat does not replace

- Google Play Console. You still create products, base plans, and offers there.
- Your app UI. You still build the paywall and display prices. RevenueCat supplies the data.
- Your authentication system. You bring your own user IDs and pass them to the SDK.

### The tradeoff

You offload verification complexity and take on a dependency. If the RevenueCat backend has an outage, purchase verification is affected. Two mitigations exist and they are different:

| Feature | What it does | When it kicks in |
|---|---|---|
| Disk cache of `CustomerInfo` | Returns the last known server state for entitlement checks | Automatic, always on |
| Offline Entitlements | Computes entitlements on the device from local Play Store purchases | Only when you explicitly configure it |

Neither is a full substitute for a reachable backend. Use both where they apply.

## Phase 2: Map the user goal to a downstream skill

Once you have the model above, pick the next skill based on what the user actually wants to do.

| User goal | Next skill |
|---|---|
| Install the SDK, wire up Gradle, add permissions, configure the Play Console product | `rc-setup` |
| Call `Purchases.configure`, pass an `appUserID`, set log level, attach attributes | `rc-configuring-the-sdk` |
| Fetch Offerings, show a paywall, call `purchase`, handle the result | `rc-purchase-flow` |
| Check `customerInfo.entitlements["..."]?.isActive`, gate features, listen for updates | `revenuecat/entitlements-and-customerinfo` |
| Identify, alias, or log out a user | `revenuecat/user-identity` |
| Handle restore purchases, cross device, promo codes | `revenuecat/restore-and-recovery` |
| Receive server side events from RevenueCat | `rc-webhooks` |
| Debug a specific purchase, receipt, or entitlement in production | `revenuecat/debugging` |

If the user's goal does not match any row, stay here and keep clarifying intent before routing.

## Phase 3: Sanity check

Before you leave this skill and route to a downstream one, confirm out loud:

1. You can name which of the three raw pillars (client billing, server Play Developer API, RTDN) the user's question touches.
2. You can state whether the user is asking about a Product, a Package, an Offering, or an Entitlement. These are not interchangeable.
3. You know whether the user needs `Offerings` (what to sell) or `CustomerInfo` (what the user already owns). Most confusion comes from mixing these two.
4. You have picked exactly one downstream skill to invoke next, or you have a concrete clarifying question.

If any of the four fail, reread Phase 1 or the chapter before proceeding.

## References

- [Full chapter](https://www.revenuecat.com/guides/revenuecat-android-sdk/understanding-revenuecat)
