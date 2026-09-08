---
name: smooth-rebase
description: "Rebases the current branch onto the repository's default branch and resolves any conflicts carefully and conservatively, asking the user whenever the correct resolution is unclear. If a rebase is already in progress, it resumes it instead of starting a new one. Use when the user asks to rebase a branch, update a branch onto main/master, fix PR conflicts, or resolve rebase conflicts."
---

# Smooth Rebase

Rebase the current branch onto the repository's default branch, resolving conflicts along the way. Preserve intent, avoid silent guesses, and ask the user whenever the correct resolution is not clearly supported by the code or surrounding context.

## Behavior

The skill follows one simple rule:

1. **If a rebase is already in progress** (conflicted or paused), do not start anything new. Resolve the current conflicts, continue the rebase, and repeat until it completes.
2. **Otherwise**, detect the repository's default branch (`main`, `master`, or whatever the remote declares), fetch it, and rebase the current branch onto it — resolving any conflicts that arise until the rebase completes.

## Scope

Use this skill when the user wants to bring a branch up to date or finish a conflicted rebase, including requests like:

- "rebase this branch"
- "rebase onto main"
- "fix PR conflicts"
- "continue the rebase and fix the conflicts"

If the user explicitly names a different base branch, rebase onto that branch instead of the default one.

## Rules

- Be conservative. Do not pick a side blindly.
- Treat conflict resolution as a semantic merge task, not a text-editing task.
- Prefer keeping both sides when they are complementary.
- Ask the user whenever the right answer depends on product intent, architecture direction, ownership, or naming/structure conventions.
- If the base branch changed structure and the feature branch changed content, do not assume which one wins. Inspect both and ask if the answer is not obvious.
- Do not discard code without being able to justify why it is obsolete or incorrect.
- Keep the final file consistent, compilable, and stylistically aligned with the surrounding code.
- Never rebase the default branch onto itself; if the current branch *is* the default branch, stop and tell the user.
- If the working tree has uncommitted changes before starting a rebase, stop and ask the user how to handle them. Do not use `git stash`.
- Rebasing rewrites history, so if a push is needed afterwards, use `git push --force-with-lease`, never a plain `--force`.

## When to ask the user

Stop and ask if any conflict involves uncertainty such as:

- base branch introduces a new structure, abstraction, or file layout
- feature branch contains business logic that no longer fits cleanly into the new structure
- both sides changed the same logic in different ways
- one side renames or moves code while the other side edits behavior
- either side may reflect a newer product decision or API contract
- conflict touches generated files, lockfiles, migrations, or large refactors where policy may vary by team

Typical questions to ask:

- "Should I preserve the structure from `main` and port this branch's behavior into it?"
- "This looks like a rename on one side and a logic change on the other. Do you want both combined?"
- "The base branch removed this code, but this branch expands it. Was the removal intentional?"

## Workflow

### 1. Determine the current state

Check whether a rebase (or another conflicted operation) is already in progress:

```sh
git status
ls .git/rebase-merge .git/rebase-apply 2>/dev/null
```

- **Rebase in progress** → skip to step 3 and resume it.
- **Merge or cherry-pick in progress** → resolve the conflicts using the same care described below, then finish with the continuation command that matches the operation (`git merge --continue` or `git cherry-pick --continue`) instead of `git rebase --continue`.
- **Clean state** → continue with step 2.

If the working tree is dirty and no rebase is in progress, stop and ask the user how to proceed. Do not stash.

### 2. Detect the default branch and start the rebase

Detect the default branch from git rather than assuming a name:

```sh
git symbolic-ref --short refs/remotes/origin/HEAD
```

If that ref is unset, resolve it first:

```sh
git remote set-head origin --auto
```

or, as a fallback, read it from the remote directly:

```sh
git ls-remote --symref origin HEAD
```

Then fetch and rebase:

```sh
git fetch origin
git rebase origin/<default-branch>
```

If the rebase completes without conflicts, report success and stop — there is nothing else to do.

### 3. Resolve conflicts, one round at a time

Each time the rebase stops on conflicts, identify the conflicted files:

```sh
git status --short
git diff --name-only --diff-filter=U
```

For each conflicted file:

