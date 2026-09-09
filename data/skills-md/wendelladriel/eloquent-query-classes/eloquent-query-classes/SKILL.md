---
name: eloquent-query-classes
description: Laravel Eloquent Query Classes pattern for extracting important database operations into focused classes. Use when refactoring repeated Eloquent queries, designing query objects, reviewing repository-like abstractions, deciding between scopes and query classes, or testing complex Laravel queries.
license: MIT
tags:
  - laravel
  - php
  - eloquent
  - database
  - architecture
metadata:
  author: wendelladriel
  version: "1.0.0"
---

# Eloquent Query Classes

Use this skill to organize important Laravel Eloquent queries into small, named classes without replacing Eloquent or introducing a generic repository layer.

## Primary Goal

- Extract only queries that have business meaning, reuse pressure, risk, or complexity.
- Keep query classes focused around one public `handle()` method.
- Preserve Eloquent's expressiveness instead of hiding it behind generic CRUD wrappers.
- Make query behavior easier to find, change, compose, and test.

## When to Apply

Use this skill when the user is:

- duplicating the same Eloquent query in controllers, jobs, commands, exports, dashboards, or API endpoints
- building a report, dashboard, export, background process, admin listing, or important write query
- asking whether a query should be a scope, repository, action, or dedicated class
- refactoring noisy controllers or actions that contain large query chains
- reviewing Laravel architecture involving repositories, model scopes, static model methods, or query objects
- writing tests for complex filtering, ordering, eager loading, aggregates, or write conditions

Do not apply this skill just because Eloquent appears in the code. Simple model lookups, relationship calls, and one-off reads should usually stay direct.

## Workflow

### 1. Inspect the Query Use Case

Before extracting anything, identify what the query means in the application.

Check whether the query:

- appears in more than one entry point
- expresses a business concept that deserves a name
- combines multiple filters, scopes, eager loads, ordering rules, pagination rules, or aggregates
- is part of a report, export, dashboard, scheduled command, or background job
- performs a conditional write that would be costly if implemented incorrectly
- needs focused tests because the exact result set matters

If the query is simple and used once, keep it inline unless the user explicitly wants otherwise.

### 2. Choose the Right Laravel Abstraction

Use the smallest useful abstraction:

- Keep direct Eloquent for simple reads and writes.
- Use local scopes for small reusable model constraints.
- Use query classes for named database use cases that coordinate constraints, filters, eager loading, ordering, aggregation, or important writes.
- Use action classes when the operation coordinates business rules, side effects, jobs, notifications, events, or multiple collaborators.
- Avoid generic repositories that wrap normal Eloquent CRUD methods without adding meaningful behavior.

Query classes and scopes can work together. Let the model own reusable constraints and let the query class own the use case.

### 3. Create the Query Class

Place query classes consistently. For small applications, prefer `app/Queries`. For domain-organized applications, prefer a domain-specific `Queries` directory such as `app/Domain/Orders/Queries`.

Shape the class like an action:

- make it focused on one database query or one related database operation
- use a clear business-oriented name ending in `Query`
- prefer `final readonly class` when dependencies are immutable
- expose one public method: `handle()`
- pass input through `handle()` unless constructor injection is needed for collaborators
- type inputs and return values
- keep helper methods private

Example names:

```text
PendingOrdersQuery
ProductsVisibleToCustomerQuery
InvoicesReadyToBeChargedQuery
ExpireAbandonedOrdersQuery
```

Avoid names that only repeat database mechanics:

```text
GetOrdersQuery
OrderWhereStatusQuery
FetchProductsQuery
FindArticleByIdQuery
```

### 4. Decide Whether `handle()` Returns Results or a Builder

If the query has one expected consumption style, execute it inside `handle()` and return the concrete result.

Use this for counts, collections, paginators, single models, existence checks, and important write operations.

If multiple callers need the same rules but different result types, return an Eloquent `Builder` from `handle()` and let each caller decide whether to call `get()`, `paginate()`, `count()`, `exists()`, or continue composing.

Returning a `Builder` is acceptable. The pattern is about naming important database logic, not hiding Eloquent.

### 5. Keep Callers Focused on Their Job

Controllers should map request input, invoke the query, and return a response. Commands should calculate command-specific inputs, invoke the query, and report the result. Jobs should invoke the query without duplicating the database rules.

Do not move HTTP, CLI, validation, authorization, response formatting, event dispatching, or notification logic into the query class.

### 6. Test Query Behavior

Use Laravel database tests and factories.

Test the query rules, not Eloquent itself:

- included records are included
- excluded records are excluded
- optional filters work independently
- ordering is correct
- eager loading is present when it prevents known N+1 problems
- write queries update only the intended records

Prefer one test for default behavior plus focused tests for important filters and risky edges. Do not test every possible filter combination unless the combinations are business-critical.

If a query class feels too trivial to test, reconsider whether it needed to be extracted.

### 7. Review the Result

After implementation or refactoring, verify that:

- the query class name describes a business question or database use case
- there is only one public `handle()` method
- the class is not becoming a repository or service object
- direct Eloquent is still used where it is clearer
- local scopes remain available for reusable model-level constraints
- callers no longer duplicate the important query rules
- tests cover the behavior that made the query worth extracting

## Rules, References, and Templates

Read before executing:

- `rules/query-class-rules.md` — constraints, decision rules, and anti-patterns for Eloquent Query Classes.
- `examples/pending-orders-query.md` — worked example showing extraction, controller usage, builder returns, writes, and testing.

## Anti-patterns

Avoid using this skill to:

- create query classes for every Eloquent call
- replace all local scopes with classes
- introduce a generic repository layer
- hide Eloquent behind method names like `find`, `create`, `update`, or `delete`
- add abstract base query classes before real duplication exists
- put business workflows, side effects, or response logic inside query classes
- add many public methods to one query class
- make simple code harder to read in the name of architecture
