---
name: tiger-strategy
description: >-
  TIGER v2 — Multi-scanner trading system for Hyperliquid perps via Senpi MCP.
  5 signal patterns (BB compression breakout, BTC correlation lag, momentum breakout,
  mean reversion, funding rate arb), DSL v4 trailing stops, goal-based aggression engine,
  and risk guardrails. Configurable profit target over deadline. 12-cron architecture (10 TIGER + prescreener + ROAR meta-optimizer).
  Pure Python analysis. Requires Senpi MCP, python3, mcporter CLI, and OpenClaw cron system.
license: Apache-2.0
compatibility: >-
  Python 3.8+, no external deps (stdlib only). Requires mcporter
  (configured with Senpi auth) and OpenClaw cron system.
metadata:
  author: jason-goldberg
  version: "4.1"
  platform: senpi
  exchange: hyperliquid
---

# TIGER v2 — Multi-Scanner Goal-Based Trading

5 scanners. 1 goal. Configurable aggression. Mechanical exits.

**Philosophy:** WOLF hunts on instinct. TIGER calculates what it needs, then hunts exactly that much. Give it a budget, a target, and a deadline — it adjusts aggression automatically.

---

## Architecture

```
┌──────────────────────────────────────────┐
│           10 OpenClaw Crons              │
│  Compress(5m) Corr(3m) Momentum(5m)     │
│  Reversion(5m) Funding(30m) OI(5m)      │
│  Goal(1h) Risk(5m) Exit(5m) DSL(30s)    │
├──────────────────────────────────────────┤
│           Python Scripts                  │
│  tiger_lib.py  tiger_config.py           │
│  5 scanners / goal-engine / risk /       │
│  exit / oi-tracker / dsl-v4              │
├──────────────────────────────────────────┤
│           Senpi MCP (via mcporter)        │
│  market_list_instruments                  │
│  market_get_asset_data / market_get_prices│
│  create_position / close_position         │
│  edit_position / cancel_order             │
│  strategy_get_clearinghouse_state         │
│  leaderboard_get_markets                  │
│  account_get_portfolio                    │
├──────────────────────────────────────────┤
│           State Files                     │
│  tiger-config.json → tiger_config.py      │
│  state/{instance}/*.json (atomic writes)  │
└──────────────────────────────────────────┘
```

**State flow:** OI Tracker samples all assets → Scanners score signals by confluence → Goal Engine sets aggression → Agent enters via `create_position` → DSL manages trailing stops → Risk Guardian enforces limits → Exit Checker handles pattern-specific exits.

---

## Quick Start

1. Ensure Senpi MCP is connected (`mcporter list` shows `senpi`)
2. Create a custom strategy: `strategy_create_custom_strategy`
3. Fund the wallet: `strategy_top_up`
4. Run setup:
   ```bash
   python3 scripts/tiger-setup.py --wallet 0x... --strategy-id UUID \
     --budget 1000 --target 2000 --deadline-days 7 --chat-id 12345
   ```
5. Create 10 OpenClaw crons from `references/cron-templates.md`

**First hour:** OI Tracker needs ~1h of history before compression/reversion scanners can use OI data. Goal engine and risk guardian work immediately.

---

## 5 Signal Patterns

### 1. Compression Breakout (Primary)

BB squeeze with OI accumulation → price breaks bands.

| Factor | Weight | Threshold |
|--------|--------|-----------|
| BB squeeze (4h) | 0.25 | Width < `bbSqueezePercentile` (default: 35th) |
| BB breakout (1h) | 0.25 | Price closes outside 1h BB |
| OI building | 0.20 | OI rising > 5% in 1h |
| OI-price divergence | 0.15 | OI rising, price flat |
| Volume surge | 0.15 | Short vol > 1.5× long avg |
| RSI not extreme | 0.10 | RSI 30-70 |
| Funding aligned | 0.10 | Funding favors direction |
| ATR expanding | 0.05 | ATR > 2% |

### 2. BTC/ETH Correlation Lag (v2 — Multi-Leader, Multi-Window)

Leader (BTC or ETH) moves significantly → high-corr alts haven't caught up.

