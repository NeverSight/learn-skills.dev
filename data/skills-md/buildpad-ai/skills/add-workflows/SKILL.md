---
name: add-workflows
description: Scaffold the Buildpad Workflows module — ready-made /workflows, /workflow-assignments, and /workflow-instances admin pages (WorkflowsManager/WorkflowDetail with a state-diagram editor, WorkflowAssignmentsManager/WorkflowAssignmentDetail, WorkflowInstancesManager/WorkflowInstanceDetail). Use when the user wants an admin UI to design workflow state machines, assign them to collections, or inspect workflow instances and their transition history. To create a workflow for a collection through DaaS (definition, assignment, fields, WorkflowButton), use create-workflow instead.
argument-hint: "[--cwd path/to/project]"
---

# Add the Workflows Module

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

A ready-made workflow administration surface installed via the Buildpad CLI (Copy & Own — the code is copied into your project). It manages three related records — **definitions** (the state machine), **assignments** (which collection a workflow applies to, with an optional filter rule), and **instances** (one per item, with its transition history) — on top of DaaS's built-in workflow engine (`daas_wf_definition`, `daas_wf_assignment`, `daas_wf_instance`, `daas_wf_history`).

Six screens ship together:

- **`WorkflowsManager`** — the `/workflows` list: search, pagination, permission-gated create/edit/delete.
- **`WorkflowDetail`** — the `/workflows/[id]` editor: name, description, statistics, and a state diagram (React Flow) where states are nodes and commands are edges, edited through a State dialog and a three-tab Command dialog (General, Actions, Policies).
- **`WorkflowAssignmentsManager`** — the `/workflow-assignments` list.
- **`WorkflowAssignmentDetail`** — the `/workflow-assignments/[id]` form: workflow picker, collection picker, and a Filter Rule JSON field.
- **`WorkflowInstancesManager`** — the `/workflow-instances` list (read-only).
- **`WorkflowInstanceDetail`** — the `/workflow-instances/[id]` page: the instance, its current state, a read-only diagram of its definition, and the transition history.

This module is the admin UI. The button that shows an item's state and runs a transition on a content form is a separate component, `WorkflowButton` — see [create-workflow](../create-workflow/SKILL.md). `WorkflowButton` is not covered by the "no proxy routes" rule below: on Buildpad UI 3.0.0 it posts transitions to the app's own origin and reads the instance as the signed-in user, so it needs a transition proxy route and read grants that this module does not — both are listed in create-workflow, step 5.

## CRITICAL: Never Create These Manually

Like all Buildpad UI, the Workflows module is CLI-installed and owned as source. Do **not** hand-write `components/ui/workflow-management/*` or the `useWorkflowDefinitions`/`useWorkflowAssignments`/`useWorkflowInstances` hooks in `lib/buildpad/hooks/` — scaffold them. Do **not** build a custom state-machine editor or a custom status field either: DaaS Workflows are a built-in platform feature (see [daas-platform](../daas-platform/SKILL.md)).

## Prerequisites Check

```bash
node --version && pnpm --version && npx --version
```

Requires Node.js v24 LTS and pnpm v10+ (see [add-buildpad](../add-buildpad/SKILL.md) for install guidance). The module **must** render under the authenticated layout (`buildpad init` generates `app/[lang]/(authenticated)/` with a `DaaSProviderWrapper`), with `<Notifications />` mounted and the Buildpad i18n provider in place (see [add-i18n](../add-i18n/SKILL.md)).

**This module calls DaaS directly from the browser. It has no proxy routes — do not add `api-routes` for it.** Every request goes to `NEXT_PUBLIC_BUILDPAD_DAAS_URL` with the session token that `DaaSProviderWrapper` supplies:

```bash
# .env.local
NEXT_PUBLIC_BUILDPAD_DAAS_URL=https://your-daas.example.com
```

<!-- buildpad-backend: supabase -->
**DaaS CORS must be configured first.** The calls are cross-origin and authenticated. DaaS's default `cors_origins: ["*"]` is **incompatible** with credentialed requests — the browser blocks every preflight, and every list shows its load-error state. Set explicit origins before mounting the module (see [daas-platform](../daas-platform/SKILL.md) "CORS must use explicit origins").

