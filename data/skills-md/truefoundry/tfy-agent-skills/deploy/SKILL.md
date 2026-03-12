---
name: deploy
description: Deploys applications to TrueFoundry. Handles single HTTP services, async/queue workers, multi-service projects, and declarative manifest apply. Supports `tfy apply`, `tfy deploy`, docker-compose translation, and CI/CD pipelines. Use when deploying apps, applying manifests, shipping services, or orchestrating multi-service deployments.
license: MIT
compatibility: Requires Bash, curl, and access to a TrueFoundry instance
metadata:
  disable-model-invocation: "true"
allowed-tools: Bash(tfy*) Bash(*/tfy-api.sh *) Bash(*/tfy-version.sh *) Bash(docker *) Bash(tfy deploy*)
---

> Routing note: For ambiguous user intents, use the shared clarification templates in [references/intent-clarification.md](references/intent-clarification.md).

# Deploy to TrueFoundry

Route user intent to the right deployment workflow. Load only the references you need.

## Intent Router

> **Gateway configs are NOT services.** If the user says "apply" or "deploy" in the context of a gateway YAML (`type: gateway-*`, `type: provider-account/*`), run `tfy apply -f <file>` and test the endpoint. Do not build Docker images, create secrets, or spin up new services.

| User Intent | Action | Reference |
|---|---|---|
| "apply gateway config", "apply gateway yaml", "tfy apply gateway", "deploy gateway" | Gateway manifest apply — use `tfy apply -f <file>` directly; do NOT build a service image | Inline: `tfy apply -f gateway.yaml` |
| "deploy", "deploy my app", "ship this" | Single HTTP service | [deploy-service.md](references/deploy-service.md) |
| "attach this deployment to mcp gateway", "register deployed mcp service", "connect deployment to mcp gateway" | Post-deploy MCP registration | Use `mcp-servers` skill after deployment endpoint is known |
| "mount this file", "mount config file", "mount certificate file", "mount key file" | Single service with file mounts (no image rebuild) | [deploy-service.md](references/deploy-service.md) |
| "tfy apply", "apply manifest", "deploy from yaml" | Declarative manifest apply | [deploy-apply.md](references/deploy-apply.md) |
| "deploy everything", "full stack", docker-compose, "docker-compose.yaml", "compose.yaml" | Multi-service: use compose as source of truth | [deploy-multi.md](references/deploy-multi.md) + [compose-translation.md](references/compose-translation.md) |
| "async service", "queue consumer", "worker" | Async/queue service | [deploy-async.md](references/deploy-async.md) |
| "deploy LLM", "serve model" | Model serving intent (may be ambiguous) | Ask user: dedicated model serving (`llm-deploy`) or generic service deploy (`deploy`) |
| "deploy helm chart" | Helm chart intent | Confirm Helm path and collect chart details, then proceed with `helm` workflow |
| "deploy postgres docker", "dockerized postgres", "deploy redis docker", "database in docker/container" | Containerized database intent | Proceed with `deploy` workflow (do not route to Helm) |
| "deploy database", "deploy postgres", "deploy redis" | Ambiguous infra intent | Ask user: Helm chart (`helm`) or containerized service (`deploy`) |

**Load only the reference file matching the user's intent.** Do not preload all references.

## Prerequisites (All Workflows)

```bash
# 1. Check credentials
grep '^TFY_' .env 2>/dev/null || true
env | grep '^TFY_' 2>/dev/null || true

# 2. Derive TFY_HOST for CLI (MUST run before any tfy command)
export TFY_HOST="${TFY_HOST:-${TFY_BASE_URL%/}}"

# 3. Check CLI
tfy --version 2>/dev/null || echo "Install: pip install 'truefoundry==0.5.0'"

# 4. Check for existing manifests
ls tfy-manifest.yaml truefoundry.yaml 2>/dev/null
```

- `TFY_BASE_URL` and `TFY_API_KEY` must be set (env or `.env`).
- **`TFY_HOST` must be set before any `tfy` CLI command.** The export above handles this automatically.
- `TFY_WORKSPACE_FQN` required. **HARD RULE: Never auto-pick a workspace. Always ask the user to confirm, even if only one workspace exists or a preference is saved.** See `references/prerequisites.md` for the full workspace confirmation flow.
- For full credential setup, see `references/prerequisites.md`.

