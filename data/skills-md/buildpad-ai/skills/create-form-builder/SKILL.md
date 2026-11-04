---
name: create-form-builder
description: Scaffold and use the Buildpad Dynamic Form Builder — a visual drag-and-drop authoring UI (FormBuilder) plus a runtime renderer (DynamicForm) layered on CollectionForm/VForm. An admin arranges a collection's fields into sections, sets width/required/readonly/hidden, and authors conditional logic, saving a reusable FormDefinition into an fb_definitions collection (the schema is never mutated). Use when the user says form builder, build a form, dynamic form, form designer, visual form editor, conditional form, or wants end users to design forms.
argument-hint: "[target collection] [--cwd path/to/project]"
---

# Create with the Dynamic Form Builder

A ready-made `/forms` experience: a **visual form builder** plus a **runtime renderer** on top of the schema-driven [`CollectionForm`/`VForm`](../create-feature/references/vform-usage.instructions.md) runtime. An admin arranges a collection's fields into ordered sections, sets width / required / readonly / hidden, and authors conditional logic, then saves the result as a reusable, named **form definition**. Definitions are stored as items in an ordinary collection and merged onto the live schema at render time via `buildFieldsFromDefinition` — **the schema is never mutated**.

This is a two-step workflow: **author** a definition with `FormBuilder`, then **fill** it with `DynamicForm`. That is why this is a `create-*` workflow skill, not just a component install.

## Relationship to VForm (do not confuse)

- `@buildpad/ui-forms` (**this** — plural) = the Form Builder module.
- `@buildpad/ui-form` (singular) = the low-level `VForm` runtime the builder wraps.

The builder emits fields consumed by `CollectionForm` → `VForm`. Do **not** re-implement VForm's controlled-component pattern here — the runtime handles state and submission. See [vform-usage](../create-feature/references/vform-usage.instructions.md) for the substrate.

## Prerequisite: the definitions collection

Definitions are persisted as items in a single collection (default **`fb_definitions`**, overridable via `formsCollection`). It is an ordinary user collection — **not** a `daas_`-prefixed system collection — and must exist before the builder can save:

| field | type | notes |
| ------------------- | ----------------- | ------------------------------------------------------------------ |
| `id`                | uuid (PK)         | auto |
| `name`              | string            | form name |
| `target_collection` | string            | collection the form targets |
| `key`               | string (nullable) | optional discriminator so multiple forms can share one collection (e.g. per issue type) |
| `definition`        | json              | the `FormDefinition` body |

If the collection is missing, the list and builder render a **`FormsEmptyState`** hint instead of failing. With DaaS **schema rights** that hint offers a one-click **Create collection** action. Use [create-collection](../create-collection/SKILL.md) to provision it explicitly if you prefer, on either kind of project; on a Supabase project [create-migration](../create-migration/SKILL.md) also works (an Engine project has no migrations).

> Authoring (arranging existing fields) needs only item `create`/`update`/`read` on the definitions collection plus `read` on the target collection's schema — **not** admin/DDL rights. Only *provisioning* (creating a collection or a new real column) needs schema rights.

## Installation

The Forms module is **opt-in** — it is not part of `bootstrap`.

```bash
# 1. Add the builder + renderer + /forms pages + useFormDefinitions hook
npx @buildpad/cli@latest add form-builder forms-routes --cwd /path/to/project

# 2. Add the DaaS proxy routes it needs (if not already present)
npx @buildpad/cli@latest add api-routes --cwd /path/to/project
```

> The docs use the shorthand `buildpad add form-builder forms-routes`; the `npx @buildpad/cli@latest add …` form is the equivalent no-install invocation used across these skills.

> **If the CLI command fails, `@buildpad/cli` IS published to npm** — verify with `npm view @buildpad/cli version` before assuming otherwise or reaching for a local clone. The CLI fetches its registry from `raw.githubusercontent.com`, so confirm the environment can reach **both** npm and the GitHub raw CDN. A local clone is only needed for CLI development, never to consume components.

