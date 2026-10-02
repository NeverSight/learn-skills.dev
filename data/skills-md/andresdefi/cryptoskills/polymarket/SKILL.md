---
name: polymarket
description: "Polymarket CLOB prediction market integration — authentication (L1/L2 HMAC signing), order placement (limit, market, GTC, GTD, FOK), orderbook reading, market data (Gamma API), WebSocket subscriptions, CTF conditional token operations (split, merge, redeem), gasless trading via relayer, and builder program attribution."
license: Apache-2.0
metadata:
  author: 0xinit
  version: "1.0"
  chain: polygon
  category: Trading
tags:
  - polymarket
  - prediction-markets
  - clob
  - conditional-tokens
  - orderbook
  - polygon
  - trading
---

# Polymarket

Polymarket is a prediction market protocol running on Polygon. It operates a Central Limit Order Book (CLOB) where users trade binary outcome tokens priced between $0 and $1. Each market has Yes and No tokens backed by USDC through the Conditional Token Framework (CTF). The CLOB uses off-chain matching with on-chain settlement via Polygon. Authentication is two-layered: L1 (EIP-712 wallet signing) to derive API credentials, L2 (HMAC-SHA256) to authenticate trading requests.

Base URLs:
- **CLOB API**: `https://clob.polymarket.com`
- **Gamma API** (market data): `https://gamma-api.polymarket.com`
- **Data API** (trades/positions): `https://data-api.polymarket.com`
- **WebSocket (Market)**: `wss://ws-subscriptions-clob.polymarket.com/ws/market`
- **WebSocket (User)**: `wss://ws-subscriptions-clob.polymarket.com/ws/user`
- **Relayer** (gasless): `https://relayer-v2.polymarket.com/`

## What You Probably Got Wrong

> LLMs have stale training data. These are the most common mistakes.

- **"Polymarket uses standard API keys"** -- Polymarket has two-level auth. You first sign an EIP-712 message with your private key (L1) to create HMAC credentials, then use those credentials (L2) to sign every trading request. You cannot skip L1 or use the credentials without HMAC signing.
- **"I can trade with just a private key"** -- You also need a **funder address** (your Polygon proxy wallet) and must select the correct **signature type** (0=EOA, 1=POLY_PROXY, 2=GNOSIS_SAFE). Most new integrations use type `2`. Without the correct funder + sig type combo, orders silently fail.
- **"Prices are in dollars"** -- Prices are probabilities between 0 and 1. A Yes token at 0.65 means the market implies 65% probability. Buying at 0.65 pays $1.00 if the event occurs, netting $0.35 profit per share.
- **"I can use any price increment"** -- Each market has a tick size (0.1, 0.01, 0.001, or 0.0001). Orders with prices that do not conform to the tick size are rejected with `INVALID_ORDER_MIN_TICK_SIZE`. Always query the tick size before placing orders.
- **"FOK amount is share count"** -- For FOK/FAK BUY orders, `amount` is the **dollar amount to spend**, not shares. For SELL orders, `amount` is shares. Getting this wrong causes unexpected fill sizes.
- **"WebSocket stays connected automatically"** -- You must send `PING` every 10 seconds. Without heartbeats, the connection drops silently after ~10 seconds.
- **"Neg risk markets work like standard markets"** -- Multi-outcome events use a different exchange contract (`0xC5d563A36AE78145C45a50134d48A1215220f80a`) and require `negRisk: true` in order options. Using the standard exchange contract for neg risk markets causes transaction reverts.
- **"I can use ethers v6"** -- The `@polymarket/clob-client` SDK requires ethers v5 (`Wallet` from `ethers`). Ethers v6 changed the Signer interface and is not compatible.

## API Configuration

| API | Base URL | Auth | Purpose |
|-----|----------|------|---------|
| CLOB | `https://clob.polymarket.com` | L2 for trades, none for reads | Orderbook, prices, order submission |
| Gamma | `https://gamma-api.polymarket.com` | None | Events, markets, search |
| Data | `https://data-api.polymarket.com` | None | Trades, positions, user data |
| WS Market | `wss://ws-subscriptions-clob.polymarket.com/ws/market` | None | Real-time orderbook |
| WS User | `wss://ws-subscriptions-clob.polymarket.com/ws/user` | API creds in message | Trade/order updates |
| Relayer | `https://relayer-v2.polymarket.com/` | Builder headers | Gasless transactions |

## Contract Addresses (Polygon)

