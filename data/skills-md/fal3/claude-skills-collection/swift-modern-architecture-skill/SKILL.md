---
name: swift-modern-architecture-skill
description: Guide for building iOS apps using Swift 6, iOS 18+, SwiftUI, SwiftData, and modern concurrency patterns. Use when writing Swift/iOS code, designing app architecture, or modernizing legacy patterns. Prevents outdated patterns like Core Data, ObservableObject, DispatchQueue, and NavigationView.
---

# Swift Modern Architecture Skill

Build iOS apps using Swift 6 and iOS 18+ best practices. This skill ensures code uses modern patterns: SwiftData (not Core Data), Observation framework (not Combine), Swift concurrency (not GCD), and current SwiftUI APIs.

## Core Principles

### 1. Swift 6 Concurrency First
Always use Swift concurrency (`async/await`, `actor`, `@MainActor`) instead of GCD or completion handlers. Use structured concurrency (`TaskGroup`, `async let`) over unstructured tasks.

### 2. Observation Framework Over Combine
Use `@Observable` macro for state management instead of `ObservableObject` with `@Published`. The Observation framework is more efficient and has cleaner syntax.

### 3. SwiftData Over Core Data
For new projects, always use SwiftData with `@Model` and `@Query`. SwiftData provides simpler APIs while maintaining Core Data's power.

### 4. Modern SwiftUI APIs
Use `NavigationStack` (not `NavigationView`), `@Entry` for environment values, `.task` modifier for async work, and built-in components like `ContentUnavailableView`.

### 5. Type Safety
Use enums instead of strings for identifiers, typed throws for specific errors, and proper `Sendable` conformance for thread safety.

### 6. Value Types When Possible
Prefer structs and enums over classes unless reference semantics are required. Use `actor` for thread-safe shared mutable state.

## When to Use This Skill

Activate this skill when:
- Writing Swift or iOS application code
- Designing application architecture
- Reviewing or modernizing existing Swift code
- Setting up SwiftUI views, view models, or data models
- Implementing networking, persistence, or business logic
- Working with async operations or concurrency

## Architecture Pattern: MVVM with Observation

### View Model Structure
```swift
@Observable
final class ViewModel {
    // Private dependencies
    private let service: ServiceProtocol
    
    // Public readable state
    private(set) var data: [Item] = []
    private(set) var isLoading = false
    private(set) var error: Error?
    
    // User input state (use @Bindable in view)
    var searchText = ""
    var selectedFilter: Filter = .all
    
    init(service: ServiceProtocol) {
        self.service = service
    }
    
    // Public actions
    func loadData() async {
        isLoading = true
        defer { isLoading = false }
        
        do {
            data = try await service.fetchData()
        } catch {
            self.error = error
        }
    }
}
```

### View Structure
```swift
struct ContentView: View {
    @Bindable var viewModel: ViewModel
    
    var body: some View {
        content
            .task { await viewModel.loadData() }
    }
    
    @ViewBuilder
    private var content: some View {
        if viewModel.isLoading {
            ProgressView()
        } else {
            List(viewModel.data) { item in
                ItemRow(item: item)
            }
        }
    }
}
```

## SwiftData Quick Reference

### Model Definition
```swift
import SwiftData

@Model
final class Item {
    var name: String
    var createdAt: Date
    @Relationship(deleteRule: .cascade) var children: [ChildItem]
    
    init(name: String) {
        self.name = name
        self.createdAt = Date()
        self.children = []
    }
}
```

### Querying Data
```swift
// In SwiftUI view
@Query(sort: \Item.createdAt, order: .reverse) 
private var items: [Item]

// With filter
@Query(filter: #Predicate<Item> { $0.isComplete }) 
private var completedItems: [Item]

// With dynamic predicate
@Query private var items: [Item]

init(searchText: String) {
    let predicate = #Predicate<Item> { item in
        searchText.isEmpty || item.name.contains(searchText)
    }
    _items = Query(filter: predicate)
}
```

### Model Context Operations
```swift
@Environment(\.modelContext) private var modelContext

func addItem() {
    let item = Item(name: "New")
    modelContext.insert(item)
    try? modelContext.save()
}

func deleteItem(_ item: Item) {
    modelContext.delete(item)
    try? modelContext.save()
}
```

