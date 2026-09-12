---
name: pipefy-ai-agents
description: >
  Use this skill when the user wants to create, read, update, delete,
  or troubleshoot AI agents (conversational agents with behaviors).
  Covers 7 MCP tools including pre-flight validation, plus pipe-scoped
  knowledge bases (list, plain text/document/data lookup CRUD, access probe) attached via dataSourceIds.
  For traditional automations and AI automations, see skills/automations/.
tags: [pipefy, ai-agents, behaviors, conversational]
---

# AI Agents

Conversational AI agents attached to pipes. Each agent has an agent-level instruction and 1–5 behaviors, each with its own trigger event, prompt, and actions. **7 MCP tools.**

For traditional automations and AI automations (prompt-driven), see [skills/automations/pipefy-automations/SKILL.md](../../automations/pipefy-automations/SKILL.md).

---

## Tools

| Tool (MCP) | CLI | Read-only | Purpose |
|------------|-----|-----------|---------|
| `get_ai_agents` | `pipefy agent list` | Yes | List AI agents for a pipe (`repo_uuid` = pipe UUID, not numeric `id`). |
| `get_ai_agent` | `pipefy agent get` | Yes | Full agent config including behaviors. |
| `create_ai_agent` | `pipefy agent create` | No | Create a new conversational agent (active by default; `active=false` / `--inactive` to start disabled). |
| `update_ai_agent` | `pipefy agent update` | No | **Full-replace** (not patch). Always send complete `behaviors`. Preserves disabled state. |
| `delete_ai_agent` | `pipefy agent delete` | No | **(Two-step destructive)**[^mcp-confirm] |
| `toggle_ai_agent_status` | `pipefy agent toggle` | No | Explicit activate/deactivate (e.g. `--inactive`). |
| `validate_ai_agent_behaviors` | `pipefy agent validate-behaviors` | Yes | **Pre-flight check before create/update.** |

[^mcp-confirm]: MCP two-step: echo `confirmation_token` from the preview with `confirm=true`. CLI: `--yes`.

The read tools (`get_ai_agents`, `get_ai_agent`, `validate_ai_agent_behaviors`) and the write tools (`create`/`update`/`delete`/`toggle`) are all remote-safe: available under the hosted (`profile=remote`) surface. `create_ai_knowledge_base_document`, `create_llm_provider`, and `update_llm_provider` take a local file and are **local profile only** — withheld on the hosted server.

Execution logs live in [skills/observability/](../../observability/pipefy-observability/SKILL.md) (`get_ai_agent_logs`, `get_ai_agent_log_details`).

---

## Active lifecycle

- Agents are **active by default**. Create-active clears the API default disabled shell via the configure update (omits `disabledAt`). Create-inactive (`active=false` / `--inactive`) sets `disabled_at` explicitly on create and the chained update.
- Routine `update_ai_agent` / `pipefy agent update` **preserves** disabled state — it does not intentionally reactivate. Prefer passing `disabled_at` from a prior `get_ai_agent` (`disabledAt`) / `pipefy agent update --disabled-at` to skip the preserve re-read; when omitted, the SDK re-reads and re-sends.
- Explicit activate/deactivate: `toggle_ai_agent_status` / `pipefy agent toggle` (`--active` / `--inactive`).
- After create/update, confirm status from the response `disabled_at` / `active` fields when present. To re-read via `get_ai_agent` / `pipefy agent get`, use agent `disabledAt` (null means active) — get does not expose write-envelope `disabled_at` / `active`, and `behaviors[].active` is not agent enablement. Never assume inactive without that confirmation. An agent with no active behavior is disabled by the API regardless of the create/update enablement flags.

---

## Creation workflow (discover → validate → create → verify)

**Consent:** create or suggest an AI agent only when the user explicitly asked for AI / an agent. If AI seems useful but was not requested, ask first — never introduce agents without being asked.

Never guess event IDs, phase IDs, action types, or field IDs.

### 1 — Get pipe metadata

Call `get_pipe(pipe_id)` and extract:

