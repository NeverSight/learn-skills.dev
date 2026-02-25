---
name: swift-concurrency
description: 'Expert guidance on Swift Concurrency best practices, patterns, and implementation. Use when developers mention: (1) Swift Concurrency, async/await, actors, or tasks, (2) modern concurrency patterns or structured concurrency, (3) migrating to Swift 6 or strict concurrency checking, (4) data races or thread safety issues, (5) refactoring closures to async/await, (6) @MainActor, Sendable, or actor isolation, (7) concurrent code architecture or performance, (8) concurrency-related linter warnings, (9) AsyncSequence, AsyncStream, or task groups, (10) nonisolated, @preconcurrency, or @unchecked Sendable.'
---
# Swift Concurrency

## Overview

This skill provides expert guidance on Swift Concurrency, covering modern async/await patterns, actors, tasks, Sendable conformance, and migration to Swift 6. Use this skill to help developers write safe, performant concurrent code and navigate the complexities of Swift's structured concurrency model.

## Agent Behavior Contract (Follow These Rules)

1. Analyze the project/package file to find out which Swift language mode (Swift 5.x vs Swift 6) and which Xcode/Swift toolchain is used when advice depends on it.
2. Before proposing fixes, identify the isolation boundary: `@MainActor`, custom actor, actor instance isolation, or nonisolated.
3. Do not recommend `@MainActor` as a blanket fix. Justify why main-actor isolation is correct for the code.
4. Prefer structured concurrency (child tasks, task groups) over unstructured tasks. Use `Task.detached` only with a clear reason.
5. If recommending `@preconcurrency`, `@unchecked Sendable`, or `nonisolated(unsafe)`, require:
   - a documented safety invariant
   - a follow-up ticket to remove or migrate it
6. For migration work, optimize for minimal blast radius (small, reviewable changes) and add verification steps.

## Project Settings Intake (Evaluate Before Advising)

Concurrency behavior depends on build settings. Always try to determine:

- Default actor isolation (is the module default `@MainActor` or `nonisolated`?)
- Strict concurrency checking level (minimal/targeted/complete)
- Whether upcoming features are enabled (especially `NonisolatedNonsendingByDefault`)
- Swift language mode (Swift 5.x vs Swift 6) and diSwiftPM tools version

### Manual checks (no scripts)

- SwiftPM:
  - Check `Package.swift` for `.defaultIsolation(MainActor.self)`.
  - Check `Package.swift` for `.enableUpcomingFeature("NonisolatedNonsendingByDefault")`.
  - Check for strict concurrency flags: `.enableExperimentalFeature("StrictConcurrency=targeted")` (or similar).
  - Check tools version at the top: `// swift-tools-version: ...`
- Xcode projects:
  - Search `project.pbxproj` for:
    - `SWIFT_DEFAULT_ACTOR_ISOLATION`
    - `SWIFT_STRICT_CONCURRENCY`
    - `SWIFT_UPCOMING_FEATURE_` (and/or `SWIFT_ENABLE_EXPERIMENTAL_FEATURES`)

If any of these are unknown, ask the developer to confirm them before giving migration-sensitive guidance.

## Quick Decision Tree

When a developer needs concurrency guidance, follow this decision tree:

1. **Starting fresh with async code?**
   - Read `references/async-await-basics.md` for foundational patterns
   - For parallel operations → `references/tasks.md` (async let, task groups)

2. **Protecting shared mutable state?**
   - Need to protect class-based state → `references/actors.md` (actors, @MainActor)
   - Need thread-safe value passing → `references/sendable.md` (Sendable conformance)

3. **Managing async operations?**
   - Structured async work → `references/tasks.md` (Task, child tasks, cancellation)
   - Streaming data → `references/async-sequences.md` (AsyncSequence, AsyncStream)

4. **Performance or debugging issues?**
   - Slow async code → `references/performance.md` (profiling, suspension points)
   - Testing concerns → `references/testing.md` (XCTest, Swift Testing)

## Triage-First Playbook (Common Errors -> Next Best Move)

- SwiftLint concurrency-related warnings
  - Use `references/linting.md` for rule intent and preferred fixes; avoid dummy awaits as “fixes”.
- SwiftLint `async_without_await` warning
  - Remove `async` if not required; if required by protocol/override/@concurrent, prefer narrow suppression over adding fake awaits. See `references/linting.md`.
- "Sending value of non-Sendable type ... risks causing data races"
  - First: identify where the value crosses an isolation boundary
  - Then: use `references/sendable.md` and `references/threading.md` (especially Swift 6.2 behavior changes)
