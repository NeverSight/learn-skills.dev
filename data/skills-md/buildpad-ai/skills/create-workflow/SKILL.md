---
name: create-workflow
description: Create workflow state machines, content versioning, and multi-stage approval processes for DaaS collections. Sets up workflow definitions, assignments, required fields, and WorkflowButton UI. Use when the user needs content lifecycles (draft/published), approval workflows, or state machine transitions.
argument-hint: "[collection name] [workflow type: simple|review|multi-level|version-based]"
---

# Create Workflow & Versioning

<!-- backend-gate:begin v1 -->
**Establish the backend first.** A Buildpad project's backend is either the Buildpad Engine or
Supabase, and some parts of this file hold for one of them only. Before you act on anything in
this file, find the backend with these steps, in order, and stop at the first step that answers:

1. Read `.buildpad/project.json` at the project root. If it is JSON and its field `backend` is
   `"engine"` or `"supabase"`, that is the backend. If `.buildpad/backend-answer.json` names the
   other backend, tell the developer the two files disagree, and follow `.buildpad/project.json`.
2. Otherwise read `.buildpad/backend-answer.json` in the same way; if its `backend` is
   `"engine"` or `"supabase"`, that is the backend.
3. If a folder named `supabase` at the project root holds a file named `config.toml`, or holds a
   folder named `migrations` that holds a file whose name ends in `.sql`, the backend is Supabase.
4. Otherwise ask the developer once: "Is this project's backend the Buildpad Engine or
   Supabase?" Write the answer to `.buildpad/backend-answer.json` as
   `{"buildpadBackendAnswer": 1, "backend": "engine"}` or
   `{"buildpadBackendAnswer": 1, "backend": "supabase"}`, and ask the developer to commit that
   file. Do not add it to `.gitignore`. Never write `.buildpad/project.json`.

To find the backend, do not open an environment file (`.env`, `.env.*`) or an MCP configuration
file, and do not call a tool that returns project credentials.

Then follow only the parts for that backend. A part starts at a line that holds only a comment
whose text is `buildpad` + `-backend: engine` or `buildpad` + `-backend: supabase`, and ends at the
next line that holds only a comment whose text is `/buildpad` + `-backend`. A comment that merely
mentions a backend is not a part. A file whose first line, after any front matter, holds only a
comment whose text is `buildpad` + `-backend-file: engine` (or `supabase`) holds for that backend
only, and so does every file in a folder named `engine-only` or `supabase-only`. Skip the other
backend's parts and copy no code from them; everything else holds for both. On an Engine project, when this file says that
something is not available, tell the developer so and stop: do not build a substitute.
<!-- backend-gate:end -->

Set up workflow state machines and content versioning for DaaS collections.

## Pre-requisite: Collection Must Exist with Workflow Fields

**Before creating a workflow**, the target collection must already exist and include the workflow fields (Group B from `create-collection` skill). If the collection doesn't exist yet, invoke the `create-collection` skill first, ensuring Group B workflow fields are included.

