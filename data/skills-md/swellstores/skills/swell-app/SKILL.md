---
name: swell-app
description: "Use this skill to build, modify, deploy, publish or debug Swell apps with the swell CLI. Covers admin, integration and code-based storefront apps: models, dashboard views and actions, functions and workflows, settings, notifications, webhooks, checkout extensions, components for admin content fields and frontends. Frontends use managed Swell hosting or self-hosting in the developer's Cloudflare account. Apply for swell.json, app resource directories, app-lifecycle CLI commands, app namespaces and model triggers, or @swell/apps-sdk runtime setup inside an app. Pair with swell-backend-api or swell-frontend-api for data and commerce operations. Independent API consumers without the Swell app lifecycle use the relevant API skill directly. Excludes Proxima / Liquid themes, swell theme commands, other commerce platforms and generic Cloudflare work."
allowed-tools: Read, Grep, Glob, Bash
---

# Swell apps

A Swell app is a package of files that the `swell` CLI installs and versions in a store. It adds data, dashboard screens, server logic and, optionally, a web frontend. Managed hosting is the recommended default: Swell hosts the resources and issues the app's credentials, with no server or store API key for the developer to manage. An app frontend can also run in the developer's own Cloudflare account while retaining Swell's app lifecycle, addresses and signed request context — see `references/frontend.md`, "Self-hosting on Cloudflare".

Independent integrations and storefronts that connect directly to the APIs, without the Swell app lifecycle and supplied runtime context, use `swell-backend-api` and `swell-frontend-api` respectively. Hosting on Cloudflare alone does not make a site a Swell app. The API skills also own the commerce operations an app performs — what a cart or an order contains, how queries and writes behave. This skill covers the app around them.

`<app_id>` below is the `id` in `swell.json`.

## App types

| `type` in `swell.json` | What the app is |
| --- | --- |
| `admin` | Extends a store: data, dashboard views and actions, server logic, and optionally custom dashboard pages |
| `integration` | The same blocks, for an app that connects the store to an outside service. It can declare extension slots that plug into Swell's own payment, shipping or tax flows — see "Integration apps and extensions" |
| `storefront` | The store's own site for shoppers, written in code in `frontend/`; managed hosting by default, with Cloudflare self-hosting supported |
| `theme` | A Proxima / Liquid theme. Not covered by this skill or by another Swell skill — say so instead of answering from app rules |

## Choose the building block

An app is assembled from the blocks below. Start from the need, pick the smallest block that covers it, and read that block's entry under "Building blocks" for its limits before designing around it.

| Need | Block |
| --- | --- |
| Keep extra data on products, orders, customers or another standard record | Model that extends the standard collection |
| Keep a new kind of record | Model for an app collection, or a child collection of a parent |
| Let merchants list, filter, create and edit that data in the dashboard | Content views |
| A field in a dashboard form that needs its own input — a picker, a preview, a lookup in an outside service | Component bound to a content field |
| A dashboard button that does something to a record, to selected rows or for the app | Action |
| React after a record changes | Function on a model event (async) |
| Validate, change or reject a write before it is saved | Function as a `before:` hook (sync) |
| Do something at a date stored on a record, or on a fixed schedule | Function with a model schedule, or a cron function |
| An HTTP endpoint for a storefront or another system to call | Route function |
| Background work in several steps that is long, waits, or must survive a failure | Workflow |
| Tell an external service that something happened | Webhook; a function when the call needs logic, signing or a custom payload |
| Send an email when a record is created or changes | Notification |
| Let the merchant configure the app, including provider credentials | Settings |
| A dashboard screen that views and actions cannot express | Frontend of an `admin` or `integration` app |
| The store's own site for shoppers | Frontend of a `storefront` app |
| A payment method, shipping rates or tax calculation inside Swell's checkout | Integration extension |
| Put the app in the live environment or in other stores, or list it in the App Store | Versions and releases — `references/app-publishing.md`. `swell app push` reaches the test environment only |

## Building blocks

