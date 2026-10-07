---
name: revenuecat-charts
description:
  Use when the user asks about RevenueCat data, analytics, charts, or KPIs — querying charts with
  get-chart-options-schema and get-chart-data, interpreting subscription metrics, or sharing
  dashboard chart links. For forecasts, projections, or run-rates, use revenuecat-forecasting.
---

# Accessing RevenueCat charts

When querying a RevenueCat chart, follow this workflow:

1. Use `get-chart-options-schema` to discover a chart's available options.
2. Use `get-chart-data` with the right options to retrieve the chart data.
3. Analyze the data, using scripts for any non-trivial arithmetic.

Via the `rc` CLI (see the `revenuecat-cli` skill): `rc charts list` to list charts, `rc charts options <chart>` for the schema, and `rc charts show <chart>` for the data.

In general, to avoid clogging the context, start with defined timeframes and larger resolution, then narrow down.

## 1. Discover chart options with `get-chart-options-schema`

- Treat `get-chart-options-schema` as the source of truth for each chart before calling
  `get-chart-data`. It returns the chart's supported `resolutions`, `filters`, `segments`, and
  `user_selectors`. Always call this tool with `"realtime": true`. Later `get-chart-data` calls must
  use string IDs exactly as returned here.
- `filters` are the dimensions you may later constrain in `get-chart-data`.
  - Each filter has:
    - an `id` to later use as the filter `name`.
    - a `value_mode` that tells you how to choose valid values:
      - `inline_enum` means you must use the `id` of one of the returned `options`. Resolve
        user-supplied names first with the matching list tool, such as `list-products`,
        `list-offerings`, `list-apps`, etc.
      - `inferred_standard` means use the standard code from `value_source` such as an ISO country
        code.
      - `dynamic` means values come from observed project data and must match exactly.
  - Do not pass display names, store product identifiers, bundle IDs, or guessed values unless the
    schema says they are valid values.
- `segments` are the dimensions you may later group by in `get-chart-data` using `segment`.
  - A segment entry directly gives the dimension `id` to use. It does not list segment values
    because the chart will group by it and show all values in the output.
  - Filters and segments are separate per-chart lists, so never assume a filterable dimension is
    segmentable. For example, `conversion_to_paying` may support `product_id` and
    `offering_identifier` as filters but not as segments.
- `user_selectors` are chart-specific switches that change what metric or window the chart returns.
  Each selector is keyed by the selector ID to pass in `get-chart-data`'s `selectors` JSON object
  and usually includes allowed option IDs plus a default. For example, the `revenue` chart may use
  `revenue_type` (`revenue`, `revenue_net_of_taxes`, `proceeds`), while conversion charts may use
  `conversion_timeframe` and default to `7_days`. State non-default selector choices when presenting
  results.
- `resolutions` list the supported time granularity and their string IDs for `get-chart-data`. You
  must always pass one of these resolution IDs (such as `"0"` for day or `"2"` for month) when later
  calling `get-chart-data`.

## 2. Retrieve chart data with `get-chart-data`

### Calling `get-chart-data`

- Always set `"realtime": true` and specify start date, end date and resolution ID.
- Always follow the guidelines from a prior `get-chart-options-schema` for that chart.
- Consider rate limits: don't query too many charts at once.
- Date ranges are inclusive (start_date and end_date are included in the range). When asked for
  data for the "last N days", take that into account (use today as end date, start date is (N-1)
  days before today).
- Use available `filters` to constrain the output. They are a JSON-encoded array of
  `{"name": "<filter id>", "values": ["<value id>", ...]}`.
  - Values within one entry are ORed; separate entries are ANDed. Example: App Store revenue in the
    US or the UK:
    `"[{\"name\": \"store\", \"values\": [\"app_store\"]}, {\"name\": \"country\", \"values\": [\"US\", \"GB\"]}]"`.
  - Use at most one entry per filter name: a repeated name silently replaces the earlier entry
    (it does not combine with it). Filter values must not contain commas.
