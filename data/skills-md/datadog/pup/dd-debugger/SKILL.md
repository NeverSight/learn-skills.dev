---
name: dd-debugger
description: Live Debugger - inspect runtime argument/variable values in production by placing log probes on methods. Use when asked what values a function receives, what parameters look like at runtime, or to capture live data from running services without redeploying.
metadata:
  version: "1.1.0"
  author: datadog-labs
  repository: https://github.com/datadog-labs/agent-skills
  tags: datadog,debugger,live-debugger,probes,dd-debugger
  globs: ""
  alwaysApply: "false"
---

# Datadog Live Debugger

Place log probes on running services without redeploying. Create probes with custom templates and conditions, and stream captured events in real time.

## Prerequisites

`pup` must be installed:

```bash
brew tap datadog-labs/pack && brew install pup
```

## Authentication

Authenticate via OAuth2 (recommended) or API keys:

```bash
# OAuth2 (recommended)
pup auth login

# Or use API keys
export DD_API_KEY="key" DD_APP_KEY="key" DD_SITE="datadoghq.com"
```

## Typical Workflow

**Prefer `--capture` expressions** over full snapshots. Capture expressions are lighter-weight, faster, and return exactly the data you need.

1. If you don't know the service, **ask the user** before proceeding.
2. **Verify the service** using `pup debugger context <service>` to list environments with active instances. If multiple environments exist, **ask the user** which one to target before proceeding.
3. **Find a method** using the `dd-symdb` skill (`pup symdb search --view probe-locations`)
4. **Place a probe** with capture expressions for the values you need
5. **Watch** events with `--fields` for compact output
6. **Delete** the probe when done

```bash
# 0. List environments (if multiple, ask user which to use)
pup debugger context my-service --fields service,language,envs

# 1. Create a probe with capture expressions (recommended)
#    Use --fields id to get just the probe ID back
pup debugger probes create \
  --service my-service \
  --env production \
  --probe-location "com.example.MyController:handleRequest" \
  --capture "request.id" \
  --capture "request.headers" \
  --ttl 1h \
  --fields id

# 2. Stream events with compact output
pup debugger probes watch <PROBE_ID> --timeout 60 --limit 10 \
  --fields "message,captures,timestamp"

# 3. Clean up
pup debugger probes delete <PROBE_ID>
```

## Service Context

**Always run this before creating probes.** It returns JSON by default (like all other commands) showing environments with active instances, tracer versions, and supported probe features. If the service runs in multiple environments, ask the user which one to target — don't guess.

```bash
# Full JSON output (default)
pup debugger context my-service

# Compact: just the fields you need
pup debugger context my-service --fields service,language,envs

# Filter to a specific environment
pup debugger context my-service --env production --fields service,envs,repo
```

| Flag | Description | Default |
|------|-------------|---------|
| `--env` | Filter to a specific environment | All environments |
| `--fields` | Comma-separated fields: `service`, `language`, `envs`, `repo` | Full JSON response |

## Probe Management

### List Probes

```bash
# All probes
pup debugger probes list

# Filter by service
pup debugger probes list --service my-service
```

### Get Probe Details

```bash
pup debugger probes get <PROBE_ID>
```

### Create a Log Probe

```bash
pup debugger probes create \
  --service my-service \
  --env staging \
  --probe-location "com.example.MyClass:myMethod" \
  --capture "user.name" \
  --capture "order.items[0].price"
```

To disambiguate overloaded methods, pass a signature with argument types:

```bash
pup debugger probes create \
  --service my-service \
  --env staging \
  --probe-location "com.example.MyClass:myMethod(int, java.lang.String)" \
  --capture "user.name"
```

**Options:**

| Flag | Description | Default |
|------|-------------|---------|
| `--service` | Service name (required) | — |
| `--env` | Environment (required) | — |
| `--probe-location` | `TYPE:METHOD` or `TYPE:METHOD(args)` (required). The signature form disambiguates overloaded methods. | — |
| `--language` | `java`, `python`, `dotnet`, `go` | Auto-detected from symdb |
| `--capture EXPR` | Capture expression (repeatable). Use dot notation for fields, brackets for indexing. | None |
| `--capture` | Without value: enable full snapshot (capture everything). | No snapshot |
| `--template` | Log message template with `{variable}` placeholders. Can combine with `--capture`. | Auto-generated |
| `--condition` | DSL condition to filter captures | None |
| `--depth` | How deep the tracer traverses the object graph when capturing (1–5). Start at 1 to see field names/types, increase to drill in. | `1` |
| `--rate` | Snapshots per second | `1` |
| `--budget` | Max probe hits. Only "total" window supported (hourly/daily not yet available). | `1000` |
| `--ttl` | Probe time-to-live (e.g., `10m`, `1h`, `24h`). Probe auto-expires. | `1h` |

### Capture Expressions (Recommended)

**Always prefer capture expressions over full snapshots.** They are lighter-weight and return exactly the data you need.

