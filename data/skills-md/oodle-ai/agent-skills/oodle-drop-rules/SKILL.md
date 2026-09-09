---
name: oodle-drop-rules
description: Create and manage Oodle metric drop rules — reduce ingestion cost by dropping or sampling high-volume, low-value metrics.
metadata:
  version: "1.0.0"
  author: oodle-ai
  repository: https://github.com/oodle-ai/agent-skills
  tags: oodle,drop-rules,cost,metrics
  globs: "**/*drop-rule*,**/*droprule*"
  alwaysApply: "false"
---

# Oodle Drop Rules — Cost Control

This skill teaches the agent to drop or sample high-volume metrics safely: estimate the impact first, prefer sampling over dropping, and never silently delete a metric a dashboard depends on.

## Prerequisites

```bash
brew install oodle-ai/oodle/oodle
oodle configure
```

Confirm the drop-rules endpoint works:

```bash
oodle drop-rules list -o json | jq 'length'
```

## Command Execution Order

Before running any oodle command:
1. Check whether the target metric prefix and matchers are already in context.
2. If not, run `oodle metrics list --match <prefix> -o json | jq 'length'` to estimate impact.
3. Confirm no critical dashboards or monitors depend on the affected series:
   - `oodle dashboards list -o json | jq '.[] | select(.panels[]?.query | contains("<metric>"))'`
   - `oodle monitors list -o json | jq '.[] | select(.query | contains("<metric>"))'`
4. Prefer `action: sample` (e.g. `sampleRate: 0.1`) on the first attempt; switch to `action: drop` only after the sampled data confirms low value.
5. Run `oodle drop-rules create -f rule.json`.

## Quick Reference

| Task | Command |
|------|---------|
| List rules | `oodle drop-rules list -o json` |
| Get rule | `oodle drop-rules get <id> -o json` |
| Create rule | `oodle drop-rules create -f rule.json` |
| Update rule | `oodle drop-rules update <id> -f rule.json` |
| Delete rule | `oodle drop-rules delete <id> --force` |

## Common Operations

### Rule schema

```json
{
  "name": "drop-noisy-debug-metrics",
  "matchers": [
    {"name": "level", "value": "debug"},
    {"name": "env",   "value": "staging"}
  ],
  "action": "drop",
  "sampleRate": null
}
```

| Field | Meaning |
|-------|---------|
| `matchers` | All matchers must match for the rule to fire (logical AND) |
| `action` | `drop` (discard) or `sample` (keep a fraction) |
| `sampleRate` | Required when `action="sample"`; float in `(0,1]`. `null` for `drop` |

### Estimating impact before creating a rule

```bash
# ✅ CORRECT — count series that will be affected
oodle metrics list --match "debug_" -o json | jq 'length'

# ✅ CORRECT — confirm no dashboard panel queries the metric
oodle dashboards list -o json | jq '.[] | select(.panels[]?.query | contains("debug_traffic_total"))'

# ✅ CORRECT — confirm no monitor depends on it
oodle monitors list -o json | jq '.[] | select(.query | contains("debug_traffic_total"))'

# ❌ WRONG — create the rule first, find out from on-call later
oodle drop-rules create -f rule.json
```

### Creating a `sample` rule (safer first step)

```json
{
  "name": "sample-debug-metrics-staging",
  "matchers": [
    {"name": "__name__", "value": "debug_traffic_total"},
    {"name": "env",      "value": "staging"}
  ],
  "action": "sample",
  "sampleRate": 0.1
}
```

```bash
# ✅ CORRECT — keep 10% of the series; observe for a week before dropping
oodle drop-rules create -f rule.json
```

### Promoting a `sample` rule to `drop`

```bash
# ✅ CORRECT — get → switch action → update
oodle drop-rules get dr_123 -o json > rule.json
jq '.action = "drop" | .sampleRate = null' rule.json > rule.new.json
oodle drop-rules update dr_123 -f rule.new.json

# ❌ WRONG — partial payload nulls matchers
oodle drop-rules update dr_123 -f <(echo '{"action":"drop"}')
```

