---
name: Swift Unit Testing Skill
description: Guidelines and templates for writing effective unit tests with XCTest, including test-driven development practices and mocking techniques.
version: 1.0
activation: Activate for queries on Swift unit testing, XCTest framework, test-driven development, mocking, or testing best practices.
---

# Swift Unit Testing Skill

This skill provides comprehensive guidance on writing effective unit tests using Apple's XCTest framework. It covers test-driven development (TDD), testing patterns, mocking strategies, and best practices for maintaining high-quality test suites.

## Best Practices

1. **Test First**: Follow TDD principles - write tests before implementation.

2. **Single Responsibility**: Each test should verify one specific behavior.

3. **Arrange-Act-Assert**: Structure tests clearly with setup, execution, and verification phases.

4. **Descriptive Names**: Use descriptive test method names that explain what is being tested.

5. **Independent Tests**: Tests should not depend on each other or shared state.

6. **Fast Execution**: Keep tests fast to encourage frequent running.

## Unit Testing Guidelines

- Test public interfaces, not implementation details.
- Use mocking for external dependencies.
- Cover both happy path and edge cases.
- Include tests for error conditions.
- Maintain test code quality equal to production code.
- Run tests frequently during development.

## Examples

### Example 1: Basic XCTest Structure

**User Prompt:** "Create a basic unit test class with setup and teardown methods."

**Expected Output:**
```swift
import XCTest
@testable import MyApp

class CalculatorTests: XCTestCase {
    
    var calculator: Calculator!
    
    override func setUp() {
        super.setUp()
        calculator = Calculator()
    }
    
    override func tearDown() {
        calculator = nil
        super.tearDown()
    }
    
    func testAddition() {
        // Given
        let a = 5
        let b = 3
        
        // When
        let result = calculator.add(a, b)
        
        // Then
        XCTAssertEqual(result, 8, "Addition should return the sum of two numbers")
    }
    
    func testAdditionWithNegativeNumbers() {
        // Given
        let a = 5
        let b = -3
        
        // When
        let result = calculator.add(a, b)
        
        // Then
        XCTAssertEqual(result, 2, "Addition should work with negative numbers")
    }
    
    func testDivisionByZero() {
        // Given
        let a = 10
        let b = 0
        
        // When & Then
        XCTAssertThrowsError(try calculator.divide(a, b)) { error in
            XCTAssertEqual(error as? CalculatorError, CalculatorError.divisionByZero)
        }
    }
}

// Production code
class Calculator {
    func add(_ a: Int, _ b: Int) -> Int {
        return a + b
    }
    
    func divide(_ a: Int, _ b: Int) throws -> Int {
        guard b != 0 else {
            throw CalculatorError.divisionByZero
        }
        return a / b
    }
}

enum CalculatorError: Error {
    case divisionByZero
}
```

### Example 2: Testing Asynchronous Code

**User Prompt:** "How do I write unit tests for asynchronous functions using expectations?"

**Expected Output:**
```swift
import XCTest
@testable import MyApp

class NetworkServiceTests: XCTestCase {
    
    var networkService: NetworkService!
    var mockURLSession: MockURLSession!
    
    override func setUp() {
        super.setUp()
        mockURLSession = MockURLSession()
        networkService = NetworkService(session: mockURLSession)
    }
    
    override func tearDown() {
        networkService = nil
        mockURLSession = nil
        super.tearDown()
    }
    
    func testFetchDataSuccess() {
        // Given
        let expectation = expectation(description: "Fetch data completes")
        let expectedData = "Hello, World!".data(using: .utf8)!
        mockURLSession.data = expectedData
        mockURLSession.response = HTTPURLResponse(url: URL(string: "https://example.com")!,
                                                 statusCode: 200,
                                                 httpVersion: nil,
                                                 headerFields: nil)
        
        // When
        networkService.fetchData(from: URL(string: "https://example.com")!) { result in
            // Then
            switch result {
            case .success(let data):
                XCTAssertEqual(data, expectedData)
            case .failure:
                XCTFail("Expected success but got failure")
            }
            expectation.fulfill()
        }
        
        wait(for: [expectation], timeout: 1.0)
    }
    
    func testFetchDataFailure() {
        // Given
        let expectation = expectation(description: "Fetch data fails")
        let expectedError = URLError(.notConnectedToInternet)
        mockURLSession.error = expectedError
        
        // When
        networkService.fetchData(from: URL(string: "https://example.com")!) { result in
            // Then
            switch result {
            case .success:
                XCTFail("Expected failure but got success")
            case .failure(let error):
                XCTAssertEqual((error as? URLError)?.code, .notConnectedToInternet)
            }
            expectation.fulfill()
        }
        
        wait(for: [expectation], timeout: 1.0)
    }
    
    // Modern async/await testing (iOS 15+)
    @available(iOS 15.0, *)
    func testFetchDataAsync() async throws {
        // Given
        let expectedData = "Hello, World!".data(using: .utf8)!
        mockURLSession.data = expectedData
        mockURLSession.response = HTTPURLResponse(url: URL(string: "https://example.com")!,
                                                 statusCode: 200,
                                                 httpVersion: nil,
                                                 headerFields: nil)
        
        // When
        let data = try await networkService.fetchDataAsync(from: URL(string: "https://example.com")!)
        
        // Then
        XCTAssertEqual(data, expectedData)
    }
}

// Mock classes
class MockURLSession: URLSession {
    var data: Data?
    var response: URLResponse?
    var error: Error?
    
    override func dataTask(with url: URL, completionHandler: @escaping (Data?, URLResponse?, Error?) -> Void) -> URLSessionDataTask {
        let task = MockURLSessionDataTask()
        task.completionHandler = {
            completionHandler(self.data, self.response, self.error)
        }
        return task
    }
}

class MockURLSessionDataTask: URLSessionDataTask {
    var completionHandler: (() -> Void)?
    
    override func resume() {
        completionHandler?()
    }
}

// Production code
class NetworkService {
    private let session: URLSession
    
    init(session: URLSession = .shared) {
        self.session = session
    }
    
    func fetchData(from url: URL, completion: @escaping (Result<Data, Error>) -> Void) {
        session.dataTask(with: url) { data, response, error in
            if let error = error {
                completion(.failure(error))
            } else if let data = data {
                completion(.success(data))
            }
        }.resume()
    }
    
    @available(iOS 15.0, *)
    func fetchDataAsync(from url: URL) async throws -> Data {
        let (data, _) = try await session.data(from: url)
        return data
    }
}
```

