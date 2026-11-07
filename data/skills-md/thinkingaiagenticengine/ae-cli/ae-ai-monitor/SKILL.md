---
name: ae-ai-monitor
version: 1.1.1
description: "Read AI Monitor traces, conversations, formal Bad Traces, overview and Agent/Tool/Model/Skill metrics, cost, security findings, existing diagnosis and investigation reports. Use for scoped observability queries and verified ZIP exports; never creates or cancels analysis."
metadata:
  requires:
    bins: ["ae-cli"]
---

# AI Monitor Read Workflows

AI Monitor belongs to the Agent component. Local CLI commands and this Skill follow the selected AE environment's Agent availability; an explicitly disabled Agent component hides the commands and removes the CLI-installed Skill. Missing business state retains compatibility with older servers.

Use either installed entrypoint; they share the same `@tant/ae-cli` version, host configuration, and CLI token:

```bash
ae-cli ai-monitor trace list
ai-monitor trace list
```

Authenticate with `ae-cli auth login` before running trace commands. Access is limited to the authenticated user's own company and requires `root` or `monitor_admin`. Do not attempt alternate credentials or scopes after a permission denial.

For an externally provisioned CLI token, both entrypoints accept `--cli-token-file <path>`. The read-only JSON file must contain `url` and `token`; the explicit file takes precedence over environment credentials and stored accounts. If `--host` is supplied, it must match the file's URL. Invalid credentials fail without falling back to another account. Pass only the file path, never the token value, on the command line. Agent runners can use the same internal `--agent-context` argument with either entrypoint; normal queries do not require it.

## Choose the Agent platform and runtime environment

`data-token` is an internal key for an Agent platform/framework instance. `report-source` is an internal key for a runtime/cluster environment. Do not guess either key and do not treat a Report Source as a business-agent filter.

Discover the account's available choices first when the platform or environment is unknown:

```bash
ai-monitor platform list --format json
```

The result contains `platform_name` and nested `environment_name` values. Trace commands accept either these display names or their corresponding IDs:

```bash
ai-monitor trace list --platform "TE Claude Hub" --environment "海外环境"
```

When no scope flags are supplied, the CLI automatically selects the only available platform/environment. If there are multiple choices, stop and use the values returned by `platform list`; do not invent keys. If both `--platform` and `--environment` are already known, pass them directly in the target command; do not run `platform list` first. `--platform` and `--environment` cannot be mixed with the advanced compatibility flags `--data-token` and `--report-source`.

For machine use, successful commands write a JSON envelope to stdout:

```json
{"ok":true,"data":{},"meta":{}}
```

Failures use `{"ok":false,"error":{"type":"...","code":"...","message":"...","hint":"..."},"meta":{}}` and exit nonzero. Keep stdout for JSON only; diagnostics are on stderr. Do not retry 401/403 errors with guessed credentials or another company scope.

## List traces

Start with a bounded list. The CLI discovers the data scope before execution. The default lookback is seven days and the default page size is 20:

```bash
ai-monitor trace list --jq '.items[] | {trace_id, start_time, status}'
```

Use `--start-date YYYY-MM-DD --end-date YYYY-MM-DD` together for an explicit inclusive range. Use `--limit` and `--offset` for pagination. Trace and Conversation lists accept `--sort-by recorded-costs`; recorded amounts sort within fee-unit groups, without summing across currencies. Prefer `--platform` and `--environment`; use `--data-token` and `--report-source` only for backward-compatible, explicitly documented raw keys.

## Get one trace

Copy an exact `trace_id` from list output:

```bash
ai-monitor trace get --trace-id <trace_id> --platform "<same platform>" --environment "<same environment>"
```

Reuse the same scope selected for the list request when more than one platform or environment is available. Do not switch scope while resolving a trace ID.

The response includes snapshot completeness, limitations, trace metadata, and spans. Treat `TRACE_NOT_FOUND_OR_OUT_OF_SCOPE` as either absent or inaccessible; do not infer that a trace exists in another company.

## Count traces

Use `trace count` when only the total is needed. It applies the same scope, date, agent, channel, and search filters as `trace list`, but does not fetch trace rows and has no pagination or sorting options:

```bash
ai-monitor trace count --platform "TE Claude Hub" --environment "海外环境" --last-days 7
```

