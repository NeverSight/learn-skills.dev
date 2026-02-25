---
name: empower-sync
description: Sync a commit from the gemini remote into sync-upstream for empower-site.
---

# Empower Sync

Use this skill to cherry-pick a single commit from the `gemini` remote into `sync-upstream` for the empower-site project.

## Inputs

- Require a commit SHA. If missing, ask for it.
- Remote is `gemini`.

## Safety Rules

- Stop if the working tree is dirty.
- Ask before resetting or recreating `sync-upstream`.
- Do not cherry-pick until the user approves after reviewing the diff.

## Workflow

1. **Preflight**
   - `git status --porcelain`
   - If not clean, stop and ask to commit or stash.

2. **Fetch remote**
   - `git fetch gemini`

3. **Prepare sync-upstream**
   - Confirm before resetting `sync-upstream` to the default branch.
   - `git checkout <default-branch>`
   - `git pull origin <default-branch>`
   - `git branch -f sync-upstream <default-branch>`
   - `git checkout sync-upstream`

4. **Dry-run review**
   - `git show <sha> --stat`
   - `git show <sha> -p`
   - Summarize files and risks.
   - Ask for approval to apply.

5. **Apply**
   - `git cherry-pick <sha>`

6. **Conflict handling**
   - If conflicts, list them and ask how to resolve.
   - Use `git cherry-pick --continue` after resolution.

7. **Report**
   - Show recent log and `git status`.
   - Confirm the branch is ready for review/testing.
