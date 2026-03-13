---
name: aureuserp-plugin-builder
description: Build or refactor AureusERP Laravel plugins using the project’s plugin-manager and Filament conventions. Use when creating/updating plugin service providers, plugin registration, install/uninstall flow, dependency setup, admin/customer panel wiring, ACL and role permissions, policies, resources/clusters/pages/widgets, settings pages, dashboard pages, model structure, and table views.
---

# Plugin Builder

Follow this workflow to build plugins exactly like existing `plugins/webkul/*` modules.

## Workflow

1. Read `references/plugin-patterns.md` first.
2. Inspect the target plugin and its nearest sibling modules (usually `purchases`, `sales`, `projects`, `website`, `accounts`).
3. Implement/adjust service provider first (`*ServiceProvider`) using `PackageServiceProvider` + `Package` chain.
4. Implement/adjust plugin class (`*Plugin`) for panel-aware registration (`admin`, `customer`).
5. Ensure package composer wiring exists (`composer.json` PSR-4, `extra.laravel.providers`, plugin factory/seeder namespaces).
6. Register ACL surface in `config/filament-shield.php`.
7. Add or align policies under `src/Policies` so generated permissions resolve cleanly.
8. Add settings migration(s) + settings class + settings page(s) when feature flags/configuration are needed.
9. Add dashboard/pages/widgets and clusters/resources based on panel + module scope.
10. Add table views to list/manage pages using `HasTableViews` + `PresetView`.
11. Add/update translations using plugin language folder conventions and nested keys.
12. Verify installation and permission lifecycle with install commands.

## Required Conventions

- Extend `Webkul\PluginManager\PackageServiceProvider` for each plugin service provider.
- Configure package metadata using chained methods on `Package`:
`name`, `hasViews`, `hasTranslations`, `hasRoute`/`hasRoutes`, `hasMigrations`, `runsMigrations`, `hasSettings`, `runsSettings`, `hasSeeder`, `hasDependencies`, `hasInstallCommand`, `hasUninstallCommand`, `icon`.
- Add installation dependencies in both places:
`->hasDependencies([...])` and install command `->installDependencies()`.
- Use plugin install command pattern:
`->hasInstallCommand(fn (InstallCommand $command) => $command->installDependencies()->runsMigrations()->runsSeeders())`
(adjust seeders when plugin has none).
- Register plugin into Filament via `Panel::configureUsing(fn (Panel $panel) => $panel->plugin(YourPlugin::make()));`.
- Gate plugin registration with install state in plugin class:
`if (! Package::isPluginInstalled($this->getId())) { return; }`.
- Ensure plugin package `composer.json` includes:
`autoload.psr-4` plugin namespace, `extra.laravel.providers` service provider entry, and plugin database factory/seeder namespaces when used.
- For admin/front split, use panel conditions in `register(Panel $panel)`:
`$panel->when($panel->getId() == 'admin', ...)` and/or `... == 'customer'`.
- Discover Filament components from panel-specific folders:
`discoverResources`, `discoverPages`, `discoverClusters`, `discoverWidgets`.
- Register ACL manage/exclude entries in `config/filament-shield.php` for resources/pages.
- Keep `RoleResource`/shield flow compatible with plugin key naming from `PluginManager\PermissionManager`.
- Use settings with Spatie Laravel Settings:
settings migration in `database/settings/*`, class in `src/Settings/*`, settings UI as `SettingsPage` when needed.
- Use table views on list/manage pages with:
`use HasTableViews;` and implement `getPresetTableViews(): array` returning `PresetView` entries.
- Use plugin translation structure under `resources/lang/en` and keep keys nested by UI surface (`navigation`, `form.sections`, `table.columns`, `table.filters`, `infolist.sections`, `actions`, `notifications`).

## Admin + Front Panel Setup

Mirror `purchases`, `website`, and `blogs` when plugin needs both panels:

- Structure Filament folders by panel:
`src/Filament/Admin/...` and `src/Filament/Customer/...`.
- In plugin `register()`:
- Configure customer panel resources/pages/clusters/widgets under the `customer` condition.
- Configure admin panel resources/pages/clusters/widgets under the `admin` condition.
- Add panel-specific navigation items (for example settings shortcuts) with visibility checks.
- If customer auth UX is custom (example: `website`), configure panel auth pages in plugin registration.
- For front/customer experience, also align plugin `routes/web.php`, frontend views, and Livewire components with panel behavior when module exposes customer-facing pages.

