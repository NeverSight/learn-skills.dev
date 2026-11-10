---
name: portfolio-review
description: |
  Health check for an Indian delivery (CNC) stock portfolio from a holdings CSV or a Zerodha Console,
  Kite, Groww or broker-MCP export: value and unrealised P&L, position and sector weights, top-5/top-10
  concentration, business-group exposure (Adani, Tata...), large/mid/small mix against a target,
  pledged, SME and surveillance flags, a per-lot STCG→LTCG countdown, volatility, beta vs NIFTY,
  drawdown, correlated clusters, portfolio heat to stops, and a tax-aware rebalance plan with charges.

  Use when the user asks: "review my portfolio", "am I too concentrated", "sector allocation of my
  holdings", "how risky is my portfolio / what is my beta", "how much am I risking to my stops",
  "rebalance to equal weight", "what should I trim", "which holdings turn long-term soon", or
  uploads a holdings file from their broker.
---

# Portfolio Review (India)

Look at the whole book before the next trade. This skill reports facts and flags (INFO / WARN /
REVIEW). It never says "sell": every flag is a prompt for the user to re-check a thesis.

## Commands

```bash
python3 scripts/portfolio.py review holdings.csv --cash 200000                    # weights, flags, tax clock
python3 scripts/portfolio.py review console.xlsx --sheet Equity --max-stock 8 --mcap-target 50/30/20
python3 scripts/portfolio.py risk holdings.csv --prices-dir prices/ --benchmark NIFTY    # or --yf
python3 scripts/portfolio.py rebalance holdings.csv --cash 50000                   # equal weight
python3 scripts/portfolio.py rebalance holdings.csv --targets targets.csv --broker groww --realized-ltcg 40000
python3 scripts/portfolio.py rebalance holdings.csv --cash 75000 --no-sell         # deploy new money only
```

Every command takes `--as-of YYYY-MM-DD` and `--json`. `--prices-dir` holds daily candles named
`SYMBOL.csv` or `SYMBOL.json` (any format `../technical-analysis/scripts/ta.py` reads) plus `NIFTY.csv`.
Targets file: `symbol,weight[,price]` or `sector,weight`, in percent. Weight 0 means exit; symbols
or sectors left out stay unchanged. A price column lets you add a stock you do not hold yet.

## Input columns

Required: `symbol`, `qty`, `buy_price` (average cost), `ltp`. Strongly recommended: `buy_date`, with one
row per lot, as in `../indian-tax-for-traders/scripts/tax.py` harvest files. Optional: `sector`,
`mcap` (large/mid/small, or a number in ₹ crore), `group`, `stop`, `pledged_qty`, `series` (EQ/BE/SM...),
`sme`, `illiquid`, `surveillance` (ASM/GSM text), `promoter_pledge` (%), `isin`, `exchange`, `fmv_2018`.

Broker headers are mapped automatically, and preamble rows above the header are skipped:

| Source | Headers recognised | Status |
|---|---|---|
| Kite Connect / Kite MCP `get_holdings` | `tradingsymbol`, `quantity` + `t1_quantity`, `average_price`, `last_price`, `collateral_quantity`, `isin`, `exchange` | Checked against the Kite Connect v3 docs |
| Zerodha Console holdings (XLSX) | Symbol, ISIN, Sector, Quantity Available, Quantity Long Term, Quantity Pledged (Margin/Loan), Average Price, Previous Closing Price | Assumed. Compare with your file |
| Kite web holdings CSV | Instrument, Qty., Avg. cost, LTP, Cur. val | Assumed |
| Groww holdings statement (Reports) | Stock Name, ISIN, Quantity, Average buy price, Buy value, Closing price/value | Assumed. Gives company names, so add a `symbol` column before running `risk --yf` |

Broker MCPs (`broker-integration`): call the holdings tool and write a CSV with one row per holding
using the fields above. Keep the raw field names; the mapper understands them. Broker exports carry
**no buy dates**. Console's "Quantity Long Term" is still used, but for a lot-level countdown, rebuild
open lots with `tax.py tradebook` and add `buy_date`. Keep holdings files local. Do not commit them.

## Defaults and why