For identical scope and filters, `data.count` is the same total used by `trace list` as `data.page.total`. Use `--jq '.count'` when an agent needs only the number.

## List and get conversations

Use conversations when the request concerns a multi-turn Agent session rather than one Trace:

```bash
ai-monitor conversation list --platform "TE Claude Hub" --environment "agent007" --last-days 7
ai-monitor conversation get --conversation-id <te_agent_conversation_id> --platform "TE Claude Hub" --environment "agent007"
```

`conversation list` returns each Conversation ID in `data.items[].te_agent_conversation_id`. Pass that exact value to `conversation get --conversation-id`. The detail response returns the selected ID as `data.conversation_id`; list items do not have a `conversation_id` field.

The `--jq` expression runs against `data`, so extract IDs from a bounded list with:

```bash
ai-monitor conversation list --platform "TE Claude Hub" --environment "agent007" --last-days 7 --limit 20 --jq '.items[].te_agent_conversation_id'
```

`conversation list` supports date, Agent, Channel, search, pagination, and sorting options. `conversation get` returns the Trace records belonging to one Conversation. Reuse the same scope when moving from list to get; do not use a Conversation ID as a Trace ID.

## Count conversations

When the user asks only for a conversation count, use the dedicated count command instead of `conversation list --limit 1`. It runs a count-only query, returns no conversation rows, and accepts the same date, Agent, Channel, and search filters:

```bash
ai-monitor conversation count --platform "TE Claude Hub" --environment "agent007" --start-date 2026-09-28 --end-date 2026-09-28 --jq '.count'
```

Always make the scope and date range explicit for a count request when more than one platform/environment is available. Do not retry a successful count by listing rows just to verify the number. A missing scope, 401/403, or 503 is an actionable error; classify it before deciding whether another request is appropriate.

## Output and safety

- Commands are read-only and return structured JSON by default.
- Use `--format table` only for human display and `--jq` for machine selection.
- Keep list calls bounded (`--limit` at most 100) and use `--offset` for additional pages.
- For automation, run `platform list` once per session and pass the returned display name or ID explicitly when more than one choice exists.
- For count-only requests, use `conversation count` or `trace count`; do not infer totals from a paginated list.
- Keep the same platform/environment across related list, count, and get calls, and include the effective date range in the response.
- Never place `cli-token` in command flags or output.
- `__default__` is a real Report Source value, not a wildcard.

## Advanced filters and formal Bad Traces

`trace list/count` and `conversation list/count` also accept `--status`, `--user-cancelled true|false`, `--filter-groups` JSON, and `--quality-flags` JSON. List and count use the same filters. Filters combine with AND; a page filter tree can express nested AND/OR. Conversation filters select Trace rows before aggregating them, so its totals describe the matching Trace subset. See the [complete command reference](references/read-commands.md) for field names and operators.

```bash
ai-monitor trace count --platform "<platform>" --environment "<environment>" --status STATUS_CODE_ERROR --user-cancelled false --start-date 2026-11-03 --end-date 2026-11-03
ai-monitor bad-trace list --platform "<platform>" --environment "<environment>" --quality-flags '["l2_infra_instant_death"]' --start-date 2026-11-03 --end-date 2026-11-03 --limit 10
ai-monitor bad-trace get --platform "<platform>" --environment "<environment>" --trace-id <trace_id>
```

Bad Trace queries use the formal warehouse tags and observation date (`pd`). Their date is not Trace start time. `l2_infra_instant_death` is the product's startup-failure indicator, not a confirmed root cause. Do not infer startup failure from any error, abort text, or error Span. Explicit user cancellation is a separate classification based on the product's specific user-cancellation message. Successful final status can coexist with failed intermediate Spans.

Trace quality has `available`, `availability` (`available`, `not_found`, or `unavailable`), `flags`, `matched_flags`, `evidence`, and `stats_date`. Neither `not_found` nor `unavailable`, nor a null flag, proves that a tag is false. Without `--quality-flags`, a failed quality-metadata lookup can return the same base data with `QUALITY_METADATA_UNAVAILABLE` in limitations; a Trace snapshot is then `PARTIAL`. When `--quality-flags` is supplied, the query cannot fall back to unfiltered base data and fails if formal quality metadata is unavailable. Preserve completeness, coverage, warnings, and limitations when explaining results. Trace summary Span counts exclude the Agent root while the detail Span array includes it.

