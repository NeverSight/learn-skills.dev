---
name: run-simulations
description: "Use BEFORE and AFTER running trading engine simulations. Helps with: (1) SETUP - choosing configs, selecting segments via segment collections, batch sizing (recommend 2,000-3,000 runs); (2) EXECUTION - running batch simulations with --collection; (3) ANALYSIS - comprehensive diagnostics after runs. Triggers on: 'run simulations', 'test configs', 'batch simulation', 'analyze sim results', 'which configs to test', 'how many segments', 'simulation setup'."
---

# Run Simulations Skill

You are helping set up and run trading engine simulations, then performing comprehensive diagnostic analysis.

## Current Phase: DUAL-FOCUS (Validation + Optimization)

**System confidence: ~85% accurate.** The simulation system is largely trustworthy, but discrepancies still exist and are critical to find.

### Priority #1: ACCURACY DISCREPANCIES (Most Important)
Any gap between expected vs actual behavior is a potential bug or misunderstanding. These must be surfaced prominently:
- Does behavior match config parameters?
- Are there logical inconsistencies in the data?
- Do results align with what the strategy SHOULD produce?

**When you spot a discrepancy, flag it prominently.** Even small accuracy issues compound over thousands of trades.

### Priority #2: PROFIT OPTIMIZATION (Active Research)
With a trustworthy system, we're now actively researching:
- Which configs perform best?
- What market conditions favor which strategies?
- How do parameters affect PnL?

Surface interesting profit patterns AND accuracy concerns. Both matter now.

---

**IMPORTANT**: This skill should be invoked BEFORE running simulations to help with setup decisions (config selection, segment selection via collections, batch sizing).

## Recommended Batch Size

**Current recommendation: 2,000-3,000 simulations per batch.**
- Runs quickly (~30-60 seconds with tick caching)
- Provides statistically meaningful results
- More than 3,000 doesn't add much value at current stage
- Formula: configs × segments = total runs (e.g., 20 configs × 100 segments = 2,000 runs)

## Phase 1: Setup & Run

### ⚠️ USER INPUT TAKES PRIORITY

**If the user provides ANY arguments, instructions, or context when invoking this skill, those take absolute priority over all defaults below.**

- User says "run config X" → run config X, ignore default config selection
- User says "test these 5 segments" → test those 5 segments, ignore default segment query
- User asks a specific question → answer that question, don't run the full default workflow
- User provides partial instructions → fill in gaps with defaults, but honor what they specified

**The defaults below are ONLY for when the skill is invoked with no arguments at all.**

---

### Default Behavior (no args only)
Pick a diverse spread of configs and segments using **segment collections** (legacy filters are deprecated):
1. Query available configs: `SELECT name, config FROM strategy_configs ORDER BY name`
2. Select 10-20 configs covering different indicator types (EMA, RSI, Bollinger, combined)
3. Choose or create a segment collection (AND-only annotations in v1):
   ```bash
   bun src/systems/trading-engine/bd-segments.ts list
   bun src/systems/trading-engine/bd-segments.ts create --name=high-activity --annotations=high_activity --limit=100
   bun src/systems/trading-engine/bd-segments.ts preview --name=high-activity
   ```
4. Run batch simulation:
   ```bash
   bun src/systems/trading-engine/batch-runner.ts --config-pattern="<pattern>" --collection=high-activity --save
   ```

### Batch Runner CLI Reference

**Location:** `src/systems/trading-engine/batch-runner.ts`

**Usage:**
```bash
bun src/systems/trading-engine/batch-runner.ts [options]
```

**Options:**
| Option | Short | Description |
|--------|-------|-------------|
| `--config=ID` | `-c` | Strategy config ID (can specify multiple) |
| `--all-configs` | `-a` | Run all available strategy configs |
| `--config-pattern=PAT` | `-p` | Run configs matching name pattern (SQL LIKE) |
| `--strategy-type=TYPE` | | Filter configs by strategy type (volatility, arb, grid) |
| `--collection=NAME|ID` | `-C` | Segment collection to run (required) |
| `--show-selection` | | Preview collection selection and exit |
| `--capital=CENTS` | | Initial capital in cents (default: 10000 = $100) |
| `--workers=N` | `-w` | Number of parallel workers (default: 8) |
| `--save` | `-S` | Save results to database |
| `--dry-run` | | Show what would run without executing |
| `--warmup-candles=N` | | Pre-load N candles before segment for indicator warmup (default: 50) |
| `--db-pool-max=N` | | DB pool size for main batch process (default: 10) |
| `--db-pool-max-worker=N` | | DB pool size for worker processes (default: 3) |

