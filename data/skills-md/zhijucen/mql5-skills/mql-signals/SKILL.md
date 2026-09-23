---
name: mql-signals
description: >
  MQL5 copy-trading signal investigation on mql5.com. Screens the MT5 signals
  catalog for candidates, deep-dives a signal detail page (statistics, risk
  gauges, reviews, MQL5 system warnings), downloads the trade-history positions
  CSV export and analyses it with the bundled script to verify the published
  numbers and expose strategy shifts, tail risk and dead-hang holding patterns.
  Produces an evidence-based verdict and subscription economics before any
  decision to subscribe or copy a signal.
license: MIT
metadata:
  version: "0.1"
  focus-areas:
    - signal-screening
    - signal-deep-dive
    - trade-history-analysis
    - copy-risk-assessment
---

# MQL5 Signals Investigation Skill

Investigate mql5.com **copy-trading signals** (MetaTrader 5) before
subscribing or deciding which signal looks trustworthy. The workflow
screens candidates, extracts every metric from the detail page, pulls the
full trade history via the CSV export, and lets the analyzer script do the
forensics. The goal is a verdict the user can act on.

## When to use

- The user asks "which signal looks best / should I subscribe?" or wants to
  compare signal candidates on mql5.com.
- The user supplies a signal URL (`https://www.mql5.com/en/signals/<ID>`,
  `.../signals/mt5`, ...) or a downloaded positions CSV and wants it analysed.
- The user wants red flags checked: exaggerated growth, strategy changes,
  hidden capital injections, unresolved drawdown, copy failures, dead-hang
  (holding losers) behaviour.

## Pipeline overview

```
1. Screen catalog     -> shortlist candidates + quick kills
2. Deep dive page     -> record every metric + risk gauge + reviews + warnings
3. CSV export         -> download /en/signals/<ID>/export/positions
4. Analyse (script)   -> verify numbers, find strategy shifts / tail / holdings
5. Verdict            -> evidence-based recommendation + subscription economics
```

## Step 1 — Screen the catalog

Open `https://www.mql5.com/en/signals/mt5` (or `/mt5/pageN` / `/mt5/forex`)
and collect candidate cards: name, author, reliability rating, price,
subscribers, growth % and "growth since YEAR". Prefer candidates that appear
in **several** curated lists (Reliability / Popular / High score / asset tab).

Quick kills at catalogue level:
- No reviews at all + designer stats -> untestable, treat as unproven.
- "Growth since <current year> -1" (e.g. since 2026) with 900%+ -> tiny account
  base or too short to mean anything.
- Brand-new accounts (started this year) with huge monthly growth -> usually
  grid/martingale-style; verify in Step 2.
- Price at 999 USD with 0 subscribers -> marketing grade; skip unless asked.

## Step 2 — Deep dive the detail page

Record the following into a table; every field is on the page:

**Account card**: price, broker server, leverage, initial deposit,
deposits/withdrawals (provider funding flows), equity/balance/profit, growth.
**Risk gauges**: Profit Trades %, Trading activity %, Max deposit load %,
Maximum drawdown %, Algo trading %.
**Statistics block**: trades, best/worst trade, gross profit/loss (USD+pips),
consecutive wins/losses, Sharpe Ratio, Profit Factor, Recovery Factor,
Expected Payoff, average win vs average loss, Monthly growth %, Annual
Forecast %, long/short mix, drawdown by balance AND by equity.
**Charts/tables**: month-by-month growth & profit per year, equity and
drawdown axes.
**Distribution**: per-symbol deals / USD / pips.
**Slippage table**: per broker-server average slippage and copy count.
**Reviews**: see /references/signals-analysis.md §"Review mining".
**What's new**: MQL5 system warnings (see red-flag taxonomy below).

Interpretation rules of thumb (details in the reference doc):
- `Growth %` is meaningless without the account base: an initial deposit of
  10-50 USD makes any % astronomically large. Judge absolute profit instead.
- Large `Deposits` with matching `Withdrawals` = provider pools money in/out
  (normal). Large net deposits with no withdrawals = possible capital masking.
- `Average Loss > Average Win` needs an extremely high win rate to survive;
  pair it with `Maximum drawdown` and the tail from the CSV.
