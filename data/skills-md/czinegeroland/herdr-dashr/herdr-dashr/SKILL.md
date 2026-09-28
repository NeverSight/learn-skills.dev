---
name: herdr-dashr
description: >-
  Build the human a live dashboard of whatever they point you at — an app
  running on this machine, containers, a database, a Kubernetes cluster, an
  AWS, Azure or Google Cloud deployment — in a Herdr pane beside you: discover
  what runs and what data exists, start live collectors, and build the panels
  a system engineer checks (CPU, memory, IO, request rate, errors, latency,
  database load), without ever seeing real data values. Use when the human
  asks to visualize, monitor, watch, graph or "show me" something, asks for a
  dashboard, pastes a deployment or pipeline link, or wants to check that the
  right log messages fire. Also use it when the dashr MCP tools are connected.
metadata:
  generated-by: herdr-dashr
---

# Live dashboards with herdr-dashr

The human talks only to you. You open a dashboard pane beside yourself, find
out what is running and what can be measured, switch on live collectors, and
design a Grafana dashboard from what they deliver. **The pane keeps the data
flowing** — you never poll or loop — and **you only change the dashboard**.
You never see data values: only schemas, masked samples, row counts and
errors. Treat that as the physics of this environment, not an obstacle.

The goal is a dashboard that feels like magic: the human names a thing, and
seconds later sees its CPU, memory, traffic, errors, latency and database
load, live, laid out the way an experienced engineer would.

## The flow

1. **Open the pane** (below) — always with `DASHR_OTEL=1`: its Prometheus and
   Loki are where collectors write.
2. **Discover.** Find out what the human means and what data exists before
   drawing anything:
   - on this machine: `dashr discover` (containers and their kind, request
     log formats, `/metrics` endpoints, installed CLIs, cloud logins, project
     files);
   - anywhere else — a cloud, a cluster, a remote host: use its CLI
     (`aws`, `az`, `gcloud`, `kubectl`, `ssh`, ...). Install a missing CLI
     yourself; ask the human before logging in or changing their config.
     `reference/environments.md` says what to look for in each.
3. **Collect.** Switch on the collectors that deliver what the human asked
   about (`reference/collectors.md`): `dashr collect docker`, `host`,
   `process`, `logs <container>`, `postgres|mysql|redis <container>`,
   `scrape <url>`, and for everything else `exec` (a command printing
   Prometheus text on a schedule) and `stream` (a command printing log
   lines). Each is tried once and reports the metric names it produced.
   For a database's query performance — PostgreSQL or SQL Server, local or
   in any cloud, even one reachable only through a CLI tunnel — use `dashr
   db add` and `dashr db dashboard` (`reference/databases.md`).
