---
name: eve-deploy-debugging
description: Deploy and debug Eve-compatible apps via the CLI, with a focus on staging environments.
---

# Eve Deploy and Debug

Use these steps to deploy and diagnose app issues quickly.

## Environment Setup

- Get the staging API URL from your admin.
- Create and use a profile:

```bash
eve profile create staging --api-url https://api.eh1.incept5.dev
eve profile use staging
```

## Deploy Flow (Staging)

```bash
# Create env if needed
eve env create staging --project proj_xxx --type persistent

# Deploy (requires --ref with 40-char SHA or a ref resolved against --repo-dir)
eve env deploy staging --ref main --repo-dir .

# When environment has a pipeline configured, the above triggers the pipeline.
# Use --direct to bypass pipeline and deploy directly:
eve env deploy staging --ref main --repo-dir . --direct

# Pass inputs to pipeline:
eve env deploy staging --ref main --repo-dir . --inputs '{"key":"value"}'
```

### Deploy Polling Flow

When `eve env deploy` is called:

1. **Direct deploy** (no pipeline): Returns `deployment_status` directly. Poll health endpoint until `ready === true`.
2. **Pipeline deploy**: Returns `pipeline_run_id`. Poll `GET /pipelines/{name}/runs/{id}` until all steps complete, then check health.

Deploy is complete when: `ready === true` AND `active_pipeline_run === null`.

## Observe the Deploy

```bash
eve job list --phase active
eve job follow <job-id>              # Real-time SSE streaming
eve job watch <job-id>               # Poll-based status updates
eve job diagnose <job-id>            # Full diagnostic
eve job result <job-id>              # Final result
eve job runner-logs <job-id>         # Raw worker logs
```

### Real-Time Debugging (3-Terminal Approach)

```bash
# Terminal 1: Pipeline/job progress
eve job follow <job-id>

# Terminal 2: Environment health
eve env diagnose <project> <env>

# Terminal 3: System-level logs
eve system logs
```

## Debugging Workflows

### Job Won't Start

1. Check dependencies: `eve job dep list <job-id>`
2. Check if blocked: `eve job show <job-id>` → look at `blocked_by`
3. Verify environment readiness: `eve env show <project> <env>`
4. Check orchestrator: `eve system orchestrator status`

### Job Failed

1. Get the error: `eve job diagnose <job-id>`
2. Check logs: `eve job follow <job-id>` or `eve job runner-logs <job-id>`
3. If build failure: `eve build diagnose <build-id>`
4. If secret failure: `eve secrets list --project <project_id>`

### Job Stuck Active

1. Check if waiting for input: `eve job show <job-id>` → `effective_phase`
2. Check thread messages: `eve thread messages <thread-id>`
3. Check runner pod: `eve system pods`

### System Issues

1. API health: `eve system health`
2. Orchestrator: `eve system orchestrator status`
3. Recent events: `eve system events`

## Common Error Messages

| Error | Cause | Fix |
|-------|-------|-----|
| `401 Unauthorized` | Token expired | `eve auth login` |
| `git clone failed` | Missing credentials | Set `github_token` or `ssh_key` secret |
| `service not provisioned` | Environment not created | `eve env create <env>` |
| `image pull backoff` | Registry auth failed | If using BYO/custom registry, verify `REGISTRY_USERNAME` + `REGISTRY_PASSWORD`; for managed apps use `registry: "eve"` |
| `healthcheck timeout` | App not starting | Check app logs, verify ports in manifest |

## Build Failures

If a deploy pipeline fails at the build step:

```bash
eve build list --project <project_id>
eve build diagnose <build_id>
eve build logs <build_id>
eve secrets list --project <project_id>     # Required for BYO/custom registry: REGISTRY_USERNAME, REGISTRY_PASSWORD
```

Common build failures:
- **Registry auth**: For BYO/custom registry, verify `REGISTRY_USERNAME` and `REGISTRY_PASSWORD` secrets
- **Dockerfile not found**: Check `build.context` path in manifest
- **Multi-stage build failure**: BuildKit handles these correctly; Kaniko may have issues
- **Workspace errors**: Build context not available — check `eve build diagnose`

## Worker Image Registry

Eve publishes worker images to the configured private registry with these variants:

| Variant | Contents |
|---------|----------|
| `base` | Node.js, git, standard CLI tools |
| `python` | Base + Python runtime |
| `rust` | Base + Rust toolchain |
| `java` | Base + JDK |
| `kotlin` | Base + Kotlin compiler |
| `full` | All runtimes combined |

**Version pinning**: Use semver tags (e.g., `v1.2.3`) in production. Use SHA tags or `:latest` in development.

## Platform Environment Variables

Eve injects these into every deployed service container:

- `EVE_API_URL` — internal cluster URL for server-to-server calls
- `EVE_PUBLIC_API_URL` — public ingress URL for browser-facing apps
- `EVE_PROJECT_ID`, `EVE_ORG_ID`, `EVE_ENV_NAME`

Use `EVE_API_URL` for backend calls. Use `EVE_PUBLIC_API_URL` for browser clients.

## Access URLs

- URL pattern: `{service}.{orgSlug}-{projectSlug}-{env}.{domain}`
- Local dev default domain: `lvh.me`
- Ask the admin for the correct domain (staging vs production).

## Environment-Specific Debugging

| Environment | How to Debug |
|-------------|--------------|
| **Local (k3d)** | Direct service access via ingress, `eve system logs` |
| **Docker Compose** | `docker compose logs <service>`, dev-only (no production use) |
| **Kubernetes** | Ingress-based access, `kubectl -n eve logs` as last resort |

## Workspace Janitor

Production disk management for agent workspaces:

- `EVE_WORKSPACE_MAX_GB` — total workspace budget
- `EVE_WORKSPACE_MIN_FREE_GB` — trigger cleanup threshold
- `EVE_SESSION_TTL_HOURS` — auto-evict stale sessions
- LRU eviction when approaching budget; TTL cleanup for idle sessions
- K8s: per-attempt PVCs deleted on completion

## Related Skills

- Local dev loop: `eve-local-dev-loop`
- Secrets: `eve-auth-and-secrets`
- Manifest changes: `eve-manifest-authoring`