- `Sharpe < 0.2` and `Deposit load > 30%` -> high variance, position-sizing risk.
- **MQL5 has its own risk engine** — read its warnings literally:
  - "80% of growth achieved within N days ... X% of days" -> burst-concentrated
    growth, the single strongest overclaim signal (Growth 300%+ hides this).
  - "Too much growth in the last month indicates a high risk".
  - "No trading activity ... last 6 days" / "Low trading activity - only N
    trades" -> inactivity episodes or maintenance gaps.
  - "Too frequent deals may negatively impact copying results" -> copy-quality
    risk on subscriber accounts.
  - "Signal account leverage was changed ... 1:500 - 1:2000" -> leverage to
    1:2000+ is an account-blender signature.
  - "No swaps are charged" -> multi-day positions cost the provider nothing,
    subscriber swap cost is hidden.

## Step 3 — CSV export and analysis

The web "Trading history" tab hides trade rows behind a subscription, but the
export endpoint returns the full history to any **logged-in** user:

```
Trading history tab -> "Export to CSV: History"  (file: <ID>.positions.csv)
```

Format (verified): UTF-8 BOM, `;`-separated, header
`Time;Type;Volume;Symbol;Price;Volume;Time;Price;Commission;Swap;Profit`,
Buy/Sell rows = closed deals, other rows = balance ops, `Profit` excludes
commission/swap (net = Profit + Commission + Swap).

Run the analyzer (stdlib only, no dependencies):

```bash
python skills/mql-signals/scripts/analyze_signals_csv.py \
  <ID>.positions.csv \
  --page-trades 1875 --page-profit 7120.51 --page-win 1386
```

`--page-*` values come straight from Step 2 and let the tool print a
**reconciliation** line (hidden trades, profit delta vs page). Add `--json`
for machine-readable output; `--min-held-days`, `--recent-days`,
`--from-month` tune the analysis. Read the output as follows:

- **per year** (n / avg lot / median holding / sum lot / net) — a year whose
  n or lot or holding mode changes >3x is a **strategy shift** (compare to
  review complaints like "strategy changed without notice").
- **per symbol** — separates the profit core from experimental additions
  (indices/gold added late often lose money).
- **monthly net** — pinpoints the loss months.
- **tail risk** — worst-k sums and "worst 1% share of all losses".
- **max consecutive losses** — run length on chronological losing close.
- **holding >= N days** — net negative with losses >> wins = the dead-hang
  signature ("winners cut, losers held").
- **recent N days** — current regime health.
- **funding ops** — deposit/withdrawal forensics from balance rows.

The tool auto-prints a `-- flagged --` block when it detects strategy shifts,
dead-hang patterns, tail concentration, lot spikes or funding anomalies.

## Step 4 — Verdict

Combine page evidence + CSV evidence into tiers:
- **Verified sound**: long track record (years), no "80% growth" bursts, no
  dead-hang signature, stable per-month curve, provider transparent about
  funding flows, current regime active.
- **Conditional**: good core + a documented bad episode (e.g. one loss year
  caused by a strategy experiment) — usable with sized-down copy and a
  drawdown stop.
- **Reject**: burst-growth warnings, no-SLTP grid strategy, leverage 2000+,
  capital masking, copy-failure complaints at scale.

Subscription economics (always compute — a signal must pay for itself):
`fee  <=  monthly_growth_pct * balance / 100`. Monthly growth of ~1% with a
30 EUR fee needs a ~3000 EUR account just to break even; say so plainly.

Copy-side advice that is quasi-universal:
- Match the provider's broker server family (slippage table: prefer brokers
  with low median slippage AND high copy counts).
- Add a subscriber-side drawdown stop ("stop copying if DD > X%") — most
  signals have no SL culture.
- The author's own "recommended minimum deposit" is a floor, not a
  suggestion — smaller accounts lose the fee plus slippage.

## Step 5 — Report format

Deliver a short report with: basic info block, statistics table, monthly
history table, per-symbol table, red flags found (page-level and CSV-level),
subscription economics, and a one-line verdict per tier above.

## Structure

```
skills/mql-signals/
├── SKILL.md                          # this file
├── scripts/
│   └── analyze_signals_csv.py        # positions CSV forensics (stdlib-only)
└── references/
    └── signals-analysis.md           # metric cheat sheet + red-flag taxonomy
```

See `references/signals-analysis.md` for the full metric interpretation and
red-flag taxonomy, and the worked example of the 2271402 signal that this
methodology was built on.