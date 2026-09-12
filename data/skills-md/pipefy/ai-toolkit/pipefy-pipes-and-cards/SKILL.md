---
name: pipefy-pipes-and-cards
description: >
  Use this skill when the user wants to read, create, update, or delete
  pipes, phases, phase fields, labels, cards, comments, or field conditions.
  Covers 40 MCP tools for the core pipe and card lifecycle. Use the
  seed-pipe-across-phases workflow when populating empty phases for demos or QA.
tags: [pipefy, pipes, cards, phases, fields, labels, comments, field-conditions]
---

# Pipes & Cards

Read, create, update, and delete pipes, phases, phase fields, labels, cards, attachments, and field conditions. **40 MCP tools.**

---

## Cross-cutting patterns

- **Field types** are not validated locally — use `introspect_type` (e.g., on `CreatePhaseFieldInput`) for allowed values.
- Most write tools support `debug=true` on errors (returns GraphQL codes + `correlation_id`).
- `extra_input` merges extra API keys (camelCase); keys that duplicate primary arguments are ignored.
- **Phase connections are UI-only.** Creating or reordering phases does not wire Phase Connections / `allowed_phases`. Configure edges in the Pipefy UI; use `get_phase_allowed_move_targets` before moves. The API cannot add transition edges.
- **Verify-after-write.** After create/update, re-read with the matching get tool (`get_pipe`, `get_card`, `get_phase_fields`, etc.) before reporting success. Do not treat the write response alone as proof.
- **Destructive MCP deletes** are two-step: the preview includes `confirmation_token`; echo it with `confirm=true` on the second call. CLI uses `--yes`.

---

## Pipe operations

| Tool (MCP) | CLI | Read-only | Purpose |
|------------|-----|-----------|---------|
| `get_pipe` | `pipefy pipe get <id>` | Yes | Fetch pipe metadata including phases and fields. |
| `search_pipes` | `pipefy pipe list` | Yes | Search by name pattern. |
| `create_pipe` | `pipefy pipe create` | No | Create a new pipe in the org. |
| `update_pipe` | `pipefy pipe update <id>` | No | Rename or change pipe settings. |
| `delete_pipe` | `pipefy pipe delete <id>` | No | **Two-step destructive.** |
| `clone_pipe` | `pipefy pipe clone <id>` | No | Clone an existing pipe. |
| `get_pipe_members` | `pipefy member list --pipe <id>` | Yes | List members of a pipe. |

### Steps — create a pipe with phases

1. **Create the pipe:**

   MCP: `create_pipe name="Customer Onboarding" organization_id=123`

   CLI: `pipefy pipe create --name "Customer Onboarding" --org 123`

2. **Add phases** — call `create_phase` for each phase (see Phase section below). Omit `index` to append after existing workflow phases, or pass a **1-based** `index` to insert among phases returned by `get_pipe`. Prefer `1` or higher; `index: 0` creates a phase that does not appear in `get_pipe`'s `phases` list. `index` only controls order — it does **not** wire Phase Connections / `allowed_phases` (configure those in the Pipefy UI; use `get_phase_allowed_move_targets` before moves).

3. **Add start form fields** — call `create_phase_field` on the start form phase.

---

## Phase operations

| Tool (MCP) | CLI | Read-only | Purpose |
|------------|-----|-----------|---------|
| `get_pipe` | `pipefy phase get <id>` | Yes | Phase metadata: use `get_pipe` (phases in the response) via MCP, or `pipefy phase get` on the CLI for a single phase. |
| `create_phase` | `pipefy phase create` | No | Add a phase to a pipe. |
| `update_phase` | `pipefy phase update <id>` | No | Rename, reorder, set done flag. |
| `delete_phase` | `pipefy phase delete <id>` | No | **Two-step destructive.** |
| `get_phase_allowed_move_targets` | `pipefy phase targets <id>` | Yes | Valid destination phases before `move_card_to_phase` (UI-configured edges only). |
| `get_phase_cards_count` | `pipefy phase count <id>` | Yes | Native per-phase card count via `get_phase`. |
| `get_phase_cards` | `pipefy phase cards <id>` | Yes | Paginated cards in a phase (`--first`, `--after`, optional `--include-fields`). |