## Translation Convention

- Keep plugin translation root at `plugins/<vendor>/<plugin>/resources/lang/en`.
- Mirror Filament location in translation path:
`filament/resources/...`, `filament/admin/...`, `filament/customer/...`, `filament/clusters/...`, `filament/pages/...`, `filament/widgets/...`, plus `models`, `enums`, and top-level `app.php` where needed.
- Keep resource/page translation file layout explicit. Example:
- `resources/lang/en/filament/resources/product.php` (resource-level labels)
- `resources/lang/en/filament/resources/product/pages/create-product.php`
- `resources/lang/en/filament/resources/product/pages/edit-product.php`
- `resources/lang/en/filament/resources/product/pages/list-products.php`
- `resources/lang/en/filament/resources/product/pages/view-product.php`
- For admin/customer split, prefix under panel path:
- `resources/lang/en/filament/admin/...`
- `resources/lang/en/filament/customer/...`
- Keep file names kebab-case and aligned with resource/page/action names.
- Prefer deeply nested, predictable arrays grouped by UI surface:
- `navigation.title`, `navigation.group`
- `form.sections.<section>.title`
- `form.sections.<section>.fieldsets.<fieldset>.title`
- `form.sections.<section>.fields.<field>.label|helper-text`
- `table.columns`, `table.groups`, `table.filters`
- `table.record-actions.<action>.notifications.<state>.title|body`
- `table.toolbar-actions.<action>.notifications.<state>.title|body`
- `table.empty-state.heading|description`
- `infolist.sections.<section>.entries.<entry>.label|helper-text`
- Use consistent key spelling (`filters`, not `fileters`).
- Keep translation keys stable and consume them from code via `__('plugin::path.to.key')`.
- `__()` usage examples:
- Resource label: `__('products::filament/resources/product.navigation.title')`
- Page title: `__('products::filament/resources/product/pages/create-product.title')`
- Field label: `__('products::filament/resources/product.form.sections.general.fields.name')`

## Extending Base Resources and Models

Prefer extension over duplication when a base module already defines the domain behavior.

- Extend base Filament resources from source plugins (common in `accounting`, `invoices`, `sales`, `purchases`, `contacts`, `recruitments`).
- Keep child resource focused on deltas: cluster assignment, pages map, minor schema/table overrides, extra actions.
- For models, follow plugin-local model namespace and existing trait conventions (`HasFactory`, soft deletes, sortable, permission traits where applicable).

## ACL, Roles, and Permission Lifecycle

- Define plugin resource/page permission scope in plugin `config/filament-shield.php`.
- Keep cluster/page excludes updated so only intended permission keys are generated.
- Ensure policy methods match expected permission keys.
- Rely on install lifecycle to regenerate/sync permissions (plugin install command and ERP install flow).
- When changing ACL surface, validate role permission assignment via security role management UI/logic.

## Settings, Dashboard, and Table Views

- Settings:
- Add settings migration in `database/settings`.
- Add settings class extending `Spatie\LaravelSettings\Settings`.
- Add settings page extending `Filament\Pages\SettingsPage` (commonly clustered under settings).
- Dashboard/pages/widgets:
- Use page shield traits on custom dashboards/pages.
- Register widget sets via dashboard page `getWidgets()`/`getHeaderWidgets()`.
- Place pages/widgets in panel-appropriate folders.
- Table views:
- Add `HasTableViews` to list/manage pages.
- Define named preset tabs with `PresetView::make(...)->modifyQueryUsing(...)`.
- Use favorites/default presets where relevant.

## Verification Checklist

1. Plugin appears in plugin manager and installs via `<plugin>:install --no-interaction`.
2. Dependencies auto-install in correct order.
3. Admin and/or customer panel components appear only on intended panel.
4. Shield permissions include new resources/pages and exclude intended clusters/pages.
5. Policies resolve and UI actions obey authorization.
6. Settings persist and settings pages load.
7. Dashboard pages/widgets render without permission regressions.
8. Table preset views apply expected query behavior.
