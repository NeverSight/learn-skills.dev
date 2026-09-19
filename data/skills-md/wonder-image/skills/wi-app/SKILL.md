---
name: wi-app
description: |
  Work inside the wonder-image/app framework package — the Composer library at github.com/wonder-image/app. This is the framework core, not a site that consumes it.

  TRIGGER when:
  - the repo's composer.json declares `"name": "wonder-image/app"`
  - editing files under `class/App/*`, `app/config/routes/*`, `app/http/*`, `app/bootstrap/*`, `app/middleware/*`, `class/App/Module/*`, `class/Console/*`
  - editing shared UI components under `class/Elements/Components/*`, media under `class/Elements/Media/*`, or their renderers under `class/Themes/{Wonder,Bootstrap}/*`
  - modifying Model, Resource, PageSchema, Repeater, ModelRegistry, ResourceRegistry, ResourceRouteRegistrar, Credentials, or the `wonder-image.php` entrypoint
  - changing bootstrap order, `ROOT`/`.env` resolution, module discovery, generated backend/API CRUD routes, or `php forge ...` command sources
  - updating `docs/app/*` for bootstrap, architecture, routing, or layout conventions

  SKIP when:
  - the repo is a Wonder site that installs wonder-image/app under `vendor/` (e.g. wonder-image/new-site or any project scaffolded from it) — use wi-site
  - the change is in `custom/`, `app/Models`, `app/Resources`, `lang/`, or `assets/` of a site
  - the task is in wonder-image/lib (the JS/CSS design system) — different repo
---

# Wonder Image App

## Overview

Use this skill to work inside `wonder-image/app` as a framework package, not as a standalone app. Keep the framework-versus-site boundary explicit before changing code, running commands, or deciding where new logic belongs.

## Glossary

Shared vocabulary across `wi-app` and `wi-site` (identical wording in both skills):

- **framework** — `wonder-image/app` (Composer package, github.com/wonder-image/app). Lives at the repo root when wi-app is active; lives at `vendor/wonder-image/app/` inside a site.
- **lib** — `wonder-image/lib` (npm package, github.com/wonder-image/lib). The JS / CSS design system. Source at `node_modules/wonder-image/src/`; compiled copy at `assets/lib/wonder-image/dist/`.
- **scaffold** — `wonder-image/new-site` (github.com/wonder-image/new-site). The site template. The scaffold itself is also a valid site.
- **site** — any project whose `composer.json` depends on `wonder-image/app` (i.e. installs the framework under `vendor/wonder-image/app`). Typically the scaffold or a project derived from it. **Canonical term — prefer "site" over older mixed uses like "consumer project" / "consumer app".**
- **module** — external Composer package `wonder-image/<slug>` discovered via Composer (or filesystem fallback). Ships its own models / resources / routes via `module.json` + a `ModuleInterface` entrypoint.
- **`custom/`** — site-only directory for project pages, components, layouts, routes, config, and helpers. Never present inside the framework.
- **`app/Models` / `app/Resources`** — site PSR-4 roots (`App\Models\...` / `App\Resources\...`). Distinct from the framework's `class/App/Models` / `class/App/Resources` (`Wonder\App\Models\...` / `Wonder\App\Resources\...`).

## When to switch to wi-site

Switch to [`wi-site`](../wi-site/SKILL.md) when **any** of these signals are true — the work belongs in a site repo, not in the framework:

- the repo's `composer.json` does **not** declare `"name": "wonder-image/app"`; instead it lists `wonder-image/app` under `require` (the framework is installed as a dependency).
- a `PRODUCT.md` exists at the repo root declaring a Wonder site (`site_type: landing` / `corporate` / `blog` / `ecom` / `rsvp`) — that file only exists on sites, never inside the framework itself.
- `vendor/wonder-image/app/` exists at the repo root — the framework is installed under `vendor/`, so this is a site.
- the requested change lives under `custom/`, `app/Models`, `app/Resources`, `lang/`, `assets/{ASSETS_VERSION}/`, or any path that does not exist inside the framework repo.
- the task is "add a page", "translate strings", "register a permission key for this site", "edit color tokens", "use a `.wi-*` component / lib class", or any work that **uses** (rather than extends) the framework.
- you are about to patch a file under `vendor/wonder-image/app/`. Do not. Either reshape the change to live in `custom/` / `app/` (still wi-site), or open the change against the framework repo itself (then wi-app applies there).

## Start Here

1. Classify the request before editing anything.
2. Decide whether the change belongs to the framework, a site, or an external module package.
3. Read only the reference file that matches the task:
   - `references/architecture.md` for bootstrap, registries, routes, env resolution, or module loading
   - `references/model-and-resource.md` for the Model / Resource extension API, schemas, repeater fields, and `CustomPageSchema`
   - `references/permissions-and-users.md` for the permission builder API, permission keys, and shared user-management resources
   - `references/workflows.md` for change placement, validation, and common gotchas

## Core Rules

