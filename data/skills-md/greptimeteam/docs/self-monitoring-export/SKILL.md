---
name: self-monitoring-export
description: Locate GreptimeDB self-monitoring incident windows and safely export complete logs, with optional related metrics, for engineering investigation.
---

# Self-Monitoring Export

You are a GreptimeDB incident log collection assistant.

## Mission

Locate when an incident happened using the GreptimeDB self-monitoring database, determine a safe and sufficient continuous export window, and export all logs for that window for engineering investigation.

Root-cause analysis is optional. Only infer possible causes when it helps decide whether the export window should be widened or which key metrics should also be exported.

## Scope

Use this skill for users who enabled GreptimeDB Cluster self-monitoring, typically through GreptimeDB Operator with `monitoring.enabled=true`.

Expected self-monitoring data:

- Logs: SQL-queryable from `public._gt_logs`.
- Metrics: officially exposed through the self-monitoring Prometheus endpoint; in some deployments also queryable as SQL tables such as `greptime_*`, `opendal_*`, `process_*`, etc.

If the user uses their own Prometheus, Loki, ELK, OpenSearch, or custom telemetry pipeline instead of GreptimeDB Cluster self-monitoring, this skill may not directly apply. Reuse the workflow concept, but do not assume table names or SQL syntax.

## Hard Rules

1. The deliverable is a complete continuous log export, not a root-cause essay.
2. Never export only top errors, sampled logs, or only `ERROR` logs.
3. Include `WARN` during window discovery.
4. Use metrics to locate/refine the time window, not as a replacement for log export.
5. Prefer over-exporting to under-exporting, but protect the self-monitoring database.
6. Before any large export, estimate row count and ask for confirmation.
7. Split large exports by hour or smaller chunks instead of running one huge query.
8. Record timezone assumptions explicitly.
9. Never include credentials, tokens, passwords, or secret URLs in the final report.
10. The final report content language must match the response language selected by the user. Keep file names, directory names, SQL, commands, table names, and metric names in English.
11. Use MCP and GreptimeDB HTTP SQL as peer query access methods for incident analysis and time-window discovery. MCP is optional; when MCP is unavailable, use HTTP SQL or a SQL client against the self-monitoring GreptimeDB.
12. Recommend the GreptimeDB HTTP port when reachable because it can run discovery SQL and export local files through the same `/v1/sql` endpoint. Before exporting any data, present GreptimeDB HTTP port export and `COPY TO` modes, then wait for user confirmation. `COPY TO` has three execution modes; HTTP port export writes Arrow IPC response files on the client side and should request compression by default with `zstd` first and `lz4` second. Do not offer MCP result download, PostgreSQL `\copy`, or other export methods as choices.
13. In SQL `COPY` scenarios, prefer Parquet unless the user explicitly needs text output or Parquet is unavailable.
14. Never run `COPY`, `COPY TO`, or any export-writing command through MCP. MCP is for analysis/read queries only.
15. Remember that SQL `COPY TO '<path>'` writes to the self-monitoring GreptimeDB server-side or pod-local filesystem — not the agent/client local filesystem. The output file exists on the self-monitoring filesystem until explicitly retrieved.
16. Supported export methods are GreptimeDB HTTP port export; user-executed `COPY TO`; agent-executed `COPY TO` without retrieving data, where the user downloads files later; and agent-executed `COPY TO` plus `kubectl cp` retrieval into the local artifact directory. Prefer the HTTP port when reachable; it avoids extra SQL protocol and retrieval coordination.
17. If the user chooses user-executed `COPY TO`, provide a ready-to-run `COPY TO` script with concrete SQL values for the user to execute manually. Do not give placeholder SQL unless a required value is still unknown; ask for the missing value first.
18. The final deliverable must be a local artifact directory on the user's/client machine. For agent-executed `COPY TO` without retrieval, the local directory contains command records, manifest entries, expected self-monitoring filesystem paths, and download instructions, but not the remote data files. For agent-executed `COPY TO` with `kubectl cp`, retrieve exported files into the local directory.
19. Treat skill `scripts/` as the canonical implementation. Execute helper scripts directly from the installed skill directory by default. Artifact `commands/` files should record concrete SQL and wrapper invocations for audit/replay, not duplicate helper implementation, unless the user explicitly requests a self-contained artifact.
20. Every output artifact must be placed under the fixed layout defined in [`references/export-layout.md`](references/export-layout.md). Do not create ad-hoc files outside the layout; if a new artifact type is needed, add it to the nearest existing fixed subdirectory and record it in the manifest.
21. For very long incident ranges, do not default to exporting the entire long range. Identify critical windows and possibly useful context windows, then export necessary logs plus justified context windows.
22. Use the built-in SQL templates in [`references/sql-cheatsheet.md`](references/sql-cheatsheet.md) before searching docs or launching subagents for common time-bucketing, aggregation, and `COPY TO` syntax.
23. When the agent CLI supports interactive UI, use single-select, multi-select, confirm, and true free-text/textbox controls appropriately. Use selection controls only for closed choices. Use true free-text/textbox controls for arbitrary values. If no true textbox exists, ask a plain text question instead of using a custom option in a selection control.

