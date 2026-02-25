---
name: golang
description: Opinionated Go coding standards, conventions, and best practices. Use this skill whenever writing, reviewing, or modifying Go code (.go files). Covers project structure, code style, error handling, testing, linting, concurrency, dependency management, and general Go idioms. Trigger on any Go-related task including writing new Go code, reviewing Go PRs, fixing Go bugs, or scaffolding Go projects.
---

# Go — Opinionated Coding Standards

## Execution Order

When implementing or changing Go code, run this sequence unless project tooling defines a different workflow:

1. Detect project commands in this order:
   - `make` targets (if `Makefile` exists)
   - `mage` targets (if `magefile.go` exists)
   - raw Go commands
2. Run checks in this order: `fmt` -> `lint` -> `test` -> `build`

Default fallback commands when project tooling is missing:

- Format: `golangci-lint fmt`
- Lint: `golangci-lint run`
- Test: `go test ./...`
- Build: `go build ./...`

## Project Structure

Choose structure based on project type:

**Libraries / small tools** — flat structure:
```
mylib/
  mylib.go
  mylib_test.go
  helpers.go
```

**Services / microservices** — standard layout:
```
cmd/
  server/main.go
  worker/main.go
internal/
  handler/
  service/
  repository/
  model/
go.mod
```

Rules:
- Use `internal/` for private packages.
- `cmd/` contains only `main.go` entrypoints. Keep them thin — parse config, wire dependencies, call `run()`.
- Group by domain, not by technical layer, when the service grows beyond a few packages.
- One package = one responsibility. If a package name needs "and" to describe it, split it.

## Code Style & Naming

- Format code with `golangci-lint fmt` (runs `gofumpt` + `goimports` via config).
- Prefer descriptive names over short names, especially for exported symbols and function parameters.
  - Acceptable short names: `ctx`, `err`, `t`, `i`, `n` for well-established Go idioms.
  - Bad: `func Process(d []byte, f string)` — Good: `func Process(data []byte, filename string)`
- Exported names must be self-documenting. Comment every exported type, function, and constant.
- Unexported helpers can be terser but must still be clear in context.
- Avoid stuttering: `user.User` is fine, `user.UserService` is not — use `user.Service`.
- Acronyms are all-caps: `HTTPClient`, `ID`, `URL`. Not `HttpClient`, `Id`, `Url`.
- Struct tags use `snake_case` for JSON, YAML, XML, and BSON.

### Constants — No `iota`

Never use `iota`. It is implicit, fragile to reordering, and produces opaque values that are hard to grep, log, and debug. Always use explicit string-typed constants.

```go
// Bad — iota: implicit values, break on reorder, meaningless in logs
const (
    assertJSON assertType = iota
    assertYAML
    assertHTML
    assertFile
)

// Good — explicit string constants
const (
    assertJSON assertType = "json"
    assertYAML assertType = "yaml"
    assertHTML assertType = "html"
    assertFile assertType = "file"
)
```

Do not use `iota` for new code in this skill.

## Interfaces

- Keep interfaces small: 1-2 methods. Compose larger interfaces from small ones.
- Accept interfaces, return concrete structs.
- Define interfaces at the **consumer** side, not the implementation side.
- Name single-method interfaces with the `-er` suffix: `Reader`, `Writer`, `Closer`, `Validator`.

```go
// Defined where it's used, not where it's implemented
type OrderStore interface {
    GetOrder(ctx context.Context, id string) (*Order, error)
}

type OrderService struct {
    store OrderStore // depends on interface
}
```

## Error Handling

Use sentinel errors + wrapping with `fmt.Errorf` and `%w`.

```go
var (
    ErrNotFound  = errors.New("not found")
    ErrConflict  = errors.New("conflict")
    ErrForbidden = errors.New("forbidden")
)

func (s *Service) GetUser(ctx context.Context, id string) (*User, error) {
    user, err := s.repo.Find(ctx, id)
    if err != nil {
        return nil, fmt.Errorf("get user %s: %w", id, err)
    }
    return user, nil
}
```

- Always wrap errors with context about what operation failed.
- Never discard errors silently. If intentionally ignoring, assign to `_` with a comment.
- No `pkg/errors` or third-party error packages. Stdlib is sufficient.
- Return errors; do not panic. Reserve `panic` for truly unrecoverable programmer errors.
- Error messages are lowercase, no punctuation: `"get user: not found"`.

## Testing

Use stdlib `testing` + `testastic`. Test the public API through external `_test` packages. Use same-package tests only for complex internals that are not meaningfully reachable through the public surface. Use `// given:` / `// when:` / `// then:` comments in every test case. Hand-roll mocks, no additional mocking frameworks.

Choose the right testing approach based on project type:

- **Libraries / packages** — unit tests. Test the public API through `_test` package suffix. See [references/unit-testing.md](references/unit-testing.md).
- **Services / microservices** — integration tests. Test components working together (handlers, DB, external APIs). See [references/integration-testing.md](references/integration-testing.md).

### Test Data Isolation

- Each test/subtest must own its test data (`actual`, `expected`, fixtures).
- Do not share package-level test payload constants/variables across tests.
- Do not reuse the same `testdata/...` fixture path across multiple tests.
- Fixture content must be unique per test case; avoid copy-paste fixtures with identical bytes.
- If two tests need similar data, create separate fixtures and change at least one scenario-relevant field so intent stays explicit.
- Repetition is acceptable only in non-executable documentation comments/examples.

