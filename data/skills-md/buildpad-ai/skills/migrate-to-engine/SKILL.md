---
name: migrate-to-engine
description: "Engine projects only: finish moving a Buildpad project from Supabase to the Buildpad Engine. Rewrites the hooks, cron jobs and custom services the Engine could not run as they were (engine-plan/automation-to-review.json) for the Engine's runtime, and ports the app's code: environment, sign-in, data calls, files, administrator code, schema and access rules, database functions. Use after a project was moved, when .buildpad/project.json says the backend is engine, or when asked to port an app or automation to the Engine. On a Supabase project it explains the move and stops."
user-invokable: true
argument-hint: "[path to automation-to-review.json, or the file to port]"
---

# Migrate to the Buildpad Engine

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
## On a Supabase project

This skill is used after a project has moved to the Buildpad Engine. This project's backend is
Supabase, so there is nothing to port yet. Tell the developer so, and stop: change no code for the
Engine while the project runs on Supabase, because the app would stop working.

A project keeps its backend for its whole life. To move, the developer creates a new Buildpad
Engine project and moves the data, access rules, automation and app code to it, with the migration
tool from their platform operator. The steps are in the public guide
<https://app.buildpad.ai/docs/migrate-to-engine>. The new project's starter kit holds a
`.buildpad/project.json` whose `backend` is `"engine"`; once the app's repository commits that file,
this skill applies.
<!-- /buildpad-backend -->
<!-- buildpad-backend: engine -->
Use this skill on an Engine project that was moved from a Supabase project, or when the developer
asks to port an app, a hook, a cron job or a custom service to the Engine. The move (the operator's
migration tool) has already copied the schema, the roles, policies and permissions, the users, the
files and the records. Two things are left, and this skill does both:

- **Part A, automation:** each hook, cron job or custom service the Engine could not run as it was.
- **Part B, app code:** every place where the app still talks to Supabase.

Removing what the Engine lacks is the work of this skill. Where a step below says a feature is not
available on an Engine project, remove its code, tell the developer what you removed and what takes
its place, build no substitute, and go on with the next step.