| Setting | Default | Reason |
|---|---|---|
| `--max-stock` | 10% of capital | One bad result or fraud should not sink the book. REVIEW above 2× |
| `--max-sector` | 25% | Sectors move together on policy, commodity and rate news |
| `--max-group` | 20% | Group companies share promoters, lenders and governance risk |
| `--mcap-target` | 60/25/15 | A core-heavy mix for a retail investor. Change it to match your plan |
| `--mcap-cutoffs` | ₹1,00,000 cr / ₹33,000 cr | Rough stand-ins for AMFI's rank-based list (top 100 / 101–250). Update every half-year |
| `--loser-pct` | 20% below cost | A decline that big needs a thesis check |
| `--max-heat` | 6% of capital | The total loss if every stop is hit together |
| `--band` / `--min-trade` | 1 pp / ₹1,000 | Avoids churn where DP charges (~₹15 per scrip per sell day) and STT eat the benefit |

Holdings without a `sector` use a built-in map of about 55 NIFTY 50 names, marked `*`, which are also
treated as large caps. Anything else shows as **Unknown**, so add the column.

## Reading the results in an Indian context

- **Your pledge vs promoter pledge.** `pledged_qty` is shares you pledged for F&O margin. A fall shrinks
  collateral and can trigger forced square-offs. `promoter_pledge` above 20% is a governance red flag;
  see `fundamental-screening`.
- **ASM/GSM/ESM and BE/BZ series.** These bring higher margins, trade-for-trade settlement and tight
  price bands. Exits get slow just when you need them.
- **SME stocks** (NSE Emerge, BSE SME; series SM/ST) trade in large lots with thin books. Size them as
  illiquid, whatever their weight.
- **Group concentration.** Three Adani or Tata companies at 8% each fit under the single-stock limit
  but form one 24% bet on a single promoter group. Add a `group` column; a small built-in map covers
  common NIFTY names.
- **Correlated clusters** from `risk`, such as private banks, PSU banks or IT exporters, are where
  diversification is weaker than the stock count suggests.
- **Beta** above about 1.2 means a 10% NIFTY fall is likely to cost more than 10%. With cash, the
  "incl. cash" beta is the one that matters.

## Tax-aware rebalancing

`rebalance` sells oldest lots first (FIFO, as for demat shares) and takes the holding-period rules,
grandfathering and rates from `indian-tax-for-traders` (`tax.py`). Charges come from `trading-costs`
(`../trading-costs/scripts/charges.py`). For each sale it flags:
- **WAIT?** A profitable short-term lot turns long-term within `--wait-days` (default 60). Selling now is
  taxed at 20%; waiting brings it to 12.5%, or nil inside the ₹1.25 lakh exemption. Weigh the tax saved
  against the price risk.
- **LTCG inside the exemption.** Pass `--realized-ltcg` so the remaining exemption is right.
- **Booked losses.** Short-term losses offset STCG or LTCG; long-term losses offset only LTCG.

Prefer `--no-sell` (new SIP or bonus money into underweights) when selling would realise STCG.
For harvesting ideas, run `tax.py harvest` on the same file; `review` already lists them.

## How it fits with other skills

- `market-regime` sets how much equity exposure makes sense. `portfolio-review` checks what you hold.
  In a risk-off regime, look at heat and beta first.
- `sector-rotation` says which sectors lead. Feed its view into a `sector,weight` targets file.
- `position-sizing` and `stop-loss-strategies` supply the `stop` column that makes heat meaningful.
- `trading-discipline` runs the pre-trade gate. Treat heat above the limit, or a WARN on the stock or
  sector you are adding to, as a reason to stop at that gate.

## Output

```
Portfolio review as of 2026-11-01 (6 stocks, 7 lots)
  Holdings ₹8,00,000 | Cash ₹2,00,000 (20.0%) | Total ₹10,00,000 (₹10.00 L)
  Invested ₹7,10,000 | Unrealised P&L ₹90,000 (+12.68%) | Top-5 76.0%
  Sectors (limit 25%): Information Technology 55.0%, Energy 10.5%, ...
  Tax clock: 1 lot turns long-term within 30 days, 1 in 31–60 days
  REVIEW AAA is 30.0% of capital (single-stock limit 10%).
```

Lead with the two or three flags that matter most, then the numbers. Say which inputs were missing
(sector, buy dates, prices). Never turn a flag into an order. Orders follow the `broker-integration`
confirmation protocol.

_Educational analysis, not investment or tax advice. Data: [holdings file + as-of date]._
