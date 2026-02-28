---
name: wolf-strategy
description: >-
  WOLF v6 — Fully autonomous multi-strategy trading for Hyperliquid perps via Senpi MCP.
  Manages multiple strategies simultaneously, each with independent wallets, budgets, slots,
  and DSL configs. 7-cron architecture with Emerging Movers scanner (90s, FIRST_JUMP + IMMEDIATE_MOVER),
  DSL v4 trailing stops (combined runner every 3min, 4-tier at 5/10/15/20% ROE),
  SM flip detector (5min), watchdog (5min), portfolio updates (15min),
  opportunity scanner v6 (15min, BTC macro + hourly trend + disqualifiers),
  and health checks (10min). Same asset can be traded in different strategies simultaneously.
  Enter early on first jumps, not at confirmed peaks. Minimum 7x leverage required.
  Requires Senpi MCP connection, python3, mcporter CLI, and OpenClaw cron system.

---

# WOLF v6 — Autonomous Multi-Strategy Trading

The WOLF hunts for its human. It scans, enters, exits, and rotates positions autonomously — no permission needed. When criteria are met, it acts. Speed is edge.

**Proven:** +$1,500 realized, 25+ trades, 65% win rate, single session on $6.5k budget.

**v6: Multi-strategy support.** Each strategy has independent wallet, budget, slots, and DSL config. Same asset can be held in different strategies simultaneously (e.g., Strategy A LONG HYPE + Strategy B SHORT HYPE).

---

## Multi-Strategy Architecture

### Strategy Registry (`wolf-strategies.json`)
Central config holding all strategies. Created/updated by `wolf-setup.py`.

```
wolf-strategies.json
├── strategies
│   ├── wolf-abc123 (Aggressive Momentum, 3 slots, 10x)
│   └── wolf-xyz789 (Conservative XYZ, 2 slots, 7x)
└── global (telegram, workspace)
```

### Per-Strategy State
Each strategy gets its own state directory:
```
state/
├── wolf-abc123/
│   ├── dsl-HYPE.json
│   └── dsl-SOL.json
└── wolf-xyz789/
    ├── dsl-HYPE.json    # Same asset, different strategy, no collision
    └── dsl-GOLD.json
```

### Signal Routing
When a signal fires, it's routed to the best-fit strategy:
1. Which strategies have empty slots?
2. Does any strategy already hold this asset? (skip within strategy, allow cross-strategy)
3. Which strategy's risk profile matches? (aggressive gets FIRST_JUMPs, conservative gets DEEP_CLIMBERs)
4. Route to best-fit -> open on that wallet -> create DSL state in that strategy's dir

### Adding a Strategy
```bash
python3 scripts/wolf-setup.py --wallet 0x... --strategy-id UUID --budget 2000 \
    --chat-id 12345 --name "Conservative XYZ" --dsl-preset conservative
```
This adds to the registry without disrupting running strategies. Disable with `enabled: false` in the registry.

---

## Entry Philosophy — THE Most Important Section

**Enter before the peak, not at the top.**

Leaderboard rank confirmation LAGS price. When an asset jumps from #31->#16 in one scan, the price is moving NOW. By the time it reaches #7 with clean history, the move is over. Speed is edge.

**Core principle:** 2 reasons at rank #25 with a big jump = ENTER. 4+ reasons at rank #5 = SKIP (already peaked).

---

## Quick Start

1. Ensure Senpi MCP is connected (`mcporter list` should show `senpi`)
2. Create a custom strategy wallet: use `strategy_create_custom_strategy` via mcporter
3. Fund the wallet via `strategy_top_up` with your budget
4. Run setup: `python3 scripts/wolf-setup.py --wallet 0x... --strategy-id UUID --budget 6500 --chat-id 12345`
5. Create the 7 OpenClaw crons using templates from `references/cron-templates.md`
6. The WOLF is hunting

To add a second strategy, run `wolf-setup.py` again with a different wallet/budget. It adds to the registry.

---

## Architecture — 7 Cron Jobs

