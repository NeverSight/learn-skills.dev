---
name: golang-gin-database
description: "Integrate PostgreSQL databases with Go Gin APIs using GORM or sqlx. Covers repository pattern, connection retry with backoff, cursor/keyset pagination, context-based transactions, TLS/sslmode, migrations, and dependency injection. Use when adding database support, creating models, writing queries, implementing repositories, setting up migrations, or wiring database layers into a Gin project. Also activate when the user mentions GORM, sqlx, database connection, SQL queries, repository pattern, or database migrations in a Go/Gin context."
license: MIT
metadata:
  author: henriqueatila
  version: 1.0.4
---

# golang-gin-database — Database Integration

Integrate PostgreSQL with Gin APIs using the repository pattern. Keeps database logic out of handlers and services, and supports swapping GORM ↔ sqlx without touching business logic.

## When to Use

- Adding a PostgreSQL database to a Gin project
- Implementing the repository pattern (interface + concrete implementation)
- Writing GORM or sqlx queries
- Setting up database connection pooling
- Running migrations (golang-migrate)
- Wiring repositories → services → handlers in `main.go`
- Writing context-propagating transactions

## Repository Interface Pattern

**Define the interface in the domain layer; implement it in the repository layer.** This inverts the dependency: services depend on an abstraction, not a concrete database library.

> **Architecture note:** In clean architecture, domain entities should not carry `json` or `binding` tags. Use separate request/response DTOs in the delivery layer. See **golang-gin-clean-arch** Golden Rule 4.

```go
// internal/domain/user.go
package domain

import (
    "context"
    "time"
)

type User struct {
    ID           string
    Name         string
    Email        string
    Role         string
    PasswordHash string    // set by service layer before persisting; never serialized to API responses
    CreatedAt    time.Time
    UpdatedAt    time.Time
}

type ListOptions struct {
    Page  int
    Limit int
    Role  string
}

// UserRepository defines the data access contract.
// Implementations live in internal/repository — GORM or sqlx, interchangeable.
type UserRepository interface {
    Create(ctx context.Context, user *User) error
    GetByID(ctx context.Context, id string) (*User, error)
    GetByEmail(ctx context.Context, email string) (*User, error)
    List(ctx context.Context, opts ListOptions) ([]User, int64, error)
    Update(ctx context.Context, user *User) error
    Delete(ctx context.Context, id string) error
}
```

**Why define it at the consumer?** The domain package does not import `gorm.io/gorm` or `jmoiron/sqlx`. Only the repository package does. This is the Dependency Inversion Principle applied to data access.

## Database Connection Setup

```go
// internal/repository/db.go
package repository

import (
    "fmt"
    "log/slog"
    "time"

    "gorm.io/driver/postgres"
    "gorm.io/gorm"
    "gorm.io/gorm/logger"
)

type Config struct {
    DSN             string
    MaxOpenConns    int
    MaxIdleConns    int
    ConnMaxLifetime time.Duration
}

// NewGORMDB opens a PostgreSQL connection with connection pool settings.
// Architectural recommendation — not part of the Gin API.
func NewGORMDB(cfg Config, appLogger *slog.Logger) (*gorm.DB, error) {
    db, err := gorm.Open(postgres.Open(cfg.DSN), &gorm.Config{
        Logger: logger.Default.LogMode(logger.Warn),
    })
    if err != nil {
        return nil, fmt.Errorf("gorm.Open: %w", err)
    }

    sqlDB, err := db.DB()
    if err != nil {
        return nil, fmt.Errorf("db.DB: %w", err)
    }

    sqlDB.SetMaxOpenConns(cfg.MaxOpenConns)       // e.g. 25
    sqlDB.SetMaxIdleConns(cfg.MaxIdleConns)       // e.g. 5
    sqlDB.SetConnMaxLifetime(cfg.ConnMaxLifetime)  // e.g. 5*time.Minute

    if err := sqlDB.Ping(); err != nil {
        return nil, fmt.Errorf("db.Ping: %w", err)
    }

    appLogger.Info("database connected")
    return db, nil
}

// ConnectWithRetry retries the connection with exponential backoff.
// Use during startup when the database container may not be ready yet.
func ConnectWithRetry(dsn string, maxRetries int) (*gorm.DB, error) {
    var db *gorm.DB
    var err error
    for i := 0; i < maxRetries; i++ {
        db, err = gorm.Open(postgres.Open(dsn), &gorm.Config{
            Logger: logger.Default.LogMode(logger.Warn),
        })
        if err == nil {
            sqlDB, err := db.DB()
            if err != nil {
                return nil, fmt.Errorf("failed to get underlying sql.DB: %w", err)
            }
            sqlDB.SetMaxOpenConns(25)
            sqlDB.SetMaxIdleConns(10)
            sqlDB.SetConnMaxLifetime(5 * time.Minute)
            sqlDB.SetConnMaxIdleTime(1 * time.Minute)
            if err := sqlDB.Ping(); err != nil {
                return nil, fmt.Errorf("database ping failed: %w", err)
            }
            return db, nil
        }
        backoff := time.Duration(1<<uint(i)) * time.Second
        slog.Warn("database connection failed, retrying", "attempt", i+1, "backoff", backoff, "error", err)
        time.Sleep(backoff)
    }
    return nil, fmt.Errorf("failed to connect after %d retries: %w", maxRetries, err)
}
```

