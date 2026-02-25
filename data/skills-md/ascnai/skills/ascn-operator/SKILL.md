---
name: ascn-operator
version: 0.0.2
owner: platform-ai
maturity: beta
description: Workflow lifecycle and tool-export operator for ASCN workspace MCP control tools.
---

# ASCN Operator

Use this guide as the source of truth for how the operator should work.

## Mission

Use workspace MCP `control.*` tools to safely discover, validate, change, activate, and export workflows, plus submit plugin bundles with clear, auditable outcomes.

## Required Inputs

The operator MUST obtain:

1. `workspace_id` (UUID)
2. `intent` (`create|repair|patch|export|publish_plugin|delete|explain`)

Optional but strongly recommended:

1. `workflow_id` for patch/repair/export/delete intents
2. required integration list and secrets map
3. success criteria (expected workflow status/tool name)
4. for `publish_plugin`: `plugin_name`, canonical handler list, and plugin definition metadata
5. `blueprint_preference` (`linear|fanout|conditional|retryable_http|tool_export`)
6. latency target (for example `latency_slo_ms`)
7. throughput target (for example `throughput_rps`)
8. idempotency requirement (`strict|best_effort`)

If `workspace_id` is missing, the operator MUST stop before any mutation.

## Required Tool Surface

The target gateway MUST expose these tools:

1. `control.docs.get`
2. `control.registry.list`
3. `control.registry.details`
4. `control.workflows.list`
5. `control.workflows.describe`
6. `control.workflows.validate`
7. `control.workflows.create`
8. `control.workflows.patch`
9. `control.workflows.activate`
10. `control.workflows.delete`
11. `control.tools.list_exports`
12. `control.tools.ensure_export`
13. `control.runs.list`
14. `control.runs.details`
15. `control.plugins.create_plugin`
16. `control.plugins.update_plugin`
17. `control.plugins.list`

If required tools are unavailable, the operator MUST fail fast with a dependency error summary.

## Companion Skill Delegation

If capability is insufficient, the operator MUST delegate integration design/implementation to:

1. `skills/ascn-integrations/SKILL.md`

The operator MUST resume lifecycle mutations only after missing capability becomes available.

## Connectivity Prerequisites

Before lifecycle operations, the operator MUST verify MCP connectivity for the workspace gateway.

Required gateway configuration:

1. transport: `streamable_http`
2. URL: `https://nocode.ascn.ai/mcp`
3. tool dependency id: `workspace-mcp-gateway`
4. workspace secret name: `mcp_gateway_token`
5. auth header: `Authorization: Bearer <token>` (must match secret value)
6. MCP auth/token source: `https://ascn.ai/no-code/mcp-list`

The operator MUST NOT attempt workflow mutations until this dependency is reachable.

## Dependency Handshake

At task start, the operator MUST perform a dependency readiness check:

1. confirm `workspace_id` is present
2. confirm MCP gateway dependency exists in agent runtime
3. confirm control tool surface is discoverable

If any check fails, classify as dependency failure and return user-facing connection instructions.

## Capability Gap Policy

After dependency checks, the operator MUST determine whether current capability is sufficient.

Required detection order:

1. inspect workflow/tool inventory (`control.workflows.list`, `control.workflows.describe`, `control.tools.list_exports`)
2. inspect handler/trigger inventory (`control.registry.list`, `control.registry.details`)
3. classify capability status:
   - sufficient
   - missing_handler
   - missing_trigger
   - missing_auth_capability
   - schema_or_contract_gap

If status is not `sufficient`, the operator MUST NOT invent handler/trigger names.

## Blueprint Selector Policy

For `create|patch|repair|export`, the operator MUST select one workflow blueprint before drafting config.

Supported blueprint types:

1. `linear`: single ordered chain
2. `fanout`: one producer, multiple parallel consumers
3. `conditional`: explicit branch routing with conditions
4. `retryable_http`: network call with explicit retry/error path
5. `tool_export`: `Trigger.Tool` surfaced via MCP

The operator MUST:

1. declare selected blueprint in output (`selected_blueprint`)
2. keep graph topology consistent with selected blueprint
3. use `control.registry.details` examples/minimal params as activity-level examples

## Execution Policy

### Global Rules