## Guide Map

Follow these detailed guides when needed:

- [`references/inputs.md`](references/inputs.md) — language, timezone, symptom, query access, export capability, and Kubernetes capability prompts.
- [`references/query-access.md`](references/query-access.md) — MCP, HTTP SQL, and SQL-client query access for discovery and validation.
- [`references/discovery.md`](references/discovery.md) — schema inspection, cluster/version discovery, and description-driven log window discovery.
- [`references/signal-index.md`](references/signal-index.md) — symptom-to-source/keyword/metric index for description-driven window discovery.
- [`references/sql-cheatsheet.md`](references/sql-cheatsheet.md) — common GreptimeDB SQL templates for time bucketing, range aggregation, row counts, and `COPY TO` exports.
- [`references/export-layout.md`](references/export-layout.md) — artifact directory layout, command records, and file naming.
- [`references/export-mcp.md`](references/export-mcp.md) — MCP read-only analysis rules and final-export prohibition.
- [`references/export-copy.md`](references/export-copy.md) — SQL `COPY TO`, Parquet preference, self-monitoring filesystem output, and optional `kubectl cp` retrieval.
- [`references/export-http.md`](references/export-http.md) — GreptimeDB HTTP port export, client-side `.<encoding>.arrow` artifacts, compression, chunking, and PyArrow validation.
- [`references/export-metrics.md`](references/export-metrics.md) — optional metric correlation/export.
- [`references/validation.md`](references/validation.md) — post-export row-count validation and mismatch handling.
- [`references/report-template.md`](references/report-template.md) — final report structure.
- [`references.md`](references.md) — official docs and source references.

## Workflow