The module must render under the authenticated layout (`app/(authenticated)/` with a `DaaSProviderWrapper`) so `DaaSProvider` header injection (the signed-in user's session token) is in scope — the hooks call `/api/items/*` (and, when provisioning in **proxy** mode, `/api/fields/*` and `/api/collections/*`).

> **On a Supabase project, DaaS CORS must be configured first.** `DynamicForm` (via `CollectionForm`) fetches `/users/me`, `/permissions/me`, and item endpoints from the browser with `credentials: 'include'`. DaaS's default `cors_origins: ["*"]` is **incompatible** with credentialed requests — the browser blocks every preflight (`Access-Control-Allow-Origin header must not be the wildcard '*'`). Set explicit origins first (see [daas-platform](../daas-platform/SKILL.md) "CORS must use explicit origins" — Bugs 17+25 — and [debugging-and-error-recovery](../debugging-and-error-recovery/SKILL.md)). This is not form-builder-specific: it affects every authenticated Buildpad component.
>
> **On an Engine project there is nothing to configure.** On an Engine project the data API accepts requests from any origin and never with cookies, as the project is provisioned. Change no cross-origin setting, and do not add the application's origin anywhere.

## The Routes

```
app/forms/
├── page.tsx            # /forms          — list of saved definitions
├── new/page.tsx        # /forms/new      — create (auto-create or bind existing)
├── [id]/page.tsx       # /forms/[id]     — the FormBuilder editor
└── [id]/fill/page.tsx  # /forms/[id]/fill — render with DynamicForm to create an item
```

## Step 1 — Author with `FormBuilder`

```tsx
// app/forms/new/page.tsx
import { FormBuilder } from "@/components/ui/form-builder";

// Start from scratch — auto-create a full fb_ collection on save (needs schema rights):
<FormBuilder onSaved={(def) => router.push(`/forms/${def.id}`)} />

// Bind to an existing collection (hybrid storage):
<FormBuilder targetCollection="issues" onSaved={(def) => router.push(`/forms/${def.id}`)} />
```

```tsx
// app/forms/[id]/page.tsx — edit an existing definition (target comes from the definition)
<FormBuilder definitionId={id} />
```

| Prop | Type | Purpose |
| ------------------ | -------------------------------- | ------------------------------------------------------------------------------------ |
| `targetCollection` | `string`                         | Required when creating a *bound* form; omit when editing or "start from scratch"       |
| `definitionId`     | `string \| number`               | Edit an existing definition                                                          |
| `formsCollection`  | `string` (default `fb_definitions`) | Definitions collection name                                                       |
| `onSaved`          | `(def: FormDefinition) => void`  | Called after a successful save with the persisted definition                          |

The **Build** tab is a three-pane workspace — field-type palette (+ **Add extra field** + existing collection fields) on the left, the section canvas in the middle, a per-field settings panel (width / required / hidden / conditions) on the right — plus a **Preview** tab that renders the in-progress form live.

## Step 2 — Fill with `DynamicForm`

```tsx
// app/forms/[id]/fill/page.tsx
"use client";

import { use } from "react";
import { useRouter } from "next/navigation";
import { DynamicForm } from "@/components/ui/form-builder";

export default function FillFormPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const router = useRouter();
  return (
    <DynamicForm
      definitionId={id}
      onSuccess={() => router.push("/forms")}
      onCancel={() => router.push("/forms")}
    />
  );
}
```

| Prop | Type | Default | Purpose |
| ------------------- | ----------------------------- | --------------- | ---------------------------------------------------------- |
| `definitionId`      | `string \| number`            | — (required)    | The saved definition to render                             |
| `formsCollection`   | `string`                      | `fb_definitions`| Definitions collection name                                |
| `itemId`            | `string \| number`            | —               | Provide to switch the form to **edit** mode                |
| `onSuccess`         | `(data?) => void`             | —               | Called after a successful create/update                    |
| `onCancel`          | `() => void`                  | —               | Called on cancel                                           |
| `scopeField`        | `string`                      | `'resource_uri'`| Target-collection field holding the scope URI (multi-tenant) |
| `injectActiveScope` | `boolean`                     | `true`          | Inject the active scope URI as a create-time default       |

## The List View & Empty State

```tsx
// app/forms/page.tsx
import { FormsEmptyState, type FormDefinition } from "@/components/ui/form-builder";
import { useFormDefinitions } from "@/lib/buildpad/hooks";

const { list } = useFormDefinitions();
// list().then(setDefinitions).catch(...) — render FormsEmptyState on error/missing collection
```

## Data Model & Hook (quick reference)

- **Hook** `useFormDefinitions()` from `@/lib/buildpad/hooks` → `list`, `get`, `create`, `update`, `remove`, `resolveScreen` (the API keeps the legacy *screen* name for a resolved definition), plus `loading`/`error`. `DEFAULT_FORMS_COLLECTION = 'fb_definitions'`.
- **On an Engine project** a list request returns at most 1000 items (`limit` is capped at 1000), and `remove` is answered `204 No Content` with no body.
- **Types** `FormDefinition`, `FormSection`, `FormFieldConfig` are re-exported from the component barrel `@/components/ui/form-builder` (as used in the list-view example above). `FieldCondition` is the exception — it is deliberately **not** re-exported from the barrel, so import it from `@/lib/buildpad/types`.

For the full data model, conditions cookbook, storage strategies, and multi-tenant scope behaviour, read **[references/form-builder.instructions.md](references/form-builder.instructions.md)**.

## See It Live

Forms Storybook (port 6010): `pnpm --filter @buildpad/ui-forms storybook`. The `FormBuilder (DaaS)` story connects to a real DaaS instance via the storybook-host proxy.

## Related

- [create-collection](../create-collection/SKILL.md) — provision the `fb_definitions` or target collections (on either kind of project).
- [create-feature/vform-usage](../create-feature/references/vform-usage.instructions.md) — the VForm runtime the builder wraps.
- [buildpad-reference](../buildpad-reference/SKILL.md) — full component catalog.
