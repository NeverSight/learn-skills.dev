---
name: logg
description: >-
  Guide for using @guiiai/logg — a lightweight structured logger for Node.js and browser.
  Use this skill whenever the user imports from '@guiiai/logg', mentions logg, needs
  structured logging with JSON or pretty output, wants caller-aware logs with clickable
  hyperlinks, needs child loggers with persistent fields, or asks about lightweight
  alternatives to winston, pino, or bunyan. Also use when setting up application logging
  with log levels, custom formatters, or error extraction.
license: MIT
metadata:
  author: guiiai
  version: "1.2.0"
---

# @guiiai/logg

Lightweight structured logger for Node.js and browser with stack parsing, caller records, and clickable hyperlinks.

## Quick Start

```ts
import { initLogger, useGlobalLogger } from '@guiiai/logg'

// Initialize with defaults (Verbose level, Pretty format)
initLogger()

const log = useGlobalLogger('MyApp')
log.log('Hello world!')
```

## Core API

### Creating Loggers

```ts
import { createLogg, createLogger, createGlobalLogger } from '@guiiai/logg'

// Named context
const log = createLogg('http/request').useGlobalConfig()

// Auto-context from call site (includes file:line clickable hyperlinks)
const log = createLogger().useGlobalConfig()

// Auto-context + auto global config
const log = createGlobalLogger()
```

**Aliases**: `useLogg` = `createLogg`, `useLogger` = `createLogger`, `useGlobalLogger` = `createGlobalLogger`

### Log Levels

```ts
import { LogLevel, setGlobalLogLevel, setGlobalLogLevelString } from '@guiiai/logg'

setGlobalLogLevel(LogLevel.Debug)
// or
setGlobalLogLevelString('debug')
```

| Level | Value | Description |
|-------|-------|-------------|
| `Error` | 0 | Only errors |
| `Warning` | 1 | Errors + warnings |
| `Log` | 2 | + general logs |
| `Verbose` | 3 | + verbose info |
| `Debug` | 4 | Everything |

### Output Formats

```ts
import { Format, setGlobalFormat } from '@guiiai/logg'

setGlobalFormat(Format.Pretty) // Colored human-readable output
setGlobalFormat(Format.JSON)   // Structured JSON for production
```

**JSON output**:
```json
{"level":"log","context":"app","timestamp":"2024-01-01T00:00:00.000Z","message":"User logged in","fields":{"userId":"123"}}
```

**Pretty output**:
```
[2024-01-01 00:00:00] LOG app: User logged in { userId: '123' }
```

### Structured Fields

```ts
// Single field (fluent chaining)
log
  .withField('requestId', req.id)
  .withField('url', req.url)
  .error('Resource not found (404)')

// Multiple fields at once
log
  .withFields({ userId: '12345', ip: '192.168.1.1' })
  .log('User logged in')
```

### Child Loggers

Child loggers inherit parent config and carry persistent fields:

```ts
const parentLog = createLogg('app').useGlobalConfig()

const childLog = parentLog.child({
  module: 'database',
  version: '1.0.0',
})

childLog.log('Connected') // includes module + version fields automatically
```

### Error Handling

```ts
try {
  // ...
} catch (err) {
  // Automatically extracts message, stack trace, and cause
  log.withError(err).error('Operation failed')

  // Or inline
  log.errorWithError('Failed to process request', err)
}
```

### Custom Processors

```ts
// Custom time format
const log = createLogg('app')
  .useGlobalConfig()
  .withTimeFormatter(date => date.toLocaleString('en-US', { timeZone: 'America/New_York' }))

// Custom error processor
const log = createLogg('app')
  .useGlobalConfig()
  .withErrorProcessor(err => {
    if (err instanceof CustomError) return { ...err, customField: 'value' }
    return err
  })
```

## Configuration Methods (Fluent API)

All return a new logger instance (immutable):

| Method | Description |
|--------|-------------|
| `.useGlobalConfig()` | Apply global level/format settings |
| `.child(fields)` | Create child with persistent fields |
| `.withContext(ctx)` | Set context string |
| `.withLogLevel(level)` | Set log level |
| `.withFormat(format)` | Set output format |
| `.withField(key, value)` | Add single field |
| `.withFields(obj)` | Add multiple fields |
| `.withError(err)` | Attach error object |
| `.withTimeFormatter(fn)` | Custom timestamp format |
| `.withErrorProcessor(fn)` | Custom error transform |

## Typical Setup Pattern

```ts
import { Format, initLogger, LogLevel, useGlobalLogger } from '@guiiai/logg'

// Once at app entry
initLogger(
  process.env.NODE_ENV === 'production' ? LogLevel.Log : LogLevel.Debug,
  process.env.NODE_ENV === 'production' ? Format.JSON : Format.Pretty,
)

// In each module
const log = useGlobalLogger('module-name')
log.log('ready')
```

## Key Rules

1. Call `initLogger()` or `setGlobalLogLevel()` + `setGlobalFormat()` once at app startup
2. Use `.useGlobalConfig()` on logger instances to pick up global settings
3. `withField` / `withFields` / `child` return new instances — they don't mutate
4. Use `Format.JSON` in production, `Format.Pretty` in development
5. Works in both Node.js and browser — format auto-adapts

## Documentation

For the latest API reference, use context7 to query `@guiiai/logg` documentation.
