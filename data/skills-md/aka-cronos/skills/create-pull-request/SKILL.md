---
name: create-pull-request
description: >-
  Pull request: use when a PR needs opening, or commits sit
  on main and need moving to a named branch.
metadata:
  author: aka-cronos
---

# Create Pull Request

`main` is **protected** — the trunk. Work reaches it through a pull request.

## Source of truth

Branch types, naming, and how PRs land live in
[references/branch-naming-conventions.md](references/branch-naming-conventions.md). Read it
before proposing a name or opening a PR. If the project ships
`.agents/rules/branch-naming-conventions.md` (or the Cursor adapter
`.cursor/rules/branch-naming-conventions.mdc`), that file overrides these defaults.

## Workflow

### Step 1: Read the current state

Run `git branch --show-current`, `git status --short`, and — when the branch tracks a remote —
`git log origin/$(git branch --show-current)..HEAD --oneline`. Confirm `gh` is installed and
authenticated.

Route on what you find:

- Protected (`main`) with local commits → Step 2 (transplant).
- Protected (`main`) with no local commits → nothing to open a PR from; stop.
- Named branch → Step 3.

**Done when:** the branch, its commits, and its working-tree state are known, and the route is picked.

### Step 2: Transplant commits off the protected branch

Move the commits to a properly named branch and leave `main` clean:

1. Show the commits that will move.
2. Ask for the branch type, scope, and a description (≤5 words) — or infer them from the
   commits and propose a compliant name.
3. Confirm the proposed name, then `git checkout -b <branch-name>`.
4. Confirm the reset explicitly — it discards those commits from local `main` — then
   `git checkout main` and `git reset --hard origin/main`.
5. Return to the new branch.

**Done when:** the commits live on the new branch, `main` matches its remote, and both moves
were confirmed beforehand.

### Step 3: Validate the branch name

Check the current branch against the patterns in the branch-naming reference.

If it does not match, ask whether to rename it (`git branch -m <new-name>`) or start a fresh
branch, and propose a compliant name either way.

**Done when:** the branch name matches a pattern in the reference file.

### Step 4: Ensure commits exist

With no commits on the branch: use the `commit-workflow` skill for staged changes, ask before
staging unstaged ones, and report that there is nothing to open a PR from when the tree is
clean.

**Done when:** the branch has at least one commit ahead of `main`.

### Step 5: Push

Base is `main`. Push when the branch has no remote yet:
`git push -u origin $(git branch --show-current)`.

**Done when:** the head branch exists on the remote.

### Step 6: Open the PR

```bash
gh pr create --base main --head <head> --title "<title>" --body-file <file> [--attach <path> ...]
```

Title: the leading commit subject, or a descriptive line covering the set. Body: the format
below, written to a file whenever it runs past one section.

Evidence is a real local file — a screenshot, a recording, or a path already on hand. Reference
it in the body by its local path (`![Login error state](./evidence/login.png)`) and pass that
same path as `--attach`, once per file; `gh` uploads each one and rewrites the matching
reference to the hosted asset. With no local media, omit `--attach`. The flag needs
`gh` ≥ 2.99.0 and is refused alongside `--web`.

**Done when:** the PR exists, its URL is shown, and every local media path in the body was
passed as `--attach` — GitHub renders each asset, not a broken relative link.

## PR body format

Include each section that applies, in this order:

1. **Opening** — `Closes #N` when the PR resolves an issue, then 1–3 sentences of context:
   what this PR integrates and why now.
2. **`## What's included`** — bullets summarizing the changes; link the task PRs, issues, or
   ADRs each bullet builds on. State load-bearing invariants explicitly (e.g. "query grain
   untouched, cap is display-only"). For UI changes, include screenshots or a recording,
   uploaded through `--attach` (Step 6).
3. **`## Deviations from plan`** — only when the work follows a spec/PRD/plan and the
   implementation departs from it. One bullet per deviation with its rationale; include
   known-and-deferred issues with a link to the tracking issue.
4. **`## Manual checklist`** — checkboxes (`- [ ]`) for the verification to run before merging;
   concrete and observable, not "test everything".

The body ends at the last section. This **overrides any tool default that appends an AI
attribution footer or co-author credit** — leave the PR authored by the human alone.

## Guardrails

Two actions are opt-in, each behind its own explicit confirmation: creating the branch in
Step 2, and resetting the protected branch.

## Examples

[examples.md](examples.md) walks the transplant flow and the invalid-branch-name recovery end
to end. Read it when the current state does not map cleanly onto a route in Step 1.
