---
name: langsmith-deployment
description: "Deploy and operate production agent servers with LangSmith Deployment. Use when work involves choosing Cloud vs Hybrid/Self-hosted-with-control-plane vs Standalone, preparing/validating langgraph.json, creating deployments or revisions, rolling back revisions, wiring CI/CD to control-plane APIs, configuring environment variables and secrets, setting monitoring/alerts/webhooks, or troubleshooting deployment/runtime/scaling issues for LangChain/LangGraph applications."
---

# LangSmith Deployment

Use this skill to deploy, revise, monitor, and troubleshoot LangGraph-based agents in LangSmith Deployment.

## Use This Skill When

- You need to deploy a new agent to LangSmith Cloud.
- You need to create a new deployment revision from Git changes or env changes.
- You need rollback guidance for a failing revision.
- You need to choose deployment model: Cloud, Hybrid/Self-hosted with control plane, or Standalone server.
- You need CI/CD automation using LangSmith Deployment control-plane APIs.
- You need monitoring and alert setup aligned with current LangSmith alert model.
- You need `langgraph.json` validation and deployment compatibility checks.

## Deployment Model Selection

| Model | Use when | Build/Source | Operates infra |
|---|---|---|---|
| Cloud | Fastest managed production path | GitHub repo via control plane | LangSmith |
| Hybrid/Self-hosted with control plane | You need private data plane + centralized deployment UI/API | Container image + control plane | You |
| Standalone server | You want direct Agent Server hosting without control plane | Containerized server | You |

## Core Workflow

1. Validate local deployment config.
2. Choose deployment model and endpoint strategy.
3. Create deployment or revision.
4. Configure environment variables and secrets correctly.
5. Configure monitoring and alerts.
6. Verify runtime behavior and keep rollback path ready.

## Script-First Commands

### 1) Validate `langgraph.json`

```bash
uv run python skills/langsmith-deployment/scripts/validate_deployment.py --config langgraph.json --target cloud
```

### 2) Create a Cloud deployment (US default)

```bash
uv run python skills/langsmith-deployment/scripts/deploy_to_langsmith.py \
  --name "my-agent-prod" \
  --owner my-org \
  --repo my-agent-repo \
  --branch main \
  --config langgraph.json
```

### 3) Create a Cloud deployment (EU)

```bash
uv run python skills/langsmith-deployment/scripts/deploy_to_langsmith.py \
  --name "my-agent-prod" \
  --owner my-org \
  --repo my-agent-repo \
  --region eu
```

### 4) Use a self-hosted control plane

```bash
uv run python skills/langsmith-deployment/scripts/deploy_to_langsmith.py \
  --name "my-agent-prod" \
  --owner my-org \
  --repo my-agent-repo \
  --control-plane-url https://<your-langsmith-host>/api-host
```

### 5) Create a revision for an existing deployment

```bash
uv run python skills/langsmith-deployment/scripts/deploy_to_langsmith.py \
  --name "my-agent-prod" \
  --owner my-org \
  --repo my-agent-repo \
  --deployment-id <deployment-id> \
  --branch main
```

### 6) Roll back deployment revision

```bash
uv run python skills/langsmith-deployment/scripts/rollback_deployment.py \
  --deployment-id <deployment-id> \
  --list-revisions

uv run python skills/langsmith-deployment/scripts/rollback_deployment.py \
  --deployment-id <deployment-id>
```

### 7) Generate monitoring + alert setup plan

```bash
uv run python skills/langsmith-deployment/scripts/setup_monitoring.py \
  --project my-agent-prod \
  --output-json /tmp/monitoring-plan.json
```

Note: `setup_monitoring.py` generates a docs-aligned setup plan/templates. Alerts are configured in LangSmith UI per project.

## Configuration Rules To Enforce

- `graphs` is required in `langgraph.json`.
- For Python projects, `dependencies` is required.
- For JS projects (`node_version` present), dependencies may be handled via `package.json`.
- `env` may be either a string path to an env file or an inline object map.
- `python_version` should be one of `3.11`, `3.12`, `3.13` when set.
- `pip_installer` should be one of `auto`, `pip`, `uv` when set.
- `node_version` currently documented for LangGraph.js as `20`.

## API/Endpoint Notes

- LangSmith Deployment control-plane API defaults are:
- US: `https://api.host.langchain.com`.
- EU: `https://eu.api.host.langchain.com`.
- Self-hosted control-plane base URL is typically `https://<host>/api-host`.
- For org-scoped API keys, include workspace/tenant id (`X-Tenant-Id`), exposed by scripts as `--tenant-id`.

## Secrets And Environment Guidance

- Never hardcode secrets in `langgraph.json` or source code.
- Prefer environment injection from deployment UI, Kubernetes Secrets, or cloud secret managers.
- Avoid passing secrets in shell arguments when possible; prefer `LANGSMITH_API_KEY` env var.
- In control-plane deployment flows, tracing auth env handling differs from standalone; rely on deployment model docs before overriding tracing/auth vars.
- For standalone server, ensure required runtime vars are present (`DATABASE_URI`, `REDIS_URI`, license key, and any app provider keys).

## Verification After Deploy

- Check deployment/revision status in LangSmith Deployments UI.
- Verify server API and health endpoints from deployment runtime (`/docs` etc.).
- Run a smoke invocation against your assistant/graph.
- Confirm traces, latency, and error metrics in Monitoring dashboards.

## References To Load By Task

- `references/deployment-guide.md`: Deployment model choice and end-to-end execution.
- `references/cicd-integration.md`: CI/CD stages, control-plane automation patterns, preview/prod strategy.
- `references/environment-management.md`: Env var sources, secrets patterns, standalone required vars.
- `references/monitoring-alerts.md`: Dashboards, alert model, webhook payload guidance.
- `references/scaling-configuration.md`: Scaling responsibilities by model and tuning knobs.
- `references/troubleshooting-deployment.md`: Failure triage and rollback strategy.

## Script Map

- `scripts/validate_deployment.py`: Validate `langgraph.json` and deployment readiness.
- `scripts/deploy_to_langsmith.py`: Create deployment or revision via control-plane API.
- `scripts/deploy_to_langsmith.ts`: TypeScript equivalent deploy/revision script.
- `scripts/rollback_deployment.py`: List and rollback revisions.
- `scripts/setup_monitoring.py`: Generate alert/dashboard/webhook setup plan.

## Assets

- `assets/templates/langgraph-cloud.json`: Cloud-oriented starter config.
- `assets/templates/github-actions-deploy.yml`: CI/CD template for deployment automation.
- `assets/templates/kubernetes-deployment.yaml`: Kubernetes template for self-managed environments.
- `assets/templates/.env.example`: Env var template for safe sharing.