- Use the available `selectors` for configuring the chart. They are a JSON-encoded object mapping
  selector IDs to option IDs, e.g. `"{\"revenue_type\": \"proceeds\"}"`. Omitted selectors use their
  defaults; the response echoes the applied values in `user_selectors`.
- Use `segment` to group the output by some of the segmentable dimension IDs:
  - Note that segmenting multiplies output size. You can keep responses small by using a coarser
    resolution, a shorter date range, `limit_num_segments` (keeps the top N by value and folds the
    rest into "Other"), or `aggregate` when you only need per-segment totals.
- Use `aggregate` for summary-only questions such as totals or averages (e.g. "total Q1 revenue").
  Prefer this over fetching and computing from raw data points yourself. Combined with `segment` it
  returns compact per-segment summaries (e.g. country averages). In the output, `values` will be
  empty and `summary` will contain just those operations.
- Pass `currency` to convert outputs to some monetary unit (see `yaxis_currency` in the response).

### Reading `get-chart-data` outputs

- `measures` lists the metrics the chart returns (display name, unit, description). Most charts
  return several, e.g. `revenue` may return Revenue, Transactions, and Ad Impressions.
- `values` is a flat array of points `{cohort, measure, value, incomplete}`, plus `segment` when
  segmented. `cohort` is the Unix timestamp of the period start; `measure` and `segment` are indexes
  into the `measures` and `segments` arrays. The first segment is usually a `"is_total": true` -
  never sum it together with the other segments.
- `summary` holds `total` and `average` per measure display name, nested per segment when segmented.
- Points with `incomplete: true` cover partial periods: the current period, and the first period
  when `start_date` falls mid-period (since `expand_periods` defaults to false). Exclude them from
  trend or comparison analysis, and call them out when presenting. Point-in-time charts (MRR,
  actives, trials) ignore `expand_periods`: their values are snapshots at period boundaries and are
  never partial.
- `annotations` lists dated notes the user made on their dashboard (e.g. releases, launches or
  experiments). Check them when explaining movements in the data.
- Invalid filters, segments, or selector values fail with a 400 `parameter_error` whose message
  lists the supported IDs. On such errors, re-read the options schema instead of retrying guesses.

## 3. Analyze the data

- Segmented responses include a `Total` segment, and the `limit_num_segments` cap folds segments
  beyond the top N into an `Other` segment. Use `Total` as the baseline; do not sum segments
  yourself.
- Do complex arithmetic on chart output (growth rates, segment shares, combining numbers across
  calls) with scripts (e.g. `jq` or a short Python script) instead of reasoning over the numbers.
- The most recent period may be flagged incomplete. Do not compare it against full periods without
  saying so.
- Before speculating about the cause of a metric shift, first check the available user annotations.
- Cohort charts measure within a cumulative window from first seen, chosen by a selector
  (`conversion_timeframe` on conversion charts, `customer_lifetime` on realized LTV charts), one
  window per call. State the window when presenting results and hold it constant when comparing
  cohorts.

# Interpreting metrics

Subscription apps are driven by four forces:

- Acquisition - how many new customers are arriving to the app
- Conversion - how many of those customers are converting into trials or paid plans
- Retention - how long do those customers retain
- Reactivation - how can you bring back old users

The net movement of an apps revenue will be the result of the combination of these forces. When
giving advice, always use benchmark data to make sure you aren't incorrectly diagnosing an issue.

General guidelines:

- Before telling the user RevenueCat has no source for a metric they named, pick the likely
  chart(s), call `get-chart-options-schema` for options, then `get-chart-data` and check its
  `periods` / `measures` — unfamiliar names are often one period or measure inside a chart
  (schema alone does not list those). Missing from `get-benchmarks` means no peer percentile
  band, not that the value can't be computed.
- After looking: if nothing in the tools matches, or two readings would produce materially
  different numbers, ask the user to define the metric. Do not invent a definition.