> **WARNING:** Never use `source .env`. The `tfy-api.sh` script handles `.env` parsing automatically. For shell access: `grep KEY .env | cut -d= -f2-`

## Quick Ops (Inline)

### Apply a manifest (most common)

```bash
# tfy CLI expects TFY_HOST when TFY_API_KEY is set
export TFY_HOST="${TFY_HOST:-${TFY_BASE_URL%/}}"

# Preview changes
tfy apply -f tfy-manifest.yaml --dry-run --show-diff

# Apply
tfy apply -f tfy-manifest.yaml
```

### Deploy from source (local code or git)

```bash
# tfy CLI expects TFY_HOST when TFY_API_KEY is set
export TFY_HOST="${TFY_HOST:-${TFY_BASE_URL%/}}"

# tfy deploy builds remotely — use for local code or git sources
tfy deploy -f truefoundry.yaml --no-wait
```

> **`tfy apply` does NOT support `build_source`.** Use `tfy deploy -f` for source-based deployments.

### Minimal service manifest template

```yaml
name: my-service
type: service
image:
  type: image
  image_uri: docker.io/myorg/my-api:v1.0
ports:
  - port: 8000
    expose: true
    app_protocol: http
resources:
  cpu_request: 0.5
  cpu_limit: 1
  memory_request: 512
  memory_limit: 1024
  ephemeral_storage_request: 1000
  ephemeral_storage_limit: 2000
env:
  LOG_LEVEL: info
replicas: 1
workspace_fqn: "WORKSPACE_FQN_HERE"
```

### Check deployment status

```bash
TFY_API_SH=~/.claude/skills/truefoundry-deploy/scripts/tfy-api.sh
bash $TFY_API_SH GET '/api/svc/v1/apps?workspaceFqn=WORKSPACE_FQN&applicationName=SERVICE_NAME'
```

Or use the `applications` skill.

## Post-Deploy Verification (Automatic)

After any successful deploy/apply action, verify deployment status automatically without asking an extra prompt.

Preferred verification path:
1. Use MCP tool call first:
```
tfy_applications_list(filters={"workspace_fqn": "WORKSPACE_FQN", "application_name": "SERVICE_NAME"})
```
2. If MCP tool calls are unavailable, fall back to:
```bash
TFY_API_SH=~/.claude/skills/truefoundry-deploy/scripts/tfy-api.sh
bash $TFY_API_SH GET '/api/svc/v1/apps?workspaceFqn=WORKSPACE_FQN&applicationName=SERVICE_NAME'
```

Always report the observed status (`BUILDING`, `DEPLOYING`, `DEPLOY_SUCCESS`, `DEPLOY_FAILED`, etc.) in the same response.

If status is `DEPLOY_FAILED` or `BUILD_FAILED`, follow [deploy-debugging.md](references/deploy-debugging.md): fetch logs (use `logs` skill), identify cause, apply one fix and retry once; if still failed, report to user with summary and log excerpt and stop.

## Optional Post-Deploy: Attach to MCP Gateway

If the deployed service exposes an MCP endpoint, ask if the user wants to register it in MCP gateway right away.

Handoff checklist to `mcp-servers` skill:
- deployment/service name
- endpoint URL (`https://.../mcp` or in-cluster URL)
- transport (`streamable-http` or `sse`)
- auth mode (`header`, `oauth2`, or `passthrough`)

### REST API fallback (when CLI unavailable)

See `references/cli-fallback.md` for converting YAML to JSON and deploying via `tfy-api.sh`.

## Auto-Detection: Single vs Multi-Service

**Before creating any manifest, scan the project:**

1. **Check for `docker-compose.yml`, `docker-compose.yaml`, or `compose.yaml` first.** If present (or user mentions docker-compose), treat it as the **primary source of truth**: load [deploy-multi.md](references/deploy-multi.md) and [compose-translation.md](references/compose-translation.md), generate manifests from the compose file, wire services per [service-wiring.md](references/service-wiring.md), then complete deployment. Do not ask the user to manually create manifests when a compose file exists.
2. Look for multiple `Dockerfile` files across the project
3. Check for service directories with their own dependency files in `services/`, `apps/`, `frontend/`, `backend/`

