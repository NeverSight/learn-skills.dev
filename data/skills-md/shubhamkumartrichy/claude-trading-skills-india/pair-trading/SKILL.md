---
name: pair-trading
description: |
  Statistical pair trading (market-neutral long/short) for NSE stocks. pairs.py tests whether two
  stocks are cointegrated (Engle-Granger with an ADF on residuals, judged against MacKinnon's
  cointegration critical values), estimates the hedge ratio, half-life and current spread z-score,
  screens every same-sector pair with a Bonferroni caution, lists in-sample z-score trades with a
  hit rate, and plans Indian execution: stock futures in whole lots, residual hedge mismatch,
  margin, charges, last-Tuesday rollover, F&O ban and lot-size revisions. Stdlib only; offline CSVs.

  Use when the user asks: "is HDFCBANK/ICICIBANK a good pair", "are TCS and INFY cointegrated",
  "find pairs in the bank/IT sector", "what is the z-score of the BPCL-HPCL spread", "pair trade
  entry and exit", "hedge ratio between two stocks", "how many lots for a pair trade", "how do I
  short the other leg in India", or wants a market-neutral or relative-value trade.
---

# Pair Trading (NSE)

Two stocks that share the same economics (two private banks, two oil marketing companies) can
drift apart for weeks, then close the gap. A pair trade is long the cheap one and short the rich
one, sized so the market move cancels out. This works only if the gap is statistically
mean-reverting (cointegrated). A high correlation is not enough.

## 1. Run it

```bash
python3 scripts/pairs.py test HDFCBANK ICICIBANK --csv-dir stocks/      # one pair, full statistics
python3 scripts/pairs.py screen --members members.csv --csv-dir stocks/   # all same-sector pairs
python3 scripts/pairs.py signal BPCL HPCL --csv-dir stocks/ --exit 0.5    # rules + in-sample trades
python3 scripts/pairs.py plan BPCL HPCL --csv-dir stocks/ --lots-csv fo_mktlots.csv \
    --ban-list fo_secban.csv --margin-a 120000 --margin-b 110000          # India execution
```
Without `--csv-dir`, prices come from Yahoo (`pip install yfinance`). Create offline CSVs with
`../technical-analysis/scripts/ta.py fetch --symbol TCS --out stocks/TCS.csv`. Only a date and a
close column are needed; a volume column turns on the liquidity filter. Use split and bonus-adjusted
closes. `--members` is a `symbol,sector` CSV. Common options: `--lookback 500` sessions (0 = all),
`--end YYYY-MM-DD` (re-test an earlier window), `--window 60` (z-score), `--entry 2 --exit 0
--stop 3.5`, `--adf-lag N` or `--max-lag N`, `--splits 3`, `--max-half-life 40`, `--json`.
Screen adds `--min-bars 250 --min-turnover 10` (₹ crore a day) `--min-corr 0.5 --top 20`.

## 2. What it computes

| Statistic | How |
|---|---|
| Correlation | Pearson correlation of daily log returns on common dates |
| Hedge ratio β | OLS of ln A on ln B. Hold ₹β of B against each ₹1 of A. Also reverse OLS and total least squares |
| Cointegration | Engle-Granger: ADF (no constant) on the OLS residuals, lag by AIC (Schwert maximum) or fixed |
| Critical values | MacKinnon (2010) Table 2, N = 2 with constant: ≈ −3.90 / −3.34 / −3.04 (1/5/10%) plus a T-adjustment. These are stricter than plain Dickey-Fuller values (≈ −2.86 at 5%) because β was fitted |
| p-value | MacKinnon (1994) asymptotic surface. Use it for ranking; the critical values decide |
| Half-life | AR(1) on the spread: s_t = c + φ·s_{t−1}; half-life = ln 0.5 / ln φ sessions |
| z-score | (spread − 60-session mean) / 60-session sd |
| Stability | β in 3 consecutive sub-periods; drift ≤ 25% of β = stable, > 50% = unstable |

Both regression directions are tested. A pair counts only if both reject the unit root.

## 3. Reading the result

- **Candidate:** rejected at 5% or better both ways, half-life 1–40 sessions (`--max-half-life`;
  3–20 fits a monthly futures cycle best) and β stable. Then look at the z-score.
- **Half-life sets the trade.** A 5-session half-life suits a 1–3 week trade inside one futures
  month. A 40-session half-life means several rollovers and more charges for the same reversion.
- **z ≥ +2:** A is rich against B, so short the spread (sell A, buy B). **z ≤ −2:** long the spread.
  **|z| beyond 3.5:** do not add. The relationship may be breaking, often because of news.
- **High correlation without cointegration** (common in a sector rally) means the stocks move
  together day to day, but the gap can trend for months. Do not trade it as mean reversion.

## 4. Signals (in-sample)

