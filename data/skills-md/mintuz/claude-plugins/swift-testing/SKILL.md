---
name: swift-testing
description: WHEN writing tests in Swift with the Swift Testing framework; NOT XCTest.
---

# Swift Testing Framework: Basics

Guidance for starting with Swift Testing (Testing framework) and writing clear, macro-driven tests.

## Core Concepts

- Import `Testing` to unlock macros; tests are plain functions annotated with `@Test`.
- Name tests freely; use `@Test("Display Name")` to set the navigator title.
- `#expect` is the primary assertion; pass a boolean expression to assert truthy outcomes.
- Async/throwing tests are supported via `async`/`throws` on the test function.
- Works alongside XCTest in the same project.

## Example: Simple Test

```swift
import Testing

func add(_ a: Int, _ b: Int) -> Int { a + b }

@Test("Verify addition function") func verifyAdd() {
    let result = add(1, 2)
    #expect(result == 3)
}
```

## Expecting Throws

Use `#expect(throws:)` to verify a thrown error. Inspect the error via the closure overload when you need to assert the specific case.

```swift
@Test func verifyThrowingFunction() {
    #expect(throws: MyError.self) {
        try throwingFunction()
    }

    #expect {
        try throwingFunction()
    } throws: { error in
        guard let myError = error as? MyError else { return false }
        return myError == .invalidInput
    }
}
```

## Require vs Expect

- `#require` throws immediately when the condition is false, halting the test early.
- Handy for unwrapping optionals before continuing with more assertions.

```swift
@Test func verifyOptionalFunc() throws {
    let result = try #require(optionalFunc()) // unwrap or fail fast
    #expect(result > 0)
}
```

## Recording Issues

Use `Issue.record("message")` to log and exit gracefully when continuing the test is pointless.

```swift
@Test func verifyOptionalFunc() throws {
    guard let result = optionalFunc() else {
        Issue.record("optional result is nil")
        return
    }
    #expect(result > 0)
}
```

## Best Practices Checklist

- [ ] Prefer `@Test`-annotated free functions; no need for XCTest naming conventions.
- [ ] Use `@Test("Name")` to keep navigator titles readable.
- [ ] Default to `#expect` for assertions; add multiple expects per test when logical.
- [ ] Use `#require` to guard preconditions/unwrap optionals before further checks.
- [ ] Assert thrown errors with `#expect(throws:)`, including specific case checks.
- [ ] Mix Swift Testing with XCTest during migration; convert incrementally.
- [ ] Keep tests small and focused; one behavior per test function.
