---
name: tilt
description: This skill should be used when the user asks to "write a Tiltfile", "configure Tilt", "set up live update", "debug Tilt", "add a resource to Tilt", "optimize Tilt builds", "view Tilt logs", "restart a Tilt resource", or mentions Tiltfile, tilt up, tilt ci, tilt down, live_update, docker_build, custom_build, k8s_resource, local_resource, or Kubernetes local development with Tilt.
---

# Tilt — Kubernetes Dev Toolkit

Tilt automates the local Kubernetes development loop: watch files, build images, deploy to cluster. Configuration lives in a `Tiltfile` (Starlark, a Python dialect). A **resource** bundles an image build + k8s deploy (or a local command) into a single manageable unit.

## CLI Operations

The commands an agent uses to interact with a running Tilt instance.

### Lifecycle

| Task | Command |
|------|---------|
| Start dev environment | `tilt up [-- <Tiltfile args>]` |
| Start with terminal log streaming | `tilt up --stream` |
| Start specific resources only | `tilt up frontend backend` |
| Run in CI/batch mode (exits on success/failure) | `tilt ci --timeout 30m` |
| Stop and delete deployed resources | `tilt down` |
| Change runtime Tiltfile args | `tilt args -- --flag value` |
| Change runtime args (clear all) | `tilt args --clear` |

On Ctrl+C from `tilt up`: K8s and Docker Compose resources **keep running**. Local `serve_cmd` processes stop. Use `tilt down` to clean up.

### Viewing Logs

| Task | Command |
|------|---------|
| Stream all logs | `tilt logs -f` |
| Stream logs for one resource | `tilt logs -f <resource>` |
| Show only errors | `tilt logs --level error` |
| Show build logs only | `tilt logs --source build` |
| Show runtime logs only | `tilt logs --source runtime` |
| Logs since 5 minutes ago | `tilt logs --since 5m` |
| Last 100 lines | `tilt logs --tail 100` |
| JSON output (for parsing) | `tilt logs --json` |

### Resource Management

| Task | Command |
|------|---------|
| List all resources | `tilt get uiresources` |
| Resource status as JSON | `tilt get uiresources -o json` |
| Describe a resource in detail | `tilt describe uiresource <name>` |
| Force rebuild a resource | `tilt trigger <resource>` |
| Enable a disabled resource | `tilt enable <resource>` |
| Disable a resource | `tilt disable <resource>` |
| Wait for resource readiness | `tilt wait --for=condition=Ready uiresource/<name>` |

### Inspection & Debugging

| Task | Command |
|------|---------|
| Diagnostics (versions, cluster) | `tilt doctor` |
| Inspect file watches | `tilt get filewatches` |
| Describe a specific file watch | `tilt describe filewatch <name>` |
| Full engine state dump (JSON) | `tilt dump engine` |
| Full UI state dump | `tilt dump webview` |
| Test Docker build as Tilt would | `tilt docker -- build <args>` |
| List API resource types | `tilt api-resources` |

The Tilt API server runs on `localhost:10350` by default. All `tilt get/describe/trigger` commands talk to it.

## Build Strategy Selector

| Situation | Function | Key detail |
|-----------|----------|------------|
| Standard Dockerfile | `docker_build(ref, context)` | Watches context dir, auto-injects into k8s |
| Custom toolchain (Bazel, ko, Buildpacks) | `custom_build(ref, cmd, deps)` | Must tag with `$EXPECTED_REF` env var |
| Non-Docker builder (Buildah, kaniko) | `custom_build(..., skips_local_docker=True)` | Builder handles push independently |
| Docker Compose services | `docker_compose(configPaths)` | Manages compose lifecycle |
| Helm charts | `k8s_yaml(helm('./chart'))` | Renders locally, deploys to cluster |
| Kustomize overlays | `k8s_yaml(kustomize('./overlay'))` | Renders locally, deploys to cluster |

