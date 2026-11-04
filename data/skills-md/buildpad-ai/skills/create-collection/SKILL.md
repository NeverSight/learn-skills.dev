---
name: create-collection
description: Generate a complete collection with its schema, API routes, UI pages (list + form), TypeScript types, and tests. Creates everything needed for a new data entity in a DaaS application. Use when the user wants to add a new collection, table, entity, or data model to the project.
argument-hint: "[collection name] [fields as name:type pairs]"
---

# Create Collection

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

<!-- buildpad-backend: supabase -->
Generate a complete collection module with API routes, UI pages, database migration, and tests.
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
Generate a complete collection module with its schema, API routes, UI pages, and tests.
<!-- /buildpad-backend -->

> **BEFORE generating ANY `.tsx` files** (list pages, form pages, components), you MUST `read_file` the Buildpad component reference at `.github/skills/buildpad-reference/SKILL.md`. This loads the full 40+ component catalog with import paths and usage patterns. Skipping this step leads to raw Mantine usage violations.

## What Gets Created

<!-- buildpad-backend: supabase -->
1. **Database Migration** — `supabase/migrations/[timestamp]_create_[name].sql`
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
1. **Schema** — the collection and its fields, created through the Engine's API or MCP tools (an Engine project has no migration file)
<!-- /buildpad-backend -->
2. **API Routes** — `app/api/items/[name]/route.ts` + `[id]/route.ts`
3. **Content Module Pages** — `app/content/[name]/page.tsx` (list) + `[id]/page.tsx` (form)
4. **Form** — Uses `CollectionForm` from Buildpad (NOT custom)
5. **Layout** — Uses `ContentLayout` + `ContentNavigation` from Buildpad
6. **API Tests** — `tests/api/[name].spec.ts`
7. **Page Tests** — `tests/pages/[name].spec.ts`

## Field Type Mapping

| Field Type         | DB Column       | Buildpad Component  |
| ------------------ | --------------- | ------------------- |
| `text`             | text            | Input               |
| `number`           | integer/numeric | Input (type=number) |
| `boolean`          | boolean         | Toggle              |
| `date`             | timestamptz     | DateTime            |
| `select`           | text + CHECK    | SelectDropdown      |
| `richtext`         | text            | RichTextHtml        |
| `file`             | uuid FK         | FileImage           |
| `m2o:[collection]` | uuid FK         | ListM2O             |
| `m2m:[collection]` | junction table  | ListM2M             |

## Standard Field Groups — Decision Tree

Before creating any collection, determine which field groups to include:

```
For EVERY new collection:
├── 1. ALWAYS add Group A (Audit Fields)
│     → user_created, date_created, user_updated, date_updated
│
├── 2. Does this collection need a state machine / approval workflow?
│     ├── YES → Add Group B (Workflow Fields) + invoke create-workflow skill after
│     └── NO  → Skip Group B
│
└── 3. Does this collection need multi-tenancy / scope isolation?
      ├── YES → Add Group C (Scope Field) + invoke manage-scope skill after
      └── NO  → Skip Group C
```

<!-- buildpad-backend: supabase -->
> **🔴 CRITICAL: Group A is NOT optional.** Every collection must have audit fields. The DaaS platform does NOT auto-add them — you must include them in every `mcp_daas_collections` create or `mcp_daas_fields` create call.

See [Standard Collection Fields reference](references/standard-fields.instructions.md) for copy-pasteable MCP JSON payloads for all three groups.
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
> **🔴 CRITICAL: Group A is NOT optional.** Every collection must have audit fields. The Engine does NOT auto-add them — create `date_created` and `date_updated` with the collection (`POST /api/collections`, fields inline) and `user_created` / `user_updated` with the `fields` tool right after. The Engine fills `user-created`, `user-updated` and `date-updated` on every write, but `date-created` only from the column default, so `date_created` needs `"schema": { "default_value": "NOW()" }`.
>
> On an Engine project collections, fields, relations, roles, policies and permissions are created through the Engine's API (`/api/collections`, `/api/fields/:collection`, `/api/relations`, `/api/roles`, `/api/policies`, `/api/access`, `/api/permissions`) or its MCP tools `collections`, `fields`, `relations`, `roles`, `policies`, `access` and `permissions`. Access is roles, policies and permissions: a permission belongs to a policy, and a policy is attached to a role or a user. The MCP `collections` and `fields` tools keep a field's name, type and `meta` but not its `schema` block (default, not-null, length): set those through `POST /api/fields/:collection` with an administrator's session.

