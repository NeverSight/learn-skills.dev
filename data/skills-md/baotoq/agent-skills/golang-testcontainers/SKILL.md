---
name: golang-testcontainers
description: Write integration tests in Go using testcontainers-go with real databases, caches, and message queues in Docker containers. Covers PostgreSQL, MySQL, Redis, RabbitMQ, Kafka, and custom containers with idiomatic Go testing patterns.
license: MIT
metadata:
  version: "1.0.0"
  domain: tests
  triggers: Go, Golang, integration tests, testcontainers, Docker, database testing, PostgreSQL, Redis, RabbitMQ, Kafka, MySQL, container testing
  role: specialist
  scope: implementation
  output-format: code
  related-skills: golang-pro, golang-testing, golang-patterns
---

# Go Integration Testing with Testcontainers

## When to Use This Skill

- Writing integration tests that need real infrastructure (databases, caches, message queues)
- Testing data access layers against actual databases instead of mocks
- Verifying message queue or cache integrations
- Testing database migrations and schema changes
- Ensuring tests work against production-like environments in CI/CD

## Core Principles

1. **Real Infrastructure Over Mocks** - Use actual databases/services in containers, not mocks
2. **Test Isolation** - Each test gets fresh containers or clean data via snapshots
3. **Automatic Cleanup** - `testcontainers.CleanupContainer(t, ctr)` handles lifecycle
4. **Idiomatic Go** - Table-driven tests, `t.Helper()`, `t.Cleanup()`, subtests
5. **Context Propagation** - Pass `context.Context` to all container operations
6. **Port Randomization** - Containers use random ports to avoid conflicts

## Reference Guide

Load detailed guidance based on context:

| Topic | Reference | Load When |
|-------|-----------|-----------|
| Advanced Patterns | `references/advanced-patterns.md` | Multi-container networks, Kafka, snapshots, TestMain, CI/CD |

## Go Module Setup

```bash
go get github.com/testcontainers/testcontainers-go
go get github.com/testcontainers/testcontainers-go/modules/postgres
go get github.com/testcontainers/testcontainers-go/modules/mysql
go get github.com/testcontainers/testcontainers-go/modules/redis
go get github.com/testcontainers/testcontainers-go/modules/rabbitmq
go get github.com/testcontainers/testcontainers-go/modules/kafka
```

## Why Testcontainers Over Mocks?

```go
// BAD: Mocking a database - doesn't test real SQL behavior
type mockDB struct{}
func (m *mockDB) GetUser(id string) (*User, error) {
    return &User{ID: id, Name: "Alice"}, nil // No real query executed
}

// GOOD: Test against a real database with testcontainers
func TestGetUser(t *testing.T) {
    ctx := context.Background()
    ctr, err := postgres.Run(ctx, "postgres:16-alpine",
        postgres.WithDatabase("testdb"),
        postgres.WithUsername("test"),
        postgres.WithPassword("test"),
        postgres.BasicWaitStrategies(),
    )
    testcontainers.CleanupContainer(t, ctr)
    require.NoError(t, err)

    connStr, err := ctr.ConnectionString(ctx)
    require.NoError(t, err)

    db, err := sql.Open("pgx", connStr)
    require.NoError(t, err)
    defer db.Close()

    // Test real SQL queries, constraints, and behavior
}
```

## Pattern 1: PostgreSQL Integration Tests

```go
package repository_test

import (
    "context"
    "database/sql"
    "testing"

    "github.com/stretchr/testify/require"
    "github.com/testcontainers/testcontainers-go"
    "github.com/testcontainers/testcontainers-go/modules/postgres"
    _ "github.com/jackc/pgx/v5/stdlib"
)

func setupPostgres(t *testing.T) *sql.DB {
    t.Helper()
    ctx := context.Background()

    ctr, err := postgres.Run(ctx, "postgres:16-alpine",
        postgres.WithDatabase("testdb"),
        postgres.WithUsername("test"),
        postgres.WithPassword("test"),
        postgres.BasicWaitStrategies(),
    )
    testcontainers.CleanupContainer(t, ctr)
    require.NoError(t, err)

    connStr, err := ctr.ConnectionString(ctx)
    require.NoError(t, err)

    db, err := sql.Open("pgx", connStr)
    require.NoError(t, err)
    t.Cleanup(func() { db.Close() })

    // Run migrations
    _, err = db.ExecContext(ctx, `
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        )`)
    require.NoError(t, err)

    return db
}

func TestUserRepository(t *testing.T) {
    db := setupPostgres(t)
    repo := NewUserRepository(db)

    t.Run("Create", func(t *testing.T) {
        err := repo.Create(context.Background(), &User{Name: "Alice", Email: "alice@test.com"})
        require.NoError(t, err)
    })

    t.Run("GetByEmail", func(t *testing.T) {
        user, err := repo.GetByEmail(context.Background(), "alice@test.com")
        require.NoError(t, err)
        require.Equal(t, "Alice", user.Name)
    })
}
```

