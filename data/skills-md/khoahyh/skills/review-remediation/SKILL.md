---
name: review-remediation
description: Remediate a frozen set of pull-request feedback with evidence-backed dispositions and minimum durable fixes.
---

# Review Remediation

Consume one frozen set of existing PR feedback, establish the truth of every finding, and remediate confirmed problems. Reviewer identity and delivery surface are metadata; human comments, bot findings, security alerts, review bodies, threads, issue comments, checks, and annotations follow the same workflow.

## Boundaries

- Address only the selected existing feedback. Later feedback belongs to another run; do not request, trigger, or wait for a new review.
- A remediation request includes local investigation, fixes, and verification. External replies, state changes, commits, pushes, and publication require explicit authority.
- Continue authorized fixes through verification and repair of attributable failures. Keep blocked items visible while completing independent work.

Inputs may identify a PR, exact review/comment/check/thread/run IDs or URLs, a reviewer, an expected SHA or time window, or a fixed set supplied by a supervising loop. Detect the PR from the current branch only when it is omitted.

## Freeze The Feedback Set

Identify the PR, provider, branch, and head SHA. Collect concrete claims, questions, and requested changes from every provider surface relevant to the selector.

Selection rules:

- When exact IDs or URLs are supplied, use only those objects and their directly attached findings.
- Apply every supplied reviewer, revision, and time constraint together.
- When only a reviewer is supplied, use that reviewer's currently open feedback.
- When no selector is supplied, use all currently open feedback on the PR, regardless of author or delivery surface.
- Exclude progress notices, eligibility notices, duplicate summaries, and other artifacts without a concrete claim, question, or requested change.

Before editing, record each item's stable ID or URL, author, surface, body, and reviewed SHA or observed timestamp. Do not guess ambiguous attribution: mark separable ambiguous items blocked and continue; ask only when ambiguity prevents freezing the set.

## Establish Each Finding

Compare each claim with the PR goal and current code; reproduce claimed behavior when useful. Treat diagnoses and suggested patches as hypotheses.

Classify every item:

- **Confirmed**: evidence shows a behavior, correctness, security, or maintainability gap requiring a fix.
- **Already addressed**: the current head no longer has the reported gap.
- **Question or informational**: requires an answer or acknowledgement, not code.
- **Rejected with evidence**: the claim does not apply, conflicts with requirements, or would make the system worse.
- **Blocked**: remediation needs product intent, credentials, infrastructure, or another user decision.

Use repository code, tests, requirements, and runtime evidence directly when they settle the claim. Consult current, version-matched primary sources when correctness hinges on external library, platform, protocol, or security behavior, or when direct evidence remains uncertain. Reviewer links are leads, not proof; external guidance does not override repository requirements or the installed version.

## Apply Minimum Durable Remediation

For each confirmed item, make the smallest semantic change that fixes the root cause:

- Put the invariant at the boundary that owns it rather than compensating at a caller or symptom site.
- Use documented public APIs and the repository's established architecture.
- Preserve unrelated behavior and avoid opportunistic refactors.
- Add a regression test at the lowest stable public boundary when the finding exposes a reproducible behavior gap.
- Cover only evidenced boundary, failure, concurrency, and security cases; prefer deleting a faulty path over adding parallel machinery.

Leave an item blocked rather than landing an unsupported workaround.

## Verify And Close

Run each focused reproduction or regression test, then only the broader format, lint, typecheck, test, build, or security checks warranted by the change's risk and repository conventions. Inspect the final diff against the PR goal and frozen set.

When provider access is available, re-fetch selected items by stable ID before closing. Each response gives the disposition and evidence: the root-cause fix and verification, conflicting evidence for a rejection, a direct answer, or the blocker and what would resolve it.

When explicitly authorized, send replies through the provider's native thread and update addressed/resolved state. Otherwise prepare the exact responses inline and finish all authorized local work.

Done when every frozen item is accounted for, all risk-matched verification passes or has a reported blocker, and authorized replies or prepared responses are complete. Report the PR and head SHA, item count and dispositions, fixes, external sources used where applicable, verification, external actions, and unresolved items.
