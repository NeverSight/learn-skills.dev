---
name: pino-logging
description: 'Pino high-performance JSON logger for Node.js with worker thread transports, child loggers, redaction, and framework integrations. Use when setting up structured logging, configuring log transports, adding request correlation IDs, redacting sensitive data, or integrating with Fastify, Hono, or Express. Use for pino, logging, structured-logs, request-id, correlation, redaction, transports, pino-http, pino-pretty.'
license: MIT
metadata:
  author: oakoss
  version: '1.0'
  source: 'https://github.com/pinojs/pino'
user-invocable: false
---

# Pino Logging

High-performance JSON logger for Node.js. Transports run in worker threads to keep the main event loop free. Produces NDJSON by default with automatic `level`, `time`, `pid`, `hostname`, and `msg` fields.

**When to use:** Structured logging in Node.js applications, request-scoped logging with correlation IDs, sensitive data redaction, multi-destination log routing, framework logging integration.

**When NOT to use:** Browser-only logging (pino has limited browser support), simple `console.log` debugging during development, projects that need human-readable logs by default (pino outputs JSON; use `pino-pretty` for dev).

**Package:** `pino` (v10+)

## Quick Reference

| Pattern             | API                                 | Key Points                                    |
| ------------------- | ----------------------------------- | --------------------------------------------- |
| Basic logger        | `pino()`                            | Defaults: level `info`, JSON to stdout        |
| Set level           | `pino({ level: 'debug' })`          | `fatal > error > warn > info > debug > trace` |
| Log with context    | `logger.info({ userId }, 'msg')`    | First arg is merged object, second is message |
| Error logging       | `logger.error({ err }, 'failed')`   | Pass errors as `err` key for serialization    |
| Child logger        | `logger.child({ requestId })`       | Bindings persist on all child logs            |
| Redaction           | `pino({ redact: ['password'] })`    | Paths use dot notation, supports wildcards    |
| Transport (worker)  | `pino({ transport: { target } })`   | Runs in worker thread, non-blocking           |
| Multiple transports | `transport: { targets: [...] }`     | Different levels per destination              |
| Pretty print (dev)  | `target: 'pino-pretty'`             | Dev only — not for production                 |
| File transport      | `target: 'pino/file'`               | Built-in, with `mkdir` option                 |
| Rotating files      | `target: 'pino-roll'`               | Size and time-based rotation                  |
| HTTP middleware     | `pinoHttp()` from `pino-http`       | Auto request/response logging                 |
| Request ID          | `genReqId` option in pino-http      | Generate or forward `X-Request-Id`            |
| Serializers         | `serializers: { req, res, err }`    | Transform objects before logging              |
| Formatters          | `formatters: { level, log }`        | Rename fields, transform output               |
| Custom levels       | `customLevels: { http: 35 }`        | Add levels between built-in ones              |
| Async destination   | `pino.destination({ sync: false })` | Buffered async writes                         |
| Fastify             | `fastify({ logger: true })`         | Built-in pino, `request.log`                  |
| Hono                | `hono-pino` middleware              | `c.get('logger')` in handlers                 |

## Common Mistakes

| Mistake                                    | Fix                                                                     |
| ------------------------------------------ | ----------------------------------------------------------------------- |
| Using `pino-pretty` in production          | Use JSON output in production; pretty-print only in dev via `transport` |
| Logging sensitive data (tokens, passwords) | Use `redact` option with paths to sensitive fields                      |
| Creating a new logger per request          | Use `logger.child({ requestId })` for request-scoped context            |
| Blocking main thread with file writes      | Use `pino.transport()` — runs in a worker thread                        |
| Using `JSON.stringify` on errors           | Pass errors as `{ err }` — pino serializes stack, cause chain           |
| Not forwarding `X-Request-Id` header       | Use `genReqId` in pino-http to check headers first                      |
| Logging inside hot loops                   | Check `logger.isLevelEnabled('debug')` before expensive operations      |
| Missing `fetch-depth: 0` with transports   | Transports are separate packages — install them as dependencies         |

## Delegation

> If the `hono` skill is available, delegate Hono middleware and routing patterns to it.
> If the `vitest-testing` skill is available, delegate test setup and mocking patterns to it.
> If the `sentry-setup-logging` skill is available, delegate Sentry integration to it — it covers `Sentry.pinoIntegration()` for forwarding pino logs to Sentry.
> Otherwise, recommend: `pnpm dlx skills add getsentry/sentry-for-claude -s sentry-setup-logging -a claude-code -y`

## References

- [Setup, configuration, and core API](references/setup-and-configuration.md)
- [Transports, destinations, and log routing](references/transports.md)
- [Child loggers, serializers, and redaction](references/child-loggers-and-redaction.md)
- [HTTP logging, correlation IDs, and framework integrations](references/http-and-frameworks.md)
