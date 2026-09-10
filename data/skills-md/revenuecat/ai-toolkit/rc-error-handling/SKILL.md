---
name: rc-error-handling
description: Use this skill when handling errors from the RevenueCat Android SDK. Covers PurchasesError, the PurchasesErrorCode enum, the userCancelled flag on PurchasesTransactionException, and the recommended UI response per code.
license: Apache-2.0; see LICENSE
metadata:
  author: RevenueCat
  source: revenuecat-handbook chapter 8
  keywords:
  - android
  - revenuecat
  - error-handling
  - purchases-error
  - purchases-error-code
  - purchases-transaction-exception
---

# Error Handling

## Phase 1: Understand

With raw Google Play Billing you enumerate every `BillingResponseCode`, split them into retriable and non retriable groups, and build backoff retry logic. RevenueCat collapses this into a single type you deal with: `PurchasesError`.

```kotlin
public class PurchasesError(
    val code: PurchasesErrorCode,
    val underlyingErrorMessage: String? = null,
) {
    val message: String // technical description, for logs
}
```

Key facts you rely on:

- `PurchasesErrorCode` is a cross platform enum with stable, readable codes.
- `error.message` is a technical string. It belongs in logs, not in the UI.
- `awaitPurchase()` throws `PurchasesTransactionException`, which adds a `userCancelled: Boolean` flag.
- Every other `await*` call (`awaitOfferings`, `awaitGetProducts`, `awaitCustomerInfo`, `awaitRestore`) throws `PurchasesException`.
- The SDK already retries transient billing and network failures internally. Any error that reaches you has exhausted the SDK retry budget. You do not add your own backoff loop. The only retry you implement is a user triggered "Try Again" button.

## Phase 2: Plan

Before writing a `catch` block, decide three things:

1. Which `await*` call are you wrapping? That picks the exception type.
2. Which codes have specific handling? Everything else falls into a generic branch.
3. What user facing string does each handled code map to?

Use this table to categorize `PurchasesErrorCode` values and pick the UX response.

| Code | Meaning | Handling |
|---|---|---|
| `PurchaseCancelledError` | User backed out of the flow | Do nothing. `userCancelled` is also `true`. |
| `ProductAlreadyPurchasedError` | Product already active for the user | Refresh `CustomerInfo` and check entitlements. |
| `PaymentPendingError` | Purchase entered pending state | Show a pending message. Wait for `UpdatedCustomerInfoListener`. |
| `NetworkError` | Request failed due to connectivity | Prompt the user to retry. |
| `StoreProblemError` | Google Play issue | Prompt to retry or update Play Store. |
| `PurchaseNotAllowedError` | Device or account cannot purchase | Show an explanatory message. |
| `IneligibleError` | User not eligible for the offer | Show the base plan instead. |

Exception type decision:

| Call | Exception to catch | `userCancelled` available? |
|---|---|---|
| `awaitPurchase()` | `PurchasesTransactionException` | Yes |
| `awaitRestore()` | `PurchasesException` | No |
| `awaitOfferings()` | `PurchasesException` | No |
| `awaitGetProducts()` | `PurchasesException` | No |
| `awaitCustomerInfo()` | `PurchasesException` | No |

## Phase 3: Execute

### Purchase errors

Check `userCancelled` first and return silently. Then branch on `error.code`.

```kotlin
try {
    val result = Purchases.sharedInstance.awaitPurchase(params)
    handleSuccess(result.customerInfo)
} catch (e: PurchasesTransactionException) {
    if (e.userCancelled) return
    when (e.error.code) {
        PurchasesErrorCode.PaymentPendingError -> showPendingMessage()
        PurchasesErrorCode.ProductAlreadyPurchasedError -> {
            val info = Purchases.sharedInstance.awaitCustomerInfo()
            handleSuccess(info)
        }
        PurchasesErrorCode.NetworkError -> showRetryDialog()
        else -> showGenericError(userFacingMessage(e.error))
    }
}
```

### Non purchase errors

Catch `PurchasesException` and branch on the code. Use offline or cached fallbacks where you have them.

```kotlin
try {
    val offerings = Purchases.sharedInstance.awaitOfferings()
    displayOfferings(offerings)
} catch (e: PurchasesException) {
    when (e.error.code) {
        PurchasesErrorCode.NetworkError -> showOfflineFallback()
        else -> logError(e.error)
    }
}
```

### Map codes to user facing strings

Keep a single mapping function. Never pass `e.error.message` to the UI.

```kotlin
fun userFacingMessage(error: PurchasesError): String = when (error.code) {
    PurchasesErrorCode.PurchaseCancelledError -> ""
    PurchasesErrorCode.NetworkError ->
        "Please check your internet connection and try again."
    PurchasesErrorCode.StoreProblemError ->
        "There was a problem with Google Play. Please try again."
    PurchasesErrorCode.ProductAlreadyPurchasedError ->
        "You already have this subscription."
    PurchasesErrorCode.PaymentPendingError ->
        "Your payment is being processed. We'll notify you when it completes."
    else -> "Something went wrong. Please try again."
}
```

## Checklist

- You picked `PurchasesTransactionException` for `awaitPurchase` and `PurchasesException` elsewhere.
- You checked `userCancelled` before any branching on `error.code`.
- You handled `PaymentPendingError`, `ProductAlreadyPurchasedError`, and `NetworkError` with their specific flows.
- You logged `error.message` and showed a mapped string from `userFacingMessage` to the user.
- You did not add retry loops around SDK calls. Retries are user initiated only.

## References

- [Full chapter](https://www.revenuecat.com/guides/revenuecat-android-sdk/error-handling)
