---
name: dtctl
description: Investigate incidents, debug performance issues, analyze logs, and manage observability resources in Dynatrace using the dtctl CLI. Use this skill whenever the user asks about error rates, latency spikes, service health, crash-looping pods, web vitals, SLO status, open problems, root cause analysis, log patterns, trace analysis, or building dashboards — even if they don't mention Dynatrace by name. Also covers DQL queries, workflow management, notebook and dashboard creation, settings configuration, and any operations against a Dynatrace environment.
---

# Dynatrace Control with dtctl

Operate `dtctl`, the kubectl-style CLI for Dynatrace. Pattern: `dtctl <verb> <resource> [flags]`.

## Initialization

Run once to establish context, permissions, and the command catalog:

```bash
dtctl commands                          # compact overview: verbs, resources, subcommands (TOON default)
# dtctl commands --brief                 # + mutating/access/scopes + flag types
# dtctl commands --full                  # exhaustive catalog: descriptions, flag defaults, global flags
dtctl config current-context            # active context
dtctl config describe-context $(dtctl config current-context) --plain  # env URL + safety level
dtctl auth status --plain               # token type (OAuth vs API/platform) + safety level
dtctl inventory                         # what data exists HERE: fetchable objects, buckets, entity census, capabilities
```

Safety levels: `readonly`, `readwrite-mine`, `readwrite-all`, `dangerously-unrestricted`.

`dtctl commands` answers "what can I run?"; `dtctl inventory` answers "what is there to query?" — run it before exploratory DQL. It partitions catalog objects into fetchable vs query-only (never `fetch metrics` or `fetch smartscape.*`), and reports capabilities as present, absent (with the evidence checked — cite it instead of re-probing), or unknown (no verdict; not evidence of absence). Org-specific capability definitions: `--definitions file.yaml`.

Don't use `dtctl auth whoami` to test connectivity — it needs an OAuth token with `app-engine:apps:run` and returns a spurious 403 for plain API or read-scoped tokens even when reads work. Confirm with a real `get`/`query`.

## DQL (required reading)

Before writing, modifying, or running any DQL (`dtctl query`, `dtctl wait query`, query files), consult `references/DQL-reference.md` and follow it over any assumption or memory.

```bash
dtctl query "fetch logs | filter status='ERROR' | limit 100" -o json --plain
dtctl query -f query.dql --set host=h-123 --set timerange=2h -o json --plain   # Go-template vars
dtctl wait query "fetch spans | filter test_id='test-123'" --for=count=1 --timeout 5m
dtctl query "timeseries avg(dt.host.cpu.usage)" -o chart --plain
```

Billable `fetch` (logs, events, bizevents, spans) bills by bytes scanned and dashboard tiles re-bill on every refresh — read "Scan Cost" in `references/DQL-reference.md` before emitting DQL, and treat a PARTIAL or sampled result as incomplete.

dtctl not installed/working? See [references/troubleshooting.md](references/troubleshooting.md).

## Companion skills (Dynatrace for AI)

