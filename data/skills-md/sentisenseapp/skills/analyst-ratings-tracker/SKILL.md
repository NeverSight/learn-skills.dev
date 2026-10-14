---
name: analyst-ratings-tracker
description: "Track Wall Street analyst ratings and price targets: who covers a stock and where each firm stands, upgrades and downgrades by ticker and market-wide, one analyst's profile and call history, the Street versus crowd comparison against SentiSense sentiment, and which firms moved after an earnings print. Use for analyst ratings API, price target consensus, analyst upgrades today, who covers a stock, analyst coverage, rating changes after earnings, analyst price targets by firm. Read-only. No trading, no purchases, no write operations, no wallet access."
license: MIT
metadata:
  homepage: https://sentisense.ai
  requires_env: SENTISENSE_API_KEY
---
# Analyst Ratings Tracker (SentiSense)

Track what Wall Street research desks say about a stock and how that compares with what the market feels. This skill reads analyst coverage, price targets, rating changes and per-analyst call history for about a thousand US names through the read-only SentiSense API, and pairs it with the SentiSense Score and Sentiment for the same ticker: who covers a stock and where each firm stands today, what changed this week on one name or across the market, one analyst's profile and record of calls, the Street versus crowd comparison, and which firms moved in the sessions after an earnings print.

Read-only educational data interface. Output is informational context, never a personalized buy or sell recommendation.

## When to Use

Reach for this skill when the question is about analysts:

- "Who covers $NVDA and what do they say?" or "what is the price target on this stock?"
- "Any upgrades or downgrades today?" (market-wide rating changes, reiterations filtered out)
- "What has this analyst said before?" (profile and call history by name or slug)
- "Do analysts and the market agree on this name?" (Street versus crowd)
- "Which firms moved after the earnings print?" (post-earnings analyst reaction)
- As one leg of a convergence check with `insider-trading-tracker`, `institutional-13f-tracker` and `stock-sentiment` on the same ticker.

Do not use it for order entry, portfolio management, or personalized advice. It has no write, trading, or wallet surface; every endpoint is a GET.

## What this data actually is (read before interpreting)

