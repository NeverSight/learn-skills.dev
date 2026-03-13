---
name: walletconnect-pay
description: Manages the walletconnect-pay CLI for creating and completing WalletConnect Pay payments from the terminal. Use when the user wants to create a payment, check payment status, or complete a checkout with a connected wallet.
---

# WalletConnect Pay CLI (Experimental)

> **This package is experimental.** APIs and CLI interfaces may change significantly between releases. Use at your own risk.

## Goal

Operate the `walletconnect-pay` CLI to create payments, check payment status, and complete checkout flows using a connected wallet.

## When to use

- User asks to create a WalletConnect Pay payment
- User asks to check the status of a payment
- User asks to pay or checkout a payment with their wallet
- User mentions `walletconnect-pay` or WalletConnect Pay
- User wants to complete a payment flow end-to-end

## When not to use

- User wants basic wallet connection without payments (use `walletconnect` skill)
- User wants to stake WCT tokens (use `walletconnect-staking` skill)
- User is working on the pay-cli source code (just edit normally)

## Prerequisites

- Binary is at `packages/pay-cli/dist/cli.js` (or globally linked as `walletconnect-pay`)
- Build first if needed: `npm run build -w @walletconnect/pay-cli`
- A connected CWP wallet provider is required for `checkout` (the `walletconnect` CLI must be installed)

## Authentication modes

The CLI supports two modes:

### Proxy mode (default, no API keys needed)
Routes requests through the WalletConnect Pay frontend. Used automatically when `WC_PAY_WALLET_API_KEY` is not set, or when `--proxy` is passed.

### Direct API mode
Requires environment variables:

```bash
# Required for all direct API calls
export WC_PAY_WALLET_API_KEY=<wallet-api-key>

# Required only for merchant operations (create)
export WC_PAY_PARTNER_API_KEY=<partner-api-key>
export WC_PAY_MERCHANT_ID=<merchant-id>
```

## Commands

```bash
# Check payment status
walletconnect-pay status <paymentId>
walletconnect-pay status <paymentId> --staging

# Create a new payment (requires merchant credentials)
walletconnect-pay create <amount>
walletconnect-pay create 1000 --unit iso4217/USD --staging

# Complete a payment with a connected wallet
walletconnect-pay checkout <paymentId>
walletconnect-pay checkout <paymentId> --staging --proxy
```

### `status <paymentId>`
Read-only. Displays payment amount, merchant, status, and expiry.

Options:
- `--staging` — Use the staging API
- `--proxy` — Force proxy mode (no API keys needed)

### `create <amount>`
Creates a new payment. Amount is in minor units (e.g. `1000` = $10.00).

Options:
- `--unit <string>` — Currency unit (default: `iso4217/USD`)
- `--reference-id <string>` — Merchant/PSP order ID
- `--staging` — Use the staging API
- `--proxy` — Force proxy mode

### `checkout <paymentId>`
Full checkout flow: fetches payment → connects wallet → gets payment options → signs transaction → submits compliance data → confirms → polls for result.

Options:
- `--wallet <string>` — Use a specific CWP wallet provider
- `--staging` — Use the staging API
- `--proxy` — Force proxy mode
- `--name <string>` — Full legal name (Travel Rule compliance)
- `--dob <string>` — Date of birth YYYY-MM-DD (Travel Rule compliance)
- `--pob-country <string>` — Place of birth country code, e.g. `US` (ISO 3166-1 alpha-2)
- `--pob-address <string>` — Place of birth city/state, e.g. `'New York, NY'`

Travel Rule data can also be set via environment variables:
```bash
export WC_PAY_NAME="John Doe"
export WC_PAY_DOB="1990-01-15"
export WC_PAY_POB_COUNTRY="US"
export WC_PAY_POB_ADDRESS="New York, NY"
```

## Default workflow

### Check a payment
1. Run `walletconnect-pay status <paymentId>`
2. Display the result to the user

### Create and pay (end-to-end)
1. Create a payment: `walletconnect-pay create 100 --staging`
2. Note the payment ID from the output
3. Checkout: `walletconnect-pay checkout <paymentId> --staging --name "..." --dob "..." --pob-country "..." --pob-address "..."`
4. Inform the user to approve the signing request in their wallet app
5. Wait for confirmation (the CLI polls automatically)

## Important notes

- **Experimental**: This CLI is under active development and may change significantly
- **Proxy mode**: When no `WC_PAY_WALLET_API_KEY` is set, the CLI automatically routes through the frontend proxy — no API keys needed
- **Travel Rule compliance**: Some payments require Information Capture (IC) data. The CLI will error with a clear message if `--name`, `--dob`, `--pob-country`, and `--pob-address` are missing when required
- **Wallet signing**: The `checkout` command requires user interaction to approve signing requests in their wallet app. Use 60s+ timeouts
- **Staging vs production**: Use `--staging` for testing. Production is the default
- **Amount format**: The `create` command expects amounts in minor units (cents). `1000` = $10.00

## Validation checklist

- [ ] Binary is built and linked (`walletconnect-pay --help` works)
- [ ] For direct API mode, environment variables are set
- [ ] For checkout, a CWP wallet is installed and connected
- [ ] Travel Rule data is provided when required (via flags or env vars)
- [ ] Command output is shown to the user
- [ ] Timeouts are 60s+ for wallet interaction commands

## Examples

### Check payment status
```
User: "What's the status of payment pay_abc123?"
Action: Run `walletconnect-pay status pay_abc123 --staging`
```

### Create a $5 payment
```
User: "Create a $5 test payment"
Action: Run `walletconnect-pay create 500 --staging`
Note: 500 = $5.00 in minor units (cents)
```

### Complete a payment
```
User: "Pay the payment pay_abc123"
Action: Run `walletconnect-pay checkout pay_abc123 --staging --name "John Doe" --dob "1990-01-15" --pob-country "US" --pob-address "New York, NY"`
Note: Inform user to approve the signing request in their wallet app. Use 60s+ timeout.
```
