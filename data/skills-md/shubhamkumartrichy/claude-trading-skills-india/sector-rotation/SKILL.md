---
name: sector-rotation
description: |
  Sector rotation across NSE sectoral and thematic indices (BANK, IT, AUTO, PHARMA, FMCG, METAL,
  REALTY, ENERGY, PSU BANK, FIN SERVICE, INFRA, PSE, CONSUMPTION and more) against NIFTY 50:
  1W–12M returns, relative strength, an RRG-style RS-Ratio/RS-Momentum quadrant with recent
  quadrant changes, distance from 50/200 DMA, cyclical-vs-defensive tilt, the midcap/smallcap size
  factor, and member breadth. sectors.py works offline from niftyindices.com CSVs or via yfinance.

  Use when the user asks: "which sectors are leading", "sector rotation", "where is money moving",
  "is the market risk-on or defensive", "are midcaps and smallcaps outperforming", "RRG for NSE
  sectors", "which sector should I focus on", "is IT/PSU bank/metal turning", or wants sector
  context before picking stocks.
---

# Sector Rotation (NSE)

Find where relative strength is building and where it is fading, then fish for setups in the
strongest groups. This is a context filter: it tells you which pond, not which fish or when.

## 1. Run it

```bash
python3 scripts/sectors.py rotation                       # Yahoo (pip install yfinance), default universe
python3 scripts/sectors.py rotation --csv-dir nse_idx/    # offline: one CSV per index + "NIFTY 50.csv"
python3 scripts/sectors.py rrg --sectors IT,BANK,METAL,PSUBANK --tail 10   # weekly trail, for plotting
python3 scripts/sectors.py breadth --members members.csv --csv-dir stocks/
python3 scripts/sectors.py universe                       # tickers and Yahoo coverage
```
`--json` gives raw output. Options: `--weeks 8` (quadrant-change look-back), `--smooth 3 --window 10
--momentum 4` (RRG settings, weeks), `--period 2y`, `--ticker NAME=TICKER` / `--map file.json` to
override or add tickers (`--ticker NIFTY=^CRSLDX` benchmarks against NIFTY 500).

**Offline CSVs:** download each index from niftyindices.com (Historical Data, price index). Name each
file after the index ("NIFTY IT.csv", "NIFTY PSU BANK.csv"); names are matched to keys
automatically. Only a date and a close column are needed. Open/High/Low, "Shares Traded" and
"Turnover" are ignored, and no volume is required. Dates like `30 Oct 2026`, `30-Oct-2026` or ISO all
parse. Daily data is best; weekly closes also work (DMAs become 10/40-week averages).

**Yahoo coverage (probed 2026-10-31).** History available: `^NSEI`, `^NSEBANK`, `^CNXIT`, `^CNXAUTO`,
`^CNXPHARMA`, `^CNXFMCG`, `^CNXMETAL`, `^CNXREALTY`, `^CNXENERGY`, `^CNXPSUBANK`, `^CNXINFRA`,
`^CNXPSE`, `^CNXCONSUM`, `^CNXMNC`, `NIFTY_FIN_SERVICE.NS`, `NIFTYMIDCAP150.NS`, `NIFTYSMLCAP250.NS`.
Quote only, no history: NIFTY MEDIA, PRIVATE BANK, HEALTHCARE, OIL & GAS, CPSE, INDIA DEFENCE,
CAPITAL MARKETS, MIDCAP 100 and SMALLCAP 100. Supply these as CSVs. Run `universe` for the full map.

## 2. What it measures

| Metric | Definition |
|---|---|
| Returns | 1W/1M/3M/6M/12M = 5/21/63/126/252 sessions; `rel` = (1+sector)/(1+NIFTY) − 1 |
| RS line | 100 × sector ÷ NIFTY, sampled at each week's last close |
| RS-Ratio | 100 × EMA3(RS) ÷ SMA10 of that EMA. Above 100 = relative trend above its 10-week norm |
| RS-Momentum | 100 × RS-Ratio now ÷ RS-Ratio 4 weeks ago. Above 100 = relative trend improving |
| Quadrant | Leading (≥100/≥100) → Weakening (≥100/<100) → Lagging (<100/<100) → Improving (<100/≥100) |
| Trend | Uptrend, Downtrend, Recovering (above a falling 50 DMA), Pullback (below a rising one), Mixed |
| Rank | (RS-Ratio − 100) + (RS-Momentum − 100) |

Both axes are percentages and are not volatility-scaled, so REALTY and PSU BANK swing wider than
FMCG. Compare quadrant, direction and weeks in quadrant, not raw distance. Rotation usually runs
clockwise. A diagonal jump (Leading straight to Lagging) is a whipsaw near the centre. That was about
9% of quadrant changes on 10 years of NSE data; wait a second week before trusting it.

**Reading it:** Improving with a rising RS-Ratio is the early long watch-list. Leading plus an Uptrend
is where breakouts follow through. Weakening means tighten trails and stop adding. Lagging plus a
Downtrend is a short or avoid list. A sector that is only Improving but still below its 200 DMA is a
bounce until its price trend confirms.

