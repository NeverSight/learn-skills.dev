---
name: testing-swift
description: Swift Testing framework (@Test, #expect, @Suite) for writing tests in Swift. Covers the modern @Test attribute replacing XCTestCase func test* methods, #expect macro replacing XCTAssert*, @Suite for test organization, parameterized tests with @Test(arguments:), test traits (.disabled, .bug, .timeLimit, .tags), testing @Observable models, testing async code with structured concurrency, confirmation API for events/callbacks, and migration from XCTest. Use when writing unit tests, integration tests, or migrating from XCTest to Swift Testing.
---

# Swift Testing Framework

Modern testing with `@Test`, `#expect`, and `@Suite`. Replaces XCTest for new projects.

## Critical Constraints

- ❌ DO NOT use `XCTAssertEqual` in Swift Testing → ✅ Use `#expect(a == b)`
- ❌ DO NOT use `func testSomething()` naming convention → ✅ Use `@Test func something()`
- ❌ DO NOT subclass `XCTestCase` → ✅ Use `@Suite struct` or plain `@Test` functions
- ❌ DO NOT use `XCTAssertThrowsError` → ✅ Use `#expect(throws:) { try something() }`
- ❌ DO NOT use `setUp/tearDown` → ✅ Use `init/deinit` on `@Suite` struct or actor

## Basic Test
```swift
import Testing

@Test("Adding items increases count")
func addItem() {
    var list = ShoppingList()
    list.add("Milk")
    #expect(list.items.count == 1)
    #expect(list.items.first == "Milk")
}
```

## @Suite for Organization
```swift
@Suite("Shopping List Tests")
struct ShoppingListTests {
    var list: ShoppingList

    init() {
        list = ShoppingList()  // Replaces setUp()
    }

    @Test func addItem() {
        list.add("Bread")
        #expect(list.items.contains("Bread"))
    }

    @Test func removeItem() {
        list.add("Bread")
        list.remove("Bread")
        #expect(list.items.isEmpty)
    }
}
```

## Parameterized Tests
```swift
@Test("Validates email format", arguments: [
    ("user@example.com", true),
    ("invalid", false),
    ("a@b.c", true),
    ("@missing.com", false),
])
func emailValidation(email: String, isValid: Bool) {
    #expect(EmailValidator.isValid(email) == isValid)
}

// With enums
enum Priority: CaseIterable { case low, medium, high }

@Test("All priorities have colors", arguments: Priority.allCases)
func priorityColor(priority: Priority) {
    #expect(priority.color != nil)
}
```

## Expectations

```swift
// Equality
#expect(result == expected)

// Boolean
#expect(user.isActive)
#expect(!list.isEmpty)

// Optional
#expect(user.name != nil)
let name = try #require(user.name)  // Unwrap or fail

// Throws
#expect(throws: ValidationError.self) {
    try validator.validate(invalidInput)
}

// Specific error
#expect {
    try parser.parse("")
} throws: { error in
    guard let parseError = error as? ParseError else { return false }
    return parseError.code == .emptyInput
}

// No throw
#expect(throws: Never.self) {
    try safeOperation()
}
```

## Testing Async Code
```swift
@Test func asyncFetch() async throws {
    let service = DataService()
    let items = try await service.fetchItems()
    #expect(!items.isEmpty)
}

@Test(.timeLimit(.minutes(1)))
func longRunningOperation() async throws {
    let result = try await processor.processLargeFile()
    #expect(result.isComplete)
}
```

## Testing @Observable Models
```swift
import Testing
import Observation

@Test func modelUpdates() {
    let model = CounterModel()
    #expect(model.count == 0)

    model.increment()
    #expect(model.count == 1)

    model.reset()
    #expect(model.count == 0)
}

@Test func asyncModelLoading() async {
    let model = ItemListModel()
    await model.loadItems()
    #expect(!model.items.isEmpty)
    #expect(!model.isLoading)
}
```

## Confirmation (for Events/Callbacks)
```swift
@Test func notificationFires() async {
    await confirmation("Callback received") { confirm in
        let observer = EventObserver { event in
            #expect(event.type == .update)
            confirm()
        }
        observer.startListening()
        EventEmitter.emit(.update)
    }
}

// Expected count
await confirmation("Multiple events", expectedCount: 3) { confirm in
    for _ in 0..<3 {
        EventEmitter.emit(.tick)
        confirm()
    }
}
```

## Test Traits
```swift
@Test(.disabled("Flaky on CI"))
func unreliableTest() { }

@Test(.bug("https://github.com/org/repo/issues/42", "Crashes on empty input"))
func knownBug() { }

@Test(.timeLimit(.seconds(5)))
func mustBeFast() async { }

@Test(.tags(.performance))
func benchmarkSort() { }

extension Tag {
    @Tag static var performance: Self
    @Tag static var integration: Self
}
```

## Migration from XCTest

| XCTest | Swift Testing |
|--------|---------------|
| `class FooTests: XCTestCase` | `@Suite struct FooTests` |
| `func testBar()` | `@Test func bar()` |
| `XCTAssertEqual(a, b)` | `#expect(a == b)` |
| `XCTAssertTrue(x)` | `#expect(x)` |
| `XCTAssertNil(x)` | `#expect(x == nil)` |
| `XCTUnwrap(x)` | `try #require(x)` |
| `XCTAssertThrowsError` | `#expect(throws:) { }` |
| `setUp()` | `init()` |
| `tearDown()` | `deinit` |
| `XCTSkip` | `try #require(condition)` |

## References

- [Swift Testing](https://developer.apple.com/documentation/Testing)
- [Migrating from XCTest](https://developer.apple.com/documentation/Testing/MigratingFromXCTest)
- [WWDC 2024: Meet Swift Testing](https://developer.apple.com/videos/play/wwdc2024/10179/)