This skill covers operating dtctl. The [Dynatrace for AI](https://github.com/Dynatrace/dynatrace-for-ai) skill pack adds the domain knowledge: `dt-dql-essentials` (DQL syntax, pitfalls, query optimization), `dt-obs-*` (logs, problems, services, tracing, hosts, kubernetes, frontends, aws/azure/gcp), and `dt-app-dashboards` / `dt-app-notebooks`. When they are loaded, use them for what to query and dtctl to run it. When they are not, tell the user they can add them with `npx skills add dynatrace/dynatrace-for-ai`; don't install them unasked.

## Resources & verbs

Resources and aliases are discoverable via `dtctl commands` (run at init). They include: analyzer, anomaly-detector, app, aws/azure/gcp connection & monitoring, bucket, copilot-skill, dashboard, document, edgeconnect, environment, extension, extension-config, function, group, intent, license, license-settings, lookup, notebook, notification, sdk-version, segment, settings, settings-schema, slo, slo-template, trash, user, workflow, workflow-execution. **Use IDs, not names** — names may be ambiguous and fail.

| Verb | Example |
|------|---------|
| get / describe | `dtctl get workflows --mine` · `dtctl describe workflow <id>` |
| apply / edit / delete | `dtctl apply -f wf.yaml --set env=prod` · `dtctl delete workflow <id>` |
| exec | `dtctl exec function <id> --payload '{...}'` · `dtctl exec analyzer <id> --input '{...}'` (also workflow, copilot) |
| query / wait | `dtctl query "fetch logs \| limit 10"` · `dtctl wait query ... --for=any` |
| inspect | `dtctl inspect <file> --head 20` · `--tail`, `--page --offset N --limit M`, `--fields a,b`, `--schema`, `--stats`, `--sample N`, `--list` (row access over a spilled result file — no Grail re-query) |
| logs / history / restore | `dtctl logs workflow-execution <id>` · `dtctl history dashboard <id>` · `dtctl restore dashboard <id> 3` (version is positional; snapshots exist only if the update passed `--create-snapshot`) |
| share / unshare | `dtctl share dashboard <id> --user a@example.com` |
| find / open | `dtctl find intents --data trace.id=abc` · `dtctl open intent <app/intent> --data k=v` |
| diff / verify | `dtctl diff -f wf.yaml` · `dtctl verify query 'fetch logs' --fail-on-warn` · `dtctl verify analyzer <id> -f in.json` |

Davis analyzers: before running one, `dtctl describe analyzer <id>` shows its required/optional inputs and result schema (add `--doc` for full docs, `-o json` for the raw schemas); `dtctl verify analyzer <id> -f in.json` validates an input without executing (exit 0 valid / 1 invalid).

## Output for agents

`--agent`/`-A` is auto-detected in AI environments (implies `--plain`; opt out with `--no-agent`). It wraps output in `{ok, result, context}` (errors: `{ok:false, error:{code,message}}`, where `context` carries `total`, `has_more`, `suggestions`).

```bash
-o toon          # token-efficient structured output — prefer for agents
-o json|yaml|csv # other machine formats
-o jsonl|parquet # streaming / columnar export for large results (pipe to a file, query with DuckDB)
-o chart|sparkline|barchart   # time series
-o table|wide    # human-readable (table is the default)
--jq '.[].id'    # filter structured output (json|yaml|toon; other formats auto-promote to json)
```

Prefer `--agent` plus `-o toon` and `--jq` to cut tokens. Agent-mode `query` trims metadata to cost/sampling fields by default; `-M=all` for the full block.

### Query results: branch on `result.kind`

In agent mode `dtctl query` defaults to `--spill=auto`: large results spill to a local file and return a summary instead of dumping rows into context. Never assume `result` is an array — branch on `result.kind`:

| `result.kind` | Meaning → action |
|---|---|
| `records` | rows inline under `result.records` → use directly |
| `result-file` | spilled: manifest with `path`, `format`, `rows`, `bytes`, column stats, `sample_rows` → interrogate the file with `dtctl inspect <path>` (below), **don't re-query** |
| `summary-only` | rows couldn't be written — manifest minus `path` → use stats/sample, or follow the cause-aware `context.suggestions` (`--spill=never` + a bound, or `--spill-to <path>`) |

Treat an unknown `kind` as opaque and fall back to `context` (`decided`, `total`, `warnings`, `suggestions`). Sampled results put stats in a `sample_stats` block (`basis: "sample"`) — not population truth.

```bash
dtctl query "fetch logs | limit 1000000" --agent     # auto-spills if large
dtctl query "fetch logs" --spill=never               # force every row inline
dtctl query "fetch logs" --spill-to ./out.jsonl      # explicit path: jsonl|json|csv|parquet
dtctl query "fetch logs" --spill=auto --spill-threshold 100KB
```

Inline results are bounded too. String values are clipped to 500 chars by default and end in `…(+N chars)` (`--max-field-chars 0` gives full values; add `| fields <col>` to fetch only that column). `--max-output-tokens N` / `--max-output-bytes SIZE` returns only the rows that fit. When `context.truncated` is true the result is incomplete: `truncated_fields` lists the clipped fields, and `returned` < `total` means rows were dropped. In that case run `context.next` (a `dtctl inspect` command) to continue at `next_offset` without re-querying.

### Inspect a spilled file (no Grail re-query)

`dtctl inspect <file>` reads the rows the summary left out — bounded, streaming, agent-context-friendly — so you never re-run the Grail scan. Pick exactly one primitive per call:

```bash
dtctl inspect <path> --head 20                          # first N rows (the manifest never carried rows)
dtctl inspect <path> --tail 10                          # last N rows
dtctl inspect <path> --page --offset 1000 --limit 50    # a window deep in the result (file order)
dtctl inspect <path> --head 20 --fields timestamp,content  # project columns (composable)
dtctl inspect <path> --schema                           # re-derive columns + types + null counts
dtctl inspect <path> --stats                            # re-derive the per-column profile (or --stats=col,col)
dtctl inspect --list                                    # lost the path? enumerate spilled files in this context
```

It is not a query engine — no filter/SQL/GROUP BY. For aggregates, push the work back into DQL (`… | summarize …`); for complex local analysis, hand the file to your preferred local analytics tooling. An oversized `inspect` window re-spills to a new file rather than flooding context, and refuses files from another context/tenant.

## Log pattern analysis (token-frugal)

For free-text log triage, don't dump raw `content` — extract the taxonomy server-side, then drill:
1. `dtctl exec analyzer dt.statistics.clustering.LogPatternExtractor --input '{"logQuery":"<DQL>","numberOfExamples":2}'` → DPL templates + match counts. `logQuery` is a **plain DQL string** (not an object) yielding `timestamp`+`content`. Projects well with `--jq` to `{patternExpression, numberOfMatches}`.
2. Lift a `patternExpression` verbatim into `parse content, "..."` (rename captures `f_1`→meaningful), then `summarize … by:{field}` to extract/count at row scale. Unmatched lines yield null captures.
3. Need raw rows? Drill with `fetch … --agent` and let it spill (above), then read them with `dtctl inspect <path> --head/--page` (above).

## Apply & templates

`dtctl apply` is idempotent: POST when new, PUT when the file has an `id`. YAML/DQL files support Go templates filled via `--set`:

```yaml
title: "{{.environment}} Deployment"
cron: "{{.schedule | default "0 0 * * *"}}"
```
`dtctl apply -f file.yaml --set environment=prod --set schedule="0 6 * * *"`

## Dashboards

Create/update: `dtctl apply -f dashboard.yaml`. Export for reference: `dtctl get dashboard <id> -o yaml --plain`. Full schema + visualizationSettings: [references/resources/dashboards.md](references/resources/dashboards.md).

```yaml
name: "Dashboard Name"
type: dashboard
content:
  settings:
    defaultTimeframe: { enabled: true, value: { from: now()-2h, to: now() } }
  layouts:
    "1": { x: 0, "y": 0, w: 12, h: 6 }    # 24-col grid (full=24); quote "y" (YAML bool)
  tiles:
    "1":
      title: "Tile"
      type: data                          # data | markdown
      query: "fetch logs | limit 10"
      visualization: lineChart            # singleValue|lineChart|areaChart|barChart|pieChart|table|honeycomb|scatterplot
      davis: { enabled: false, davisVisualization: { isAvailable: true } }
```

Gotchas: set `davis.enabled: false` on data tiles; `makeTimeseries` for log/span series, `timeseries` for metrics; `id` present → update, absent → create; the `version` warning on create is benign.

## Permissions & safety

- Verify before mutating: `dtctl auth can-i <verb> <resource>`. Scopes: [TOKEN_SCOPES.md](https://github.com/dynatrace-oss/dtctl/blob/main/docs/TOKEN_SCOPES.md).
- Destructive ops may be blocked by safety level — switch with `dtctl config use-context <name>`, or raise the level when creating the context.
- Prefer `get`/`describe` first; `--mine` scopes to resources you own; `--plain` for all machine consumption.

## Credentials & teardown

Credentials are dtctl's business: read and remove them only through dtctl.

```bash
dtctl config delete-context <name> --delete-credentials  # context + its credential
dtctl config delete-credentials <token-ref>              # credential alone (shared, or context already gone)
dtctl auth status --plain                                # presence check — never prints the token
```

**Never invoke OS keychain tooling** — `security` (macOS), `secret-tool`
(Linux), `cmdkey` (Windows) — for any purpose, cleanup included. Their delete
verbs miss most of what a credential occupies; their read verbs print secrets,
and `security dump-keychain` covers *every* keychain on the machine, not just
dtctl's. **Never verify a deletion by reading the secret back** — a teardown
step that prints a token has leaked exactly what it was told to destroy.

## More

[troubleshooting](references/troubleshooting.md) · [multi-tenant config](references/config-management.md) · [DQL](references/DQL-reference.md) · [notebooks](references/resources/notebooks.md) · [extensions](references/resources/extensions.md) · `dtctl --help`, `dtctl <command> --help`
