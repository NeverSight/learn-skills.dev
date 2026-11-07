---
name: polymarket-arbitrage-bot
description: TypeScript bot implementing dump-and-hedge arbitrage strategy on Polymarket 15-minute Up/Down prediction markets with CLOB order execution and simulation mode.
triggers:
  - set up polymarket arbitrage bot
  - configure polymarket trading bot
  - implement dump and hedge strategy polymarket
  - polymarket 15 minute market trading automation
  - polymarket CLOB order execution typescript
  - run polymarket bot in simulation mode
  - polymarket arbitrage strategy configuration
  - automate polymarket up down markets
---

# Polymarket Arbitrage Bot

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

TypeScript bot automating the **dump-and-hedge** strategy on Polymarket's 15-minute Up/Down markets (BTC, ETH, SOL, XRP). Detects sharp price drops, buys the dipped side, then hedges the opposite outcome when combined cost falls below a profit threshold.

## Installation

```bash
git clone https://github.com/infraform/polymarket-arbitrage-bot.git
cd polymarket-arbitrage-bot
npm install
npm run build
cp .env.example .env
```

## Key Commands

| Command | Description |
|---------|-------------|
| `npm start` | Run compiled bot (simulation by default) |
| `npm run sim` | Explicitly run in simulation (no real orders) |
| `npm run prod` | Run with real trades (`PRODUCTION=true`) |
| `npm run dev` | Run TypeScript directly via ts-node |
| `npm run build` | Compile TypeScript to `dist/` |

**Always test with `npm run sim` before enabling production mode.**

## Project Structure

```
src/
├── main.ts            # Entry point, config load, market discovery, wiring
├── config.ts          # Loads/validates .env into typed config
├── api.ts             # Gamma + CLOB API client (markets, orderbook, orders, redemption)
├── monitor.ts         # Orderbook snapshot polling, strategy callback driver
├── dumpHedgeTrader.ts # Dump detection, leg1/leg2, stop-loss, P&L tracking
├── models.ts          # Shared types: Market, OrderBook, TokenPrice, etc.
└── logger.ts          # history.toml append log + stderr output
```

## Environment Configuration

Create `.env` from `.env.example`:

```env
# --- Wallet & Auth (required for production) ---
PRIVATE_KEY=0x_your_private_key_here
PROXY_WALLET_ADDRESS=0x_your_proxy_wallet_address
SIGNATURE_TYPE=2                        # 0=EOA, 1=Proxy, 2=GnosisSafe

# --- Optional explicit CLOB API credentials ---
# If not set, credentials are derived from signer automatically
API_KEY=
API_SECRET=
API_PASSPHRASE=

# --- API Endpoints (defaults are production Polymarket) ---
GAMMA_API_URL=https://gamma-api.polymarket.com
CLOB_API_URL=https://clob.polymarket.com

# --- Markets ---
MARKETS=btc                             # comma-separated: btc,eth,sol,xrp

# --- Polling ---
CHECK_INTERVAL_MS=1000
MARKET_CLOSURE_CHECK_INTERVAL_SECONDS=20

# --- Strategy Parameters ---
DUMP_HEDGE_SHARES=10                    # Shares per leg
DUMP_HEDGE_SUM_TARGET=0.95             # Hedge when leg1 + opposite_ask <= this
DUMP_HEDGE_MOVE_THRESHOLD=0.15         # 15% drop triggers dump detection
DUMP_HEDGE_WINDOW_MINUTES=2            # Watch window at period start
DUMP_HEDGE_STOP_LOSS_MAX_WAIT_MINUTES=5
DUMP_HEDGE_STOP_LOSS_PERCENTAGE=0.2

# --- Mode ---
PRODUCTION=false                        # true = real trades
```

## Core Types (models.ts)

```typescript
// Key shared types used throughout the bot
interface Market {
  conditionId: string;
  questionId: string;
  tokens: Token[];         // [upToken, downToken]
  startTime: number;
  endTime: number;
  asset: string;           // "BTC", "ETH", etc.
}

interface Token {
  tokenId: string;
  outcome: string;         // "Up" or "Down"
}

interface OrderBook {
  tokenId: string;
  outcome: string;
  bids: PriceLevel[];
  asks: PriceLevel[];
  bestBid: number;
  bestAsk: number;
}

interface TokenPrice {
  tokenId: string;
  outcome: string;
  bestBid: number;
  bestAsk: number;
  timestamp: number;
}

interface MarketSnapshot {
  upPrice: TokenPrice;
  downPrice: TokenPrice;
  timeRemainingSeconds: number;
  periodStart: number;
}
```

