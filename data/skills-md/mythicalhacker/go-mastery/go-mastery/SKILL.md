---
name: go-mastery
description: >
  The definitive Go (Golang) development skill for producing production-grade, idiomatic, high-performance Go code across any domain — APIs, CLIs, distributed systems, real-time applications, AI/ML infrastructure, trading systems, SaaS platforms, automation tools, data pipelines, and more. Trigger this skill whenever writing, reviewing, debugging, or architecting ANY Go code. Also trigger for: Go project setup, Go concurrency design, Go performance optimization, Go error handling patterns, Go testing strategies, Go database access, Go HTTP servers/clients, Go WebSocket implementations, Go gRPC services, Go CLI tools, Go cross-platform builds (especially Windows), Go generics, Go code review, or any task involving .go files. Even if the user doesn't explicitly mention "Go best practices," use this skill whenever Go code is being produced to ensure it meets production standards.
---

# Go Mastery Skill

Write production-grade, idiomatic Go for any purpose. This skill encodes the collective wisdom of the Go ecosystem as of Go 1.22+ (2024-2026).

> **Go version baseline: 1.22 | Features through: 1.26 | Updated: February 2026**

**Before writing any Go code, internalize the principles below. For deep dives on specific topics, read the referenced files.**

## Reference Files — Read As Needed

| File | When to Read |
|------|-------------|
| `references/concurrency.md` | Any goroutine, channel, sync primitive, or parallel work |
| `references/http-and-apis.md` | HTTP servers, routers, middleware, REST/gRPC APIs, WebSockets |
| `references/database.md` | SQL, ORMs, connection pools, migrations, transactions |
| `references/testing.md` | Unit tests, integration tests, benchmarks, fuzzing |
| `references/errors-and-resilience.md` | Error handling, retries, circuit breakers, graceful degradation |
| `references/performance.md` | Profiling, allocation reduction, GC tuning, benchmarking |
| `references/cli-and-config.md` | CLI frameworks, configuration, environment management |
| `references/project-patterns.md` | Project layout, DI, plugin systems, code generation |
| `references/platform-and-build.md` | Cross-compilation, Windows specifics, embedding, distribution |
| `references/security.md` | Auth, secrets, input validation, TLS, OWASP patterns |
| `references/modern-go.md` | Go 1.21–1.26 features, deprecated patterns, what pre-training gets wrong |
| `references/advanced-patterns.md` | Generics, state machines, streaming, scheduling, AI/LLM integration |
| `references/advanced-resources.md` | Curated external resources: compiler/runtime internals, assembly, unsafe, cgo, Raft, K8s operators, Wasm, cryptography, profiling, books, conferences, academic papers |
| `references/observability.md` | OpenTelemetry setup, tracing, metrics, structured logging with trace correlation, health checks, flight recorder, production instrumentation checklist |
| `references/ecosystem-and-tooling.md` | Curated lists (awesome-go), framework comparisons (web, ORM, CLI, DI, config), style guides, CI/CD, Docker, release management, vulnerability scanning, learning platforms, Go governance |
| `references/internals.md` | GMP scheduler, garbage collector, memory model, stack management, memory allocator, compiler pipeline, unsafe, reflection, compiler directives |
| `references/networking.md` | TCP/UDP servers, net.Conn deadlines, connection pooling, mTLS, Unix sockets, DNS resolvers, custom binary protocols, gnet |
| `references/mcp-and-agents.md` | MCP servers (mcp-go, official SDK), tools/resources/prompts, agent frameworks (ADK, langchaingo, eino), multi-agent patterns, gopls MCP |
| `references/api-design.md` | REST naming, pagination (cursor/offset), RFC 9457 errors, rate limiting, API versioning, OpenAPI codegen (oapi-codegen), backward compatibility, deprecation headers |
| `references/cgo-and-interop.md` | CGo basics, C type mapping, memory management across boundary, pointer passing rules, callbacks, static/dynamic linking, cross-compilation, pure Go alternatives |
| `references/design-patterns.md` | GoF patterns in Go (factory, builder, strategy, observer, decorator), composition over inheritance, decision tree |
| `references/distributed-systems.md` | Raft, outbox pattern, sagas, distributed locking, idempotency, CRDTs, consistent hashing |
| `references/cloud-native.md` | Kubernetes client-go, controller-runtime operators, admission webhooks, leader election, Helm/Kustomize |
| `references/debugging-and-diagnostics.md` | Delve debugger, stack traces, GODEBUG flags, profiling workflow, symptom-to-diagnosis tables |
| `references/style-synthesis.md` | Merged Google + Uber + community style rules, naming, formatting, code organization |
| `references/modules-and-dependencies.md` | go.mod operations, MVS, workspaces, GOPROXY, GOAUTH, vendoring, multi-module monorepos |
| `references/encoding-and-serialization.md` | JSON (v1/v2), Protocol Buffers, MessagePack, CBOR, CSV, YAML, TOML, format decision table |
| `references/wasm-and-embedded.md` | WebAssembly (WASI, browser), go:wasmexport, TinyGo, embedded/IoT patterns |
| `references/migration-guides.md` | Idiomatic Go translations from Python, Java, TypeScript, Rust, C++ — concept maps and traps |
| `references/testing-advanced.md` | Property-based testing (rapid), contract testing (Pact), load testing (Vegeta), chaos engineering, synctest advanced |
| `references/supply-chain-security.md` | govulncheck, SBOM generation, SLSA framework, cosign, reproducible builds, GODEBUG compatibility |
| `references/ebpf.md` | eBPF from Go (cilium/ebpf), bpf2go workflow, tracing, networking, profiling kernel-level |
| `references/event-driven.md` | Kafka, RabbitMQ, NATS consumers/producers, Watermill framework, DLQ, exactly-once patterns |
| `references/data-structures-and-caching.md` | container/heap, container/list, LRU caches, singleflight, sharded maps, bloom filters, weak reference caches, cache strategy patterns (aside/write-through/write-behind) |
| `references/ai-ml-beyond-llm.md` | ONNX Runtime inference, Gonum, vector DB clients, embedding pipelines, ML serving from Go |
| `references/file-io.md` | File operations, io.Reader/Writer composition, buffered I/O, streaming, path handling, os.Root, fs.FS abstraction, fsnotify |

