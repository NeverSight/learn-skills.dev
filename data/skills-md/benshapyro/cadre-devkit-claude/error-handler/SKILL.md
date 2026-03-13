---
name: error-handler
description: Provides battle-tested error handling patterns for TypeScript and Python. Use when implementing error handling, creating try/catch blocks, or handling exceptions.
---

# Error Handler Skill

Implements robust error handling patterns that provide meaningful errors, graceful degradation, and proper logging.

## Resources

For detailed code examples, see:
- `references/typescript-patterns.md` - TypeScript/JavaScript patterns (Express, React)
- `references/python-patterns.md` - Python patterns (FastAPI, Flask)

## Core Principles

1. **Fail Fast, Fail Loudly** - Catch errors early, make them visible
2. **Context is King** - Include relevant information in error messages
3. **Never Swallow Errors** - Always log, re-throw, or handle explicitly
4. **User-Friendly Messages** - Show generic messages to users, log details server-side
5. **Typed Errors** - Use custom error classes for different failure types

## Quick Patterns

### Custom Error Class (TypeScript)

```typescript
export class AppError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 500,
    public context?: Record<string, unknown>
  ) {
    super(message);
    this.name = this.constructor.name;
  }
}

// Specific types
export class ValidationError extends AppError {
  constructor(message: string, context?: Record<string, unknown>) {
    super(message, 'VALIDATION_ERROR', 400, context);
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string, id: string) {
    super(`${resource} not found`, 'NOT_FOUND', 404, { resource, id });
  }
}
```

### Custom Exception (Python)

```python
class AppError(Exception):
    def __init__(self, message: str, code: str, status_code: int = 500, context: dict | None = None):
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code
        self.context = context or {}

class ValidationError(AppError):
    def __init__(self, message: str, context: dict | None = None):
        super().__init__(message, "VALIDATION_ERROR", 400, context)
```

### Error Handling Pattern

```typescript
async function fetchData(id: string): Promise<Data> {
  if (!id) throw new ValidationError('Invalid ID', { id });

  try {
    const data = await db.find(id);
    if (!data) throw new NotFoundError('Data', id);
    return data;
  } catch (error) {
    if (error instanceof AppError) throw error;
    throw new DatabaseError('Fetch failed', { id, originalError: error.message });
  }
}
```

## Best Practices

### DO

- Use custom error classes for different error types
- Include context in errors (but sanitize before sending to client)
- Log errors with structured data (method, path, user ID, etc.)
- Provide user-friendly error messages
- Handle errors at appropriate levels (function, route, global)
- Always clean up resources (use try/finally or context managers)
- Add retry logic for transient failures
- Test error paths (negative tests)

### DON'T

- Swallow errors silently (`catch (e) {}`)
- Leak sensitive information in error messages
- Use generic error messages without context
- Ignore promise rejections
- Re-throw errors without adding context
- Return errors as values when exceptions are better
- Use errors for control flow

## Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [{ "field": "email", "message": "Invalid format" }]
  }
}
```

Remember: Good error handling prevents debugging nightmares and provides a better user experience.

---

## Version
- v1.1.0 (2025-12-05): Split into references (typescript-patterns.md, python-patterns.md)
- v1.0.0 (2025-11-15): Initial version