## Strategy Flow

```
1. Discovery  → Gamma API finds current 15m market slug for each asset
2. Monitor    → Poll CLOB orderbooks every CHECK_INTERVAL_MS
3. Watch      → First DUMP_HEDGE_WINDOW_MINUTES: detect if ask drops >= MOVE_THRESHOLD
4. Leg 1      → Buy DUMP_HEDGE_SHARES of dumped side at current ask
5. Wait       → Watch for: leg1_entry + opposite_ask <= DUMP_HEDGE_SUM_TARGET
6. Leg 2      → Buy DUMP_HEDGE_SHARES of opposite outcome (hedge)
7. Stop-loss  → If hedge not triggered within STOP_LOSS_MAX_WAIT_MINUTES, hedge anyway
8. Rollover   → New 15m period → discover new market, reset state
9. Closure    → Redeem winning tokens (production), log P&L
```

## Code Examples

### Loading and using config (config.ts pattern)

```typescript
import * as dotenv from 'dotenv';
dotenv.config();

interface BotConfig {
  privateKey: string;
  proxyWalletAddress: string | undefined;
  signatureType: number;
  markets: string[];
  production: boolean;
  checkIntervalMs: number;
  dumpHedgeShares: number;
  dumpHedgeSumTarget: number;
  dumpHedgeMoveThreshold: number;
  dumpHedgeWindowMinutes: number;
  stopLossMaxWaitMinutes: number;
  stopLossPercentage: number;
  gammaApiUrl: string;
  clobApiUrl: string;
}

function loadConfig(): BotConfig {
  return {
    privateKey: process.env.PRIVATE_KEY ?? '',
    proxyWalletAddress: process.env.PROXY_WALLET_ADDRESS,
    signatureType: parseInt(process.env.SIGNATURE_TYPE ?? '2'),
    markets: (process.env.MARKETS ?? 'btc').split(',').map(m => m.trim()),
    production: process.env.PRODUCTION === 'true',
    checkIntervalMs: parseInt(process.env.CHECK_INTERVAL_MS ?? '1000'),
    dumpHedgeShares: parseInt(process.env.DUMP_HEDGE_SHARES ?? '10'),
    dumpHedgeSumTarget: parseFloat(process.env.DUMP_HEDGE_SUM_TARGET ?? '0.95'),
    dumpHedgeMoveThreshold: parseFloat(process.env.DUMP_HEDGE_MOVE_THRESHOLD ?? '0.15'),
    dumpHedgeWindowMinutes: parseFloat(process.env.DUMP_HEDGE_WINDOW_MINUTES ?? '2'),
    stopLossMaxWaitMinutes: parseFloat(process.env.DUMP_HEDGE_STOP_LOSS_MAX_WAIT_MINUTES ?? '5'),
    stopLossPercentage: parseFloat(process.env.DUMP_HEDGE_STOP_LOSS_PERCENTAGE ?? '0.2'),
    gammaApiUrl: process.env.GAMMA_API_URL ?? 'https://gamma-api.polymarket.com',
    clobApiUrl: process.env.CLOB_API_URL ?? 'https://clob.polymarket.com',
  };
}
```

### Fetching market via Gamma API (api.ts pattern)

```typescript
import axios from 'axios';

// Find current 15m market for an asset
async function findCurrentMarket(
  gammaApiUrl: string,
  asset: string  // "btc", "eth", "sol", "xrp"
): Promise<Market | null> {
  // Polymarket 15m slug format: btc-updown-15m-<period_timestamp>
  // Round current time down to nearest 15m period
  const now = Math.floor(Date.now() / 1000);
  const periodStart = now - (now % (15 * 60));
  const slug = `${asset}-updown-15m-${periodStart}`;

  try {
    const response = await axios.get(`${gammaApiUrl}/markets`, {
      params: { slug }
    });
    const markets = response.data;
    if (!markets || markets.length === 0) return null;
    return markets[0] as Market;
  } catch (err) {
    console.error(`[${asset}] Market discovery failed:`, err);
    return null;
  }
}
```

