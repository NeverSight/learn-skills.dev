---
name: cmc-x402
description: |
  Access CoinMarketCap data via x402 pay-per-request protocol with USDC payments on Base.
  Use when users mention x402, want CMC data without API keys, ask about pay-per-request APIs, or need to integrate CMC with on-chain payments. Also use for any Coinbase x402 protocol questions.
  Trigger: "x402", "pay per request", "no API key", "USDC payment", "CMC without subscription", "/cmc-x402"
user-invocable: true
---

# CoinMarketCap x402

Pay-per-request crypto market data powered by the x402 protocol. Access CoinMarketCap endpoints instantly with on-chain USDC payment. No API key or subscription required.

## What is x402?

x402 is an open payment protocol developed by Coinbase that enables automatic stablecoin payments over HTTP. Instead of managing API keys, you pay $0.01 USDC per request on Base. The x402 client library handles payment signing automatically.

Learn more: https://docs.x402.org

## Prerequisites

Before using x402 endpoints, ensure you have:

1. **Node.js 18+** and npm installed
2. **Base network wallet** with a private key you control
3. **USDC on Base** to pay for requests ($0.01 per request)
4. **Small amount of ETH on Base** for gas fees

## Use Cases

**Get current prices for specific coins:**
Use `/x402/v3/cryptocurrency/quotes/latest` with symbol or id parameter.
Example: Get BTC and ETH prices for a portfolio tracker.

**List top cryptocurrencies:**
Use `/x402/v3/cryptocurrency/listing/latest` with limit parameter.
Example: Display top 100 coins ranked by market cap.

**Search for DEX tokens:**
Use `/x402/v1/dex/search` with keyword parameter.
Example: Find a memecoin by name when you don't know the contract address.

**Get DEX pair trading data:**
Use `/x402/v4/dex/pairs/quotes/latest` with pair address.
Example: Monitor liquidity and volume for a specific Uniswap pool.

**AI agent data access:**
Use the MCP endpoint at `https://mcp.coinmarketcap.com/x402/mcp`.
Example: Let Claude or other LLMs fetch live crypto data with automatic payment.

## Quick Start

Install the x402 TypeScript SDK:

```bash
npm install @x402/axios @x402/evm viem
```

Fetch data with automatic payment:

```typescript
import { createX402AxiosClient } from "@x402/axios";
import { ExactEvmScheme, toClientEvmSigner } from "@x402/evm";
import { privateKeyToAccount } from "viem/accounts";
import { createPublicClient, http } from "viem";
import { base } from "viem/chains";

// SECURITY: Never hardcode private keys in source code.
// Use environment variables: process.env.PRIVATE_KEY
// For production, use a dedicated hot wallet with limited funds.
const account = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`);
const publicClient = createPublicClient({ chain: base, transport: http() });
const signer = toClientEvmSigner(account, publicClient);

const client = createX402AxiosClient({
  schemes: [new ExactEvmScheme(signer)],
});

const response = await client.get(
  "https://pro.coinmarketcap.com/x402/v3/cryptocurrency/quotes/latest",
  { params: { symbol: "BTC,ETH" } }
);

console.log(response.data);
```

## Endpoints

Base URL: `https://pro.coinmarketcap.com`

| Endpoint | Path | Use For |
|----------|------|---------|
| Quotes | `/x402/v3/cryptocurrency/quotes/latest` | Current prices for specific coins |
| Listings | `/x402/v3/cryptocurrency/listing/latest` | Top coins by market cap |
| DEX Search | `/x402/v1/dex/search` | Find DEX tokens by keyword |
| DEX Pairs | `/x402/v4/dex/pairs/quotes/latest` | DEX pair trading data |

All parameters from the standard CMC Pro API work with x402 endpoints. See [endpoints.md](references/endpoints.md) for full parameter reference.

## MCP for AI Agents

The x402 MCP endpoint lets AI agents access CMC data with automatic payment.

**Connection URL:**
```
https://mcp.coinmarketcap.com/x402/mcp
```

**Transport:** Streamable HTTP (POST)

Connect using any MCP client with an x402-aware HTTP transport. The server exposes the same tools as the REST endpoints and supports automatic tool discovery.

## Pricing

$0.01 USDC per request on Base (Chain ID: 8453).

Payment only occurs on successful data delivery. If the request fails, no payment is deducted.

## References

- [endpoints.md](references/endpoints.md) - Full parameter reference for all endpoints
- [payment-details.md](references/payment-details.md) - 402 response format, contract addresses, manual integration

## Resources

- x402 Protocol: https://x402.org
- x402 Documentation: https://docs.x402.org
- x402 GitHub: https://github.com/coinbase/x402
- CMC API Documentation: https://coinmarketcap.com/api/documentation
