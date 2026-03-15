---
name: swift-patterns
description: Core Swift language patterns, optionals, closures, protocols, generics, and modern Swift features.
---

# Swift Language Patterns

Modern Swift idioms for clean, safe code.

## Optionals

### Safe Unwrapping

```swift
// ✅ Good: guard let for early exit
func processUser(_ user: User?) {
    guard let user = user else {
        print("User is nil")
        return
    }
    // user is non-optional here
    print(user.name)
}

// ✅ Good: if let for conditional
if let email = user.email {
    sendEmail(to: email)
}

// ✅ Good: nil coalescing
let displayName = user.name ?? "Anonymous"

// ✅ Good: Optional chaining
let street = user.address?.street

// ❌ Bad: Force unwrap (crashes if nil)
let email = user.email!  // Don't do this
```

### Optional Mapping

```swift
// ✅ map for transformation
let uppercase = user.name?.map { $0.uppercased() }

// ✅ flatMap for chaining optionals
let domain = user.email?.flatMap { $0.split(separator: "@").last }
```

## Closures

### Trailing Closures

```swift
// ✅ Trailing closure syntax
viewModel.fetchUsers { users in
    self.users = users
}

// Equivalent to
viewModel.fetchUsers { users in
    self.users = users
}

// ✅ Shorthand argument names
viewModel.fetchUsers {
    self.users = $0
}
```

### Capture Lists

```swift
// ✅ Capture lists to avoid retain cycles
class UserViewController: UIViewController {
    private let viewModel: UserViewModel

    func setupRefresh() {
        viewModel.onRefresh = { [weak self] in
            guard let self = self else { return }
            self.tableView.reloadData()
        }
    }

    // ✅ Or capture self explicitly when ownership is clear
    func setupTimer() {
        timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { [self] _ in
            self.updateUI()
        }
    }
}
```

### Higher-Order Functions

```swift
let numbers = [1, 2, 3, 4, 5]

// ✅ map - transform
let doubled = numbers.map { $0 * 2 }  // [2, 4, 6, 8, 10]

// ✅ filter - select
let evens = numbers.filter { $0 % 2 == 0 }  // [2, 4]

// ✅ reduce - combine
let sum = numbers.reduce(0) { $0 + $1 }  // 15

// ✅ compactMap - filter out nils
let names = users.compactMap { $0.name }

// ✅ forEach - side effects
numbers.forEach { print($0) }

// ❌ Don't use forEach for transformation
// ❌ Bad: numbers.forEach { doubled.append($0 * 2) }
// ✅ Good: let doubled = numbers.map { $0 * 2 }
```

## Properties

### Computed Properties

```swift
struct User {
    let firstName: String
    let lastName: String

    // ✅ Computed property
    var fullName: String {
        "\(firstName) \(lastName)"
    }

    // ✅ With setter
    var age: Int {
        get { _age }
        set {
            guard newValue >= 0 else { return }
            _age = newValue
        }
    }
    private var _age: Int = 0
}
```

### Property Observers

```swift
class Settings {
    var theme: Theme = .light {
        didSet {
            saveSettings()
            notifyThemeChanged()
        }
    }

    var score: Int = 0 {
        willSet {
            print("Score will change from \(score) to \(newValue)")
        }
        didSet {
            if oldValue > score {
                print("Score decreased!")
            }
        }
    }
}
```

### Lazy Properties

```swift
struct DataProcessor {
    // ✅ Lazy - created only when accessed
    private lazy var formatter: DateFormatter = {
        let formatter = DateFormatter()
        formatter.dateFormat = "yyyy-MM-dd"
        return formatter
    }()

    func process(date: Date) -> String {
        formatter.string(from: date)
    }
}
```

## Protocols

### Protocol-Oriented Programming

```swift
// ✅ Protocol with associated type
protocol Repository {
    associatedtype Item
    func fetch(id: String) async throws -> Item
    func save(_ item: Item) async throws
}

// ✅ Generic where clause
extension Repository {
    func fetchAll(ids: [String]) async throws -> [Item] {
        try await withThrowingTaskGroup(of: Item.self) { group in
            for id in ids {
                group.addTask { try await fetch(id: id) }
            }
            return try await group.reduce(into: [Item]()) { $0.append($1) }
        }
    }
}
```

### Protocol Extensions

```swift
protocol Identifiable {
    var id: String { get }
}

extension Identifiable {
    func debugInfo() -> String {
        "ID: \(id)"
    }
}

struct User: Identifiable {
    let id: String
    let name: String
}

let user = User(id: "123", name: "John")
print(user.debugInfo())  // "ID: 123"
```

