---
name: polymarket-copy-trading-bot
description: TypeScript bot that monitors a Polymarket wallet and mirrors BUY trades to your own account via the Polymarket CLOB API on Polygon.
triggers:
  - set up polymarket copy trading bot
  - mirror polymarket trades automatically
  - copy trade polymarket wallet
  - configure polymarket trading bot
  - polymarket clob order bot typescript
  - automate polymarket buying from target wallet
  - polymarket websocket trade monitor
  - polymarket bot environment setup
---

# Polymarket Copy Trading Bot

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

A TypeScript bot that continuously monitors a target Polymarket wallet, detects trades in real time via REST polling and/or WebSocket, and mirrors BUY orders to your own account using the Polymarket CLOB SDK on Polygon mainnet.

---

## What It Does

- **Monitors** a target wallet via Polymarket Data API (REST polling every ~2s) and optionally WebSocket
- **Mirrors BUY trades only** — SELL trades are detected but skipped by default
- **Sizes copies** using a configurable `POSITION_MULTIPLIER` (default 10%) with min/max caps
- **Submits orders** as FOK, FAK, or LIMIT via the Polymarket CLOB client
- **Enforces risk limits** — per-session and per-market notional caps
- **Supports three auth modes** — EOA (`SIG_TYPE=0`), Poly Proxy (`SIG_TYPE=1`), Poly Polymorphic (`SIG_TYPE=2`)

---

## Installation

```bash
git clone https://github.com/Neron888/Polymarket-copy-trading-bot.git
cd Polymarket-copy-trading-bot
npm install
```

Requires Node.js v18+. The CLOB SDK requires **ethers v5** (already pinned in `package.json`).

---

## Configuration

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Required
TARGET_WALLET=0xTargetWalletAddressToMonitor
WALLET_PRIVATE_KEY=0xYourPrivateKey
RPC_URL=https://your-quicknode-polygon-endpoint.quiknode.pro/your-key/

# Auth mode (0=EOA default, 1=Poly Proxy, 2=Poly Polymorphic)
SIG_TYPE=0
# Required only for SIG_TYPE=1 or 2
PROXY_WALLET_ADDRESS=

# Sizing
POSITION_MULTIPLIER=0.1      # 10% of target's trade size
MAX_TRADE_SIZE=100            # Max USDC per copied trade
MIN_TRADE_SIZE=1              # Min USDC per copied trade

# Order behavior
ORDER_TYPE=FOK                # FOK | FAK | LIMIT
SLIPPAGE_TOLERANCE=0.02       # 2%

# Risk caps (0 = disabled)
MAX_SESSION_NOTIONAL=500      # Total USDC for entire session
MAX_PER_MARKET_NOTIONAL=100   # Per market USDC cap

# Monitoring
USE_WEBSOCKET=true
POLL_INTERVAL=2000            # ms between REST polls
USE_USER_CHANNEL=false        # true = user WS channel, false = market channel

# Optional
POLYMARKET_GEO_TOKEN=
WS_ASSET_IDS=                 # comma-separated asset IDs for market WS
WS_MARKET_IDS=                # comma-separated condition IDs for user channel
MIN_PRIORITY_FEE_GWEI=30
MIN_MAX_FEE_GWEI=60
```

---

## Key Commands

```bash
# Start the bot (development mode with ts-node)
npm start

# Generate and persist API credentials to .polymarket-api-creds
npm run generate-api-creds

# Validate existing API credentials
npm run test-api-creds

# Compile TypeScript to dist/
npm run build

# Run compiled production build
npm run start:prod
```

---

## Architecture Overview

```
index.ts
  └── TradeMonitor      — REST polls Polymarket Data API for new target trades
  └── WebSocketMonitor  — Optional low-latency WS subscription (market or user channel)
  └── TradeExecutor     — Sizes trade, checks balance/allowance, submits CLOB order
  └── PositionTracker   — In-memory positions updated on fills
  └── RiskManager       — Session + per-market notional enforcement
```

Execution flow:
```
detect trade → BUY? → subscribe WS if needed → compute copy size
  → risk check → execute order (FOK/FAK/LIMIT) → record fill → update stats
```

---

## Code Examples

### Starting the bot programmatically

```typescript
import { startBot } from './src/index';

// The bot reads all config from process.env / .env
startBot();
```

### TradeMonitor — polling pattern

```typescript
import { TradeMonitor } from './src/TradeMonitor';

const monitor = new TradeMonitor({
  targetWallet: process.env.TARGET_WALLET!,
  pollInterval: Number(process.env.POLL_INTERVAL ?? 2000),
});

monitor.on('trade', (trade) => {
  console.log('New trade detected:', trade);
  // trade.side: 'BUY' | 'SELL'
  // trade.asset: token ID (outcome token address)
  // trade.size: USDC size
  // trade.price: fill price (0–1)
});

monitor.start();
```

### TradeExecutor — placing a copy order

```typescript
import { TradeExecutor } from './src/TradeExecutor';
import { ClobClient } from '@polymarket/clob-client';
import { ethers } from 'ethers';

const provider = new ethers.providers.JsonRpcProvider(process.env.RPC_URL);
const signer = new ethers.Wallet(process.env.WALLET_PRIVATE_KEY!, provider);

const clobClient = new ClobClient(
  'https://clob.polymarket.com',
  137, // Polygon chainId
  signer,
  apiCreds,          // loaded from .polymarket-api-creds
  Number(process.env.SIG_TYPE ?? 0),
  process.env.PROXY_WALLET_ADDRESS || undefined,
);

