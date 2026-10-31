---
name: allium-investigation
description: >-
  Investigate an onchain entity, protocol, market, or wallet question with Allium. Use when the task needs a defensible analytical answer rather than a one-off lookup: check Terminal for existing coverage, select the right source, build the method from a small test to production, validate the result, make calibrated claims, and save reproducible Explorer queries (with an optional dashboard hand-off prompt for Allium Assistant). Chains after `data-matching` (source selection) rather than repeating it.
---

# Allium Investigation

Use this for a scoped investigation, not for a current price or balance lookup. Its output
is a conclusion that another person can inspect, rerun, and challenge.

Use the Allium MCP tools directly — `run_sql_query`, `get_query_run_results`,
`create_explorer_query`, `search_terminal`, `get_terminal_results`, `search_schemas`,
`search_docs` — rather than describing what a query would show. If the MCP isn't
available, fall back to the `allium-data` skill / CLI.

## Output contract

Start by stating the decision question, subject, time window, networks, and proposed
metric. If any of these would materially change the answer, ask before querying.

End with the answer and the evidence that directly supports it, plus clearly marked
interpretation and open uncertainty. If the result will be shared, reused, or is
decision-relevant, finish with step 7 below — saving the load-bearing queries to Explorer
— rather than leaving the evidence only in the chat transcript.

## Investigation workflow

### 1. Check Terminal before investigating from scratch

Someone on the Allium team may have already built and maintained the answer. Call
`search_terminal` with the entity/metric/protocol before writing any SQL — it's a
metadata-only search (dashboard label, path, category, tags), no compute cost. If a
dashboard looks relevant, call `get_terminal_results` with its `dashboard_id` (no
`chart_id`) to see the chart manifest, then again with a `chart_id` to pull its SQL
and/or latest precomputed rows — this also costs no compute units, since it only reads
existing definitions and results. If it directly answers the question, cite it (with
`result.queried_at` for the precomputed rows) and link the dashboard instead of
re-deriving the same thing from raw tables. If it's close but not exact, it's still a
faster starting point than a blank investigation — adapt its SQL rather than starting
over.

### 2. Select the source before committing to a method

Run `data-matching` next if a Terminal dashboard didn't already answer the question — it
defines the data contract, compares candidate tables/endpoints against it, and proves
coverage with a bounded query via `search_schemas`/`search_docs`. Don't guess a table name
or infer coverage from a chain merely being listed; a catalog entry alone is not coverage.
Once a source is selected, identify the native network and distinguish it from bridged or
wrapped representations before proceeding.

### 3. Write a data plan

Before the main query, record:

- the metric definition and denominator;
- inclusion, exclusion, and entity-attribution rules;
- time grain and timezone;
- the checks that could falsify the intended interpretation.

Treat this as a hypothesis. Revise it when the discovered schema or first result disagrees.

### 4. Build from a small test to a production query

For the narrow-sample/cardinality/units check, use `run_sql_query` — it's explicitly
ephemeral (not saved, can't back a chart or dashboard), which is exactly right for a
throwaway check. It returns a `run_id` immediately; call `get_query_run_results` with that
`run_id` to get status, columns, row count, and cost (pass `poll_timeout_seconds` if it's
still running). If the run failed, errored, or came back with zero rows, fix the SQL and
re-run — don't report an empty or failed run as the answer unless zero rows genuinely *is*
the answer to the question asked.

Once the small test looks right and you're about to run the query whose result you'll
actually use, switch to `create_explorer_query` (with `run_on_creation=True`) instead of
running it through `run_sql_query` first — re-running an already-validated query through
`run_sql_query` and saving it afterward duplicates the compute. This also means the
production query is already a saved Explorer query by the time you reach step 7.

Use Realtime data for current state of a known asset or wallet. Use Explorer/SQL for
historical, comparative, aggregated, or cross-chain questions. Do not mix their freshness
semantics into one unlabeled metric.

### 5. Validate the result

Apply the checks that fit the method:

- reconcile a total with its components;
- check joins for duplicate multiplication and verify `COUNT(DISTINCT ...)` at the
  intended grain;
- confirm token units, decimals, USD conversions, and the denominator;
- compare adjacent periods and investigate discontinuities rather than smoothing them;
- independently re-query at least one load-bearing figure from a different aggregation,
  filter, or sample.

Do not treat agreement with an external aggregator as proof. It can be a sanity check, but
the published claim needs its own method and source trail.

### 6. Make calibrated claims

Separate three kinds of statements:

- **Observed:** what the query directly shows.
- **Interpretation:** a plausible explanation, labelled as such and tied to supporting
  evidence.
- **Unknown:** what the available data cannot establish.

Do not turn correlation into causation, a labelled address into a verified controller, or
a sample into a population without evidence.

### 7. Make it reproducible in Explorer

A conclusion that only exists in the chat transcript isn't reproducible — anyone revisiting
it has to retype the SQL from memory. By step 4 your load-bearing query should already be
saved via `create_explorer_query`; if it isn't yet, save it now rather than leaving it as
an unsaved `run_sql_query` result.

**Single result** — if the investigation produced one load-bearing query, that's usually
enough on its own: optionally call `create_explorer_visual` on it (chart/value/table — pick
the type that fits the data) and `share_explorer_query` to hand back a link. Skip the rest
of this step.

**Multiple results meant to become a dashboard** — the Allium Assistant in the app builds
dashboards, but it cannot write SQL in dashboard mode; it only assembles saved queries it's
told about. There's no MCP tool to assemble a multi-query dashboard directly, so the
hand-off is a prompt the user pastes into Assistant. After saving each query, print one:

```
Build me a dashboard.

Title: <short title>
Goal: <one sentence — what should this dashboard show?>

Queries:
- <query_id>: <one-line description>. Cols: <col> (stock→last), <col> (flow→sum), ...
- <query_id>: <one-line description>. Cols: ...

Filters: <optional, one line>
Elements: <optional, one line — e.g. "KPI: total_x (last); chart: y over time by chain">
```

The two things that must never be dropped are the **query IDs** and each column's
**stock/flow tag** — a stock metric (supply, balance, TVL, price: aggregate `last`/`first`)
summed like a flow metric (volume, count, fees: aggregate `sum`) is the most common real
dashboard bug, and Assistant can't infer it from the column name alone. If the prompt is
running long, cut `Filters`/`Elements`/`Goal` down to a phrase before cutting a query or a
stock/flow tag. Keep the whole thing well under 800 characters — short enough that someone
can glance at it, copy it, and paste it straight into Assistant without editing.