See [Standard Collection Fields reference](references/standard-fields.instructions.md) for copy-pasteable payloads for all three groups.
<!-- /buildpad-backend -->

### Group A: Audit Fields (ALWAYS include)

| Field          | Type      | Special Attribute | Purpose                            |
| -------------- | --------- | ----------------- | ---------------------------------- |
| `user_created` | uuid      | `user-created`    | Auto-set to current user on create |
| `date_created` | timestamp | `date-created`    | Auto-set to current time on create |
| `user_updated` | uuid      | `user-updated`    | Auto-set to current user on update |
| `date_updated` | timestamp | `date-updated`    | Auto-set to current time on update |

### Group B: Workflow Fields (include when collection uses workflows)

| Field               | Type   | Required Meta                                               | Purpose                         |
| ------------------- | ------ | ----------------------------------------------------------- | ------------------------------- |
| `workflow_instance` | uuid   | `special: ["m2o"]`, `options.related_collection: "daas_wf_instance"` | Links item to workflow instance |
| `workflow_state`    | string | `interface: "xtr-interface-workflow"`, `readonly: true`              | Stores current workflow state   |

<!-- buildpad-backend: supabase -->
Add `workflow_instance` (and the `user_created` / `user_updated` audit fields) with the `fields` tool after the collection exists, declaring the relation in `meta.options.related_collection` — not inline in the `collections` create call and not with `schema.foreign_key_table`. See the [Standard Fields reference](references/standard-fields.instructions.md) for why.

In addition to the MCP field create, add the columns to the local Supabase migration so the database mirrors DaaS:

```sql
alter table public.<collection>
    add column if not exists workflow_instance uuid null references daas_wf_instance(id) on delete set null,
    add column if not exists workflow_state    text null;
create index if not exists idx_<collection>_workflow_instance on public.<collection> (workflow_instance);
```
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
Add `workflow_instance` (and the `user_created` / `user_updated` audit fields) with the `fields` tool after the collection exists, declaring the relation in `meta.options.related_collection` — not inline in the collection create and not with `schema.foreign_key_table`, which the Engine refuses. The `fields` tool reads the field's name from `data.field`. See the [Standard Fields reference](references/standard-fields.instructions.md).

There is nothing to mirror on an Engine project: the field the Engine creates is the column.
<!-- /buildpad-backend -->

After adding Group B fields, proceed to the **`create-workflow` skill** to define workflow definition, assignment, and UI integration.

<!-- buildpad-backend: supabase -->
### Group C: Multi-Tenancy Field (include when collection is scoped)

| Field          | Type | Required Meta                                                               | Purpose            |
| -------------- | ---- | --------------------------------------------------------------------------- | ------------------ |
| `resource_uri` | text | `special: ["m2o"]`, `foreign_key_table: "daas_scope_items"`, FK on uri_path | Scope partitioning |

After adding Group C field, proceed to the **`manage-scope` skill** to register the collection in scope config.

<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
### Group C: Multi-Tenancy Field (include when collection is scoped)

| Field          | Type   | Required Meta                                                                                   | Purpose            |
| -------------- | ------ | ----------------------------------------------------------------------------------------------- | ------------------ |
| `resource_uri` | string | `special: ["m2o"]`, `options.related_collection: "daas_scope_items"`, `options.related_field: "uri_path"` | Scope partitioning |

On an Engine project the project is one tenant. Every scope hierarchy begins below the project's tenant node: create no scope type without a parent and no scope item without a parent. Scope types, items and collection settings are managed through `/api/scope/types`, `/api/scope/items` and `/api/scope/collection-config` with an administrator's session; the MCP `scope` tool, served to an administrator only, assigns a role to a user at a scope (`assign_user_role`) and registers a collection as tenanted (`create_config`, the body of `POST /api/scope/collection-config`).

After adding Group C field, proceed to the **`manage-scope` skill** to register the collection in scope config.

<!-- /buildpad-backend -->
<!-- buildpad-backend: supabase -->
## Standard Columns — SQL Migration (when using migration approach)

```sql
id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
date_created timestamptz DEFAULT now(),
date_updated timestamptz,
user_created uuid REFERENCES auth.users(id),
user_updated uuid REFERENCES auth.users(id)
```

