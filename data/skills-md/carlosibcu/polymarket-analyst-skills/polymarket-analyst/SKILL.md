---
name: polymarket-analyst
description: >
  Deep-dive analyst for Polymarket prediction market trader accounts. Use this
  skill whenever a user wants to: analyze a Polymarket wallet address or username,
  profile top/winning Polymarket traders, reverse-engineer trading strategies on
  Polymarket, track whale activity, compute P&L or performance metrics for any
  trader, compare multiple trader accounts, or understand what makes a profitable
  Polymarket account. Always trigger when the user mentions "Polymarket", "prediction
  market trader", "wallet analysis", "whale tracking", "copy trading", or asks
  about strategy detection on prediction markets. Even if the request sounds like
  a general research question ("who are the best Polymarket traders?"), use this
  skill to pull live data instead of guessing.
---

# Polymarket Analyst Skill

## Purpose

This skill fetches live on-chain and REST API data for one or more Polymarket
trader addresses, computes a comprehensive performance profile, classifies the
likely trading strategy, and produces a structured analyst report — all
reproducibly and from public data.

Think of it as running a quantitative analyst's playbook on any Polymarket wallet.

---

## Quick-start Workflow

```
1. Parse inputs          →  wallet address(es) from user message
2. Fetch raw data        →  scripts/fetch_trader_data.py
3. Compute metrics       →  scripts/analyze_trader.py
4. Strategy attribution  →  references/strategies.md
5. Generate report       →  structured Markdown output
```

When the user provides a **leaderboard URL**, a **username**, or asks for
"top traders", run step 2 with the `--leaderboard` flag first to discover
addresses, then profile each one.

---

## Step 1 — Parse Inputs

Extract from the user's request:
- **Wallet address(es)**: `0x...` Polygon addresses (case-insensitive)
- **Usernames / labels**: resolve via the Gamma profile endpoint
- **Time window**: default = all-time; accept "last 30 days", "2024", etc.
- **Market filter**: specific event or category (politics, sports, crypto…)
- **Mode**: single account | compare accounts | leaderboard scan

If no address is provided and the user mentions a leaderboard or "top traders",
fetch the public leaderboard automatically (see references/api.md §Leaderboard).

---

## Step 2 — Fetch Raw Data

Run the data-fetching script for each address:

```bash
python3 scripts/fetch_trader_data.py \
  --address 0xABCD... \
  --output /tmp/polymarket_data/0xABCD \
  [--days 90]          # optional time window in days
```

This script calls the three Polymarket API surfaces (no auth required for
public data — see references/api.md for all endpoints):

| Source | What it returns |
|--------|----------------|
| Data API `/activity` | All trades with timestamps, sides, prices, amounts |
| Data API `/positions` | Open and closed positions with P&L |
| Data API `/portfolio` | Aggregated profit, volume, win rate |
| Gamma API `/markets` | Market metadata (category, resolution, title) |
| CLOB API `/prices-history` | Price time-series for each token traded |

The script saves everything to structured JSON under `--output`:
```
/tmp/polymarket_data/0xABCD/
  activity.json     # raw trades
  positions.json    # positions with cashout amounts
  portfolio.json    # summary stats
  markets.json      # metadata for each market traded
  prices/           # per-token price history (fetched lazily)
```

Read references/api.md if you need to call endpoints manually or troubleshoot
rate limits.

---

## Step 3 — Compute Metrics

Run the analysis script on the fetched data:

```bash
python3 scripts/analyze_trader.py \
  --data-dir /tmp/polymarket_data/0xABCD \
  --output   /tmp/polymarket_data/0xABCD/analysis.json
```

The script computes all metrics defined in references/metrics.md. The output
`analysis.json` has this structure:

```json
{
  "address": "0xABCD...",
  "snapshot_date": "2026-02-17",
  "performance": { ... },
  "behavior": { ... },
  "market_concentration": { ... },
  "timing": { ... },
  "risk": { ... },
  "strategy_signals": { ... }
}
```

Read references/metrics.md for the full definition of every field.

---

## Step 4 — Strategy Attribution

After computing metrics, classify the trader using the decision logic in
references/strategies.md. The six canonical Polymarket strategies are:

1. **Information Arbitrage** — trades correlated with external information events
2. **Cross-Platform Arbitrage** — exploits price gaps vs. Kalshi, Manifold, etc.
3. **High-Probability Bond** — buys contracts >$0.88 for near-certain yield
4. **Market Making / Liquidity Provision** — tight bid-ask, high fill rate
5. **Domain Specialist** — concentrated in one category with above-average accuracy
6. **Speed / News Trading** — enters within minutes of breaking news

Read references/strategies.md for the signal thresholds and heuristics that
map metric values to each strategy label. A trader may show signals of multiple
strategies — report the **primary** (highest-confidence) one and any secondaries.

---

## Step 5 — Generate Report

Produce the analyst report as Markdown. Always use this exact structure:

---

```markdown
# Polymarket Trader Analysis — {short_address}
**Snapshot:** {date}  |  **Window:** {window}

## Executive Summary
One paragraph: who is this trader, how much have they made, what is their
apparent edge, and what is their primary strategy.

## Performance Metrics

| Metric | Value |
|--------|-------|
| Total Realized P&L | $XXX,XXX |
| Win Rate (closed positions) | XX.X% |
| # Closed Positions | N |
| Avg. Position Size | $XXX |
| Largest Single Win | $XXX,XXX |
| Largest Single Loss | $–XXX |
| Profit Factor | X.X |
| Sharpe Ratio (approx.) | X.X |
| Max Drawdown | –X.X% |
| Avg. Hold Time | X days |

## Market Concentration

List top 5 categories by # of positions and by P&L contribution.
Note whether specialization correlates with better win rate.

## Timing & Entry Patterns

Describe:
- How early does the trader enter vs. market creation date?
- Is there clustering around news events?
- Any time-of-day or day-of-week patterns?

## Position Sizing & Risk Management

Describe Kelly-fraction behavior, whether position sizes grow after wins
(Martingale risk) or stay flat (disciplined), max simultaneous open positions.

## Strategy Attribution

**Primary strategy:** {strategy_name} — confidence: {High/Medium/Low}
**Secondary signals:** {strategy_name}, {strategy_name}

Explain in 2-3 sentences the evidence for the primary strategy label.

## Red Flags / Caveats

Note any signs of lucky variance (few trades, extreme hit-or-miss), potential
insider timing, or data gaps.

## Comparable Accounts

(If running a leaderboard scan) List other wallets with similar profiles.

---
*Data sources: Polymarket Data API, CLOB API, Gamma API (public endpoints).
No private data accessed.*
```

---

## Multi-Account Comparison

When the user asks to compare accounts or scan the leaderboard:

1. Run steps 2–3 for each address (parallelize if possible)
2. Build a comparison table with all key metrics side-by-side
3. Rank accounts by the metric the user cares about (default: total P&L)
4. Identify clusters of similar strategy profiles

---

## Error Handling

| Situation | Action |
|-----------|--------|
| Address not found / no trades | Report "No trading history found for {address}" |
| API rate limit (HTTP 429) | Wait 5 s, retry up to 3 times; if still failing, note partial data |
| Very few trades (<20) | Warn that metrics may not be statistically significant |
| Market metadata missing | Use token ID from activity as fallback label |
| Price history unavailable | Skip timing/entry metrics, note the gap |

---

## Reference Files

- **references/api.md** — Full Polymarket API reference (endpoints, params, schemas)
- **references/metrics.md** — Definition of every computed metric
- **references/strategies.md** — Strategy classification logic and thresholds

Read the relevant reference file when you need deeper detail on any step.
