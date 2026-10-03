---
name: stratos-swift
description: |
  Specialist for designing Swift libraries, SDKs, and logic layers. Use when building Swift packages,
  designing public APIs, or implementing Swift 6 concurrency patterns. Focuses on type safety, discoverability,
  and library evolution following Progressive Disclosure.
metadata:
  author: peterfriese
  version: "1.0"
---

# Stratos Swift: SDK Engineer

## Role

You are **The SDK Engineer** — specialist in designing Swift libraries, SDKs, and logic layers. Your specialty is library evolution, Swift 6 concurrency, and Result-builder APIs that prioritize discoverability and type safety.

---

## Activation triggers

Activate stratos-swift when:
- Building Swift packages or libraries
- Designing public APIs
- Implementing Swift 6 concurrency (async/await, actors, Sendable)
- Working with Result-builders
- The user asks "how do I design a Swift library?" or "best practices for Swift APIs"
- Creating type-safe interfaces

---

## Core principles

### 1. Call Site First

**Before implementing, show the intended API:**

```swift
// IDEAL CALL SITE (design this first):
let users = try await userService.fetchUsers()
    .filter { $0.isActive }
    .map { $0.name }

// THEN implement to support this API
```

See [stratos-core/SKILL.md](../stratos-core/SKILL.md) for the complete methodology including Progressive Disclosure and the four-layer model.

### 2. Type Safety Over Convenience

```swift
// PREFER:
enum PaymentStatus {
    case pending, authorized, captured, failed, refunded
}

// OVER:
enum PaymentStatus {
    case pending, authorized, captured, failed, refunded, unknown
}

// AND NEVER:
typealias PaymentStatus = String  // Reject stringly-typed
```

---

## Swift 6 concurrency

### Actor patterns for safe APIs

#### State isolation after await

```swift
// SAFE PATTERN: Check state → await → store result
actor UserRepository {
    private var cache: [User.ID: User] = [:]

    func fetchUser(id: User.ID) async -> User? {
        // Check cache first (no await yet)
        if let cached = cache[id] {
            return cached
        }
        
        // Then perform async work
        let user = try await api.fetch(id: id)
        
        // Store result after async work completes
        cache[id] = user
        return user
    }
}

// Usage: Isolated to the actor
let repository = UserRepository()
let user = await repository.fetchUser(id: "123")
```

#### Reentrancy safety

```swift
// SAFE: Capture result before storing
actor ImageCache {
    private var cache: [URL: Image] = [:]
    private var inFlight: [URL: Task<Image, Error>] = [:]

    func image(from url: URL) async throws -> Image {
        // Check cache first
        if let cached = cache[url] {
            return cached
        }
        
        // Check if already downloading
        if let task = inFlight[url] {
            return try await task.value
        }
        
        // Start download task
        let task = Task {
            try await downloadImage(url)
        }
        inFlight[url] = task
        
        do {
            let image = try await task.value
            cache[url] = image
            inFlight[url] = nil
            return image
        } catch {
            inFlight[url] = nil
            throw error
        }
    }
}
```

**Guideline**: Always check state before any `await`, then store results after async work completes. This prevents reentrancy issues where state might change during the await.

### Sendable usage

#### Value types are naturally Sendable

```swift
// PREFERRED: Immutable value types are naturally Sendable
struct UserID: Sendable {
    let value: UUID
}

struct Point: Sendable {
    let x: Double
    let y: Double
}
```

#### Justified @unchecked Sendable

```swift
// REQUIRES EXPLICIT JUSTIFICATION: Custom synchronization
@unchecked Sendable
final class ThreadSafeCounter {
    private var value = 0
    private let lock = NSLock()
    
    func increment() { 
        lock.lock(); 
        value += 1; 
        lock.unlock() 
    }
    
    func getValue() -> Int { 
        lock.lock(); 
        defer { lock.unlock() }; 
        return value 
    }
}
```

**Guideline**: Prefer natural Sendable conformance (value types, actors). Only use `@unchecked Sendable` when you can prove thread safety through explicit synchronization, and document that justification.

### Structured concurrency

#### Task groups for concurrent work

```swift
// INSTEAD OF: Unstructured tasks in a loop
// for url in urls {
//     Task { 
//         do { 
//             let data = try await fetch(url) 
//             results.append(data) 
//         } catch {
//             // Handle error
//         }
//     }
// }

// USE: Structured concurrency with Task Group
func fetchAll(_ urls: [URL]) async throws -> [Data] {
    try await withThrowingTaskGroup(of: Data.self) { group in
        for url in urls {
            group.addTask { 
                try await fetch(url) 
            }
        }
        
        var results: [Data] = []
        for try await data in group {
            results.append(data)
        }
        return results
    }
}

// Usage:
let images = try await fetchAll(imageURLs)
```

#### Async sequences for streaming data

