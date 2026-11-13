---
name: acceptance-traceability
description: >-
  Turn a request, issue, or specification into observable acceptance criteria
  and trace each criterion to implementation and verification evidence. Use
  when planning a delivery, checking whether a feature satisfies the request,
  reviewing scope changes, or preparing an evidence-backed delivery report.
  Distinguish implemented, verified, blocked, and excluded work; green builds
  alone do not prove acceptance. Do not invent product decisions or approval.
---

# Acceptance traceability

Make the gap between “the code changed” and “the requested outcome works” visible.
Maintain a small acceptance map, not a second test policy or task tracker.

## Establish the contract

Read the latest user request, applicable instructions, issue/specification,
existing acceptance criteria, relevant implementation, and documented tests.
Use the user's current scope as authority; a historical plan is only evidence.

Extract outcomes, constraints, exclusions, failure behavior, and integrations.
Give each distinct requirement a stable identifier (for example, AC-01), its
source, and an observable result. Split compound statements when they can pass
independently. Keep explicit requirements separate from suggested improvements.
Do not infer payments, notifications, production access, new UX rules, or product
semantics from an implementation detail. Surface consequential ambiguity before
building or marking the outcome accepted. Record unresolved criteria as pending.

Prefer the existing issue/spec/report location. If none exists, use a concise
chat map for a small task or include it in the approved per-task progress record
for multi-step work. Do not create a competing permanent acceptance document by
default. Use [references/acceptance-map.md](references/acceptance-map.md) as a
compact template; adapt it to the project's convention.

## Map proof before implementation

For each criterion, identify:

- the user-observable outcome and preconditions;
- implementation entry points and affected layers, when known;
- a meaningful test/check and the expected result;
- the evidence to retain, including relevant side effects;
- setup, permissions, or dependencies that might block verification.

Plan negative/authorization/empty/error cases when the request or changed
boundary warrants them. Do not invent an entire edge-case product contract.
Missing test coverage is a gap, not automatically a new user requirement.

Delegate test boundaries and full quality gates to `testing-standard`; inspect
the repository's commands instead of assuming a stack. Use a project verifier
authored with `create-verification-skill` for real user journeys. A screenshot
may prove visible state, not persisted data, emitted messages, or a valid export.
Inspect those effects too when the criterion requires them. Do not substitute
mocked success, directly seeded outcomes, or test-only shortcuts for the actual
journey. Use safe synthetic/local resources; ask at external-action boundaries.

## Keep scope and evidence current

Update the same map when the user changes scope, an outcome is implemented,
verification runs, a defect is found, or a blocker changes. Keep stable IDs for
unchanged requirements. Mark removed requirements excluded/superseded with the
current source; do not count them as verified or leave them as active obligations.
Do not quietly weaken a failed criterion to match existing behavior.

Record implementation separately from verification. Suggested states are:

- **pending:** not yet established or implemented;
- **implemented / unverified:** code exists, but suitable proof is absent;
- **verified:** the exact criterion has current, direct evidence;
- **failed:** an executed check contradicts the expected result;
- **blocked:** a concrete dependency prevents the necessary check;
- **excluded:** explicitly removed or out of scope, with provenance.

For an executed check record the command/workflow, result, artifact pointer, and
relevant revision/worktree or changed-file snapshot. Test names and file paths
alone are not execution evidence. After relevant changes, mark old proof stale
until rerun or explain precisely why it still applies. Do not reuse a prior
commit's green CI run as proof of an untested dirty checkout. Capture limitations
without exposing secrets, customer data, or sensitive logs.

## Close with evidence, not a score

Compare every active criterion against the latest request and actual artifacts.
Report verified criteria, failures/blockers/unverified work, exclusions, and
remaining required actions. Never call the delivery complete just because all
files exist, the build is green, or most rows pass. A technical gate can pass
while an acceptance criterion fails, and vice versa; report both.

Use `task-completion` for execution and honest delivery state, and
`document-decisions` for substantive rationale. Save the final acceptance result
in the existing issue/delivery documentation before an approved task-progress
record is removed; do not lose proof with the scratch file. Link retained
artifacts and state if they are local-only, expired, or inaccessible to reviewers.

This skill does not grant product acceptance, authorize commits/deployments,
enforce automatic skill activation, or prove that untested journeys work.
