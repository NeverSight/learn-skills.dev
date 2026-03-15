---
name: ios-architecture
description: iOS architecture patterns, system design, and project structure guide. Covers MVVM, TCA, Clean Architecture, and scalability strategies for Swift/SwiftUI applications.
license: MIT
metadata:
  author: OkminLee
  version: "2.0.0"
---

# iOS Architecture & System Design

Comprehensive architecture guide for Swift/SwiftUI applications covering patterns, planning, and scalability.

## When to Apply

- Designing or evaluating iOS application architecture
- Choosing between MVVM, TCA, or Clean Architecture
- Planning new features or refactoring existing ones
- Defining module boundaries and data flow
- Scaling an app from MVP to enterprise
- Creating Architecture Decision Records (ADRs)
- Reviewing pull requests for architectural consistency

## Quick Reference

### Core Architecture Principles

| Principle | Description |
|-----------|-------------|
| Single Responsibility | Each component has one reason to change |
| Dependency Inversion | Depend on abstractions (protocols), not concretions |
| Interface Segregation | Small, focused protocols over large ones |
| Testability | Design every layer for easy unit testing |
| Modularity | Clear boundaries between features and layers |

### Layer Diagram

```
┌─────────────────────────────────────────────────────┐
│                  Presentation Layer                  │
│  SwiftUI Views + ViewModels (or TCA Reducers)       │
│  Handles UI rendering and user interaction          │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│                    Domain Layer                      │
│  Use Cases + Entities + Repository Protocols         │
│  Business logic, independent of frameworks           │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│                     Data Layer                       │
│  Repository Implementations + Data Sources           │
│  API clients, local storage, external services       │
└─────────────────────────────────────────────────────┘
```

### iOS-Specific Principles

- **View as a function of State**: Embrace SwiftUI's declarative model
- **Unidirectional Data Flow**: State flows down, actions flow up
- **Actor Isolation**: Use actors and `@MainActor` for thread-safe concurrency
- **Protocol-Oriented Design**: Swift's preferred approach over class inheritance

---

## Key Patterns

### MVVM (Model-View-ViewModel)

Best for small-to-medium apps. ViewModel manages state; View observes it.

```swift
@Observable
final class HomeViewModel {
    private(set) var items: [Item] = []
    private(set) var isLoading = false

    private let useCase: FetchItemsUseCaseProtocol

    init(useCase: FetchItemsUseCaseProtocol) {
        self.useCase = useCase
    }

    @MainActor
    func fetchItems() async {
        isLoading = true
        defer { isLoading = false }
        items = (try? await useCase.execute()) ?? []
    }
}
```

> See [references/mvvm-patterns.md](references/mvvm-patterns.md) for full ViewModel, View, Service, and API Client patterns.

### TCA (The Composable Architecture)

Best for apps requiring strict state management and testability.

```swift
@Reducer
struct HomeFeature {
    @ObservableState
    struct State: Equatable {
        var items: [Item] = []
        var isLoading = false
    }

    enum Action {
        case fetchItems
        case itemsResponse(Result<[Item], Error>)
    }

    var body: some ReducerOf<Self> {
        Reduce { state, action in
            switch action {
            case .fetchItems:
                state.isLoading = true
                return .run { send in
                    let result = await Result { try await fetchItems() }
                    await send(.itemsResponse(result))
                }
            case .itemsResponse(let result):
                state.isLoading = false
                state.items = (try? result.get()) ?? []
                return .none
            }
        }
    }
}
```

> See [references/tca-patterns.md](references/tca-patterns.md) for full Reducer, Coordinator, and composition patterns.

### Repository & UseCase Pattern

Abstracts data sources and encapsulates business logic.

```swift
// Repository: data source abstraction
protocol ItemRepositoryProtocol: Sendable {
    func fetchItems() async throws -> [Item]
    func saveItem(_ item: Item) async throws
}

// UseCase: business logic encapsulation
protocol FetchItemsUseCaseProtocol: Sendable {
    func execute() async throws -> [Item]
}

final class FetchItemsUseCase: FetchItemsUseCaseProtocol {
    private let repository: ItemRepositoryProtocol

    init(repository: ItemRepositoryProtocol) {
        self.repository = repository
    }

    func execute() async throws -> [Item] {
        try await repository.fetchItems()
    }
}
```

> See [references/clean-architecture.md](references/clean-architecture.md) for full Repository, DTO mapping, concurrency, and deep link patterns.

### Navigation (NavigationStack)

