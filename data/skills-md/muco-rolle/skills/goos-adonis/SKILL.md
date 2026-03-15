---
name: goos-adonis
description: Use when building, testing, or refactoring AdonisJS v7 applications with test-driven development. Covers outside-in TDD workflow, writing acceptance tests (api-client and browser-client), designing testable services with dependency injection, creating test doubles with container.swap, fixing fragile or slow tests, and restructuring fat controllers into clean service layers
---

# GOOS-Style TDD for AdonisJS v7

## Philosophy

**Core principle**: Tests verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't.

**Good tests** are integration-style: they exercise real code paths through public APIs. They describe _what_ the system does, not _how_ it does it. A good test reads like a specification — "authenticated user can create a post" tells you exactly what capability exists. These tests survive refactors because they don't care about internal structure.

**Bad tests** are coupled to implementation. They mock internal collaborators, test private methods, or verify through external means (like querying the database directly instead of using the API). The warning sign: your test breaks when you refactor, but behavior hasn't changed.

**Develop from inputs to outputs**: Work outside-in — start from the external event (HTTP request, browser action) and let each test drive you inward through the layers. The acceptance test defines the entry point; inner-loop tests discover the services and collaborators needed to fulfill it. Don't start from the database schema or model layer and build outward.

See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines.

## Anti-Pattern: Horizontal Slices

**DO NOT write all tests first, then all implementation.** This is "horizontal slicing" — treating RED as "write all tests" and GREEN as "write all code."

```
WRONG (horizontal):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (vertical / tracer bullet):
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  RED→GREEN: test3→impl3
```

Why horizontal slicing fails:

- Tests written in bulk test _imagined_ behavior, not _actual_ behavior
- You end up testing the _shape_ of things (data structures, function signatures) rather than user-facing behavior
- You outrun your headlights, committing to test structure before understanding the implementation
- Tests become insensitive to real changes — they pass when behavior breaks, fail when behavior is fine

This connects directly to GOOS outer/inner loops: each cycle through the inner loop teaches you something about the design. You need that learning before writing the next test.

## The Golden Rule

**Never write new functionality without a failing test.** No exceptions.

## Quick Reference