---

## Core Philosophy

Go is deliberately simple. Resist the urge to import complexity from other ecosystems.

1. **Clarity over cleverness.** Code is read 10x more than written. Explicit beats implicit — future maintainers (including your future self) will thank you.
2. **Composition over inheritance.** Embed interfaces and structs; avoid deep hierarchies. Go has no classes, and that's intentional — small, composable pieces beat complex type trees.
3. **Accept interfaces, return structs.** Functions should depend on behavior (interfaces) and expose concrete types. This keeps call sites flexible while keeping implementations discoverable and debuggable.
4. **Make the zero value useful.** Design types so `var x T` is ready to use without initialization. This eliminates an entire class of nil-pointer bugs and makes APIs feel natural (`bytes.Buffer`, `sync.Mutex`, `http.Client` all work at zero value).
5. **Errors are values.** Handle them; never ignore them. Wrap with context using `fmt.Errorf("doing X: %w", err)`. Discarded errors become silent failures that surface hours later in production.
6. **Don't start goroutines you can't stop.** Every goroutine needs a shutdown path via context cancellation or channel close. Leaked goroutines consume memory indefinitely and make graceful shutdown impossible.
7. **stdlib first.** Go's standard library is unusually complete. Reach for third-party libraries only when stdlib genuinely falls short — fewer dependencies mean fewer security audits, fewer version conflicts, and faster builds.
8. **Code isn't done until it's `gofmt`-clean, builds, and vets.** Run `gofmt`/`goimports`, `go build`, `go vet`, `go test -race`, and `golangci-lint` — make them CI gates; the race detector finds bugs invisible to review. When emitting code without tool access, hold the same bar by hand: keep it gofmt-formatted and include **only the imports you actually use** (an unused import is a compile error — the classic slip right after swapping one idiom for another).
9. **Honor the caller's contract, then optimize.** When a task specifies exact identifiers, signatures, output format, or types, reproduce them exactly — even if you would name or structure them differently. Default to the simplest correct solution that satisfies the spec; add abstraction, indirection, or defensive layers only when the task's complexity demands it. Matching the required surface *is* part of correctness — gratuitous renaming or restructuring breaks callers and tests.

