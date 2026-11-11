---
name: tiltup
description: Use when starting tilt, debugging Tiltfile errors, or bootstrapping a dev environment. Starts Tilt in zmx, monitors bootstrap to healthy state, fixes Tiltfile bugs without hard-coding or fallbacks.
---

# Tilt Up

## Principles (Always Active)

These apply whenever working with Tiltfiles, Tilt errors, or dev environment bootstrap:

### Fix the Tiltfile, Not the Symptoms

- **Fix the source config directly** - Tiltfile, Dockerfile, k8s manifest, or helm values
- **Never add shell workarounds** - no wrapper scripts, no `|| true`, no `try/except pass`
- **Never hard-code** ports, paths, hostnames, image tags, or container names that should be dynamic
- **Never add fallbacks** that mask the real error - if a resource fails, the failure must be visible
- **Never add sleep/retry loops** for flaky dependencies - fix dependency ordering via `resource_deps()` or `k8s_resource(deps=)`
- **Never add polling** for readiness that Tilt already handles - use `k8s_resource(readiness_probe=)` or probe configs

### Express Dependencies Declaratively

- Port conflicts: fix the port allocation source, don't pick a different port
- Resource ordering: use `resource_deps()`, not sequential startup scripts
- Env vars: use `silo.toml` or gen-env output, not inline defaults
- Image availability: use `image_deps` or `deps`, not sleep-until-ready

### Tilt Live-Reloads

After editing a Tiltfile, Tilt picks up changes automatically. **Never restart `tilt up`** for:
- Tiltfile edits
- Source code changes
- Kubernetes manifest updates

Restart only for: Tilt version upgrades, port/host config changes, crashes, cluster context switches.

## Workflow (When Explicitly Starting Tilt)

### Step 1: Assess Current State

1. Check if tilt is already running:
   ```bash
   PROJECT=$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" || basename "$PWD")
   zmx list --short 2>/dev/null | grep -q "^${PROJECT}-tilt$"
   ```
   If running, check health via `tilt get uiresources -o json` and skip to Step 3.

2. Check for required env files (`.localnet.env`, `.env.local`, `silo.toml`):
   - If `silo.toml` exists, use `silo up` path
   - If gen-env script exists, run it first
   - If neither, check project README for bootstrap instructions

3. Check for k3d cluster or Docker prerequisites.

### Step 2: Start Tilt in zmx

Follow the `zmx` skill patterns:
```bash
PROJECT=$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" || basename "$PWD")
SESSION="${PROJECT}-tilt"

if zmx list --short 2>/dev/null | grep -q "^${SESSION}$"; then
  echo "Tilt session already exists: $SESSION"
else
  zmx run "$SESSION" 'tilt up'
  echo "Started tilt in zmx session: $SESSION"
fi
```

For silo projects: `silo up` instead of `tilt up`.

### Step 3: Monitor Bootstrap

Poll for convergence:
1. Wait 10s for initial resource registration
2. Poll every 15s, up to 20 iterations. Include docker-compose container health
   (`composeResourceInfo.healthStatus`) — an `Up (unhealthy)` compose container
   keeps `runtimeStatus=ok` and is otherwise invisible, so bootstrap can look
   "done" while canton/splice/postgres are silently failing their HEALTHCHECK:
   ```bash
   tilt get uiresources -o json | jq -r '.items[] | select(.status.runtimeStatus == "error" or .status.updateStatus == "error" or .status.updateStatus == "pending" or .status.composeResourceInfo.healthStatus == "unhealthy") | "\(.metadata.name): runtime=\(.status.runtimeStatus) update=\(.status.updateStatus) compose=\(.status.composeResourceInfo.healthStatus // "-")"'
   ```
3. Track resources: `pending` -> `in_progress` -> `ok`
4. Success: all resources reach `runtime=ok, update=ok` (or `not_applicable`)
   AND no docker-compose resource is `composeResourceInfo.healthStatus == "unhealthy"`
5. If resources stabilize in `error`, OR a compose resource stays `unhealthy`,
   proceed to Step 4. For an unhealthy compose probe, read the real cause with
   `docker inspect <compose-project>-<svc> --format '{{json .State.Health}}'` —
   often the mounted healthcheck script calls a CLI the image lacks (the service
   is up; fix the probe script, don't disable the check)

### Step 4: Diagnose and Fix Errors

For each resource in error state:
1. Read logs: `tilt logs <resource> --since 2m`
2. Read the Tiltfile and relevant k8s manifests
3. Identify root cause in the config (not the running process)
4. Apply fix following the Principles above
5. Tilt live-reloads - re-poll status to verify

After 3 fix iterations on the same resource without progress:
- Report the error with full logs
- Identify whether it's a Tiltfile bug, upstream dependency, or infrastructure problem
- Do not silently skip or disable the resource

### Step 5: Report

```
## Tilt Status: <healthy|degraded|errored>

**Resources**: X/Y ok
**Session**: zmx $SESSION

### Errors (if any)
- <resource>: <root cause> — <what was fixed or what remains>
```
