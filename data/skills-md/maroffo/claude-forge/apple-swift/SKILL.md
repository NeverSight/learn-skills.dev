---
name: apple-swift
description: "Apple platform development with Swift 6, SwiftUI, async/await, and performance. Use when working with .swift files, Package.swift, Xcode projects, or building for iOS/macOS/watchOS/visionOS."
compatibility: "Requires Xcode and platform SDKs. Optional: SwiftLint."
allowed-tools: [mcp__acp__Read, mcp__acp__Edit, mcp__acp__Write, mcp__acp__Bash]
---

# ABOUTME: Apple platform guide - Swift 6, SwiftUI, concurrency, testing, performance
# ABOUTME: Modern Swift (2025-2026): @Observable, SwiftData, NavigationStack, strict concurrency

# Apple Platform Development

## Quick Reference

```bash
# Build
xcodebuild -scheme MyApp -sdk iphoneos build
xcodebuild -scheme MyApp -sdk macosx build

# Tests
xcodebuild test -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 16'

# SwiftLint / SPM
swiftlint lint [--fix]
swift build && swift test && swift package resolve

# ast-grep
sg --pattern '@Observable final class $NAME { $$$ }' --lang swift
sg --pattern '@MainActor' --lang swift
```

**See also:** `_AST_GREP.md`, `_PATTERNS.md`, `source-control`, `references/`

---

## Swift 6

- **Strict concurrency** - Data-race safety at compile time
- **@Observable** - Replaces ObservableObject
- **@MainActor** - UI thread isolation
- **Sendable** - Safe cross-actor value types
- **Macros** - @Observable, @Model, #Preview

**Migration:** Enable `swiftLanguageModes: [.v6]`, replace ObservableObject, add @MainActor to UI classes, add Sendable to value types, use actors for shared state, replace callbacks with `async throws`.

For detailed migration patterns, see `references/swift6-patterns.md`.

---

## SwiftUI

### Property Wrappers

| Wrapper | Use |
|---------|-----|
| `@State` | View-owned values, @Observable |
| `@Binding` | Two-way to parent |
| `@Bindable` | Two-way to @Observable props |
| `@Environment` | System/app values |
| `@StateObject` | View-owned ObservableObject (legacy) |

**View property order:** @Environment, let, @State/@Binding, computed, init, body, private methods

**View sizing:** <100 lines = single view; 100-200 = extract subviews; >200 = multiple files; business logic = @Observable VM; network/DB = repository pattern

For NavigationStack, SwiftData, MVVM, and DI patterns, see `references/swiftui-patterns.md`.

---

## Concurrency

### Common Fixes

| Error | Fix |
|-------|-----|
| Main actor isolation | Add `@MainActor` to class/func |
| Non-isolated access | Mark `nonisolated` |
| Sendable violation | Add `@unchecked Sendable` or fix |
| Protocol async | Require `async` in protocol |
| Closure capture | Use `@Sendable` closure |

### When to use what

| Use Case | Choice |
|----------|--------|
| One-shot network | async/await |
| Parallel fetches | async let / TaskGroup |
| Real-time streams | Combine / AsyncStream |
| UI events, debounce | Combine |

For MainActor, parallel execution, and actor patterns, see `references/concurrency-patterns.md`.

---

## Architecture

**MVVM with @Observable:** `@Observable @MainActor final class VM` with `private(set)` properties, injected service protocols, `async` load methods with `defer { isLoading = false }`.

**DI:** Protocol-based with `EnvironmentKey` for SwiftUI injection.

**Testing (Swift Testing, iOS 18+):** `@Suite`, `@Test`, `#expect`. Parameterized with `arguments:`. Mock via protocol injection.

For full code examples, see `references/swiftui-patterns.md` and `references/swift6-patterns.md`.

---

## Review Checklists

**Concurrency:** MainActor for UI, Sendable for cross-actor data, task cancellation handled, no data races (Swift 6)

**SwiftUI:** @Observable not ObservableObject (iOS 17+), NavigationStack not NavigationView, .task not .onAppear + Task, LazyVStack for long lists

**CRITICAL:** Force unwrap without safety, UI updates off MainActor, data races, retain cycles

**HIGH:** ObservableObject when @Observable available, NavigationView instead of NavigationStack

---

## Detailed References

- `references/swift6-patterns.md` - Swift 6 migration, Sendable, actors, macros
- `references/swiftui-patterns.md` - NavigationStack, SwiftData, MVVM, dependency injection
- `references/concurrency-patterns.md` - async/await, TaskGroup, MainActor, actors, AsyncStream
- `references/performance.md` - Optimization, Instruments profiling, memory management

**Official:** [Swift](https://developer.apple.com/swift/) | [SwiftUI](https://developer.apple.com/documentation/swiftui/) | [SwiftData](https://developer.apple.com/documentation/swiftdata/)

**Libraries:** [TCA](https://github.com/pointfreeco/swift-composable-architecture) | [Snapshot Testing](https://github.com/pointfreeco/swift-snapshot-testing) | [SwiftLint](https://github.com/realm/SwiftLint)