---

## Project Structure

Start simple. Add structure only as the project demands it.

### Single Binary (CLI or small service)
```
myapp/
├── go.mod
├── main.go              # package main, entry point
├── app.go               # core application logic
├── app_test.go
└── internal/            # private packages as needed
    └── parser/
        ├── parser.go
        └── parser_test.go
```

### Multi-Binary / Production Service
```
myproject/
├── go.mod
├── cmd/                 # entry points — thin main() functions
│   ├── api-server/
│   │   └── main.go
│   └── worker/
│       └── main.go
├── internal/            # private application code (enforced by compiler)
│   ├── auth/
│   ├── user/            # domain package: handler + service + repo
│   │   ├── handler.go
│   │   ├── service.go
│   │   ├── repository.go
│   │   └── model.go
│   ├── platform/        # cross-cutting: db, cache, logging
│   │   ├── postgres/
│   │   └── redis/
│   └── middleware/
├── pkg/                 # OPTIONAL: public reusable libraries
├── api/                 # OpenAPI specs, protobuf definitions
├── migrations/          # SQL migration files
├── scripts/             # build, deploy, dev tooling
├── configs/             # default config files
└── Makefile
```

**Key rules:**
- `internal/` is enforced by the Go compiler — code here cannot be imported by external modules.
- `cmd/*/main.go` should be thin: parse flags, wire dependencies, call `run()`, handle shutdown.
- Group by **domain/feature**, not by technical layer. Avoid `models/`, `controllers/`, `services/` — this is Java-style layering that fights Go's package model.
- Avoid `utils/`, `helpers/`, `common/` packages — name packages by what they provide, since vague names attract unrelated code and make imports meaningless.
- A directory IS a package. Don't create directories just for organization.

---

## Naming Conventions

```go
// Packages: short, lowercase, single-word. No underscores or mixedCaps.
package user      // good
package userService // bad — mixedCaps

// Exported: MixedCaps. Unexported: mixedCaps. Underscores are legal but the
// community treats them as a style bug — they signal non-idiomatic code.
func ParseRequest()  // exported
func parseHeader()   // unexported

// Interfaces: method + "-er" suffix for single-method interfaces
type Reader interface { Read(p []byte) (n int, err error) }
type Validator interface { Validate() error }

// Getters: Owner(), not GetOwner(). Setters: SetOwner().
func (u *User) Name() string       // getter — the "Get" prefix is un-Go
func (u *User) SetName(n string)   // setter

// Acronyms: all caps. URL, HTTP, ID, API — not Url, Http, Id, Api.
type HTTPClient struct{}
var userID int

// Error variables: ErrXxx. Error types: XxxError.
var ErrNotFound = errors.New("not found")
type ValidationError struct { Field string; Message string }

// Context: first parameter, always named ctx. This is a universal Go convention
// that makes context propagation instantly recognizable in any codebase.
func (s *Service) GetUser(ctx context.Context, id string) (*User, error)
```

---

## Error Handling

This is Go's most distinctive pattern. Master it.

```go
// Check every error — wrap with context using %w
f, err := os.Open(name)
if err != nil {
    return fmt.Errorf("opening config %s: %w", name, err)
}
defer f.Close()

// errors.AsType — generic typed error extraction [Go 1.26+]
// Preferred over errors.As: type-safe, no pre-declared variable needed.
if pathErr, ok := errors.AsType[*fs.PathError](err); ok {
    fmt.Println("failed at path:", pathErr.Path)
}
```

