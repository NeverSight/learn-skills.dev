---
name: error-handling
description: Standardizes error handling across a codebase with a unified error taxonomy, consistent error codes, proper propagation chains, user-facing vs internal error separation, and structured logging with correlation IDs. Use when adding error handling, implementing error classes, standardizing exceptions, creating error responses, or when the user needs consistent error patterns.
---

# Error Handling

## Overview

Standardize error handling across a codebase by implementing a unified error
taxonomy, stable error codes, proper propagation chains, and structured logging.
The core principle: every error must be categorized, coded, wrapped with
context, and split into a safe user-facing message and a detailed internal log
entry.

## When to use

- When adding error handling to an API or service
- When implementing custom error/exception classes
- When standardizing how errors propagate through layers
- When designing error response formats for an API
- When the user mentions "error handling", "exceptions", "error codes", or
  "error responses"
- When adding structured logging for errors with correlation IDs

**Do NOT use when:**

- The user needs to debug a specific runtime error (use a debugging skill)
- The user wants monitoring/alerting setup (use a monitoring skill)
- The task is only about input validation logic, not error handling patterns

## Workflow

### 1. Audit existing error handling

Scan the codebase for current error patterns:

- Search for `try/catch`, `try/except`, `.catch()`, `rescue`, error middleware
- Identify swallowed exceptions (empty catch blocks, catch-and-ignore)
- Find bare throws/raises without context wrapping
- Note inconsistent error response formats across endpoints
- Check for leaked internal details in user-facing responses

**Output:** A list of error handling gaps and inconsistencies.

### 2. Define the error taxonomy

Create error categories that map to HTTP status codes (for APIs) or exit
conditions (for services). Every error in the system must belong to exactly one
category.

| Category              | HTTP Status | Error Code Prefix | Description                                  |
| --------------------- | ----------- | ----------------- | -------------------------------------------- |
| `validation`          | 400         | `ERR_VALIDATION_` | Invalid input, malformed request             |
| `authentication`      | 401         | `ERR_AUTH_`       | Missing or invalid credentials               |
| `authorization`       | 403         | `ERR_FORBIDDEN_`  | Valid credentials but insufficient access    |
| `not_found`           | 404         | `ERR_NOT_FOUND_`  | Requested resource does not exist            |
| `conflict`            | 409         | `ERR_CONFLICT_`   | State conflict (duplicate, version mismatch) |
| `rate_limit`          | 429         | `ERR_RATE_LIMIT_` | Too many requests                            |
| `internal`            | 500         | `ERR_INTERNAL_`   | Unexpected server error                      |
| `service_unavailable` | 503         | `ERR_UPSTREAM_`   | Dependency failure (DB, external API)        |

### 3. Implement error class hierarchy

Create a base error class and category-specific subclasses. Every error class
must carry:

- **`code`** — Stable string code clients can match on (e.g.,
  `ERR_USER_NOT_FOUND`)
- **`message`** — Safe, user-facing message (no stack traces, no internal paths)
- **`statusCode`** — HTTP status code for API responses
- **`category`** — Error taxonomy category
- **`details`** — Optional structured data (field validation errors,
  constraints)
- **`cause`** — Original error for propagation chain (preserves stack trace)

**TypeScript example:**

```typescript
export class AppError extends Error {
  public readonly code: string;
  public readonly statusCode: number;
  public readonly category: string;
  public readonly details?: Record<string, unknown>;
  public readonly isOperational: boolean;

  constructor(params: {
    code: string;
    message: string;
    statusCode: number;
    category: string;
    details?: Record<string, unknown>;
    cause?: Error;
    isOperational?: boolean;
  }) {
    super(params.message, { cause: params.cause });
    this.code = params.code;
    this.statusCode = params.statusCode;
    this.category = params.category;
    this.details = params.details;
    this.isOperational = params.cause !== undefined
      ? true
      : (params.isOperational ?? true);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }
}

export class ValidationError extends AppError {
  constructor(
    message: string,
    details?: Record<string, unknown>,
    cause?: Error,
  ) {
    super({
      code: "ERR_VALIDATION",
      message,
      statusCode: 400,
      category: "validation",
      details,
      cause,
    });
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string, identifier: string, cause?: Error) {
    super({
      code: `ERR_NOT_FOUND_${resource.toUpperCase()}`,
      message: `${resource} not found`,
      statusCode: 404,
      category: "not_found",
      details: { resource, identifier },
      cause,
    });
  }
}

export class ConflictError extends AppError {
  constructor(
    message: string,
    details?: Record<string, unknown>,
    cause?: Error,
  ) {
    super({
      code: "ERR_CONFLICT",
      message,
      statusCode: 409,
      category: "conflict",
      details,
      cause,
    });
  }
}

export class AuthenticationError extends AppError {
  constructor(message = "Authentication required", cause?: Error) {
    super({
      code: "ERR_AUTH_INVALID",
      message,
      statusCode: 401,
      category: "authentication",
      cause,
    });
  }
}

export class AuthorizationError extends AppError {
  constructor(message = "Insufficient permissions", cause?: Error) {
    super({
      code: "ERR_FORBIDDEN",
      message,
      statusCode: 403,
      category: "authorization",
      cause,
    });
  }
}

export class RateLimitError extends AppError {
  constructor(retryAfterSeconds?: number, cause?: Error) {
    super({
      code: "ERR_RATE_LIMIT",
      message: "Too many requests",
      statusCode: 429,
      category: "rate_limit",
      details: retryAfterSeconds
        ? { retryAfter: retryAfterSeconds }
        : undefined,
      cause,
    });
  }
}

export class InternalError extends AppError {
  constructor(message: string, cause?: Error) {
    super({
      code: "ERR_INTERNAL",
      message: "An unexpected error occurred",
      statusCode: 500,
      category: "internal",
      cause,
      isOperational: false,
    });
  }
}
```

