---
name: go-best-practices
description: |
  WHEN: User is writing Go code, asking about Go patterns, reviewing Go code, asking
  "what's the best way to...", "how should I structure...", "is this idiomatic?",
  or any question about error handling, concurrency, interfaces, packages, testing patterns,
  or code organization in Go. Also activate when user is debugging Go code, refactoring Go,
  or working in a Go project (go.mod present) and asks general coding questions.
  Trigger this skill liberally for ANY Go-related development work.
  WHEN NOT: Non-Go languages, questions entirely unrelated to programming
---

# Go Best Practices Skill

Apply idiomatic Go patterns and best practices from Gopher Guides training materials.

## When Helping with Go Code

### Error Handling

- **Wrap errors with context**: Use `fmt.Errorf("operation failed: %w", err)`
- **Check errors immediately**: Don't defer error checking
- **Return errors, don't panic**: Panics are for unrecoverable situations only
- **Create sentinel errors** for expected conditions: `var ErrNotFound = errors.New("not found")`
- **Use errors.Is() and errors.As()** for error comparison

```go
// Good
if err != nil {
    return fmt.Errorf("failed to process user %s: %w", userID, err)
}

// Avoid
if err != nil {
    log.Fatal(err)  // Don't panic on recoverable errors
}
```

### Interface Design

- **Accept interfaces, return structs**: Functions should accept interfaces but return concrete types
- **Keep interfaces small**: Prefer single-method interfaces
- **Define interfaces at point of use**: Not where the implementation lives
- **Don't export interfaces unnecessarily**: Only if users need to mock

```go
// Good - interface defined by consumer
type Reader interface {
    Read(p []byte) (n int, err error)
}

func ProcessData(r Reader) error { ... }

// Avoid - exporting implementation details
type Service interface {
    Method1() error
    Method2() error
    Method3() error  // Too many methods
}
```

### Concurrency

- **Don't communicate by sharing memory; share memory by communicating**
- **Use channels for coordination, mutexes for state**
- **Always pass context.Context as first parameter**
- **Use errgroup for coordinating goroutines**
- **Avoid goroutine leaks**: Ensure goroutines can exit

```go
// Good - using errgroup
g, ctx := errgroup.WithContext(ctx)
for _, item := range items {
    item := item  // capture loop variable
    g.Go(func() error {
        return process(ctx, item)
    })
}
if err := g.Wait(); err != nil {
    return err
}
```

### Testing

- **Use table-driven tests** for multiple scenarios
- **Call t.Parallel()** for independent tests
- **Use t.Helper()** in test helpers
- **Test behavior, not implementation**
- **Use testify for assertions** when it improves readability

```go
func TestAdd(t *testing.T) {
    tests := []struct {
        name string
        a, b int
        want int
    }{
        {"positive numbers", 2, 3, 5},
        {"with zero", 5, 0, 5},
        {"negative numbers", -2, -3, -5},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel()
            got := Add(tt.a, tt.b)
            if got != tt.want {
                t.Errorf("Add(%d, %d) = %d, want %d", tt.a, tt.b, got, tt.want)
            }
        })
    }
}
```

### Package Organization

- **Package names should be short and lowercase**: `user` not `userService`
- **Avoid package-level state**: Use dependency injection
- **One package per directory**: No multi-package directories
- **internal/ for non-public packages**: Prevents external imports

### Naming Conventions

- **Use MixedCaps or mixedCaps**: Not underscores
- **Acronyms should be consistent**: `URL`, `HTTP`, `ID` (all caps for exported, all lower otherwise)
- **Short names for short scopes**: `i` for loop index, `err` for errors
- **Descriptive names for exports**: `ReadConfig` not `RC`

### Code Organization

- **Declare variables close to use**
- **Use defer for cleanup immediately after resource acquisition**
- **Group related declarations**
- **Order: constants, variables, types, functions**

## Anti-Patterns to Avoid

- **Empty interface (`interface{}` or `any`)**: Use specific types when possible
- **Global state**: Prefer dependency injection
- **Naked returns**: Always name what you're returning
- **Stuttering**: `user.UserService` should be `user.Service`
- **init() functions**: Prefer explicit initialization
- **Complex constructors**: Use functional options pattern

## When in Doubt

- Refer to [Effective Go](https://go.dev/doc/effective_go)
- Check the Go standard library for examples
- Use `go vet` and `staticcheck` for automated guidance

---

*This skill is powered by Gopher Guides training materials. For comprehensive Go training, visit [gopherguides.com](https://gopherguides.com).*
