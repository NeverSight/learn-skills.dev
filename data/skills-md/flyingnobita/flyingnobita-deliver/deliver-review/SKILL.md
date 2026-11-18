---
name: deliver-review
description: Review and repair an existing branch using delivery profiles and independent verification on Orca, Herdr or Paseo, without starting a full delivery or publishing it.
---

# Review and repair a branch

Resolve target branch (default current), fixed-point SHA (default merge-base
with the repo's default branch), spec and repo rules. Record the original target
HEAD. Read [host detection](../deliver/references/host-detection.md),
the selected adapter and [configuration](../deliver/references/configuration.md).
For a request to review only, run the reviewer and report; dispatch no repairs.

For review-and-repair, establish allowed scope and test seams from existing
approved artifacts. Ask only where those are missing or where a finding changes
scope. Record this review request and repair approval in the run; do not invent
approval for the original implementation or for shipping.

Create the appropriate `review-only` or `review-repair` purpose and record
`approved.review` (plus repair `seams` when applicable) using
[run records](../deliver/references/run-record.md). Record the
user's actual review request and settled scope; no full-delivery approval is needed.

Create an isolated review worktree/branch from the recorded target HEAD using
the adapter. Preserve a target checked out elsewhere and never switch or edit
the user's checkout. The reviewer reads the diff from the immutable fixed point.
Run the baseline, then follow the shared
[review loop](../deliver/references/review.md), saving artifacts
outside disposable worktrees. All fixes go through an implementer following
repository commit rules (or a configured custom commit skill). If baseline failures predate repairs, report them
and require a scope decision before claiming a clean result.

When clean, report the repair branch and exact target/repair SHAs. If the target
already moved, preserve the repair branch and report the divergence. Otherwise
leave the tested repair branch ready for the caller to integrate; do not move
another checkout's branch, push, merge a PR or deploy. Retain a worktree holding
unlanded repairs. For review-only/no-change runs, preserve artifacts first and
remove only the owned clean temporary workspace through the adapter.

Done when the review names every remaining finding, independent checks follow
the last repair commit, and each worker/workspace has a verified ownership or
retention decision. Report baseline, repair tests/red checks, final review,
commits, artifact paths, and whether the result is clean or blocked.
