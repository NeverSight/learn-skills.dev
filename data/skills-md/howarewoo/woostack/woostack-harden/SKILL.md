---
name: woostack-harden
description: Public standalone read-only review of a supplied specification or candidate issue plan against bounded repository evidence; reports discrepancies and unresolved decisions without synthesizing approval.
---

# woostack-harden

`woostack-harden` is a requested read-only review of a supplied specification or candidate issue
plan. It is standalone: nothing invokes it by default, and it never publishes issues, edits source,
dispatches another phase, or writes repository or GitHub state.

## Command and input

```text
/woostack-harden <specification-or-issue-plan>
```

The user supplies the content to review and the repository it targets. Resolve the canonical
repository and its immutable baseline from the explicitly selected or unambiguous checkout, and
name the evidence you actually read. Ask only when the target or the reviewed content is ambiguous
or inaccessible; never substitute a repository found by title, branch, or recent activity. Retained
historical content is evidence until its identity and freshness are revalidated. An exact GitHub
issue or pull request may be read as evidence when the user explicitly selects it and the
authorized host capability can read and verify it completely; a GitHub Project configuration is
never required.

## Reconciliation invariant

Repository evidence can expose a question; it cannot answer a user-owned decision. Verified
schemas, routes, migrations, existing conventions, and dependency versions are observations to
report, not questions to ask. Harden never changes scope, behavior, architecture, compatibility,
security boundaries, acceptance, verification, or plan dependencies on its own.

Check the removal-first question: whether safe deletion, reuse, or simplification satisfies the
supplied contract before accepting additive work. Report the cheaper option as a recommendation, and
keep required safety and compatibility protections.

Then reconcile the content against bounded evidence. Compare claimed storage and interface facts
with actual schemas, migrations, routes, and data-layer code. For a candidate issue plan, compare
each task's outcome, scope, non-goals, affected paths, acceptance, and checks with the specification
and the repository, and declared prerequisites with real dependency edges. Report what matches,
what conflicts, and what the repository shows that the content never mentions. Never invent an issue
endpoint, parent, prerequisite, or publication identity.

## Discrepancies

Report every material discrepancy together instead of one at a time. Each carries the exact content
affected, the observed fact separated from its interpretation, the recommended correction, and the
consequence of leaving it. Where the correction is a routine technical detail consistent with the
requested outcome, propose it and keep going; where it changes product behavior, compatibility,
security or data boundaries, irreversible effects, cost, or scope, leave it to the user. A choice to
keep an inconsistency is itself a user decision. Never speculate about an unobserved check or report
a command as passing because it appears in the content.

## Read-only boundary

Harden performs no GitHub or remote writes, issue creation, source edit, implementation-worker
dispatch, commit, branch, worktree, PR, or execution action. It only reads. It creates no manifest,
ledger, mirror, or hidden record, and it never invokes another phase. A user may explicitly save
the review, but saving it is not approval or authority.

## Return

Return a focused, readable review rather than a fixed envelope: an overall verdict, each material
discrepancy with its evidence and recommended correction, the unresolved decisions that need the
user, and the read-back limits or unavailable evidence that bound the review. Preserve the user's
content and decisions; the user decides what to change and what happens next.
