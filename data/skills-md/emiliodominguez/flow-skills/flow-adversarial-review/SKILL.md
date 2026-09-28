---
name: flow-adversarial-review
description: "Security and abuse review that traces attacker input to reachable impact. Use when a change touches auth, untrusted input, secrets, permissions or isolation, or a security review is requested. Hands off to `flow-work` or `flow-review`."
metadata:
  stage: verify
---

# Adversarial review

Try to disprove the system's important invariants with concrete inputs and state. Findings
need a reachable path or an explicit evidence gap; a clean report is allowed.

## Phase 1: Bound the target

Review the named target (diff, change request, branch or paths); a fresh reviewer context may lack the
conversation. If none is given, state the target inferred from the working tree, or ask when
inference is unsafe.

- Read scope, repository instructions, architecture and diff; inspect committed, staged,
  unstaged and relevant untracked changes separately. Record revision, test environment and
  intended invariants.
- Map the attack surface: entry points, untrusted data, transformations, authorization
  decisions, sinks, persistence, and who controls each input.
- Reproduce only in local fixtures or an authorized environment, never with destructive
  traffic against a live system.

## Phase 2: Pick lenses for actual risks

- **Exploit developer:** input reaches an unsafe interpreter, file path, renderer or command.
- **Boundary breaker:** one actor reaches another actor's resource or crosses an isolation rule.
- **Data-integrity auditor:** concurrent writes, retries or partial failure violate invariants.
- **Chaos engineer:** lost connections, unavailable dependencies or interruption break recovery.
- **Malicious user:** legal UI/API operations combine into an unauthorized result.
- **Time bomb:** expiry, growth, resource limits or stale state change behavior over time.

Split surfaces across independent read-only agents only when available, authorized and useful,
with a shared findings schema. A persona label grants neither independence nor permissions.

## Phase 3: Trace and challenge

For each candidate record location/revision, preconditions, attacker-controlled input, exact
sequence, affected invariant, impact and smallest correction. Follow the path through guards
and caller contracts; a suspicious function name is not a finding. Reproduce safely when
possible. Have an independent verifier challenge consequential or disputed claims:

- CONFIRMED: impact reproduced or the reachable path demonstrated.
- PLAUSIBLE: a specific path argued, required evidence missing; name the gap.
- REFUTED: a concrete control or reproduction makes the scenario impossible.

Keep severity separate from confidence. Keep useful plausible risks, drop refuted ones. Type
assertions, comments or worker reports do not establish runtime trust for network, storage,
DOM or external input.

## Phase 4: Report

Deduplicate by failure path. Lead with confirmed findings, then material unresolved risks and
unchecked scope, each with evidence and remediation direction. State residual risk from actual
coverage limits. Review-only work stops at findings; never quietly repair an artifact you are
verifying. Requested fixes stay in scope and are rechecked on the new revision.

## Anti-patterns

- Generic vulnerability lists without an input-to-impact trace.
- Calling a missing reproduction REFUTED, or a suspicion CONFIRMED.
- A full red-team panel for every filesystem or input-handling edit.
- Inventing a vulnerability to fill a section, or calling a system secure because a scoped
  review found nothing.

## Done when

- Relevant invariants and boundaries are assessed at the recorded revision.
- Findings separate reproduced impact, unresolved evidence and disproven paths.
- Residual risk and coverage limits are stated without padding or implied certification.

Return the findings; use `flow-work` for fixes only when authorized, or `flow-review` for wider
code-quality review.
