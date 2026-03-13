---
name: swift-6-agent-skill
description: >
  Generate, review, or refactor Swift code using modern language features from
  Swift 6.0 through 6.2.3. Use when writing new Swift code, reviewing existing code
  for outdated patterns, migrating from Swift 5.x to 6.x, debugging concurrency
  warnings, or answering questions about current Swift idioms. Covers concurrency,
  typed throws, noncopyable types, observation, testing, and more.
---

# Swift Modern Patterns (6.0–6.2)

## Overview

Use this skill to ensure Swift code uses current language features and avoids
deprecated or outdated patterns. It covers Swift 6.0, 6.1, and 6.2 with
SE-proposal-level traceability. This skill focuses on language-level features
and best practices without enforcing specific architectures.

## Workflow Decision Tree

### 1) Generate new Swift code
- Determine the target Swift version and language mode (5 vs 6)
- Use modern concurrency patterns by default (see [Concurrency Guidelines](#concurrency))
- Apply typed throws where the error set is fixed and internal (see `references/SWIFT_6_0.md`)
- Use `@Observable` + `Observations` for reactive state outside SwiftUI (SE-0475, see `references/SWIFT_6_2.md`)
- Use trailing commas in multi-line parameter lists (SE-0439)
- Use raw identifiers for test names (SE-0451, see `references/SWIFT_6_2.md`)
- Name all tasks for debuggability (SE-0469)
- Prefer `InlineArray` for fixed-size collections (SE-0453, see `references/SWIFT_6_2.md`)

### 2) Review existing Swift code
- Check for deprecated or outdated patterns against the [Quick Reference](#quick-reference-old--new) table below
- Audit concurrency safety: global variables, actor isolation, Sendable conformance (see `references/SWIFT_6_0.md`)
- Verify `@MainActor` annotations are explicit where needed post-SE-0401
- Check import visibility: transitive imports should be explicit (SE-0444, see `references/SWIFT_6_1.md`)
- Look for unnecessary `@unchecked Sendable` — compiler region analysis (SE-0414) may make them redundant
- Verify test code uses Swift Testing patterns, not legacy XCTest (see [Testing](#testing))
- Run through the [Review Checklist](#review-checklist) systematically

### 3) Refactor or migrate Swift 5.x → 6.x
- Read `references/MIGRATION.md` for comprehensive old → new mappings with before/after code
- Start with concurrency: enable strict checking, resolve global variable warnings (SE-0412)
- Add explicit `@MainActor` to views using `@StateObject`/`@ObservedObject` (SE-0401)
- Consider enabling `-default-isolation MainActor` for UI-focused modules (SE-0466, Swift 6.2+)
- Replace implicit imports with explicit per-file imports (SE-0444)
- Upgrade test suites: `#expect(throws:)` return values (ST-0006), exit tests (ST-0008)
- For version-specific details, see `references/SWIFT_6_0.md`, `references/SWIFT_6_1.md`, `references/SWIFT_6_2.md`

### 4) Debug concurrency warnings or errors
- "Sending value of non-Sendable type..." → Check if compiler region analysis (SE-0414) resolves it; if not, see `references/SWIFT_6_0.md` for `sending` keyword (SE-0430)
- "Main actor-isolated ... cannot be used from nonisolated context" → Verify `@MainActor` annotations; consider `nonisolated` at type level (SE-0449, see `references/SWIFT_6_1.md`)
- "Global variable ... is not concurrency-safe" → Make it `let`, isolate to `@MainActor`, or use `nonisolated(unsafe)` as last resort (SE-0412, see `references/SWIFT_6_0.md`)
- Nonisolated async running on wrong actor → In Swift 6.2+, nonisolated async inherits caller's actor (SE-0461); use `@concurrent` to opt out (see `references/SWIFT_6_2.md`)
- Deinit cannot access actor-isolated state → Use `isolated deinit` (SE-0371, Swift 6.2+, see `references/SWIFT_6_2.md`)

### 5) Answer questions about Swift features
- Identify the Swift version the question relates to
- Route to the appropriate reference file for syntax and examples
- Always cite SE proposal numbers when explaining features

## Core Guidelines

### Concurrency

- **Default to MainActor isolation when appropriate.** For app/UI modules in Swift 6.2+, prefer `-default-isolation MainActor` and only opt out with `nonisolated` or `@concurrent` where background work is genuinely needed (SE-0466).
- **Trust the compiler's isolation region analysis.** Do not add unnecessary `@Sendable` conformances or `@unchecked Sendable` when the compiler can prove safety through region isolation (SE-0414).
- **Use `Mutex` for shared mutable state** — prefer `Mutex` from the Synchronization library over `NSLock` or `os_unfair_lock`. Use `Atomic` for simple lock-free flags and counters (SE-0433, SE-0410).
- **Use `nonisolated` on types** to opt out of inherited actor isolation at the type level rather than annotating every member (SE-0449, Swift 6.1+).
- **Prefer `Task.immediate`** when the task must begin executing synchronously from the caller's context before any suspension point (SE-0472, Swift 6.2+).
- **Name tasks for debuggability.** Always pass a `name:` parameter to `Task.init()`, `Task.detached()`, and `addTask()` in task groups (SE-0469, Swift 6.2+).
- **Understand nonisolated async changes.** Nonisolated async functions now run on the caller's actor by default. Use `@concurrent` to opt into the old hop-off behavior (SE-0461, Swift 6.2+).
- **Use `isolated deinit`** for actor-isolated classes that need safe cleanup of non-Sendable state (SE-0371, Swift 6.2+).
- **Use global-actor isolated conformances** when protocol conformance requires access to actor-isolated state, e.g., `@MainActor Equatable` (SE-0470, Swift 6.2+).

### Error Handling

- **Prefer typed throws for constrained domains** where the error set is fixed and known (internal modules, embedded Swift). Use untyped `throws` for public library APIs to preserve flexibility (SE-0413).
- **Leverage typed throws in generic contexts** — `throws(E)` enables `throws(Never)` inference for non-throwing closures, eliminating unnecessary do/catch.

### Types and Data

- **Use `InlineArray`** for fixed-size collections where the count is known at compile time. Prefer `[N of T]` sugar syntax (SE-0483). Note: does not conform to `Sequence`/`Collection` — iterate via `.indices` (SE-0453, Swift 6.2+).
- **Use `weak let`** for immutable weak references, especially in `Sendable` types where `weak var` would prevent conformance (SE-0481, Swift 6.2+).
- **Prefer noncopyable types (`~Copyable`)** for unique-ownership semantics. `Optional` and `Result` now support noncopyable wrapped types (SE-0427, SE-0437, Swift 6.0+).

### Observation

- **Use `Observations`** for programmatic observation of `@Observable` changes outside SwiftUI — replaces manual KVO or Combine-based observation (SE-0475, Swift 6.2+).

### Debugging

- **Use `@DebugDescription`** on types with `CustomDebugStringConvertible` to enable custom formatting in LLDB's `p` command and Xcode's variables view (SE-0440, Swift 6.0+).

### Enums and API Design

- **Leave public package enums extensible** — do not add `@frozen` unless the case list is genuinely complete and will never grow. This allows adding cases in minor versions without breaking consumers (SE-0487, Swift 6.2.3+).
- **Add `@unknown default` to switches** over public enums from external packages to future-proof against new cases.
- **Add `@retroactive`** when conforming external types to external protocols to acknowledge the retroactive conformance and silence the compiler warning (SE-0364, Swift 6.0+).

### Code Style

- **Use trailing commas** in multi-line parameter lists, arrays, and generics. Improves diff quality and commenting convenience (SE-0439, Swift 6.1+).
- **Use raw identifiers** for human-readable test names and enum cases starting with numbers (SE-0451, Swift 6.2+).
- **Use default values in string interpolation** — `\(optional, default: "fallback")` supports cross-type defaults (SE-0477, Swift 6.2+).

### Imports and Modules

- **Use access-level import modifiers** — `internal import` or `private import` to prevent accidental API leakage (SE-0409, Swift 6.0+).
- **Enable `MemberImportVisibility` flag** to require explicit imports per file (SE-0444, Swift 6.1+).

### Testing

- **Prefer Swift Testing over XCTest** for new test targets. Use `@Test`, `#expect`, `#require`.
- **Use range-based confirmations** — `confirmation(expectedCount: 5...10)` (ST-0005, Swift 6.1+).
- **Use returned errors from `#expect(throws:)`** instead of the deprecated dual-trailing-closure form (ST-0006, Swift 6.1+).
- **Use test scoping traits** for concurrency-safe shared test configuration via `TestScoping` protocol (ST-0007, Swift 6.1+).
- **Use exit tests** — `#expect(processExitsWith: .failure)` for testing `precondition`/`fatalError` paths (ST-0008, Swift 6.2+).
- **Use test attachments** — `Attachment.record(value, named:)` for debugging failing tests (ST-0009, Swift 6.2+).

## Quick Reference: Old → New

| Deprecated / Outdated | Modern Replacement | Since | SE |
|-----------------------|-------------------|-------|-----|
| Bare global `var` | `let`, `@MainActor var`, or `nonisolated(unsafe)` | 6.0 | SE-0412 |
| `@StateObject` infers `@MainActor` | Explicit `@MainActor` on view required | 6.0 | SE-0401 |
| Catch-all for exhaustive error types | `throws(SpecificError)` eliminates catch-all | 6.0 | SE-0413 |
| `withTaskGroup(of: T.self)` | `withTaskGroup { }` (type inferred) | 6.1 | SE-0442 |
| Per-member `nonisolated` | `nonisolated struct/class` at type level | 6.1 | SE-0449 |
| Transitive imports leak across files | Enable `MemberImportVisibility` flag | 6.1 | SE-0444 |
| `#expect { } throws: { }` (dual closure) | `let error = #expect(throws: T.self) { }` | 6.1 | ST-0006 |
| Manual `@MainActor` on every type | `-default-isolation MainActor` per module | 6.2 | SE-0466 |
| camelCase test names + `@Test("...")` | Raw identifiers: `` @Test func `readable name`() `` | 6.2 | SE-0451 |
| Nonisolated async hops off actor | Now stays on caller's actor; `@concurrent` to opt out | 6.2 | SE-0461 |
| `Task { }` for immediate work | `Task.immediate { }` runs synchronously until first `await` | 6.2 | SE-0472 |
| `weak var` in Sendable types | `weak let` enables Sendable conformance | 6.2 | SE-0481 |
| Combine/KVO for `@Observable` changes | `Observations { }` AsyncSequence | 6.2 | SE-0475 |
| Tuples for fixed-size data | `InlineArray<N, T>` with subscript access | 6.2 | SE-0453 |
| `\(optional ?? "fallback")` (same type only) | `\(optional, default: "fallback")` (cross-type) | 6.2 | SE-0477 |
| Regular `deinit` in actor-isolated class | `isolated deinit` for safe cleanup | 6.2 | SE-0371 |
| `InlineArray<N, T>` (verbose) | `[N of T]` sugar syntax | 6.2 | SE-0483 |
| `NSLock` / `os_unfair_lock` | `Mutex` from Synchronization library | 6.0 | SE-0433 |
| Manual atomic operations / locks for flags | `Atomic<Value>` from Synchronization library | 6.0 | SE-0410 |
| No LLDB summary from `debugDescription` | `@DebugDescription` macro enables `p` command formatting | 6.0 | SE-0440 |
| Silent retroactive conformance | `@retroactive` annotation required (compiler warning) | 6.0 | SE-0364 |
| `String(bytes:encoding:)` | `String(validating:as: UTF8.self)` returns `Optional` | 6.0 | SE-0405 |
| Adding enum case = SemVer-major break | Extensible by default; `@frozen` to opt out | 6.2.3 | SE-0487 |

## Review Checklist

### Concurrency Safety
- [ ] No bare mutable global variables (must be `let`, actor-isolated, or `nonisolated(unsafe)`)
- [ ] Views using `@StateObject`/`@ObservedObject` have explicit `@MainActor`
- [ ] No unnecessary `@unchecked Sendable` — check if region analysis handles it
- [ ] Shared mutable state uses `Mutex` or `Atomic`, not `NSLock`/`os_unfair_lock`
- [ ] Tasks are named with `name:` parameter
- [ ] `nonisolated async` behavior is intentional (caller-inheriting in 6.2+ vs hop-off in <6.2)
- [ ] `isolated deinit` used where actor-isolated class accesses non-Sendable state in cleanup

### Error Handling
- [ ] Typed throws used for internal/fixed error sets; untyped throws for public APIs
- [ ] No unnecessary catch-all blocks when typed throws covers all cases

### Modern Patterns
- [ ] `InlineArray` uses `[N of T]` sugar syntax where available
- [ ] `weak let` used instead of `weak var` where immutability suffices (enables `Sendable`)
- [ ] `Observations` used instead of Combine/KVO for `@Observable` outside SwiftUI
- [ ] String interpolation uses `default:` parameter for optional cross-type fallbacks
- [ ] Trailing commas in multi-line lists
- [ ] `@DebugDescription` used on types with `CustomDebugStringConvertible`
- [ ] `String(validating:as:)` used instead of `String(bytes:encoding:)` for safe encoding

### Imports
- [ ] No transitive import dependencies (`MemberImportVisibility` enabled)
- [ ] Access-level imports used to prevent API leakage (`internal import`, `private import`)

### API Design
- [ ] Public package enums: extensible by default, `@frozen` only when case list is truly fixed
- [ ] Consumer `switch` over external enums includes `@unknown default`
- [ ] Retroactive conformances annotated with `@retroactive`

### Testing
- [ ] Swift Testing preferred over XCTest for new tests
- [ ] `#expect(throws:)` returns error for separate validation (not dual-closure form)
- [ ] Exit tests used for `precondition`/`fatalError` paths
- [ ] Test scoping traits used for shared configuration (not mutable shared state)
- [ ] Raw identifiers used for readable test names

## Version Coverage

| Version | Release     | Key Features |
|---------|-------------|-------------|
| 6.0     | Sep 2024    | Complete concurrency by default, typed throws, Mutex/Atomics, noncopyable upgrades, RangeSet, Int128 |
| 6.1     | Spring 2025 | Trailing commas, metatype key paths, diagnostic groups, nonisolated types, import visibility |
| 6.2     | WWDC 2025   | Default MainActor isolation, raw identifiers, InlineArray + `[N of T]` sugar, immediate tasks, weak let, Observations |
| 6.2.3   | Late 2025   | Extensible enums for non-resilient modules (SE-0487) |

## References

- `references/SWIFT_6_0.md` — Concurrency defaults, Mutex/Atomics, typed throws, @DebugDescription, noncopyable upgrades, AsyncSequence generics, RangeSet, Int128, BitwiseCopyable
- `references/SWIFT_6_1.md` — Trailing commas, metatype key paths, TaskGroup inference, nonisolated types, import visibility, diagnostic groups, Swift Testing improvements
- `references/SWIFT_6_2.md` — Default MainActor isolation, raw identifiers, InlineArray + `[N of T]` sugar, immediate tasks, weak let, Observations, Span/MutableSpan, method key paths, exit tests
- `references/SWIFT_6_2_3.md` — Extensible enums for non-resilient modules (SE-0487)
- `references/MIGRATION.md` — Comprehensive old → new pattern mappings with before/after code for all versions

## Philosophy

This skill focuses on **language-level facts and best practices**, not opinions:

- **No architecture enforcement.** We don't prescribe MVVM, TCA, VIPER, or any pattern. We suggest modern language features; how you structure your app is your decision.
- **No formatting or linting rules.** Property ordering, brace style, and line length are out of scope.
- **SE-proposal grounded.** Every recommendation traces to a Swift Evolution proposal. If it's not in an SE, it's not in this skill.
- **Version-aware.** Every feature is tagged with the Swift version that introduced it. The agent should not suggest Swift 6.2 features to a project targeting Swift 6.0.
- **Practical over comprehensive.** The agent's context window is finite. These files contain what matters for day-to-day code generation and review, not exhaustive API documentation.
