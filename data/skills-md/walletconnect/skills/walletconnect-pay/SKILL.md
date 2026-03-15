---
name: walletconnect-pay
description: Guides wallet developers through integrating WalletConnect Pay SDK into mobile wallets (Kotlin, Swift, React Native, Flutter). Use when adding WC Pay payment acceptance, implementing pay link detection, handling USDC payment flows, or troubleshooting Pay SDK integration issues.
---

# WalletConnect Pay — Wallet Integration

## Goal

Help wallet developers integrate WalletConnect Pay so their users can pay at any compatible POS terminal or online checkout using USDC. The integration enables wallets to detect payment links, fetch payment options, collect signatures, and confirm transactions.

## When to use

- Adding WalletConnect Pay support to a mobile wallet
- Implementing payment link (QR code) detection and handling
- Debugging WC Pay SDK initialization or API errors
- Choosing between WalletKit, Standalone SDK, or API-First approaches
- Implementing data collection (KYC/KYT) WebView flow
- Setting up CAIP-10 account formatting for multi-chain payment options

## When not to use

- Building a merchant POS terminal (use the POS SDK instead — separate product)
- Building an e-commerce checkout (coming soon, different SDK)
- General WalletConnect pairing/session management unrelated to payments

## Supported Platforms & Assets

**Frameworks:** Kotlin (Android), Swift (iOS), React Native, Flutter
**Assets:** USDC only (currently)
**Networks:** Ethereum (`eip155:1`), Base (`eip155:8453`), Optimism (`eip155:10`), Polygon (`eip155:137`), Arbitrum (`eip155:42161`)

## Choose Your Integration Path

| Path | When to use | Complexity |
|------|-------------|------------|
| **WalletKit** (recommended) | Already using WalletConnect WalletKit | Lowest — Pay initializes automatically |
| **Standalone SDK** | No WalletKit dependency, want SDK convenience | Medium |
| **API-First** | Full control, no SDK, direct Gateway calls | Highest |

Jump to the right reference:
- [Kotlin (WalletKit)](references/kotlin-walletkit.md)
- [Swift (WalletKit)](references/swift-walletkit.md)
- [React Native (WalletKit)](references/react-native-walletkit.md)
- [Flutter (WalletKit)](references/flutter-walletkit.md)
- [Kotlin Standalone SDK](references/kotlin-standalone.md)
- [Swift Standalone SDK](references/swift-standalone.md)
- [React Native Standalone SDK](references/react-native-standalone.md)
- [Flutter Standalone SDK](references/flutter-standalone.md)
- [API-First (all platforms)](references/api-first.md)

## Prerequisites

