---
name: eve-manifest-authoring
description: Author and maintain Eve manifest files (.eve/manifest.yaml) for services, environments, pipelines, workflows, and secret interpolation. Use when changing deployment shape or runtime configuration in an Eve-compatible repo.
---

# Eve Manifest Authoring

Keep the manifest as the single source of truth for build and deploy behavior.

## Minimal skeleton (v2)

```yaml
schema: eve/compose/v2
project: my-project

registry: "eve"  # Use managed registry by default for Eve apps
services:
  api:
    build:
      context: ./apps/api           # Build context directory
      dockerfile: Dockerfile        # Optional, defaults to context/Dockerfile
    # image omitted by default; when build is present, Eve derives image name from service key
    ports: [3000]
    environment:
      NODE_ENV: production
    x-eve:
      ingress:
        public: true
        port: 3000

environments:
  staging:
    pipeline: deploy
    pipeline_inputs:
      some_key: default_value

pipelines:
  deploy:
    steps:
      - name: build
        action:
          type: build               # Builds all services with build: config
      - name: release
        depends_on: [build]
        action:
          type: release
      - name: deploy
        depends_on: [release]
        action:
          type: deploy
```

## Registry Image Labels

Some registries require package metadata for permission and ownership inheritance.
Add these labels to your Dockerfiles when supported by your registry:

```dockerfile
LABEL org.opencontainers.image.source="https://github.com/YOUR_ORG/YOUR_REPO"
LABEL org.opencontainers.image.description="Service description"
```

**Why this matters**: Metadata helps preserve repository ownership and improves traceability. The Eve builder injects these labels automatically, but including them in your Dockerfile is still recommended.

For multi-stage Dockerfiles, add the labels to the **final** stage (the production image).

## Registry Modes

```yaml
registry: "eve"     # Eve-native registry (internal JWT auth)
registry: "none"    # Disable registry handling (public images)
registry:           # BYO registry (full object — see section below)
  host: public.ecr.aws/w7c4v0w3
  namespace: myorg
  auth: { username_secret: REGISTRY_USERNAME, token_secret: REGISTRY_PASSWORD }
```

For BYO/private registries, provide:

```yaml
registry:
  host: public.ecr.aws/w7c4v0w3
  namespace: myorg
  auth:
    username_secret: REGISTRY_USERNAME
    token_secret: REGISTRY_PASSWORD
```

## Managed Databases

Declare platform-provisioned databases with `x-eve.role: managed_db`:

```yaml
services:
  db:
    x-eve:
      role: managed_db
      managed:
        class: db.p1
        engine: postgres
        engine_version: "16"
```

Not deployed to K8s — provisioned by the orchestrator on first deploy.
Reference managed values elsewhere: `${managed.db.url}`.

## Legacy manifests

If the repo still uses `components:` from older manifests, migrate to `services:`
and add `schema: eve/compose/v2`. Keep ports and env keys the same.

## Services

- Provide `image` and optionally `build` (context and dockerfile).
- Use `ports`, `environment`, `healthcheck`, `depends_on` as needed.
- Use `x-eve.external: true` and `x-eve.connection_url` for externally hosted services.
- Use `x-eve.role: job` for one-off services (migrations, seeds).

### Build configuration

Services with Docker images should define their build configuration:

```yaml
services:
  api:
    build:
      context: ./apps/api           # Build context directory
      dockerfile: Dockerfile        # Optional, defaults to context/Dockerfile
    # image: api      # optional if using build; managed registry derives this
    ports: [3000]
```

Note: Every deploy pipeline should include a `build` step before `release`. The build step creates tracked BuildSpec/BuildRun records and produces image digests that releases use for deterministic deployments.

## Local dev alignment

- Keep service names and ports aligned with Docker Compose.
- Prefer `${secret.KEY}` and use `.eve/dev-secrets.yaml` for local values.

## Environments, pipelines, workflows

- Link each environment to a pipeline via `environments.<env>.pipeline`.
- When `pipeline` is set, `eve env deploy <env>` triggers that pipeline instead of direct deploy.
- Use `environments.<env>.pipeline_inputs` to provide default inputs for pipeline runs.
- Override inputs at runtime with `eve env deploy <env> --ref <sha> --inputs '{"key":"value"}' --repo-dir ./my-app`.
- Use `--direct` flag to bypass pipeline and do direct deploy: `eve env deploy <env> --ref <sha> --direct --repo-dir ./my-app`.
- Pipeline steps can be `action`, `script`, or `agent`.
- Use `action.type: create-pr` for PR automation when configured.
- Workflows live under `workflows` and are invoked via CLI; `db_access` is honored.

## Platform-Injected Environment Variables

Eve automatically injects these into all deployed service containers:

| Variable | Description |
|----------|-------------|
| `EVE_API_URL` | Internal cluster URL for server-to-server calls |
| `EVE_PUBLIC_API_URL` | Public ingress URL for browser-facing apps |
| `EVE_PROJECT_ID` | The project ID |
| `EVE_ORG_ID` | The organization ID |
| `EVE_ENV_NAME` | The environment name |

Use `EVE_API_URL` for backend calls from your container. Use `EVE_PUBLIC_API_URL` for
browser/client-side code. Services can override these in their `environment` section.

## Interpolation and secrets

- Env interpolation: `${ENV_NAME}`, `${PROJECT_ID}`, `${ORG_ID}`, `${ORG_SLUG}`, `${COMPONENT_NAME}`.
- Secret interpolation: `${secret.KEY}` pulls from Eve secrets or `.eve/dev-secrets.yaml`.
- Managed DB interpolation: `${managed.<service>.<field>}` resolves at deploy time.
- Use `.eve/dev-secrets.yaml` for local overrides; set real secrets via the API for production.

## Eve extensions

- Top-level defaults via `x-eve.defaults` (env, harness, harness_profile, harness_options, hints, git, workspace).
- Top-level agent policy via `x-eve.agents` (profiles, councils, availability rules).
- Agent packs via `x-eve.packs` with optional `x-eve.install_agents` defaults.
- Agent config paths via `x-eve.agents.config_path` and `x-eve.agents.teams_path`.
- Chat routing config via `x-eve.chat.config_path`.
- Service extensions under `x-eve` (ingress, role, api specs, worker pools).
- API specs: `x-eve.api_spec` or `x-eve.api_specs` (spec URL relative to service by default).

Example:

```yaml
x-eve:
  agents:
    version: 1
    config_path: agents/agents.yaml
    teams_path: agents/teams.yaml
  chat:
    config_path: agents/chat.yaml
  install_agents: [claude-code, codex]
  packs:
    - source: ./skillpacks/my-pack
```