## Linting

Use `golangci-lint` v2. Run `golangci-lint run` for linting and `golangci-lint fmt` for formatting.

For the full reference config, enabled/disabled linter rationale, and rules, see [references/linting.md](references/linting.md).

Key rules:
- All code must pass `golangci-lint run` before committing.
- No `//nolint` without a comment explaining why.
- Test files have relaxed rules (funlen, dupl, mnd, wrapcheck, err113, gocognit, gosec excluded).

## Context

- `ctx context.Context` is always the first parameter. No exceptions.
- Never store `context.Context` in a struct. Pass it through function calls.
- Use `context.WithTimeout` or `context.WithCancel` to scope work.
- Respect context cancellation: check `ctx.Err()` or `select` on `ctx.Done()` in long operations.

## Concurrency

- Do not start goroutines without a clear ownership and shutdown strategy.
- Use `errgroup.Group` for concurrent operations that can fail.
- Channels for communication, mutexes for state protection. Do not mix unnecessarily.
- Always handle goroutine lifecycle: `context.Context` for cancellation, `sync.WaitGroup` or `errgroup` for joining.
- Prefer `sync.Once` over `init()` for lazy initialization.
- Never fire-and-forget goroutines in production code.
- Buffer channels only with a clear reason and known capacity.

```go
g, ctx := errgroup.WithContext(ctx)
for _, item := range items {
    g.Go(func() error {
        return process(ctx, item)
    })
}
if err := g.Wait(); err != nil {
    return fmt.Errorf("process items: %w", err)
}
```

## Dependency Injection

- Constructor-based injection. No global mutable state. No DI frameworks.
- Constructors return concrete types, accept interfaces.
- Wire dependencies in `main()` or a dedicated `run()` function in `cmd/`.

```go
func NewOrderService(store OrderStore) *OrderService {
    return &OrderService{store: store}
}
```

## Options Pattern

Use the functional options pattern for configurable constructors or functions with optional parameters. Do not use config structs with zero-value ambiguity.

```go
// Option type is an unexported function that modifies config.
type Option func(*serverConfig)

// serverConfig holds all configurable fields with sensible defaults.
type serverConfig struct {
    port         int
    readTimeout  time.Duration
    writeTimeout time.Duration
}

// Exported option constructors — one per configurable field.
func WithPort(port int) Option {
    return func(c *serverConfig) {
        c.port = port
    }
}

func WithReadTimeout(timeout time.Duration) Option {
    return func(c *serverConfig) {
        c.readTimeout = timeout
    }
}

// Constructor applies defaults, then options.
func NewServer(opts ...Option) *Server {
    cfg := serverConfig{
        port:         8080,
        readTimeout:  5 * time.Second,
        writeTimeout: 10 * time.Second,
    }
    for _, opt := range opts {
        opt(&cfg)
    }

    return &Server{cfg: cfg}
}

// Usage: clean, readable, self-documenting.
srv := NewServer(
    WithPort(9090),
    WithReadTimeout(10 * time.Second),
)
```

Rules:
- Config struct is unexported. Options are the public API.
- Set sensible defaults in the constructor, not in each option.
- Each option constructor is a `With*` function returning `Option`.
- Option constructors return the `Option` type (not the concrete closure) — this is a valid exception to "return concrete types".
- Use this pattern when a function has more than 2-3 optional parameters. Do not use it for required parameters — those stay as regular arguments.

## Logging

Use `log/slog` with context-aware logging. Configure the default logger once in `main()` via `slog.SetDefault()`. Always log with context using `slog.InfoContext(ctx, ...)`, `slog.ErrorContext(ctx, ...)`, etc. Do not pass `*slog.Logger` as a parameter — `ctx` already carries correlation IDs, trace IDs, and other request-scoped data.

For setup patterns, handler configuration, and context attribute extraction, see [references/logging.md](references/logging.md).

## No init(), No Globals

- No `init()` functions. They make testing hard and hide side effects.
- No mutable global state. Pass dependencies explicitly.
- Package-level `var` is acceptable only for sentinel errors, constants, and `sync.Once`.

## Dependency Management

- Use Go modules (`go.mod`). Run `go mod tidy` before committing.
- Pin direct dependency versions. Do not use `latest`.
- Review `go.sum` changes in PRs.
- Avoid vendoring unless required by build environment constraints.
- Minimize external dependencies. Prefer stdlib when reasonable.

## Ask Before Proceeding

Ask the user before:

- Adding a new third-party dependency.
- Introducing or switching framework-level choices (router, ORM, logging stack, queue client).
- Using same-package tests for internals as the primary strategy in a package.
- Choosing integration test runtime strategy (containers, docker-compose, external shared services).

## Done Criteria

A Go change is done when all are true:

- Formatting passes (`golangci-lint fmt` or project equivalent).
- Lint passes (`golangci-lint run` or project equivalent).
- Relevant tests pass (`go test ./...` or project equivalent).
- Build passes (`go build ./...` or project equivalent for changed binaries/packages).
- No unresolved placeholders, partial implementations, or undocumented exceptions to rules.