- When using the data tools, date ranges are inclusive (start_date and end_date are included in the range). When asked for data for the "last N days", take that into account (use today as end date, start date is (N-1) days before today).
- Provide links to RevenueCat charts (see the Dashboard URL Format section below) where it is useful. Provide specific links including filters, segments, date ranges, etc — eg. if you are asked for proceeds in the last 3 months, link to the revenue chart with custom date range of the last 3 months and the `revenue_type` selector set to `proceeds`, don't link to the plain revenue chart
- For forecasts, projections, or run-rates, load the `revenuecat-forecasting` skill before pulling charts.

## Revenue

- When asked for general revenue numbers without additional specification, default to gross revenue (ie. revenue including taxes and store commissions) and call it out.

## Acquisition

- Use the New Customers chart to understand how much top of funnel the app is driving.
- Segmenting New Customers by Country, or Apple Ads dimensions can be helpful in informing
  acquisition.
  - RevenueCat's Apple Ads integration sets attribution dimension information like campaign, ad
    group, keyword
  - Developers can also manually set these attribution dimensions on a per-customer level using
    reserved customer attributes
- Do not treat a zero result from an explicit attribution filter as proof that the broader channel
  has zero users or zero activity. For example, `attribution_source = Organic` only means users
  explicitly tagged with that value; it does not include untagged users or every organic/non-paid
  user.
- If attribution data is sparse or missing, say that clearly. Use "unattributed" or "not explicitly
  tagged" rather than assuming those users came from a specific channel.

## Conversion

The definition of conversion may vary depending on what model the app is using. They may be
converting to a trial, that then converts into a subscription. Or they may be sending users directly
to a subscription.

- Use the Initial Conversion chart to see the proportion of new customers that start a subscription
  or trial within the selected conversion timeframe.
- Use the Conversion to Paying chart to see the proportion of new customers that made a payment
  within the selected conversion timeframe.
- Initial Conversion (started a trial or subscription) and Conversion to Paying (made a payment)
  measure different events. Never use one as a stand-in for the other, or compare a value from one
  against a value from the other.
- You can then further determine if they are using free trials by looking at the New Trials chart.
- The Trial Conversion Rate chart is a helpful chart for understanding the performance of just that
  trial conversion.
- Filtered charts keep the all-new-customers denominator. For example, filtering Conversion to
  Paying on a specific `product_id` gives the share of ALL new customers converting to that product,
  not that product's own conversion rate. State this caveat when presenting filtered results.

## Retention

- The Churn chart will tell you the % of the active subscriber base that is lost each period. It can
  be difficult to interpret or benchmark because it is a blend of different periods.
- When you want to understand the long term retention of different products, look at the
  Subscription Retention chart or the Cohort Explorer chart using the `retained_subscriptions`
  measure, which returns how many subscriptions remained active (ie. not expired) over time.
- To understand when in their lifecycle subscriptions get cancelled (ie. auto-renewal turned off),
  use Cohort Explorer with the `subscriptions_set_to_renew` measure.
- The Subscription Retention chart reports each cohort's renewals period by period, as counts and
  precomputed rates ("Month N" / "Month N rate" columns). A single period answers questions like
  "what share renewed once": the first renewal is the period matching the plan length (Month 1 for
  monthly plans, Year 1 for annual). Filter by `product_duration` to keep one plan length per read,
  and by `subscription_type` (`new`) to exclude product changes and resubscriptions. Periods a
  cohort hasn't had the full opportunity to reach are reported as incomplete — don't read them as
  zeros.

## Reactivation

- The only real way to understand Reactivation is looking at the MRR Movement chart and the
  Resubscription MRR

## Investigating metric shifts

When a metric change needs explaining — revenue dropped, trials fell, conversion spiked — follow
this order before answering:

1. **Quantify the shift.** Pull the chart data, confirm the magnitude and timing.
2. **Check configuration.** Offerings, packages, products, paywalls and experiments are not visible
   in metrics, so never infer them from a chart. If your answer names any of them, look it up in
   this run:
   - `list-experiments` with `status="stopped"` and `status="running"`. If an experiment stopped
     near the shift, call `get-experiment-results` to see which variant won.
   - `list-offerings` with `limit: 100` (the default page of 20 rarely covers a real project), then
     `get-offering` on the `is_current` id with `expand: ["package.product"]`. An offering with
     `paywall_id: null` has no RevenueCat paywall — load `revenuecat-paywall-design` before giving
     paywall advice.
   - `get-product-store-state` before saying a product is retired, unavailable, or no longer
     selling. Report store status in plain language, never raw field names.
   - If experiments and offerings don't explain it, `list-paywalls` for paywall changes.
