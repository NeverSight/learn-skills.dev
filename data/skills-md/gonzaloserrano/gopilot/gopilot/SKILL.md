---
name: gopilot
description: "v1.0.21 — Go programming language skill for writing idiomatic Go code, code review, error handling, testing, concurrency, security, and program design. Use when writing, reviewing, debugging, or asking about Go code — even if the user doesn't explicitly mention 'Go best practices'. Also use when: reviewing Go PRs, debugging Go tests, fixing Go errors, designing Go APIs, implementing security-sensitive code, handling user input, authentication, sessions, cryptography, building resource-oriented gRPC APIs with Google AIP standards, configuring golangci-lint, setting up structured logging with slog, or any question about Go idioms and patterns. Covers table-driven tests, error wrapping, goroutine patterns, interface design, generics, iterators, stdlib patterns up to Go 1.26, OWASP security practices, and Google AIP (API Improvement Proposals) with einride/aip-go for pagination, filtering, ordering, field masks, and resource names."
---

# Go Engineering

## Design Guidelines

- Keep things simple.
   - Prefer stateless, pure functions over stateful structs with methods if no state is needed to solve the problem. 
   - Prefer synchronous code to concurrent code, an obvious concurrency pattern applies.
   - Prefer simple APIs and small interfaces.
   - Make the zero value useful: `bytes.Buffer` and `sync.Mutex` work without init. When zero values compose, there's less API.
   - Avoid external dependencies. A little copying is better than a little dependency.
- Clear is better than clever. Maintainability and readibility are important.
- Don't just check errors, handle them gracefully.
- Design the architecture, name the components, document the details: Good names carry the weight of expressing your design. If names are good, the design is clear on the page.
- Reduce nesting by using guard clauses.
    - Invert conditions for early return
    - In loops, use early `continue` for invalid items instead of nesting
    - Max 2-3 nesting levels
    - Extract helpers for long methods

## Code Style

- Avoid stuttering: `http.Client` not `http.HTTPClient`
- Getters: `Foo()` not `GetFoo()`
- Receiver: short (1-2 chars), consistent across type methods
- `Must` prefix for panicking functions
- Enums: use `iota + 1` to start at one, distinguishing intentional values from zero default

## Error Handling

- Errors are values. Design APIs around that.
- Wrap with context: `fmt.Errorf("get config %s: %w", name, err)`
- Sentinel errors: `var ErrNotFound = errors.New("not found")`
- Check with `errors.Is(err, ErrNotFound)` or `errors.As(err, &target)`, or use generic `errors.AsType[T]` (Go 1.26+)
- Static errors: prefer `errors.New` over `fmt.Errorf` without formatting
- Join multiple errors: `err := errors.Join(err1, err2, err3)` (Go 1.20+)
- Error strings: lowercase, no punctuation
- Avoid "failed to" prefixes - they accumulate through the stack (`"connect: %w"` not `"failed to connect: %w"`)
- Always check errors immediately before using returned values — in Go 1.21–1.24, the compiler could reorder statements and execute method calls on nil receivers before the error check ran, causing panics (fixed in Go 1.25)

### Error Strategy (Opaque Errors First)

Prefer **opaque error handling**: treat errors as opaque values, don't inspect internals. This minimizes coupling.

Three strategies in order of preference:

1. **Opaque errors** (preferred): return and wrap errors without exposing type or value. Callers only check `err != nil`.
2. **Sentinel errors** (`var ErrNotFound = errors.New(...)`): use sparingly for expected conditions callers must distinguish. They become public API.
3. **Error types** (`type NotFoundError struct{...}`): use when callers need structured context. Also public API — avoid when opaque or sentinel suffices.

### Assert Behavior, Not Type

When you must inspect errors beyond `errors.Is`/`errors.As`, assert on **behavior interfaces** instead of concrete types:

```go
type temporary interface {
    Temporary() bool
}

func IsTemporary(err error) bool {
    te, ok := err.(temporary)
    return ok && te.Temporary()
}
```

### Handle Errors Once

An error should be handled exactly once. Handling = logging, returning, or degrading gracefully. Never log and return — duplicates without useful context.

