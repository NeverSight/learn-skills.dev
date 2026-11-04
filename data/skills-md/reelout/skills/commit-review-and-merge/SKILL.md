---
name: commit-review-and-merge
description: "Coordinates the commit-and-review and merge-pull-request workflows in sequence. Use when the user asks to commit changes, have a PR reviewed, and merge it once it is ready."
license: MIT
---

# Commit, Review, and Merge

Run the existing `commit-and-review` and `merge-pull-request` skills in sequence, passing the specific PR from the first workflow to the second. Do not duplicate or bypass their workflows, approval gates, or safety checks.

## Workflow

1. Invoke `/commit-and-review` and let it complete its workflow.
2. Proceed only if that skill successfully publishes the branch, opens or updates a PR, completes its review-and-fix loop, and confirms that the specific PR is ready to merge.
   - If the user declines publication, the PR is not ready, or the workflow stops at a blocker, do not invoke the merge skill. Report the outcome and any blocker.
3. Invoke `/merge-pull-request` for that PR and follow its workflow. Obtain the user's explicit approval of the merge method and, for a squash merge, the exact commit message.
4. Report the merge and branch-cleanup outcome returned by the merge skill. Claim success only if it verifies the merge.

## Safety

- Treat publication approval and merge approval as separate decisions. Agreement to publish or asking for a merge does not approve a merge method or squash commit message.
- Do not start the merge workflow unless the commit-and-review workflow confirms the PR is ready. Do not merge if the merge workflow reports a blocker or lacks required approval.
- If either skill is unavailable, stop and identify which workflow could not be run. Do not substitute an independent commit, review, publication, or merge process.