- `uuid` → use as `repo_uuid` in all AI-agent tools.
- `phases[].id` / `phases[].name` → needed for `move_card` actions.
- Fields via `get_start_form_fields(pipe_id)` and/or `get_phase_fields(phase_id)` → needed for `update_card` actions.

### 2 — Check existing agents

`get_ai_agents(repo_uuid)` to avoid duplicates. To modify an existing agent, use `update_ai_agent` (not create). For full config, use `get_ai_agent(uuid)`.

### 3 — Discover valid trigger events

`get_automation_events(pipe_id)`. Common events:

| Event (`event_id` value) | `event_params` required | Example |
|------------|-------------------------|---------|
| card_created | None | `{}` |
| card_moved | `{"to_phase_id":"<phase_id>"}` | Fires only when card enters that phase. |
| field_updated | `{"triggerFieldIds":["<field_id>", ...]}` | Fires only when those fields change. |
| manually_triggered | None | User clicks button on card. |

For `card_moved` and `field_updated`, you MUST include `event_params`. Omitting it makes the behavior fire on every occurrence.

### 4 — Discover valid action types

`get_automation_actions(pipe_id)`. The 6 known `actionType` values and their required `metadata`:

| Action (`actionType` value) | `metadata` required |
|--------------|---------------------|
| update_card | `pipeId` + `fieldsAttributes` (each entry needs `fieldId` + `inputMode`) |
| move_card | `destinationPhaseId` |
| create_card | `pipeId` + `fieldsAttributes` |
| create_connected_card | `pipeId` + `fieldsAttributes` (requires pipe relation) |
| create_table_record | `tableId` + `fieldsAttributes` (table field IDs; **no** `pipeId`) |
| send_email_template | `emailTemplateId`; optional `allowTemplateModifications` (bool) |

`fieldId` values for card actions accept slug or numeric `internal_id`; for `create_table_record` they are **table** field IDs (validate with `get_table` / `get_table_record`, not the pipe).

### 5 — Build the behavior dict

```json
{
  "name": "<descriptive name>",
  "event_id": "<from step 3>",
  "event_params": {},
  "actionParams": {
    "aiBehaviorParams": {
      "instruction": "<prompt for the AI when this event fires>",
      "actionsAttributes": [
        { "name": "<action label>", "actionType": "<from step 4>", "metadata": { } }
      ]
    }
  }
}
```

- Each behavior MUST have at least one action in `actionsAttributes`.
- **Maximum 5 behaviors per agent.**
- The MCP tool auto-injects `referenceId` and `%{action:<uuid>}` placeholders — do NOT generate these yourself.
- **`inputMode` is required on every `fieldsAttributes` entry** (omitting it fails model validation). Values: `fill_with_ai` (AI writes the value into an **output** field), `fixed_value` (use the literal `value`), `copy_from` (`value` is a `%{…}` template copying another field).
- **Input** field references (`%{field:<internal_id>}` in the behavior `instruction`, auto-populated into `referencedFieldIds` on create/update) are needed **only when** the AI must read card field values, not for every `fill_with_ai` (e.g. instruction-only, OCR/attachment, or knowledge-base context). When card inputs are needed and omitted, `card.fields` arrives empty at trigger time and the model may hallucinate. A wrong **numeric** input id is accepted silently (validate and create/update) and becomes a dead `referencedFieldId`; a wrong **slug** never resolves and is dropped by the digits-only extractor (unresolved token). Either way `card.fields` stays empty (same hallucination); confirm the id with `get_start_form_fields` / `get_phase_fields`. Dotted connected-pipe refs (`%{field:<parent>.<child>}`) are not forwarded at runtime; to read a connected card field, use a field on the current pipe.
- For `update_card`: set `destinationPhaseId: ""` when not moving the card.

#### Example identifiers (fictional)

Use real values from `get_pipe` / `get_start_form_fields` for your org. Placeholders below match unit-test fixtures in this repo. **The syntax matters** (`pipeId`, `fieldId`, `%{field:<internal_id>}`, `inputMode`) — **the example digits do not**; substitute each pipe's numeric `internal_id` and phase id.

