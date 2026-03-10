---
name: polymarket-analyzer
description: >
  Use this skill whenever the user wants to find trading opportunities, detect arbitrage,
  analyze a market, perform edge detection, find mispricing, do probability analysis,
  evaluate orderbook depth, find momentum signals, or assess Polymarket market quality.
  Triggers: "find opportunities", "detect arbitrage", "analyze market", "edge detection",
  "mispricing", "probability analysis", "orderbook analysis", "momentum scanner",
  "market inefficiency", "price gap", "volume surge", "trading edge", "market analysis".
---

# Polymarket Analyzer Skill

Detect trading edges and opportunities across Polymarket prediction markets using
real-time data from the Gamma and CLOB APIs. Zero authentication required -- all
analysis is read-only.

## Available Scripts

### 1. Find Arbitrage Edges (`scripts/find_edges.py`)

Scans all active markets for pricing inefficiencies:

- **Underpriced**: YES + NO < $1.00 (guaranteed profit if you buy both sides)
- **Overpriced**: YES + NO > $1.02 (sell opportunity)
- Calculates profit after fees for each opportunity
- Outputs market name, prices, sum, potential profit, and fee impact

```bash
python scripts/find_edges.py
python scripts/find_edges.py --min-edge 0.02 --limit 500
```

### 2. Analyze Order Book (`scripts/analyze_orderbook.py`)

Deep analysis of a single market's order book:

- Spread, mid-price, bid/ask depth (top N levels)
- Bid-ask imbalance ratio (signals directional pressure)
- Thin vs thick book classification
- Liquidity concentration analysis

```bash
python scripts/analyze_orderbook.py --token-id <TOKEN_ID>
python scripts/analyze_orderbook.py --token-id <TOKEN_ID> --depth 10
```

### 3. Momentum Scanner (`scripts/momentum_scanner.py`)

Detect markets with unusual activity:

- **Volume surges**: 24h volume significantly exceeds 7-day average
- **Price momentum**: recent price moves in one direction
- **Liquidity changes**: markets gaining or losing depth
- Ranked output by signal strength

```bash
python scripts/momentum_scanner.py
python scripts/momentum_scanner.py --min-volume 10000 --limit 300
```

### 4. Correlation Tracker (`scripts/correlation_tracker.py`)

Detect hidden correlated exposure in your portfolio:

- Groups positions by topic (crypto, politics, sports, geopolitics, etc.)
- Detects shared qualifiers ("insider trading", "FIFA World Cup", etc.)
- Warns when correlated clusters exceed concentration limits
- Outputs diversification score (0-100)

```bash
python scripts/correlation_tracker.py
python scripts/correlation_tracker.py --json
python scripts/correlation_tracker.py --threshold 0.10
```

## Workflow

1. Run `find_edges.py` to scan for arbitrage across all active markets
2. For interesting markets, run `analyze_orderbook.py` to check if the edge is executable
3. Run `momentum_scanner.py` to find markets with directional momentum
4. Combine findings to identify the best opportunities

## Fee Awareness

Most Polymarket markets are fee-free. Crypto 5-min/15-min markets have dynamic taker
fees: `fee = baseRate * min(price, 1 - price) * size`. See `references/fee-model.md`
for the full fee calculator and breakeven analysis.

## Strategy Reference

See `references/viable-strategies.md` for the four strategies that still work in 2026
with win rates, expected returns, and risk profiles.

## Important Disclaimers

- This skill performs read-only analysis only -- no trades are executed
- Past patterns do not guarantee future results
- Always verify opportunities manually before trading
- Not financial advice
