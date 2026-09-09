---
name: oodle-monitors
description: Create, update, and manage Oodle monitors — alerting thresholds, query scoping, and best practices to avoid alert fatigue.
metadata:
  version: "1.0.0"
  author: oodle-ai
  repository: https://github.com/oodle-ai/agent-skills
  tags: oodle,monitors,alerting,alerts
  globs: "**/*monitor*,**/*alert*"
  alwaysApply: "false"
---

# Oodle Monitors — CRUD and Alerting

This skill teaches the agent to build, validate, and update Oodle monitors so that alerts are actionable, scoped, and free from flapping.

## Prerequisites

```bash
# Install + configure (see oodle-cli skill)
brew install oodle-ai/oodle/oodle
oodle configure
# or
export OODLE_API_KEY=<key>
export OODLE_INSTANCE=<instance>
export OODLE_DEPLOYMENT=<url>
```

Confirm authentication and that at least one monitor list call succeeds before creating new monitors:

```bash
oodle monitors list -o json | jq 'length'
```

## Command Execution Order

Before running any oodle command:
1. Check whether the required resource ID or name is already in context.
2. If not, run the discovery command (e.g., `oodle monitors list -o json`).
3. If the result is ambiguous, ask the user to confirm before proceeding.
4. Run the target command with the resolved ID.
5. Do not run speculative commands (e.g., do not `delete` without first `get`-ing the resource).

## Quick Reference

| Task | Command |
|------|---------|
| List all monitors | `oodle monitors list -o json` |
| Filter by status | `oodle monitors list --status alert -o json` |
| Filter by labels | `oodle monitors list --labels env=prod,team=platform -o json` |
| Get one monitor | `oodle monitors get <id> -o json` |
| Create from file | `oodle monitors create -f monitor.json` |
| Update from file | `oodle monitors update <id> -f monitor.json` |
| Delete (CI) | `oodle monitors delete <id> --force` |

## Common Operations

### Listing monitors

```bash
# ✅ CORRECT — JSON output for scripting
oodle monitors list -o json

# ✅ CORRECT — narrow with --status to find only firing alerts
oodle monitors list --status alert -o json

# ✅ CORRECT — narrow with --labels for a specific team
oodle monitors list --labels env=prod,team=platform -o json

# ❌ WRONG — pulling everything then grepping
oodle monitors list | grep CPU
```

### Reading a monitor before changing it

```bash
# ✅ CORRECT — fetch full JSON, edit, then update
oodle monitors get mon_123 -o yaml > monitor.yaml
$EDITOR monitor.yaml
oodle monitors update mon_123 -f monitor.yaml

# ❌ WRONG — building update payload from memory; overwrites unrelated fields
oodle monitors update mon_123 -f <(echo '{"options":{"thresholds":{"critical":90}}}')
```

### Creating a monitor

A complete, valid monitor JSON:

```json
{
  "name": "High CPU on web servers",
  "type": "metric alert",
  "query": "avg(last_5m):avg:system.cpu.user{env:prod,service:api} by {host} > 80",
  "message": "CPU above 80% on {{host.name}}. Runbook: https://runbooks.example.com/cpu\n@slack-ops",
  "labels": {"team": "platform", "env": "prod"},
  "options": {
    "thresholds": {
      "critical": 80,
      "critical_recovery": 70,
      "warning": 60,
      "warning_recovery": 50
    }
  }
}
```

```bash
# ✅ CORRECT
oodle monitors create -f monitor.json

# ❌ WRONG — no `type`, no `options.thresholds`, monitor will be rejected
oodle monitors create -f <(echo '{"name":"x","query":"y"}')
```

### Updating a monitor

```bash
# ✅ CORRECT — get → edit → update
oodle monitors get mon_123 -o json > monitor.json
jq '.options.thresholds.critical = 85' monitor.json > monitor.new.json
oodle monitors update mon_123 -f monitor.new.json

# ❌ WRONG — sending only the changed field; missing fields become null
oodle monitors update mon_123 -f <(echo '{"options":{"thresholds":{"critical":85}}}')
```

