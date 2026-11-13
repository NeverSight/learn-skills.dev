---
name: actions-billing-local-validation
description: >-
  Complete equivalent local checks when GitHub Actions cannot run because of
  confirmed billing, spending limits, or quota. Use to diagnose billing-blocked
  PR checks, avoid futile reruns, and produce SHA-bound local validation evidence
  without pretending remote CI passed or bypassing branch protection.
---

# Billing-blocked CI: verify locally

An explicit billing/spending-limit rejection is not a code failure. Do not
create empty commits, toggle draft state, or close/reopen PRs repeatedly to
retry a condition those operations cannot fix.

## Establish the cause and equivalent checks

1. Inspect the execution's message or annotation safely. `startup_failure`
   alone does not establish billing; configuration, runner, and transient errors
   require their own diagnosis.
2. Record the reason, repository, head SHA, and current base SHA.
3. Read applicable workflows, composite actions, scripts, matrices, repository
   instructions, and required-check policy. Map each check to its local command.
   A convenient test target may cover only part of the workflow.

## Finish local verification

- Run all reproducible build, format, lint, type, unit, integration, security,
  generation, and other required checks for each touched repository.
- Match relevant toolchain versions, features, and test matrices. Use local/test
  credentials and real local dependencies where supplied; follow `testing-standard`.
- Fix failures and revalidate. Rebase, conflict resolution, and later edits
  invalidate evidence tied to the previous head.
- Mark unavailable platforms/services/checks as unverified. Never silently
  substitute a smaller matrix or claim an unavailable check passed.
- Deployment and publication are not local tests and require separate authority.

## Distinguish technical verification from merge permission

Where the user or repository authorizes local substitution for confirmed billing
failures, complete that validation without repeatedly asking to ignore the same
billing condition. Else report local evidence separately from the unsatisfied CI
policy. A generic skill cannot waive a repository's required checks.

Keep merge authorization and platform protections intact. If protection requires
remote success, report the merge blocker; do not disable checks, fabricate green
statuses, or use an administrative bypass without specific authorization.
Real test failures never qualify for the billing exception.

Report a check → command → result table, tested SHA, matrix coverage, and any
unreproduced checks. Say “local validation passed; Actions blocked by billing,”
not “CI passed.”
