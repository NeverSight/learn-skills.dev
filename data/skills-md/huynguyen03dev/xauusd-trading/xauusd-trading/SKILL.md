---
name: xauusd-trading
description: Fetch XAUUSD (Gold) price data and analyze it using LLM reasoning to generate scalping signals. Optimized for small accounts with tight stop losses (5 points). Use 5m/15m timeframes for precise entry timing.
---

# XAUUSD LLM Scalping Analysis

Skill for **small account scalping** with tight stop losses (~5 points / $5).

## Philosophy

You ARE the analyst. Your PRIMARY decision tool is **price structure** — where price is relative to support, resistance, swing points, and key levels.

Indicators (RSI, MACD, Stoch, etc.) are **context only** — they confirm or deny what structure is telling you. Never take a trade purely because an indicator says so. Structure first, indicators second, TradingView rating last.

**Your priority stack**:
1. Price structure (where is price relative to levels?)
2. Candle patterns (rejection wicks, engulfing, momentum)
3. Indicator confluence (do RSI/MACD/Stoch agree with structure?)
4. TradingView signal rating (treat as a secondary opinion, not gospel)

## Quick Start - Fetch Data

### 1. Real-time price + indicators (TradingView - NO DELAY)

```bash
bash /home/hazeruno/.config/opencode/skill/xauusd-trading/scripts/fetch_price.sh
```

Returns live price, current candle OHLC, RSI, MACD, Stoch, ADX, CCI, EMA, BB, ATR on 5m/15m/1h timeframes. **Use for current snapshot and indicator context.**

### 2. Real-time candle history (Twelve Data - NO DELAY)

```bash
# Requires: export TWELVE_DATA_API_KEY="your_key"
# Get free key: https://twelvedata.com (800 requests/day, free forever)

# 5-minute candles (primary for scalping)
bash /home/hazeruno/.config/opencode/skill/xauusd-trading/scripts/fetch_candles.sh 5min 30

# 15-minute candles (for trend/structure)
bash /home/hazeruno/.config/opencode/skill/xauusd-trading/scripts/fetch_candles.sh 15min 20

# 1-minute candles (for micro entries)
bash /home/hazeruno/.config/opencode/skill/xauusd-trading/scripts/fetch_candles.sh 1min 40
```

Returns last N candles with OHLC — **real-time, no delay**. Use for structure analysis: swing highs/lows, support/resistance, patterns.

**Intervals**: 1min, 5min, 15min, 30min, 1h, 4h, 1day

### 3. Fallback candle history (Yahoo Finance - ~15-20min delay, NO key needed)

```bash
bash /home/hazeruno/.config/opencode/skill/xauusd-trading/scripts/fetch_gold.sh 5m 1d 50
```

Only use if Twelve Data key is not set. Data is delayed ~15-20 minutes.

## Analysis Workflow

1. **Run `fetch_price.sh`** → get live price + indicators snapshot
2. **Run `fetch_candles.sh 5min 30`** → get real-time candle structure (swing points, patterns)
3. **Optionally run `fetch_candles.sh 15min 20`** → for higher timeframe trend
4. **Analyze** → structure first, indicators as context
5. **Output signal** → with checklist, levels, and probabilities

## Scalping Analysis Framework (5-Point Stop Loss)

### 1. IDENTIFY MICRO STRUCTURE
With only 5 points of risk, you need PRECISE entries:
- Find the **immediate swing high/low** (last 5-10 candles)
- Identify **micro support/resistance** levels
- Look for **tight consolidation** ranges (< 10 points)

### 2. ENTRY TIMING CRITERIA
Only signal when:
- Price is AT a clear level (not in the middle of a range)
- Recent candle shows **rejection wick** or **engulfing pattern**
- Stop loss placement is LOGICAL (behind structure, not arbitrary)

### 3. CALCULATE EXACT LEVELS
For every signal, specify:
```
Entry: [exact price]
Stop Loss: [entry ± 5 points]
Take Profit: [minimum 1:1.5 R:R = 7.5 points]
```

### 4. MOMENTUM CHECK
On 5m chart, confirm:
- Last 3-5 candles show directional bias
- No major wick rejections against your direction
- Volume/candle size increasing in your direction

### 5. EXTREME INDICATOR READINGS (High-Probability Triggers)
These extreme readings often precede reversals — use them as entry confirmations:

