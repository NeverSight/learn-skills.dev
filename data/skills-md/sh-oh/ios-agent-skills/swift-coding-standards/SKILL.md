---
name: swift-coding-standards
description: Universal coding standards, best practices, and patterns for Swift and iOS development following Apple's API Design Guidelines.
license: MIT
metadata:
  author: OkminLee
  version: "2.0.0"
---

# Swift Coding Standards & Best Practices

Universal coding standards applicable across all iOS/Swift projects.

## When to Apply

- Writing new Swift code in any iOS, iPadOS, macOS, watchOS, tvOS, or visionOS project
- Reviewing pull requests for Swift codebases
- Refactoring existing Swift code
- Setting up new project architecture and file organization
- Making decisions about naming, error handling, concurrency, or performance

## Quick Reference

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Type | UpperCamelCase | `UserProfile` |
| Function | lowerCamelCase | `fetchUserProfile()` |
| Variable | lowerCamelCase | `userProfile` |
| Constant | lowerCamelCase | `maxRetryCount` |
| Protocol | UpperCamelCase | `Fetchable`, `UserProviding` |
| Enum case | lowerCamelCase | `.loading`, `.success` |
| Boolean | `is`/`has`/`can`/`should` prefix | `isLoading`, `hasCompleted` |
| File (Extension) | `Type+Category` | `Date+Formatting.swift` |

### Access Control

| Level | Scope | Use Case |
|-------|-------|----------|
| `private` | Same declaration | Default for implementation details |
| `fileprivate` | Same file | Rarely used |
| `internal` | Same module | Default (omit keyword) |
| `public` | Other modules | API surface |
| `open` | Other modules + subclass | Framework extension points |

## Core Principles

### 1. Clarity at the Point of Use

Code should read naturally at call sites. Prioritize clarity over brevity. Use descriptive names that explain purpose.

```swift
// Usage reads like English
let market = try await fetchMarketData(for: "market-123")
let score = calculateSimilarity(between: vectorA, and: vectorB)
if isValidEmail(input) { }
```

### 2. KISS (Keep It Simple, Stupid)

- Simplest solution that works
- Avoid over-engineering
- No premature optimization
- Easy to understand > clever code

### 3. DRY (Don't Repeat Yourself)

- Extract common logic into functions
- Create reusable components
- Use protocol extensions for shared behavior
- Avoid copy-paste programming

### 4. YAGNI (You Aren't Gonna Need It)

- Don't build features before they're needed
- Avoid speculative generality
- Add complexity only when required
- Start simple, refactor when needed

## Key Patterns

### Naming Conventions

Follow Apple's API Design Guidelines. Types use PascalCase, everything else uses camelCase. Functions should be verb-based and read naturally at call sites. Booleans should read as assertions (`isLoading`, `hasCompleted`, `canSubmit`).

See [references/naming-conventions.md](references/naming-conventions.md) for comprehensive examples.

### Immutability (CRITICAL)

```swift
// ALWAYS prefer let over var
let user = User(name: "John")
let items = [1, 2, 3]

// Prefer struct over class
struct User {
    let id: UUID
    let name: String
    let email: String
}

// Create new instances instead of mutating
let updatedUser = user.withName("Jane")
let updatedItems = items + [4]
```

### Error Handling

Use the appropriate strategy for each situation:

| Strategy | When to Use |
|----------|-------------|
| `throws` + `do-catch` | Default for recoverable errors |
| Typed throws (Swift 6+) | When callers need specific error types |
| `Result<T, E>` | Callback-based APIs, storing outcomes |
| `Optional` | Simple absence without error details |

See [references/error-handling.md](references/error-handling.md) for detailed patterns and input validation.

### Async/Await

```swift
// Parallel execution with async let
func loadDashboard() async throws -> Dashboard {
    async let users = fetchUsers()
    async let markets = fetchMarkets()
    async let stats = fetchStats()

    return try await Dashboard(
        users: users,
        markets: markets,
        stats: stats
    )
}
```

See [references/concurrency-patterns.md](references/concurrency-patterns.md) for TaskGroup, @MainActor, Sendable, cancellation, and Swift 6.2 features.

### Performance

```swift
// Lazy evaluation for large collections
let processedItems = items.lazy
    .filter { $0.isActive }
    .map { $0.transformed }
    .prefix(10)

// Weak self in closures to avoid retain cycles
Task { [weak self] in
    guard let self else { return }
    let data = try await fetchData()
    await MainActor.run { self.items = data }
}
```

See [references/performance.md](references/performance.md) for value types, file organization, protocol design, and code smell detection.

## SwiftUI Essentials

### View Structure

```swift
// Small, focused views (100-200 lines max)
struct MarketCard: View {
    let market: Market

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(market.name).font(.headline)
            StatusBadge(status: market.status)
            MarketMetrics(market: market)
        }
        .padding()
        .cardStyle()
    }
}
```

