---
name: deployment-plan
description: 'Produce the operational runbook in docs/deployment-plan/, one file per section, by first grilling the user on infrastructure, environments, secrets, release flow, and rollback until every gap is resolved. It covers environments, infra overview, initial deploy, release updates, rollback, database reset, and a database debugging cookbook with copy-paste commands. On a running project it documents the deployment as it runs today. Use when the user wants a deployment plan, deployment runbook, ops/release documentation, or asks to "write a DEPLOYMENT_PLAN".'
---

# Deployment Plan

Two phases: **grill first, then write.** A deployment runbook is only useful if it reflects the real infrastructure and the operator can paste its commands verbatim and have them work. So extract the truth before writing a line of the document.

**Running project (adopt mode).** If the system already deploys, document how it deploys today. Record each gap you find (no backups, no rollback path, secrets in the repo) as a finding in the runbook and in your report. Do not redesign the deployment here.

## Phase 1: Grill

Interview the user relentlessly about how this system actually deploys, one question at a time, walking each branch until resolved. For every question, give your recommended answer and explain the trade-off, but don't move on until they confirm.

**Inspect before asking.** Read the repo first: `docker-compose*.yml`, `Dockerfile`, `.github/workflows/`, `deploy/`, nginx configs, `.env.example`, migration setup, README, any existing `CLAUDE.md` or `AGENTS.md`, and in `docs/technical-specs/` the security section (the reset-API decision) and the environment configuration (the gating flag names). Every fact you can read, read; don't ask what the repo already answers. Ask only to fill genuine gaps and to confirm inferences.

Cover, at minimum (skip what's irrelevant to this stack, probe what's load-bearing):

- **Environments.** How many (dev / test / staging / prod), their URLs/hosts, who can deploy to each, and how they differ.
- **Infrastructure.** Hosting (VPS / cloud / k8s / PaaS), what runs where, the topology (app, db, cache, proxy, object storage), and the network boundaries between them. **Pin down whether the app and the database live on the same host or separate VMs**: if separate, capture the DB host/port, how the app reaches it (private network, security group, allowlisted IP), and whether DB commands must run from the DB VM or can run remotely from the app VM. Cross-VM topology is the common cause of a reset going wrong (commands run against the wrong host, or the app keeps a stale connection pool after the DB is wiped).
- **Artifacts & registry.** How images/builds are produced (CI? manual?), where they're stored (GHCR / ECR / Docker Hub), tagging scheme, and how a host authenticates to pull.
- **Configuration & secrets.** The full env-var set, which are required vs optional, how secrets are generated and injected, and what must never be committed.
- **Initial deploy.** Prerequisites on a fresh host, the exact bring-up sequence, first-run migrations, seeding, and the admin/bootstrap credentials.
- **Reverse proxy & TLS.** Proxy choice, domains, certificate issuance/renewal, and security headers.
- **Release updates.** The update flow with and without schema changes, how migrations run against a new image safely, version pinning, and how a deploy is verified. **Establish one migrate command and one seed command** that resolve their own paths and connection string (the Writing rules below give the rule).
- **Rollback.** How to revert an image, what happens to the database on rollback (destructive migrations? down-migrations? manual?), and who to contact.
- **Operations.** DB access for debugging, backup/restore, log access, and health checks.
- **Database state reset.** This is load-bearing for QA: how the database is wiped, re-migrated, and reseeded back to a known initial state, and which seed (dev vs QA) each environment uses. Establish which environments allow a reset (dev / test / SIT / UAT only; never prod), who triggers it, whether it goes through a guarded reset API (see the technical specs) or a manual runbook, and the exact order of operations across the app and DB hosts. Capture what must happen to the app after a wipe (restart, drain connection pool, clear cache) so it doesn't keep serving against a dropped schema. Confirm the seed datasets are version-controlled and idempotent.

Surface contradictions as you find them ("the compose file pulls `:latest` but you said releases are version-pinned; which is authoritative?"). Note anything genuinely dangerous (no backups before destructive migration, secrets in the repo, no rollback path) and make sure the plan addresses it.

When every branch is resolved, summarize the decisions back and confirm before writing.

## Phase 2: Write the runbook

Write `docs/deployment-plan/` in the layout of [references/layout.md](references/layout.md): an `_index.md` and one file per section. It is operational, not aspirational: every command must be copy-paste-runnable for this project, using its real service names, paths, image refs, and env vars. Use fenced shell blocks with terse `#` comments explaining each step. Adapt section depth to the stack.

### Writing rules

- Commands must reflect reality: real container/service names from the compose file, real image refs, real env-var names. No placeholders where a real value is known.
- Every destructive command carries a one-line warning about what it deletes and how to back up first.
- **Never document migrations or seeding as a hardcoded path or an inline raw-SQL read**, in any language. The migration and seed steps must invoke the project's own runner, which resolves the migrations location relative to its own module and reads the connection string from the environment. State the migrate and seed steps as one stable command each (whatever the stack's equivalent is: a make target, a manage.py command, a `mix`/`rake`/`artisan`/`bun run` script, a migrate binary), never as an operator-supplied file path. The failure mode this prevents: an operator who cannot find the migrations inside a distroless or minimal image and resorts to piping a specific `.sql` file by absolute path through a one-liner, applying schema partially and outside the migration ledger.

  [references/migration-commands.md](references/migration-commands.md) shows the good and the bad form.
- Annotate, number, and order steps so an operator can follow top-to-bottom on a fresh host.
- No AI slop: no filler or hedging; every sentence informs. Use the `stop-slop` skill on prose when unsure.
- No em-dashes, no double-dashes (`--`) in prose; dashes only as Markdown syntax (list bullets, table rules) or in literal code/CLI flags (e.g. `--no-deps`).
- No emoji. Professional, declarative tone.
- If the document carries a metadata header (`**Version:**`, `**Date:**`, `**Author:**`, `**Status:**`, `**Phase:**`), each such line ends with two trailing spaces so Markdown renders them on separate lines.
- Write to `docs/deployment-plan/`. If the runbook exists, read and update it in place rather than clobbering, and report what changed. If it exists as one older `docs/DEPLOYMENT_PLAN.md`, ask once whether to migrate it (see [references/layout.md](references/layout.md)); if not, update the single file in place.
