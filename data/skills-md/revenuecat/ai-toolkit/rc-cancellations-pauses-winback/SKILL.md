---
name: rc-cancellations-pauses-winback
description: Use this skill when surfacing cancellation, pause, and winback state on Android with RevenueCat. Covers reading unsubscribeDetectedAt, billingIssuesDetectedAt, pause state via periodType, managementURL for deep link, and pause resume date lookup via the REST API.
license: Apache-2.0; see LICENSE
metadata:
  author: RevenueCat
  source: revenuecat-handbook chapter 13
  keywords:
  - android
  - revenuecat
  - cancellation
  - pause
  - winback
  - management-url
---

# Cancellations, Pauses, and Winback

Detect cancellation, pause, and winback states on Android by reading `CustomerInfo`. Most of these events are passive: your app observes them rather than initiates them. Open Google Play's manage screen with `managementURL`. Look up the pause resume date from the REST API.

## Phase 1: Scope

Decide what state you need to surface to the user.

| State | Signal in CustomerInfo | Notes |
|---|---|---|
| Canceled, still has access | `entitlement.unsubscribeDetectedAt != null` and `isActive == true` | Show "ends on [expirationDate]" |
| Billing issue (grace or hold) | `entitlement.billingIssuesDetectedAt != null` | Payment failed, recovery in progress |
| Paused | `entitlement.isActive == false` while product is still owned | Resume date requires REST API |
| Active and renewing | `entitlement.willRenew == true` | Normal state |

Backend win back campaign segmentation uses the `CANCELLATION` webhook `cancel_reason` field (`UNSUBSCRIBE`, `BILLING_ERROR`, `DEVELOPER_INITIATED`, `PRICE_INCREASE`).

## Phase 2: Prepare

Confirm you already have a fetched `CustomerInfo` from `Purchases.sharedInstance.getCustomerInfo(...)` or a listener. You do not need to call `BillingClient.queryPurchasesAsync` with `setIncludeSuspendedSubscriptions(true)`. RevenueCat resolves pause state from the server side subscription state.

Rules:

- `managementURL` is already `Uri?`. Pass it straight to the Intent. Do not call `Uri.parse(url.toString())`.
- Do not compute access manually from `expirationDate`. Read `isActive` and `willRenew`.
- Pause resume date is not in the SDK. Fetch it from `/v1/subscribers/{app_user_id}` in your backend.

## Phase 3: Execute

### Detect cancellation with remaining access

```kotlin
val entitlement = customerInfo.entitlements["pro_access"]
if (entitlement?.unsubscribeDetectedAt != null && entitlement.isActive) {
    entitlement.expirationDate?.let { expiry ->
        showCancellationBanner(expiry)
    }
}
```

`unsubscribeDetectedAt` is set when RevenueCat receives the `SUBSCRIPTION_CANCELED` RTDN. `isActive` stays `true` until the billing period ends.

### Detect pause

```kotlin
val entitlement = customerInfo.entitlements["pro_access"]
val hasAccess = entitlement?.isActive == true
// When paused, isActive == false. Pause resume date is not in the SDK.
```

### Open the subscription management screen

```kotlin
customerInfo.managementURL?.let { url ->
    startActivity(Intent(Intent.ACTION_VIEW, url))
}
```

`managementURL` is typed as `Uri?`. Use it directly. Wrapping it with `Uri.parse(url.toString())` is redundant and error prone.

### Look up pause resume date via REST

From your backend, call the subscribers endpoint and read `paused_expiration_time_ms` on the subscription:

```bash
curl -H "Authorization: Bearer $RC_SECRET_API_KEY" \
  https://api.revenuecat.com/v1/subscribers/$APP_USER_ID
```

The subscription object contains `paused_expiration_time_ms` when paused. Expose this to your client through your own endpoint.

### Resubscribe before expiry

Google's resubscribe before expiry flow fires `SUBSCRIPTION_RESTARTED`. RevenueCat clears `unsubscribeDetectedAt` and sets `willRenew = true`. No extra code required, just re-read `customerInfo`.

### Resubscribe after expiry

A resubscribe after expiry fires a `RENEWAL` webhook, not `INITIAL_PURCHASE`. Grant entitlement access on both events in your backend handler.

## Phase 4: Verify

| Check | How |
|---|---|
| Cancellation banner shows | Cancel in Play Store, pull fresh `CustomerInfo`, confirm `unsubscribeDetectedAt != null` and `isActive == true` |
| Management deep link opens | Tap the link, verify Play subscriptions screen opens for the correct product |
| Pause is reflected | Pause in Play Store sandbox, confirm `entitlement.isActive == false` |
| Pause resume date | Call `/v1/subscribers/{id}`, confirm `paused_expiration_time_ms` is present |
| Win back accepted | Accept a Play configured win back offer, confirm the purchase surfaces as a normal subscription in `CustomerInfo` |

## Notes

- Deferral and revocation are done through the Google Play Developer API (`purchases.subscriptionsv2.defer`, `purchases.subscriptionsv2.revoke`) from your backend. RevenueCat processes the resulting RTDN and updates `CustomerInfo` automatically.
- Win back campaigns need no SDK code. They are configured in Play Console or the RevenueCat dashboard.
- RevenueCat does not currently emit a dedicated pause webhook. Pause state appears in `CustomerInfo` once the Google Play RTDN is processed.

## References

- [Full chapter](https://www.revenuecat.com/guides/revenuecat-android-sdk/cancellations-pauses-and-winback)
