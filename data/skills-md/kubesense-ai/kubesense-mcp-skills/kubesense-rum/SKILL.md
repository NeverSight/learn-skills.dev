---
name: kubesense-rum
description: Aggregate and read real user monitoring (RUM) data via KubeSense MCP — sessions, views, actions, errors, resources and long tasks from browser and mobile apps. Covers the rum_<type> signals, the per-event-type field catalog, which fields accept LIKE or group-by, nanosecond durations and their _ms/_s twins, feature flags and attributes, and the dashboard panel shape. Counts, rates and percentiles with analyze-telemetry, raw rows with search-rum. There is no alerting, SQL or SPL for RUM.
metadata:
  version: "1.0.0"
  author: kubesense
  repository: https://github.com/kubesense-ai/kubesense-mcp-skills
  tags: kubesense,rum,real-user-monitoring,web-vitals,sessions,frontend,errors,observability
---

# KubeSense RUM

Requires the KubeSense MCP server; see **[kubesense-mcp](../kubesense-mcp/SKILL.md)** for
connection, auth, and the shared WHERE-clause reference. RUM queries resolve RBAC against
the **RUM** module (`rbac(rum)`). A key without it fails with
`rbac(rum): this API key does not have access to this resource`; ask for the RUM grant
rather than retrying. `search-rum` needs the same grant. So do the RUM list routes it reads through
(`POST /rum/explorer/{sessions,views,actions,errors,resources,longtasks}`), which also
guard the RUM pages.

## Signals

RUM has six signals, one per event type. Each reads its own table.

| Signal | One row is | Typical question |
|---|---|---|
| `rum_session` | a user session | how many sessions, how many had errors |
| `rum_view` | a finished page or screen view | LCP, load time, views per page |
| `rum_action` | a click, tap or scroll | which actions are slow or frustrating |
| `rum_error` | a captured error or crash | which errors, how many crashes |
| `rum_resource` | an HTTP or asset request | slow or failing requests, by host |
| `rum_long_task` | a main-thread long task | what blocks the UI |

`rum_view` counts only ended views of non-system sessions. Every row is placed in time by
its own `start_timestamp`, so a long session is counted in the window where it started.

## Tools