## Generics

### Generic Functions

```swift
// ✅ Generic function
func first<T>(_ array: [T]) -> T? {
    array.first
}

// ✅ With constraints
func sorted<T: Comparable>(_ array: [T]) -> [T] {
    array.sorted()
}

// ✅ Multiple constraints
func process<T: Sequence & Sendable>(_ items: T) where T.Element: Hashable {
    // Process items
}
```

### Associated Types

```swift
protocol DataSource {
    associatedtype Item
    func getItems() async throws -> [Item]
}

class RemoteDataSource: DataSource {
    typealias Item = User

    func getItems() async throws -> [User] {
        try await api.getUsers()
    }
}
```

## Result Type

```swift
// ✅ Result for error handling
func fetchUser(id: String) async -> Result<User, Error> {
    do {
        let user = try await api.getUser(id)
        return .success(user)
    } catch {
        return .failure(error)
    }
}

// Usage
let result = await fetchUser(id: "123")
switch result {
case .success(let user):
    displayUser(user)
case .failure(let error):
    showError(error)
}

// ✅ map, flatMap on Result
let name = await fetchUser(id: "123").map(\.name)
```

## Async/Await

### Structured Concurrency

```swift
// ✅ async let for concurrent work
func loadDashboard() async throws -> Dashboard {
    async let user = getUser()
    async let notifications = getNotifications()
    async let stats = getStats()

    return try await Dashboard(
        user: user,
        notifications: notifications,
        stats: stats
    )
}

// ✅ TaskGroup for dynamic concurrency
func fetchAllImages(urls: [URL]) async throws -> [Image] {
    try await withThrowingTaskGroup(of: Image.self) { group in
        for url in urls {
            group.addTask {
                try await downloadImage(from: url)
            }
        }

        var images: [Image] = []
        for try await image in group {
            images.append(image)
        }
        return images
    }
}
```

### MainActor

```swift
// ✅ MainActor for UI updates
@MainActor
class HomeViewModel: Observable {
    @Published var users: [User] = []

    func loadUsers() async {
        // Already on main actor
        let users = try? await api.getUsers()
        self.users = users ?? []
    }
}

// ✅ Explicit main actor dispatch
class NetworkService {
    func fetch() async -> Data {
        // Background work
        let data = ...

        // Dispatch to main if needed
        await MainActor.run {
            // UI work
        }

        return data
    }
}
```

## Enums

### Associated Values

```swift
// ✅ Enum with associated values
enum NetworkError: Error {
    case invalidURL
    case noConnection
    case serverError(code: Int, message: String)
    case decodingError(Error)
}

func handle(_ error: NetworkError) {
    switch error {
    case .invalidURL:
        print("Invalid URL")
    case .noConnection:
        print("No connection")
    case .serverError(let code, let message):
        print("Server error \(code): \(message)")
    case .decodingError(let error):
        print("Decoding failed: \(error)")
    }
}
```

### Enum as State

```swift
// ✅ Enum for exhaustive state
enum LoadState<T> {
    case idle
    case loading
    case loaded(T)
    case error(Error)

    var isLoading: Bool {
        if case .loading = self { return true }
        return false
    }

    var value: T? {
        if case .loaded(let value) = self { return value }
        return nil
    }
}

// Usage
@Published var state: LoadState<[User]> = .idle

switch state {
case .idle:
    EmptyView()
case .loading:
    ProgressView()
case .loaded(let users):
    UserList(users: users)
case .error(let error):
    ErrorView(error: error)
}
```

## Access Control

```swift
// ✅ Use explicit access control
public struct PublicAPI {
    public var value: String

    private init() {
        value = "default"
    }

    // ✅ private for fileprivate only when needed
    private var helper: String {
        "helper"
    }

    // ✅ internal (default, same module)
    var internalValue: String = "internal"

    // ✅ fileprivate (same file)
    fileprivate var fileOnly: String = "fileOnly"
}
```

## Key Paths

```swift
// ✅ Key paths for type-safe references
struct User {
    let name: String
    let email: String
    let age: Int
}

let nameKeyPath = \User.name
let users = [User(...)]

let names = users.map(\.name)  // [String]

// ✅ With functions
func sort<T>(_ users: [T], by keyPath: KeyPath<T, String>) -> [T] {
    users.sorted { $0[keyPath: keyPath] < $1[keyPath: keyPath] }
}

let sorted = sort(users, by: \.name)
```

---

**Remember**: Swift is designed for safety. Use optionals, type inference, and value types to write robust code.