3. **Check annotations.** Look at the `annotations` field in the chart response.
4. **Only then form a hypothesis.** Present it as a hypothesis, not a finding. An unverified guess
   about configuration is a missing tool call, never your headline finding.

Do not skip step 2. Once you have made the calls, if their results cannot explain the shift, say
so explicitly rather than constructing a mechanism.

## Populations and denominators

A rate only describes the population in its denominator. Before presenting one, check that this is
the population the question is about.

- When one segment dominates the denominator, the blended rate describes that segment, not the app.
  Re-query filtered to the population the question is about and lead with that number.
- **Never present a rate as evidence while also calling its denominator inflated or
  unrepresentative.** Re-query with a filter instead of caveating.
- Report the filtered numbers yourself rather than recommending the user go look at a filtered
  chart.

## Analytics comparisons

- Compare like with like. Any two numbers compared against each other must come from the same
  chart and metric, with the same conversion window and cohort definition. Use the same date range
  too, except in deliberate period-over-period comparisons.
- If you have a metric for one side of a comparison but not the other, query the missing side with
  the same chart and settings before comparing. Do not substitute a value from a different chart.
- For open-ended questions like "how are {segment} users doing?", do not stop at segment-only
  metrics. Pull the requested segment and an overall/unfiltered baseline for the key conversion or
  revenue-quality metric, then judge performance relative to that baseline. Do not evaluate a
  segment as "healthy", "underperforming" etc. without comparing it to a baseline.
- Do not compare revenue or conversions from a filtered new-customer cohort against total app
  revenue from all cohorts and renewals. If you cannot get a matching baseline, say so and avoid
  directional performance claims.
- When a user is confused that two metrics diverge, say what each one counts before explaining the
  gap.

Wrong — different charts merged under one header:

| Country | Conversion to paying (14d)          |
| ------- | ----------------------------------- |
| US      | 26.3% (this is Initial Conversion)  |
| PL      | 2.1% (this is Conversion to Paying) |

Correct — one column per metric, every value in a column from the same chart, metric, and settings:

| Country | Initial conversion (14d) | Conversion to paying (14d) |
| ------- | ------------------------ | -------------------------- |
| US      | 26.3%                    | 9.6%                       |
| PL      | 4.3%                     | 2.1%                       |

# Chart Dashboard Links

Generate shareable links to RevenueCat dashboard charts.

## Constructing a Link