Each folder holds one kind of block, and a file's name decides what it becomes: its collection, its endpoint, its settings group. Keep `_` out of these names: it deploys as a dash, and push warns about it. Push removes a deployed resource whose file is gone, so renaming a file replaces the resource, unless the new name deploys as the old one did: `my_report.ts` renamed `my-report.ts` keeps it.

### Manifest — `swell.json`

The app's `id`, `name`, `type`, `version` and `permissions`, plus `frontend.hosting` when there is a frontend and `extensions[]` for integration slots. **Always declare `permissions`**: empty or absent means full access to the store (see "Permissions"). Billing fields (`price`, `price_interval`, `price_trial_days`, `price_external`) and listing fields fill the App Store listing: `references/app-publishing.md`, "Listing".

### Data models — `models/*.json`

The database schema. Three shapes:

- **Extend a standard model** (`models/products.json`; `models/accounts.json` for customers): the app's fields merge into the standard record under `$app.<app_id>.*`. Use when the data belongs to an existing entity. `swell inspect models` lists the standard collections.
- **A new app collection** (`models/vendor-profiles.json`, kebab-case): lives at `apps/<app_id>/<collection>` — its Fully Qualified Name, used in API paths, links and queries. Use when the data has its own lifecycle, events or public access.
- **A child collection** inside either: records that exist only under a parent.

Models also declare relationships (links), formulas, and the custom events that functions, webhooks and notifications subscribe to. Data logic belongs here; how the data looks in the dashboard belongs in content views.

**Nothing is visible to a storefront by default.** An app collection is closed to the Frontend API until the model declares what is public. The declaration can open reads, pin a filter, allow writes to listed fields, and scope a customer's reads and writes, or only writes, to their own records behind a login. That covers customer-owned data such as a wishlist, and data that everyone reads and customers submit, such as reviews; read "Storefront exposure" in `references/data-models.md` and the Frontend API skill's `references/app-data.md`. Fields added to a standard model are visible to storefronts when marked public.

Read `references/data-models.md` before authoring a model.

### Content views — `content/*.json`

Dashboard screens for a collection: list columns, record forms, tabs, navigation. A content file maps to a standard or an app collection — `content/products.json` adds fields, tabs and columns to the native product screens without replacing them, and merchants can reorder or hide the additions. Content holds UI only: a content field must match a data-model field.

- An app collection appears in the sidebar only when its list view declares `nav`. An app cannot create a new sidebar section.
- Views are lists and record forms. A multi-step flow, a chart or summary across records, a custom layout or an embedded third-party widget needs a frontend.
- A single field whose input the built-in types cannot provide renders with an app component (`type: "component"`, see "Components").

Read `references/content-models.md` before authoring views; `swell schema content --format=dts` lists every field type and property.

### Actions — declared in content views and settings files

A dashboard button or menu item that runs one of the app's functions or workflows: on a record, on selected rows, among a record's fields, or on the app's own page, optionally after a dialog that asks for inputs. This is how a merchant triggers an operation without a custom frontend.

- Swell authenticates the store user on the action invocation path, used by the dashboard and by `swell app action`. Ordinary function calls and storefront callers cannot invoke an action function. The handler still checks record state and any finer access rules — `references/actions.md` owns the invocation and authorization contract.
- The merchant waits for the result, within the function timeout. Longer work, or a bulk action over many records, runs as a workflow.

Read `references/actions.md` before adding one.

### Functions — `functions/*.ts`

Server logic. Each top-level file is one function with exactly one trigger; shared code goes in subdirectories (`functions/lib/`).

