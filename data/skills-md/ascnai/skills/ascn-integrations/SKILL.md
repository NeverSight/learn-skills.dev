---
name: ascn-integrations
version: 0.0.2
owner: platform-ai
maturity: beta
description: Deterministic guide for designing and delivering new ASCN integrations and wrapping them into user plugins.
---

# ASCN Integrations

This document is normative. RFC2119 keywords (`MUST`, `SHOULD`, `MAY`) define required behavior.

## Mission

Design and deliver missing capability as reusable ASCN integrations, then package them as user-visible plugins.

## When To Use

Use this skill when a workflow task cannot be completed with existing handlers/triggers/tools.

Typical triggers:

1. missing handler for a required API/service
2. missing trigger type for required event source
3. schema/contract mismatch blocks reliable workflow composition
4. required UI ergonomics (`params_ui`, options, conditional fields) are missing

## Required Inputs

The integrator MUST collect:

1. `workspace_id` (UUID)
2. capability gap summary (what cannot be built today)
3. target use-cases (at least one concrete workflow scenario)
4. expected input/output contract (JSON-level)
5. auth/secret requirements
6. publish target (`user` plugin first, system copy later)

If `workspace_id` or contract expectations are missing, stop and request them.

## Required MCP Tool Surface

1. `control.docs.get`
2. `control.registry.list`
3. `control.registry.details`
4. `control.workflows.list`
5. `control.workflows.describe`
6. `control.workflows.validate`
7. `control.workflows.create`
8. `control.workflows.patch`
9. `control.workflows.activate`
10. `control.tools.ensure_export`
11. `control.tools.list_exports`
12. `control.plugins.create_plugin`
13. `control.plugins.update_plugin`
14. `control.plugins.list`

## Delivery Modes

### Mode A: Workflow-backed integration (preferred first)

Use existing handlers to build a reusable workflow and export it through `Trigger.Tool`.

### Mode B: Native integration (new handler/trigger code)

Use only when Mode A cannot satisfy latency, auth, determinism, or protocol constraints.

Native integrations MUST still be wrapped/published as plugins for user consumption.

## Deterministic Flow

1. Discover existing capability (`control.registry.list`, `control.registry.details`, `control.tools.list_exports`).
2. Produce contract draft:
   - canonical handler id (`Vendor.Action`)
   - `params_schema` (input object)
   - `returns_schema` (output object)
3. Choose delivery mode (`A` or `B`) with explicit reason.
4. Implement integration.
5. Validate workflow/config contract (`control.workflows.validate`).
6. Activate export (`control.workflows.activate`, `control.tools.ensure_export`).
7. Bundle handlers into plugin (`control.plugins.create_plugin` then `update_plugin` if needed).
8. Verify plugin visibility with `control.plugins.list` and registry views.

## Plugin Packaging Rules

1. Plugin name MUST be stable and vendor/domain-scoped (e.g. `StripeOps`, `CRMHubspot`).
2. Handler names MUST be canonical and collision-safe.
3. One plugin MAY contain multiple handlers if they share domain and auth model.
4. Plugin definitions SHOULD include UI metadata (`name`, `description`, `icon`, `tags`) before handoff.
5. Unwrapped `Trigger.Tool` exports MUST still be user-visible as flat `User.<Handler>` entries.
6. Wrapped/published handlers MUST be rendered as first-class plugin cards/forms with plugin metadata (`name`, `description`, `icon`) and handler `params_ui`.

## Params UI Best Practices

`params_ui` MUST be human-usable and contract-aligned.

1. Every key in `params_ui` SHOULD exist in `params_schema.properties`.
2. Localize labels/hints where possible (`en`, `ru`).
3. Prefer explicit controls:
   - `string`, `string_multiline`, `number`, `boolean`, `options`, `array`, `object`, `string_json`
4. Use conditional visibility for complex forms via `displayOptions.show`.
5. Put dangerous/advanced options behind conditional toggles.
6. Include safe defaults where deterministic behavior is expected.
7. Use `options` only for selectable values; use `displayOptions.show` only for conditional visibility.
8. Keep field order identical to the execution mental model (auth -> target -> behavior -> advanced).

Example conditional field pattern:

```json
[
  {
    "key": "auth_mode",
    "control": "options",
    "label": {"en": "Auth mode"},
    "options": [
      {"value": "api_key", "label": {"en": "API key"}},
      {"value": "oauth", "label": {"en": "OAuth"}}
    ]
  },
  {
    "key": "api_key",
    "control": "string",
    "label": {"en": "API key"},
    "displayOptions": {"show": {"auth_mode": ["api_key"]}}
  }
]
```

Minimal `params_ui` field contract (recommended):

```json
{
  "key": "string",
  "control": "string|string_multiline|number|boolean|options|array|object|string_json",
  "label": {"en": "Field label"},
  "hint": {"en": "Optional guidance"},
  "required": false,
  "default": null,
  "options": [
    {"value": "v1", "label": {"en": "Value 1"}}
  ],
  "displayOptions": {"show": {"other_key": ["match_value"]}}
}
```

Rules for this contract:

1. `options` MUST exist only when `control=options`.
2. `displayOptions.show` MUST reference keys that exist in the same `params_ui`.
3. `required=true` fields SHOULD be present in `params_schema.required`.
4. Secret-bearing fields SHOULD use hints directing users to secrets, not literal defaults.

## Security & Secrets

1. Credentials MUST come from secrets (`={{ $secrets.name }}`), never literals.
2. `params_schema` SHOULD mark required secret-driven fields clearly.
3. Integration MUST document minimum secret set for successful invocation.

## Output Contract

Every completion MUST include:

```json
{
  "integration": {
    "mode": "workflow|native",
    "capability_status": "implemented",
    "handler_names": ["Vendor.Action"]
  },
  "plugin": {
    "plugin_name": "VendorOps",
    "created_or_updated": true
  },
  "verification": {
    "validated": true,
    "activated": true,
    "visible_in_plugins_list": true
  },
  "open_items": []
}
```

## Hand-off Back To ASCN Operator

After integration delivery:

1. return canonical handler/plugin identifiers
2. return required secrets and minimal invocation payload
3. instruct caller to resume lifecycle operations with `ascn-operator`