**Examples:**
```bash
# Run one config on a segment collection
bun src/systems/trading-engine/bd-segments.ts create --name=swings100 --annotations=high_activity
bun src/systems/trading-engine/batch-runner.ts --config=abc123 --collection=swings100 --save

# Run all configs on a collection
bun src/systems/trading-engine/batch-runner.ts --all-configs --collection=swings50 --save

# Run all configs on specific segment IDs (snapshot collection)
bun src/systems/trading-engine/bd-segments.ts create --name=segment-set --segment-ids=949,950,951,952 --mode=snapshot
bun src/systems/trading-engine/batch-runner.ts --all-configs --collection=segment-set --save

# Run configs matching "RSI-*" on high_activity segments
bun src/systems/trading-engine/bd-segments.ts create --name=rsi-activity --annotations=high_activity
bun src/systems/trading-engine/batch-runner.ts --config-pattern="RSI-%" --collection=rsi-activity --save

# Dry run to see what would execute
bun src/systems/trading-engine/batch-runner.ts --all-configs --collection=swings100 --dry-run
```

### Key CLI Flags (Quick Reference)
- `--collection=NAME|ID` or `-C`: REQUIRED segment collection selector
- `--show-selection`: Preview resolved segment list and exit
- `--config-pattern="TEST-%"` or `-p`: Filter configs by name pattern
- `--strategy-type=grid`: Filter configs by strategy type

## Phase 2: Comprehensive Analysis (ALWAYS RUN)

After simulations complete, run ALL of the following diagnostic queries. Present results in tables.

### 2.1 Core Stats
```sql
SELECT
  sc.name,
  COUNT(*) as runs,
  ROUND(AVG(trade_count)::numeric, 1) as avg_trades,
  ROUND(STDDEV(trade_count)::numeric, 1) as stddev_trades,
  MIN(trade_count) as min_trades,
  MAX(trade_count) as max_trades
FROM (
  SELECT r.id, sc.name, COUNT(t.id) as trade_count
  FROM sim_runs r
  JOIN strategy_configs sc ON r.config_id = sc.id
  LEFT JOIN sim_trades t ON t.run_id = r.id
  WHERE r.created_at > NOW() - INTERVAL '1 hour'
  GROUP BY r.id, sc.name
) sub
JOIN strategy_configs sc ON sc.name = sub.name
GROUP BY sc.name
ORDER BY avg_trades;
```

### 2.2 Entry Signal Frequency (RED FLAG: median < 60s is suspicious)
```sql
WITH entries AS (
  SELECT
    t.run_id, sc.name as config, t.entry_at,
    LAG(t.entry_at) OVER (PARTITION BY t.run_id ORDER BY t.entry_at) as prev_entry
  FROM sim_trades t
  JOIN sim_runs r ON t.run_id = r.id
  JOIN strategy_configs sc ON r.config_id = sc.id
  WHERE r.created_at > NOW() - INTERVAL '1 hour'
)
SELECT
  config,
  COUNT(*) as entry_gaps,
  ROUND(AVG((entry_at - prev_entry)/1000.0)::numeric, 1) as avg_gap_sec,
  ROUND(PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY (entry_at - prev_entry)/1000.0)::numeric, 1) as median_gap_sec,
  COUNT(*) FILTER (WHERE entry_at - prev_entry < 1000) as gaps_under_1s,
  COUNT(*) FILTER (WHERE entry_at - prev_entry < 5000) as gaps_under_5s,
  COUNT(*) FILTER (WHERE entry_at - prev_entry < 60000) as gaps_under_1min
FROM entries
WHERE prev_entry IS NOT NULL
GROUP BY config
ORDER BY median_gap_sec;
```
**Interpretation**: Median gaps < 60s suggest overtrading. Healthy configs should have gaps in minutes (20-30min typical). Gaps < 1s are a MAJOR RED FLAG - indicates indicator firing constantly.