const executor = new TradeExecutor({
  client: clobClient,
  positionMultiplier: Number(process.env.POSITION_MULTIPLIER ?? 0.1),
  maxTradeSize: Number(process.env.MAX_TRADE_SIZE ?? 100),
  minTradeSize: Number(process.env.MIN_TRADE_SIZE ?? 1),
  orderType: (process.env.ORDER_TYPE ?? 'FOK') as 'FOK' | 'FAK' | 'LIMIT',
  slippageTolerance: Number(process.env.SLIPPAGE_TOLERANCE ?? 0.02),
});

// Copy a detected trade
await executor.copyTrade({
  side: 'BUY',
  tokenId: '0xAssetId...',
  originalSize: 12.5,   // USDC from target's trade
  price: 0.62,
});
```

### RiskManager — checking before execution

```typescript
import { RiskManager } from './src/RiskManager';

const riskManager = new RiskManager({
  maxSessionNotional: Number(process.env.MAX_SESSION_NOTIONAL ?? 0),
  maxPerMarketNotional: Number(process.env.MAX_PER_MARKET_NOTIONAL ?? 0),
});

const allowed = riskManager.checkTrade({
  marketId: '0xConditionId...',
  notional: copySize,
});

if (!allowed) {
  console.log('Trade blocked by risk limits');
}
```

### WebSocket monitor — low-latency subscription

```typescript
import { WebSocketMonitor } from './src/WebSocketMonitor';

const wsMonitor = new WebSocketMonitor({
  useUserChannel: process.env.USE_USER_CHANNEL === 'true',
  assetIds: process.env.WS_ASSET_IDS?.split(',').filter(Boolean) ?? [],
  marketIds: process.env.WS_MARKET_IDS?.split(',').filter(Boolean) ?? [],
});

wsMonitor.on('orderFilled', (fill) => {
  console.log('Fill received via WS:', fill);
});

wsMonitor.connect();
```

---

## Authentication Modes

### EOA (default — `SIG_TYPE=0`)

```env
SIG_TYPE=0
WALLET_PRIVATE_KEY=0xYourKey
# PROXY_WALLET_ADDRESS — leave empty
```

On first run, the bot auto-submits USDC.e/CTF approval transactions. Wallet needs POL for gas.

### Poly Proxy (`SIG_TYPE=1`)

```env
SIG_TYPE=1
WALLET_PRIVATE_KEY=0xSignerKey
PROXY_WALLET_ADDRESS=0xYourPolymarketProxyAddress
```

### Poly Polymorphic (`SIG_TYPE=2`)

```env
SIG_TYPE=2
WALLET_PRIVATE_KEY=0xSignerKey
PROXY_WALLET_ADDRESS=0xYourPolymorphicSafeAddress
```

---

## Generating API Credentials

```bash
npm run generate-api-creds
```

This derives API keys from your wallet signature and writes them to `.polymarket-api-creds`. Run once before `npm start` if you want to pre-generate credentials. The bot also auto-generates them on first start in EOA mode.

Validate credentials:

```bash
npm run test-api-creds
```

---

## Common Patterns

### Conservative testing setup

```env
POSITION_MULTIPLIER=0.05
MAX_TRADE_SIZE=5
MIN_TRADE_SIZE=1
MAX_SESSION_NOTIONAL=20
ORDER_TYPE=FOK
USE_WEBSOCKET=false
```

### WebSocket-only market channel (lower latency)

```env
USE_WEBSOCKET=true
USE_USER_CHANNEL=false
WS_ASSET_IDS=0xTokenId1,0xTokenId2
```

### LIMIT orders with slippage buffer

```env
ORDER_TYPE=LIMIT
SLIPPAGE_TOLERANCE=0.03
```

---

## Troubleshooting

**Bot starts but no trades detected**
- Verify `TARGET_WALLET` is a valid Polymarket wallet with recent activity
- Check `POLL_INTERVAL` — default 2000ms; lower means more API calls
- Confirm the target wallet trades on Polymarket (not just holds positions)

**`ethers` version conflicts**
- The project pins ethers v5. Do not upgrade to v6 — the CLOB SDK requires v5
- Run `npm ls ethers` to check for duplicate versions

**Approval transactions failing**
- Ensure the wallet has sufficient POL (MATIC) for gas on Polygon mainnet
- Try increasing `MIN_PRIORITY_FEE_GWEI` and `MIN_MAX_FEE_GWEI` if transactions stall

**`generate-api-creds` fails**
- Confirm `WALLET_PRIVATE_KEY` is correct and 0x-prefixed
- For `SIG_TYPE=1/2`, ensure `PROXY_WALLET_ADDRESS` matches your Polymarket account

**Orders rejected by CLOB**
- FOK orders fail if insufficient liquidity — try `ORDER_TYPE=FAK` or `LIMIT`
- Check `SLIPPAGE_TOLERANCE` isn't too tight for illiquid markets

**Session notional cap hit immediately**
- `MAX_SESSION_NOTIONAL` resets per process run; restart the bot to reset
- Set `MAX_SESSION_NOTIONAL=0` to disable the cap entirely

---

## Wallet Requirements

- **USDC.e** on Polygon mainnet (collateral for trades)
- **POL** (formerly MATIC) for gas fees
- Approve USDC.e for Polymarket CTF Exchange and CLOB contracts (bot does this automatically on first EOA run)

---

## References

- [QuickNode Guide — Building a Polymarket Copy Trading Bot](https://www.quicknode.com/guides/defi/polymarket-copy-trading-bot)
- [Polymarket CLOB Client SDK](https://github.com/Polymarket/clob-client)
- [Polymarket](https://polymarket.com/)
- [Polymarket CLOB API Docs](https://docs.polymarket.com/)
