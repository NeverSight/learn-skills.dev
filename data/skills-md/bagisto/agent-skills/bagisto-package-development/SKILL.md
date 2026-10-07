---
name: bagisto-package-development
description: Use when creating or changing a Bagisto package — service providers, migrations, models, contracts, proxies, repositories, routes, controllers, Blade views, localization, admin menus, ACL or system configuration. Trigger phrases include "new package", "service provider", "migration", "model", "repository", "controller", "route", "ACL", "admin menu", "system config", "concord".
requires: bagisto-coding-standards
license: MIT
---

# Package Development in Bagisto

A Bagisto package is a self-contained Laravel module under `packages/Webkul/<Name>/`.
Core packages draw from one shared layout but take only the parts they need —
copy the closest existing package rather than scaffolding a generic Laravel one.

## Reference files — load only what the current task needs

| File | Load when |
|---|---|
| [core.md](core.md) | Creating a package — directory layout, `composer.json`, providers, Concord registration |
| [data-layer.md](data-layer.md) | Migrations, models, contracts, proxies, repositories |
| [ui.md](ui.md) | Routes, controllers, Blade views |
| [features.md](features.md) | Admin menus, ACL, system configuration |

## The shape of a package

```
packages/Webkul/<Name>/src/
├── Config/           # system.php, admin-menu.php, acl.php
├── Contracts/        # one interface per model
├── Database/         # Migrations/, Seeders/, Factories/
├── DataGrids/        # admin listings
├── Http/Controllers/ # separate Admin/ and Shop/
├── Models/           # Eloquent models + Proxy classes
├── Providers/        # <Name>ServiceProvider + ModuleServiceProvider
├── Repositories/     # all database access
├── Resources/        # views/, lang/{22 locales}/, assets/
└── Routes/           # admin-routes.php, shop-routes.php
```

**Most packages carry only part of this, and that is deliberate.** Only
`Providers/` is universal. Of the core packages, roughly 25 have
`Contracts/Models/Repositories`, 14 have `Config/`, 11 have
`Http/Controllers/` and 8 have `Routes/` — and the handful with all three
UI pieces are `Admin`, `Shop` and the payment gateways (`Stripe`, `PayU`,
`Razorpay`, `PayGlocal`, `PhonePe`).

A domain package such as `Category`, `CartRule`, `CMS` or `Marketing` is a
**data layer only** — contracts, models and repositories. Its admin screens live
in `Admin`, its storefront pages in `Shop`. Do not add `Routes/` or
`Http/Controllers/` to one of those unless the feature genuinely owns its own
routes, as a payment gateway does. Check the closest existing package before
deciding which directories yours needs.

## The rules that are not negotiable

- **Dual registration.** Every package registers twice: its main
  `ServiceProvider` in `bootstrap/providers.php`, and its `ModuleServiceProvider`
  in `config/concord.php`. Miss either and the package half-loads in a way that
  is hard to diagnose. See [core.md](core.md).
- **Three-part models.** Every entity is a Contract, a Model implementing it, and
  a Proxy. Repositories return the **Contract** from `model()`, and cross-package
  type hints use the **Proxy** — that is what makes a model replaceable without
  editing core. See [data-layer.md](data-layer.md).
- **Docblocks, member order, comments, the repository rule and translations**
  are owned by the **`bagisto-coding-standards`** skill. They apply to every Bagisto
  file, not only to a package, and they are the most common review rejection.
- **Fix what you touch.** A pre-existing violation in a file you edit is yours:
  scan the whole class's member order and docblocks, not just your own lines.

## Related skills

- **`bagisto-coding-standards`** — docblocks, member order, comments, repository access,
  localization. Load it alongside this one for any PHP.
- **`bagisto-datagrid-development`** — admin listing pages. `features.md` sketches the
  DataGrid; that skill owns columns, filters, actions, export and the security
  rules.
- **`bagisto-coding-standards`** — including the Blade layer: any `.blade.php`, in any package.
- **`bagisto-pest-testing`** / **`bagisto-playwright-testing`** — tests for what you build.
- **`bagisto-change-verification`** — the completion gate.

**REQUIRED SUB-SKILL:** Use bagisto-change-verification before calling any change done.
