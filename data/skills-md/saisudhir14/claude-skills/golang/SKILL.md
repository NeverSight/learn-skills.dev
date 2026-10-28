---
name: golang
description: >-
  Use when writing, reviewing, or refactoring Go code. Provides production
  best practices for Go covering error handling, concurrency, naming,
  testing, performance, generics, iterators, and common pitfalls. Distilled from
  Google Go Style Guide, Uber Go Style Guide, Effective Go, and Go Code Review
  Comments. Updated for Go 1.25.
version: "2.0.0"
license: MIT
compatibility:
  agents:
    - claude-code
    - cursor
    - github-copilot
    - codex
    - gemini-cli
    - opencode
    - amp
    - windsurf
    - zed
    - goose
    - roo-code
    - kiro
    - cline
    - antigravity
    - trae
    - clawdbot
    - droid
    - kilo
    - continue
    - aider
    - sourcegraph-cody
  platforms:
    - linux
    - macos
    - windows
  languages:
    - go
metadata:
  author: saisudhir14
  tags: golang go best-practices google uber style-guide error-handling concurrency testing performance generics iterators code-review production
  category: languages
---

# Go Best Practices

Production patterns from Google, Uber, and the Go team. Updated for Go 1.25.

> Sub-skills: `skills/go-error-handling`, `skills/go-concurrency`, `skills/go-testing`, `skills/go-performance`, `skills/go-code-review`, `skills/go-linting`, `skills/go-project-layout`, `skills/go-security`. Deep-dive references in `references/`.

## Core Principles

Readable code prioritizes these attributes in order:

1. **Clarity**: purpose and rationale are obvious to the reader
2. **Simplicity**: accomplishes the goal in the simplest way
3. **Concision**: high signal to noise ratio
4. **Maintainability**: easy to modify correctly
5. **Consistency**: matches surrounding codebase

---

## Error Handling

> Full guide: `skills/go-error-handling/SKILL.md` | Reference: `references/error-handling.md`

- **Return errors, never panic** in production code
- **Wrap with `%w`** when callers need `errors.Is`/`errors.As`; use `%v` at boundaries
- **Keep context succinct**: `"new store: %w"` not `"failed to create new store: %w"`
- **Handle errors once**: don't log and return the same error
- **Error strings**: lowercase, no punctuation
- **Indent error flow**: handle errors first, keep happy path at minimal indentation
- **Use `errors.Join`** (Go 1.20+) for multiple independent failures
- **Sentinel errors**: `Err` prefix for vars, `Error` suffix for types

```go
if err != nil {
    return fmt.Errorf("load config: %w", err)
}
```

---

## Concurrency

> Full guide: `skills/go-concurrency/SKILL.md` | Reference: `references/concurrency.md`

- **Channel size**: 0 (unbuffered) or 1; anything else needs justification
- **Document goroutine lifetimes**: when and how they exit
- **Use `errgroup.Group`** over manual `sync.WaitGroup` for error-returning goroutines
- **Prefer synchronous functions**: let callers add concurrency
- **Zero value mutexes**: don't use pointers; don't embed in public structs
- **Typed atomics** (Go 1.19+): `atomic.Int64`, `atomic.Bool`, `atomic.Pointer[T]`
- **`sync.Map`** (Go 1.24+): significantly improved performance for disjoint key sets

```go
g, ctx := errgroup.WithContext(ctx)
g.SetLimit(10)
for _, item := range items {
    g.Go(func() error { return process(ctx, item) })
}
return g.Wait()
```

---

## Naming

- **MixedCaps always**: never underscores (`MaxLength` not `MAX_LENGTH`)
- **Initialisms**: consistent case (`URL`, `ID`, `HTTP` not `Url`, `Id`, `Http`)
- **Short variables**: scope determines length (`i` for loops, `DefaultTimeout` for globals)
- **Receiver names**: 1-2 letter abbreviation, consistent across methods, never `this`/`self`
- **Package names**: lowercase single word, no `util`/`common`/`misc`
- **No repetition**: `http.Serve` not `http.HTTPServe`; `c.WriteTo` not `c.WriteConfigTo`

### Pointer vs Value Receivers

