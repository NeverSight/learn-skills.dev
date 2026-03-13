---
name: vapor-fluent
description: Guide for using Vapor's Fluent ORM framework in Swift server-side applications
---

# Vapor Fluent ORM

Fluent is an ORM framework for Swift used with the Vapor web framework. It leverages Swift's strong type system to provide a type-safe interface for database operations. Instead of writing raw queries, you define model types that represent database structures and use them for CRUD operations.

## When to use

Use this skill when:
- Setting up Fluent in a new or existing Vapor project
- Defining database models with property wrappers (`@ID`, `@Field`, `@Parent`, `@Children`, etc.)
- Writing database migrations
- Performing CRUD operations (create, read, update, delete)
- Setting up relations between models (one-to-many, many-to-many)
- Querying the database with Fluent's query builder
- Configuring database drivers (PostgreSQL, SQLite, MySQL, MongoDB)

## Instructions

### 1. Add Dependencies

For a new project, use `vapor new` and answer "yes" to including Fluent. For an existing project, add the Fluent package and a database driver to `Package.swift`:

```swift
// Package dependencies
.package(url: "https://github.com/vapor/fluent.git", from: "4.0.0"),
.package(url: "https://github.com/vapor/fluent-<db>-driver.git", from: "<version>"),

// Target dependencies
.target(name: "App", dependencies: [
    .product(name: "Fluent", package: "fluent"),
    .product(name: "Fluent<Db>Driver", package: "fluent-<db>-driver"),
    .product(name: "Vapor", package: "vapor"),
]),
```

### 2. Configure the Database Driver

In `configure.swift`, import Fluent and the driver, then configure the database connection.

**PostgreSQL** (recommended):
```swift
import Fluent
import FluentPostgresDriver

app.databases.use(
    .postgres(
        configuration: .init(
            hostname: "localhost",
            username: "vapor",
            password: "vapor",
            database: "vapor",
            tls: .disable
        )
    ),
    as: .psql
)
```

**SQLite** (good for prototyping):
```swift
import Fluent
import FluentSQLiteDriver

// File-based
app.databases.use(.sqlite(.file("db.sqlite")), as: .sqlite)

// In-memory (ephemeral, useful for testing)
app.databases.use(.sqlite(.memory), as: .sqlite)
```

**MySQL / MariaDB**:
```swift
import Fluent
import FluentMySQLDriver

app.databases.use(.mysql(
    hostname: "localhost",
    username: "vapor",
    password: "vapor",
    database: "vapor"
), as: .mysql)
```

**MongoDB**:
```swift
import Fluent
import FluentMongoDriver

try app.databases.use(.mongo(connectionString: "<connection string>"), as: .mongo)
```

PostgreSQL, MySQL, and MongoDB also support connection string URLs:
```swift
try app.databases.use(.postgres(url: "<connection string>"), as: .psql)
```

### 3. Define Models

Create model classes conforming to `Model`. Mark them `final` for performance. Every model needs:
- A static `schema` property (table/collection name, `snake_case` and plural)
- An `@ID` field
- An empty `init()`

```swift
final class Galaxy: Model, Content {
    static let schema = "galaxies"

    @ID(key: .id)
    var id: UUID?

    @Field(key: "name")
    var name: String

    init() { }

    init(id: UUID? = nil, name: String) {
        self.id = id
        self.name = name
    }
}
```

Key property wrappers for fields:
- `@ID(key: .id)` -- unique identifier, use `UUID?` by default
- `@Field(key: "db_column")` -- required stored field
- `@OptionalField(key: "db_column")` -- optional stored field
- `@Parent(key: "foreign_key_id")` -- belongs-to relation (stores a foreign key)
- `@Children(for: \.$parentField)` -- has-many relation (inverse of `@Parent`)
- `@Siblings(...)` -- many-to-many relation via a pivot table
- `@Timestamp(key: "created_at", on: .create)` -- auto-managed timestamp

Add `Content` conformance to return models directly from route handlers.

### 4. Define Relations

**One-to-many (Parent/Children):**

On the child model, add a `@Parent` field:
```swift
final class Star: Model, Content {
    static let schema = "stars"

    @ID(key: .id)
    var id: UUID?

    @Field(key: "name")
    var name: String

    @Parent(key: "galaxy_id")
    var galaxy: Galaxy

    init() { }

    init(id: UUID? = nil, name: String, galaxyID: UUID) {
        self.id = id
        self.name = name
        self.$galaxy.id = galaxyID
    }
}
```

