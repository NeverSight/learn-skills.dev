---
name: swift-tdd-workflow
description: Test-Driven Development workflow for Swift/iOS. Enforces write-tests-first methodology using Swift Testing framework with XCTest fallback. Covers RED-GREEN-REFACTOR cycle, mocking strategies, and coverage targets.
license: MIT
metadata:
  author: OkminLee
  version: "2.0.0"
---

# Swift TDD Workflow

Test-Driven Development workflow for Swift/iOS projects. Write tests first, implement minimal code, then refactor.

## When to Apply

Use this skill when:
- Implementing new iOS features (ViewModels, UseCases, Repositories)
- Fixing bugs (write a test that reproduces the bug first)
- Refactoring existing Swift code
- Building critical business logic
- Adding new test coverage to existing code

## Quick Reference

### TDD Cycle

```
RED    -> Write a failing test that defines expected behavior
GREEN  -> Write minimal code to make the test pass
REFACTOR -> Improve code quality while keeping tests green
REPEAT -> Continue until the feature is complete
```

### Framework Selection

| Scenario | Framework | Reason |
|----------|-----------|--------|
| New project / new test suite | **Swift Testing** | Apple recommended, declarative API |
| Extending existing XCTest suite | **XCTest** | Maintain consistency |
| Performance tests | **XCTest** | `XCTMetric` support (not in Swift Testing) |
| E2E / UI tests | **XCUITest** (XCTest-based) | Apple official UI testing |
| iOS 17+ new project | **Swift Testing** | Recommended default |
| iOS 16 or below | **XCTest** | Required for compatibility |
| Mixed project | **Both** | Swift Testing for unit, XCTest for UI |

### XCTest to Swift Testing Conversion

| XCTest | Swift Testing |
|--------|---------------|
| `import XCTest` | `import Testing` |
| `class FooTests: XCTestCase` | `@Suite struct FooTests` |
| `func testXxx()` | `@Test func xxx()` |
| `XCTAssertEqual(a, b)` | `#expect(a == b)` |
| `XCTAssertTrue(x)` | `#expect(x)` |
| `XCTAssertFalse(x)` | `#expect(!x)` |
| `XCTAssertNil(x)` | `#expect(x == nil)` |
| `XCTAssertNotNil(x)` | `#expect(x != nil)` |
| `XCTAssertGreaterThan(a, b)` | `#expect(a > b)` |
| `XCTAssertThrowsError` | `#expect(throws:)` |
| `XCTUnwrap(optional)` | `try #require(optional)` |
| `XCTFail("message")` | `Issue.record("message")` |
| `XCTSkip("reason")` | `throw TestSkipped("reason")` |
| `setUpWithError()` | `init() async throws` |
| `tearDown()` | `deinit` |
| `expectation/fulfill` | `confirmation {}` |

## Key Patterns

### RED-GREEN-REFACTOR Cycle

```swift
// Step 1: RED - Write failing test
@Suite struct AddToCartTests {
    @Test func addToCart_withValidItem_addsToCart() async throws {
        let mockCart = MockCartRepository()
        let sut = AddToCartUseCase(cartRepository: mockCart)
        let item = Item.stub()

        try await sut.execute(item: item)

        #expect(mockCart.addedItems.contains(item))
    }
}

// Step 2: GREEN - Minimal implementation
final class AddToCartUseCase {
    private let cartRepository: CartRepositoryProtocol

    init(cartRepository: CartRepositoryProtocol) {
        self.cartRepository = cartRepository
    }

    func execute(item: Item) async throws {
        try await cartRepository.add(item)
    }
}

// Step 3: REFACTOR - Add validation, error handling
@Test func addToCart_withOutOfStockItem_throwsError() async throws {
    let mockCart = MockCartRepository()
    let mockInventory = MockInventoryRepository()
    mockInventory.stockCount = 0
    let sut = AddToCartUseCase(
        cartRepository: mockCart,
        inventoryRepository: mockInventory
    )

    await #expect(throws: CartError.outOfStock) {
        try await sut.execute(item: Item.stub())
    }
}
```