**Key rules:**
- `return err` without context makes debugging painful — always wrap with `fmt.Errorf("doing X: %w", err)`.
- `log.Fatal(err)` in library code calls `os.Exit(1)`, skipping deferred cleanup — return errors to callers.
- `panic()` is for programmer bugs, not runtime conditions — return errors instead.
- Wrap third-party errors with `%v` (not `%w`) to avoid coupling callers to the underlying error type.
- **Error message style:** lowercase, no punctuation: `fmt.Errorf("reading config file: %w", err)`.

See `references/errors-and-resilience.md` for sentinel errors, custom error types, `errors.Join`, retry patterns, circuit breakers, and graceful degradation.

---

## Concurrency Essentials

See `references/concurrency.md` for comprehensive patterns including errgroup, worker pools, and fan-out/fan-in. Core rules:

1. **Use context for cancellation.** Every goroutine must check `ctx.Done()` — without it, there's no way to signal "stop work."
2. **Prefer `errgroup` over raw `sync.WaitGroup`.** Bundles wait + error collection + context cancellation. See `concurrency.md` for full examples with `SetLimit`.
3. **Protect shared state** — channels for communication, mutex when simpler. Comment what each mutex protects.
4. **Every goroutine needs a shutdown path.** No cancellation check = leaked goroutine = memory leak.
5. **A panic in a goroutine kills the entire process.** Recover in spawned goroutines, or use `sourcegraph/conc`.

**Novel sync primitives:**

`sync.OnceValue` / `sync.OnceValues` [Go 1.21+] — type-safe lazy init replacing `sync.Once` + package var:
```go
var loadConfig = sync.OnceValues(func() ([]byte, error) {
    return os.ReadFile("config.json") // runs exactly once, safe from any goroutine
})
data, err := loadConfig() // subsequent calls return cached result
```

`sync.WaitGroup.Go` [Go 1.25+] — combines `Add(1)` + `go func` + `Done()`:
```go
var wg sync.WaitGroup
wg.Go(func() { process(1) })
wg.Go(func() { process(2) })
wg.Wait()
```

**Channel sizing:** unbuffered (0) for synchronization, buffered (1) for signals, buffered (N) for known-bounded work.

---

## Interfaces

```go
// Accept interfaces, return concrete types
type UserStore interface {
    GetUser(ctx context.Context, id string) (*User, error)
}
func NewService(store UserStore) *Service { return &Service{store: store} }

// Keep interfaces small — 1-3 methods. Compose larger ones from small ones.
type ReadWriter interface { Reader; Writer }

// Define interfaces where they're USED, not implemented. Go interfaces are
// satisfied implicitly, so the consumer decides what behavior it needs.

// Compile-time verification (catches drift between interface and impl):
var _ UserStore = (*PostgresStore)(nil)
```

---

## Struct Design

```go
// Make the zero value useful — reduces initialization bugs and simplifies APIs
type Server struct {
    Addr    string        // "" is valid — will use default
    Handler http.Handler  // nil is valid in net/http
    timeout time.Duration // unexported, set via option
}

// Functional options — the Go pattern for complex constructors with optional config
type Option func(*Server)
func WithTimeout(d time.Duration) Option { return func(s *Server) { s.timeout = d } }

func NewServer(addr string, opts ...Option) *Server {
    s := &Server{Addr: addr, timeout: 30 * time.Second}
    for _, opt := range opts { opt(s) }
    return s
}

// Receiver consistency: if any method needs a pointer receiver, use pointer
// receivers for all methods. Mixing causes subtle bugs with interface satisfaction.
```

---

## Dependency Injection

Go uses constructor injection — no DI framework needed for most applications.

