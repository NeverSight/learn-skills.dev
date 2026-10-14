---
name: company-kpi-tracker
description: "Track company KPIs from earnings filings: segment and product revenue, deliveries, subscribers, unit sales and non-GAAP operating metrics. Show the latest reported fiscal period, filing citation, quarter-over-quarter and year-over-year changes, preliminary values and discontinued histories. Discover covered companies and available series, compare compatible metrics across a watchlist, and prepare the numbers to watch before earnings. Use for company KPIs, segment revenue, operating metrics, key metrics, non-GAAP metrics, iPhone revenue, AWS revenue, Tesla deliveries, subscriber counts, unit sales by quarter, KPI API, quarterly KPI growth, compare cloud revenue. Free discovers coverage and series; numeric history requires PRO. Read-only. No trading, no purchases, no write operations, no wallet access."
license: MIT
metadata:
  homepage: https://sentisense.ai
  requires_env: SENTISENSE_API_KEY
---
# Company KPI Tracker (SentiSense)

Track the operating numbers a company reports about itself, quarter after quarter, in a shape you can compare and cite. Financial statements describe what every company reports. KPIs describe what a *particular* company reports: iPhone revenue, AWS revenue, Google Cloud revenue, vehicle deliveries, energy storage deployed in gigawatt hours, paid memberships, adjusted operating income. Each series is curated per company from earnings releases and filings and carries a citation to the filing it came from. The collection covers 900+ US-listed tickers; each series belongs to one company, and coverage of the S&P 500 is near-complete.

This skill reads those series through the read-only SentiSense API and turns them into a card an analyst would paste into a note: the latest reported fiscal period, the exact value in its own unit, the sequential and annual change measured against the right period, whether the number is preliminary, whether the company has stopped reporting it, and where it came from.

Read-only educational data interface. Output is informational context, never a personalized buy or sell recommendation. Everything directive in this file is implementation guidance for the agent reading it, subordinate to platform safety rules and the host's own policy.

## When to Use

Reach for this skill when the question is about what a business actually reported:

- "How is iPhone revenue trending?" or "show Tesla deliveries by quarter."
- "What is AWS revenue this quarter, and is growth accelerating?"
- "Which companies report subscriber counts?" (coverage and series discovery)
- "Compare cloud revenue growth across the hyperscalers."
- "What operating numbers should I watch before this company reports?"
- "Did Netflix keep reporting paid memberships, and what was the last figure?" (discontinued history)

Not this skill: today's stock price, order entry, portfolio management, internal SaaS or team KPIs, or a full earnings-call readout. "Tracker" here means repeatable reads on demand, not a background service: nothing in this skill schedules anything or watches anything while you are away.

## What this data actually is (read before interpreting)