### Swift Testing Basics

```swift
import Testing

@Suite struct MarketSearchTests {
    let sut: MarketSearchUseCase

    init() {
        sut = MarketSearchUseCase(repository: MockMarketRepository())
    }

    @Test func search_returnsSemanticallySimilarMarkets() async throws {
        // Given - setup done in init()

        // When
        let results = try await sut.search(query: "election")

        // Then
        #expect(results.count == 5)
        #expect(results[0].name.contains("Trump"))
    }
}
```

### #require for Optional Unwrapping

```swift
@Test func user_hasValidEmail() throws {
    let user = try #require(fetchUser())  // Fails test if nil
    #expect(user.email.contains("@"))
}
```

### Parameterized Tests

```swift
@Test(arguments: ["election", "sports", "crypto"])
func search_returnsResults(query: String) async throws {
    let results = try await sut.search(query: query)
    #expect(!results.isEmpty)
}

// Multiple argument combinations
@Test(arguments: [
    ("admin", true),
    ("user", false),
    ("guest", false)
])
func permission_check(role: String, expected: Bool) {
    let result = sut.canDelete(role: role)
    #expect(result == expected)
}
```

### Test Naming Conventions

```swift
// XCTest: SUT_Action_ExpectedResult
func test_fetchUser_withInvalidId_throwsError() { }
func test_login_whenNetworkFails_showsAlert() { }

// Swift Testing: Natural language description
@Test("Login with valid credentials returns user")
func loginSuccess() { }

@Test("Fetch user throws error when ID is empty")
func fetchUserInvalidId() { }
```

## Workflow

### Step-by-Step TDD Process

1. **Understand the requirement** - What behavior needs to be implemented?
2. **Define protocols** - Establish contracts and interfaces first
3. **Write the test first** - Define expected inputs and outputs using `@Test` and `#expect`
4. **Run the test** - Confirm it fails (RED). Compile errors count as failure
5. **Write minimal implementation** - Just enough to pass
6. **Run the test** - Confirm it passes (GREEN)
7. **Refactor** - Clean up while tests stay green
8. **Verify coverage** - Ensure adequate coverage (80%+)
9. **Repeat** - Next feature/scenario

### Unit Tests (Swift Testing) - Mandatory

Test in isolation with dependency injection:

```swift
@Suite struct HomeViewModelTests {
    @Test func fetchItems_updatesItems() async throws {
        let mockRepo = MockItemRepository()
        mockRepo.items = [Item.stub()]
        let sut = HomeViewModel(repository: mockRepo)

        await sut.fetchItems()

        #expect(sut.items.count == 1)
        #expect(mockRepo.fetchItemsCallCount == 1)
    }

    @Test func fetchItems_onError_showsAlert() async throws {
        let mockRepo = MockItemRepository()
        mockRepo.error = NetworkError.noConnection
        let sut = HomeViewModel(repository: mockRepo)

        await sut.fetchItems()

        #expect(sut.showingError)
        #expect(sut.items.isEmpty)
    }
}
```

### Integration Tests (Swift Testing) - Mandatory

Test component interaction:

```swift
@Suite struct ItemRepositoryIntegrationTests {
    @Test func fetchAndCache_worksCorrectly() async throws {
        let mockNetwork = MockNetworkClient()
        let realCache = InMemoryCache()
        let sut = ItemRepository(network: mockNetwork, cache: realCache)
        mockNetwork.response = ItemDTO.stubList()

        let items = try await sut.fetchItems()

        #expect(!items.isEmpty)
        let cached = await realCache.get("items")
        #expect(cached != nil)
    }
}
```

### UI Tests (XCUITest) - For Critical Flows

XCUITest uses XCTest framework, NOT Swift Testing. Cannot mix in the same target.

**Recommended structure:**
- `MyAppTests` target: Swift Testing (Unit + Integration)
- `MyAppUITests` target: XCTest (XCUITest only)