| Tool | Use when | Notes |
|---|---|---|
| `get-fields` (`signal: "rum_view"`, …) | Always, first | Field catalog for that event type |
| `analyze-telemetry` | Counts, rates, percentiles, trends | One sub-query per signal, set with `selectedMode` |
| `search-rum` | Reading individual sessions, errors, requests | Raw rows for one signal; see [search-rum](#search-rum) |

There is no `analyze-rum`. `analyze-logs` and `analyze-traces` do not take RUM signals.
To compare RUM with logs or traces, or to compute a rate, put several sub-queries in one
`analyze-telemetry` call and add a formula; see
[multi-query](../kubesense-mcp/references/multi-query.md).

## Discover First

Call `get-fields` with the signal you will query. The field set differs per event type:
`lcp` exists only on `rum_view`, `error_type` only on `rum_error`, and `view_name` allows
LIKE on `rum_view` but not elsewhere. The full catalog for every event type is in
**[references/field-catalog.md](./references/field-catalog.md)**; use it to check a name
before the call, and `get-fields` as the authority for the deployment you are talking to.

`get-fields` for RUM returns the static catalog only, in the usual TSV:

- The header line is `# signal=rum_view total_count=<N> truncated=<bool> note=RUM has no
  attribute-key scan; ...`. There is no `attribute_scan_error`. The note says to type a
  custom attribute as `@key` (no LIKE on attributes) and a feature flag as
  `feature_flag.<key>`.
- Operators come as sets (`# ops.o1=EQ|NEQ|IN|NIN|LT|GT|LTE|GTE`). A field that allows
  LIKE has a set that includes `LIKE` / `ILIKE`; an exact field such as `user_email` does
  not. Trust the set over any assumption about the field.
- A trailing `notes` column appears when some field has a note, for example
  `filter-only: use it in WHERE only (milliseconds); aggregate the base field lcp instead; platform: browser`
  on `lcp_ms` and `filter-only: not groupable; platform: browser` on `lcp_target_selector`.
- `enum_values` carries `severity`'s `crash` and `error`.
- Pass `search` to narrow the list (`search=lcp` returns `lcp`, `lcp_ms`, `lcp_s` and
  `lcp_target_selector`).

There is no attribute-key discovery. When the user needs a custom attribute, ask for the
key or infer it from their instrumentation, and type it with the `@` prefix. A wrong key
matches nothing and returns an empty result, not an error.

## search-rum

`search-rum` reads raw rows for one signal: the same rows the Data Explorer List panel
shows. Use it to look at individual events (which sessions crashed, what the slowest
requests were, the text of an error). Use `analyze-telemetry` for anything that is a number:
counts, rates, percentiles and trends. Reading rows to compute a count is slower and cuts
off at the page limit.

Call `get-fields` with the same `signal` first. `where` and `required_fields` take catalog
labels, `@key` for an attribute and `feature_flag.<key>` for a flag (views and errors only).
`from_time`, `to_time` and `signal` are required. There is no `clusters` argument; passing
one is refused. Scope to an app with `application_id = "<id>"` or `env = production`.

**The slowest failed requests in the last hour, 20 per page**

```json
{
  "signal": "rum_resource",
  "from_time": "2026-10-20T10:00:00Z",
  "to_time": "2026-10-20T11:00:00Z",
  "where": "status_code >= 500",
  "sort_by": "duration_ms",
  "sort_order": "desc",
  "page_size": 20
}
```

Arguments beyond the shared search ones: `sort_by` (catalog label; default
`start_timestamp`), `sort_order` (`asc` or `desc`, default `desc`) and `cursor`.
`required_fields` picks columns; empty gives the type's defaults.

| Signal | Default columns |
|---|---|
| `rum_session` | `start_timestamp`, `session_type`, `time_spent_ms`, `view_count`, `error_count`, `action_count`, `frustration_count`, `first_view_name`, `last_view_name` |
| `rum_view` | `start_timestamp`, `view_name`, `frustration_count`, `loading_type`, `loading_time_ms`, `view_time_spent_ms`, `country`, `browser_name` |
| `rum_action` | `start_timestamp`, `action_type`, `action_name`, `frustration_type`, `view_name` |
| `rum_error` | `start_timestamp`, `view_name`, `error_source`, `error_message` |
| `rum_resource` | `start_timestamp`, `view_name`, `resource_url`, `duration_ms`, `response_size`, `status_code`, `resource_type` |
| `rum_long_task` | `start_timestamp`, `duration_ms`, `view_name` |

The defaults use the `_ms` twins. A raw duration you request by name (`duration`) comes
back in nanoseconds; ask for `duration_ms` or `duration_s` instead.

**Output** is TSV. The first line is
`# total_count=unknown returned_rows=<N> truncated=<bool> next_cursor=<c> window_clamped=<bool> ...`,
followed by `# notice=<n>` lines when something needs saying, a header, and one line per
row. Every row also carries `application_id`, `session_id`, `row_id` (the event's own id),
`timestamp`, `has_replay` (set when the session has a stored replay) and `severity` (errors: `error` or `crash`).
Whatever `required_fields` you ask for, every row also carries the columns that identify it, always present: sessions `application_id`, `session_id`, `session_start`, `session_has_replay`; views add `view_id`, `view_start`; actions `action_id`, `action_start`; errors `error_id`, `error_start`, `is_crash`; resources `resource_id`, `resource_start`; long tasks `task_id`, `task_start` (each with `view_id` except sessions).

**Paging.** There is no total (`total_count=unknown`). While `next_cursor` is non-empty,
call again with the same `from_time`, `to_time`, `where`, `sort_by`, `sort_order`,
`page_size` and `required_fields`, and `cursor=<next_cursor>`. The cursor is a page token
bound to the query, so a cursor replayed under a different query is refused.

- Paging is page-based with no depth limit, for every `sort_by`. There is no keyset.
- `page_size` defaults to 10 and is clamped to 200. The Data Explorer List panel loads 50
  rows per page.

**What a row is**

- Rows match the RUM page tables. Sessions and views are deduplicated. Live (still open)
  views are listed.
- Actions, errors, resources and long tasks are grouped by id: one row per id, start is the
  first occurrence, resource durations are medians and long-task durations are averages.
- `rum_error` lists only errors (`type = 3`).
- Blob fields cannot be listed or sorted by: `error_stack`, `handling_stack`, `threads`,
  `graphql`, `display`, `tags`.
- Array fields (`service`, `state`, `city`, `network_connectivity`, `ip`, `action_id`) cannot be
  sorted by.
- Each cell in the TSV output is cut at 2048 bytes. The list API itself does not cut strings.

**Window.** The window is clamped and snapped by the RUM data window. A `from_time` older
than raw retention (30 days for sessions and views, 7 days for the rest) is moved up to the
retention edge, and the window widens to the bucket boundaries of the RUM data. The header
says `window_clamped=true` when the window changed. A window entirely older than retention
is left as asked.

**No read-budget errors.** The list reads have no read-budget limit. A slow read can still
time out; shorten the window or filter on `application_id`, `env` or `session_id`.

## WHERE Syntax

The shared syntax from [kubesense-mcp](../kubesense-mcp/SKILL.md#where-syntax) applies,
with the field names from the RUM catalog.

```
env = production AND browser_name = Chrome
severity = crash AND country IN (US, DE)
view_name ILIKE "%checkout%"                    (rum_view only)
lcp_ms > 2500 AND browser_name = Chrome         (rum_view)
status_code >= 500 AND resource_host = api.example.com   (rum_resource)
error_count > 0                                 (rum_session)
feature_flag.new_checkout = true                (any event type)
@checkout.step = payment                        (attribute)
```

Quote values that contain `/`, `:`, `%` or a space. Write `NOT (x IN (...))`, not
`x NOT IN (...)`.

## Rules

1. **LIKE and ILIKE only on fields whose `LIKE` column says `yes`** in the catalog.
   Those are the low-cardinality columns (`env`, `country`, `error_type`, `action_name`,
   `view_name` on `rum_view`). Everything else (`user_id`, `view_url`, `resource_url`,
   `error_message`, `view_name` on the other event types) takes `=` and `IN`. A LIKE on
   them is refused with `LIKE is not supported on <field>; use = or IN`.
2. **No LIKE on `@attribute` fields.** Attributes take `=`, `!=`, `IN`, `<`, `>`, `<=`
   and `>=`. Comparisons need a number. `@plan LIKE ...` is refused with
   `operator "LIKE" not allowed for rum_view attribute field "plan"`.
3. **Array fields filter only.** `service`, `state`, `city`, `network_connectivity` and
   `ip` on `rum_session`, `ip` on `rum_view`, and `action_id` on `rum_error`,
   `rum_resource` and `rum_long_task` hold lists. `=` and `IN` test membership. They
   cannot be grouped or measured.
4. **Durations are nanoseconds.** Raw columns (`lcp`, `duration`, `loading_time`,
   `time_spent`, …) are stored and returned in nanoseconds, and cannot be a group-by.
   Each has an `_ms` and an `_s` twin (`lcp_ms`, `duration_s`) that is **filter-only**: use
   it in `where` (`lcp_ms > 2500` filters at 2.5 seconds), never as an aggregation field,
   group-by or list column. To aggregate a duration, use the base field (`p75` of `lcp`);
   the result is nanoseconds.
5. **Group-by is `no` for free-search ids and text** (`session_id`, `view_id`,
   `trace_id`, …). Group by a low-cardinality field instead. Five are groupable and return
   the top N groups (the page size): `error_message` (grouped by its first 200
   characters), `fingerprint`, `issue_id`, and `view_url` / `resource_url` (grouped by the
   path, without query string or fragment). Filters still read the full value, so a URL
   group label is a path, and `view_url = "<path>"` matches only URLs that have no query
   string.
6. **`feature_flag.<key>`** filters on every event type. It groups or measures only on
   `rum_view` and `rum_error`, where the flag value is stored on the row. On the other
   four it is stored per session, so a group-by there is refused. Keys are
   case-sensitive and values are text (`true`, `dark`, `5`). A group-by on a flag key
   (`feature_flag.new-checkout`) is confirmed on `rum_view`. The `where` form follows the
   engine source and has not been run against a live server.
7. **Attributes need `@`** in `where` (`@checkout.step`) and `is_attribute: true`
   without `@` in `group_by_fields` / `fields`. There is no discovery for the key.
8. **`severity`** on `rum_error` is `crash` or `error`, lowercase. It is the label for
   `is_crash`; type `severity`, not `is_crash` as a string.
9. **Boolean fields** (`session_is_active`, `slow_rendered`) take `true` or `false`.
10. **Platform-specific fields are not enforced.** `lcp` is browser-only and
    `battery_level` is mobile-only. Filtering on one for the wrong application type matches
    nothing and raises no error.
11. **`value_operation`** is `row_count`, `unique_count`, `avg`, `sum`, `min`, `max`,
    `p50`, `p75`, `p90`, `p95` or `p99`. `row_count` takes no field. Everything else takes
    exactly one `fields` entry. The numeric operations need a number field or an
    attribute; `unique_count` takes any non-list field.
12. **`alert_mode`, `group_by_present_only` and `lookback_seconds` are refused** for RUM.

## analyze-telemetry

Set `selectedMode` to the signal. Omitting it makes the sub-query a metrics query.

**p90 LCP per page, Chrome only, in milliseconds**

```json
{
  "from_time": "2026-10-20T10:00:00Z",
  "to_time": "2026-10-20T11:00:00Z",
  "query_type": "instant",
  "queries": {
    "A": {
      "selectedMode": "rum_view",
      "where": "browser_name = Chrome",
      "group_by_fields": [ { "field": "view_name", "is_attribute": false } ],
      "value_operation": "p90",
      "fields": [ { "field": "lcp", "is_attribute": false } ],
      "sort_direction": "DESC",
      "limit": 10
    }
  }
}
```

**Crashes per hour by error type**

```json
{
  "from_time": "2026-10-20T00:00:00Z",
  "to_time": "2026-10-21T00:00:00Z",
  "query_type": "range",
  "queries": {
    "A": {
      "selectedMode": "rum_error",
      "where": "severity = crash AND env = production",
      "group_by_fields": [ { "field": "error_type", "is_attribute": false } ],
      "value_operation": "row_count"
    }
  }
}
```

**Share of sessions that hit an error** — two queries and a formula, both ungrouped:

```json
{
  "from_time": "2026-10-20T10:00:00Z",
  "to_time": "2026-10-20T11:00:00Z",
  "query_type": "instant",
  "queries": {
    "A": { "selectedMode": "rum_session", "value_operation": "row_count" },
    "B": { "selectedMode": "rum_session", "where": "error_count > 0", "value_operation": "row_count" },
    "C": { "query_type": "formula", "expression": "(B/A)*100" }
  }
}
```

**Slowest hosts by p95 request time, failed requests only**
`selectedMode: rum_resource`, `where: "status_code >= 500"`,
`group_by_fields: [{"field":"resource_host"}]`, `value_operation: p95`,
`fields: [{"field":"duration"}]` (nanoseconds)

**Errors by feature flag value**
`selectedMode: rum_error`, `group_by_fields: [{"field":"feature_flag.new_checkout"}]`,
`value_operation: row_count`

**Sessions by a custom attribute**
`selectedMode: rum_session`, `group_by_fields: [{"field":"checkout.step","is_attribute":true}]`,
`where: "@checkout.step IN (cart, payment)"`

## Dashboard Panels

A stored panel query and the analyze call name the event type differently:

| | Field | Value |
|---|---|---|
| analyze-telemetry sub-query | `selectedMode` | `rum_view` |
| dashboard panel query | `selectedMode` + `rumEventType` | `"rum"` + `"view"` |

A panel with `selectedMode: "rum_view"` fails validation, and `"rum"` without
`rumEventType` is refused on save. The panel shape, with a `_ms` measure and its unit, is
in **[kubesense-dashboards](../kubesense-dashboards/SKILL.md#rum-query)**. Test the query
with `analyze-telemetry` first, then translate it.

Panel recipes for the usual RUM questions (unique users, crash-free users, Web Vitals
good/poor shares, Apdex, top errors and URLs, ANR rate) are in
**[references/dashboard-recipes.md](./references/dashboard-recipes.md)**.

## Limits

- **Retention.** Raw RUM rows are kept 7 days for `rum_action`, `rum_error`,
  `rum_resource` and `rum_long_task`, and 30 days for `rum_session` and `rum_view`, by
  default. A longer window returns only what is still stored (`search-rum` reports it as
  `window_clamped=true`); deployments can change the retention.
- **Row reads are bounded per call.** `search-rum` returns at most 200 rows a call and has
  no total. Paging has no depth limit. For questions that are a number,
  aggregate instead.
- **No alerts, SQL or SPL.** RUM is not a datasource for alert rules, `execute-sql` or
  `execute-spl`. Say so rather than approximating with logs.
- **No attribute-key discovery.** See Discover First.

## Failure Messages

Seen from a live server:

| Message | Cause |
|---|---|
| `unknown field "services" for signal=rum_session ...` | A storage name; type the catalog name (`service`) |
| `analysis failed: cannot group by lcp_ms` | Rule 4: `_ms` / `_s` twins are filter-only; aggregate the base field |
| `analysis failed: LIKE is not supported on user_email; use = or IN` | Rule 1 |
| `operator "LIKE" not allowed for rum_view attribute field "plan" — use one of: EQ, NEQ, ...` | Rule 2 |
| `rbac(rum): this API key does not have access to this resource` | The key lacks the RUM module |

Worded from the kubeapi source, not seen live:

| Message | Cause |
|---|---|
| `<field> is not a filterable field for <type>` | The field belongs to another event type, or is hidden |
| `<field> holds a list and cannot be grouped or measured; filter on it instead` | Rule 3 |
| `cannot group by <field>; it is a duration in nanoseconds` | Rule 4, on a raw column such as `lcp` |
| `cannot group by <field>` | Rule 5 |
| `feature flags are stored per session for <type>; filter on them instead` | Rule 6 |
| `<op> needs a numeric field; <field> is not numeric` | Measure on a string or boolean |
| `rum is not configured` | The deployment has no RUM database |
