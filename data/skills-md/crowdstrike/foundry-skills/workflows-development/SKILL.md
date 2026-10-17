---
name: workflows-development
description: Create and configure Falcon Fusion SOAR workflow YAML for Falcon Foundry apps. TRIGGER when user asks to "create a workflow", "build an automation", "configure Fusion SOAR", "add an on-demand workflow", runs `foundry workflows create`, or needs help with Fusion YAML syntax, triggers, actions, or variable references. DO NOT TRIGGER for UI pages, functions, or collection schemas — use the appropriate sub-skill.
version: 1.6.0
updated: 2026-10-01
tags: [foundry, workflows, fusion-soar, yaml]
author: CrowdStrike
license: MIT
compatibility: Claude Code >=1.0
metadata:
  category: automation
---

# Foundry Workflows Development

> Write every workflow definition in Fusion YAML, validate step dependencies before running it, and handle failures with conditional routing and action-level flags ([Error Handling](#error-handling)) — Fusion has no `onError` blocks and no built-in retry.

> **Part of a suite.** If `development-workflow` has not already run, and this is a new app or its first capability, load the `development-workflow` skill first — it owns the CLI prerequisite check, scaffolding order, and manifest coordination.

Falcon Foundry Workflows are YAML-defined automation units executed by the Falcon Fusion engine. They orchestrate multi-step operations across Functions, Collections, CrowdStrike APIs, and RTR sessions with parallelism and state management.

## Prerequisites

- **Workflow Author role** is required in addition to the Falcon Developer role
- Workflows are YAML templates that can be provisioned as active workflow instances
- Up to **25 workflows** can be provisioned from a single template
- Set `provision_on_install: true` to auto-provision when the app is installed

## CLI Scaffolding

```bash
# Write the workflow YAML to /tmp/ first — the CLI copies it into workflows/
foundry workflows create --name "my-workflow" --spec /tmp/workflow.yaml --no-prompt
# After: edit workflows/my-workflow.yml to refine workflow logic
```

### Discover Available Actions and Triggers

```bash
foundry workflows actions view --name "send email" --no-prompt              # Look up by name
foundry workflows actions view --name "send email" --no-prompt --output-schema  # Output schema
foundry workflows actions view --name "send email" --no-prompt --mock       # Mock output
foundry workflows triggers view --no-prompt                                 # List triggers
```

> **Always use `--no-prompt` on `actions view` and `triggers view`.** As of CLI 2.1.1, multiple matches are listed non-interactively. On older CLIs, partial matches trigger an interactive prompt that fails in headless environments (`Error: no TTY available`). The bundled `action_search.py` is an alternative that works without a manifest directory — see [references/action-discovery.md](references/action-discovery.md).

## Workflow Structure

### Trigger + Actions Format (standard)

This is the format produced by `foundry workflows create` and used by all production Foundry sample apps:

```yaml
name: list-okta-users
description: On-demand workflow to list Okta users and print results
provision_on_install: true
trigger:
    next:
        - list_users
    name: On demand
    type: On demand
actions:
    list_users:
        id: api_integrations.Okta.listUsers
        next:
            - print_results
        properties: {}
        version_constraint: ~0
    print_results:
        id: aadbf530e35fc452a032f5f8acaaac2a
        properties:
            text_data: "${data['list_users.API_Integration.Custom_Okta.listUsers.body']}"
        version_constraint: ~1
output_fields: []
```

**Trigger types:**

| Type | Format |
|------|--------|
| On demand | `name: On demand`, `type: On demand` |
| Scheduled | `event: Schedule`, `schedule: {time_cycle: "0 */6 * * *", tz: Etc/UTC}` |

> **⚠️ Null-guard trigger parameters:** When run from the Falcon console, the UI prompts users to fill in parameters. However, when triggered via API or from another workflow, parameters may be empty. Guard defensively:
>
> ```yaml
> conditions:
>     check_param:
>         cel_expression: "data['param_name'] != null && data['param_name'] != ''"
>         next:
>             - use_param
>         display:
>             - param_name was provided
>         else:
>             - handle_missing
> ```
>
> Or inline in CEL: `${data[?'param'].orValue("default")}` (preferred) or `${data['param'] != null ? data['param'] : "default"}` (traditional)

**Variable syntax in actions:** Use `${data['action_key.path.to.field']}` CEL expressions. See [Variable References](#variable-references) for the full syntax. Do NOT use `$action_name.output.body` — it passes as a literal string and is not resolved.

**Version constraints:** Every action requires `version_constraint`. The `~N` value pins against the activity's declared `semantic_version` field, not its internal iteration count. The rule:

- `~0` = activity has **no** `semantic_version` defined (functions, API integrations, and some platform actions like "contain device")
- `~1` = activity **has** a `semantic_version` (most platform actions: Print data, Send email, Create/Update variable, Get device details, etc.)

Use `foundry workflows actions view --name "<action>" --no-prompt` to check. If the activity output shows a semantic_version field, use `~1`. If it does not, use `~0`.

```yaml
actions:
    my_function:
        id: functions.my-func.process
        properties: {}
        version_constraint: ~0       # no semantic_version defined
    contain_host:
        id: <contain-device-action-id>
        properties:
            device_id: "${data['trigger.device_id']}"
        version_constraint: ~0       # no semantic_version defined
    print_results:
        id: aadbf530e35fc452a032f5f8acaaac2a
        properties:
            text_data: "${data['my_function.output']}"
        version_constraint: ~1       # has semantic_version
```

### Manifest Configuration

```yaml
# manifest.yml
workflows:
  - name: my-workflow
    path: workflows/my-workflow/workflow.yaml
    permissions: []
```

Trigger type and schedule are defined inside the workflow YAML file (via `trigger:` block), not in the manifest. The manifest only declares the workflow name, path, and optional permissions.

For full RTR multi-host orchestration and investigation pipeline examples, see [references/workflow-examples.md](references/workflow-examples.md).

> RTR scripts are not supported in certified Foundry apps (apps published to the CrowdStrike Store). RTR workflows work in custom/internal apps only.

## Calling Functions from Workflows

Functions referenced in workflow actions (via `id: functions.{name}.{handler}`) must have `workflow_integration` in the manifest. This binds only at creation time, via `foundry functions create --wf-expose` (plus `--input-schema`/`--output-schema`) — hand-editing `manifest.yml` does not work.

If a function was created without it, recreate the function. That changes its `workflow_integration.id`, so update the `id: functions.{name}.{handler}` reference in your workflow YAML in place. Do NOT delete and recreate the workflow itself — see the warning below.

**Deploy error if missing:**
```
❌ Error: referenced function '{name}' and handler '{handler}' does not have workflow_integration properties defined
```

**Calling the app's own AI agent**: use `id: ai_agents.<agent name>` (the manifest `name`) with `input` for the prompt and `version_constraint: ~1`; the agent needs `exposure.workflows.system_action: true`. `apps validate` doesn't resolve it, so check the deploy output. See the `ai-agents-development` skill's `references/workflow-invocation.md`.

> **⚠️ Reading Falcon alerts, detections, or incidents? It depends on whether the workflow already holds the object.** *Enriching* a detection the workflow was triggered on (query by its ID, e.g. `Ngsiem.detection.id = ?detectID`) → Event Query action, go schemaless. *Fetching a population you don't have* ("summarize all high-severity alerts") → source-of-truth API: a native platform action (e.g. Cases → Search Cases) first, or a FalconPy `Alerts`/`Detects` function when none fits — an Event Query can silently return nothing since NG-SIEM contents are connector-dependent. See [references/event-query-vs-api.md](references/event-query-vs-api.md).

## Calling API Integration Operations

> **💡 Consider HTTP Actions first.** For a simple REST call that doesn't need a custom UI or reusable function, an [HTTP Action](https://www.crowdstrike.com/tech-hub/ng-siem/build-api-integrations-with-falcon-fusion-soar-http-actions/) is faster than an API integration — no app, no OpenAPI spec, no deploy, and 130+ pre-built templates. Use a full API integration when the operation is reused across workflows or paired with functions/UI. See [references/http-actions.md](references/http-actions.md).

Workflows invoke API integration operations using the `api_integrations.{name}.{operationId}` pattern:

> **⚠️ Always use registered integrations.** If an API integration is declared in `manifest.yml`, the workflow MUST call it via `api_integrations.{name}.{operationId}`. Do NOT use a function that makes raw HTTP calls to the same API with hardcoded credentials or template variables like `{{API_TOKEN}}`. The platform manages authentication, rate limiting, and audit logging through the integration.

```yaml
actions:
    list_users_action:
        id: api_integrations.Okta.listUsers    # {name}.{operationId}
        properties: {}
        version_constraint: ~0
        next:
            - print_data

    print_data:
        id: aadbf530e35fc452a032f5f8acaaac2a
        properties:
            text_data: "${data['list_users_action.API_Integration.Custom_Okta.listUsers.body']}"
        version_constraint: ~1
```

The `{name}` must exactly match the `name` field from the `api_integrations` entry in `manifest.yml`, prefixed with `Custom_`. The platform adds `Custom_` to all API integration names in the variable path. The OpenAPI spec must have a matching `operationId` with a properly structured `x-cs-operation-config`:

```yaml
x-cs-operation-config:
  workflow:
    name: listUsers
    description: List all users
    expose_to_workflow: true
    system: false
```

The `workflow` nesting is required — a flat `expose_to_workflow: true` under `x-cs-operation-config` will not work. Auth scopes for CLI-created artifacts are managed automatically.

## Platform Actions

Platform actions (send email, log output, create detection) require platform-specific action IDs. These IDs are verified identical across us-1, us-2, and eu-1 clouds:

| Action Name | ID |
|------------|-----|
| Create variable | `702d15788dbbffdf0b68d8e2f3599aa4` |
| Update variable | `6c6eab39063fa3b72d98c82af60deb8a` |
| Print data | `aadbf530e35fc452a032f5f8acaaac2a` |
| Sleep | `4f1af1ae4c13dc1e3bcd725f8dc0f63b` |
| Send email | `07413ef9ba7c47bf5a242799f59902cc` |
| Request human input - Send email | `d6731c10b24834e2e0f4bd9d390a29c8` |
| Get device details | `6265dc947cc2252f74a5f25261ac36a9` |
| Contain device | `bec9fbeb4999d207937854fd56088107` |

For actions not in this table, use `foundry workflows actions view --name "..." --no-prompt` or the API query in [references/action-discovery.md](references/action-discovery.md). There are 9,000+ platform actions available. MUST NOT guess action IDs — use discovery commands.

### Common Action Properties

**Print data** (`aadbf530e35fc452a032f5f8acaaac2a`):

Print data has three input properties: `fields` (array — dropdown of trigger/workflow metadata), `text_data` (string — general-purpose), and `custom_json` (object only). Use `text_data` for API integration responses since `body` may be an array (example above).

The data path follows the pattern: `action_key.API_Integration.Custom_{IntegrationName}.{operationId}.{field}`. The platform adds `Custom_` to all API integration names in the variable path. Copy exact paths from the workflow editor's **Workflow data** panel: clicking a data pill copies its `${data['...']}` expression.

**Send email** (`07413ef9ba7c47bf5a242799f59902cc`):

Use Print data as the primary output action. Only add Send email when the user explicitly requests it. In headless/automated runs (`claude -p`), use Print data only — skip Send email entirely since the recipient cannot be prompted.

In interactive mode, when the user requests email, **ask for their email address** (with the assistant's input mechanism, or in chat). Never guess or infer it. The `to` field must be a real address — placeholders like `user@example.com` fail at runtime.

```yaml
    send_email:
        id: 07413ef9ba7c47bf5a242799f59902cc
        properties:
            to:
                - recipient@company.com    # Ask user for real address, or mark as parameterized
            subject: "Email subject"
            msg: "${data['list_users_action.API_Integration.Custom_Okta.listUsers.body']}"
            msg_type: "text"
        version_constraint: ~1
```

## Variable References

Falcon Fusion SOAR uses [Common Expression Language (CEL)](https://github.com/google/cel-spec/blob/master/doc/langdef.md) for data references. All variable references use `${data['...']}` expression syntax:

| Syntax | Description |
|--------|-------------|
| `${data['action_key.API_Integration.Custom_Name.operationId.body']}` | Response body from an API integration action |
| `${data['action_key.API_Integration.Custom_Name.operationId.body']}[0].field` | Access a field in the first element of an array response |
| `${data['action_key.output.field']}` | Field from a platform action's output |
| `${data['action_key.response']}` | Reply from an app's own AI agent (`ai_agents.<agent name>`); no `.output` segment. A `json_with_schema` agent has no `response`: use `${data['action_key.<schema field>']}` |
| `${data['action_key.FaaS.<function>.<handler>.<field>']}` | Function action output; a loop item's field is `...<field>.#.<item field>` |
| `${data['param_name']}` | On-demand trigger parameter value (use the parameter name directly, no prefix) |

**CRITICAL:** Do NOT use `$action_name.output.body` — this passes as a literal string and is NOT resolved at runtime. Always use `${data['...']}` expressions.

The `action_key` is the YAML key of the action (e.g., `list_users` from `actions: list_users:`), NOT the action's `id`. The integration name in the variable path is `Custom_{name}` where `{name}` is the `name` field in your `api_integrations` manifest entry (spaces become underscores). Use the **Workflow data** panel in the workflow editor to copy exact data paths — it produces the correct expression when you click a data pill.

### CEL Expressions

Falcon Fusion SOAR supports CEL for data transformations, conditions, and field access. Common patterns:

```yaml
# Null-safe field access — optional pattern (preferred)
"${data[?'action.field'].orValue(\"default\")}"

# Traditional null check
"${data['action.field'] != null ? data['action.field'] : \"default\"}"

# Array element access (index goes INSIDE the ${...}, not after it)
"${data['action.API_Integration.Custom_Name.op.body'][0]}"
```

**`has()` only works on retrieved objects, not data store keys.** `has(data['key'])` fails with `Q0910`; use `data['key'] != null` for keys, or `has(data['var'].field)` to check a field on an already-retrieved object.

CrowdStrike adds [custom CEL extensions](https://docs.crowdstrike.com/r/k223d842) (`cs.json.decode()`, `cs.ip.valid()`, `cs.timestamp.parse()`, etc.). For the full pattern catalog, the `has()`/`!= null`/optional decision guide, and extension details, see [references/cel-expressions.md](references/cel-expressions.md).

## Control Flow

**Loops** iterate over arrays or paginate with cursor-based conditions. Loops are self-contained sub-workflows at the root `loops:` level. The action before a loop must name it in its `next:` list, or the loop deploys but never runs:

```yaml
loops:
    DeviceLoop:
        for:
            input: device_query.Device.query.devices
            continue_on_partial_execution: true
            sequential: true
        trigger:
            next:
                - get_device_details
        actions:
            get_device_details:
                id: 6265dc947cc2252f74a5f25261ac36a9
                next:
                    - platform_check
                properties:
                    device_id: "${device_query.Device.query.devices.#}"
                version_constraint: ~1
        conditions:
            platform_check:
                next:
                    - remediate
                expression: get_device_details.Device.GetDetails.Platform:'Windows'
                display:
                    - Platform is Windows
                else:
                    - skip_device
```

**Conditions** use FQL-style `expression:` or CEL `cel_expression:` with optional `else:` for fallback routing:

```yaml
conditions:
    has_detection:
        next:
            - GetDetectionDetails
        cel_expression: data['detection_id'] != null && data['detection_id'] != ''
        display:
            - Detection ID was provided
        else:
            - PrintSummary
```

See [references/workflow-examples.md](references/workflow-examples.md) for full loop and condition examples from production apps.

## The "0" Gotcha

See [pagination-patterns](references/pagination-patterns.md#the-0-gotcha) for the "0" gotcha and fix pattern. Key point: check for both null and `"0"` in loop conditions.

## Workflow Name Uniqueness

Workflow names must be unique across all apps in the same tenant. If two apps deploy workflows with the same name, the second deploy fails silently or produces an "Unknown error." Use app-specific prefixes when the workflow name is generic.

## NEVER Delete and Recreate Workflows

> **⚠️ DANGER:** Deleting a workflow and recreating it with the same name causes cascading failures requiring a fresh app to recover.

Removing a workflow from the manifest does NOT delete its server-side artifact. Recreating with the same name → `409 name must be unique for an app`. A once-failed artifact taints the dependency graph (`400 dependent artifact failed`), blocking all further deploys.

**Instead, update in place** — edit the workflow YAML and redeploy. To re-bind a workflow to a recreated function, update the `id: functions.{name}.{handler}` reference in the YAML. Only delete a workflow if you genuinely no longer need it and won't recreate it with the same name.

## Workflow Sharing

```yaml
workflows:
  - name: my-workflow
    path: workflows/my-workflow/workflow.yaml
    workflow_integration:
      id: <generated-id>
      disruptive: false
      system_action: false   # false = available as a Fusion SOAR response action; true = internal app use only
```

> **⚠️ SOAR action visibility:** `system_action: false` = workflow appears as a Fusion SOAR response action (analysts trigger from detections/incidents). `system_action: true` = internal app use only (scheduled sync, helpers). If the user asks for a "SOAR action" or "response action", use `false`.

## Error Handling

Foundry workflows handle errors through conditional routing and action-level flags — not `onError` blocks or retry middleware. Key mechanisms: `fail_fast_enabled: false` (function actions), `continue_on_partial_execution` (loop blocks), and `conditions:`/`else:` routing. No built-in retry or backoff exists. For the full table, examples, and pagination-polling pattern, see [references/advanced-patterns.md](references/advanced-patterns.md).

## Testing

See [references/advanced-patterns.md](references/advanced-patterns.md) for workflow testing commands (mock triggers, mock actions, execution validation, and `foundry apps validate`).

## Reading Guide

| Task | Reference |
|------|-----------|
| Reading alerts/detections: Event Query vs. source-of-truth API | [references/event-query-vs-api.md](references/event-query-vs-api.md) |
| Full workflow examples (RTR, investigation) | [references/workflow-examples.md](references/workflow-examples.md) |
| Platform action discovery via API | [references/action-discovery.md](references/action-discovery.md) |
| CEL expressions (patterns, has() vs null, extensions) | [references/cel-expressions.md](references/cel-expressions.md) |
| CEL syntax, schemaless queries, dynamic data | [Falcon Fusion SOAR Event Queries: When and How to Go Schemaless](https://www.crowdstrike.com/tech-hub/ng-siem/falcon-fusion-soar-event-queries-when-and-how-to-go-schemaless/) |
| CEL extension functions reference | [Data Transformation Functions](https://docs.crowdstrike.com/r/k223d842) |
| Pagination strategies | [references/pagination-patterns.md](references/pagination-patterns.md) |
| HTTP Actions (call REST APIs without an app) | [references/http-actions.md](references/http-actions.md) |
| Error handling, HTTP Request actions, parameterized fields, counter-rationalizations | [references/advanced-patterns.md](references/advanced-patterns.md) |

## Use Cases

For real-world implementation patterns, see:
- `use-cases/schemaless-queries.md` — CEL expressions, dynamic data, Event Query configuration
- `use-cases/api-pagination.md` — Pagination strategies in functions and workflows
- `use-cases/custom-soar-actions.md` — Custom Falcon Fusion SOAR actions

## Reference Implementations

- **[foundry-sample-threat-intel](https://github.com/CrowdStrike/foundry-sample-threat-intel)**: Threat intelligence workflows with pagination
- **[foundry-sample-rapid-response](https://github.com/CrowdStrike/foundry-sample-rapid-response)**: Rapid response automation
- **[foundry-sample-scalable-rtr](https://github.com/CrowdStrike/foundry-sample-scalable-rtr)**: Scalable RTR orchestration
- **[foundry-sample-ngsiem-importer](https://github.com/CrowdStrike/foundry-sample-ngsiem-importer)**: Threat intel import for NG-SIEM
