---
name: cleanup-branches
description: "Clean completed local and remote Git branches using integration and pull-request evidence. Explicit invocation only."
disable-model-invocation: true
---

# Cleanup Branches

Requires Git and repository access; use authenticated `gh` for GitHub evidence.

Clean completed local and remote branches in the requested repository. A cleanup
request authorizes both scopes unless the user narrows it. Choose and perform
routine deletions from evidence without a separate approval round. Ask only when
an unresolved fact or retention decision materially changes what can be removed;
complete independent cleanup first. Honor requests limited to inspection.

## Establish the live state

- Resolve the repository, fetch and push destinations, default branch, and
  durable integration branches from configuration, repository instructions, and
  PR history. Do not assume `origin`, `main`, or that every configured remote is
  a deletion target; distinguish the project's repository from upstreams and
  forks. Resolve ambiguous ownership before deleting from that remote.
- Inspect local branches, upstreams, worktrees, and working-tree status. Refresh
  relevant remote branch refs and inspect live remote tips. Scope fetching and
  pruning to branch refs; do not prune tags or other namespaces. Pruning stale
  remote-tracking refs does not delete branches on the server.
- For GitHub, use `gh` to obtain complete relevant PR history, open PR heads and
  bases, and branch protection/ruleset evidence. Match repository identity as
  well as branch name. Follow pagination; a failed or partial lookup is unknown,
  not evidence that no PR or protection exists. For another host, use its
  equivalent API. Continue only deletions whose required evidence is available.

## Decide what is finished

Preserve the current branch, branches checked out in any worktree, default and
protected branches, established long-lived branches such as `dev` or release
lines, intentional backups, and branches serving as an open PR's head or base.
Apply these retention checks to corresponding remote branches too. Do not switch
branches, remove worktrees, stash, reset, or discard working files to enable
cleanup; dirty files need not block deletion of unrelated completed branches.

Evaluate each local and remote tip independently. A branch is eligible when it
passes the retention checks and either:

- Its exact tip is an ancestor of a freshly verified durable integration tip.
  A PR is not required for work demonstrably integrated this way.
- For a squash/rebase merge, a merged PR in the correct repository identifies
  that exact final head, and its resulting merge commit is reachable from the
  durable integration tip. Verify the current branch has no additional commits.
  Trace stacked merges through to durable integration; merging into a temporary
  branch alone does not establish completion. If this proof is unavailable,
  preserve the branch and explain the missing evidence.

Age, a missing upstream, a closed unmerged PR, a matching name, or a successful
`git branch -d` alone does not establish completion. Preserve branches with
unaccounted-for commits. Infer routine retention from repository evidence;
batch only consequential remaining questions with a recommended disposition.

## Delete and verify

1. Record each selected ref, repository/remote, full tip OID, and integration
   evidence before deletion. Briefly state the intended cleanup and proceed
   within the existing request; do not turn the record into an approval gate.
2. Recheck tips, worktree occupancy, and relevant PR/protection state immediately
   before mutation. Reclassify changed branches; do not delete using stale proof.
3. After verifying worktree retention checks, delete the exact local tip with
   `git update-ref -d "refs/heads/$branch" "$oid"`. This fails if another process
   moved the ref; refresh and reassess instead of dropping the expected OID.
   This plumbing command does not enforce worktree occupancy: coordinate with
   active local writers so no worktree can start using the branch during deletion.
   If that cannot be established, defer that local deletion. Remove its branch
   configuration only after successful deletion and while recreation is excluded.
4. Delete remote heads with an explicit expected-tip lease:
   `git push --force-with-lease="refs/heads/$branch:$oid" "$remote" ":refs/heads/$branch"`.
   Populate these variables from the verified record and quote ref names. A lease
   rejection means the evidence changed: refresh and reassess, never retry with
   an unguarded deletion or bypass server protection.
5. Verify local ref absence and query the server for remote ref absence; prune
   only obsolete branch-tracking refs. Confirm the current branch and working
   files are unchanged. Report deleted branches, retained/uncertain branches with
   reasons, and failures separately, retaining the deleted tip OIDs in the report.
   Continue independent eligible deletions after an isolated failure; do not
   claim remote deletion merely because a local tracking ref disappeared.
   Claim verified absence only from an observed follow-up check, never from
   command success or an assumed result. If that check is unavailable or fails,
   report the deletion command's outcome and mark absence as unverified.