### Example 3: Mocking with Protocols

**User Prompt:** "Create unit tests with protocol-based mocking for dependency injection."

**Expected Output:**
```swift
import XCTest
@testable import MyApp

class UserManagerTests: XCTestCase {
    
    var userManager: UserManager!
    var mockUserService: MockUserService!
    var mockNotificationCenter: MockNotificationCenter!
    
    override func setUp() {
        super.setUp()
        mockUserService = MockUserService()
        mockNotificationCenter = MockNotificationCenter()
        userManager = UserManager(userService: mockUserService,
                                notificationCenter: mockNotificationCenter)
    }
    
    override func tearDown() {
        userManager = nil
        mockUserService = nil
        mockNotificationCenter = nil
        super.tearDown()
    }
    
    func testLoginSuccess() {
        // Given
        let user = User(id: 1, name: "John Doe")
        mockUserService.loginResult = .success(user)
        
        // When
        userManager.login(username: "john", password: "password") { result in
            // Then
            switch result {
            case .success(let loggedInUser):
                XCTAssertEqual(loggedInUser.id, user.id)
                XCTAssertEqual(loggedInUser.name, user.name)
                XCTAssertTrue(self.mockNotificationCenter.postCalled)
            case .failure:
                XCTFail("Expected success but got failure")
            }
        }
    }
    
    func testLoginFailure() {
        // Given
        mockUserService.loginResult = .failure(UserServiceError.invalidCredentials)
        
        // When
        userManager.login(username: "john", password: "wrong") { result in
            // Then
            switch result {
            case .success:
                XCTFail("Expected failure but got success")
            case .failure(let error):
                XCTAssertEqual(error as? UserServiceError, .invalidCredentials)
                XCTAssertFalse(self.mockNotificationCenter.postCalled)
            }
        }
    }
    
    func testLogout() {
        // When
        userManager.logout()
        
        // Then
        XCTAssertTrue(mockUserService.logoutCalled)
        XCTAssertTrue(mockNotificationCenter.postCalled)
    }
}

// Mock implementations
class MockUserService: UserServiceProtocol {
    var loginResult: Result<User, Error>?
    var logoutCalled = false
    
    func login(username: String, password: String, completion: @escaping (Result<User, Error>) -> Void) {
        if let result = loginResult {
            completion(result)
        }
    }
    
    func logout() {
        logoutCalled = true
    }
}

class MockNotificationCenter: NotificationCenterProtocol {
    var postCalled = false
    
    func post(name: Notification.Name, object: Any?) {
        postCalled = true
    }
}

// Protocols
protocol UserServiceProtocol {
    func login(username: String, password: String, completion: @escaping (Result<User, Error>) -> Void)
    func logout()
}

protocol NotificationCenterProtocol {
    func post(name: Notification.Name, object: Any?)
}

// Production code
class UserManager {
    private let userService: UserServiceProtocol
    private let notificationCenter: NotificationCenterProtocol
    
    init(userService: UserServiceProtocol, notificationCenter: NotificationCenterProtocol) {
        self.userService = userService
        self.notificationCenter = notificationCenter
    }
    
    func login(username: String, password: String, completion: @escaping (Result<User, Error>) -> Void) {
        userService.login(username: username, password: password) { [weak self] result in
            if case .success = result {
                self?.notificationCenter.post(name: .userDidLogin, object: nil)
            }
            completion(result)
        }
    }
    
    func logout() {
        userService.logout()
        notificationCenter.post(name: .userDidLogout, object: nil)
    }
}

struct User {
    let id: Int
    let name: String
}

enum UserServiceError: Error {
    case invalidCredentials
    case networkError
}

extension Notification.Name {
    static let userDidLogin = Notification.Name("userDidLogin")
    static let userDidLogout = Notification.Name("userDidLogout")
}
```

