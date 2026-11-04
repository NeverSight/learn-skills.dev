---
name: apta-go-backend
description: Scaffold an Apta-standard Go + Gin backend (GORM/Postgres, JWT auth, users/roles/user-roles, slog, Swagger, cobra, uber/dig DI, OpenTelemetry) modeled on fleet-backend, and add CRUD endpoints to it. Use whenever the user wants to start, bootstrap, init or scaffold a new Go/Gin/golang backend or API service, or add a new resource, entity, model or CRUD endpoint (handler, service, repository, route) to an Apta Go backend, or enable its optional S3, Infisical or NATS modules, even if they never say "scaffold" or "skill".
---

# Apta Go backend

Generates a backend that is a trimmed copy of `fleet-backend`: same versioned layered layout,
env names, naming and response envelope, with only the shared foundations (users, roles,
user-roles) kept. Everything is produced by `scripts/scaffold.py` from the templates in `assets/`,
so output is deterministic and the module path is rewritten in one pass. Run the script rather than
hand-copying files — hand copies drift from the standard and leave stale module paths.

The script needs `python3` (stdlib only). Locate it relative to this skill, e.g.
`python3 <skill-dir>/scripts/scaffold.py ...`. Run `--help` on any subcommand for all flags.

## What ships

- Enabled: Gin, GORM + Postgres, JWT (access + refresh), users / roles / user-roles, slog
  (stdout + OTel, GORM queries logged through slog), Swagger (swaggo), cobra (`serve`, `migrate`),
  uber/dig DI, OpenTelemetry (traces, logs, metrics), pagination, TTL read caching on every repository
  (`ttlcache`, 5 min, cleared on writes), Dockerfile, compose, CI workflows.
- Present but commented out (zero cost until enabled): **S3**, **Infisical**, **NATS**. Use
  `enable` below — never uncomment by hand.

## 1. New project

1. Get the Go **module path** (e.g. `github.com/devapta/orders-api`). Ask if the user did not give
   one; it cannot be guessed. Optional: `--name` (kebab-case app/image name, defaults to last module
   segment), `--title`, `--db-name`, `--port` (default 7008), `--dir` (default `./<name>`; pass `--dir .`
   to scaffold into the current empty repo).
2. Run:
   ```bash
   python3 <skill-dir>/scripts/scaffold.py init --module <module> [--name ...] [--dir ...]
   ```
   It renders ~66 files, replaces every `fleet-backend` / module reference (it fails loudly if a
   placeholder or reference name survives), writes a stub `docs/`, creates `.env` with a random
   `JWT_SECRET`, then runs `go mod tidy` and `swag init` when those tools exist.
3. If tidy/swag were skipped or failed (offline, tool missing), tell the user exactly what to run.
4. Report what was created and the next steps for the user: review `.env`, `make migrate`, `make go`.
   The default admin comes from `DEFAULT_USER` / `DEFAULT_EMAIL` / `DEFAULT_PASSWORD`.

Do not run `serve` or `migrate` — they need a database and belong to the user. Respect the project's
own agent rules file (the generated AGENTS.md forbids build/run commands; if it is in force, skip
`go build` and leave verification to the user).

## 2. Add a CRUD endpoint

From the project root (the directory with `go.mod`; or pass `--dir`):

```bash
python3 <skill-dir>/scripts/scaffold.py crud --name VehicleType \
  --field code:string:unique:notnull --field displayName:string --field tolerance:float64
```

- `--name` is the singular entity in any case (`VehicleType`, `vehicle-type`, `vehicle type`).
  Plurals are derived (`vehicle-types`); pass `--plural` when the rule is wrong (`person` → `people`).
- `--field name:type[:unique][:notnull]`, repeatable; types `string int int64 uint float64 bool time date` (`date` = date-only column); `notnull` also makes the field `binding:"required"` on the request model.
  Foreign keys are plain `uint` fields (`ownerId:uint`). With no `--field` you get a `Name` string.
- It creates entity, model, repository, service, handler and route files, and wires them into
  `internal/container/di.go`, `internal/v1/routes/router.go`, `internal/configs/postgres.go`
  (migrate + drop) and `internal/enums/permissions.go` (`<plural>#create|read|update|delete`).
  `--cache-endpoint` also adds `DELETE /<plural>/caches` (needs `<plural>#update`) to flush that resource's read cache.
  Repositories come with the read cache already (see `references/architecture.md`, "Read caching").
  It refuses to overwrite existing files.

Then finish what a generator cannot know — read `references/crud-endpoint.md` for how: joins in the
repository `pageQuery`, GORM relations on the entity, custom service logic, extra routes, and
whether the new permissions should be granted to a seeded role. Remind the user to run `make swag`
and `make migrate`.

If the project has no `// scaffold:` markers (older or hand-edited project), make the same edits by
hand following `references/crud-endpoint.md` instead of failing.

## 3. Enable S3 / Infisical / NATS

```bash
python3 <skill-dir>/scripts/scaffold.py enable s3 infisical nats   # any subset
```

Uncomments the module's files, DI providers, env struct fields and example env vars, adds needed
imports, and runs `go mod tidy` to pull the SDK. Afterwards the user must fill in the new env vars.
NATS ships a generic `ExampleConsumer`; see `references/optional-modules.md` for adapting it and for
what each module expects.

## Conventions to keep when editing the generated code

Read `references/architecture.md` before changing structure. The short version:

- Layers: `entities` → `v1/models` → `v1/repositories` → `v1/services` → `v1/handlers` → `v1/routes`,
  all constructors registered in `internal/container/di.go`; entities registered in `postgres.go`.
- All DB access lives in repositories. Handlers pass `c.Request.Context()` onward.
- Responses use `common.Result[T]` (`ResultOk` / `ResultErr`); lists return `paginate.Page`.
- Every handler carries swaggo annotations; never edit generated files under `docs/`.
- Any repository method that writes must call `r.ClearCaches()` on success, or lists stay stale for the TTL.
- Look up dependency APIs with Context7 before writing library-specific code.

## Retained from fleet-backend as-is

These are faithful to the reference, so say so to the user instead of silently changing them:
`POST /api/v1/users` is public (self-registration) and there is no `users#create` permission;
`/api/v1/user-roles` routes require authentication but no permission check; the Admin role seeded by
`migrate` holds `*`. Offer to tighten them if the user wants.

Two fleet-backend bugs are fixed in the templates (cookie `MaxAge` was in nanoseconds; `GetPermissions`
failed for users with no roles). Mention them if the user compares against fleet-backend.