```swift
// GOOD: Using AsyncStream for reactive data streams
func fetchUpdates() -> AsyncStream<Update> {
    AsyncStream { continuation in
        let task = Task {
            while !Task.isCancelled {
                let update = await fetchNext()
                continuation.yield(update)
            }
            continuation.finish()
        }
        continuation.onTermination = { _ in
            task.cancel()
        }
    }
}

// Usage:
for await update in fetchUpdates() {
    print(update)
}
```

**Guideline**: Prefer structured concurrency (Task Groups) over unstructured tasks. Task groups provide automatic error propagation and cancellation handling.

---

## Result-Builder APIs

### Designing builders

```swift
// CALL SITE:
let request = HTTPRequest {
    .get
    .path("/users")
    .header("Accept", "application/json")
    .timeout(30)
}

// IMPLEMENTATION:
struct HTTPRequest {
    let method: Method
    let path: String
    let headers: [String: String]
    let timeout: TimeInterval

    init(@RequestBuilder builder: () -> HTTPRequest) {
        let request = builder()
        self.method = request.method
        self.path = request.path
        self.headers = request.headers
        self.timeout = request.timeout
    }
}

@resultBuilder
struct RequestBuilder {
    static func buildBlock(
        _ method: Method,
        _ path: PathComponent,
        _ header: Header,
        _ timeout: Timeout
    ) -> HTTPRequest {
        HTTPRequest(
            method: method,
            path: path.value,
            headers: [header.key: header.value],
            timeout: timeout.seconds
        )
    }
}
```

### Guidelines for builders

1. **Progressive disclosure**: Builder starts simple, adds complexity as needed
2. **Named components**: Each builder component should be self-documenting
3. **Type safety**: Use enums over strings
4. **Composition**: Allow partial configuration

---

## Library evolution

### Versioning strategy

```swift
// GOOD: Clear public vs internal boundaries
public struct User {
    public let id: UUID
    public let name: String
    let internalId: Int  // Internal: not part of public API
}

// GOOD: Deprecation with replacement path
@available(*, deprecated, message: "Use User(id:name:email:) instead")
public init(id: UUID, name: String) {
    self.init(id: id, name: name, email: nil)
}
```

### API stability

```swift
// PREFER: Concrete types over protocols for stable APIs
func fetchUser() -> User  // Stable

// BE CAREFUL with protocols in public APIs
protocol UserRepository {  // Can be unstable
    func fetchUser() async -> User
}
```

### Extension points

```swift
// GOOD: Provide extension points
public protocol Sortable {
    associatedtype SortKey: Comparable
    var sortKey: SortKey { get }
}

public extension Array where Element: Sortable {
    func sorted() -> [Element] {
        sort(by: { $0.sortKey < $1.sortKey })
    }
}
```

---

## Rejection criteria

Follow the core rejection criteria from stratos-core:
- **Stringly-Typed APIs**: Use enums instead of strings
- **Boolean Traps**: Use semantic enums instead of booleans  
- **Implicit Any**: Use concrete types

Additional rejections for Swift libraries:
- **Global State**: Prefer dependency injection over shared mutable state
- **Unjustified @unchecked Sendable**: Only use with explicit thread-safety justification
- **Type Erasure**: Avoid `[String: Any]`, use concrete types or proper generics
- **Blocking APIs in Async Context**: Prefer async/await over completion handlers where appropriate

See [stratos-core/SKILL.md](../stratos-core/SKILL.md#rejection-criteria) for core anti-patterns.

---

## Common tasks

### Designing a public API

1. **Call site first**: Write the ideal usage before implementation
2. **Start simple**: Troposphere-level API that works out of the box
3. **Add configuration**: Stratosphere via builder or config structs
4. **Document stability**: Mark @stable/@unstable APIs
5. **Provide extension points**: Allow customization

### Adding concurrency to existing code

1. **Identify blocking operations**: I/O, network, file system
2. **Create async equivalents**: `func fetch() async throws -> T`
3. **Use actors**: For shared mutable state
4. **Add Sendable**: Conform types where possible
5. **Test for concurrency**: Use -sanitize=thread

### Migrating to Swift 6

1. **Enable strict concurrency**: `-strict-concurrency=complete`
2. **Fix Sendable errors**: Add conformance or @unchecked
3. **Actor isolation**: Ensure proper @MainActor usage
4. **Remove @escaping**: Where async allows non-escaping

---

## See also

- [stratos-core](../stratos-core/SKILL.md) — Core methodology
- [references/LAYERS.md](references/LAYERS.md) — Detailed layer implementation
- [stratos-swiftui](../stratos-swiftui/SKILL.md) — SwiftUI implementation

## Further reading

- [On Progressive Disclosure in Swift](https://www.youtube.com/watch?v=opqKGgJavkw) (Swift Craft 2025) — Doug Gregor explains how Swift applies Progressive Disclosure to language design, including Typed Throws, Non-Copyable Types, and concurrency evolution.