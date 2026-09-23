---
name: supabase
description: >-
  Use this skill when developing applications with Supabase, running the Supabase CLI, designing migrations and RLS policies, testing database behavior, generating client types, deploying the official self-hosted Docker stack, or administering its Postgres, Auth, Storage, Realtime, Functions, API gateway, backups, upgrades, and security. Use it for managed and self-hosted projects. Do not use for generic PostgreSQL work with no Supabase services or conventions.
license: MIT
compatibility: Requires network access for documentation lookup. Local development requires the Supabase CLI and a Docker-compatible runtime; self-hosting requires Linux, Git, Docker Engine, and Docker Compose.
metadata:
  source: https://supabase.com/docs
  research_checked: "2026-07-16"
---

# Supabase

Treat Supabase as a Postgres-centered system with multiple independently versioned services, not as one opaque backend. The managed platform, CLI local stack, and official self-hosted Compose stack share concepts but are different operating environments. Identify which one the task targets before choosing commands.

## Operating contract

1. Discover the target and current state before changing it: managed project, CLI local stack, or self-hosted Compose; CLI and service versions; project link; database and migration state; enabled services; public URLs; backup and rollback path.
2. Confirm target, scope, and rollback path before the first mutation. Read-only discovery may proceed without confirmation. An explicit user directive to deploy or change the named target satisfies this gate.
3. Keep publishable keys client-side and secret/service-role keys server-side only. Never print, commit, or place secret keys, database passwords, JWT signing material, SMTP credentials, or connection strings containing passwords in reports.
4. Make database changes through versioned migrations. Review generated diffs as drafts, replay the full chain, test RLS negative cases, and regenerate client types before deployment.
5. For self-hosting, use the official `supabase/supabase` Docker directory and its `setup.sh`, `run.sh`, update notes, and tests. Do not invent a reduced Compose stack unless the user explicitly wants one and accepts the lost capabilities.
6. Verify at the delivery boundary: container health is not API health; an API response is not authorization proof; a backup is not recovery evidence.

## Choose the path

| Need | Read first |
|---|---|
| Understand services, trust boundaries, keys, and environment differences | [architecture and boundaries](references/architecture-and-boundaries.md) |
| Install/use the CLI, establish a local workflow, or operate managed Functions, secrets, branches, SSL enforcement, CIDR restrictions, and network bans | [local development and CLI](references/local-development-and-cli.md) |
| Create schemas, migrations, seed data, RLS policies, tests, and generated types | [database development and testing](references/database-development-and-testing.md) |
| Build with Auth, REST, Realtime, Storage, and Edge Functions | [application services](references/application-services.md) |
| Deploy or harden the official Docker stack | [self-hosting deployment](references/self-hosting-deployment.md) |
| Back up, restore, update, upgrade, monitor, or recover a self-hosted instance | [administration and recovery](references/administration-and-recovery.md) |
| Diagnose unhealthy containers, bad URLs, auth failures, drift, or migration failures | [troubleshooting](references/troubleshooting.md) |
| Evaluate how well an agent can use Supabase with scored scenarios | [agent evals harness](references/agent-evals.md) |
| Check claim currency or authoritative source coverage | [source index](references/source-index.md) |

## First read-only discovery

```sh
supabase --version
supabase status --output json       # CLI local project; may fail when stopped
supabase migration list            # linked/local migration comparison when configured
docker compose config --quiet       # self-hosted project directory
docker compose ps --format json
```

For a managed project, also establish the project reference, linked status, target environment, and whether direct production changes have created drift. For self-hosting, inspect `docker/CHANGELOG.md`, `docker/versions.md`, the active `COMPOSE_FILE`, disk/memory headroom, and backup evidence before updates.

## Development loop

Use one schema-authoring mode per project:

```sh
# Declarative: edit supabase/schemas/*.sql first
supabase db diff -f change-name

# Imperative: write the generated migration directly
supabase migration new change-name

# Both paths converge on the same checks
supabase db reset
supabase test db
supabase gen types --lang typescript --local > database.types.ts
```

Review every generated migration. `db diff` does not capture DML and has known gaps around policy renames, views, and some privileges. `db reset` is destructive to the local database but is the reproducibility proof: migrations in order, then seed data.

Before a linked deployment:

```sh
supabase migration list
supabase db push --dry-run
supabase db push
```

Never use `db reset --linked` or `db push --include-seed` against production. Pass `--local` or `--linked` explicitly when ambiguity could hit the wrong database; command defaults differ.

## Self-hosted lifecycle

Use the checked-in official helper scripts from the deployment directory:

```sh
sh run.sh config
sh run.sh compose-config >/dev/null
docker compose config --quiet
sh run.sh start
sh run.sh status
sh tests/test-self-hosted.sh http://localhost:8000
```

Production requires real secrets, correct external URLs, TLS termination, WebSocket forwarding, protected database ports, SMTP/provider configuration as needed, backups, and restore tests. The official default stack exposes Kong on `8000`, Kong TLS on `8443`, and Supavisor on `5432`/`6543`; bind or firewall them deliberately.

## Verification matrix

| Layer | Minimum evidence |
|---|---|
| Configuration | `docker compose config --quiet`; no placeholder secrets; URLs agree with proxy/auth callbacks |
| Runtime | Every required service is running and healthy; bounded logs show no current failure loop |
| Database | Expected Postgres version; migration history matches; representative query succeeds |
| API gateway | Studio auth boundary, Auth health, REST with correct key role, JWKS endpoint |
| Authorization | Positive and negative RLS tests as anon/authenticated users; service-role bypass never used as proof |
| Storage | Bucket/object upload, download, integrity, signed URL, and cleanup |
| Realtime | WebSocket subscription and database-change delivery, not just an HTTP route |
| Functions | Invoke a real function through `/functions/v1`; verify auth behavior and logs |
| Recovery | Independent logical/physical backup plus restore into a separate test target |

## Hard boundaries and gotchas

- The CLI local stack is development-only: default credentials, no TLS, and no production rate limiting. Do not expose it publicly.
- RLS must be enabled on every table in an exposed schema. A publishable key is safe in a client only when grants and RLS policies are correct. Test denial paths.
- Secret/service-role keys bypass RLS. They never belong in browser bundles, mobile apps, logs, examples, or chat output.
- `API_EXTERNAL_URL` includes `/auth/v1` in the current self-hosted configuration. `SITE_URL` is the application landing URL, not necessarily the Supabase hostname.
- Update the Compose configuration as a tested release set. Pulling arbitrary `latest` images independently can create incompatible service combinations.
- Postgres 17 is the current default for new self-hosted deployments. Never point it at a Postgres 15 data directory. Preserve both database data and the `db-config` volume containing the pgsodium root key.
- `docker compose down -v`, `reset.sh`, remote reset, key regeneration, and migration-history repair can destroy data, access, or sessions. Treat them as separate confirmed operations with recovery evidence.
- Self-hosted feature parity is not managed-platform parity. Backups, availability, upgrades, abuse controls, SMTP, observability, and support are operator responsibilities.

## Exit criteria

The task is complete only when the requested artifact or state exists and the relevant boundary has been exercised: a local project replays from migrations and passes tests; a deployment passes configuration, health, and service-level smoke tests; an update has rollback evidence and post-update checks; a backup has been restored into a separate target; and no secret material appears in committed or reported output.