| Role | Example value |
|------|----------------|
| Pipe (numeric repo id) | `987654321` |
| Field `internal_id` | `900000101` |
| Destination phase (`move_card`) | `900000201` |
| Target pipe (`create_card`) | `900000301` |

#### Metadata examples

```json
// update_card — output field fill_with_ai; input fields referenced in instruction
{ "pipeId": "987654321", "destinationPhaseId": "", "fieldsAttributes": [{ "fieldId": "900000101", "inputMode": "fill_with_ai", "value": "" }] }
// companion instruction (aiBehaviorParams.instruction), not metadata:
// "Read %{field:900000102} (title) and %{field:900000103} (description), then fill the category."

// move_card
{ "destinationPhaseId": "900000201", "pipeId": "", "fieldsAttributes": [] }

// create_card
{ "pipeId": "900000301", "fieldsAttributes": [{ "fieldId": "title", "inputMode": "fill_with_ai", "value": "" }] }

// create_table_record (fieldsAttributes are TABLE field IDs; no pipeId)
{ "tableId": "<table_id>", "fieldsAttributes": [{ "fieldId": "<table_field_id>", "inputMode": "fill_with_ai", "value": "" }] }

// send_email_template
{ "emailTemplateId": "<template_id>", "allowTemplateModifications": false }
```

### 5b — Optional: capabilities and LLM provider

Inside `actionParams.aiBehaviorParams` a behavior may also carry:

- **`capabilitiesAttributes`** — advanced tools the behavior can use. Each entry is exactly `{ "capabilityType": "<type>", "enabled": true|false }` (both keys required, no extra keys — bare strings or `{ "type": ... }` are rejected).

  | Product name | `capabilityType` |
  |---|---|
  | IDP / Intelligent Document Processing | `advanced_ocr` |
  | Calculations & Analysis | `math_operations` |
  | Web Search | `web_search` |
  | Web Scraping | `web_scraping` |
  | Max effort | `max_effort` |

  `capabilityType` is not checked against a fixed set — any value passes through and the API validates the enum on write, so new capabilities work without a toolkit update. Validation checks **shape only, not entitlement** — a capability may still require organization-level enablement to have any effect, so a green pre-flight does not guarantee the capability is active for the org.
