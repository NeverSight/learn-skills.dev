---
name: vexdock-api
description: Operate a Vexdock server (self-hosted deployment platform) through its REST API with a bearer token. Use when asked to deploy, inspect, restart, run a command in, configure or clean up anything on a Vexdock host, or when VEXDOCK_URL and VEXDOCK_TOKEN are set in the environment.
---

# Vexdock API

Vexdock has no CLI. The API is the whole interface; the dashboard is just one
client of it. Everything below is `curl` and `jq`.

## Setup

Two environment variables. Ask the user for them when they are missing; never
print the token back.

```sh
export VEXDOCK_URL=https://panel.example.com   # no trailing slash
export VEXDOCK_TOKEN=...                        # System → Settings → API tokens, shown once
```

Define this once per shell and use it for every call:

```sh
vx() { curl -sS -H "Authorization: Bearer $VEXDOCK_TOKEN" -H 'Content-Type: application/json' "$VEXDOCK_URL$@"; }
```

Verify: `vx /api/me` returns the account; `vx /api/health` (public) reports
`{"status":"healthy"}` or `503`.

Create a token from a session-authenticated context, or ask the user to:
`POST /api/tokens {"name":"agent"}` → `201 {"token":{...},"value":"..."}`;
`value` never appears again. `DELETE /api/tokens/{id}` revokes.

## Conventions

- Bearer token means no CSRF header. Session cookies need same-origin; do not use them from scripts.
- JSON bodies, `Content-Type: application/json`. Unknown fields are rejected with `400`.
- Errors: `{"error":{"code","message","details"?}}`. Codes: `INVALID_REQUEST` 400,
  `UNAUTHORIZED` 401, `CROSS_ORIGIN` 403, `NOT_FOUND` 404, `CONFIRMATION_REQUIRED` 428,
  `CONFLICT` 409, `TASK_RUNNING` 409, `UNHEALTHY` 409, `GIT_PROVIDER_IN_USE` 409, `PROJECT_NOT_EMPTY` 409,
  `DATABASE_NOT_RUNNING` 409, `STUDIO_UNSUPPORTED` 400, `QUERY_FAILED` 400,
  `GIT_PROVIDER_UNAVAILABLE` 400, `GIT_PROVIDER_ERROR` 502, `CERTIFICATE_FAILED` 502, `INTERNAL` 500. `429` comes from Nginx without the envelope.
- Ids are opaque strings. Resolve names to ids by listing; never guess.
- Project routes act on the project's **default environment** unless `?environment={id}` is given.
  Applies to `deploy`, `stop`, `services`, `services/export`, `deployments`.
- Deploys return `202` immediately. Poll `GET /api/deployments/{id}` until `deployment.status` is
  `success`, `failed` or `cancelled` (`queued`/`running` meanwhile), or stream `.../events`.
- A non-zero exit from `exec` or a task `run` is still `200`; read `exit_code`.
- Destructive calls: volume deletes and `cleanup/volumes` need `?confirm=true`; an
  environment delete takes `?volumes=true` to also drop data. A project deletes only once it has no
  services (`409 PROJECT_NOT_EMPTY`). Confirm with the user before
  passing either flag. Every mutation is audit-logged.
- Streams are SSE: `curl -N` and read `event:`/`data:` lines. The terminal is a WebSocket; use
  `POST .../exec` instead.

## Finding things

```sh
vx /api/projects | jq '.[] | {id, name, environments: [.environments[] | {id, name, is_default}]}'
vx /api/projects/$PROJECT/services | jq '.[] | {id, name, provider, state, status, health}'
vx /api/projects/$PROJECT/services?environment=$ENV
vx /api/docker/containers | jq '.[] | {id, name, state, managed}'
vx /api/domains | jq '.[] | {id, hostname, service, project_id}'
vx /api/tasks | jq '.[] | {id, name, schedule, service_name, project_name}'
```

## Deploy and wait

```sh
DEP=$(vx /api/services/$SERVICE/deploy -X POST | jq -r .id)     # or /api/projects/$PROJECT/deploy
until [ "$(vx /api/deployments/$DEP | jq -r .deployment.status)" != "queued" ] && \
      [ "$(vx /api/deployments/$DEP | jq -r .deployment.status)" != "running" ]; do sleep 3; done
vx /api/deployments/$DEP | jq '{status: .deployment.status, steps: [.steps[] | {name, status}]}'
```

Live log instead of polling: `curl -N -H "Authorization: Bearer $VEXDOCK_TOKEN" $VEXDOCK_URL/api/deployments/$DEP/events`.

