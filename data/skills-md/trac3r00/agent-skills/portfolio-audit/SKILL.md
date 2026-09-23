---
name: portfolio-audit
description: Analyzes an exported portfolio CSV for concentration risk, asset-type allocation drift, and gain/loss. Reads a file you exported yourself (no login, no network, fully offline and deterministic) and warns when any single position or asset class exceeds your stated limits. Covers stocks, crypto, ETFs, and any asset type you label.
when_to_use: You have a brokerage or exchange export and want to know "am I one bad day from a problem" — not what you own, but how much of it is concentrated. NOT a trading tool or a live-price fetcher; it analyzes the snapshot you give it.
version: 1.0.0
license: MIT
metadata:
  agentskills:
    tags: [finance, portfolio, crypto, stocks, risk]
---

# Portfolio Audit

A brokerage export tells you what you own. This tells you whether one position
or one asset class is quietly too big.

## Commands

```bash
python3 scripts/portfolio_audit.py portfolio.csv
python3 scripts/portfolio_audit.py portfolio.csv --json
python3 scripts/portfolio_audit.py portfolio.csv --max-position 0.20 \
    --max-type crypto=0.10
```

## CSV format

Header, any order, case-insensitive:

```csv
symbol,type,quantity,cost_basis,current_price
AAPL,stock,100,150.0,300.0
BTC,crypto,0.5,20000,60000
```

`type` is freeform (stock, crypto, etf, cash...). `cost_basis` and
`current_price` are per-unit.

## Semantics

| Check | Default | Gate |
|---|---|---|
| Single position weight | `--max-position 0.25` | exit 1 when any position exceeds |
| Asset type weight | `--max-type type=weight` | exit 1 when the type exceeds |
| Gain/loss | informational | always reported |

Warnings name the symbol and the actual weight. A clean portfolio (no
concentration, no drift) exits 0.

## Pairs with

`subscription-audit` (the other personal-finance CSV tool — recurring charges
vs asset allocation).
