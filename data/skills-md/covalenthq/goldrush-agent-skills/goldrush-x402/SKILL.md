---
name: goldrush-x402
description: "GoldRush x402 — pay-per-request blockchain data access using the x402 protocol (HTTP 402 Payment Required). Use this skill whenever the user is building an AI agent that needs blockchain data without API keys, wants wallet-based micropayments for on-chain data, needs autonomous or no-account access to the GoldRush API, mentions the x402 protocol, or wants no-signup/no-onboarding blockchain data access. This is the right skill for autonomous agents, serverless applications, and prototyping without onboarding. Provides access to 60+ Foundational API endpoints through a transparent reverse proxy with stablecoin payments on Base. If the user needs a traditional API key with monthly billing, use goldrush-foundational-api instead. If the user needs real-time streaming data via WebSocket, use goldrush-streaming-api instead."
---

# GoldRush x402

Pay-per-request access to GoldRush blockchain data using the x402 protocol. No API key, no signup, no billing — just a funded wallet. Provides access to Foundational API endpoints through a transparent reverse proxy.

## Quick Start

```typescript
import { HTTPClient } from "@x402/core";
import { ExactEvmScheme } from "@x402/evm";

const client = new HTTPClient({
  scheme: new ExactEvmScheme({
    network: "eip155:84532", // Base Sepolia
    privateKey: process.env.WALLET_PRIVATE_KEY,
  }),
});

// Get token balances — payment handled automatically
const balances = await client.get(
  "https://x402.goldrush.dev/v1/eth-mainnet/address/demo.eth/balances_v2/"
);
console.log(balances);
```

**Install:** `npm install @x402/core @x402/evm`

## How x402 Works

```
1. REQUEST  → Agent calls endpoint without payment
2. 402      → Server responds with payment instructions (amount, token, recipient)
3. PAY      → Agent signs payment with stablecoins on Base, retries with proof
4. DATA     → Server validates request *before* charging, returns data
```

The x402 client libraries handle steps 2-3 automatically. From your code, it's just a GET request.

**Key safety feature:** The proxy validates your request before charging. Malformed addresses, unsupported chains, or bad parameters get a clear error — you pay nothing.

**Payment:** USDC on Base Sepolia (testnet). Base mainnet support coming soon.

## Cross-Reference

x402 serves the **same endpoints** as the Foundational API with the same parameters and response format. For detailed endpoint documentation (parameters, response schemas, use cases), see the **goldrush-foundational-api** skill.

**Base URL mapping:**
- Foundational API: `https://api.covalenthq.com/v1/...`
- x402 proxy: `https://x402.goldrush.dev/v1/...`

## Pricing Summary

| Model | Description | Example |
|-------|-------------|---------|
| **Fixed** | One price per call | Token balances, NFT holdings, block details |
| **Tiered** | Price by data volume | Transactions, event logs |

### Tiers (for variable-length data)

| Tier | Items | Use Case |
|------|-------|----------|
| Small | 1-50 | Quick lookups, recent activity |
| Medium | 51-200 | Standard queries |
| Large | 201-500 | Detailed analysis |
| XL | 501+ | Full history |

Select tier via query parameter: `?tier=small`

### Response Caching

Cached responses cost less. Cache TTLs:
- **Balances:** 30 seconds
- **Pricing data:** 5 minutes

## AI Agent Workflow

### 1. Discover (free)
```bash
curl https://x402.goldrush.dev/v1/x402/endpoints | jq
curl https://x402.goldrush.dev/v1/x402/search?q=balance | jq
```

### 2. Evaluate
```bash
curl https://x402.goldrush.dev/v1/x402/endpoints/get-token-balances-for-address | jq
```
Returns credit rate, pricing model, supported chains — everything to decide what to call.

### 3. Pay & consume
```typescript
const balances = await client.get(
  `https://x402.goldrush.dev/v1/eth-mainnet/address/${wallet}/balances_v2/`
);
// Same JSON format as standard GoldRush API
```

## Reference Files

Read the relevant reference file when you need details beyond what this index provides.

| File | When to read |
|------|-------------|
| [overview.md](references/overview.md) | Need x402 protocol details, pricing model breakdown, or quickstart code |
| [ai-agents.md](references/ai-agents.md) | Building an autonomous agent — four-step workflow, x402 vs API key comparison, rate limits |
| [endpoints.md](references/endpoints.md) | Need the discovery API details (free), or the catalog of available data endpoints |
