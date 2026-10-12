---
name: reviewing-filament-plans
description: "Audit and review an application codebase against a generated Filament v5.x architecture plan. Use when the user asks to review, verify, audit, or check a Filament implementation against a plan in plans/*.md, checking modular Schemas/Tables/Infolists classes, widgets, multi-tenancy scoping, policies, and Pest tests."
license: MIT
compatibility: "Laravel 10+ and Filament v5.x projects"
metadata:
  author: edmer664
  version: "1.2.1"
---

# Filament v5.x Implementation Review (`reviewing-filament-plans`)

## What This Skill Does

Audits the current Laravel & Filament v5.x repository checkout against a saved architecture plan (`plans/{feature}.md`). It verifies that all planned resources, modular schemas (`Schemas/`, `Tables/`, `Infolists/`), widgets, multi-tenancy configurations, authorization policies, and Pest PHP tests exist and follow Filament v5 conventions.

## When to Use It (and When Not To)

**Use this skill when:**
- Verifying whether an implemented Filament feature matches its architecture plan in `plans/{feature}.md`.
- Auditing a Filament v5 codebase for modular class compliance (ensuring forms, tables, and infolists are not inlined inside Resource classes).
- Checking for missing model policies, tenant scoping, or Pest feature tests after code generation.
- The user mentions "review filament", "verify filament plan", "audit filament implementation", or asks to check progress against a plan.

**Do NOT use this skill when:**
- Creating a brand-new architecture plan from scratch (use `planning-filament` instead).

## Inputs Needed

- **Plan File Path**: Path to the Markdown architecture plan (e.g., `plans/{feature}.md`).
- **Application Root Path** (optional): Defaults to the current project root directory.

## Step-by-Step Procedure

### 1. Load the Target Plan & Run Automated Audit

- Read the target plan file from `plans/{feature}.md`.
- If the `review_filament_implementation` MCP tool is available, run it with `plan_path` to obtain an automated structural audit report.

### 2. Audit Filament v5.x Modular Directory Compliance

For each Resource defined in the plan:
- Confirm `app/Filament/Resources/{Cluster?}/{Name}s/{Name}Resource.php` exists and delegates to modular classes rather than declaring large inline form/table/infolist closures.
- Confirm `app/Filament/Resources/{Cluster?}/{Name}s/Schemas/{Name}Form.php` exists.
- Confirm `app/Filament/Resources/{Cluster?}/{Name}s/Tables/{Name}sTable.php` exists.
- If an infolist was planned, confirm `app/Filament/Resources/{Cluster?}/{Name}s/Infolists/{Name}Infolist.php` exists.

### 3. Verify Widgets, Tenancy, and Themes

- **Widgets**: Verify all planned `StatsOverviewWidget`, `ChartWidget`, and `TableWidget` classes exist in `app/Filament/Widgets/` or resource `Widgets/` subdirectories.
- **Multi-Tenancy**: If planned, confirm the Tenant model (`Team` / `Company`) exists, panel configuration registers `->tenant()`, and scoped models define tenant foreign keys (`team_id`).
- **Themes**: If planned, verify panel provider color palettes (`->colors(...)`), fonts, and render hooks match the plan.

### 4. Verify Security & Authorization Policies

- Confirm `app/Policies/{Name}Policy.php` exists for each planned resource model.
- Verify explicit gate methods (`viewAny`, `view`, `create`, `update`, `delete`) are implemented and enforce tenant ownership where applicable.

### 5. Verify Pest Tests & Code Quality Gates

- Confirm corresponding feature test files exist in `tests/Feature/Filament/`.
- Execute `vendor/bin/pest` and `vendor/bin/pint --test` to verify all tests pass and code style conforms to project standards.

## Validation / How to Know We're Done

- [ ] A clear compliance report is presented to the user listing passed checks, missing files, and architectural violations.
- [ ] All monolithic inline schemas or missing policies are flagged with actionable file-level remediation steps.
- [ ] Test suite (`vendor/bin/pest`) and code formatter (`vendor/bin/pint --test`) status are reported.

## Common Failure Modes and Fixes

- **Failure Mode**: Resource class contains inline `$schema->components([...])` or `$table->columns([...])` instead of modular classes.
  - **Fix**: Refactor inline definitions into `Schemas/{Name}Form.php` and `Tables/{Name}sTable.php` and call `{Name}Form::configure($schema)` / `{Name}sTable::configure($table)` from the Resource.
- **Failure Mode**: Missing authorization policy allows unauthorized panel access.
  - **Fix**: Generate `app/Policies/{Name}Policy.php` and ensure tenant and role checks are enforced across all CRUD actions.
