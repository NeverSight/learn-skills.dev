---
name: restic
description: >-
  Install, configure, operate, secure, automate, tune, troubleshoot, and recover restic backups across local, SFTP, S3-compatible, cloud, and REST backends. Use when creating or managing a restic repository, designing backup or retention policy, validating restores, handling repository health or locks, moving repositories, or building safe scheduled backup jobs. Do not use for a generic file-copy task that does not need encrypted, deduplicated snapshots.
license: MIT
compatibility: Requires the restic CLI. Live operations also require a reachable repository and its credentials; backend-specific tools or credentials may be required.
metadata:
  source: https://restic.readthedocs.io/en/stable/
  research_checked: "2026-07-15"
---

# Restic

Restic is a backup CLI, not a daemon. Treat a scheduled job or service manager as the execution layer. Every usable backup design proves four things: the source was captured, the repository is readable, retention is intentional, and a restore works in a separate target.

## Operating contract

1. Discover before changing anything: restic version, backend type, repository format, source paths, credentials mechanism, schedule, retention policy, and recovery objective.
2. Keep repository passwords and backend credentials out of command history, logs, templates, and chat. Prefer a root/user-readable password file or a secret manager command over inline values.
3. Before any mutation, confirm target repository, source scope, exclusions, retention groups, schedule, maintenance window, and rollback/recovery path. Read-only discovery may proceed without confirmation.
4. Back up with stable host and tag conventions. Inspect the resulting snapshot, then test a restore into an empty, separate target. A successful backup exit code is not recovery evidence.
5. Treat `forget`, `prune`, `key remove`, `rebuild-index`, `repair`, `migrate`, and backend lifecycle rules as consequential operations. Preview where possible and keep a known-good recovery path.

## First read-only discovery

```sh
scripts/restic-preflight.sh
restic version
restic snapshots --json
restic stats --mode raw-data
```

Set repository location and password source through the environment or command flags before commands that open a repository. Do not export a literal password into a shared shell history. See [repository and backend setup](references/repository-and-backends.md).

## When not to use

Do not load this for a one-time unencrypted file copy, a database backup format that restic cannot create, or provider-specific object-storage administration without a restic repository. Use the relevant application backup procedure for consistency, then use this skill to protect its resulting artifacts.

## Choose the path

| Need | Read first |
|---|---|
| Install or choose a supported binary | [foundations and installation](references/foundations-and-installation.md) |
| Initialize a repository or select local, SFTP, object storage, REST, or rclone backend | [repository and backends](references/repository-and-backends.md) |
| Design sources, excludes, tags, schedules, or service-manager automation | [backup design and automation](references/backup-design-and-automation.md) |
| Write unattended jobs, handle exit codes, parse JSON, or reason about locks | [scripting and command contract](references/scripting-and-command-contract.md) |
| Define retention, run maintenance, verify integrity, or conduct a restore drill | [retention, integrity, and recovery](references/retention-integrity-and-recovery.md) |
| Threat-model secrets, access, ransomware, or credentials | [security and threat model](references/security-and-threat-model.md) |
| Reduce runtime, control bandwidth/cache, or collect useful evidence | [performance and observability](references/performance-and-observability.md) |
| Diagnose failure, locks, corruption, backend errors, or copy/migration work | [troubleshooting and migration](references/troubleshooting-and-migration.md) |
| Check source scope, version currency, or a backend claim | [source index](references/source-index.md) |

## Safe workflow

**Generated data:** Before embedding a database export in a backup job, read
[the scripting and command contract](references/scripting-and-command-contract.md).
`--stdin-from-command` runs exactly one producer command after `--`; an outer
shell pipe is not part of that producer. For compression or transformation, pass
a tested wrapper program as the producer, or use `backup --stdin` only with
`pipefail` and explicit failure handling.

```sh
# 1. Read-only preflight. It never prints secret values.
scripts/restic-preflight.sh

# 2. Initialize only after confirming the intended empty target.
restic init --repo /path/to/repository --password-file /secure/path/restic-password

# 3. Create a tagged snapshot, then inspect it.
restic --repo /path/to/repository --password-file /secure/path/restic-password \
  backup /data --tag production --tag files
restic --repo /path/to/repository --password-file /secure/path/restic-password snapshots

# 4. Restore to an empty, separate directory and inspect the result.
restic --repo /path/to/repository --password-file /secure/path/restic-password \
  restore latest --target /var/tmp/restic-restore-test
```

Use `templates/backup-policy.env.example` to document non-secret policy and `templates/restore-drill.md` to record an evidence-backed recovery test. For Linux scheduling, adapt `templates/systemd/restic-backup.service` and `templates/systemd/restic-backup.timer`; keep secret paths and source paths local, not committed.

## Scripts

- `scripts/restic-preflight.sh` — read-only local configuration and CLI checks; it redacts values and never opens a repository.
- `scripts/restic-verify.sh` — bounded repository verification: metadata check by default, optional sampled or full data reads. It does not alter retention or prune data.
- `scripts/test-restic-preflight.sh` — deterministic shell test using a fake `restic` executable.
- `scripts/test-restic-verify.sh` — deterministic shell test for bounded check-command construction.

Run scripts from the skill root. They require Bash and `restic`; `restic-verify.sh` also requires an already configured repository and password mechanism.

## Hard boundaries

- Never run `prune` in the same unattended window as the only backup job unless its duration and lock impact are understood.
- Never equate `forget` with reclaimed storage. `forget` removes snapshot references; `prune` later removes unreferenced data.
- Never restore over a production source path as a first recovery step. Restore elsewhere, validate, then perform a deliberate cutover.
- Never use `unlock` merely because a backup is blocked. First establish whether another restic process is active and whether the lock is stale.
- Never assume provider immutability, retention, permissions, or object-lock semantics from a generic S3 URL. Verify the specific backend's policy and restore it in a drill.

## Exit criteria

The requested operation is complete only when its relevant boundary is evidenced: installation reports the expected binary; a backup has a listed snapshot; maintenance has a post-operation `check`; and recovery has a restore into a separate target plus an inspection of the restored data.
