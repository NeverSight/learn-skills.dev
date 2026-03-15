---
name: laravel-best-practices
description: "Laravel framework skill for writing, reviewing, and testing PHP applications built with Laravel. Use whenever working on Laravel-specific patterns: controllers, FormRequests, Eloquent models, service/action classes, Blade templates, jobs, events, policies, observers, or Artisan commands. Also applies to Inertia frontends (React or Vue) embedded inside a Laravel project — covering useForm, usePage, Link navigation, partial reloads, page component naming (PostsIndexPage), and shadcn wrapper conventions. Trigger any time someone mentions Laravel, Eloquent, Artisan, Blade, FormRequest, Inertia within Laravel, N+1 queries in a Laravel app, inline controller validation, where business logic should live in a Laravel controller, or asks to follow best practices in a Laravel codebase. Does not apply to plain PHP scripts without Laravel, Rails, Django, standalone Next.js, or non-Laravel frameworks."
metadata:
  installed_path: .codex/skills/laravel-best-practices
  outputs:
    - review (findings + patch outline)
    - generate (file plan + code)
    - tests (test matrix + starter tests)
---

## Purpose
This skill guides an AI coding agent to:
1) generate Laravel code aligned with established best practices,
2) review Laravel code (or diffs) and propose refactors aligned to those practices,
3) propose and scaffold tests (Pest preferred; PHPUnit supported).

## Use when
- Implementing or refactoring controllers, FormRequests, service/action classes, jobs, events/listeners, policies, observers
- Reviewing PRs, diffs, or entire files in a Laravel application
- Designing maintainable application layering and test strategy
- Working on Inertia + React or Inertia + Vue frontends within a Laravel project

## Rulebook
Use **references/rulebook.json** as the source of truth for:
- rule ids
- detection signals
- recommended refactor patterns
- expected outputs

When you flag an issue, always include:
- rule_id
- evidence (file + line numbers or excerpt)
- minimal refactor steps first
- test impact plan

## Core principles (high-level)
- **Single Responsibility**: one reason to change per class; one main concern per method.
- **Thin controllers**: controllers orchestrate; business logic lives elsewhere.
- **Validation in FormRequests**: move validation and authorization there.
- **Business logic in services/actions**: extract workflows into testable units.
- **DRY**: centralize repeated logic (Eloquent scopes, value objects/DTOs, helpers).
- **Prefer Eloquent + Collections**: use expressive domain modeling where practical.
- **No queries in Blade**: views must not query the database; eager load to avoid N+1.
- **Chunk/stream large datasets**: avoid loading large tables into memory.
- **Policies for authorization**: use Policy classes per model; keep `authorize()` calls in the HTTP layer, never inside services.
- **No `env()` outside config files**: access environment values via `config()` throughout the app; `env()` only in `config/*.php`.
- **Follow naming conventions**: singular PascalCase models and controllers, camelCase methods, snake_case config/migration keys, kebab-case route slugs.

## Frontend / Inertia principles

### Inertia + React
When reviewing or generating Inertia React code, apply rules `INRT-001`–`INRT-010` from the rulebook.
See **references/inertia-react-summary.md** for a quick-reference cheat sheet, or **references/inertia-react.md** for the full annotated directory structure and examples.

- **Directory structure**: `common` (shared primitives), `modules` (feature code), `pages` (Inertia-rendered), `shadcn` (generated components).
- **Page components**: suffix with `Page`, use a default export (e.g. `PostsIndexPage.tsx`).
- **Component files**: one component per `.tsx` file, PascalCase filenames, function declarations.
- **Type page props**: define a TypeScript interface per page; use `usePage<SharedProps>()` for globally shared data.
- **Form submissions**: use `useForm` from `@inertiajs/react`; avoid raw `fetch`/`axios` for Inertia-driven forms.
- **Shared data**: access via `usePage()` rather than prop-drilling auth/flash data through every component layer.
- **Internal navigation**: use `<Link>` from `@inertiajs/react`; reserve plain `<a>` tags for external URLs.
- **Partial reloads**: use `router.reload({ only: [...] })` to refresh a subset of props instead of a full page visit.

### Inertia + Vue
When reviewing or generating Inertia Vue code, apply rules `INRT-VUE-001`–`INRT-VUE-005` from the rulebook.
See **references/inertia-vue.md** for the annotated directory structure and conventions.

- **Directory structure**: `common` (shared UI primitives), `modules` (feature code), `pages` (Inertia-rendered), `lib` (third-party/generated).
- **Page components**: suffix with `Page`, use `<script setup>` or `export default` (e.g. `PostsIndexPage.vue`).
- **Component files**: one component per `.vue` file, PascalCase filenames, prefer `<script setup>` + Composition API.
- **Third-party UI**: keep in `resources/js/lib`; wrap in `common` for a project-friendly API — don't modify sources directly.

## Workflow: Review
When asked to review code:
1) Identify the layer (Controller, Request, Model, Service/Action, Blade, etc.).
2) Apply rules from rulebook.json; emit findings with rule ids.
3) Provide a patch outline (what files to create/change) and a test plan.

### Recommended output (JSON)
Return a JSON object:
- summary: score, counts
- findings[]: rule_id, severity, evidence, rationale, recommendations, patch outline
- tests: a short matrix or list of impacted tests

## Workflow: Generate code
When asked to implement a feature:
1) Propose file layout first (Controller + FormRequest + Service/Action + Model scopes, etc.).
2) Generate code using Laravel idioms: dependency injection, FormRequests, policies, resources.
3) Include a minimal test plan (Feature + Unit tests).

## Workflow: Generate tests
Prefer Pest if repository uses Pest (presence of pestphp/pest in composer.json); otherwise PHPUnit.
- FormRequest validation/authorization
- Service/action business rules (unit)
- Feature tests for endpoints (happy path + validation + authz)
- Mock external systems (HTTP, queues, notifications) as needed