- read the conflict markers in the working tree
- inspect the surrounding file for structure and intent
- inspect the base, ours, and theirs versions if needed
- look at nearby code that references the conflicted symbols

```sh
git show :1:path/to/file
git show :2:path/to/file
git show :3:path/to/file
```

During a rebase, remember that stage 2 (`ours`) is the base branch of the rebase — whatever the branch is being rebased *onto* — and stage 3 (`theirs`) is the commit from the current branch being replayed. This is the opposite of what merge intuition suggests. When this skill started the rebase, the base is the default branch; when resuming a rebase that was already in progress, identify the base from the `git status` output ("rebasing onto ...") or `.git/rebase-merge/onto` instead of assuming it is the default branch.

### 4. Classify each conflict

For each file or hunk, decide what kind of conflict it is:

- **structure vs content** — one side reorganized code, the other changed logic
- **parallel logic edits** — both sides changed behavior in overlapping lines
- **rename/move vs edit** — one side moved code, the other modified it
- **deletion vs modification** — one side removed code, the other updated it
- **mechanical conflict** — imports, formatting, generated sections, lockfiles

Mechanical conflicts can often be resolved directly.
Semantic conflicts require stronger evidence and often a user question.

### 5. Resolve only what is clear

Resolve without asking only when the correct result is strongly supported by context, for example:

- duplicate imports or trivial ordering conflicts
- both sides can be safely combined
- one side is clearly stale or mechanically superseded
- a move/rename is obvious and the behavioral change can be ported cleanly

When resolving:

- preserve all required behavior
- preserve the current architecture unless the conflicting change clearly replaces it
- rewrite the merged result cleanly instead of stitching conflict markers together line-by-line

If one or more hunks are unclear, pause and present:

- conflicted file
- short explanation of the two sides
- what you think each side is trying to do
- the concrete decision you need from the user

Keep the question specific and decision-oriented.

### 6. Continue the rebase until it completes

After resolving all conflicts in the current round:

- verify no conflict markers remain
- stage the resolved files with `git add`
- continue:

```sh
git rebase --continue
```

Repeat steps 3–6 for every round of conflicts until the rebase finishes. Do not abort the rebase unless the user asks for it.

### 7. Finalize

Once the rebase completes:

- confirm the branch history looks sane (`git log --oneline <base>..HEAD`, where `<base>` is the branch the rebase was performed onto)
- if the user asked you to update the remote branch, push with lease safety:

```sh
git push --force-with-lease
```

Do not push unless the user asked for it or the task clearly requires it (e.g. fixing PR conflicts).

## Resolution heuristics

### Prefer combining both sides when:

- one side changes API shape and the other side changes behavior using the same concept
- imports, dependencies, or registrations from both sides are needed
- a new wrapper or abstraction from base can host the branch-specific logic cleanly

### Prefer base-branch structure when:

- base introduced a broader refactor adopted across nearby files
- the feature branch's code can be ported into the new structure with little ambiguity
- keeping the old structure would reintroduce obsolete patterns

### Prefer feature-branch content when:

- it contains the feature or fix under review
- base-side changes are mostly mechanical and can be incorporated around it
- dropping it would silently remove the branch's intended behavior

These are heuristics, not automatic rules. Ask when in doubt.

## Output format

For each conflicted file, summarize:

- `file`
- `conflict type`
- `decision`
- `reason`
- `needs user input` (`yes` or `no`)

If asking the user something, end with a short numbered list of the decisions you need.

## Troubleshooting

- If conflict markers remain, search for `<<<<<<<`, `=======`, and `>>>>>>>` before continuing.
- If stage meanings are confusing during rebase, inspect the file content and commit history rather than relying on assumptions.
- If `refs/remotes/origin/HEAD` is missing, run `git remote set-head origin --auto` before detecting the default branch.
- If a commit becomes empty after conflict resolution, use `git rebase --skip` for that commit — its changes already exist on the base branch.
- If a lockfile or generated file conflicts, prefer regenerating it only when the project has a clear standard workflow and the result is deterministic.
- If a file was deleted on one side and modified on the other, do not guess whether the deletion was intentional; inspect nearby code and ask if unclear.
- If the rebase must be undone entirely, `git rebase --abort` restores the original branch state — but only do this if the user asks.