```go
type Service struct {
    repo   Repository
    cache  Cache
    logger *slog.Logger
}

func NewService(repo Repository, cache Cache, logger *slog.Logger) *Service {
    return &Service{repo: repo, cache: cache, logger: logger}
}

// Wire everything in main() — this is your composition root
func main() {
    db := postgres.NewDB(cfg.DatabaseURL)
    svc := user.NewService(postgres.NewUserRepo(db), redis.NewCache(cfg.RedisURL),
        slog.New(slog.NewJSONHandler(os.Stdout, nil)))
}
```

For large applications (20+ services), consider Google's `wire` for compile-time DI code generation.

---

## Logging with slog (Go 1.21+)

```go
// slog is stdlib structured logging — prefer it over third-party loggers
logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
    Level: slog.LevelInfo,
}))
logger.InfoContext(ctx, "user created",
    slog.String("user_id", user.ID), slog.String("email", user.Email))

// Choose: log OR return the error, not both. Double-logging clutters dashboards
// and makes it impossible to count how many times an error actually occurred.
```

---

## HTTP Server Pattern

Go 1.22+ has method-based routing and path parameters built in, so most APIs no longer need a third-party router.

```go
mux := http.NewServeMux()
mux.HandleFunc("GET /users/{id}", handleGetUser)
mux.HandleFunc("POST /users", handleCreateUser)

srv := &http.Server{
    Addr:         ":8080",
    Handler:      withMiddleware(mux),
    ReadTimeout:  5 * time.Second,  // prevent slow-loris attacks
    WriteTimeout: 10 * time.Second,
    IdleTimeout:  120 * time.Second,
}
// Graceful shutdown — see references/http-and-apis.md for full pattern
```

For larger APIs, consider `chi` (lightweight, stdlib-compatible) or `connect-go` (gRPC+HTTP). See `references/http-and-apis.md` for middleware, JSON APIs, WebSockets, SSE, and more.

---

## Database Access

```go
// pgx is the recommended PostgreSQL driver — fastest, most feature-complete
pool, _ := pgxpool.New(ctx, databaseURL)
// Set pool limits to prevent overwhelming the database under load
config.MaxConns = 25; config.MinConns = 5; config.MaxConnLifetime = time.Hour

// Parameterized queries prevent SQL injection — string concatenation is unsafe
rows, err := pool.Query(ctx, "SELECT id, name FROM users WHERE active = $1", true)
if err != nil { return fmt.Errorf("querying users: %w", err) }
defer rows.Close() // unclosed rows hold a connection from the pool

// Transactions — defer Rollback is safe (no-op after Commit)
tx, _ := pool.Begin(ctx)
defer tx.Rollback(ctx)
// ... do work ...
tx.Commit(ctx)
```

See `references/database.md` for sqlc, migrations, ORMs, connection tuning, and batch operations.

---

## Testing

```go
// Table-driven tests — the idiomatic Go testing pattern
func TestParseSize(t *testing.T) {
    tests := []struct {
        name string; input string; want int64; wantErr bool
    }{
        {"bytes", "100B", 100, false},
        {"kilobytes", "2KB", 2048, false},
        {"empty", "", 0, true},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := ParseSize(tt.input)
            if (err != nil) != tt.wantErr {
                t.Errorf("ParseSize(%q) error = %v, wantErr %v", tt.input, err, tt.wantErr)
                return
            }
            if got != tt.want {
                t.Errorf("ParseSize(%q) = %d, want %d", tt.input, got, tt.want)
            }
        })
    }
}
// Run with: go test -race -count=1 ./...
```

See `references/testing.md` for mocking, httptest, benchmarks, fuzzing, golden files, and integration tests.

---

## Build and Distribution

```go
//go:embed static/*
var staticFiles embed.FS  // embed files at compile time — no external dependencies

// go build -ldflags="-s -w -X main.version=1.2.3" -o myapp ./cmd/myapp
// Cross-compile: GOOS=linux GOARCH=arm64 go build -o myapp ./cmd/myapp
```

See `references/platform-and-build.md` for Windows specifics, CGO, Docker builds, and GoReleaser.

---

## Quick Reference: Common Anti-Patterns