| # | Job | Interval | Session | Script | Purpose |
|---|-----|----------|---------|--------|---------|
| 1 | Emerging Movers | **90s** | **main** | `scripts/emerging-movers.py` | Hunt FIRST_JUMP + IMMEDIATE_MOVER signals — primary entry trigger |
| 2 | DSL Combined | **3min** | isolated | `scripts/dsl-combined.py` | Trailing stop exits for ALL open positions across ALL strategies |
| 3 | SM Flip Detector | 5min | isolated | `scripts/sm-flip-check.py` | Cut positions where SM conviction collapses |
| 4 | Watchdog | 5min | isolated | `scripts/wolf-monitor.py` | Per-strategy margin buffer, liq distances, rotation candidates |
| 5 | Portfolio Update | 15min | isolated | (agent-driven) | Per-strategy PnL reporting to user |
| 6 | Opportunity Scanner | 15min | **main** | `scripts/opportunity-scan-v6.py` | Deep-dive 4-pillar scoring with BTC macro, hourly trend, disqualifiers |
| 7 | Health Check | 10min | isolated | `scripts/job-health-check.py` | Per-strategy orphan DSL detection, state validation |

**v6 change:** One set of crons for all strategies. Each script reads `wolf-strategies.json` and iterates all enabled strategies internally.

**v6 change:** Opportunity Scanner v6 replaces the old scanner with BTC macro context, hourly trend filter, hard disqualifiers, parallel candle fetches, and cross-scan momentum tracking.

### Model Selection Per Cron — 3-Tier Approach

Configure per-cron in OpenClaw. Step down from your primary model for isolated crons to save ~60-70% on those runs.

**Example model IDs** (confirmed working on OpenClaw):

| Tier | Role | Crons | Example Model IDs |
|------|------|-------|--------------------|
| **Primary** | Complex judgment, multi-strategy routing | Emerging Movers, Opportunity Scanner | Your configured model (runs on main session) |
| **Mid** | Structured tasks, script output parsing | DSL Combined, Portfolio Update, Health Check | `anthropic/claude-sonnet-4-20250514`, `openai/gpt-4o`, `google/gemini-2.0-flash` |
| **Budget** | Simple threshold checks, binary decisions | SM Flip, Watchdog | `anthropic/claude-haiku-4-5`, `openai/gpt-4o-mini`, `google/gemini-2.0-flash-lite` |

| Cron | Session | Model Tier | Reason |
|------|---------|-----------|--------|
| Emerging Movers | main | **Primary** | Multi-strategy routing judgment, entry decisions |
| Opportunity Scanner | main | **Primary** | Complex 4-pillar analysis, conflict resolution |
| DSL Combined | isolated | Mid | Script output parsing, rule-based close/alert |
| Portfolio Update | isolated | Mid | Clearinghouse data formatting, no decisions |
| Health Check | isolated | Mid | Rule-based file repair, action routing |
| SM Flip Detector | isolated | Budget | Binary: conviction≥4 + 100 traders → close |
| Watchdog | isolated | Budget | Threshold checks → alert |

**Single-model option:** All 7 crons can run on one model. Simpler but costs more for the 5 isolated crons that do structured/binary work.

**Model ID gotchas:**
- Pick one model per tier from your provider. The tier concept (Primary / Mid / Budget) matters more than the specific model — any provider's equivalent works.
- Budget should be the cheapest model that can follow explicit if/then rules. Mid should handle structured JSON parsing reliably.
- Agents are often not model-aware — they may suggest deprecated IDs (e.g. `claude-3-5-haiku-20241022`) or hallucinate model names. Always use the exact IDs from the table above.
- If a cron fails to create or run due to an invalid model ID, fall back to your primary model for that cron. A working cron on the "wrong" tier is better than a broken cron.
- When in doubt, use your primary model for all 7 crons (single-model option) and optimize tiers later.

## Cron Setup

**Critical:** Crons are **OpenClaw crons**, NOT senpi crons. WOLF uses two session types:
- **Main session** (`systemEvent`): Emerging Movers + Opportunity Scanner. These share the primary session context for accumulated routing knowledge.
- **Isolated session** (`agentTurn`): DSL Combined, Portfolio, Health Check, SM Flip, Watchdog. Each runs in its own session — no context pollution, enables cheaper model tiers.

Create each cron using the OpenClaw cron tool. The exact mandate text for each cron is in **`references/cron-templates.md`**. Read that file, replace the placeholders (`{TELEGRAM}`, `{SCRIPTS}`, and `{WORKSPACE}` in v6), and create all 7 crons.

**v6 simplification:** No more per-wallet/per-strategy placeholders in cron mandates. Scripts read all strategy info from the registry.

