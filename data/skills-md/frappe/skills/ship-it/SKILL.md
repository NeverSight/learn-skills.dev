---
name: ship-it
description: Take finished work to a merge-ready PR in one pass - intent, review, live test, docs, lint, PR, and CI. User-invoked only - run /ship-it [wip|prod] ["intent"], or /ship-it on a branch with an open PR to resume or babysit it.
disable-model-invocation: true
---

# Ship it

You own the work from "code is done" to "PR is ready for the human to merge". Run the pipeline in order. Every step answers for its own edits, and the pipeline only moves forward. The human always merges.

## Tier

Use the prod tier by default. A tier argument (`/ship-it wip` or `/ship-it prod`) sets the tier for this run. On resume without a tier argument, use the tier in the `## Review` marker (see Resume).

- **prod**: a project in production. Every step runs.
- **wip**: a personal or work-in-progress project. Steps marked – are skipped.

## Pipeline

| #   | Step            | prod                | wip                        | Detail                             |
| --- | --------------- | ------------------- | -------------------------- | ---------------------------------- |
| 1   | Intent          | user confirms       | written, not confirmed     | [steps/intent.md](steps/intent.md) |
| 2   | Rebase          | ✓                   | ✓                          | below                              |
| 3   | Review          | correctness + taste | correctness, blockers only | [steps/review.md](steps/review.md) |
| 4   | Test            | ✓                   | –                          | [steps/test.md](steps/test.md)     |
| 5   | Docs            | ✓                   | –                          | below                              |
| 6   | Lint            | ✓                   | ✓                          | below                              |
| 7   | Commit and push | ✓                   | ✓                          | below                              |
| 8   | PR              | full body           | Summary, Intent, Review    | [steps/pr.md](steps/pr.md)         |
| 9   | CI and bots     | CI, then bot loop   | CI only                    | [steps/ci.md](steps/ci.md)         |

Read a step's detail file when you reach that step, not before.

Steps 4 to 9 can add commits after the review: test fixes, docs, lint, CI fixes, and bot fixes. Before step 8 opens or updates the PR, and before you report done, compare `HEAD` with the last reviewed sha. When commits follow it, re-review `<sha>..HEAD` as in [steps/review.md](steps/review.md). Then put the new reviewed sha in the `## Review` marker. In prod, when those commits change behavior that a live scenario covers, re-run that scenario as in [steps/test.md](steps/test.md) and replace its evidence in the PR body before you report done.

**Done** means: the PR is open and ready (not draft), the `## Review` marker names `HEAD`, CI is green, and in prod the bot loop has stopped by its rule. Report to the user and ask them to review and merge. Stop there.

## Resume

There is no state file. The branch, the commits, and the PR are the record. On every run, find the first unfinished step:

1. No commits ahead of the base branch and no uncommitted changes → nothing to ship. Say so.
2. Uncommitted changes that belong to this intent → commit them first, in logical groups with messages as in step 7. Do not push. Changes that mix in other work → ask first, as in "Where it runs".
3. Read the PR for this branch (`gh pr view --json number,body,headRefOid,isDraft`).
   - No PR → start at step 1.
   - The PR body has `## Intent` → that is the intent. Skip step 1 unless the user gave a new one.
   - The `<!-- ship-it: reviewed=<sha> tier=<tier> -->` marker in `## Review` names the last reviewed commit. Commits after it (local or pushed) → re-run review on `<sha>..HEAD` only, then continue forward.
4. The tier for this run is prod and the marker says `tier=wip` → step 1. Wip did not confirm the intent, ran only part of the review, and skipped the test and docs steps. Step 3 reviews the whole change again, and step 8 writes the full prod body and sets the marker to `tier=prod`.
5. Otherwise: unpushed commits → step 7. PR is a draft → step 8. CI failing or running → step 9. CI green → step 9's bot loop (prod) or done (wip).

Tell the user which step you are resuming from and why, in one line.

## Where it runs