**Python equivalent:**

```python
class AppError(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int,
        category: str,
        details: dict | None = None,
        cause: Exception | None = None,
        is_operational: bool = True,
    ):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.category = category
        self.details = details or {}
        self.is_operational = is_operational
        self.__cause__ = cause

class NotFoundError(AppError):
    def __init__(self, resource: str, identifier: str, cause: Exception | None = None):
        super().__init__(
            code=f"ERR_NOT_FOUND_{resource.upper()}",
            message=f"{resource} not found",
            status_code=404,
            category="not_found",
            details={"resource": resource, "identifier": identifier},
            cause=cause,
        )

class ValidationError(AppError):
    def __init__(self, message: str, details: dict | None = None, cause: Exception | None = None):
        super().__init__(
            code="ERR_VALIDATION",
            message=message,
            status_code=400,
            category="validation",
            details=details,
            cause=cause,
        )
```

### 4. Implement error propagation rules

**Never swallow exceptions.** Every catch block must either:

1. **Re-raise** the error unchanged (if this layer can't add context)
2. **Wrap** the error in a domain-specific error with the original as `cause`
3. **Handle** the error completely (log it, return a response, trigger recovery)

**Always preserve the chain.** When wrapping, pass the original error as `cause`
so the full stack trace is available in logs:

```typescript
// WRONG: swallows the original error
try {
  await db.query(sql);
} catch (err) {
  throw new Error("Database query failed"); // original error lost
}

// RIGHT: wraps with context, preserves cause
try {
  await db.query(sql);
} catch (err) {
  throw new InternalError("Database query failed", err as Error);
}
```

### 5. Separate user-facing from internal errors

**User-facing response** — safe, minimal, actionable:

```json
{
  "error": {
    "code": "ERR_NOT_FOUND_USER",
    "message": "User not found",
    "details": {
      "resource": "user",
      "identifier": "usr_abc123"
    }
  },
  "requestId": "req_7f3a2b1c"
}
```

**Internal log entry** — full diagnostic context:

```json
{
  "level": "error",
  "code": "ERR_NOT_FOUND_USER",
  "message": "User not found",
  "category": "not_found",
  "correlationId": "req_7f3a2b1c",
  "userId": "usr_abc123",
  "path": "/api/users/usr_abc123",
  "method": "GET",
  "stack": "NotFoundError: User not found\n    at UserService.getById ...",
  "cause": "MongoError: connection refused at 10.0.0.5:27017",
  "timestamp": "2026-03-06T10:15:32.456Z",
  "service": "user-api",
  "environment": "production"
}
```

**Rules:**

- Never expose stack traces, file paths, or database errors to users
- Never expose internal service names or infrastructure details
- Always include the error `code` in both user response and log
- Always include a `requestId` / `correlationId` in both
- Log the full causal chain internally; show only the top-level message to users
- For `InternalError` (500), always use a generic message: "An unexpected error
  occurred"

### 6. Implement error response middleware

Centralize error-to-response conversion in middleware (Express) or exception
handlers (FastAPI, Django). This is the single place where errors become HTTP
responses.

```typescript
// Express error middleware
function errorHandler(
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction,
) {
  const correlationId = req.headers["x-request-id"] || crypto.randomUUID();

  if (err instanceof AppError) {
    // Operational error — expected, safe to expose
    logger.error({
      code: err.code,
      message: err.message,
      category: err.category,
      correlationId,
      path: req.path,
      method: req.method,
      stack: err.stack,
      cause: err.cause?.message,
    });

    return res.status(err.statusCode).json({
      error: {
        code: err.code,
        message: err.message,
        ...(err.details && { details: err.details }),
      },
      requestId: correlationId,
    });
  }

  // Unexpected error — do NOT expose details
  logger.error({
    code: "ERR_INTERNAL",
    message: err.message,
    category: "internal",
    correlationId,
    path: req.path,
    method: req.method,
    stack: err.stack,
  });

  return res.status(500).json({
    error: {
      code: "ERR_INTERNAL",
      message: "An unexpected error occurred",
    },
    requestId: correlationId,
  });
}
```

### 7. Add structured error logging

Every error log entry must include:

| Field           | Required | Description                                    |
| --------------- | -------- | ---------------------------------------------- |
| `level`         | Yes      | `error`, `warn`, or `fatal`                    |
| `code`          | Yes      | Stable error code (e.g., `ERR_NOT_FOUND_USER`) |
| `message`       | Yes      | Human-readable description                     |
| `category`      | Yes      | Error taxonomy category                        |
| `correlationId` | Yes      | Request ID for tracing across services         |
| `path`          | Yes      | Request path or operation name                 |
| `method`        | Yes      | HTTP method or operation type                  |
| `stack`         | Yes      | Full stack trace                               |
| `cause`         | No       | Original error message if wrapped              |
| `timestamp`     | Yes      | ISO 8601 timestamp                             |
| `service`       | Yes      | Service name for multi-service architectures   |
| `userId`        | No       | Authenticated user ID if available             |
| `details`       | No       | Structured error details (validation fields)   |

## Checklist

- [ ] Error taxonomy defined with categories mapping to HTTP status codes
- [ ] Base error class implemented with code, message, statusCode, category,
      cause
- [ ] Category-specific error subclasses created (validation, auth, not-found,
      etc.)
- [ ] Error codes are stable strings clients can match on programmatically
- [ ] All catch blocks either re-raise, wrap with context, or fully handle
- [ ] No swallowed exceptions (empty catch blocks)
- [ ] User-facing responses contain only code, message, and safe details
- [ ] Internal logs contain full stack traces, causal chains, and request
      context
- [ ] Correlation ID flows through from request to response to logs
- [ ] Centralized error middleware converts errors to consistent HTTP responses
- [ ] 500 errors always use generic message, never expose internals

## Error Response Schema

All API error responses must follow this schema:

```json
{
  "error": {
    "code": "ERR_VALIDATION",
    "message": "Invalid email format",
    "details": {
      "field": "email",
      "constraint": "Must be a valid email address",
      "received": "not-an-email"
    }
  },
  "requestId": "req_7f3a2b1c"
}
```

| Field           | Type   | Required | Description                                  |
| --------------- | ------ | -------- | -------------------------------------------- |
| `error.code`    | string | Yes      | Stable error code for programmatic matching  |
| `error.message` | string | Yes      | Human-readable description, safe for users   |
| `error.details` | object | No       | Structured context (validation fields, etc.) |
| `requestId`     | string | Yes      | Correlation ID for support and debugging     |

## Common mistakes

| Mistake                                             | Fix                                                                                                    |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Swallowing exceptions in empty catch blocks         | Every catch must re-raise, wrap, or fully handle. Log at minimum.                                      |
| Leaking stack traces to API consumers               | Error middleware must strip internals. Only expose code + message + safe details.                      |
| Using HTTP status codes as error codes              | Status codes are transport-level. Use stable string codes (ERR_USER_NOT_FOUND) for programmatic use.   |
| Inconsistent error response format                  | Centralize in error middleware. Every error response uses the same JSON schema.                        |
| Throwing raw strings instead of error objects       | Always throw typed error instances with code, category, and cause chain.                               |
| Missing correlation IDs                             | Generate a request ID at the edge (middleware/gateway) and propagate through all layers and logs.      |
| Logging user-facing message only                    | Internal logs must include stack trace, cause chain, request context, and correlation ID.              |
| Different error formats per endpoint                | One error middleware, one response schema. Endpoints throw typed errors; middleware formats responses. |
| Catching too broadly (catch Exception)              | Catch specific error types when possible. Use broad catch only at the top-level error boundary.        |
| Not distinguishing operational vs programmer errors | Operational errors (bad input, not found) are expected. Programmer errors (null deref) need alerts.    |

## Key principles

1. **Every error gets a stable code** — HTTP status codes change meaning across
   contexts. String error codes like `ERR_USER_NOT_FOUND` are stable contracts
   that clients, monitoring, and documentation can rely on. Never use numeric
   codes alone.

2. **Never swallow, always wrap** — Empty catch blocks hide bugs. Every caught
   error must be re-raised, wrapped with domain context (preserving the original
   as `cause`), or fully handled. The causal chain must survive from origin to
   log.

3. **User-facing and internal are separate concerns** — Users see a safe message
   and an error code. Logs see the full stack trace, causal chain, correlation
   ID, and request context. The error middleware is the boundary between these
   two worlds.

4. **Correlation IDs connect everything** — A single request ID generated at the
   edge must appear in the HTTP response, every log entry, and any downstream
   service calls. Without this, debugging production errors across services is
   impossible.

5. **Centralize the error boundary** — One error middleware, one response
   schema, one logging format. Individual endpoints throw typed errors; they
   never format error responses directly. This eliminates inconsistency.
