---
name: pipefy-introspection
description: >
  Use this skill when you need to discover GraphQL type shapes, mutation
  signatures, enum values, or execute arbitrary GraphQL as a fallback.
  This is the first fallback tier (Tier 2) when dedicated MCP tools fail
  or don't exist for an operation. 7 MCP tools.
tags: [pipefy, introspection, graphql, schema, fallback]
---

# Introspection & Raw GraphQL

Schema discovery, organization info, and a fallback executor. **7 MCP tools.**

This is **Tier 2** in the resolution strategy: when a dedicated MCP tool fails or doesn't exist, use introspection to understand the API, then `execute_graphql` to run the operation directly.

**Tier 1:** dedicated MCP tool exists — use it.
**Tier 2:** use introspection + `execute_graphql` (this skill).
**Tier 3:** direct curl/httpx fallback — see [skills/api-troubleshoot/pipefy-api-fallback/SKILL.md](../../api-troubleshoot/pipefy-api-fallback/SKILL.md).

---

## Tools

| Tool (MCP) | CLI | Read-only | Purpose |
|------------|-----|-----------|---------|
| `introspect_type` | `pipefy introspect type` | Yes | Type shape: `fields`, `inputFields`, `enumValues`. Optional `max_depth`. |
| `introspect_query` | `pipefy introspect query` | Yes | Root query arguments and return type. Optional `max_depth`. |
| `introspect_mutation` | `pipefy introspect mutation` | Yes | Root mutation arguments and return type. Optional `max_depth`. |
| `search_schema` | `pipefy introspect schema search` | Yes | Keyword search on type names/descriptions. Optional `kind` filter. |
| `execute_graphql` | `pipefy graphql exec` | No | Execute arbitrary GraphQL. Queries ungated. Mutations: MCP two-step with `confirmation_token`; CLI `--yes`. |
| `get_organization` | `pipefy org get` | Yes | Load organization info (name, plan, UUID, member count, pipe count). |
| `list_organizations` | `pipefy org list` | Yes | List organizations the caller can access — no id required. The zero-knowledge entry point for org discovery. |

---

## The `include_parsed` flag

`execute_graphql`, `introspect_type`, `introspect_mutation`, `introspect_query`, and `get_organization` all accept an optional `include_parsed: bool` (default `false`).

- **Default (`false`):** response is `{ success, result }` where `result` is the raw GraphQL JSON as a **string**.
- **`true`:** response includes **both** `result` (the raw JSON string) AND `data` (the parsed dict). Drill into `data` programmatically; keep `result` to forward verbatim.

Use `include_parsed=true` whenever you plan to read nested fields (e.g. iterating over `phases[].fields[]`). Leave it off for one-shot reads where the raw string is sufficient.

## `max_depth` (introspect_type / query / mutation)

MCP tools accept `max_depth` (default `1`). CLI: `--max-depth`.

- **`1`** — type/field info only (no inlined sub-types).
- **`2+`** — resolves referenced input/output types inline (`resolvedType`), so one call can replace introspecting the mutation then each input type separately.

Example (CLI):

```bash
pipefy introspect mutation createCard --max-depth 2 --json
```

Example (MCP):

```
introspect_mutation mutation_name="createCard" max_depth=2 include_parsed=true
```

Scalars (`ID`, `String`, `Int`, …) are never expanded.

## `kind` on `search_schema`

Optional filter: `OBJECT`, `INPUT_OBJECT`, `ENUM`, `SCALAR`, `INTERFACE`, `UNION`.

```
search_schema keyword="automation" kind="INPUT_OBJECT"
```

```bash
pipefy introspect schema search automation --kind INPUT_OBJECT --json
```

---

## When to use introspection

- A dedicated tool returned an error and you need to understand why — introspect the input type to check argument names/types.
- Before creating fields: `introspect_type('CreatePhaseFieldInput')` to discover valid `type` enum values.
- Before using `extra_input`: introspect the corresponding input type to find optional keys.
- Unknown mutation signature: `introspect_mutation('createSomething')` before `execute_graphql`.
- Schema exploration: `search_schema('automation')` to find related types and inputs.

