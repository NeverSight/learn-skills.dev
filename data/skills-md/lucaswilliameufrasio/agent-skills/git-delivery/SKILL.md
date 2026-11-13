---
name: git-delivery
description: >-
  Plan and carry out a safe Git delivery from branch preparation through commit,
  push, pull request, CI, and release handoff. Use when asked to deliver a
  feature/fix, prepare a commit or PR, release a batch of changes, or address
  review comments on the author's own pull request. Discover the repository's
  workflow instead of assuming branch names, ticket systems, or merge policies.
---

# Git delivery

Coordinate Git tasks without assuming every repository uses the same flow.
Treat repository instructions, remote configuration, branch protections, and
the user's explicit authorization as the source of truth.

Read and apply [`task-completion`](../task-completion/SKILL.md) for tracking
requested outcomes, finishing authorized steps, and reporting remaining work.
Use the skill loader or sibling file; if unavailable, report the limitation.
This does not grant permission for any delivery step.

## Inspect before acting

1. Check the repository, current branch, remotes, `git status`, recent history,
   and the diff. Preserve unrelated local changes; do not reset or discard work.
2. Read `AGENTS.md`, release docs, CI configuration, and project scripts for
   branch bases, naming, required checks, PR templates, and release steps.
3. Determine whether the request authorizes only preparation, or also commit,
   push, PR creation, merge, tagging, or publication. Do not infer permission
   for a later step from permission for an earlier one.
4. Check whether pushing a target branch triggers deployment and whether shared
   branch restrictions apply. Follow the repository's exact process; do not
   treat a backport requirement or a second PR as implied authorization.

## Branch and changes

- Use the repository's documented base branch and branch naming. If unclear,
  ask rather than assuming `main`, `develop`, or a particular Git flow.
- Before creating a branch **or rebasing an existing branch onto its base**,
  refresh the actual local base branch, not just its remote-tracking reference:
  1. Identify the intended base, remote and upstream; inspect the working tree,
     other worktrees using the base, and local/remote divergence after fetching.
  2. If the checkout is clean, the base is available, and it has no local-only
     commits to rewrite, switch to the base and run `git pull --rebase` with its
     verified upstream, or `git pull --rebase <remote> <base>` when appropriate.
     Verify the local base matches the refreshed upstream after the pull.
  3. Create the new branch from that base, or return to the intended existing
     branch and rebase it onto the updated base. Confirm the rebase and any
     published-history rewrite are authorized; validate the resulting head.
  4. If uncommitted work, local-only/divergent base commits, another worktree,
     missing upstream/access, conflicts, or repository policy prevents safe
     updating, stop and explain. Do not stash, discard changes, rewrite shared
     base history, force-update refs, or switch worktrees without authorization.
     A fetch alone is not a substitute for updating the local base.
  The pull itself may fetch newer commits: verify against the post-pull upstream.
  Recheck freshness before subsequent rebases when the remote may have moved.
- Follow documented commit language and ticket-reference conventions. Do not
  invent issue identifiers or infer Git flow solely from a branch name.
- Keep changes focused. Inspect the final diff and stage only intended files.
- Follow the `conventional-commits` skill for commit messages. Do not commit,
  amend, force-push, or push unless explicitly authorized.
- Before a commit or delivery claim, run the `testing-standard` skill for
  every repository changed.

## Pull requests

Before opening a PR, verify the current branch and commit range, ensure there is
not already an open PR for the same head, and review the complete diff. Use the
repository's target branch and template. A useful description explains:

- **Context:** the problem or request (link a ticket only if one exists).
- **Changes:** meaningful changes and why they were made.
- **Validation:** checks run and any limitations.
- **Compatibility:** breaking changes and migration notes, when applicable.

Use an accurate title based on the change. Do not invent ticket IDs, test
results, or requirements. After opening, report the PR link and monitor required
checks if requested.

Do not merge unless the user authorized merging. Verify the head, mergeability,
checks, and actionable review threads first. Before merging any feature/bugfix
PR, use `pr-merge-sequence` to refresh the local base with `git pull --rebase`,
run a rebase of the feature branch onto that updated base even if already current,
and validate the resulting head. Repeat if the base moves before merge. Respect
authorization for rewriting published history and pushing the changed head;
stop when that authorization or safe base refresh is missing. This requirement
does not turn release-promotion branches into feature branches.

## Comments on the author's own pull request

When asked to handle comments on that person's own pull request, confirm
authorship, the branch, and the head. Read the general comments and every
review thread, including earlier replies and whether each thread is resolved or
outdated. Apply the steps below to each suggestion. This work does not include
approving the pull request or merging it.

Reply in the language of that thread. When the thread does not show a language,
use the language of reviews in that repository or organization. When that
language is Brazilian Portuguese, a done closing is exactly `Feito`.

- **It applies:** correct it or apply the appropriate solution, validate the
  behavior, and update the branch once that update is authorized. When the
  correction is on the pull request and follows the requested approach, reply
  on that same thread with the done closing, then resolve the conversation. An
  incidental difference still uses that closing when the requested behavior is
  what landed. When the issue is fixed by a different approach, reply with one
  sentence saying what was done instead. Add the reason only when the diff does
  not make the difference obvious. Do not use the done closing for that reply.
  Resolve when no decision or question remains. If that other approach still
  needs the reviewer's agreement, handle it as partial.
- **It does not apply:** explain respectfully, and with the reason, why the
  suggestion does not apply. After that reply, resolve the conversation when no
  decision or question remains. If the point still depends on the reviewer's
  agreement or clarification, leave the thread open and wait.
- **Partial, inconclusive, or out of scope:** separate what holds from what
  does not, and get the missing data or decision. Do not send the done closing,
  including `Feito`, and do not resolve the thread while any doubt or work is
  still pending.

Push, reply, and resolution are separate actions. Have authorization for each
one before doing it. Reply before using **Resolve conversation** /
**Resolver conversa**, or the equivalent control. Handling threads on the
author's own pull request does not authorize resolving someone else's threads
on another person's pull request.

## Release handoff

Discover the project's release process; do not impose a release-branch pattern.
Confirm the intended contents and target, run the quality gate, and use
`semantic-versioning` to select or validate the version. Prepare a release PR or
notes only when requested. Creating tags, publishing artifacts, or deploying
requires explicit authorization.

Release promotion is not an ordinary feature rebase. Consult
`pr-merge-sequence` for the distinction when a development/release/main flow is
in use. For confirmed Actions billing blocks, use
`actions-billing-local-validation` for evidence and approved local substitution,
without treating this as permission to bypass checks or protection.

## Final report

State what was completed, the branch/commit/PR references, which checks actually
ran, what remains, and any blocker. Never say a PR is ready or a release is
published based on an unverified or cached result.
