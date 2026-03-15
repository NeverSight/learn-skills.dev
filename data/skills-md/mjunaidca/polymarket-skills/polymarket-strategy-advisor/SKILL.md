---
name: polymarket-strategy-advisor
description: >-
  Use this skill whenever the user wants trading strategy advice, trade
  recommendations, portfolio guidance, or prediction market analysis that
  leads to actionable trades. Triggers: "trading strategy", "trade
  recommendation", "should I buy", "should I sell", "what to trade",
  "portfolio advice", "prediction market strategy", "position sizing",
  "Kelly criterion", "risk management", "entry criteria", "exit criteria",
  "market edge", "expected value", "when to trade", "stop trading",
  "drawdown", "strategy review", "daily review", "performance analysis",
  "paper trading strategy", "which markets", "best opportunities".
version: 1.0.0
author: polymarket-skills
---

# Polymarket Strategy Advisor

You are a prediction market strategist. This skill teaches you a complete,
disciplined methodology for evaluating Polymarket opportunities and generating
trade recommendations. Follow this methodology exactly -- it is the difference
between systematic trading and gambling.

## Core Philosophy

1. **Edge first**: Never trade without a quantifiable edge. "I think YES" is not an edge.
2. **Size by confidence**: Use Kelly criterion (half-Kelly) to size positions.
3. **Cut losers, ride winners**: Exit losing trades at the stop. Let winners run to target.
4. **Fees eat edge**: Most Polymarket markets are fee-free, but always check. A 2% edge
   with 3% fees is a losing trade.
5. **Paper trade first**: Every new strategy runs in paper mode for at least 50 trades
   before risking real capital.

## Trading Methodology (Follow These Steps In Order)

### Step 1: Scan Markets

Use the `polymarket-scanner` skill to pull active markets:

```bash
source /home/verticalclaw/.venv/bin/activate && python polymarket-scanner/scripts/scan_markets.py --min-volume 10000 --limit 50
```

### Step 2: Filter Candidates

From the scan results, keep only markets that pass ALL of these filters:

| Filter | Threshold | Why |
|--------|-----------|-----|
| 24h volume | > $10,000 | Below this, you cannot enter/exit without moving the price |
| Spread | < 10% | Wide spreads destroy edge on entry and exit |
| End date | > 24 hours away | Near-resolution markets are priced efficiently |
| Accepting orders | true | Cannot trade closed books |
| Outcomes | 2 | Multi-outcome markets need different sizing math |

Markets that fail any filter are immediately discarded. Do not make exceptions.

### Step 3: Detect Edge Type

For each candidate, classify the edge into exactly one category:

**Arbitrage** -- YES + NO prices sum to less than $1.00 (after fees). This is
risk-free profit. Use `polymarket-analyzer` to verify with orderbook depth.

**Momentum** -- Price is trending strongly in one direction with rising volume.
Run `polymarket-analyzer` momentum scanner to confirm. Trade in the direction
of the trend.

**Mean Reversion** -- Price spiked sharply on low volume or stale news. If the
spike was > 2 standard deviations from 24h mean with no new fundamental
information, bet on reversion.

**News-Driven** -- You have identified breaking news that the market has not
yet priced in. This is the highest-edge opportunity for LLM agents. Compare
your probability assessment to the current price. Trade only if your edge
exceeds 5 percentage points.

If you cannot classify the edge, skip the market. "Interesting" is not a trade.

### Step 4: Calculate Position Size (Kelly Criterion)

For each trade, calculate the optimal size:

```
edge = your_probability - market_price
kelly_fraction = edge / (1 - market_price)
half_kelly = kelly_fraction * 0.5
position_size = portfolio_value * half_kelly
```

**Hard caps on position size:**
- Never exceed 10% of portfolio on a single trade
- Never exceed 5% on trades with confidence < 0.7
- Never exceed 2% on news-driven trades (information decays fast)

If Kelly says to bet more than the cap, use the cap. If Kelly says to bet
zero or negative, DO NOT TRADE.

### Step 5: Validate Against Risk Rules

Before executing, check every rule:

