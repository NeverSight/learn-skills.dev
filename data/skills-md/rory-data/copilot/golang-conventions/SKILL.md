---
name: golang-conventions
description: Go coding standards for Go 1.21+, including idioms, error handling, testing patterns, concurrency, and golangci-lint configuration. Use when writing, reviewing, or refactoring Go code, working with goroutines, or setting up Go projects.
license: Proprietary. See parent repository LICENSE
---

# Go Coding Conventions

## Quick Reference

- **Go version**: Use Go 1.21+ for modern features (generics, slices package, cmp)
- **Formatting**: Use `gofmt` and `goimports` (automatic via gopls)
- **Linting**: Use `golangci-lint` with comprehensive linters enabled
- **Testing**: Table-driven tests, test fixtures, subtests with `t.Run()`
- **Error handling**: Explicit, descriptive errors with `errors.Is()` and `errors.As()`

## Core Principles

### 1. Simplicity and Clarity

- Write clear, idiomatic Go code
- Prefer simple solutions over clever ones
- Follow the principle of least surprise
- "Clear is better than clever" - Go Proverbs

### 2. Explicit Over Implicit

- No hidden control flow
- Explicit error handling (no exceptions)
- Clear dependency management
- Visible type conversions

### 3. Composition Over Inheritance

- Use interfaces for abstraction
- Prefer struct embedding over inheritance
- Accept interfaces, return structs
- Keep interfaces small and focused

## Code Style and Formatting

### Naming Conventions

```go
// Package names: lowercase, single word, no underscores
package user

// Exported identifiers: PascalCase
type UserService struct {}
func NewUserService() *UserService {}

// Unexported identifiers: camelCase
type userData struct {}
func validateEmail(email string) error {}

// Interface names: single method interfaces end with -er
type Reader interface { Read(p []byte) (n int, err error) }
type UserRepository interface { /* multiple methods */ }

// Acronyms: consistent case (HTTP, ID, URL, not Http, Id, Url)
type HTTPServer struct {}
var userID int64
```

### File Organisation

```go
// 1. Package declaration
package user

// 2. Import statements (grouped: stdlib, external, internal)
import (
    "context"
    "fmt"
    "time"

    "github.com/google/uuid"

    "myapp/internal/database"
)

// 3. Constants
const (
    MaxRetries = 3
    DefaultTimeout = 30 * time.Second
)

// 4. Variables (avoid package-level vars, prefer const or functions)
var (
    ErrUserNotFound = errors.New("user not found")
)

// 5. Types
type User struct {
    ID        uuid.UUID
    Email     string
    CreatedAt time.Time
}

// 6. Functions and methods (exported first, then unexported)
```

### Modern Go Features (1.21+)

```go
// Generics for type-safe collections
func Map[T, U any](slice []T, fn func(T) U) []U {
    result := make([]U, len(slice))
    for i, v := range slice {
        result[i] = fn(v)
    }
    return result
}

// min/max built-ins
func clamp(val, minVal, maxVal int) int {
    return max(minVal, min(val, maxVal))
}

// clear() built-in for maps and slices
func resetCache(cache map[string]any) {
    clear(cache)
}

// slices package for common operations
import "slices"
sorted := slices.Clone(original)
slices.Sort(sorted)
```

## Error Handling

### Explicit and Descriptive

```go
// Good: Clear error handling
func GetUser(ctx context.Context, id uuid.UUID) (*User, error) {
    user, err := db.FindUserByID(ctx, id)
    if err != nil {
        return nil, fmt.Errorf("failed to get user %s: %w", id, err)
    }
    return user, nil
}

// Use errors.Is() and errors.As() for sentinel errors
if errors.Is(err, ErrUserNotFound) {
    return handleNotFound()
}

var validationErr *ValidationError
if errors.As(err, &validationErr) {
    return handleValidation(validationErr)
}

// Custom error types for rich error information
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation failed on %s: %s", e.Field, e.Message)
}
```

### Error Wrapping

```go
// Wrap errors to preserve context
func processUser(ctx context.Context, id uuid.UUID) error {
    user, err := GetUser(ctx, id)
    if err != nil {
        return fmt.Errorf("process user failed: %w", err)
    }

    if err := validateUser(user); err != nil {
        return fmt.Errorf("validation failed for user %s: %w", id, err)
    }

    return nil
}
```

## Testing

### Table-Driven Tests

