---
name: shukka
description: "Prepare software for responsible release, migration, deployment, rollback, and handoff with evidence about compatibility, health, ownership, and recovery."
---

# Shukka

Shukka means shipping or dispatching a finished thing. In software, release is
part of the product: move verified behavior into use with operational
discipline, clear ownership, and a recovery path. This is a Japanese-inspired
engineering metaphor, not a rule that every change needs a ceremony.

## Use this skill when

- preparing a release, deployment, migration, or handoff;
- changing configuration, infrastructure, schemas, or public contracts;
- deciding whether a feature is ready for users;
- staging a high-risk or irreversible change; or
- defining what must be observed after release.

## Outcome

Produce a release decision and handoff containing:

- exact scope and version or revision;
- compatibility and migration considerations;
- required configuration, secrets, permissions, and owners;
- checks run and their results;
- health, observability, and success signals;
- rollout, rollback, and recovery paths;
- user or operator communication; and
- residual risk and explicit release blockers.

## Workflow

### 1. Define the release boundary

Identify what changes, who is affected, what must remain compatible, and which
data or external state can be changed. Separate reversible from irreversible
steps.

### 2. Verify the artifact

Check the relevant tests, type checks, builds, migrations, contracts, security
checks, smoke checks, and operational prerequisites. Do not use “merged” or
“compiles” as a release decision.

### 3. Prepare safe movement

Choose a staged rollout, feature flag, backup, transaction, maintenance window,
or rollback mechanism when risk justifies it. Confirm that rollback is real,
tested enough to trust, and does not destroy newer data.

### 4. Prepare observation and ownership

Name the signals that indicate success, degradation, and recovery. Identify who
responds, how to find diagnostics, and when to stop or reverse the rollout.

### 5. Communicate the handoff

State what changed, how to use it, how to operate it, known limitations, and
what to do if it fails. Keep the message useful to the next person, not merely
ceremonial.

### 6. Verify after movement

Run smoke or health checks and inspect real signals after release. Record the
result and any follow-up. If a meaningful check fails, use `jidoka` and do not
hide the failure behind a successful deployment status.

## Evidence standard

Every release claim must name the check, environment, revision, and result
when that information matters. If rollback, recovery, or production behavior
was not verified, state the limitation explicitly.

## Boundaries

- Do not deploy or mutate external systems without the user's authorization.
- Do not treat a checklist as evidence when the underlying check did not run.
- Do not add release complexity without a risk or recovery need.
- Do not call a migration safe without considering partial failure and rollback.
- Do not hand off undocumented operational responsibility.

## Handoff

End with a release decision: ready, blocked, or ready with explicitly accepted
risk. Link the evidence, owners, recovery path, and next reflection. Use
`andon` for missing signals, `jidoka` for failed checks, and `hansei` after the
release to preserve lessons.

If a referenced skill is not installed, apply its named lens inline instead of
trying to invoke it.