The module works against both DaaS backends (the Supabase-backed DaaS and the Go engine); the hooks absorb their differences in list and error shapes.
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
On an Engine project the data API's address is the Engine_URL, which both `NEXT_PUBLIC_BUILDPAD_DAAS_URL` and `NEXT_PUBLIC_SUPABASE_URL` hold. The Studio's address is an administration interface: send no data call to it.

**Leave the cross-origin settings as they are.** On an Engine project the data API accepts requests from any origin and never with cookies, as the project is provisioned. Change no cross-origin setting, and do not add the application's origin anywhere. The module's calls carry the signed-in user's access token as `Authorization: Bearer`, never a cookie, so nothing needs configuring before you mount it.

The hooks absorb the Engine's list and error shapes. Definitions go through `/api/workflows` and assignments through `/api/workflow-assignments`; instances and their history are read through `/api/workflow-instances`. On an Engine project the Engine creates instances, and an instance changes only through `POST /api/workflow/transition`: never create, update or delete a `daas_wf_instance` or `daas_wf_history` row yourself, through the items API or in custom code.
<!-- /buildpad-backend -->

## Installation

The Workflows module is **opt-in** — it is not part of `bootstrap`.

```bash
# 1. Install the diagram library first. The diagram is drawn with React Flow
#    (@xyflow/react, MIT). `add` only installs a dependency when it can ask on a
#    terminal; run by an agent, a script or CI it prints the command and then
#    fails its own validation on the missing module.
cd /path/to/project && pnpm add "@xyflow/react@^12.9.3"

# 2. Add the module: six page shells, components/ui/workflow-management/ (22 files),
#    the workflow hooks, types and editor logic, and three sidebar entries under "Automation"
npx @buildpad/cli@latest add workflows-routes --cwd /path/to/project
```

If step 2 was run first and exited with `Cannot find module '@xyflow/react'`, nothing is broken: run step 1, then `npx @buildpad/cli@latest validate --cwd /path/to/project`.

Do not import its stylesheet anywhere: `workflow-diagram.tsx` imports `@xyflow/react/dist/style.css` itself.

To install only the components (no pages, no sidebar entries) — for an app that has its own routes and shell:

```bash
npx @buildpad/cli@latest add workflow-management --cwd /path/to/project
```

> The docs use the shorthand `buildpad add workflows-routes` when the CLI is installed globally; `npx @buildpad/cli@latest add …` is the equivalent no-install form used across these skills.

> **If the CLI command fails, `@buildpad/cli` IS published to npm** — verify with `npm view @buildpad/cli version` before assuming otherwise. The CLI fetches its registry from `raw.githubusercontent.com`, so confirm the environment can reach **both** npm and the GitHub raw CDN. If `add workflows-routes` reports an unknown target, the installed CLI predates this module: use `@latest`.

## The Routes

```
app/[lang]/(authenticated)/
├── workflows/
│   ├── page.tsx            # /workflows                  — WorkflowsManager
│   └── [id]/page.tsx       # /workflows/[id]             — WorkflowDetail (/workflows/new creates)
├── workflow-assignments/
│   ├── page.tsx            # /workflow-assignments       — WorkflowAssignmentsManager
│   └── [id]/page.tsx       # /workflow-assignments/[id]  — WorkflowAssignmentDetail (/workflow-assignments/new creates)
└── workflow-instances/
    ├── page.tsx            # /workflow-instances         — WorkflowInstancesManager
    └── [id]/page.tsx       # /workflow-instances/[id]    — WorkflowInstanceDetail
```

The sidebar labels are dictionary keys (`app.nav.workflows`, `app.nav.workflowAssignments`, `app.nav.workflowInstances`, and `app.nav.automation` for the group). An app created before this module gets them with `npx @buildpad/cli@latest upgrade i18n`.

## Usage

The components never navigate. Each page passes router callbacks, so your router (and its locale prefix) decides where a click goes.

### List view — `WorkflowsManager`

```tsx
// app/[lang]/(authenticated)/workflows/page.tsx
"use client";

import { useLocaleRouter } from "@/lib/i18n/navigation";
import { WorkflowsManager } from "@/components/ui/workflow-management";

export default function WorkflowsPage() {
  const router = useLocaleRouter();
  return (
    <WorkflowsManager
      onWorkflowClick={(workflow) => router.push(`/workflows/${workflow.id}`)}
      onCreateWorkflow={() => router.push("/workflows/new")}
    />
  );
}
```