| Contract | Address | Last verified March 2026 |
|----------|---------|--------------------------|
| USDC (USDC.e) | `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174` | Bridged USDC collateral |
| CTF (Conditional Tokens) | `0x4D97DCd97eC945f40cF65F87097ACe5EA0476045` | Token storage and operations |
| CTF Exchange | `0x4bFb41d5B3570DeFd03C39a9A4D8dE6Bd8B8982E` | Standard market trading |
| Neg Risk CTF Exchange | `0xC5d563A36AE78145C45a50134d48A1215220f80a` | Multi-outcome market trading |
| Neg Risk Adapter | `0xd91E80cF2E7be2e162c6513ceD06f1dD0dA35296` | Neg risk conversions |

## Authentication

Polymarket uses two-level auth: **L1** (EIP-712 signing) to create credentials, **L2** (HMAC-SHA256) to authenticate requests.

### L1: Derive API Credentials

L1 proves wallet ownership via EIP-712 signature. Used once to create or derive API credentials.

```typescript
import { ClobClient } from "@polymarket/clob-client";
import { Wallet } from "ethers";

const HOST = "https://clob.polymarket.com";
const CHAIN_ID = 137;
const signer = new Wallet(process.env.PRIVATE_KEY!);

const tempClient = new ClobClient(HOST, CHAIN_ID, signer);
const apiCreds = await tempClient.createOrDeriveApiKey();
// { apiKey: "uuid", secret: "base64...", passphrase: "string" }
```

The EIP-712 domain used under the hood:

```typescript
const domain = {
  name: "ClobAuthDomain",
  version: "1",
  chainId: 137,
};

const types = {
  ClobAuth: [
    { name: "address", type: "address" },
    { name: "timestamp", type: "string" },
    { name: "nonce", type: "uint256" },
    { name: "message", type: "string" },
  ],
};
```

### L2: Initialize Trading Client

L2 uses HMAC-SHA256 signatures from the derived credentials. Required for all trade endpoints.

```typescript
import { ClobClient, Side, OrderType } from "@polymarket/clob-client";
import { Wallet } from "ethers";

const signer = new Wallet(process.env.PRIVATE_KEY!);

const client = new ClobClient(
  "https://clob.polymarket.com",
  137,
  signer,
  apiCreds,
  2,                                    // signatureType: 0=EOA, 1=POLY_PROXY, 2=GNOSIS_SAFE
  process.env.POLYMARKET_FUNDER_ADDRESS! // proxy wallet from polymarket.com/settings
);
```

### Signature Types

| Type | Value | When to Use |
|------|-------|-------------|
| EOA | `0` | Standard wallet. Funder = wallet address. Needs POL for gas. |
| POLY_PROXY | `1` | Magic Link proxy. User exported PK from Polymarket.com. |
| GNOSIS_SAFE | `2` | Most common for new integrations. Gnosis Safe multisig proxy. |

### L2 Headers (sent automatically by SDK)

| Header | Description |
|--------|-------------|
| `POLY_ADDRESS` | Polygon signer address |
| `POLY_SIGNATURE` | HMAC-SHA256 signature of request |
| `POLY_TIMESTAMP` | Current UNIX timestamp |
| `POLY_API_KEY` | API key from credential creation |
| `POLY_PASSPHRASE` | Passphrase from credential creation |

## Order Placement

All orders are limit orders. Market orders are limit orders with a marketable price that execute immediately.

### Order Types

| Type | Behavior | Use Case |
|------|----------|----------|
| **GTC** | Good-Til-Cancelled. Rests on book until filled or cancelled. | Default limit orders |
| **GTD** | Good-Til-Date. Active until expiration (UTC seconds). Min = `now + 60 + N`. | Auto-expire before events |
| **FOK** | Fill-Or-Kill. Fill entirely immediately or cancel. | All-or-nothing market orders |
| **FAK** | Fill-And-Kill. Fill what is available, cancel rest. | Partial-fill market orders |

### Limit Order (GTC)

```typescript
const response = await client.createAndPostOrder(
  {
    tokenID: "TOKEN_ID",
    price: 0.50,
    size: 10,
    side: Side.BUY,
  },
  {
    tickSize: "0.01",
    negRisk: false,
  },
  OrderType.GTC
);
console.log(response.orderID, response.status);
```

### Two-Step Pattern (Sign Then Submit)

```typescript
const signedOrder = await client.createOrder(
  { tokenID: "TOKEN_ID", price: 0.50, size: 10, side: Side.BUY },
  { tickSize: "0.01", negRisk: false }
);
const response = await client.postOrder(signedOrder, OrderType.GTC);
```

### Market Order (FOK)