```go
// Bad: logs AND returns
if err != nil {
    log.Printf("connect failed: %v", err)
    return fmt.Errorf("connect: %w", err)
}

// Good: wrap and return; let the top-level caller log
if err != nil {
    return fmt.Errorf("connect to %s: %w", addr, err)
}
```

Wrap with context at each layer; log/handle only at the application boundary.

### Context with Cause (Go 1.21+)

Propagate cancellation reasons through context:

```go
ctx, cancel := context.WithCancelCause(parent)
cancel(fmt.Errorf("shutdown: %w", reason))

// Later retrieve the cause
if cause := context.Cause(ctx); cause != nil {
    log.Printf("context cancelled: %v", cause)
}
```

## Generics

- Type parameters: `func Min[T cmp.Ordered] (a, b T) T`
- Use `comparable` for map keys, `cmp.Ordered` for sortable types
- Custom constraints: `type Number interface { ~int | ~int64 | ~float64 }`
- Generic type alias (Go 1.24+): `type Set[T comparable] = map[T]struct{}`
- Self-referential constraints (Go 1.26+): `type Adder[A Adder[A]] interface { Add(A) A }`
- Prefer concrete types when generics add no value
- Use `any` sparingly; prefer specific constraints

## Built-in Functions

- `min(a, b, c)` and `max(a, b, c)` - compute smallest/largest values (Go 1.21+)
- `clear(m)` - delete all map entries; `clear(s)` - zero all slice elements (Go 1.21+)
- `new(expr)` - allocate and initialize with value (Go 1.26+): `ptr := new(computeValue())`

## Testing

### Table-Driven Tests
```go
func TestFoo(t *testing.T) {
    testCases := []struct {
        name           string
        input          string
        expectedResult string
        expectedError  error
    }{
        {
            name:          "EmptyInput",
            input:         "",
            expectedError: ErrEmpty,
        },
        {
            name:           "ValidInput",
            input:          "hello",
            expectedResult: "HELLO",
        },
    }
    for _, tc := range testCases {
        t.Run(tc.name, func(t *testing.T) {
            t.Parallel()
            got, err := Foo(tc.input)
            if tc.expectedError != nil {
                require.ErrorIs(t, err, tc.expectedError)
                return
            }
            require.NoError(t, err)
            require.Equal(t, tc.expectedResult, got)
        })
    }
}
```

### Benchmarks (Go 1.24+)
```go
func BenchmarkFoo(b *testing.B) {
    for b.Loop() {  // Cleaner than for i := 0; i < b.N; i++
        Foo()
    }
}
```
Benefits: single execution per `-count`, prevents compiler optimizations away.

### Assertions
- Use the testify library for conciseness. Use `require` for fatal assertions, `assert` for non-fatal
- `require.ErrorIs` for sentinel errors (not string matching)
- `require.JSONEq`/`require.YAMLEq` for semantic comparison
- Use `testdata/` folders for expected values
- Use `embed.FS` for test data files

### Practices
- Test function names: use `TestFooBar` (PascalCase), not `TestFoo_Bar` (no underscores)
- `t.Helper()` in helper functions
- `t.Cleanup()` for resource cleanup
- `t.Context()` for test-scoped context (Go 1.24+)
- `t.Chdir()` for temp directory changes (Go 1.24+)
- `t.ArtifactDir()` for test output files (Go 1.26+)
- `t.Parallel()` for independent tests
- `-race` flag always
- Don't test stdlib; test YOUR code
- Bug fix → add regression test first
- Concurrent code needs concurrent tests

### Testing Concurrent Code with synctest (Go 1.25+)

`testing/synctest` creates an isolated "bubble" with virtualized time. The fake clock advances automatically when all goroutines in the bubble are blocked.

```go
import "testing/synctest"

func TestPeriodicWorker(t *testing.T) {
    synctest.Test(t, func(t *testing.T) {
        var count atomic.Int32
        go func() {
            for {
                time.Sleep(time.Second)
                count.Add(1)
            }
        }()

        // Fake clock advances 5s instantly (no real waiting)
        time.Sleep(5 * time.Second)
        synctest.Wait() // wait for all goroutines to settle
        require.Equal(t, int32(5), count.Load())
    })
}
```