| Trigger | Runs | Scope and limits |
| --- | --- | --- |
| Model event (async) | After a record change is saved | For downstream effects: denormalization, fan-out, sync. Any declared event, standard or custom. Retried on failure. One run at a time per record, in order. Not woken by its own writes, or by an update that changes only other apps' fields |
| Model hook (sync) | Inside the API request, `before:` or `after:` the write | A `before:` hook can change what is saved or reject the write. Any declared event can be hooked: the hook runs inside the write that triggers the event. A hook does not run for writes inside a transaction, so back a critical rule with model validation as well. Not run for its own writes. → `references/functions-hooks.md` |
| Model schedule | At a time taken from the record | One pending run per record: a new time moves it, an empty one cancels it |
| Cron | On a fixed schedule | No record context |
| HTTP route | On a call to `/functions/<app_id>/<function_name>` | Fixed path, no path parameters. Callers need a key — see below. → `references/functions-routes.md` |
| Dashboard action | On an authenticated store-user action request | Dashboard click or equivalent CLI request; not a route call. → `references/actions.md` |

Calling a route from outside Swell:

- The address is `https://<store>.swell.store/functions/<app_id>/<name>`, and the caller **must send a valid public key in `Authorization` even when the route is `public`**. A storefront sends it as a header. A third-party service that only takes a callback address, such as a provider's webhook, gets the app's public key in the address, which its HTTP client turns into that header: `https://<store>:<public key>@<store>.swell.store/functions/<app_id>/<name>`. A sender whose body is not JSON, or that will not keep credentials in an address, needs another receiver: an `/app-api` endpoint of the app's frontend, or the developer's own service.
- `req.session` holds the shopper's session only when a storefront calls the route at that address.

Limits that hold for every function:

- **Edge runtime (Cloudflare Workers), not Node.js**: Web APIs such as `fetch` and Web Crypto, no Node built-ins.
- **A 10-second limit**, detailed in `references/functions.md`. Work that does not fit is a workflow.
- **No environment variables or secrets.** Configuration comes from the app's settings only (see "Configuration and secrets").
- **A function acts as the app**, with the app's `permissions`, whoever or whatever triggered it. `req.swell` is its client to the store's data and follows Backend API semantics.

Read `references/functions.md` before writing a function — the `req` object, payload shapes per trigger, errors, local testing — and the trigger's own reference where the table names one. When a deployed function, hook or webhook does not fire, start with "When a function does not run" there — except for an extension function of an integration app, where `swell inspect extensions` comes first (see "Integration apps and extensions").

### Workflows — `functions/*.ts` with `kind: 'workflow'`

A durable background process: a sequence of steps, each with its own timeout and retry policy, recorded so a completed step never runs twice, and able to sleep for long periods. Use it for work that outlives a function timeout or must survive a failure between steps — a sync to an external system, a long bulk operation, a delayed follow-up.

- Started by a function, by a frontend's server code or by a dashboard action. A workflow cannot start another workflow.
- Its store client is narrower than a function's: no transactions, and only the app's own settings.
- Workflows do not run under `swell app dev`; they are tested after a push.

Read `references/functions-workflows.md` before writing one.

### Settings — `settings/*.json`

The app's configuration, edited by the merchant on the app's page in the dashboard and read in code with `settings()`. Use it for the merchant's own provider credentials, feature flags and options; every kind of condition reads it as `$settings`. Settings files can also carry actions.

- Values belong to one store and environment. An installed app starts with empty values.
- Settings are the only configuration channel for functions and managed frontends, and they are not a secret store (see "Configuration and secrets").

Read `references/settings.md` before authoring a settings file.

### Webhooks — `webhooks/*.json`

A manifest that makes Swell POST an event to an external URL. Use it when the handling logic lives outside Swell; for logic hosted by Swell, use a function.

- Async events only: a webhook cannot validate or block a write.
- The endpoint must answer within 10 seconds. A failed delivery is retried for days, then the webhook is disabled.
- Requests are signed: verify them with `verifySwellWebhook` from `@swell/apps-sdk` before acting. The `Swell-Store-Id` header names the store.

Read `references/webhooks.md` before adding one.

### Notifications — `notifications/<name>.json` + `<name>.tpl`

A transactional email: a manifest that binds to a model event, and a Liquid template with the same basename. Sent to an address taken from the record (`contact`) or to the store's administrators.

