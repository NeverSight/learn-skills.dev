---
name: clean-ddd-backend
description: Use when starting, structuring, or adding features to a back-end service (TypeScript/Node or similar) that should follow Clean Architecture, Hexagonal Architecture (ports and adapters), DDD and SOLID — creating entities, aggregates, value objects, use cases, repositories, domain events, routes/controllers, presenters, mappers, factories, or unit/e2e tests in such a codebase, with any framework (NestJS, Fastify, Express) or ORM (Prisma, Drizzle, TypeORM).
---

# Clean DDD Back-end

## Overview

A framework-agnostic blueprint for back-end services, distilled from a reference NestJS + Prisma project. **The domain is the center. Everything else is a replaceable adapter.** Dependencies point inward only: `infra → domain (application → enterprise) → core`.

The examples use NestJS, Prisma, Zod and Vitest. Every rule applies unchanged to Fastify, Express, Drizzle, TypeORM, TypeBox, Jest and similar tools. Only the adapter code changes.

If the project already has conventions that conflict with this skill, follow the project and point out the divergence. Otherwise, follow this skill exactly: the names, folders and test titles below are the convention, not suggestions.

## Layers

| Layer | Path | Contains | May import |
|---|---|---|---|
| Shared kernel | `src/core/` | `Either`, `Entity`, `AggregateRoot`, `ValueObject`, `UniqueEntityId`, `WatchedList`, `DomainEvents`, generic errors (`core/errors/errors/`), shared types | nothing outside `core` |
| Enterprise | `src/domain/<context>/enterprise/` | `entities/`, `entities/value-objects/`, `events/` | `core`, same context |
| Application | `src/domain/<context>/application/` | `use-cases/`, `use-cases/errors/`, `repositories/`, other ports grouped by capability (`cryptography/`, `storage/`…), `subscribers/` | `core`, own `enterprise`; subscribers may also import other contexts' **events** and port types |
| Infra | `src/infra/` | HTTP, database, env, auth, cache, storage, cryptography, events wiring, entrypoint | everything |
| Test support | `test/` | in-memory repositories, fakes, factories, e2e setup, utils | everything |