```bash
# Capture specific fields using dot notation
--capture "user.name"
--capture "request.headers"

# Access array elements
--capture "orders[0].total"
--capture "items[len(items)].name"

# Chain member access
--capture "response.body.data.id"
```

Multiple `--capture` flags can be combined. Each expression is independently evaluated.

```bash
# Capture multiple specific values
pup debugger probes create \
  --service my-service --env prod \
  --probe-location "OrderService:processOrder" \
  --capture "order.id" \
  --capture "order.items[0].price" \
  --capture "customer.email"
```

> **Tip:** Start with `--depth 1` (the default) to see field names and types, then increase depth to drill into interesting subtrees. Use `--depth 5` for deeply nested objects.

### Full Snapshot (use sparingly)

Use bare `--capture` (no value) only when you don't know which fields to inspect:

```bash
# Full snapshot — captures all arguments, locals, return value
pup debugger probes create \
  --service my-service --env staging \
  --probe-location "com.example.MyClass:myMethod" \
  --capture
```

You can combine snapshot with capture expressions:

```bash
# Full snapshot + specific expressions
--capture --capture "user.name"
```

### Templates

Templates can be used alongside capture expressions for custom log messages:

```bash
# Template with capture expressions
pup debugger probes create \
  --service my-service --env prod \
  --probe-location "MyClass:myMethod" \
  --capture "user.id" \
  --template "Processing request for user={user.id}, took {@duration}ms"
```

**Template syntax** uses `{variable}` placeholders:

```bash
--template "Processing order={orderId} for user={userId}"
--template "handleRequest took {@duration}ms"
```

**Conditions** filter when the probe fires:

```bash
--condition "status == 'error'"
--condition "@duration > 100"
```

### Delete a Probe

```bash
pup debugger probes delete <PROBE_ID>
```

## Watch Probe Events

Stream log events and status errors from a probe in real time.

```bash
pup debugger probes watch <PROBE_ID>
```

**Options:**

| Flag | Description | Default |
|------|-------------|---------|
| `--timeout` | Exit after N seconds | `120` |
| `--limit` | Exit after N log events | unlimited |
| `--from` | Start time for log query | `now` |
| `--wait` | Wait up to N seconds for the probe to become available | `0` |
| `--fields` | Comma-separated fields to include: `message`, `captures`, `timestamp`. Compact JSON output. | Full debugger payload |

**Behavior:**
- Without `--fields`: outputs the trimmed debugger payload (snapshot, probe info, stack) — not the full log envelope
- With `--fields`: outputs only the requested fields as compact JSON per event
- Polls for new log events and probe status errors every 1s
- Default `--from` is `now` — only shows new events going forward
- Use `--from 5m` or `--from 1h` to include recent historical events
- Probe status errors (e.g., instrumentation failures) go to stderr
- Exit code 0 if events received, 1 if timed out with no events
- Use `--wait <seconds>` to retry probe existence check (handles create → watch pipeline); default is 0 (fail immediately if not found)

### Using `--fields` for compact output

For most agent use cases, `--fields` gives you exactly what you need without jq:

```bash
# Message + captures + timestamp (most common)
pup debugger probes watch <ID> --fields "message,captures,timestamp" --limit 5

# Template message only (one line per event)
pup debugger probes watch <ID> --fields "message" --limit 10

# Just captures (expression values or snapshot data)
pup debugger probes watch <ID> --fields "captures" --limit 1
```

### Extracting fields with jq (reference)

When using the default output (no `--fields`), the debugger payload is at the top level. Common jq patterns:

```bash
# Extract a specific captured expression
pup debugger probes watch <ID> --limit 1 \
  | jq '.snapshot.captures.return.captureExpressions'

# Get captured argument values
pup debugger probes watch <ID> --limit 1 \
  | jq '.snapshot.captures.return.arguments'
```

**Default output structure (trimmed to debugger payload):**
```
.snapshot.captures.return.arguments          → method arguments
.snapshot.captures.return.locals             → local variables
.snapshot.captures.return.captureExpressions → capture expression values
.snapshot.probe.id                           → probe ID
.snapshot.probe.location                     → source location
```

## Supported Languages

| Language | `--language` value |
|----------|-------------------|
| Java | `java` |
| Python | `python` |
| .NET | `dotnet` |

## Failure Handling

| Problem | Fix |
|---------|-----|
| Wrong env / no instances | Use `pup debugger context <service>` to list valid environments |
| "probe not found" | Use `--wait <seconds>` to retry, e.g. `pup debugger probes watch <ID> --wait 10` |
| No events appearing | Check `--from` (default is `now`); probe may need time to instrument |
| Instrumentation errors | Check stderr output from watch for status errors |
| Auth error | Run `pup auth login` or set `DD_API_KEY` + `DD_APP_KEY` + `DD_SITE` |
| Wrong method signature | Use the `dd-symdb` skill to find exact `TYPE:METHOD` or `TYPE:METHOD(args)` values |

## References

- [Live Debugger Docs](https://docs.datadoghq.com/dynamic_instrumentation/)
- [Log Probe Templates](https://docs.datadoghq.com/dynamic_instrumentation/symdb/expressions/)