- Sent on `created`, `updated`, or an event declared in the collection's data model; mail on a delete belongs in a function.
- **Once per record by default**: a notification bound to an update sends on the first qualifying update and never again for that record unless `repeat` is set.

Read `references/notifications.md` before authoring one.

### Frontend — `frontend/`

A web app connected to the installed app through Swell's signed request context; `swell app push` deploys it. Swell builds and hosts it by default, with Cloudflare self-hosting also supported. What it is depends on the app type:

- In an `admin` or `integration` app: custom pages for store users, shown inside the dashboard and opened through links the app declares in its content views and settings. It is the most expensive way to put something in the dashboard — content views and actions come first.
- In a `storefront` app: the store's own site, served at the storefront's address. Commerce calls go through the Frontend API (the `swell-frontend-api` skill).

What decides whether it fits:

- **Scaffold it from a Swell template** and build on its helpers and `@swell/apps-sdk`; do not hand-roll the connection. `swell-vinext` (the Next.js App Router API on Vite, rendered on the server) is the default for both kinds; `swell-react` is for a dashboard app rendered in the browser, with a small Worker for its endpoints.
- **Every address of a frontend is public, and its server code holds the app's credentials.** A dashboard frontend is shown inside the dashboard and also answers at its own address to anyone. Pages and endpoints must check who is viewing — a store user, a customer or a visitor — before returning store data.
- **Managed hosting has a fixed profile**: no custom variables, bindings or secrets, Vinext or React + Vite only, a package of up to 8 MiB. An app that needs more, secrets of its own included, can host its frontend in the developer's own Cloudflare account and stay an app. A site hosted anywhere else is not an app frontend.
- A frontend can also have server endpoints, under `/app-api`. Work that must happen with nobody looking at the frontend — reacting to store events, schedules — belongs in a function.

Read `references/frontend.md` before touching `frontend/`, then `references/frontend-dashboard.md` or `references/frontend-storefront.md` for what is being built.

### Components — `components/*.{jsx,tsx}`

Browser UI written in Preact. Each top-level file is one component, of one of two kinds:

- **Admin content field component**: renders a `type: "component"` field of a content view in place of a built-in input, in a cross-origin iframe on the app's own origin. It can call the app's functions and `/app-api` with a platform-verified caller (`req.swellContext`). A default export is required; the build fails without one. Scaffold it with `swell create component <Name> -y` and read `references/components.md` before writing one.
- **Checkout payment component**: one whose `config.extension` is `{ id }` of a `payment` extension in `swell.json`, with `targets: [{ id: 'checkout.payment.methods' }]`. Hosted checkout renders it in the same kind of iframe, in the body of the payment method bound to the extension; it returns `{ billing }` from `submit` handlers and calls `call('createIntent', data)`. Scaffold with `swell create component <Name> --extension <id> --target checkout.payment.methods -y` and read `references/payment-extensions.md` before writing one.

Shipping and tax have no component place, and a storefront renders components only when its own page mounts them with `createComponents` (`references/components.md`, "Other pages"). Components are unrelated to `frontend/`; an app may ship both.

### Assets and tests

- **`assets/`** is the app's only **public** directory: its files are served from an unauthenticated CDN address, while every other file push uploads is stored private. Put nothing there you would not publish. The app's icon and listing images are taken from its files, by name or by the paths `swell.json` gives — `references/app-publishing.md`, "Listing".
- **`test/`** holds the Vitest suite: `test/unit/` and `test/integration/`, plus helpers — `mock-request.ts` mocks the function context, and `swell-client.ts` reaches the store through the CLI's login, with no credentials to configure. Scaffold it with `swell create tests`.

## Integration apps and extensions

Integration apps declare extension slots in `swell.json` that the platform binds into native payment, shipping, or tax flows. Branch here when the requested feature is a payment method, shipping service, or tax service, or when `swell.json` has `type: "integration"` or `extensions[]`, when functions set `config.extension`, or when `components/` has top-level `.tsx`/`.jsx` files that set `config.extension` (checkout payment components; components without it are admin field components — `references/components.md`). Generic integrations (`type: "integration"` without `extensions[]`) need only `references/app-integrations.md`'s manifest section — skip the type-specific references.