If the collection already exists but lacks workflow fields, add them using the MCP payload from the [Standard Fields reference](../create-collection/references/standard-fields.instructions.md#group-b-workflow-fields-include-when-collection-uses-workflows) **before** proceeding with workflow definition and assignment.

> **Do NOT create custom status fields or manual state management.** DaaS Workflows are a built-in platform feature. See [Built-in DaaS features](../daas-platform/references/builtin-features.instructions.md) for the full list of features you must not rebuild.

## Handling an Existing `status` (or similar) Field

<!-- buildpad-backend: supabase -->
If the target collection already has a custom lifecycle field (e.g. `status: select-dropdown` with values like `todo`/`in_progress`/`done`), `workflow_state` will be the new source of truth. **DaaS does not support deleting field metadata via the MCP API**, so the existing field must be hidden rather than removed — and there are two follow-up actions you must take, or items will fail to save:

1. **Hide the field AND drop its `required` flag.** Setting `meta.hidden = true` alone is not enough: if `meta.required = true` is left in place, every item create that doesn't supply the old field will 400. Update both at once:
   ```json
   {
     "name": "mcp_daas_fields",
     "arguments": {
       "action": "update",
       "collection": "your_collection",
       "field": "status",
       "data": { "meta": { "hidden": true, "required": false } }
     }
   }
   ```
   Alternatively, set a column-level default in the database so writes that omit the field still satisfy `NOT NULL`.
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
If the target collection already has a custom lifecycle field (e.g. `status: select-dropdown` with values like `todo`/`in_progress`/`done`), `workflow_state` will be the new source of truth. Hide the existing field rather than delete it while code and data still use it — and there are two follow-up actions you must take, or items will fail to save:

1. **Hide the field AND drop its `required` flag.** Setting `meta.hidden = true` alone is not enough: if `meta.required = true` is left in place, every item create that doesn't supply the old field can be refused. Update both at once. On an Engine project the `fields` tool reads the field's name from `data.field`:
   ```json
   {
     "name": "mcp_daas_fields",
     "arguments": {
       "action": "update",
       "collection": "your_collection",
       "data": { "field": "status", "meta": { "hidden": true, "required": false } }
     }
   }
   ```
   Alternatively, give the column a default in the same update (`"schema": { "default_value": "todo" }`) so writes that omit the field still satisfy `NOT NULL`.
<!-- /buildpad-backend -->

2. **Migrate consumers off the old field.** Search the codebase for the old field name and replace with `workflow_state`. Common offenders: `archiveField="status"` / `archiveValue="cancelled"` props on `CollectionList`, custom badges keyed off `item.status`, filter UIs, and seed data. Leaving these in place silently breaks the new lifecycle.

## Workflow-Enabled Collection Requirements

Any collection using workflows MUST have these fields:

| Field               | Type   | Purpose                         | Required Meta                                                                    |
| ------------------- | ------ | ------------------------------- | -------------------------------------------------------------------------------- |
| `workflow_state`    | string | Stores current workflow state   | `interface: "xtr-interface-workflow"`                                            |
| `workflow_instance` | uuid   | Links item to workflow instance | `special: ["m2o"]`, `options.related_collection: "daas_wf_instance"` (a real relation) |

`workflow_state` is the one the engine needs: instances are created from the **assignment**, and the engine finds the state field by its interface. `workflow_instance` is a convenience pointer; it is only filled when it is a real many-to-one (foreign key + `daas_relations` row), which is what `options.related_collection` produces.

## Setup Steps

### 1. Add Workflow Fields to Collection

Add them with the `fields` tool, **after** the collection exists — not inline in the `collections` create call:

```json
{
  "name": "mcp_daas_fields",
  "arguments": {
    "action": "create",
    "data": [
      {
        "collection": "your_collection",
        "field": "workflow_instance",
        "type": "uuid",
        "schema": { "is_nullable": true },
        "meta": {
          "interface": "select-dropdown-m2o",
          "special": ["m2o"],
          "readonly": true,
          "hidden": true,
          "options": {
            "related_collection": "daas_wf_instance",
            "related_field": "id",
            "on_delete": "SET NULL"
          }
        }
      },
      {
        "collection": "your_collection",
        "field": "workflow_state",
        "type": "string",
        "schema": { "is_nullable": true },
        "meta": { "interface": "xtr-interface-workflow", "readonly": true }
      }
    ]
  }
}
```

Three things that go wrong here, all of them silently:

- **Declare the relation with `meta.options.related_collection`, not `schema.foreign_key_table`.** `schema.foreign_key_table` is not read on create (and the Go engine refuses it with 400). The field is created as a bare column with no foreign key and no relation, so `workflow_instance` is never filled.
- **Do not list `workflow_instance` inline in `collections` create (observed on DaaS 0.1.98).** That path gives every `uuid` column `DEFAULT gen_random_uuid()`. Without a relation the column fills with random UUIDs that reference nothing; with a relation every insert fails on the foreign key. Create the collection first, then add the field with the `fields` tool as above.
- **`workflow_state` stays `readonly: true`.** The state must only change through a transition. (On Buildpad UI 3.0.0 a readonly state field renders an inert `WorkflowButton` inside `VForm`/`CollectionForm` — see step 5.)

<!-- buildpad-backend: supabase -->
### 2. Create Workflow Definition

Create in `daas_wf_definition` with `workflow_json`. **Naming convention: state and command names are display strings rendered directly by `WorkflowButton` — use Title Case with spaces ("In Progress", "Submit for Review"), not snake_case identifiers.** They must match exactly across `initial_state`, `states[].name`, and `commands[].next_state`.

```json
{
  "initial_state": "Draft",
  "states": [
    {
      "name": "Draft",
      "commands": [
        {
          "name": "Submit",
          "next_state": "Review",
          "policies": [],
          "actions": []
        }
      ],
      "isEndState": false
    },
    {
      "name": "Review",
      "commands": [
        {
          "name": "Approve",
          "next_state": "Published",
          "policies": [],
          "actions": []
        },
        {
          "name": "Reject",
          "next_state": "Draft",
          "policies": [],
          "actions": []
        }
      ],
      "isEndState": false
    },
    { "name": "Published", "commands": [], "isEndState": true }
  ]
}
```

> **Default behavior: `policies: []` means anyone with collection write access can run the command.** This skill leaves policies empty by default. To gate a command to a specific role, follow the [Locking commands to roles](#locking-commands-to-roles) section below before considering setup complete — or surface to the user that the workflow is unsecured.

### 3. Create Workflow Assignment

Create in `daas_wf_assignment`. The assignment row links a definition to a collection; `filter_rule: {}` means "every item in the collection gets a workflow instance auto-created on insert."

```json
{
  "workflow": "<workflow-definition-uuid>",
  "collection": "your_collection",
  "filter_rule": {}
}
```

> **Field name is `workflow`, not `workflow_definition`.** The row has exactly `workflow`, `collection` and `filter_rule` — no `name`, `status` or `auto_assign` column; sending one fails the create ("Could not find the 'name' column").

> **Exactly one assignment must match each item.** To run different workflows on one collection, give each assignment a `filter_rule` and make the rules mutually exclusive and exhaustive, e.g. `{"amount": {"_lte": 5000}}` and `{"amount": {"_gt": 5000}}`. An item that matches none, or more than one, gets **no instance** and no error — at most a line in the DaaS logs. The rule is evaluated once, when the item is created; later edits do not re-route it.

### 4. (Optional) Generated Supabase Migration

Even though steps 1–3 use MCP only, the local Supabase database also needs the new columns mirrored so app code (and tests) can read/write them. Generate a migration alongside the MCP changes:

```sql
-- supabase/migrations/<timestamp>_add_workflow_to_<collection>.sql
alter table public.<collection>
    add column if not exists workflow_instance uuid null references daas_wf_instance(id) on delete set null,
    add column if not exists workflow_state    text null;

create index if not exists idx_<collection>_workflow_instance on public.<collection> (workflow_instance);
```

Tell the user to commit this file — leaving it uncommitted means teammates' local databases drift from DaaS.
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
### 2. Create Workflow Definition

Create it with `POST /api/workflows` and an administrator's session. The body is `{ "name", "description", "workflow_json" }`, and the route answers 201 with the new definition's id. Change a definition later with `PATCH /api/workflows/:id`. **Naming convention: state and command names are display strings rendered directly by `WorkflowButton` — use Title Case with spaces ("In Progress", "Submit for Review"), not snake_case identifiers.** They must match exactly across `initial_state`, `states[].name`, and `commands[].next_state`.

```json
{
  "name": "Article Approval",
  "description": "Draft, review, publish",
  "workflow_json": {
    "initial_state": "Draft",
    "states": [
      {
        "name": "Draft",
        "commands": [
          {
            "name": "Submit",
            "next_state": "Review",
            "policies": [],
            "actions": []
          }
        ],
        "isEndState": false
      },
      {
        "name": "Review",
        "commands": [
          {
            "name": "Approve",
            "next_state": "Published",
            "policies": [],
            "actions": []
          },
          {
            "name": "Reject",
            "next_state": "Draft",
            "policies": [],
            "actions": []
          }
        ],
        "isEndState": false
      },
      { "name": "Published", "commands": [], "isEndState": true }
    ]
  }
}
```

The route checks only that `initial_state` is set and `states` is an array: check the names yourself (Verify, step 2).

> **Default behavior: `policies: []` means anyone with collection write access can run the command.** This skill leaves policies empty by default. To gate a command to a specific role, follow the [Locking commands to roles](#locking-commands-to-roles) section below before considering setup complete — or surface to the user that the workflow is unsecured.

### 3. Create Workflow Assignment

Create it with `POST /api/workflow-assignments` and an administrator's session. The assignment links a definition to a collection; `filter_rule: {}` means "every item in the collection gets a workflow instance auto-created on insert."

```json
{
  "workflow": "<workflow-definition-uuid>",
  "collection": "your_collection",
  "filter_rule": {}
}
```

> **Field name is `workflow`, not `workflow_definition`.** The assignment has exactly `workflow`, `collection` and `filter_rule`.

> **Exactly one assignment must match each item.** To run different workflows on one collection, give each assignment a `filter_rule` and make the rules mutually exclusive and exhaustive, e.g. `{"amount": {"_lte": 5000}}` and `{"amount": {"_gt": 5000}}`. An item that matches none, or more than one, gets **no instance** and no error — at most a line in the Engine's logs (`/api/logs`). The rule is evaluated once, when the item is created; later edits do not re-route it.

### 4. No Database Mirror

An Engine project has no migrations: the fields created in step 1 are the columns. Write no migration file.
<!-- /buildpad-backend -->

### 5. Add WorkflowButton to UI

```tsx
import { WorkflowButton } from "@/components/ui/workflow-button";

<WorkflowButton
  itemId={itemId}
  collection="articles"
  onTransition={() => refetch()}
/>;
```

Inside a Buildpad form (`VForm` / `CollectionForm`) the state field renders this button by itself and gets the record key from the form as `primaryKey` — a page needs no workflow code. Outside a form, pass `itemId` yourself. Without either, the button treats the item as new and shows no state.

What the button needs in order to work for a **non-admin** user:

- **Read on `daas_wf_instance` and `daas_wf_definition`.** The button reads the item's instance and its definition as the signed-in user. Without these grants it shows `HTTP error! status: 403` and no state. Scope the instance read to the user's own items where that matters (e.g. `{"user_created": {"_eq": "$CURRENT_USER"}}`). Add read on `daas_wf_history` if the app shows history.
- **Nothing on the collection beyond what the user already has.** The transition itself runs with elevated permissions on the server; the command's `policies` / `module_access_keys` are the gate.

Behaviour observed on Buildpad UI 3.0.0 — re-check on a later version before relying on the workarounds:

- A `readonly` (or permission-locked) state field makes the in-form button inert. Exclude the field from the form (`excludeFields={["workflow_state", "workflow_instance"]}`) and render `<WorkflowButton itemId={id} collection="…" />` next to it.
<!-- buildpad-backend: supabase -->
- The button calls relative `/api/…` paths, so the app needs a same-origin proxy for `POST /api/workflow/transition` (the CLI's `api-routes` does not ship one): forward the body to `${DAAS_URL}/api/workflow/transition` with the session's bearer token, as `app/api/items/[collection]/route.ts` does.
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
- The button calls relative `/api/…` paths, so the app needs a same-origin proxy for `POST /api/workflow/transition` (the CLI's `api-routes` does not ship one): forward the body to `<Engine_URL>/api/workflow/transition` with the headers of `getAuthHeaders()` (the signed-in user's access token as `Authorization: Bearer`), as `app/api/items/[collection]/route.ts` does, and pass the Engine's status and body back.
<!-- /buildpad-backend -->
- Commands gated only by `module_access_keys` are offered to every user (the server still refuses them), and commands gated by `policies` are hidden from everyone. Gate with module access keys and expect the 403 for users without the key.

`CollectionForm` disables the whole form — the button included — for a user with no `update` permission on the collection. Approvers who may not edit the record need the standalone button.

To give administrators screens for designing definitions on a diagram, assigning workflows to collections, and inspecting instances and their history, scaffold the Workflows module instead of building pages: see [add-workflows](../add-workflows/SKILL.md).

## Locking Commands to Roles

The default skill output produces an unsecured workflow: **a command with neither `policies` nor `module_access_keys` can be run by any authenticated user who knows the instance id — including on items they cannot read or update.** Leave a command open only when that is acceptable (a "Submit" on the user's own draft usually is, because only they can see the instance).

To restrict a transition to the holders of a policy:

<!-- buildpad-backend: supabase -->
1. Find or create the policy (`mcp_daas_policies`). A policy is the unit you reference from `workflow_json` — not the role.
2. Attach the policy to the role (or user) with `mcp_daas_access`.
3. Put the **policy's own UUID** (`daas_policies.id`) in the command's `policies` array. A user can run the command if they hold any policy listed.

```json
{
  "name": "Approve",
  "next_state": "Published",
  "policies": ["<daas_policies.id of the approver policy>"],
  "actions": []
}
```

> Use the policy id, **not** the `daas_access.id` returned when you attach it. The server compares the list against the ids `get_user_policies` returns; an access-row id never matches, which locks the command for everyone.

Policy UUIDs differ per environment, so prefer module access keys (next section) when the workflow has to be portable.

## Locking Commands to Module Access Keys (alternative / complement)

Instead of (or alongside) policy UUIDs, commands can be gated by named module-level access keys from `daas_module_access_keys`. This is preferred when the capability is already modelled as a key (e.g. the platform seeds `workflow:approve` and `workflow:reject`).

```json
{
  "name": "Approve",
  "next_state": "Published",
  "policies": [],
  "module_access_keys": ["workflow:approve"],
  "actions": []
}
```

`policies` and `module_access_keys` are **OR'd** — the user may execute the command if they satisfy either list. Both can be populated simultaneously.

Use the seeded `workflow:approve` / `workflow:reject` for generic approvals and register your own key (`<domain>:<capability>`, e.g. `purchase:finance_approve`) when a step needs a narrower audience. The Command dialog of the Workflows module edits `policies` only; `module_access_keys` are set through the API and are preserved when a definition is saved from the diagram.

> **Administrators (observed on DaaS 0.1.98):** the transition endpoint checks the grant map only, so an administrator who does not hold the key (or policy) is refused with 403. Grant the key on the admin's policy if admins must run gated commands.

To grant a key to a role:
1. Confirm the key exists in `daas_module_access_keys` (the platform seeds `workflow:approve` and `workflow:reject` by default).
2. Find or create the policy for the role.
3. Set `module_access: { "workflow:approve": true }` on that policy:

```json
{
  "name": "mcp_daas_policies",
  "arguments": {
    "action": "update",
    "id": "<policy-uuid>",
    "data": { "module_access": { "workflow:approve": true } }
  }
}
```

Users whose effective policies OR-merge to `workflow:approve: true` can then run the command without their policy UUID ever appearing in `policies[]`. This makes permission grants portable across environments (no UUID hard-coding).

If the user explicitly opts out of role gating, mention it once in your final summary so they know what was left open.

## Protect the State Field from Direct Writes

A transition is the only legitimate way to change `workflow_state`. Check that a plain item update cannot do it — otherwise anyone with `update` on the collection can PATCH the state to "Approved" and skip every gate.

- **Go engine:** restrict the role's `update` permission `fields` to the business fields (leave out `workflow_state` and `workflow_instance`). The engine applies the field list to every write.
- **Next.js backend (observed on 0.1.98):** the field list is **not enforced** on `/api/items/*` writes, so restricting `fields` is not enough. Add a filter extension on `<collection>.items.update` that rejects a `workflow_state` different from the instance's `current_state` (the engine writes the state *after* it updates the instance, so its own write passes):

```javascript
// mcp_daas_extensions: type "filter", event "<collection>.items.update"
if (!payload || payload.workflow_state === undefined) return payload;
const keys = meta.keys && meta.keys.length ? meta.keys : meta.key ? [meta.key] : [];
const deny = () => { throw new Error('workflow_state can only be changed through a workflow transition'); };
if (keys.length === 0) deny();
const instances = await services.items('daas_wf_instance', { elevated: true });
for (const key of keys) {
  const rows = await instances.readByQuery({
    filter: { collection: { _eq: '<collection>' }, item_id: { _eq: String(key) } },
    limit: 1,
  });
  if (!rows || !rows[0] || payload.workflow_state !== rows[0].current_state) deny();
}
return payload;
```

Do not use a filter extension on this event to *veto* a transition on 0.1.98: an error thrown while the engine writes the state is swallowed, so the instance advances and the item keeps its old state.

## Verify the Workflow Was Set Up Correctly

After running the steps above, confirm the following before reporting success — every failure here is silent:

1. **The instance pointer is a real relation** — `mcp_daas_relations` action: `read`, collection: `<your_collection>`. There must be a row with `many_field: "workflow_instance"` and `one_collection: "daas_wf_instance"`. An empty list means the field was declared with `schema.foreign_key_table` or without `options.related_collection`; delete it and create it again as in step 1.
2. **Definition is valid JSON** — `mcp_daas_items` action: `read`, collection: `daas_wf_definition`. Every `commands[].next_state` must match a `states[].name`, and `initial_state` must be one of them. The API checks only that `initial_state` and a `states` array exist.
3. **Assignments are wired up** — `mcp_daas_items` action: `read`, collection: `daas_wf_assignment`. With several assignments on one collection, check that their `filter_rule`s cannot overlap and leave no gap.
4. **Auto-instance creation works** — create one item (`mcp_daas_items` action: `create`), then **read it back with a second call**: the instance is created by a hook after the insert, so the create response still shows `workflow_state: null`. Confirm `workflow_state` equals the workflow's `initial_state`, and that `workflow_instance` equals the `id` of the `daas_wf_instance` row whose `item_id` is this item. A `workflow_instance` that names no instance means step 1 went wrong. Repeat for one item per assignment.
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
1. Find or create the policy (`mcp_daas_policies`). A policy is the unit you reference from `workflow_json` — not the role.
2. Attach the policy to the role (or user) with `mcp_daas_access`.
3. Put the **policy's own UUID** (`daas_policies.id`) in the command's `policies` array. A user can run the command if they hold any policy listed.

```json
{
  "name": "Approve",
  "next_state": "Published",
  "policies": ["<daas_policies.id of the approver policy>"],
  "actions": []
}
```

> Use the policy id, **not** the `daas_access.id` returned when you attach it. The Engine compares the list against the user's effective policy ids; an access-row id never matches, which locks the command for everyone but administrators.

Policy UUIDs differ per environment, so prefer module access keys (next section) when the workflow has to be portable.

## Locking Commands to Module Access Keys (alternative / complement)

Instead of (or alongside) policy UUIDs, commands can be gated by named module-level access keys from `daas_module_access_keys`. This is preferred when the capability is already modelled as a key (the Engine seeds `workflow:approve` and `workflow:reject`).

```json
{
  "name": "Approve",
  "next_state": "Published",
  "policies": [],
  "module_access_keys": ["workflow:approve"],
  "actions": []
}
```

`policies` and `module_access_keys` are **OR'd** — the user may execute the command if they satisfy either list. Both can be populated simultaneously.

Use the seeded `workflow:approve` / `workflow:reject` for generic approvals and register your own key (`<domain>:<capability>`, e.g. `purchase:finance_approve`) when a step needs a narrower audience — on an Engine project with the `items` tool on `daas_module_access_keys` (see [grant-module-access](../grant-module-access/SKILL.md)). The Command dialog of the Workflows module edits `policies` only; `module_access_keys` are set through the API and are preserved when a definition is saved from the diagram.

> **Administrators:** on an Engine project an administrator passes every gate, so an administrator can run every command without holding the key or the policy.

To grant a key to a role:
1. Confirm the key exists in `daas_module_access_keys` (the Engine seeds `workflow:approve` and `workflow:reject`).
2. Find or create the policy for the role.
3. Set `module_access: { "workflow:approve": true }` on that policy:

```json
{
  "name": "mcp_daas_policies",
  "arguments": {
    "action": "update",
    "id": "<policy-uuid>",
    "data": { "module_access": { "workflow:approve": true } }
  }
}
```

Users whose effective policies OR-merge to `workflow:approve: true` can then run the command without their policy UUID ever appearing in `policies[]`. This makes permission grants portable across environments (no UUID hard-coding).

If the user explicitly opts out of role gating, mention it once in your final summary so they know what was left open.

## Protect the State Field from Direct Writes

A transition is the only legitimate way to change `workflow_state`. Check that a plain item update cannot do it — otherwise anyone with `update` on the collection can PATCH the state to "Approved" and skip every gate.

On an Engine project, restrict the role's `update` permission `fields` to the business fields (leave out `workflow_state` and `workflow_instance`). The Engine applies the field list to every write, so a PATCH cannot change `workflow_state`, while the transition, which writes the state with the Engine's own authority, still moves it. No stored hook is needed.

```json
{ "policy": "<editor-policy-uuid>", "collection": "<collection>", "action": "update", "fields": ["title", "content"] }
```

## Verify the Workflow Was Set Up Correctly

After running the steps above, confirm the following before reporting success — every failure here is silent:

1. **The instance pointer is a real relation** — `mcp_daas_relations` action: `read`, collection: `<your_collection>`. There must be a row with `field: "workflow_instance"` and `related_collection: "daas_wf_instance"`. An empty list means the field was declared without `options.related_collection`; delete it and create it again as in step 1.
2. **Definition is valid JSON** — `GET /api/workflows/<id>`. Every `commands[].next_state` must match a `states[].name`, and `initial_state` must be one of them. The API checks only that `initial_state` and a `states` array exist.
3. **Assignments are wired up** — `GET /api/workflow-assignments`. With several assignments on one collection, check that their `filter_rule`s cannot overlap and leave no gap.
4. **Auto-instance creation works** — create one item (`mcp_daas_items` action: `create`), then **read it back with a second call**: the create response may still show `workflow_state: null`. Confirm `workflow_state` equals the workflow's `initial_state`, and that `workflow_instance` equals the `id` of the `daas_wf_instance` row whose `item_id` is this item (`GET /api/workflow-instances`, filtered on `collection` and `item_id`). A `workflow_instance` that names no instance means step 1 went wrong. Repeat for one item per assignment.
<!-- /buildpad-backend -->
5. **The state cannot be written directly** — as a non-admin user, `PATCH /api/items/<collection>/<id>` with `{"workflow_state": "<any other state>"}`, then read the item: the state must be unchanged.
6. **Gating** — sign in as a user without the key/policy and call `POST /api/workflow/transition` for a gated command: it must answer 403. Then as a user with it: 200, and the item's `workflow_state` follows.

There is no MCP action for running a transition; use `POST /api/workflow/transition` with a user's session (`{ "workflowInstanceId": "<daas_wf_instance.id>", "commandName": "<command>" }`). MCP item deletes are disabled by default, so remove probe rows through the REST API or the app.

Surface any failures here to the user — do not stop at "the MCP calls returned 200."

## Common Patterns

- **Simple Draft/Published**: 2 states, 2 commands
- **Content Review**: draft → under_review → published/rejected
- **Multi-Level Approval**: draft → manager_review → director_review → published
- **Version-Based**: Each version has its own workflow state

## Hooks

```typescript
import { useWorkflowAssignment } from "@/lib/buildpad/hooks";
import { useVersions, useWorkflowVersioning } from "@/lib/buildpad/hooks";
```

## References

- [Workflow JSON schema](references/workflow-schema.instructions.md)
- [Workflow versioning](references/workflow-versioning.instructions.md)
- [Workflow components](references/workflow-components.instructions.md)