On the parent model, add a `@Children` property:
```swift
// Add to Galaxy model
@Children(for: \.$galaxy)
var stars: [Star]
```

Note: Access the underlying property wrapper with `$` prefix (e.g., `self.$galaxy.id = galaxyID`).

### 5. Write Migrations

Create migrations conforming to `AsyncMigration` to set up database schemas. The `prepare` method creates/modifies the schema, and `revert` undoes those changes.

```swift
struct CreateGalaxy: AsyncMigration {
    func prepare(on database: Database) async throws {
        try await database.schema("galaxies")
            .id()
            .field("name", .string)
            .create()
    }

    func revert(on database: Database) async throws {
        try await database.schema("galaxies").delete()
    }
}
```

For models with foreign keys, add a `.references` constraint:
```swift
struct CreateStar: AsyncMigration {
    func prepare(on database: Database) async throws {
        try await database.schema("stars")
            .id()
            .field("name", .string)
            .field("galaxy_id", .uuid, .references("galaxies", "id"))
            .create()
    }

    func revert(on database: Database) async throws {
        try await database.schema("stars").delete()
    }
}
```

Register migrations in `configure.swift` **in dependency order** (parent tables first):
```swift
app.migrations.add(CreateGalaxy())
app.migrations.add(CreateStar())
```

Run migrations from the command line:
```
swift run App migrate
```

For in-memory SQLite databases, auto-migrate on startup:
```swift
try await app.autoMigrate()
```

### 6. Perform CRUD Operations

**Create:**
```swift
app.post("galaxies") { req async throws -> Galaxy in
    let galaxy = try req.content.decode(Galaxy.self)
    try await galaxy.create(on: req.db)
    return galaxy
}
```

**Read all:**
```swift
app.get("galaxies") { req async throws in
    try await Galaxy.query(on: req.db).all()
}
```

**Read one by ID:**
```swift
app.get("galaxies", ":id") { req async throws -> Galaxy in
    guard let galaxy = try await Galaxy.find(req.parameters.get("id"), on: req.db) else {
        throw Abort(.notFound)
    }
    return galaxy
}
```

**Update:**
```swift
app.put("galaxies", ":id") { req async throws -> Galaxy in
    guard let galaxy = try await Galaxy.find(req.parameters.get("id"), on: req.db) else {
        throw Abort(.notFound)
    }
    let updated = try req.content.decode(Galaxy.self)
    galaxy.name = updated.name
    try await galaxy.save(on: req.db)
    return galaxy
}
```

**Delete:**
```swift
app.delete("galaxies", ":id") { req async throws -> HTTPStatus in
    guard let galaxy = try await Galaxy.find(req.parameters.get("id"), on: req.db) else {
        throw Abort(.notFound)
    }
    try await galaxy.delete(on: req.db)
    return .noContent
}
```

### 7. Use Eager Loading for Relations

Use `.with(\.$relation)` on the query builder to load related models:
```swift
app.get("galaxies") { req async throws in
    try await Galaxy.query(on: req.db).with(\.$stars).all()
}
```

This returns galaxies with their stars nested in the response:
```json
[
    {
        "id": "...",
        "name": "Milky Way",
        "stars": [
            { "id": "...", "name": "Sun", "galaxy": { "id": "..." } }
        ]
    }
]
```

### 8. Enable Query Logging (Optional)

To see the generated SQL statements in the console, set the log level to debug in `configure.swift`:
```swift
app.logger.logLevel = .debug
```

## Key Reminders

- Always mark model classes as `final`.
- Every model must have an empty `init() { }`.
- Use `snake_case` and plural names for `schema` values (e.g., `"galaxies"`, `"star_tags"`).
- Database field keys in property wrappers should use `snake_case` (e.g., `"galaxy_id"`).
- Register migrations in dependency order -- parent tables before child tables.
- Use `$` prefix to access the underlying property wrapper (e.g., `$galaxy.id`).
- Add `Content` conformance to models you want to return directly from route handlers.
- Do not disable TLS certificate verification in production (MySQL/PostgreSQL).
