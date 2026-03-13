---
name: ios-testing
description: iOS testing with XCTest. Unit tests, UI tests, mocks, and test patterns for Swift/SwiftUI.
---

# iOS Testing

Testing patterns for Swift and SwiftUI apps.

## Unit Tests

### Basic Unit Test

```swift
import XCTest
@testable import MyApp

class UserViewModelTests: XCTestCase {
    var sut: UserViewModel!
    var mockService: MockUserService!

    override func setUp() {
        super.setUp()
        mockService = MockUserService()
        sut = UserViewModel(service: mockService)
    }

    override func tearDown() {
        sut = nil
        mockService = nil
        super.tearDown()
    }

    func testLoadUsers_whenSuccessful_populatesUsers() async throws {
        // Given
        let expectedUsers = [User.mock1, User.mock2]
        mockService.usersToReturn = expectedUsers

        // When
        await sut.loadUsers()

        // Then
        XCTAssertEqual(sut.users, expectedUsers)
        XCTAssertFalse(sut.isLoading)
        XCTAssertNil(sut.errorMessage)
    }

    func testLoadUsers_whenFailure_setsErrorMessage() async throws {
        // Given
        mockService.shouldThrowError = true

        // When
        await sut.loadUsers()

        // Then
        XCTAssertTrue(sut.users.isEmpty)
        XCTAssertNotNil(sut.errorMessage)
    }
}
```

### Mocking

```swift
// ✅ Protocol-based mocking
protocol UserServiceProtocol {
    func getUsers() async throws -> [User]
}

class MockUserService: UserServiceProtocol {
    var usersToReturn: [User] = []
    var shouldThrowError = false
    var getUsersCalled = false

    func getUsers() async throws -> [User] {
        getUsersCalled = true
        if shouldThrowError {
            throw NetworkError.noConnection
        }
        return usersToReturn
    }
}

// ✅ Verify method calls
func testRefreshButton_callsService() async {
    // When
    await sut.refresh()

    // Then
    XCTAssertTrue(mockService.getUsersCalled)
}
```

## Async Testing

```swift
func testAsyncOperation_completesSuccessfully() async throws {
    // Given
    let expectation = expectation(description: "Async completes")

    // When
    Task {
        await sut.asyncOperation()
        expectation.fulfill()
    }

    // Then
    await fulfillment(of: [expectation], timeout: 1.0)
}

// ✅ Swift async/await
func testAsyncFetch_returnsUsers() async throws {
    let users = try await sut.fetchUsers()
    XCTAssertFalse(users.isEmpty)
}
```

## Property Testing

```swift
func testUserValidation_validEmails() {
    let validEmails = [
        "test@example.com",
        "user.name@example.co.uk",
        "user+tag@example.com"
    ]

    for email in validEmails {
        XCTAssertTrue(Validator.isValidEmail(email), "Failed for: \(email)")
    }
}

func testUserValidation_invalidEmails() {
    let invalidEmails = [
        "invalid",
        "@example.com",
        "user@",
        "user @example.com"
    ]

    for email in invalidEmails {
        XCTAssertFalse(Validator.isValidEmail(email), "Passed for: \(email)")
    }
}
```

## UI Tests

### Basic UI Test

```swift
import XCTest

class LoginUITests: XCTestCase {
    var app: XCUIApplication!

    override func setUp() {
        super.setUp()
        continueAfterFailure = false
        app = XCUIApplication()
        app.launchArguments = ["--uitesting"]
        app.launch()
    }

    func testLoginButton_enabledWhenFieldsFilled() {
        // When
        let emailField = app.textFields["emailField"]
        let passwordField = app.secureTextFields["passwordField"]
        let loginButton = app.buttons["loginButton"]

        // Then
        XCTAssertFalse(loginButton.isEnabled)

        // When
        emailField.tap()
        emailField.typeText("test@example.com")

        passwordField.tap()
        passwordField.typeText("password123")

        // Then
        XCTAssertTrue(loginButton.isEnabled)
    }

    func testSuccessfulLogin_navigatesToHome() {
        // Given
        app.textFields["emailField"].tap()
        app.textFields["emailField"].typeText("test@example.com")

        app.secureTextFields["passwordField"].tap()
        app.secureTextFields["passwordField"].typeText("password123")

        // When
        app.buttons["loginButton"].tap()

        // Then
        XCTAssertTrue(app.staticTexts["welcomeMessage"].exists)
    }
}
```

### Snapshot Testing

```swift
// ✅ Using View snapshot testing
import SwiftUI
import XCTest

struct UserCard_Previews: PreviewProvider {
    static var previews: some View {
        UserCard(user: .mock)
    }
}

// Snapshot test
func testUserCard_snapshot() {
    let view = UserCard(user: .mock)
    assertSnapshot(matching: view, as: .image(layout: .sizeThatFits))
}
```

## Testing SwiftUI Views

```swift
import XCTest
import ViewInspector  // https://github.com/nalexn/ViewInspector

class UserRowTests: XCTestCase {
    func testUserRow_displaysUserName() throws {
        let user = User(id: "1", name: "John Doe", email: "john@example.com")
        let view = UserRow(user: user)

        let text = try view.inspect().find(ViewType.Text.self).string()
        XCTAssertEqual(text, "John Doe")
    }

    func testUserRow_tapping_callsAction() throws {
        let user = User(id: "1", name: "John", email: "john@example.com")
        var tapped = false
        let view = UserRow(user: user, onTap: { tapped = true })

        try view.inspect().find(ViewType.Button.self).tap()

        XCTAssertTrue(tapped)
    }
}
```

## Test Helpers

```swift
// ✅ Test doubles
extension User {
    static let mock1 = User(id: "1", name: "John", email: "john@example.com")
    static let mock2 = User(id: "2", name: "Jane", email: "jane@example.com")
}

// ✅ Wait helpers
func waitForElementToExist(
    _ element: XCUIElement,
    timeout: TimeInterval = 5.0
) -> Bool {
    let existsPredicate = NSPredicate(format: "exists == true")
    let expectation = expectation(for: existsPredicate, evaluatedWith: element)

    let result = XCTWaiter.wait(for: [expectation], timeout: timeout)
    return result == .completed
}
```

## Performance Tests

```swift
func testUserParsing_performance() {
    let jsonData = largeUserJSONData

    measure {
        _ = try? JSONDecoder().decode([User].self, from: jsonData)
    }
}
```

## Test Organization

```
Tests/
├── Unit/
│   ├── ViewModels/
│   │   ├── HomeViewModelTests.swift
│   │   └── ProfileViewModelTests.swift
│   ├── Services/
│   │   ├── UserServiceTests.swift
│   │   └── NetworkServiceTests.swift
│   └── Models/
│       └── UserTests.swift
├── UI/
│   ├── LoginUITests.swift
│   └── HomeUITests.swift
└── Mocks/
    ├── MockUserService.swift
    └── MockNetworkService.swift
```

---

**Remember**: Tests are your safety net. Write them first (TDD) or alongside your code, but always maintain them.