## Pattern 2: MySQL Integration Tests

```go
func setupMySQL(t *testing.T) *sql.DB {
    t.Helper()
    ctx := context.Background()

    ctr, err := mysql.Run(ctx, "mysql:8.0.36",
        mysql.WithDatabase("testdb"),
        mysql.WithUsername("test"),
        mysql.WithPassword("test"),
    )
    testcontainers.CleanupContainer(t, ctr)
    require.NoError(t, err)

    connStr, err := ctr.ConnectionString(ctx)
    require.NoError(t, err)

    db, err := sql.Open("mysql", connStr)
    require.NoError(t, err)
    t.Cleanup(func() { db.Close() })

    return db
}
```

## Pattern 3: Redis Integration Tests

```go
package cache_test

import (
    "context"
    "testing"

    "github.com/redis/go-redis/v9"
    "github.com/stretchr/testify/require"
    "github.com/testcontainers/testcontainers-go"
    tcredis "github.com/testcontainers/testcontainers-go/modules/redis"
)

func setupRedis(t *testing.T) *redis.Client {
    t.Helper()
    ctx := context.Background()

    ctr, err := tcredis.Run(ctx, "redis:7")
    testcontainers.CleanupContainer(t, ctr)
    require.NoError(t, err)

    endpoint, err := ctr.Endpoint(ctx, "")
    require.NoError(t, err)

    client := redis.NewClient(&redis.Options{Addr: endpoint})
    t.Cleanup(func() { client.Close() })

    return client
}

func TestCacheService(t *testing.T) {
    client := setupRedis(t)
    cache := NewCacheService(client)
    ctx := context.Background()

    t.Run("SetAndGet", func(t *testing.T) {
        err := cache.Set(ctx, "key1", "value1", 0)
        require.NoError(t, err)

        val, err := cache.Get(ctx, "key1")
        require.NoError(t, err)
        require.Equal(t, "value1", val)
    })

    t.Run("GetMiss", func(t *testing.T) {
        _, err := cache.Get(ctx, "nonexistent")
        require.ErrorIs(t, err, ErrCacheMiss)
    })
}
```

## Pattern 4: RabbitMQ Integration Tests

```go
package messaging_test

import (
    "context"
    "testing"

    amqp "github.com/rabbitmq/amqp091-go"
    "github.com/stretchr/testify/require"
    "github.com/testcontainers/testcontainers-go"
    "github.com/testcontainers/testcontainers-go/modules/rabbitmq"
)

func setupRabbitMQ(t *testing.T) *amqp.Connection {
    t.Helper()
    ctx := context.Background()

    ctr, err := rabbitmq.Run(ctx, "rabbitmq:3-management-alpine",
        rabbitmq.WithAdminUsername("guest"),
        rabbitmq.WithAdminPassword("guest"),
    )
    testcontainers.CleanupContainer(t, ctr)
    require.NoError(t, err)

    endpoint, err := ctr.AmqpURL(ctx)
    require.NoError(t, err)

    conn, err := amqp.Dial(endpoint)
    require.NoError(t, err)
    t.Cleanup(func() { conn.Close() })

    return conn
}

func TestPublishAndConsume(t *testing.T) {
    conn := setupRabbitMQ(t)
    ctx := context.Background()

    ch, err := conn.Channel()
    require.NoError(t, err)
    defer ch.Close()

    q, err := ch.QueueDeclare("test-queue", false, true, false, false, nil)
    require.NoError(t, err)

    // Publish
    body := []byte("hello")
    err = ch.PublishWithContext(ctx, "", q.Name, false, false, amqp.Publishing{
        ContentType: "text/plain",
        Body:        body,
    })
    require.NoError(t, err)

    // Consume
    msgs, err := ch.Consume(q.Name, "", true, false, false, false, nil)
    require.NoError(t, err)

    msg := <-msgs
    require.Equal(t, body, msg.Body)
}
```