> **⚠️ Verify Actual Field Names:** The standard column names above (`date_created`, `date_updated`, etc.) are conventions for new migrations. Existing DaaS collections may use different names (e.g., `created_at`, `updated_at`). **Always check the actual schema** via `mcp_daas_schema` or `mcp_daas_fields` before writing queries. Using a wrong field name in `sort` or `filter` causes a silent **500 error** from the DaaS backend.

<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
## Standard Columns — on an Engine project

An Engine project has no SQL migration: the standard columns are fields created through the Engine.

| Field          | Type      | Set on create                                                      |
| -------------- | --------- | ------------------------------------------------------------------ |
| `id`           | uuid      | `schema.is_primary_key: true` (the Engine gives it `gen_random_uuid()`) |
| `date_created` | timestamp | `schema.default_value: "NOW()"`                                    |
| `date_updated` | timestamp | —                                                                  |
| `user_created` | uuid      | m2o to `daas_users` (`fields` tool)                                |
| `user_updated` | uuid      | m2o to `daas_users` (`fields` tool)                                |

> **⚠️ Verify Actual Field Names:** The standard names above (`date_created`, `date_updated`, etc.) are conventions for new collections. Existing collections may use different names (e.g., `created_at`, `updated_at`; a collection created without fields gets `created_at` and `updated_at`). **Always check the actual schema** via the `schema` or `fields` tool before writing queries. A wrong field name in `sort` or `filter` fails the request.

<!-- /buildpad-backend -->
<!-- buildpad-backend: supabase -->
## API Response Format

```typescript
// Success
{ data: Item | Item[] }
{ data: Item[], meta: { total_count, filter_count } }

// Aggregate (no pagination meta)
{ data: [{ count: { id: 42 }, sum: { amount: 12500 } }] }

// Error
{ errors: [{ message: string, extensions?: { code: string } }] }
```
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
## API Response Format

```typescript
// Success
{ data: Item | Item[] }

// Aggregate (no pagination meta)
{ data: [{ count: { id: 42 }, sum: { amount: 12500 } }] }

// Error
{ errors: [{ message: string, extensions?: { code: string } }] }
```

On an Engine project a create on `/api/items` answers 200, a delete of one item answers 204 with no body and a delete of several answers 200 with a body, and the `meta` query parameter is ignored, so a list carries no `total_count` / `filter_count`. `limit` is capped at 1000.
<!-- /buildpad-backend -->

## Using CollectionForm (preferred for forms)

```tsx
import { CollectionForm } from '@/components/ui/collection-form';

// Create mode
<CollectionForm collection="products" onSuccess={(data) => console.log('Saved:', data)} />

// Edit mode
<CollectionForm collection="products" id={itemId} mode="edit" />
```

## Using CollectionList for ALL Listing Views (MANDATORY)

Every page that renders a list of collection records **MUST** use `CollectionList`. This ensures consistent search, filtering, pagination, permissions, and bulk-action behavior across the entire application.

### CollectionList Props Reference

| Prop                  | Type                                   | Default  | Description                                                     |
| --------------------- | -------------------------------------- | -------- | --------------------------------------------------------------- |
| `collection`          | `string`                               | —        | Collection name (required)                                      |
| `enableSearch`        | `boolean`                              | `true`   | Search bar in toolbar                                           |
| `enableFilter`        | `boolean`                              | `false`  | Inline FilterPanel toggle with active-count badge               |
| `enableSelection`     | `boolean`                              | `false`  | Row selection checkboxes                                        |
| `enableCreate`        | `boolean`                              | `false`  | Create (+) button in toolbar                                    |
| `enableSort`          | `boolean`                              | `true`   | Column sorting                                                  |
| `enableResize`        | `boolean`                              | `true`   | Column resize                                                   |
| `enableReorder`       | `boolean`                              | `true`   | Column drag-and-drop reorder                                    |
| `enableHeaderMenu`    | `boolean`                              | `true`   | Right-click column header menu                                  |
| `enableAddField`      | `boolean`                              | `true`   | Inline "+" button for adding columns                            |
| `enableDelete`        | `boolean`                              | `false`  | Built-in delete with confirmation modal                         |
| `limit`               | `number`                               | `25`     | Items per page (10, 25, 50, 100)                                |
| `tableSpacing`        | `"compact" \| "cozy" \| "comfortable"` | `"cozy"` | Row density                                                     |
| `filter`              | `Record<string, unknown>`              | —        | External DaaS-style filter object                               |
| `archiveField`        | `string`                               | —        | Enable archive filter UI (e.g. `"status"`)                      |
| `archiveValue`        | `string`                               | —        | Value marking items as archived (e.g. `"archived"`)             |
| `unarchiveValue`      | `string`                               | —        | Value marking items as unarchived (e.g. `"draft"`)              |
| `bulkActions`         | `BulkAction[]`                         | `[]`     | Bulk action buttons (permission-gated via `requiredPermission`) |
| `onItemClick`         | `(item) => void`                       | —        | Row click handler (navigate to detail)                          |
| `onCreate`            | `() => void`                           | —        | Create button click handler                                     |
| `onFilterChange`      | `(filter) => void`                     | —        | Filter change callback                                          |
| `onPermissionsLoaded` | `(perms) => void`                      | —        | Permission state callback                                       |
| `onDeleteSuccess`     | `() => void`                           | —        | Callback after successful bulk delete                           |