- "Main actor-isolated ... cannot be used from a nonisolated context"
  - First: decide if it truly belongs on `@MainActor`
  - Then: use `references/actors.md` (global actors, `nonisolated`, isolated parameters) and `references/threading.md` (default isolation)
- "Class property 'current' is unavailable from asynchronous contexts" (Thread APIs)
  - Use `references/threading.md` to avoid thread-centric debugging and rely on isolation + Instruments
- XCTest async errors like "wait(...) is unavailable from asynchronous contexts"
  - Use `references/testing.md` (`await fulfillment(of:)` and Swift Testing patterns)
- Core Data concurrency warnings/errors
  - Use `references/core-data.md` (DAO/`NSManagedObjectID`, default isolation conflicts)

## Core Patterns Reference

### When to Use Each Concurrency Tool

**async/await** - Making existing synchronous code asynchronous
```swift
// Use for: Single asynchronous operations
func fetchUser() async throws -> User {
    try await networkClient.get("/user")
}
```

**async let** - Running multiple independent async operations in parallel
```swift
// Use for: Fixed number of parallel operations known at compile time
async let user = fetchUser()
async let posts = fetchPosts()
let profile = try await (user, posts)
```

**Task Group** - Dynamic parallel operations with structured concurrency
```swift
// Use for: Unknown number of parallel operations at compile time
await withTaskGroup(of: Result.self) { group in
    for item in items {
        group.addTask { await process(item) }
    }
}
```

**Actor** - Protecting mutable state from data races
```swift
// Use for: Shared mutable state accessed from multiple contexts
actor DataCache {
    private var cache: [String: Data] = [:]
    func get(_ key: String) -> Data? { cache[key] }
}
```

**@MainActor** - Ensuring UI updates on main thread
```swift
// Use for: View models, UI-related classes
@MainActor
class ViewModel: ObservableObject {
    @Published var data: String = ""
}
```

### Common Scenarios

**Scenario: Multiple parallel network requests**
```swift
async let users = fetchUsers()
async let posts = fetchPosts()
async let comments = fetchComments()
let (u, p, c) = try await (users, posts, comments)
```

**Scenario: Processing array items in parallel**
```swift
await withTaskGroup(of: ProcessedItem.self) { group in
    for item in items {
        group.addTask { await process(item) }
    }
    for await result in group {
        results.append(result)
    }
}
```

## Swift 6 Migration Quick Guide

Key changes in Swift 6:
- **Strict concurrency checking** enabled by default
- **Complete data-race safety** at compile time
- **Sendable requirements** enforced on boundaries
- **Isolation checking** for all async boundaries

For detailed migration steps, see `references/migration.md`.

## Reference Files

Load these files as needed for specific topics:

- **`async-await-basics.md`** - async/await syntax, execution order, async let, URLSession patterns
- **`tasks.md`** - Task lifecycle, cancellation, priorities, task groups, structured vs unstructured
- **`threading.md`** - Thread/task relationship, suspension points, isolation domains, nonisolated
- **`actors.md`** - Actor isolation, @MainActor, global actors, reentrancy, custom executors, Mutex
- **`sendable.md`** - Sendable conformance, value/reference types, @unchecked, region isolation
- **`async-sequences.md`** - AsyncSequence, AsyncStream, when to use vs regular async methods
- **`performance.md`** - Profiling with Instruments, reducing suspension points, execution strategies
- **`testing.md`** - XCTest async patterns, Swift Testing, concurrency testing utilities
- **`production-patterns.md`** - Advanced patterns: actor state machines, ~Copyable state, structured concurrency, lock-free atomics, service lifecycle

## Best Practices Summary

1. **Prefer structured concurrency** - Use task groups over unstructured tasks when possible
2. **Minimize suspension points** - Keep actor-isolated sections small to reduce context switches
3. **Use @MainActor judiciously** - Only for truly UI-related code
4. **Make types Sendable** - Enable safe concurrent access by conforming to Sendable
5. **Handle cancellation** - Check Task.isCancelled in long-running operations
6. **Avoid blocking** - Never use semaphores or locks in async contexts
7. **Test concurrent code** - Use proper async test methods and consider timing issues

### Use Structured Concurrency for Resource Management

When managing resources that need cleanup (connections, file handles, etc.), use the `withX` pattern to ensure proper cleanup through structured concurrency.

**Bad - Unstructured cleanup:**
```swift
func withConnection<R>(
    _ body: (Connection) async throws -> R
) async throws -> R {
    let connection = Connection()
    try await connection.connect()
    defer {
        Task {
            await connection.disconnect()  // Unstructured! May not complete
        }
    }
    return try await body(connection)
}
```