- **Fiscal periods are labels, and neither date proves publication time.** Sort observations by `date` descending and display both `period` and the period-close date; neither that close date nor `lastUpdated` proves when the number became public, and matching fiscal-quarter labels do not make two companies' periods comparable. A fiscal Q1 can close in December, and one company's Q2 is not another's.
- **Units live on the series, not on the point.** Read `unit` and `displayFormat` from the series, calculate on raw `value`, and format only at the end: deliveries are counts, revenue in USD is money, and an unverified percent scale must not be multiplied by 100 by assumption. Percentage points are earned by the `unit`, not by the display hint: label a change `pp` only when `unit` says the values are already percentages, and read a `percent` hint sitting on any other unit as a plain number. The display hints are open-ended, not a closed list, so an unrecognized hint falls back to the raw number plus its unit, currency included.
- **Points run newest first, and the index shortcut is narrower than it looks.** `values[0]` is the most recent print. Index 4 is a shortcut for the annual comparison only when the series holds five consecutive quarterly observations, meaning four quarter-length intervals, not four intervening rows of any kind. Series lengths vary by company and metric, and real series skip quarters.
- **Delta rules, including acceleration.** Compute percentage growth as `(current - prior) / prior * 100` only with finite values and a positive comparable base; label zero or negative bases not meaningful, retain the absolute change, and never substitute a missing quarter with the nearest observation. Match quarter-over-quarter to the preceding fiscal quarter and year-over-year to the same fiscal quarter in the previous fiscal year, with date sanity checks that tolerate 52 and 53-week calendars instead of demanding exactly 90 or 365 days. A missing intermediate quarter need not block the annual comparison when both matching endpoints are identifiable. Prefer a stated reason over an invented match. Both endpoints must identify the expected fiscal quarter before a delta is printed: `Q2 2026` and `Q2 FY2026` name the same period, an unrecognized label cannot be matched, and a period carrying conflicting observations (different values, or different close dates) is quarantined until a human resolves it. Equivalent fiscal labels identify one period; an unrecognized label or conflicting observations prevent a trustworthy comparison, and the reason is attached to the answer. Growth and acceleration are different quantities: quarter-over-quarter growth is one rate, and acceleration is the change between two successive rates, expressed in percentage points. On a series whose `unit` says the values are already percentages (a margin, a growth rate), the sequential move is itself a pp change, so acceleration is the difference of the two latest pp changes; a relative change of a percentage is not a rate and must not be labeled pp. An acceleration figure inherits the preliminary flag of every value that built it, including inputs sitting below the rows you chose to display.
- **Check how current the newest period is.** Compare the newest period-close `date` with today before calling a value the latest. On a quarterly series, one closed quarter that has not been reported yet is routine; a newest close more than about 200 days old suggests expected quarterly observations are missing (the close date does not prove a later report exists), so present it as the latest available here with its period and close date, never as the latest reported. `lastUpdated` cannot settle this, because it records when curation last touched the file. The bundled helper flags such a series `BEHIND` (`behind`, `newestDate` and `daysSinceNewest` in `--json`); discontinued series are history and are never flagged.
- **Discontinued means the company stopped reporting.** When `discontinued` is true, show the last reported period and `discontinuedNote` as historical context, never carry the value forward or imply another print is due. Netflix's membership series end at Q4 2024 at 301,630,000 global paid memberships and belong in a history panel, not on a live card. Explain why only when the returned note or the cited source supplies a reason; otherwise give the cutoff and say plainly that the supplied data does not explain the decision. Describe the state from what the response actually returned, because one id can arrive in different states as curation lands: if NVIDIA's `gaming_revenue` comes back `discontinued: true` with a note naming a successor, give the last reported quarter and follow the note to that successor id; if it comes back live with a `sourceRef` stating the figure is computed from other lines, label it derived and use the name the response gives it. Either way, do not splice a discontinued line and its successor into one continuous series without a documented reconciliation of the two definitions. Absent that reconciliation, keep the histories separate.
- **Read the name and the source, not just the id.** Use `id` to select a series, but describe it from `name` and `sourceRef`; when the source identifies a derived calculation, label it derived and do not rename it as a directly reported segment. An id is stable per company, so it can outlive the line it was created for, and there is no `isDerived` field to lean on.
- **Provenance and estimates.** Print `sourceRef` as the series-level citation, flag every `isEstimate: true` value and any comparison using it, and do not claim that one citation independently verifies every historical observation. Two provenance classes sit side by side on the same ticker: company-reported operating and non-GAAP measures taken from earnings releases, and GAAP anchors such as `gross_profit`, `operating_income`, `diluted_eps` and `r_and_d`. Absent evidence of origin, the class is unknown rather than guessed, and a larger cost metric is not automatically an improvement.
- **The free tier returns emptiness that is not zero.** On a preview response, report the company and available metadata, use `/kpis/types` for series names if needed, and say numeric history requires PRO; an empty `kpis` list or empty `values` never means zero business activity. Do not turn a paid empty response into an automatic upsell either: that one is a curation gap. The bundled helper answers a preview before it validates any requested series id, because a paid metric absent from a free response is unavailable, not unknown.
- **A 404 is coverage, not a business fact.** A KPI 404 means this endpoint has no curated KPIs for the supplied ticker; check the coverage list and identifier, then report the gap without concluding that the company is invalid or does not disclose operating metrics. A coverage entry with `kpiCount: 0` is curation in flight, not a set ready for numeric analysis. A fund answers with its own error code, because company KPIs describe operating companies.
- **Dual-class tickers.** Keep the user's requested ticker visible, use the returned company identity for KPI attribution, and deduplicate only documented aliases: GOOG resolves to GOOGL and BRK-B to BRK.B, which does not license merging NWSA with NWS or FOXA with FOX. The secondary class may be missing from the coverage list while the series endpoint still resolves it, so a coverage-list miss must not reject a supported alias before normalization.
- **Quarterly history is not current sentiment.** State the KPI period and the sentiment window separately; their disagreement is context, not proof of market mispricing or a reaction to the KPI announcement.