## 3. Rotation read (India)

- **Cyclical / domestic beta:** METAL, REALTY, PSU BANK, AUTO, INFRA. Their earnings ride credit
  growth, government capex, commodity prices and rate cuts.
- **Defensive:** IT, PHARMA, HEALTHCARE, FMCG. IT and pharma are dollar earners that gain when the
  rupee weakens, and they often hold up when FIIs sell India. FMCG has steady staples demand. IT is
  defensive only versus the Indian cycle: it still tracks US tech spending.
- **Kept out of the tilt:** BANK, FIN SERVICE and PVT BANK. These heavyweights are about a third of NIFTY
  and largely *are* the benchmark. ENERGY and OIL & GAS track crude. PSE, CPSE, DEFENCE, CAPITAL
  MARKETS, CONSUMPTION, MNC and MEDIA are reported as themes.
- **Tilt:** cyclicals' average RS-Ratio minus the defensives'. Above +0.5, with the 3M relative
  return agreeing, the read is risk-on. Below −0.5 it is defensive. Anything else is mixed.
- **Size factor:** MIDCAP 150/SMALLCAP 250 vs NIFTY. Both outperforming means broadening, which is
  healthy retail and DII risk appetite. Both lagging means narrowing into large caps, which often
  precedes or accompanies corrections. Smallcaps rolling over first is an early warning.

| Driver | Sectors to check | Typical read |
|---|---|---|
| FII flows (NSDL fortnightly data) | BANK, FIN SERVICE, IT | FII buying lifts private banks first; persistent selling drags them while DII-held mid/small caps hold up |
| Rupee (USD/INR) | IT, PHARMA vs importers | Weak rupee helps exporters' margins and hurts OMCs and capital-goods importers |
| Crude (Brent) | OIL & GAS, ENERGY, paints, tyres, aviation | Falling crude helps OMCs (BPCL, HPCL, IOC), paints and tyres; rising crude helps upstream (ONGC, Oil India) |
| Monsoon and rural demand (IMD, Jun–Sep) | FMCG, AUTO (tractors, 2-wheelers) | A good monsoon helps rural volumes; watch the Sep–Nov festive season |
| Union Budget (1 Feb) and capex | PSE, CPSE, INFRA, DEFENCE, PSU BANK | Capex or divestment themes run into the Budget and can fade after it |
| RBI rate cycle (MPC) | BANK, REALTY, AUTO, NBFCs (FIN SERVICE) | Cuts help realty, auto and NBFCs; banks' margins can compress early in a cutting cycle |
| Global metals and China | METAL | LME prices, China stimulus and steel safeguard duties |

## 4. Breadth inside a sector

`breadth` reports the percentage of members above their 50 and 200 DMA. `--members` takes a CSV of
`sector,symbol`, and `--csv-dir` holds one CSV per stock. Create the stock CSVs with
`../technical-analysis/scripts/ta.py fetch --symbol TCS --out stocks/TCS.csv`. Membership comes from
the index factsheet on niftyindices.com. An index Leading on fewer than 50% of members above their
50 DMA is being carried by one or two heavyweights, so its leadership is narrow.

## 5. How other skills use this

- **`market-pulse`:** fill the "Sectors" line with Leading/Improving vs Lagging, the tilt and the
  size read from `rotation`, instead of ranking 1-week returns by hand. Suggested wording there:
  "Sectors: run sector-rotation; quote quadrant leaders, tilt and size factor".
- **`india-market-analyst`:** at the Context stage, look up the stock's sector quadrant. Prefer longs
  in Leading or Improving sectors that are in an Uptrend. Flag a long in a Lagging, Downtrend sector
  as swimming against the tide. Then hand off to `technical-analysis` for the stock (and
  `multi-timeframe-analysis` on the sector index itself).

## Caveats

- NSE reconstitutes sector indices semi-annually and changes weights through capping. Very long RS
  histories mix different baskets. Concentrated indices (NIFTY IT, BANK, METAL) can turn on one stock.
- Yahoo has gaps and late bars for some indices. The script warns when an index ends more than 3 days
  before NIFTY, or when the data is stale. Prefer niftyindices.com CSVs for anything you act on.
- A mid-week run treats the partial week as the latest weekly point. Re-check after Friday's close.
- Price indices exclude dividends, so high-yield PSE and energy look slightly weaker than their total
  return. Relative strength is not absolute: a Leading sector in a falling market can still lose money.

## Output

```
Sector rotation vs NIFTY 50: data to [date] ([source])
Leading: .. | Improving: .. | Weakening: .. | Lagging: ..
Tilt: [Risk-on/Defensive/Mixed]: [spread] | Size: [Broadening/Narrowing/Mixed]
Key changes ([N] weeks): [sector from→to (week)]
Watch-list: [Improving + rising RS-Ratio] | Avoid: [Lagging + Downtrend]
Drivers to verify: [FII flows / USD-INR / crude / RBI / Budget, with sources]
```

_Educational analysis, not investment advice. Data: [sources + timestamps]._
