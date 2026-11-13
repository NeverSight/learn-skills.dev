---
name: credential-lifecycle-and-rotation
description: >-
  Design, implement, or review credential enrollment, secure custody, renewal,
  refresh rotation, revocation, and consumer adoption for CLIs, workers and
  services. Use when credentials expire, rotation spans a secret store and live
  clients, a renewal response is lost, or recovery could reactivate a revoked
  credential. Prefer documented protocols and existing credential providers.
---

# Credential lifecycle and rotation

Model credentials as authority with a lifecycle, not configuration strings that
can be copied between components. Inspect the identity provider's documented
protocol, repository auth/storage adapters, consumer lifecycle and key custody.
Apply `secrets-safety`; inspect metadata and references instead of revealing values.

## Define identity and authority

Distinguish operator identity, service/worker identity, enrollment proof,
short-lived access authority, renewable credentials, and target-system secrets.
Record audience/origin, principal and tenant scope, allowed actions, expiry,
revocation behavior, storage owner and recovery authority for each.

Do not reuse a human token as a machine identity or use a bootstrap secret for
ordinary requests. If the protocol supports enrollment, make its proof scoped,
expiring and single-use, and consume it atomically with identity creation.
Persist non-secret identity metadata so users do not have to copy secret-bearing
registration output into settings. Use native/OIDC/provider SDK capabilities
instead of inventing an authentication protocol or cryptographic derivation.

## Choose custody explicitly

- Prefer the established OS credential store, service-manager credential
  mechanism, workload identity, or secret manager appropriate to the runtime.
- A headless environment may not have an unlocked desktop keyring. Qualify the
  actual runtime, not merely whether a library is installed.
- If an encrypted-file backend is approved, use a vetted implementation and
  independently supplied unlock material. A key beside the encrypted file is
  not the missing security boundary. Never fall back to plaintext silently.
- Keep the selected backend and reference stable. Backend changes are explicit
  migrations with recovery/cleanup rules, not an automatic fallback on any error.
- Keep credential values out of process arguments, URLs, ordinary config,
  database history, browser bundles, command fingerprints, logs and artifacts.
  Use secure input/reference mechanisms; returns should expose minimal metadata.
- Do not send credentials to another origin through redirects or fallback hosts.
  Bound responses and validate the expected issuer/audience/token purpose.

Server storage requirements depend on the protocol: use non-recoverable
verifiers for opaque bearer credentials when appropriate; securely retain
recoverable upstream credentials only when the application genuinely needs them.
Do not hash a credential that must later be presented to a provider and claim
it can still be used, or store plaintext merely to make retry convenient.

## Renew and reconcile ambiguous outcomes

Treat refresh rotation as a state machine with durable intent, protocol-defined
request identity, outcome and consumer adoption. Concurrent renewals need
coordination; a compare-and-swap revision is not itself replay-safe renewal.

If a response is lost, the provider may already have consumed the old refresh
credential. Follow its documented idempotency, overlap/grace, lookup or recovery
mechanism. Retry an identical operation only when that protocol makes it safe;
do not generate another candidate, blindly reuse a stale refresh, or promise
exactly-once behavior. Where the outcome cannot be reconciled, preserve the
uncertain state and require the supported reauthentication/recovery path.

If recoverable renewal is implemented by a system you own, define and test the
atomic server transition, secure client persistence before/after send, exact
duplicate acknowledgement, stale/different requests, restart recovery and bounded
retention. Do not transplant a private system's token scheme as a general recipe.

## Rotate the whole dependency chain

Map the issuer/data plane, secret store, application metadata and every active
consumer. Separate an administrative rotation receipt from proof that running
clients/pools have adopted the new credential. Qualify replacement, drain,
connection reuse, refresh errors and retired-client cleanup.

Define ordering, concurrency protection, interrupted/unknown outcomes and
reconciliation before executing a cross-system rotation. Preserve version/key
identity needed by already-started operations; do not substitute today's latest
key for an earlier recorded version. A supported overlap window may aid planned
rotation, but availability must not silently preserve authority that an incident
response deliberately revoked.

Rollback to an old credential is allowed only when explicitly safe and approved
for that reason for rotation. Never automatically reactivate a compromised or
revoked credential. If the data plane and metadata disagree, expose degraded/
uncertain state and stop unsafe progression. Do not promise zero downtime
without provider/consumer evidence.

## Qualify with synthetic authority

Test enrollment replay/expiry, separate-principal/audience denial, expiry and
renewal, concurrent rotation, lost response, crash/restart, revocation, storage
unavailability, redirect refusal and real client adoption. Use real local stores
when available and protocol fixtures for external providers; do not read live
credentials, issue real enrollment codes or mutate a shared service for a test.
Separate library/fixture coverage from native keyring and real-provider evidence.

State explicit test oracles, not only failure-mode names: synthetic revoked
credentials must fail new authentication and must never be automatically
restored; test the provider-defined treatment of already-open sessions separately.
The replacement must authenticate through a newly established consumer, and an
interruption between store publication and adoption must remain incomplete until
reconciled. Keep these planned checks separate from claims that they actually ran.

Report the lifecycle, custody choice, protocol recovery guarantees, adoption and
revocation evidence, tests and remaining operational approvals. Use
`runtime-configuration-and-policy` for configuration publication and
`resilient-async-workflows` for delivery; neither substitutes for credential
revocation semantics or authorizes a live rotation.
