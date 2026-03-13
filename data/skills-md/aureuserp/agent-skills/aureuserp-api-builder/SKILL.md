---
name: aureuserp-api-builder
description: Generate or update Laravel plugin REST APIs in AureusERP for any module. Use when implementing new API resources or refactoring existing endpoints to match shared project conventions for routes, controllers, requests, resources, policies, Spatie QueryBuilder filtering/includes/sorting, soft-delete restore/force endpoints, and Scribe attributes/documentation.
---

# API Builder

Follow this workflow to generate APIs that match shared AureusERP plugin conventions.

## Workflow

1. Read the conventions reference: `references/api-conventions.md`.
2. Inspect the target plugin module (models, existing policies, existing routes, and Filament resources/pages).
3. Perform Filament resource analysis before generating API classes:
- map workflow/state transitions from Filament pages and actions (create/edit/view/list and custom actions)
- extract validation rules from Filament forms/components, including conditional requirements and nested repeaters
- build request payload field definitions from user-editable fields only (exclude readonly/computed/system-managed fields)
- identify parent Filament resources/classes when the module extends resources from another plugin
- **identify optional plugin dependencies**: detect columns, relations, or features that only exist when another plugin is installed (check conditional migrations using `Schema::hasTable` or `Schema::hasColumn` guards)
4. Implement API files in this order:
- route entries in `routes/api.php`
- controller(s) in `src/Http/Controllers/API/V1`
- form request(s) in `src/Http/Requests`
- resource(s) in `src/Http/Resources/V1`
- policy methods (`restore`, `forceDelete`) when using soft deletes
5. If Filament/API classes extend a parent from another plugin, mirror that inheritance in generated API classes:
- generated request class must extend the parent plugin request class for the same API concept when available
- generated HTTP resource class must extend the parent plugin HTTP resource class for the same API concept when available
- keep child class focused on plugin-specific deltas to avoid duplicating parent validation/serialization logic
6. Keep naming and response messages consistent with existing APIs in the target plugin.
7. Validate by checking route registration and running targeted tests if present.
8. Write comments only above the function definition. Do not include any comments inside the function body.

## Required conventions

- Use route group pattern: `Route::name('admin.api.v1.<plugin>.')->prefix('admin/api/v1/<plugin>')->middleware(['auth:sanctum'])->group(...)`.
- Use `Route::softDeletableApiResource(...)` for soft-deletable resources; implement `restore()` and `forceDestroy()` in controller.
- Use Scribe PHP attributes on controllers and endpoints (`Group`, `Subgroup`, `Authenticated`, `Endpoint`, `QueryParam`, `UrlParam`, `Response`, `ResponseFromApiResource`).
- Use `Gate::authorize(...)` in each endpoint.
- Use `Spatie\QueryBuilder\QueryBuilder` with explicit `allowedFilters`, `allowedSorts`, and `allowedIncludes`.
- Return API resources for CRUD responses; return JSON `{ "message": "..." }` for delete/force-delete success responses.
- In `FormRequest`, always define validation rules as arrays (for example `['required', 'email']`), not pipe-delimited strings.
- For update handling (`PUT`/`PATCH`), define `$isUpdate = $this->isMethod('PUT') || $this->isMethod('PATCH');` and use per-field ternary rule entries (for example `$isUpdate ? ['sometimes', 'required'] : ['required']`) instead of rule-transformation loops.
- Use enum validation with rule objects in rule arrays (for example `Rule::enum(Status::class)`) instead of `'in:...'` string composition.
- Ensure every FormRequest supports partial updates consistently: fields required on create must become `$isUpdate ? ['sometimes', 'required'] : ['required']` on update unless a field is intentionally immutable.
- In `FormRequest`, only expose writable payload fields from the corresponding Filament form workflow. Do not accept or document system-calculated, readonly, hidden, or lifecycle-managed columns.
- For nested line arrays, mirror the same writable-only rule: include only user-editable fields; never validate/document computed totals, margins, status fields, or server-derived linkage columns unless explicitly editable in Filament.
- Derive `FormRequest` rules from comprehensive Filament analysis: include workflow-specific requirements, conditional validation, nested payload structure, and action-specific writable fields.
- When a module extends a Filament/resource class from another plugin, generated request classes must inherit the corresponding parent plugin request class when it exists; only append or override delta rules needed by the child plugin.
- Include `bodyParameters()` for documentation and keep examples restricted to writable fields only.
- In `JsonResource`, include scalar IDs/timestamps and conditional relations via `whenLoaded(...)`.
- When a module extends a Filament/resource class from another plugin, generated HTTP resources must inherit the parent plugin HTTP resource class when it exists; only add plugin-specific serialization fields/relations in the child class.
- **Plugin dependency handling**: when a controller action depends on a feature from an optional plugin (for example delivery operations from the `inventories` plugin), guard execution with `Package::isPluginInstalled('<plugin>')` and return a graceful empty/default response when the plugin is absent. Never let the request hit a query against a table that may not exist.

## Reference files

- `references/api-conventions.md`: canonical conventions and implementation checklist.