## Pattern 5: Generic Container

For services without a dedicated module:

```go
func setupMinio(t *testing.T) string {
    t.Helper()
    ctx := context.Background()

    ctr, err := testcontainers.Run(ctx, "minio/minio:latest",
        testcontainers.WithExposedPorts("9000/tcp"),
        testcontainers.WithEnv(map[string]string{
            "MINIO_ROOT_USER":     "minioadmin",
            "MINIO_ROOT_PASSWORD": "minioadmin",
        }),
        testcontainers.WithCmd("server", "/data"),
        testcontainers.WithWaitStrategy(
            wait.ForListeningPort("9000/tcp"),
        ),
    )
    testcontainers.CleanupContainer(t, ctr)
    require.NoError(t, err)

    endpoint, err := ctr.Endpoint(ctx, "")
    require.NoError(t, err)

    return endpoint
}
```

## Pattern 6: Table-Driven Integration Tests

Combine testcontainers with Go's table-driven test pattern:

```go
func TestOrderRepository_Create(t *testing.T) {
    db := setupPostgres(t)
    repo := NewOrderRepository(db)

    tests := []struct {
        name    string
        order   Order
        wantErr bool
    }{
        {
            name:  "valid order",
            order: Order{CustomerID: "CUST1", Total: 99.99},
        },
        {
            name:    "missing customer ID",
            order:   Order{Total: 50.00},
            wantErr: true,
        },
        {
            name:    "negative total",
            order:   Order{CustomerID: "CUST2", Total: -10.00},
            wantErr: true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            err := repo.Create(context.Background(), &tt.order)
            if tt.wantErr {
                require.Error(t, err)
                return
            }
            require.NoError(t, err)
            require.NotZero(t, tt.order.ID)
        })
    }
}
```

## Pattern 7: Shared Container with TestMain

Reuse a single container across all tests in a package for speed:

```go
package repository_test

var testDB *sql.DB

func TestMain(m *testing.M) {
    ctx := context.Background()

    ctr, err := postgres.Run(ctx, "postgres:16-alpine",
        postgres.WithDatabase("testdb"),
        postgres.WithUsername("test"),
        postgres.WithPassword("test"),
        postgres.BasicWaitStrategies(),
    )
    if err != nil {
        log.Fatal(err)
    }

    connStr, err := ctr.ConnectionString(ctx)
    if err != nil {
        log.Fatal(err)
    }

    testDB, err = sql.Open("pgx", connStr)
    if err != nil {
        log.Fatal(err)
    }

    // Run migrations
    runMigrations(testDB)

    code := m.Run()

    testDB.Close()
    testcontainers.TerminateContainer(ctr)
    os.Exit(code)
}

func TestWithSharedDB(t *testing.T) {
    // Use testDB directly - container is shared across all tests
    repo := NewUserRepository(testDB)
    // ...
}
```

## Best Practices

1. **Use `testcontainers.CleanupContainer(t, ctr)`** - Automatic cleanup tied to test lifecycle
2. **Use `t.Helper()`** - Mark setup functions as helpers for clean stack traces
3. **Use `t.Cleanup()`** - Register deferred cleanup for connections and clients
4. **Prefer module APIs** - `postgres.Run()`, `tcredis.Run()` over generic containers
5. **Random ports always** - Never bind fixed ports; use `Endpoint()` or `ConnectionString()`
6. **Share containers with `TestMain`** - One container per package, not per test
7. **Table-driven tests** - Combine with real infrastructure for comprehensive coverage
8. **Context propagation** - Pass `context.Background()` to container operations
9. **Race detector** - Always run integration tests with `go test -race`
10. **Build tags** - Separate integration tests with `//go:build integration`

## Build Tag Separation

```go
//go:build integration

package repository_test

// These tests only run with: go test -tags=integration ./...
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Container startup timeout | Increase Docker resource limits or use lightweight images (alpine) |
| Port conflicts | Always use random ports via `Endpoint()` - never fixed ports |
| Tests fail in CI | Ensure CI runner has Docker (`ubuntu-latest` on GitHub Actions) |
| Slow test suite | Share containers via `TestMain` instead of per-test containers |
| Flaky connection | Use module-provided wait strategies (`postgres.BasicWaitStrategies()`) |
| Leaked containers | Always call `testcontainers.CleanupContainer(t, ctr)` immediately after `Run` |