---

## Seed pipe across phases

Use this workflow to place at least one card in each workflow phase (demos, QA checklists, chaos pipes) **without** `execute_graphql`. Transition edges must already exist in the Pipefy UI.

### Tools needed

| Tool (MCP) | CLI | Read-only |
|------------|-----|-----------|
| `get_pipe` | `pipefy pipe get <pipe_id>` | Yes |
| `get_phase_cards_count` | `pipefy phase count <phase_id>` | Yes |
| `create_card` | `pipefy card create <pipe_id> --phase-id <id>` | No |
| `get_phase_cards` | `pipefy phase cards <phase_id>` | Yes |
| `get_phase_allowed_move_targets` | `pipefy phase targets <phase_id>` | Yes |
| `move_card_to_phase` | `pipefy card move <card_id> --phase <id>` | No |

Before `move_card_to_phase`, call `get_phase_allowed_move_targets`. On a required empty field, MCP may return `success: false` naming the field (optional hide hint); CLI stays raw GraphQL.

### Steps

1. **Load phase IDs** — `get_pipe(pipe_id)` → collect `phases[].id` for workflow phases. Omit `phase_id` on `create_card` for start-form intake.

   MCP: `get_pipe pipe_id="306996634"`

   CLI: `pipefy pipe get 306996634 --json`

2. **Find empty phases** — for each candidate `phase_id`, call `get_phase_cards_count`. Target phases where `cards_count` is 0 (if the start form shows 0 but you suspect cards, call `get_phase_cards` before creating duplicates).

   MCP: `get_phase_cards_count phase_id="340012345"`

   CLI: `pipefy phase count 340012345 --json`

3. **Create cards in empty phases** — loop `create_card` with `phase_id` (and `skip_elicitation=true` for agent seeding). When `fields` is non-empty, keys are filtered via `get_phase_fields(phase_id)` and `get_start_form_fields(pipe_id)`.

   MCP:
   ```
   create_card pipe_id="306996634" phase_id="340012345" skip_elicitation=true title="Seeded"
   ```

   CLI:
   ```bash
   pipefy card create 306996634 --phase-id 340012345 --title "Seeded"
   ```

4. **Verify inventory** — `get_phase_cards(phase_id, first=50)` and confirm expected card IDs/titles.

   CLI: `pipefy phase cards 340012345 --json`

5. **Before moves** — on the card's current phase, `get_phase_allowed_move_targets` then `move_card_to_phase` only to an `allowed_phases[].id`.

   MCP: `get_phase_allowed_move_targets phase_id="<current_phase_id>"`

   CLI: `pipefy phase targets <current_phase_id> --json`

### Success criteria

- Every targeted phase reports `cards_count >= 1` (or `get_phase_cards` lists the seeded cards).
- Moves use only phases returned in `allowed_phases`.

### Failure modes

- **Empty `allowed_phases`:** configure **Phase → Connections** in the Pipefy UI; the API cannot add edges.
- **Unexpected empty count:** use `get_phase_cards` to list cards before creating duplicates.

---

## Phase field operations

| Tool (MCP) | CLI | Read-only | Purpose |
|------------|-----|-----------|---------|
| `get_phase_fields` | `pipefy field list --phase <id>` | Yes | List fields on a phase. |
| `get_start_form_fields` | `pipefy pipe start-form <pipe_id>` | Yes | List start-form fields for card creation. |
| `create_phase_field` | `pipefy field create --phase <id>` | No | Add field to a phase. |
| `update_phase_field` | `pipefy field update <id>` | No | Rename, reorder, change required flag. |
| `delete_phase_field` | `pipefy field delete <id>` | No | **Two-step destructive.** |

**Discover field types:**

MCP: `introspect_type type_name="CreatePhaseFieldInput"`

This returns valid `type` enum values and their descriptions.

---

## Card operations

