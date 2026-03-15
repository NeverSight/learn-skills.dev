---
name: smart-rebase
description: Help the user safely rebase a feature branch onto `main`, `develop`, or another target branch while preserving feature behavior through conflicts. Use this skill whenever the user asks to rebase or update a long-lived branch, replay a feature onto a newer base, or resolve rebase conflicts after refactors, renamed APIs, moved files, typing changes, or new conventions on the target branch.
---

# Smart Rebase

Use this skill to move a feature branch onto a newer target branch without flattening away the feature's intent.

The point is not only to make `git rebase` finish. The point is to preserve the business logic from the feature branch while adapting it to the architecture and conventions that now exist on the target branch.

## Inputs

- `target branch`: default to `main` unless the user names another branch.
- `source branch`: default to the current branch unless the user names another branch.

If the user only says "rebase my branch", infer the source branch from `git branch --show-current`.

## Safety Rules

1. Check `git status --short` before rebasing.
2. If the working tree is dirty, stop and tell the user a rebase would be risky until they stash or commit the changes.
3. Create a safety branch before rewriting history.
4. Never resolve conflicts by blindly taking "ours" or "theirs" for the whole file unless the diff clearly proves one side is obsolete.
5. Never force-push automatically. If the rebase succeeds and the branch is already published, tell the user to review the result and then use `git push --force-with-lease` themselves.

## Workflow

### 1. Identify the branches

1. Determine the source branch.
2. Determine the target branch.
3. Confirm both branches exist locally before proceeding.

Useful commands:

```bash
git branch --show-current
git branch --list
git status --short
```

### 2. Find the merge base

Run:

```bash
git merge-base <target_branch> <source_branch>
```

Capture the result as `BASE_COMMIT`.

This commit is the shared starting point for both lines of work. Every later comparison should be anchored to it.

### 3. Analyze the feature branch

Run:

```bash
git diff <BASE_COMMIT>..<source_branch>
```

Read this diff to understand:

- what the feature adds or changes
- which files carry the core business logic
- what assumptions the feature makes about APIs, file layout, naming, and types

Summarize the feature in plain language before rebasing. If you cannot explain what the feature is trying to do, you are not ready to resolve conflicts well.

### 4. Analyze target-branch changes

Run:

```bash
git diff <BASE_COMMIT>..<target_branch>
```

Read this diff to spot:

- refactors that moved code to new files or modules
- renamed functions, types, props, or variables
- changed interfaces, signatures, schemas, or typing rules
- new architectural conventions, helper layers, or validation patterns
- deleted code that the feature used to touch

Write a short "risk map" of what is likely to conflict before starting the rebase.

### 5. Prepare a safety branch

Run:

```bash
git checkout <source_branch>
git checkout -b <source_branch>_rebased
```

Work on the safety branch, not directly on the original source branch.

### 6. Start the rebase

Run:

```bash
git rebase <target_branch>
```

If the rebase stops on conflicts, resolve them commit by commit.

### 7. Resolve conflicts intelligently

For each conflicted file:

1. Read the conflict markers and the surrounding code.
2. Compare the file to both:
   - the feature diff from `BASE_COMMIT..source_branch`
   - the target diff from `BASE_COMMIT..target_branch`
3. Preserve the feature's intent.
4. Rewrite that intent using the target branch's current architecture.

When resolving, prefer these patterns:

- If the target branch renamed a function used by the feature, update the feature code to the new name.
- If the target branch changed a function signature, adapt the feature call sites instead of restoring the old signature.
- If the target branch moved logic into a new module or service, port the feature to the new location.
- If imports changed, keep the target branch import structure and reattach the feature logic to it.
- If types, schemas, or validation became stricter, update the feature to satisfy the new contract.
- If both branches edited the same condition or algorithm, merge the intent explicitly instead of keeping one side wholesale.
- If the target branch deleted obsolete code, do not resurrect it just because the feature used it earlier.

Useful commands while resolving:

```bash
git status
git diff
git diff --ours -- <path>
git diff --theirs -- <path>
git add <path>
git rebase --continue
```

If a resolution is unclear, explain the tradeoff and ask the user before continuing.

### 8. Verify after each meaningful resolution

After resolving conflicts, verify the adapted code is internally consistent.

At minimum:

```bash
git diff --check
```

Also inspect for:

- broken imports
- stale names from the pre-refactor code
- mismatched types or interfaces
- duplicated logic introduced during manual merges
- references to files or symbols that no longer exist on the target branch

If the repository has a small, relevant test or lint command and it is safe to run, run it before declaring success.

### 9. Final review

After the rebase completes:

1. Inspect the resulting diff against the target branch.
2. Confirm the feature still exists functionally.
3. Confirm the code now matches the target branch conventions.
4. Summarize what changed during conflict resolution.

Useful command:

```bash
git diff <target_branch>...HEAD
```

## Response Format

When reporting back to the user, keep the response structured like this:

1. `Base commit`: the merge base hash used for analysis.
2. `Feature intent`: what the source branch was trying to accomplish.
3. `Target changes`: the main architectural or API changes discovered on the target branch.
4. `Conflict plan` or `Conflicts resolved`: what had to be adapted and why.
5. `Verification`: checks run and their outcome, or what still needs verification.
6. `Next step`: whether the rebase can continue, is complete, or needs user input.

## Example

User request:

```text
Rebase feature/bulk-edit-users onto main and keep the new validation flow that landed on main.
```

Good behavior:

1. Find the merge base between `main` and `feature/bulk-edit-users`.
2. Read the feature diff to understand bulk edit behavior.
3. Read the `main` diff to understand the new validation flow.
4. Create `feature/bulk-edit-users_rebased`.
5. Rebase onto `main`.
6. During conflicts, keep the bulk edit behavior but route it through the new validation layer instead of restoring the old flow.
7. Verify imports, types, and any touched tests before finishing.

The skill succeeds when the resulting branch behaves like the feature branch, but looks like it was implemented against the current target branch from the start.