## Live Update Decision Tree

Live update replaces full image rebuilds with in-place container file syncs — seconds instead of minutes.

| Step | Purpose | Ordering |
|------|---------|----------|
| `fall_back_on(files)` | Force full rebuild when these files change | Must come first |
| `sync(local, remote)` | Copy changed files into running container | After fall_back_on |
| `run(cmd, trigger=files)` | Execute command in container (e.g., install deps) | After sync |
| `restart_container()` | Restart the container process | Must come last |

```python
docker_build('myapp', '.', live_update=[
    fall_back_on(['requirements.txt']),
    sync('./src', '/app/src'),
    run('pip install -r requirements.txt', trigger=['requirements.txt']),
])
```

**When live update breaks:** Changes to files outside the `docker_build` context trigger a full rebuild. Changes outside any `sync()` path also trigger a full rebuild. First `tilt up` always does a full build — live update requires a running container.

## Resource Configuration

```python
# Kubernetes resource with port forwarding and dependencies
k8s_resource('frontend',
    port_forwards=['3000:3000'],
    resource_deps=['api', 'database'],
    labels=['web'],
    trigger_mode=TRIGGER_MODE_MANUAL,
)

# Local resource (build tool, test runner, code generator)
local_resource('codegen',
    cmd='make generate',
    deps=['./proto'],
    labels=['tools'],
)

# Local server (runs continuously)
local_resource('storybook',
    serve_cmd='npm run storybook',
    deps=['./src/components'],
    allow_parallel=True,
    readiness_probe=probe(http_get=http_get_action(port=6006)),
)
```

**Parallelism:** Local resources run serially by default. Set `allow_parallel=True` for independent resources. Image builds default to 3 concurrent — adjust with `update_settings(max_parallel_updates=N)`.

**Dependencies:** `resource_deps` gates on first-ever readiness only — once a dependency is ready once, dependents unlock permanently for that session.

## Debugging Flow

```
Service crashing?     → tilt logs -f <resource> --source runtime
Build failing?        → tilt logs -f <resource> --source build
                        tilt docker -- build <args>  (reproduces Tilt's exact build)
Wrong files rebuild?  → tilt get filewatches
                        tilt describe filewatch <name>
                        Check .tiltignore, watch_settings(ignore=), ignore= param
Force a rebuild?      → tilt trigger <resource>
Resource stuck?       → tilt describe uiresource <name>
                        Check resource_deps chain
                        For CRDs: pod_readiness='ignore'
General diagnostics?  → tilt doctor
Full state dump?      → tilt dump engine | jq .
```

## Top 10 Pitfalls

| Pitfall | Fix |
|---------|-----|
| `local()` calls don't track file deps | Wrap with `read_file()` or add `watch_file()` |
| Live update paths outside docker_build context | Ensure sync local paths fall within context dir |
| Local resources block each other | Set `allow_parallel=True` on independent resources |
| `resource_deps` doesn't re-gate on updates | It only checks first-ever readiness, not current version |
| Starlark has no while/try-except/class/recursion | Use for loops, `fail()` for errors, dicts for state |
| `.tiltignore` doesn't affect Docker build context | Use `.dockerignore` to exclude from both rebuild triggers AND context |
| `$EXPECTED_REF` not used in custom_build | Build script MUST tag the image with this env var |
| `run()` trigger files not in a `sync()` step | Trigger paths must also be covered by a sync step |
| First `tilt up` always does full build | Live update cannot work until a container is running |
| CRD pods stuck in pending | Set `pod_readiness='ignore'` on CRD resources |

## Additional Resources

### Reference Files

For detailed API signatures and advanced patterns, consult:
- **`references/api-reference.md`** — Complete Tiltfile API catalog organized by category, Starlark language notes, ignore mechanism comparison
- **`references/patterns.md`** — Multi-service architectures, environment config, CI integration, performance optimization, programmatic Tilt interaction, extension ecosystem