Two non-obvious traps distinguish extension work from ordinary app work:

1. **Dispatch is platform-filtered, not condition-based.** A function whose `model.events` match still does not run unless the native settings record selects this app via `extension_app_id`/`extension_config_id` AND the function's `config.extension` matches. Most "function never runs" reports are merchant-activation gaps, not code bugs. Run `swell inspect extensions [--app=.]` (or with `app.<slug>.<extId>` for one extension); each row carries a `status`, an `action_owner` (`dev` | `merchant` | `null`), and an `action` string — route on `action_owner`, surface `action` verbatim when `merchant`.
2. **Binding paths differ by extension type.** Payment alt methods, payment card gateways, shipping carriers, and tax each bind through a different native settings path with a different key shape — never reuse one shape for another.

**Read** `references/app-integrations.md` **first**. **Then** load exactly one of `references/payment-extensions.md` (for `payment`) or `references/shipping-tax-extensions.md` (for `shipping`/`tax`). Do not load the other type's reference.

## Rules that cut across blocks

### Who the code runs as

Functions, workflows and a frontend's Backend client all act as **the app**: they use the credentials Swell issued to the installed app and return the same data whoever triggered them. The person is known separately, and only in some places — a store user in a dashboard frontend, in an action's `$action.user_id` and in `req.swellContext` of a route the app's own admin component calls, a customer in a storefront's session and in `req.session` of a route called through the storefront address. Decide what a person may do from that identity, never from an id in the request.

### API clients and operations

Use the client the runtime supplies. Pair this skill with the API skill when implementing queries, writes or commerce operations; do not replace the app's connection with standalone key setup.

| Runtime client | Identity and boundary | Runtime reference | Operations |
| --- | --- | --- | --- |
| Function `req.swell` | The app; Backend access within its permissions | `references/functions.md` | `swell-backend-api` |
| Workflow `req.swell` | The app, with a smaller method and endpoint surface | `references/functions-workflows.md` | `swell-backend-api`, within those workflow limits |
| Frontend Backend client (`getBackend()` in Vinext) | The app; server code authorizes business operations for the caller | `references/frontend.md` and the relevant viewer reference | `swell-backend-api` |
| Frontend Storefront clients (`getStorefront()` / `useSwell()` in Vinext) | The shopper's session, shared between server and browser | `references/frontend.md` and `references/frontend-storefront.md` | `swell-frontend-api` |

Clients share API operations, not necessarily initialization, methods or error behavior: follow the selected client's contract. A workflow's `req.swell`, for example, has no transactions and reaches only the app's own settings, and those limits still apply when reading Backend API guidance.

### Permissions

`permissions` in `swell.json` limits the app's credentials. **An empty or absent array means full access to the store**, including when the app uses only its own collections or the Storefront client. Always declare the scopes the app uses and nothing more; do not treat the scaffold's empty array as a restricted configuration.

Read `references/permissions.md` before declaring or changing permissions. It owns scope names, exemptions, wrapper calls, verification and the unresolved case where the app needs no scopes. A successful push does not prove the scope set is correct.

### Configuration and secrets

- Settings are the configuration channel for deployed functions and managed frontends; local environment files do not provision runtime variables or bindings. A frontend self-hosted on Cloudflare can use its own bindings and secrets.
- A `secret` settings field hides the value in the dashboard. It is stored and returned like any other setting, and other installed apps with access to settings can read it.
- A secret the merchant must not see cannot live in settings, functions or a managed frontend. Keep it in the developer's own service, or in a frontend hosted in the developer's own Cloudflare account. Never put one in app code or in `assets/`.

`references/settings.md` owns configuration and credential handling; `references/frontend.md` owns provisioning through Cloudflare self-hosting.

## CLI

