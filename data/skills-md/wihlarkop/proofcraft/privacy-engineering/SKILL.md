---
name: privacy-engineering
description: >-
  Translate privacy requirements into engineering behavior across data purpose, minimization,
  access, retention, deletion, consent, residency, derived data, telemetry, and AI traces. Use
  when a feature collects or processes personal/sensitive data or must prove lifecycle behavior.
  Keep legal interpretation outside this skill; privacy owns what data should exist and for how
  long, while security owns protection mechanisms.
license: MIT
compatibility: Portable Agent Skills methodology; no runtime dependency.
metadata:
  suite: proofcraft
  suite-version: "0.1.0"
  skill-version: "0.1.1"
---


# Privacy Engineering

Engineer the full data lifecycle from purpose through deletion.

## Workflow

1. State the declared purpose for each material data category and reject speculative collection that has no concrete use.
2. Classify data sensitivity and map collection, processing, storage, access, sharing, derived copies, logs/telemetry, backups, and deletion.
3. Define minimization: collect only what the product requirement actually needs.
4. Define retention trigger and duration from accepted product/legal policy; do not invent jurisdiction-specific legal requirements. If the policy is genuinely undecided, preserve it as a human decision rather than substituting a default.
5. Define consent/revocation behavior where applicable, including how system behavior changes after revocation. Do not infer notice, opt-out, deletion-right, or revocation promises that the product/legal policy has not established.
6. Define deletion propagation across primary stores, replicas, caches, exports, traces, and derived datasets as required by the accepted policy.
7. Report unresolved lifecycle policy to the active core workflow owner as an explicit gate. Distinguish architecture readiness from implementation-contract readiness: a provider-neutral boundary can be architecturally settled while a complete executable plan remains blocked if retention, deletion, consent/revocation, residency, or user-rights decisions materially change the data model, API, UI, or lifecycle.
8. Convert settled privacy requirements into observable acceptance criteria and verify deletion/retention behavior rather than trusting documentation alone.
9. Route encryption/authz/secrets implementation to security-engineering and storage mechanics to database/platform specialists.

## Readiness

Privacy work is not complete merely because collection purpose and minimization are clear. When a missing human policy is material to implementation, the owning core workflow may continue shaping or settle independent architecture, but it must not present the full implementation contract as ready or silently plan around placeholder privacy defaults.

## Stop

Stop when relevant personal/sensitive data has a clear purpose and all material lifecycle decisions needed for the current stage are either settled or explicitly reported as blocking gates. For implementation planning/readiness, retention/deletion behavior and other material privacy policy must be concrete enough that a fresh agent can implement without inventing product or legal policy.
## Reference Guide

Load only the references needed for the current task:

- [data lifecycle](references/data-lifecycle.md)
- [deletion verification](references/deletion-verification.md)
- [telemetry ai traces](references/telemetry-ai-traces.md)
- [principles](references/_shared/constitution/principles.md)
- [decision lock](references/_shared/constitution/decision-lock.md)
- [concerns](references/_shared/orchestration/concerns.md)
- [authority](references/_shared/state/authority.md)
- [cache](references/_shared/state/cache.md)
- [evidence](references/_shared/verification/evidence.md)
- [risk depth](references/_shared/verification/risk-depth.md)