1. The operator MUST call `control.docs.get` before intent-specific mutations.
2. The operator MUST validate before every create/patch mutation.
3. The operator MUST mutate by `workflow_id`, never inferred names.
4. The operator MUST not perform delete without explicit `confirm=true`.
5. The operator MUST run `control.workflows.activate` after successful create/patch/export.
6. For exported MCP tools, the operator MUST run smoke-test trace checks using `control.runs.list`.
7. The operator MUST use a minimal-valid first draft, then expand.
8. The operator MUST complete schema-lock and reference-safety checks before mutation.
9. The operator MUST use a consistent node naming convention.
10. The operator MUST prepare patch strategy from error class before retrying failed validation.

### Authoring Pipeline (Required)

For `create|patch|repair|export`, operator MUST apply this order:

1. select blueprint type
2. schema-lock from `control.registry.details`:
   - required params
   - defaults
   - secret-backed fields
3. build minimal valid draft:
   - smallest runnable set of nodes
   - explicit trigger entry edge(s)
4. run reference safety gate:
   - each `$node[...]` has reachable directed path
   - no raw `$...` dynamic directives without `={{ ... }}`
   - no secret literals
5. validate (`control.workflows.validate`)
6. mutate (`create` or `patch`)
7. activate
8. expand/iterate only if required by scope

### Intent Flows

`create`

1. `control.docs.get`
2. `control.workflows.list`
3. `control.registry.list`
4. `control.registry.details`
5. select blueprint + schema-lock + minimal valid draft
6. `control.workflows.validate`
7. `control.workflows.create`
8. `control.workflows.activate`

`patch|repair`

1. `control.docs.get`
2. `control.workflows.list`
3. `control.workflows.describe`
4. `control.registry.details`
5. select blueprint + schema-lock + minimal patch draft
6. `control.workflows.validate`
7. `control.workflows.patch`
8. `control.workflows.activate`

`export`

1. `control.docs.get`
2. `control.workflows.describe`
3. `control.tools.list_exports` with `expose_mcp_only=false` to inspect all exports
4. `control.tools.ensure_export` with canonical `output_path`
5. `control.workflows.validate`
6. `control.workflows.activate`
7. invoke exported tool with minimal valid payload
8. `control.runs.list` for latest run verification
9. `control.runs.details` for node outputs and timeline diagnostics

`delete`

1. `control.workflows.describe`
2. summarize destructive impact
3. `control.workflows.delete` with `confirm=true`

`publish_plugin`

1. `control.docs.get`
2. `control.registry.details` for each selected handler
3. `control.plugins.create_plugin`
4. `control.plugins.update_plugin` (only when edits are required)
5. verify the published plugin appears under `user` category in plugin UI (`control.plugins.list`)
6. enforce UX behavior:
   - unwrapped exports stay visible as flat `User.<Handler>` entries
   - published bundles render as first-class plugin cards/forms
7. instruct user to test via plugin card/form flow (not raw handler list)

### Capability-Gap Flow

When capability is insufficient, operator MUST run this branch:

1. produce `gap_summary` with classification and impact
2. propose reuse-first options in priority order:
   - compose with existing handlers/triggers/tools
   - reuse/patch existing exported tool
   - connect external MCP tool
   - implement new reusable integration (handler/trigger)
3. produce at least one **Integration Proposal Card**
4. ask user to choose path before continuing mutations
5. run the `ascn-integrations` skill flow for the selected option

The operator MUST pause lifecycle mutations until user selects a path.

## Post-Export Testability and Traceability

After export and activation, operator MUST validate runtime behavior:

1. invoke exported MCP tool with minimal valid payload
2. query latest runs via `control.runs.list`
3. confirm latest run status is expected (`COMPLETED` for happy-path smoke)
4. inspect full run payload via `control.runs.details` when run is failed or unexpected
5. if run fails, include `run_id` and `trace_id` in failure summary

## Export Robustness Rules

When handling export intent, operator MUST:

1. list exports with `expose_mcp_only=false` before reconciliation
2. ensure export output uses canonical `output_path`
3. verify `output_path` resolves to output-producing node
4. check canonical tool name conflicts before activation
5. smoke-test after activation and inspect runs on any failure

## Idempotency and Retry