**Multi-window detection**: Checks 1h, 4h, 12h, and 24h rolling windows with scaled thresholds (1×, 1×, 1.5×, 2× base threshold). Catches sustained moves that single-candle checks miss.

**Multi-leader**: BTC and ETH are both tracked as leaders. ETH uses 0.8× threshold multiplier (more volatile). Each leader has its own alt list:
- **BTC alts**: SOL, DOGE, AVAX, LINK, ADA, DOT, NEAR, ATOM, FIL, INJ, SEI, SUI, TIA, JUP, WIF, PEPE, RENDER, FET, TAO, AR
- **ETH alts** (ecosystem-specific): OP, ARB, MATIC, STRK, AAVE, UNI, LDO, SNX, MKR, ENS, PENDLE, EIGEN, ENA, ETHFI, DYDX, CRV, COMP, SUSHI, IMX, BLUR

**Smart dedup**: If BTC and ETH move in the same direction, only BTC's alts are scanned (avoids redundancy). Max 4 alts total per scan to stay within 55s timeout.

| Factor | Weight | Threshold |
|--------|--------|-----------|
| Leader significant move | 0.20 | > `btcCorrelationMovePct` (default: 2%) in any rolling window |
| Alt lagging | 0.25 | Lag ratio ≥ 0.5 |
| Volume quiet | 0.15 | Alt volume not spiked yet |
| RSI safe | 0.10 | Not at extremes |
| SM aligned | 0.15 | Smart money direction matches |
| High correlation | 0.10 | Asset in leader's known alt list |
| Sufficient leverage | 0.05 | Max leverage ≥ `minLeverage` |

Window quality: STRONG (lag > 0.7), MODERATE (0.5-0.7), CLOSING (0.4-0.5).

### 3. Momentum Breakout

Strong price move with volume confirmation.

| Factor | Weight | Threshold |
|--------|--------|-----------|
| 1h move | 0.25 | > 1.5% |
| 2h move | 0.15 | > 2.5% |
| Volume surge | 0.20 | Ratio > 1.5× |
| 4h trend aligned | 0.15 | Move matches 4h direction |
| RSI not extreme | 0.10 | 30-70 |
| SMA aligned | 0.10 | Price correct side of SMA20 |
| ATR healthy | 0.05 | > 1.5% |

**DSL note:** Tighter Phase 1 retrace (0.012) — momentum reversals are fast.

### 4. Mean Reversion

Overextended asset with exhaustion signals → counter-trend.

| Factor | Weight | Threshold |
|--------|--------|-----------|
| RSI extreme (4h) | 0.20 | > `rsiOverbought` or < `rsiOversold` (required) |
| RSI extreme (1h) | 0.15 | Confirms 4h |
| RSI divergence | 0.20 | Divergence aligned with reversal |
| Price extended | 0.10 | > 10% move in 24h |
| Volume exhaustion | 0.15 | Declining volume on extension |
| At extreme BB | 0.10 | Price beyond BB bands |
| OI crowded | 0.15 | OI 15%+ above avg |
| Funding pays us | 0.10 | Collect funding in our direction |

### 5. Funding Rate Arb

Extreme funding → go opposite the crowd, collect income.

| Factor | Weight | Threshold |
|--------|--------|-----------|
| Extreme funding | 0.25 | Annualized > `minFundingAnnualizedPct` (default: 30%) |
| Trend aligned | 0.20 | SMA20 supports direction |
| RSI safe | 0.15 | Not extreme against us |
| OI stable | 0.15 | Funding source not collapsing |
| SM aligned | 0.10 | Smart money on our side |
| High daily yield | 0.10 | > 5% daily yield on margin |
| Volume healthy | 0.05 | > $10M daily |

**DSL note:** Wider retrace tiers (0.02+) — edge is income, not price direction. Risk Guardian auto-exits if funding flips.

---

## Goal Engine & Aggression

`goal-engine.py` runs hourly. Calculates required daily return and sets aggression:

| Aggression | Daily Rate Needed | Min Confluence | Trailing Lock | Behavior |
|------------|-------------------|----------------|---------------|----------|
| CONSERVATIVE | < 3% | 0.75 | 85% | Quality-only setups, tight locks |
| NORMAL | 3-8% | 0.65 | 70% | Standard operation |
| ELEVATED | 8-15% | 0.55 | 50% | Wider entries, lower threshold |
| ABORT | > 15% | 999 (never) | 90% | Stop new entries, tighten all |