### Fetching orderbook from CLOB (api.ts pattern)

```typescript
async function getOrderBook(
  clobApiUrl: string,
  tokenId: string
): Promise<OrderBook | null> {
  try {
    const response = await axios.get(`${clobApiUrl}/book`, {
      params: { token_id: tokenId }
    });
    const data = response.data;
    
    const bestBid = data.bids?.length > 0 
      ? Math.max(...data.bids.map((b: any) => parseFloat(b.price))) 
      : 0;
    const bestAsk = data.asks?.length > 0 
      ? Math.min(...data.asks.map((a: any) => parseFloat(a.price))) 
      : 1;
    
    return {
      tokenId,
      outcome: data.outcome ?? '',
      bids: data.bids ?? [],
      asks: data.asks ?? [],
      bestBid,
      bestAsk,
    };
  } catch (err) {
    console.error(`OrderBook fetch failed for ${tokenId}:`, err);
    return null;
  }
}
```

### Dump detection logic (dumpHedgeTrader.ts pattern)

```typescript
interface DumpHedgeState {
  phase: 'watching' | 'leg1_placed' | 'hedging' | 'closed';
  leg1Outcome?: 'Up' | 'Down';
  leg1EntryPrice?: number;
  leg1PlacedAt?: number;
  leg1TokenId?: string;
  hedgeTokenId?: string;
  periodStart: number;
}

function detectDump(
  snapshot: MarketSnapshot,
  priceHistory: TokenPrice[],
  config: BotConfig
): 'Up' | 'Down' | null {
  const now = Date.now() / 1000;
  const windowStart = snapshot.periodStart;
  const windowEnd = windowStart + config.dumpHedgeWindowMinutes * 60;

  // Only detect within watch window
  if (now > windowEnd) return null;

  // Get earliest prices in window for comparison
  const windowHistory = priceHistory.filter(p => p.timestamp >= windowStart);
  if (windowHistory.length < 2) return null;

  const earliest = windowHistory[0];
  const current = snapshot;

  // Check Up side dump
  if (earliest.upPrice.bestAsk > 0) {
    const upDrop = (earliest.upPrice.bestAsk - current.upPrice.bestAsk) / earliest.upPrice.bestAsk;
    if (upDrop >= config.dumpHedgeMoveThreshold) {
      console.error(`[DUMP] Up side dropped ${(upDrop * 100).toFixed(1)}%`);
      return 'Up';
    }
  }

  // Check Down side dump
  if (earliest.downPrice.bestAsk > 0) {
    const downDrop = (earliest.downPrice.bestAsk - current.downPrice.bestAsk) / earliest.downPrice.bestAsk;
    if (downDrop >= config.dumpHedgeMoveThreshold) {
      console.error(`[DUMP] Down side dropped ${(downDrop * 100).toFixed(1)}%`);
      return 'Down';
    }
  }

  return null;
}

function shouldHedge(
  state: DumpHedgeState,
  snapshot: MarketSnapshot,
  config: BotConfig
): boolean {
  if (state.phase !== 'leg1_placed' || !state.leg1EntryPrice) return false;

  const oppositeAsk = state.leg1Outcome === 'Up'
    ? snapshot.downPrice.bestAsk
    : snapshot.upPrice.bestAsk;

  const combinedCost = state.leg1EntryPrice + oppositeAsk;
  return combinedCost <= config.dumpHedgeSumTarget;
}

function shouldStopLoss(
  state: DumpHedgeState,
  config: BotConfig
): boolean {
  if (state.phase !== 'leg1_placed' || !state.leg1PlacedAt) return false;
  const waitedMinutes = (Date.now() / 1000 - state.leg1PlacedAt) / 60;
  return waitedMinutes >= config.stopLossMaxWaitMinutes;
}
```

### Placing an order via CLOB (api.ts pattern)

