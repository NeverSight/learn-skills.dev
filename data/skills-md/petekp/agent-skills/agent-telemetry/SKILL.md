---
name: agent-telemetry
description: Make application behavior visible to coding agents by exposing structured logs and telemetry. Use when asked to "add telemetry", "make logs accessible to agents", "add observability", "debug with logs", or when an agent needs to understand runtime behavior but has no way to query logs. Also use when debugging is difficult because there are no structured logs, when agent docs (CLAUDE.md, AGENTS.md) lack instructions for querying application logs, or when setting up logging infrastructure for a new or existing web application.
---

# Agent Telemetry

Make application runtime behavior queryable by coding agents through structured logging and telemetry endpoints.

## Core Problem

Coding agents debugging issues often can't answer "what actually happened at runtime?" because:
- Logs don't exist, or are unstructured `console.log` noise
- Logs exist but there's no documented way for agents to query them
- Agent docs (CLAUDE.md, AGENTS.md) don't mention how to access telemetry

## Workflow

### Phase 1: Audit Current State

Determine what telemetry already exists.

**1. Check for logging infrastructure:**

```bash
# Find logging configuration and usage
grep -r "winston\|pino\|bunyan\|log4j\|slog\|Logger\|logging\.config" --include="*.{ts,js,py,rb,go,rs}" -l .
```

```bash
# Find log output configuration
grep -r "LOG_LEVEL\|LOG_FORMAT\|LOG_FILE\|OTEL_\|SENTRY_DSN" .env* config/ -l 2>/dev/null
```

**2. Check for existing telemetry endpoints:**

```bash
# Health/debug/metrics endpoints
grep -r "health\|metrics\|debug\|status\|readiness\|liveness" --include="*.{ts,js,py,rb,go}" -l src/ app/ 2>/dev/null
```

**3. Check agent docs for log access instructions:**

```bash
# Do agent docs mention logs?
grep -ri "log\|telemetry\|debug\|observ" CLAUDE.md AGENTS.md .claude/*.md .cursor/*.md 2>/dev/null
```

**4. Classify the result:**

| Finding | Action |
|---------|--------|
| No structured logging exists | Go to Phase 2 |
| Logging exists but no agent access | Go to Phase 3 |
| Logging + access exists but undocumented | Go to Phase 4 |
| Everything in place | Validate and suggest improvements |

### Phase 2: Add Structured Logging

If no structured logging exists, add it. See `references/logging-setup.md` for framework-specific patterns.

**Principles:**
- Use structured JSON logs, not string interpolation
- Include correlation IDs for request tracing
- Log at boundaries: incoming requests, outgoing calls, errors, state transitions
- Use consistent field names: `timestamp`, `level`, `message`, `requestId`, `userId`, `duration`, `error`

**Where to add logging (priority order):**
1. Request/response middleware (every request gets logged)
2. Error handlers (unhandled errors get captured with context)
3. External service calls (DB queries, API calls, queue operations)
4. Business logic decision points (state transitions, authorization decisions)

**Minimum viable logging — add a request logger middleware that captures:**
```
{timestamp, level, requestId, method, path, statusCode, duration, userId?}
```

This single addition makes most debugging possible.

### Phase 3: Expose Logs to Agents

Agents need a way to query logs without SSH access or cloud console dashboards. Provide at least one of:

**Option A: Log file (simplest)**
Write structured logs to a known file path agents can read directly.

```
# Agent reads recent errors
tail -100 logs/app.json | jq 'select(.level == "error")'

# Agent reads logs for a specific request
grep "requestId.*abc123" logs/app.json | jq .
```

**Option B: Dev log endpoint (recommended for web apps)**
Add a development-only endpoint that returns recent log entries with filtering.

```
GET /__dev/logs?level=error&last=50
GET /__dev/logs?path=/api/users&last=20
GET /__dev/logs?requestId=abc-123
```

This endpoint must:
- Only be available in development (`NODE_ENV=development` or equivalent)
- Return JSON array of log entries
- Support filtering by level, path, timerange, requestId
- Limit response size (default 100 entries)

See `references/dev-endpoint.md` for implementation patterns by framework.

**Option C: CLI query tool**
Wrap log access in a script agents can execute:

```bash
# Query recent errors
./scripts/query-logs.sh --level error --last 50

# Query by request path
./scripts/query-logs.sh --path /api/users --since "5 minutes ago"
```

**Choose based on project context:**

| Project Type | Best Option |
|-------------|-------------|
| Next.js / Express / Rails with local dev | Option B (dev endpoint) |
| CLI tool or background worker | Option A (log file) |
| Docker-based development | Option A (mounted log volume) or Option C |
| Monorepo with multiple services | Option C (unified query script) |

### Phase 4: Document in Agent Docs

This is critical. Without documentation, agents won't know telemetry exists.

**Update CLAUDE.md (or equivalent agent doc) with a Debugging section:**

```markdown
## Debugging

### Querying Application Logs

Structured JSON logs are available at [location].

**Quick commands:**

```bash
# View recent errors
[command to view errors]

# View logs for a specific endpoint
[command to filter by path]

# View logs for a specific request
[command to filter by request ID]

# View logs from the last N minutes
[command to filter by time]
```

**Log format:**
```json
{
  "timestamp": "ISO-8601",
  "level": "info|warn|error",
  "message": "Human-readable description",
  "requestId": "correlation-id",
  "method": "GET",
  "path": "/api/resource",
  "statusCode": 200,
  "duration": 45
}
```

**Common debugging workflows:**
- User reports error → query by time range and error level
- Flaky test → query by endpoint path during test run
- Performance issue → query by path, sort by duration
```

**Key rules for the documentation:**
- Include copy-pasteable commands (agents execute, not read)
- Show the log schema so agents know what fields to filter on
- List 3-4 common debugging workflows with exact commands
- Mention where log config lives for agents that need to adjust log levels

### Phase 5: Validate

Test the full loop:

1. **Trigger a request** — hit an endpoint or run an operation
2. **Query the logs** — use the documented method to find the log entry
3. **Verify agent usability** — can an agent find the relevant log in <3 commands?
4. **Check error capture** — trigger an error and verify it appears with full context

If any step fails, iterate on the logging or documentation.

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do Instead |
|-------------|-------------|-----------|
| `console.log("here")` | No structure, no context, no filtering | Structured JSON with consistent fields |
| Logs only in cloud dashboard | Agents can't access Datadog/CloudWatch | Local file or dev endpoint |
| Log everything at debug level | Too noisy, can't find signal | Log at boundaries, use appropriate levels |
| Logging sensitive data | PII in logs is a liability | Redact tokens, passwords, PII |
| No request correlation | Can't trace a request across log lines | Add requestId to every log entry |
| Docs say "check the logs" with no how | Agent doesn't know where or how | Exact commands with examples |