```go
func TestValidateEmail(t *testing.T) {
    tests := []struct {
        name    string
        email   string
        wantErr bool
    }{
        {
            name:    "valid email",
            email:   "user@example.com",
            wantErr: false,
        },
        {
            name:    "missing at sign",
            email:   "userexample.com",
            wantErr: true,
        },
        {
            name:    "empty email",
            email:   "",
            wantErr: true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            err := ValidateEmail(tt.email)
            if (err != nil) != tt.wantErr {
                t.Errorf("ValidateEmail() error = %v, wantErr %v", err, tt.wantErr)
            }
        })
    }
}
```

### Test Fixtures and Helpers

```go
// testdata/ directory for fixtures
// helper_test.go for test utilities

func setupTestDB(t *testing.T) *sql.DB {
    t.Helper()

    db, err := sql.Open("sqlite3", ":memory:")
    if err != nil {
        t.Fatalf("failed to open test db: %v", err)
    }

    t.Cleanup(func() {
        db.Close()
    })

    return db
}

// Use testify for assertions (optional but popular)
import "github.com/stretchr/testify/assert"

func TestUserCreation(t *testing.T) {
    user := NewUser("test@example.com")

    assert.NotNil(t, user.ID)
    assert.Equal(t, "test@example.com", user.Email)
    assert.False(t, user.CreatedAt.IsZero())
}
```

### Benchmarks and Examples

```go
// Benchmark functions
func BenchmarkValidateEmail(b *testing.B) {
    email := "user@example.com"

    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        ValidateEmail(email)
    }
}

// Example functions (appear in godoc)
func ExampleValidateEmail() {
    err := ValidateEmail("user@example.com")
    fmt.Println(err == nil)
    // Output: true
}
```

## Project Structure

### Standard Layout

```
myproject/
├── cmd/                    # Main applications
│   └── server/
│       └── main.go
├── internal/               # Private application code
│   ├── user/
│   │   ├── user.go
│   │   ├── user_test.go
│   │   ├── repository.go
│   │   └── service.go
│   └── database/
│       └── postgres.go
├── pkg/                    # Public libraries (optional)
│   └── utils/
├── api/                    # API definitions (OpenAPI, protobuf)
├── web/                    # Web assets (if applicable)
├── scripts/                # Build and automation scripts
├── deployments/            # Deployment configs (Docker, k8s)
├── test/                   # Additional test data
├── go.mod
├── go.sum
├── Makefile                # Common tasks
└── README.md
```

### Package Organisation

```go
// internal/user/user.go - Domain types
package user

type User struct {
    ID    uuid.UUID
    Email string
}

// internal/user/repository.go - Data access
package user

type Repository interface {
    Create(ctx context.Context, user *User) error
    FindByID(ctx context.Context, id uuid.UUID) (*User, error)
}

// internal/user/service.go - Business logic
package user

type Service struct {
    repo Repository
}

func NewService(repo Repository) *Service {
    return &Service{repo: repo}
}
```

## Dependency Management

### Go Modules Best Practices

```bash
# Initialise module
go mod init github.com/username/project

# Add dependencies (automatically)
go get github.com/google/uuid@latest

# Tidy up (remove unused, add missing)
go mod tidy

# Verify integrity
go mod verify

# Vendor dependencies (optional)
go mod vendor
```

### Version Pinning

```go
// go.mod with specific versions
module github.com/username/project

go 1.21

require (
    github.com/google/uuid v1.5.0
    github.com/lib/pq v1.10.9
)

require (
    // Indirect dependencies
    golang.org/x/crypto v0.17.0 // indirect
)
```

## Concurrency

### Goroutines and Channels

```go
// Use context for cancellation
func processItems(ctx context.Context, items []Item) error {
    results := make(chan Result, len(items))
    errors := make(chan error, 1)

    for _, item := range items {
        go func(item Item) {
            select {
            case <-ctx.Done():
                return
            case results <- processItem(item):
            }
        }(item)
    }

    // Collect results
    for i := 0; i < len(items); i++ {
        select {
        case <-ctx.Done():
            return ctx.Err()
        case err := <-errors:
            return err
        case result := <-results:
            // Handle result
        }
    }

    return nil
}
```

### sync Package Patterns

