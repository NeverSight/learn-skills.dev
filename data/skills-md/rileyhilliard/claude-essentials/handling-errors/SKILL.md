---
name: handling-errors
description: Prevents silent failures and context loss in error handling. Use when writing try-catch blocks, designing error propagation, reviewing catch blocks, or implementing Result patterns.
---

# Handling Errors

## Iron Laws

1. **Never swallow errors** - Empty catch blocks hide bugs that surface later in unrelated places, making them much harder to trace
2. **Never convert errors to booleans** - Loses all context and forces callers to guess what went wrong
3. **Preserve error context** when wrapping or propagating - upstream handlers need the original cause to make good decisions
4. **Log once where handled**, not at every layer - duplicate logs across layers create noise that obscures the real signal

## Error Messages

Every error message answers: **What happened? Why? How to recover?**

**For logs (developers):**

```typescript
logger.error("Failed to save user: Connection timeout after 30s", {
  userId: user.id,
  dbHost: config.db.host,
  error: error.stack,
});
```

**For users:**

For user-facing error copy, use `Skill(ce:writer)` with **The UX Writer** persona. Key principles:

- Brief and specific (not "Something went wrong")
- Actionable (tell them what to do next)
- No blame (never "You entered invalid...")

```typescript
showError({
  title: "Upload failed",
  message: "File exceeds 10MB limit. Choose a smaller file.",
  actions: [{ label: "Choose file", onClick: selectFile }],
});
```

## Error Categories

| Type         | Examples                           | Handling                    |
| ------------ | ---------------------------------- | --------------------------- |
| **Expected** | Validation, Not found, Unauthorized| Return Result type, log info|
| **Transient**| Network timeout, Rate limit        | Retry with backoff, log warn|
| **Unexpected**| Null reference, DB crash          | Log error, show support ID  |
| **Critical** | Auth down, Payment gateway offline | Circuit breaker, alert      |

## Fail Fast vs Degrade Gracefully

**Fail fast** for critical dependencies:

```typescript
await connectToDatabase(); // Throws on failure - app can't run without it
```

**Degrade gracefully** for optional features:

```typescript
const prefs = await loadPreferences(userId).catch(() => DEFAULT_PREFS);
```

## Log at the Right Layer

```typescript
// ❌ Logging at every layer = same error 3x
async function fetchData() {
  try { return await fetch(url); }
  catch (e) { console.error("Fetch failed:", e); throw e; }
}

// ✅ Log once where handled
async function fetchData() {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  return response;
}
// Top level logs the error once
```

## Language-Specific Patterns

- **TypeScript/React**: See [references/typescript-react.md](references/typescript-react.md) for Error Boundaries, typed errors, Result pattern, UI display
- **Python**: See [references/python.md](references/python.md) for EAFP, exception chaining, context managers
- **Go**: See [references/go.md](references/go.md) for explicit error returns, wrapping with %w, sentinel errors

## Anti-Patterns

| Pattern | Problem | Fix |
|---------|---------|-----|
| Empty catch blocks | Hides errors | Log or re-throw |
| `return false` on error | Loses context | Return Result type |
| Generic "Error" messages | Undebuggable | Include what/why/context |
| Logging same error at each layer | Log pollution | Log once at boundary |
| Bare `except:` / `catch (e)` all | Catches system signals | Catch specific types |