**First:** check that `.buildpad/project.json` (from the new project's starter kit) is committed
and that its `backend` is `"engine"`. Work on a branch.

## What the move leaves you

| What | Where | What it holds |
|---|---|---|
| Automation to rewrite | `engine-plan/automation-to-review.json`, in the folder the migration tool wrote | One entry per item: `kind` (`extension`, `cron` or `service`), `id`, `name`, `file` (the export file that holds the original row and its `code`), `was_active`, `findings` (each with `rule`, `line` and `message`) and a ready `prompt` that names this skill |
| Automation that passed | The new project, **switched off** | Copied as it was; switched on at cut-over |
| App-code places | The migration tool's app scan | `file:line` and a pattern id for each place that uses a Supabase-only feature |
| Permission rules to review | The move's report | Copied rules whose meaning changes on the Engine (see [Permission rules that change meaning](#permission-rules-that-change-meaning)) |

The migration tool's folder holds users' emails, records and files. Read only the `engine-plan`
file and the one export file an entry names; copy nothing from that folder into the repository,
and never commit it.

## Part A: Automation

On an Engine project stored code (hooks, cron jobs, custom services) runs in the Engine's runtime, which provides only what the table [Engine runtime](#engine-runtime) lists; for each interface it lacks, the table says what replaces it.

The runtime is JavaScript. The code is the body of an async function: `await` and `return` work at
the top level. Its globals are `context`, `services`, `console`, `JSON`, `Date` and `Math`, plus
`payload`, `meta` and `HookError` in a hook; a custom service reaches the services through
`context.services` and has no `console`. The services are listed, with every signature, in
[hooks-extensions](../hooks-extensions/SKILL.md) (its Engine services API reference).

### Steps, for each entry

Work through custom services first (an entry with a `dependency` finding waits for the service it
names), then hooks, then cron jobs: hooks and jobs call services by name.

1. **Read the original.** Find the row whose `id` is the entry's `id` in the export file the entry
   names (`file`), and read its `code` and its other fields (`event`, `type`, `schedule`,
   `timezone`, `timeout_ms`, `tests`, `dependencies`). If the developer points at code instead, start
   from that code.
2. **Explain each finding** to the developer: the line, what the Engine lacks, and what replaces it
   (the table below). The check is static: read the whole body for what it cannot see, such as the
   rows of [Also check](#also-check-what-the-scan-does-not-flag).
3. **Rewrite** the body for the Engine's runtime and keep its behaviour: the same events, the same
   writes, the same mail and the same outside calls. Before-and-after examples for every finding are
   in [Automation rewrites](references/automation-rewrites.instructions.md). Where the Engine cannot
   do the work at all (a library, a hash, a long job), move that work into an API route of the app
   (see [create-api-route](../create-api-route/SKILL.md)) or a custom service, and keep the stored code
   small.
4. **Show the rewrite** and the list of what changed to the developer before you create anything.
5. **Create it switched off**, with the original's `name`, so callers find it: a hook with `status`
   `inactive`, a cron job with `status` `inactive`, a custom service with `status` `draft`. Use the
   Studio (its Extensions, Cron and Custom Services modules) or, as an administrator's agent, the
   Engine's MCP tools `extensions`, `cron` and `services`, which are listed and served to an
   administrator only. If a tool is not listed, the project's Engine is older than 0.1.0-dev.4: use
   the Studio. Before you create an item, list the existing ones: an item of that name made by an
   earlier run is updated, not created twice. See [hooks-extensions](../hooks-extensions/SKILL.md),
   [create-cron](../create-cron/SKILL.md) and [create-service](../create-service/SKILL.md).
6. **Test it**: run a custom service's tests; run a cron job by hand and read its history; for a
   hook, follow the check in [hooks-extensions](../hooks-extensions/SKILL.md) (activate it, write a
   scratch item, read the answer and the log, delete the item) and switch it off again. Before you
   switch on a hook that sends mail or calls an outside system, ask the developer: it acts for real.
7. **Leave it switched off until cut-over**, so the old and the new project never both run it. At
   cut-over the migration tool switches on the items it copied and the items you rewrote: it finds
   a rewritten item by its kind and its **name**, and switches it on when the original's
   `was_active` is `true`. So keep each rewritten item's original name. An item it cannot find is
   reported as still to rewrite. On an Engine project an active cron job fires at its scheduled time.

### Engine runtime

The `rule` of each finding, what it means, and what replaces it.

| `rule` | On the Engine | Replacement |
|---|---|---|
| `require`, `import`, `module` | There are no modules: no package and no other file can be loaded | Inline a small helper; put shared code in a custom service (`await services.custom('name')`) that `return`s an object; move work that needs a package into an API route |
| `process` | `process` does not exist | `services.env.KEY` (`context.env.KEY` in a custom service). It is empty unless the Engine's operator names the key: ask the operator to expose each key the code needs. Never write a secret into stored code: every administrator can read it |
| `fetch` | The global `fetch` does not exist | `services.fetch(url, init)`, to the hosts the Engine's operator allows: ask the operator to allow each host. Send a string `body` (`JSON.stringify(...)`) |
| `timers` | `setTimeout`, `setInterval` and the rest do not exist | No delay inside a run. A wait or a later retry becomes a cron job that picks up pending rows; a job can also be run at once with `services.cron.trigger('name')` |
| `eval` | `eval` and `Function` are removed | Write the code out |
| `supabase` | The Supabase service is refused permanently (`501 RUNTIME_SUPABASE_UNAVAILABLE`); there is no SQL and no Supabase client | `services.items(collection)`, with `{ elevated: true }` where a hook or custom service must act as an administrator; a database function becomes items calls or a custom service |
| `node-global` | `Buffer`, `URL`, `URLSearchParams`, `TextEncoder`, `atob`, `btoa`, `crypto`, `structuredClone`, `window` and the other browser and Node globals do not exist | Build query strings with `encodeURIComponent`; copy with `JSON.parse(JSON.stringify(x))`; let a `uuid` field make ids; move hashing, signing and binary work into an API route |
| `services-member` | That `services.<name>` is not part of the Engine's services | `services.items`, `files`, `mail`, `fetch`, `env`, `cron`, `custom` and the read-only schema services are all there is |
| `dependency` | The custom service it needs is itself on the list | Rewrite that service first, under the same name |
| `empty` | The item has no code | Ask the developer whether it is still needed |

### Also check (what the scan does not flag)

- `readByQuery` returns the array itself: read `result`, not `result.data`.
- A read returns 25 rows without `limit`, and at most 1000. Query keys other than `fields`,
  `filter`, `sort`, `limit`, `page`, `offset` and `search` are refused (`deep`, `aggregate`,
  `groupBy`).
- There is no query-wide update or delete: read the keys, then `updateMany(keys, data)` or
  `deleteMany(keys)`.
- In update and delete hooks the ids are `meta.keys` (an array); `meta.key` is set on create only.
- `services.mail(...)` does not throw when mail cannot be sent: check `success`.
- A filter hook refuses a write with `throw new HookError(message, status, code)`.
- `console` is not in scope in a custom service body; `Intl` is not in the runtime.
- The services' write methods are `createOne`, `createMany`, `updateOne`, `updateMany`, `deleteOne`
  and `deleteMany`; schema services and `services.files` are read only.

The items the move copied passed the scan, so they can still hold one of these: test each one
before cut-over.

## Part B: App code

Run the migration tool's app scan on the repository if the developer has it, and work through the
checklist below in order. The scan's pattern ids are given with each step. Details and
before-and-after code are in [App code](references/app-code.instructions.md).

On an Engine project the data API's address is the Engine_URL, which both `NEXT_PUBLIC_BUILDPAD_DAAS_URL` and `NEXT_PUBLIC_SUPABASE_URL` hold. The Studio's address is an administration interface: send no data call to it.

### Checklist

- [ ] **1. Environment** (`service-role`, `platform-supabase`). Take the new starter kit's
  `.env.local` as it is. In every other place that sets the app's environment (`.env.example`,
  the deployment's settings, CI secrets), set these values and remove the service-role key
  variable. On an Engine project the environment is: `NEXT_PUBLIC_SUPABASE_URL=<Engine_URL>`, `NEXT_PUBLIC_BUILDPAD_DAAS_URL=<Engine_URL>`, `NEXT_PUBLIC_SUPABASE_ANON_KEY=buildpad-engine-public-anon-key` (a fixed value that is not a secret; the Engine does not read it, the Supabase client needs one), and `NEXT_PUBLIC_BUILDPAD_TENANT_ID=<the project's tenant id>`. There is no service-role key on an Engine project: add none.
- [ ] **2. Sign-in** (`client-auth`, `sign-up`, `stored-supabase`). Sign in with a password
  through the app's own server route, as the Engine starter does: the login route of
  [create-api-route](../create-api-route/SKILL.md) sends the sign-in to
  `<Engine_URL>/auth/v1/token?grant_type=password` with the header `X-Tenant-Id` set to
  `NEXT_PUBLIC_BUILDPAD_TENANT_ID`. Remove the sign-up, magic-link, one-time-code, password-reset,
  change-password and change-email pages and routes, the OAuth buttons and the code-exchange
  callback route. For XAppHub sign-in, use the Engine variant in
  [add-external-oauth](../add-external-oauth/SKILL.md).
  On an Engine project the Supabase client is kept for sign-in only. Password sign-in, session refresh, reading the signed-in user and sign-out work through it, and its default sign-out ends the user's sessions on every device. An account that holds no role in the project's tenant is refused at password sign-in. XAppHub sign-in also works through it while the project's XAppHub connector is connected: the application's server gives the ID token from XAppHub to `signInWithIdToken` with the provider `my-apps`, and ends the session of an account that holds no role yet (the `add-external-oauth` skill). Not available on an Engine project: sign-up; OAuth sign-in with any provider other than XAppHub; magic link and one-time code; password recovery; changing a password, an email or a profile through the Supabase client; the Supabase client's code exchange; and the Supabase administration API. The Platform's password-less handoff opens the Studio; it is not a way for an application to sign a user in.
  On an Engine project multi-factor enrolment, challenge and verification are not served through the Supabase client. The Engine's own routes, each called with the user's session, are `POST /api/auth/mfa/enroll`, `GET /api/auth/mfa/factors`, `POST /api/auth/mfa/verify` and `POST /api/auth/mfa/unenroll`; a session that still needs its second factor is accepted elsewhere only after `POST /api/auth/mfa/verify`.
- [ ] **3. Data calls** (`rest`, `bare-items`, `cookies`). Every data path starts with `/api`
  (`/api/items/:collection`, `/api/files`, `/api/users/me`). Replace the Supabase client's table
  calls and PostgREST addresses with the items API, through the app's forwarding routes
  ([create-api-route](../create-api-route/SKILL.md)) or the Buildpad SDK. Send no cookie and no
  tenant header after sign-in.
  On an Engine project every data call carries the signed-in user's access token as `Authorization: Bearer <access token>`, from the application's own server route or from the SDK. The Engine accepts no cookie session on its data API. The token in the project's MCP configuration is accepted only on the MCP endpoint `/api/mcp`: never send it, or any other administrator token, to the data API.
- [ ] **4. Administrator code** (`service-role`, `auth-admin`). Remove every Supabase client built
  with the service-role key. Do administrator tasks in the Studio, or in a server route that
  forwards a signed-in administrator's own access token. Static tokens on user records are not
  accepted by the data API: give their holders a signed-in session instead.
  On an Engine project an administrator creates every user who signs in with a password, through the Engine's user API (`POST /api/users` with an administrator's session) or the Studio's Users module, and gives the user a role in the project's tenant (`POST /api/users/:id/roles` with `role_id`, or the Users module). A user's first XAppHub sign-in creates that user's account, which holds no role until an administrator gives it one in the same way. An administrator resets a user's password, in the Studio's Users module.
  For admin pages in the app, see [add-users](../add-users/SKILL.md).
  On an Engine project some files the Buildpad CLI generates cannot be used yet: `lib/supabase/admin.ts`, the OAuth callback and provider routes of the `external-oauth` module, the server-side enforcer and session modules, and `lib/module-access/enforce.ts`. Do not call them; check module access by forwarding the user's token to `GET <Engine_URL>/api/permissions/me` and reading `isAdmin` and `moduleAccess`. For XAppHub sign-in the CLI installs the `external-oauth-engine` module in place of `external-oauth`; its routes are used as the `add-external-oauth` skill says.
- [ ] **5. Files** (`storage`, `storage-url`). Replace Supabase Storage (calls on
  `supabase.storage` and `/storage/v1` addresses) with the Engine's file routes; see
  [add-files](../add-files/SKILL.md). The move kept every file's id, so a record that points to a
  file still works; code that named a file by bucket and path names it by its id now. Image
  transform parameters (`width`, `height`, `fit`, `quality`, `format`, `withoutEnlargement`, or a
  preset `key`) work on `/api/files/assets/:id` and on signed URLs; a request for WebP or AVIF can
  be answered as JPEG or PNG.
  On an Engine project files are stored and served by the Engine: `/api/files`, `/api/folders`, `/api/files/signed-url`, and file content at `/api/files/assets/:id` (with a session or a signed token). A file shown in a browser, a public one included, is loaded through a signed URL from `/api/files/signed-url`, not by an anonymous read: an `<img>` element or a link sends no `X-Tenant-Id`. Set no storage bucket option: the Engine stores files on its own disk or in S3.
- [ ] **6. Schema and access** (`migration`, `migration-file`, `sql-policy`). Delete the Supabase
  migrations folder (`supabase/migrations`) and the rest of the `supabase` folder once nothing in
  it is still to port (database functions and edge functions: step 7). Change the schema in the
  Studio or over MCP. Each row-level security policy becomes roles, policies and permissions: check
  that the moved permissions give the same rows, and add what is missing with
  [create-rbac](../create-rbac/SKILL.md). Then review [Permission rules that change meaning](#permission-rules-that-change-meaning).
  On an Engine project collections, fields, relations, roles, policies and permissions are created through the Engine's API (`/api/collections`, `/api/fields/:collection`, `/api/relations`, `/api/roles`, `/api/policies`, `/api/access`, `/api/permissions`) or its MCP tools `collections`, `fields`, `relations`, `roles`, `policies`, `access` and `permissions`. Access is roles, policies and permissions: a permission belongs to a policy, and a policy is attached to a role or a user. The MCP `collections` and `fields` tools keep a field's name, type and `meta` but not its `schema` block (default, not-null, length): set those through `POST /api/fields/:collection` with an administrator's session.
- [ ] **7. Database functions** (`rpc`). Calls to the Supabase client's `rpc` method, database
  functions, triggers, views and edge functions did not move. Move each one's logic into an API
  route of the app, an Engine hook ([hooks-extensions](../hooks-extensions/SKILL.md)) or a custom
  service ([create-service](../create-service/SKILL.md)): a trigger usually becomes a hook, a
  function the app calls becomes an API route, and logic shared by hooks and jobs becomes a custom
  service.
- [ ] **8. Cross-origin settings.** Remove any code or setup that sets them.
  On an Engine project the data API accepts requests from any origin and never with cookies, as the project is provisioned. Change no cross-origin setting, and do not add the application's origin anywhere.
- [ ] **9. What sits around the app.** Tests: build their users, sign-in and environment for the
  Engine ([create-tests](../create-tests/SKILL.md)). A runtime worker: follow
  [worker-messaging](../worker-messaging/SKILL.md). A mobile wrapper: point it at the new
  deployment ([add-mobile-app](../add-mobile-app/SKILL.md)). The deployment: the app moves to a
  microapp of the new project, with the environment of step 1.
- [ ] **10. Verify.** Run the app scan again (it should report nothing), then the build, the lint
  and the tests, and fix what fails. Sign in as a moved user with their old password, and read and
  write a record of each collection the app uses. Report to the developer what changed, what was
  removed, and what is left for cut-over.

## Permission rules that change meaning

The move copied the project's permission rules. A rule that uses one of these variables matched as
`null` on the Supabase project, because Supabase did not resolve them, and resolves on the Engine:

- `$CURRENT_ROLES`
- `$CURRENT_ROLE.<field>`
- `$CURRENT_USER.role.<field>`
- `$NOW` with an adjustment, such as `$NOW(-1 day)`

Such a rule can now match rows it never matched before, so a user can see or change more than on
the old project. The move flags each one for the project owner to acknowledge before cut-over. Show
every such rule to the developer, with its policy, collection, action and filter, and say what it
matched before and what it matches now. Change a rule only when the owner asks, through
[create-rbac](../create-rbac/SKILL.md). Rules the move could not copy at all are listed for
rewriting in the move's report: rewrite them the same way.
<!-- /buildpad-backend -->
