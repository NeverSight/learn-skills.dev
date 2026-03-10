---
name: golang
description: "Go development: conventions, architecture, concurrency, performance, and code review. Use when working with .go files, go.mod, or user asks about goroutines, channels, error handling, interfaces."
compatibility: "Requires Go compiler. Optional: golangci-lint."
allowed-tools: [mcp__acp__Read, mcp__acp__Edit, mcp__acp__Write, mcp__acp__Bash]
---

# ABOUTME: Complete Go development guide - code, design, concurrency, performance, review
# ABOUTME: Modern Go (1.22-1.26): stdlib router, Green Tea GC, fgprof, easyjson, pgx batching

# Go Development

## Quick Reference

```bash
gofmt -w . && goimports -w . && go fix ./... && go vet ./...
go test ./... && go test -race ./... && go test -cover ./...
go build -pgo=cpu.pprof -o bin/app ./cmd/app
golangci-lint run
```

**See also:** `_AST_GREP.md`, `_PATTERNS.md`, `source-control`

---

## Pre-Commit Verification (MANDATORY)

```bash
gofmt -w .                    # Fix formatting FIRST (sqlc/codegen can misalign)
go fix ./...                  # Apply any pending API migrations
go vet ./...                  # Static analysis
go build ./...                # Compilation check
go test -race -count=1 ./...  # Tests with race detector
golangci-lint run             # Lint
```

**Why gofmt before build:** Code generators (sqlc, protoc) may produce code `gofmt` disagrees with. Always run `gofmt -w` after regeneration and before commit.

---

## Modern Go (1.22+)

**1.22:** Loop var fix (each iteration owns its variable). Range over int: `for i := range 10`. Stdlib router: `mux.HandleFunc("GET /api/v1/feed/{id}", h)` + `r.PathValue("id")`.

**1.23:** `iter.Seq[T]` lazy sequences. Use sparingly.

**1.25:** Container-aware GOMAXPROCS, Green Tea GC (experimental), `sync.WaitGroup.Go()`.

**1.26:** Green Tea GC default ON (10-40% lower overhead), `new(42)`, self-referential generics, ~30% faster cgo, goroutine leak detection (`/debug/pprof/goroutineleak`).

---

## Code Conventions

**Formatting:** `gofmt`/`goimports`: NON-NEGOTIABLE.

**Naming:** Short vars in funcs (`i`, `c`), descriptive at pkg level (`ErrNotFound`). Receivers 1-2 letter (`c *Client`). Initialisms all-caps or all-lower (`ServeHTTP`, `appID`). Packages lowercase singular.

**Errors:** Always handle (never `_`). Wrap: `fmt.Errorf("decompress %v: %w", name, err)`. Lowercase, no punctuation, guard clauses.

**Testing:** Table-driven with `t.Run()`, use `t.Helper()` in helpers.
```go
tests := []struct{ name string; a, b, want int }{
    {"positive", 2, 3, 5},
}
for _, tt := range tests {
    t.Run(tt.name, func(t *testing.T) {
        if got := Add(tt.a, tt.b); got != tt.want {
            t.Errorf("Add(%d,%d)=%d; want %d", tt.a, tt.b, got, tt.want)
        }
    })
}
```

**Build tags for simulation:** `//go:build simulation` in `driver_sim.go`, `//go:build !simulation` in `driver_real.go`. Same type, different impl. Use for hardware, external APIs, infra deps.

---

## Architecture & Design

**Project structure:**
```
cmd/api-server/main.go    # Entry points
internal/domain/          # Business entities
internal/service/         # Use cases
internal/repository/      # Data access
```
Organize by **feature/domain**, not technical layer. Avoid `/src`, `/utils`, `/common`, `/helpers`.

**Functional Options:**
```go
type Option func(*Server)
func WithPort(p int) Option { return func(s *Server) { s.port = p } }
func NewServer(opts ...Option) *Server { /* apply opts */ }
```

**Constructor Injection:** Accept interfaces, return structs. **No global mutable state**: pass deps explicitly.

**Interfaces:** Small (1-3 methods), accept interfaces, return structs.

**Useful Zero Values:** Uninitialized struct = safe to use or obviously invalid. Stdlib examples: `sync.Mutex`, `bytes.Buffer`.

---

## Concurrency

**Golden Rules:**
- Always know WHEN and HOW a goroutine terminates
- **Libraries are synchronous**: never launch goroutines from lib code unless concurrency IS the feature

**errgroup** (preferred over WaitGroup), **context** always first param, **bounded pools** for load, **sender closes** channels. `time.After` in loops leaks timers, use `time.NewTicker`.

For detailed concurrency patterns, performance optimization, profiling, and code review checklists, see `references/golang-patterns.md`.

---

## Resources

[Effective Go](https://go.dev/doc/effective_go) | [Code Review Comments](https://go.dev/wiki/CodeReviewComments) | [Release Notes](https://go.dev/doc/) | [goperf.dev](https://goperf.dev/) | [fgprof](https://github.com/felixge/fgprof)