```go
import "sync"

// Use sync.WaitGroup for coordinating goroutines
var wg sync.WaitGroup

for _, item := range items {
    wg.Add(1)
    go func(item Item) {
        defer wg.Done()
        process(item)
    }(item)
}

wg.Wait()

// Use sync.Once for one-time initialisation
var (
    instance *Service
    once     sync.Once
)

func GetService() *Service {
    once.Do(func() {
        instance = newService()
    })
    return instance
}

// Use sync.Pool for frequently allocated objects
var bufferPool = sync.Pool{
    New: func() any {
        return new(bytes.Buffer)
    },
}

func processData(data []byte) {
    buf := bufferPool.Get().(*bytes.Buffer)
    defer bufferPool.Put(buf)

    buf.Reset()
    buf.Write(data)
    // Process buffer
}
```

## Performance Best Practices

### Memory Optimisation

```go
// Preallocate slices when size is known
items := make([]Item, 0, expectedCount)

// Use pointers for large structs in maps
type Cache map[string]*LargeStruct

// Reuse buffers
var buf bytes.Buffer
buf.Reset() // Clear for reuse

// Use string builder for concatenation
var sb strings.Builder
for _, s := range strings {
    sb.WriteString(s)
}
result := sb.String()
```

### Profiling

```go
import (
    "runtime/pprof"
    "net/http"
    _ "net/http/pprof"
)

// CPU profiling
f, _ := os.Create("cpu.prof")
pprof.StartCPUProfile(f)
defer pprof.StopCPUProfile()

// Memory profiling
f, _ := os.Create("mem.prof")
pprof.WriteHeapProfile(f)

// HTTP profiling endpoint
go func() {
    http.ListenAndServe("localhost:6060", nil)
}()
```

## Linting and Quality

### golangci-lint Configuration

```yaml
# .golangci.yml
run:
  timeout: 5m
  go: "1.21"

linters:
  enable:
    - errcheck # Check error handling
    - gosimple # Simplify code
    - govet # Examine Go source code
    - ineffassign # Detect ineffectual assignments
    - staticcheck # Advanced static analysis
    - unused # Find unused code
    - gofmt # Format checking
    - goimports # Import management
    - misspell # Spell checking
    - revive # Fast, configurable linter
    - gocritic # Comprehensive diagnostics
    - gosec # Security issues
    - errname # Error naming conventions
    - errorlint # Error wrapping
    - exhaustive # Enum switch exhaustiveness

linters-settings:
  errcheck:
    check-blank: true
  govet:
    check-shadowing: true
  gofmt:
    simplify: true
  revive:
    rules:
      - name: unexported-return
        disabled: true
```

## Documentation

### Package Documentation

```go
// Package user provides user management functionality.
//
// It includes user creation, validation, and repository patterns
// for data persistence. All operations support context-based
// cancellation and timeout.
package user

// User represents a system user with authentication credentials.
//
// Email must be unique and validated before persistence.
// Passwords are stored using bcrypt hashing.
type User struct {
    ID        uuid.UUID `json:"id"`
    Email     string    `json:"email"`
    CreatedAt time.Time `json:"created_at"`
}

// NewUser creates a User with a generated UUID and current timestamp.
//
// Email validation is performed during persistence, not at creation.
func NewUser(email string) *User {
    return &User{
        ID:        uuid.New(),
        Email:     email,
        CreatedAt: time.Now(),
    }
}
```

### Comments

```go
// Good: Explain WHY, not WHAT
// Hash password using bcrypt to protect against rainbow table attacks
hashedPassword, err := bcrypt.GenerateFromPassword(password, bcrypt.DefaultCost)

// Bad: Restating the code
// Hash the password
hashedPassword, err := bcrypt.GenerateFromPassword(password, bcrypt.DefaultCost)

// Use godoc comments for exported identifiers
// Use regular comments for implementation details
```

## Common Patterns

### Constructor Pattern

```go
// NewService creates a Service with required dependencies.
func NewService(repo Repository, logger *slog.Logger) *Service {
    return &Service{
        repo:   repo,
        logger: logger,
    }
}

// With options pattern for complex constructors
type Option func(*Service)

func WithCache(cache Cache) Option {
    return func(s *Service) {
        s.cache = cache
    }
}

func NewServiceWithOptions(repo Repository, opts ...Option) *Service {
    s := &Service{repo: repo}
    for _, opt := range opts {
        opt(s)
    }
    return s
}
```

### Interface Segregation

```go
// Good: Small, focused interfaces
type Reader interface {
    Read(ctx context.Context, id string) (*Data, error)
}

type Writer interface {
    Write(ctx context.Context, data *Data) error
}

type ReadWriter interface {
    Reader
    Writer
}

// Accept interfaces, return structs
func ProcessData(r Reader, id string) (*Result, error) {
    data, err := r.Read(context.Background(), id)
    // ...
}
```

