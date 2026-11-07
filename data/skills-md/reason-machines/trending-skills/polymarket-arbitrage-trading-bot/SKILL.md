---
name: polymarket-arbitrage-trading-bot
description: Automated dump-and-hedge arbitrage trading bot for Polymarket's 15-minute crypto Up/Down markets, supporting BTC, ETH, SOL, and XRP.
triggers:
  - set up polymarket arbitrage bot
  - configure polymarket trading bot
  - run polymarket dump hedge strategy
  - polymarket 15 minute market bot
  - automate polymarket trading
  - polymarket clob arbitrage typescript
  - polymarket bot simulation mode
  - hedge polymarket prediction markets
---

# Polymarket Arbitrage Trading Bot

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Automated dump-and-hedge arbitrage bot for Polymarket's 15-minute crypto Up/Down prediction markets. Written in TypeScript using the official `@polymarket/clob-client`. Watches BTC, ETH, SOL, and XRP markets for sharp price drops on one leg, then buys both legs when combined cost falls below a target threshold to lock in a structural edge before resolution.

---

## Installation

```bash
git clone https://github.com/apechurch/polymarket-arbitrage-trading-bot.git
cd polymarket-arbitrage-trading-bot
npm install
cp .env.example .env
# Configure .env — see Configuration section
npm run build
```

**Requirements:** Node.js 16+, USDC on Polygon (for live trading), a Polymarket-compatible wallet.

---

## Project Structure

```text
src/
  main.ts              # Entry point: market discovery, monitors, period rollover
  monitor.ts           # Price polling & snapshots
  dumpHedgeTrader.ts   # Core strategy: dump → hedge → stop-loss → settlement
  api.ts               # Gamma API, CLOB API, order placement, redemption
  config.ts            # Environment variable loading
  models.ts            # Shared TypeScript types
  logger.ts            # History file (history.toml) + stderr logging
```

---

## Key Commands

| Command | Purpose |
|---------|---------|
| `npm run dev` | Run via `ts-node` (development, no build needed) |
| `npm run build` | Compile TypeScript to `dist/` |
| `npm run typecheck` | Type-check without emitting output |
| `npm run clean` | Remove `dist/` directory |
| `npm run sim` | **Simulation mode** — logs trades, no real orders |
| `npm run prod` | **Production mode** — places real CLOB orders |
| `npm start` | Run compiled output (defaults to simulation unless `--production` passed) |

---

## Configuration (`.env`)

```bash
# Wallet / Auth
PRIVATE_KEY=0xYOUR_PRIVATE_KEY_HERE
PROXY_WALLET_ADDRESS=0xYOUR_PROXY_WALLET
SIGNATURE_TYPE=2          # 0=EOA, 1=Proxy, 2=Gnosis Safe

# Markets to trade (comma-separated)
MARKETS=btc,eth,sol,xrp

# Polling
CHECK_INTERVAL_MS=1000

# Strategy thresholds
DUMP_HEDGE_SHARES=10                    # Shares per leg
DUMP_HEDGE_SUM_TARGET=0.95             # Max combined price for both legs
DUMP_HEDGE_MOVE_THRESHOLD=0.15         # Min fractional drop to trigger (15%)
DUMP_HEDGE_WINDOW_MINUTES=5            # Only detect dumps in first N minutes of round
DUMP_HEDGE_STOP_LOSS_MAX_WAIT_MINUTES=8 # Force stop-loss hedge after N minutes

# Mode flag (use --production CLI flag for live trading)
PRODUCTION=false

# Optional API overrides
GAMMA_API_URL=https://gamma-api.polymarket.com
CLOB_API_URL=https://clob.polymarket.com
API_KEY=
API_SECRET=
API_PASSPHRASE=
```

---

## Strategy Overview

```text
New 15m round starts
        │
        ▼
Watch first DUMP_HEDGE_WINDOW_MINUTES minutes
        │
        ├── Up or Down leg drops ≥ DUMP_HEDGE_MOVE_THRESHOLD?
        │         │
        │         ▼
        │   Buy dumped leg (Leg 1)
        │         │
        │         ├── Opposite ask cheap enough?
        │         │   (leg1_entry + opposite_ask ≤ DUMP_HEDGE_SUM_TARGET)
        │         │         │
        │         │         ▼
        │         │   Buy hedge leg (Leg 2) → locked-in edge
        │         │
        │         └── Timeout (DUMP_HEDGE_STOP_LOSS_MAX_WAIT_MINUTES)?
        │                   │
        │                   ▼
        │           Execute stop-loss hedge
        │
        └── Round ends → settle winners, redeem on-chain (production)
```