The CLI runs the whole cycle: discover → scaffold → validate → deploy → verify. Every command takes `--help`, and interactive ones take `-y`; read `references/cli.md` before using any of them in anger — the flags are discoverable, the failure modes are not.

| Command | Use it to |
|---|---|
| `swell inspect {components\|content\|extensions\|frontend\|functions\|models\|notifications\|settings\|webhooks\|workflows\|workflow-runs}` | Read deployed state. List mode discovers, detail mode verifies after a push |
| `swell schema <type> --format=dts` | The authoritative structure for a resource type — consult before authoring |
| `swell schema <type> ./file` | Validate one manifest locally |
| `swell create {content\|function\|model\|notification\|setting\|webhook\|component\|tests\|frontend\|app}` | Scaffold; do not hand-author what a scaffold produces |
| `swell app push` | Deploy every app resource to the test environment |
| `swell app dev` | Local tunnel; model hooks, model events and dashboard actions execute locally, and the frontend is previewed through Swell |
| `swell app pull` | Adopt an existing app — a two-way sync, not a download |
| `swell app action <id>` | Run an app action as a dashboard user does: `references/actions.md`, "Verify" |
| `swell app version` / `install` / `release` | Publishing lifecycle — see `references/app-publishing.md` |
| `swell logs [-f]` | Remote logs for functions, webhooks and API calls |

Five behaviours that decide whether a deploy actually did what you think:

- **`swell app push` is not all-or-nothing.** A file the CLI cannot parse, compile or accept prints one line saying why and is skipped while the rest deploys, and the push then ends with `<n> file(s) failed to push: …` and exits non-zero. A file Swell refuses stops the push there, with its reasons.
- **Push deletes.** Per config type, remote configs whose local file is gone are removed with no prompt.
- **Push skips unchanged files by hash.** From `@swell/cli` 2.9.27 the hash covers the files a function or component imports; older CLIs leave importers stale after a lib-only edit — use `--force` there.
- **`swell app dev` pushes first, then intercepts** that environment's model hooks, model events and dashboard actions for every caller until it exits.
- **`swell api` targets the test environment** unless `--live` is passed.

## Development cycle

The five gates describe delivery of a working app change. Apply them to the requested outcome and affected behavior; related resources can share schema discovery, a deployment and test evidence. A `frontend/` uses the adaptations under "Gate alignment" in `references/frontend.md`.

- **Architecture or read-only review:** identify building blocks, constraints and dependencies. Read relevant references; do not scaffold, mutate data or deploy.
- **Debugging:** inspect the failing path and reproduce within the task's permitted environment. If a fix is requested, validate the change and the behavior it affects.
- **Narrow edits:** reuse current schema and verification evidence for unchanged behavior. Check the affected resource and its dependencies; a label or layout edit does not require recreating every record or retesting unrelated flows.
- **Working feature delivery:** complete the applicable gates end to end. When deployment is part of the task, verify the test-environment deployment and runtime behavior. For local-only work, run local checks and report deployment-dependent behavior as unverified.

### Gate 1 — Explore

Identify the resources in scope and the prerequisites they depend on: model events for functions, webhooks and notifications; data fields for content views; relationship targets for links. Use the existing manifests and relevant references. When the task needs deployed-state discovery, list remote models with `swell inspect models` and explore them with the same command to avoid duplicating a standard resource.
If the app is an integration app or declares `extensions[]`, identify the extension type, matching extension id, required platform flow, required functions, and whether checkout components are part of the design before authoring ordinary resources.
Pass: You know (a) which resources you will create or extend, (b) which prerequisites must exist, and (c) that prerequisites are present or will be created first.

### Gate 2 — Schema

Obtain the authoritative structural rules of the target resource type before authoring. Execute `swell schema {content|function|model|notification|setting|webhook} --format=dts`. For schema-backed resources, the schema is the structural source of truth. For integration manifest metadata and components, first check whether the current CLI exposes schema support; otherwise use the extension references and deploy-time validation.
Pass: You have the schema output and understand the structural requirements for your resource type.