### Middleware Pattern

```go
type HandlerFunc func(http.ResponseWriter, *http.Request)

type Middleware func(HandlerFunc) HandlerFunc

func LoggingMiddleware(logger *slog.Logger) Middleware {
    return func(next HandlerFunc) HandlerFunc {
        return func(w http.ResponseWriter, r *http.Request) {
            start := time.Now()
            next(w, r)
            logger.Info("request",
                "method", r.Method,
                "path", r.URL.Path,
                "duration", time.Since(start),
            )
        }
    }
}

// Chain middlewares
func Chain(h HandlerFunc, middlewares ...Middleware) HandlerFunc {
    for i := len(middlewares) - 1; i >= 0; i-- {
        h = middlewares[i](h)
    }
    return h
}
```

## Build and Deployment

### Makefile

```makefile
.PHONY: build test lint clean

# Build binary
build:
	go build -o bin/server cmd/server/main.go

# Run tests
test:
	go test -v -race -coverprofile=coverage.out ./...

# Run linter
lint:
	golangci-lint run ./...

# Format code
fmt:
	gofmt -s -w .
	goimports -w .

# Clean build artifacts
clean:
	rm -rf bin/ coverage.out

# Install tools
tools:
	go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
	go install golang.org/x/tools/cmd/goimports@latest
```

### Build Tags

```go
//go:build integration
// +build integration

package user_test

// Integration tests only run with: go test -tags=integration
```

## Anti-Patterns to Avoid

❌ **Don't do this:**

```go
// Panic in library code (use errors)
func GetUser(id string) *User {
    user := findUser(id)
    if user == nil {
        panic("user not found")
    }
    return user
}

// Ignoring errors
result, _ := doSomething()

// Naked returns in long functions
func calculate(a, b int) (result int) {
    // ... 50 lines of code ...
    return
}

// Global mutable state
var users = make(map[string]*User)
```

✅ **Do this instead:**

```go
// Return errors explicitly
func GetUser(id string) (*User, error) {
    user := findUser(id)
    if user == nil {
        return nil, ErrUserNotFound
    }
    return user, nil
}

// Handle all errors
result, err := doSomething()
if err != nil {
    return fmt.Errorf("operation failed: %w", err)
}

// Explicit returns
func calculate(a, b int) int {
    result := a + b
    return result
}

// Dependency injection
type UserService struct {
    users map[string]*User
}
```

## Tools and Ecosystem

### Essential Tools

```bash
# Format and imports
go install golang.org/x/tools/cmd/goimports@latest

# Linting
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest

# Testing utilities
go install github.com/stretchr/testify@latest

# Code generation (if needed)
go install github.com/golang/mock/mockgen@latest

# Hot reload for development
go install github.com/cosmtrek/air@latest
```

### IDE Configuration

```json
// VSCode settings.json
{
  "go.useLanguageServer": true,
  "go.lintTool": "golangci-lint",
  "go.lintOnSave": "package",
  "go.formatTool": "goimports",
  "editor.formatOnSave": true,
  "go.testFlags": ["-v", "-race"],
  "go.coverOnSave": true
}
```

## Security Best Practices

```go
// Use crypto/rand for random values
import "crypto/rand"

func generateToken() (string, error) {
    b := make([]byte, 32)
    if _, err := rand.Read(b); err != nil {
        return "", err
    }
    return base64.URLEncoding.EncodeToString(b), nil
}

// Validate and sanitise inputs
func sanitiseUserInput(input string) string {
    return html.EscapeString(strings.TrimSpace(input))
}

// Use prepared statements for SQL
stmt, err := db.PrepareContext(ctx, "SELECT * FROM users WHERE id = $1")
defer stmt.Close()

// Set timeouts on contexts
ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
defer cancel()
```

## Alignment with Core Principles

- **SOLID Principles**: Single responsibility through package design, dependency inversion via interfaces
- **DRY**: Avoid duplication through proper abstraction and generics
- **YAGNI**: Build what you need now, Go's simplicity encourages this
- **KISS**: Go's design philosophy emphasises simplicity
- **Test Pyramid**: 70% unit (table-driven), 20% integration (with build tags), 10% e2e

## References

- [Effective Go](https://go.dev/doc/effective_go)
- [Go Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments)
- [Standard Go Project Layout](https://github.com/golang-standards/project-layout)
- [Uber Go Style Guide](https://github.com/uber-go/guide/blob/master/style.md)
