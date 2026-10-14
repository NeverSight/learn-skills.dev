---
name: institutional-13f-tracker
description: "13F institutional ownership tracker: quarterly hedge fund and mutual fund holdings from SEC 13F filings, by ticker or by manager, with top institutional holders per stock, quarter-over-quarter buying and selling deltas, and activist investor positions across thousands of managers. Use for 13F filings, 13F holdings changes, hedge fund holdings, institutional ownership by ticker, who owns this stock, activist fund positions, and superinvestor portfolios. Read-only. No trading, no purchases, no write operations, no wallet access."
license: MIT
metadata:
  homepage: https://sentisense.ai
  requires_env: SENTISENSE_API_KEY
---
# Institutional 13F Tracker (SentiSense)

See who owns a stock and how the big money is repositioning. This skill reads institutional ownership from SEC 13F filings through the read-only SentiSense API: the top institutional holders for any ticker, aggregate buying and selling per stock, activist positions, and a full portfolio for any manager (from Berkshire Hathaway to the largest index funds), with quarter-over-quarter change types (new, increased, decreased, sold out) across thousands of filers.

Read-only educational data interface. Output is informational context, never a personalized buy or sell recommendation.

## When to Use

Reach for this skill when the question is about institutional ownership or 13F positioning:

- "Who owns $NVDA?" or "top institutional holders of $TSLA"
- "What did Berkshire Hathaway buy and sell last quarter?" (a manager's whole portfolio)
- "Is institutional money accumulating or distributing $AAPL?" (aggregate flows)
- "Which activist funds took new positions this quarter?"
- "How did 13F ownership of $COIN change quarter over quarter?"

This skill pairs naturally with `politicians-stock-tracker` and `insider-trading-tracker`: line up 13F accumulation against a congressional purchase or an insider cluster buy on the same ticker. Convergence across sources is the high-conviction read.

Do not use it for order entry, portfolio management, or personalized advice. It has no write, trading, or wallet surface; every endpoint is a GET.

## What this data actually is (read before interpreting)

- **13F is quarterly and lagged.** Institutions file 13F-HR within 45 days after each quarter end, so the freshest complete data is always the prior quarter. Never present it as real-time positioning.
- **Always resolve the quarter first.** The quarter-scoped feeds (`/flows`, `/activist`, `/bonds`, `/options`) need a `reportDate`. Four endpoints do not: `/quarters` is the resolver itself, `/holders/{ticker}` resolves the latest settled quarter for the ticker when you omit it and echoes the one it used, `/institutions` takes an optional `quarter` (the `value` form, `2026Q2`, not a `reportDate`), and `/institution/{slugOrCik}` takes neither and answers on its own latest quarter. During the 45-day filing window after a quarter ends, the newest entry is `pending: true` and holds only early filers; use the first quarter with `pending: false` for complete data. **Filter on the flag, never on position.** Once the filing window closes, the pending entry is gone and the newest quarter in the array is already complete, so code that skips index 0 on the assumption that the first row is always pending will quote a quarter that is three months staler than what you were served. Checked live on 2026-08-31: the array led with Q2 2026 at `pending: false` and contained no pending entry at all.
- **Filer categories:** `INDEX_FUND`, `HEDGE_FUND`, `ACTIVIST`, `PENSION`, `BANK`, `INSURANCE`, `MUTUAL_FUND`, `SOVEREIGN_WEALTH`, `ENDOWMENT`, `CONGLOMERATE`, `OTHER`.
- **Parent/subsidiary rollups.** Large managers file under many CIKs (e.g. Vanguard). A filer profile carries `multiCikRollup` / `childCikCount` / `childCiks` so sub-manager holdings roll up into one portfolio. Report the rollup, not double-counted child rows.
- **Report values as given.** The dollar field is **`valueUsd`** on both sides of the join: on a holder row under `/holders/{ticker}` and on a holding row inside a manager's portfolio. There is no bare `value` field on either. It arrives already denominated in US dollars, so quote it as the reported 13F value and do not re-scale or invent a unit. (`/bonds` names its own total `totalValue` and `/institutional/options` splits into `callValue` / `putValue`; those are the only other dollar keys in this family.)

## Prerequisites

- A free `SENTISENSE_API_KEY`. Get one at https://app.sentisense.ai/get-api-key. Required on every call; anonymous requests return `401 api_key_required`.
- Any HTTP client. Plain `curl` works, or Python 3.8+ using only the standard library. On macOS python.org installs can raise `CERTIFICATE_VERIFY_FAILED`: run `Install Certificates.command`, use the system `/usr/bin/python3`, or use `curl`.
- Network access to `https://app.sentisense.ai`.
- Read-only scope. Every endpoint here is a GET.

| Tier | Quota | Rate | 13F data |
|------|-------|------|----------|
| Free | 1,000 requests/month | 30 requests/min | preview slice (top N per endpoint) |
| PRO ($15/mo) | Unlimited | 300 requests/min | full holder lists and full portfolios |

## Permissions

- Network: HTTPS to app.sentisense.ai only.
- Credentials: SENTISENSE_API_KEY from the environment.
- Shell: none required.
- Files: none.

## How to Run

Issue HTTP GET requests to `https://app.sentisense.ai`, authenticated with the `X-SentiSense-API-Key` header. Keep the key in the shell environment; never place it in a query string or in user-facing output.

**Step 1, always: resolve the quarter.** `/quarters` is a bare array (no envelope). Every other institutional endpoint returns the wrapped envelope `{ isPreview, previewReason, data }`, so unwrap `.data` first. Unwrapping is not the same as iterating: on `/holders/{ticker}`, `/institution/{slugOrCik}`, `/institutions` and `/flows` the unwrapped `data` is an **object**, and the rows sit one level further in (`data.holders`, `data.holdings`, `data.institutions`, and `data.inflows` / `data.outflows` respectively). Check for a list before you loop. A `429` returns a `Retry-After` header; back off rather than serving a stale value.

**Identify your client.** Send a `User-Agent` naming your agent runtime and this skill, for
example `OpenClaw/1.4 (institutional-13f-tracker)` or `ClaudeCode/2.1 (institutional-13f-tracker)`. Substitute your own runtime and
version if neither matches. You can also volunteer what your agent is called by adding an
`agent/<your-agent-name>` token inside the same parentheses, as in
`OpenClaw/1.4 (institutional-13f-tracker; agent/research-desk)`. All of it is optional, and it is what tells
us this skill has real integrations behind it, so it gets prioritized and you get notice before it
changes.

```bash
# 1) get valid reporting quarters, pick the first with pending=false
curl -s -H "X-SentiSense-API-Key: $SENTISENSE_API_KEY" \
  "https://app.sentisense.ai/api/v1/institutional/quarters"
# -> [{ "value": ..., "label": "Q4 2025", "reportDate": "2025-12-31", "pending": false }, ...]
```

## Endpoints

- **`GET /api/v1/institutional/quarters`** : available 13F reporting quarters. **Public**, bare array of `{ value, label, reportDate, pending }`, newest first. Call this first; use the first `pending: false` `reportDate` everywhere below.
- **`GET /api/v1/institutional/holders/{ticker}`** : institutional holders for a stock. `reportDate` is **optional here**: omit it and the endpoint resolves the latest quarter that actually has holders for this ticker, preferring a settled quarter over a still-filing one, and tells you which one it used in `data.reportDate`. Pass `?reportDate=` from `/quarters` when you want a specific quarter or are comparing several tickers on one date. The holder list is nested at **`data.holders`** (not `data` directly). Each holder carries `filerName`, `filerCik`, `filerCategory`, `entitySlug`, `cikCount`, `shares`, `sharesChange`, `sharesChangePct`, **`valueUsd`** (the dollar field, there is no bare `value`), and `changeType` (`NEW` / `INCREASED` / `DECREASED` / `SOLD_OUT` / `UNCHANGED`). `data` always carries `holderCount` (full-quarter count). **Paging (recommended):** pass `limit` (1-1000), `offset`, `sortBy`, `sortDir`. A mega-cap can have 5,000+ holders, and `notableChanges` (holders with a 10%+ change on 10k+ shares) plus `returnedCount` are returned **only when `limit` is passed**. Free: top 5, and free previews omit `returnedCount`, `offset`, and `notableChanges` even when `limit` is passed (`holderCount` stays the full-quarter count).
- **`GET /api/v1/institutional/flows?reportDate=`** : aggregate institutional buying/selling per ticker. **`data` is an object, not a list**, so iterating `.data` gets you nothing: the two ranked ticker arrays are at **`data.inflows`** and **`data.outflows`**, alongside `data.reportDate`, `data.filerCount`, `data.baselineFilerCount` and `data.isPending`. Each row carries `ticker`, `companyName`, `dollarFlowUsd`, `netSharesChange`, `totalSharesBought` / `totalSharesSold`, the position counts (`newPositions`, `increasedPositions`, `decreasedPositions`, `soldOutPositions`), `avgClosePrice`, and a per-category net-change breakdown (`hedgeFundNetChange`, `indexFundNetChange`, `activistNetChange`, and one per remaining filer category). Free: top 5.
- **`GET /api/v1/institutional/activist?reportDate=`** : activist-filer positions for the quarter (NEW or INCREASED stakes). Free: top 3; PRO: full.
- **`GET /api/v1/institutional/bonds?reportDate=`** : convertible bond flows grouped by base ticker, the credit-side leg of the same 13F filings. Free: top 3; PRO: full.
- **`GET /api/v1/institutional/options?reportDate=`** : institutional options positions with the call/put breakdown, as disclosed on 13F. Quarterly and end-of-quarter, not live flow. Free: top 3; PRO: full.
- **`GET /api/v1/institutional/institutions`** : the filterable universe of tracked filers (use it to find a manager's slug/CIK for the endpoint below). Query `category`, `minAumUsd`, `sort`, `quarter`. Full list on every tier, and quota-exempt.
- **`GET /api/v1/institutional/institution/{slugOrCik}`** : a single manager's profile, summary stats, and current-quarter equity holdings. Resolve by URL slug (`Berkshire-Hathaway`) or numeric CIK (`1067983`). Free: profile + top 10 holdings; PRO: full holdings. Holdings include `ticker, companyName, shares, valueUsd, changeType, sharesChange, sharesChangePct, portfolioWeight`, plus `multiCikRollup` / `childCiks` for parent/subsidiary rollups. Returns 404 for an unknown slug or CIK.

## Workflows

**1. Who owns this stock?**

```bash
Q=2026-06-30  # first pending:false reportDate from /quarters
curl -s -H "X-SentiSense-API-Key: $SENTISENSE_API_KEY" \
  "https://app.sentisense.ai/api/v1/institutional/holders/NVDA?reportDate=$Q&limit=25"
```
Read `data.holders` and lead with the largest holders and their `NEW` / `INCREASED` / `SOLD_OUT` change types; on PRO, `limit` also returns `notableChanges` (a `count` of holders that changed 10% or more on 10k+ shares, plus the `top` five of them by dollar value), while a free preview omits it, so on free read the changes off the five holders shown and never report "no notable changes".

**2. A manager's whole portfolio (what did they buy and sell?)**

```bash
curl -s -H "X-SentiSense-API-Key: $SENTISENSE_API_KEY" \
  "https://app.sentisense.ai/api/v1/institutional/institution/Berkshire-Hathaway"
```
Summarize new positions, adds, trims, and exits by `changeType`, and the biggest holdings by `portfolioWeight`.

**3. Aggregate accumulation vs distribution**

```bash
Q=2026-06-30  # first pending:false reportDate from /quarters
curl -s -H "X-SentiSense-API-Key: $SENTISENSE_API_KEY" \
  "https://app.sentisense.ai/api/v1/institutional/flows?reportDate=$Q"
```

Read the accumulation side from `data.inflows` and the distribution side from `data.outflows`, each already ranked by the size of `dollarFlowUsd` (negative on the outflow side). A ticker appears on the side its net quarter landed on, never on both, so read the two lists as one board rather than netting them against each other.

**4. Activist watch**

```bash
Q=2026-06-30  # first pending:false reportDate from /quarters
curl -s -H "X-SentiSense-API-Key: $SENTISENSE_API_KEY" \
  "https://app.sentisense.ai/api/v1/institutional/activist?reportDate=$Q"
```

**5. Follow the convergence.** When institutional accumulation lines up with a congressional purchase (`politicians-stock-tracker`) or insider buying (`insider-trading-tracker`) on the same ticker, that agreement is the read worth surfacing. Cite each source.

## Answering well

- Always state the `reportDate` you are quoting and that 13F data is a quarterly snapshot filed up to 45 days after quarter end.
- Attribute holdings to the filer and category; roll parent/subsidiary CIKs into one manager rather than double-counting.
- Use `changeType` and `sharesChangePct` to describe direction; quote `valueUsd` as the reported 13F value without re-scaling.
- Report only what the API returns. Do not infer positions, prices, or intent that are not in the data, and do not frame any of it as advice.

## Going further

Free covers every workflow above at a preview depth (top holders, top-10 portfolio). **PRO ($15/mo)** lifts the monthly cap (no monthly limit, just a 300/min rate) and returns full holder lists and full manager portfolios, plus congressional, insider, options, and AI-insight data across the SentiSense API. Apply coupon `AGENTS` at checkout for a builder launch discount: https://app.sentisense.ai/pricing?coupon=AGENTS

**Install:** `npx skills add SentiSenseApp/skills` (add `-s institutional-13f-tracker` for just this skill).

---

*SentiSense is a read-only financial intelligence API. This data is for informational and educational purposes only, not investment advice.*
