---
name: he9-commit
description: "Commit the current task with a Conventional Commit message (auto-links the tracked issue from the branch name). Use when the user asks to commit the current work, or to finalize and save the task in progress. Takes no argument."
license: MIT
metadata:
  opencode/autoinvoke: false
---

# Commit task

Goal: finalize the current task with a commit on the current branch.

**Invocation.** This workflow takes no argument: everything it needs comes from the working tree and the resolved project inputs below. Do not wait for an invocation target — read the task from `git status` and the diff.

**Project inputs (optional adapter).** Read `.opencode/powers.jsonc` if present; it overrides the defaults below. This skill uses: `conventions` (`openspec/conventions.md`), `specs` (`openspec/specs/*/spec.md`). Probe for paths; if one is absent, skip that step rather than guessing. `specs` is the canonical spec location to update when behavior changes.

## Step 1. Understand context

- Review `git status` and `git diff` for the currently modified files.

## Step 2. Verify

- Run the project's test suite (and the relevant integration/manual checks for scene, gameplay, or UI changes) unless there were no code changes since the last run. If the project documents a required test step in its conventions or `AGENTS.md`, use that.
- If tests fail, fix them before committing.

## Step 3. Documentation update

- If the task changes technical or runtime behavior, update the relevant canonical spec under the resolved specs glob (per the project's documentation precedence).

## Step 4. Commit changes

- Stage added/modified/deleted files.
- Derive the tracked issue reference from the branch name:
  - If the branch follows the `issue-{id}` convention, extract the number.
  - Use `Fixes #<id>` for bug fixes, `Refs #<id>` otherwise.
  - Skip the reference if the branch is not issue-based.
- Commit with a Conventional Commit message:
  1. **Format:** `feat:`, `fix:`, `docs:`, `refactor:`, `chore:`, etc.
  2. **Mood:** imperative ("Add feature", not "Added"/"Adding").
  3. **Length:** subject under 72 characters.
  4. **Issue link:** append the reference last when issue-based (`Fixes #123` / `Refs #123`).
- Do not hand-format unrelated code; the project's formatter hooks own formatting.