| Tool (MCP) | CLI | Read-only | Purpose |
|------------|-----|-----------|---------|
| `get_card` | `pipefy card get <id>` | Yes | Title, phase, pipe, optional fields. Does not return labels or assignees. |
| `get_cards` | `pipefy card list --pipe <id>` | Yes | Paginated card list by pipe. |
| `find_cards` | `pipefy card find --pipe <id>` | Yes | Filter by a single field value. |
| `create_card` | `pipefy card create <pipe_id>` | No | Default: start form. Optional `--phase-id` / `phase_id` creates in that phase; interactive clients may elicit start-form fields unless `skip_elicitation=true`. |
| `fill_card_phase_fields` | `pipefy card fill <id> --phase <id>` | No | Fill phase fields non-interactively; filters to editable IDs. Uses `--fields` JSON object; for ad-hoc updates use `card update --field-updates` (JSON array). |
| `update_card` | `pipefy card update <id>` (`--field-updates` = `updateFieldsValues`) | No | Update title, assignees, labels, due date, or fields. For list-valued **fields** (connections, attachments, checklists), prefer `--field-updates` / `field_updates` with `operation` ADD/REMOVE. Pipe labels and assignees are card attributes (`label_ids` / `assignee_ids`, replace-all), not fields — see Label operations. If `field_updates` is set, attribute args are discarded. For connectors, send related **card ids**. |
| `update_card_field` | *(MCP only; no direct CLI twin — use `card update --field-updates`)* | No | Single-field `updateCardField`; list-valued fields are **replace-all**. For connectors, values are related **card ids** (not display titles). Do not rebuild from `get_card` `value` (titles only); read ids via `get_card_relations`. Prefer `update_card` + ADD/REMOVE for fields. Pipe labels use `label_ids`, not this tool. |
| `move_card_to_phase` | `pipefy card move <card_id> --phase <id>` | No | Call `get_phase_allowed_move_targets` first. On required empty field, MCP may return `success: false` naming the field (optional hide hint). |
| `delete_card` | `pipefy card delete <id>` | No | **Two-step destructive.** |
| `add_card_comment` | `pipefy card comment add <id>` | No | Add a text comment to a card. |
| `update_comment` | `pipefy card comment update` | No | Update an existing card comment. |
| `delete_comment` | `pipefy card comment delete` | No | **Two-step destructive.** |
| `upload_attachment_to_card` | `pipefy attachment upload --card` | No | Attach a file to an attachment field (`field_id` = slug). Exactly one source: `file_path` (local; local profile only) or `file_url` (downloaded, SSRF-guarded; any profile — required on the hosted server). See [`pipefy-attachments`](../../attachments/pipefy-attachments/SKILL.md). |

### Steps — create a card

1. **Get start form fields** (required — never skip):

   MCP: `get_start_form_fields pipe_id=67890`

   CLI: `pipefy pipe start-form 67890 --json`

2. **Create the card with fields:**

   MCP:
   ```
   create_card pipe_id=67890 title="My Card" fields_attributes='[{"field_id":"field_slug","field_value":"value"}]'
   ```

   CLI:
   ```bash
   pipefy card create 67890 --title "My Card" --fields '{"field_slug":"value"}'
   ```

3. **Report result** with card ID and link: `https://app.pipefy.com/open-cards/<CARD_ID>`

### Pagination for get_cards

```
get_cards pipe_id=67890 first=50 after=<endCursor>
```

Read `pageInfo.hasNextPage` and `pageInfo.endCursor` from the response; pass `after=<endCursor>` for the next page.

---

## Label operations

| Tool (MCP) | CLI | Read-only | Purpose |
|------------|-----|-----------|---------|
| `get_labels` | `pipefy label list --pipe <id>` | Yes | List pipe labels. |
| `create_label` | `pipefy label create` | No | Create a label with a color. |
| `update_label` | `pipefy label update <id>` | No | Rename or recolor. |
| `delete_label` | `pipefy label delete <id>` | No | **Two-step destructive.** |

