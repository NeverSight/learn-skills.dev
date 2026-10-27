---
name: git-workflow
description: >-
  Applies the user's git defaults: branch from the remote default, merge rather
  than rebase for ordinary branches, use native GitHub stacks when selected,
  never amend, and squash-merge pull requests. Use when branching, syncing,
  committing, pushing, or merging in the user's repos.
license: Unlicense OR MIT
compatibility: >-
  Requires git; pull-request operations also require the GitHub CLI (gh) and
  network access. Publishing to GitHub also requires Python 3.11+; protected
  native stack publication also requires a POSIX shell.
---

# Git workflow

Keep every change on a fresh, focused branch whose history stays reviewable and
recoverable: merge instead of rewriting, never lose local work, and land each
pull request as one squash commit with a meaningful subject. A git request
authorizes only the repository and GitHub state required for that operation.

An explicit user instruction about one of these defaults replaces only that
default for the active workstream. Preserve it across turns until changed; a
new repository or operation needs its own scope.

## Start or resume work

- Resolve the base from the remote default; never hardcode `main`.
- Make remote-default synchronization an automatic preflight for new work; do
  not ask permission to perform a safe clean update.
- When new work starts from the local default branch, inspect status before
  fetching or editing. If it is clean, fetch and fast-forward it to the fetched
  remote-default tip automatically. Stop on local-only commits, divergence, or
  a non-fast-forward update.
- If that local default worktree is dirty, stop before fetching, updating, or
  editing and ask the user to choose: discard the state, or preserve it and
  create a focused branch/worktree from the latest remote default. Do not make
  either choice, stash, commit, or discard anything without the answer.
- Before the first edit in any other newly selected or reused branch or
  worktree, require a clean worktree and fetch the remote default branch. Stop
  and report dirty files; never stash, commit, or discard them automatically.
- Automatically create every new focused local branch and worktree at the exact
  freshly fetched remote-default tip. Do not configure a focused branch to
  track the remote default; set its upstream only when pushing that focused
  branch.
