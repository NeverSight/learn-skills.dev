---
name: go-concurrency-patterns
description: Master Go concurrency with goroutines, channels, sync primitives, and context. Use when building concurrent Go applications, implementing worker pools, or debugging race conditions.
metadata:
  author: caijiatao
  version: "2026.2.24"
  source: https://go.dev/doc/effective_go#concurrency
  language: en
  tags: [goroutines, channels, context, worker-pool, sync, race-detection]
  category: concurrency
---

# Go Concurrency Patterns

Production patterns for Go concurrency including goroutines, channels, synchronization primitives, and context management.

## When to Use This Skill

- Building concurrent Go applications
- Implementing worker pools and pipelines
- Managing goroutine lifecycles
- Using channels for communication
- Debugging race conditions
- Implementing graceful shutdown

## Core Concepts

### Primitives

| Primitive | Purpose | Reference |
|-----------|---------|-----------|
| `goroutine` | Lightweight concurrent execution | [core-goroutines](references/core-goroutines.md) |
| `channel` | Communication between goroutines | [core-channels](references/core-channels.md) |
| `select` | Multiplex channel operations | [core-channels](references/core-channels.md) |
| `sync.Mutex` | Mutual exclusion | [core-sync](references/core-sync.md) |
| `sync.WaitGroup` | Wait for goroutines to complete | [core-sync](references/core-sync.md) |
| `context.Context` | Cancellation and deadlines | [core-context](references/core-context.md) |

### Patterns

| Pattern | Description | Reference |
|---------|-------------|-----------|
| **Worker Pool** | Fixed number of workers processing jobs | [patterns-worker-pool](references/patterns-worker-pool.md) |
| **Pipeline** | Fan-out/fan-in for data flow | [patterns-pipeline](references/patterns-pipeline.md) |
| **Graceful Shutdown** | Clean shutdown with signal handling | [patterns-graceful-shutdown](references/patterns-graceful-shutdown.md) |
| **Error Group** | Concurrent error handling with errgroup | [patterns-errgroup](references/patterns-errgroup.md) |

## The Go Concurrency Mantra

```
Don't communicate by sharing memory;
share memory by communicating.
```

## Quick Reference

### Spawning a Goroutine
```go
go func() {
    // Do work concurrently
}()
```

### Creating a Channel
```go
ch := make(chan int)     // Unbuffered
ch := make(chan int, 10) // Buffered
```

### Waiting for Goroutines
```go
var wg sync.WaitGroup
wg.Add(1)
go func() {
    defer wg.Done()
    // Work
}()
wg.Wait()
```

### Context Cancellation
```go
ctx, cancel := context.WithCancel(context.Background())
go func() {
    <-ctx.Done()
    // Cleanup
}()
cancel() // Signal shutdown
```

## Race Detection

```bash
# Run tests with race detector
go test -race ./...

# Build with race detector
go build -race .
```

## Best Practices

- **Do**: Use context for cancellation
- **Do**: Close channels from sender side only
- **Do**: Use errgroup for concurrent operations
- **Do**: Buffer channels when you know the count
- **Don't**: Leak goroutines - always have exit path
- **Don't**: Close channels from receiver
- **Don't**: Use shared memory unless necessary
- **Don't**: Ignore context cancellation

## Resources

- [Go Concurrency Patterns](https://go.dev/blog/pipelines)
- [Effective Go - Concurrency](https://go.dev/doc/effective_go#concurrency)
- [Go by Example - Goroutines](https://gobyexample.com/goroutines)