---

## DSL v4 — Trailing Stop System

Per-position DSL state file. Combined runner (`dsl-v4.py`) checks all active positions every 30s.

**IMPORTANT**: The DSL cron must first check `activePositions` in TIGER state. If no positions are open, output `HEARTBEAT_OK` immediately and do NOT invoke `dsl-v4.py`. This prevents unnecessary session spam when TIGER is idle.

**Phase 1** (pre-Tier 1): Absolute floor. 3 consecutive breaches → close. Max duration: 90 minutes.

**Phase 2** (Tier 1+): Trailing tiers.

| Tier | ROE Trigger | Lock % of High-Water | Notes |
|------|-------------|---------------------|-------|
| 1 | 5% | 2% | Early profit signal |
| 2 | 10% | 6% | Momentum confirmed |
| 3 | 15% | 11% | Fills the old T3→T4 gap |
| 4 | 20% | 16% | Solid runner |
| 5 | 30% | 25% | Strong trend |
| 6 | 40% | 34% | Extended move |
| 7 | 50% | 44% | Exceptional run |
| 8 | 65% | 57% | Rare territory |
| 9 | 80% | 72% | Near-max |
| 10 | 100% | 90% | Moon lock |

**Stagnation TP:** ROE ≥ 8% + high-water stale 1h → auto-close.

### DSL Tuning by Pattern

| Pattern | Phase 1 Retrace | Tier Widths | Notes |
|---------|----------------|-------------|-------|
| COMPRESSION | 0.015 (standard) | Standard | Watch for false breakouts |
| CORRELATION_LAG | 0.015 | Standard | Tight absolute floor — window closes fast |
| MOMENTUM | 0.012 (tighter) | Standard | Fast reversals |
| MEAN_REVERSION | 0.015 | Medium | Expect 2-3 ATR move |
| FUNDING_ARB | 0.020+ (wider) | Wider | Income-based, needs room |

---

## Risk Management

| Rule | Limit | Config Key | Default |
|------|-------|-----------|---------|
| Max single trade loss | 3% of balance | `maxSingleLossPct` | 3 |
| Max daily loss | 8% of day-start balance | `maxDailyLossPct` | 8 |
| Max drawdown from peak | 15% | `maxDrawdownPct` | 15 |
| Max concurrent positions | 2 | `maxSlots` | 2 |
| OI collapse exit | OI drops > 25% in 1h | `oiCollapseThresholdPct` | 25 |
| Funding reversal exit | Funding flips on FUNDING_ARB | — | Auto |
| Deadline proximity | Final 24h → tighten all stops | — | Auto |

All percentage values are whole numbers (5 = 5%).

---

## Anti-Patterns

1. **NEVER enter in ABORT aggression.** Goal engine set ABORT for a reason.
2. **NEVER override DSL.** DSL auto-closes. Don't re-enter after DSL exit.
3. **NEVER hold FUNDING_ARB after funding flips.** The thesis is dead.
4. **NEVER chase momentum after 2h.** If you missed the 1h move, wait for the next one.
5. **NEVER enter reversion without 4h RSI extreme.** That's the required filter, not optional.
6. **NEVER run scanners without timeout wrapper.** `timeout 55` prevents overlap.
7. **NEVER mix xyz: assets into main scanner groups.** Prescreener isolates them into `group_xyz`; scanners hard-filter them out.

---

## Resilience Architecture

### xyz: Hard Isolation (3 layers)
1. **Prescreener**: Separates `xyz:` prefixed assets into `group_xyz`, never mixed with main groups a-f
2. **Scanner filtering**: Every scanner has `names = {n for n in names if not n.startswith("xyz:")}` guard
3. **Per-asset try/except**: Even if an xyz: asset leaks through, it's caught by the per-asset error handler

### Per-Asset Error Isolation
All 4 scanners (compression, correlation, momentum, reversion) wrap their per-asset analysis loops in try/except. One bad asset (missing data, API error, unexpected format) logs the error and skips — the rest of the scan continues normally. This prevents cascade failures where one problematic asset kills an entire scan run.

