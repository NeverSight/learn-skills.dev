---
name: resolve-pr-conflicts
description: "Use when a PR has merge conflicts with its base branch, including conflicts found during babysitting or merging."
---

# Resolve PR conflicts

Update the PR's own branch against its current base. This skill does not
authorize merging the PR or retargeting it to another base.

## Inspect and update

```sh
gh pr view <n> -R <owner/repo> --json state,headRefName,headRefOid,baseRefName,mergeable,isCrossRepository,maintainerCanModify
```

1. Confirm the PR is open and record its head SHA and base branch.
2. Work in a temporary worktree, preserving existing local edits.
3. Fetch the PR head and base from their actual repositories; record the base tip.
4. Confirm fork permissions and the destination remote before updating the PR branch.
5. Merge or rebase onto the fetched base according to the repository's guidance.

Get explicit approval before rewriting a branch you do not own, unless already
authorized in the session. Disclose every rewrite. Use an explicit
`--force-with-lease=<branch>:<recorded-head-sha>` for an authorized rewrite.
If another contributor moved the PR head, stop and reconcile with its owner.
Never push to the base branch.

## Resolve and verify

Read [the conflict guidance](references/conflicts.md) before resolving hunks.
Preserve both changes' intent and check for semantic conflicts even when Git
merges cleanly. Ask when the resolution requires a product decision.

1. Resolve the conflicts and complete the merge or rebase.
2. Run the repository's relevant build, format, lint, and tests on the combined tree.
3. Recheck the remote head and base before pushing.
4. Update and re-verify if the base moved; preserve concurrent head changes.
5. Push the verified update to the PR branch within the user's authorized scope.
6. Re-read the PR head and mergeability after the push.
7. Remove the temporary worktree after preserving the completed work.

Report the resolved conflicts, any rewrite, checks run, and remaining blockers.
Return to the calling workflow for CI watching or an authorized merge.
