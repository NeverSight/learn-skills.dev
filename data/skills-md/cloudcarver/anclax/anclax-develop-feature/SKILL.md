---
name: anclax-develop-feature
description: Develop, review, or refactor Go services built with Anclax, including OpenAPI specs, handlers, service/business logic, database/sqlc changes, async tasks, and Wire dependency injection.
---

# Anclax Development Workflow

Use Anclax generated types as the contract between layers and keep specs/SQL as the source of truth.

## Design principles

- Singleton services with dependency injection.
- High cohesion, low coupling.

## Core flow

1. Inspect `anclax.yaml` to learn generation paths and enabled generators.
2. Update sources first:
   - OpenAPI: `api/v1.yaml`
   - Tasks: `api/tasks.yaml`
   - DB schema: `sql/migrations`
   - Queries: `sql/queries`
3. Run `anclax gen` after any spec/SQL/Wire changes.
4. Implement code against generated interfaces and types.
5. Add unit tests for service logic with mocks.

## Layering rules

- Handler: parse HTTP, call service, map errors to HTTP responses.
- Service: implement business logic, accept and return `apigen` types.
- Model: use `pkg/zcore/model` and sqlc-generated queries.
- Async tasks: define in `api/tasks.yaml`, implement `taskgen.ExecutorInterface`, enqueue via `taskgen.TaskRunner`.

## References and Examples
  - [Config](./anclax-config.md): How to use `anclax.yaml` for generator inputs/outputs.
  - [CRUD operations](./crud.md): End-to-end CRUD flow and mapping examples.
  - [OpenAPI Spec](./openapi-spec.md): Conventions for OpenAPI specs in Anclax.
  - [Business Logic](./business-logic.md): Service-layer rules and error handling.
  - [Database](./database.md): SQL/schema rules and transaction helpers.
  - [Dependency Injection](./dependency-injestion.md): Wire DI conventions.
  - [Async Tasks](./async-tasks.md): Task definitions, execution, retries, and hooks.
