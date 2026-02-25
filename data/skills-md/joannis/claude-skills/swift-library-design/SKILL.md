---
name: swift-library-design
description: 'Expert guidance on Swift library and framework design. Use when developers mention: (1) designing a Swift library or framework, (2) public API design patterns, (3) protocol-oriented architecture or associated types, (4) result builders or DSL design, (5) performance optimization for libraries, (6) @inlinable or @usableFromInline, (7) noncopyable types for APIs, (8) progressive disclosure in API design, (9) ResponseGenerator or builder patterns.'
---

# Swift Library Design

Patterns and best practices for designing high-quality Swift libraries and frameworks.

## Core Principles

### 1. Protocol-Oriented Design
Design around protocols with associated types for flexibility and testability. Use generics for type safety with runtime polymorphism.

### 2. Compile-Time Safety
Leverage Swift's type system to catch errors at compile time. Use noncopyable types, generics, and protocol constraints to make invalid states unrepresentable.

### 3. Performance by Default
Design APIs that are efficient by default. Use `@inlinable` for hot paths, avoid unnecessary allocations, and provide zero-copy options.

### 4. Progressive Disclosure
Simple things should be simple, complex things should be possible. Provide sensible defaults while allowing customization.

## Key Patterns

### Protocol with Associated Types

```swift
public protocol Handler<Context>: Sendable {
    associatedtype Context
    func handle(input: Input, context: Context) async throws -> Output
}

// Consumers accept any conforming type
public struct Pipeline<Context> {
    public func add<H: Handler>(handler: H) where H.Context == Context {
        // Type-safe composition
    }
}
```

### ResponseGenerator Pattern

Allow multiple return types with automatic conversion:

```swift
public protocol ResponseGenerator: Sendable {
    func response(from request: Request, context: some RequestContext) throws -> Response
}

// Extend standard types
extension String: ResponseGenerator {
    public func response(from request: Request, context: some RequestContext) -> Response {
        Response(status: .ok, body: .init(string: self))
    }
}

extension HTTPResponse.Status: ResponseGenerator {
    public func response(from request: Request, context: some RequestContext) -> Response {
        Response(status: self)
    }
}
```

### Result Builder for DSLs

```swift
@resultBuilder
public enum PipelineBuilder<Context> {
    public static func buildExpression<M: Middleware>(_ m: M) -> M
        where M.Context == Context { m }

    public static func buildPartialBlock<M0: Middleware, M1: Middleware>(
        accumulated m0: M0, next m1: M1
    ) -> CombinedMiddleware<M0, M1> {
        CombinedMiddleware(m0, m1)
    }
}

// Usage
let pipeline = PipelineBuilder {
    LoggingMiddleware()
    AuthMiddleware()
    RateLimitMiddleware()
}
```

### Static Builder Methods

```swift
public struct ServerBuilder: Sendable {
    private let build: @Sendable () throws -> Server

    public static func http1(config: HTTP1Config = .init()) -> ServerBuilder {
        .init { HTTP1Server(config: config) }
    }

    public static func http2(tlsConfig: TLSConfiguration) -> ServerBuilder {
        .init { HTTP2Server(tlsConfig: tlsConfig) }
    }
}

// Fluent usage
let server = Application(server: .http1(config: .init(idleTimeout: .seconds(30))))
```

## Reference Files

- **`references/api-patterns.md`** - Protocol design, result builders, builder pattern, error handling, parameter extraction
- **`references/performance.md`** - Inlining, noncopyable types, data structures, lock-free patterns, state machines
