---
name: bitrix-controllers
description: "Engine Controller/JsonController: thin actions, filter attributes, CurrentUser, errors. Use for AJAX/REST/routed endpoints."
---

# Bitrix Controllers

Baseline: **main 23.0+**. Features newer than baseline are marked **Since**.

Progressive disclosure: open **only** the rule files that match the task. Do not read every `rules/*.md`.

## How to use

1. Identify the layer the task touches.
2. Open the matching `rules/*.md` below.
3. Prefer framework-native Bitrix patterns over custom abstractions.


## Choose a rule file

### When to read `rules/basics.md`

Read `rules/basics.md` (`Location, thin controller, autowire`) when the task involves:

- Location and Naming
- Minimal Controller
- Action Parameter Autowiring
- Controller Lifecycle
- Additional Autowire Types
- Front-end Call

### When to read `rules/filters.md`

Read `rules/filters.md` (`Filters and attributes`) when the task involves:

- Default Prefilters
- Action Filters
- PHP 8 Attribute Filters (preferred)
- `#[ActionAccess]` / `AccessCheck` (module ACL)

### When to read `rules/errors-response.md`

Read `rules/errors-response.md` (`Errors, responses, scope`) when the task involves:

- Errors
- Response Types
- Scope (AJAX / REST / CLI)
- Checklist

## Cross-cutting invariants (apply regardless of rule file)

- Never configure the same action **both** via filter attributes and `configureActions()` — the controller fails with `Invalid configuration of actions`.
- Do not register one controller both as an HTTP route target (`/local/routes/web.php`) and in the AJAX `controllers.defaultNamespace` of `.settings.php`. Keep separate `Web\*` and `Ajax\*` controllers, each with its own `getAutoWiredParameters()`.
- Rendering helpers `renderView()` / `renderComponent()` / `renderExtension()` — **Since main 25.700.0**. They return HTML (`HttpResponse`-based) and are for HTTP routes only; `BX.ajax.runAction()` expects JSON. For AJAX use `renderComponentAjax()` — JSON with `html`, `assets`, `additionalParams`, `componentResult`. `renderExtension()` / `renderView()` / `renderComponent()` accept `withSiteTemplate: false` to skip the site template. `renderExtension()` requires `controllerEntrypoint` in the extension's `config.php`; it renders in the browser (not SSR).
- `PageNavigation` autowire (global, nav id `nav`) accepts a page size only within 1–50 (`setPageSizes(range(1, 50))`); an out-of-range `size` is silently ignored and the default 20 is used.
- Request DTOs are wired with `new ValidationParameter(...)` in `getAutoWiredParameters()` — **not** a `#[ValidationParameter]` attribute (that class does not exist).
- `#[ActionAccess]` requires the controller to implement `AccessCheckControllerInterface`. Without it the engine throws `SystemException`.

## Checklist

- [ ] Opened only the rule file(s) needed for this task.
- [ ] Followed DI / `/local/` / security canons from `AGENTS.md`.
- [ ] Respected the cross-cutting invariants above (no attribute + `configureActions()` mix, separate Web/Ajax controllers).