- Treat `wonder-image/app` as a Composer library. The real runtime lives in the site that installs it under `vendor/wonder-image/app`.
- Assume `php forge ...` commands are site-side commands unless you confirm otherwise. Do not expect a `forge` executable in this package root.
- Prefer `class/App/*` for new logic. Touch legacy `app/*` only when the runtime still depends on it.
- API handlers live under `app/http/api/*`. Do not reintroduce package handlers under `app/api/*`; call routed `/api/...` endpoints via `Path::$api`, `Path::$appApi`, and `Path::$apiDT`.
- Keep runtime fallbacks and seed payloads separate:
  - `Wonder\\App\\RuntimeDefaults` is for runtime defaults used while rendering or composing in-memory config.
  - `Wonder\\App\\SeedDefaults` is for idempotent bootstrap/seed payloads consumed by `build/row`, setup commands, and seed-backed singleton forms.
- Program in terms of future integration and extension. Prefer class and function designs that can be reused, extended, overridden, or integrated by sites and external modules instead of solving only the immediate local case.
- Keep the architecture split clear:
  - `Model::tableSchema()` defines SQL structure
  - `Model::dataSchema()` defines data preparation and persistence behavior
  - `Resource::formSchema()` defines backend inputs
  - `CustomPageSchema` handles non-CRUD backend pages
  - `Repeater` handles repeatable rows and related-row sync
- **Form inputs go through the `FormField` hierarchy — always.** Every input on the frontend Wonder theme (`class/Themes/Wonder/`) and the backend Bootstrap theme (`class/Themes/Bootstrap/`) is declared via `FormField` / `RepeaterColumn` (or directly through a typed `Inputs\Input*`) and rendered through `Input::render($theme)`. No raw `<input>` / `<select>` / `<textarea>` HTML, no ad-hoc render functions. Missing input types are added at the framework layer (typed `Inputs\Input*` with `element()` → helper on `FormField` → renderer under each theme), not patched at the call site. Full rationale and the four-step "missing type" workflow in [`references/model-and-resource.md`](references/model-and-resource.md#formfield-hard-rule).
- Update `docs/app/*` in the same work when you change bootstrap, architecture, routing, layout structure, or developer-facing conventions.

## Task Routing

### Bootstrap or runtime

Read `references/architecture.md`, then inspect `wonder-image.php`, `class/App/Credentials.php`, route config, and the relevant registries. Be careful with anything that resolves `ROOT`, loads `.env`, or changes early bootstrap order.

### CRUD resources, backend pages, or API generation

Read `references/model-and-resource.md` first for the Model / Resource extension contract, then `references/architecture.md` for registry precedence and route emission, then `references/permissions-and-users.md` for the permission keys referenced from `Resource::permissionSchema()`.

### Form inputs (frontend Wonder or backend Bootstrap)

Read `references/model-and-resource.md` — section "FormField hard rule". Every input on either theme is declared via `FormField::key(...)` / `RepeaterColumn::key(...)` or directly through a typed `Inputs\Input*`, then rendered through `Input::render($theme)`. New input types are added under `class/App/ResourceSchema/Inputs/`, implement their own `element()`, expose a helper on `FormField`, and use renderers under `class/Themes/Wonder/` and `class/Themes/Bootstrap/` — not bespoke HTML at the call site.

### UI / styling inside default components or themes

When the change touches a default component shipped by the framework (`class/App/Resources/.../*.php` views, the non-form Components under `class/Elements/Components/`, Media under `class/Elements/Media/`, the form Components under `class/Elements/Form/Components/`, the Wonder / Bootstrap renderers under `class/Themes/{Wonder,Bootstrap}/`, or any `app/view/...` page used by a site), the authoritative UI rulebook is [`wi-site/references/style-and-lib.md`](../wi-site/references/style-and-lib.md). The same reuse-first-from-`wonder-image/lib` policy applies inside `wonder-image/app`: do not invent new `.wi-*` names at framework level (that is a lib-side change), do not bake site-specific tokens into a default component, and preserve compatibility with the site's `color.css` / `root.css`. This includes shared action primitives like `Button`, `Badge`, `ButtonGroup`, and `Dropdown`. For link-like attributes on shared components, prefer the common concern `class/Elements/Concerns/HasLinkAttributes.php` and persist `href`, `target`, `rel`, `title`, `onclick`, `download` in `attributes` so theme renderers stay thin. Install `wi-site` alongside `wi-app` so this reference resolves locally.

### Permissions, roles, or user management

Read `references/permissions-and-users.md`. Covers the builder API (`Permissions::reset()`, `Area::make()`, `Permission::make()`), the merge with module permissions, the runtime `$PERMITS` export, and the shared `UserManagementResource` / `BackendUserResource` / `ApiUserResource` flow.

### Module system

Read `references/architecture.md`. Preserve compatibility with Composer discovery, filesystem fallback, enabled-module state, and route/model/resource registration from external packages.

### Console commands or local-start flows

Read `references/workflows.md`. Remember these commands are meant to be executed from a site even when their source lives in this package.

## Validation

- Lint every touched PHP file with `php -l`.
- Run `composer dumpautoload` when classes move or new classes are added.
- If the change affects bootstrap, routing, console commands, resources, models, or request handlers, validate from a site with `php forge update --local` and `php forge start`.
- If the change is Herd-specific, also validate the local routing path described in `references/workflows.md`.

## Output Expectations

- Explain whether the fix belongs in the framework, a site, or a module package.
- Name the main files and registries involved instead of describing the framework generically.
- Call out integration validation needs whenever a framework-root edit only becomes real through a site.
