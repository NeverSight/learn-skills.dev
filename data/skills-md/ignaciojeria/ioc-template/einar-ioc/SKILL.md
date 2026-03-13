---
name: einar-ioc
description: Best practices for building Go applications using Hexagonal Architecture and Einar-IoC
metadata:
  tags: go, golang, hexagonal-architecture, dependency-injection, ioc, fuego, einar-cli, vibe-coding
---

## Purpose

This skill is **100% oriented to vibe-coding**: the agent scaffolds, wires, and modifies code by following these rules. **Einar CLI is never used**—the agent replicates its behavior manually. The Einar CLI equivalents and `.einar.template.json` are described **only as reference** so the agent understands how Einar CLI works and can produce equivalent output.

## When to use

Use this skill whenever you are writing or modifying Go code that uses the `github.com/Ignaciojeria/ioc` library, or when you are creating APIs, event-driven components, or database adapters in a Hexagonal Architecture. When adding new components (controllers, repositories, consumers, etc.), apply the patterns from the rules—including adding blank imports to `cmd/api/main.go`—as if Einar CLI had scaffolded them.

> [!TIP]
> **Living Documentation**: The rules in `./rules/` are generated from the actual `.go` files. Read the source code in `app/adapter` and `app/shared` as your primary reference—the rules reflect the template as it exists.

## Quick reference

| Domain           | Rule files |
|------------------|------------|
| Architecture     | [architecture-guidelines](rules/architecture-guidelines.md), [domain](rules/domain.md) – domain by intention (entity, repository, client, service) |
| Einar CLI config | [einar-template](rules/einar-template.md) – template config for generators |
| Structure & main | [structure](rules/structure.md), [main](rules/main.md), [archetype-version](rules/archetype-version.md) |
| Configuration    | [configuration](rules/configuration.md) |
| HTTP / REST      | [httpserver](rules/httpserver.md), [request-logger-middleware](rules/request-logger-middleware.md), [fuegoapi-controllers](rules/fuegoapi-controllers.md) |
| EventBus         | [eventbus-strategy](rules/eventbus-strategy.md), [eventbus-gcp](rules/eventbus-gcp.md), [eventbus-nats](rules/eventbus-nats.md), [consumer](rules/consumer.md), [publisher](rules/publisher.md) |
| Use cases        | [usecase](rules/usecase.md), [ports](rules/ports.md), [architecture-guidelines](rules/architecture-guidelines.md) |
| Database         | [postgresql-connection](rules/postgresql-connection.md), [postgresql-migrations](rules/postgresql-migrations.md), [postgres-repository](rules/postgres-repository.md) |
| Observability    | [observability](rules/observability.md) |

## Dependency Injection (IoC)

All components MUST be registered in the IoC container via `var _ = ioc.Register(Constructor)`. See any rule file (e.g. [httpserver](rules/httpserver.md), [fuegoapi-controllers](rules/fuegoapi-controllers.md)) for the exact pattern.

**Blank imports are critical:** Each package that registers constructors MUST be imported in `cmd/api/main.go` via a blank import (`_ "archetype/path/to/package"`). Without it, the package never loads and the IoC container will not receive those constructors. **When adding a new component, the agent must add the corresponding blank import**—the user does not do this manually.

## Einar CLI equivalents (reference only—do not run the CLI)

The following section explains **how Einar CLI works** so the agent can replicate it. **Never execute Einar CLI commands.** When the user asks for something Einar CLI would do, scaffold the equivalent manually: use the rules as templates, apply the replacements, create modular files, and add the blank import to `cmd/api/main.go`.

**New components not in the template:** The user can request components not covered by the template (e.g. a new adapter type, a custom handler). The agent may create them freely but **must follow the same structure and practices** as the generator: one file per component, `ioc.Register`, constructor injection, blank import in `main.go`, and consistent naming (PascalCase for types, snake_case for files). For functions that are **not candidates to be registered as singletons** (helpers, pure functions, utilities), create them as you see fit—adjusted to the structure and following best practices.