### Example 4: Performance Testing

**User Prompt:** "Write a performance test to ensure a function executes within acceptable time limits."

**Expected Output:**
```swift
import XCTest
@testable import MyApp

class PerformanceTests: XCTestCase {
    
    var dataProcessor: DataProcessor!
    
    override func setUp() {
        super.setUp()
        dataProcessor = DataProcessor()
    }
    
    override func tearDown() {
        dataProcessor = nil
        super.tearDown()
    }
    
    func testDataProcessingPerformance() {
        // Given
        let largeDataset = Array(1...10000)
        
        // When & Then
        measure {
            _ = dataProcessor.process(data: largeDataset)
        }
    }
    
    func testDataProcessingPerformanceWithMetrics() {
        // Given
        let largeDataset = Array(1...10000)
        
        // When & Then
        measure(metrics: [XCTClockMetric(), XCTCPUMetric(), XCTMemoryMetric()]) {
            _ = dataProcessor.process(data: largeDataset)
        }
    }
    
    func testDataProcessingDoesNotExceedTimeLimit() {
        // Given
        let largeDataset = Array(1...10000)
        let maximumAllowedTime: TimeInterval = 0.1 // 100ms
        
        // When
        let startTime = Date()
        let result = dataProcessor.process(data: largeDataset)
        let elapsedTime = Date().timeIntervalSince(startTime)
        
        // Then
        XCTAssertLessThan(elapsedTime, maximumAllowedTime,
                         "Data processing took \(elapsedTime) seconds, which exceeds the limit of \(maximumAllowedTime) seconds")
        XCTAssertFalse(result.isEmpty)
    }
}

// Production code
class DataProcessor {
    func process(data: [Int]) -> [Int] {
        // Simulate some processing work
        return data.map { $0 * 2 }.filter { $0 > 100 }
    }
}
```

### Example 5: UI Testing Basics

**User Prompt:** "Create a basic UI test for a SwiftUI view with a button and text field."

**Expected Output:**
```swift
import XCTest

class MyAppUITests: XCTestCase {
    
    var app: XCUIApplication!
    
    override func setUp() {
        super.setUp()
        continueAfterFailure = false
        app = XCUIApplication()
        app.launch()
    }
    
    override func tearDown() {
        app = nil
        super.tearDown()
    }
    
    func testLoginFlow() {
        // Given
        let usernameField = app.textFields["Username"]
        let passwordField = app.secureTextFields["Password"]
        let loginButton = app.buttons["Login"]
        let welcomeMessage = app.staticTexts["Welcome!"]
        
        // When
        usernameField.tap()
        usernameField.typeText("testuser")
        
        passwordField.tap()
        passwordField.typeText("password123")
        
        loginButton.tap()
        
        // Then
        XCTAssertTrue(welcomeMessage.exists, "Welcome message should appear after successful login")
    }
    
    func testLoginValidation() {
        // Given
        let loginButton = app.buttons["Login"]
        let errorMessage = app.staticTexts["Please enter username and password"]
        
        // When
        loginButton.tap()
        
        // Then
        XCTAssertTrue(errorMessage.exists, "Error message should appear when trying to login without credentials")
    }
    
    func testNavigation() {
        // Given
        let settingsButton = app.buttons["Settings"]
        let backButton = app.navigationBars.buttons["Back"]
        
        // When
        settingsButton.tap()
        
        // Then
        XCTAssertTrue(app.navigationBars["Settings"].exists, "Settings screen should be displayed")
        
        // When
        backButton.tap()
        
        // Then
        XCTAssertTrue(app.navigationBars["Home"].exists, "Should navigate back to home screen")
    }
}
```

Note: UI tests require setting up accessibility identifiers in your SwiftUI views:

```swift
struct LoginView: View {
    @State private var username = ""
    @State private var password = ""
    
    var body: some View {
        VStack {
            TextField("Username", text: $username)
                .accessibility(identifier: "Username")
            
            SecureField("Password", text: $password)
                .accessibility(identifier: "Password")
            
            Button("Login") {
                // Login logic
            }
            .accessibility(identifier: "Login")
        }
    }
}
```