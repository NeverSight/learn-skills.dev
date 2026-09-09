---
name: oodle-synthetic
description: Create and manage Oodle synthetic monitors — HTTP and TCP health checks with assertions and configurable intervals.
metadata:
  version: "1.0.0"
  author: oodle-ai
  repository: https://github.com/oodle-ai/agent-skills
  tags: oodle,synthetic,monitoring,health-checks
  globs: "**/*synthetic*"
  alwaysApply: "false"
---

# Oodle Synthetic Monitors — HTTP / TCP Checks

This skill teaches the agent to configure synthetic monitors that actually catch failures: assertions, sane intervals, and update-without-overwrite.

## Prerequisites

```bash
brew install oodle-ai/oodle/oodle
oodle configure
```

Confirm the synthetic-monitors endpoint works:

```bash
oodle synthetic-monitors list -o json | jq 'length'
```

## Command Execution Order

Before running any oodle command:
1. Check whether the target URL or hostport is already in context.
2. If not, ask the user to confirm the target.
3. Test the target manually (`curl -I <url>`) to confirm it is reachable from the public internet.
4. Run `oodle synthetic-monitors create -f monitor.json`.
5. After creation, verify the first run succeeded with `oodle synthetic-monitors get <id> -o json`.

## Quick Reference

| Task | Command |
|------|---------|
| List monitors | `oodle synthetic-monitors list -o json` |
| Get monitor | `oodle synthetic-monitors get <id> -o json` |
| Create monitor | `oodle synthetic-monitors create -f monitor.json` |
| Update monitor | `oodle synthetic-monitors update <id> -f monitor.json` |
| Delete monitor | `oodle synthetic-monitors delete <id> --force` |

## Common Operations

### Synthetic monitor schema (HTTP)

```json
{
  "name": "API health check",
  "type": "http",
  "target": "https://api.example.com/health",
  "interval": 60,
  "assertions": [
    {"type": "statusCode",   "value": "200"},
    {"type": "responseTime", "value": "2000"}
  ]
}
```

| Field | Meaning |
|-------|---------|
| `type` | `http` or `tcp` |
| `target` | URL (HTTP) or `host:port` (TCP) |
| `interval` | Seconds between probes; minimum 30, recommended ≥ 60 |
| `assertions[].type` | `statusCode`, `responseTime`, `bodyContains`, `headerEquals` |
| `assertions[].value` | String form of the expected value (e.g. `"200"`, `"2000"`, `"ok"`) |

### Synthetic monitor schema (TCP)

```json
{
  "name": "Postgres reachability",
  "type": "tcp",
  "target": "postgres.example.com:5432",
  "interval": 60,
  "assertions": [
    {"type": "responseTime", "value": "1000"}
  ]
}
```

### Creating a monitor

```bash
# ✅ CORRECT — manual reachability test, then create
curl -sSfI https://api.example.com/health
oodle synthetic-monitors create -f monitor.json

# ❌ WRONG — creating against an unreachable target leaves a permanently-failing monitor
oodle synthetic-monitors create -f monitor.json
```

### Updating a monitor

```bash
# ✅ CORRECT — get → edit → update preserves all assertions
oodle synthetic-monitors get syn_123 -o json > monitor.json
jq '.interval = 30' monitor.json > monitor.new.json
oodle synthetic-monitors update syn_123 -f monitor.new.json

# ❌ WRONG — partial payload removes assertions
oodle synthetic-monitors update syn_123 -f <(echo '{"interval":30}')
```

### Deleting a monitor

```bash
# ✅ CORRECT
oodle synthetic-monitors get syn_123 -o json > /dev/null
oodle synthetic-monitors delete syn_123 --force

# ❌ WRONG — name-grep delete
oodle synthetic-monitors delete "$(oodle synthetic-monitors list | grep health | awk '{print $1}')" --force
```

## Best Practices

### Use `interval: 60` (or higher) for non-critical endpoints

A 10-second interval on every endpoint multiplies cost and noise. Reserve short intervals for critical user-facing flows.

```bash
# ✅ CORRECT — 60s interval for a /health endpoint
"interval": 60

# ❌ WRONG — 10s on dozens of internal endpoints
"interval": 10
```

### Always include at least one `statusCode` assertion

A monitor with no assertions only checks TCP reachability — it will pass even if the app returns 500 to every request.

```bash
# ✅ CORRECT
"assertions": [{"type":"statusCode","value":"200"},{"type":"responseTime","value":"2000"}]

# ❌ WRONG — monitor "succeeds" on a 500 response
"assertions": []
```

### Add a `responseTime` assertion to catch slow dependencies

A 200 response that takes 30 seconds is still a failure for users.

```bash
# ✅ CORRECT
"assertions": [
  {"type":"statusCode","value":"200"},
  {"type":"responseTime","value":"2000"}
]

# ❌ WRONG — only checks status code, doesn't catch latency regressions
"assertions": [{"type":"statusCode","value":"200"}]
```

### Always `get` before `update` to preserve assertions

Update is a full-document replace.

```bash
# ✅ CORRECT
oodle synthetic-monitors get syn_123 -o json > m.json
jq '.assertions += [{"type":"bodyContains","value":"ok"}]' m.json > m.new.json
oodle synthetic-monitors update syn_123 -f m.new.json

# ❌ WRONG — drops `assertions` and `target`
oodle synthetic-monitors update syn_123 -f <(echo '{"interval":120}')
```

### Use a stable `name` per environment

Encode env in the name (`API health check (prod)`, `API health check (staging)`) so the alert recipient knows which env to investigate.

```bash
# ✅ CORRECT
"name": "API health check (prod)"

# ❌ WRONG
"name": "health"
```

## Failure Handling

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Invalid or missing API key | Run `oodle configure` or set `OODLE_API_KEY` |
| 404 Not Found | Synthetic monitor ID does not exist | Verify with `oodle synthetic-monitors list -o json` |
| connection refused | Wrong `OODLE_DEPLOYMENT` URL | Check `OODLE_DEPLOYMENT` env var |
| Monitor permanently red | Target unreachable from the probe egress | `curl -I` from the public internet; check firewall, DNS, TLS cert |
| Monitor flaps | `interval` too aggressive or `responseTime` assertion too tight | Raise interval to 60s; raise `responseTime` to p95+headroom |
| Assertions silently dropped | `update` was called with a partial payload | Re-create from the last `get` snapshot; always `get` → edit → `update` |
| 429 Too Many Requests | Many probes scheduled at the same second | Stagger by editing `interval` per monitor; use `--retries 3` for bulk operations |

## References

- [Oodle CLI repo](https://github.com/oodle-ai/oodle-cli)
- [Oodle docs](https://docs.oodle.ai)