---

## API Dependencies

| Tool | Used By | Purpose |
|------|---------|---------|
| `market_list_instruments` | all scanners, oi-tracker | Asset discovery, OI, funding, volume |
| `market_get_asset_data` | all scanners | Candles (1h, 4h), funding |
| `market_get_prices` | correlation-scanner, risk-guardian | BTC price, alt prices |
| `leaderboard_get_markets` | correlation, funding scanners | SM alignment |
| `account_get_portfolio` | goal-engine | Portfolio balance |
| `strategy_get_clearinghouse_state` | goal-engine, risk-guardian | Margin, positions |
| `create_position` | agent (from scanner output) | Open positions |
| `close_position` | dsl-v4, risk-guardian, tiger-exit | Close positions |
| `edit_position` | risk-guardian | Resize positions |

---

## State Schema

See `references/state-schema.md` for full schema with field descriptions.

Key state files:
```
state/{instanceKey}/
├── tiger-state.json              # Positions, aggression, safety, daily stats
├── dsl-{ASSET}.json              # Per-position DSL trailing stop state
├── oi-history.json               # 24h OI time-series
├── trade-log.json                # All trades with outcomes
└── scan-history/                 # Scanner output history
```

All state files include `version`, `active`, `instanceKey`, `createdAt`, `updatedAt`. All writes use `atomic_write()`.

---

## Cron Setup

See `references/cron-templates.md` for ready-to-use OpenClaw cron payloads.

**Silence Policy — CRITICAL**: When a cron fires and the result is HEARTBEAT_OK, NO_POSITIONS, or no actionable signals:
- Do NOT notify Telegram
- Do NOT reply in chat
- Do NOT explain what the cron did
- Do NOT summarize the scan results
- Produce NO output of any kind — complete silence
Only speak (chat or Telegram) when something actionable happens: trade opened, trade closed, aggression changed, risk halt triggered, or an error that needs attention. Idle cycles = total silence.

**All crons run isolated.** No main session crons. No narration during scan cycles. The user should never see HEARTBEAT_OK, scanner reasoning, or "systems nominal" messages.

| # | Job | Interval | Script | Model Tier |
|---|-----|----------|--------|------------|
| 0 | Prescreener | 5 min | `prescreener.py` | Tier 1 |
| 1 | Compression Scanner | 5 min | `compression-scanner.py` | Tier 1 |
| 2 | Correlation Scanner | 3 min | `correlation-scanner.py` | Tier 1 |
| 3 | Momentum Scanner | 5 min | `momentum-scanner.py` | Tier 1 |
| 4 | Reversion Scanner | 5 min | `reversion-scanner.py` | Tier 1 |
| 5 | Funding Scanner | 30 min | `funding-scanner.py` | Tier 1 |
| 6 | OI Tracker | 5 min | `oi-tracker.py` | Tier 1 |
| 7 | Goal Engine | 1 hour | `goal-engine.py` | Tier 2 |
| 8 | Risk Guardian | 5 min | `risk-guardian.py` | Tier 2 |
| 9 | Exit Checker | 5 min | `tiger-exit.py` | Tier 2 |
| 10 | DSL Combined | 30 sec | `dsl-v4.py` | Tier 1 |
| 11 | ROAR Analyst | 8 hour | `roar-analyst.py` | Tier 2 |

**Tier 1** (fast/cheap): threshold checks, data collection, DSL math. Runs `isolated` with `delivery.mode: "none"` and explicit model (the configured model).
**Tier 2** (capable): aggression decisions, risk judgment, exit evaluation. Runs `isolated` with `delivery.mode: "announce"` and explicit model (the configured model). OpenClaw auto-suppresses HEARTBEAT_OK — only real content gets delivered.
**DSL** (Cron 10): Runs in `main` session (`systemEvent`) — needs position state context.

Scanners are staggered by 1-2 minutes to avoid mcporter rate limits (see cron-templates.md).

---

## ROAR — Recursive Optimization & Adjustment Runtime