**Better - Explicit cleanup in all paths:**
```swift
func withConnection<R>(
    _ body: (Connection) async throws -> R
) async throws -> R {
    let connection = Connection()
    try await connection.connect()
    do {
        let result = try await body(connection)
        await connection.disconnect()
        return result
    } catch {
        await connection.disconnect()
        throw error
    }
}
```

**Best - Make the pattern impossible to misuse:**
```swift
actor Client {
    private let connection: Connection  // Non-optional, always valid

    private init(connection: Connection) {
        self.connection = connection
    }

    static func withConnection<R>(
        _ body: (Client) async throws -> R
    ) async throws -> R {
        let connection = try await Connection.establish()
        let client = Client(connection: connection)
        do {
            let result = try await body(client)
            await connection.close()
            return result
        } catch {
            await connection.close()
            throw error
        }
    }

    // No public connect()/disconnect() methods - can't forget cleanup
}
```

This pattern:
- Makes the initializer private so users must go through `withConnection`
- Stores resources as non-optional properties (no guard-let needed)
- Guarantees cleanup happens before the function returns
- Eliminates `notConnected` error cases entirely

### Swift 6 Strict Concurrency with Global Mutable State

When accessing C globals like `stdout` in Swift 6 strict concurrency mode, use a **local** `nonisolated(unsafe)` variable:

```swift
@inline(__always)
private func flushStdout() {
    nonisolated(unsafe) let out = stdout
    fflush(out)
}
```

The `nonisolated(unsafe)` annotation tells the compiler to skip concurrency checking for this specific access to the C global.

### ThrowingDiscardingTaskGroup for Fire-and-Forget Tasks

Use `withThrowingDiscardingTaskGroup` when you need to spawn multiple tasks but don't need to collect their individual results:

```swift
try await withThrowingDiscardingTaskGroup { taskGroup in
    taskGroup.addTask {
        try await handleClient(client1)
    }
    taskGroup.addTask {
        try await handleClient(client2)
    }
}
```

### Graceful Shutdown Patterns

Check for both cancellation and graceful shutdown in long-running loops:

```swift
while !Task.isShuttingDownGracefully && !Task.isCancelled {
    try await handle(value)
}

// Use gracefulShutdown() for clean termination
try await gracefulShutdown()
```

### AsyncStream: Avoid When Possible

**AsyncStream has no backpressure.** If the producer yields faster than the consumer processes, values accumulate in an unbounded buffer, leading to memory growth.

**Prefer mapping NIOAsyncSequence** or other backpressured sequences instead:

```swift
// Bad - no backpressure, unbounded buffer
let stream = AsyncStream<Message> { continuation in
    Task {
        for await rawMessage in nioChannel.inbound {
            continuation.yield(Message(rawMessage))
        }
        continuation.finish()
    }
}

// Good - preserves backpressure from NIO
let messages = nioChannel.inbound.map { Message($0) }
for try await message in messages {
    process(message)
}
```

If you must use AsyncStream, use structured concurrency with `makeStream()`:

```swift
func run() async {
    let (stream, continuation) = AsyncStream<Value>.makeStream()

    async let producer: Void = runProducer(continuation: continuation)

    for await value in stream {
        process(value)
    }

    await producer
}

private func runProducer(
    continuation: sending AsyncStream<Value>.Continuation
) async {
    let cont = consume continuation  // Transfer ownership

    try? await withThrowingDiscardingTaskGroup { group in
        group.addTask {
            while !Task.isCancelled {
                cont.yield(produceValue())
                try await Task.sleep(for: .seconds(1))
            }
        }
    }

    cont.finish()
}
```

Key points:
- `sending` parameter transfers ownership into the function
- `consume continuation` allows safe sharing across task group children
- `AsyncStream.Continuation` is `Sendable` - no need for `nonisolated(unsafe)`
- Avoid `Task { }` inside `AsyncStream.init` - it's unstructured concurrency

## Verification Checklist (When You Change Concurrency Code)

- Confirm build settings (default isolation, strict concurrency, upcoming features) before interpreting diagnostics.
- After refactors:
  - Run tests, especially concurrency-sensitive ones (see `references/testing.md`).
  - If performance-related, verify with Instruments (see `references/performance.md`).
  - If lifetime-related, verify that the code is structured correctly, using `with`-style APIs.

## Glossary

See `references/glossary.md` for quick definitions of core concurrency terms used across this skill.