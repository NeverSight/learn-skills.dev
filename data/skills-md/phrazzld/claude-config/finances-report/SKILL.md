---
name: finances-report
description: |
  Generate financial analytics and insights from ~/Documents/finances/ data.
  Terminal report shows: net worth trends (30d/90d/1y), asset allocation, liability
  table with APR and monthly interest, cash flow (last 30 days), Bitcoin detail with
  sparkline. HTML dashboard: interactive plotly charts for all of the above over time.
  Use when: reviewing finances, answering questions about net worth, spending patterns,
  debt paydown progress, Bitcoin holdings, asset allocation. Keywords: financial report,
  net worth, spending, cash flow, debt, liabilities, bitcoin, how am I doing financially,
  finances summary, show me my finances, portfolio.
user-invocable: true
effort: low
---

# finances-report

Generate financial analytics from the local ledger.

## Terminal Report (default)

```bash
cd ~/Documents/finances && uv run python scripts/report.py
```

Sections: Net Worth (with 30d/90d/1y deltas), Asset Allocation, Liabilities (APR +
monthly interest), Cash Flow (last 30 days + top categories), Bitcoin detail + sparkline.

Single section:
```bash
uv run python scripts/report.py --section networth
uv run python scripts/report.py --section liabilities
uv run python scripts/report.py --section cashflow
```

## HTML Dashboard

```bash
cd ~/Documents/finances && uv run python scripts/report.py --html
```

Opens `reports/dashboard-YYYY-MM-DD.html` — interactive plotly charts:
- Net worth over time (USD + BTC dual axis)
- Asset allocation over time (stacked area)
- Monthly cash flow (income vs spending bars)
- Liability balances over time
- BTC price history

## Data Sources

- `data/snapshots.jsonl` — net worth history (175+ entries back to 2022)
- `data/transactions/copilot.jsonl` — 10K+ transactions for cash flow analysis
- `data/prices/*.jsonl` — BTC/gold/silver price history
- `data/liabilities.jsonl` — liability history with APRs