---

## Code Examples

### Loading Config (`src/config.ts` pattern)

```typescript
import * as dotenv from 'dotenv';
dotenv.config();

export const config = {
  privateKey: process.env.PRIVATE_KEY!,
  proxyWalletAddress: process.env.PROXY_WALLET_ADDRESS ?? '',
  signatureType: parseInt(process.env.SIGNATURE_TYPE ?? '2', 10),
  markets: (process.env.MARKETS ?? 'btc').split(',').map(m => m.trim()),
  checkIntervalMs: parseInt(process.env.CHECK_INTERVAL_MS ?? '1000', 10),
  dumpHedgeShares: parseFloat(process.env.DUMP_HEDGE_SHARES ?? '10'),
  dumpHedgeSumTarget: parseFloat(process.env.DUMP_HEDGE_SUM_TARGET ?? '0.95'),
  dumpHedgeMoveThreshold: parseFloat(process.env.DUMP_HEDGE_MOVE_THRESHOLD ?? '0.15'),
  dumpHedgeWindowMinutes: parseInt(process.env.DUMP_HEDGE_WINDOW_MINUTES ?? '5', 10),
  dumpHedgeStopLossMaxWaitMinutes: parseInt(
    process.env.DUMP_HEDGE_STOP_LOSS_MAX_WAIT_MINUTES ?? '8', 10
  ),
  production: process.env.PRODUCTION === 'true',
};
```

### Initializing the CLOB Client

```typescript
import { ClobClient } from '@polymarket/clob-client';
import { ethers } from 'ethers';
import { config } from './config';

function createClobClient(): ClobClient {
  const wallet = new ethers.Wallet(config.privateKey);
  return new ClobClient(
    config.clobApiUrl,         // e.g. 'https://clob.polymarket.com'
    137,                        // Polygon chain ID
    wallet,
    undefined,                  // credentials (set after key derivation if needed)
    config.signatureType,
    config.proxyWalletAddress
  );
}
```

### Discovering the Active 15-Minute Market

```typescript
import axios from 'axios';

interface GammaMarket {
  conditionId: string;
  question: string;
  endDateIso: string;
  active: boolean;
  tokens: Array<{ outcome: string; token_id: string }>;
}

async function findActive15mMarket(asset: string): Promise<GammaMarket | null> {
  const tag = `${asset.toUpperCase()}-15m`;
  const resp = await axios.get(`${config.gammaApiUrl}/markets`, {
    params: { tag, active: true, limit: 5 }
  });
  const markets: GammaMarket[] = resp.data;
  // Return the earliest-closing active market
  return markets.sort(
    (a, b) => new Date(a.endDateIso).getTime() - new Date(b.endDateIso).getTime()
  )[0] ?? null;
}
```

### Fetching Best Ask Price from CLOB

```typescript
async function getBestAsk(tokenId: string): Promise<number | null> {
  try {
    const resp = await axios.get(`${config.clobApiUrl}/book`, {
      params: { token_id: tokenId }
    });
    const asks: Array<{ price: string; size: string }> = resp.data.asks ?? [];
    if (asks.length === 0) return null;
    // Best ask = lowest price
    return Math.min(...asks.map(a => parseFloat(a.price)));
  } catch {
    return null;
  }
}
```

### Dump Detection Logic

```typescript
interface PriceSnapshot {
  timestamp: number;
  ask: number;
}

function detectDump(
  history: PriceSnapshot[],
  currentAsk: number,
  threshold: number,
  windowMs: number
): boolean {
  const cutoff = Date.now() - windowMs;
  const recent = history.filter(s => s.timestamp >= cutoff);
  if (recent.length === 0) return false;
  const highestRecentAsk = Math.max(...recent.map(s => s.ask));
  const drop = (highestRecentAsk - currentAsk) / highestRecentAsk;
  return drop >= threshold;
}

// Usage:
const windowMs = config.dumpHedgeWindowMinutes * 60 * 1000;
const isDump = detectDump(
  priceHistory,
  currentAsk,
  config.dumpHedgeMoveThreshold,
  windowMs
);
```

### Placing a Market Buy Order (Production)

