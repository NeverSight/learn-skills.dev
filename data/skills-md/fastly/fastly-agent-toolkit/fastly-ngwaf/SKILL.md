---
name: fastly-ngwaf
description: "Performs an internal audit of Fastly Next-Gen WAF (NGWAF) workspaces to audit that critical templated protection rules are configured and enabled. Use when auditing NGWAF workspace security posture, checking for missing or disabled login protection rules (LOGINDISCOVERY, LOGINATTEMPT, LOGINSUCCESS, LOGINFAILURE), auditing credit card validation rules (CC-VAL-ATTEMPT, CC-VAL-FAILURE, CC-VAL-SUCCESS), auditing gift card protection rules (GC-VAL-ATTEMPT, GC-VAL-FAILURE, GC-VAL-SUCCESS), identifying potential login endpoints not covered by NGWAF rules, or comparing attack traffic against blocked traffic to confirm enabled rules are actually blocking."
---

# Fastly NGWAF Workspace Audit

Audits NGWAF workspaces to verify critical templated rules are configured and enabled. Use the **fastly-cli** skill to configure rules; this skill identifies gaps.

## Quick Start

Run the bundled assessment script (requires `jq` and `FASTLY_API_KEY`):

```bash
./scripts/assess_ngwaf_rules.sh
```

For manual inspection or partial audits, work through the steps below with the `fastly` CLI.

The CLI ignores `FASTLY_API_KEY`. Its precedence is `--token` > `FASTLY_API_TOKEN` > `fastly.toml` profile > default
stored token. To reuse the script's credential:

```bash
export FASTLY_API_TOKEN="$FASTLY_API_KEY"
```

## Audit Workflow

1. **List workspaces** — verify the account has NGWAF workspaces
2. **Fetch rules per workspace** — retrieve each workspace's rule set
3. **Validate critical signals** — confirm required rules exist and are enabled
4. **Flag gaps and search for uncovered endpoints** — report missing/disabled rules
5. **Check attack traffic against blocked traffic** — confirm enabled rules are actually blocking

### Step 1: List Workspaces

```bash
fastly ngwaf workspace list --json | jq -r '.data[].id'
```

If empty, NGWAF is not configured for this account.

### Step 2: Fetch Rules for a Workspace

```bash
fastly ngwaf workspace rule list --workspace-id "$WORKSPACE_ID" --json
```

Both list commands return `{"data": [...], "meta": {...}}` and cap at 100 items with no flag to raise it. Check
`.meta.total`; above 100, fall back to `GET /ngwaf/v1/workspaces?limit=200` or `.../rules?limit=200`.

`rule list` also takes `--enabled` and `--action` to filter server-side.

### Step 3: Validate Critical Signals

For each workspace, verify these templated rules exist and `enabled` is `true`:

| Category               | Required Signals                                                 |
| ---------------------- | ---------------------------------------------------------------- |
| Login Protection       | `LOGINDISCOVERY`, `LOGINATTEMPT`, `LOGINSUCCESS`, `LOGINFAILURE` |
| Credit Card Validation | `CC-VAL-ATTEMPT`, `CC-VAL-FAILURE`, `CC-VAL-SUCCESS`             |
| Gift Card Validation   | `GC-VAL-ATTEMPT`, `GC-VAL-FAILURE`, `GC-VAL-SUCCESS`             |

Check a specific signal:

```bash
fastly ngwaf workspace rule list --workspace-id "$WORKSPACE_ID" --json \
  | jq '[.data[] | select(.actions[].signal == "LOGINDISCOVERY") | {enabled, id}]'
```

### Step 4: Search for Uncovered Login Endpoints

When `LOGINATTEMPT` is missing or disabled, search recent request logs for login-like traffic the WAF isn't protecting.
No CLI equivalent exists (there is no `fastly ngwaf workspace requests`), so use the API:

```bash
curl -s -H "Fastly-Key: $FASTLY_API_KEY" \
  "https://api.fastly.com/ngwaf/v1/workspaces/$WORKSPACE_ID/requests?limit=100&page=1&q=from%3A-30min%20method%3APOST%20path%3A~%22%2Alogin%2A%22" \
  | jq -r '.data[].path' | sort | uniq -c
```

### Step 5: Check Attack Traffic Against Blocked Traffic