- When entering an existing focused branch or worktree, fetch its remote base
  before editing; merge it in only under the
  [up-to-date rule](#update-commit-and-push) below.
- Before new work starts, apply the
  [default-branch health](#default-branch-health) gate.

## Update, commit, and push

- Merge the remote base to update a branch. Never rebase. The remote base is
  the branch the open PR targets when that is the remote default or a named
  base as [create-pr](../create-pr/SKILL.md) step 1 defines it, such as a
  release branch for a backport. Never merge the remote default into a branch
  whose PR targets a named base. Without an open PR, the remote base is the
  remote default.
- A pull request branch, and a focused branch headed for one, need not be up
  to date with its base. Merge the remote base into it only when:
  - it conflicts with the base;
  - the repository requires up-to-date branches through a ruleset or branch
    protection setting (GitHub then reports the PR's `mergeStateStatus` as
    `BEHIND`);
  - a [Stale or Red](#default-branch-health) repair needs base commits, such
    as the commit it fixes; or
  - the person asks.

  Being behind alone is no reason, and neither is an edit or a push: every
  base merge restarts the PR's checks, including any full CI run.
- A layer of a native stack is updated through the stack reference. When an
  open PR targets any other non-default branch, it has no remote base: stop
  before merging or pushing and report that base instead of choosing one. The
  user can then name it or have the PR restacked.
- During an authorized PR update, resolve conflicts whose intended behavior is
  established by the selected change and current base. Preserve both sides'
  required behavior, regenerate generated files with the project tool, and
  validate the result. Pause when resolution requires a material unresolved
  choice. During a new-work preflight, report conflicts before implementation.
- Never amend commits. Add a new commit for every correction.
- Never force-push. Stop if a plain push is rejected by divergent history.
- Stage only relevant files and exclude secrets or unrelated local work.
- Run the [publication guard](#publication-guard) before each commit, push
  and pull request write to a GitHub repository.
- Use concise Conventional Commit subjects in imperative mood. Each commit title
  must state its observable impact, not only the mechanism changed.
- Let hooks run unless the user explicitly asks otherwise.

## Publication guard

Run [scripts/publication_guard.py](scripts/publication_guard.py) from this
installed skill with Python 3.11 or newer, using its actual installed path, for
example `python3 /path/to/git-workflow/scripts/publication_guard.py`. It needs
`gh` signed in to GitHub. When the repository receiving the content is public,
it rewrites private GitHub references and local machine paths out of it.

- Before each commit, write the message to a file, run `staged --message-file
  FILE`, and commit with `git commit -F FILE`.
- Before each push, including `gh stack push`, `gh stack submit` and
  `gh stack link`, run `outgoing --base BASE`. BASE is `REMOTE/DEFAULT`, or for
  a stack layer the branch beneath it. Add `--remote NAME` when the push goes
  to a remote other than the branch's push remote. Commit what it stages
  through the commit step above, then push.
- Before each pull request title or body write, write the title and body to
  files and run `pr --repo OWNER/REPO --title-file FILE --body-file FILE`, where
  `OWNER/REPO` is the repository the pull request is opened in. Then create or
  edit the pull request from those files. This covers `gh pr create`,
  `gh pr edit`, `gh api .../pulls --input FILE` (build its JSON from the
  checked files), and the titles and bodies that `gh stack submit` and
  `gh stack link` create, which you reconcile with `gh pr edit` afterwards.

Act on its result:

- Exit 0 with `is not public; nothing checked` or `nothing to rewrite`:
  continue.
- Exit 0 with `rewrote ...` lines: the staged files and the files you passed
  now hold the rewritten text, and unstaged edits to those files get the same
  rewrite. Continue, and report each `rewrote` and `placeholder` line.
- `warning: commit ... pushing publishes that commit unchanged`: history is
  never rewritten. Report the named commits and files to the user with the
  push.
- `warning: PATH was not checked`: the guard could not read that file as text.
  Check it yourself for private repository names and local paths before
  publishing, and report it.
- `warning:` about `.github/publication-guard.json` or a keep pattern: report
  it; the guard used its default keep list for what it could not read.
- Exit 2: Git or GitHub could not answer a question the guard depends on, or
  an argument was wrong, and nothing was changed. Fix the cause the error names
  and rerun. Never publish without a run that exits 0.
- Any other exit: the guard failed. Stop, do not publish, and report its
  output.

## Default-branch health

A pull request's own checks protect the default branch; the default branch's
own runs report on what already landed. Establish the default branch's health
before new work starts, and recheck it immediately before each merge, from the
CI the project requires on default-branch commits, such as its push CI, not an
integration deployment. For each required workflow, list its recent
default-branch runs, for example with `gh run list --workflow WORKFLOW
--branch DEFAULT --limit 50 --json
databaseId,headSha,event,status,conclusion,createdAt`. Raise `--limit` until
the listing reaches a run that succeeded or failed (`failure`, `timed_out` or
`startup_failure`), or the workflow's whole history. Push runs and the
[coverage sampler](#coverage-sampler)'s dispatched runs both count. The
deciding commit is the newest commit in `git log --first-parent
origin/DEFAULT` with a run that succeeded or failed, whichever event started
it. List every run for that commit (`gh run list --workflow WORKFLOW --commit
SHA --json databaseId,event,status,conclusion,attempt,updatedAt`); the one
whose latest attempt completed last is the deciding run. Cancelled, superseded
and skipped runs carry no result.

- **Green:** each deciding run succeeded, or the project requires no CI on
  default-branch commits, and no run for a later commit was cancelled or
  superseded. Work starts and merges. Runs still queued or in progress for
  later commits hold neither, and a merge may supersede or cancel them. Never
  make parallel deliveries take turns or hold a shared merge token to keep a
  run alive.
- **Stale:** each deciding run succeeded, but a run for a later commit was
  cancelled or superseded, usually because the workflow cancels in-progress
  runs on each push (a `concurrency` group with `cancel-in-progress`), so
  completed runs no longer cover every commit that landed. A required workflow
  with no run that succeeded or failed is Stale too. Merging never pauses
  for it: each PR's own required checks, and any full CI run its declared rule
  requires, stay the merge gate, and only a completed failed run stops
  merging. The [coverage sampler](#coverage-sampler) closes the gap, unless
  the repository declares a [staleness bound](#declared-staleness-bound).
- **Red:** a deciding run failed. Stop merging: getting the branch green comes
  first, and only its repair starts or merges. It stays red until a rerun of
  that run, or a run of that workflow for the same or a newer commit,
  succeeds, even after the repair lands. Identify the failing job and its cause; when a sampler run failed,
  the culprit is among the commits it newly covered, `git log --first-parent
  PREVIOUS-DECIDING-SHA..SAMPLER-SHA`. A flake is cleared by rerunning the
  failed jobs where the project allows. Otherwise look for an owner of the
  fix: an open PR, an issue or another session. When no one owns it and the
  active request authorizes merging, deliver the repair as its own work item
  through `/deliver` and land it first. Otherwise report the failing job, its
  cause and the repair it needs. Once the repair has landed, await its run
  with `delivery-wait`'s `workflow-terminal` wait, and merge nothing that
  would supersede or cancel it. Independent local investigation can continue;
  nothing else starts development or merges.

The red rule is strict by default. Only the person or the project can relax it,
explicitly, for example to let an unrelated docs-only change land.

### Coverage sampler

Under Stale, keep one run of each required workflow in flight that no merge
can cancel. Coverage then advances by one run's duration however many merges
land, for at most one extra run per workflow duration.

- When no such run is queued or in progress for the workflow, dispatch one on
  the current tip outside its cancelling group, for example with `gh workflow
  run WORKFLOW --ref DEFAULT`, and record its run ID and commit. Keep merging;
  never wait for it.
- Every delivery reuses the run in flight; none starts its own. When the
  listing after a dispatch shows an earlier sampler run in flight for the same
  workflow, cancel the run just dispatched.
- It decides like any other run: when it succeeds and its commit is the
  newest with a result, everything up to that commit is covered. When it
  fails and decides, the branch is Red.
- A dispatch escapes the cancelling group only when the workflow has a
  `workflow_dispatch` trigger and its `concurrency` group keeps dispatches
  apart from pushes. A group keyed only on the workflow and the ref puts a
  dispatch on the default branch into the same group as the next push, which
  cancels it. When the workflow allows no run outside the group, report that
  as a project gap with its fix, such as adding `github.event_name` to the
  group key and cancelling in progress only for pushes, and keep merging under
  the PR gates.

### Declared staleness bound

A repository may declare a default-branch staleness bound in the monitoring
policy of its repository-root `ORCHESTRATION.md`: a limit on uncovered
commits (`git rev-list --count --first-parent DECIDING-SHA..origin/DEFAULT`),
on the deciding commit's age, or both. Without one there is no bound, only the
sampler. A declared bound applies whenever the deciding run lags the tip,
whatever the cause. A setting that is malformed or contradicts
higher-authority instructions counts as already exceeded; report it. A
required workflow with no run that succeeded or failed is past the bound.

Past the bound, merging pauses until a completed run brings the gap back
within it. Await the run that does, with `delivery-wait`'s `workflow-terminal`
wait: the sampler in flight when the gap after its commit is within the
bound, otherwise the tip's own run, which nothing cancels while merging
pauses. Dispatch a sampler on the tip only when the tip has no run queued or
in progress. Every delivery waits on that same run. When it completes, its
result decides, and everything that became ready meanwhile merges.

## Merge

- Merge a pull request as soon as it is ready under the
  [readiness contract](../address-feedback/references/pr-readiness.md) for its
  exact head, which includes any full CI run the repository's declared
  full-CI rule requires. Never wait for the base branch's runs from earlier
  merges, except where [default-branch health](#default-branch-health) is Red
  or past a [declared staleness bound](#declared-staleness-bound).
- Before each merge, recheck
  [default-branch health](#default-branch-health).
- Squash-merge pull requests and delete the source branch afterward.
- Because the merge is a squash, the pull request **title** becomes the commit
  subject on the base branch: the branch's own commit subjects do not survive.
  Give the title a Conventional Commit subject that states the observable impact
  of the change as a whole. Pick its type from the net effect rather than the
  most frequent commit under it. Where a project generates its changelog or
  version bump from commit history, a non-conforming title merges cleanly and is
  then silently absent from it.
- After a squash merge, sync the local base and remove the merged local branch.

## Native GitHub stacks

Use the official `gh stack` workflow when the user selects a stack, when work
has a real dependency chain, or when a confirmed large issue is deliberately
split into cumulative, independently reviewable layers. Do not stack unrelated
work. Each layer must have one clear claim, a bounded diff, its own validation,
and an explicit subset of the requirements.

Read [references/github-stacks.md](references/github-stacks.md) before creating,
syncing, pushing, submitting, reviewing, or merging a stack. That reference is
the only exception to the merge-only and never-force-push defaults above:
rebases and force-with-lease are permitted only when performed by verified
`gh stack` commands against a clean, confirmed native stack. Raw `git rebase`,
`git push --force`, and manual `git push --force-with-lease` remain forbidden.
