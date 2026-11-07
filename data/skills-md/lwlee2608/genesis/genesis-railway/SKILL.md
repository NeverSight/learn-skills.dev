---
name: genesis-railway
description: Use when deploying a project scaffolded with genesis (services/<app>-server Go API, services/<app>-web React app, Postgres) to Railway — creating the Railway project, services, variables, volume, GitHub auto-deploy, and public domain via the Railway MCP server.
user-invocable: true
disable-model-invocation: true
argument-hint: "[app name]"
---

# genesis-railway

Deploys a genesis monorepo to Railway using the Railway MCP tools. The layout it expects: `services/<app>-server` (Go API with a `Dockerfile` and `/health`), `services/<app>-web` (nginx-served React app with a `Dockerfile`), and Postgres.

```
Railway project: <app>
├── Postgres        # Railway Postgres template
├── <app>-server    # builds services/<app>-server/Dockerfile
└── <app>-web       # builds services/<app>-web/Dockerfile, gets the public domain
        web ──▶ server ──▶ Postgres   (private networking)
```

## Prerequisites

**Railway MCP server** (`mcp__railway__*` tools). If they are not available, stop and tell the user — do not fall back to guessing CLI commands.

**Railway CLI** (`npm i -g @railway/cli` or `brew install railway`), used only for `railway login`, `railway init`, `railway add`, `railway link`, and reading resolved variables.

## Rules

1. **Use MCP tools for every Railway mutation.** Settings, variables, volumes, sources, and domains go through `mcp__railway__*`. The CLI is for login, link, and `railway add --database postgres` only.

2. **Never add `railway.json` / `railway.toml`.** Config-as-code is deprecated and stops working 2026-12-01, and no MCP tool writes it. All build/deploy settings are set on the service via `update-service` (step 3). Its successor, `.railway/railway.ts` (`railway config pull/plan/apply`, CLI ≥ 5), is out of scope.

3. **Create services in dependency order.** A `${{Service.VAR}}` reference is empty until the referenced service exists: Postgres, then server, then web.

4. **Find required variables before creating anything.** Grep `cmd/<app>/main.go` for config checks that `os.Exit` — each needs a variable. Config keys map to env with `.` → `_` (`http.port` → `HTTP_PORT`).

5. **Use the Railway Postgres template.** It ships with a volume, the Database tab, backups, and `DATABASE_URL` / `PG*` variables. Only if a migration runs `CREATE EXTENSION vector` fall back to a `pgvector/pgvector` image service (see pgvector exception) — the template image lacks it.

6. **Resolve the project and environment IDs first.** If the repo root is linked, read `~/.railway/config.json` (`.projects["<abs repo path>"].project`). Otherwise `list-projects`, or `railway init --name <app>` from the repo root. Resolve the target environment with `list-services`; use explicit project, environment, and service IDs for configuration and verification.

## Steps

1. **Create services** — `railway add --database postgres` from the linked repo root (the remote MCP has no template tool; the CLI names the service `Postgres`), then `create-service` `<app>-server`, then `<app>-web` (no image).
2. **Variables** via `set-variables` with `skipDeploys: true`:
   - Server: `PORT=8080`, `HTTP_PORT=${{PORT}}` (both — the server reads `HTTP_PORT`; without it the healthcheck probes the wrong port), `DB_URL=${{Postgres.DATABASE_URL}}?sslmode=disable`, `LOG_LEVEL=info`, plus anything found in rule 4 (generate secrets, report them to the user).
   - Web: `BACKEND_URL=http://${{<app>-server.RAILWAY_PRIVATE_DOMAIN}}:8080`
3. **Settings** via `update-service` on server and web: `rootDirectory: services/<app>-{server,web}`, `dockerfilePath: Dockerfile`, `watchPatterns: ["services/<app>-{server,web}/**"]` (repo-root relative), `restartPolicyType: ON_FAILURE`, `restartPolicyMaxRetries: 1`. Server also: `healthcheckPath: /health`, `healthcheckTimeout: 60` (startup only; justify any increase).
4. **Read back** both services' live `config` via `get-service-config`; confirm step 3 and server `PORT=HTTP_PORT=8080` via `list-variables`. If values are hidden, use `railway variables --json --project <project-id> --environment <environment-id> --service <server-id>` without exposing secrets. Fix and recheck mismatches; stop if unverifiable.
5. **Source** — after steps 2–4, `connect-service-source` on server, then web: `repo: <owner>/<repo>`, `branch: main`. This starts builds and GitHub auto-deploy. Record triggered deployment IDs from the response or scoped `list-deployments`, matching source and trigger time; report ambiguity rather than guess.
6. **Domain** — `generate-domain` on web.
7. **Link subdirs** so the CLI works from inside them (absolute paths for `cd`):
   ```sh
   cd <abs>/services/<app>-server && railway link -p <app> -e production -s <app>-server
   cd <abs>/services/<app>-web    && railway link -p <app> -e production -s <app>-web
   ```

## Additional infra

If `docker-compose.yml` has more infra than Postgres (Redis, MinIO, etc.), create each from the official Railway template, not a plain image, and do it before the server so its variables can be referenced. Fall back to `create-service` with `image:` only when no template exists.

## pgvector exception

Replaces step 1's Postgres and adds what the template would have provided:

- `create-service` `Postgres` with `image: pgvector/pgvector:<tag from docker-compose.yml>`.
- `set-variables` (`skipDeploys: true`): `POSTGRES_DB=<app_underscore>`, `POSTGRES_USER=postgres`, `POSTGRES_PASSWORD=<openssl rand -hex 24>`, `PGDATA=/var/lib/postgresql/data/pgdata` (volume root isn't empty), `PGHOST=${{RAILWAY_PRIVATE_DOMAIN}}`, `PGPORT=5432`, `PGUSER=${{POSTGRES_USER}}`, `PGPASSWORD=${{POSTGRES_PASSWORD}}`, `PGDATABASE=${{POSTGRES_DB}}` (the `PG*` set turns on the dashboard's Database tab), `DATABASE_URL=postgres://${{POSTGRES_USER}}:${{POSTGRES_PASSWORD}}@${{RAILWAY_PRIVATE_DOMAIN}}:5432/${{POSTGRES_DB}}`.
- `create-volume` on Postgres, `mountPath: /var/lib/postgresql/data`.
- No Database tab in the dashboard; that only comes with the template.

## Verification procedure

1. Poll scoped `list-deployments` for each recorded ID until `SUCCESS`; never substitute another deployment. On `FAILED`/`CRASHED`, fetch its `get-logs` with `types: ["build", "deploy"]` and report the cause. If blocked or polling stops, report the ID, state, and next action as unverified. Check Postgres with `environment-status`.
2. `curl --fail --max-time 10 https://<web domain>/health` must return the expected backend health response; HTTP errors or unexpected bodies fail verification.
3. For proxy failures, inspect resolved `BACKEND_URL` via MCP or scoped CLI. If `http://:8080`, `redeploy` web and repeat verification with the new deployment ID.

## Common mistakes to watch for

- **Setting only `PORT`.** The server reads `HTTP_PORT`; without it the healthcheck probes the wrong port and every deploy fails.
- **Skipping `PGDATA` on a pgvector image service.** The volume root isn't empty, so Postgres refuses to init without a subdirectory.
- **Connecting the source before variables/settings.** The first build fires immediately and runs with missing config.
- **Using a plain image service when the template would do.** You lose the Database tab and backups for nothing.
- **Using the placeholder `project-00` in `watchPatterns` or service names.** References like `${{project-00-server.RAILWAY_PRIVATE_DOMAIN}}` resolve to empty.
