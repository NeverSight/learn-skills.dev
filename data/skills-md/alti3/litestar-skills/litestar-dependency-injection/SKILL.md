---
name: litestar-dependency-injection
description: Apply Litestar dependency injection with Provide, Dependency markers, layered scopes, overrides, generator-based cleanup, per-request caching, and nested providers. Use when wiring services, settings, database sessions, request-derived resources, or test doubles into Litestar handlers, controllers, routers, and apps. Do not use when plain local function parameters or a small helper are sufficient.
---

# Dependency Injection

## Execution Workflow

1. Choose the contract to inject first: settings object, service, repository, session, current user, or request-derived value.
2. Pick the narrowest scope that should own it: app, router, controller, or handler.
3. Implement the provider as a callable wrapped in `Provide`, choosing async, sync, or generator form based on lifecycle needs.
4. Keep the dependency key identical to the injected parameter name.
5. Use overrides intentionally at lower scopes and in tests.
6. Mark special cases with `Dependency(...)` when validation, defaults, or OpenAPI behavior need to be explicit.
7. Verify cleanup behavior for generator dependencies and startup-time failure for missing explicit dependencies.

## Core Rules

- Register dependencies at the narrowest scope that matches their reuse boundary.
- Keep dependency keys stable and descriptive: `settings`, `db_session`, `current_user`, `tenant`, `clock`.
- Keep injected annotations runtime-importable. Avoid hiding injected types behind `TYPE_CHECKING` unless you also provide a working runtime signature namespace.
- Accept keyword arguments and `self` in providers, never positional-only runtime arguments.
- Match the provider key and the consumer parameter name exactly.
- Prefer injecting services and repositories instead of raw transport objects unless the dependency is explicitly request-derived.
- Avoid hidden mutable singletons. If state must be shared, make lifecycle and mutability obvious.

## Scope Selection

Litestar resolves dependencies from outer to inner scope, with lower scopes overriding higher ones when the same key is reused.

- App scope: global settings, shared clients, top-level service factories.
- Router scope: feature-area dependencies shared across related routes.
- Controller scope: controller-local services or authorization context.
- Handler scope: per-endpoint customization and local overrides.

Choose the lowest scope that still matches the reuse boundary. Reusing the same key is an intentional override contract, not a naming accident.

## Provider Selection

- Use async providers for I/O-bound work that is naturally asynchronous.
- Use sync providers only when the work is truly synchronous.
- Set `sync_to_thread=True` for blocking I/O or CPU-heavy sync providers.
- Set `sync_to_thread=False` for cheap, non-blocking sync providers to document intent and avoid warnings.
- Use generator providers when setup and cleanup belong to the same logical resource.
- Use callable instances when constructor-time configuration is required but invocation should still be DI-managed.

## Reference Files

Read only the sections you need:

- For scope examples, provider forms, request-derived values, `yield` cleanup, overrides, caching, nested dependency graphs, and service wiring patterns, read [references/provider-patterns.md](references/provider-patterns.md).
- For `Annotated[..., Dependency(...)]` usage, validation control, OpenAPI-safe defaults, and fail-fast explicit dependency markers, read [references/dependency-markers.md](references/dependency-markers.md).

## Recommended Defaults

- Keep validation enabled unless the provider is trusted and the performance or type-system tradeoff is justified.
- Keep dependency graphs shallow enough to reason about quickly.
- Compose stable layers: settings -> client/session -> repository -> service.
- Use request-derived providers as translation boundaries from transport inputs to domain types.
- Reuse the same dependency keys in tests to swap in fakes without touching handler code.

## Anti-Patterns

- Registering everything at app scope because it is convenient.
- Using dependencies as an opaque service locator with unclear names like `dep1`.
- Returning mutable global singletons from providers and mutating them per request.
- Performing blocking I/O in sync providers without `sync_to_thread=True`.
- Using `skip_validation=True` broadly instead of fixing the type boundary.
- Repeating lookup logic in handlers when a request-derived provider should own it.

## Validation Checklist

- Confirm every injected parameter name matches a registered dependency key.
- Confirm the chosen scope matches reuse and override needs.
- Confirm sync providers declare the right `sync_to_thread` behavior.
- Confirm generator dependencies always close, even on exceptions.
- Confirm nested provider graphs stay readable and testable.
- Confirm `Dependency(default=...)` is used when fallback dependencies must stay out of OpenAPI.
- Confirm explicit `Dependency()` markers catch missing required wiring at startup.
- Confirm tests can override keys cleanly without monkeypatching internals.

## Cross-Skill Handoffs

- Use `litestar-databases` for SQLAlchemy or Piccolo session provisioning.
- Use `litestar-testing` for dependency override patterns and client-based verification.
- Use `litestar-security` or `litestar-authentication` when DI is carrying auth context.
- Use `litestar-routing` when the main issue is route/controller structure rather than service wiring.

## Litestar References

- https://docs.litestar.dev/latest/usage/dependency-injection.html
- https://docs.litestar.dev/latest/usage/applications.html
- https://docs.litestar.dev/latest/usage/testing.html