1. **Project ID** — create a project at [dashboard.walletconnect.com](https://dashboard.walletconnect.com)
2. **App ID** — from the same dashboard; required for Pay initialization
3. **Android min SDK 23** / **iOS 13+** / **Node 16+** / **Flutter 3+**
4. For Standalone: contact WalletConnect team to obtain an API key

## Universal Payment Flow (all platforms)

Every integration follows these 6 steps:

```
QR Scan / Deep Link
        ↓
1. isPaymentLink(uri)       → branch: Pay vs. standard WC pairing
        ↓
2. getPaymentOptions(link, accounts)  → list of options + merchant info
        ↓
3. User selects option
        ↓
4. getRequiredPaymentActions(paymentId, optionId)  → signing actions
        ↓
5a. Sign actions (EIP-712 typed data, preserve order)
5b. [If collectData present] Show WebView → await IC_COMPLETE
        ↓
6. confirmPayment(paymentId, optionId, signatures)
```

### Step 1 — Detect payment links

Always check before routing to standard WalletConnect pairing.

```kotlin
// Kotlin (WalletKit)
if (WalletKit.Pay.isPaymentLink(uri)) {
    processPayment(uri)
} else {
    WalletKit.pair(Wallet.Params.Pair(uri))
}
```

```swift
// Swift (WalletKit)
if WalletKit.isPaymentLink(scannedString) {
    startPaymentFlow(paymentLink: scannedString)
}
```

```js
// React Native
import { isPaymentLink } from "@reown/walletkit";
if (isPaymentLink(uri)) { await processPayment(uri); }
```

```dart
// Flutter
if (walletKit.isPaymentLink(uri)) { /* process */ }
```

### Step 2 — Get payment options

Accounts **must** use CAIP-10 format: `eip155:{chainId}:{address}`
Provide accounts on all supported chains to maximize option availability.

```kotlin
val result = WalletKit.Pay.getPaymentOptions(
    paymentLink = uri,
    accounts = listOf("eip155:1:0x...", "eip155:8453:0x...", "eip155:137:0x...")
)
```

Response contains:
- `paymentId` — use in all subsequent calls
- `options[]` — each has `id`, `amount`, `account`, `collectData?`
- `info` — merchant name, amount, expiry (`expiresAt`)

### Step 3 — Get required signing actions

```kotlin
val actions = WalletKit.Pay.getRequiredPaymentActions(
    Wallet.Params.RequiredPaymentActions(paymentId, selectedOption.id)
)
```

Each action is a `WalletRpcAction` with `chainId`, `method` (`eth_signTypedData_v4`), and `params`.

### Step 4 — Sign actions

Sign **all** actions. **Order must match** the actions array exactly.

```kotlin
// Sign EIP-712 typed data — Kotlin example
val paramsArray = JSONArray(rpc.params)
val typedData = paramsArray.getString(1)
val encoder = StructuredDataEncoder(typedData)
val hash = encoder.hashStructuredData()
val signature = Sign.signMessage(hash, keyPair, false)
```

### Step 5 — Data collection (conditional)

Only show WebView when `selectedOption.collectData != null`.
**Never build native forms** — the WebView handles compliance, validation, and T&C.

```kotlin
selectedOption.collectData?.let { collectAction ->
    // Optional: prefill known user data
    val prefillBase64 = Base64.encode(JSONObject(userData).toString().toByteArray())
    val url = Uri.parse(collectAction.url)
        .buildUpon()
        .appendQueryParameter("prefill", prefillBase64)
        .build().toString()
    showWebView(url) // Listen for IC_COMPLETE / IC_ERROR
}
```

WebView JavaScript bridge messages:
- `IC_COMPLETE` → proceed to confirm
- `IC_ERROR` → show error, allow retry

### Step 6 — Confirm payment

```kotlin
val result = WalletKit.Pay.confirmPayment(
    Wallet.Params.ConfirmPayment(paymentId, selectedOption.id, signatures)
)
// Status: SUCCEEDED | PROCESSING | FAILED | EXPIRED | REQUIRES_ACTION
```

If `isFinal == false` and `pollInMs` is present, poll again after the delay.

## Validation checklist

- [ ] `isPaymentLink()` called before any WalletConnect pairing attempt
- [ ] All accounts formatted as CAIP-10 (`eip155:{chainId}:{address}`)
- [ ] Accounts provided for all 5 supported networks
- [ ] Signatures array order matches actions array order
- [ ] `collectData` checked per-option, not globally
- [ ] WebView used for data collection (no native form built)
- [ ] `expiresAt` monitored; user warned before expiry
- [ ] Loading states shown during API calls and signing
- [ ] Users shown WalletConnect Terms & Privacy Policy before data submission
- [ ] All 5 payment statuses handled in UI

## Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| `PaymentNotFound` | Invalid or deleted payment link | Show "payment not found" to user |
| `PaymentExpired` | User took too long | Show "payment expired, ask merchant to retry" |
| `InvalidAccount` | Bad CAIP-10 format | Verify `eip155:{chainId}:{address}` format |
| `ComplianceFailed` | KYC/KYT blocked the payment | Show message; do not retry automatically |
| `InvalidSignature` | Wrong signing order or method | Ensure signatures match actions array order |
| Init fails | Missing `appId` or `packageName` | Check dashboard for App ID |

## Examples

### Example 1 — QR scan handler (React Native)

```js
async function handleScan(uri) {
  if (isPaymentLink(uri)) {
    const options = await walletkit.pay.getPaymentOptions({
      paymentLink: uri,
      accounts: ["eip155:1:0xABC", "eip155:8453:0xABC"],
    });
    const option = options.options[0];
    const actions = await walletkit.pay.getRequiredPaymentActions({
      paymentId: options.paymentId,
      optionId: option.id,
    });
    const signatures = await Promise.all(
      actions.map(a => wallet.signTypedData(a.walletRpc.chainId, a.walletRpc.params))
    );
    const result = await walletkit.pay.confirmPayment({
      paymentId: options.paymentId,
      optionId: option.id,
      signatures,
    });
    showStatus(result.status); // "succeeded" | "processing" | etc.
  } else {
    await walletkit.pair({ uri });
  }
}
```

### Example 2 — Data collection gating (Swift)

```swift
// After getting actions and signing them:
if let collectData = selectedOption.collectData {
    // Must show WebView before confirmPayment
    let url = buildPrefillURL(base: collectData.url, userData: knownUserData)
    showWebView(url) { [weak self] in
        // IC_COMPLETE callback
        self?.confirmPayment(paymentId, selectedOption.id, signatures)
    }
} else {
    // No data collection needed → confirm directly
    confirmPayment(paymentId, selectedOption.id, signatures)
}
```

## Evaluations

1. **Activation** — "I'm building an Android wallet and want to support WalletConnect Pay. Walk me through the Kotlin WalletKit integration."
2. **Non-activation** — "How do I set up WalletConnect session management for my dApp?" (standard WC, not Pay)
3. **Edge case** — "My wallet only has Ethereum accounts. Will WC Pay still work?" (Answer: yes, but fewer options; recommend adding multi-chain accounts)
4. **Edge case** — "When should I show the WebView for data collection?" (Answer: only when `collectData` is non-null on the selected option)
5. **Framework choice** — "I don't use WalletKit. How do I integrate WC Pay on Flutter?" (Answer: use Flutter Standalone SDK)
6. **Standalone Swift** — "I'm building an iOS wallet without WalletKit. How do I add WC Pay?" (Answer: use Swift Standalone SDK with SPM)
7. **Standalone React Native** — "How do I add WC Pay to my React Native wallet without WalletKit?" (Answer: use `@walletconnect/pay` standalone package)