---

## Autonomy Rules

The WOLF operates autonomously by default. The agent does NOT ask permission to:
- Open a position when entry checklist passes
- Close a position when DSL triggers or conviction collapses
- Rotate out of weak positions into stronger signals
- Cut dead weight (SM conv 0, negative ROE, 30+ min)

The agent DOES notify the user (via Telegram) after every action.

---

## Entry Signals — Priority Order

### 1. FIRST_JUMP (Highest Priority)

**What:** Asset jumps 10+ ranks from #25+ in ONE scan AND was not in previous scan's top 50 (or was at rank >= #30).

**Action:** Enter IMMEDIATELY. This is the money signal. Route to best-fit strategy with available slots.

**Checklist:**
- `isFirstJump: true` in scanner output
- **2+ reasons is enough** (don't require 4+)
- **vel > 0 is sufficient** (velocity hasn't had time to build on a first jump)
- Max leverage >= 7x (check `max-leverage.json`)
- Slot available in target strategy (or rotation justified)
- >= 10 SM traders (crypto); for XYZ equities, ignore trader count

**What to ignore:**
- Erratic rank history — the scanner excludes the current jump from erratic checks.
- Low velocity — first jumps haven't had time to build velocity.

**If CONTRIB_EXPLOSION accompanies it:** Double confirmation. Even stronger entry.

### 2. CONTRIB_EXPLOSION

**What:** 3x+ contribution increase in one scan from asset at rank #20+.

**Action:** Enter even if rank history looks "erratic." The contrib spike IS the signal regardless of prior rank bouncing.

**Never downgraded for erratic history.** Often accompanies FIRST_JUMP for double confirmation.

### 3. DEEP_CLIMBER

**What:** Steady climb from #30+, positive velocity (>= 0.03), 3+ reasons, clean rank history.

**Action:** Enter when it crosses into top 20. Route to conservative strategy if available.

### 4. NEW_ENTRY_DEEP

**What:** Appears in top 20 from nowhere (wasn't in top 50 last scan).

**Action:** Instant entry.

### 5. Opportunity Scanner (Score 175+)

Runs every 15min. v6 scanner with BTC macro context, hourly trend classification, and hard disqualifiers. Complements Emerging Movers as a secondary signal source for deeper technical analysis.

---

## Anti-Patterns — When NOT to Enter

- **NEVER enter assets already at #1-10.** That's the top, not the entry. Rank = what already happened.
- **NEVER wait for a signal to "clean up."** By the time rank history is smooth and velocity is high, the move is priced in.
- **4+ reasons at rank #5 = SKIP.** The asset already peaked. You'd be buying the top.
- **2 reasons at rank #25 with a big jump = ENTER.** The move is just starting.
- **Leaderboard rank != future price direction.** Rank reflects past trader concentration. Price moves first, rank follows.
- **Negative velocity + no jump = skip.** Slow bleeders going nowhere.
- **Oversold shorts** (RSI < 30 + extended 24h move) = skip.

---

## Late Entry Anti-Pattern

This deserves its own section because it's the #1 way to lose money with WOLF.

**The pattern:** Scanner fires FIRST_JUMP for ASSET at #25->#14. You hesitate. Next scan it's #10. Next scan #7 with 5 reasons and clean history. NOW it looks "safe." You enter. It reverses from #5.

**The fix:** Enter on the FIRST signal or don't enter at all. If you missed it, wait for the next asset. There's always another FIRST_JUMP coming.

**Rule:** If an asset has been in the top 10 for 2+ scans already, it's too late. Move on.

---

## Phase 1 Auto-Cut

Positions that never gain momentum get cut automatically.

**Rules:**
- **90-minute maximum** in Phase 1 (pre-Tier 1 DSL). If ROE never hits 5% in 90 minutes, close.
- **Weak peak early cut:** If peak ROE was < 3% and ROE is now declining -> close after 45 minutes. Don't wait 90.
- **Dead weight:** SM conviction = 0, negative ROE, position open 30+ minutes -> instant cut regardless of phase.

**Why:** Phase 1 positions have no trailing stop protection. They're running on faith. If SM conviction doesn't materialize in 90 min, the thesis is wrong.

---

## Exit Rules

### 1. DSL v4 Mechanical Exit (Trailing Stops)

All trailing stops handled automatically by `dsl-combined.py` across all strategies.

### 2. SM Conviction Collapse
Conv drops to 0 or 4->1 with mass trader exodus -> instant cut.

### 3. Dead Weight
Conv 0, negative ROE, 30+ min -> instant cut.

### 4. SM Flip
Conviction 4+ in the OPPOSITE direction with 100+ traders -> cut immediately.

### 5. Race Condition Prevention
When ANY job closes a position -> immediately:
1. Set DSL state `active: false` in `state/{strategyKey}/dsl-{ASSET}.json`
2. Alert user
3. Evaluate: empty slot in that strategy for next signal?

**v6 note:** Since DSL is a combined runner iterating all strategies, no per-position crons to manage. Just set `active: false` in the state file.

---

## DSL v4 — Trailing Stop System

### Phase 1 (Pre-Tier 1): Absolute floor
- LONG floor = entry x (1 - 5%/leverage)
- SHORT floor = entry x (1 + 5%/leverage)
- 3 consecutive breaches -> close
- **Max duration: 90 minutes** (see Phase 1 Auto-Cut above)

### Phase 2 (Tier 1+): Trailing tiers

| Tier | ROE Trigger | Lock % of High-Water | Breaches to Close |
|------|-------------|---------------------|-------------------|
| 1 | 5% | 50% | 2 |
| 2 | 10% | 65% | 2 |
| 3 | 15% | 75% | 2 |
| 4 | 20% | 85% | 1 |

### Stagnation Take-Profit
Auto-close if ROE >= 8% and high-water stale for 1 hour.

### DSL State File
Each position gets `state/{strategyKey}/dsl-{ASSET}.json`. The combined runner iterates all active state files across all strategies. See `references/state-schema.md` for the full schema and critical gotchas (triggerPct not threshold, lockPct not retracePct, etc.).

---

## Opportunity Scanner v6

The v6 scanner addresses all reliability issues from the previous version:

| Fix | What Changed |
|-----|-------------|
| **BTC Macro Context** | Stage 0 analyzes BTC 4h+1h trend. Prevents alt longs during BTC crashes. |
| **Hourly Trend Filter** | `classify_hourly_trend()` analyzes swing structure. Counter-trend on hourly = hard skip. |
| **Hard Disqualifiers** | 6 conditions that skip assets entirely (not just penalize score). |
| **Parallel Fetches** | ThreadPoolExecutor for candle fetches (~20s vs ~60s). |
| **Cross-Scan Momentum** | `scoreDelta` and `scanStreak` from scan history. |
| **Configurable Thresholds** | Read from `history/scanner-config.json`. |
| **Per-TF Error Recovery** | One failed timeframe doesn't kill the asset. |
| **Position Awareness** | Checks ALL strategies' DSL states for conflicts. |
| **No Cold Start** | First scan produces baseline results immediately. |

### Hard Disqualifiers
1. Counter-trend on hourly (the "$346 lesson")
2. Extreme RSI (<20 shorts, >80 longs)
3. Counter-trend on 4h with strength >50
4. Volume dying (<0.5x on both timeframes)
5. Heavy unfavorable funding (>50% annualized)
6. BTC macro headwind >30 points

Disqualified assets appear in output with `reason` and `wouldHaveScored` for transparency.

---

## Rotation Rules

When slots are full in a strategy and a new FIRST_JUMP or IMMEDIATE fires:
- **Rotate if:** new signal is FIRST_JUMP or has 3+ reasons + positive velocity AND weakest position in that strategy is flat/negative ROE with SM conv 0-1
- **Hold if:** current position in Tier 2+ or trending up with SM conv 3+
- **Cross-strategy:** If one strategy is full but another has slots, route to the available strategy instead of rotating

---

## Budget Scaling

All sizing is calculated from budget (30% per slot):

| Budget | Slots | Margin/Slot | Leverage | Daily Loss Limit |
|--------|-------|-------------|----------|------------------|
| $500 | 2 | $150 | 7x | -$75 |
| $2,000 | 2 | $600 | 10x | -$300 |
| $6,500 | 3 | $1,950 | 10x | -$975 |
| $10,000+ | 3-4 | $3,000 | 10x | -$1,500 |

**Minimum leverage: 7x.** If max leverage for an asset is below 7x, skip it. Low leverage = low ROE = DSL tiers never trigger = dead position.

**Auto-Delever:** If a strategy's account drops below its `autoDeleverThreshold` -> reduce max slots by 1, close weakest in that strategy.

---

## Position Lifecycle

### Opening
1. Signal fires -> validate checklist -> route to best-fit strategy
2. `create_position` on that strategy's wallet (use `leverageType: "ISOLATED"` for XYZ assets)
3. Create DSL state file in `state/{strategyKey}/dsl-{ASSET}.json` with `strategyKey` field
4. Alert user

### Closing
1. Close via `close_position` (or DSL auto-closes)
2. **Immediately** set DSL state `active: false`
3. Alert user with strategy name for context
4. Evaluate: empty slot in that strategy for next signal?

---

## Margin Types

- **Cross-margin** for crypto (BTC, ETH, SOL, etc.)
- **Isolated margin** for XYZ DEX (GOLD, SILVER, TSLA, etc.) — set `leverageType: "ISOLATED"` and `dex: "xyz"`
- Same wallet holds both cross crypto + isolated XYZ side by side

---

## XYZ Equities

XYZ DEX assets (GOLD, SILVER, TSLA, AAPL, etc.) behave differently:

- **Ignore trader count.** XYZ equities often have low SM trader counts — this doesn't invalidate the signal.
- **Use reason count + rank velocity** as primary quality filter instead.
- **Always use isolated margin** (`leverageType: "ISOLATED"`, `dex: "xyz"`).
- **Check max leverage** — many XYZ assets cap at 5x or 3x. If below 7x, skip.

---

## Token Optimization & Context Management

**Model tiers:** See "Model Selection Per Cron" table. Primary for main-session crons, Mid/Budget for isolated crons. Configure per-cron in OpenClaw.

**Heartbeat policy:** If script output contains no actionable signals, output HEARTBEAT_OK immediately. Do not reason about what wasn't found.

**Context isolation (multi-signal runs):** Read `wolf-strategies.json` ONCE per cron run. Build a complete action plan before executing any tool calls. Send ONE consolidated Telegram per run, not one per signal.

**Skip rules:** Skip redundant checks when data < 3 min old. If all slots full and no FIRST_JUMPs → skip scanner processing. If SM check shows no flips and < 5 min old → skip.

---

## Known Limitations

- **Watchdog blind spot for XYZ isolated:** The watchdog monitors cross-margin buffer but can't see isolated position liquidation distances in the same way. XYZ positions rely on DSL for protection.
- **Health check only sees crypto wallet:** The health check can't see XYZ positions for margin calculations. Total equity may differ.
- **Scanner needs history for momentum:** Cross-scan momentum (scoreDelta, scanStreak) requires at least 2 scans. First scan produces scored results immediately but without momentum data.

---

## Backward Compatibility

- `wolf_config.py` auto-migrates legacy `wolf-strategy.json` to registry format on first load
- Old `dsl-state-WOLF-*.json` files detected and migrated to `state/wolf-{id}/dsl-*.json`
- All scripts work with both layouts during transition
- All DSL logic is handled by `dsl-combined.py` (multi-strategy runner)

---

## Troubleshooting

See `references/learnings.md` for known bugs, gotchas, and trading discipline rules. Key ones:
- **`dryRun: true` actually executes** — NEVER use dryRun
- **Max leverage varies per asset** — always check `max-leverage.json`
- **`close_position` is the close tool** — not `edit_position`
- **Tier 1 lock != guaranteed profit** — lock is from high-water, not entry

---

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `scripts/wolf-setup.py` | Setup wizard — adds strategy to registry from budget |
| `scripts/wolf_config.py` | Shared config loader — all scripts import this |
| `scripts/emerging-movers.py` | Emerging Movers v4 scanner (FIRST_JUMP, IMMEDIATE, CONTRIB_EXPLOSION) |
| `scripts/dsl-combined.py` | DSL v4 combined trailing stop engine (all positions, all strategies) |
| `scripts/sm-flip-check.py` | SM conviction flip detector (multi-strategy) |
| `scripts/wolf-monitor.py` | Watchdog — per-strategy margin buffer + position health |
| `scripts/opportunity-scan-v6.py` | Opportunity Scanner v6 (BTC macro, hourly trend, disqualifiers) |
| `scripts/job-health-check.py` | Per-strategy orphan DSL / state validation |