### 2.3 Position Overlap
```sql
-- How many concurrent positions on average?
WITH trade_events AS (
  SELECT t.run_id, sc.name as config, t.entry_at as ts, 1 as delta
  FROM sim_trades t
  JOIN sim_runs r ON t.run_id = r.id
  JOIN strategy_configs sc ON r.config_id = sc.id
  WHERE r.created_at > NOW() - INTERVAL '1 hour'
  UNION ALL
  SELECT t.run_id, sc.name as config, t.exit_at as ts, -1 as delta
  FROM sim_trades t
  JOIN sim_runs r ON t.run_id = r.id
  JOIN strategy_configs sc ON r.config_id = sc.id
  WHERE r.created_at > NOW() - INTERVAL '1 hour' AND t.exit_at IS NOT NULL
),
running_pos AS (
  SELECT run_id, config, ts,
    SUM(delta) OVER (PARTITION BY run_id ORDER BY ts, delta DESC) as open_positions
  FROM trade_events
)
SELECT
  config,
  MAX(open_positions) as max_concurrent,
  ROUND(AVG(open_positions)::numeric, 2) as avg_concurrent,
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY open_positions) as median_concurrent
FROM running_pos
GROUP BY config
ORDER BY avg_concurrent DESC;
```

### 2.4 Holding Duration Distribution
```sql
SELECT
  sc.name as config,
  CASE
    WHEN t.holding_duration_ms < 30000 THEN '<30s'
    WHEN t.holding_duration_ms < 60000 THEN '30-60s'
    WHEN t.holding_duration_ms < 120000 THEN '1-2min'
    WHEN t.holding_duration_ms < 180000 THEN '2-3min'
    WHEN t.holding_duration_ms < 240000 THEN '3-4min'
    WHEN t.holding_duration_ms < 300000 THEN '4-5min'
    ELSE '5min+'
  END as hold_bucket,
  COUNT(*) as trades,
  ROUND(AVG(t.net_pnl_cents)::numeric, 1) as avg_pnl,
  ROUND(COUNT(*)::numeric / SUM(COUNT(*)) OVER (PARTITION BY sc.name) * 100, 1) as pct
FROM sim_trades t
JOIN sim_runs r ON t.run_id = r.id
JOIN strategy_configs sc ON r.config_id = sc.id
WHERE r.created_at > NOW() - INTERVAL '1 hour' AND t.holding_duration_ms IS NOT NULL
GROUP BY sc.name, hold_bucket
ORDER BY sc.name, MIN(t.holding_duration_ms);
```

### 2.5 Exit Reason Analysis
```sql
SELECT
  sc.name as config,
  t.exit_reason,
  COUNT(*) as trades,
  ROUND(AVG(t.net_pnl_cents)::numeric, 1) as avg_pnl,
  ROUND(COUNT(*)::numeric / SUM(COUNT(*)) OVER (PARTITION BY sc.name) * 100, 1) as pct
FROM sim_trades t
JOIN sim_runs r ON t.run_id = r.id
JOIN strategy_configs sc ON r.config_id = sc.id
WHERE r.created_at > NOW() - INTERVAL '1 hour'
GROUP BY sc.name, t.exit_reason
ORDER BY sc.name, trades DESC;
```

### 2.6 YES vs NO Side Analysis (IMPORTANT - check for asymmetries)
```sql
SELECT
  sc.name as config,
  t.side,
  COUNT(*) as trades,
  ROUND(AVG(t.net_pnl_cents)::numeric, 1) as avg_pnl,
  ROUND(AVG(CASE WHEN t.net_pnl_cents > 0 THEN 1 ELSE 0 END)::numeric * 100, 1) as win_pct,
  ROUND(AVG(t.entry_price)::numeric, 1) as avg_entry_price,
  ROUND(AVG(t.exit_price)::numeric, 1) as avg_exit_price,
  ROUND(AVG(t.quantity)::numeric, 1) as avg_qty
FROM sim_trades t
JOIN sim_runs r ON t.run_id = r.id
JOIN strategy_configs sc ON r.config_id = sc.id
WHERE r.created_at > NOW() - INTERVAL '1 hour'
GROUP BY sc.name, t.side
ORDER BY sc.name, t.side;
```
**Interpretation**: Significant asymmetry between YES/NO performance suggests bugs in price conversion or side selection logic. Both sides should have similar characteristics unless the strategy explicitly favors one.

