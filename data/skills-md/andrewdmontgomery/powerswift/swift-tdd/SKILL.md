---
name: swift-tdd
description: Use when implementing any Swift or SwiftUI feature or bugfix, before writing implementation code
---

## Overview

The fundamental approach is: **Write the test first. Watch it fail. Write minimal code to pass.**

**Core principle:** "If you didn't watch the test fail, you don't know if it tests the right thing."

This skill combines Test-Driven Development discipline with Swift Testing, SwiftUI, and Swift Concurrency best practices.

## When to Use

Apply TDD consistently for:
- New features (SwiftUI views, view models, services)
- Bug fixes
- Refactoring
- Behavior changes
- Async/concurrent logic

Exceptions require explicit human approval and typically only apply to throwaway prototypes, generated code, asset catalogs, or configuration plists.

## The Iron Law

**NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST.**

Code written before tests must be deleted completely and reimplemented through TDD, without keeping it as reference material.

## Red-Green-Refactor Cycle

**RED:** Write one minimal failing test demonstrating required behavior

**GREEN:** Implement the simplest Swift code that passes the test

**REFACTOR:** Clean up code while keeping all tests green

## Testing Rules by Layer

### View Models (`@Observable` classes)

- Test logic and state changes; do not test SwiftUI rendering.
- Mark view models `@MainActor` and call them from `@MainActor` test contexts.
- Inject dependencies (network, persistence) via protocols so tests can substitute fakes.

```swift
@MainActor
@Suite("ProfileViewModel")
struct ProfileViewModelTests {

    @Test("loading sets user name")
    func loadingSetsUserName() async throws {
        let fake = FakeUserService(stub: User(name: "Ada"))
        let vm = ProfileViewModel(service: fake)
        await vm.load()
        #expect(vm.userName == "Ada")
    }
}
```

### Services and Repositories

- Use in-memory or fake implementations, not real network/database.
- Use `#require` to unwrap optionals when subsequent assertions depend on them.

### Async / Concurrent Code

- Mark test functions `async` and `await` all async calls — never spin or sleep.
- Bridge callback-based APIs with `withCheckedContinuation` or `AsyncStream` rather than `XCTestExpectation`.
- Use `confirmation()` for callback-based event verification.

### SwiftUI Views

SwiftUI `body` should not be unit-tested directly. Instead:

1. **Extract logic** into `@Observable` view models and test the model.
2. **Extract pure helpers** (formatters, validators) as free functions or types and test those.
3. **Use UI tests** (`XCUIApplication`) only for end-to-end critical paths.

```swift
// GOOD — test the model that drives the view
@Test("submit disables when title is empty")
func submitDisabledWhenTitleEmpty() {
    let vm = NewPostViewModel()
    vm.title = ""
    #expect(vm.isSubmitDisabled == true)
}

// AVOID — testing SwiftUI rendering or view hierarchy directly in unit tests
```

## Fake/Stub Strategy

Use real code unless a boundary forces isolation:

| Boundary | Strategy |
|----------|----------|
| Network | Protocol + in-memory fake |
| Database | In-memory repository |
| System clock | Injected `Clock` / `TimeProvider` |
| File system | Temp directory per test |
| `@Observable` dependencies | Fake conforming to same protocol |

Never mock `@Observable` view models themselves — test them directly.

## Red Flags for Incomplete TDD

- Code was written before the test
- Test passed immediately on first run (test may not exercise the right thing)
- Cannot explain what the failure message means
- "I'll add tests after" or "it's too simple to test"
- Test only verifies mock calls, not actual behavior

## Common Rationalizations — Addressed

- **"SwiftUI views are hard to test"** — Test the view model, not the view.
- **"async code is tricky"** — Write the async test first; let the compiler guide the implementation.
- **"Too simple to test"** — Simple logic is easiest to TDD. Start there.
- **"I'll test after"** — Code written before tests is tested after. That violates the iron law.
- **"Deleting code is wasteful"** — Sunk-cost fallacy. Delete it and re-implement with TDD.

## Verification Checklist

Before marking any task complete:

- [ ] Every new function, method, or computed property has at least one test
- [ ] Each test was watched failing before implementation was written
- [ ] Minimal production code was written — no speculative logic
- [ ] All tests pass with clean output (`swift test` or Xcode test navigator green)
- [ ] Async tests use `await`, not sleeps or expectations
- [ ] Parameterized tests replace repetitive test methods
- [ ] No test-only methods leaked into production types
- [ ] View models are tested; SwiftUI `body` is not
- [ ] Fakes, not mocks, used at real system boundaries

## Anti-Patterns Reference

See `testing-anti-patterns.md` for Swift-specific testing anti-patterns and how to fix them.

## Related Skills

This skill works in conjunction with:
- **swift-testing-expert** — Deep reference on Swift Testing APIs, traits, async waiting, XCTest migration
- **swiftui-expert-skill** — SwiftUI state management, view composition, modern APIs
- **swift-concurrency** — Actors, Sendable, task isolation, Swift 6 migration
