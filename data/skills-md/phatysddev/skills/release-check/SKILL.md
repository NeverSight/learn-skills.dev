---
name: release-check
description: "Assess a named release candidate and target environment using existing build, verification, configuration, migration, and rollback evidence. Use when preparing a release or explicitly checking deployment readiness; does not deploy or add a mandatory post-review stage."
---

# Release Check

Produce a bounded readiness assessment for a release candidate. Do not deploy,
publish, push, tag, create a release, change configuration, run migrations, or
modify infrastructure. Readiness is tied to a candidate and environment, not a
general claim that the whole repository is production-ready.

## Identify the candidate

Read repository guidance, the requested release scope, candidate commit/artifact
or working-tree state, target environment, relevant requirements/specs/tasks,
verification policy, existing CI/build evidence, and release/runbook conventions.
Preserve unrelated work. Do not switch branches or clean the tree for inspection.

If the candidate, scope, or environment is unspecified, inspect what is available
and request only material missing information. Continue independent checks but
report the assessment as incomplete until a meaningful target is established.
A local dirty-tree assessment does not prove that a built/deployed artifact
contains those changes. Do not label it ready for a clean commit artifact.

## Check applicable release requirements

Use a compact evidence table. Include a category only when the release or its
existing policy makes it relevant:

- scope and approvals: intended included changes, unfinished work, and required
  task review/verification evidence;
- build/package: repository-supported build result and its relation to the exact
  artifact, runtime, dependency resolution, and target;
- configuration: required variable names, environment wiring, and safe evidence
  of provisioning; a template's presence is not proof a target is configured;
- data/contracts: changed schemas, migration order, compatibility between old and
  new versions, and rollback limitations for this change;
- operations: the existing deployment path, health/smoke checks, rollback or
  recovery procedure, and their applicability to the candidate.

Distinguish a demonstrated failure, missing required evidence, and a non-blocking
observation. Do not demand Docker, a database, CI, a monitoring platform, or a
particular hosting provider when the project does not require them. Do not turn
this assessment into an unsolicited infrastructure backlog.

## Evidence and execution boundaries

Inspect local configuration structure and safe templates; report variable names
or missing requirements only. Do not open live secret files, print environment
values, or request credentials in chat. Target provisioning can remain unknown.
Reuse credible existing reports, checking candidate/environment applicability;
a task's `done` status alone does not demonstrate build or release readiness.

Run existing bounded local build/check commands only after inspecting their
scripts for external or destructive side effects. Allow ordinary disposable
outputs, not source/configuration edits. Do not install missing tools, provision
services, call live endpoints, run deploy hooks, or execute data migrations for
this assessment. A failed or unavailable check stays failed/unverified; report
the prerequisite and stop rerunning it without new evidence.

Respect effective verification/review policy without changing it. Do not invoke
all task test skills or add another final review. Reuse `$verify-feature` reports
when available, but their absence alone is not a blocker or a mandatory handoff.
If a genuine cross-task acceptance gap prevents release assessment, recommend
one scoped `$verify-feature` check. A known implementation defect goes directly
to its owning `$implement-task`, or `$debug-task` when the cause is unclear.

## Readiness report

Use one verdict:

- `ready`: all applicable release requirements are evidenced for the identified
  candidate and target, with no unresolved blockers;
- `blocked`: a known failed requirement or missing required prerequisite prevents
  release; specify evidence, owner/action, and the exact unblock condition;
- `incomplete`: target, artifact identity, access, or verification evidence is
  insufficient to decide, without asserting a failure that was not observed.

If failure and uncertainty coexist, report `blocked` and list the uncertainties.
State scope/candidate/environment, checks and provenance, blocking issues,
non-blocking observations, and what was not verified. An `off` check is not a
pass; an explicit policy exemption is distinct from an unknown result. Explain
any documented exemption without inventing one to obtain `ready`.

Do not update task/spec status or mark a deployment complete. If ready, finish
with the existing release procedure reference, if known; execution remains a
separate user-directed action. If not ready, provide one primary remedy or owning
workflow, not a chain of mandatory skills. `$change-scope` applies only when the
user intends to change the release's agreed behavior, not to waive a failed gate.
Return the report in the response unless saving it was requested. A repeated
check should focus on changed evidence and previously unresolved requirements.
