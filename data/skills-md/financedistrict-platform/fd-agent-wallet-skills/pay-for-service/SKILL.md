---
name: pay-for-service
description: Access paid API endpoints and content using the x402 payment protocol. Use when you or the user want to call a paid API, access gated content, make an x402 payment, use a paid service, or retrieve content that requires payment. Covers "fetch this paid resource", "access x402 content", "pay for this API call".
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(fdx status*)", "Bash(fdx call getX402Content*)", "Bash(fdx call authorizePayment*)", "Bash(fdx call getWalletOverview*)"]
---

# Paying for Services (x402)

Use the Finance District wallet to access paid API endpoints and gated content via the x402 HTTP payment protocol. The wallet handles payment authorization and signing automatically — the agent fetches the content in a single call.

## How x402 Works

x402 is an HTTP-native payment protocol:

1. A server returns HTTP 402 with payment requirements
2. The wallet signs a payment and retries the request with a payment header
3. The facilitator verifies and settles the payment
4. The server returns the content

The Finance District wallet supports x402 payments on multiple chains and assets, not just a single network.

## Confirm wallet is authenticated

```bash
fdx status
```

If the wallet is not authenticated, refer to the `authenticate` skill.

## Check Balance

Ensure the wallet has sufficient funds to cover the payment:

```bash
fdx call getWalletOverview
```

## Fetching Paid Content

### getX402Content — Fetch content from a paid endpoint

The primary command for accessing x402 resources. It discovers payment requirements, authorizes payment, and retrieves the content in one step:

```bash
fdx call getX402Content --url <endpoint-url>
```

#### Parameters

| Parameter                | Required | Description                                           |
| ------------------------ | -------- | ----------------------------------------------------- |
| `--url`                  | Yes      | The x402-enabled endpoint URL                         |
| `--preferredNetwork`     | No       | Preferred chain ID for payment (e.g. `8453` for Base) |
| `--preferredNetworkName` | No       | Preferred chain name (e.g. `base`, `ethereum`)        |
| `--preferredAsset`       | No       | Preferred payment asset (e.g. `USDC`)                 |
| `--maxPaymentAmount`     | No       | Maximum payment amount to authorize                   |

### authorizePayment — Pre-authorize a payment

For cases where you want to inspect payment requirements or authorize without fetching:

```bash
fdx call authorizePayment --url <endpoint-url>
```

#### Parameters

Same as `getX402Content`.

## Examples

```bash
# Fetch content from a paid API (auto-discovers requirements and pays)
fdx call getX402Content \
  --url https://api.example.com/premium/data

# Prefer paying with USDC on Base
fdx call getX402Content \
  --url https://api.example.com/premium/data \
  --preferredNetworkName base \
  --preferredAsset USDC

# Set a max payment cap
fdx call getX402Content \
  --url https://api.example.com/premium/data \
  --maxPaymentAmount 1000000

# Just authorize without fetching
fdx call authorizePayment \
  --url https://api.example.com/premium/data
```

## Flow

1. Check authentication with `fdx status`
2. Check wallet balance with `fdx call getWalletOverview`
3. Call `fdx call getX402Content --url <endpoint>` to fetch paid content
4. If the payment amount seems high, use `fdx call authorizePayment` first to inspect, then confirm with the human before proceeding
5. Return the fetched content to the human

**Important:** Always inform your human about the payment before executing, especially for unfamiliar endpoints or amounts that seem high. Let them confirm they want to proceed.

## Difference from Coinbase x402

The Finance District wallet supports **multi-chain and multi-asset** x402 payments. You can specify a preferred network and asset, giving flexibility to pay from whichever chain and token has available balance. Coinbase's implementation is limited to Base USDC.

## Prerequisites

- Must be authenticated (`fdx status` to check, see `authenticate` skill)
- Wallet must have sufficient balance in the required payment asset on the required network
- If insufficient funds, suggest using the `fund-wallet` skill or `swap-tokens` skill

## Error Handling

- "Not authenticated" — Run `fdx setup` first, or see `authenticate` skill
- "Insufficient balance" — Check balance; see `fund-wallet` skill
- "No x402 payment requirements found" — The URL may not be an x402-enabled endpoint
- "Payment failed" — May be a network issue; retry or try a different preferred network
