---
name: shark
description: >-
  SHARK — Liquidation Cascade Front-Runner. Identifies leveraged position
  clusters on Hyperliquid, estimates liquidation zones from OI + funding data,
  and enters JUST BEFORE price reaches those zones — riding the forced cascade.
  3-phase signal pipeline: Liquidation Mapper (5min) → Proximity Scanner (2min)
  → Cascade Entry (2min). 9-tier DSL v5.3.1 trailing stops, risk guardian with
  cascade invalidation (OI increase = immediate cut). Max 2 concurrent positions,
  7-10x leverage, 18% margin per trade. Most aggressive strategy in the Senpi
  ecosystem. Use when user wants to trade liquidation cascades, front-run
  forced liquidations, or set up cascade-based trading on Hyperliquid.
license: Apache-2.0
compatibility: >-
  Requires python3, mcporter (configured with Senpi auth), OpenClaw cron,
  and DSL v5.3.1 skill (dsl-dynamic-stop-loss). Hyperliquid perps only.
metadata:
  author: jason-goldberg
  version: "1.0.0"
  platform: senpi
  exchange: hyperliquid
---

# SHARK — Liquidation Cascade Front-Runner

SHARK is the most aggressive strategy in the Senpi ecosystem. It identifies
where leveraged positions are clustered on Hyperliquid, estimates where
liquidation zones sit, and enters JUST BEFORE price reaches those zones —
riding the forced cascade that follows.

## How It's Different

```
WOLF/FOX:  Enter WITH momentum early (leaderboard signals)
SHARK:     Enter AHEAD of forced liquidation cascades
```

SHARK doesn't care about chart patterns, smart money signals, or funding
rate extremes. It cares about one thing: where are the liquidation clusters,
and is price moving toward them?

## Core Thesis

When OI builds up at a price level with high leverage, the liquidation zone
for those positions is calculable. When price approaches the cluster, the
first liquidations trigger forced selling/buying that pushes price further,
triggering more liquidations. This is the cascade — mechanical, predictable
in direction, and violent in execution.

## Data Sources

All data comes from Senpi MCP. No external APIs needed.

| Data | Tool | Purpose |
|------|------|---------|
| Aggregate OI | `market_list_instruments` | Where OI is concentrated |
| Funding rates | `market_list_instruments` | Which side is over-leveraged |
| Funding history | `market_get_asset_data` | Leverage estimation |
| Price candles | `market_get_asset_data` | Momentum, proximity |
| Order book L2 | `market_get_asset_data` | Thin book detection |
| SM concentration | `leaderboard_get_markets` | Smart money positioning |
| Prices | `market_get_prices` | Real-time for DSL |

## Signal Pipeline

### Phase 1: Liquidation Mapper (every 5 min)

Estimates where liquidation clusters sit for all viable assets.

1. Stores OI + price + funding snapshots from `market_list_instruments`
2. Identifies OI buildup periods and estimates average entry prices
3. Calculates liquidation zones: `entry × (1 ± 1/leverage)`
4. Scores by: OI size (0.25), leverage (0.20), proximity (0.25),
   momentum (0.20), book depth (0.10)
5. Score ≥ 0.55 → asset enters **STALKING** watchlist

### Phase 2: Proximity Scanner (every 2 min)

Watches STALKING assets as price approaches the zone.

| Signal | Weight |
|--------|--------|
| Price within 3% of zone | Required gate |
| Momentum accelerating toward zone | 0.30 |
| OI starting to crack (>1% drop in 10min) | 0.30 |
| Volume surge (15min > 2x avg) | 0.20 |
| Book thinning on cascade side | 0.20 |

Proximity ≥ 0.60 AND within 3% → asset enters **STRIKE** state.

### Phase 3: Cascade Entry (every 2 min)

The moment the cascade begins. Needs ≥ 2 triggers firing:

| Trigger | Confidence |
|---------|-----------|
| OI drops >3% in 5min interval | HIGH |
| Price breaks into liquidation zone | HIGH |
| Funding rate spiking | MEDIUM |
| Volume explosion (5min > 3x avg) | MEDIUM |
| SM already positioned in cascade direction | HIGH |

**Direction:** Longs liquidating → SHORT. Shorts liquidating → LONG.

## Position Management

- **15-20% margin** per trade (of budget)
- **Max 2 concurrent** — cascades are correlated
- **7-10x leverage** — not higher (whipsaw risk)
- **DSL v5.3.1** trailing stops with 9 tiers

### DSL Configuration

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Phase 1 retrace | 0.025 | Moderate — cascades can bounce |
| Hard timeout | 30 min | No cascade in 30min = wrong thesis |
| Weak peak cut | 15 min | Peak ROE < 3% declining → exit |
| Dead weight cut | 10 min | Never positive = no cascade |
| Phase 2 tiers | 9-tier | Lock profits aggressively |

