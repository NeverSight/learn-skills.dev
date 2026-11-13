---
name: pytorch-clickhouse
description: Load this FIRST whenever working with PyTorch CI data (any pytorch/* org repo), the torchci/HUD codebase, or the PyTorch HUD ClickHouse database. Covers the two MCP servers that reach this data — pytorch-hud (curated no-SQL triage plus ~145 pre-tuned named queries) and clickhouse-mcp (raw SQL, schema introspection, EXPLAIN, query optimization) — including which tool to reach for, the data model, and how to debug and speed up queries. Use when investigating CI/trunk failures, flaky or disabled tests, queue times, job/workflow/runner status, benchmarks, or writing, debugging, or optimizing any ClickHouse query against HUD data — even if the MCP servers aren't named explicitly.
---

# PyTorch HUD ClickHouse

Two MCP servers reach the **same** PyTorch HUD ClickHouse backend — the only ClickHouse you have access to. Pick by task:

- **`pytorch-hud`** — curated, no-SQL triage and ~145 pre-tuned named queries. **Try this first.** Cheaper, structured, hard to get wrong.
- **`clickhouse-mcp`** — raw SQL, schema introspection, EXPLAIN, and the tools for debugging and optimizing queries. Drop to this when no curated query fits.

Both hit the same data, so you can prototype with a curated query and refine in raw SQL.

## Start here (once per session)

- `mcp__pytorch-hud__readme_howto_pytorch_treehugging_guide` — the triage workflow tour.
- `mcp__clickhouse-mcp__readme_howto_use_clickhouse_tools` — the raw-query usage guide.

These MCP tools are deferred: load their schemas with `ToolSearch` (e.g. query `select:mcp__pytorch-hud__readme_howto_pytorch_treehugging_guide`) before calling them.

## pytorch-hud — curated triage (no SQL)

Each tool answers one question without you writing SQL:

| Tool | Answers |
|---|---|
| `get_recent_commits_with_jobs_resource` | What's failing on a branch/SHA? The workhorse — filter with `job_name_filter_regex`, `failure_line_filter_regex`, and the `include_success/pending/failures` flags to keep the context small. |
| `get_job_details_resource` | Full detail for one job, once you've narrowed down. |
| `get_master_commit_red_resource` | How red/green has trunk been over a time range? |
| `get_queued_jobs_resource` | Is the CI queue backed up? |
| `find_commits_with_similar_failures_resource` | When did this failure first appear? (full-text search, date-range bisection) |
| `get_disabled_test_historical_resource` | Flaky / disabled-test history. |
| `get_artifacts_resource` | Build/test artifacts for a job. |

**Logs — download once, then dissect (never pull a whole log into context):**
`download_log_to_file_resource` → then `extract_log_patterns_resource` / `filter_log_sections_resource` / `extract_test_results_resource`. `get_s3_log_url_resource` gives the raw URL without downloading.

## pytorch-hud — curated named queries (the fast path)

~145 hand-tuned, maintained queries. Prefer these over ad-hoc SQL for speed and correctness.

1. **List:** `get_clickhouse_queries_resource` → catalog of names (e.g. `master_commit_red`, `queue_times_historical`, `commit_jobs_query`, `flaky_tests`).
2. **Inspect params:** `get_clickhouse_query_params_resource(query_name)` → `{params: {name: Type}, tests: [...]}`. Doubles as a data-model hint.
3. **Run:** `query_clickhouse_resource(query_name, parameters)` — `parameters` is a **JSON string** matching those params.

**These named queries ARE the repo's `clickhouse_queries/`.** To see exactly what a query does, open `torchci/clickhouse_queries/<name>/query.sql` and its `params.json`. The loader is `torchci/lib/clickhouse.ts` → `queryClickhouseSaved(queryName, params)`. `params.json` declares `params` (name → ClickHouse type), optional `defaults`, and `tests` (sample values; `{"from_now": N}` means N days from now — negative is the past, e.g. `-7`). SQL uses typed placeholders `{name: Type}` with server-side binding. Editing guide: torchci `README.md`, section "How to edit ClickHouse queries".

The catalog spans trunk health, commit/job/workflow status, tests (flaky/disabled/timing), queue & latency, cost & duration, runner utilization, merge/revert/PR metrics, autorevert, benchmarks, and CRCR.

## clickhouse-mcp — raw SQL, debug & optimize

| Tool | Use |
|---|---|
| `get_clickhouse_tables` | List tables. `database` defaults to `default`; pass `databases='all'` to span all three. |
| `get_clickhouse_schema(table)` | **Full `CREATE TABLE` DDL** — engine, `ORDER BY`, skip indexes, column comments. The first stop for any perf work. |
| `explain_clickhouse_query` | `EXPLAIN`. Add `explain_plan=true` (index/granule pruning) and `explain_estimate=true` (parts/rows/marks to read). |
| `run_clickhouse_query` | Execute. `measure_performance=true` → `duration_ms` + `memory_usage`. Big results go to a `result_file`; `total_result_rows_n` is the true row count. |
| `get_query_details(name)` | Fetch a checked-in named query to reuse as a template. Pass `include_performance_samples=0`. |
| `semantic_search_docs` | Search the official ClickHouse docs (PREWHERE, FINAL, partition pruning, …). |

### Optimize a slow query

1. `get_clickhouse_schema(table)` — read the DDL. Find `ORDER BY` (the sort key), `PARTITION BY`, and any skip indexes. This dictates what to filter on.
2. Filter on the **sort-key prefix** (or a skip-indexed column). Reuse a proven query via `get_query_details` if one exists.
3. `explain_clickhouse_query(..., explain_plan=true, explain_estimate=true)` — confirm pruning *before* running. In the `Indexes` block, granules-kept ≈ granules-total means **no pruning, i.e. a full scan**.
4. `run_clickhouse_query(..., measure_performance=true)` — get the real `duration_ms` and `memory_usage`.
5. Iterate: narrow the time range, drop `SELECT *`, avoid `FINAL`, and hit the sort key or a skip index. Re-EXPLAIN → re-run → compare.

## Writing performant queries (first try)

The surest path to a fast query is to **reuse a curated named query** (above) — they're already tuned. When you must write raw SQL, this checklist gets you a near-optimal query on the first pass.

**First, read the DDL:** `get_clickhouse_schema(table)`. The `ORDER BY` decides which filters are fast — writing a WHERE without knowing the sort key is guessing.

- **Filter on the `ORDER BY` prefix, left-to-right** — that's what prunes granules. A non-key, non-skip-indexed filter is a full scan. (See Data model essentials for the `workflow_job` "sorted by `id`, not time" trap.)
- **Never wrap a filter column in a function** — `toDate(ts)=…`, `lower(x)=…` defeat the index. Transform the constant instead: `WHERE ts >= today() AND ts < today()+1`.
- **Bound time as a range**, and **select only the columns you need — never `SELECT *`** (I/O scales with columns read).
- **Dedup yourself** on the SharedReplacingMergeTree tables — `... ORDER BY _inserted_at DESC LIMIT 1 BY id` (preferred) or `FINAL` (costlier); see Data model essentials. A bare SELECT can return duplicates. **Check the sort key first:** if it ends in a per-row unique column, `FINAL` collapses nothing and `argMax` on one version column drops the remaining tiebreak.
- **Don't filter on ALIAS columns** (e.g. `log_url`) — computed per-row, no index.
- **Reference each CTE once.** ClickHouse does not materialize a named subquery — every reference site is a separate execution, so N references cost N scans. Keep `WITH <expr> AS <alias>` scalars one level deep too; they expand textually into the AST and nesting them multiplies, up to a hard `TOO_BIG_AST` failure.
- **Joins:** smaller table on the RIGHT; pre-filter each side in a subquery; use `IN (subquery)` when you only need to filter. `join_use_nulls=0` here, so an unmatched row fills with the **type default, not NULL** — `IS NULL` will not find it.
- **Aggregation:** filter in WHERE not HAVING; use approximate `uniqCombined`/`quantile()` on high cardinality; `countIf`/`sumIf` to segment in one pass.
- **Verify, don't assume:** `EXPLAIN indexes = 1` and read `Granules: kept/total` — kept ≈ total means a full scan.

For the full ~30-rule reference — mechanisms, examples, join algorithms, memory-spill settings, types, and version notes — read `references/clickhouse-perf.md`.

## Data model essentials

Three databases: **`default`** (CI/GitHub — `workflow_job`, `workflow_run`, `test_run_s3`, `push`, `pull_request`, `merges`, …), **`benchmark`** (`oss_ci_benchmark_*`, …), and **`misc`** (`autorevert_*`, `disabled_tests_historical`, `queue_times_*`, `oss_ci_utilization_*`, `greenlight_pr_state`, …). `*_mv` are materialized views; `*_dict` are dictionaries.

- **Don't assume "filter on a time column = fast."** Check the DDL. Example: `default.workflow_job` is `ORDER BY (id, run_id, ...)` — sorted by `id`, **not by time**. A `WHERE created_at > ...` gets zero primary-key pruning but ~99% pruning from a minmax skip index on `created_at`. If a filter column is neither in `ORDER BY` nor skip-indexed, it is a full scan.
- Core tables are **SharedReplacingMergeTree** (ClickHouse Cloud's ReplacingMergeTree) — rows can be duplicated until a background merge collapses them. Curated queries dedup with `FINAL` or `ORDER BY _inserted_at DESC LIMIT 1 BY id`. `FINAL` is correct but costs; prefer the `LIMIT 1 BY` pattern on hot paths.
- **`misc.greenlight_pr_state`** — the GreenLight verdict ledger, one row per emission. `ORDER BY (repo, pr_number, run_id, emit_id)` ends in a per-row unique column, so **`FINAL` collapses nothing** (measured: 904 rows in, 904 out) and `argMax(…, version)` throws away the `run_id` tiebreak. Read the current state per PR with `ORDER BY pr_number, run_id DESC, version DESC LIMIT 1 BY pr_number`. This is the general trap, not a quirk of one table — see "Deduplication & FINAL" in `references/clickhouse-perf.md`.
- **`default.merges` holds one row per merge *push*, not per landed PR.** A ghstack stack lands as a single push whose non-final commits appear only in `push.commits`; those stack members have **no row in `merges` at all** — 8% of pytorch/pytorch main-branch merge commits over a recent 90-day window, and higher inside the GreenLight cohort. If you need every landed PR, derive merges from main-branch commit titles (`extract(…, '\\(#(\\d+)\\)\\s*$')`) or expand the `commits` array, rather than reading `merges`.
- **Same shape, same undercount: `clickhouse_queries/reverts/` and `num_reverts/` read only `push.head_commit.message`.** A revert that lands as a non-final commit of a multi-commit push is invisible to them — ~11% of main-branch revert commits over a 90-day window. Neither query warns its readers, so treat their output as a lower bound.

## Gotchas (live-verified)

- **No trailing `;`** — the readme says not to append one. The tools happen to tolerate it, but follow the readme to be safe.
- **`lint_clickhouse_query` is broken** — it returns an internal SQLFluff error on all input. Don't rely on it.
- **`get_query_execution_stats` is permission-denied** for this user (`system.query_log` is not granted). The same denial hits `get_query_details` performance samples, so always pass `include_performance_samples=0`. That leaves `explain` + `run(measure_performance=true)` as your only perf instruments.
- `run_clickhouse_query` inline output caps at `inline_result_limit_bytes` (default 1024, max 10240). Cap with `LIMIT` and read the `result_file` for large results.