ROAR is TIGER's meta-optimizer. It runs every 8 hours (+ ad-hoc every 5th trade), analyzes TIGER's trade log, and tunes execution parameters within bounded ranges. User intent (budget, target, risk limits) is never touched.

**What ROAR tunes** (within hard min/max bounds):
- Per-pattern confluence thresholds (0.25–0.85)
- Scanner thresholds (BB squeeze percentile, BTC correlation move, funding annualized)
- DSL retrace thresholds per phase (0.008–0.03)
- Trailing lock percentages per aggression level

**What ROAR never touches** (protected): budget, target, deadline, max_slots, max_leverage, maxDrawdownPct, maxDailyLossPct, maxSingleLossPct.

**Rules engine** (6 rules):
1. Win rate < 40% over 10+ trades → raise pattern confluence threshold by 0.05
2. Win rate > 70% over 10+ trades → lower threshold by 0.03 to catch more signals
3. Avg DSL exit tier < 2 → loosen phase1 retrace by 0.002 (let positions run)
4. Avg DSL exit tier ≥ 4 → tighten phase1 retrace by 0.001 (lock gains)
5. No entries in 48h for a pattern with 5+ trades → lower threshold by 0.02
6. Negative expectancy over 20+ trades → disable pattern for 48h (auto-re-enables)

**Safety**: revert-if-worse checks every cycle. If both win rate AND avg PnL degraded since last adjustment, auto-reverts to previous config.

Scripts: `roar-analyst.py` (engine), `roar_config.py` (bounds, state, revert logic).

---

## Expected Performance

| Metric | Target |
|--------|--------|
| Trades per day | 1-4 (quality over quantity) |
| Win rate | 55-65% |
| Profit factor | 1.8-2.5 |
| Daily return target | 1.5-3% (proven sustainable in Mission 1) |
| Best conditions | Volatile with clear setups (squeeze→breakout) |
| Worst conditions | Low-vol grind (few signals), choppy (false breakouts) |
| Fee drag (10x, round-trip) | ~1.8% of margin — factor into all PnL estimates |

---

## Known Limitations

- **OI history bootstrap.** Scanners need ~1h of OI data before OI-dependent signals are reliable.
- **mcporter latency.** ~6s per call. Scanners limited to 8 assets per cycle.
- **DSL is per-position.** Each position needs its own DSL state file.
- **Correlation scanner tracks BTC + ETH as leaders.** Doesn't detect moves led by other assets (e.g., SOL-led rallies).
- **Funding arb needs patience.** Edge is income over time; DSL must be wide enough.
- **Goal engine recalculates hourly.** Aggression can shift mid-trade.

---

## Optimization Levers

| Lever | Config Key | Conservative | Default | Aggressive |
|-------|-----------|-------------|---------|------------|
| Confluence threshold (NORMAL) | `minConfluenceScore.NORMAL` | 0.75 | 0.65 | 0.55 |
| BB squeeze percentile | `bbSqueezePercentile` | 20 | 25 | 35 |
| BTC corr move % | `btcCorrelationMovePct` | 4 | 3 | 2 |
| Max leverage | `maxLeverage` | 7 | 10 | 10 |
| Max slots | `maxSlots` | 1 | 2 | 3 |
| Daily loss halt % | `maxDailyLossPct` | 5 | 8 | 12 |
| Trailing lock (NORMAL) | `trailingLockPct.NORMAL` | 0.85 | 0.70 | 0.50 |
| Margin % per slot | `margin_pct_per_slot` | 0.25 | 0.30 | 0.40 |
| Volume ratio gate (momentum) | `volume_ratio_gate.MOMENTUM` | 1.5 | 1.2 | 1.0 |

---

## Gotchas

- `maxSingleLossPct` is a whole number: `5` = 5%.
- `minConfluenceScore` values are decimals (0.40 = 40%), NOT whole numbers — this is a weighted score 0-1.
- `trailingLockPct` values are decimals (0.60 = lock 60%).
- `triggerPct` in DSL tiers is ROE % (5 = 5% ROE), not price %.
- `lockPct` in DSL is % of high-water move to lock, not a retrace threshold.
- DSL reads `DSL_STATE_FILE` env var ONLY — positional args are silently ignored.
- `timeout 55` on all scanner scripts to prevent cron overlap.
- Cron stagger offsets: :00 compression, :01 momentum, :02 reversion, :03 OI, :04 risk+exit.

