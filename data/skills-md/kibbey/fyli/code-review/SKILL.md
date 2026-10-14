---
name: code-review
description: Review code for quality, standards compliance, and best practices. Use when asked to review code, check for issues, audit code quality, or validate implementations against project standards.
allowed-tools: Read, Grep, Glob, Bash
---

# Code Review Skill

Perform a comprehensive code review for the personal_assistant project, checking against established standards and best practices.

## Review Checklist

## Backwards Compatability
All backend changes must be 100% backwards compatible for drops (memories) and access to drops (which users have access to drops they or others created). Breaking changes should be flagged regardless of what they break (i.e. any breaking change, not just drops and access).

### Architecture Compliance

**Backend (C#/.NET):**
- [ ] 3-tier architecture respected (Controllers → Services → Repositories)
- [ ] Controllers only handle HTTP request/response and basic validation
- [ ] Services contain business logic and business validation
- [ ] Repositories handle all database operations
- [ ] Domain models used between layers (not raw DB entities in controllers)
- [ ] Request/Response DTOs defined for controllers
- [ ] Dependency injection used for all service/repository wiring
- [ ] Global error handling used (throw immediately, catch globally via middleware)
- [ ] Jsonb column was not used.  Only use Jsonb if other alternatives are not available.
- [ ] Database changes use EF Core Code-First pattern: POCO entity in `Entities/`, FK config in `StreamContext.OnModelCreating`, `DbSet<T>` property added, migration generated via `dotnet ef migrations add`. No raw SQL for schema changes.
- [ ] Each EF Core migration has a corresponding `.sql` script in `docs/migrations/`, generated via `dotnet ef migrations script <PreviousMigration> <NewMigration> --project Domain --startup-project Memento --idempotent`. This script is used for production deployments.
- [ ] Raw SQL scripts use **SQL Server syntax** (not PostgreSQL): `INT IDENTITY(1,1)` not `SERIAL`, `DATETIME2` not `TIMESTAMPTZ`, `BIT` not `BOOLEAN`, `UNIQUEIDENTIFIER` not `UUID`, `NVARCHAR` for Unicode, square brackets `[TableName]` not double quotes

**Frontend (Vue.js):**
- [ ] Composition API with `<script setup>` syntax used
- [ ] Components are single-responsibility
- [ ] Props for parent-to-child, Emits for child-to-parent
- [ ] Pinia stores for app-wide state, composables for simple sharing
- [ ] Business logic in stores, components focused on presentation
- [ ] Template order: `<template>`, `<script setup>`, `<style scoped>`

### Code Quality

- [ ] Methods under 100 lines
- [ ] SOLID principles followed
- [ ] Factory patterns used instead of if/else chains or switch statements where appropriate
- [ ] DRY - no unnecessary code duplication
- [ ] Composability favored for reusable logic
- [ ] C# types properly defined (no `dynamic` or `object` without justification)
- [ ] Functions have brief summary comments

### Type Standards

**Frontend:**
- [ ] Props typed with `defineProps<PropsType>()`
- [ ] Emits typed with `defineEmits<EmitsType>()`
- [ ] Explicit types for refs
- [ ] Interfaces for API responses and store state
- [ ] Does the project build (npm run build) with no errors?
- [ ] !IMPORTANT! **Strict indexed access safety:** Array element access (e.g. `arr[i]`, `str.split("x")[0]`) returns `T | undefined` under `noUncheckedIndexedAccess`. All such accesses must use a non-null assertion (`!`), nullish coalescing (`??`), or a guard check before use. Run `npx vue-tsc --noEmit` to catch these — do NOT rely on `vite build` alone, as Vite skips type checking.
- [ ] !IMPORTANT! **Test fixture type completeness:** When new required properties are added to shared types (e.g. `Drop`, `User`), verify that test fixture factories in `src/test/fixtures.ts` include defaults for the new fields. `Partial<T>` spreads can leave required properties as `undefined`, causing `vue-tsc` failures. Always run `npx vue-tsc --noEmit` after adding properties to shared types.

**Backend (C#):**
- [ ] Request/Response DTOs defined
- [ ] Domain model classes with proper encapsulation
- [ ] Repository interfaces with explicit return types
- [ ] Async methods return `Task<T>` and follow `Async` naming suffix

### Testing

**Backend:**
- [ ] Tests written for new functionality (TDD approach)
- [ ] Business layer has unit tests
- [ ] Repository layer has unit tests
- [ ] Utilities have unit tests
- [ ] Minimum 70% coverage target

**Frontend (Vitest + Vue Test Utils):**
- [ ] New Vue components have corresponding `.test.ts` files
- [ ] Component tests cover rendering, props, emits, and user interactions
- [ ] Pinia stores have tests for actions, getters, and state mutations
- [ ] API service files have tests with Axios mocked
- [ ] Both success and error paths are tested
- [ ] All frontend tests pass (`cd fyli-fe-v2 && npm run test:unit -- --run`)

> **Full testing standards:** See `docs/TESTING_BEST_PRACTICES.md` for detailed patterns and examples.

### Security

- [ ] No hardcoded secrets or credentials
- [ ] Input validation at system boundaries
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] Authentication/authorization properly checked

### Performance (Frontend)

- [ ] `v-show` for frequent toggles, `v-if` for rare changes
- [ ] Routes lazy loaded
- [ ] Unique IDs (not indexes) as v-for keys
- [ ] `shallowRef` for large objects
- [ ] Virtual scroll for long lists

### Documentation

- [ ] AI prompts documented in `/docs/AI_PROMPTS.md` if modified
- [ ] Database migrations documented in `cimplur-core/docs/DATA_SCHEMA.md`
- [ ] Release notes updated in `/docs/release_note.md` for new features

### Style Compliance

- [ ] No "powered by AI" or "AI suggested" terminology
- [ ] Tabs for indentation
- [ ] Double quotes
- [ ] Semicolons used
- [ ] Line length under 100 characters
- [ ] **Backend (C#):** PascalCase for methods, properties, and public members; camelCase for local variables, parameters, and private fields; PascalCase for classes and interfaces (prefix interfaces with `I`)
- [ ] **Frontend:** camelCase for variables/functions; PascalCase for components
- [ ] UPPER_CASE for constants

### Look and Feel
- [ ] Have the designer skill review the work and verify compliance with design standards
- [ ] Add designer feedback on changes that need to be made

## Review Output Format

Provide findings organized by severity:

### Critical Issues
Issues that must be fixed (security vulnerabilities, breaking bugs, architecture violations)

### Improvements
Recommended changes for better code quality

### Suggestions
Optional enhancements and best practice recommendations

### Positive Notes
Well-implemented patterns worth highlighting

## Archiving

When a TDD is fully complete (all phases built and code review passed), move the TDD from `docs/tdd/` to `docs/tdd/archive/`.
