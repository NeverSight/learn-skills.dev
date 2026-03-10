---
name: workleap-logging
description: |
  Guide for @workleap/logging, a structured logging library for Workleap frontend TypeScript applications.

  Use this skill when:
  (1) Setting up or configuring @workleap/logging loggers (BrowserConsoleLogger, CompositeLogger)
  (2) Using @workleap/logging API: log levels, chained segments, scopes, styled output
  (3) Composing or filtering @workleap/logging loggers for multi-destination logging
  (4) Integrating @workleap/logging with LogRocket via CompositeLogger
  (5) Reviewing PRs or troubleshooting @workleap/logging usage
metadata:
  version: 1.2
---

# Workleap Logging (@workleap/logging)

A structured logging library for Workleap frontend applications. Provides composable, styled console logging with support for scopes, multiple log levels, and integration with telemetry tools.

## Installation

```bash
pnpm add @workleap/logging
```

## Core Concepts

### Loggers
- **BrowserConsoleLogger**: Outputs to browser console with styling support
- **CompositeLogger**: Forwards logs to multiple underlying loggers

### Log Levels (lowest to highest severity)
1. `debug` - Detailed diagnostic info for development
2. `information` - General application flow events
3. `warning` - Non-critical issues needing attention
4. `error` - Failures preventing functionality
5. `critical` - Severe errors risking data integrity

### Scopes
Group related log entries under a label. Useful for tracing operations or correlating events.

**IMPORTANT:** Only a `RootLogger` instance can start a scope. If the logger is typed as a `Logger` (e.g., when using `useLogger()` from Squide), you must cast it to `RootLogger` before starting a scope:

```ts
// Squide example:
import { useLogger } from "@squide/firefly";
import type { RootLogger } from "@workleap/logging";

const logger = useLogger();
(logger as RootLogger).startScope("User signup");
```

## Chained Segments

Build complex log entries by chaining segments. **Always complete the chain with a log level method** (`.debug()`, `.error()`, etc.) or nothing is output.

```ts
logger
    .withText("Processing order")
    .withObject({ orderId: 123 })
    .withError(new Error("Failed"))
    .error();
```

## Common Mistakes

1. **Forgetting to call log method**: Chained segments require `.debug()`, `.error()`, etc. to output
2. **Not ending scopes**: Always call `scope.end()` or logs won't output
3. **Using wrong log level**: Use `error` for failures, not `warning`
4. **Logging sensitive data**: Never log passwords, tokens, or PII
5. **Missing error context**: Always include `withObject()` for relevant data and `withError()` for exceptions
6. **Calling startScope on a non-RootLogger**: Only `RootLogger` instances can start scopes. When using `useLogger()` from Squide, cast to `RootLogger` first: `(logger as RootLogger).startScope("Label")`

## Reference Guide

For detailed documentation beyond the patterns above, consult:

- **`references/api.md`** — Logger constructors, all methods (styled text, line breaks), scope API, createCompositeLogger, log level guidelines
- **`references/patterns.md`** — Common patterns (app setup, error logging, scoping, multi-destination), LogRocket integration, PR review checklist
