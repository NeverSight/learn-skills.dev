---
name: clean-branch
description: Extract the essential feature changes from mixed committed and working-tree work into a new branch. Use when the user asks for a clean branch or a minimal feature branch; use recommit instead when only the commit history should change.
---

# Clean branch

Build the smallest complete feature diff on a fresh branch, preserving the source
branch, index, and working files. This changes the selected content; it is not a
history-only cleanup.

## Identify the feature and base

Infer the intended behavior and scope from the request, conversation, and relevant
issue or PR. Inspect the actual committed diff, staged and unstaged changes, and
untracked files. Record the source HEAD and status before extraction. If multiple
features are equally plausible, ask which one to extract before creating a branch.

Use the user's chosen base, otherwise the current PR's base, otherwise the
repository's default branch. Resolve it to a commit; refresh a remote-tracking ref
when possible and disclose any freshness limitation. If no base can be established,
ask rather than guessing. Inspect source changes since the merge base, but create
the destination at the selected base tip so newer base changes survive.

## Extract in a separate worktree

Create a new branch with the provided name or a descriptive unused name. Use
`git-wt` when available, otherwise `git worktree add`. Keep the source untouched;
apply edits only in the destination. Inspect worktree copy settings so ignored or
unrelated working files are not carried over automatically.

Select changes by feature dependency, not by whole commit or file. Mixed hunks may
need to be reimplemented against the destination. Include the integration,
dependencies, generated files, documentation, and tests the feature actually needs.
Leave unrelated refactors, formatting, experiments, and speculative work behind.
Resolve extraction conflicts against the intended behavior and current base;
copying a source file wholesale must not erase newer base changes.

Use clear names, simple control flow, and existing patterns. Keep comments that
explain non-obvious intent or constraints. Limit cleanup to the extracted change.

## Verify and hand off

Review the complete destination diff against the recorded base, including new files.
Run relevant feature tests and repository-required checks in the destination.
Verify the original requirements end to end; when performance or quality matters,
compare the relevant behavior with the source and state what was actually measured.
Fix failures introduced by extraction and report any unverified requirements.

Confirm that the source HEAD, index, and working files remain unchanged. Report the
destination branch, base commit, worktree path, what was kept or omitted, and check
results. Leave the extracted changes uncommitted unless committing is requested or
already authorized; the same authorization rule applies to pushing or opening a PR.