### State Management

```swift
@State private var count = 0                     // Local state
@Binding var isPresented: Bool                    // Parent-owned state
@Environment(\.dismiss) private var dismiss       // Environment value
@StateObject private var viewModel = ViewModel()  // Observable object (pre-iOS 17)
```

### Extract ViewBuilder for Readability

```swift
var body: some View {
    VStack {
        headerView
        contentView
        footerView
    }
}

@ViewBuilder
private var headerView: some View {
    HStack {
        titleStack
        Spacer()
        actionButton
    }
}
```

## Comments & Documentation

```swift
// GOOD: Explain WHY, not WHAT
// Use exponential backoff to avoid overwhelming the API during outages
let delay = min(pow(2.0, Double(retryCount)) * 1000, 30000)

/// Searches markets using semantic similarity.
///
/// - Parameters:
///   - query: Natural language search query
///   - limit: Maximum number of results (default: 10)
/// - Returns: Array of markets sorted by similarity score
/// - Throws: `NetworkError` if API fails
func searchMarkets(query: String, limit: Int = 10) async throws -> [Market] { }
```

## Common Patterns

```swift
// Guard early return
guard let value = optionalValue else { return }

// Defer for cleanup
func process() {
    let resource = acquire()
    defer { release(resource) }
    // Use resource
}

// Custom view modifiers for reuse
struct CardStyle: ViewModifier {
    func body(content: Content) -> some View {
        content
            .padding()
            .background(Color(.systemBackground))
            .cornerRadius(12)
            .shadow(radius: 2)
    }
}
```

## Testing Standards

```swift
// Given-When-Then structure
func test_searchMarkets_returnsRelevantResults() async throws {
    // Given
    let query = "election"
    let sut = MarketSearchService()

    // When
    let results = try await sut.search(query: query, limit: 10)

    // Then
    XCTAssertFalse(results.isEmpty)
}

// Descriptive test naming
func test_fetchMarkets_whenNetworkFails_throwsNetworkError() { }
func test_createMarket_withInvalidName_throwsValidationError() { }
```

## Common Mistakes (Anti-Patterns)

### 1. Force Unwrapping

```swift
// BAD: Crashes on nil
let url = URL(string: urlString)!

// GOOD: Safe unwrapping
guard let url = URL(string: urlString) else {
    throw ValidationError.invalidURL
}
```

### 2. Massive Views/ViewModels

Files exceeding 500 lines indicate too much responsibility. Split into focused components: extract subviews, use cases, and services.

### 3. Magic Numbers

```swift
// BAD
if retryCount > 3 { }

// GOOD
private enum Constants {
    static let maxRetries = 3
}
if retryCount > Constants.maxRetries { }
```

### 4. Sequential Async When Parallel is Possible

```swift
// BAD: Each awaits the previous
let users = try await fetchUsers()
let markets = try await fetchMarkets()

// GOOD: Run in parallel
async let users = fetchUsers()
async let markets = fetchMarkets()
return try await (users, markets)
```

### 5. Using print() in Production

```swift
// BAD
print("Debug: \(value)")

// GOOD
import os
private let logger = Logger(subsystem: "com.company.app", category: "Network")
logger.debug("Debug: \(value)")
```

## Code Quality Checklist

- [ ] Follows Swift API Design Guidelines
- [ ] Functions under 40 lines (max 80)
- [ ] SwiftUI View under 200 lines, ViewController under 400 lines
- [ ] Total file under 500 lines (max 800)
- [ ] Nesting under 3 levels
- [ ] 1 major type per file
- [ ] `struct` > `class`, `let` > `var`
- [ ] `guard` for early returns, `private` by default
- [ ] No `print()` in production, use `os_log`/`Logger`
- [ ] No force unwrapping (except `@IBOutlet`)
- [ ] Explicit `@MainActor` for UI updates
- [ ] `Sendable` conformance verified
- [ ] `Task` cancellation handled
- [ ] Meaningful `Error` types with context
- [ ] No unused imports, dead code, or TODO/FIXME without tracking issue
- [ ] Accessibility labels for interactive elements
- [ ] Localization-ready strings
- [ ] Support Dynamic Type and Dark Mode

## References

- [Naming Conventions](references/naming-conventions.md) - Complete naming rules, Apple API Design Guidelines, file naming
- [Error Handling](references/error-handling.md) - Result, throws, typed throws, input validation patterns
- [Concurrency Patterns](references/concurrency-patterns.md) - async/await, actors, Sendable, Swift 6.2, Observation
- [Performance](references/performance.md) - Value types, lazy evaluation, retain cycles, code smell detection

**Remember**: Code quality is not negotiable. Clear, maintainable code enables rapid development and confident refactoring.
