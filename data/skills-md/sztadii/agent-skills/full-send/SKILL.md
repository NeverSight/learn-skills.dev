---
name: full-send
description: "Trigger only when the user or another skill explicitly invokes this skill."
---

# Full Send

Run only when the user explicitly invokes `$full-send` (Codex) or
`/full-send` (Claude Code), or another skill explicitly instructs you to invoke
this skill.
Mentions, examples and matching tasks alone do not trigger this workflow.

## Required skill check — first action

Required skills: [$proof](../proof/SKILL.md), [$council](../council/SKILL.md),
[$file-pr](../file-pr/SKILL.md), [$babysit-pr](../babysit-pr/SKILL.md),
[$leaving-pr-comments](../leaving-pr-comments/SKILL.md) and
[$simplify](../simplify/SKILL.md) through council.

At entry, check once through the host's skill discovery that the skills listed
above are installed and their `SKILL.md` files are readable. If any are unavailable,
stop the entire workflow, including the caller, and tell the user which are
missing. Do not skip, substitute or auto-install them. After this check succeeds,
proceed with the workflow below without repeating the availability check.

## Purpose and scope

Own delivery from the initial request to the requested endpoint. Invocation
includes implementation, local setup and verification, independent agent review,
task commits and pushes, PR publication through file-pr, feedback replies and
in-scope CI/conflict fixes. Default delivery is a verified PR with available
current-head checks and reviews settled and actionable feedback addressed. If the
initial request includes merging or deployment, continue through that endpoint
under repository policy; never infer production deployment from “full-send”.

Honor narrower instructions such as “do not push”. Do not ask for
routine phase approvals, approval of a prepared PR, selection of individual
comments or permission already given. Make reversible implementation choices
from the request and repository conventions. Escalate only an unresolved product
choice, missing access or action outside the authorized scope that actually blocks
progress; complete independent work first and explain the exact blocker.

## Deliver

1. **Establish the contract.** Read initial context and repository instructions,
   inspect existing work and infer acceptance criteria, actual base and destination.
   Record scope, completion condition and available verification. Reuse a matching
   task branch/PR and preserve unrelated changes. Do not require a ticket, update
   an issue tracker or ask the user to supply facts available in the repository.
2. **Implement.** Make the complete in-scope change, including meaningful regression
   coverage and required documentation. Resolve integration issues, inspect the
   diff and simplify worthwhile complexity while preserving behavior. Take a fresh
   look at the complete task diff for human readability; prefer a smaller coherent
   change when code quality and useful coverage are preserved. Keep tests
   proportional to risk, avoiding redundant cases and unnecessary scaffolding.
   Council owns the simplify pass before its reviewers start; do not invoke
   simplify separately in implementation or after each repair.
   Do not turn cleanup into a separate redesign.
3. **Verify.** Invoke **$proof** to run required repository checks and exercise the
   acceptance criteria.
   Inspect evidence suited to the behavior. Diagnose failures and fix their causes;
   a mock or screenshot proves only what it exercises. A missing optional artifact
   is not a blocker if adequate evidence exists. Full-send owns product-code fixes;
   proof reports failures, then reruns affected verification after repairs.
4. **Review and repair.** Invoke **$council** to obtain two independent reviews with
   inherited settings by default, following host delegation rules and any
   user-selected reviewers.
   Council must invoke **$simplify** once before freezing the snapshot and starting
   its reviewers. Pass the local task diff so preparation edits become part of
   the delivered change. Keep the prepared snapshot stable and forbid reviewer
   edits or further delegation. Validate findings, fix substantiated in-scope issues and refresh
   affected checks and review after substantive edits. Refresh affected **$proof**
   checks after council's preparation so final evidence covers the reviewed code.
   Cosmetic changes do not restart the whole process. Stop repeating unsuccessful rounds when no new
   evidence or progress is possible; report the remaining issue honestly.
5. **Publish.** Invoke **$file-pr** with the prepared task changes, matching PR URL
   when present, user constraints, current verification, review findings and
   useful evidence. File-pr owns commits, pushes, PR creation or updates and
   publication policy. Use its verified result.
   Do not duplicate or override its publication rules. Report delivery as incomplete
   when required verification or review has gaps, or publication returns a blocker.
6. **Maintain to the endpoint.** Invoke **$babysit-pr** with the existing PR and any
   prepared unpublished task changes; it prepares and verifies fixes, then uses
   file-pr for publication. It also handles current-head CI failures, valid review feedback
   and necessary base updates/conflicts. Verify
   fixes before pushing, reply with evidence and refresh invalidated review. Do not rewrite a shared
   branch without authority; an authorized rewrite uses a lease. Pass the user's
   requested endpoint and explicit permissions to babysit-pr. Wait for required checks/reviews using the
   host's event watcher, not polling. Resume until the completion condition is met.
   Babysit-pr invokes **$leaving-pr-comments** for comments and replies during
   maintenance, using verified findings and evidence without starting another review.
   If merging was requested, respect protection and verify the expected head and
   actual merge. If deployment was requested, verify the specified environment.

## Continuation

Pass scope, authorization, exact revision, evidence and endpoint to each skill;
a phase's completion is not completion of the whole delivery. Full-review remains
a separate review workflow.

Keep a compact continuation record in the host's task state: acceptance criteria,
branch/base/head, local diff, PR URL, checks/evidence, review findings, blockers and
next action. In T3 Code the parent arms the PR watcher and ends the turn while
waiting; delegated reviewers never watch. Remove the watch when finished, stopped
or handing back a blocker. Do not promise continued monitoring without an active
watcher. If monitoring is unavailable, report pending work as incomplete.

Report what was delivered, evidence, PR URL and the actual state returned by
file-pr and babysit-pr. Distinguish deferred requirements from failed or pending
checks; do not claim unperformed checks passed. A requested merge remains pending
until actually merged.
External blockers may need intervention; do not manufacture success, bypass
required approval or repeatedly ask the same question.