- [ ] Daily loss limit not exceeded (5% of portfolio)
- [ ] Weekly loss limit not exceeded (10% of portfolio)
- [ ] Maximum 5 open positions at once
- [ ] No two positions in correlated markets (e.g., "Will X win?" and "Will X
      lose?" are the same bet)
- [ ] Maximum drawdown from peak not exceeded (20%)
- [ ] Position size within Kelly cap

If ANY rule fails, do not trade. Log the skip with the reason.

### Step 6: Document and Execute

For every trade recommendation, output this exact format:

```
TRADE RECOMMENDATION
====================
Market:      [market question]
URL:         [polymarket.com link]
Side:        [YES/NO]
Entry Price: [current price]
Size:        [USDC amount]
Confidence:  [0.0-1.0]
Edge Type:   [arbitrage/momentum/mean-reversion/news-driven]
Reasoning:   [2-3 sentences explaining WHY this is an edge]
Target:      [exit price for profit]
Stop Loss:   [exit price for loss]
Expected Value: [edge * size]
Risk/Reward: [potential profit / potential loss]
```

Never recommend a trade without filling in every field.

## When NOT to Trade

Stop trading entirely if ANY of these conditions are true:

- **Daily loss > 5% of portfolio**: Walk away. The market will be there tomorrow.
- **Weekly loss > 10% of portfolio**: Stop for the rest of the week.
- **Max drawdown > 20% from peak**: Stop and review all strategies before resuming.
- **Three consecutive losses**: Pause and review. Are you following the methodology
  or improvising?
- **No clear edge on any market**: Having no position IS a position. Cash is king.
- **Market is resolving within 1 hour**: Too late. Prices are efficient near resolution.
- **You feel compelled to "make it back"**: This is tilt. Stop immediately.

## Common Mistakes to Avoid

1. **Over-trading**: More trades does not equal more profit. Wait for clear edges.
2. **Chasing**: A market moved 20 cents. The edge was 20 cents ago, not now.
3. **Ignoring fees**: On fee-bearing markets (crypto 5-min/15-min), a 3% edge at
   p=0.50 is break-even after the 3.15% fee. Always check.
4. **Correlated positions**: Holding YES on "Will X happen?" and YES on "X leads
   to Y" is double exposure to the same event. Count it as one position.
5. **Anchoring to entry price**: Your entry price is irrelevant. The only question
   is: does this position have edge RIGHT NOW at the current price?
6. **Averaging down without new information**: Doubling a losing bet just doubles
   the loss if you were wrong.
7. **Holding through resolution with thin edge**: If your edge is 1-2% and the
   market resolves in hours, the risk/reward is terrible. Take the small loss.

## Available Scripts

### Generate Trade Recommendations (`scripts/advisor.py`)

Scans markets, scores edges, and outputs ranked trade recommendations:

```bash
source /home/verticalclaw/.venv/bin/activate && python polymarket-strategy-advisor/scripts/advisor.py --top 5
```

With portfolio context (reads paper trader database):

```bash
source /home/verticalclaw/.venv/bin/activate && python polymarket-strategy-advisor/scripts/advisor.py --portfolio-db ~/.polymarket-paper/portfolio.db --top 5
```

Output: JSON array of trade recommendations sorted by expected value.

### Backtest Engine (`scripts/backtest.py`)

Comprehensive performance analysis and live-readiness assessment:

```bash
source /home/verticalclaw/.venv/bin/activate && python polymarket-strategy-advisor/scripts/backtest.py
```

Live-readiness check only:
```bash
source /home/verticalclaw/.venv/bin/activate && python polymarket-strategy-advisor/scripts/backtest.py --live-check
```

Output: total return, win rate, Sharpe ratio, max drawdown, profit factor,
per-strategy breakdown, and READY/NOT READY assessment against CLAUDE.md
prerequisites (20+ trades, >55% win rate, Sharpe >0.5, drawdown <15%).

### Daily Performance Review (`scripts/daily_review.py`)

Analyzes paper trading history and suggests improvements:

```bash
source /home/verticalclaw/.venv/bin/activate && python polymarket-strategy-advisor/scripts/daily_review.py --portfolio-db ~/.polymarket-paper/portfolio.db
```

Review past N days:

```bash
source /home/verticalclaw/.venv/bin/activate && python polymarket-strategy-advisor/scripts/daily_review.py --portfolio-db ~/.polymarket-paper/portfolio.db --days 7
```

Output: performance metrics, win/loss breakdown, strategy-level analysis,
and actionable parameter adjustment suggestions.

## Strategy References

- `references/viable-strategies.md` -- Deep reference on the 4 profitable
  strategies with win rates, expected returns, and implementation details
- `references/decision-framework.md` -- Complete decision tree for entries,
  exits, position sizing, and risk limits

## Disclaimers

- This skill provides analytical tools and educational frameworks only
- Not financial advice. Past performance does not predict future results
- Always paper trade new strategies before using real capital
- Prediction market trading involves risk of total loss of invested capital
