---
name: php-best-practices
description: Use this skill when the user asks to create, review, refactor, or migrate PHP backend components (controllers, services, DTOs, repositories, responses, tests) following TreeNation's Domain-Driven Design architecture.
---

# PHP Best Practices

Use this skill as a rulebook for building and migrating PHP backend components following TreeNation's DDD architecture.

## Workflow

1. Open `AGENTS.md`.
2. Identify which components need to be created or changed (controller, service, DTO, repository, response, test).
3. Load only the relevant rule files from `rules/`.
4. Implement the smallest correct change that satisfies the requirement.
5. Run PHP CS Fixer and PHPStan before finishing.

## Repository Guardrails

- New PHP files go inside `src/` except controllers (which stay in `app/Http/Controllers/`).
- Controllers must not contain business logic; delegate to a service.
- Services must be unit-tested; mock all dependencies.
- Always register new repository interfaces in `app/Providers/TreeNationProvider.php`.
- Use strict typing (`declare(strict_types=1)`) in all new files.
- Do not add comments unless the user explicitly asks.
- Follow the Criteria pattern for all repository queries.
- Access model data via getter methods, not direct property access (see `rules/model-getters.md`).
- Commits follow pattern: `TNIT-####: description`.

## Output Expectations

- Explain which rules were applied and why.
- Generate all required files for the feature (controller, request, DTO if needed, service, response, repository interface, repository implementation, test).
- Keep changes incremental; avoid broad rewrites unless asked.