### Gate 3 — Author & Validate

For new schema-backed resources, scaffold with `swell create {content|function|model|notification|setting|webhook} [name] [flags] -y`. Use a scaffold for supported shapes. Keep `_` out of file names. Explore `--help` for resource-specific flags. Edit existing resources in place. Validate affected files with `swell schema {type} ./path/file`. For functions and components, also run `npm run typecheck` when configured. Fix errors caused by the change.
Pass: Supported local validation and relevant type checks pass. Name unavailable checks and any pre-existing failures separately; do not claim deployment validation from local checks alone.

### Gate 4 — Deploy & Verify

When deployment is in scope, push resources to the platform test environment with `swell app push`. The platform performs additional validation beyond local schema checks: reference integrity (e.g., links to non-existent collections), reserved field conflicts, and event binding validity. Deployment errors indicate issues local validation cannot catch. Verify the affected deployed resources with `swell inspect <type> --app=.` for list-level state (enabled, trigger, failure indicators) and `swell inspect <type> <key>` for the full record. For runtime probing, paste the commands printed under `Next steps` (e.g. `/events`, `/events:webhooks`) rather than constructing event or log queries by hand. For integration apps, also run `swell inspect extensions --app=.` and act on `action_owner`/`action` per `references/app-integrations.md`.
Pass: Push exits 0 with no `file(s) failed to push` line. List-mode meta shows the resource enabled with the expected trigger/binding; detail-mode JSON matches the source manifest.

### Gate 5 — Test

Confirm the affected behavior under realistic conditions. Run relevant existing tests and add coverage when it would catch a meaningful regression. For a new resource or a change to its runtime contract, choose the applicable checks:

- Event-driven resources (model-triggered functions, webhooks, notifications): Trigger via `swell api [post|put|delete] /apps/<app_id>/<collection>` with payloads matching event conditions (model events propagate asynchronously).
- Route functions: Call via `swell api [get|post|put|delete] /functions/<app_id>/<function_name>` with appropriate `--body`.
- Action functions: cannot be called as routes. Run the action from the dashboard, or with `swell app action <id>` (`references/actions.md`).
- Data models: Execute create → read → update → delete cycle via `swell api` or integration test. Test relationship expansion with `?expand=`.

Pass: The affected behavior produces the expected result and relevant tests pass. State any runtime checks that could not be performed within the task's scope.

Consider formalizing your checks as unit and integration tests of the app. Scaffold tests with `swell create tests` if necessary.

## References

Load a reference when its block is in play; none of them needs to be read up front.

| Reference | Read it when |
| --- | --- |
| `references/cli.md` | Before relying on any CLI command: push, pull, dev, inspect, validation |
| `references/data-models.md` | Authoring a model: shapes, links, events, storefront exposure |
| `references/content-models.md` | Authoring dashboard views |
| `references/actions.md` | Adding a dashboard action |
| `references/functions.md` | Writing or debugging any function |
| `references/functions-hooks.md` | The function is a `before:` / `after:` hook |
| `references/functions-routes.md` | The function is an HTTP route |
| `references/functions-workflows.md` | Writing a workflow |
| `references/settings.md` | Authoring settings; handling credentials |
| `references/permissions.md` | Declaring or changing `permissions`; a 403 from the app's own client |
| `references/webhooks.md` | Adding or debugging a webhook |
| `references/notifications.md` | Authoring an email notification |
| `references/frontend.md` | Anything in `frontend/` — read first |
| `references/frontend-dashboard.md` | Dashboard pages of an `admin` or `integration` app |
| `references/frontend-storefront.md` | The site of a `storefront` app |
| `references/app-integrations.md` | Integration apps and `extensions[]` — read first |
| `references/components.md` | A component for an admin content field |
| `references/payment-extensions.md` | A `payment` extension or a checkout payment component |
| `references/shipping-tax-extensions.md` | A `shipping` or `tax` extension |
| `references/app-publishing.md` | Versions, installing in other stores, releasing, billing and listing fields |
