---
name: findata
description: >-
  Free, keyless financial data via CDP. Stock price snapshots and historical
  OHLCV (Yahoo Finance) plus income / balance-sheet / cash-flow statements
  (SEC EDGAR XBRL). No API key, no account. Returns structured JSON or
  pretty-printed tables. Requires browser-harness-js on PATH and a running
  Chromium-based browser with remote debugging.
setup: bash <skill-dir>/scripts/setup
compatibility: Requires browser-harness-js on PATH and a running Chromium-based browser with remote debugging (chrome://inspect or --remote-debugging-port). No API key. Statements come from SEC EDGAR (public, free); prices from Yahoo Finance's chart API (rendered through the browser to bypass bot blocks).
---

# findata — free financial data via CDP

Free, keyless financial data scraped/fetched through a real browser via CDP — the same data the paid `financialdatasets.ai` API sells, but sourced directly from the free public origins (SEC EDGAR for statements, Yahoo Finance for prices). Each call opens its own tab and WebSocket session — safe for parallel use.

## Commands

```bash
findata price    <ticker>                                          # live/last price snapshot
findata prices   <ticker> [--range 1mo|--start S --end E] [--interval 1d] [--limit N]
findata income   <ticker> [--period annual|quarterly] [--limit N]  # income statement
findata balance  <ticker> [--period annual|quarterly] [--limit N]  # balance sheet
findata cashflow <ticker> [--period annual|quarterly] [--limit N]  # cash flow statement
findata --json   <command> ...                                     # raw JSON instead of pretty table
```

| Flag | Applies to | Meaning |
|------|-----------|---------|
| `--json`            | all            | Emit raw JSON instead of pretty-printed text |
| `--period annual\|quarterly` | statements | Reporting period (default `annual`) |
| `--limit N`         | statements/prices | Statements: periods to show (default 4, 0 = up to 40). Prices: most-recent N bars (default all) |
| `--range R`         | prices         | Yahoo range: `1d 5d 1mo 3mo 6mo 1y 2y 5y 10y ytd max` (default `1mo`) |
| `--start`/`--end YYYY-MM-DD` | prices | Exact date range (alternative to `--range`; needs `node`) |
| `--interval R`      | prices         | Bar interval: `1m 2m 5m 15m 30m 60m 1d 5d 1wk 1mo` (default `1d`) |

### Examples

```bash
findata price AAPL
findata prices TSLA --range 3mo --interval 1wk
findata prices MSFT --start 2025-01-01 --end 2025-06-30 --limit 5
findata income AAPL --period quarterly --limit 4 --json
findata balance NVDA --limit 2
findata cashflow AAPL

# Parallel — each call uses its own tab
findata price AAPL &  findata price MSFT &  wait
```

## Result shapes

**`price`** (snapshot):
```json
{"ticker":"AAPL","name":"Apple Inc.","price":310.05,"previous_close":308.63,
 "change":1.42,"change_percent":0.46,"currency":"USD","exchange":"NMS",
 "time":"2026-07-06T14:16:41Z"}
```
`previous_close` is the prior trading day's close (derived from the second-to-last daily bar), not the start-of-range close — so `change` is the true day-over-day move. `price` is the live/last trade (`regularMarketPrice`).

**`prices`** (historical OHLCV):
```json
{"ticker":"AAPL","name":"Apple Inc.","currency":"USD","interval":"1d","prices":[
  {"date":"2026-07-02","open":294.12,"high":309.42,"low":293.68,"close":308.63,"volume":75352800,"adj_close":308.63}
]}
```

**`income` / `balance` / `cashflow`** (statements):
```json
{"ticker":"AAPL","name":"Apple Inc.","cik":320193,"period":"annual","statement":"income",
 "statements":[{
   "period_end":"2025-09-27","fiscal_year":2025,"fiscal_period":"FY","form":"10-K",
   "filed":"2025-10-31","accession":"0000320193-25-000079",
   "filing_url":"https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/0000320193-25-000079-index.htm",
   "revenue":416161000000,"cost_of_revenue":220960000000,"gross_profit":195201000000,
   "operating_income":133050000000,"net_income":112010000000,
   "eps_basic":7.49,"eps_diluted":7.46,"shares_basic":14948500000,"shares_diluted":15004697000
 }]}
```
Each statement object carries `period_end`, `fiscal_year`, `fiscal_period`, `form`, `filed`, `accession`, `filing_url` for traceability back to the SEC filing, plus the line-item fields. `cashflow` adds a derived `free_cash_flow = operating_cf + capex`.

### Statement fields

- **income**: `revenue, cost_of_revenue, gross_profit, operating_expenses, sgna, rnd, operating_income, interest_expense, income_tax, net_income, eps_basic, eps_diluted, shares_basic, shares_diluted, dividends_per_share`
- **balance**: `total_assets, current_assets, cash, inventory, investments, total_liabilities, current_liabilities, long_term_debt, total_debt, equity, retained_earnings, shares_outstanding`
- **cashflow**: `net_income, operating_cf, capex, investing_cf, financing_cf, dividends_paid, share_repurchases, debt_repayment, free_cash_flow`

Each field maps to one or more candidate US-GAAP XBRL concepts (preferred order); the concept whose most recent period is latest wins, so a stale legacy concept (e.g. `Revenues` after a company switches to `RevenueFromContractWithCustomerExcludingAssessedTax`) never shadows the current one.

## How it works

| Data | Source | CDP technique |
|------|--------|----------------|
| Prices | `query1.finance.yahoo.com/v8/finance/chart/<ticker>?interval=&range=&period1=&period2=` | **Event-driven fetch**: navigate to the JSON URL, wait for the `Page.frameNavigated` commit (which *does* fire for `application/json`, unlike `loadEventFired`/`networkIdle`), then a same-origin `fetch(window.location.href)` returns the raw body without waiting for Chrome's JSON-viewer to render it into the DOM. The async projection IIFE runs with `awaitPromise`. Yahoo's chart endpoint returns clean OHLCV + `regularMarketPrice` as JSON — no DOM scraping. Going through the browser sidesteps the crumb/consent walls that block `curl`. |
| Ticker→CIK | `www.sec.gov/files/company_tickers.json` | Same event-driven fetch; parsed into a map cached on `globalThis.__secTickerMap` for the server's lifetime (one fetch per session). |
| Statements | `data.sec.gov/api/xbrl/companyfacts/CIK<padded>.json` (SEC EDGAR XBRL) | **Readiness poll** (not the fetch path — see below). Navigate to the JSON URL, then poll the in-page projection IIFE every ~80ms until it reports `{ready:true}`. Top-level navigation bypasses CORS; only the small projection crosses CDP, so the multi-MB companyfacts object stays in the page. |

**Why two capture strategies.** JSON navigations fire *neither* `Page.loadEventFired` *nor* `networkIdle` (verified), so the event-driven wait `gsearch`/`xsearch` use doesn't apply directly. `Page.frameNavigated` *does* fire on commit, and a same-origin `fetch` after it returns the raw body the instant it's downloaded — skipping the JSON-viewer render entirely. That's a clear win for **small** endpoints (prices ~0.3s, ticker map ~0.25s), where the viewer render is pure overhead with little parse to reuse.

For the **multi-MB companyfacts**, the opposite is true: by the time `document.body.innerText` is ready, Chrome's JSON viewer has *already parsed* the 3.7 MB body, so the projection's own `JSON.parse` is nearly free (~16 ms). A cold `fetch`+parse costs ~800 ms there, so polling (total ~1.1s) beats the fetch path (~1.5s). The clean way to skip the viewer render there would be `Network.getResponseBody` at `loadingFinished` (~0.56s), but that crashes the harness's WebSocket on multi-MB bodies, so polling is kept for companyfacts.

Per call: `Target.createTarget(about:blank, background)` → `Target.attachToTarget` → per-call `sessionId` → navigate + (fetch | poll) → fire-and-forget `closeTab` in `finally`. Same pattern as `gsearch`/`xsearch` — safe for parallel use, no `activeSessionId` clobbering.

**Typical latency** (warm server, cold HTTP cache): `price` / `prices` ~0.3s, statements ~1.1–1.4s (the companyfacts download + parse dominates; the first statement call per session adds ~0.25s for the one-time ticker-map fetch). Warm HTTP cache cuts prices to ~0.25s.

## Why these sources

- **SEC EDGAR for statements**: it is the *source of truth* — `financialdatasets.ai`'s statements are derived from it (their JSON even carries the same SEC `accession_number` and `filing_url`). Free, keyless, structured JSON, both annual (10-K) and quarterly (10-Q). No reason to go anywhere else.
- **Yahoo Finance v8 chart for prices**: the only free source that returns OHLCV as structured JSON (not an HTML table) and covers snapshot + history + intraday in one endpoint. `curl` is blocked by bot protection on every free price site; the browser bypasses it. (`stockanalysis.com` 403s `curl` and shows a Cloudflare "Just a moment…" wall even to a real browser; Yahoo's quote page is inconsistent due to EU consent redirects — but its JSON chart endpoint works cleanly through the browser.)

## Traps

- **Quarterly statements are YTD cumulative, not per-quarter.** SEC 10-Q facts are reported year-to-date within the fiscal year (a Q3 figure is the 9-month cumulative). `findata` returns **as-reported** values — it does not difference them into 3-month stubs. This matches the filing; if you need per-quarter, subtract consecutive periods yourself. Balance-sheet items are point-in-time (not cumulative), as expected.
- **Cash-flow line-item signs are normalized.** SEC filers are inconsistent: some report `capex`/`dividends_paid`/`share_repurchases`/`debt_repayment` as positive magnitudes, some as negative. These four are always cash outflows, so `findata` normalizes them to negative. The net subtotals (`operating_cf`, `investing_cf`, `financing_cf`) keep their as-reported directional signs. `free_cash_flow` is derived as `operating_cf + capex` (with `capex` normalized negative), which equals `operating_cf − |capex|` regardless of the filer's convention.
- **`period_end` duplicate facts.** companyfacts often contains the original 10-K fact *and* a comparative-column restatement filed in a later 10-K (same `end`, same value, the later one tagged with a `frame` like `CY2024`). `findata` dedupes periods by `period_end` and prefers the earliest-filed `10-K` fact, so each column points back to the original filing, not a later comparative.
- **Concept coverage varies by filer.** A field shows `-`/`null` if the company reports that line item under a concept not in the candidate list (e.g. Apple reports dividends under `PaymentsOfDividends` and repurchases under `PaymentsForRepurchaseOfCommonStock`). The candidate lists cover the common concepts; esoteric filers may leave some fields null.
- **`previous_close` for `price`** is the close of the prior trading day (second-to-last daily bar of a 5-day window), so `change` is day-over-day. `chartPreviousClose` in Yahoo's meta is the close *before the range start* (~5 days ago), not yesterday — that's why it isn't used.
- **Yahoo rate limits.** Yahoo may return `429` / a non-JSON page under heavy use; `findata` surfaces this as a `Yahoo Finance error … non-JSON response (possibly rate-limited)`. Back off and retry. Intraday intervals are limited by Yahoo to recent windows (e.g. 1-minute bars only for the last ~7 days).
- **SEC rate limit / User-Agent.** SEC asks for <10 req/s and a descriptive `User-Agent`; the browser supplies one automatically. Normal use is 1–2 requests per call (ticker map is cached), well within limits.
- **Ticker map is cached** on `globalThis.__secTickerMap` for the server process lifetime, so recently listed tickers won't appear until `browser-harness-js --restart`.
- **Share-class tickers use a hyphen.** SEC EDGAR's `company_tickers.json` and Yahoo's chart endpoint both key share-class symbols with `-` (`BRK-B`, `BF-B`), not `.`. `findata` uppercases the ticker and normalizes `.`→`-`, so `BRK.B`, `brk.b`, and `BRK-B` all resolve. Without this, `BRK.B` failed with `Ticker not found in SEC EDGAR`.
- **Two capture paths.** `Page.frameNavigated` + same-origin `fetch` for prices and the ticker map (skips the JSON-viewer render — fast for small bodies); readiness polling for the multi-MB companyfacts, where the viewer's pre-parse makes the projection nearly free (a cold fetch+parse is slower there). See *How it works*.
- **No lifecycle events for JSON pages.** Chrome emits neither `Page.loadEventFired` nor `networkIdle` for `application/json` navigations. The fetch path keys off `Page.frameNavigated` (which does fire on commit); the poll path keys off `document.body.innerText` parseability, bailing fast on a non-JSON `content-type` instead of waiting out the timeout.
- **No `jq` dependency** — JSON is parsed in-page and projected to the exact output shape; pretty-printing is done in JS. Date→unix conversion uses `node` (already required by `browser-harness-js`).
