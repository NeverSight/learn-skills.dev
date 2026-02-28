---
name: ysl-api
description: "Laravel 12 + PHP 8.3 API patterns: JWT auth, repository pattern, versioned controllers, Form Requests, API Resources, jobs, services, observers."
color: "#129748"
---

# Laravel API Skill

You are working on the **E-commerce API** — a Laravel 12 + PHP 8.3 backend for a multi-app logistics/e-commerce platform.

## Required Companion Skills

- `ysl-i18n` — Three-language internationalization (en, km, zh)

## Rules

- Follow @references/rules.md (MUST)

## Coding Standards (MUST)

- Follow @references/coding-standards.md

## Tech Stack

- Laravel 12, PHP 8.3
- JWT Authentication (tymon/jwt-auth)
- Repository Pattern (prettus/l5-repository)
- Hashids for ID obfuscation
- Intervention Image for media processing

## Architecture Overview

See @references/architecture.md for the full directory map.

## Workflow

When building a new feature:

1. Define constants if needed → `app/Constants/Const{Name}.php`
2. Create/update model → `app/Models/{Name}.php`
3. Create repository pair → Interface + Eloquent implementation
4. Create Form Request → `app/Http/Requests/{Feature}/{Action}Request.php`
5. Create API Resource → `app/Http/Resources/{Feature}/{Name}Resource.php`
6. Create controller → `app/Http/Controllers/V1_0/{Name}Controller.php`
7. Add routes → `routes/api/v1_0/{feature}.php`
8. Create migration → Only `up()` method, no `down()`

## References

- @references/architecture.md — Directory structure and key folders
- @references/rules.md — Non-negotiable rules (TODO list, no tests, summaries)
- @references/coding-standards.md — PHP 8.3+ and Laravel best practices (MUST follow)
- @references/authentication.md — JWT auth, device tokens, middleware chain
- @references/controllers.md — CRUD conventions, versioned routing
- @references/repositories.md — Repository pattern with prettus/l5-repository
- @references/validation.md — Form requests, custom rules, error format
- @references/resources.md — API resource transformations
- @references/constants.md — Constants pattern, role enums
- @references/services.md — Business logic services
- @references/jobs.md — Queue jobs (115 jobs)
- @references/observers.md — Model event observers (15 observers)
- @ysl-i18n — Three-language internationalization (REQUIRED)