### Standard List Page Pattern (use for EVERY collection)

```tsx
// app/content/[collection]/page.tsx — collection list view
"use client";
import { use } from "react";
import { useRouter } from "next/navigation";
import { CollectionList } from "@/components/ui";

export default function CollectionPage({
  params,
}: {
  params: Promise<{ collection: string }>;
}) {
  const { collection } = use(params);
  const router = useRouter();

  return (
    <CollectionList
      collection={collection}
      enableSearch
      enableFilter
      enableSelection
      enableCreate
      enableDelete
      enableSort
      enableResize
      enableReorder
      enableHeaderMenu
      limit={25}
      onCreate={() => router.push(`/content/${collection}/+`)}
      onItemClick={(item) => router.push(`/content/${collection}/${item.id}`)}
    />
  );
}
```

### Content Module Layout

```tsx
// app/content/layout.tsx — shared layout with sidebar navigation
import { ContentLayout, ContentNavigation } from "@/components/ui";
import { useCollections } from "@/lib/buildpad/hooks";

// app/content/[collection]/[id]/page.tsx — item form view
import { CollectionForm } from "@/components/ui";
import { isNewItem } from "@/lib/buildpad/utils"; // ALWAYS use isNewItem() for new-item detection
```

See `buildpad-reference` skill for full content module pattern.

<!-- buildpad-backend: supabase -->
## Testing Requirements

All tests MUST pass before the collection is considered complete:

- GET list with pagination
- GET single item by ID
- POST create with validation
- PATCH update with validation
- DELETE item
- Page renders correctly
- Navigation between list and detail
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
## Testing Requirements

All tests MUST pass before the collection is considered complete:

- GET list with pagination
- GET single item by ID
- POST create with validation (the Engine answers 200)
- PATCH update with validation
- DELETE item (the Engine answers 204 with no body)
- Page renders correctly
- Navigation between list and detail
<!-- /buildpad-backend -->

## Post-Generation Validation (MANDATORY)

After generating ALL files for this collection, run the Buildpad-First violation check:

```bash
# Scan generated files for forbidden raw Mantine form/input imports
grep -rn "from '@mantine/form'\|from '@mantine/dates'\|from '@mantine/dropzone'\|<TextInput\|<NumberInput\|<Select \|<Switch \|<Checkbox \|<DatePicker\|<Dropzone" app/ components/ 2>/dev/null
```

**If any matches are found, replace them with Buildpad equivalents before proceeding.**

Quick fix reference:
| Violation | Replace With |
|---|---|
| `<TextInput>` / `<Textarea>` | `Input` / `Textarea` from `@/components/ui` |
| `<Select>` | `SelectDropdown` from `@/components/ui` |
| `<DatePicker>` | `DateTime` from `@/components/ui` |
| `<Switch>` / `<Checkbox>` | `Toggle` / `Boolean` / `SelectMultipleCheckbox` |
| `<Dropzone>` | `Upload` / `Files` from `@/components/ui` |
| `useForm` (@mantine/form) | `VForm` or `CollectionForm` from `@/components/ui` |
| Custom `<Table>` for records | `CollectionList` from `@/components/ui` |

<!-- buildpad-backend: supabase -->
## Scope (Multi-Tenancy) — Adding `resource_uri` to a Collection

