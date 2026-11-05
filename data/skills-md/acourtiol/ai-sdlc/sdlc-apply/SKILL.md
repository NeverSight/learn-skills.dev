---
name: sdlc-apply
description: >-
  Implement an accepted intent step by step, prove each acceptance scenario,
  hand it to sdlc-verify and the user, then close it. Use when the user asks
  to build an accepted change, or to close a finished intent.
license: MIT
metadata:
  author: acourtiol
  version: "3.0"
---

# sdlc-apply

Build what the accepted intent says, show that it works, and let the user accept it. Do not push or deploy unless asked.

Need `intent/<slug>/intent.md` with `status: accepted` (for `tier: critical` that acceptance includes its `## Spec`). If a choice that changes architecture, safety or acceptance is still open, ask the user one question; otherwise state your assumption and continue.

## Working agreements

- **Lanes.** Default: the current checkout, one intent at a time. Independent intents (disjoint files, no shared contract or migration order) may run in parallel, one worktree each at `$(git rev-parse --show-toplevel)/.worktrees/<slug>`, inside the repository and never in the folder that holds your projects (add it to `.git/info/exclude` if not ignored; anchor the root once, never nest), merged into the main branch by fast-forward or rebase when verified. No integration branches. A worktree is not isolation: concurrent services need their own database, compose project and ports, via the product's existing worktree setup.
- **Subagents.** Use them for read-only research or disjoint parallel work when that saves wall-clock or main-context size, with a bounded objective each. Do not fan out a swarm; coordination has a cost.
- **After a restart or interruption**, re-read `intent.md`, `git status` and the ticked steps before continuing. A past dispatch is not proof that work ran.
- **Ownership.** Record `git status --short` before writing. Others' dirty files are theirs; never reset, stash or stage them.
- **YAGNI.** Reuse existing code and patterns, then installed dependencies or the platform. Add a dependency or abstraction only for a demonstrated gap. Keep validation, error handling, security and accessibility.
- **No unrequested scope.** No new screens, required inputs or gates the user did not ask for. If one seems necessary, stop and present the tradeoff.
- **Commits.** One commit per coherent step, with the step's checkbox ticked in the same commit as its code. Conventional Commits: `type(scope): imperative summary`, blank line, one sentence of why. No commits that only record verification.

## Steps

1. Read `intent.md` and record `base: <HEAD hash>` in its frontmatter (committed with the first step). If `## Steps` is empty or vague, write the steps now: a few coherent slices, each with a `check:`. Order them so the riskiest boundary is exercised first.
2. For each step: implement, run its check, tick the box only after you saw it pass, commit.
3. Proof must exercise the real path, not a stand-in:
   - A new or changed input in a pipeline is asserted where it is consumed (the outgoing request or consumer), not just where it is stored.
   - Stateful or async flows: check persisted state after failure, retry and reload, not only the immediate response.
   - Schema changes: prove the upgrade from the previously applied migration state on a disposable database, with existing rows preserved. A fresh database passing is not enough. Never edit an applied migration.
   - Check that the test runner actually discovers the tests you rely on (component tests, other extensions).
   - Never run checks against production or a shared default database. Confirm the connection target before anything that mutates.
4. When the last step is done run typecheck, lint and the affected tests. For UI, drive the main path and one error path in the running local app and keep a screenshot or DOM excerpt path.
5. Fill `## Result` in `intent.md`: one line per Acceptance item with PASS or FAIL and the evidence, plus anything not checked. A FAIL or an unchecked required item is reported, never hidden.
6. Commit the finished candidate and hand it to `sdlc-verify` (both tiers). Fix what it finds with new commits, then re-review.
7. Present the Result and report to the user. The user accepts.

## Close (only after verify passed and the user accepted)

Order is fixed: apply, `sdlc-verify` (`report.md` with `verdict: pass`), user acceptance, then close. Never close straight after the last step. Closing records acceptance; it does not claim a release.

Check: steps ticked, `## Result` has no unexplained FAIL, `report.md` passes and the reviewed files are unchanged since it (`git diff --quiet <reviewed_head> HEAD -- $(git diff --name-only <base> <reviewed_head> -- . ':(exclude)intent')`; other commits landing meanwhile do not matter), unless the user waived review or, for tier `change` with no independent route, accepted "not independently reviewed". Then delete the folder and keep the story in history: `rm -rf intent/<slug> && git add -A intent/<slug>`, commit `chore(<slug>): close intent` with the Result lines (one per Acceptance item) and any unresolved reviewer findings in the body. An intent is open while its folder exists; finished ones are listed with `git log --diff-filter=D --format='%h %s' -- intent/` and read with `git show <commit>^:intent/<slug>/intent.md`. If the project has a knowledge bundle and this work supersedes a durable note, update it through that workflow. Do not push.

After two failures of the same kind, stop repeating the full gate and reproduce the failure narrowly. If the work turns out to need a different outcome, update the intent with the user rather than drifting from it.