- **`providerId`** / **`systemProviderId`** — pick the behavior's LLM provider. Set **at most one** (a behavior resolves to a single active provider). Discover valid IDs with `get_llm_providers` (CLI: `pipefy ai-provider list`): each provider carries `type` — use `providerId` for a custom (`byom`) provider and `systemProviderId` for a Pipefy-managed (`system`) one. `get_default_llm_provider` shows what a behavior falls back to when neither is set. IDs are also visible in the organization's AI settings in the Pipefy UI.

  **Bring your own model (custom provider).** To back a behavior with your own vendor credentials, create a custom provider first, then use its `id` as `providerId`: `validate_llm_provider_access` (confirm read access — writes need the stronger `manage_ai_providers` org permission and an eligible plan, so a write may still be denied) → `create_llm_provider` with the configuration in a **local JSON file** (`configuration_file_path`; never inline — secrets are never logged or returned; the file's `provider` key selects the vendor). `create_llm_provider` and `update_llm_provider` are local profile only (`configuration_file_path` has no meaning on the hosted server; both tools are withheld there). On the hosted URL, attach an existing provider via `get_llm_providers` and `providerId` / `systemProviderId`, or create the provider from the CLI / Quick-install path. Manage a local-profile provider with `update_llm_provider` (send the **full** configuration; leave the `__REDACTED__` placeholders from `get_llm_providers` in place to keep existing secrets, or put a new value to rotate one), `set_llm_provider_active_status`, and `delete_llm_provider` (check `get_llm_provider_dependencies` first). Set the organization default with `set_default_llm_provider` (exactly one of `provider_id` / `system_provider_id`) or clear it with `reset_default_llm_provider`. CLI: `pipefy ai-provider create` / `update` / `delete` / `set-active-status` / `default set` / `default reset`.
- **`dataSourceIds`** — knowledge base sources the behavior can draw on. Each ID is a knowledge base item ID from `get_ai_knowledge_bases` (CLI: `pipefy kb list`). Agents also carry an agent-level `data_source_ids`; the two are unioned. See [Knowledge bases](#knowledge-bases-data-sources) below for the create → attach flow.

```json
{
  "instruction": "Extract totals from the attached invoice.",
  "capabilitiesAttributes": [{ "capabilityType": "advanced_ocr", "enabled": true }],
  "actionsAttributes": [ /* ... */ ]
}
```

### 6 — Validate (recommended for complex behaviors)

`validate_ai_agent_behaviors(pipe_id, behaviors)` checks:
- Output field IDs (`fieldsAttributes[].fieldId`) exist in the pipe
- Phase IDs exist
- Pipe relations exist for `create_connected_card`
- Action types are valid (the 6 in `KNOWN_AI_ACTION_TYPES`; `create_table_record` `fieldsAttributes` are **table** field IDs, so they are not checked against the pipe and surface a warning to verify with `get_table`; `send_email_template` metadata runs no pipe field-ID checks)
- Behavior structure passes Pydantic validation (including canonical `capabilitiesAttributes` shape and at most one of `providerId` / `systemProviderId`)
- `fieldsAttributes[].fieldId` values (outputs) are checked against start-form and phase fields, accepting both slug `id` and numeric `internal_id`. Instruction `%{field:...}` tokens (inputs) are **not** existence-checked: a missing id/slug still yields `valid: true`. Slug → numeric rewrite happens only on create/update, not here.
- Pass `data_source_ids` (agent-level) to also check knowledge base membership: it is unioned with each behavior's `dataSourceIds` and checked against the pipe's knowledge bases. Unknown IDs are **warnings only** (`valid` stays true); if the knowledge base list cannot be read, a single warning is added and the check is skipped.

**`strict_unknown_action_types`** (default `true`): an `actionType` outside the known 6 is reported in `problems` (blocking). Set `false` to demote unknown action types to `warnings` only, so `valid` stays true. CLI: `--strict` (default) / `--no-strict` on `agent validate-behaviors`, `agent create`, and `agent update`.

### 7 — Create the agent

`create_ai_agent` with `name`, `repo_uuid`, `instruction`, and `behaviors`. One-call creation is preferred — avoids partial agent shells. Agents are **active by default**; pass `active=false` (MCP) or `--inactive` (CLI) to start disabled (see [Active lifecycle](#active-lifecycle)).

The **CLI** `agent create` / `agent update` require `--pipe` (numeric pipe id) and run `validate_ai_agent_behaviors` automatically as a pre-flight, blocking the write when `problems` are found and surfacing `warnings` under a `preflight` key. The MCP tools do **not** auto-preflight, so call `validate_ai_agent_behaviors` yourself (step 6) before `create_ai_agent` / `update_ai_agent`. CLI flags: `--repo-uuid`, `--name`, `--instruction`, `--behaviors` (JSON array), `--data-sources` (JSON array); create also: `--active` / `--inactive` (update has no status flags — use `agent toggle`); `agent validate-behaviors` instead takes `--data-source-id` (repeatable).

On create/update, slug `fieldId` values are resolved to numeric `internal_id`, `%{field:<slug>}` is rewritten to `%{field:<internal_id>}`, and `referencedFieldIds` is auto-populated when applicable.

### 8 — Handle responses

- **Success with `agent_uuid`** → confirm `disabled_at` / `active` on the response (active when `disabled_at` is null).
- **Partial failure (UUID returned, behaviors rejected)** → call `update_ai_agent` with the **full required payload**: `uuid`, `repo_uuid` (same pipe UUID used on create), `name`, `instruction`, and complete `behaviors` (full-replace, not patch). Do NOT create a second agent. The create shell is often disabled (`disabled_at` on the partial-failure envelope); update preserves that state — call `toggle_ai_agent_status` after a successful recovery update if you need the agent active.
- **Failure without UUID** → validation or API error. Trust the hint text in the enriched error.

### 9 — Verify

`get_ai_agent(uuid)` to confirm behaviors match expectations **and**, when the write response is unclear, re-read agent enablement via `disabledAt` (null means active). Prefer create/update response `disabled_at` / `active` when present. Do not treat `behaviors[].active` as agent enablement; never assume inactive without confirmation.

---

## Knowledge bases (data sources)

Knowledge bases are pipe-scoped data sources an agent draws on. Attach one by putting its ID in a behavior's `dataSourceIds` (or the agent-level `data_source_ids`). All knowledge base operations are scoped by the pipe **UUID** (`pipe_uuid`), not the numeric pipe ID — `get_pipe` returns the `uuid`.

| Tool (MCP) | CLI | Read-only | Purpose |
|------------|-----|-----------|---------|
| `get_ai_knowledge_bases` | `pipefy kb list` | Yes | List every item on a pipe (plain texts, documents, data lookups); each has an `id` for `dataSourceIds` and a `type` (`knowledge_base_plain_texts`, `knowledge_base_documents`, or `data_lookups`). |
| `get_ai_knowledge_base_plain_text` | `pipefy kb plain-text get` | Yes | Fetch one plain text with its content. |
| `create_ai_knowledge_base_plain_text` | `pipefy kb plain-text create` | No | Create a plain text (`name`, `content` 1-3500, `description` 1-900 — all required). |
| `update_ai_knowledge_base_plain_text` | `pipefy kb plain-text update` | No | Partial update; pass at least one of name/content/description. |
| `delete_ai_knowledge_base_plain_text` | `pipefy kb plain-text delete` | No | **(Two-step destructive)**[^mcp-confirm] |
| `get_ai_knowledge_base_document` | `pipefy kb document get` | Yes | Fetch one document's metadata (`content` is the stored URL, not text). |
| `create_ai_knowledge_base_document` | `pipefy kb document create` | No | Upload a local PDF in one shot (`file_path`/`--file`, `name`, `description` 1-900). `.pdf` + 20 MiB cap client-side; indexing is async. `file_path` is local profile only — withheld on the hosted server (no hosted-safe source). |
| `update_ai_knowledge_base_document` | `pipefy kb document update` | No | Metadata-only update (name/description); no file replacement. |
| `delete_ai_knowledge_base_document` | `pipefy kb document delete` | No | **(Two-step destructive)**[^mcp-confirm] |
| `get_ai_knowledge_base_data_lookup` | `pipefy kb data-lookup get` | Yes | Fetch one data lookup; the payload never includes `conditions` — keep the definition client-side. |
| `create_ai_knowledge_base_data_lookup` | `pipefy kb data-lookup create` | No | Create a data lookup (`name`, `description` 1-900, `source_repo_id` numeric pipe ID, `output_fields` 1-30, `conditions` — all required). |
| `update_ai_knowledge_base_data_lookup` | `pipefy kb data-lookup update` | No | Full replacement: resend `source_repo_id`/`output_fields`/`conditions` every call; omitted `search_query` clears it; only name/description are partial. |
| `delete_ai_knowledge_base_data_lookup` | `pipefy kb data-lookup delete` | No | **(Two-step destructive)**[^mcp-confirm] |
| `validate_knowledge_base_access` | `pipefy kb validate-access` | Yes | Probe read access before writes. |

### Flow: validate-access → create plain text → attach

1. **Probe access** — `validate_knowledge_base_access(pipe_uuid)` (CLI: `pipefy kb validate-access`). A green result proves read access only (`read_ai_agents`), never the `manage_ai_agents` entitlement writes need. The CLI create/update commands gate on this automatically; MCP callers should probe first (create/update do not auto-probe).
2. **Create the source** — `create_ai_knowledge_base_plain_text(pipe_uuid, name, content, description)`. Limits fail fast client-side: `content` 1-3500 chars, `description` 1-900 chars (both required). Keep the returned `id`.
3. **Attach** — add that `id` to a behavior's `dataSourceIds` (or the agent-level `data_source_ids`) when calling `create_ai_agent` / `update_ai_agent`. Validate first with `validate_ai_agent_behaviors(pipe_id, behaviors, data_source_ids=[...])` — unknown IDs surface as warnings.

For a **PDF document** instead of plain text, use `create_ai_knowledge_base_document(pipe_uuid, name, description, file_path)` (CLI: `pipefy kb document create --file …`) at step 2. That tool is local profile only (`file_path` is a file on the machine running the MCP server; it is withheld on the hosted URL). On the hosted server, create a plain-text source instead, or use the CLI / Quick-install path. Locally, it uploads the PDF in one shot; `.pdf` and the 20 MiB cap are enforced client-side, and indexing is asynchronous (the document may not be searchable immediately). The rest of the flow is identical — keep the returned `id` and attach it.

### Data lookups: create with an AI-filled condition → attach → update (full replacement)

A **data lookup** lets the agent search cards in a source pipe by conditions and return selected field values. Same flow as above at step 2, with three rules of its own:

1. **Create** — `create_ai_knowledge_base_data_lookup(pipe_uuid, name, description, source_repo_id, output_fields, conditions)` (CLI: `pipefy kb data-lookup create --source-repo-id … --output-fields '[…]' --conditions '[…]'`). `source_repo_id` is the **numeric** ID of the source pipe (a UUID is accepted by the API but the lookup then breaks when the agent runs it). `output_fields` takes 1-30 field IDs (field slugs plus static fields like `id`, `title`, `created_at`). Each condition needs `field` + `operator` (opaque backend string, e.g. `"eq"`, `"contains"`) and is either **static** (string `value` required) or **AI-filled** — the AI asks the user for the value at runtime:

   ```json
   [{"field": "customer_email", "operator": "eq", "usingFillWithAi": true,
     "inputName": "Customer email", "inputType": "text",
     "inputDescription": "The customer's email address"}]
   ```

2. **Attach** — keep the returned `id` and add it to `dataSourceIds`, exactly as for the other kinds. **Also keep the definition you sent**: reads never return `conditions`, so your copy is the only complete record of the lookup.
3. **Update replaces everything** — `update_ai_knowledge_base_data_lookup` requires `source_repo_id`, `output_fields`, and `conditions` on every call (the complete condition set, not a delta), and omitting `search_query` clears it. Only `name`/`description` keep their stored values when omitted.

---

## Token normalization & slug resolution

Instructions accept five token aliases — all normalize to canonical `%{field:<internal_id>}`:

| Form | Behavior |
|------|----------|
| `%{<internal_id>}` | Canonical short form. |
| `{<internal_id>}` | Bare; auto-prefixed with `%`. |
| `{field:<internal_id>}` | Bare-with-prefix; auto-`%`. |
| `{field:<slug>}` | Bare slug; resolved to numeric when behavior action carries `pipeId`. |
| `%{field:<internal_id>}` | Canonical full form. |

`%{field:<slug>}` is rewritten to `%{field:<internal_id>}` when an action in the behavior supplies `pipeId`. If the Pipefy UI shows plain text instead of chips in token slots, the payload probably still has non-canonical tokens.

---

## Template params / placeholders

Per behavior you can pass `template_params` (or `placeholders`) with `str → str` values and use `{{name}}` in any string (instruction, metadata IDs, etc.). Optionally set `instruction_template` instead of `aiBehaviorParams.instruction` — the tool interpolates and writes the final instruction before the API call. These keys are stripped before validation.

```json
{
  "name": "Classify card",
  "event_id": "card_created",
  "instruction_template": "Read {{field_ref}} and classify the card.",
  "template_params": { "field_ref": "%{field:900000101}" },
  "actionParams": {
    "aiBehaviorParams": {
      "actionsAttributes": [
        {
          "name": "Fill classification",
          "actionType": "update_card",
          "metadata": { "pipeId": "{{pipe}}", "fieldsAttributes": [{ "fieldId": "{{class_field}}", "inputMode": "fill_with_ai", "value": "" }] }
        }
      ]
    }
  },
  "placeholders": { "pipe": "987654321", "class_field": "900000101" }
}
```

`template_params` and `placeholders` merge (placeholders wins on conflict).

---

## Naming differences (UI vs API)

| Pipefy UI | API / Tool field |
|-----------|------------------|
| Description (agent creation step 1) | `instruction` (agent-level) |
| Instruction / Prompt (per behavior) | `actionParams.aiBehaviorParams.instruction` |
| Pipe UUID | `repo_uuid` (from `get_pipe().uuid`, NOT the numeric `id`) |

---

## Success criteria

- Create/update response shows the expected `disabled_at` / `active` (active when `disabled_at` is null). If confirming via `get_ai_agent`, use agent `disabledAt` (null means active) — not write-envelope keys and not `behaviors[].active`.
- `validate_ai_agent_behaviors` reports no errors before creation.
- Agent appears in the Pipefy UI under the pipe's AI settings.

## Failure modes

- **`update_ai_agent` is full-replace, not patch.** Fetch existing behaviors with `get_ai_agent` first, merge, then update — otherwise existing behaviors are silently dropped. Update never reactivates a disabled agent — use `toggle_ai_agent_status` / `pipefy agent toggle` for that.
- **Behavior save is all-or-nothing (`RECORD_NOT_SAVED`).** One invalid behavior rejects the entire list. The MCP tool auto-validates the payload on failure; if structurally correct, the error indicates a pipe-level restriction (not your payload). Inform the user this pipe does not support AI agent behaviors and suggest alternatives.
- **Partial-failure recovery.** If `create_ai_agent` returns a UUID but reports failure, call `update_ai_agent(uuid, repo_uuid, name, instruction, behaviors)` — all five are required. Reuse the create `repo_uuid`; send the full behaviors list. Do NOT create a second agent. Update preserves disabled state; use `toggle_ai_agent_status` / `pipefy agent toggle` to change enablement.
- **Cross-pipe `PERMISSION_DENIED`.** Behaviors with `create_connected_card` or cross-pipe `create_card` require the service account to be a member of **both** source and destination pipes. When it is not, the API returns a bare `PERMISSION_DENIED`. Recovery: `get_pipe_members` + `invite_members` on the destination pipe.
- **Phase transition rule on `move_card`.** Destination must be reachable from the source phase (`cards_can_be_moved_to_phases`). Both `validate_ai_agent_behaviors` and `create_ai_agent` / `update_ai_agent` enrich this error with `valid_destinations` and a hint that transition rules are editable in the Pipefy UI only.
- **Maximum 5 behaviors per agent.** Adding a 6th rejects the whole save.
- **Ghost agents.** An agent listed by `get_ai_agents` may return "Agent not found" on `get_ai_agent` — a Pipefy backend artifact, persists across sessions, do not retry.
- **GraphQL error hints.** When a dedicated read tool returns permission-denied or not-found, the `error.message` may cite concrete tools (e.g. `"Use 'get_ai_agents' to list agents..."`). Trust the hint; don't improvise alternative flows.
- **Validation rejections.** Common issues: invalid `trigger_event`, prompt too long, missing required action config. Read the `errors` field per behavior.
- **`delete_ai_agent` first call returns preview.** Expected. Show the preview to the user and get their approval, then call with `confirm=true` and the preview's `confirmation_token`.

## See also

- [skills/automations/pipefy-automations/SKILL.md](../../automations/pipefy-automations/SKILL.md) — traditional automations and AI automations (different from AI agents).
- [skills/observability/pipefy-observability/SKILL.md](../../observability/pipefy-observability/SKILL.md) — agent execution logs and credit usage.
- [skills/introspection/pipefy-introspection/SKILL.md](../../introspection/pipefy-introspection/SKILL.md) — Recipe 2 inspects full behavior config via `execute_graphql`.
- `docs/mcp/tools/identifiers.md#ai-agents-and-knowledge-bases` — canonical map of which tool/argument expects slug vs `internal_id` vs uuid vs numeric id (AI agents scope by `repo_uuid` = pipe UUID).