These tools manage label definitions on the pipe. Applying a pipe label to a card is `update_card(label_ids=[...])`, which **replaces** the card's whole label list: include every id that should remain; do not send only the new one. `get_card` does not return labels — read current ids via `execute_graphql` (`card(id: ...) { labels { id } }`), merge, then write. `field_updates` with `operation` ADD/REMOVE is for list-valued **fields**, not for card-attribute labels. When the user wants a label applied **automatically** ("mark it late when it goes past the due date"), stop and read [Applying a label has no automation action](../../automations/pipefy-automations/SKILL.md#applying-a-label-has-no-automation-action): no automation action does it, and driving `update_card` over a set of cards makes the agent the runtime instead of the process.

---

## Field condition operations

| Tool (MCP) | CLI | Purpose |
|------------|-----|---------|
| `get_field_conditions` | `pipefy field-condition list --phase <id>` | List all field conditions on a phase. |
| `get_field_condition` | `pipefy field-condition get` | Load one field condition by ID. |
| `create_field_condition` | `pipefy field-condition create` | Create show/hide rule. After create, verifies the rule on the requested phase (`verified: true`); missing/wrong phase → `success: false` with `error.details.condition_id` (two-step `delete_field_condition` with `confirmation_token` before recreating); if verify reads are inconclusive, may return success with a warning (verification unavailable). |
| `update_field_condition` | `pipefy field-condition update` | Update condition action or rule (MCP rejects required+hide when top-level `actions` is set; `actions` in `extra_input` → `INVALID_ARGUMENTS`; CLI still raw). |
| `delete_field_condition` | `pipefy field-condition delete` | **Two-step destructive.** |

Do not hide a required field — MCP rejects `hide`/`hidden` on `required=true` (CLI still raw SDK; see `docs/parity.md`); clear `required` first.

---

## Success criteria

- Pipe and phases visible in Pipefy UI.
- `get_pipe` returns the new pipe ID and phases.
- Cards created via `create_card` appear in the pipe's first phase.

## Failure modes

- **`create_field_condition` fails with missing/wrong phase:** use `error.details.condition_id` (or the id in the message) with two-step `delete_field_condition` (echo `confirmation_token`) before recreating; do not blind-retry create on the same requested phase.
- **`create_card` fails with missing required fields:** call `get_start_form_fields` first to discover required `field_id` values.
- **`create_card` / write reports failure (empty or unclear message):** do not blind-retry. Re-read `get_cards` / `get_phase_cards_count` (or pipe `cards_count`) before any retry — see [Ambiguous write failure](../../api-troubleshoot/pipefy-api-fallback/SKILL.md#ambiguous-write-failure-re-read-before-retry).
- **Connections missing after a connector field update:** `update_card_field` is replace-all — writing one related card id drops the rest (same replace-all applies to other list-valued fields: attachments, checklists). Prefer `update_card` / CLI `card update --field-updates` with `operation` ADD/REMOVE and related **card ids**. Do not rebuild a full list from `get_card` `value` (display titles only); for REMOVE or a safe full rewrite, get current related-card ids from `get_card_relations` (or GraphQL `array_value`). For *writes* via a pipe relation (not a connector field), use `create_card_relation` / `delete_card_relation` — see `skills/relations/`. Pipe labels and assignees are not fields: use `update_card(label_ids=)` / `assignee_ids` (replace-all); `field_updates` ADD cannot address them.
- **`create_phase_field` rejects type:** call `introspect_type type_name="CreatePhaseFieldInput"` to get valid values.
- **Delete fails with preview error:** expected. Show the preview to the user and get their approval, then call again with `confirm=true` and the preview's `confirmation_token`. CLI uses `--yes`.

## See also

- `skills/relations/` — link pipes and cards across workflows.
- `skills/automations/` — add automation rules to a pipe.
- `skills/introspection/` — discover field types and mutation signatures.
- `docs/mcp/tools/identifiers.md#field-references-slug-vs-internal_id` — canonical map of which tool/argument expects slug vs `internal_id` vs uuid vs numeric id (e.g. `update_card_field` uses a field slug).