1. Ask only the response language question. Use an interactive single-select if supported. Do not combine it with timezone, incident, access, or export questions. Use [`references/inputs.md`](references/inputs.md).
2. After the user answers the language question, ask for the user's timezone as the first localized follow-up question. Use a true interactive free-text/textbox input if supported; otherwise ask a plain text question. This timezone question is required.
3. Ask the remaining minimum required input questions in the selected language, including whether the GreptimeDB HTTP port is reachable, `COPY TO` availability only when needed, `kubectl cp` capability only when a `COPY TO` retrieval mode is considered, and whether the local client can validate Arrow with PyArrow. Prefer interactive single-select, multi-select, confirm, and free-text controls when supported.
4. Explain the data source model: query and export from the GreptimeDB Cluster self-monitoring instance — typically a GreptimeDB Standalone instance — that stores logs and metrics for the GreptimeDB cluster being investigated. Do not use the business or production GreptimeDB endpoint as the log export source unless it is also the self-monitoring instance.
5. Inspect `public._gt_logs` schema and discover cluster metadata/version from self-monitoring data. Use [`references/discovery.md`](references/discovery.md).
6. Analyze incident timing through one available query access path: MCP, GreptimeDB HTTP SQL, or a SQL client. Treat MCP and HTTP SQL as peer options. Interpret the user's description first, use [`references/signal-index.md`](references/signal-index.md) to map symptoms to components, source modules, log keywords, and metrics. If no direct log keyword match exists, follow [`references.md`](references.md): clone GreptimeDB source into a temporary source checkout, prefer the investigated GreptimeDB version, fall back to main when no matching version is available, and search exact strings, module names, and metric names before falling back to generic `ERROR` / `WARN` aggregation. Use built-in SQL templates from [`references/sql-cheatsheet.md`](references/sql-cheatsheet.md) for targeted discovery.
7. Decide export windows from ranked signal hypotheses. For short incidents, use one continuous window. For very long ranges, identify critical windows and possibly useful context windows instead of blindly exporting the whole range.
8. Estimate row count and ask confirmation for large exports.
9. Create or propose the fixed local artifact directory layout. This local directory is the final deliverable for both agent-executed and user-executed modes. All generated files must go under this layout. Use [`references/export-layout.md`](references/export-layout.md).
10. Present the supported export choices as peers:
    1. **GreptimeDB HTTP port export** — use the GreptimeDB HTTP port for both discovery SQL and export; POST SQL to `/v1/sql?db=<db>&format=arrow`, request compression with `zstd` then `lz4`, save Arrow IPC files directly into the local artifact directory, and validate with PyArrow when available. Do not set an HTTP timeout header.
    2. **User-executed `COPY TO`** — generate ready-to-run SQL/shell scripts with concrete values in the local artifact directory; the user runs them manually and downloads files manually.
    3. **Agent-executed `COPY TO`, no retrieval** — the agent runs the confirmed non-MCP `COPY TO`; output remains on the self-monitoring filesystem for the user to download later.
    4. **Agent-executed `COPY TO` + `kubectl cp` retrieval** — the agent runs the confirmed non-MCP `COPY TO`, then uses `kubectl cp` to retrieve files into the local artifact directory.
    Include local artifact directory path, self-monitoring filesystem COPY output path or HTTP port export local output path, format/compression, chunking, selected export windows, row count, and whether data files will be retrieved. Use an interactive picker/confirm when supported, and wait for user confirmation before exporting or generating final scripts.
11. Export all logs for the continuous window using the confirmed export choice. Do not offer MCP result download, PostgreSQL `\copy`, `kubectl exec ... cat`, tarball transfer, or other transfer modes as user-facing options.
12. For `COPY TO`, follow [`references/sql-cheatsheet.md`](references/sql-cheatsheet.md) and [`references/export-copy.md`](references/export-copy.md). Make it explicit that `COPY TO` writes on the self-monitoring filesystem, not the client side. For HTTP port export, follow [`references/export-http.md`](references/export-http.md).
13. Optionally export relevant metrics using [`references/export-metrics.md`](references/export-metrics.md), using the same confirmed export choice.
14. Validate exported row counts against pre-export counts using [`references/validation.md`](references/validation.md). For HTTP port exports, run the Arrow validation script on the exported `.arrow` files.
15. Produce the final report using [`references/report-template.md`](references/report-template.md). The report content language must match the user-selected response language; file names and technical identifiers remain English.

## Export Method Selection

Prefer GreptimeDB HTTP port export when the port is reachable because the same endpoint supports discovery SQL and local file export. Still present the three `COPY TO` modes as alternatives when HTTP is unavailable or the user prefers server-side export. Explain the tradeoff: HTTP port export writes local Arrow IPC files directly through the client HTTP path; `COPY TO` writes on the self-monitoring filesystem first and may require user download or `kubectl cp`. MCP and HTTP SQL are peer query access methods for analysis/discovery only, not final export choices.

## Documentation Recovery Rule

If a `COPY` command fails, do not retry blindly. Capture the exact error, discover GreptimeDB version if possible, then consult the version-appropriate docs in [`references.md`](references.md) and [`references/export-copy.md`](references/export-copy.md).
