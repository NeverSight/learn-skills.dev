---
name: vps-blue-green-prepare
description: >-
  Design and prepare repeatable blue-green deployments for applications hosted
  on a VPS. Use when a user wants to deploy to a VPS with less downtime, create
  or improve a deployment script, or document a VPS release and rollback process.
  Inspect the repository and choose a runtime strategy that fits it (such as a
  Go binary managed by systemd or Docker Compose); ask when deployment facts are
  missing or consequential. Produce project-specific deployment artifacts but
  do not connect to or deploy on the VPS.
---

# Prepare a blue-green VPS deployment

Design a repeatable, project-specific deployment that keeps the current version
serving traffic until a replacement has started and passed verification. Blue-
green reduces application downtime, but does not by itself guarantee zero
downtime: database changes, singleton work, shared state, and infrastructure
limits can still require coordination or a maintenance window.

Read and apply [`task-completion`](../task-completion/SKILL.md) using the skill
loader or sibling file; report if unavailable. Complete and validate the
requested preparation artifacts. A verified preparation task can be complete
without a live deployment: list operator prerequisites separately, and do not
connect to a host or deploy merely to eliminate a preparation-only next step.

## Establish the project and deployment model

1. Inspect the repository, build/test commands, runtime entrypoint, existing
   deployment scripts, service definitions, proxy configuration, health checks,
   migrations, and documentation. Preserve established conventions and local
   changes.
2. Determine whether the project is a binary/service, containerized application,
   or another runtime. Prefer the existing deployment model when it is safe.
   For example, a Go binary may use two systemd-managed slots behind an existing
   reverse proxy; Docker Compose may use two app services or release projects.
   Do not require Docker when the project does not use it.
3. Do not infer topology from a project name. Confirm whether the application
   owns or modifies Nginx, binds fixed ports, must be a singleton, schedules
   exclusive jobs, writes local files, or shares resources with other apps.
4. Ask focused questions when a consequential fact cannot be established from
   the repository or user-provided context: target host/environment, deployment
   path, proxy/traffic switch, health-check URL, service ownership, state and
   database migration behavior, or artifact delivery. State safe assumptions
   explicitly; do not invent production paths, domains, ports, or credentials.
5. Explain the selected strategy and any remaining downtime or rollback limits
   before generating production-affecting configuration.

## Design the release lifecycle

Use the existing VPS topology and make the release lifecycle explicit:

1. Validate inputs and prerequisites; build or obtain an immutable release
   artifact and identify its version/checksum.
2. Acquire a deployment lock so overlapping runs cannot race.
3. Prepare the inactive slot without stopping or overwriting the active release.
   Keep user data, uploads, and mutable state outside disposable release
   directories.
4. Start the inactive slot and wait for a bounded readiness/health check. A
   failed check must leave traffic on the active slot and report useful,
   redacted diagnostics.
5. Validate the traffic-switch configuration before applying it. Use the
   project's actual proxy/service mechanism; for Nginx, validate configuration
   before a graceful reload. Do not replace an entire shared proxy config when
   a scoped upstream or include is sufficient.
6. Verify the new version through the real traffic path. If verification fails,
   switch traffic back to the previous healthy slot and verify rollback.
7. Keep the previous release available for rollback. Make cleanup a separate,
   documented operation; never delete releases, data, backups, or unrelated
   services as an implicit part of deploy.

Treat database migrations separately from traffic switching. Prefer
backward-compatible expand/migrate/contract changes so old and new application
versions can coexist. If that is not possible, state the required maintenance
window and recovery plan; do not claim an application rollback also reverses
data changes.

## Create project-specific artifacts

When asked to prepare the deployment, create or update the smallest appropriate
set of project files:

- A repeatable deployment script following the repository's language and
  conventions. If shell is appropriate, use strict error handling, validated
  arguments, safe quoting, bounded waits, a lock, cleanup/trap behavior, clear
  logs, and a dry-run/preflight mode where practical. Never embed credentials.
- Any narrowly scoped service/proxy/config templates actually required by the
  selected strategy. Preserve existing files and avoid changing unrelated
  services.
- `DEPLOY.md` (or the repository's existing deployment-doc location) with
  prerequisites, initial VPS setup, configuration, first deploy, subsequent
  deploys, health verification, rollback, troubleshooting, and safe cleanup.
- Tests or validation for script behavior when feasible, including a failed
  health check that proves traffic remains on or returns to the previous slot.

Do not execute remote commands or deploy as part of preparation. Do not claim
that the generated artifacts are production-ready until their assumptions,
syntax, and available tests have been checked. Summarize changed files, required
operator-supplied configuration, checks run, and unresolved risks.

## Review checklist

- Does the strategy match the repository's runtime and actual VPS topology?
- Can the new slot be started and checked without interrupting the old one?
- Is the traffic switch validated, scoped, reversible, and followed by a
  real-path health check?
- Are concurrent deploys prevented and failures handled without losing the
  previous release?
- Are database compatibility, local/shared state, singleton work, disk space,
  and resource constraints addressed?
- Are secrets absent from code, script arguments, docs, and logs?
- Are rollback and cleanup separate, documented, and honest about data changes?