Key rules:
- `synctest.Wait()` blocks until all bubble goroutines are idle
- `time.Sleep`, `time.After`, `time.NewTimer`, `time.NewTicker` all use the fake clock inside the bubble
- Goroutines spawned inside the bubble belong to it; goroutines outside are unaffected
- Blocking on I/O or syscalls does NOT advance the clock — only channel ops, sleeps, and sync primitives do
- Prefer `synctest.Test` over manual `timeNow` mocking for new code

## Concurrency

Share memory by communicating — channels orchestrate; mutexes serialize.

- Use `errgroup.WithContext` to launch goroutines that return errors; `g.Wait()` returns first error
- `sync.WaitGroup.Go()` (Go 1.25+): combines Add(1) + goroutine launch
  ```go
  var wg sync.WaitGroup
  wg.Go(func() { work() })  // Combines Add(1) + go
  wg.Wait()
  ```
- Make goroutine lifetime explicit; document when/why they exit
- Avoid goroutine leaks (blocked on unreachable channels); detect with `GOEXPERIMENT=goroutineleakprofile` (Go 1.26+)
- Use `context.Context` for cancellation; subscribe to `context.Done()` for graceful shutdown
- Prefer synchronous functions; let callers add concurrency if needed
- `sync.Mutex`/`RWMutex` for shared state protection; zero value is ready to use
- `RWMutex` when reads far outnumber writes
- Pointer receivers with mutexes (prevents struct copy which breaks lock semantics)
- Keep critical sections small; avoid holding locks across I/O
- `sync.Once` for one-time initialization; helpers: `sync.OnceFunc()`, `sync.OnceValue()`, `sync.OnceValues()` (Go 1.21+)
- `atomic` for primitive counters (simpler than mutex for single values)
- Don't embed mutex (exposes Lock/Unlock to callers); use a named field instead
- Channels: sender closes, receiver checks; never close from receiver side or with multiple concurrent senders

### Channel Axioms

| Operation | nil channel | closed channel |
|-----------|-------------|----------------|
| Send      | blocks forever | **panics** |
| Receive   | blocks forever | returns zero value |
| Close     | **panics** | **panics** |

- Nil channels are useful in `select` to disable a case
- Use `for range ch` to receive until closed
- Check closure with `v, ok := <-ch`

## Iterators (Go 1.22+)

### Range Over Integers (Go 1.22+)
```go
for i := range 10 {
    fmt.Println(i)  // 0..9
}
```

### Range Over Functions (Go 1.23+)
```go
// String iterators
for line := range strings.Lines(s) { }
for part := range strings.SplitSeq(s, sep) { }
for field := range strings.FieldsSeq(s) { }

// Slice iterators
for i, v := range slices.All(items) { }
for v := range slices.Values(items) { }
for v := range slices.Backward(items) { }
for chunk := range slices.Chunk(items, 3) { }

// Map iterators
for k, v := range maps.All(m) { }
for k := range maps.Keys(m) { }
for v := range maps.Values(m) { }

// Collect iterator to slice
keys := slices.Collect(maps.Keys(m))
sorted := slices.Sorted(maps.Keys(m))

// Custom iterator
func (s *Set[T]) All() iter.Seq[T] {
    return func(yield func(T) bool) {
        for v := range s.items {
            if !yield(v) {
                return
            }
        }
    }
}
```

## Interface Design

- Accept interfaces, return concrete types
- Define interfaces at the consumer, not the provider; keep them small (1-2 methods)
- Compile-time interface check: `var _ http.Handler = (*MyHandler)(nil)`
- For single-method dependencies, use function types instead of interfaces
- Don't embed types in exported structs—exposes methods and breaks API compatibility

## Slice & Map Patterns

- Pre-allocate when size known: `make([]User, 0, len(ids))`
- Nil vs empty: `var t []string` (nil, JSON null) vs `t := []string{}` (non-nil, JSON `[]`)
- Copy at boundaries with `slices.Clone(items)` to prevent external mutations
- Prefer `strings.Cut(s, "/")` over `strings.Split` for prefix/suffix extraction
- Append handles nil: `var items []Item; items = append(items, newItem)`

