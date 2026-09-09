---
name: oodle-log-metrics
description: Create and manage Oodle log-based metric rules — extract metrics from log streams using filter expressions and groupBy labels.
metadata:
  version: "1.0.0"
  author: oodle-ai
  repository: https://github.com/oodle-ai/agent-skills
  tags: oodle,log-metrics,logs,metrics
  globs: "**/*log-metric*,**/*logmetric*"
  alwaysApply: "false"
---

# Oodle Log Metrics — Rules and Cardinality

This skill teaches the agent to convert log streams into metrics safely: validate the filter, narrow the `groupBy`, and avoid creating high-cardinality time series.

## Prerequisites

```bash
brew install oodle-ai/oodle/oodle
oodle configure
```

Confirm the log-metrics endpoint works:

```bash
oodle log-metrics list -o json | jq 'length'
```

## Command Execution Order

Before running any oodle command:
1. Check whether the rule's filter and `groupBy` are already in context.
2. If not, run a sample log query (e.g. `oodle traces list ...` or the log explorer) to verify the filter actually matches logs.
3. Estimate cardinality: `groupBy` count × distinct values per label.
4. Run `oodle log-metrics create -f rule.json` only after the filter is validated.
5. Do not run `update` without first running `get` to capture the existing rule.

## Quick Reference

| Task | Command |
|------|---------|
| List rules | `oodle log-metrics list -o json` |
| Get rule | `oodle log-metrics get <id> -o json` |
| Create rule | `oodle log-metrics create -f rule.json` |
| Update rule | `oodle log-metrics update <id> -f rule.json` |
| Delete rule | `oodle log-metrics delete <id> --force` |

## Common Operations

### Rule schema

```json
{
  "name": "http_errors_from_logs",
  "filter": "level=error AND service=api",
  "groupBy": ["service", "env"],
  "metricName": "oodle.log.http_errors"
}
```

Field meaning:

| Field | Meaning |
|-------|---------|
| `name` | Human identifier for the rule |
| `filter` | Boolean expression over log fields (`AND`/`OR`/`NOT`, `=`, `!=`, `contains`) |
| `groupBy` | Labels promoted from log fields onto the emitted metric |
| `metricName` | The Prometheus-style metric name to emit |

### Creating a rule

```bash
# ✅ CORRECT — validate filter first, then create
# (preview with the log explorer or `oodle traces list` if traces and logs share the same backend)
oodle log-metrics create -f rule.json

# ❌ WRONG — creating with an untested filter; the resulting metric is silently empty
oodle log-metrics create -f <(echo '{"name":"x","filter":"levl=eror","groupBy":[],"metricName":"x"}')
```

### Updating a rule

```bash
# ✅ CORRECT — get → edit → update
oodle log-metrics get lm_123 -o json > rule.json
jq '.groupBy = ["service","env"]' rule.json > rule.new.json
oodle log-metrics update lm_123 -f rule.new.json

# ❌ WRONG — partial payload removes existing fields
oodle log-metrics update lm_123 -f <(echo '{"groupBy":["service"]}')
```

### Deleting a rule

```bash
# ✅ CORRECT — verify and delete
oodle log-metrics get lm_123 -o json > /dev/null
oodle log-metrics delete lm_123 --force

# ❌ WRONG — speculative delete by name match
oodle log-metrics delete "$(oodle log-metrics list | grep errors | awk '{print $1}')" --force
```

## Best Practices

### Validate the `filter` against real log volume before creating the rule

A typo in the filter (`levl=eror`) creates a rule that silently emits zero data points.

```bash
# ✅ CORRECT — preview matching log volume in the log explorer first;
# only then run `oodle log-metrics create`
# (or temporarily create a synthetic monitor that hits the matching logs and confirm count > 0)

# ❌ WRONG — create the rule, then notice the dashboard panel is empty next week
oodle log-metrics create -f rule.json
```

### Keep `groupBy` to 2–3 low-cardinality labels

Each label multiplies the time-series count. Avoid `request_id`, `user_id`, `trace_id`, `path` (with IDs).

```bash
# ✅ CORRECT — bounded labels
"groupBy": ["service", "env"]

# ❌ WRONG — `user_id` blows up cardinality (one series per user)
"groupBy": ["service", "env", "user_id"]
```

### Always `get` before `update` to preserve fields

`update` replaces the document. Sending a single field nulls everything else.

```bash
# ✅ CORRECT
oodle log-metrics get lm_123 -o json > rule.json
jq '.filter = "level=error AND service=api AND status=5xx"' rule.json > rule.new.json
oodle log-metrics update lm_123 -f rule.new.json

# ❌ WRONG — clobbers groupBy and metricName
oodle log-metrics update lm_123 -f <(echo '{"filter":"level=error"}')
```

### Use a stable, namespaced `metricName`

`oodle.log.<domain>.<measurement>` makes the metric easy to find in dashboards and drop rules.

```bash
# ✅ CORRECT
"metricName": "oodle.log.http_errors"

# ❌ WRONG — generic name collides with other rules
"metricName": "errors"
```

## Failure Handling

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Invalid or missing API key | Run `oodle configure` or set `OODLE_API_KEY` |
| 404 Not Found | Log-metric rule ID does not exist | Verify with `oodle log-metrics list -o json` |
| connection refused | Wrong `OODLE_DEPLOYMENT` URL | Check `OODLE_DEPLOYMENT` env var |
| `invalid filter expression` | Filter has a syntax error | Use `field=value` (no spaces around `=`); combine with `AND`/`OR`/`NOT` |
| Metric exists but has no data points | Filter doesn't match any logs | Re-test the filter in the log explorer; check label names match the log schema |
| Cardinality alarm in the UI | `groupBy` includes a high-cardinality field | Edit the rule to drop that field; old series age out at the regular retention |
| 429 Too Many Requests | Bulk rule creation | Add `--retries 3`, throttle to <10 creates per second |

## References

- [Oodle CLI repo](https://github.com/oodle-ai/oodle-cli)
- [Oodle docs](https://docs.oodle.ai)