| Pointer receiver | Value receiver |
|---|---|
| Modifies receiver | Small, immutable struct |
| Large struct | Doesn't modify state |
| Contains sync.Mutex | Map, func, or chan |
| Consistency with other methods | Basic types |

---

## Imports

```go
import (
    "context"
    "fmt"

    "github.com/google/uuid"
    "golang.org/x/sync/errgroup"

    "yourcompany/internal/config"
)
```

- Three groups: stdlib, external, internal (separated by blank lines)
- Rename only to avoid collisions
- No dot imports except test files with circular deps
- Blank imports (`import _ "pkg"`) only in main or tests

---

## Module Management (Go 1.24+)

Track tool dependencies in `go.mod` with tool directives:

```go
tool (
    golang.org/x/tools/cmd/stringer
    github.com/golangci/golangci-lint/cmd/golangci-lint
)
```

```bash
go get -tool golang.org/x/tools/cmd/stringer  # add
go tool stringer -type=Status                  # run
go get tool                                    # update all
go install tool                                # install to GOBIN
```

---

## Structs

- **Always use field names** in initialization (positional breaks on changes)
- **Omit zero value fields**
- **Don't embed types** in public structs (exposes API unintentionally)
- **Use `var` for zero value structs**: `var user User`

---

## Slices and Maps

- **Nil slices preferred**: `var t []string` (use `[]string{}` only for JSON `[]` encoding)
- **Copy at boundaries**: `copy()` or `maps.Clone()` to prevent mutation
- **Preallocate**: `make([]T, 0, len(input))` when size is known
- **Use `slices` and `maps` packages**: `slices.Sort`, `slices.Clone`, `maps.Clone`, `maps.Equal`

---

## Generics (Go 1.18+)

- Use when writing identical code for different types
- Use `cmp.Ordered` or custom constraints for type safety
- **Generic type aliases** (Go 1.24+): `type Set[T comparable] = map[T]struct{}`
- **Don't over-generalize**: use concrete types or interfaces when they suffice

```go
func Filter[T any](s []T, pred func(T) bool) []T {
    result := make([]T, 0, len(s))
    for _, v := range s {
        if pred(v) {
            result = append(result, v)
        }
    }
    return result
}
```

---

## Iterators (Go 1.23+)

Range over functions for custom iterators:

```go
func Backward[T any](s []T) func(yield func(int, T) bool) {
    return func(yield func(int, T) bool) {
        for i := len(s) - 1; i >= 0; i-- {
            if !yield(i, s[i]) {
                return
            }
        }
    }
}

for i, v := range Backward(items) {
    fmt.Println(i, v)
}
```

String/bytes iterators (Go 1.24+): `strings.Lines`, `strings.SplitSeq`, `strings.SplitAfterSeq`

---

## Structured Logging (Go 1.21+)

```go
slog.Info("user created", "id", userID, "email", email)
slog.With("service", "auth").Info("starting")
handler := slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{Level: slog.LevelInfo})
```

- `slog.DiscardHandler` (Go 1.24+) for suppressing logs in tests
- Use consistent key names, group related fields with `slog.Group`

---

## Performance

> Full guide: `skills/go-performance/SKILL.md` | Reference: `references/performance.md`

- **`strconv` over `fmt`**: `strconv.Itoa(n)` not `fmt.Sprintf("%d", n)`
- **Avoid repeated `[]byte` conversions**: store once, reuse
- **Preallocate map capacity**: `make(map[string]int, len(items))`
- **`strings.Builder`** with `Grow()` for concatenation

---

## Testing

> Full guide: `skills/go-testing/SKILL.md` | Reference: `references/testing.md`

- **Table-driven tests** with `t.Parallel()` for subtests
- **`go-cmp`** over `reflect.DeepEqual` for clear diff output
- **Useful failure messages**: include input, got, want
- **`t.Fatal`** for setup failures
- **Interfaces belong to consumers**, not producers
- **`T.Context`** and **`T.Chdir`** (Go 1.24+)
- **`b.Loop()`** (Go 1.24+): cleaner benchmarks, no `b.ResetTimer()` needed
- **`synctest.Test`** (Go 1.25+): deterministic concurrent testing with synthetic time

---

## Resource Management (Go 1.24+)