### 2.7 Position Sizing Verification
```sql
-- Check if fills match expected sizes and align with order book
SELECT
  sc.name as config,
  t.quantity as fill_qty,
  COUNT(*) as occurrences,
  ROUND(AVG(t.entry_price)::numeric, 1) as avg_entry_price,
  ROUND(AVG(t.net_pnl_cents)::numeric, 1) as avg_pnl
FROM sim_trades t
JOIN sim_runs r ON t.run_id = r.id
JOIN strategy_configs sc ON r.config_id = sc.id
WHERE r.created_at > NOW() - INTERVAL '1 hour'
GROUP BY sc.name, t.quantity
ORDER BY sc.name, t.quantity;
```
**Check**: Does quantity match config's maxTradeSize? Are partial fills happening? Compare with maxPositionPerMarket.

### 2.8 Trade Sequence Performance
```sql
WITH numbered_trades AS (
  SELECT t.*, sc.name as config,
    ROW_NUMBER() OVER (PARTITION BY t.run_id ORDER BY t.entry_at) as trade_num
  FROM sim_trades t
  JOIN sim_runs r ON t.run_id = r.id
  JOIN strategy_configs sc ON r.config_id = sc.id
  WHERE r.created_at > NOW() - INTERVAL '1 hour'
)
SELECT
  config,
  CASE
    WHEN trade_num = 1 THEN '1st'
    WHEN trade_num BETWEEN 2 AND 5 THEN '2-5th'
    WHEN trade_num BETWEEN 6 AND 10 THEN '6-10th'
    WHEN trade_num BETWEEN 11 AND 20 THEN '11-20th'
    ELSE '21st+'
  END as position,
  COUNT(*) as trades,
  ROUND(AVG(net_pnl_cents)::numeric, 1) as avg_pnl,
  ROUND(AVG(CASE WHEN net_pnl_cents > 0 THEN 1 ELSE 0 END)::numeric * 100, 1) as win_pct
FROM numbered_trades
GROUP BY config, position
ORDER BY config, MIN(trade_num);
```

### 2.9 Market Segment Analysis
```sql
SELECT
  ms.definition_name,
  COUNT(DISTINCT r.id) as runs,
  COUNT(t.id) as trades,
  ROUND(AVG(r.total_pnl_cents)::numeric, 1) as avg_run_pnl,
  ROUND(AVG((ms.metrics->>'swing_count')::int)::numeric, 1) as avg_swings,
  ROUND(AVG((ms.metrics->>'reversion_rate')::float)::numeric, 2) as avg_reversion_rate
FROM sim_runs r
JOIN market_segments ms ON ms.source_meta->>'legacy_test_case_id' = r.test_case_id::text
LEFT JOIN sim_trades t ON t.run_id = r.id
JOIN strategy_configs sc ON r.config_id = sc.id
WHERE r.created_at > NOW() - INTERVAL '1 hour'
GROUP BY ms.definition_name
ORDER BY runs DESC;
```

### 2.10 Run Health Check
```sql
SELECT status, COUNT(*) as count
FROM sim_runs
WHERE created_at > NOW() - INTERVAL '1 hour'
GROUP BY status;
```
**RED FLAG**: Any "running" status after batch completes = crashed simulations.

## Phase 3: Log Analysis (ALWAYS RUN)

Check recent simulation logs for anomalies:

```bash
# Find most recent sim log
ls -lt logs/sim/ | head -5

# Sample entries from most recent log with content
LOG=$(ls -ltS logs/sim/*.log | head -1 | awk '{print $NF}')
echo "Analyzing: $LOG ($(du -h "$LOG" | cut -f1))"

# Check log volume by category (PERFORMANCE RED FLAG: >1M indicator logs)
echo "Log volume by category:"
rg '"category"' "$LOG" | jq -r '.category' 2>/dev/null | sort | uniq -c | sort -rn

# Check run duration from timestamps
echo "Run duration:"
FIRST_TS=$(head -1 "$LOG" | jq -r '.time' 2>/dev/null)
LAST_TS=$(tail -1 "$LOG" | jq -r '.time' 2>/dev/null)
if [ "$FIRST_TS" != "null" ] && [ "$LAST_TS" != "null" ]; then
  echo "Duration: $(( (LAST_TS - FIRST_TS) / 1000 )) seconds"
fi

# Count exit reasons
echo "Exit reason distribution:"
rg '"reason"' "$LOG" | jq -r '.reason' 2>/dev/null | sort | uniq -c | sort -rn | head -20

# Check for errors
echo "Errors in log:"
rg -i '"level":50' "$LOG" | head -10

# Check for warnings
echo "Warnings in log:"
rg -i '"level":40' "$LOG" | head -10
```