```typescript
// BUY: amount = dollar amount to spend. SELL: amount = shares to sell.
const response = await client.createAndPostMarketOrder(
  { tokenID: "TOKEN_ID", side: Side.BUY, amount: 100, price: 0.55 },
  { tickSize: "0.01", negRisk: false },
  OrderType.FOK
);
```

### GTD Order (Expiring)

```typescript
// Expire in 1 hour. Security threshold: add 60 seconds minimum.
const expiration = Math.floor(Date.now() / 1000) + 60 + 3600;

const response = await client.createAndPostOrder(
  { tokenID: "TOKEN_ID", price: 0.50, size: 10, side: Side.BUY, expiration },
  { tickSize: "0.01", negRisk: false },
  OrderType.GTD
);
```

### Post-Only Orders

Guarantee maker status. Rejected if the order would cross the spread.

```typescript
const response = await client.postOrder(signedOrder, OrderType.GTC, true);
```

Post-only works with GTC and GTD only. Rejected if combined with FOK or FAK.

### Batch Orders (up to 15)

```typescript
import { PostOrdersArgs } from "@polymarket/clob-client";

const orders: PostOrdersArgs[] = [
  {
    order: await client.createOrder(
      { tokenID: "TOKEN_ID", price: 0.48, side: Side.BUY, size: 500 },
      { tickSize: "0.01", negRisk: false }
    ),
    orderType: OrderType.GTC,
  },
  {
    order: await client.createOrder(
      { tokenID: "TOKEN_ID", price: 0.52, side: Side.SELL, size: 500 },
      { tickSize: "0.01", negRisk: false }
    ),
    orderType: OrderType.GTC,
  },
];
const response = await client.postOrders(orders);
```

### Cancel Orders

```typescript
await client.cancelOrder("0xORDER_ID");
await client.cancelOrders(["0xID_1", "0xID_2"]);
await client.cancelAll();
await client.cancelMarketOrders({ market: "0xCONDITION_ID" });
await client.cancelMarketOrders({
  market: "0xCONDITION_ID",
  asset_id: "TOKEN_ID",
});
```

### Heartbeat (Dead Man's Switch)

If heartbeat not received within 10 seconds (5s buffer), all open orders are cancelled.

```typescript
let heartbeatId = "";
setInterval(async () => {
  const resp = await client.postHeartbeat(heartbeatId);
  heartbeatId = resp.heartbeat_id;
}, 5000);
```

## Orderbook and Market Data

### Read Orderbook (No Auth)

```typescript
const readClient = new ClobClient("https://clob.polymarket.com", 137);
const book = await readClient.getOrderBook("TOKEN_ID");
console.log("Best bid:", book.bids[0], "Best ask:", book.asks[0]);

const mid = await readClient.getMidpoint("TOKEN_ID");
const spread = await readClient.getSpread("TOKEN_ID");
const lastPrice = await readClient.getLastTradePrice("TOKEN_ID");
```

### Price History

```typescript
import { PriceHistoryInterval } from "@polymarket/clob-client";

const history = await readClient.getPricesHistory({
  market: "TOKEN_ID",
  interval: PriceHistoryInterval.ONE_DAY,
  fidelity: 60,
});
// Each entry: { t: timestamp, p: price }
```

### Gamma API (Events and Markets)

```bash
# Active events sorted by volume
curl "https://gamma-api.polymarket.com/events?active=true&closed=false&sort=volume_24hr&ascending=false&limit=100"

# Event by slug
curl "https://gamma-api.polymarket.com/events?slug=fed-decision-in-october"

# Events by tag
curl "https://gamma-api.polymarket.com/events?tag_id=100381&limit=10&active=true&closed=false"

# Discover tags
curl "https://gamma-api.polymarket.com/tags/ranked"
```

### Batch Orderbook Queries

All orderbook queries have batch variants (up to 500 tokens):

```typescript
const prices = await readClient.getPrices([
  { token_id: "TOKEN_A", side: Side.BUY },
  { token_id: "TOKEN_B", side: Side.BUY },
]);
```

| Single | Batch | REST |
|--------|-------|------|
| `getOrderBook()` | `getOrderBooks()` | `POST /books` |
| `getPrice()` | `getPrices()` | `POST /prices` |
| `getMidpoint()` | `getMidpoints()` | `POST /midpoints` |
| `getSpread()` | `getSpreads()` | `POST /spreads` |

## WebSocket Subscriptions

### Market Channel (Public)