- **`runtime.AddCleanup`**: multiple cleanups per object, no cycle leaks (replaces `SetFinalizer`)
- **`weak.Pointer[T]`**: weak references for caches, canonicalization, observers
- **`os.Root`**: scoped file access preventing path traversal attacks

---

## Patterns

> Full reference: `references/patterns.md`

- **Functional options**: `WithTimeout(d)`, `WithLogger(l)` for configurable constructors
- **Interface compliance**: `var _ http.Handler = (*Handler)(nil)`
- **Defer for cleanup**: small overhead, worth the safety
- **Graceful shutdown**: signal handling + `srv.Shutdown(ctx)`
- **Enums start at one**: zero = invalid/unset
- **Use `time.Duration`**: never raw ints for time
- **Two-value type assertions**: `t, ok := i.(string)` to avoid panics
- **Context first**: `func Process(ctx context.Context, ...)`
- **Avoid mutable globals**: use dependency injection
- **Avoid `init()`**: prefer explicit initialization in `main`
- **`//go:embed`** (Go 1.16+): embed static files
- **Field tags**: explicit `json:"name"` on marshaled structs
- **Container-aware GOMAXPROCS** (Go 1.25+): automatic cgroup-based tuning

---

## Common Gotchas

> Full reference: `references/gotchas.md`

| Gotcha | Fix |
|--------|-----|
| Loop variable capture (pre-1.22) | Fixed in Go 1.22+ (per-iteration vars) |
| Defer evaluates args immediately | Capture in closure |
| Nil interface vs nil pointer | Return `nil` explicitly |
| Use result before error check | Always check `err` first (Go 1.25 enforces) |
| Map iteration order | Sort keys with `slices.Sorted(maps.Keys(m))` |
| Slice append shared backing | Full slice expression `a[:2:2]` |

---

## Linting

> Full guide: `skills/go-linting/SKILL.md`

- **Use golangci-lint** as the standard linter aggregator
- **Recommended linters**: errcheck, govet, staticcheck, revive, gosimple, goimports, errorlint, bodyclose
- **Add as a tool dependency** (Go 1.24+): `go get -tool github.com/golangci/golangci-lint/cmd/golangci-lint`
- **Run in CI**: use `golangci/golangci-lint-action` for GitHub Actions
- **Suppress sparingly**: prefer fixing over `//nolint` comments

---

## Project Layout

> Full guide: `skills/go-project-layout/SKILL.md`

- **`cmd/`**: one subdirectory per executable, keep `main.go` thin
- **`internal/`**: private packages, enforced by the Go toolchain
- **Avoid `pkg/`, `src/`, `models/`, `utils/`**: name packages by purpose
- **Flat is fine**: small projects should not have deep directory trees
- **Dockerfile**: multi-stage build, `CGO_ENABLED=0`, distroless base image

---

## Security

> Full guide: `skills/go-security/SKILL.md`

- **Parameterized SQL queries**: never interpolate user input
- **`os.Root`** (Go 1.24+): scoped file access preventing path traversal
- **Validate at boundaries**: decode into typed structs, validate fields
- **Never hardcode or log secrets**: use `Secret` type with redacted `String()`
- **Standard crypto only**: `crypto/rand` for random bytes, `bcrypt` for passwords
- **HTTP timeouts**: always set `ReadTimeout`, `WriteTimeout`, `IdleTimeout`
- **`govulncheck`**: scan dependencies for known vulnerabilities
- **`go test -race`**: always run with the race detector in CI

---

## Experimental (Go 1.25)

- **`encoding/json/v2`**: enable with `GOEXPERIMENT=jsonv2`. Better performance, streaming, custom marshalers per call.

---

## Documentation

- Comments are full sentences starting with the declared name
- Package comments: before `package` declaration, no blank line

---

## References

1. [Google Go Style Guide](https://google.github.io/styleguide/go/)
2. [Uber Go Style Guide](https://github.com/uber-go/guide)
3. [Effective Go](https://go.dev/doc/effective_go)
4. [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments)
5. [Go 1.23 Release Notes](https://go.dev/doc/go1.23)
6. [Go 1.24 Release Notes](https://go.dev/doc/go1.24)
7. [Go 1.25 Release Notes](https://go.dev/doc/go1.25)
