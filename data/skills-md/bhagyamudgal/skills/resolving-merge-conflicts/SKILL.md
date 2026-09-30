---
name: resolving-merge-conflicts
description: "Resolve an in-progress git conflict without a silent drop. Use when the worktree is mid-merge, mid-rebase, mid-cherry-pick or mid-stash-pop: `CONFLICT (content)`, `<<<<<<<` markers, `Unmerged paths`, or `fix conflicts and then commit the result`."
---

1. Orient before you touch anything. Establish from `git status` whether you are in a merge, a rebase, or a cherry-pick. Under a rebase `ours` is the upstream you are replaying onto and `theirs` is your own commit, the inverse of a merge, and getting this backwards is the most common wrong resolution.

   Then split the conflicted files. Regenerate generated artifacts and lockfiles from source, never hand-merge them. That means `bun.lock`, `pnpm-lock.yaml`, `_generated/`, and snapshots. Only hand-written files go through steps 2-3.

2. Find the primary sources for each conflict. Understand why each change was made and what the original intent was. Read the commit messages, check the PRs, check original issues and tickets.

3. Resolve each hunk against the primary sources, not against the markers. Preserve both intents. Where incompatible, pick the one matching the merge's stated goal and note the trade-off. Every line in the resolution traces to one side's original or to a mechanical combination of both.

   Before staging, diff your resolution against both parents for every conflicted file. Run `git diff --cc <file>`, or `git diff :2:<file> <file>` and `git diff :3:<file> <file>`. Place every hunk from both sides in exactly one bucket. The buckets are kept, superseded with a note naming what replaced it, or dropped with a note naming why. A hunk you cannot place is a silent drop, an unresolved conflict wearing a resolution. State the ledger before you commit.

   Always resolve. When the two intents are genuinely incompatible and no stated goal decides between them, stop and put both candidate resolutions to the user rather than guessing.

4. Run the project's checks. `/done` owns this pipeline. Let it select the acceptance lanes, verify each one, assign states, and build its readiness card. Stop at that card and take none of the handoffs its final section ends in. Committing mid-merge concludes the merge with a generated conventional subject instead of the merge message, so `git-commit` and `file-pr` both wait for step 5. Fix anything the merge broke.

5. Finish the merge or rebase. When the operation rewrites commits or refs already published or consumed, invoke `preflight-mutations` immediately before continuing that published-history operation or updating its shared ref. Pass the exact operation, local, upstream, base, and head SHAs, affected remote refs, dependent branches and PRs, recovery ref, and explicit rewrite authorization. Apply its result contract before continuing. Unpublished local conflict resolution does not use this gate.

   Stage everything and commit. If rebasing, continue until all commits are replayed. The same conflict often resurfaces at each replayed commit, and your resolution must stay consistent across them.