## Prerequisites

- A free `SENTISENSE_API_KEY`. Get one at https://app.sentisense.ai/get-api-key. Send it on every REST call as the `X-SentiSense-API-Key` header (`curl -H "X-SentiSense-API-Key: $SENTISENSE_API_KEY" ...`). A call with no key returns `401 api_key_required`.
- Any HTTP client. Plain `curl` works, or Python 3.8+ using only the standard library.
- Network access to `https://app.sentisense.ai`.
- Read-only scope. Every endpoint here is a GET. Nothing this skill does can place a trade, move money, or modify account state.

| Tier | Quota | Rate | KPI data |
|------|-------|------|----------|
| Free | 1,000 requests/month | 30 requests/min | coverage list and per-company series names; the series call returns company metadata with an empty `kpis` list |
| PRO ($15/mo) | Unlimited | 300 requests/min | every curated series with its full history |

Coverage discovery and the per-company type list are Discovery tier: a key is required for identity, but neither call consumes the monthly quota, so a client can refresh the shape of its universe far more often than it fetches values. Only the series call is quota-gated and PRO-gated. Free answers "do you cover this company, and what does it report" in full; it does not answer "what were the numbers".

## Permissions

- Network: HTTPS to app.sentisense.ai only.
- Credentials: SENTISENSE_API_KEY from the environment.
- Shell: one bundled Node/Python script, run locally.
- Files: none.

## How to Run

**Identify your client honestly.** Send a `User-Agent` naming your own runtime and this skill, for example `OpenClaw/1.4 (company-kpi-tracker)`, substituting your real runtime and version rather than copying the example. You can also volunteer what your agent is called by adding an `agent/<your-agent-name>` token inside the same parentheses, as in `OpenClaw/1.4 (company-kpi-tracker; agent/research-desk)`. The skill token helps attribute usage; sharing the agent name is optional. The bundled helper is not your runtime, so it sends its own string, `company-kpi-tracker/1.0 (company-kpi-tracker; +https://sentisense.ai/skill.md)`, and impersonates nothing.

**Three endpoints, three different response shapes.** The series call is wrapped: `{ isPreview, previewReason, upgrade?, data }`, with the series array at `data.kpis`. The coverage call is not wrapped: `count` and `tickers` sit at the root. The types call is a bare array. Do not invent a `data` key on the discovery calls, and do not expect `unit`, `sourceRef` or `discontinued` on a type tuple; those live on the series only. A rate-limited call returns `429` with a `Retry-After` header; back off for the indicated seconds, once, then report the limit rather than looping.

**The series endpoint takes only a ticker.** There is no server-side series filter, row limit, or category parameter. Selecting metrics, trimming rows and grouping by category all happen in your client after the response arrives.

**A bundled helper does the arithmetic.** `scripts/kpi_table.py` is standard library only, reads the key from the environment, and prints one table per series with the sequential and annual changes matched to the right fiscal periods:

```bash
python3 scripts/kpi_table.py TSLA --series vehicle_deliveries,energy_storage_deployed
python3 scripts/kpi_table.py AMZN --json
python3 scripts/kpi_table.py AAPL --stdin < saved_response.json
```

