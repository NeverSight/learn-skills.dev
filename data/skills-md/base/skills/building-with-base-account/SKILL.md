---
name: building-with-base-account
description: Integrates Base Account SDK for authentication and payments. Covers Sign in with Base (SIWB), Base Pay, Paymasters, Sub Accounts, Spend Permissions, Prolinks, and batch transactions. Use when building apps with wallet authentication, USDC payments, sponsored transactions, smart wallet features, recurring subscriptions, shareable payment links, or any onchain interaction on Base. Covers phrases like "add sign in with Base", "SIWB button", "accept USDC payments", "Base Pay", "paymaster setup", "gas sponsorship", "smart wallet", "sub account", "spend permissions", or "payment link".
---

# Building with Base Account

Base Account is an ERC-4337 smart wallet providing universal sign-on, one-tap USDC payments, and multi-chain support (Base, Arbitrum, Optimism, Zora, Polygon, BNB, Avalanche, Lordchain, Ethereum Mainnet).

## Quick Start

```bash
npm install @base-org/account @base-org/account-ui
```

```typescript
import { createBaseAccountSDK } from '@base-org/account';

const sdk = createBaseAccountSDK({
  appName: 'My App',
  appLogoUrl: 'https://example.com/logo.png',
  appChainIds: [8453], // Base Mainnet
});

const provider = sdk.getProvider();
```

## Feature References

Read the reference for the feature you're implementing:

| Feature | Reference | When to Read |
|---------|-----------|-------------|
| Sign in with Base | [references/authentication.md](references/authentication.md) | Wallet auth, SIWE, backend verification, SignInWithBaseButton, Wagmi/Privy setup |
| Base Pay | [references/payments.md](references/payments.md) | One-tap USDC payments, payerInfo, server-side verification, BasePayButton |
| Subscriptions | [references/subscriptions.md](references/subscriptions.md) | Recurring charges, spend permissions, CDP wallet setup, charge/revoke lifecycle |
| Sub Accounts | [references/sub-accounts.md](references/sub-accounts.md) | App-specific embedded wallets, key generation, funding |
| Capabilities | [references/capabilities.md](references/capabilities.md) | Batch transactions, gas sponsorship (paymasters), atomic execution, auxiliaryFunds, attribution |
| Prolinks | [references/prolinks.md](references/prolinks.md) | Shareable payment links, QR codes, encoded transaction URLs |
| Troubleshooting | [references/troubleshooting.md](references/troubleshooting.md) | Popup issues, gas usage, unsupported calls, migration, doc links |

## Critical Requirements

### Security

- **Track transaction IDs** to prevent replay attacks
- **Verify sender matches authenticated user** to prevent impersonation
- **Use a proxy** to protect Paymaster URLs from frontend exposure
- **Paymaster providers must be ERC-7677-compliant**
- **Never expose CDP credentials client-side** (subscription backend only)

### Popup Handling

- Generate nonces **before** user clicks "Sign in" to avoid popup blockers
- Use `Cross-Origin-Opener-Policy: same-origin-allow-popups`
- `same-origin` breaks the Base Account popup

### Base Pay

- Base Pay works independently from SIWB — no auth required for `pay()`
- `testnet` param in `getPaymentStatus()` must match `pay()` call
- Never disable actions based on onchain balance alone — check `auxiliaryFunds` capability

### Sub Accounts

- Call `wallet_addSubAccount` each session before use
- Ownership changes expected on new devices/browsers
- Only Coinbase Smart Wallet contracts supported for import

### Smart Wallets

- ERC-6492 wrapper enables signature verification before wallet deployment
- Viem's `verifyMessage`/`verifyTypedData` handle this automatically

## For Edge Cases and Latest API Changes

- **AI-optimized docs**: [docs.base.org/llms.txt](https://docs.base.org/llms.txt)
- **Full reference**: [docs.base.org/base-account](https://docs.base.org/base-account)
