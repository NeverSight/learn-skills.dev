---
name: bitrix-framework
description: 'Canon for any 1C-Bitrix / Bitrix24 PHP task — /local only, D7 first, DI boundaries, security defaults, version policy and Since markers. Use at the start of Bitrix work or when unsure which bitrix-* skill applies.'
---

# Bitrix Framework canon

Baseline: main 23.0+ · Verified: main 26.800.0

Pick task skills by their descriptions; this file holds the rules they all assume.

## Version policy

- Check the project first: `bitrix/modules/main/classes/general/version.php` → `SM_VERSION`.
- `**Since main X.Y**` — feature needs that version; each skill gives a fallback.
- `**Since main X.Y\***` — exact version unknown; verified present in X.Y and absent in main 25.100.500. It may exist a bit earlier. Same for modules (`**Since rest 26.200\***`): absent in the module version shipped with main 25.100.500.
- Kernel sources: `bitrix/modules/<module>/lib/`. Since main 26.600 many `lib/` dirs are PascalCase (`lib/Data`), older ones lower-case — search case-insensitively.

| Feature | Since main |
| --- | --- |
| Routing (`/local/routes`) | 21.400 |
| `/local/.settings.php` | 24.100 |
| Validation (`Bitrix\Main\Validation`) | 24.300 |
| Controller render helpers | 25.700 |
| New `make:*` (service, entity, event, message, agent …) | 25.900 |
| Persistent Storage | 25.1100 |
| Controller filter attributes, rules on action params, `LoggerFactory` | 26.250* |
| Module installers on `install/migrations` (`UpdateSystem\Migration`) | 26.600* |
| `#[ActionAccess]` | 26.600* |
| Feature flags `Config\Feature` | 26.700 |

## Hard canons

- All custom code in `/local/`; never edit `/bitrix/`. A file in `/local/` wins over the same path in `/bitrix/`.
- D7 first; legacy (`CIBlock*`, `CUser`, `$DB`) only where no D7 API exists — say so in a comment.
- Thin controllers, routes, components and event handlers; logic in services; data in ORM tablets.
- `Loader::includeModule()` / `requireModule()` before any module class.
- `declare(strict_types=1)`, typed signatures, `Result`/`Error` across module boundaries instead of exceptions or magic arrays.
- `/local/.settings.php` replaces `/bitrix/.settings.php` entirely — copy every section, not just the changed one.
- Routes only in `/local/routes/*.php` (module routes are `require`d from there). Never add new routes to `urlrewrite.php`.
- Migrations: a module's own tables/events/agents go to its installer (`install/migrations`, `bitrix-modules`); project data and settings go to `sprint.migration`. If it is not installed, propose installing it — never invent a migration framework.

## DI boundaries

| Context | Constructor DI | How |
| --- | --- | --- |
| Application service | Yes | autowired by `ServiceLocator::get(FQCN)`; register in `services` only for interfaces or scalar args |
| Controller action | Yes, params | type-hint a concrete class; interfaces in action params are not resolved |
| Controller constructor | No | engine passes `Request` only |
| Console command | No | `ServiceLocator::getInstance()->get()` in `execute()` |
| Event handler | No | resolve inside the handler |
| Messenger receiver | Yes | autowired; register only for interfaces or scalar args |

`services` entry with only `className` for a concrete class disables autowire (`new $class()` without args). Use `constructor` closure or `constructorParams`, or don't register it. Details: `bitrix-service-locator`.

## Security defaults

- Never read `$_GET`/`$_POST`/`$_SESSION`/`$_COOKIE`; use `Context` request and `Application::getSession()`.
- AJAX actions keep default prefilters (`Authentication`, `HttpMethod`, `Csrf`); add rights checks per action.
- Escape output (`htmlspecialcharsbx`, `Json::encode`), cast input, whitelist anything that reaches ORM `select`/`order`/`runtime`/`ExpressionField`.
- Secrets from env or `.settings.php`, never in code, options or migrations.

## Before you finish

- [ ] Code in `/local/`, modules loaded, strict types.
- [ ] Every kernel class, method and named argument exists in the project's main version (check `Since`).
- [ ] No DB access in controllers/components/templates; errors returned via `Result`.
- [ ] Cache with tags where reads repeat; ORM cache cleared via `cleanCache()`.
- [ ] Events and agents registered on install and removed on uninstall.
- [ ] `exception_handling.debug` is `false` on production.