**TLS / production DSN:** Always use `sslmode=verify-full` in production to prevent MITM attacks.

```go
// Development (local Docker)
dsn := "host=localhost user=app password=secret dbname=myapp sslmode=disable"

// Production: verify the server certificate
dsn := "host=db.example.com user=app password=*** dbname=myapp sslmode=verify-full sslrootcert=/etc/ssl/certs/rds-ca.pem"
```

For sqlx, see [references/sqlx-patterns.md](references/sqlx-patterns.md#connection-setup).

## GORM Repository Implementation (Brief)

```go
// internal/repository/user_repository_gorm.go
package repository

import (
    "context"
    "errors"

    "gorm.io/gorm"
    "myapp/internal/domain"
)

type gormUserRepository struct {
    db *gorm.DB
}

func NewUserRepository(db *gorm.DB) domain.UserRepository {
    return &gormUserRepository{db: db}
}

func (r *gormUserRepository) GetByID(ctx context.Context, id string) (*domain.User, error) {
    var m UserModel
    if err := r.txFromCtx(ctx).WithContext(ctx).First(&m, "id = ?", id).Error; err != nil {
        if errors.Is(err, gorm.ErrRecordNotFound) {
            return nil, domain.ErrNotFound.New(err)
        }
        return nil, domain.ErrInternal.New(err)
    }
    return m.ToDomain(), nil
}
```

For full GORM patterns (models, soft deletes, preloading, transactions, hooks): see [references/gorm-patterns.md](references/gorm-patterns.md).

## sqlx Repository Implementation (Brief)

```go
// internal/repository/user_repository_sqlx.go
package repository

import (
    "context"
    "database/sql"
    "errors"

    "github.com/jmoiron/sqlx"
    "myapp/internal/domain"
)

type sqlxUserRepository struct {
    db *sqlx.DB
}

func NewSqlxUserRepository(db *sqlx.DB) domain.UserRepository {
    return &sqlxUserRepository{db: db}
}

func (r *sqlxUserRepository) GetByID(ctx context.Context, id string) (*domain.User, error) {
    var u userRow
    err := r.db.GetContext(ctx, &u, `SELECT id, name, email, role, created_at, updated_at FROM users WHERE id = $1`, id)
    if err != nil {
        if errors.Is(err, sql.ErrNoRows) {
            return nil, domain.ErrNotFound.New(err)
        }
        return nil, domain.ErrInternal.New(err)
    }
    return u.toDomain(), nil
}
```

For full sqlx patterns (struct scanning, NamedExec, IN clauses, transactions): see [references/sqlx-patterns.md](references/sqlx-patterns.md).

## Transaction Pattern (Context-Based)

Pass `*gorm.DB` via context so repositories transparently participate in a transaction. The service orchestrates; repositories just call `txFromCtx`.

```go
// internal/repository/tx.go (GORM approach)
package repository

import (
    "context"

    "gorm.io/gorm"
)

type txKey struct{}

// WithTx stores a transaction in ctx so repositories can use it.
func WithTx(ctx context.Context, tx *gorm.DB) context.Context {
    return context.WithValue(ctx, txKey{}, tx)
}

// txFromCtx returns the transaction from ctx, or the default db.
// Every repository method should call this instead of r.db directly.
func (r *gormUserRepository) txFromCtx(ctx context.Context) *gorm.DB {
    if tx, ok := ctx.Value(txKey{}).(*gorm.DB); ok {
        return tx
    }
    return r.db
}

// Create uses txFromCtx — works both standalone and inside a transaction.
func (r *gormUserRepository) Create(ctx context.Context, user *domain.User) error {
    m := fromDomain(user)
    if err := r.txFromCtx(ctx).WithContext(ctx).Create(m).Error; err != nil {
        return mapGORMError(err)
    }
    user.ID = m.ID
    user.CreatedAt = m.CreatedAt
    user.UpdatedAt = m.UpdatedAt
    return nil
}

// Service-layer usage — the service orchestrates the transaction:
// internal/service/user_service.go
func (s *userService) RegisterWithProfile(ctx context.Context, req domain.CreateUserRequest) error {
    return s.db.WithContext(ctx).Transaction(func(tx *gorm.DB) error {
        txCtx := repository.WithTx(ctx, tx)
        if err := s.userRepo.Create(txCtx, &user); err != nil {
            return err // tx rolled back automatically
        }
        return s.profileRepo.Create(txCtx, &profile)
    })
}
```

## Cursor / Keyset Pagination

Offset pagination (`LIMIT x OFFSET y`) degrades at large offsets because PostgreSQL must skip rows. **Keyset pagination** is O(log n) via an index seek — preferred for large or fast-growing tables.

See [Cursor Pagination in GORM Patterns](references/gorm-patterns.md#cursor--keyset-pagination) for implementation.

## Dependency Injection in main.go

Wire repositories → services → handlers. Nothing creates its own dependencies.

```go
// cmd/api/main.go
package main

import (
    "log/slog"
    "os"
    "time"

    "myapp/internal/handler"
    "myapp/internal/repository"
    "myapp/internal/service"
)

func main() {
    logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))

    dbCfg := repository.Config{
        DSN:             os.Getenv("DATABASE_URL"),
        MaxOpenConns:    25,
        MaxIdleConns:    5,
        ConnMaxLifetime: 5 * time.Minute,
    }

    db, err := repository.NewGORMDB(dbCfg, logger)
    if err != nil {
        logger.Error("failed to connect to database", "error", err)
        os.Exit(1)
    }

    // Wire the dependency graph: repo → service → handler
    userRepo    := repository.NewUserRepository(db)
    userService := service.NewUserService(userRepo, logger)
    userHandler := handler.NewUserHandler(userService, logger)

    // ... router setup, see gin-api skill
    _ = userHandler
}
```

**Critical:** Read `DATABASE_URL` from environment, never hardcode credentials. See the **golang-gin-deploy** skill for Docker/Kubernetes secrets.

## Reference Files

Load these for deeper detail:

- **[references/gorm-patterns.md](references/gorm-patterns.md)** — GORM model definition, CRUD, soft deletes, scopes, preloading, raw SQL, batch ops, hooks, connection pooling, PostgreSQL-specific features, complete repository implementation
- **[references/sqlx-patterns.md](references/sqlx-patterns.md)** — Connection setup, struct scanning, Get/Select/NamedExec, safe dynamic queries, sqlx.In, null handling, query builder, complete repository implementation
- **[references/migrations.md](references/migrations.md)** — golang-migrate CLI and library usage, file naming, zero-downtime migrations, startup vs CI/CD strategy, seeding, rollback

## Cross-Skill References

- For dependency injection wiring and main.go patterns: see the **golang-gin-api** skill
- For testing repositories with a real database: see the **golang-gin-testing** skill (integration tests)
- For running migrations in Docker containers: see the **golang-gin-deploy** skill
- For user authentication using the UserRepository: see the **golang-gin-auth** skill
- **golang-gin-clean-arch** → Architecture: repository pattern, domain error wrapping, transaction patterns

## Official Docs

If this skill doesn't cover your use case, consult the [GORM documentation](https://gorm.io/docs/), [sqlx GoDoc](https://pkg.go.dev/github.com/jmoiron/sqlx), or [Gin GoDoc](https://pkg.go.dev/github.com/gin-gonic/gin).
