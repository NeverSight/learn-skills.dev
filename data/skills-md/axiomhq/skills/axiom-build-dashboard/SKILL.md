---
name: axiom-build-dashboard
description: Designs and builds Axiom dashboards via API. Covers chart types, APL and metrics/MPL query patterns, SmartFilters, layout, and configuration options. Use when creating dashboards, migrating from Splunk, or configuring chart options.
---

# Building Dashboards

## Philosophy

1. **Decisions first.** Every panel answers a question that leads to an action.
2. **Overview → drilldown → evidence.** Start broad, narrow on click/filter, end with raw logs.
3. **Rates and percentiles over averages.** Averages hide problems; p95/p99 expose them.
4. **Simple beats dense.** One question per panel. No chart junk.
5. **Validate with data.** Never guess fields—discover schema first.
6. **Compute what's asked, or defer.** If a panel can't be computed, replace it with a `Note` documenting the blocker. Never substitute a different quantity, even disclosed. See [Compute or Defer](#compute-or-defer).

---

## Entry Points

| Starting from | Workflow |
|---------------|----------|
| **Vague description** | Intake → check dataset kind → design blueprint (APL or MPL) → queries per panel → deploy |
| **Template** | Pick template → customize dataset/service/env → deploy |
| **Splunk dashboard** | Extract SPL → translate via axiom-spl-to-apl → map to chart types → deploy |
| **Grafana dashboard** | Project canonical panel spec (`expr`, `legendFormat`, `unit`, `title`, `description`) → translate PromQL → map chart types → deploy. See [reference/grafana-migration.md](./reference/grafana-migration.md). |
| **Exploration** | Use axiom-sre to discover schema/signals → productize into panels |

---

## Intake: What to Ask First

1. **Audience & decision**
   - Oncall triage? (fast refresh, error-focused)
   - Team health? (daily trends, SLO tracking)
   - Exec reporting? (weekly summaries, high-level)

2. **Scope**
   - Service, environment, region, cluster, endpoint?
   - Single service or cross-service view?

3. **Dataset kind.** Use MCP `listDatasets` and check `kind`. For a separately configured deployment, use `scripts/metrics/datasets <deploy>`.
   - `otel:metrics:v1` / `otel-metrics-v1` → metrics dataset, follow the **Metrics path**.
   - anything else → events/logs dataset, follow the **APL path**.

   > **Never run `getschema` on a metrics dataset.** It returns 0 rows without error.

   **APL path:** discover fields with `['dataset'] | where _time between (ago(1h) .. now()) | getschema`. Continue to steps 4–5.

   **Metrics path:** Use Axiom MCP for metrics discovery and queries, then follow the **Metrics/MPL Blueprint**.

4. **Golden signals** (APL path)
   - Traffic: requests/sec, events/min
   - Errors: error rate, 5xx count
   - Latency: p50, p95, p99 duration
   - Saturation: CPU, memory, queue depth, connections

5. **Drilldown dimensions** (APL path)
   - What do users filter/group by? (service, route, status, pod, customer_id)

---

## Dashboard Blueprint

Pick the blueprint matching the dataset kind.

### APL Blueprint (events/logs datasets)

#### 1. At-a-Glance (Statistic panels)
Single numbers that answer "is it broken right now?"
- Error rate (last 5m)
- p95 latency (last 5m)
- Request rate (last 5m)
- Active alerts (if applicable)

#### 2. Trends (TimeSeries panels)
Time-based patterns that answer "what changed?"
- Traffic over time
- Error rate over time
- Latency percentiles over time
- Stacked by status/service for comparison

#### 3. Breakdowns (Table/Pie panels)
Top-N analysis that answers "where should I look?"
- Top 10 failing routes
- Top 10 error messages
- Worst pods by error rate
- Request distribution by status

#### 4. Evidence (LogStream + SmartFilter)
Raw events that answer "what exactly happened?"
- LogStream filtered to errors
- SmartFilter for service/env/route
- Key fields projected for readability

### Metrics/MPL Blueprint (metrics datasets)

Use `align to $__interval using …` for bucketing — `$__interval` is supplied by the dashboard runtime. Hard-coded windows over- or under-resolve. Follow the [Metrics/MPL chart contract](./reference/metrics-mpl.md) for discovery and validation. `chart-add --mpl` rejects inline time ranges (`[1h..]`).

Exception: for sparse metrics where `$__interval` rounds to empty buckets, a fixed wider window (e.g. `1h`) is acceptable; document why on the chart.

#### 1. At-a-Glance (Statistic panels)
Current values — "what's the state right now?"
- Choose the `group` function by what the panel should show across series.
- Pass the unit of the result to `chart-add --unit`: the metric's `unit` from its metadata, or the new unit after a `map` or a rate that changes it (`prom::rate` on `By` gives `By/s`). Ratio metrics (0–1) need `| map * 100` in MPL before `--unit "%"`.

#### 2. Trends (TimeSeries panels)
Trends over time — "what changed?"
- Choose the `align` function by what each interval should show.
- Group by low-cardinality tags only (≤10 series per chart).
- Embed the unit in `--name` (`"P95 Latency (ms)"`, `"Memory (MiB)"`); scale magnitudes in MPL (`| map / 1048576` for bytes → MiB).
- Overlay pipelines that one query cannot produce together (p95 and p99, replicas vs HPA max) with `queries[]` on one chart: one `chart-add` run per pipeline, then merge. See [chart-config.md § Multiple Queries](./reference/chart-config.md#timeseries--multiple-queries).

#### 3. Breakdowns (TimeSeries or Table panels)
Per-entity detail — "where should I look?"
- Metrics broken down by entity (host, pod, service).
- Filter to keep series count manageable.
- One dimension per panel; don't overload a single chart.

#### 4. Entity State (TimeSeries or Table panels)
Boolean/state metrics — answer "what is on/off/active?"
- Choose the `align` function by the state question each interval answers.
- Sparse state metrics may need a fixed wider interval (1h+).

---

## Required Chart Structure

Each chart needs a unique kebab-case `id` (`error-rate`, `p95-latency`); every layout `i` must match one. Pass the same id to `chart-add --id` and `layout-pack <id>:…`. `dashboard-assemble` cross-checks before emit.

---

## Chart Unit Configuration

Pass a unit string to `chart-add --unit` (`"%"`, `"ms"`, `"req/s"`). `chart-add` never writes the `unit` enum, which the Console ignores. On an MPL Statistic, `chart-add` writes `set custom_unit="<unit>";` into the query and adds a `customUnits` suffix only for units the Console does not format. Pass the UCUM code of the result (`USD`, `s`, `By`, `%`), never a symbol such as `$`. For a 0–1 ratio, multiply by 100 and pass `--unit "%"`. On an APL Statistic, `chart-add` adds the suffix only for units the Console does not format, because the Console formats a field from its unit metadata. `%` keeps its suffix there. See [chart configuration](./reference/chart-config.md) for other options.

---

## Compute or Defer

Each panel either computes the requested quantity, or it's replaced by a `Note` documenting the blocker. Substituting a different quantity is never acceptable — disclaimers don't reach whoever acts on the number.

Defer template (use `chart-add --type Note`):

```
**Deferred — blocked by:** <one-line reason>.

**Original spec:** <what the panel should compute, dimensions, unit>.

**To unblock:** <pointer to the fix>.
```

Common blockers: MPL parser limits, missing tag with no reverse-tag equivalent, missing metric with no OTel rename match. Full rationale: [reference/design-playbook.md § Substituting a Different Quantity](./reference/design-playbook.md#substituting-a-different-quantity-for-the-asked-one).

---

## Chart Types

| Type          | When                                                | Key constraint                                                       |
|---------------|-----------------------------------------------------|----------------------------------------------------------------------|
| Statistic     | Single KPI, current value                           | Query must return one row.                                           |
| TimeSeries    | Trends over time, percentile overlays               | `bin_auto(_time)`; `percentiles_array()` for multi-percentile. Several pipelines on one chart via `queries`; see [chart-config.md § Multiple Queries](./reference/chart-config.md#timeseries--multiple-queries). |
| Table         | Top-N lists, breakdowns                             | Bound with `top N`; control columns via `project`.                   |
| Pie           | Share-of-total for ≤6 categories                    | Aggregate to ≤6 slices; never high-cardinality.                      |
| LogStream     | Raw event inspection                                | No row limit (`take`, `limit`, `top`), aggregation, or join. The Console adds its own sort and limit. Select fields with `project-keep`, keep `_time`, and filter hard. |
| Heatmap       | Distribution / latency density                      | `summarize histogram(field, buckets) by bin_auto(_time)`.            |
| Scatter Plot  | Correlate two metrics per group                     | `summarize avg(x), avg(y) by group`.                                 |
| SmartFilter   | Interactive filter bar                              | Each panel query needs `declare query_parameters`. See `reference/smartfilter.md`. |
| Monitor List  | Monitor status display                              | No APL — select monitors in UI.                                      |
| Note          | Markdown context, headers, runbook links            | `chart-add --type Note --text "<md>"`.                               |

Per-type APL recipes: `reference/chart-cookbook.md`.

---

## Chart Configuration

`chart-add` covers the common path (type, id, name, query, dataset, unit, sparkline). For options it doesn't expose — `aggChartOpts` variants on TimeSeries, several queries on one TimeSeries (`queries`), `tableSettings.columns` on Table/LogStream, `hideHeader`, etc. — start from a `chart-add` output and merge the extra fields with `jq`. See `reference/chart-config.md` for the full option set, and the rejected-field list before merging anything bespoke.

---

## APL Patterns

### Time Filtering

Dashboard chart queries inherit time from the picker — omit `_time` filters. Ad-hoc queries (Axiom Query tab, `axiom-sre`) need an explicit `where _time between (ago(1h) .. now())`.

### Bin Size Selection

Use `bin_auto(_time)` — it adjusts to the dashboard time window. Manual `bin(_time, …)` is only justified for non-standard cases (e.g. matching an upstream batch interval); document why.

### Cardinality Guardrails

Bound `summarize … by …` with `top N` or a filter. Unbounded grouping on high-cardinality fields (`user_id`, `trace_id`) blows up.

```apl
| summarize count() by route | top 10 by count_   // bounded
| summarize count() by user_id                    // unbounded — avoid
```

### Field Escaping
Fields with dots need bracket notation:

```apl
| where ['kubernetes.pod.name'] == "frontend"
```

Fields with dots IN the name (not hierarchy) need escaping:

```apl
| where ['kubernetes.labels.app\\.kubernetes\\.io/name'] == "frontend"
```

### Recipes

Traffic, error-rate, latency-percentile, and other golden-signal APL recipes: `reference/chart-cookbook.md`.

---

## Layout Composition

`layout-pack` packs charts row-major into the 12-column grid using per-type defaults (Statistic 3×3, TimeSeries 6×4, Table 6×5, LogStream 12×6, Note 12×2). Override with `id:WxH` when needed. Grid recipes: `reference/layout-recipes.md`. Naming and panel-ordering conventions: `reference/design-playbook.md`.

### Sections

Collapsible groups are a top-level `sections` array. Pass them to `dashboard-assemble`. Do not invent `sectionId` on the chart file, and do not discover the shape by sending an invalid update.

```bash
dashboard-assemble \
  --name "API" \
  --datasets logs \
  --layout /tmp/d/layout.json \
  --section "Requests:err-rate,traffic-ts" \
  --section-collapsed "Errors:top-errors" \
  /tmp/d/c-err-rate.json /tmp/d/c-traffic-ts.json /tmp/d/c-top-errors.json
```

- The title is the text before the first `:`. Chart ids follow, comma-separated, and must match chart `id`s.
- Flag order is display order. `--section-collapsed` sets `defaultCollapsed: true`.
- The section `id` is a UUID derived from the title, so the same title keeps the same id on the next run.
- A chart omitted from every `--section` stays ungrouped. Leave every SmartFilter chart ungrouped.
- A Note used as a grid header is layout, not a section. Use `--section` when the dashboard should collapse a group and stop its queries.

---

## Dashboard Settings

### Refresh Rate

`dashboard-assemble --refresh oncall|team|exec` (60/300/900s) or pass an explicit integer (≥60). Short refresh + long time range = expensive queries; pick the longer end for exec/weekly boards.

### Sharing

API tokens create shared dashboards only (`owner: "X-AXIOM-EVERYONE"`); private dashboards aren't supported. Per-user data visibility is still enforced by dataset permissions.

### URL Time Range Parameters

`?t_qr=24h` (quick range), `?t_ts=...&t_te=...` (custom), `?t_against=-1d` (comparison)

---

## Setup

Tools, prerequisites, and `~/.axiom.toml` configuration: see `README.md`. Verify with `scripts/setup`.

---

## Deployment

### Scripts

| Script | Usage |
|--------|-------|
| `scripts/chart-add --type <T> --id <id> --name <n> [--apl <q> \| --mpl <q> --dataset <d>] [--unit <u>]` | **Emit a single chart JSON** to stdout. Splits APL vs MPL; MPL queries are checked for inline time ranges; unit fields applied per chart type. |
| `scripts/layout-pack <id>:<Type\|WxH> ...` | **Emit a layout JSON array** to stdout. Row-major into a 12-column grid; type names map to default sizes. |
| `scripts/dashboard-assemble --name … --datasets … --layout F.json [--section TITLE:id,id ...] [opts] CHART_FILES…` | **Compose a complete dashboard JSON** from chart files + layout. Owns the envelope (`owner`, `schemaVersion`, `qr-` prefix, `refreshTime` validation, id cross-checks, `sections`). |
| `scripts/dashboard-list <deploy>` | List all dashboards |
| `scripts/dashboard-get <deploy> <id>` | Fetch dashboard JSON |
| `scripts/dashboard-validate <file>` | Validate JSON structure |
| `scripts/dashboard-create <deploy> <file>` | Create dashboard |
| `scripts/dashboard-update <deploy> <id> <file>` | Update (needs version) |
| `scripts/dashboard-chart-patch <deploy> <id> <chart-id> <patch-file> (--version <version> \| --overwrite)` | Patch one chart |
| `scripts/dashboard-copy <deploy> <id>` | Clone dashboard |
| `scripts/dashboard-link <deploy> <id>` | Get shareable URL |
| `scripts/dashboard-delete <deploy> <id>` | Delete (with confirm) |
| `scripts/axiom-api <deploy> <method> <path>` | **Dashboard/app API only** (rewrites to `app.*`). For data/metrics endpoints use `scripts/metrics/axiom-api` |
| `scripts/metrics/axiom-api <deploy> <method> <path>` | **Data/metrics API** (supports `AXIOM_URL_OVERRIDE` for edge routing) |
| `scripts/metrics/datasets <deploy>` | List datasets with `kind` and edge deployment |
| `scripts/metrics/metrics-spec` | Fetch MPL query specification |
| `scripts/metrics/metrics-info <deploy> <dataset> ...` | Discover metrics, tags, and values |
| `scripts/metrics/metrics-query <deploy> <mpl> <start> <end>` | Execute a metrics query (raw — no `$__interval` injection) |
| `scripts/metrics/mpl-validate-chart <deploy> '<MPL>' [start] [end]` | **Validate a chart MPL pipeline.** Rejects inline time ranges. The server fills `$__interval`. Use this in place of raw `metrics-query` when authoring chart queries. |

> The two `axiom-api` scripts are not interchangeable. `scripts/axiom-api` is for the dashboard app API; `scripts/metrics/axiom-api` is for data/metrics endpoints and edge routing. Wrong one → 404.

### Targeted Chart Updates

Use `scripts/dashboard-chart-patch` when changing one existing chart and the dashboard layout, metadata, and other charts should remain untouched. It calls `PATCH /v2/dashboards/uid/{uid}/charts/{chartId}` with a JSON Merge Patch under the `chart` request field.

Patch files contain only the chart fields to change:

```json
{
  "name": "Error Rate (5m)",
  "query": { "apl": "['logs'] | summarize errors=countif(status >= 500)" },
  "config": { "stale": null }
}
```

`null` removes an existing field. Nested objects merge recursively. If `id` is present in the patch, it must match the `<chart-id>` path argument. The server validates the resulting full dashboard before saving.

Use `--version <version>` for optimistic concurrency after fetching the dashboard with `dashboard-get`. Use `--overwrite` only when last-write-wins behavior is intended. Continue using `dashboard-update` for layout changes, multi-chart edits, dashboard metadata, owner, refresh interval, or time window updates.

### Workflow

`chart-add`, `layout-pack`, and `dashboard-assemble` own the JSON shape. Each chart lives in its own temp file; nothing chart-shaped re-enters the agent's context.

1. Discover schema (`axiom-sre` / `getschema` for events; Axiom MCP for metrics).
2. Write each panel query. Validate APL via `axiom-sre` with an explicit time filter; follow the [Metrics/MPL chart contract](./reference/metrics-mpl.md) for MPL.
3. `chart-add --type … --apl '<APL>'` *or* `chart-add --type … --mpl '<MPL>' --dataset <name>` per chart, redirected to its own file.
4. `layout-pack <id>:<Type|WxH> …` for the layout (ids in display order).
5. `dashboard-assemble --name … --datasets … --layout LAYOUT [--section TITLE:id,id ...] CHART_FILES…` to compose. Repeat `--section` for each collapsible group. Use `--section-collapsed` when the group should start collapsed.
6. `dashboard-validate` then `dashboard-create` (or `dashboard-update`).
7. `dashboard-link` for the URL — never hand-construct.

---

## Sibling Skill Integration

- **axiom-spl-to-apl** — Splunk SPL → APL (`timechart` → TimeSeries, `stats` → Statistic/Table). See `reference/splunk-migration.md`.
- **axiom-sre** — schema discovery via `getschema`, baseline exploration.

---

## Templates

Compose with `chart-add` + `layout-pack` + `dashboard-assemble`. Pre-built templates remain under `reference/templates/` (`blank.json`, `service-overview.json`, `service-overview-with-filters.json`, `api-health.json`) for legacy use; `dashboard-from-template` instantiates them but assumes specific field names (`service`, `status`, `route`, `duration_ms`) and needs sed-fixing. Prefer composition for new work.

---

## Common Pitfalls

| Problem | Cause | Solution |
|---------|-------|----------|
| `getschema` returns 0 rows | Dataset is `otel:metrics:v1` or `otel-metrics-v1` | Use MCP `listMetrics` for metrics discovery. |
| 404 from metrics API calls | Used `scripts/axiom-api` (dashboard) instead of `scripts/metrics/axiom-api` | Use `scripts/metrics/axiom-api` for `/v1/query/*`, `/v1/datasets`. |
| Statistic shows `1` instead of `100%` for a 0–1 ratio | The Console does not scale OTel unit `1` | `\| map * 100` in MPL, then `chart-add --unit "%"`. |
| Statistic shows the unit twice (`$1.031K$`) | A `customUnits` suffix on a unit the Console formats (`"$"` on `USD`) | Pass the UCUM code (`--unit USD`). `chart-add` rejects `$`. |
| MPL Statistic shows a bare number after `map` or a rate | The result no longer carries the metric's unit | Pass the unit of the result to `chart-add --unit` (`map / 3600` on `s` gives `--unit h`). |
| MPL rate tile shows `KB` instead of `KB/s` | `--unit` names the metric's unit, not the rate's | Pass the per-second unit (`prom::rate` on `By` gives `--unit By/s`). |
| OTel histogram chart shows nonsense | Histogram aligned as a scalar | Use `bucket … using interpolate_cumulative_histogram` (or `_delta` per `temporality`). See [promql-to-mpl.md § Histogram translation](./reference/promql-to-mpl.md#histogram-translation-histogram_quantile--bucket--using-interpolate__histogram). |
| Grafana migration filters/groups on the wrong subset | Read `expr` without `description`, or vice versa | Project all five panel fields before authoring; see [reference/grafana-migration.md](./reference/grafana-migration.md). |
| PromQL metric name not found | Skipped OTel rename rules | Drop `_total`, decompose histograms, normalise units; validate with `listMetrics`. Labels need reverse-tag discovery. See [grafana-migration.md § Name Mapping](./reference/grafana-migration.md#name-mapping-promql--otel-ingest). |
| MPL chart aggregates across a dimension PromQL filtered/grouped on | Dropped a selector or `by(...)` during translation | Every `{label=…}` → `where`; every `by(…)` → `group by`. See [reference/promql-to-mpl.md](./reference/promql-to-mpl.md). |
| Two related series need different pipelines (p95 and p99 histograms, replicas vs HPA max) | Forced into one query, or split across two panels | Put each pipeline in `queries[]` on one TimeSeries, one `chart-add` run per query, then merge with `jq`. See [chart-config.md § Multiple Queries](./reference/chart-config.md#timeseries--multiple-queries). |
| Panel shipped a different quantity than asked | Substituted instead of deferring | Replace with a `Note` documenting the blocker. See [Compute or Defer](#compute-or-defer). |
| 403 "creating private dashboards" | API tokens only create shared dashboards | Leave `owner` as `dashboard-assemble`'s default (`X-AXIOM-EVERYONE`). |
| 400 `invalid_dashboard` while adding sections | Chart JSON invented `sections` or `sectionId` | Pass `--section` / `--section-collapsed` to `dashboard-assemble`. Do not probe the API. |

---

## Reference

- `reference/chart-config.md` — All chart configuration options (JSON), including several queries on one TimeSeries
- `reference/metrics-mpl.md` — Metrics/MPL chart contract and discovery scripts
- `reference/smartfilter.md` — SmartFilter/FilterBar full configuration
- `reference/chart-cookbook.md` — APL patterns per chart type
- `reference/layout-recipes.md` — Grid layouts and section blueprints
- `reference/splunk-migration.md` — Splunk panel → Axiom mapping
- `reference/grafana-migration.md` — Grafana panel → Axiom mapping (canonical-spec projection, PromQL→MPL pointers, OTel rename rules)
- `reference/promql-to-mpl.md` — PromQL → MPL translation rules (selectors, groupings, rate, histograms, ratios, reverse-tag discovery)
- `reference/design-playbook.md` — Decision-first design principles
- `reference/templates/` — Ready-to-use dashboard JSON files

For APL syntax: https://axiom.co/docs/apl/introduction