- **Coverage is by firm; ratings are the firm's, not the named analyst's.** A coverage row is one research desk with its latest price-target note and its latest rating action. The `analysts[]` on the row are the people the publisher named on that desk's notes. More than half of notes arrive with no byline; the response says so in `attributionNote` and the counts are `attributedNoteCount` and `unattributedNoteCount`.
- **Ratings and price targets are two feeds, and they do not move together.** A firm can rate a stock for months without publishing a target, or the reverse. `firmCount` is every firm in the window; `ratingOnlyFirmCount` is how many of them are there on a rating action alone. A row with `firmRating` set and `noteCount` zero is an ordinary row.
- **`ratingBuckets` is the whole book, counted server-side.** `{ buy, hold, sell, unrated, total }` groups every covering firm by the tier of its current rating (Buy, Overweight, Outperform and their kin are Buy; Hold, Neutral, Equal-Weight, Market Perform are Hold), counted before the free-tier preview truncates the firm list, so a free key reads the same counts as a paid key. `unrated` is target-only desks. The four sum to `total`.
- **Consensus counts are a different population.** `/consensus` carries the vendor's survey (`strongBuy` through `strongSell`, PRO only, and they arrive as `0` on a free key, not null). Never mix them with `ratingBuckets` in one bar; pick one source per number.
- **Consensus counts are a survey panel, not a tally of the actions feed.** The `strongBuy` to `strongSell` counts are broker recommendations currently in effect, revised in batches through the month as brokers submit, most of which never become a published note. They can move on any sweep with no matching row on `/actions` or `/activity`. Never explain a count move by hunting for an action, and never say "no analyst moved" because the counts are flat. The actions feed is the event record (each row has the note's `actionDate`); the counts are a snapshot of the panel when the sweep ran. A ticker whose panel fetch returned nothing keeps the stored counts, which may be initial zeros when no panel has ever been observed. History consumers must use `countsObserved` to distinguish an observed panel, including an all-zero panel, from carried counts; `countsObserved: false` is not evidence of dropped coverage.
- **Grades come back in one spelling per rating.** `Equal-Weight`, `In-Line`, `Market Perform`, never their variants. A firm's own scale word is kept (`Outperform` stays `Outperform`), so group by tier, not by string equality, when you want "how many say Buy".
- **An initiation never carries a prior grade.** `actionType: INITIATE` always has `fromGrade: null`. Render it as "initiated at Buy", never as a change. When both grades are present, `actionType` agrees with the pair. An `UPGRADE` or `DOWNGRADE` can still arrive with `fromGrade: null` when the publisher did not report the prior grade: render it as "downgraded to Underweight, prior grade not reported" and never invent the prior.
- **Most of the market-wide feed is reiterations.** Roughly seven rows in ten on `/activity` are `REITERATE`; ask for `actionTypes=UPGRADE,DOWNGRADE,INITIATE` unless you want them.
- **The SentiSense Score is a nowcast.** It reads today's news and social tone, weighted by how actively the stock is discussed, centered on zero with strong readings beyond +/-23. It describes today and says nothing about tomorrow. `sentiment` is polarity from -1 to +1.
- **Freshness:** analyst data refreshes in one sweep over the whole universe about once a day, and the hour it lands drifts (measured completions from 8:49am to 5:33pm ET). Read `updatedAt` on consensus rather than assuming a schedule. A rating change can be up to a day old before it appears.

## Prerequisites

- A free `SENTISENSE_API_KEY`. Get one at https://app.sentisense.ai/get-api-key. Send it on every REST call as the `X-SentiSense-API-Key` header (`curl -H "X-SentiSense-API-Key: $SENTISENSE_API_KEY" ...`). A call without it: a request without a valid key gets at most a shaped crawler-facing preview slice, never the dataset, and that fallback is not a contract you can build on.
- Any HTTP client. Plain `curl` works, or Python 3.8+ using only the standard library.
- Network access to `https://app.sentisense.ai`.
- Read-only scope. Every endpoint here is a GET. Nothing this skill does can place a trade, move money, or modify account state.

| Tier | Quota | Rate | Analyst data |
|------|-------|------|--------------|
| Free | 1,000 requests/month | 30 requests/min | coverage: 5 firms plus whole-book counts; actions: 3 rows; activity: first 50 rows; calls: first 25; profile: 5 tickers; earnings calendar: the Monday-to-Sunday week containing `from` |
| PRO ($15/mo) | Unlimited | 300 requests/min | full books and full history |

The free tier exercises every workflow below; preview-gated endpoints return a truncated but real slice on a free key, and the response-level counts are never truncated.

**A preview is a slice, not the window.** When `isPreview` is true and `totalCount` is larger than the rows returned, the rows are the newest (or most recently active) few of `totalCount`. Label them that way ("newest 3 of 27 rating actions, free preview"), never count them as the window, and never infer absence from them: three rows with no downgrade is not "no firm downgraded". The same holds for the free earnings calendar: an empty `data.earnings` with `totalCount` above zero means the event sits outside the one week returned, not that nothing is scheduled.

## Permissions

- Network: HTTPS to app.sentisense.ai only.
- Credentials: SENTISENSE_API_KEY from the environment.
- Shell: none required.
- Files: none.

## How to Run

**Identify your client.** Send a `User-Agent` naming your agent runtime and this skill, for example `OpenClaw/1.4 (analyst-ratings-tracker)` or `ClaudeCode/2.1 (analyst-ratings-tracker)`. Substitute your own runtime and version if neither matches. You can also volunteer what your agent is called by adding an `agent/<your-agent-name>` token inside the same parentheses, as in `OpenClaw/1.4 (analyst-ratings-tracker; agent/research-desk)`. All of it is optional, and it is what tells us this skill has real integrations behind it, so it gets prioritized and you get notice before it changes.

The REST recipe in this file is the primary path. A maintained command-line client is available as the separate `sentisense-cli` skill for hosts that prefer one.

Coverage, people and the market-wide feed are plain REST. Every `/api/v1/analyst/...` endpoint returns the wrapped envelope `{ isPreview, previewReason, data }`; read `.data`, and when `isPreview` is true say so ("showing the free preview slice"). The two crowd-metric series under `/api/v2/metrics/...` are the exception: a bare JSON array of points with no envelope, so read them directly. A rate-limited call returns `429` with a `Retry-After` header; back off for the indicated seconds.

## Endpoints

- **`GET /api/v1/analyst/{ticker}/coverage`** : who covers the stock, by firm, most recently active first. Query `lookbackDays` (default 365, up to 1825). Response level, all under `data` alongside `ticker`, `windowDays` and `asOf`: `firmCount`, `ratingOnlyFirmCount`, `namedAnalystCount`, `noteCount`, `attributedNoteCount`, `unattributedNoteCount`, `attributionNote`, `ratingBuckets`. **The firm rows are nested at `data.coverage`, not at `data` directly**, so unwrapping the envelope is only half the read. Each row: `firm`, `analysts[]` (`slug`, `name`, `noteCount`, `latestPriceTarget`), `noteCount`, `latestNote` (`publishedDate`, `priceTarget`, `priceWhenPosted`, `newsPublisher`, `newsUrl`), `firmRating` (`rating`, `priorRating`, `actionType`, `date`). Free: 5 firms plus `totalCount`; PRO: all.
- **`GET /api/v1/analyst/{ticker}/consensus`** : the price-target band. `targetLow`, `targetMean`, `targetHigh`, `numberOfAnalysts`, `currentPrice`, `upsidePercent`, `consensusLabel`, `updatedAt` (UTC instant), `updatedAtEpoch`. PRO adds `targetMedian`, `recommendationMean` and the five survey counts.
- **`GET /api/v1/analyst/{ticker}/consensus/history`** : daily observations ordered by `snapshotDate` ascending. Query `from` and `to` as `YYYY-MM-DD` dates plus `limit` (default 90, capped at 366); omitted dates select the 90 days ending today. Response data: `{ ticker, from, to, count, history }`, with `totalCount` on the envelope. Free: the last 30 days ending at `to`, with `targetMedian`, `recommendationMean` and the five survey counts null; PRO: the requested window and all fields. `countsObserved: false` marks carried counts from a sweep where the panel did not return.
- **`GET /api/v1/analyst/{ticker}/called-it`** : recorded large moves with same-direction price-target revisions published beforehand. Query `limit` (default 10, capped at 50; below 1 returns `400 invalid_limit`). Response data: `{ ticker, count, moves }`, newest first by `moveEndDate`, with the pre-limit `totalCount` on the envelope. Free: newest move, up to 5 calls, move-level counts intact; PRO: requested moves and all calls. Each move carries its dates, `movePct`, `moveWindowSessions`, `lookbackDays`, `coveringFirms`, `revisedWithMove`, `revisedAgainstMove`, `leftUnchanged`, `insightId`, `generatedAt` (epoch seconds), and `calls`. Each call: `firm`, nullable `analystName`, `attribution` (`firm` or `analyst`), `priceTarget`, `priorPriceTarget`, `publishedOn`, `daysBeforeMove`. Known stocks with no qualifying move return `200` with empty `moves`; unknown symbols return `404 entity_not_found` with suggestions, and ETFs return `404 ticker_is_etf` with an analyst aggregate pointer.
- **`GET /api/v1/analyst/{ticker}/actions`** : rating actions for one stock, newest first. Query `lookbackDays` (default 90), counted back from today, so the window always ends today. Each row: `actionDate`, `firm`, `actionType` (`UPGRADE`, `DOWNGRADE`, `INITIATE`, `REITERATE`, `OTHER`), `fromGrade`, `toGrade`. Free: the newest 3 rows plus `totalCount`; PRO: the full window in one response.
- **`GET /api/v1/analyst/activity`** : market-wide rating actions, newest first. Query `lookbackDays` (default 30), `limit` (default 50, up to 500; above 500 is clamped), `offset`, `actionTypes` (comma-separated). Same row shape plus `ticker`. `totalCount` on the envelope is the size of the whole filtered window, so `offset + data.length < totalCount` means another page is waiting: one call is one page, not the window. Free: the first 50 rows of the window in full; a free request whose `limit` or `offset` reaches past row 50 comes back as a preview holding only the rows inside the first 50.
- **`GET /api/v1/analyst/people/{slug}`** : one analyst's profile: the firms they have published under with first and last note dates, and their coverage book across tickers. Free: 5 most recent tickers; PRO: full book. 404 for a slug we do not hold.
- **`GET /api/v1/analyst/people/{slug}/calls`** : their price-target notes, newest first. Query `limit` (default 25, up to 200), `offset`; `totalCount` in the response. Free: first 25 rows in full.
- **`GET /api/v1/analyst/{ticker}/estimates`** : forward EPS estimates and past surprises. Free: 1 estimate and 2 surprises.
- **`GET /api/v2/metrics/entity/{ticker}/metric/sentisense`** and **`.../metric/sentiment`** : the crowd side. `{entityId}` accepts a ticker directly. Time-ascending points with a flat `value`; the last point is today's reading. Counts toward the monthly quota like every other call.
- **`GET /api/v1/calendar/earnings?ticker={ticker}&from={date}`** : scheduled print dates and sessions (`before_open`, `after_close`). PRO gets the whole requested window; a free key gets only the Monday-to-Sunday week containing `from` (or the current week when `from` is omitted), with `totalCount` counting the whole window, so compare it with `data.earnings.length` before saying a date is missing.
- **`GET /api/v1/stocks/{ticker}/earnings/reactions`** : the last twelve announcements that already traded, newest first, each `{ reportDate, timing, priorClose, nextClose, movePct }`, returned directly with no envelope. Not tier-gated, so it is the way to find a past print on any key. `timing` is `AMC` (after the close, the reaction session is the next trading day), `BMO` (before the open, the reaction session is the report date) or `null` (session inferred).
- **`GET /api/v1/insights/stock/{ticker}`** : the stock's insights, including `analyst_reaction` once a print has one. Add `insightType=analyst_reaction` to ask for that type directly; a free key gets only the top 3 insights, so an unfiltered call can miss it.

## Workflows

**1. Who covers this stock, and where do they stand today**

Call `GET /api/v1/analyst/NVDA/coverage` (the whole-book counts are on `data` itself, the per-firm rows are the array at `data.coverage`), then `GET /api/v1/analyst/NVDA/consensus`. Lead with `ratingBuckets` as the rating line, with the percentages taken over the rated firms (`buy + hold + sell`) and the target-only desks named separately ("32 of 42 covering firms rate it: 97% Buy, 3% Hold, 0% Sell; 10 publish targets only"), then the consensus target against `currentPrice`, then the three most recently active firms by name with their latest target. Say how many firms are rating-only and how many notes carried no byline. On a free key the firm list is five rows and `totalCount` tells you the book size; the counts at the top are whole either way.

**2. Consensus drift**

Call `GET /api/v1/analyst/NVDA/consensus/history` to pull the default 90-day window. If `data.history` is empty, report no observations in the returned `data.from` to `data.to` window and stop before reading first or last rows. For an empty response where `isPreview` is true and `totalCount` is positive, say the free preview is empty but observations exist in the full requested window. For non-empty history, read the first and last rows of `data.history`; the stored history can start later than the requested `data.from`, so head the report with the first and last `snapshotDate` rather than the requested window, and report the first and last `targetMean`, then report the change in each count bucket from `strongBuy` through `strongSell`. List every `snapshotDate` whose `countsObserved` is false as carried; do not interpret a carried row as a coverage change.

```text
Consensus drift, {first.snapshotDate} to {last.snapshotDate} ({data.count} observations)
Mean target: ${first.targetMean} -> ${last.targetMean}
Counts: strong buy {first.strongBuy} -> {last.strongBuy}; buy {first.buy} -> {last.buy}; hold {first.hold} -> {last.hold}; sell {first.sell} -> {last.sell}; strong sell {first.strongSell} -> {last.strongSell}
Carried observations: {dates where countsObserved is false, or "none"}
```

On a free key the five counts are null and the returned window is 30 days. Report the available target drift, label the response as the free preview, and do not turn null counts into zeros.

**3. What changed**

For one name: `GET /api/v1/analyst/NVDA/actions?lookbackDays=30`. Market-wide: `GET /api/v1/analyst/activity?lookbackDays=7&actionTypes=UPGRADE,DOWNGRADE,INITIATE&limit=500`, then compare `totalCount` with the rows returned and page with `offset` until `offset + data.length` reaches `totalCount`; a busy week can hold more changes than a 100-row page, and the missing rows are the answer to "any downgrades?". Print "showing N of {totalCount}" whenever the two differ. On a free key ask for `limit=50`: the first 50 rows are served in full, and a larger `limit` returns the same 50 rows labelled as a preview. Report the firm, the direction and the grades; an `INITIATE` reads "initiated at Neutral", a change reads "Equal-Weight to Overweight". When one firm initiates a dozen names in one morning, that is one event, not twelve stories.

**4. One analyst's record**

Take a `slug` from `analysts[].slug` on the coverage row. Call `GET /api/v1/analyst/people/{slug}` and `GET /api/v1/analyst/people/{slug}/calls?limit=25`. Report the firms and dates, the coverage book, and the calls as published facts: the date, the target, the price when posted, the publisher. This is call history, not an accuracy score. Do not compute a hit rate or rank analysts; the API does not, on purpose.

**5. Street versus crowd**

Combine workflow 1 with the two metric calls (`.../metric/sentisense` and `.../metric/sentiment` for the same ticker; read the last point of each). Then one sentence, present tense, from a closed set: "Street and crowd lean the same way", "The Street is more positive than the crowd", "The crowd is more positive than the Street", or, with fewer than five rated firms, "Not enough coverage to compare". Compare the majority bucket with the Score's band (positive is bullish, negative bearish, strong beyond +/-23). State the Score as a label and a direction, and say it is a nowcast. On a day when the price runs through several published targets while tone stays flat, say exactly that; it is the most useful shape the comparison produces.

**6. Who moved after the print**

For "what did company actually report?", hand off to the `stock-earnings-analysis` skill when available. Pass the ticker, report date, and reaction window. Return quarter results, guidance, and filing changes, kept separate from the Street reaction. Hand off only when the user changes the question; do not automatically route back. If the sibling is unavailable, answer the supported part here using a connected tool or the inline REST workflow, state any remaining gap, and never require an install.

Find the print first. `GET /api/v1/stocks/NVDA/earnings/reactions` lists past announcements that already traded on every tier: take the newest `reportDate` and its `timing` (`AMC` rolls the reaction to the next trading day, `BMO` reacts the same day). For a print this week that has not traded yet, use `GET /api/v1/calendar/earnings?ticker=NVDA`, which covers the current Monday-to-Sunday week on every tier; on PRO a `from` date reaches any earlier window, and on a free key `from` returns only the week that contains it.

Then size the actions window from that date, not a fixed number: `/actions` counts `lookbackDays` back from today, so set it to the days from the report date to today plus two (`GET /api/v1/analyst/NVDA/actions?lookbackDays={days since report + 2}`). A fixed 14 reaches back only two weeks, so for an older print it returns later, unrelated rows and misses the reaction entirely. Add the coverage call for target notes. Keep the rows dated from the first reaction session through the end of your reaction window (for example the first five sessions), then count two things: rating changes from the `/actions` rows (which carry direction), and firms whose `latestNote.publishedDate` on the coverage call falls inside the window (which only says "published a target at $X"; the coverage row carries the latest target, not the prior one, so do not claim "raised" or "lowered" from it). Always print the denominator from `firmCount`: "6 of 31 covering firms moved; 25 have not published since." Firms, not people. On a free key `/actions` holds the newest 3 rows of `totalCount` and the coverage list the 5 most recently active firms, so neither supports a full count of who moved: say which slice you have, and prefer the written-up insight below. Where SentiSense has already written this up, `GET /api/v1/insights/stock/NVDA?insightType=analyst_reaction` carries an `analyst_reaction` insight whose `insightText` already states the moves and the denominator ("4 of 37 covering firms moved in the five sessions that followed ... 33 firms have not published since"); quote that sentence rather than re-deriving. The counts live in the text only: the insight object has `insightId`, `insightType`, `insightText`, `confidence`, `urgency`, `generatedAt` and no metadata field.

**7. The convergence check.** Analyst upgrades plus insider buying plus institutional accumulation on the same ticker, read against the crowd. Four calls, all plain REST: rating changes from `GET /api/v1/analyst/NVDA/actions?lookbackDays=90` (keep `UPGRADE`, `DOWNGRADE`, `INITIATE`); insider trades from `GET /api/v1/insider/trades/NVDA?lookbackDays=90` (envelope, rows under `data`; count purchases, code `P`, by distinct insider, and treat 3 or more as a cluster); institutional holders from `GET /api/v1/institutional/holders/NVDA?limit=25` (omit `reportDate` and it resolves this ticker's latest quarter with holders, reporting it back in `data.reportDate`; pass `&reportDate=YYYY-MM-DD` only when you need a specific quarter. The list is nested at `data.holders`, each holder has `changeType` of `NEW`, `INCREASED`, `DECREASED`, `SOLD_OUT` or `UNCHANGED`; count `NEW` plus `INCREASED` against `DECREASED` plus `SOLD_OUT` among the top holders); and the crowd from the two metric series in workflow 5. Cite each leg separately with its window (analyst 90 days, insider 90 days, 13F the latest quarter, crowd today), say which legs agree, and never sum them into one score; one leg alone is context, not a case. On a free key the actions and insider legs come back as preview slices (`isPreview` true, `totalCount` larger than the rows): label each as the newest N of `totalCount` and never read a slice with no purchases as "no insider buying". The `insider-trading-tracker`, `institutional-13f-tracker` and `stock-sentiment` skills each treat their leg in full when they are installed.

**8. Who called it**

Call `GET /api/v1/analyst/NVDA/called-it?limit=10`. For each move, report `moveStartDate` to
`moveEndDate`, `movePct`, and `moveWindowSessions`, then the counts: `revisedWithMove` of
`coveringFirms` firms revised in that direction, `revisedAgainstMove` revised against it, and
`leftUnchanged` left their targets unchanged. Under the move, list each call's firm, named
analyst when present, `priorPriceTarget` to `priceTarget`, `publishedOn`, and `daysBeforeMove`.
When `analystName` is null, attribute the published revision to the firm without inventing a name.

Label `isPreview: true` as the free preview: newest move only, up to 5 calls. The move-level
counts remain complete even when fewer calls are displayed; do not replace them with the
displayed list length. If `moves` is empty, say no qualifying move is stored for this stock and
stop. Describe the published revisions and the subsequent recorded move as dated facts only.

## Answering well

- **A wrong symbol looks like an uncovered stock.** `/coverage`, `/actions` and `/estimates` answer `200` with a well-formed all-zero payload for a symbol SentiSense does not hold (`TESLA`, `ZZZZ`), while `/consensus` for the same symbol answers `404`. Never conclude "no analyst covers this" from an empty book alone. When the user typed a company name, resolve it first with `GET /api/v1/kb/entities/search?q={name}&type=company&limit=5` (a bare array of `{name, urlSlug, type, ticker}`, best match first; take the first match with a non-null `ticker`). When a typed symbol returns an empty book, check `/consensus`: a `404` there means the symbol was wrong, not that coverage is empty.
- Ratings belong to firms. Write "Morgan Stanley upgraded to Overweight" and, only when the vendor named the person, "Morgan Stanley's Michael Cyprys". Never invent a name for an unattributed note and never write "unknown analyst".
- One population per number: `ratingBuckets` for "how many say Buy", `numberOfAnalysts` and `targetMean` for the target band. Do not average the two.
- Quote the target's date and `priceWhenPosted` next to the target; a July target on a stock that has run 30% since is a fact about July.
- Print the denominator on every count: "8 of 20 published targets are below the price" beats "most targets are below the price".
- The Score describes today. No verb about the future, no "buy signal", no "upside ahead".
- Report only what the API returns. Do not infer motives, and do not frame any of it as advice. This is public research activity presented for education.

## Going further

Free covers every workflow above at a preview depth, and the whole-book counts are never truncated. **PRO ($15/mo)** lifts the monthly cap (no monthly limit, just a 300/min rate) and returns full coverage books, full action history, full call histories and the consensus survey counts, plus institutional flows, insider detail and AI insights across the SentiSense API. Apply coupon `AGENTS` at checkout for a builder launch discount: https://app.sentisense.ai/pricing?coupon=AGENTS

For the full REST reference on every endpoint this skill touches, install the `sentisense` skill; for the complete CLI command set, install `sentisense-cli`.

**Install:** `npx skills add SentiSenseApp/skills` (add `-s analyst-ratings-tracker` for just this skill).

---

*SentiSense is a read-only financial intelligence API. This data is for informational and educational purposes only, not investment advice.*