**Look for**:
- Unusual exit reasons (not profit_target, time_limit, collapse, end_of_data)
- Error level (50) entries
- Patterns suggesting bugs (repeated identical entries, missing fields)
- **PERFORMANCE**: Log file > 500MB = excessive logging
- **PERFORMANCE**: >1M indicator category logs = debug logging bottleneck

## Phase 3.5: Performance Analysis

Check simulation throughput:

```sql
-- Runs per second over recent batch
SELECT
  DATE_TRUNC('minute', created_at) as minute,
  COUNT(*) as runs,
  ROUND(COUNT(*)::numeric / 60, 1) as runs_per_sec
FROM sim_runs
WHERE created_at > NOW() - INTERVAL '1 hour'
GROUP BY minute
ORDER BY minute DESC
LIMIT 10;
```

**Expected throughput**: 20-40 runs/sec with tick caching. If < 10 runs/sec, investigate:
- Is tick cache being used? (check for "Pre-loaded" in batch script output)
- Is indicator debug logging enabled? (check log size)
- Are workers I/O bound? (check worker count vs CPU cores)

## Phase 4: Analysis Summary

**DUAL FOCUS**: Surface both accuracy concerns AND profit insights.

### First: Accuracy Check (Priority #1)
Flag any discrepancies between expected vs actual behavior:
1. Does config behavior match parameters?
2. Are there unexplained patterns or anomalies?
3. Do metrics make logical sense?

**Accuracy issues take precedence.** A 1% accuracy bug can invalidate profit analysis.

### Then: Profit Insights (Priority #2)
With accuracy validated, analyze:
1. Which configs are most profitable?
2. What patterns emerge across market conditions?
3. Are there optimization opportunities?

### Validation Questions to Answer

For each finding, ask: **"Does this match what we'd expect? If not, why?"**

| Observation | Expected Behavior | Actual | Match? | If No, Investigate |
|-------------|-------------------|--------|--------|-------------------|
| Entry gaps | Based on indicator params | ? | ? | Indicator calculation? Candle aggregation? |
| Exit reasons | Balanced mix | ? | ? | Exit logic? Threshold bugs? |
| YES vs NO performance | Similar (market is symmetric) | ? | ? | Price conversion? Side selection? |
| Position sizes | Match config maxTradeSize | ? | ? | Fill logic? Depth parsing? |
| Holding durations | Spread across buckets | ? | ? | Exit conditions firing? |
| Trade sequence | Later trades ≈ earlier | ? | ? | State accumulation bugs? |
| Bollinger/other indicators | Should trigger sometimes | ? | ? | Indicator implementation? |

### Key Validation Checks

1. **Indicator Firing Frequency**
   - Does the gap between entries match what the indicator period implies?
   - EMA(20) with 60s candles = 20 min of data needed. Are we seeing entries faster than that makes sense?

2. **Price/Side Consistency**
   - YES and NO should be mirror images. Major asymmetry = likely bug in price handling.
   - Check: Are we converting bid/ask correctly for each side?

3. **Config Parameters Actually Applied**
   - Is stopLossCents actually triggering at that price?
   - Is profitTargetCents actually triggering?
   - Is maxSpreadToEnter being checked?

4. **Data Flow Integrity**
   - Are ticks reaching the strategy in order?
   - Is depth data being parsed correctly?
   - Are fills being recorded accurately?

## Phase 5: Findings & Next Steps

Based on analysis, organize findings into:

### Accuracy Concerns (Surface First)
1. **Likely Bugs** - Discrepancies that suggest code errors
   - "X should be Y but we see Z" → investigate code path
2. **Unclear Behavior** - Things we don't understand yet
   - "We expected X, got Y, not sure why" → needs deeper investigation
3. **Confirmed Working** - Things that match expectations
   - "This behaves as expected" → increased confidence

### Profit Insights (Surface Second)
1. **Top Performers** - Which configs show best results?
2. **Market Patterns** - What conditions favor which strategies?
3. **Optimization Opportunities** - Parameter tuning suggestions

### Next Steps
- Investigation priorities for accuracy concerns
- Experiments to validate profit hypotheses
- Config variations to test

**Remember**: Accuracy comes first. Surface discrepancies prominently, then provide profit optimization insights. Both matter, but a small accuracy bug can invalidate all profit analysis.
