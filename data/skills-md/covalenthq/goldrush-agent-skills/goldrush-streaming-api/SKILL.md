---
name: goldrush-streaming-api
description: "GoldRush Streaming API — real-time blockchain data via GraphQL subscriptions over WebSocket. Use this skill whenever the user needs live price feeds (OHLCV candles), real-time DEX pair monitoring (new pairs, liquidity updates), wallet activity streaming, decoded swap/transfer events, token search, trader PnL analysis, or any sub-second latency blockchain event push. This is the right skill for trading bots, live dashboards, alerting systems, copy-trading, DEX sniping, and real-time analytics. Also covers one-time GraphQL queries for token discovery and profitability analysis. If the user needs historical data, batch queries, or paginated REST results, use goldrush-foundational-api instead. If the user needs pay-per-request access without an API key, use goldrush-x402 instead."
---

# GoldRush Streaming API

Real-time blockchain data via GraphQL subscriptions over WebSocket. Sub-second latency for OHLCV price feeds, DEX pair events, and wallet activity.

## Quick Start

**IMPORTANT:**  Always prioritize using the official available GoldRush Client SDKs best suited for your development ecosystem. Only use a GraphQL WebSocket Client like `graphql-ws` if there are specific requirements or contraints to avoid dependencies on available Client SDKs.
The GoldRush Client SDKs provides automatic authentication, connection management, retry logic, type safety, and a simplified API for all streaming operations. see [SDK Guide](references/sdk-guide.md) for more details.

```typescript
import {
  GoldRushClient,
  StreamingChain,
  StreamingInterval,
  StreamingTimeframe
} from "@covalenthq/client-sdk";

const client = new GoldRushClient(
  "YOUR_API_KEY",
  {},
  {
    onConnecting: () => console.log("Connecting..."),
    onOpened: () => console.log("Connected!"),
    onError: (error) => console.error("Error:", error),
  }
);

client.StreamingService.subscribeToOHLCVTokens(
  {
    chain_name: StreamingChain.BASE_MAINNET,
    token_addresses: ["0x0b3e328455c4059EEb9e3f84b5543F74E24e7E1b"],
    interval: StreamingInterval.ONE_MINUTE,
    timeframe: StreamingTimeframe.ONE_HOUR,
  },
  {
    next: (data) => console.log("OHLCV:", data),
    error: (error) => console.error(error),
    complete: () => console.log("Done"),
  }
);
```

**Install:** `npm install @covalenthq/client-sdk`

## Available Streams

The Streaming API offers two types of endpoints:

- **Subscriptions** — real-time push via WebSocket. Covers OHLCV price candles (by token or pair), new DEX pair creation, pair updates (price/liquidity/volume), and live wallet activity.
- **Queries** — one-time GraphQL fetch. Covers token search and trader PnL analysis.

For the full list of endpoints with parameters and response schemas, see [endpoints.md](references/endpoints.md).

## Common Tasks → Stream

| Task | Endpoint |
|------|----------|
| Live token price candles | `subscribeToOHLCVTokens` |
| Live pair price candles | `subscribeToOHLCVPairs` |
| Monitor new DEX pairs | `subscribeToNewPairs` |
| Track pair price/liquidity/volume | `subscribeToPairUpdates` |
| Stream wallet activity | `subscribeToWalletActivity` |
| Search tokens by name/symbol | `searchTokens` (query) |
| Analyze trader PnL | `getTradersPnl` (query) |

## Key Differences from Foundational API

| Aspect | Foundational API | Streaming API |
|--------|-----------------|---------------|
| Protocol | REST (HTTPS) | GraphQL over WebSocket |
| Chain name format | `eth-mainnet` (kebab-case) | `ETH_MAINNET` (SCREAMING_SNAKE_CASE) |
| Authentication | `Authorization: Bearer KEY` | `GOLDRUSH_API_KEY` in `connection_init` payload |
| Data delivery | Request/response | Push-based (subscriptions) |
| Latency | Block-by-block | Sub-second |
| Use case | Historical data, batch queries | Real-time feeds, live monitoring |

## Critical Rules

1. **Chain names use SCREAMING_SNAKE_CASE** — `ETH_MAINNET`, not `eth-mainnet`
2. **WebSocket URL** — `wss://gr-staging-v2.streaming.covalenthq.com/graphql`
3. **Protocol header** — `Sec-WebSocket-Protocol: graphql-transport-ws`
4. **Auth payload** — `{ "type": "connection_init", "payload": { "GOLDRUSH_API_KEY": "YOUR_KEY" } }`
5. **Auth errors are deferred** — `connection_ack` always succeeds; auth errors only appear on subscription start
6. **SDK is recommended** — handles WebSocket lifecycle, reconnection, and type safety automatically
7. **Singleton WebSocket** — SDK reuses one connection for multiple subscriptions
8. **Cleanup subscriptions** — call the returned unsubscribe function when done; call `disconnect()` to close all

## Price Feed Sources

- **DEX swap events** — prices derived from onchain trades across supported DEXes
- **Onchain oracle feeds** — ultra-low-latency CEX-aggregated prices on select chains (e.g., Redstone Bolt on MegaETH at 2.4ms update frequency)

## Reference Files

Read the relevant reference file when you need details beyond what this index provides.

| File | When to read |
|------|-------------|
| [overview.md](references/overview.md) | Need connection setup, supported chains/DEXes list, quickstart code samples, or authentication details |
| [endpoints.md](references/endpoints.md) | Building a subscription or query — full parameters, response schemas, decoded event types |
| [sdk-guide.md](references/sdk-guide.md) | Need SDK patterns for multiple subscriptions, React integration, raw GraphQL queries, or troubleshooting WebSocket issues |