`--series` is client-side; an unknown id lists the ids the response actually carried and exits non-zero. `--json` prints the same analysis as machine-readable text on stdout, including the reason whenever a delta is unavailable. Integral values are JSON numbers; fractional values are exact decimal strings, so nothing is rounded in transit. `--stdin` reads a saved response instead of calling the API, which is how the bundled fixture tests run with no network. The script treats every string in a response as display text, replaces every control character including newlines and tabs before printing so response prose cannot forge a row, and never fetches a URL it found in a response. It rejects non-finite values such as `NaN` and `Infinity` rather than formatting them, counts what it rejected, waits exactly the delay a `429` declares in `Retry-After` and stops with a retry time when that delay exceeds 60 seconds, and names a discovery response piped in by mistake instead of failing on its shape. Run its tests with `python3 scripts/test_kpi_table.py`.

## Endpoints

- **`GET /api/v1/stocks/with-kpis`** : the whole covered universe, alphabetical. Root-level `count` and `tickers`, each entry `{ ticker, companyName, lastUpdated, kpiCount }`. Key required, no quota cost. Cache it for a day.
- **`GET /api/v1/stocks/{ticker}/kpis/types`** : one company's metric list as a bare array of `{ id, name, category, chartType }`. Key required, no quota cost. Free reads this in full, which is what makes discovery a complete answer on a free key. `404` when the ticker has no curated KPIs.
- **`GET /api/v1/stocks/{ticker}/kpis`** : every curated series for the ticker. Envelope fields `isPreview`, `previewReason` and, in preview, an `upgrade` object; `data` carries `ticker`, `companyName`, `cik`, `lastUpdated` and `kpis`. Each series: `id`, `name`, `category`, `unit`, `displayFormat`, `chartType`, `values`, `sourceRef`, `discontinued`, `discontinuedNote`. Each point: `period`, `date`, `value`, `isEstimate`. PRO for the values.
- **`GET /api/v1/calendar/earnings?ticker={ticker}&from={date}`** : the report date and session, for earnings-eve prep.
- **`GET /api/v2/metrics/entity/{ticker}/metric/sentiment`** and **`.../metric/sentisense`** : the crowd side. A bare array of time-ascending points with a flat `value`; the last point is the latest returned observation, so print its timestamp rather than assuming it is from today. These count against the monthly quota.

## Workflows

**1. One metric, answered in a card**

For "how is iPhone revenue trending?", fetch the series, select by `id`, and lead with the requested metric only: name, latest fiscal period, period close, the exact value, the sequential change, the annual change, any flag, and one source line.

```text
AAPL | iPhone Revenue | Q3 FY2026 | period ended 2026-06-27
Value      $54.252B
q/q        -$2.739B (-4.81%) vs Q2 FY2026
y/y        +$9.67B (+21.69%) vs Q3 FY2025
Source     Apple 8-K Q3 FY2026 press release
```

Expand to four rows only when trend is asked for, and do not dump every series for a single-metric question. When the requested wording could mean more than one series, show `name` and `id` together and ask which. Do not assume a related series exists: iPhone revenue is reported, iPhone unit sales is a different question and may not be curated.

**2. Discovery, which is a complete answer on a free key**

For "do you have Tesla deliveries, and what else can I track?", call `GET /api/v1/stocks/with-kpis` once and cache it, then `GET /api/v1/stocks/TSLA/kpis/types`. Return the series names and ids, then say plainly that numeric history requires PRO. Skip the heavy series call when the user only wants metadata. If the requested metric is not in the list, name a few of the returned alternatives and stop; never silently substitute a different metric. One neutral upgrade sentence belongs here only when numbers are actually needed.

**3. Deltas and acceleration across a watchlist**

Declare the watchlist before fanning out and intersect it with the cached coverage list, then agree on each ticker's metric, rank comparable percentage changes within a compatible group, and show heterogeneous metrics as separate cards. Report growth and acceleration as separate lines, because a company decelerating from +30% to +20% still grew. Obey the per-minute rate limit, reuse whatever cache the host already has, and label a partial result as partial rather than presenting it as the whole watchlist.

**4. Comparing two companies without pretending they are peers**