| Prop | Purpose |
| ----------------- | ------------------------------------------------------ |
| `onWorkflowClick` | Open a definition (navigate to the detail page) |
| `onCreateWorkflow` | Handle the permission-gated create action |
| `pageSize` / `pageSizeOptions` | Pagination control |
| `hideHeader` | Embed the list without its own header chrome |
| `urlParams` / `urlParamPrefix` | Search and page live in the query string by default; turn off for an embedded list, prefix when two lists share a page |
| `translations` | Override strings for this instance |

`WorkflowAssignmentsManager` is the same with `onAssignmentClick` / `onCreateAssignment`. `WorkflowInstancesManager` has only `onInstanceClick`: instances are created by the backend and change only through a transition.

### Detail view — `WorkflowDetail`

```tsx
// app/[lang]/(authenticated)/workflows/[id]/page.tsx
"use client";

import { use } from "react";
import { useLocaleRouter } from "@/lib/i18n/navigation";
import { WorkflowDetail } from "@/components/ui/workflow-management";

export default function WorkflowDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const router = useLocaleRouter();
  return (
    <WorkflowDetail
      id={id}
      onBack={() => router.push("/workflows")}
      onSaved={() => {
        if (id === "new") router.push("/workflows");
      }}
    />
  );
}
```

**Navigate after a create.** From Buildpad UI 3.2.0, after a successful create the component goes on as the editor of the stored record: a further Save updates it and does not create a second one. The URL still says `/workflows/new`, though, and a reload would open an empty form. `onSaved` receives the saved record; navigate to the list (as the generated pages do) or to the new record. Keep this when you customise the pages. On 3.0.x–3.1.x the component kept `id="new"` after a create and a second Save created a duplicate — upgrade (`npx @buildpad/cli@latest upgrade workflow-management`) rather than working around it.

`WorkflowAssignmentDetail` (`id`, `onBack`, `onSaved`) and `WorkflowInstanceDetail` (`id`, `onBack`) follow the same pattern. `onBack` is what Cancel, the breadcrumb and the Back button of the not-found / access-denied / load-error states call.

### Supporting components (reuse anywhere)