| GOOS Principle    | AdonisJS Pattern                                                          |
| ----------------- | ------------------------------------------------------------------------- |
| Walking Skeleton  | Functional test (API) or browser test (rendered) on real route            |
| Acceptance Test   | `@japa/api-client` (JSON APIs) or `@japa/browser-client` (rendered pages) |
| Page Objects      | Class-based pages (`BasePage` from `@japa/browser-client`)                |
| Unit Test         | Japa test with `container.swap()` for isolation                           |
| Mock Objects      | `app.container.swap(Service, () => fake)`                                 |
| Adapter Layer     | Service wrapping third-party API (only for services the framework doesn't wrap) |
| Ports & Adapters  | Services + IoC Container + `@inject()`                                    |
| Test Data Builder | AdonisJS model factories                                                  |
| Tell, Don't Ask   | Thin controllers delegating to injected services                          |
| Listen to Tests   | Difficulty testing = design feedback                                      |

## Workflow

### 1. Planning

Before writing any code:

- [ ] Confirm with user what interface changes are needed
- [ ] Determine acceptance test type: API client (JSON APIs) or browser client (rendered pages)
- [ ] Confirm which behaviors to test (prioritize — you can't test everything)
- [ ] Identify opportunities for [deep modules](deep-modules.md)
- [ ] Design interfaces for [testability](interface-design.md)
- [ ] List behaviors to test (not implementation steps)
- [ ] Get user approval on the plan

Ask: "What should the public interface look like? Which behaviors matter most?"

### 2. Tracer Bullet (Walking Skeleton)

Write ONE failing acceptance test → minimal implementation → GREEN. This is your walking skeleton — the thinnest end-to-end slice that proves the architecture works. It front-loads integration risk before you write real features.

The walking skeleton decides broad-brush architecture: routing style, rendering approach, database connectivity, authentication mechanism. Keep it thin but real — a health check or the simplest possible version of the first feature.

```
API app:    RED: client.post('/endpoint') → GREEN: Route → Controller → Service → Model
Rendered:   RED: visit('/page') → assertTextContains → GREEN: Route → Controller → View/Inertia
```

See [acceptance-tests.md](acceptance-tests.md) for tool selection and examples.

### 3. Incremental Loop

For each remaining behavior:

```
RED:   Write next test → fails
GREEN: Minimal code to pass → passes
```

Rules:

- One test at a time
- Only enough code to pass current test
- Don't anticipate future tests
- Keep tests focused on observable behavior

### 4. Refactor

After all tests pass, look for [refactor candidates](refactoring.md). Never refactor while RED — get to GREEN first.

### 5. Brownfield: Adding Features to Existing Code

When working in an existing codebase, the same cycle applies — but start by understanding what's already there:

1. **Read existing tests** to understand current behavior and conventions
2. **Write a failing acceptance test** for the new feature (same as greenfield)
3. **Work inward** through existing layers — reuse existing services, models, and patterns
4. **Extract and refactor** only when the new feature creates clear duplication or design strain

Don't restructure existing code preemptively. Let the new test reveal where the design needs to flex.

## Per-Cycle Checklist

```
[ ] Test describes behavior, not implementation
[ ] Test uses public interface only
[ ] Test would survive internal refactor
[ ] Only mocking types I own (adapters, not third-party)
[ ] Code is minimal for this test
[ ] No speculative features added
```

## Listening to the Tests (Design Feedback)

When tests are hard to write, that's not a testing problem — it's a design problem. The tests are telling you something about your code's structure:

| Test Smell | What It Means | AdonisJS Fix |
| --- | --- | --- |
| Too many `container.swap()` calls in setup | Object has too many dependencies | Split into smaller, focused services |
| Test setup is 30+ lines | Object does too much | Extract collaborators, simplify the API |
| Can't test without mocking your own services | Services too tightly coupled | Let services call through real container; test at a higher level |
| Need to mock concrete classes, not adapters | Missing an abstraction at the boundary | Introduce an adapter service you own |
| Test name needs "and" | Testing multiple behaviors | Split into separate tests |
| Mocking values or DTOs | Overusing mocks | Use real value objects — only mock services at system boundaries |

See [goos-principles.md](goos-principles.md) Part IV for the complete "Listening to the Tests" reference.

## Common Mistakes

| Mistake                                    | Fix                                                       |
| ------------------------------------------ | --------------------------------------------------------- |
| Mocking the framework (Route, HttpContext) | Use functional tests via `@japa/api-client`               |
| Testing methods instead of behavior        | Name tests by feature: "calculates tax for premium users" |
| Skipping the failing test step             | Watch it fail first — verify diagnostics are useful       |
| Fat controllers with all logic inline      | Extract services, inject with `@inject()`                 |
| Mocking third-party libraries directly     | Write adapter service, mock the adapter                   |
| Writing all tests before implementation    | Vertical slices: one RED→GREEN cycle at a time            |
| Starting from the database/model layer     | Develop from inputs to outputs — start from the HTTP request |
| Building all infrastructure before features | Walking skeleton first — thinnest slice end-to-end        |

## Detailed References

- **[acceptance-tests.md](acceptance-tests.md)**: Acceptance test reference — API & browser tools, page objects, walking skeletons
- **[goos-principles.md](goos-principles.md)**: Complete GOOS book concepts organized by part
- **[adonis-testing-patterns.md](adonis-testing-patterns.md)**: AdonisJS v7 code patterns with examples
- **[tests.md](tests.md)**: Good vs bad test examples for AdonisJS
- **[mocking.md](mocking.md)**: When and how to mock in AdonisJS
- **[deep-modules.md](deep-modules.md)**: Deep vs shallow module design
- **[interface-design.md](interface-design.md)**: Designing testable interfaces
- **[refactoring.md](refactoring.md)**: Post-TDD refactor candidates
