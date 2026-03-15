---
name: golang-gin-testing
description: "Test Go Gin REST APIs with unit, integration, e2e, benchmark, and fuzz tests. Covers httptest patterns, table-driven tests, golden file snapshots, mocking repositories, testcontainers, coverage thresholds, race detection, and CI/CD integration. Use when writing tests for Gin handlers, services, middleware, or setting up test infrastructure for a Go API."
license: MIT
metadata:
  author: henriqueatila
  version: 1.0.3
---

# golang-gin-testing — Testing REST APIs

Write confident tests for Gin APIs: unit tests with mocked repositories, integration tests with real PostgreSQL via testcontainers, and e2e tests for critical flows. This skill covers the 80% of testing patterns you need daily.

## When to Use

- Writing tests for Gin handlers (`UserHandler`, `AuthHandler`)
- Testing services with a mocked `UserRepository`
- Setting up integration tests with a real database (testcontainers)
- Testing JWT auth middleware in isolation
- Adding table-driven tests for request validation and error paths
- Setting up `TestMain` for shared test infrastructure

## Table of Contents

1. [Testing Philosophy](#testing-philosophy)
2. [Test Helpers](#test-helpers)
3. [Handler Tests with httptest](#handler-tests-with-httptest)
4. [Table-Driven Handler Tests](#table-driven-handler-tests)
5. [Service Tests with Mocked Repository](#service-tests-with-mocked-repository)
6. [Running Tests](#running-tests)
7. [Reference Files](#reference-files)
8. [Cross-Skill References](#cross-skill-references)

---

## Testing Philosophy

| Layer | Tool | Goal |
|---|---|---|
| Handler | `httptest` + mock service | Verify HTTP contract (status codes, JSON shape) |
| Service | mock repository | Verify business logic, error mapping |
| Repository | testcontainers (real DB) | Verify SQL correctness |
| E2E | running server + real DB | Verify critical user flows end-to-end |

Unit tests run fast and cover most cases. Integration tests verify real database behavior. E2e tests catch wiring bugs. **Never mock what you're testing** — mock the layer below.

---

## Test Helpers

Define reusable helpers in `internal/testutil/` to keep tests DRY.

```go
// internal/testutil/helpers.go
package testutil

import (
    "bytes"
    "encoding/json"
    "net/http"
    "net/http/httptest"
    "testing"

    "github.com/gin-gonic/gin"
)

func init() {
    // Suppress Gin debug output in tests
    gin.SetMode(gin.TestMode)
}

// NewTestRouter creates a bare Gin engine for tests (no Logger/Recovery noise).
func NewTestRouter() *gin.Engine {
    return gin.New()
}

// PerformRequest executes an HTTP request against the given router and returns the recorder.
func PerformRequest(t *testing.T, router *gin.Engine, method, path string, body any, headers map[string]string) *httptest.ResponseRecorder {
    t.Helper()

    var reqBody *bytes.Buffer
    if body != nil {
        b, err := json.Marshal(body)
        if err != nil {
            t.Fatalf("PerformRequest: failed to marshal body: %v", err)
        }
        reqBody = bytes.NewBuffer(b)
    } else {
        reqBody = bytes.NewBuffer(nil)
    }

    req, err := http.NewRequest(method, path, reqBody)
    if err != nil {
        t.Fatalf("PerformRequest: failed to create request: %v", err)
    }

    if body != nil {
        req.Header.Set("Content-Type", "application/json")
    }
    for k, v := range headers {
        req.Header.Set(k, v)
    }

    w := httptest.NewRecorder()
    router.ServeHTTP(w, req)
    return w
}

// AssertJSON unmarshals the recorder body into dst, failing the test on error.
func AssertJSON(t *testing.T, w *httptest.ResponseRecorder, dst any) {
    t.Helper()
    if err := json.Unmarshal(w.Body.Bytes(), dst); err != nil {
        t.Fatalf("AssertJSON: failed to unmarshal %q: %v", w.Body.String(), err)
    }
}

// BearerHeader returns an Authorization header map for JWT-protected routes.
func BearerHeader(token string) map[string]string {
    return map[string]string{"Authorization": "Bearer " + token}
}
```

---

## Handler Tests with httptest

Test handlers by wiring a real router with a **mock service**, then using `httptest.NewRecorder` + `router.ServeHTTP`.

```go
// internal/handler/user_handler_test.go
package handler_test

import (
    "context"
    "log/slog"
    "net/http"
    "testing"
    "time"

    "github.com/gin-gonic/gin"
    "myapp/internal/domain"
    "myapp/internal/handler"
    "myapp/internal/service"
    "myapp/internal/testutil"
)

// mockUserService implements service.UserService for tests.
type mockUserService struct {
    createFn  func(ctx context.Context, req domain.CreateUserRequest) (*domain.User, error)
    getByIDFn func(ctx context.Context, id string) (*domain.User, error)
}

func (m *mockUserService) Create(ctx context.Context, req domain.CreateUserRequest) (*domain.User, error) {
    return m.createFn(ctx, req)
}

func (m *mockUserService) GetByID(ctx context.Context, id string) (*domain.User, error) {
    return m.getByIDFn(ctx, id)
}

func setupUserRouter(svc service.UserService) *gin.Engine {
    r := testutil.NewTestRouter()
    h := handler.NewUserHandler(svc, slog.Default())
    r.POST("/users", h.Create)
    r.GET("/users/:id", h.GetByID)
    return r
}

func TestUserHandler_Create_Success(t *testing.T) {
    now := time.Now()
    svc := &mockUserService{
        createFn: func(ctx context.Context, req domain.CreateUserRequest) (*domain.User, error) {
            return &domain.User{
                ID:        "user-123",
                Name:      req.Name,
                Email:     req.Email,
                Role:      "user",
                CreatedAt: now,
                UpdatedAt: now,
            }, nil
        },
    }

    router := setupUserRouter(svc)
    body := map[string]any{
        "name":     "Alice",
        "email":    "alice@example.com",
        "password": "secret123",
    }

    w := testutil.PerformRequest(t, router, http.MethodPost, "/users", body, nil)

    if w.Code != http.StatusCreated {
        t.Errorf("expected status 201, got %d; body: %s", w.Code, w.Body)
    }

    var got domain.User
    testutil.AssertJSON(t, w, &got)
    if got.ID != "user-123" {
        t.Errorf("expected user ID 'user-123', got %q", got.ID)
    }
}

func TestUserHandler_GetByID_NotFound(t *testing.T) {
    svc := &mockUserService{
        getByIDFn: func(ctx context.Context, id string) (*domain.User, error) {
            return nil, domain.ErrNotFound
        },
    }

    router := setupUserRouter(svc)
    w := testutil.PerformRequest(t, router, http.MethodGet, "/users/missing-id", nil, nil)

    if w.Code != http.StatusNotFound {
        t.Errorf("expected status 404, got %d", w.Code)
    }
}
```

---

## Table-Driven Handler Tests

Table-driven tests cover all request variants (valid, invalid, edge cases) in one function.

```go
// internal/handler/user_handler_table_test.go
package handler_test

import (
    "context"
    "net/http"
    "testing"

    "myapp/internal/domain"
    "myapp/internal/testutil"
)

func TestUserHandler_Create_Validation(t *testing.T) {
    svc := &mockUserService{
        createFn: func(ctx context.Context, req domain.CreateUserRequest) (*domain.User, error) {
            return &domain.User{ID: "1", Name: req.Name, Email: req.Email, Role: "user"}, nil
        },
    }
    router := setupUserRouter(svc)

    tests := []struct {
        name       string
        body       any
        wantStatus int
    }{
        {
            name:       "valid request",
            body:       map[string]any{"name": "Alice", "email": "alice@example.com", "password": "secret123"},
            wantStatus: http.StatusCreated,
        },
        {
            name:       "missing email",
            body:       map[string]any{"name": "Alice", "password": "secret123"},
            wantStatus: http.StatusBadRequest,
        },
        {
            name:       "invalid email format",
            body:       map[string]any{"name": "Alice", "email": "not-an-email", "password": "secret123"},
            wantStatus: http.StatusBadRequest,
        },
        {
            name:       "name too short",
            body:       map[string]any{"name": "A", "email": "alice@example.com", "password": "secret123"},
            wantStatus: http.StatusBadRequest,
        },
        {
            name:       "password too short",
            body:       map[string]any{"name": "Alice", "email": "alice@example.com", "password": "short"},
            wantStatus: http.StatusBadRequest,
        },
        {
            name:       "invalid role value",
            body:       map[string]any{"name": "Alice", "email": "alice@example.com", "password": "secret123", "role": "superadmin"},
            wantStatus: http.StatusBadRequest,
        },
    }

    for _, tc := range tests {
        t.Run(tc.name, func(t *testing.T) {
            t.Parallel()
            w := testutil.PerformRequest(t, router, http.MethodPost, "/users", tc.body, nil)
            if w.Code != tc.wantStatus {
                t.Errorf("want status %d, got %d; body: %s", tc.wantStatus, w.Code, w.Body)
            }
        })
    }
}
```

---

## Service Tests with Mocked Repository

Test business logic without touching the database. The mock implements `domain.UserRepository`.

```go
// internal/service/user_service_test.go
package service_test

import (
    "context"
    "errors"
    "log/slog"
    "testing"

    "myapp/internal/domain"
    "myapp/internal/service"
)

// mockUserRepository implements domain.UserRepository for service tests.
type mockUserRepository struct {
    createFn     func(ctx context.Context, user *domain.User) error
    getByEmailFn func(ctx context.Context, email string) (*domain.User, error)
    getByIDFn    func(ctx context.Context, id string) (*domain.User, error)
}

func (m *mockUserRepository) Create(ctx context.Context, user *domain.User) error {
    return m.createFn(ctx, user)
}
func (m *mockUserRepository) GetByEmail(ctx context.Context, email string) (*domain.User, error) {
    return m.getByEmailFn(ctx, email)
}
func (m *mockUserRepository) GetByID(ctx context.Context, id string) (*domain.User, error) {
    if m.getByIDFn != nil {
        return m.getByIDFn(ctx, id)
    }
    return nil, domain.ErrNotFound
}
func (m *mockUserRepository) List(ctx context.Context, opts domain.ListOptions) ([]domain.User, int64, error) {
    return nil, 0, nil
}
func (m *mockUserRepository) Update(ctx context.Context, user *domain.User) error { return nil }
func (m *mockUserRepository) Delete(ctx context.Context, id string) error         { return nil }

func TestUserService_Create_DuplicateEmail(t *testing.T) {
    repo := &mockUserRepository{
        getByEmailFn: func(ctx context.Context, email string) (*domain.User, error) {
            return &domain.User{Email: email}, nil // email already taken
        },
        createFn: func(ctx context.Context, user *domain.User) error {
            return nil
        },
    }

    svc := service.NewUserService(repo, slog.Default())
    _, err := svc.Create(context.Background(), domain.CreateUserRequest{
        Name:     "Alice",
        Email:    "alice@example.com",
        Password: "secret123",
    })

    // Use errors.As to unwrap *AppError and inspect the HTTP status code.
    // errors.Is works only if AppError implements Is(); errors.As is always safe.
    var appErr *domain.AppError
    if !errors.As(err, &appErr) || appErr.Code != 409 {
        t.Errorf("expected ErrConflict (409 AppError), got %v", err)
    }
}
```

---

## Running Tests

```bash
# All tests with race detector and coverage
go test -v -race -cover ./...

# Specific package
go test -v -race ./internal/handler/...

# Run only unit tests (exclude integration)
go test -v -race -cover -tags='!integration' ./...

# Run integration tests only (requires Docker)
go test -v -race -tags=integration ./internal/repository/...

# Coverage report
go test -race -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

---

## Reference Files

Load these when you need deeper detail:

- **[references/unit-tests.md](references/unit-tests.md)** — Handler httptest patterns, testing authenticated routes with mock JWT, middleware isolation tests, mock generation with `gomock`/manual mocks, `t.Helper`/`t.Cleanup`/`t.Parallel`, test fixtures and factories, benchmark tests (`BenchmarkX`), fuzz tests (`FuzzX`), golden file/snapshot testing, test organization (same-package vs external-package, build tags), testify assertions
- **[references/integration-tests.md](references/integration-tests.md)** — testcontainers-go setup, `TestMain` for DB lifecycle, repository integration tests, cleanup between tests, build tags, fixture loading
- **[references/e2e.md](references/e2e.md)** — End-to-end flow testing (register → login → CRUD), docker-compose test setup, GitHub Actions CI/CD, environment configuration, cleanup and idempotency

## Cross-Skill References

- For handler and service implementations being tested: see the **golang-gin-api** skill
- For `UserRepository` interface and GORM/sqlx implementations: see the **golang-gin-database** skill
- For JWT middleware and auth handler test patterns: see the **golang-gin-auth** skill
- **golang-gin-clean-arch** → Architecture: mock strategy (boundaries only), testing by layer, test fixtures

## Official Docs

If this skill doesn't cover your use case, consult the [Go testing package](https://pkg.go.dev/testing), [httptest GoDoc](https://pkg.go.dev/net/http/httptest), or [testcontainers-go docs](https://golang.testcontainers.org/).
