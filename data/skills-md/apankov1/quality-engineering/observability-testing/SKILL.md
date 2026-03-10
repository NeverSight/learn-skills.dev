---
name: observability-testing
description: Verifies structured log output and error context. Provides mock logger creation, log level policy enforcement, and assertion patterns for observability testing.
---

# Observability Testing

Test that your code produces correct logs — not just that it runs.

Logs are your only window into production behavior. If critical paths don't log correctly, you're flying blind during incidents. This skill teaches you to verify structured log output as part of your test suite.

**When to use**: Testing error logging with context, audit trails, monitoring integration, log level policy enforcement, any code where observability matters.

**When not to use**: Pure business logic tests, UI components, tests where logging is incidental not critical.

## Rationalizations (Do Not Skip)

| Rationalization | Why It's Wrong | Required Action |
|-----------------|----------------|-----------------|
| "Logs are side effects, not behavior" | Incorrect logs = blind in production | Assert log output as first-class behavior |
| "I can see logs when I run it" | Manual inspection doesn't scale | Automate with mock logger assertions |
| "Any log level is fine" | Wrong levels = alert fatigue or missed incidents | Enforce log level policy |
| "Context isn't important" | Context-free logs are useless for debugging | Assert required context fields |

---

## What To Protect (Start Here)

Before generating log assertions, identify which observability decisions apply to your code:

| Decision | Question to Answer | If Yes → Use |
|----------|--------------------|--------------|
| Error paths must be debuggable from logs alone | Could an on-call engineer diagnose this failure without access to the request? | `assertLogEntry` with context fields |
| Happy paths must not trigger alerts | Would a warn/error log here fire a PagerDuty alert on every success? | `assertNoLogsAbove` |
| Log levels must match operational severity | Is this log classified correctly — would the wrong level cause alert fatigue or missed incidents? | `classifyLogLevel` |
| Error logs must include the Error instance | Does the error log carry a stack trace for root cause analysis? | `assertErrorLogged` |

**Do not generate tests for decisions the human hasn't confirmed.** A log assertion that checks "error was logged" without verifying the context contains fields an on-call engineer needs is slop — it passes while the team stays blind in production.

---

## Included Utilities

```typescript
import {
  createMockLogger,
  assertLogEntry,
  assertNoLogsAbove,
  assertHasLogLevel,
  assertErrorLogged,
  LOG_LEVEL_POLICY,
  LOG_LEVEL_ORDER,
  classifyLogLevel,
} from './structured-logger.ts';
```

## Core Workflow

### Step 1: Create Mock Logger

Replace real loggers with mock loggers that capture entries for assertion:

```typescript
const logger = createMockLogger();

// Pass to code under test
await myHandler({ logger });

// Assert on captured entries
assert.equal(logger.entries.length, 2);
```

### Step 2: Assert Specific Log Entries

Verify that specific logs were recorded with correct level, message, and context:

```typescript
it('logs error with full context on failure', async () => {
  const logger = createMockLogger();

  await assert.rejects(() => myHandler({ logger, shouldFail: true }));

  assertLogEntry(logger, 'error', 'Request failed', {
    component: 'Handler',
    path: '/api/test',
  });
});
```

### Step 3: Verify Happy Path Has No Warnings/Errors

Happy paths should not produce warnings or errors — that's alert fatigue:

```typescript
it('happy path produces no warnings or errors', async () => {
  const logger = createMockLogger();

  await myHandler({ logger });

  assertNoLogsAbove(logger, 'info');  // Only debug/info allowed
});
```

### Step 4: Verify Error Logs Include Error Instances

Error logs should include the actual Error object for stack traces:

```typescript
it('error log includes Error instance', async () => {
  const logger = createMockLogger();

  try {
    await myHandler({ logger, causeError: true });
  } catch {}

  assertErrorLogged(logger, 'Database connection failed', {
    name: 'ConnectionError',
    message: 'timeout',
  });
});
```

### Step 5: Follow Log Level Policy

Use the correct log level based on the nature of the message:

