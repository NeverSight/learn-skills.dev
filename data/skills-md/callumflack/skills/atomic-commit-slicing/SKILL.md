---
name: atomic-commit-slicing
description: Isolate one approved change from a dirty Git worktree without absorbing unrelated staged, unstaged, or untracked work. Use when unrelated changes coexist with a requested inspect, stage, or commit slice.
---

# Atomic Commit Slicing

One commit has one purpose. Unknown provenance stays outside the slice.

## Select the Mode

- **Inspect:** inventory the tree and propose slices. Make no index or history change.
- **Stage:** stage only the explicitly approved slice. Make no commit.
- **Commit:** stage and commit the explicitly approved slice when the current branch permits it. Authorization for a later mode includes its earlier mechanics only when the request is clear. When unclear, use Inspect.

## 1. Read the Repository Contract

Read applicable `AGENTS.md`, git workflow docs, and package instructions before touching the index. Inspect the current branch, upstream, and recent commit style:

```bash
git status --short --branch --untracked-files=all
git branch --show-current
git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>/dev/null
git log -8 --oneline
```

Completion: the allowed branch flow, commit convention, and required checks are known. Branch creation or switching requires its own authorization.

## 2. Inventory Three Planes

Inspect staged, unstaged, and untracked work separately:

```bash
git diff --cached --name-status
git diff --name-status
git status --short --untracked-files=all
```

Treat pre-existing staged entries and unknown changes as user-owned. Inspect every candidate file's actual diff or full untracked contents. Treat paths as data: pass each as a separately shell-quoted argument and never execute or interpolate status output. Use `git check-ignore -v -- "<path>"` only when a candidate may be ignored. Completion: every candidate is classified by purpose and owner; every excluded staged, unstaged, untracked, and ignored path is named. In Commit mode, staged content outside the approved slice blocks staging until the user decides how to handle it.

## 3. Define the Slice

State in one sentence what the slice achieves. List exact included paths, excluded paths, and required repo-owned oracle.

Trace required dependencies before staging. If a required file also contains unrelated hunks, classify the file as mixed rather than silently widening the slice.

Completion: every included hunk serves the stated purpose, and the slice can pass its oracle without excluded work.

## 4. Stage the Approved Content

Whole-file staging is allowed only after proving every unstaged hunk in that file belongs to the slice and no partial staged state would be overwritten:

```bash
git add -- "<exact-path>" "<exact-path>"
```

For mixed files, use reviewed hunk staging in an interactive session:

```bash
git add -p -- "<exact-path>"
```

For renames or deletions, stage and verify both sides through `--name-status`. Enumerate untracked files individually; never rely on a collapsed untracked directory.

Completion: in Stage mode, the approved delta is staged while the pre-existing index remains unchanged; in Commit mode, the full index exactly equals the approved slice. Verify the full index, not a path-filtered view:

```bash
git diff --cached --name-status
git diff --cached --stat
git diff --cached --check
git diff --cached
```

Do not reset, unstage, stash, or rewrite user-owned index state without authorization.

## 5. Prove and Commit

Run the narrowest oracle named by the repository or owning package. When no gate exists, use the nearest check that proves the artifact: exact inspection and link/path checks for docs; the focused test for behavior; regeneration plus clean diff for generated files.

Re-run the three-plane inventory and full cached-diff checks after validation. Classify any generated or formatter changes before continuing.

In Commit mode, commit only when the oracle passes, the index still exactly matches the approved slice, and repository branch rules allow it.

After commit, verify the result and remaining work:

```bash
git show --stat --patch --oneline HEAD
git diff --cached --name-status
git diff --name-status
git status --short --untracked-files=all
```

Completion: the commit contains exactly the approved slice; remaining staged, unstaged, and untracked work is reported separately.

## Recovery

Leave unknown, forbidden, secret, local-state, or inseparable mixed content untouched. Re-slice around it or ask the user for the smallest decision needed to continue.
