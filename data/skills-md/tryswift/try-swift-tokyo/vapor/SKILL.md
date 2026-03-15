---
name: vapor
description: Expert guidance for Vapor 4+ development, focusing on async/await, Fluent, and content negotiation.
---

# Vapor Best Practices

## 1. Concurrency

- ALWAYS use Swift Concurrency (`async`/`await`) over `EventLoopFuture`.
- Use `req.application.asyncController` patterns if using custom executors, but standard `async` route handlers are preferred.

## 2. Controllers & Routing

- Organize routes into `RouteCollection` conformances.
- Do not put logic in `routes.swift`; delegate immediately to a Controller.
- Group routes by feature (e.g., `UsersController`, `AuthController`).

## 3. Fluent (Database)

- Use `@Parent` and `@Children` property wrappers correctly.
- Always use `DTOs` (Data Transfer Objects) implementation `Content` for API requests/responses. NEVER return a Fluent Model directly to the client.
- Run migrations via `app.migrations.add(...)`.

## 4. Environment

- Use `Environment.get("KEY")` for configuration.
- Support `Production` vs `Development` modes explicitly in `configure.swift`.

## Example Route

```swift
func boot(routes: RoutesBuilder) throws {
    let users = routes.grouped("users")
    users.get(use: index)
}

@Sendable
func index(req: Request) async throws -> [UserDTO] {
    let users = try await User.query(on: req.db).all()
    return users.map { $0.toDTO() }
}
