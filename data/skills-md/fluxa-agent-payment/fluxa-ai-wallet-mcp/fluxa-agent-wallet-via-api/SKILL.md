---
name: fluxa-agent-wallet-via-api
description: >-
  FluxA Agent Wallet integration via REST API. Enables agents to make x402 payments
  for paid APIs, send USDC payouts to any wallet, and create payment links to receive
  payments. Use when the user asks about crypto payments, x402, USDC transfers,
  payment links, or interacting with the FluxA Agent Wallet via direct API calls.
---

# FluxA Agent Wallet (via API)

FluxA Agent Wallet lets AI agents perform onchain financial operations — payments, payouts, and payment links — without managing private keys. All signing is handled server-side by FluxA Wallet; agents only need an Agent JWT to authenticate API calls.

## Capabilities

| Capability | What it does | When to use |
|------------|-------------|-------------|
| **x402 Payment (v3)** | Pay for APIs using the x402 protocol with intent mandates | Agent hits HTTP 402, needs to pay for API access |
| **Payout** | Send USDC to any wallet address | Agent needs to transfer funds to a recipient |
| **Payment Link** | Create shareable URLs to receive payments | Agent needs to charge users, create invoices, sell content |

## Prerequisites

Every API call requires an **Agent JWT** obtained by registering an Agent ID.

### Register Agent ID

```bash
curl -X POST https://agentid.fluxapay.xyz/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "agent@example.com",
    "agent_name": "My AI Agent",
    "client_info": "Agent v1.0"
  }'
```

Response returns `agent_id`, `token`, and `jwt`. Use the `jwt` as `Authorization: Bearer <jwt>` for all subsequent calls.

**Refresh JWT** when expired (via CLI):

```bash
fluxa-wallet refreshJWT
```

Or via API:

```bash
curl -X POST https://agentid.fluxapay.xyz/refresh \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "<AGENT_ID>", "token": "<TOKEN>"}'
```

## Quick Decision Guide

- Need to **pay for an API** that returned HTTP 402? → See [X402-PAYMENT.md](X402-PAYMENT.md)
- Need to **send funds** to a wallet address? → See [PAYOUT.md](PAYOUT.md)
- Need to **receive payments** via a shareable link? → See [PAYMENT-LINK.md](PAYMENT-LINK.md)

## Base URLs

| Service | URL |
|---------|-----|
| Agent ID API | `https://agentid.fluxapay.xyz` |
| Wallet API | `https://walletapi.fluxapay.xyz` |

## Common Patterns

### Authentication Header

All Wallet API calls require:

```
Authorization: Bearer <AGENT_JWT>
Content-Type: application/json
```

### Supported Currencies

| Currency | Value | Description |
|----------|-------|-------------|
| `USDC` | `USDC` | USD Coin |
| `XRP` | `XRP` | XRP |
| `FLUXA_MONETIZE_CREDITS` | `FLUXA_MONETIZE_CREDITS` | Credits for FluxA Monetize, used to consume FluxA Monetize resources |

### Amount Format

All amounts are in **smallest units** (atomic units). For USDC (6 decimals):

| Human-readable | Atomic units |
|---------------|-------------|
| 0.01 USDC | `10000` |
| 0.10 USDC | `100000` |
| 1.00 USDC | `1000000` |
| 10.00 USDC | `10000000` |

### Default Asset

- **Network:** Base (chain ID 8453)
- **Currency:** USDC
- **Asset address:** `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