4. **Build** the system dashboard (`reference/collectors.md`, "The system
   dashboard"): a stat row of health, then per service CPU, memory, network
   and disk IO, request rate, error %, p95 latency; a database row when there
   is one; recent errors from the logs. Then the panels specific to the
   human's question.
5. **Verify** with `panel_status`; fix or remove every panel that is not `ok`.
6. **Evolve** as the human reacts — add a collector, a drill-down, a watch.

**Never generate traffic to measure it.** Do not probe, curl or load-test the
human's services to fill a panel: it pollutes their logs and metrics. Measure
what already happens. If there is no traffic, say so.

## Opening the dashboard

**Open the pane. Do not describe how to open it.** Herdr opens a plugin pane
on request, so telling the human to find an action or run a command is the
failure this section exists to prevent.

```bash
"${HERDR_BIN_PATH:-herdr}" plugin pane open --plugin herdr-dashr --entrypoint dashboard \
  --placement split --target-pane "$HERDR_PANE_ID" --direction right --no-focus \
  --env DASHR_OTEL=1
```

`HERDR_PANE_ID` is your own pane, so the dashboard opens beside you rather
than beside whatever pane has focus. When the human pasted an AWS
CodePipeline console link, also add `--env DASHR_PIPELINE_URL=<the link>`:
dashr then inspects the pipeline's stacks and applies a first dashboard.

The command prints JSON; the new pane's id is its `pane_id`. The first start
pulls the Grafana image, so wait for it:

```bash
dashr wait --session <pane_id>
```

`dashr wait` prints the `session` id and a `brief`. The pane is a narrow
column showing the dashboard's link and how many collectors are live; the
human Ctrl-clicks the link to watch the dashboard in their browser, which
follows every change you make. Say that in one line, then discover.

The human closes the pane when they are done; closing it stops every
collector and deletes the Grafana and everything in it. Close it yourself
only when asked: `herdr pane close <pane_id>`.

## Before you start

```bash
dashr --help
dashr doctor
```

If `dashr` is not found, it has not been installed globally. `npx
herdr-dashr` runs it for one invocation without putting it on `PATH`;
installing does:

```bash
npm install -g herdr-dashr
```

A shell opened before that install keeps its old `PATH`, so a new terminal
may be all that is missing. `dashr doctor` checks Docker, which must be
running; if it is not, tell the human — you cannot start it for them.

## Calling the tools

Every dashboard tool is one command:

```bash
dashr tool <name> --session <session> --args '<json object>'
dashr tool apply_dashboard --session <session> --args-file dashboard.json
dashr tool                      # every tool with its arguments
```

It prints the tool's JSON answer and exits 0, or prints the error on stderr
and exits 1 (2 for a bad command line). Prefer `--args-file` for anything
long — a whole dashboard — and on Windows, where quoting JSON in a shell is
fragile. Inside a dashr chat pane the same tools are connected as MCP tools
with the same names and arguments; use those there.

## Building, step by step

Work in short iterations. A useful dashboard in two minutes beats a perfect
one in twenty.

1. **Understand the question.** What is the human debugging? A deploy, an
   error spike, a queue backing up, slow requests? Ask one short question if
   it is unclear; otherwise start.
2. **Probe.** `list_datasources` (uids, types, which are personal). Then
   `probe_query` the data you think answers the question — it returns field
   names, types, row counts and masked samples. Two or three probes are
   usually enough. See `reference/datasources.md` for each query model.
3. **Design.** Pick three to six panels that answer the question, most
   important first (top-left). Start from a recipe in
   `reference/recipes.md`; panel JSON rules are in
   `reference/dashboard-json.md`.
4. **Apply.** `apply_dashboard` with the whole dashboard. dashr validates
   datasource references, assigns ids and layout where missing, pins the uid,
   refresh and tags. The human watches it in their own browser, which
   shows the change within seconds without a reload.
5. **Verify.** `panel_status`. Every panel should be `ok`. For each `empty` or
   `error` panel: read the (masked) error, `probe_query` a simpler version,
   fix, re-apply. Never leave a broken panel on the dashboard; remove it if
   you cannot fix it and say why.
6. **Evolve.** When the human reacts ("what about the DLQ?", "only prod",
   "why did that spike?"), change the dashboard: add a drill-down panel,
   narrow a query, split by a label, change the time range. `get_dashboard`
   returns the current JSON to edit — modify it and re-apply rather than
   rebuilding from scratch.
7. **Watch and keep.** If the human wants to be told when something happens,
   `watch_panel` (evaluated locally; you never see the values). If the
   dashboard is worth keeping, `save_dashboard` it under a name the human
   picks (it stays on this machine and `load_dashboard` reopens it in a
   later pane), or `promote` it to the team's Grafana. When the human names a
   saved dashboard, open the pane and load it before building anything.

Report briefly after each apply: what the dashboard now shows and what is
still empty or failing. Do not describe values — you do not know them; the
human can see them.

## Privacy rules (enforced — do not work around them)

- Samples are masked: `<email#1>`, `<ipv4#2>`, `<user#3>`, `<card#1>`. The same
  value gets the same pseudonym within one answer, so repetition and
  cardinality are visible. Use that: "12 rows, 3 distinct users" is fine.
- Never try to read values another way: no `curl` to the Grafana port, no
  reading the dashboard pane (`herdr pane read`), no screenshots of
  dashboards with personal datasources (the `screenshot` tool refuses them;
  it exists for layout checks on non-personal data).
- Do not put personal data into queries or titles. Filter by labels and
  services, not by a person's email.
- Error messages are masked too; a `<email#1>` in an error is a hint that the
  query matched personal data.

## Tools at a glance

| Tool | Use it to |
|---|---|
| `list_datasources` | Learn uids, types and the personal flag. |
| `probe_query` | Test one query and see its schema and masked rows before building a panel. |
| `apply_dashboard` | Push the whole dashboard JSON. |
| `get_dashboard` | Fetch the current JSON to modify. |
| `panel_status` | Check every panel: ok / empty / error, rows, fields, masked errors. |
| `panel_data_sample` | Masked rows of one existing panel, to refine it. |
| `watch_panel` / `list_watches` / `remove_watch` | Alert the human on a threshold (Herdr notification, pane turns blocked). |
| `screenshot` | Layout check — non-personal dashboards only. |
| `open_for_pipeline` | Inspect an AWS CodePipeline and apply a first dashboard. |
| `promote` | Copy the dashboard to the team's persistent Grafana. |
| `session_info` | Mode and, in OpenTelemetry mode, the OTLP endpoint programs export to. |
| `save_dashboard` / `list_saved_dashboards` / `load_dashboard` / `delete_saved_dashboard` | Keep a dashboard on this machine by name and reopen it in a later session. |
| `expect_logs` / `log_expectations` / `clear_log_expectations` | "Did the right log messages fire?" — tiles per expected (or forbidden) message, a highlighted live trail, a counts-only verdict. |

The same references are available as MCP resources (`dashr://guide/...`) if
this skill's files are not on disk. Collectors, their metric names and the
system dashboard are in `reference/collectors.md`; discovering and feeding
clouds, clusters and remote hosts is in `reference/environments.md`; database
query performance (top statements, waits, blocking, indexes; RDS through the
AWS CLI, Azure SQL) is in `reference/databases.md`.

## OpenTelemetry sessions and log checks

When `session_info` says `opentelemetry`, the session's own Loki, Tempo and
Prometheus receive whatever is sent to its OTLP endpoint, and `dashr tail --
<command>` ships any command's output as logs. The human's typical ask is
"run this and show me the right messages are logged": arm them with
`expect_logs`, let the code run, then answer from `log_expectations`. Details,
LogQL/TraceQL/PromQL for OTel data and patterns that work are in
`reference/otel-and-logs.md`.

## Choosing panels

| Question | Panel |
|---|---|
| Is it happening right now? One number | `stat` with thresholds |
| How is it trending? Rates, latency, depth | `timeseries` |
| What exactly failed? | `logs` (recent lines) or `table` |
| Which one is worst? Breakdown by service/queue/route | `bargauge` or `table` sorted |
| Is it within limits? | `gauge` with min/max |
| When did state change? | `state-timeline` |
| Context the human needs | `text` (markdown) — short |

## When things go wrong

- **`unknown datasource`**: use a uid from `list_datasources`, never a name.
- **`empty` panel**: the query ran but matched nothing. Widen the time range
  (`"time": {"from": "now-6h", "to": "now"}`), loosen label matchers, check
  the metric/log group name with `probe_query`.
- **`error` panel**: read the masked error. Syntax errors — fix the query
  language. Auth/credentials errors (CloudWatch, SQL) — tell the human; you
  cannot fix credentials. Timeouts — shorten the range or aggregate more.
- **CodePipeline**: if `open_for_pipeline` opened a new tab, a different
  session owns that pipeline; continue there.
