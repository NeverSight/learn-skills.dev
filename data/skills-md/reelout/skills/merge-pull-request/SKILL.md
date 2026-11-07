---
name: merge-pull-request
description: "Verifies and merges a pull request using a user-approved method, then safely cleans up its source branches. Use when the user asks to merge a PR."
license: MIT
---

# Merge a Pull Request

Verify that the PR is ready to merge, recommend a method based on its changes and repository policy, and get the user's approval before merging. After a successful merge, safely clean up its source branches.

## Workflow

1. **Inspect the PR and repository.**
   - Confirm the repository, target and source branches, PR head SHA, state, mergeability, reviews, required checks, and available merge methods.
   - Review the commits and diff to determine whether the PR contains a single logical change or several distinct concerns. Check whether either source branch has commits beyond the PR head.
   - If the PR is already merged, verify the merge and proceed to cleanup. If it is closed without merging, explain why and stop. If it has conflicts, lacks required reviews, or has failing checks, explain the blocker and stop. For conflicts or failing checks, give specific guidance on resolving them before the user tries to merge again.
   - Treat pending required checks as blockers. Wait for them when practical; otherwise, report the blocker and stop.
2. **Recommend and confirm a merge method.**
   - Base the recommendation on the PR's changes, commit history, and repository conventions. Do not use commit count alone to decide whether it contains one logical change or several.
   - Prefer **squash merge** when the PR represents a single logical change and its individual commits do not need to appear in the target history.
   - Prefer a **merge commit** when the PR addresses several distinct concerns and preserving its branch history is useful.
   - Prefer **rebase merge** when the repository favors linear history and preserving individual commits matters.
   - Tell the user which methods are available and recommend one with a brief rationale. Use the ask-user tool to get their explicit choice; do not merge without approval.
   - If the user selects squash merge, prepare the exact commit subject and body for the target branch. Show the complete message and get approval before merging. If the user declines, stop without merging.
3. **Merge the approved PR.**
   - Immediately before merging, confirm that the PR is still open and mergeable, its head SHA is unchanged, and all required checks and reviews pass. If the PR head SHA or approved merge method has changed since approval, ask the user to confirm again.
   - Use supported tooling to merge with the approved method. Do not modify the PR or bypass repository protections.
   - Verify that the PR was merged and record the resulting commit SHA. If the merge fails or cannot be verified, do not clean up any branches.
4. **Clean up the source branches safely.**
   - Never delete the target branch or the repository's default branch. Check local and remote source branches separately; the hosting platform may already have deleted the remote branch.
   - Delete the remote source branch only with an atomic compare-and-delete that requires its ref to match the exact PR head SHA. Invoke Git through an argv-safe process or API, passing the executable and arguments separately; never interpolate branch or remote names into a shell command. If the operation cannot enforce the expected SHA atomically, preserve the branch and explain why.
   - Before changing the local checkout, confirm that the worktree is clean. If it is not, leave the local source branch untouched and report that local cleanup is pending. Remote cleanup may proceed independently if its atomic safety check is available.
   - If the local checkout is on the source branch, switch to the target branch and fast-forward it from its configured remote. If switching or updating would be unsafe, leave the local source branch intact.
   - Delete the local source branch only if its tip exactly matches the PR head SHA, confirming that it has no additional commits. Prefer normal deletion. If Git refuses because a squash or rebase merge leaves the PR head outside the target history, force-delete the local ref only after verifying the merge and exact tip match. Otherwise, preserve the branch.
5. **Report the outcome.**
   - Report the PR, chosen merge method, resulting commit SHA, and cleanup status for each source branch. Explain any pending cleanup.

## Safety

- Get explicit approval for the merge method and, for squash merges, the exact commit message.
- Never force-push branch commits. Force-delete a ref only for the verified local cleanup described above; remote deletion requires an atomic expected-SHA check.
- Never bypass required checks, discard uncommitted changes, or delete a source branch whose tip differs from the verified PR head.