```typescript
import { ethers } from 'ethers';

interface OrderParams {
  tokenId: string;
  price: number;      // 0.0 to 1.0
  size: number;       // number of shares
  side: 'BUY' | 'SELL';
}

async function placeOrder(
  clobApiUrl: string,
  signer: ethers.Wallet,
  apiKey: string,
  apiSecret: string,
  apiPassphrase: string,
  params: OrderParams,
  production: boolean
): Promise<string | null> {
  if (!production) {
    console.error(`[SIM] Would place ${params.side} ${params.size} shares of ${params.tokenId} @ ${params.price}`);
    return `sim-order-${Date.now()}`;
  }

  // Build and sign order for CLOB
  const order = {
    token_id: params.tokenId,
    price: params.price.toFixed(4),
    size: params.size.toString(),
    side: params.side,
    type: 'GTC',
  };

  // CLOB requires L1/L2 auth headers derived from API credentials
  const timestamp = Math.floor(Date.now() / 1000).toString();
  const signature = await signClobOrder(signer, order, timestamp);

  try {
    const response = await axios.post(`${clobApiUrl}/order`, order, {
      headers: {
        'POLY_ADDRESS': await signer.getAddress(),
        'POLY_SIGNATURE': signature,
        'POLY_TIMESTAMP': timestamp,
        'POLY_API_KEY': apiKey,
      }
    });
    return response.data.orderId ?? null;
  } catch (err) {
    console.error('[ORDER] Placement failed:', err);
    return null;
  }
}
```

### Monitor loop (monitor.ts pattern)

```typescript
async function startMonitor(
  market: Market,
  config: BotConfig,
  onSnapshot: (snapshot: MarketSnapshot) => Promise<void>
): Promise<void> {
  const [upToken, downToken] = market.tokens;

  const poll = async () => {
    try {
      const [upBook, downBook] = await Promise.all([
        getOrderBook(config.clobApiUrl, upToken.tokenId),
        getOrderBook(config.clobApiUrl, downToken.tokenId),
      ]);

      if (!upBook || !downBook) return;

      const now = Math.floor(Date.now() / 1000);
      const snapshot: MarketSnapshot = {
        upPrice: {
          tokenId: upToken.tokenId,
          outcome: 'Up',
          bestBid: upBook.bestBid,
          bestAsk: upBook.bestAsk,
          timestamp: now,
        },
        downPrice: {
          tokenId: downToken.tokenId,
          outcome: 'Down',
          bestBid: downBook.bestBid,
          bestAsk: downBook.bestAsk,
          timestamp: now,
        },
        timeRemainingSeconds: market.endTime - now,
        periodStart: market.startTime,
      };

      await onSnapshot(snapshot);
    } catch (err) {
      console.error('[MONITOR] Poll error:', err);
    }
  };

  // Start polling
  const intervalId = setInterval(poll, config.checkIntervalMs);
  await poll(); // immediate first poll

  // Stop when market ends
  const msUntilEnd = (market.endTime * 1000) - Date.now();
  setTimeout(() => clearInterval(intervalId), msUntilEnd + 5000);
}
```

### History logging (logger.ts pattern)

```typescript
import * as fs from 'fs';

const HISTORY_FILE = 'history.toml';

interface TradeRecord {
  timestamp: string;
  asset: string;
  action: 'leg1' | 'hedge' | 'stop_loss' | 'redemption';
  outcome: string;
  price: number;
  shares: number;
  simulation: boolean;
  pnl?: number;
}

function logTrade(record: TradeRecord): void {
  const entry = `
[[trade]]
timestamp = "${record.timestamp}"
asset = "${record.asset}"
action = "${record.action}"
outcome = "${record.outcome}"
price = ${record.price}
shares = ${record.shares}
simulation = ${record.simulation}
${record.pnl !== undefined ? `pnl = ${record.pnl}` : ''}
`;
  fs.appendFileSync(HISTORY_FILE, entry, 'utf8');
  console.error(`[LOG] ${record.action} ${record.outcome} @ ${record.price} (sim=${record.simulation})`);
}
```

### Main entry pattern (main.ts)