## When to use `execute_graphql`

- No dedicated MCP tool exists for the operation.
- A dedicated tool failed and you've used introspection to understand the correct payload.
- Ad-hoc queries like resolving an org UUID via `pipe(id: $id) { organization { uuid } }`.
- Complex nested queries that no single tool covers.

**Always prefer dedicated MCP tools.** They validate inputs, handle pagination, and format errors consistently. `execute_graphql` is the fallback when dedicated tools can't solve the problem. Queries are ungated; MCP mutations need the two-step `confirmation_token`.

---

## Steps — discover a mutation signature

1. **Search for the mutation by keyword:**

   ```
   search_schema keyword="label"
   ```

2. **Get the full mutation signature:**

   ```
   introspect_mutation mutation_name="createLabel"
   ```

3. **Discover input type fields:**

   ```
   introspect_type type_name="CreateLabelInput"
   ```

4. **Execute the mutation (CLI):**

   ```bash
   pipefy graphql exec --query "mutation …" --vars '{"input":{…}}' --yes --json
   ```

   > **Mutations:** the CLI exits with code 2 unless `--yes` is passed (guardrail for agents and scripts). It also exits 2, with or without `--yes`, when the document is too deeply nested to parse: nothing is sent, because a document that cannot be classified could carry an unconfirmed mutation. `execute_graphql` refuses the same document with an error payload.

5. **Execute the mutation (MCP):** two-step. The first call returns a preview with `confirmation_token` and does not mutate. The preview names the mutation; it does not claim the write is irreversible, because this server cannot tell create from delete. Resend the call unchanged with `confirm=true` and the token; if the document changed, the response is a fresh preview whose token is bound to the new document.

   ```
   execute_graphql query="mutation CreateLabel($input: CreateLabelInput!) { createLabel(input: $input) { label { id name } } }" variables='{"input": {"pipe_id": 67890, "name": "Urgent", "color": "#FF0000"}}'
   ```

   Then after the preview:

   ```
   execute_graphql query="mutation CreateLabel($input: CreateLabelInput!) { createLabel(input: $input) { label { id name } } }" variables='{"input": {"pipe_id": 67890, "name": "Urgent", "color": "#FF0000"}}' confirm=true confirmation_token="<token from preview>"
   ```

---

## Common fallback recipes

Ready-to-use patterns for situations where dedicated tools are insufficient.

### Recipe 1 — Discover valid field types for `create_phase_field`

```
introspect_type('CreatePhaseFieldInput')
```

Look for the `type` field; it references an enum. Introspect the enum to get all valid values.

### Recipe 2 — Get full behavior config of an AI agent

`get_ai_agent` returns behavior headers only. To inspect the full config (`event_params`, `actionParams`, `actionsAttributes`):

```
execute_graphql query='query($uuid: ID!) { aiAgent(uuid: $uuid) { uuid name instruction behaviors { id name active event_id event_params { to_phase_id triggerFieldIds fromPhaseId } action_params { aiBehaviorParams { instruction referencedFieldIds actionsAttributes { name actionType referenceId metadata { destinationPhaseId pipeId fieldsAttributes { fieldId inputMode value } } } } } } } }' variables='{"uuid":"<agent-uuid>"}'
```

### Recipe 3 — Find a card by title (not possible with `find_cards`)

`find_cards` only searches custom field values. To search by title:

```
execute_graphql query='query($pipeId: ID!, $first: Int) { cards(pipe_id: $pipeId, first: $first) { edges { node { id title current_phase { name } } } } }' variables='{"pipeId":"<pipe-id>","first":50}'
```

Filter by title client-side. For large pipes, paginate with `after`.

### Recipe 4 — Discover what `extra_input` accepts for any mutation

When a tool accepts `extra_input` (e.g. `create_automation`, `update_label`), discover all optional keys:

```
introspect_mutation('createAutomation')     # find the input type name
introspect_type('CreateAutomationInput')    # see all inputFields
```

Compare with the tool's primary arguments to know which keys are additive via `extra_input`.

### Recipe 5 — Discover organization IDs

To answer "which organizations do I have access to?" with nothing in hand, call `list_organizations` — it needs no id and returns each org's `id`, `uuid`, `name`, and your role. That is the entry point; reach for the GraphQL fallbacks below only when you already have a pipe.

When the user only has a pipe ID and needs its `organization_id`:

```
execute_graphql query='query($id: ID!) { pipe(id: $id) { organization { id uuid name } } }' variables='{"id":"<pipe-id>"}'
```

### Recipe 6 — Update a select field's options after creation

`create_phase_field` does not accept options. Create first, then update. MCP mutations are two-step: preview, then `confirm=true` plus `confirmation_token`. Resend the call unchanged with `confirm=true` and the token; if the document changed, the response is a fresh preview whose token is bound to the new document. CLI `--yes` can stay one-shot.

```
execute_graphql query='mutation($id: ID!, $options: [String!]) { updatePhaseField(input: { id: $id, options: $options }) { phase_field { id label options } } }' variables='{"id":"<field-id>","options":["High","Medium","Low"]}'
```

Then after the preview:

```
execute_graphql query='mutation($id: ID!, $options: [String!]) { updatePhaseField(input: { id: $id, options: $options }) { phase_field { id label options } } }' variables='{"id":"<field-id>","options":["High","Medium","Low"]}' confirm=true confirmation_token="<token from preview>"
```

### Recipe 7 — Check phase transition rules

When `move_card_to_phase` fails with "not a valid target phase":

```
execute_graphql query='query($id: ID!) { phase(id: $id) { id name cards_can_be_moved_to_phases { id name } } }' variables='{"id":"<current-phase-id>"}'
```

Returns the valid destination phases from the current phase.

---

## Optional schema cache

For long-running agent sessions, the MCP can reuse the fetched GraphQL schema across requests instead of re-introspecting on every call. Enable via the `gql_reuse_fetched_graphql_schema` setting (env or settings file). Off by default. After a breaking Pipefy schema change, the process must be restarted to pick up the new schema. Single-session agents rarely benefit — leave it off unless you measure real improvement.

---

## Success criteria

- `introspect_type` returns the complete field list for the input type.
- `execute_graphql` returns the expected data without errors.

## Failure modes

- **`introspect_type` returns `null`** — type name is case-sensitive; try PascalCase (e.g., `CreateLabelInput`, not `create_label_input`).
- **`search_schema` returns many hits** — case-insensitive substring matching; broad keywords like `"card"` flood results. Prefer specific names like `"AiAgent"`, `"FieldCondition"`.
- **`introspect_mutation` is expensive** — fetches all root mutation fields and filters client-side (single large query). Prefer `introspect_type` on the specific input type when you already know the mutation name.
- **`execute_graphql` returns GraphQL errors** — check `path` and `message`; pass `debug=true` on the next call to surface the `correlation_id`.
- **Endpoint confusion** — introspection uses `app.pipefy.com/graphql`; real operations use `api.pipefy.com/graphql`. The MCP server handles this automatically; raw-API users must distinguish (see [api-fallback](../../api-troubleshoot/pipefy-api-fallback/SKILL.md)).

## See also

- [docs/mcp/tools/introspection.md](../../../docs/mcp/tools/introspection.md) — MCP parameters, query/mutation mismatch hints on `execute_graphql`.
- [skills/api-troubleshoot/pipefy-api-fallback/SKILL.md](../../api-troubleshoot/pipefy-api-fallback/SKILL.md) — Tier 3: direct HTTP fallback when MCP is unavailable.
- [skills/pipes-and-cards/pipefy-pipes-and-cards/SKILL.md](../../pipes-and-cards/pipefy-pipes-and-cards/SKILL.md) — most common dedicated tools (prefer over `execute_graphql`).
