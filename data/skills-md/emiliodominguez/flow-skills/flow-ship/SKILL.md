---
name: flow-ship
description: "Delivery through the requested Git or review stage: commit, push, pull or merge request, ready or merge. Use when asked to push, commit and push, open or update a PR or MR, or merge. Routes to `flow-commit`, `flow-pr-fix`, `flow-git-fix` or `flow-release`."
metadata:
  stage: deliver
---

# Ship

Complete the delivery action the user requested. Push, draft change request (pull or merge
request), ready, merge, deploy and publish are distinct outcomes; one never authorizes another.

## Phase 1: Establish the terminal action

Read current authorization, repository delivery rules, branch/remotes, status and existing change request
metadata. Resolve base, head and target remote from evidence; reuse an existing change request. Do not
re-prompt for an authorized action, and never treat a skill handoff as permission for an
unrequested merge, deployment, reviewer request or message.

## Phase 2: Verify the artifact

- Inspect committed, staged, unstaged and relevant untracked changes separately; preserve
  unrelated user work.
- Run the pre-launch checklist: required format, lint, types, tests, build, generated docs and
  relevant runtime checks. Use `flow-review` where the task or repository requires review.
- Run each check fresh and read its output before reporting it; record the verified revision. If hooks or CI fixes change behavior, repeat affected checks
  and review. A previous green revision does not verify the current one; keep unrun checks and
  missing access explicit.

## Phase 3: Commit and push when requested

- Use atomic commits under the conventional-commit policy of `flow-commit`. Never bypass hooks.
- After a failed plain commit, fix and create a new commit; never amend the unrelated previous
  commit. Honor an explicitly requested amend only after checking HEAD.
- Push fast-forward to the identified remote/branch. Conflicts or rewritten history go to
  `flow-git-fix`; no routine force-push. Verify the remote head. Do not let a CLI silently pick a
  fork or push target.

## Phase 4: Create or update the requested change request

- A requested draft stops at draft. For ready, follow the repository workflow; draft-first
  helps when checks must run before readiness, but is not a universal gate.
- Body: problem, change, resulting behavior, validation, meaningful limitations or rollback
  considerations. Pass it via a structured field or body file with real newlines. No reviewer
  pings or comments unless requested.
- Inspect checks on the current head and distinguish passed, failed, pending, skipped and
  absent. Some pipelines run only once a change leaves draft; others are disabled. Do not deadlock
  on a check that cannot start in draft or call absent CI passing. Use bounded waits and report
  outstanding required checks.

## Phase 5: Confirm the result

Verify the remote SHA, change request URL, draft/ready/merged state and check summary. For an explicitly
requested merge, deployment or publication, complete its preparation and required gates first.
Otherwise stop at the requested stage with a usable link.

## Anti-patterns

- Turning "push this" into a ready change request, reviewer ping, merge and deployment.
- Claiming review passed after adding unreviewed behavioral fixes.
- Treating missing CI as green or waiting forever on a disabled workflow.
- Editing or discarding unrelated staged work for convenience.

## Done when

- The authorized stage is reached and confirmed against remote state.
- Verification belongs to the delivered revision; remaining limits are visible.
- The user has the commit or change request reference.

Use `flow-release` for requested versioned publication, `flow-pr-fix` for later review feedback
or `flow-git-fix` for a demonstrated Git problem.