`signal` enters at |z| ≥ 2 once |z| has reset inside the band. It exits when z returns to 0 (or
±0.5 with `--exit 0.5`), stops at |z| ≥ 3.5, and time-stops after 2× the half-life
(`--max-hold`, `--time-stop-mult`). Each trade is returned as % of gross notional. **The trade list
is in-sample:** β, the test and the half-life all come from the same data, so the hit rate is an
optimistic upper bound and excludes costs. Check out of sample: run `test` with `--end` six
months back, then see whether the pair still holds on the newer data.

## 5. Executing in India (`plan`)

- **The short leg.** Cash-market shorts must be covered the same day. A short left undelivered
  goes to the exchange auction and pays a close-out penalty. Multi-day pairs therefore use **stock
  futures**: both legs (default), or `--legs cash-long` to buy the long leg for delivery and short
  the other leg in futures. SLB (stock lending) exists but is thin.
- **Whole lots.** A stock-futures lot is several lakh rupees, so β rarely maps to whole lots.
  `plan` rounds the B leg, reports the residual mismatch in % and ₹, and lists the lot combinations
  with the tightest hedge. With `--legs cash-long`, the delivery leg is sized in shares.
- **Lot sizes:** `--lot-a/--lot-b`, or `--lots-csv` with NSE's `fo_mktlots.csv` (one column per
  contract month). NSE revises lot sizes periodically, and corporate actions adjust them. If the
  file shows a different size in a later month, the plan flags it: re-size the hedge when you roll.
- **Margin:** `--margin-a/--margin-b` (₹ per lot from your broker), otherwise `--margin-pct 25` of
  contract value per leg. Margin is summed leg by leg. A long/short across two different stocks is
  not a recognised spread, so do not count on a hedge margin benefit. Futures are marked to market
  daily, so keep a buffer.
- **Charges** come from `../trading-costs/scripts/charges.py` (futures STT 0.05% on the sell side
  since Apr 2026). The plan counts one round trip per leg plus one per roll, and futures carry (the
  long leg pays it, the short earns it).
- **Rollover:** stock futures expire on the last Tuesday of the month, or the previous trading day
  if that is a holiday (from `../fno-options-analysis/scripts/options.py`). They are physically
  settled. The plan lists roll-by dates within the expected hold (2× half-life). Near expiry, it
  switches to the next month.
- **F&O ban:** a stock enters the ban when OI crosses 95% of MWPL, and stays until it falls below
  80%. In a ban you can only reduce, so you cannot open the pair or roll the leg. Pass
  `--ban-list` (NSE `fo_secban.csv`), `--banned SYM`, or `--mwpl-a/--mwpl-b` (%). See
  `indian-market-structure`.

## 6. Classic Indian pairs to test (not recommendations)

HDFCBANK/ICICIBANK, KOTAKBANK/AXISBANK, SBIN/BANKBARODA, TCS/INFY, HCLTECH/WIPRO, BPCL/HPCL
(IOC as a third), ULTRACEMCO/SHREECEM, TATASTEEL/JSWSTEEL. They share sector, regulation and
macro drivers. That makes them worth testing, not cointegrated by default. Re-test every quarter.

## 7. Pitfalls

- **Structural breaks:** mergers and demergers end relationships. HDFC Ltd merged into HDFC Bank
  in July 2023, which ended the classic HDFC/HDFCBANK pair. A demerger (Jio Financial out of
  Reliance, 2023) leaves a price gap in unadjusted data. Results, management changes and
  regulatory actions can break a pair for good. A stop is for that case, not for noise.
- **Corporate actions:** use adjusted closes for splits and bonuses. A large special dividend shows
  up as a spread jump on the ex-date.
- **Look-ahead:** in-sample signals use tomorrow's β today. Expect worse results live.
- **Multiple testing:** 10 bank stocks give 45 pairs. At 5%, about 2 will pass by chance. Apply a
  Bonferroni-style bar (0.05 / 45 ≈ 0.001), which `screen` reports, and confirm on a later window.
- **Short samples:** under about 250 sessions, the test has little power and β is noisy.
- **Results season:** a quarterly result on one leg alone can blow through the stop. Know both dates.

## Related skills

Size the risk-to-stop rupee figure with `position-sizing`; compare broker costs in `trading-costs`;
ban and margin rules in `indian-market-structure`; expiries in `fno-options-analysis`; sector
backdrop in `sector-rotation`.

## Output

```
Pair A / B: N sessions [from → to] | corr r | β (OLS / TLS) | EG t = x vs 5% crit y → reject? p≈
Half-life H sessions | z now Z → zone | β stability: stable/drifting/unstable | verdict
Signal (in-sample): trades n, hit rate h%, avg r% | now: flat / open / signal
Plan: SELL A fut n lots / BUY B fut m lots | mismatch ±x% | margin ₹ | charges ₹ | roll by date
Risks: F&O ban, lot revision, results dates, structural break
```

_Educational analysis, not investment advice._