<!-- buildpad-backend: supabase -->
`WorkflowDiagram` (controlled by `workflowJson` + `onChange`; `readOnly`, `height`, and `hideAttribution` — React Flow's attribution is shown unless you set it), `WorkflowStateModal`, `WorkflowCommandModal`, and the loaders `loadAllWorkflowPolicyOptions` and `loadWorkflowCollectionNames`. The assignment form's pickers take `workflows` / `loadWorkflows` and `collections` / `loadCollections` when you want to filter what they offer (by default the Collection picker lists everything `/api/collections` returns, system collections included).
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
`WorkflowDiagram` (controlled by `workflowJson` + `onChange`; `readOnly`, `height`, and `hideAttribution` — React Flow's attribution is shown unless you set it), `WorkflowStateModal`, `WorkflowCommandModal`, and the loaders `loadAllWorkflowPolicyOptions` and `loadWorkflowCollectionNames`. The assignment form's pickers take `workflows` / `loadWorkflows` and `collections` / `loadCollections` when you want to filter what they offer. By default the Collection picker lists everything `/api/collections` returns to the signed-in user: on an Engine project that is every collection, system collections included, for an administrator or a holder of read on `daas_collections`, and otherwise only the collections the user may read.
<!-- /buildpad-backend -->

## The Data Layer (reuse anywhere)

All six screens are thin wrappers over hooks from `@/lib/buildpad/hooks`:

```tsx
import {
  useWorkflowDefinitions,
  useWorkflowAssignments,
  useWorkflowInstances,
} from "@/lib/buildpad/hooks";
```

- **`useWorkflowDefinitions()`** → `fetchDefinitions`, `fetchAllDefinitions` (every page, for pickers), `getDefinition`, `createDefinition`, `updateDefinition`, `deleteDefinition` (+ `loading`, `error`, `errorInfo`)
- **`useWorkflowAssignments()`** → `fetchAssignments`, `getAssignment`, `createAssignment`, `updateAssignment`, `deleteAssignment`
- **`useWorkflowInstances()`** → `fetchInstances`, `getInstance`, `fetchInstanceHistory`

Every method rejects with a typed `DaaSRequestError` whose `kind` is `notFound | forbidden | mfaRequired | unauthenticated | invalid | failure`. Branch on `kind`; never treat a rejected load as an empty list. Types (`WorkflowDefinitionRecord`, `WorkflowJson`, …) and the collection-name constants (`WORKFLOW_COLLECTIONS`) come from `@/lib/buildpad/types`; the pure editor logic (`normalizeWorkflowJson`, `buildWorkflowCommand`, `parseWorkflowFilterRule`, …) from `@/lib/buildpad/utils`.
<!-- buildpad-backend: engine -->

`mfaRequired` is the Engine refusing a session that still needs its second factor. On an Engine project multi-factor enrolment, challenge and verification are not served through the Supabase client. The Engine's own routes, each called with the user's session, are `POST /api/auth/mfa/enroll`, `GET /api/auth/mfa/factors`, `POST /api/auth/mfa/verify` and `POST /api/auth/mfa/unenroll`; a session that still needs its second factor is accepted elsewhere only after `POST /api/auth/mfa/verify`. Send the user through that verification, then retry; do not show the refusal as an empty list.
<!-- /buildpad-backend -->

These hooks are for administering workflows. To read an item's workflow state or run a transition, use `WorkflowButton` / `useWorkflow` (see [create-workflow](../create-workflow/SKILL.md)).

## Access-Control Semantics (IMPORTANT)

- The UI gates controls on the collections the API enforces: `daas_wf_definition` and `daas_wf_assignment` (`create` / `update` / `delete`). A reader without `update` gets the detail page read-only. Instances and history have no client gate: the API's answer decides, and a refusal draws the access-denied state.
- Until the permissions are known, no write control is drawn and the editors take no edit (3.2.0 and later; earlier versions showed them for the length of the permissions request). The lists and records still load at once. Do not "fix" the short wait by rendering buttons optimistically.
- The gates only hide controls. Grant the collection permissions through policies (see [create-rbac](../create-rbac/SKILL.md)); a hidden button is not the protection.
- Gate your navigation links too, so a user without read access to `daas_wf_definition` does not see the Automation group.
- **Who may run a command.** A command stores `policies` (policy ids) and `module_access_keys`. A caller who holds any listed policy **or** any listed key may run it. **A command with neither list is open to every authenticated user.** The Command dialog edits `policies`; it keeps stored `module_access_keys` on save and shows a notice that the command is gated by them, but has no field to edit them — set keys through the API (see [grant-module-access](../grant-module-access/SKILL.md)).
- An assignment's Filter Rule must be a JSON object (or empty). The form refuses anything else before it sends a request.
- An action's Parameters must be a JSON object too; the Go engine refuses a whole definition that holds anything else there.
- A definition answered without its `workflow_json` (a read grant that withholds the field) is shown with a notice and cannot be saved over. Do not treat a missing document as an empty machine in custom code.

## Post-Install Validation

```bash
npx @buildpad/cli@latest status --cwd /path/to/project
npx @buildpad/cli@latest validate --cwd /path/to/project
cd /path/to/project && pnpm build
```

<!-- buildpad-backend: supabase -->
Then open `/workflows` signed in as a user with read on `daas_wf_definition`: the list loads (an empty DaaS shows the empty state, not a load error). A load error on every list means `NEXT_PUBLIC_BUILDPAD_DAAS_URL` or the DaaS CORS origins are wrong.
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
Then open `/workflows` signed in as a user with read on `daas_wf_definition`: the list loads (an empty Engine shows the empty state, not a load error). A load error on every list means `NEXT_PUBLIC_BUILDPAD_DAAS_URL` does not hold the Engine_URL, or the session has expired (sign in again). Do not change a cross-origin setting to fix it.
<!-- /buildpad-backend -->

## Related

- [create-workflow](../create-workflow/SKILL.md) — create a workflow for a collection through DaaS, add the workflow fields, and place `WorkflowButton` on a form.
- [add-buildpad](../add-buildpad/SKILL.md) — the underlying CLI and low-level field widgets.
- [add-users](../add-users/SKILL.md) — the Users module; its `/policies` pages manage the policies a command can be locked to.
- [create-rbac](../create-rbac/SKILL.md) — the collection permissions this module's gates read.
- [grant-module-access](../grant-module-access/SKILL.md) — module access keys, the other way to lock a command.
- [buildpad-reference](../buildpad-reference/SKILL.md) — full component catalog.