- **In place** when the checkout is a feature branch or worktree and every uncommitted change belongs to this intent.
- **Ask first** when on the default branch, or when uncommitted changes mix this work with other work. Offer to move this work to a new worktree. Create one only on a yes.
- **Frappe app inside a bench**: a plain `git worktree` is invisible to the bench. Run in place.

## Subagents

Every reviewer and every fixer is a fresh subagent that never saw this conversation. Its prompt carries everything it needs: the intent, the recorded decisions, the diff range, and the reviewer file to follow. A fixer is never the reviewer that reported the finding, and a re-review is a new subagent.

| Agent                                         | How to start one                                                                               |
| --------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Claude Code                                   | The `Agent` tool.                                                                              |
| Codex                                         | `spawn_agent`. Codex spawns only when told to, so spawn explicitly.                            |
| T3 Code (the `t3-code` MCP tools are present) | `delegate_task` with `mode: "wait"`. Pick provider and model from `orchestrator_capabilities`. |

Use the strongest model available for every subagent. When the agent can start a model from a different provider, give the correctness reviewer that model: a second model family catches mistakes the first one shares with the author.

## Findings and the user

Reviewers return findings in the format in [review/verdict.md](review/verdict.md). Fix `auto-fix` findings without asking. Collect every `ask-user` finding from a step and ask the user about them in one message, laid out as in [review/ask.md](review/ask.md). Answers become decisions, which nothing in the run reverses.

## Inline steps

### 2. Rebase

`git fetch origin`. When `origin/<branch>` exists, record its sha for step 7 and take in the remote work that local history lacks. Find the last commit this clone pushed: `git reflog show --format='%H %gs' origin/<branch> | grep -m1 'update by push'`. Use that sha only when the local branch's own reflog has it (`git reflog show --format=%H <branch> | grep -qx <sha>`), which shows this branch was at that commit. Every commit up to it is already in local history, possibly rewritten by an earlier rebase. The commits after it, `<pushed sha>..origin/<branch>`, were pushed by someone else: take each one in, for example with `git cherry-pick`. When that sha is not an ancestor of `origin/<branch>` (`git merge-base --is-ancestor <sha> origin/<branch>` fails), someone else rewrote the remote branch after your push: stop and ask the user. When there is no such sha, take in `HEAD..origin/<branch>`. Skip a commit whose change `HEAD` already has. Then rebase onto `origin/<base>`. Resolve conflicts in the spirit of both sides and the intent. When a conflict needs a product decision, ask. When the diff against the base is empty after rebase, stop: there is nothing to ship.

### 5. Docs (prod)

Find what the change made stale: README, docs pages, `AGENTS.md`, code comments near the change, examples. Fix each stale fact in its one authoritative place. Report what you could not resolve as an `ask-user` finding.

### 6. Lint

Run the repo's own formatter and linters with their fix modes: look at `package.json` scripts, `pyproject.toml`, `.pre-commit-config.yaml`, and the CI workflow to see what CI will run. Fix what remains, up to 3 attempts. When the repo has no linters configured, skip.

### 7. Commit and push

Commit in logical groups with conventional messages (`feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`). Review fixes follow the commit rule in the Fix loop of [steps/review.md](steps/review.md). Keep `tidy:` commits separate from behavior changes. Commit messages describe the change only.

Push safely:

- When this run has not recorded the sha of `origin/<branch>` (a resume at step 7), fetch, record it, and take in remote work as in step 2. Otherwise `git fetch origin`.
- Compare `origin/<branch>` with the recorded sha. When it moved, the remote has work you have not taken in: go back to step 2.
- When `origin/<branch>` does not exist or is an ancestor of `HEAD`, use a plain push. Otherwise `HEAD` rewrote pushed commits, in this run or an earlier one: push with `--force-with-lease=<branch>:<recorded sha>`.
- When the push is rejected because the remote changed after the fetch (`non-fast-forward`, `fetch first`, or `stale info`), go back to step 2. Any other rejection (permissions, branch protection, a server-side hook) does not change after a rebase. Stop and show the error to the user.
- After the push, record the pushed sha as the new recorded sha, so later pushes from step 9 compare against it.
- Note the push time. The bot loop in [steps/ci.md](steps/ci.md) uses it.
