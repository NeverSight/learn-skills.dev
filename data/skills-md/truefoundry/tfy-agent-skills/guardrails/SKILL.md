---
name: guardrails
description: Configures content safety guardrails for TrueFoundry AI Gateway. Supports PII filtering, content moderation, prompt injection detection, and custom rules. Use when adding safety controls to LLM or MCP tool calls.
license: MIT
compatibility: Requires Bash, curl, and access to a TrueFoundry instance
allowed-tools: Bash(*/tfy-api.sh *)
---

> Routing note: For ambiguous user intents, use the shared clarification templates in [references/intent-clarification.md](references/intent-clarification.md).

<objective>

# Guardrails

Configure content safety guardrails for TrueFoundry AI Gateway. Guardrails add safety controls to LLM inputs/outputs and MCP tool invocations.

## When to Use

Set up guardrail providers, create guardrail rules, or manage content safety policies for AI Gateway endpoints. This includes PII filtering, content moderation, prompt injection detection, secret detection, and custom validation rules.

## Deploying a Custom Guardrails Server

When the user asks to **deploy a guardrails server** or run guardrails as a deployed service, start from the official template so the server adheres to the gateway's input/output formats:

1. **Clone the default repo:** [truefoundry/custom-guardrails-template](https://github.com/truefoundry/custom-guardrails-template)
2. **Build on top of it** — Add or adjust custom rules, providers, or config within the template structure; do not build from scratch.
3. **Deploy** — Use the `deploy` skill to deploy the resulting service (Dockerfile or build from source as in the template).

This keeps guardrail servers compatible with TrueFoundry AI Gateway expectations.

</objective>

<instructions>

## Overview

Guardrails require a two-step setup:

1. **Guardrail Config Group** — Register guardrail provider integrations (credentials and configuration)
2. **Gateway Guardrails Config** — Create rules that reference those providers and attach them to a gateway

## Step 1: Create Guardrail Config Group

A guardrail config group holds integration credentials for one or more guardrail providers. See `references/guardrail-providers.md` for all supported providers.

When using direct API, set `TFY_API_SH` to the full path of this skill's `scripts/tfy-api.sh`. See `references/tfy-api-setup.md` for paths per agent.

### List Existing Config Groups

#### Via Tool Call

```
tfy_guardrail_config_groups_list()
```

#### Via Direct API

```bash
TFY_API_SH=~/.claude/skills/truefoundry-guardrails/scripts/tfy-api.sh

$TFY_API_SH GET '/api/svc/v1/provider-accounts?type=guardrail-config-group'
```

### Create Config Group

#### Via Tool Call

```
tfy_guardrail_config_groups_create(payload={"name": "my-guardrails", "type": "provider-account/guardrail-config-group", "integrations": [...]})
```

**Note:** Requires human approval (HITL) via tool call.

#### Via Direct API

```bash
$TFY_API_SH POST /api/svc/v1/provider-accounts '{
  "name": "my-guardrails",
  "type": "provider-account/guardrail-config-group",
  "integrations": [
    {
      "type": "integration/guardrail/tfy-pii",
      "config": {}
    },
    {
      "type": "integration/guardrail/tfy-content-moderation",
      "config": {}
    }
  ]
}'
```

Each integration has a `type` (from the providers reference) and a `config` object with provider-specific fields. Some providers (like `tfy-pii`, `tfy-content-moderation`) require no config. Others (like `aws-bedrock`, `azure-content-safety`) need cloud credentials.

> **Security:** Guardrail providers with external `endpoint_url` fields (e.g., `custom`, `opa`, `fiddler`, `palo-alto-prisma-airs`) route request data to third-party services. Verify that all external endpoints are trusted and controlled by your organization before registering them. Prefer TrueFoundry built-in providers (`tfy-pii`, `tfy-content-moderation`, `tfy-prompt-injection`) when possible.

### Presenting Config Groups

```
Guardrail Config Groups:
| Name             | ID       | Integrations |
|------------------|----------|--------------|
| my-guardrails    | pa-abc   | 3            |
| prod-safety      | pa-def   | 5            |
```

## Step 2: Create Gateway Guardrails Config

Gateway guardrails config defines rules that control which guardrails apply to which models, users, and tools.

### Get Existing Guardrails Config

#### Via Tool Call

```
tfy_gateway_guardrails_list()
```

#### Via Direct API

```bash
$TFY_API_SH GET /api/svc/v1/gateway-guardrails-configs
```

### Create Guardrails Config

#### Via Tool Call

```
tfy_gateway_guardrails_create(payload={"name": "production-guardrails", "type": "gateway-guardrails-config", "gateway_ref": "GATEWAY_FQN", "rules": [...]})
```

**Note:** Requires human approval (HITL) via tool call.

#### Via Direct API

```bash
$TFY_API_SH POST /api/svc/v1/gateway-guardrails-configs '{
  "name": "production-guardrails",
  "type": "gateway-guardrails-config",
  "gateway_ref": "GATEWAY_FQN",
  "rules": [
    {
      "id": "pii-filter-all-models",
      "when": {
        "target_conditions": {
          "models": ["*"],
          "mcp_servers": [],
          "tools": []
        },
        "subject_conditions": {
          "users": ["*"],
          "teams": []
        }
      },
      "llm_input_guardrails": [
        {
          "provider_ref": "provider-account-id:integration/guardrail/tfy-pii",
          "operation": "validate",
          "enforcing_strategy": "enforce",
          "priority": 1
        }
      ],
      "llm_output_guardrails": [
        {
          "provider_ref": "provider-account-id:integration/guardrail/tfy-pii",
          "operation": "validate",
          "enforcing_strategy": "enforce",
          "priority": 1
        }
      ],
      "mcp_tool_pre_invoke_guardrails": [],
      "mcp_tool_post_invoke_guardrails": []
    }
  ]
}'
```

### Update Existing Guardrails Config

#### Via Direct API

```bash
$TFY_API_SH PUT /api/svc/v1/gateway-guardrails-configs/GUARDRAILS_CONFIG_ID '{
  "name": "production-guardrails",
  "type": "gateway-guardrails-config",
  "gateway_ref": "GATEWAY_FQN",
  "rules": [...]
}'
```

### Rule Structure

Each rule contains:

- **id** — Unique identifier for the rule
- **when** — Conditions controlling when the rule applies:
  - `target_conditions.models` — Model name patterns (use `["*"]` for all)
  - `target_conditions.mcp_servers` — MCP server names to target
  - `target_conditions.tools` — Specific tool names to target
  - `subject_conditions.users` — User patterns (use `["*"]` for all)
  - `subject_conditions.teams` — Team names
- **llm_input_guardrails** — Applied to LLM request inputs
- **llm_output_guardrails** — Applied to LLM response outputs
- **mcp_tool_pre_invoke_guardrails** — Applied before MCP tool execution
- **mcp_tool_post_invoke_guardrails** — Applied after MCP tool execution

### Guardrail Reference Fields

Each guardrail entry in a rule has:

- **provider_ref** — Format: `<provider-account-id>:integration/guardrail/<provider-type>`
- **operation** — `validate` (check and block) or `mutate` (modify content, e.g., redact PII)
- **enforcing_strategy** — How violations are handled:
  - `enforce` — Block the request on violation
  - `audit` — Log the violation but allow the request
  - `enforce_but_ignore_on_error` — Enforce if guardrail succeeds, allow if guardrail errors
- **priority** — Integer for ordering when multiple mutate guardrails apply (lower runs first)

## Common Patterns

### PII Detection on All Models

```bash
# Step 1: Create config group with tfy-pii
$TFY_API_SH POST /api/svc/v1/provider-accounts '{
  "name": "pii-guardrails",
  "type": "provider-account/guardrail-config-group",
  "integrations": [
    {"type": "integration/guardrail/tfy-pii", "config": {}}
  ]
}'

# Step 2: Create rule targeting all models
# Use the provider account ID from step 1 response in provider_ref
```

### Content Moderation with Audit Mode

Use `"enforcing_strategy": "audit"` to log violations without blocking — useful for monitoring before enforcement.

### MCP Tool Guardrails

Target specific MCP tools with `mcp_tool_pre_invoke_guardrails` to validate inputs before tool execution, or `mcp_tool_post_invoke_guardrails` to scan tool outputs.

### Model-Specific Rules

Use `target_conditions.models` to apply guardrails only to specific models:

```json
"when": {
  "target_conditions": {
    "models": ["openai/gpt-4*", "anthropic/claude-*"],
    "mcp_servers": [],
    "tools": []
  }
}
```

### Exempt Specific Users

Combine broad model targeting with specific user conditions to exempt admin users:

```json
"subject_conditions": {
  "users": ["user1@example.com", "user2@example.com"],
  "teams": ["engineering"]
}
```

## Finding the Gateway Reference

The `gateway_ref` is the fully qualified name (FQN) of your AI Gateway deployment. Use the `ai-gateway` skill to list gateways and get the FQN.

</instructions>

<success_criteria>

## Success Criteria

- The user can list existing guardrail config groups
- The user can create a new guardrail config group with the desired provider integrations
- The user can create or update gateway guardrails config with rules
- Rules correctly target the intended models, users, and tools
- The agent has confirmed create/update operations before executing
- Provider references correctly link to the config group integrations

</success_criteria>

<references>

## Composability

- **Preflight**: Use `status` skill to verify credentials before configuring guardrails
- **Requires ai-gateway**: Get the gateway FQN for `gateway_ref`
- **Requires access-control**: For subject exemptions in rules (users, teams)
- **References mcp-servers**: For MCP tool guardrail targets
- **Provider reference**: See `references/guardrail-providers.md` for all 23 supported providers

</references>

<troubleshooting>

## Error Handling

### Config Group Not Found
```
Provider account not found. List config groups first to find the correct ID.
```

### Invalid Provider Type
```
Unknown guardrail integration type. Check references/guardrail-providers.md for valid types.
```

### Gateway Not Found
```
Gateway reference not found. Use the ai-gateway skill to list available gateways.
```

### Duplicate Rule ID
```
Rule ID already exists in this config. Use a unique ID for each rule.
```

### Missing Provider Credentials
```
Integration config missing required fields. Check the provider reference for required config.
```

### Permission Denied
```
Cannot manage guardrails. Check your API key permissions.
```

</troubleshooting>