```typescript
// Reference table
console.log(LOG_LEVEL_POLICY);
/*
{
  error: {
    description: "Actionable failures requiring investigation",
    examples: ["Database connection failed", "Authentication error"],
    production: "100% always",
  },
  warn: {
    description: "Degraded but recoverable",
    examples: ["Retry exhausted but fallback worked", "Deprecated API called"],
    production: "100% always",
  },
  info: {
    description: "Significant state changes",
    examples: ["User logged in", "Config loaded", "Session started"],
    production: "sampled (1-10%)",
  },
  debug: {
    description: "Routine operations",
    examples: ["Cache hit/miss", "Heartbeat tick", "Request timing"],
    production: "off (or LOG_LEVEL=warn)",
  },
}
*/
```

### Step 6: Classify Log Levels Automatically

Use the classifier to suggest appropriate levels:

```typescript
// Returns suggested level based on keywords
classifyLogLevel("Database connection failed");  // 'error'
classifyLogLevel("Retry attempt 3 of 5");        // 'warn'
classifyLogLevel("User logged in");              // 'info'
classifyLogLevel("Cache hit for key xyz");       // 'debug'
```

### Step 7: Enforce Logger Interface

The mock logger implements a strict interface. Your production logger should match:

```typescript
interface StructuredLogger {
  debug(message: string, context?: Record<string, unknown>): void;
  info(message: string, context?: Record<string, unknown>): void;
  warn(message: string, context?: Record<string, unknown>): void;
  error(message: string, error?: Error, context?: Record<string, unknown>): void;
}
```

Note: `error()` has a different signature — it accepts an optional Error instance as the second argument for stack trace capture.

---

## Common Misclassifications

| Log Message | Wrong Level | Correct Level | Why |
|-------------|-------------|---------------|-----|
| Cold start recovery | warn | info | Recovery is expected, not degradation |
| Stale flush skip | warn | debug | Expected race condition, not actionable |
| Periodic heartbeat tick | info | debug | Routine operation, not state change |
| User authentication failed | info | error | Security event requiring investigation |
| Config validation warning | debug | warn | Human should know about config issues |

---

## Violation Rules

### missing_error_log_assertion
Error paths MUST have log assertions verifying correct error logging with context.
**Severity**: must-fail

### happy_path_logs_error
Happy paths MUST NOT produce warn or error logs. Use `assertNoLogsAbove(logger, 'info')`.
**Severity**: must-fail

### log_level_misclassification
Log levels MUST follow the policy. Routine operations at warn/error = alert fatigue.
**Severity**: should-fail

### missing_context_fields
Error logs MUST include context fields for debugging (component, userId, requestId, etc.).
**Severity**: should-fail

### console_spy_instead_of_mock
DO NOT spy on `console.*` — use a proper mock logger interface.
**Severity**: must-fail

---

## Companion Skills

This skill provides **testing utilities** for structured logging, not logging architecture guidance. For broader methodology:

- Search `logging` or `observability` on [skills.sh](https://skills.sh) for production logging architecture, wide events, and OpenTelemetry integration
- Error paths tested here often originate from resilience scenarios — use [fault-injection-testing](https://github.com/apankov1/quality-engineering/tree/main/skills/fault-injection-testing) for circuit breaker, retry policy, and queue preservation testing
- State machine transitions should log state changes at correct levels — use [model-based-testing](https://github.com/apankov1/quality-engineering/tree/main/skills/model-based-testing) for systematic transition matrix coverage

---

## Quick Reference

| Assertion | When | Example |
|-----------|------|---------|
| `assertLogEntry` | Verify specific log | `assertLogEntry(logger, 'error', 'Failed', { component: 'X' })` |
| `assertNoLogsAbove` | Happy path validation | `assertNoLogsAbove(logger, 'info')` |
| `assertHasLogLevel` | Verify level exists | `assertHasLogLevel(logger, 'error')` |
| `assertErrorLogged` | Verify Error instance | `assertErrorLogged(logger, 'Failed', { name: 'TypeError' })` |
| `classifyLogLevel` | Suggest correct level | `classifyLogLevel("Connection timeout")` → 'warn' |

See [patterns.md](./references/patterns.md) for correlation field patterns, log level migration guides, and framework integration.
