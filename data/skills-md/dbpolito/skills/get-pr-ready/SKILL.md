---
name: get-pr-ready
description: Fix CI failures and address review feedback on an existing PR. Use when asked to get a PR ready for merge.
---

# Get PR ready

Use the given PR or the current branch's PR. Follow repository instructions and preserve local work.

1. Confirm the repository and PR's head branch. Use `gh` to inspect failed checks, reviews, and inline review threads, including replies and outdated threads. Paginate every collection, including comments within threads.
2. Fetch the PR's base branch from the base repository. If its latest tip is not an ancestor of the PR head, merge it into the PR branch and resolve conflicts, even if GitHub reports no conflicts. Follow repository history policy; do not rewrite published history without authorization.
3. Verify feedback against the code and group related issues by root cause. Fix CI failures and valid review issues across affected sibling branches, consumers, recovery paths, and derived state, not just the commented line. Run relevant tests at the actual entry point or enforcement boundary, not only helpers or policies; check the final diff for regressions. Batch cohesive fixes, commit only your changes, and push. Explain disagreements or ask for clarification.
4. After a successful push, reply in each inline thread addressed by the pushed changes, following the rules below. Also reply to verified fixes already present on the PR when no adequate response exists; do not leave older or outdated comments unanswered merely because a later review approves.
5. Recheck the latest base/head, checks, and feedback after each push. Address available issues before waiting for required checks (`gh pr checks <number> --repo <owner/repo> --required --watch --fail-fast`). Also wait for already-triggered review automation on that head, even when advisory, then fetch its published review and threads. A successful job alone is not a clean review; if an expected review is missing or incomplete, report the blocker rather than claiming readiness.
6. Repeat until the PR head includes the freshly fetched base tip, required checks pass, required reviews are approved, and no actionable feedback remains. Report any feedback replies that could not be delivered.

## Reply to review feedback

- Reply in the original inline thread, not only in a top-level PR summary. For a fix, briefly state what changed, link the pushed commit, and report relevant validation accurately. Never claim a fix is pushed before the push succeeds or claim unrun tests passed.
- For a disagreement, explain the code evidence in that thread; ask there when clarification is needed. Record accepted or deferred risks only with an explicit user decision, and link that decision. Unresolved thread status alone does not mean a defect remains, and outdated status or approval alone does not prove a fix.
- Use the root review comment's numeric ID with `gh api --method POST repos/OWNER/REPO/pulls/NUMBER/comments/COMMENT_ID/replies`. Build the JSON body with `jq` and pass it through `--input -` to preserve Markdown safely. GraphQL thread IDs are not REST comment IDs.
- Read existing replies before posting. Avoid duplicate responses for the same fix or decision. Confirm the API response; after an uncertain submission, refetch the thread before retrying. If replying fails, report it as a blocker rather than silently considering feedback handled.
- Leave thread resolution to reviewers unless the user explicitly asks you to resolve addressed threads. Never resolve an unfixed concern to make the PR appear ready.

If progress requires human input or an external fix, report the current state and blocker. Never self-approve, dismiss reviews, or merge the PR.