**Framework in the domain layer:** keep `domain/` and `core/` free of framework, ORM, HTTP and validation libraries. One explicit exception is allowed: a DI decorator on use cases and subscribers (for example Nest's `@Injectable()`). This trades purity for less wiring, and switching frameworks would mean revisiting those files anyway. If the project avoids that trade-off, wire use cases in infra instead (factory providers or a composition root).

## Directory layout

Every bounded context is mirrored in `domain/`, `infra/` and `test/`, **even when there is only one context**. Adapters live in per-context folders, never in a flat `controllers/`, `routes/`, `mappers/` or `repositories/` folder shared by all contexts.

```
src/
├── core/                                  # shared kernel
├── domain/<context>/
│   ├── enterprise/{entities,entities/value-objects,events}/
│   └── application/{use-cases,use-cases/errors,repositories,subscribers,<port-group>}/
└── infra/
    ├── main.ts (entrypoint), app module / composition root
    ├── env/  auth/  events/  cryptography/  storage/  cache/
    ├── database/
    │   ├── database module (binds every port to its adapter)
    │   └── <orm>/
    │       ├── client/service, migrations, cross-context adapters (unit of work, transaction context)
    │       └── <context>/{mappers,repositories,schemas}/
    └── http/
        ├── http module / server       # only registers one module/plugin per context
        ├── shared/                    # validation pipe, error handler, auth hooks
        └── <context>/
            ├── <context>-http module/plugin   # routes + use case providers of the context
            ├── presenters/
            └── <resource>/            # <action>.controller.ts + <action>.controller.e2e-spec.ts
test/
├── setup-e2e.ts
├── utils/                             # waitFor, …
└── <context>/{factories,repositories,<port-group>}/   # make-x.ts, in-memory-xs-repository.ts, fake-x.ts
```

Example: `src/infra/database/prisma/lending/mappers/prisma-loan-mapper.ts`, `src/infra/http/lending/loans/borrow-book.controller.ts`, `test/lending/repositories/in-memory-loans-repository.ts`.

## Naming (exact)

| Artifact | File | Symbol |
|---|---|---|
| Use case | `use-cases/borrow-book.ts` | `export class BorrowBookUseCase` with one `execute()` |
| Use case input | same file | `export interface BorrowBookUseCaseRequest` (no input: `export type …Request = Record<string, never>`) |
| Use case output | same file | `export type BorrowBookUseCaseResponse = Either<ErrA \| ErrB, { loan: Loan }>` (no output: `null` on the right; no failure: `null` on the left) |
| Use case test | `use-cases/borrow-book.spec.ts` | `describe('Borrow Book Use Case')`, `it('should be able to …')`, `it('should not be able to …')`, instance named `sut` |
| Error | `use-cases/errors/loan-limit-reached-error.ts`, generic ones in `core/errors/errors/` | `class LoanLimitReachedError extends Error implements UseCaseError` |
| Port | `repositories/loans-repository.ts` | `export abstract class LoansRepository` (plural, abstract class even without a DI container) |
| Event | `enterprise/events/loan-created-event.ts` | `class LoanCreatedEvent implements DomainEvent` with `occurredAt` |
| Subscriber | `<consumer>/application/subscribers/on-loan-created.ts` | `class OnLoanCreated implements EventHandler` |
| Route handler | `infra/http/<context>/<resource>/borrow-book.controller.ts` | `BorrowBookController` with `handle` |
| E2E test | next to the handler: `borrow-book.controller.e2e-spec.ts` | `describe('Borrow Book (E2E)')` + exactly `test('[POST] /books/:bookId/loans')` |
| Presenter | `infra/http/<context>/presenters/loan-presenter.ts` | `LoanPresenter.toHTTP(loan)` |
| Mapper | `infra/database/<orm>/<context>/mappers/prisma-loan-mapper.ts` | `PrismaLoanMapper.toDomain(raw)` / `.toPrisma(loan)` |
| Adapter | `infra/database/<orm>/<context>/repositories/prisma-loans-repository.ts` | `PrismaLoansRepository extends/implements LoansRepository` |
| Factory | `test/<context>/factories/make-loan.ts` | `makeLoan(override?, id?)` + `LoanFactory.make<Orm>Loan()` (`makePrismaLoan`, `makeTypeOrmLoan`) |
| In-memory | `test/<context>/repositories/in-memory-loans-repository.ts` | `InMemoryLoansRepository` with `public items` |

The e2e title is the HTTP method in brackets plus the route path **with its parameter placeholders**, nothing else: no description suffix, no status code, and `test`, not `it`. One e2e test per route covers the success path. Failure branches are covered by the unit tests.

## Rules

1. **One use case per action, one spec per use case.**
2. **Use cases never throw for business failures.** They `return left(new SomeError())` or `return right({...})`. Only infrastructure failures may throw. Inputs are primitives (string ids). Outputs are wrapped in an object (`{ loan }`), so new fields don't break callers.
3. **Entities** extend `Entity`, or `AggregateRoot` when they raise events or own child collections. They have protected `props` and a protected constructor, and are created only via `static create(props: Optional<Props, 'defaulted'>, id?: UniqueEntityId)`. When `id` is absent the entity is new and may raise a creation event; when present it is rehydrated. Expose getters for everything. State changes go through setters for plain fields, or intention-revealing methods for transitions (`read()`, `cancel()`, `releaseSeats()`). When the entity has `updatedAt`, these call `touch()`.
   - Business rules that can fail are exposed as queries (`canBorrow(activeLoans)`, `allowsCancellationAt(now)`), which the use case checks before mutating so it can return `left`. Entity methods throw only for programmer errors (impossible states).
   - A rule spanning several aggregates lives in the use case. If it is reused, it goes in a pure domain service in `enterprise/services/`.
4. **Bounded contexts talk only through domain events.**
   - The aggregate calls `addDomainEvent` when something happens.
   - Repositories of `AggregateRoot`s call `DomainEvents.dispatchEventsForAggregate(id)` after the write succeeds, in both the real and the in-memory adapters. Repositories of plain `Entity`s don't dispatch.
   - The consuming context reacts in a subscriber, which calls its own use case. The subscriber's handler catches and logs failures, so an error never becomes an unhandled rejection.
   - Never call another context's use cases. Never mutate another context's aggregates.
5. **Typed env vars.** A schema validates `process.env` once at boot and the app fails fast. `type Env` is inferred from the schema, values are read through `env.get(key)` or a typed object, and `.env.example` lists every key. Application code never reads `process.env`. The only other files allowed to touch it are tool configs (ORM/migration CLI config) and test support files under `test/` (e2e setup, test app builder).
6. **Every input a route receives is validated by a schema** (Zod, TypeBox, …) declared in the handler file: one schema each for body, query and params when present. The handler input type is inferred from the schema. The authenticated user comes from the auth layer (typed payload), not from a schema. Schemas check shape and format. Business rules stay in the domain even when a schema already rejects the same input, because the use case must stay correct for every caller.
7. **Handlers are thin.** Validate → call exactly one use case → if the response's left side has error classes, map **each** to its HTTP status → return through a presenter. No business logic and no repository access in handlers.

   | Error | Status |
   |---|---|
   | `ResourceNotFoundError` | 404 |
   | `NotAllowedError` | 403 |
   | `InvalidCredentialsError` | 401 |
   | conflicts with current state (`…AlreadyExistsError`, `BookAlreadyOnLoanError`, `…AlreadyCancelledError`) | 409 |
   | other business-rule violations (`LoanLimitReachedError`, `CancellationWindowClosedError`) | 422 |
   | `default` branch of the `switch (error.constructor)` | 400 |
8. **Presenters for HTTP output, mappers for persistence.** Never return entities or ORM rows directly.
9. **Type everything.** Ports, `execute(): Promise<XUseCaseResponse>`, mappers and presenters get explicit types. Never use `any`; use `unknown` plus narrowing instead (`DomainEvents` callbacks included).
10. **Tests use in-memory repositories and fakes** (`FakeHasher`, `FakeClock`, `FakeUploader`) in place of ports. `vi.fn()`/`jest.fn()` never replace a port. `vi.spyOn` is used only to observe calls on a real object, for example a subscriber calling a use case. Entities in tests come from `makeX()` factories, and records in e2e tests come from `XFactory`.
11. **Consistency.** Uniqueness and race conditions are guaranteed by database constraints. The adapter translates a constraint violation into the domain error class, and the use case returns it as `left`. When one use case must write several aggregates atomically, add a `UnitOfWork` port (`run(work)`) in `application/` and implement it with the ORM's transaction in infra.
12. **Time-dependent rules** read the time from a `Clock` port (`FakeClock` in tests), never from `new Date()` inside the rule.

## Definition of done (every feature, every request size)

A feature is not done until all of these exist. "Quick", "minimal" or "just for a demo" changes nothing: this list *is* the minimal version.

- [ ] Entity/value object changes in `enterprise/`, plus an event if another context must react
- [ ] Port method(s) in `application/repositories` (abstract class)
- [ ] `<action>.ts` with exported `<Action>UseCaseRequest` / `<Action>UseCaseResponse` and error classes
- [ ] `<action>.spec.ts`: one `it('should be able to …')` per success behavior and one `it('should not be able to …')` per `left` branch
- [ ] `test/<context>/repositories/in-memory-*` and `test/<context>/factories/make-*` updated
- [ ] Database schema change + migration file
- [ ] Mapper + ORM repository under `infra/database/<orm>/<context>/`, bound in the database module
- [ ] Handler under `infra/http/<context>/<resource>/` with schema validation, error mapping and presenter, registered in the context's HTTP module (created when the context gets its first route)
- [ ] `<action>.controller.e2e-spec.ts` with `test('[METHOD] /path')`
- [ ] Any new env var added to the env schema and `.env.example`
- [ ] Cross-context reaction: subscriber + its spec (`waitFor`) + event-flow e2e + registration in the events module

## Red flags

| Thought | Reality |
|---|---|
| "The user asked for minimal, so I'll skip e2e/factories/presenters" | The definition of done is the minimum. Skipping it creates the debt this architecture exists to avoid. |
| "Only one context, so a flat `controllers/` folder is fine" | Contexts get added later and flat folders never get split. Use `infra/http/<context>/<resource>/` from day one. |
| "`interface` is more idiomatic for ports" | `abstract class` survives compilation and works as a DI token. Keep one convention. |
| "A descriptive e2e title is more helpful" | The title is the route (`[POST] /books/:bookId/loans`). Describe behaviors in unit tests. |
| "`it('returns 404 …')` reads fine" | Unit tests start with `should`. |
| "Generic errors belong to this context" | `ResourceNotFoundError`/`NotAllowedError` live in `core/errors/errors/` and are shared. |
| "I'll call the other context's use case directly, it's simpler" | Emit an event. A subscriber in the consuming context reacts. |

## Bootstrapping a new project

Copy the whole shared kernel from `references/core.md` into `src/core/` on day one, even the parts the first feature doesn't use. It is small, stable, and the next features will need it. Then create the layout above, the typed env, the e2e setup and the auth-by-default layer before the first feature.

## References (load when implementing)

- `references/core.md` – shared-kernel source to copy: Either, Entity, AggregateRoot, ValueObject, WatchedList, DomainEvents, errors, Optional.
- `references/domain.md` – entity, value object, event, ports, use case, error, subscriber examples.
- `references/infra.md` – env, validation, handler with error mapping, presenter, mapper, repository adapter, module wiring (with and without a DI container), auth-by-default, cache.
- `references/testing.md` – unit spec, in-memory repository, fakes, factories, subscriber test, e2e setup with an isolated schema, e2e route test.
