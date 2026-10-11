---
name: option-wall-analysis
description: Computes max pain (where options expire worthless = dealer profit point), top open interest clusters as gamma walls (resistance/support), put/call ratio sentiment, dealer positioning. Identifies short-term magnetic price levels into next monthly OPEX. Triggers in English ("max pain on X", "option walls for X", "where will X go this week", "support and resistance options X", "OPEX target X") or Chinese ("X 的 max pain", "X 期权墙", "X 这周走哪里", "X 期权磁吸位", "X OPEX 目标").
---

# Option Wall Analysis — Reading the Order Book

## Goal

Use option chain data to predict **short-term price magnets** (next 1-4 weeks) by finding:
1. **Max pain** — strike where option holders lose most (= dealers profit most)
2. **Call walls** — high call OI = upside resistance (writers will defend)
3. **Put walls** — high put OI = downside support (writers will defend)
4. **Put/call ratio** — sentiment indicator
5. **Dealer gamma positioning** — how dealer hedging affects price

## Core Concepts (1-min crash course)

### What is "max pain"?
The strike price where **the most options expire worthless** = where option writers (dealers) profit the most.

**Theory**: As expiry approaches, dealers hedge their books, and the gravitational pull is toward max pain. Most reliable on **monthly OPEX (3rd Friday)** and **quarterly OPEX**.

### What's a "gamma wall"?
A strike with **massive OI** (e.g., 50,000+ contracts). At this strike:
- Dealers are short calls → they BUY stock as price rises (buying acts as resistance breaks higher)
- OR dealers are long calls → they SELL stock as price rises (acts as resistance)

**Practical reading**:
- **Highest call OI strike** = often **resistance** (writers defend)
- **Highest put OI strike** = often **support** (writers defend)

### What's "put/call ratio"?
- **Total Put OI / Total Call OI**
- > 1.0 = more puts than calls = bearish sentiment
- < 1.0 = more calls than puts = bullish sentiment
- **Contrarian indicator**: extreme >1.3 = capitulation low, <0.5 = euphoria top

## The 4-Step Workflow

### Step 1 — Run max_pain.py
```bash
uv run --with yfinance python $(ls ~/.claude/{skills,plugins/claude-investment-skills}/review-investment-screenshot/scripts/max_pain.py 2>/dev/null | head -1) TICKER 4
```

This gives you, for the next 4 expiries:
- Max pain strike
- Spot vs max pain %
- Top 5 call walls (resistance)
- Top 5 put walls (support)
- Put/call ratio

### Step 2 — Run option_walls.py for gamma map
```bash
uv run --with yfinance python $(ls ~/.claude/{skills,plugins/claude-investment-skills}/review-investment-screenshot/scripts/option_walls.py 2>/dev/null | head -1) TICKER 4
```

Gives top 10 OI strikes for both calls and puts per expiry. **Wider view** than max_pain.

### Step 3 — Identify the trade levels

**Read the data:**

| Output | What it means | Trade implication |
|---|---|---|
| Max pain $X (vs spot $Y where Y > X) | Bearish gravity, dealers want price down | Lean short into OPEX |
| Max pain $X (vs spot $Y where Y < X) | Bullish gravity, dealers want price up | Lean long into OPEX |
| Top call wall at $Z | Resistance | Don't expect to break through easily |
| Top put wall at $W | Support | Buyers likely to defend |
| Put/Call > 1.2 | Bearish sentiment | Contrarian buy signal |
| Put/Call < 0.5 | Bullish sentiment | Contrarian sell signal |
| Gamma wall = bigger than next 3 strikes combined | Magnet | Price likely sticks here |

### Step 4 — Build the trade plan

**Short-term play (1-2 weeks):**
- Spot $200, Max pain $195 (next OPEX)
- Top call wall $210 (15K OI), Top put wall $190 (12K OI)
- Put/Call: 0.85 (slightly bullish)
- **Plan**: Range $190-210, expect drift to $195 by OPEX
- **Strategy**: Short $210 call OR long $200/$210 call spread (sell upper)

**Around earnings:**
- Higher OI tends to span IV crush
- Walls become VERY relevant immediately post-earnings (price magnetizes to nearest wall after IV deflates)

## Interpretation guide (real examples)

### Example 1: NVDA pinned to $195 (high OI, neutral)
- Spot $198
- Max pain $195
- Top call wall $200 (28K OI)
- Top put wall $190 (24K OI)
- Put/call 0.86
**Read**: Range $190-200, drift toward $195 into next OPEX (15 days).
**Trade**: $200/$210 call spread (cap upside, collect premium) OR sell $190 put for income.

### Example 2: NOK $13, broken upward
- Spot $13.14
- Max pain $11.50 (lagging, just had major earnings rally)
- Top call wall $14 (8K OI), $15 (12K OI)
- Top put wall $12 (5K OI)
- Put/call 0.6 (bullish)
**Read**: Bullish skew, support at $12, resistance $14-15.
**Trade**: $14 calls if break out, $12 covered puts if pullback.