### How Einar CLI works (template + replace)

Einar CLI **generates and renames** `.go` files guided by [.einar.template.json](rules/einar-template.md). That file defines, per generator: `source_file` (template), `destination_dir`, `replace_holders` (PascalCase/SnakeCase), and `ioc_discovery` (add blank import). The agent must:
1. Take the template from the corresponding rule (e.g. [fuegoapi-controllers](rules/fuegoapi-controllers.md) for get.go).
2. Create a **new modular file** (one file per operation/entity).
3. Apply PascalCase/SnakeCase replacements: `Template` → `{OperationName}`.
4. Add the blank import to `cmd/api/main.go` (the agent does this; the user does nothing).

### Replace holders by component (see [einar-template](rules/einar-template.md) for full config)

| Component | Template placeholder | Replace with (PascalCase `X` = operation name) |
|-----------|---------------------|------------------------------------------------|
| **get-controller** | `NewTemplateGet` | `New{X}` (e.g. `NewGetUser`) |
| **post/put/patch-controller** | `NewTemplatePost`, `TemplatePostRequest`, `TemplatePostResponse` | `New{X}`, `{X}Request`, `{X}Response` |
| **delete-controller** | `NewTemplateDelete` | `New{X}` |
| **postgres-repository** | `NewTemplateRepository`, `TemplateRepository`, `TemplateStruct` | `New{X}Repository`, `{X}Repository`, `{X}` (and `template_table` → `{x}_table`) |
| **pubsub-consumer** | `NewTemplateConsumer`, `TemplateConsumer`, `TemplateMessage`, `template_topic_or_hook` | `New{X}Consumer`, `{X}Consumer`, `{X}Message`, `{x}_topic` (SnakeCase) |
| **publisher** | `NewTemplatePublisher`, `TemplatePublisher` | `New{X}Publisher`, `{X}Publisher` |

### Commands reference

