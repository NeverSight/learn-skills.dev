---
name: backup-restore-drills
description: >-
  Design, implement, review, or safely test application backup and restoration.
  Use for encrypted archives, database/object consistency, recovery kits,
  disaster-recovery drills, RPO/RTO claims, or checking whether a successful
  backup command really proves recoverability. Separate isolated drills from
  destructive or live restores, which require explicit approval.
---

# Backup and restore drills

A backup is useful only if the intended operator can recover the required state
without damaging the current system. Define what is being recovered and test it;
do not equate an archive upload, process exit code, or database integrity check
with application recovery.

## Define the recovery contract

Read the repository's backup tools, database/storage documentation, data model,
key custody, deployment topology, and runbooks. Confirm the exact scope and
authorization before accessing backups or running tools. For a drill identify:

- authoritative databases, object/filesystem state, configuration and versions;
- consistency boundaries between them and the backup's actual recovery point;
- encryption identities, key availability, restore tool versions and prerequisites;
- required application invariants and the acceptable data-loss/recovery targets;
- isolated destination, resource budget, cleanup ownership, and abort conditions.

An app binary rollback, database restore, and whole-host recovery are different
operations. Do not infer permission for one from another. Backups may contain
credentials and private records even when their filenames look harmless.

## Acquire a consistent, protected recovery set

Use the datastore's supported online snapshot/backup mechanism or an explicitly
approved quiesced backup. Copying only a live database file may miss a journal or
WAL; independent database/object copies may represent incompatible points.
Document snapshot/version pinning or another supported consistency mechanism.

Use established archive/encryption tools and authenticated formats. Keep recovery
keys outside the archive, its storage account, and the source host's sole failure
domain, under the approved custody policy. Do not create custom crypto or put a
key next to ciphertext as a substitute for recovery design. Recovery tooling
must be obtainable after host loss; test its documented version/format support.
Do not invent a requirement for a particular external tool when a reviewed,
supported recovery path already satisfies the contract.

Validate archive completion, identity/manifest, integrity and bounded sizes.
Handle interrupted writes without publishing a partial archive as complete.
Use explicit retention policy; a drill does not authorize deleting old backups.
A same-disk copy alone is not evidence of surviving disk/host loss.

## Restore into an isolated new destination

Prefer local synthetic recovery sets for qualification. Do not download real
customer backups, resolve real keys, or write to a live database merely because
the tools are available. Real-data access and destructive recovery require a
separate reviewed plan and approval of target, data impact and rollback limits.

Create a new private destination and refuse overwrite by default. Bound disk,
CPU, memory, decompression, object counts and wall time to the recovery set.
Treat archive paths, links and metadata as untrusted: prevent traversal and
symlink/hard-link escapes with race-safe extraction appropriate to the tool.
Disable production notifications, schedulers, webhooks and outbound effects in
the recovered app; a successful restore must not send or charge anything.

Run one drill per isolated project/network/path/port set, or serialize runs that
share resources. Record only resources created by the drill; never clean up a
neighboring service to make the test pass.

## Verify state, not just commands

- Fail on database import/script errors even if the wrapper process exits zero;
  inspect the tool's actual error-propagation contract.
- Check database integrity plus expected schema/version, record identities and
  relationships, object references/content fingerprints, and application-level
  invariants. A structurally valid empty database is not the required state.
- Prove decryption using the intended independently available recovery identity.
  Regenerating a lost encryption key does not recover old ciphertext.
- Start the restored application in isolation and exercise bounded critical
  reads/workflows without external effects. Test permissions and secret custody.
- Record precisely when timing starts/ends. RPO follows the newest consistent
  recoverable point; RTO includes the declared recovery journey, not just import.
  Small synthetic results are not a production SLA.

Cover wrong/missing keys, corrupt/truncated archives, incompatible versions,
missing objects, partial writes, insufficient disk, cancellation/crash, repeated
restore, and attempted overwrite. Verify failure leaves the active system intact
and partial destinations clearly unusable. A resumed restore needs its own
supported idempotency/checkpoint contract; do not improvise retry into live data.

Make the no-damage oracle observable in synthetic drills: record a read-only
baseline of protected fixture records/object fingerprints outside the restore
destination, inject the failure, and compare afterward. Specify what must remain
unchanged and how it is checked; an assertion that the active state is unchanged
without a comparison method is not recovery evidence. Do not inspect production
state to add this proof to an otherwise local drill.

## Report proof and gaps

Report the recovery set and consistency mechanism, isolated checks and outcomes,
measured timing/data loss with scale caveats, key/tool availability, failure-mode
coverage, cleanup performed, and untested host/provider scenarios. Redact values,
private identifiers and record contents. State whether recoverability is proven
for the tested scope, partial, or blocked; do not report a drill as a live restore.

Use `secrets-safety` for credential handling, `testing-standard` for local test
boundaries and `vps-deploy-executor` only for a separately approved live release
or restore plan. A runbook is not permission to execute it.