1. Mutation operations MUST use a deterministic operation key: 
`{workspace_id}:{intent}:{workflow_id|workflow_name}:{payload_hash}`.
2. Transient failures (`timeout`, `5xx`, gateway unavailable) MAY retry up to 3 attempts with exponential backoff.
3. Validation/context/export-conflict failures MUST NOT auto-retry; patch context/payload first.
4. Retry behavior MUST be recorded in the final output.

## Authoring Standards

1. Activity IDs MUST be unique.
2. Every `edges[].to` MUST reference an existing activity.
3. Trigger entry edges SHOULD be explicit for deterministic starts.
4. `$json` MUST be used only for current node input.
5. Upstream reads MUST use `$node['id'].json.field` with graph reachability.
6. Dynamic expressions and secrets MUST use `={{ ... }}`.
7. Credentials MUST NOT be hardcoded.
8. If required capability is missing, operator MUST propose reusable integration path instead of ad-hoc one-off node logic.

## Naming Convention

For generated/updated workflow nodes, operator MUST use:

1. activity id pattern: `<verb>_<domain>_<seq>` (example: `fetch_orders_01`)
2. trigger id pattern: `<kind>_<seq>` (example: `tool_01`, `cron_01`)
3. workflow name pattern: `<domain>_<intent>_<variant>` (example: `orders_sync_tool`)
4. lowercase snake_case ids for stable `$node[...]` references

## Node Reference Syntax (Required)

The operator MUST explicitly use and communicate these patterns when authoring workflow params:

1. Current node input:
   - `={{ $json }}`
   - `={{ $json.field }}`
2. Upstream node output:
   - `={{ $node['build'].json }}`
   - `={{ $node['build'].json.message }}`
3. Upstream array/object access:
   - `={{ $node['fetch'].json.items[0].id }}`
4. Secrets:
   - `={{ $secrets.telegram_bot_token }}`

The operator MUST NOT use raw `$node[...]` or raw `$json...` strings without `={{ ... }}` in dynamic fields.
If a node reference is used, graph reachability MUST be validated (`A -> ... -> B`).

## Error Handling Standard

The operator MUST map errors to `contracts/error-taxonomy.yaml`.

Mandatory handling classes:

1. `validation`: patch payload and re-validate.
2. `context`: correct workspace/workflow mismatch before proceeding.
3. `export_conflict`: list exports and reconcile canonical name/output path.
4. `transient`: bounded retries with backoff.
5. `dependency`: stop execution and provide MCP connection runbook to user.
6. `capability_gap`: propose reusable integration options and request user decision.

## Failure Patch Strategy Templates

On failed validation or mutation, operator MUST choose patch strategy by class:

1. `validation`: patch params/edges/references, then re-validate
2. `context`: rebind workspace/workflow id, then retry once
3. `export_conflict`: list exports, reconcile tool+handler+output_path
4. `dependency`: stop and return connection runbook
5. `transient`: bounded retry with backoff (max 3)
6. `capability_gap`: return proposals and wait for user decision

## Output Contract

Every completion MUST include this shape:

```json
{
  "operations_executed": [
    {
      "step": 1,
      "tool": "control.docs.get",
      "result": "success",
      "duration_ms": 12
    }
  ],
  "final_state": {
    "workflow_id": "<uuid>",
    "version": 3,
    "status": "ACTIVE"
  },
  "validation_summary": {
    "valid": true,
    "issue_count": 0
  },
  "unresolved_risks": []
}
```

On failure, output MUST include:

1. `failing_operation`
2. `error_code` (taxonomy-aligned)
3. `error_message`
4. `next_action`
5. `connection_instructions` when error class is `dependency`
6. `integration_proposals` when class is `capability_gap`
7. `run_trace` (`run_id`, `trace_id`) when runtime execution started
8. `patch_strategy` selected from Failure Patch Strategy Templates

For `publish_plugin`, output MUST additionally include:

1. `definition_id`
2. `plugin_name`
3. `handlers`
4. `visibility_state` (`visible_in_user_category|not_visible`)
5. `next_action` with user-facing test steps

For `create|patch|repair|export`, output SHOULD additionally include:

1. `selected_blueprint`
2. `schema_lock_summary` (required/default/secret-backed fields)
3. `edge_intents` map (`sequence|branch_true|branch_false|error_path`)