- `POST /api/deployments/{id}/cancel` while queued or running.
- `POST /api/deployments/{id}/rollback` redeploys the commit that deployment recorded (`400` if none).
- `POST /api/projects/{id}/stop` is `compose down`; volumes stay.

## Run a command in a service

```sh
vx /api/services/$SERVICE/exec -d '{"command":"php artisan migrate --force"}'
# → {"exit_code":0,"output":"..."}
```

`shell` is `sh` (default) or `bash`. Shell syntax works (pipes, `&&`, env).
Runs in the service's container, never on the host. After 10 minutes the call
gives up but the command keeps running, so check before retrying it; output
over 1 MiB keeps its tail. The container must be running.

## Query a database (Studio)

Catalog databases only; the manager connects over the compose network, no published port needed.

```sh
vx /api/services/$SERVICE/studio | jq '.schemas[] | {name, tables: [.tables[].name]}'
vx "/api/services/$SERVICE/studio/rows?schema=public&table=users&limit=20&sort=id&order=desc"
vx /api/services/$SERVICE/studio/query -d '{"schema":"public","query":"select count(*) from users"}'
# → {"columns":["count"],"rows":[["42"]],"affected":0,"duration_ms":3,"truncated":false}
vx /api/services/$SERVICE/studio/changes -d '{"schema":"public","table":"users","updates":[{"key":{"id":"7"},"values":{"name":"Ada"}}]}'
```

- Every cell is a string or `null`; non-UTF-8 bytes come as `\x` hex, MongoDB fields as relaxed Extended JSON.
- `where` is URL-encoded JSON `[{"column","op","value"}]`; `op`: `eq neq gt gte lt lte contains starts_with is_null is_not_null`.
- `limit` 1-500; query results stop at 1,000 rows (`truncated`). A table whose `key` is empty is read-only.
- The query is SQL, one Extended JSON command for MongoDB (`{"find":"users","limit":5}`),
  or one command line for Valkey (schema `db0`, table `keys`). It runs in autocommit: confirm writes with the user first.
- `QUERY_FAILED` carries the database's own error message.

## Lifecycle without a pipeline

```sh
vx /api/services/$SERVICE/start   -X POST
vx /api/services/$SERVICE/stop    -X POST
vx /api/services/$SERVICE/restart -X POST
vx /api/docker/containers/$CONTAINER/restart -X POST   # any container, managed or not
```

## Logs and stats

```sh
curl -N -H "Authorization: Bearer $VEXDOCK_TOKEN" "$VEXDOCK_URL/api/services/$SERVICE/logs"   # SSE: log, end
curl -N -H "Authorization: Bearer $VEXDOCK_TOKEN" "$VEXDOCK_URL/api/services/$SERVICE/stats"  # SSE: stats
vx "/api/services/$SERVICE/metrics?window=1h"     # 30m 1h 6h 24h 7d
vx "/api/system/metrics?window=24h"
vx /api/system/info
```

## Projects and services

```sh
vx /api/projects -d '{"name":"shop"}'                                    # 201
vx /api/services/$SERVICE -X PATCH -d '{"auto_deploy":true}'
vx /api/projects/$PROJECT -X DELETE                                      # only once it has no services

# git application
vx /api/projects/$PROJECT/services -d '{"name":"web","provider":"github","repository_url":"https://github.com/o/r","branch":"main"}'
# image
vx /api/projects/$PROJECT/services -d '{"name":"cache","provider":"image","image":"redis:7-alpine"}'
# database from the catalog (image, volume, credentials generated)
vx /api/projects/$PROJECT/services -d '{"name":"db","database":{"engine":"postgres","version":"17-alpine"}}'
vx /api/services/$SERVICE/database                                       # connection details
# pasted compose fragment
vx /api/projects/$PROJECT/services -d '{"name":"worker","provider":"raw","compose_fragment":"image: x\ncommand: run"}'

vx /api/services/$SERVICE -X PATCH -d '{"branch":"release"}'
vx /api/services/$SERVICE -X DELETE                                      # named volume is kept
vx /api/engines; vx /api/engines/postgres/versions
```

Create and edit never start a container: deploy afterwards. `provider` is
`unconfigured`, `github|gitlab|bitbucket|gitea|git`, `image` or `raw`. Git
credentials: `credential_kind` `none|token|ssh_key` + `credential_secret`
(write-only), or `git_provider_id` + `owner` + `repository` for a connected
provider (`GET /api/git-providers`, `.../{id}/repositories`).

