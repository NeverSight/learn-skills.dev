---
name: insert-only-predeploy-import
description: >-
  Prepare repeatable legacy-data imports and pre-deploy hooks that preserve
  existing operational records. Use for object-storage-to-database imports,
  retryable migration commands, conflict policies, and deployment-blocking
  import verification without executing unauthorized remote operations.
---

# Import without replacing operational data

Inspect the requested source, destination, record identities, associated data,
and conflict policy. When preservation is required, destination records win;
an upsert that updates their content or metadata violates that contract.

## Implement a repeatable operation

- Use atomic conditional insertion with appropriate keys/constraints. Checking
  for existence before inserting is not sufficient concurrency protection.
- Include related records and preserve referential integrity; importing only
  the primary object may leave the workflow unusable.
- Make reruns after partial progress safe. State whether the import is globally
  transactional or incremental; do not promise rollback it cannot provide.
- Report imported/existing/error counts without sensitive record contents.
- If the destination becomes authoritative, do not add a hidden live-source
  fallback for ordinary requests.

## Wire deployment without performing it

Inspect the platform config and produced executable path before connecting a
pre-deploy command. Failure must propagate a nonzero status and block the new
version, rather than become a warning followed by startup.

Use the same approved configuration sources for server and importer; follow
`vault-bootstrap-configuration` where appropriate. Inspect backend-specific
options instead of copying one provider's region or endpoint to all providers.
Use the repository's migration generator when required.

Editing a hook does not authorize remote imports, provisioning, push, deployment,
or deletion. Respect an explicitly local-only verification boundary.

## Verify

Use real local database and compatible object-storage services to test an empty
destination, different existing content, associated records, repeated execution,
failure and resumption, and applicable concurrency. Read destination state back
to prove old records remained unchanged. Follow `testing-standard` and report
implementation separately from any actually executed remote import or deploy.