### Deleting a monitor

```bash
# ✅ CORRECT — verify first, then delete
oodle monitors get mon_123 -o json > /dev/null
oodle monitors delete mon_123 --force

# ❌ WRONG — speculative delete by name match
oodle monitors delete "$(oodle monitors list | grep CPU | head -1 | awk '{print $1}')" --force
```

## Best Practices

### Use a `last_5m` (or longer) evaluation window, not `last_1m`

Short windows cause alert flapping on normal traffic spikes. Use `last_5m` minimum for production alerts, `last_15m` for noisy metrics.

```bash
# ✅ CORRECT
"query": "avg(last_5m):avg:system.cpu.user{env:prod} by {host} > 80"

# ❌ WRONG — flaps on every brief spike
"query": "avg(last_1m):avg:system.cpu.user{env:prod} by {host} > 80"
```

### Scope queries with explicit labels — never use `{*}`

`{*}` matches every series in the system and produces alerts for resources you don't own.

```bash
# ✅ CORRECT — scoped to a specific env + service
"query": "avg(last_5m):avg:system.cpu.user{env:prod,service:api} by {host} > 80"

# ❌ WRONG — alerts on every host in the org
"query": "avg(last_5m):avg:system.cpu.user{*} > 80"
```

### Always set `*_recovery` thresholds below the trigger thresholds

Without recovery thresholds the monitor stays in `alert` state until the metric drops below the critical threshold exactly — small oscillations keep the alert active forever.

```bash
# ✅ CORRECT — clear recovery band (10pt below trigger)
"thresholds": {"critical": 80, "critical_recovery": 70, "warning": 60, "warning_recovery": 50}

# ❌ WRONG — no recovery values; monitor never cleanly recovers
"thresholds": {"critical": 80, "warning": 60}
```

### Put a runbook URL and an `@notifier` handle in `message`

Alerts without an action are noise. Every monitor message must answer "what do I do?" and "who is paged?".

```bash
# ✅ CORRECT
"message": "CPU above 80% on {{host.name}} (env=prod, service=api).\nRunbook: https://runbooks.example.com/cpu\n@slack-ops @pagerduty-platform"

# ❌ WRONG — no actionable content, no routing
"message": "CPU is high"
```

### Tag every monitor with at least `team` and `env` labels

Labels are how notification policies route alerts and how `oodle monitors list --labels ...` filters work.

```bash
# ✅ CORRECT
"labels": {"team": "platform", "env": "prod", "service": "api"}

# ❌ WRONG
"labels": {}
```

## Failure Handling

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Invalid or missing API key | Run `oodle configure` or set `OODLE_API_KEY` |
| 404 Not Found | Monitor ID does not exist | Verify with `oodle monitors list -o json` |
| connection refused | Wrong `OODLE_DEPLOYMENT` URL | Check `OODLE_DEPLOYMENT` env var |
| `invalid query` | PromQL/Datadog-style query has a syntax error | Test the query in the UI metrics explorer; ensure `avg(last_5m):` prefix and `by {label}` suffix |
| Alert never fires | Query returns no data, or threshold is unreachable | Run `oodle metrics list --match <metric>` to confirm the metric exists; lower the threshold temporarily and re-check |
| Too many alerts (flapping) | Evaluation window too short, missing recovery thresholds | Increase window to `last_5m` or `last_15m`; set `critical_recovery` and `warning_recovery` |
| `no data` alerts | Agent not reporting, or label filter excludes all hosts | Verify the agent is alive (`oodle metrics list --match up`); widen the label filter to confirm any series match |
| 429 Too Many Requests | Bulk monitor creation hit rate limit | Add `--retries 3`, throttle to <10 creates per second |

## References

- [Oodle CLI repo](https://github.com/oodle-ai/oodle-cli)
- [Oodle docs](https://docs.oodle.ai)