## Variables

Three layers, all `GET | PUT`, written whole (`PUT` replaces the set):

```sh
vx /api/projects/$PROJECT/variables        # every environment of the project
vx /api/environments/$ENV/variables        # this environment only; wins on collision
vx /api/services/$SERVICE/variables        # this service only
vx /api/services/$SERVICE/variables -X PUT -d '{"variables":[{"key":"APP_ENV","value":"production","is_secret":false},{"key":"APP_KEY","value":"...","is_secret":true}]}'
```

Read first, merge, then `PUT`; a `PUT` with a partial list drops the rest.
A change needs a deploy to reach the container.

## Environments

```sh
vx /api/projects/$PROJECT/environments
vx /api/projects/$PROJECT/environments -d '{"name":"staging","branch":"develop"}'
vx /api/environments/$ENV -X PATCH -d '{"branch":""}'   # "" = each service follows its own branch
vx /api/environments/$ENV -X DELETE                     # ?volumes=true; default env answers 400
vx "/api/projects/$PROJECT/deploy?environment=$ENV" -X POST
```

## Domains

```sh
vx /api/domains -d '{"project_id":"'$PROJECT'","service":"web","hostname":"shop.example.com","container_port":3000,"https_enabled":true,"redirect_https":true}'
vx /api/domains/$DOMAIN/certificate -X POST              # issue/renew now; 502 CERTIFICATE_FAILED with reason
vx /api/domains/$DOMAIN -X DELETE
```

Optional: `environment_id`, `certificate_source` `letsencrypt|custom` (+
`certificate_pem`, `private_key_pem`). A create/update may answer with a
`warning` when the vhost saved but the certificate did not; retry via
`certificate`.

## Scheduled tasks

```sh
vx /api/services/$SERVICE/tasks -d '{"name":"prune","schedule":"0 3 * * *","timezone":"Europe/Warsaw","command":"php artisan model:prune"}'
vx /api/tasks/$TASK -X PATCH -d '{"enabled":false}'
vx /api/tasks/$TASK/run -X POST                          # answers with the finished run; 409 TASK_RUNNING if busy
vx "/api/tasks/$TASK/runs?limit=5"
vx /api/tasks/$TASK -X DELETE
```

Five-field cron plus `@hourly|@daily|@weekly|@monthly|@yearly`. Nothing is
replayed for ticks missed while the manager was down. A run still going after
30 minutes is given up on, though its process may keep running.

## Docker housekeeping

```sh
vx /api/docker/cleanup                                   # dry run: bytes per kind
vx /api/docker/cleanup/images -X POST                    # containers | images | networks | build-cache
vx "/api/docker/cleanup/volumes?confirm=true" -X POST    # ask the user first
vx /api/docker/images/pull -d '{"reference":"nginx:1.27"}'
vx "/api/docker/images/$IMAGE?force=true" -X DELETE
vx "/api/docker/volumes/$NAME?confirm=true" -X DELETE
vx /api/docker/containers/$CONTAINER/remove?force=true -X POST
```

## System

```sh
vx /api/system/settings                                  # PUT writes the whole object; cloudflare_api_token is write-only
vx /api/system/backup -X POST                            # ?volumes=true is slow and large; snapshot holds the master key
vx /api/system/backups; vx /api/system/backups/2026-01-05T031500 -X DELETE
vx /api/system/version; vx /api/system/version/check -X POST
vx /api/system/update -X POST -d '{}'                    # latest on track; refuses 409 UNHEALTHY
vx /api/system/update/status                             # phase: idle|backup|pulling|restarting|done|rolled-back
vx /api/system/certificates
vx /api/registries -d '{"name":"ghcr","url":"ghcr.io","username":"u","password":"..."}'   # login is verified on create
```

`POST /api/system/update` recreates the manager: expect the API to drop for a
minute during `restarting`; keep polling `update/status`.

## Working style

1. Resolve ids by listing, print names next to ids when reporting.
2. Prefer the narrowest call: service deploy over project deploy, `exec` over restart.
3. Read-modify-write for `PUT` endpoints (variables, settings).
4. State what a destructive call will remove and get a yes before `confirm=true` / `volumes=true`.
5. After a deploy, report `status` and the failing step's name if any; the step log is in the events stream.
6. Never echo `VEXDOCK_TOKEN`, `credential_secret`, registry passwords or `?secrets=true` exports.

The full reference with response shapes is `docs/api.md` in the Vexdock
repository; `GET /api/health` and `/api/system/version` are the only public
reads.