| Indicator | Extreme LONG Zone | Extreme SHORT Zone |
|-----------|-------------------|-------------------|
| Stochastic K | **< 10** | **> 90** |
| CCI | **< -100** | **> +100** |
| RSI | **< 30** | **> 70** |

**When multiple indicators are extreme simultaneously**, bounce probability increases significantly.

Example from real session: Stoch K hit 7.2 with CCI at -92 → price bounced 12+ points.

## Hard "NO TRADE" Gates

Before generating any signal, check these. Gates marked **HARD** = must skip. Gates marked **SOFT** = warn but can still trade.

### HARD Gate 1: Volatility Filter
- If 5m ATR > 8 points → **SKIP** (your 5-point SL is noise in this volatility)
- If 15m ATR > 20 points → **SKIP** (market too wild for scalping)

### HARD Gate 2: News Event Filter
Do NOT trade during or 15 minutes before/after these events:
- **US**: CPI, NFP (Non-Farm Payrolls), FOMC rate decisions, PCE, PPI
- **Global**: ECB/BOE/BOJ rate decisions, geopolitical shocks
- Gold can move 30-50+ points in seconds during these events. A 5-point SL is meaningless.

If you're unsure whether a news event is happening, add a warning: "Check economic calendar before entering."

### HARD Gate 3: Script Failure
- If `fetch_price.sh` returns an error or "Market may be closed" → **NO TRADE**
- If data looks stale (price hasn't changed in multiple fetches) → **NO TRADE**

### SOFT Gate 4: Spread/Slippage Cost Awareness
Gold spread is typically 2-3 points, plus ~1 point slippage on entries.

**Your REAL risk per trade**:
```
Effective SL = 5 (your SL) + 2-3 (spread) + 1 (slippage) = 8-9 points total cost
Effective TP1 = 5 (your TP) - 2-3 (spread) = 2-3 points net gain
Effective TP2 = 10 (your TP) - 2-3 (spread) = 7-8 points net gain
```

Always mention this in your analysis, but still suggest the trade if structure looks good.

### HARD Gate 5: Rollover Period (21:00-22:00 UTC)
- **DO NOT TRADE** during 21:00-22:00 UTC (daily rollover/swap time)
- Stop hunts are extremely common during this window — market makers sweep liquidity before the new session
- If you must trade during rollover, use **minimum 8-point SL** (not 5) to survive the wicks
- This gate was upgraded from SOFT to HARD based on real session experience where two consecutive 5-pt SLs were hunted during rollover

### SOFT Gate 6: Session Timing
- **Best**: London-NY overlap (13:00-17:00 UTC) — tightest spreads, best liquidity
- **OK**: London session (08:00-12:00 UTC), NY session (13:00-21:00 UTC)
- **Warn but allow**: Asian session (wider spreads, note it)

## Signal Output Format

```
## XAUUSD SCALP SIGNAL

**Action**: 🟢 BUY (Long) / 🔴 SELL (Short) / ⚪ NO TRADE
**Confidence**: [High / Medium / Low]

### Levels
- Current Price: $XXXX.XX
- Entry Zone: $XXXX.XX - $XXXX.XX
- Stop Loss: $XXXX.XX (5 points risk)
- Take Profit 1: $XXXX.XX (+5 points)
- Take Profit 2: $XXXX.XX (+10 points)

### Win Probability & Scenarios

**IMPORTANT**: These probabilities are HEURISTIC — educated guesses based on structure, not statistical models. Be honest but not paralyzed.

**Probability guidelines**:
- Use ranges: "35-45%", not "42%"
- Cap at 70% max for any single outcome
- If SL probability > TP1 probability by a wide margin → SKIP
- If everything is 33/33/33 → lean toward the direction momentum supports

Estimate how likely each outcome is based on the current structure:

| Scenario | Target | Gross Pts | Net After Spread (~3pts) | Est. Probability |
|----------|--------|-----------|--------------------------|-----------------|
| SL Hit | $XXXX | -5 | -8 (SL + spread + slip) | XX-XX% |
| TP1 Hit | $XXXX | +5 | +2 to +3 | XX-XX% |
| TP2 Hit | $XXXX | +10 | +7 to +8 | XX-XX% |

**Expected Value (cost-adjusted)**:
- TP1 play: (TP1% x net_TP1) - (SL% x net_SL) = $X.XX
- TP2 play: (TP2% x net_TP2) - (SL% x net_SL) = $X.XX

**Verdict**: [WORTH TAKING / MARGINAL / SKIP]

The goal is to help the user DECIDE, not to block all trades. If a setup has any structural edge at all, present it with honest probabilities and let the user judge.

### Pre-Signal Checklist

Answer these. Flag any "No" items as risks, but still suggest the trade if the overall picture has an edge.

| # | Check | Answer |
|---|-------|--------|
| 1 | Is price near a clear level? | Yes/No |
| 2 | Is 5m ATR reasonable (≤ 8)? | Yes/No |
| 3 | Is there a candle pattern or momentum confirming? | Yes/No |
| 4 | Does higher timeframe direction agree? | Yes/No |
| 5 | Is SL behind some structure? | Yes/No |
| 6 | No major news event right now? | Yes/No |

**Trade if**: Majority are "Yes" and #2 + #6 pass. Flag any "No" as a risk factor.

### Structure Analysis
[What micro structure you see - support/resistance, swing points]

### Entry Trigger
[Specific condition to enter - e.g., "break above 5032", "rejection candle at 5025"]

### Reasoning
[2-3 sentences on why this setup works]

### Risk Warning
This is LLM-based analysis for testing only. Not financial advice.
```

## What to Look For (5m Chart)

### 🟢 BUY (Long) Setups
1. **Support Bounce**: Price touches recent low, forms rejection wick up
2. **Breakout Pullback**: Breaks resistance, pulls back to retest, holds
3. **Higher Low**: Creates higher low after swing up, momentum continuing
4. **Stop Hunt Reversal** (High Probability): Price makes a sharp wick that sweeps previous lows by 3-5+ pts, then V-recovers. Enter LONG after candle closes back above the swept level. SL below wick (6-8 pts). Key signal: Stochastic K < 10 during wick = extreme oversold, high bounce probability.

### 🔴 SELL (Short) Setups  
1. **Resistance Rejection**: Price hits recent high, rejection wick down
2. **Breakdown Retest**: Breaks support, pulls back to retest, rejected
3. **Lower High**: Creates lower high after swing down, momentum continuing
4. **Stop Hunt Reversal** (High Probability): Price makes a sharp wick that sweeps previous highs by 3-5+ pts, then V-reverses down. Enter SHORT after candle closes back below the swept level. SL above wick (6-8 pts). Key signal: Stochastic K > 90 during wick = extreme overbought.

### ⚪ NO TRADE Conditions
- Price in middle of range (no clear level nearby)
- Choppy/whipsaw action (alternating direction candles)
- Wide spread candles (volatility too high)
- Near session open/close (unpredictable)

## Example Analysis Process

1. **Fetch real-time indicators**:
```bash
bash /home/hazeruno/.config/opencode/skill/xauusd-trading/scripts/fetch_price.sh
```

2. **Fetch real-time candle history** (for structure):
```bash
bash /home/hazeruno/.config/opencode/skill/xauusd-trading/scripts/fetch_candles.sh 5min 30
```

3. **Analyze**: Use candles to find swing points, support/resistance. Use indicators to confirm direction. Apply the Analysis Framework.

4. **Generate signal with exact levels** based on live price

## Multi-Timeframe (Optional)

For higher confidence, fetch multiple timeframes:

```bash
bash /home/hazeruno/.config/opencode/skill/xauusd-trading/scripts/fetch_price.sh
bash /home/hazeruno/.config/opencode/skill/xauusd-trading/scripts/fetch_candles.sh 15min 20
bash /home/hazeruno/.config/opencode/skill/xauusd-trading/scripts/fetch_candles.sh 5min 30
```

Rule: Only take 5m signals that ALIGN with 15m direction.

## Important Notes

1. **LLM is NOT predictive** - You are doing opinionated pattern reading, not forecasting. Scalping with tight SLs has high failure rates even among experienced human traders.
2. **Small account = strict risk** - Never risk more than 1-2% of account per trade
3. **5 points is TIGHT** - After spread+slippage, your real risk is ~8 points. Be extremely selective — most of the time the correct signal is NO TRADE.
4. **Spread eats your edge** - With ~3pt spread, your TP1 of +5pts nets only +2-3pts. You need high win rates or bigger TP2 plays.
5. **Session timing** - Best: London-NY overlap (13:00-17:00 UTC). Avoid Asian session and rollover.
6. **News kills scalpers** - A single CPI print can move gold 40 points in 1 second. Check calendar.
7. **This is experimental** - For paper trading and learning ONLY until you have evidence it works.

## Trade Management (Once in a Position)

### Breakeven Rule
- When trade reaches **+2.5 to +3 pts** profit, move SL to **breakeven** (entry price)
- This creates a "risk-free" trade — worst case you exit at 0, not -5
- Especially important after experiencing stop hunts earlier in the session

### Trailing Stop Option
- After hitting +5 pts, consider trailing SL to **+2 pts** (lock in some profit)
- Or hold for TP2 with breakeven SL if momentum is strong

### Session Loss Limit
- After **2 consecutive losses** (-10 pts total), STOP trading for the session
- Emotional state after losses leads to revenge trading and poor decisions
- Exception: If you identify a clear stop hunt reversal pattern, one more attempt is acceptable with WIDER SL (6-8 pts instead of 5)

### Recovery After Losses
- If you continue after losses, **widen your SL** to 6-8 pts
- Stop hunts often come in clusters during low-liquidity periods
- Accept that you're trading with worse R:R but better survival odds

## Trading Experience Log

Use this section as a running journal. Each time the user asks, append a new entry based on the actual trade outcome.

### How to log each trade

For every completed trade, add one block using this template:

```markdown
### Trade #N - YYYY-MM-DD HH:MM UTC
- Session: [London / NY / Overlap / Asian]
- Direction: [BUY / SELL]
- Setup Type: [Support Bounce / Resistance Rejection / Breakout Pullback / Stop Hunt Reversal / Other]
- Entry: [price]
- Stop Loss: [price] (5 points)
- TP1 / TP2: [price] / [price]
- Outcome: [TP1 / TP2 / SL / Manual Exit]
- Net Result (points): [+X / -X]
- Key Context: [ATR, spread estimate, news status, market condition]
- What Worked: [1-2 bullets]
- What Failed: [1-2 bullets]
- Lesson: [single sentence]
```

### Weekly review (every 10-20 trades)

After enough entries, add a summary block:

```markdown
### Weekly Review - YYYY-MM-DD
- Total Trades: X
- Wins: X | Losses: X | Win Rate: XX%
- Avg Win (pts): X.X | Avg Loss (pts): X.X
- Best Setup Type: [name + stats]
- Worst Setup Type: [name + stats]
- Most Common Mistake: [one line]
- Rule Adjustment: [one concrete rule to keep/change]
```

Rule: Experience log is for factual outcomes and lessons only. Do not rewrite past entries.

## Setup

1. Get a free Twelve Data API key: https://twelvedata.com/pricing (10 seconds, free forever, 800 req/day)
2. Set it: `export TWELVE_DATA_API_KEY="your_key"`
3. Test: `bash /home/hazeruno/.config/opencode/skill/xauusd-trading/scripts/fetch_candles.sh 5min 10`

## File Structure

```
xauusd-trading/
├── SKILL.md              # This file
└── scripts/
    ├── fetch_price.sh    # REAL-TIME price + indicators (TradingView, no key)
    ├── fetch_candles.sh  # REAL-TIME candle history (Twelve Data, free key)
    └── fetch_gold.sh     # Fallback candles (Yahoo Finance, delayed, no key)
```

## Continuous Monitoring Mode

When asked to monitor XAUUSD for scalping opportunities, use this workflow:

### Monitor Loop Execution Rules (CRITICAL)

**This is an INFINITE loop.** You MUST continue until user explicitly says "stop", "exit", or "pause".

| State          | Action After Analysis                          |
| -------------- | ---------------------------------------------- |
| `NEUTRAL`      | `sleep 120` → fetch again → **DO NOT STOP**    |
| `WATCHING`     | `sleep 60` → fetch again → **DO NOT STOP**     |
| `CONSOLIDATING`| `sleep 90` → fetch again → **DO NOT STOP**     |
| `SIGNAL`       | Output signal → **STOP and wait for user**     |

**HARD RULES:**
- After `NEUTRAL`, `WATCHING`, or `CONSOLIDATING` → execute sleep → immediately fetch new data
- Do NOT say "let me know if you want me to continue" — just continue
- Do NOT rationalize stopping ("market seems quiet", "no setup forming") — keep monitoring
- Only stop on: `SIGNAL` state, user command, or HARD gate failure (market closed, script error)

After user responds to `SIGNAL`:
- User enters → switch to 30-second active trade monitoring
- User skips → resume normal monitoring loop with sleep

### Monitor Loop

1. **Load this skill** for all analysis
2. **Fetch data** — you MUST run BOTH scripts every cycle:
   ```bash
   # REQUIRED: Run these in parallel every monitoring cycle
   bash /home/hazeruno/.config/opencode/skill/xauusd-trading/scripts/fetch_price.sh
   bash /home/hazeruno/.config/opencode/skill/xauusd-trading/scripts/fetch_candles.sh 5min 15
   ```
   - `fetch_price.sh` → indicators (RSI, MACD, Stoch, ATR, etc.)
   - `fetch_candles.sh` → **structure** (swing highs/lows, support/resistance, patterns)
   - **DO NOT skip candles** — indicators alone cannot identify structure levels
   - Every 3-5 cycles, also fetch 15m candles for trend context:
     ```bash
     bash /home/hazeruno/.config/opencode/skill/xauusd-trading/scripts/fetch_candles.sh 15min 10
     ```
3. **Analyze** and determine state (structure first, indicators as confirmation)
4. **Wait** based on state, then repeat

### Wait Discipline (Important)

When monitoring continuously, you MUST actually pause between cycles using `sleep`.

- `WATCHING` (1 minute):
  ```bash
  sleep 60
  ```
- `NEUTRAL` (2 minutes):
  ```bash
  sleep 120
  ```
- `CONSOLIDATING` (3 minutes):
  ```bash
  # Some tool environments time out at 120s.
  # If so, split into two waits:
  sleep 90
  # run fetch scripts
  sleep 90
  ```

Rule: Do not run back-to-back fetches without waiting unless the user explicitly says "check now" or "new candle now".

### Adaptive Intervals

| State          | Description                                                    | Wait Time     |
| -------------- | -------------------------------------------------------------- | ------------- |
| `NEUTRAL`      | Price mid-range, no clear level nearby                         | **2 minutes** |
| `WATCHING`     | Price near key level, overbought/oversold, rejection forming   | **1 minute**  |
| `CONSOLIDATING`| Price stuck in tight range (<5 pts), low momentum, no breakout | **3 minutes** |
| `SIGNAL`       | Entry opportunity confirmed per skill criteria                 | **Ask user**  |

### Detecting CONSOLIDATING State

Switch to `CONSOLIDATING` when ALL of these are true:
1. **Tight range**: Last 3-5 candles have total range < 5 points (highs and lows compressed)
2. **Flat MACD**: Histogram near zero (between -0.10 and +0.10)
3. **No breakout**: Price not testing key support/resistance (stuck in middle)
4. **Low momentum**: CCI between -30 and +30, or Mom indicator flat

**Why this matters**: Checking every minute during consolidation wastes API calls and adds no value. Wait for the range to break, then switch back to WATCHING.

**Exit CONSOLIDATING**: When price breaks out of the range OR volatility expands (ATR increases, MACD histogram expands)

### State Transitions

- `NEUTRAL` → `WATCHING`: Price approaches support/resistance, or indicators reach extreme zones
- `NEUTRAL` → `CONSOLIDATING`: Price enters tight range with no momentum
- `WATCHING` → `SIGNAL`: Entry trigger confirmed (rejection wick, breakout, stop hunt reversal)
- `WATCHING` → `NEUTRAL`: Price moves away from level without triggering
- `WATCHING` → `CONSOLIDATING`: Price stalls at level, forms tight range instead of breaking
- `CONSOLIDATING` → `WATCHING`: Range breaks, price moves toward key level
- `CONSOLIDATING` → `SIGNAL`: Breakout with momentum confirms entry
- `SIGNAL` → User decides to enter or skip

### On SIGNAL

Output the full signal format (see Signal Output Format above) and ask user whether to enter.

### On Active Trade

When user enters a position:
- Switch to **30-second** monitoring intervals
- Track P&L, distance to SL/TP
- Alert on key levels (+2.5 pts for breakeven move, approaching TP, approaching SL)
- Continue until trade closes