A chart link must follow a specific [Dashboard URL Format](#dashboard-url-format) and must be built
from a verified previous successful `get-chart-data` call.

0. If there isn't a previous successful `get-chart-data` call for this chart, follow the Querying
   RevenueCat charts workflow above first.
1. Construct the link, starting with base:
   `https://app.revenuecat.com/projects/{project_id}/charts/{chart_name}`.
2. Add [`range` param](#range-param--required) with date range. This is required.
3. Add [`resolution` param](#resolution-param) with resolution. Don't trust defaults.
4. Add any filters as [`filter` params](#filter-params).
5. Add segment as [`segment` param](#segment-param), if segmenting.
6. Add [chart-specific selectors](#chart-specific-selectors) as needed.
7. URL-encode all values (spaces → `+`, colons → `%3A`, etc.)

## Dashboard URL Format

**IMPORTANT**: Use this exact structure:

```
https://app.revenuecat.com/projects/{project_id}/charts/{chart_name}?range={range_value}
```

- `{project_id}` — The short hex ID (e.g., `56965ae1`), not the full `proj56965ae1`
- `{chart_name}` — The same chart name used with `get-chart-data` (`revenue`, `churn`, `mrr`,
  `conversion_to_paying`, etc.)
- Project ID goes in the **path**, not as a query parameter

**Correct example:**

```
https://app.revenuecat.com/projects/56965ae1/charts/revenue?range=Custom%3A2025-11-16%3A2026-02-13
```

**WRONG — do not use:**

```
https://app.revenuecat.com/charts/revenue?project=proj56965ae1&chart_start=...&chart_end=...
```

## Query Parameters

### `range` param — required

The `range` parameter controls the date range. Format: `{preset}:{start_date}:{end_date}`, with
start_date and end_date in YYYY-MM-DD format. Use `Custom` as the preset.

**Always use this format** — do not use `start_date`, `end_date`, `chart_start`, or `chart_end`
params. Note: The `:` between parts must be URL-encoded as `%3A`.

Example: `range=Custom%3A2025-01-01%3A2025-12-31`

### `resolution` param

| Value | Meaning               |
| ----- | --------------------- |
| `0`   | Daily granularity     |
| `1`   | Weekly granularity    |
| `2`   | Monthly granularity   |
| `3`   | Quarterly granularity |
| `4`   | Yearly granularity    |

### `segment` param

Dimension to break down the data by. Use the exact dimension ID you were using to make the
`get-chart-data` request.

- `country` — by country
- `store` — by app store (App Store, Play Store, etc.)
- `product_id` — by product identifier
- `platform` — by platform (iOS, Android, etc.)
- `offering_identifier` — by offering

Segments vary per chart — only link a segment you successfully used in a `get-chart-data` call for
that chart.

### `filter` params

Filters are passed as individual query `filter` params with the content
`{dimension}%3A%3D%3A{value}`. Use the dimension names you used for the `get-chart-data` request.

| Dimension    | Example                                    |
| ------------ | ------------------------------------------ |
| `country`    | `filter=country%3A%3D%3AUS`                |
| `store`      | `filter=store%3A%3D%3Aapp_store`           |
| `product_id` | `filter=product_id%3A%3D%3Aprodbb68905d98` |
| `platform`   | `filter=platform%3A%3D%3AiOS`              |

To use multiple filters, regardless of whether they are for the same dimension or multiple
dimensions, include multiple `filter` query parameters. Passing multiple filters for the same
dimension will result in an OR operation, passing filters for different dimensions will result in an
AND operation.

### Chart-Specific Selectors

Selectors are passed as individual query params, with the same names and values used in the
`get-chart-data` `selectors` argument. Orientative examples (truth in `get-chart-data`):

- `revenue_type` (revenue chart) — `revenue`, `revenue_net_of_taxes`, or `proceeds`
- `conversion_timeframe` (conversion charts) — `0_days`, `3_days`, `7_days`, `14_days`, `30_days`,
  or `unbounded`
- `customer_lifetime` (realized LTV charts) — `7_days`, `14_days`, `30_days`, `3_months` up to
  `24_months`, or `unbounded`

## API to Dashboard Parameter Mapping

When translating from API parameters to dashboard URLs:

| API Parameter             | Dashboard Parameter                                    |
| ------------------------- | ------------------------------------------------------ |
| `start_date` + `end_date` | `range=Custom%3A{start}%3A{end}` (use `Custom` preset) |
| `segment`                 | `segment`                                              |
| `filters` (JSON array)    | Individual `filter` query params                       |
| `selectors` (JSON object) | Individual query params                                |

## Example: Building a Link

User wants: "Revenue chart for last 90 days, segmented by country, filtered to US and Germany"

Calculate dates: if today is 2026-02-13, then 90 days ago is 2025-11-16.

```
https://app.revenuecat.com/projects/56965ae1/charts/revenue?range=Custom%3A2025-11-16%3A2026-02-13&segment=country&filter=country%3A%3D%3AUS&filter=country%3A%3D%3ADE
```

User wants: "Churn chart from August 2025 to now"

```
https://app.revenuecat.com/projects/56965ae1/charts/churn?range=Custom%3A2025-08-01%3A2026-02-13
```

## Getting Project ID

The project ID can be found via the `list-projects` tool, which lists all projects with their ID.

- The tool returns IDs starting with `proj`, for example `proj56965ae1`
- **For dashboard URLs, strip the `proj` prefix** — use just `56965ae1` in the path