---

## Lessons from Live Trading

### Operational

- **DSL state file `active` field**: MUST include `active: true` or `dsl-v4.py` returns `{"status": "inactive"}` (line 22 check). This is the #1 gotcha when setting up new positions.
- **DSL invocation syntax**: `DSL_STATE_FILE=/path/to/file.json python3 scripts/dsl-v4.py COIN`
- **API latency**: `market_get_asset_data` ~4s/call, `market_list_instruments` ~6s. Max 8 assets per 55s scan window. This is NORMAL — design around it, don't blame it.
- **Correlation scanner timeouts**: Max 4 alts per scan (down from 6) to stay within 55s. Cron interval tightened to 3min for time-sensitive lag trades.
- **Compression scanner signals**: Requires `breakout: true` AND a `direction` to be actionable — a high compression score alone is not enough.
- **Test exit scripts after EVERY edit**: A crashing exit script is invisible and bleeds real money (lost ~$43 on PUMP from UnboundLocalError).
- **Config changes mean nothing if code doesn't read them**: Always verify the consuming code actually loads changed config keys.
- **Exchange SLs FIRST, DSL state SECOND**: Set exchange-level SL via `edit_position` immediately after entry. DSL is intelligence, exchange SL is safety net.
- **Zombie processes from frequent cron spawns**: Can accumulate under PID 1 and cause fork failures. Monitor and restart container if needed.
- **mcp-remote stdio proxy is unreliable**: Use direct streamable-http transport instead.

### Trading

- **Don't short compressed assets with building OI** — compression often resolves upward.
- **No duplicate positions**: Skip signals for assets already in `active_positions`.
- **Re-entry in opposite direction IS valid**: When signals are strong, entering the same asset in the opposite direction works.
- **DSL trailing stops >> fixed TP**: Every winning trade ran past where a fixed TP would have closed. Let winners run.
- **High-score signals (0.85+) justify overriding blacklists**: If original loss was small and new direction differs, take the trade.
- **`create_position` format**: Requires `orders` array with `coin`, `direction`, `leverage`, `marginAmount`, `orderType` fields.
- **ALO fee optimization**: Use `orderType: "FEE_OPTIMIZED_LIMIT"` + `ensureExecutionAsTaker: true` for entries AND non-urgent exits (stagnation, time-stop, daily target). Saves ~8 bps per fill. Use `MARKET` ONLY for: DSL breach closures, risk guardian hard stops, daily loss limit hits, and exchange-level SLs. Exchange SL `orderType` in `edit_position` must always be `MARKET`.
- **`close_position` syntax**: `mcporter call 'senpi.close_position(...)'`
- **CLOSE_NO_POSITION pattern**: Position may already be closed on-chain before DSL's close call — handle gracefully (not an error).
- **Position sizing: think in MARGIN first**: `per_slot_budget` = 30% of balance as margin. Multiply by leverage for notional. Old formula (balance÷slots÷leverage) left $730 on the table on PUMP.
- **Fees at 10x eat 1.8% of margin per round-trip**: Track balance from clearinghouse `accountValue`, NOT price deltas.
- **24h correlation signals go stale when 4h diverges**: Always check timeframe alignment. Lost ~$90 on SEI/OP/ARB LONG trades that reversed in 1 hour.
- **Volume ratio < 1.2 = no conviction for momentum entries**: XPL at 0.42 volume ratio stopped out immediately. Hard gate in config.
- **RSI > 70 on entry = red flag**: FARTCOIN entered at RSI 70.4, lost -13.7% ROE. Tightened RSI gates.
- **LIMIT SL on exchange = unreliable**: Always use `orderType: "MARKET"` for stop losses. LIMIT can fail on fast moves.
- **Realistic targets beat moonshots**: Mission 1 (18.5% in 2.5 days, ~3%/day) succeeded. Mission 3 (8%/day) ABORTed. Target 1.5-3%/day max.
- **2 slots > 3 slots at $3K**: Concentration beats diversification at small capital. Each position gets meaningful margin.
