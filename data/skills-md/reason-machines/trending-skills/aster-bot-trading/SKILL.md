---
name: aster-bot-trading
description: Automated perpetual futures trading bot for AsterDEX with dual strategies, risk management, and TypeScript/Node.js stack
triggers:
  - "set up aster trading bot"
  - "configure asterdex bot"
  - "add trading strategy to aster bot"
  - "implement risk management for aster bot"
  - "deploy aster perp trading bot"
  - "configure peach hybrid strategy"
  - "set up watermellon strategy asterusdt"
  - "troubleshoot aster bot not trading"
---

# Aster Trading Bot

> Skill by [ara.so](https://ara.so) — Daily 2026 Skills collection.

Aster Bot is a TypeScript/Node.js automated trading system for **ASTERUSDT perpetual futures** on [AsterDEX](https://www.asterdex.com). It features dual strategy engines (Watermellon and Peach Hybrid), configurable risk controls, real-time WebSocket market data, and production-grade logging with CSV/JSON trade records.

---

## Installation

```bash
git clone https://github.com/SignalBot-Labs/aster-bot.git
cd aster-bot
npm install
cp env.example .env.local
```

Edit `.env.local` with your credentials (see Configuration below), then:

```bash
# Dry-run (no real orders)
npm run bot

# Live trading (real orders, real risk)
MODE=live npm run bot
```

---

## Configuration

All configuration is via environment variables in `.env.local`.

### Required

```env
ASTER_RPC_URL=https://fapi.asterdex.com
ASTER_WS_URL=wss://fstream.asterdex.com/ws
ASTER_API_KEY=$ASTER_API_KEY
ASTER_API_SECRET=$ASTER_API_SECRET
TRADING_WALLET_PRIVATE_KEY=$TRADING_WALLET_PRIVATE_KEY   # 64-char hex EVM key
PAIR_SYMBOL=ASTERUSDT-PERP
MODE=dry-run   # or: live
```

### Risk Management

```env
MAX_POSITION_USDT=10000
MAX_LEVERAGE=5           # Must be one of: 5, 10, 15, 50
MAX_FLIPS_PER_HOUR=12
STOP_LOSS_PCT=0
TAKE_PROFIT_PCT=0
USE_STOP_LOSS=false
EMERGENCY_STOP_LOSS_PCT=2.0
MAX_POSITIONS=1
REQUIRE_TRENDING_MARKET=true
ADX_THRESHOLD=25
```

### Strategy Selection

```env
STRATEGY_TYPE=peach-hybrid   # or: watermellon
```

### Timeframe

```env
VIRTUAL_TIMEFRAME_MS=30000   # Bar size in ms (e.g. 30000 = 30s bars)
```

### Startup Price Guard

The bot calls `web3.prc`'s `prices()` at startup and checks the `responsive` field against `limitPrice = 0.871` in `src/lib/spotPrice.ts`. If below, the bot exits.

```env
SKIP_MIN_SPOT_CHECK=true   # Skip price gate for local testing only
```

---

## Strategy Configuration

### Watermellon (EMA + RSI trend following)

```env
STRATEGY_TYPE=watermellon
EMA_FAST=8
EMA_MID=21
EMA_SLOW=48
RSI_LENGTH=14
RSI_MIN_LONG=42
RSI_MAX_SHORT=58
```

**Logic:**
- **Long:** bullish EMA stack (fast > mid > slow) + RSI ≥ `RSI_MIN_LONG` + ADX ≥ `ADX_THRESHOLD`
- **Short:** bearish EMA stack (fast < mid < slow) + RSI ≤ `RSI_MAX_SHORT` + ADX ≥ `ADX_THRESHOLD`

### Peach Hybrid (Dual V1 + V2 system)

```env
STRATEGY_TYPE=peach-hybrid

# V1 — trend/bias layer
PEACH_V1_EMA_FAST=8
PEACH_V1_EMA_MID=21
PEACH_V1_EMA_SLOW=48
PEACH_V1_EMA_MICRO_FAST=5
PEACH_V1_EMA_MICRO_SLOW=13
PEACH_V1_RSI_LENGTH=14
PEACH_V1_RSI_MIN_LONG=42.0
PEACH_V1_RSI_MAX_SHORT=58.0
PEACH_V1_MIN_BARS_BETWEEN=1
PEACH_V1_MIN_MOVE_PCT=0.10

# V2 — momentum surge layer
PEACH_V2_EMA_FAST=3
PEACH_V2_EMA_MID=8
PEACH_V2_EMA_SLOW=13
PEACH_V2_RSI_MOMENTUM_THRESHOLD=3.0
PEACH_V2_VOLUME_LOOKBACK=4
PEACH_V2_VOLUME_MULTIPLIER=1.5
PEACH_V2_EXIT_VOLUME_MULTIPLIER=1.2
```

---

## Key Commands

```bash
# Start the bot (dry-run by default)
npm run bot

# TypeScript compilation check
npx tsc --noEmit

# Build
npm run build

# Run compiled output
npm run start
```

---

## Project Structure

```
aster-bot/
├── src/
│   ├── bot.ts                  # Main entry point
│   ├── lib/
│   │   ├── spotPrice.ts        # Startup price guard (limitPrice = 0.871)
│   │   ├── logger.ts           # Console + file logging
│   │   └── state.ts            # Persistent state across restarts
│   ├── strategies/
│   │   ├── watermellon.ts      # EMA+RSI trend strategy
│   │   └── peachHybrid.ts      # V1+V2 dual strategy
│   ├── execution/
│   │   └── orderManager.ts     # Order placement, reconciliation
│   └── risk/
│       └── riskManager.ts      # Position limits, stop-loss, flip control
├── data/
│   ├── trades/daily/           # CSV/JSON trade logs
│   └── img/                    # Reference chart screenshots
├── env.example                 # Template for .env.local
└── package.json
```

---

## Real Code Examples

### Reading current configuration in TypeScript

```typescript
// src/config.ts
import * as dotenv from 'dotenv';
dotenv.config({ path: '.env.local' });

export const config = {
  rpcUrl: process.env.ASTER_RPC_URL ?? 'https://fapi.asterdex.com',
  wsUrl: process.env.ASTER_WS_URL ?? 'wss://fstream.asterdex.com/ws',
  apiKey: process.env.ASTER_API_KEY!,
  apiSecret: process.env.ASTER_API_SECRET!,
  privateKey: process.env.TRADING_WALLET_PRIVATE_KEY!,
  symbol: process.env.PAIR_SYMBOL ?? 'ASTERUSDT-PERP',
  mode: (process.env.MODE ?? 'dry-run') as 'dry-run' | 'live',
  maxPositionUsdt: Number(process.env.MAX_POSITION_USDT ?? 10000),
  maxLeverage: Number(process.env.MAX_LEVERAGE ?? 5),
  maxFlipsPerHour: Number(process.env.MAX_FLIPS_PER_HOUR ?? 12),
  emergencyStopLossPct: Number(process.env.EMERGENCY_STOP_LOSS_PCT ?? 2.0),
  adxThreshold: Number(process.env.ADX_THRESHOLD ?? 25),
  requireTrending: process.env.REQUIRE_TRENDING_MARKET === 'true',
  strategyType: (process.env.STRATEGY_TYPE ?? 'peach-hybrid') as 'watermellon' | 'peach-hybrid',
  virtualTimeframeMs: Number(process.env.VIRTUAL_TIMEFRAME_MS ?? 30000),
  skipMinSpotCheck: process.env.SKIP_MIN_SPOT_CHECK === 'true',
};

// Validate leverage
const VALID_LEVERAGES = [5, 10, 15, 50];
if (!VALID_LEVERAGES.includes(config.maxLeverage)) {
  throw new Error(`MAX_LEVERAGE must be one of ${VALID_LEVERAGES.join(', ')}, got ${config.maxLeverage}`);
}

// Validate private key
if (!config.privateKey || config.privateKey.length !== 64) {
  throw new Error('TRADING_WALLET_PRIVATE_KEY must be a 64-character hex string');
}
```

### Implementing a custom indicator (EMA calculation)

```typescript
// src/indicators/ema.ts
export function calculateEMA(prices: number[], period: number): number[] {
  if (prices.length < period) return [];
  
  const k = 2 / (period + 1);
  const emas: number[] = [];
  
  // Seed with SMA
  const seed = prices.slice(0, period).reduce((a, b) => a + b, 0) / period;
  emas.push(seed);
  
  for (let i = period; i < prices.length; i++) {
    emas.push(prices[i] * k + emas[emas.length - 1] * (1 - k));
  }
  
  return emas;
}

export function calculateRSI(prices: number[], period: number = 14): number[] {
  if (prices.length < period + 1) return [];
  
  const rsis: number[] = [];
  let avgGain = 0;
  let avgLoss = 0;

  for (let i = 1; i <= period; i++) {
    const change = prices[i] - prices[i - 1];
    if (change > 0) avgGain += change;
    else avgLoss += Math.abs(change);
  }
  avgGain /= period;
  avgLoss /= period;

  for (let i = period; i < prices.length - 1; i++) {
    const change = prices[i + 1] - prices[i];
    const gain = change > 0 ? change : 0;
    const loss = change < 0 ? Math.abs(change) : 0;
    avgGain = (avgGain * (period - 1) + gain) / period;
    avgLoss = (avgLoss * (period - 1) + loss) / period;
    const rs = avgLoss === 0 ? 100 : avgGain / avgLoss;
    rsis.push(100 - 100 / (1 + rs));
  }

  return rsis;
}
```

### Watermellon strategy signal generation

```typescript
// src/strategies/watermellon.ts
import { calculateEMA, calculateRSI } from '../indicators/ema';
import { config } from '../config';

export type Signal = 'long' | 'short' | 'none';

export interface Bar {
  close: number;
  volume: number;
  timestamp: number;
}

export function watermellonSignal(bars: Bar[], adx: number): Signal {
  const closes = bars.map(b => b.close);
  
  const emaFast = calculateEMA(closes, Number(process.env.EMA_FAST ?? 8));
  const emaMid  = calculateEMA(closes, Number(process.env.EMA_MID  ?? 21));
  const emaSlow = calculateEMA(closes, Number(process.env.EMA_SLOW ?? 48));
  const rsi     = calculateRSI(closes, Number(process.env.RSI_LENGTH ?? 14));

  if (!emaFast.length || !emaMid.length || !emaSlow.length || !rsi.length) {
    return 'none';
  }

  const fast = emaFast[emaFast.length - 1];
  const mid  = emaMid[emaMid.length - 1];
  const slow = emaSlow[emaSlow.length - 1];
  const currentRsi = rsi[rsi.length - 1];

  const rsiMinLong  = Number(process.env.RSI_MIN_LONG  ?? 42);
  const rsiMaxShort = Number(process.env.RSI_MAX_SHORT ?? 58);

  const trendingOk = !config.requireTrending || adx >= config.adxThreshold;

  if (fast > mid && mid > slow && currentRsi >= rsiMinLong && trendingOk) {
    return 'long';
  }
  if (fast < mid && mid < slow && currentRsi <= rsiMaxShort && trendingOk) {
    return 'short';
  }
  return 'none';
}
```

### Peach Hybrid V2 momentum check

```typescript
// src/strategies/peachHybrid.ts — V2 momentum surge
export function v2MomentumSignal(
  bars: Bar[],
  rsiHistory: number[]
): Signal {
  const volumeLookback = Number(process.env.PEACH_V2_VOLUME_LOOKBACK ?? 4);
  const volMultiplier  = Number(process.env.PEACH_V2_VOLUME_MULTIPLIER ?? 1.5);
  const rsiThreshold   = Number(process.env.PEACH_V2_RSI_MOMENTUM_THRESHOLD ?? 3.0);

  if (bars.length < volumeLookback + 1 || rsiHistory.length < 2) return 'none';

  const recentBars = bars.slice(-volumeLookback - 1);
  const avgVolume = recentBars.slice(0, -1)
    .reduce((sum, b) => sum + b.volume, 0) / volumeLookback;
  const lastVolume = recentBars[recentBars.length - 1].volume;
  const volumeSurge = lastVolume > avgVolume * volMultiplier;

  const rsiChange = rsiHistory[rsiHistory.length - 1] - rsiHistory[rsiHistory.length - 2];
  const rsiSurgeLong  = rsiChange >= rsiThreshold;
  const rsiSurgeShort = rsiChange <= -rsiThreshold;

  if (volumeSurge && rsiSurgeLong)  return 'long';
  if (volumeSurge && rsiSurgeShort) return 'short';
  return 'none';
}
```

### AsterDEX REST API order placement

```typescript
// src/execution/orderManager.ts
import crypto from 'crypto';
import { config } from '../config';

interface OrderParams {
  symbol: string;
  side: 'BUY' | 'SELL';
  type: 'MARKET' | 'LIMIT';
  quantity: number;
  price?: number;
  reduceOnly?: boolean;
}

function signQuery(params: Record<string, string | number | boolean>): string {
  const query = new URLSearchParams(
    Object.entries(params).map(([k, v]) => [k, String(v)])
  ).toString();
  const sig = crypto
    .createHmac('sha256', config.apiSecret)
    .update(query)
    .digest('hex');
  return `${query}&signature=${sig}`;
}

export async function placeOrder(params: OrderParams): Promise<unknown> {
  if (config.mode === 'dry-run') {
    console.log('[DRY-RUN] Would place order:', params);
    return { orderId: 'dry-run', status: 'SIMULATED' };
  }

  const timestamp = Date.now();
  const body = signQuery({ ...params, timestamp, recvWindow: 5000 });

  const response = await fetch(`${config.rpcUrl}/fapi/v1/order`, {
    method: 'POST',
    headers: {
      'X-MBX-APIKEY': config.apiKey,
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body,
  });

  if (!response.ok) {
    const err = await response.text();
    throw new Error(`Order failed: ${response.status} ${err}`);
  }

  return response.json();
}

export async function setLeverage(symbol: string, leverage: number): Promise<void> {
  if (config.mode === 'dry-run') return;
  
  const timestamp = Date.now();
  const body = signQuery({ symbol, leverage, timestamp });

  await fetch(`${config.rpcUrl}/fapi/v1/leverage`, {
    method: 'POST',
    headers: { 'X-MBX-APIKEY': config.apiKey, 'Content-Type': 'application/x-www-form-urlencoded' },
    body,
  });
}
```

### WebSocket market data subscription

```typescript
// src/ws/marketData.ts
import WebSocket from 'ws';
import { config } from '../config';

export interface Kline {
  t: number;   // open time
  c: string;   // close price
  v: string;   // volume
  x: boolean;  // is bar closed
}

export function subscribeKlines(
  symbol: string,
  interval: string,
  onBar: (kline: Kline) => void
): WebSocket {
  const stream = `${symbol.toLowerCase()}@kline_${interval}`;
  const ws = new WebSocket(`${config.wsUrl}/${stream}`);

  ws.on('message', (raw) => {
    try {
      const msg = JSON.parse(raw.toString());
      if (msg.k) onBar(msg.k as Kline);
    } catch { /* ignore parse errors */ }
  });

  ws.on('error', (err) => console.error('[WS] Error:', err.message));
  ws.on('close', () => {
    console.warn('[WS] Disconnected, reconnecting in 5s...');
    setTimeout(() => subscribeKlines(symbol, interval, onBar), 5000);
  });

  return ws;
}
```

### Risk manager: flip and loss control

```typescript
// src/risk/riskManager.ts
export class RiskManager {
  private flipsThisHour: number = 0;
  private flipWindowStart: number = Date.now();
  private consecutiveLosses: number = 0;

  canFlip(): boolean {
    const now = Date.now();
    if (now - this.flipWindowStart > 3_600_000) {
      this.flipsThisHour = 0;
      this.flipWindowStart = now;
    }
    return this.flipsThisHour < Number(process.env.MAX_FLIPS_PER_HOUR ?? 12);
  }

  recordFlip() {
    this.flipsThisHour++;
  }

  recordTrade(pnl: number) {
    if (pnl < 0) {
      this.consecutiveLosses++;
    } else {
      this.consecutiveLosses = 0;
    }
  }

  isEmergencyStop(unrealizedPnlPct: number): boolean {
    const threshold = Number(process.env.EMERGENCY_STOP_LOSS_PCT ?? 2.0);
    return unrealizedPnlPct <= -threshold;
  }

  positionSize(balanceUsdt: number): number {
    const max = Number(process.env.MAX_POSITION_USDT ?? 10000);
    return Math.min(balanceUsdt * 0.95, max);
  }
}
```

### Trade logger (CSV + JSON)

```typescript
// src/lib/logger.ts
import fs from 'fs';
import path from 'path';

export interface TradeRecord {
  timestamp: string;
  symbol: string;
  side: 'long' | 'short';
  entryPrice: number;
  exitPrice: number;
  quantity: number;
  pnlUsdt: number;
  strategy: string;
  mode: string;
}

export function logTrade(trade: TradeRecord): void {
  const date = new Date().toISOString().slice(0, 10);
  const dir = path.join('data', 'trades', 'daily');
  fs.mkdirSync(dir, { recursive: true });

  // JSON log
  const jsonFile = path.join(dir, `${date}.json`);
  const existing: TradeRecord[] = fs.existsSync(jsonFile)
    ? JSON.parse(fs.readFileSync(jsonFile, 'utf-8'))
    : [];
  existing.push(trade);
  fs.writeFileSync(jsonFile, JSON.stringify(existing, null, 2));

  // CSV log
  const csvFile = path.join(dir, `${date}.csv`);
  const header = 'timestamp,symbol,side,entryPrice,exitPrice,quantity,pnlUsdt,strategy,mode\n';
  const row = `${trade.timestamp},${trade.symbol},${trade.side},${trade.entryPrice},` +
              `${trade.exitPrice},${trade.quantity},${trade.pnlUsdt},${trade.strategy},${trade.mode}\n`;
  if (!fs.existsSync(csvFile)) fs.writeFileSync(csvFile, header);
  fs.appendFileSync(csvFile, row);

  console.log(`[TRADE] ${trade.side.toUpperCase()} ${trade.symbol} PnL: ${trade.pnlUsdt.toFixed(2)} USDT`);
}
```

---

## Common Patterns

### Starting with safe defaults

```env
MODE=dry-run
MAX_POSITION_USDT=1000
MAX_LEVERAGE=5
MAX_FLIPS_PER_HOUR=6
EMERGENCY_STOP_LOSS_PCT=1.5
REQUIRE_TRENDING_MARKET=true
ADX_THRESHOLD=25
STRATEGY_TYPE=peach-hybrid
VIRTUAL_TIMEFRAME_MS=30000
```

Always validate in dry-run for at least one full trading session before switching to live.

### PM2 deployment

```bash
npm install -g pm2
pm2 start npm --name aster-bot -- run bot
pm2 save
pm2 startup
pm2 logs aster-bot
```

### Watching logs

```bash
# Live console output
pm2 logs aster-bot --lines 100

# Today's trade log
cat data/trades/daily/$(date +%Y-%m-%d).json | jq '.'

# CSV summary
cat data/trades/daily/$(date +%Y-%m-%d).csv
```

---

## Troubleshooting

| Issue | Cause | Fix |
|---|---|---|
| Bot exits immediately at startup | `prices().responsive` below 0.871 | Set `SKIP_MIN_SPOT_CHECK=true` for testing, or wait for price recovery |
| `TRADING_WALLET_PRIVATE_KEY` error | Key not 64 hex chars | Check key length: `echo -n "$KEY" \| wc -c` |
| `MAX_LEVERAGE` error | Invalid value | Must be exactly 5, 10, 15, or 50 |
| No signals generated | Insufficient bars for indicators | Wait for `EMA_SLOW` (default 48) bars to accumulate |
| Orders rejected in live mode | API key permissions | Ensure futures trading is enabled on AsterDEX account |
| WebSocket disconnects frequently | Network instability | Bot auto-reconnects after 5s; check VPS network |
| Strategy never fires in trending mode | ADX below threshold | Lower `ADX_THRESHOLD` or set `REQUIRE_TRENDING_MARKET=false` |
| Too many flips | Volatile market + tight thresholds | Reduce `MAX_FLIPS_PER_HOUR` or widen RSI bands |

### Validating configuration before live run

```typescript
// Quick config sanity check script
import { config } from './src/config';

const checks = [
  { ok: !!config.apiKey, msg: 'ASTER_API_KEY is set' },
  { ok: !!config.apiSecret, msg: 'ASTER_API_SECRET is set' },
  { ok: config.privateKey?.length === 64, msg: 'Private key is 64 chars' },
  { ok: [5, 10, 15, 50].includes(config.maxLeverage), msg: 'Leverage is valid' },
  { ok: config.maxPositionUsdt > 0, msg: 'MAX_POSITION_USDT > 0' },
  { ok: config.mode === 'dry-run', msg: 'Starting in dry-run mode' },
];

checks.forEach(({ ok, msg }) => {
  console.log(`${ok ? '✓' : '✗'} ${msg}`);
});
```

---

## Important Notes

- **Dry-run first**: Always validate strategy behavior in `MODE=dry-run` before live trading.
- **Leverage risk**: `MAX_LEVERAGE=50` means 50x amplified losses. Start with 5.
- **Price gate**: The `web3.prc` startup check (`limitPrice = 0.871`) prevents trading when ASTER price is too low. Only bypass with `SKIP_MIN_SPOT_CHECK=true` in non-production.
- **API endpoint**: All REST calls go to `https://fapi.asterdex.com`; WebSocket to `wss://fstream.asterdex.com/ws`.
- **State persistence**: Bot state survives restarts via `data/` directory — do not delete between sessions if you have open positions.
- **Valid leverages**: Only `5`, `10`, `15`, `50` are accepted by AsterDEX; any other value throws at startup.
