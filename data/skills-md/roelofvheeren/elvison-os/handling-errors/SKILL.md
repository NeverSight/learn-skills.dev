---
name: handling-errors
description: Provides robust error handling strategies and patterns. Use when the user mentions resilience, error handling, fallbacks, or debugging failures.
---

# Handling Errors

## When to use this skill
- Implementing error handling in new features.
- Designing error-resilient APIs and distributed systems.
- Improving application reliability through Circuit Breakers or Graceful Degradation.
- Standardizing error messages and custom exception hierarchies.

## Workflow

1.  **Categorization**
    - [ ] Determine if the error is **Recoverable** (e.g., Network Timeout) or **Unrecoverable** (e.g., OOM).
2.  **Strategy Selection**
    - [ ] Choose a pattern: **Fail Fast**, **Retry**, **Circuit Breaker**, or **Graceful Degradation**.
3.  **Implementation**
    - [ ] Use language-specific best practices (Custom Exceptions, Result Types, or Explicit Returns).
4.  **Verification**
    - [ ] Validate that errors are logged with context and resources are cleaned up.

## Universal Patterns

### Circuit Breaker
Prevent cascading failures by rejecting requests when a service is failing.
```python
# Logic: CLOSED -> failure threshold reached -> OPEN (wait timeout) -> HALF_OPEN (test)
```

### Error Aggregation
Collect multiple errors (e.g., during validation) instead of failing on the first one.
```typescript
class ErrorCollector {
  private errors: Error[] = [];
  add(error: Error) { this.errors.push(error); }
  throw() { if (this.errors.length) throw new AggregateError(this.errors); }
}
```

### Graceful Degradation
Provide fallback functionality (e.g., fetch from cache if DB is down).
```python
def with_fallback(primary, fallback):
    try: return primary()
    except Exception: return fallback()
```

## Language-Specific Patterns

### Python
- **Hierarchy:** Use `ApplicationError(Exception)` as a base.
- **Cleanup:** Use `@contextmanager` or `try/finally`.
- **Retry:** Implement decorators with exponential backoff.

### TypeScript/JS
- **Results:** Use `type Result<T, E> = { ok: true; value: T } | { ok: false; error: E }`.
- **Async:** Handle Promise rejections explicitly; avoid swallowing errors in `catch`.

### Rust/Go
- **Rust:** Prefer `Result<T, E>` and the `?` operator.
- **Go:** Check `if err != nil` explicitly; use `fmt.Errorf("...: %w", err)` for wrapping.

## Best Practices
- **Fail Fast:** Validate early.
- **Preserve Context:** Log metadata, stack traces, and timestamps.
- **Don't Swallow Errors:** Log or re-throw; empty catch blocks are forbidden.
- **Cleanup:** Always close files and connections.

## Resources
- [retry-patterns.md](resources/retry-patterns.md)
- [custom-errors.ts](examples/custom-errors.ts)
