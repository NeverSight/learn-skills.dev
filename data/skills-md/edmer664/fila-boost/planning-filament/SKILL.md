---
name: planning-filament
description: "Generate comprehensive, self-contained Filament v5.x architecture and implementation plans for Laravel applications. Use when the user asks to plan, design, architect, or spec out Filament v5 resources, modular form schemas, tables, infolists, widgets, multi-tenancy, custom themes, clusters, or admin panels."
license: MIT
compatibility: "Laravel 10+ and Filament v5.x projects (recommended with Laravel Boost MCP)"
metadata:
  author: edmer664
  version: "1.2.1"
---

# Filament v5.x Architecture Planning (`planning-filament`)

## What This Skill Does

Generates a structured, self-contained Filament v5.x architecture and implementation plan saved to `plans/{feature}.md`. It enforces Filament v5's strict modular class architecture (`Schemas/`, `Tables/`, `Infolists/`), flags unresolved business decisions upfront, and defines Eloquent models, migrations, policies, widgets, tenancy rules, themes, and Pest PHP test suites before any application code is written.

## When to Use It (and When Not To)

**Use this skill when:**
- Designing or planning a new Filament v5 resource, cluster, or admin panel feature.
- Drafting technical specifications for Filament forms, tables, infolists, or dashboard widgets.
- Planning multi-tenant Filament panels (`Team` / `Company` scoping) or custom panel themes.
- The user mentions "plan filament", "filament architecture", "filament resource plan", or asks for a spec before coding.

**Do NOT use this skill when:**
- Auditing or reviewing existing code against an already-written plan (use `reviewing-filament-plans` instead).
- Making a trivial one-line bug fix to an existing Blade view or non-Filament controller.

## Inputs Needed

- **Feature Description**: Domain entities, relationships, fields, status workflows, and user roles.
- **Target Panel / Tenancy Context** (optional): Panel ID, tenant model (e.g., `Team`), and custom styling requirements.
- **Output Path** (optional): Defaults to `plans/{feature-slug}.md`.

## Step-by-Step Procedure

### 1. Ground Against Official Filament v5.x Docs

Before guessing method signatures or component namespaces:
- If Laravel Boost MCP (`search-docs`) is available, query `packages: ["filament/filament"]` for relevant topics (e.g., `queries: ["infolist entries", "repeatable entry"]`, `queries: ["stats overview widget", "chart widget"]`, `queries: ["multi-tenancy"]`).
- If `generate_filament_plan` MCP tool is available, you may invoke it to scaffold the baseline plan structure.

### 2. Surface Ambiguities & Unresolved Decisions

At the very top of the plan under `## ⚠️ Unresolved Decisions`, list any underspecified business rules that require developer confirmation before implementation (e.g., soft-delete behavior, decimal vs. integer cents for currency, tenant isolation boundaries, role permissions).

### 3. Enforce Strict Filament v5.x Modular Class Layout

Every planned Filament v5 resource MUST separate form schemas, tables, and infolists into dedicated classes rather than inlining monolithic closures inside `{Name}Resource.php`:

```plaintext
app/Filament/Resources/{Cluster?}/{Name}s/
├── {Name}Resource.php
├── Pages/
│   ├── List{Name}s.php
│   ├── Create{Name}.php
│   ├── Edit{Name}.php
│   └── View{Name}.php
├── Schemas/
│   └── {Name}Form.php          # Dedicated Schema configuration class
├── Tables/
│   └── {Name}sTable.php        # Dedicated Table configuration class
└── Infolists/
    └── {Name}Infolist.php      # Dedicated Infolist configuration class
```

### 4. Specify Full Domain Coverage

Include concrete class names, method signatures, and field/column definitions for:
- **Data Layer**: Eloquent models (`app/Models/{Name}.php`), `$fillable`, `casts(): array` method, relationships, and migrations.
- **Form Schema (`Schemas/{Name}Form.php`)**: `configure(Schema $schema): Schema` with layout components (`Section`, `Grid`), inputs, validation rules, and relationship selects.
- **Table Schema (`Tables/{Name}sTable.php`)**: `configure(Table $table): Table` with columns, filters, row actions (`EditAction`, `ViewAction`, `DeleteAction`), and bulk actions.
- **Infolist Schema (`Infolists/{Name}Infolist.php`)**: `configure(Infolist $infolist): Infolist` using `TextEntry`, `IconEntry`, `ImageEntry`, `Badge`, and `RepeatableEntry`.
- **Widgets**: Dashboard and resource widgets (`StatsOverviewWidget`, `ChartWidget`, `TableWidget`).
- **Multi-Tenancy**: Tenant models, panel provider `->tenant(Team::class)` configuration, and tenant-scoped relationships.
- **Themes & Styling**: Panel color palettes (`Color::Amber`, `Color::Slate`), custom fonts, and `PanelsRenderHook` registrations.
- **Authorization Policies**: `App\Policies\{Name}Policy` covering `viewAny`, `view`, `create`, `update`, and `delete` with tenant ownership checks.
- **Pest PHP Tests**: Feature test specifications (`tests/Feature/Filament/{Name}ResourceTest.php`) testing page rendering, form validation, table filtering, actions, and policy enforcement.

### 5. Write the Plan File

Save the complete Markdown plan to `plans/{feature}.md` in the project root.

## Validation / How to Know We're Done

- [ ] Plan file exists at `plans/{feature}.md`.
- [ ] `## ⚠️ Unresolved Decisions` clearly highlights any domain ambiguities.
- [ ] Every resource defines modular `Schemas/{Name}Form.php` and `Tables/{Name}sTable.php` classes (plus `Infolists/{Name}Infolist.php` when read-only views are needed).
- [ ] Authorization policies and Pest PHP test cases are explicitly specified for every resource.

## Common Failure Modes and Fixes

- **Failure Mode**: Placing `->schema([...])` and `->columns([...])` directly inline inside `{Name}Resource.php` (Filament v3 style).
  - **Fix**: Extract form fields into `Schemas/{Name}Form::configure(Schema $schema)` and table columns into `Tables/{Name}sTable::configure(Table $table)`.
- **Failure Mode**: Hallucinating non-existent Filament v5 methods or namespaces.
  - **Fix**: Verify component imports and method signatures via Laravel Boost's `search-docs` tool prior to finalizing the plan.
- **Failure Mode**: Omitting tenant ownership checks in multi-tenant panels.
  - **Fix**: Ensure every model includes the `team_id` (or tenant foreign key) relationship and every policy verifies `$user->teams->contains($record->team_id)`.