- **Compose file present or user says "docker-compose"** → Multi-service from compose: load `deploy-multi.md` + `compose-translation.md`
- **Single service** → Load `references/deploy-service.md`
- **Multiple services (no compose)** → Load `references/deploy-multi.md`

## Secrets Handling (Default: Secret Groups)

**By default, do not put secrets in env as raw values.** For any env var that looks sensitive (e.g. `*PASSWORD*`, `*SECRET*`, `*TOKEN*`, `*KEY*`, `*API_KEY*`, `*DATABASE_URL*` with credentials):

1. Create a secret group (use the `secrets` skill or API) with those keys.
2. Reference them in the manifest with `tfy-secret://` format.

```yaml
env:
  LOG_LEVEL: info                                              # plain text OK
  DB_PASSWORD: tfy-secret://my-org:my-service-secrets:DB_PASSWORD  # sensitive
```

Pattern: `tfy-secret://<TENANT_NAME>:<SECRET_GROUP_NAME>:<SECRET_KEY>` where TENANT_NAME is the subdomain of `TFY_BASE_URL`.

Use the `secrets` skill for guided secret group creation. For the full workflow, see `references/deploy-service.md` (Secrets Handling section).

## File Mounts (Config, Secrets, Shared Data)

When users ask to mount files into a deployment, prefer manifest `mounts` over Dockerfile edits:

- `type: secret` for sensitive file content (keys, certs, credentials)
- `type: config_map` for non-sensitive config files
- `type: volume` for writable/shared runtime data

See `references/deploy-service.md` (File Mounts section) for the end-to-end workflow.

## Shared References

These references are available for all workflows — load as needed:

| Reference | Contents |
|---|---|
| `manifest-schema.md` | Complete YAML field reference (single source of truth) |
| `manifest-defaults.md` | Per-service-type defaults with YAML templates |
| `cli-fallback.md` | CLI detection and REST API fallback pattern |
| `cluster-discovery.md` | Extract cluster ID, base domains, available GPUs |
| `resource-estimation.md` | CPU, memory, GPU sizing rules of thumb |
| `health-probes.md` | Startup, readiness, liveness probe configuration |
| `gpu-reference.md` | GPU types and VRAM reference |
| `container-versions.md` | Pinned container image versions |
| `prerequisites.md` | Credential setup and .env configuration |
| `rest-api-manifest.md` | Full REST API manifest reference |

## Workflow-Specific References

| Reference | Used By |
|---|---|
| `deploy-api-examples.md` | deploy-service |
| `deploy-errors.md` | deploy-service |
| `deploy-scaling.md` | deploy-service |
| `load-analysis-questions.md` | deploy-service |
| `codebase-analysis.md` | deploy-service |
| `tfy-apply-cicd.md` | deploy-apply |
| `tfy-apply-extra-manifests.md` | deploy-apply |
| `compose-translation.md` | deploy-multi |
| `dependency-graph.md` | deploy-multi |
| `multi-service-errors.md` | deploy-multi |
| `multi-service-patterns.md` | deploy-multi |
| `service-wiring.md` | deploy-multi |
| `deploy-debugging.md` | All deploy/apply (when status is failed) |
| `async-errors.md` | deploy-async |
| `async-queue-configs.md` | deploy-async |
| `async-python-library.md` | deploy-async |
| `async-sidecar-deploy.md` | deploy-async |

## Composability

- **Find workspace**: Use `workspaces` skill
- **Check what's deployed**: Use `applications` skill
- **View logs**: Use `logs` skill
- **Manage secrets**: Use `secrets` skill
- **Deploy Helm charts**: Use `helm` skill
- **Deploy LLMs**: Use `llm-deploy` skill
- **Register deployment in MCP gateway**: Use `mcp-servers` skill
- **Test after deploy**: Use `service-test` skill

## Success Criteria

- User confirmed service name, resources, port, and deployment source before deploying
- Deployment URL and status reported back to the user
- Deployment status verified automatically immediately after apply/deploy (no extra prompt)
- Health probes configured for production deployments
- Secrets stored securely (not hardcoded in manifests)
- For multi-service: all services wired together and working end-to-end