### Example 3: TSLA $250, bearish gravity
- Spot $250
- Max pain $230 (-8% below)
- Top call wall $260 (40K OI) — strong resistance
- Top put wall $245 (15K OI)
- Put/call 1.4 (bearish, capitulation possible)
**Read**: Dealers want $230, strong $260 ceiling, but extreme PCR = bounce possible.
**Trade**: $245 puts to play the gravity, $245/$235 spread for cheaper.

## Output format

```markdown
# [TICKER] Option Wall Analysis — [Date]
**Spot**: $XXX | **Next OPEX**: [date] | **Days to expiry**: N

## Verdict
[One paragraph: Bias (bullish/bearish/pinned) + recommended levels + suggested trade]

## Max Pain by Expiry
| Expiry | Max Pain | Spot vs MP % | Interpretation |
| 2026-05-15 | $X | +X.X% | Bullish gravity / Bearish gravity / Pinned |
| 2026-05-22 | $X | ... | ... |

## Top Call Walls (Resistance)
| Strike | OI | Notes |
| $X | XX,XXX | Major resistance — needs catalyst to break |
| $X | XX,XXX | Secondary |

## Top Put Walls (Support)
| Strike | OI | Notes |
| $X | XX,XXX | Major support — buyers likely defend |
| $X | XX,XXX | Secondary |

## Put/Call Ratio
- This expiry: 0.XX
- Sentiment: [bullish/neutral/bearish]
- Contrarian signal: [yes/no, what it implies]

## Trade Levels (next [N] days)
- **Range**: $X (support) to $Y (resistance)
- **Magnet**: $Z (max pain)
- **Above $Y**: Breakout, target $YY
- **Below $X**: Breakdown, target $XX

## Strategy Recommendations
- **Bullish bias**: [specific trade]
- **Neutral / range-bound**: [specific trade]
- **Bearish bias**: [specific trade]
- **High conviction**: [single best trade]
```

## Hard rules

1. **Max pain is most reliable on monthly OPEX (3rd Friday)**, less so on weeklies.
2. **OI > 20,000 = real wall.** OI < 5,000 = noise.
3. **Don't trade against multiple confirming signals** (e.g., max pain + biggest OI both at $200 = $200 is the level).
4. **Earnings invalidate walls.** Pre-earnings, walls are theoretical; IV crush + price gap > wall.
5. **Cite actual numbers.** "Strong support at $190" without OI = useless.
6. **Time horizon = expiry.** Walls fade as new OI builds for next expiry.
7. **Combine with chart.** If $200 is wall AND 50DMA AND prior breakout, **that's the level**.

## Common pitfalls

| Pitfall | Example | Lesson |
|---|---|---|
| Trading max pain in week 1 of expiry | "Max pain is $195, sell calls" | Walls only matter last 5-7 days |
| Ignoring earnings risk | Selling $200 calls into NVDA earnings | Implied move >> wall |
| Using thin OI as walls | "Wall at $X" with 500 OI | < 5K OI is meaningless |
| Confusing call wall = resistance vs support | Spot above call wall in uptrend | Then it's support, not resistance (flip) |
| Anchor to one expiry | Just looking at 5/15 | Look at 5/15 + 5/22 + 5/29 = composite picture |

## When to invoke

- **User asks**: "Where's max pain on X?"
- **User asks**: "What are the option walls?"
- **User asks**: "Where will X go this week?"
- **User asks**: "Is there strong support/resistance on X?"
- **Pre-OPEX**: 7 days before any monthly/quarterly OPEX
- **Post-earnings**: Day after earnings to see new walls form
- **Companion to `earnings-prep`**: Add this analysis after earnings-prep

## Tool cheat-sheet

| Need | Tool |
|---|---|
| Max pain calc | `$(ls ~/.claude/{skills,plugins/claude-investment-skills}/review-investment-screenshot/scripts/max_pain.py 2>/dev/null | head -1) TICKER 4` |
| Top OI walls | `$(ls ~/.claude/{skills,plugins/claude-investment-skills}/review-investment-screenshot/scripts/option_walls.py 2>/dev/null | head -1) TICKER 4` |
| Live spot | `mcp__yfmcp__yfinance_get_ticker_info` |
| Option chain raw | `mcp__yfmcp__yfinance_get_option_chain` |

## Pro tips

1. **Friday afternoon before OPEX** = max pain becomes very strong magnet (expect price gravitation).
2. **Friday after OPEX** = new walls form for next month, watch which strikes accumulate first.
3. **Combine with VIX**: low VIX + clear walls = ranges hold; high VIX + walls = walls break.
4. **Stock-specific patterns**:
   - **NVDA**: Walls usually break (high momentum)
   - **AAPL**: Walls hold (low vol, mean-reverting)
   - **TSLA**: Walls break violently (high gamma squeeze potential)
   - **NOK**: Walls hold (low vol)

## Output combined with `analyze-stock` skill

If user runs `analyze-stock` first, then this skill, the option-wall analysis becomes **Step 9.5** (between LEAPS and final entry plan):
- Use walls to refine **3-tier entry**: instead of "50DMA", use "put wall at $X" if it's higher and stronger
- Use walls to set **stop loss**: "below put wall at $X = downside extension"