## Overview, execution, cost and security

Use scoped read commands to move from overview to exact observed entities. Copy IDs and names from responses; keep the same scope.

```bash
ai-monitor overview get --platform "<platform>" --environment "<environment>" --last-days 7
ai-monitor agent get --platform "<platform>" --environment "<environment>" --agent "<agent name>" --last-days 7
ai-monitor tool calls --platform "<platform>" --environment "<environment>" --tool-name "<tool name>" --last-days 7 --limit 10
ai-monitor model list --platform "<platform>" --environment "<environment>" --has-issue true --limit 10
ai-monitor skill traces --platform "<platform>" --environment "<environment>" --skill-name "<skill name>" --last-days 7 --limit 10
ai-monitor cost actual-summary --platform "<platform>" --environment "<environment>" --start 2026-11-01 --end 2026-11-04
ai-monitor security issues --platform "<platform>" --environment "<environment>" --decision pending --limit 10
```

Cost intervals are **[start, end)**, at most 90 days; Token totals and recorded monetary amounts are different measures. Preserve monetary units, decimal strings, coverage and unavailable states. `cost report-list` uses inclusive `--period-start/--period-end` to filter existing reports instead. `model list` is the latest snapshot and has no date flags. Security list commands use the exact response cursor fields; do not invent timestamps or mix cursor pairs. Security reads do not review issues, modify rules, or create audit tasks.

## Existing diagnosis and investigation tasks

```bash
ai-monitor diagnosis queue --platform "<platform>" --environment "<environment>" --limit 20
ai-monitor diagnosis list --platform "<platform>" --environment "<environment>" --entity-type trace --entity-key <trace_id>
ai-monitor diagnosis get --platform "<platform>" --environment "<environment>" --task-id <task_id>
ai-monitor diagnosis report --platform "<platform>" --environment "<environment>" --entity-type conversation --entity-key <conversation_id>
ai-monitor investigation modes --platform "<platform>" --environment "<environment>" --entity-type trace
ai-monitor investigation list --platform "<platform>" --environment "<environment>" --analysis-mode bad_case_commonality --limit 20
ai-monitor investigation run-get --platform "<platform>" --environment "<environment>" --case-id <case_id> --run-id <run_id>
```

These commands read existing state and results. They never create, retry, or cancel a diagnosis. Read `diagnosis get` again only when checking an active task; queued/running is not success, and failed/skipped/cancelled is not an empty report. Investigation cases have multiple runs; use the exact run ID for result/status correlation. A completed run may still return partial evidence or limitations. Bad Case commonality uses human-selected Bad/Good samples; it is distinct from formal Bad Trace classification.

## Conversation spans and ZIP exports

```bash
ai-monitor conversation get --conversation-id <conversation_id> --platform "<platform>" --environment "<environment>" --include-spans --span-limit 20 --span-offset 0
ai-monitor trace export --platform "<platform>" --environment "<environment>" --trace-ids '["<trace_id>"]' --output ./traces.zip
ai-monitor conversation export --platform "<platform>" --environment "<environment>" --conversation-ids '["<conversation_id>"]' --output ./conversations.zip
```

Conversation detail retains `items` and `total`; opt-in spans add `trace_snapshots`, `trace_failures`, `spans_page`, `spans_completeness`, and `spans_limitations`. Pagination can mean PARTIAL/PAGINATED even without query failures. Use the next span offset or bounded ZIP export for more data.

Exports accept at most 100 Trace IDs or 20 Conversation IDs (at most 200 Traces per conversation batch). Choose a new local `--output` path. The CLI checks byte length and SHA-256, writes with mode 0600, refuses existing files/symlinks, and prints only file metadata and the manifest. Check partial failures in the manifest even after exit 0. `--validate` and `--dry-run` do not create a file; they are alternative prechecks, not steps to call together. Use smaller batches when backend limits or upstream timeouts are reached.

All 64 command paths, parameters, defaults and capability mappings are in the [read command reference](references/read-commands.md). This extends the existing `ae-ai-monitor` Skill and retains both CLI entrypoints.
