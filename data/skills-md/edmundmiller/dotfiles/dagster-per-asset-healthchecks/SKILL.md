---
name: dagster-per-asset-healthchecks
description: Split a monolithic Dagster job into per-asset schedules with individual healthchecks.io pings. Use when adding monitoring to Dagster assets, splitting a catch-all job, or wiring per-job healthchecks into the Nix bugster module.
---

# Dagster Per-Asset Healthchecks

Pattern for giving each Dagster asset its own schedule + healthchecks.io check.

## Why

One `sync_all_hourly` means a failure anywhere kills all monitoring signal.
Per-asset: each job has its own check, own schedule, own ping URL.

## The Pattern

### 1. Create healthchecks.io checks via API

```bash
curl -s -X POST "https://healthchecks.io/api/v3/checks/" \
  -H "X-Api-Key: <key>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "bugster: <asset_name>",
    "tags": "bugster nuc",
    "grace": 3600,
    "schedule": "0 * * * *",
    "tz": "America/Chicago"
  }' | jq '{name, ping_url, uuid}'
```

Delete an old combined check:

```bash
curl -s -X DELETE "https://healthchecks.io/api/v3/checks/<uuid>" \
  -H "X-Api-Key: <key>"
```

API key in 1Password: `hcw_Xxfgcx40LFjb2JJlDJvDainCDIXg`

### 2. definitions.py — per-asset schedules

Build one `ScheduleDefinition` per loaded asset:

```python
_schedules: list[dg.ScheduleDefinition] = []
_SCHEDULE_PING_URLS: dict[str, str] = {}

for _asset in _assets:
    _asset_key = _asset.key.path[-1]          # e.g. "github_personal_tasknotes"
    _schedule_name = f"sync_{_asset_key}_hourly"
    _schedules.append(
        dg.ScheduleDefinition(
            name=_schedule_name,
            cron_schedule="0 * * * *",
            target=dg.AssetSelection.assets(_asset_key),
            default_status=dg.DefaultScheduleStatus.RUNNING,  # ← critical
        )
    )
    # Wire healthcheck URL if env var is set
    _url = os.environ.get(f"HEALTHCHECK_PING_URL_{_asset_key.upper()}")
    if _url:
        _SCHEDULE_PING_URLS[_schedule_name] = _url
```

**Gotcha:** Schedules default to `STOPPED`. Always set `default_status=DefaultScheduleStatus.RUNNING` or they never fire on fresh deployments.

### 3. Generic sensors — one set, all schedules

```python
def _get_ping_url(context: dg.RunStatusSensorContext) -> str | None:
    schedule_name = (context.dagster_run.tags or {}).get("dagster/schedule_name")
    return _SCHEDULE_PING_URLS.get(schedule_name) if schedule_name else None

@dg.run_status_sensor(run_status=dg.DagsterRunStatus.STARTED, name="healthcheck_run_started")
def healthcheck_run_started(context):
    if url := _get_ping_url(context):
        requests.post(f"{url}/start?rid={context.dagster_run.run_id}", timeout=10)

@dg.run_status_sensor(run_status=dg.DagsterRunStatus.SUCCESS, name="healthcheck_run_success")
def healthcheck_run_success(context):
    if url := _get_ping_url(context):
        requests.post(f"{url}?rid={context.dagster_run.run_id}", timeout=10)

@dg.run_status_sensor(run_status=dg.DagsterRunStatus.FAILURE, name="healthcheck_run_failure")
def healthcheck_run_failure(context):
    if url := _get_ping_url(context):
        requests.post(f"{url}/fail?rid={context.dagster_run.run_id}", timeout=10)

_sensors = [healthcheck_run_started, healthcheck_run_success, healthcheck_run_failure] \
    if _SCHEDULE_PING_URLS else []
```

### 4. Nix module — per-asset ping URLs

In `modules/services/bugster/default.nix`:

```nix
healthcheckPingUrls = mkOpt (types.attrsOf types.str) { };
```

Generates env vars:

```nix
// lib.mapAttrs' (
  name: url: lib.nameValuePair "HEALTHCHECK_PING_URL_${lib.strings.toUpper name}" url
) cfg.healthcheckPingUrls
```

Note: use `lib.strings.toUpper` — `builtins.toUpper` doesn't exist in NixOS Nix.

In `hosts/nuc/default.nix`:

```nix
bugster.healthcheckPingUrls = {
  github_personal_tasknotes = "https://hc-ping.com/...";
  linear_personal_tasknotes = "https://hc-ping.com/...";
  travel_time_blocks        = "https://hc-ping.com/...";
};
```

## Verify via GraphQL

```bash
# Check schedule/sensor status
ssh nuc "curl -s http://127.0.0.1:3001/graphql -X POST -H 'Content-Type: application/json' \
  -d '{\"query\": \"{ workspaceOrError { ... on Workspace { locationEntries { locationOrLoadError { ... on RepositoryLocation { repositories { schedules { name scheduleState { status } } sensors { name sensorState { status } } } } } } } } }\"}'" \
  | python3 -m json.tool"

# Start a stopped schedule
SCHEDULE=sync_github_personal_tasknotes_hourly
ssh nuc "curl -s http://127.0.0.1:3001/graphql -X POST -H 'Content-Type: application/json' \
  -d '{\"query\": \"mutation { startSchedule(scheduleSelector: { repositoryLocationName: \\\"grpc:localhost:4000\\\", repositoryName: \\\"__repository__\\\", scheduleName: \\\"$SCHEDULE\\\" }) { ... on ScheduleStateResult { scheduleState { status } } } }\"}'"
```

## Deploying bugster repo changes

The `bugster-setup` service runs `git reset --hard origin/main`, so local edits get wiped.
Always push changes to GitHub via root + emiller's SSH key:

```bash
cat > /tmp/push.sh << 'SCRIPT'
#!/bin/bash
set -euo pipefail
cd /var/lib/dagster/bugster
git add -A && git commit -m "your message"
GIT_SSH_COMMAND="ssh -i /home/emiller/.ssh/id_ed25519 -o StrictHostKeyChecking=accept-new" \
  git push origin main
SCRIPT
scp /tmp/push.sh nuc:/tmp/push.sh && ssh nuc "sudo bash /tmp/push.sh"
```