```typescript
import { ClobClient, OrderType, Side } from '@polymarket/clob-client';

async function buyShares(
  client: ClobClient,
  tokenId: string,
  price: number,
  shares: number,
  simulate: boolean
): Promise<string | null> {
  if (simulate) {
    console.error(`[SIM] BUY ${shares} shares @ ${price} token=${tokenId}`);
    return 'sim-order-id';
  }
  const order = await client.createOrder({
    tokenID: tokenId,
    price,
    size: shares,
    side: Side.BUY,
    orderType: OrderType.FOK,   // Fill-or-Kill for immediate execution
  });
  const resp = await client.postOrder(order);
  return resp.orderID ?? null;
}
```

### Core Dump-Hedge Cycle

```typescript
interface LegState {
  filled: boolean;
  tokenId: string;
  entryPrice: number | null;
  orderId: string | null;
}

async function runDumpHedgeCycle(
  client: ClobClient,
  upTokenId: string,
  downTokenId: string,
  simulate: boolean
): Promise<void> {
  const leg1: LegState = { filled: false, tokenId: '', entryPrice: null, orderId: null };
  const leg2: LegState = { filled: false, tokenId: '', entryPrice: null, orderId: null };
  const startTime = Date.now();
  const windowMs = config.dumpHedgeWindowMinutes * 60 * 1000;
  const stopLossMs = config.dumpHedgeStopLossMaxWaitMinutes * 60 * 1000;
  const priceHistory: Record<string, PriceSnapshot[]> = {
    [upTokenId]: [], [downTokenId]: []
  };

  const interval = setInterval(async () => {
    const elapsed = Date.now() - startTime;
    const upAsk = await getBestAsk(upTokenId);
    const downAsk = await getBestAsk(downTokenId);
    if (upAsk == null || downAsk == null) return;

    // Record history
    const now = Date.now();
    priceHistory[upTokenId].push({ timestamp: now, ask: upAsk });
    priceHistory[downTokenId].push({ timestamp: now, ask: downAsk });

    // === LEG 1: Detect dump, buy dumped leg ===
    if (!leg1.filled && elapsed <= windowMs) {
      const upDumped = detectDump(
        priceHistory[upTokenId], upAsk, config.dumpHedgeMoveThreshold, windowMs
      );
      const downDumped = detectDump(
        priceHistory[downTokenId], downAsk, config.dumpHedgeMoveThreshold, windowMs
      );

      if (upDumped || downDumped) {
        const dumpedToken = upDumped ? upTokenId : downTokenId;
        const dumpedAsk = upDumped ? upAsk : downAsk;
        leg1.tokenId = dumpedToken;
        leg1.entryPrice = dumpedAsk;
        leg1.orderId = await buyShares(
          client, dumpedToken, dumpedAsk, config.dumpHedgeShares, simulate
        );
        leg1.filled = true;
        console.error(`[LEG1] Bought dumped leg @ ${dumpedAsk}`);
      }
    }

    // === LEG 2: Hedge when sum is favorable ===
    if (leg1.filled && !leg2.filled) {
      const hedgeToken = leg1.tokenId === upTokenId ? downTokenId : upTokenId;
      const hedgeAsk = leg1.tokenId === upTokenId ? downAsk : upAsk;
      const combinedCost = leg1.entryPrice! + hedgeAsk;

      const shouldHedge =
        combinedCost <= config.dumpHedgeSumTarget ||
        elapsed >= stopLossMs; // Stop-loss: force hedge on timeout

      if (shouldHedge) {
        const label = combinedCost <= config.dumpHedgeSumTarget ? 'HEDGE' : 'STOP-LOSS';
        leg2.tokenId = hedgeToken;
        leg2.entryPrice = hedgeAsk;
        leg2.orderId = await buyShares(
          client, hedgeToken, hedgeAsk, config.dumpHedgeShares, simulate
        );
        leg2.filled = true;
        console.error(`[LEG2:${label}] Bought hedge @ ${hedgeAsk}, combined=${combinedCost}`);
        clearInterval(interval);
      }
    }
  }, config.checkIntervalMs);
}
```

### Settlement and Redemption

```typescript
async function settleRound(
  client: ClobClient,
  conditionId: string,
  winningTokenId: string,
  simulate: boolean
): Promise<void> {
  if (simulate) {
    console.error(`[SIM] Would redeem winning token ${winningTokenId}`);
    return;
  }
  // Redeem via CLOB client (CTF redemption on Polygon)
  await client.redeemPositions({
    conditionId,
    amounts: [{ tokenId: winningTokenId, amount: config.dumpHedgeShares }]
  });
  console.error(`[SETTLE] Redeemed ${config.dumpHedgeShares} shares for ${winningTokenId}`);
}
```