### Deleting (re-enabling ingestion)

```bash
# ✅ CORRECT
oodle drop-rules get dr_123 -o json > /dev/null
oodle drop-rules delete dr_123 --force

# ❌ WRONG — speculative delete by name match
oodle drop-rules delete "$(oodle drop-rules list | grep debug | awk '{print $1}')" --force
```

## Best Practices

### Estimate impact with `oodle metrics list --match <prefix> -o json | jq 'length'` before creating a rule

A drop rule that matches more series than expected can hide real signal.

```bash
# ✅ CORRECT
oodle metrics list --match "kube_pod_" -o json | jq 'length'
# 1742 series — confirm with the team that all 1742 are safe to drop before creating a rule

# ❌ WRONG — create rule based on a guess; later discover a critical metric was matched
oodle drop-rules create -f rule.json
```

### Prefer `action: sample` with `sampleRate: 0.1` on the first iteration

Sampling preserves enough signal to confirm the metric truly is low-value before fully dropping it.

```bash
# ✅ CORRECT — week 1: sample at 10%, observe dashboards
"action": "sample", "sampleRate": 0.1
# week 2: if no dashboards or monitors regressed, switch to drop
"action": "drop", "sampleRate": null

# ❌ WRONG — drop on first attempt; can break a dashboard nobody remembered
"action": "drop"
```

### Always include both `env` and `service` (or `__name__`) in matchers

Broad matchers like `{level: debug}` alone can match production metrics that happen to share a label.

```bash
# ✅ CORRECT — scoped to one env
"matchers": [{"name":"level","value":"debug"},{"name":"env","value":"staging"}]

# ❌ WRONG — also drops debug metrics in prod
"matchers": [{"name":"level","value":"debug"}]
```

### Always `get` before `update` to preserve fields

Update is a full-document replace.

```bash
# ✅ CORRECT
oodle drop-rules get dr_123 -o json > rule.json
jq '.sampleRate = 0.05' rule.json > rule.new.json
oodle drop-rules update dr_123 -f rule.new.json

# ❌ WRONG — drops matchers and action
oodle drop-rules update dr_123 -f <(echo '{"sampleRate":0.05}')
```

### Name rules with `<action>-<metric-or-domain>-<scope>`

Predictable names make it easy to find and revert a rule when a dashboard breaks.

```bash
# ✅ CORRECT
"name": "drop-debug-metrics-staging"
"name": "sample-kube-pod-info-prod"

# ❌ WRONG
"name": "rule1"
```

## Failure Handling

| Error | Cause | Fix |
|-------|-------|-----|
| 401 Unauthorized | Invalid or missing API key | Run `oodle configure` or set `OODLE_API_KEY` |
| 404 Not Found | Drop rule ID does not exist | Verify with `oodle drop-rules list -o json` |
| connection refused | Wrong `OODLE_DEPLOYMENT` URL | Check `OODLE_DEPLOYMENT` env var |
| `sampleRate required` | `action: sample` without `sampleRate` | Add `sampleRate` between 0 and 1 (e.g. 0.1) |
| Dashboard panel suddenly empty | Drop rule matched a metric the panel queries | Run `oodle drop-rules list -o json` to find the rule; delete it (`oodle drop-rules delete <id> --force`) or narrow its matchers |
| Monitor went into `no data` | Drop rule matched the monitor's metric | Same fix as above; alternatively switch the rule from `drop` to `sample` |
| Cost did not decrease | Matchers don't actually match the high-volume series | Re-run `oodle metrics list --match ...` and compare label sets to the rule's matchers |
| 429 Too Many Requests | Bulk drop-rule sync | Add `--retries 3`, throttle to <10 creates per second |

## References

- [Oodle CLI repo](https://github.com/oodle-ai/oodle-cli)
- [Oodle docs](https://docs.oodle.ai)