## Integration Proposal Card

When capability gap is detected, proposal MUST follow this structure:

```json
{
  "integration_name": "Acme Orders Connector",
  "kind": "activity",
  "proposed_handler_id": "AcmeOrders.CreateOrder",
  "why_reusable": "Can be reused for all order create flows across workspaces",
  "params_schema": {"type": "object"},
  "returns_schema": {"type": "object"},
  "required_secrets": ["acme_api_key"],
  "auth_model": "api_key_header",
  "retry_policy": {"max_attempts": 3, "backoff": "exponential"},
  "rate_limit_hint": "100 req/min",
  "acceptance_tests": [
    "creates order with valid payload",
    "returns typed error on 4xx/5xx",
    "schema validation passes in control.workflows.validate"
  ],
  "reusability_scope": "multi-workflow"
}
```

## User Decision Gate

For capability gap, operator MUST ask user to pick one option:

1. Compose from existing handlers/tools
2. Connect external MCP tool
3. Build new reusable integration (handler/trigger)

Mutations resume only after explicit user choice.

## User Decision Message Templates

For capability-gap responses, operator SHOULD use these standardized user-facing templates.

`compose_existing_handlers_or_tools`

```text
I can complete this using existing capabilities without building a new integration.
Plan:
1) compose current handlers/tools,
2) validate graph and schema,
3) activate workflow.
Choose this if you want fastest delivery with current platform components.
```

`connect_external_mcp_tool`

```text
I can connect an external MCP tool and reuse it in this workflow.
Plan:
1) connect MCP tool endpoint,
2) verify tool schema and auth,
3) wire tool into workflow and validate.
Choose this if the capability already exists in an external MCP server.
```

`build_new_reusable_integration`

```text
Current capabilities are insufficient. I propose a reusable integration:
- handler: {proposed_handler_id}
- scope: {reusability_scope}
- required secrets: {required_secrets}
Plan:
1) define params/returns schema,
2) implement reusable handler/trigger,
3) validate with acceptance tests and reuse in this workflow.
Choose this for long-term reuse across automations.
```

## User-Facing MCP Connection Playbook

When the skill is loaded but MCP is not connected, the operator MUST provide this actionable instruction set:

1. Verify the ASCN base URL is reachable.
2. Configure MCP gateway connection:
   - name: `workspace-mcp-gateway`
   - transport: `streamable_http`
   - url: `https://nocode.ascn.ai/mcp`
3. Ensure workspace secret `mcp_gateway_token` exists and has the intended token value.
4. Add `Authorization: Bearer <token>` header using the same token value.
5. Reconnect MCP client/session.
6. Re-run and verify control tool availability (`control.docs.get` or tool list inspection).

Recommended user message template:

```text
MCP control gateway is not connected for workspace {workspace_id}.
Please add/update MCP connection:
- transport: streamable_http
- url: https://nocode.ascn.ai/mcp
- workspace secret: mcp_gateway_token = <token>
- auth header: Authorization: Bearer <token>
- token source: https://ascn.ai/no-code/mcp-list
Then reconnect MCP and retry this request.
```

## Observability and Audit Fields

The final summary MUST include:

1. `workspace_id`
2. `intent`
3. `tool_sequence`
4. `total_duration_ms`
5. `retry_count`
6. `mutation_count`

## Mutation Safety

1. Before delete, operator MUST provide impact summary.
2. After every mutation, operator MUST report affected `workflow_id`, `version`, `status`.
3. If activation fails, operator MUST stop and provide concrete patch plan.

## Consistency Requirements

1. `SKILL.md` MUST remain consistent with `contracts/skill-contract.yaml`.
2. Scenario files in `contracts/scenarios/` SHOULD cover create, repair, and export flows.

## Change Management

1. Contract/toolflow changes MUST update `VERSION` and `CHANGELOG.md`.
2. Breaking changes MUST increment major version.
3. Non-breaking behavior additions SHOULD increment minor version.

## References

1. `references/workflow-construction.md`
2. `references/troubleshooting.md`
3. `references/mcp-connection.md`
4. `references/integration-proposals.md`
5. `references/plugin-publishing.md`
6. `contracts/skill-contract.yaml`
7. `contracts/error-taxonomy.yaml`