### Tier Structure

| Tier | ROE Trigger | Lock % |
|------|------------|--------|
| T1 | 5% | 2% |
| T2 | 10% | 5% |
| T3 | 20% | 14% |
| T4 | 30% | 24% |
| T5 | 40% | 34% |
| T6 | 50% | 44% |
| T7 | 65% | 56% |
| T8 | 80% | 72% |
| T9 | 100% | 90% |

## Risk Management

| Rule | Limit |
|------|-------|
| Max concurrent positions | 2 |
| Max daily loss | 12% of budget |
| Max drawdown from peak | 25% |
| Max single trade loss | 5% of account |
| Correlation guard | Max 1 BTC-correlated position |
| Cascade invalidation | OI increases >2% after entry → cut immediately |
| Max entries per day | 6 (unless ROE positive) |
| Consecutive loss cooldown | 3 losses → 45min pause |

**Cascade invalidation is the most important rule.** If OI is going UP after
entry, there's no cascade. Cut immediately — don't wait for DSL.

## Anti-Patterns (Hard-Coded)

1. **NEVER enter if OI is INCREASING** — rising OI = new positions, not liquidations
2. **NEVER chase a started cascade** — OI dropped 10%+, price moved 5%+ = too late
3. **NEVER hold through a bounce** — if OI stabilizes and price reverses 2%+, exit
4. **Max 1 BTC-correlated trade** — BTC cascade = everything cascades
5. **Cascade invalidation is immediate** — OI increases >2% → close now

## Cron Architecture (8 crons)

| # | Job | Interval | Session | Script |
|---|-----|----------|---------|--------|
| 1 | OI Tracker | 5 min | isolated | `shark-oi-tracker.py` |
| 2 | Liq Mapper | 5 min | isolated | `shark-liq-mapper.py` |
| 3 | Proximity | 2 min | isolated | `shark-proximity.py` |
| 4 | Entry | 2 min | main | `shark-entry.py` |
| 5 | Movers | 3 min | main | `shark-movers.py` |
| 6 | Risk Guardian | 5 min | isolated | `shark-risk.py` |
| 7 | DSL v5.3.1 | 3 min | isolated | `dsl-v5.py` (shared) |
| 8 | Health | 10 min | isolated | `shark-health.py` |

### Emerging Movers Integration

`shark-movers.py` runs the Emerging Movers scanner (SM rank acceleration)
and opens positions when IMMEDIATE_MOVER signals fire. This keeps capital
productive between cascade events. Same wallet, same risk rails, same DSL.

Entry criteria are stricter than standalone EM:
- IMMEDIATE signal, not erratic, not low velocity
- 15+ traders (vs EM's 10), top 30 rank, velocity >= 0.03
- 4h price change aligned with direction
- All SHARK risk rules still apply (gate, capacity, correlation guard)

See [references/cron-templates.md](references/cron-templates.md) for full payloads.

## State Files

See [references/state-schema.md](references/state-schema.md) for complete schemas.

```
state/{strategyKey}/
  shark-state.json         # Watchlists + active positions
  shark-oi-history.json    # 24h of OI snapshots
  shark-liq-map.json       # Estimated liquidation zones
  trade-counter.json       # Daily counter + gates
  peak-balance.json        # Peak balance for drawdown

dsl/{strategyId}/
  {ASSET}.json             # DSL v5.3.1 per position
```

## Setup

Before running setup, create a strategy wallet via `strategy_create_custom_strategy` (include `skill_name: "shark"`, `skill_version: "1.0.0"` — see `references/skill-attribution.md`).

```bash
python3 scripts/shark-setup.py \
  --wallet 0x... \
  --strategy-id UUID \
  --budget 5000 \
  --chat-id 12345
```

Setup will:
1. Validate wallet and strategy ID against Senpi
2. Calculate all parameters from budget
3. Create strategy registry entry
4. Initialize state directories
5. Output cron templates (agent creates them via OpenClaw cron)

**OI tracker needs ~1 hour of data before signals are reliable.**

## Notification Policy

**Notify:** Position opened, position closed, risk halt, cascade invalidation,
DSL tier upgrades.

**Never notify:** Scanner heartbeats, OI collection, risk all-clear, routine DSL ticks.

## Dependencies

- **python3** — all scripts
- **mcporter** — Senpi MCP calls (configured with auth)
- **OpenClaw cron** — 7 scheduled jobs
- **DSL v5.3.1 skill** — `~/.agents/skills/dsl-dynamic-stop-loss/` (must be installed)

## Success Metrics (1 week)

| Metric | Target |
|--------|--------|
| Trades entered | 3-8 |
| Win rate | >55% |
| Avg winner ROE | >15% |
| Avg loser ROE | <-8% |
| Cascade invalidation exits | <30% |
| Max single loss | <5% of account |
