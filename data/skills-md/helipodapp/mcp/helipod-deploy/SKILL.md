---
name: helipod-deploy
description: Deploy an application, worker or database to Helipod containers and operate it - choose image vs Git vs Dockerfile, set environment variables and secrets, connect services, add domains, scale, read build and runtime logs, use one-click templates. Use when the user wants to deploy, host, ship or debug an app on Helipod.
---

# Deploy to Helipod containers

Follow the `helipod` skill rules (price first, confirm destructive actions, never print secrets).

## 1. Find where to deploy

`list_projects` → pick the project and environment (usually `production`). If several fit, ask the user.
`list_services` on that environment shows what already runs (avoid duplicate names; reuse an existing database).

## 2. Choose the source

| The project has | Use |
|---|---|
| A published image (Docker Hub, GHCR, private registry) | `image` (fastest, no build). Private: `registryUsername` + `registryPassword` |
| A public Git repo | `repo` (+ `branch`, `rootDirectory` for monorepos). Built by Helipod: a `Dockerfile` in the folder is used, else **Helipack** detects Node/Bun, PHP and Python frameworks |
| Only local files | Push to a public Git repo first, or build and push an image. A short `dockerfile` can be sent inline |
| A database or known app (Postgres, MySQL, Redis, WordPress, n8n, ...) | `list_templates` → `deploy_template` |

Private Git repos are connected in the dashboard (GitHub/GitLab integration), not through the API.

Before deploying a repo, check it quickly: the port the app listens on (prefer `process.env.PORT`), the start command, a health endpoint. For Next.js Helipack adds `output: "standalone"` itself. To override detection, add `helipack.json` at the app root:

```json
{ "run": { "port": 3000, "command": "node server.js" }, "build": { "command": "npm run build" }, "health": { "path": "/health" } }
```

## 3. Create (price first)

1. `create_service` with `dryRun: true` → show `dailyCost` (IDR per day) to the user, wait for yes.
2. `create_service` again without `dryRun`, with an `idempotencyKey`. Give `ports: [{ "port": <app port> }]` so it gets an HTTPS `*.helipod.app` domain.
3. Poll `get_deployment` until `success` / `failed`. Builds take 1 to 5 minutes; images are faster.
4. On `success`: give the user the domain `url`. On `failed`: `get_deployment_logs`, find the real error (missing env var, wrong port, build error), fix, `deploy_service` again.

## Variables and connecting services

- `set_variables` creates or updates keys; put credentials in `secrets` (write-only afterwards).
- Reference other services instead of copying values: `DATABASE_URL = ${{Postgres.DATABASE_URL}}`, private host `${{Postgres.HELIPOD_PRIVATE_DOMAIN}}`, random secret once: `${{secret(32)}}`.
- Variable, volume and setting changes apply on the **next deploy**: call `deploy_service` after changing them.

## Operate

- Logs: `get_service_logs` (`filter: "error"`, `since: "1h"`); metrics: `get_service_metrics`.
- Restart without rebuild: `restart_service` (running services only).
- Scale: `scale_service` with `dryRun: true` first, show current vs new daily cost.
- Custom domain: `add_service_domain` with `kind: "custom"`, then tell the user the DNS record from the response (`CNAME` to `cname.helipod.app`, or the `A` record for a root domain). If the domain is on Helipod, the `helipod-domains` skill can create the record.
- Persistent files: `add_volume` (mount path), then redeploy. Without a volume, files are lost on every deploy.

## Several services at once

`create_stack` takes a template spec (services with `source`, `variables`, `networking`, `volumes`, `dependsOn`) and deploys them in dependency order. Always `dryRun: true` first. Spec reference: https://docs.helipod.io/docs/container-api/templates-and-stacks

## Common failures

| Symptom | Fix |
|---|---|
| Health check / deploy timeout | App must listen on the exposed port, on `0.0.0.0`, not `localhost` |
| `402` | Plan limit (services, CPU, RAM, storage) or low balance: tell the user |
| Crash loop on start | Read runtime logs; usually a missing variable or failed DB connection |
| Monorepo built from root | Set `rootDirectory` (`update_service`) and redeploy |