## Common Patterns

### Options Pattern
Define `type Option func(*Config)`. Create `WithX` functions returning `Option` that set fields. Constructor takes `...Option`, applies each to default config.

### Default Values (Go 1.22+)
Use `cmp.Or(a, b, c)` to return first non-zero value—e.g., `cmp.Or(cfg.Port, envPort, 8080)`.

### Context Usage
- First parameter: `func Foo(ctx context.Context, ...)`
- Don't store in structs
- Use for cancellation, deadlines, request-scoped values only

### HTTP Best Practices
- Use `http.Server{}` with explicit `ReadTimeout`/`WriteTimeout`; avoid `http.ListenAndServe`
- Always `defer resp.Body.Close()` after checking error
- Accept `*http.Client` as dependency for testability

### HTTP Routing (Go 1.22+)
```go
// Method-based routing with path patterns
mux.HandleFunc("POST /items/create", createHandler)
mux.HandleFunc("GET /items/{id}", getHandler)
mux.HandleFunc("GET /files/{path...}", serveFiles)  // Greedy wildcard

// Extract path values
func getHandler(w http.ResponseWriter, r *http.Request) {
    id := r.PathValue("id")
}
```

### AIP: Resource-Oriented gRPC APIs

For building resource-oriented gRPC APIs following [Google AIP](https://google.aip.dev/) standards, use [einride/aip-go](https://github.com/einride/aip-go) (`go.einride.tech/aip`).

- **Resource names** (AIP-122): hierarchical paths like `publishers/123/books/les-miserables`; use `resourcename.Sscan`/`Sprint`/`Match` for parsing and construction
- **Standard methods**: Get (131), List (132), Create (133), Update (134), Delete (135) — prefer these over custom methods
- **Pagination** (AIP-158): implement from day one with `pagination.ParsePageToken`; opaque tokens, coerce oversized `page_size`, never require `page_size`
- **Filtering** (AIP-160): parse with `filtering.ParseFilter` and typed `Declarations`; validate server-side, return `INVALID_ARGUMENT`
- **Ordering** (AIP-132): parse with `ordering.ParseOrderBy`; validate against allowed fields with `ValidateForPaths`
- **Field masks** (AIP-134, AIP-161): use `fieldmask.Update` for partial updates, `fieldmask.Validate` for path validation; prefer `PATCH` over `PUT`
- **Field behavior** (AIP-203): annotate every field — `REQUIRED`, `OPTIONAL`, `OUTPUT_ONLY`, `IMMUTABLE`, or `IDENTIFIER`

See [AIP reference](reference/go-aip.md) for detailed patterns, code examples, and best practices.

### CSRF Protection (Go 1.25+)
```go
import "net/http"

handler := http.CrossOriginProtection(myHandler)
// Rejects non-safe cross-origin requests using Fetch metadata
```

### Directory-Scoped File Access (Go 1.24+)
```go
root, err := os.OpenRoot("/var/data")
if err != nil {
    return err
}
f, err := root.Open("file.txt")  // Can't escape /var/data
```
Prevents path traversal attacks; works like a chroot.

### Cleanup Functions (Go 1.24+)
```go
runtime.AddCleanup(obj, func() { cleanup() })
```
Advantages over `SetFinalizer`: multiple cleanups per object, works with interior pointers, no cycle leaks, faster.

## Structured Logging (log/slog)

- Use `slog.Info("msg", "key", value, "key2", value2)` with key-value pairs
- Add persistent attributes: `logger := slog.With("service", "api")`
- JSON output: `slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{Level: slog.LevelDebug}))`

## Common Gotchas

- **Check errors immediately** (Go 1.25 fixed compiler bug): always check `err != nil` before using any returned values
  ```go
  // WRONG: could execute f.Name() before err check in Go 1.21-1.24
  f, err := os.Open("file")
  name := f.Name()
  if err != nil { return }

  // CORRECT: check immediately
  f, err := os.Open("file")
  if err != nil { return }
  name := f.Name()
  ```
- `time.Ticker`: always call `Stop()` to prevent leaks
- Slices hold refs to backing arrays (can retain large memory)
- `nil` interface vs `nil` concrete: `var err error = (*MyError)(nil)` → `err != nil` is true
- Loop variables: each iteration has own copy (Go 1.22+); older versions share
- Timer/Ticker channels: capacity 0 (Go 1.23+); previously capacity 1
- `init()` is an anti-pattern; prefer explicit initialization

## Linting

Use `golangci-lint` with recommended linters: errcheck, govet, staticcheck, gocritic, gofumpt, wrapcheck, errorlint. See [linting reference](reference/linting.md) for the full `.golangci.yml` config template and commands.

## Pre-Commit

Check for Makefile targets first (`make help`, or read Makefile). Common targets:
- `make lint` or `make check`
- `make test`
- `make build`

Fallback if no Makefile:
1. `go build ./...`
2. `go test -v -race ./...`
3. `golangci-lint run`
4. `go fix ./...` (Go 1.26+: modernizes code to latest idioms)
5. `gofmt -w .` or `goimports -w .`
6. `go mod tidy`

## Performance

### Profile-Guided Optimization (PGO)
```bash
# Collect profile
go test -cpuprofile=default.pgo

# PGO automatically enabled if default.pgo exists in main package
go build  # Uses default.pgo

# Typical 2-7% performance improvement
```

## Security

Based on OWASP Go Secure Coding Practices. Read the linked reference for each topic.

### Quick Checklist

**Input/Output:**
- [ ] All user input validated server-side
- [ ] SQL queries use prepared statements only
- [ ] XSS protection via `html/template`
- [ ] CSRF tokens on state-changing requests
- [ ] File paths validated against traversal (`os.OpenRoot` Go 1.24+)

**Auth/Sessions:**
- [ ] Passwords hashed with bcrypt/Argon2/PBKDF2
- [ ] `crypto/rand` for all tokens/session IDs (`crypto/rand.Text()` Go 1.24+)
- [ ] Secure cookie flags (HttpOnly, Secure, SameSite)
- [ ] Session expiration enforced

**Communication:**
- [ ] HTTPS/TLS everywhere, TLS 1.2+ only (post-quantum ML-KEM default Go 1.24+)
- [ ] HSTS header set
- [ ] `InsecureSkipVerify = false`

**Data Protection:**
- [ ] Secrets in environment variables, never in logs/errors
- [ ] Generic error messages to users

### Detailed Guides

Read the relevant guide when implementing security-sensitive features. Each covers patterns, code examples, and common pitfalls for its domain.

- [Input Validation](reference/input-validation.md) — read when accepting user input: whitelisting, boundary checks, escaping
- [Database Security](reference/database-security.md) — read when writing SQL or database code: prepared statements, parameterized queries
- [Authentication](reference/authentication.md) — read when implementing login, signup, or password flows: bcrypt, Argon2, password policies
- [Cryptography](reference/cryptography.md) — read when generating tokens, secrets, or random values: `crypto/rand`, never `math/rand` for security
- [Session Management](reference/session-management.md) — read when implementing user sessions: secure cookies, session lifecycle, JWT
- [TLS/HTTPS](reference/tls-https.md) — read when configuring servers or HTTP clients: TLS config, HSTS, mTLS, post-quantum key exchanges
- [CSRF Protection](reference/csrf.md) — read when building forms or state-changing endpoints: token generation, `http.CrossOriginProtection` (Go 1.25+)
- [Secure Error Handling](reference/error-handling.md) — read when designing error responses: generic user messages, detailed server logs
- [File Security](reference/file-security.md) — read when handling file uploads or filesystem access: path traversal prevention, `os.OpenRoot`
- [Security Logging](reference/logging.md) — read when implementing audit trails: what to log, what never to log, redaction
- [Access Control](reference/access-control.md) — read when implementing authorization: RBAC, ABAC, principle of least privilege
- [XSS Prevention](reference/xss.md) — read when rendering user content in HTML: `html/template`, CSP, sanitization

### Security Tools

| Tool | Purpose | Command |
|------|---------|---------|
| gosec | Security scanner | `gosec ./...` |
| govulncheck | Vulnerability scanner | `govulncheck ./...` |
| trivy | Container/dep scanner | `trivy fs .` |