Centralized routing with type-safe navigation (iOS 16+).

```swift
@Observable
final class Router {
    var path = NavigationPath()

    func push(_ destination: Destination) {
        path.append(destination)
    }

    func pop() {
        path.removeLast()
    }

    func popToRoot() {
        path.removeLast(path.count)
    }
}

struct ContentView: View {
    @State private var router = Router()

    var body: some View {
        NavigationStack(path: $router.path) {
            HomeView()
                .navigationDestination(for: Destination.self) { dest in
                    destinationView(for: dest)
                }
        }
        .environment(router)
    }
}
```

---

## App Scale Strategy

| Aspect | MVP | Growth | Enterprise |
|--------|-----|--------|------------|
| **File count** | ~50 | ~200 | 500+ |
| **Team size** | 1-2 | 3-5 | 5+ |
| **Architecture** | Single module, basic MVVM | Feature modules, Clean Architecture | Multi-module, micro-features |
| **Testing** | Unit tests for critical paths | Unit + Integration + UI tests | Comprehensive coverage, snapshot tests |
| **Modularization** | None | Feature-based separation begins | SPM-based independent modules |
| **Dependencies** | Minimal, built-in frameworks | Carefully selected third-party | Internal frameworks, strict governance |
| **Build optimization** | N/A | N/A | Incremental builds, caching |

### Choosing Your Architecture

- **MVP / Solo dev**: MVVM is simplest. Avoid over-engineering.
- **Growth / Small team**: Clean Architecture layers + MVVM or TCA. Feature modules.
- **Enterprise / Large team**: TCA or modularized Clean Architecture. SPM modules with clear ownership.

---

## Planning Process

### 1. Requirements Analysis

- Understand the feature request completely
- Identify success criteria and constraints
- Check App Store Guidelines compliance early
- List assumptions and iOS version support requirements

### 2. Architecture Review

- Analyze existing codebase structure (MVVM, TCA, Clean Architecture)
- Identify affected components across layers
- Review similar implementations in the project
- Consider reusable patterns and existing utilities

### 3. Design & Step Breakdown

- Propose architecture changes with module boundaries
- Create detailed steps with file paths and dependencies
- Follow implementation order: **Domain -> Data -> Presentation**
- Group related changes by feature module
- Enable incremental testing at each step

### 4. Trade-off Analysis

- Evaluate alternatives and document pros/cons
- Consider long-term maintainability vs. implementation complexity
- Document decisions in ADRs

> See [references/project-structure.md](references/project-structure.md) for ADR templates, planning checklists, and project structure guides.

---

## References

- [MVVM Patterns](references/mvvm-patterns.md) - Full MVVM pattern with ViewModel, View, Service, API Client, DI, and state management
- [TCA Patterns](references/tca-patterns.md) - The Composable Architecture with Reducer, Coordinator, and composition patterns
- [Clean Architecture](references/clean-architecture.md) - Repository, UseCase, DTO mapping, concurrency, and deep link patterns
- [Project Structure](references/project-structure.md) - File structure, naming conventions, testing, deployment, ADRs, and App Store checklists

---

## Common Mistakes

### 1. God ViewModel

A single ViewModel that manages state for an entire screen with dozens of properties and methods. Break it into smaller, focused ViewModels or use child reducers in TCA.

### 2. Business Logic in Views

Placing networking, data transformation, or validation directly inside SwiftUI `body`. Views should only describe UI; delegate logic to ViewModels or UseCases.

### 3. Tight Coupling Between Modules

Feature modules importing each other directly instead of communicating through protocols or a coordinator. This prevents independent development and testing.

### 4. Shared Mutable State Without Actor Isolation

Accessing shared state from multiple threads without using `actor`, `@MainActor`, or other synchronization. This causes data races that are hard to reproduce and debug.

### 5. Over-Engineering for Scale Not Yet Needed

Building full micro-feature architecture with SPM modules for a 20-screen MVP. Match architecture complexity to actual team size and app scale. Start simple, refactor when growth demands it.

---

## Critical Rules

1. **No force unwrapping** in production code
2. **All UI updates** on `@MainActor`
3. **Protocols for all dependencies** to enable testing and DI
4. **No hardcoded strings** - use `Localizable.strings` or String Catalogs
5. **Accessibility identifiers** on all interactive elements
6. **80%+ test coverage** minimum for ViewModels and Services
7. **No `print` statements** in production - use `os.Logger`
8. **Keychain for sensitive data** - never UserDefaults
