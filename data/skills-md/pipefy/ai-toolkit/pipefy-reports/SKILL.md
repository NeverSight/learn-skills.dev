---
name: pipefy-reports
description: >
  Use this skill when the user wants to create, read, update, delete, or
  export pipe reports or organization reports. Covers the async export
  workflow (trigger, poll, download). 17 MCP tools.
tags: [pipefy, reports, exports, pipe-reports, organization-reports]
---

# Reports

Pipe reports and organization reports: discovery, CRUD, and async exports. **17 MCP tools.**

---

## Cross-cutting patterns

- Build `ReportCardsFilter` using `get_pipe_report_columns` and `get_pipe_report_filterable_fields`; use `introspect_type` for uncommon inputs.
- `get_pipe_reports` omits `cardCount` in the query (Pipefy can error when resolving it).
- `debug=true` on writes like other mutation tools.

---

## Pipe report tools

| Tool (MCP) | CLI | Read-only | Purpose |
|------------|-----|-----------|---------|
| `get_pipe_reports` | `pipefy report-pipe list` | Yes | List all reports for a pipe. |
| `get_pipe_report` | `pipefy report-pipe get` | Yes | Single report data. |
| `get_pipe_report_columns` | `pipefy report-pipe columns` | Yes | Discover available columns for a report filter. |
| `get_pipe_report_filterable_fields` | `pipefy report-pipe filterable-fields` | Yes | Discover filterable fields for a report. |
| `create_pipe_report` | `pipefy report-pipe create` | No | Create a new pipe report. |
| `update_pipe_report` | `pipefy report-pipe update` | No | Update report name or filters. |
| `delete_pipe_report` | `pipefy report-pipe delete` | No | **Two-step destructive.**[^mcp-confirm] |
| `export_pipe_report` | `pipefy report-pipe export` | No | Trigger async export. |

## Organization report tools

| Tool (MCP) | CLI | Read-only | Purpose |
|------------|-----|-----------|---------|
| `get_organization_reports` | `pipefy report-org list` | Yes | List all org-level reports. |
| `get_organization_report` | `pipefy report-org get` | Yes | Single org report data. |
| `create_organization_report` | `pipefy report-org create` | No | Create an org-wide report. |
| `update_organization_report` | `pipefy report-org update` | No | Update report config. |
| `delete_organization_report` | `pipefy report-org delete` | No | **Two-step destructive.**[^mcp-confirm] |
| `export_organization_report` | `pipefy report-org export` | No | Trigger async export. |

[^mcp-confirm]: MCP two-step: echo `confirmation_token` from the preview with `confirm=true`. CLI: `--yes`.

## Export status & download

| Tool (MCP) | CLI | Purpose |
|------------|-----|---------|
| `get_pipe_report_export` | poll via `pipefy report-pipe export --format json` | Poll pipe report export status (after `export_pipe_report`). |
| `get_organization_report_export` | poll via `pipefy report-org export --format json` | Poll org report export status (after `export_organization_report`). |
| `export_pipe_audit_logs` | `pipefy audit export` | Export pipe audit logs (separate from card report exports). |

---

## Steps — export a pipe report

1. **List available reports:**

   MCP: `get_pipe_reports pipe_id=67890`

2. **Trigger the export:**

   MCP: `export_pipe_report report_id=123`

3. **Poll until finished:**

   MCP: `get_pipe_report_export export_id=<EXPORT_ID>`

   Repeat every 5–10 seconds until the response indicates `finished` (or `failed`).

4. **Download:** use the signed `fileUrl` from the finished export response over HTTPS (the MCP tool surfaces it in the payload).

---

## Steps — create a filtered pipe report

1. **Discover filterable fields:**

   MCP: `get_pipe_report_filterable_fields pipe_id=67890`

2. **Create the report with a `ReportCardsFilter` shape** (not a top-level `current_phase` array):

   MCP:
   ```
   create_pipe_report pipe_id=67890 name="Phase subset" filter='{"operator":"and","queries":[{"field":"current_phase","operator":"eq","type":"select","value":"<phase_id>"}]}'
   ```

   Use the exact `field` string from step 1. Invalid shapes are rejected before GraphQL with a message pointing at `get_pipe_report_filterable_fields`.

---

## Success criteria

- `get_pipe_report_export` (or `get_organization_report_export`) reaches a terminal `finished` or `failed` state.
- Downloaded export contains the expected card/report data.

## Failure modes

- **Export stuck in `processing`:** large pipes with many cards can take minutes. Wait at least 60 seconds per poll. Retry the export trigger if still `processing` after several minutes.
- **`get_pipe_reports` returns `null` for `cardCount`:** known Pipefy API behavior; the tool omits that field automatically.
- **Filter rejected before GraphQL:** do not pass `{"current_phase":["id"]}`; use `operator` + `queries` (see step 2 above).
- **Filter not working after create:** use `get_pipe_report_filterable_fields` to confirm the exact `field` string and `value` format.

## See also

- `skills/observability/` — export automation job history (different from pipe reports).
- `skills/introspection/` — discover `ReportCardsFilter` input shape for complex filters.