See `references/xcuitest-patterns.md` for full patterns.

### @MainActor ViewModel Testing

```swift
@Suite @MainActor struct HomeViewModelTests {
    @Test func fetchItems_updatesState() async {
        let mockRepo = MockItemRepository()
        mockRepo.items = [Item.stub()]
        let sut = HomeViewModel(repository: mockRepo)

        await sut.fetchItems()

        #expect(sut.items.count == 1)
        #expect(!sut.isLoading)
    }
}
```

Apply `@MainActor` to the entire `@Suite` when testing main-actor-isolated types.

## Coverage Targets

| Layer | Target | Notes |
|-------|--------|-------|
| Domain (UseCase, Entity) | 90%+ | Core business logic |
| Data (Repository, DTO) | 80%+ | Data transformation/mapping |
| Presentation (ViewModel) | 70%+ | UI logic |
| View (SwiftUI/UIKit) | 0-30% | Use snapshot tests instead |

### Coverage Exclusions
- Generated code (Core Data entities, SwiftGen)
- Simple DTOs with no logic
- SwiftUI View body
- `#Preview` code

### 100% Coverage Required For
- Financial calculations
- Authentication logic
- Security-critical code (Keychain, encryption)
- Core business logic (UseCases)

### Running Tests with Coverage

```bash
# Run tests with coverage
xcodebuild test \
  -scheme MyApp \
  -destination 'platform=iOS Simulator,name=iPhone 16' \
  -enableCodeCoverage YES

# View coverage report
xcrun xccov view --report --json Build/Logs/Test/*.xcresult

# Swift Package
swift test
swift test --filter LiquidityCalculatorTests
swift test --parallel
```

## References

- `references/swift-testing.md` - Full Swift Testing guide (@Suite, @Test, Tags, Traits, Confirmation)
- `references/xcuitest-patterns.md` - Screen Object Pattern, XCUIElement extensions, CI/CD integration
- `references/mocking-patterns.md` - Protocol-based mocks, actor-based mocks, stubs, fixtures
- `scripts/run-tests.sh` - Shell script for running tests with coverage

## Common Mistakes

### 1. Testing Implementation Details

```swift
// Bad - depends on internal state
#expect(viewModel.internalState == .loading)

// Good - tests observable behavior
#expect(viewModel.isLoading)
```

### 2. No Assertions

```swift
// Bad - no verification
@Test func something() {
    _ = sut.doSomething()
}

// Good - verifies result
@Test func something_returnsExpectedValue() {
    let result = sut.doSomething()
    #expect(result == expectedValue)
}
```

### 3. Flaky Tests (Non-Deterministic)

```swift
// Bad - depends on real network
@Test func network_succeeds() async throws {
    let result = try await realNetworkCall()
    #expect(result != nil)
}

// Good - uses mock
@Test func network_succeeds() async throws {
    let mockNetwork = MockNetworkClient()
    mockNetwork.response = .success(MockData.user)
    let sut = UserService(network: mockNetwork)
    let result = try await sut.fetchUser()
    #expect(result != nil)
}
```

### 4. Too Many Assertions per Test

```swift
// Bad - tests multiple behaviors
@Test func user_isValid() {
    #expect(user.name == "John")
    #expect(user.age == 30)
    #expect(user.email.contains("@"))
    #expect(user.isActive)
}

// Good - focused tests
@Test func user_hasValidName() { #expect(user.name == "John") }
@Test func user_hasValidAge() { #expect(user.age == 30) }
@Test func user_hasValidEmail() { #expect(user.email.contains("@")) }
```

### 5. Mixing Swift Testing and XCTest in the Same Target

```swift
// Bad - both frameworks in one target
import XCTest
import Testing

// Good - separate targets
// MyAppTests: Swift Testing (unit + integration)
// MyAppUITests: XCTest (XCUITest only)
```

**Remember**: Tests are documentation. They should clearly express what the code does and why. Good tests make refactoring safe and confident. Never write implementation before tests.
