---
name: ascn-operator
version: 0.0.4
owner: platform-ai
maturity: beta
description: Workflow and tool-export operator for ASCN workspace MCP control tools.
---

# ASCN Operator

Operate ASCN workflows using MCP `control.*` tools with deterministic, auditable outcomes.

## When To Use

Use this skill for:

1. workflow lifecycle changes (`create|repair|patch|export|delete`)
2. plugin publication (`publish_plugin`)
3. operator diagnostics (`explain`)

Do not use this skill to design brand-new handlers/triggers. Delegate that to `ascn-integrations`.

## Required Inputs

The operator MUST collect:

1. `intent` (`create|repair|patch|export|publish_plugin|delete|explain`)

Intent-specific required inputs:

1. `workflow_id` for `patch|repair|export|delete`
2. `plugin_name` and `handlers[]` for `publish_plugin`
3. `publish_plugin` handlers MUST be user-defined and match `User.<Handler>`

Recommended inputs:

1. success criteria (expected tool name, run status, or plugin visibility)
2. `blueprint_preference` (`linear|fanout|conditional|retryable_http|tool_export`)
3. constraints (`latency_slo_ms`, `throughput_rps`, `idempotency_requirement`)

If required inputs are missing, stop and return `input_validation_error`.

Workspace scope MUST come from runtime authorization/session context (for example MCP `/mcp` bearer-token resolution), not from manual user-provided `workspace_id` input.

If workspace context is missing, stop and return `input_validation_error`.

## Dependency And Discovery Policy

At task start, the operator MUST run:

1. `control.docs.get`
2. tool discovery check for required surface:
   - `control.registry.list`
   - `control.registry.details`
   - `control.registry.resolve_options`
   - `control.workflows.list`
   - `control.workflows.describe`
   - `control.workflows.validate`
   - `control.workflows.create`
   - `control.workflows.patch`
   - `control.workflows.activate`
   - `control.workflows.delete`
   - `control.tools.list_exports`
   - `control.tools.ensure_export`
   - `control.runs.list`
   - `control.runs.details`
   - `control.plugins.create_plugin`
   - `control.plugins.validate_definition`
   - `control.plugins.update_plugin`
   - `control.plugins.get`
   - `control.plugins.list`

Connectivity defaults (use as hints, not hard requirements):

1. transport: `streamable_http`
2. dependency id: `workspace-mcp-gateway`
3. URL hint: `https://nocode.ascn.ai/mcp`
4. secret hint: `mcp_gateway_token`

If discovery fails, do not mutate. Return `dependency_failure` with missing tools and connection hints.

## Capability Gap Policy

After dependency checks, classify capability in this order:

1. inspect workflows/exports (`control.workflows.list`, `control.workflows.describe`, `control.tools.list_exports`)
2. inspect handlers/triggers (`control.registry.list`, `control.registry.details`)
3. classify as one of:
   - `sufficient`
   - `missing_handler`
   - `missing_trigger`
   - `missing_auth_capability`
   - `schema_or_contract_gap`

If not `sufficient`, the operator MUST NOT invent handler names. It MUST pause mutations and delegate to `skills/ascn-integrations/SKILL.md`.

## Blueprint Selection

For `create|patch|repair|export`, choose exactly one:

1. `linear`
2. `fanout`
3. `conditional`
4. `retryable_http`
5. `tool_export`

Then enforce topology consistency with the selected blueprint.

## Execution Flow

Common authoring pipeline:

1. select blueprint
2. schema-lock from `control.registry.details` (required fields, defaults, secret-backed fields)
3. build minimal valid draft
4. run reference safety gate:
   - every `$node[...]` has a reachable path
   - no raw `$...` directive without `={{ ... }}`
   - no secret literals
5. validate (`control.workflows.validate`)
   - payload MUST be wrapped as `{ "workflow": { ... } }`
6. mutate (`create` or `patch`)
7. activate (`control.workflows.activate`)
8. expand only when required by scope

Intent call order:

`create`
1. `control.workflows.list`
2. `control.registry.list`
3. `control.registry.details`
4. authoring pipeline with `create`

`patch|repair`
1. `control.workflows.list`
2. `control.workflows.describe`
3. `control.registry.details`
4. authoring pipeline with `patch`

`export`
1. `control.workflows.describe`
2. `control.tools.list_exports` with `expose_mcp_only=false`
3. `control.tools.ensure_export` (must include `output_path`)
4. `control.workflows.validate`
   - payload MUST be wrapped as `{ "workflow": { ... } }`
5. `control.workflows.activate`
6. smoke invoke exported tool with minimal payload
7. `control.runs.list`
8. `control.runs.details` on failure/unexpected status

`publish_plugin`
1. validate every handler matches `User.<Handler>`; reject system handlers (for example `Telegram.*`)
2. `control.registry.details` for each handler
3. collect existing plugin examples using `control.plugins.list` with `include_definition=true` (never query DB directly)
4. use `control.plugins.get` for deterministic single-definition reads when a `definition_id` already exists
5. for fields with `options_source`, resolve via `control.registry.resolve_options`
6. when editing `params_ui`, apply conditional patterns and validation checklist from `skills/ascn-integrations/SKILL.md` (`Conditional UI Recipes`, `Conditional UI Validation Checklist`)
7. preflight with `control.plugins.validate_definition`
8. `control.plugins.create_plugin`
9. optional `control.plugins.update_plugin`
10. `control.plugins.list` verify plugin is visible

`delete`
1. `control.workflows.describe`
2. summarize destructive impact
3. `control.workflows.delete` with `confirm=true`

## Authoring Standards

1. Activity IDs MUST be unique.
2. Every `edges[].to` MUST reference an existing activity.
3. Trigger entry edges SHOULD be explicit for clear starts.
4. `$json` MUST be used only for current node input.
5. Upstream reads MUST use `$node['id'].json.field` with graph reachability.
6. Dynamic expressions and secrets MUST use `={{ ... }}`.
7. Credentials MUST NOT be hardcoded.

## Retry And Stop Rules

1. Operation key format: `{workspace_id}:{intent}:{workflow_id|workflow_name}:{payload_hash}`
2. Retry only transient failures (`timeout`, `5xx`, transport unavailable), max 3 attempts with exponential backoff.
3. Never auto-retry validation, schema, or export-conflict errors.
4. Never delete without explicit `confirm=true`.
5. Never mutate when dependency checks fail.

## Output Contract

Every completion MUST return:

```json
{
  "intent": "create|repair|patch|export|publish_plugin|delete|explain",
  "workspace_id": "uuid",
  "workflow_id": "uuid-or-null",
  "selected_blueprint": "linear|fanout|conditional|retryable_http|tool_export|null",
  "capability_status": "sufficient|missing_handler|missing_trigger|missing_auth_capability|schema_or_contract_gap",
  "actions": [
    {
      "step": "string",
      "tool": "control.*",
      "status": "completed|skipped|failed"
    }
  ],
  "validation": {
    "validated": true,
    "activated": true
  },
  "verification": {
    "smoke_tested": true,
    "latest_run_status": "COMPLETED|FAILED|RUNNING|UNKNOWN",
    "run_id": "string-or-null",
    "trace_id": "string-or-null"
  },
  "plugin": {
    "plugin_name": "string-or-null",
    "visible_in_plugins_list": true
  },
  "failure": {
    "class": "none|input_validation_error|dependency_failure|validation_failure|runtime_failure|capability_gap",
    "message": "string"
  },
  "next_action": "string"
}
```