If this collection needs to be partitioned by tenant/organization/region, add scope support via `/manage-scope` skill. When enabling scope on a collection:

1. **Add `resource_uri` column with FK constraint:**

```sql
ALTER TABLE public.<collection>
    ADD COLUMN IF NOT EXISTS resource_uri TEXT DEFAULT NULL
    REFERENCES public.daas_scope_items(uri_path) ON DELETE RESTRICT;

CREATE INDEX IF NOT EXISTS idx_<collection>_resource_uri ON public.<collection>(resource_uri);
```

> **FK constraint is required** — it prevents orphaned values and enables M2O nesting (`?fields=resource_uri.name`). Without it, scope item deletions become unsafe.

2. **Register collection in scope config:**

Use `/manage-scope` skill's **Step 4** to register the collection with `field_name: "resource_uri"` and set `inheritance_mode` (exact vs down).

3. **API behavior:**
   - Requests include `X-Resource-Uri` header or `daas_resource_uri` cookie
   - Reads filtered to matching scope items
   - Creates auto-tag items with the active scope
   - Updates/deletes only allowed on items within the active scope
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
## Scope (Multi-Tenancy) — Adding `resource_uri` to a Collection

If this collection needs to be partitioned by organization, department or region, add scope support via `/manage-scope` skill. On an Engine project the project is one tenant. Every scope hierarchy begins below the project's tenant node: create no scope type without a parent and no scope item without a parent. Scope types, items and collection settings are managed through `/api/scope/types`, `/api/scope/items` and `/api/scope/collection-config` with an administrator's session; the MCP `scope` tool, served to an administrator only, assigns a role to a user at a scope (`assign_user_role`) and registers a collection as tenanted (`create_config`, the body of `POST /api/scope/collection-config`).

When enabling scope on a collection:

1. **Add the `resource_uri` field as a many-to-one to `daas_scope_items`:**

```json
{
  "name": "fields",
  "arguments": {
    "action": "create",
    "collection": "<collection>",
    "data": {
      "field": "resource_uri",
      "type": "string",
      "meta": {
        "interface": "select-dropdown-m2o",
        "special": ["m2o"],
        "readonly": true,
        "hidden": true,
        "options": { "related_collection": "daas_scope_items", "related_field": "uri_path", "on_delete": "RESTRICT" }
      }
    }
  }
}
```

> **The relation is required** — its foreign key prevents orphaned values and enables M2O nesting (`?fields=resource_uri.name`). Without it, scope item deletions become unsafe.

2. **Register collection in scope config:**

Use `/manage-scope` skill to register the collection through `/api/scope/collection-config` with `field_name: "resource_uri"`, `inheritance_mode` (`exact` or `down`) and `missing_uri_mode` (`strict` or `reject`).

3. **API behavior:**
   - Requests name the active scope in the `X-Resource-Uri` header
   - Reads filtered to matching scope items
   - Creates stamp the request's scope onto the scope field
   - Updates/deletes only allowed on items within the active scope
   - With `missing_uri_mode: "reject"`, a request without a scope is refused with `MISSING_SCOPE`
<!-- /buildpad-backend -->

## Post-Creation — Next Steps

After creating the collection with its standard fields:

1. **If Group B (Workflow) fields were included** → Invoke the `create-workflow` skill to define the workflow definition, assignment, and add `WorkflowButton` to the item form UI
2. **If Group C (Scope) fields were included** → Invoke the `manage-scope` skill to register the collection in scope config
3. **Audit logging is automatic** — DaaS logs all item create/update/delete operations to `daas_activity`. Do NOT build custom audit trail code. Query audit data via `GET /api/activity?collection=your_collection`

## References

- [Standard Collection Fields](references/standard-fields.instructions.md) — canonical MCP JSON payloads for audit, workflow, and scope fields
<!-- buildpad-backend: supabase -->
- [API route patterns](../create-api-route/references/api-routes.instructions.md)
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
- [API routes](../create-api-route/SKILL.md) — the routes that forward each data call to the Engine
<!-- /buildpad-backend -->
- [Workflow setup](/create-workflow) — define workflow definitions, assignments, and UI after adding Group B fields
- [Multi-Tenancy Scope Setup](/manage-scope) — register scope config after adding Group C field
- [Built-in DaaS features](../daas-platform/references/builtin-features.instructions.md) — features you must NOT rebuild