## API Client Pattern

Create an `actor` for thread-safe API operations:

```swift
actor APIClient {
    private let session: URLSession
    private let decoder: JSONDecoder
    
    init(session: URLSession = .shared) {
        self.session = session
        self.decoder = JSONDecoder()
    }
    
    func fetch<T: Decodable>(_ endpoint: Endpoint) async throws -> T {
        let (data, response) = try await session.data(for: endpoint.urlRequest)
        
        guard let httpResponse = response as? HTTPURLResponse,
              (200...299).contains(httpResponse.statusCode) else {
            throw APIError.invalidResponse
        }
        
        return try decoder.decode(T.self, from: data)
    }
}
```

## Navigation Pattern

Use type-safe navigation with `NavigationStack`:

```swift
struct AppView: View {
    @State private var path = NavigationPath()
    
    var body: some View {
        NavigationStack(path: $path) {
            RootView()
                .navigationDestination(for: Item.self) { item in
                    ItemDetailView(item: item)
                }
                .navigationDestination(for: User.self) { user in
                    UserProfileView(user: user)
                }
        }
    }
}
```

## Testing with Swift Testing

Use the modern Swift Testing framework instead of XCTest:

```swift
import Testing

@Test("View model loads data successfully")
func dataLoading() async throws {
    let viewModel = ViewModel(service: MockService())
    await viewModel.loadData()
    #expect(viewModel.data.isEmpty == false)
}

@Test("Validation fails with invalid input", arguments: [
    "invalid-email",
    "missing@",
    "@domain.com"
])
func emailValidation(invalidEmail: String) throws {
    #expect(throws: ValidationError.self) {
        try validateEmail(invalidEmail)
    }
}
```

## Common Modernization Checks

Before writing code, verify you're using:
- ✅ `@Observable` NOT `ObservableObject`
- ✅ `@Query` NOT `@FetchRequest`
- ✅ `NavigationStack` NOT `NavigationView`
- ✅ `async/await` NOT completion handlers
- ✅ `@MainActor` NOT `DispatchQueue.main.async`
- ✅ `actor` NOT serial `DispatchQueue`
- ✅ `SwiftData.ModelContext` NOT `NSManagedObjectContext`
- ✅ Swift Testing `@Test` NOT XCTest
- ✅ Typed `throws(ErrorType)` when appropriate

## Bundled Resources

### References
Load when you need detailed guidance:

- **modern-patterns.md** - Comprehensive patterns for Swift 6/iOS 18+
  - Load when: Implementing any feature, especially concurrency, data persistence, or API calls
  
- **anti-patterns.md** - What NOT to do and why
  - Load when: Reviewing code, modernizing legacy patterns, or unsure about approach
  
- **examples.md** - Complete working implementations
  - Load when: Starting new features (Todo app, Weather app, Auth flow examples)

### Usage Pattern
1. Read the relevant reference file before implementing complex features
2. Check anti-patterns when reviewing existing code
3. Reference complete examples when starting new app components

## Quick Decision Tree

**Need state management?**
→ Use `@Observable` for view models
→ Use `@State` for simple view-local state
→ Use `@Environment` for dependency injection

**Need data persistence?**
→ Use SwiftData with `@Model` and `@Query`
→ Never use Core Data for new code

**Need async operations?**
→ Use `async/await` and structured concurrency
→ Mark UI-bound code with `@MainActor`
→ Use `actor` for thread-safe shared state

**Need navigation?**
→ Use `NavigationStack` with `NavigationPath`
→ Type-safe destinations with `.navigationDestination(for:)`

**Need API calls?**
→ Create an `actor` with `async throws` methods
→ Use `URLSession.data(from:)` with async/await

## Error Prevention

This skill actively prevents these outdated patterns:
- Core Data (`NSManagedObject`, `@FetchRequest`)
- Combine (`ObservableObject`, `@Published`, `.sink`)
- GCD (`DispatchQueue`, `DispatchGroup`)
- Old SwiftUI (`NavigationView`, `NavigationLink(destination:)`)
- Manual threading (`Thread`, `NSOperationQueue`)
- Completion handlers when `async/await` is available
- XCTest when Swift Testing is more appropriate

When encountering these patterns in existing code, suggest modern alternatives from the references.