| User intent / Einar CLI command | Template rule | Output (modular files) | Blank import |
|---------------------------------|---------------|------------------------|--------------|
| `einar install fuego` | [httpserver](rules/httpserver.md), [request-logger-middleware](rules/request-logger-middleware.md) | server.go, request_logger.go | `_ "archetype/app/shared/infrastructure/httpserver"`, middleware |
| `einar install postgresql` | [postgresql-connection](rules/postgresql-connection.md), [postgresql-migrations](rules/postgresql-migrations.md) | connection.go, migrations/*.sql | `_ "archetype/app/shared/infrastructure/postgresql"` |
| `einar install gcp-pubsub` | [eventbus-strategy](rules/eventbus-strategy.md), [eventbus-gcp](rules/eventbus-gcp.md) | gcp_*.go | `_ "archetype/app/shared/infrastructure/eventbus"` |
| `einar generate get-controller X` | [fuegoapi-controllers](rules/fuegoapi-controllers.md) (get.go) | `get_{x}.go` in fuegoapi/ | `_ "archetype/app/adapter/in/fuegoapi"` |
| `einar generate post-controller X` | post.go | `post_{x}.go` | same |
| `einar generate postgres-repository X` | [postgres-repository](rules/postgres-repository.md) | `{x}_repository.go` in postgres/ | `_ "archetype/app/adapter/out/postgres"` |
| `einar generate pubsub-consumer X` | [consumer](rules/consumer.md) | `{x}_consumer.go` in eventbus/ | `_ "archetype/app/adapter/in/eventbus"` |
| `einar generate publisher X` | [publisher](rules/publisher.md) | `{x}_publisher.go` in eventbus/ | `_ "archetype/app/adapter/out/eventbus"` |

## Constraints (from README)

1. **No `init()`** for business components. Use `ioc.Register` at package level instead.
2. **No `os.Getenv` in logic.** Inject `configuration.Conf` as a dependency.
3. **No ORMs with auto-migrations.** Schema changes go in `.sql` files under `app/shared/infrastructure/postgresql/migrations/`. Use `sqlx` + `golang-migrate`.
4. **Don't extract variables for testability.** Avoid `var jsonMarshal = json.Marshal` or injectable stubs just to reach 100% coverage. Prefer constructor injection; accept slightly lower coverage for unreachable error paths.

## Architecture (see [architecture-guidelines](rules/architecture-guidelines.md))

5. **No `app/domain/port/` folder.** Define interfaces at the same level as the implementation—in the consumer package (usecase) or next to the adapter.
6. **Always inject and return interfaces** in IoC constructors. Each interface must have **exactly one implementation** registered; otherwise the IoC cannot resolve unambiguously.

### Example: injecting a use case into a controller

The controller injects the **input port** (`in.GetTemplateExecutor`). The IoC resolves it from `NewGetTemplateUseCase`:

```go
// Controller: inject ports/in executor
func NewGetTemplate(s *httpserver.Server, uc in.GetTemplateExecutor) {
	fuegofw.Get(s.Manager, "/templates/{id}",
		func(c fuegofw.ContextNoBody) (GetTemplateResponse, error) {
			out, err := uc.Execute(c.Context(), c.PathParam("id"))
			if err != nil {
				// handle error...
			}
			return GetTemplateResponse{ID: out.ID, Name: out.Name}, nil
		},
	)
}
```

The use case constructor returns `(in.GetTemplateExecutor, error)`; the IoC stores that value and injects it into the controller.

## Use case output: DTOs over domain entities

**Prefer use case-specific DTOs** (`XxxInput`, `XxxOutput`) over returning domain entities. Reasons:
- **Decoupling:** The API contract stays independent of the domain model.
- **Explicit contracts:** Each use case exposes only the fields it needs.
- **Agent-friendly:** DTOs allow self-contained use case files with predictable patterns; agents can generate complete use cases without cross-package lookups.

## Rules by domain

### Architecture

- [architecture-guidelines](rules/architecture-guidelines.md) – No ports folder, interfaces co-located, inject interfaces (one implementation per interface)

### Einar CLI / generators

- [einar-template](rules/einar-template.md) – `.einar.template.json`: how Einar CLI generates and renames files

### Structure and entry point

- [structure](rules/structure.md) – Project directory tree (`app/adapter`, `app/shared`, `cmd`, `scripts`)
- [main](rules/main.md) – Entry point and `ioc.LoadDependencies()`
- [archetype-version](rules/archetype-version.md) – Embedded `Version` from `.version` file

### Configuration

- [configuration](rules/configuration.md) – Environment config with caarlos0/env and godotenv

### HTTP / REST (Fuego)

Use `github.com/go-fuego/fuego` for REST. Do not use `net/http`, `gin`, or `fiber` directly.

- [httpserver](rules/httpserver.md) – Fuego server, healthcheck, graceful shutdown
- [request-logger-middleware](rules/request-logger-middleware.md) – HTTP request logging
- [fuegoapi-controllers](rules/fuegoapi-controllers.md) – REST controller scaffold (GET, POST, PUT, PATCH, DELETE)

### EventBus (CloudEvents, GCP / NATS)

- [eventbus-strategy](rules/eventbus-strategy.md) – Interfaces, factory, and strategy pattern
- [eventbus-gcp](rules/eventbus-gcp.md) – GCP Pub/Sub client, publisher, subscriber
- [eventbus-nats](rules/eventbus-nats.md) – NATS client, publisher, subscriber
- [consumer](rules/consumer.md) – Inbound consumer pattern
- [publisher](rules/publisher.md) – Outbound publisher adapter

### Database (PostgreSQL)

- [postgresql-connection](rules/postgresql-connection.md) – SQLx + golang-migrate, connection lifecycle
- [postgresql-migrations](rules/postgresql-migrations.md) – Example migrations: naming (`NNNNNN_name.up/down.sql`), up/down pattern
- [postgres-repository](rules/postgres-repository.md) – Repository pattern with sqlx and go-sqlmock

### Observability

- [observability](rules/observability.md) – OpenTelemetry, slog injection, context propagation