A rule can be present and enabled and still block nothing when the workspace mode overrides it. `requests_attack` is
what NGWAF flagged; `requests_total_blocked` is what it stopped. Attacks above zero with nothing blocked means the
workspace is in `log` or `off` mode. Report it even when every rule checks out.

```bash
fastly ngwaf workspace time-series get --workspace-id "$WORKSPACE_ID" \
  --from=2026-08-01T00:00:00Z --to=2026-08-08T00:00:00Z \
  --metrics=requests_total,requests_attack,requests_total_blocked \
  --granularity=86400 --json \
  | jq -r '.data[] | "\(.timestamp)  total=\(.requests_total)  attack=\(.requests_attack)  blocked=\(.requests_total_blocked)"'
```

Across every workspace at once, grouped by workspace:

```bash
fastly ngwaf time-series list \
  --from=2026-08-01T00:00:00Z --to=2026-08-08T00:00:00Z \
  --metrics=requests_total,requests_attack \
  --granularity=86400 --dimensions=workspaces --json \
  | jq -r '.data[] | "\(.dimensions.workspace)  \(.dimensions.time)  \(.values | add)"'
```

The workspace-level subcommand is `get`, the account-level one is `list`. They differ in three ways that break audit
scripts:

- Output shape. `get` returns flat objects keyed by metric with a `timestamp`. `list` nests them under `dimensions`
  and a `values` array, hence `.values | add`.
- Bucket size. The CLI only sends `--granularity` when passed; `get` then buckets hourly and `list` daily. Always
  pass it.
- Zeroes. `get` reports a quiet metric as `0`. `list` drops it from `values`, and returns
  `{"data":[],"meta":{"total":0}}` when nothing recorded. A missing key means zero, not an error.

Read `requests_total_blocked` through `get`. A workspace that blocked nothing is the case this audit is looking for,
and `list` reports it as an absence.

`--from` and `--metrics` are required on both. Timestamps are RFC 3339, not the `YYYY-MM-DD` that `fastly stats` takes.

`--metrics` also accepts `XSS`, `SQLI`, `HTTP404` and any custom signal name on the workspace, so a rule verified in
step 3 can be checked for real traffic by signal name. Query those through `get`.

## Expected Output

**Healthy workspace** — all signals present and enabled:

```text
### Workspace: abc123
  [LOGIN Rules]
  - LOGINDISCOVERY: ENABLED
  - LOGINATTEMPT: ENABLED
  - LOGINSUCCESS: ENABLED
  - LOGINFAILURE: ENABLED
  [CC Rules]
  - CC-VAL-ATTEMPT: ENABLED
  - CC-VAL-FAILURE: ENABLED
  - CC-VAL-SUCCESS: ENABLED
  [GC Rules]
  - GC-VAL-ATTEMPT: ENABLED
  - GC-VAL-FAILURE: ENABLED
  - GC-VAL-SUCCESS: ENABLED
```

**Unhealthy workspace** — missing or disabled rules require remediation:

```text
### Workspace: def456
  [LOGIN Rules]
  - LOGINDISCOVERY: NOT CONFIGURED (Recommended: CRITICAL: Configure and enable this rule to discover unknown login endpoints)
  - LOGINATTEMPT: IS DISABLED (Recommended: Enable this rule)
  - LOGINSUCCESS: ENABLED
  - LOGINFAILURE: ENABLED
  -> LOGINATTEMPT is not enabled. Searching recent request logs for potential login paths...
  -> Found potential login paths in last 30 minutes:
       3 /api/v1/login
       1 /auth/signin
```

## Error Handling

| Error                             | Cause                        | Fix                                            |
| --------------------------------- | ---------------------------- | ---------------------------------------------- |
| `FASTLY_API_KEY not set`          | Environment variable missing | `export FASTLY_API_KEY=<token>`                |
| `API call failed with status 403` | Token lacks NGWAF scope      | Verify token has `global:read` permission      |
| `No workspaces found`             | NGWAF not provisioned        | Enable NGWAF on the account first              |
| `jq is not installed`             | Missing dependency           | `brew install jq` or `apt-get install -y jq`   |

## API References

- [List Workspaces](https://www.fastly.com/documentation/reference/api/ngwaf/workspaces/#ngwafListWorkspaces)
- [List Workspace Rules](https://www.fastly.com/documentation/reference/api/ngwaf/rules/#ngwafListWorkspaceRules)
- [Time Series Metrics](https://www.fastly.com/documentation/reference/api/ngwaf/timeseries/)