```typescript
const ws = new WebSocket("wss://ws-subscriptions-clob.polymarket.com/ws/market");

ws.onopen = () => {
  ws.send(JSON.stringify({
    type: "market",
    assets_ids: ["TOKEN_ID"],
    custom_feature_enabled: true,
  }));
  setInterval(() => ws.send("PING"), 10_000);
};

ws.onmessage = (event) => {
  if (event.data === "PONG") return;
  const msg = JSON.parse(event.data);
  switch (msg.event_type) {
    case "book":
      console.log("Snapshot:", msg.bids.length, "bids", msg.asks.length, "asks");
      break;
    case "price_change":
      for (const pc of msg.price_changes) {
        console.log(`${pc.side} ${pc.size}@${pc.price}`);
      }
      break;
    case "last_trade_price":
      console.log(`Trade: ${msg.side} ${msg.size}@${msg.price}`);
      break;
    case "tick_size_change":
      console.log(`Tick: ${msg.old_tick_size} -> ${msg.new_tick_size}`);
      break;
  }
};
```

Set `custom_feature_enabled: true` to enable `best_bid_ask`, `new_market`, and `market_resolved` events.

### Market Channel Event Types

| Event | Trigger | Key Fields |
|-------|---------|------------|
| `book` | On subscribe + trade affects book | `bids[]`, `asks[]`, `hash`, `timestamp` |
| `price_change` | Order placed or cancelled | `price_changes[]` with `price`, `size`, `side` |
| `last_trade_price` | Trade executed | `price`, `side`, `size`, `fee_rate_bps` |
| `tick_size_change` | Price hits >0.96 or <0.04 | `old_tick_size`, `new_tick_size` |
| `best_bid_ask` | Top-of-book changes | `best_bid`, `best_ask`, `spread` |
| `market_resolved` | Market resolved | `winning_asset_id`, `winning_outcome` |

`tick_size_change` is critical for bots -- if the tick size changes and you use the old one, orders are rejected.

### User Channel (Authenticated)

Subscribes by condition IDs (market IDs), not asset IDs.

```typescript
const ws = new WebSocket("wss://ws-subscriptions-clob.polymarket.com/ws/user");

ws.onopen = () => {
  ws.send(JSON.stringify({
    auth: {
      apiKey: process.env.POLY_API_KEY!,
      secret: process.env.POLY_API_SECRET!,
      passphrase: process.env.POLY_PASSPHRASE!,
    },
    markets: ["0xCONDITION_ID"],
    type: "USER",
  }));
  setInterval(() => ws.send("PING"), 10_000);
};
```

### Dynamic Subscribe/Unsubscribe

```typescript
// Add more assets without reconnecting
ws.send(JSON.stringify({ assets_ids: ["NEW_TOKEN_ID"], operation: "subscribe" }));

// Remove assets
ws.send(JSON.stringify({ assets_ids: ["OLD_TOKEN_ID"], operation: "unsubscribe" }));
```

## CTF Operations (Split, Merge, Redeem)

The Conditional Token Framework creates ERC1155 tokens for market outcomes. Every binary market has Yes and No tokens, each backed by $1.00 USDC.

### Split: USDC into Outcome Tokens

```
$100 USDC -> 100 Yes tokens + 100 No tokens
```

| Parameter | Type | Value |
|-----------|------|-------|
| `collateralToken` | address | `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174` (USDC) |
| `parentCollectionId` | bytes32 | `0x0000...0000` (32 zero bytes) |
| `conditionId` | bytes32 | Market condition ID |
| `partition` | uint[] | `[1, 2]` for binary (Yes=1, No=2) |
| `amount` | uint256 | USDC amount to split |

Prerequisites: USDC balance on Polygon, USDC approval for CTF contract.

### Merge: Outcome Tokens Back to USDC

```
100 Yes tokens + 100 No tokens -> $100 USDC
```

Same parameters as split. Burns one unit of each position per unit of collateral returned. Requires equal amounts of both tokens.

### Redeem: Winning Tokens After Resolution

```
Market resolves YES:
  100 Yes tokens -> $100 USDC
  100 No tokens  -> $0
```

Redemption burns your entire token balance for the condition -- no amount parameter. Winning tokens are always redeemable with no deadline.

### Standard vs Neg Risk Markets

| Feature | Standard | Neg Risk |
|---------|----------|----------|
| Exchange | CTF Exchange | Neg Risk CTF Exchange |
| Multi-outcome | Independent | Linked via conversion |
| `negRisk` flag | `false` | `true` |
| Order option | `negRisk: false` | `negRisk: true` |

### Approval Matrix

| Operation | Contract to Approve | Token |
|-----------|-------------------|-------|
| Buy (standard) | CTF Exchange | USDC |
| Sell (standard) | CTF Exchange | Conditional tokens |
| Buy (neg risk) | Neg Risk CTF Exchange | USDC |
| Sell (neg risk) | Neg Risk CTF Exchange | Conditional tokens |
| Split | CTF | USDC |
| Neg risk conversion | Neg Risk Adapter | Conditional tokens |

