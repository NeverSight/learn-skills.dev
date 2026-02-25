---
name: streaming-patterns
description: Go 1.23 iter.Seq2 streaming patterns for Beluga AI v2. Use when implementing streaming, transforms, or backpressure.
---

# Streaming Patterns

## Primary Primitive: iter.Seq2[T, error]

```go
func (m *Model) Stream(ctx context.Context, msgs []schema.Message) iter.Seq2[schema.StreamChunk, error] {
    return func(yield func(schema.StreamChunk, error) bool) {
        stream, err := m.client.Stream(ctx, msgs)
        if err != nil { yield(schema.StreamChunk{}, err); return }
        defer stream.Close()
        for {
            select {
            case <-ctx.Done(): yield(schema.StreamChunk{}, ctx.Err()); return
            default:
            }
            chunk, err := stream.Recv()
            if err == io.EOF { return }
            if err != nil { yield(schema.StreamChunk{}, err); return }
            if !yield(convertChunk(chunk), nil) { return } // consumer stopped
        }
    }
}
```

## Composition

- **Pipe**: `func Pipe[A, B any](first iter.Seq2[A, error], transform func(A) (B, error)) iter.Seq2[B, error]`
- **Collect**: Stream to slice — `func Collect[T any](stream iter.Seq2[T, error]) ([]T, error)`
- **Invoke from Stream**: Stream, collect, return last.
- **Fan-out**: `iter.Pull2()` to get next/stop, broadcast to N consumers.
- **BufferedStream**: Channel-backed buffer for backpressure.

## Rules

1. Public API: `iter.Seq2[T, error]` — never `<-chan`.
2. Internal goroutine communication: channels are fine.
3. Always check context cancellation in producers.
4. `yield` returning false = consumer stopped — respect immediately.
5. Use `iter.Pull2` only when pull semantics are genuinely needed.