---

## Running Modes

### Simulation (Recommended First)

```bash
# Via npm script
npm run sim

# Or directly with flag
node dist/main.js --simulation

# Monitor output
tail -f history.toml
```

### Production (Live Trading)

```bash
# Ensure .env has correct PRIVATE_KEY, PROXY_WALLET_ADDRESS, SIGNATURE_TYPE
npm run prod

# Or:
PRODUCTION=true node dist/main.js --production
```

### Single Asset, Custom Thresholds

```bash
MARKETS=btc \
DUMP_HEDGE_MOVE_THRESHOLD=0.12 \
DUMP_HEDGE_SUM_TARGET=0.93 \
DUMP_HEDGE_SHARES=5 \
npm run prod
```

---

## Common Patterns

### Multi-Asset Parallel Monitoring

```typescript
// main.ts pattern: spin up one monitor per asset
import { config } from './config';

async function main() {
  const isProduction = process.argv.includes('--production') || config.production;

  await Promise.all(
    config.markets.map(asset =>
      runAssetMonitor(asset, isProduction)
    )
  );
}

async function runAssetMonitor(asset: string, production: boolean) {
  while (true) {
    const market = await findActive15mMarket(asset);
    if (!market) {
      console.error(`[${asset}] No active market, retrying in 30s`);
      await sleep(30_000);
      continue;
    }
    const [upToken, downToken] = market.tokens;
    const client = createClobClient();
    await runDumpHedgeCycle(client, upToken.token_id, downToken.token_id, !production);
    // Wait for round end, then loop for next round
    const roundEnd = new Date(market.endDateIso).getTime();
    await sleep(Math.max(0, roundEnd - Date.now() + 5_000));
  }
}

function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

main().catch(console.error);
```

### Logging to history.toml

```typescript
import * as fs from 'fs';

interface TradeRecord {
  asset: string;
  roundEnd: string;
  leg1Price: number;
  leg2Price: number;
  combined: number;
  target: number;
  mode: 'hedge' | 'stop-loss';
  timestamp: string;
}

function appendHistory(record: TradeRecord): void {
  const entry = `
[[trade]]
asset = "${record.asset}"
round_end = "${record.roundEnd}"
leg1_price = ${record.leg1Price}
leg2_price = ${record.leg2Price}
combined = ${record.combined}
target = ${record.target}
mode = "${record.mode}"
timestamp = "${record.timestamp}"
`;
  fs.appendFileSync('history.toml', entry, 'utf8');
}
```

---

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `Failed to fetch market/orderbook` | API/network error | Temporary; check `GAMMA_API_URL` / `CLOB_API_URL` connectivity, retries are built in |
| Orders fail in production | Wrong auth config | Verify `PRIVATE_KEY`, `SIGNATURE_TYPE`, and `PROXY_WALLET_ADDRESS` match your Polymarket account |
| No market found for asset | Round gap or unsupported asset | Only use `btc`, `eth`, `sol`, `xrp`; wait for next 15m round to start |
| Bot never triggers leg 1 | Threshold too high or quiet market | Lower `DUMP_HEDGE_MOVE_THRESHOLD` or increase `DUMP_HEDGE_WINDOW_MINUTES` |
| Combined cost always above target | Market conditions | Lower `DUMP_HEDGE_SUM_TARGET` or adjust `DUMP_HEDGE_STOP_LOSS_MAX_WAIT_MINUTES` |
| `Cannot find module` errors | Missing build step | Run `npm run build` before `npm start` / `npm run prod` |
| Simulation not placing orders | Expected behavior | Simulation mode logs only; switch to `--production` for real orders |

---

## Safety Checklist

1. **Always simulate first** — run `npm run sim` across multiple rounds and inspect `history.toml`
2. **Start small** — use low `DUMP_HEDGE_SHARES` (e.g. `1`) in first production runs
3. **Secure credentials** — never commit `.env` to version control; add it to `.gitignore`
4. **Monitor stop-loss behavior** — tune `DUMP_HEDGE_STOP_LOSS_MAX_WAIT_MINUTES` carefully; forced hedges at bad prices reduce edge
5. **Polygon USDC** — ensure sufficient USDC balance on Polygon before running production
6. **Round timing** — the bot auto-rolls to the next round; verify rollover logs look correct in simulation first
