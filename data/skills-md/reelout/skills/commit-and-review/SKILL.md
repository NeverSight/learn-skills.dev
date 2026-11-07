---
name: commit-and-review
description: "Guides requested changes through branch selection and focused commits, then asks whether to publish a PR for review and fixes. Use when the user asks to commit changes and have them reviewed."
license: MIT
---

# Commit and Review

Commit only the requested changes, grouped into focused commits. Then ask whether to push the branch and open or update a pull request. If the user agrees, run a delegated review-and-fix loop until the PR is ready. Never merge it.

## Workflow

1. **Inspect the repository and identify the requested changes.**
   - Check the current and default branches, worktree status, staged and unstaged diffs, untracked files, and commits on the current branch that are not in the default branch. Refresh remote references if needed.
   - Identify which staged, unstaged, and untracked changes belong to this request. Preserve unrelated work and existing commits; never include, discard, or rewrite them.
   - If it is unclear which changes belong to this request, ask the user before staging or switching branches.
2. **Choose the working branch.**
   - Create a topic branch from the default branch if the current branch is the default branch or contains commits not in the default branch. Otherwise, continue on the current feature branch.
   - When creating a branch, carry over only this request's staged, unstaged, and untracked changes. Leave all existing commits on their original branch; do not cherry-pick, replay, or otherwise move them.
   - Preserve unrelated staged, unstaged, and untracked changes. If switching branches could disturb them, or this request depends on commits that would remain on the original branch, stop and ask how to proceed.
   - Choose a short, descriptive branch name and confirm it is unused locally and remotely before creating it. Never overwrite an existing branch.
3. **Implement and verify.**
   - Make only the requested changes, following repository conventions.
   - Run the focused tests and checks relevant to those changes. Fix failures caused by the changes and report unrelated failures.
4. **Group and commit the changes.**
   - Group changes by logical concern. Create separate commits for distinct concerns when each is meaningful on its own; otherwise, use one cohesive commit.
   - Stage one group at a time and review its staged diff. Include only request-specific staged, unstaged, or untracked changes; exclude unrelated changes, secrets, and generated artifacts.
   - Give each commit a clear message that follows repository conventions. Keep commit order coherent; never amend existing commits.
   - Before each commit, recheck the worktree and staged diff. If no relevant uncommitted changes remain, report that instead of recreating existing commits.
5. **Ask whether to publish.**
   - After committing all requested changes, use the ask-user tool to ask whether to push the branch and open or update a PR.
   - If the answer is unclear, ask again. Publish only after the user clearly agrees.
   - If the user declines, stop without pushing, opening a PR, or starting the review loop.
   - If the user agrees, push the branch to its configured remote. Never force-push or rewrite history. If the push is rejected or the remote branch has diverged, stop and ask how to proceed.
6. **Open or update the PR.**
   - Check whether the working branch already has a PR. If it does, update that PR rather than creating a duplicate.
   - If no PR exists, use an available PR-creation skill (such as `create-pull-request`) and follow its instructions. If none is available, use the repository's preferred tooling.
   - When updating an existing PR, use a dedicated PR skill if it supports updates; otherwise, use the repository's preferred tooling.
   - Ensure the PR title and description summarize the changes and include the verification performed. Do not merge the PR.
7. **Review and fix until ready.**
   - Start a read-only review subagent with the PR diff and relevant context. Ask it to report actionable defects introduced by the changes, citing files and lines and explaining severity and rationale.
   - If it finds actionable issues, start a separate fix subagent limited to those findings. Ask it to preserve unrelated work and report its edits and tests.
   - Inspect the fix agent's diff, run relevant checks, and verify each finding is resolved without unrelated changes. Group fixes into focused commits and push them to update the PR.
   - Request a fresh review of the updated PR diff. Repeat review, fixes, verification, commits, and pushes until no actionable issues remain and required checks pass.
   - If a subagent is unavailable, a finding cannot be fixed safely, the same finding recurs without progress, or an external check blocks readiness, stop and report the blocker. Do not claim the PR is ready without evidence.
8. **Report the outcome.**
   - Report the branch, commits, PR link, checks run, and review status. Note any pending CI, approvals, or other requirements outside your control.

## Safety

- The user's answer after committing controls publication and PR review. A yes authorizes pushing, opening or updating the PR, and pushing focused review-fix commits. A no means stop without publishing or reviewing.
- Never force-push, rewrite history, amend existing commits, or alter unrelated work. Do not merge the PR.