## Gasless Trading (Builder Program)

The Relayer Client enables gasless transactions. Polymarket pays gas fees; users only need USDC. Requires Builder Program membership.

```bash
npm install @polymarket/builder-relayer-client @polymarket/builder-signing-sdk
```

```typescript
import { createWalletClient, http, type Hex } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { polygon } from "viem/chains";
import { RelayClient } from "@polymarket/builder-relayer-client";
import { BuilderConfig } from "@polymarket/builder-signing-sdk";

const account = privateKeyToAccount(process.env.PRIVATE_KEY as Hex);
const wallet = createWalletClient({
  account,
  chain: polygon,
  transport: http(process.env.RPC_URL),
});

const builderConfig = new BuilderConfig({
  localBuilderCreds: {
    key: process.env.POLY_BUILDER_API_KEY!,
    secret: process.env.POLY_BUILDER_SECRET!,
    passphrase: process.env.POLY_BUILDER_PASSPHRASE!,
  },
});

const relayClient = new RelayClient(
  "https://relayer-v2.polymarket.com/",
  137,
  wallet,
  builderConfig
);
```

### Gasless Token Approval Example

```typescript
import { encodeFunctionData, maxUint256 } from "viem";

const USDC = "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174";
const CTF = "0x4D97DCd97eC945f40cF65F87097ACe5EA0476045";

const approveTx = {
  to: USDC,
  data: encodeFunctionData({
    abi: [{
      name: "approve", type: "function",
      inputs: [{ name: "spender", type: "address" }, { name: "amount", type: "uint256" }],
      outputs: [{ type: "bool" }],
    }],
    functionName: "approve",
    args: [CTF, maxUint256],
  }),
  value: "0",
};

const response = await relayClient.execute([approveTx], "Approve USDC for CTF");
await response.wait();
```

## Builder Program

Builders receive order attribution and relayer access. Setup:

1. Go to `polymarket.com/settings?tab=builder`
2. Create builder profile and generate API keys
3. Add builder config to your CLOB client

```typescript
import { BuilderConfig, type BuilderApiKeyCreds } from "@polymarket/builder-signing-sdk";

const builderCreds: BuilderApiKeyCreds = {
  key: process.env.POLY_BUILDER_API_KEY!,
  secret: process.env.POLY_BUILDER_SECRET!,
  passphrase: process.env.POLY_BUILDER_PASSPHRASE!,
};

const builderConfig = new BuilderConfig({ localBuilderCreds: builderCreds });

const client = new ClobClient(
  "https://clob.polymarket.com",
  137,
  signer,
  apiCreds,
  2,
  funderAddress,
  undefined,
  false,
  builderConfig
);
// Orders automatically include builder attribution headers
```

### Builder Headers

| Header | Description |
|--------|-------------|
| `POLY_BUILDER_API_KEY` | Builder API key |
| `POLY_BUILDER_TIMESTAMP` | Unix timestamp |
| `POLY_BUILDER_PASSPHRASE` | Builder passphrase |
| `POLY_BUILDER_SIGNATURE` | HMAC-SHA256 of request |

### Remote Signing

Keep builder credentials on a separate server for security:

```typescript
const builderConfig = new BuilderConfig({
  remoteBuilderConfig: { url: "https://your-server.com/sign" },
});
```

Your server receives `{ method, path, body }` and returns the 4 `POLY_BUILDER_*` headers.

## Related Skills

- [gmx](../gmx/SKILL.md) -- GMX perpetual futures on Arbitrum/Avalanche
- [vertex](../vertex/SKILL.md) -- Vertex edge DEX with cross-chain orderbook
- [hyperliquid](../hyperliquid/SKILL.md) -- Hyperliquid perpetual futures on its own L1

## References

- [Polymarket CLOB Docs](https://docs.polymarket.com/)
- [CLOB Client SDK (TypeScript)](https://github.com/Polymarket/clob-client)
- [CLOB Client SDK (Python)](https://github.com/Polymarket/py-clob-client)
- [Builder Relayer Client](https://github.com/Polymarket/builder-relayer-client)
- [Builder Signing SDK](https://github.com/Polymarket/builder-signing-sdk)
- [Gamma API](https://gamma-api.polymarket.com)
- [CTF Contracts (Gnosis)](https://github.com/gnosis/conditional-tokens-contracts)
- [Polymarket App](https://polymarket.com)