```typescript
import { loadConfig } from './config';
import { findCurrentMarket } from './api';
import { startMonitor } from './monitor';
import { DumpHedgeTrader } from './dumpHedgeTrader';

async function main() {
  const config = loadConfig();

  console.error(`[BOOT] Mode: ${config.production ? 'PRODUCTION' : 'SIMULATION'}`);
  console.error(`[BOOT] Markets: ${config.markets.join(', ')}`);

  // Start a monitor+trader for each configured asset
  const tasks = config.markets.map(async (asset) => {
    while (true) {
      // Discover current 15m market
      const market = await findCurrentMarket(config.gammaApiUrl, asset);
      if (!market) {
        console.error(`[${asset}] No active market found, retrying in 30s`);
        await sleep(30_000);
        continue;
      }

      console.error(`[${asset}] Found market: ${market.conditionId}, ends ${new Date(market.endTime * 1000).toISOString()}`);

      const trader = new DumpHedgeTrader(asset, market, config);
      await startMonitor(market, config, (snap) => trader.onSnapshot(snap));

      // Market ended — handle closure, then loop to find next period
      await trader.onClose();
      console.error(`[${asset}] Period ended, discovering next market...`);
      await sleep(5_000);
    }
  });

  await Promise.all(tasks);
}

function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

main().catch(err => {
  console.error('[FATAL]', err);
  process.exit(1);
});
```

## Common Patterns

### Multi-asset configuration

```env
# Monitor BTC and ETH simultaneously
MARKETS=btc,eth

# More aggressive dump detection
DUMP_HEDGE_MOVE_THRESHOLD=0.10
DUMP_HEDGE_WINDOW_MINUTES=3

# Tighter profit target
DUMP_HEDGE_SUM_TARGET=0.93
```

### Tuning for volatile markets

```env
# Larger position per leg
DUMP_HEDGE_SHARES=25

# Wider dump threshold catches more opportunities
DUMP_HEDGE_MOVE_THRESHOLD=0.10

# Longer window to detect slower dumps
DUMP_HEDGE_WINDOW_MINUTES=4

# More time before stop-loss kicks in
DUMP_HEDGE_STOP_LOSS_MAX_WAIT_MINUTES=8
```

### Switching simulation → production

```bash
# 1. Verify strategy looks correct in simulation
npm run sim

# 2. Check history.toml for expected trade pattern
cat history.toml

# 3. Enable production (ensure wallet funded with USDC + POL for gas)
PRODUCTION=true npm start
# or
npm run prod
```

### Using EOA wallet (no proxy)

```env
PRIVATE_KEY=0x_your_eoa_private_key
SIGNATURE_TYPE=0
# Leave PROXY_WALLET_ADDRESS unset
```

### Using GnosisSafe proxy (default Polymarket setup)

```env
PRIVATE_KEY=0x_your_signer_private_key
PROXY_WALLET_ADDRESS=0x_your_polymarket_profile_address
SIGNATURE_TYPE=2
```

## Profit Mechanics

```
Per resolved pair:
  Revenue:          1.00  (winning outcome pays $1/share)
  Cost (leg1):      e.g. 0.45  (bought dumped side)
  Cost (leg2):      e.g. 0.49  (hedge at ask)
  Combined cost:    0.94  (<= SUM_TARGET of 0.95)
  Profit/share:     0.06  (6% per share pair, before fees)

Worst case (stop-loss hedge):
  If hedge triggers at stop-loss, combined cost may exceed 0.95
  Loss is bounded by STOP_LOSS_PERCENTAGE (e.g. 0.2 = 20% of leg1 size)
```

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| No markets found | Wrong slug/timing | Check `GAMMA_API_URL` connectivity; confirm asset name is lowercase |
| Orders fail in production | Bad credentials | Verify `PRIVATE_KEY`, `PROXY_WALLET_ADDRESS`, `SIGNATURE_TYPE` |
| Redemption fails | Insufficient POL gas | Fund wallet with POL/MATIC on Polygon mainnet |
| No dumps detected | Threshold too high | Lower `DUMP_HEDGE_MOVE_THRESHOLD` (e.g. 0.10) or extend window |
| Strategy never hedges | Sum target too tight | Raise `DUMP_HEDGE_SUM_TARGET` (e.g. 0.97) |
| Frequent stop-loss triggers | Market low volatility | Increase `STOP_LOSS_MAX_WAIT_MINUTES` |

### Debugging with simulation logs

```bash
# Run simulation and watch logs in real time
npm run sim 2>&1 | tee debug.log

# Review all trades
grep "action" history.toml

# Check P&L entries
grep "pnl" history.toml
```

## Security Checklist

- `.env` is in `.gitignore` — never commit it
- Use a **dedicated wallet** with limited USDC (not your main wallet)
- Always run `npm run sim` first and review `history.toml` before going live
- Rotate `PRIVATE_KEY` immediately if it may have been exposed
- API keys derived from signer are preferred over explicit `API_KEY` / `API_SECRET`