| Anti-Pattern | Why It's a Problem | Fix |
|---|---|---|
| `_ = someFunc()` ignoring errors | Silent failures surface hours later | Handle every error |
| `go func() { ... }()` without shutdown | Goroutine leak — memory grows until OOM | Context cancellation + errgroup |
| `time.Sleep()` for synchronization | Flaky, race-condition-prone | Channels, sync primitives, or tickers |
| `init()` for complex setup | Hidden side effects, impossible to test | Explicit initialization in `main()` |
| `any` everywhere | Loses type safety, runtime assertions | Generics or specific interfaces |
| `sync.Mutex` without comment | Unclear what data it protects | `mu sync.Mutex // protects count` |
| Global mutable state | Race conditions, test pollution | Dependency injection |
| `log.Fatal` in library code | Calls `os.Exit(1)`, skips deferred cleanup | Return errors to caller |
| `select {}` without `ctx.Done()` | Blocks forever, prevents shutdown | Include cancellation case |
| `time.After` in select loops | Allocates a new timer every iteration; leaks pre-Go 1.23 | `time.NewTimer` + `Reset`; or `time.AfterFunc` |
| Not calling `t.Parallel()` in subtests | Independent subtests run serially, slow CI | Add `t.Parallel()` to independent subtests |
| No `context.Context` in library APIs | Uncancellable operations, no deadline propagation | Accept `ctx context.Context` as first parameter |
| Not draining `http.Response.Body` | TCP connections not reused (kills keep-alive) | `io.Copy(io.Discard, resp.Body)` before `Close` |

---

## Library Recommendations

| Category | Recommended | Notes |
|---|---|---|
| HTTP Router | `net/http` (1.22+), `chi` | stdlib sufficient for most cases |
| Database (PG) | `pgx`, `sqlc` | pgx driver, sqlc for type-safe queries |
| Database (General) | `database/sql` + `sqlx` | stdlib-compatible, any driver |
| Migrations | `golang-migrate`, `atlas` | atlas for declarative schema |
| CLI | `cobra`, `kong` | cobra is ecosystem standard |
| Config | `koanf`, `viper` | koanf lighter, viper more popular |
| Logging | `slog` (stdlib) | zerolog only for extreme perf |
| Testing | `testing` + `testify` | assert + mock |
| gRPC | `connectrpc.com/connect` | HTTP-compatible gRPC |
| WebSocket | `nhooyr.io/websocket` | Better API than gorilla |
| Concurrency | `errgroup`, `conc` | errgroup for most, conc for panic safety |
| Validation | `go-playground/validator` | Struct tag validation |
| AI/LLM | `anthropic-sdk-go`, `openai-go` | Official SDKs |
| MCP / Agent Tools | `modelcontextprotocol/go-sdk`, `mark3labs/mcp-go` | go-sdk is official; mcp-go is mature community alternative |
| Container Runtime | *(stdlib)* | Go 1.25+ has built-in container-aware GOMAXPROCS — `uber-go/automaxprocs` no longer needed |

---

## Generics Decision Framework (Go 1.18+)

**Use generics when** the alternative is code duplication or `any`:
- Data structures (stacks, queues, trees, caches)
- Slice/map utilities (`Map`, `Filter`, `Keys`)
- Type-safe result/option types

**Prefer interfaces when** you only need to call methods:
```go
func Process(items []Validator)           // good — simple, clear
func Process[T Validator](items []T)      // unnecessary complexity
```

```go
// Generics shine for data structures where any would lose type safety
type Stack[T any] struct{ items []T }
func (s *Stack[T]) Push(v T) { s.items = append(s.items, v) }
func (s *Stack[T]) Pop() (T, bool) {
    if len(s.items) == 0 { var zero T; return zero, false }
    v := s.items[len(s.items)-1]
    s.items = s.items[:len(s.items)-1]
    return v, true
}
```

See `references/advanced-patterns.md` for constraint composition, self-referential generics, and advanced patterns.