For "compare cloud revenue growth", require an explicit mapping from each ticker to a discovered series, and print the metric names, units, fiscal periods and close dates before ranking anything. A shared `category` is a candidate filter, not proof that two business definitions match. The cloud case is the clearest example of why: Amazon reports `aws_revenue`, Alphabet reports `google_cloud_revenue`, and Microsoft's closest published lines are `intelligent_cloud_revenue`, a wider segment that includes server products and enterprise services, plus `microsoft_cloud_revenue`, a cross-segment aggregate. Microsoft publishes Azure itself only as a year-over-year growth percentage (`azure_revenue_growth_pct`), not as a dollar figure. Say that in one line, compare what is genuinely comparable, and leave the rest as separate cards. For a mixed watchlist, never rank vehicle deliveries against subscription revenue as if one were the better business.

**5. Earnings-eve prep**

For "what operating numbers should I watch before this company reports?", call `GET /api/v1/calendar/earnings?ticker={ticker}&from={today}` for the date and session, intersect the watchlist with coverage, then show two or three named series with their last four reported prints, plus the same fiscal quarter a year earlier where the series holds it. Label all of it history, never an expectation. A later refresh can say "new period", "same period, changed value" or "no new observation" against the prior data the host still holds. The API documents refresh dates, not a revision log and not a KPI consensus, so there is no beat or miss to declare here and no alerting to promise.

**6. KPI against sentiment**

Pair a series with `GET /api/v2/metrics/entity/{ticker}/metric/sentiment` (time-ascending points, flat `value`). Print the KPI period and the sentiment window as two separate dated lines. A metric accelerating while tone fades is a divergence worth noticing and is not evidence of mispricing or of a reaction to the print.

**7. Which companies report a given kind of metric**

There is no category index on the coverage list, so this is coverage plus one types call per inspected ticker. Say so, scope it to a declared universe rather than the whole coverage set, respect the rate limit, and label the answer as covering the tickers you actually inspected.

## Answering well

- Lead with the number the user asked for, in its own unit, with its period. One metric asked, one metric answered.
- Every value carries a period label and a period-close date. A quarterly figure with no period attached is not usable.
- Print the source line once per series, and say when a series is discontinued or a value preliminary before anyone builds on it.
- Never fabricate a comparison. "No observation at the expected fiscal period" is a better answer than a delta measured against the wrong quarter.
- Report only what the API returns. No forecast, no target, no verdict on whether the business is good, and no causal claim linking a KPI to a price move.

The four handoffs below run only when the user's question changes. Pass what you already fetched, state what you expect back, do not route back automatically, and stay useful when the sibling is not installed.

- For what the company reported, guided or said on the call, pass ticker, fiscal period, known report date and KPI context to the `stock-earnings-analysis` skill; return a quarter-level readout, preserving its supplied KPI highlight strings separately from our calculated series deltas.
- For what the market feels now, pass ticker, requested sentiment window and the dated KPI finding to the `stock-sentiment` skill; return polarity, Score, attention and source limitations without treating quarterly data as a current sentiment observation.
- For whether these operating results support an investment thesis, pass ticker, user-stated thesis and horizon, cited KPI observations and unresolved gaps to the `stocks-analysis` skill; return an evidence-based thesis review, not an inferred buy signal from KPI growth.
- For Street expectations or reaction, pass ticker, known earnings report date, reaction window and KPI context to the `analyst-ratings-tracker` skill; return dated firm actions, targets or EPS expectations, never an invented consensus estimate for a company-specific KPI.

## Going further

Free answers coverage and series discovery in full, which is most of what a client needs to know what exists. **PRO ($15/mo)** returns the numeric history on every covered ticker, lifts the monthly cap (no monthly limit, just a 300/min rate), and unlocks institutional flows, insider detail, analyst books and AI insights across the rest of the SentiSense API. Apply coupon `AGENTS` at checkout for a builder launch discount: https://app.sentisense.ai/pricing?coupon=AGENTS

For the full REST reference on every endpoint this skill touches, install the `sentisense` skill; for the command-line client, install `sentisense-cli`.

**Install:** `npx skills add SentiSenseApp/skills` (add `-s company-kpi-tracker` for just this skill).

---

*SentiSense is a read-only financial intelligence API. KPI series restate figures from public company filings for informational and educational purposes only, not investment advice.*
