---
name: create-pr
description: Create a pull request by branching from the default branch, committing changes with a signed commit, and pushing.
argument-hint: "[description of the changes]"
allowed-tools: Read, Glob, Grep, Bash(git checkout *), Bash(git switch *), Bash(git branch *), Bash(git add *), Bash(git commit *), Bash(git diff *), Bash(git status *), Bash(git log *), Bash(git remote *), Bash(git rev-parse *), Bash(gh pr create *)
---

# create-pr

Create a branch, commit staged changes with a signed commit, and push to open a pull request.

## When to use

- When the user asks to create a pull request
- When the user wants to commit and push their changes as a PR
- When the user runs `/create-pr`

## Instructions

1. **Identify the default branch**:
   - Run `git remote show origin` or check `git symbolic-ref refs/remotes/origin/HEAD` to determine the default branch (e.g., `main` or `master`).

2. **Review the current changes**:
   - Run `git status` and `git diff` to understand what has been modified.
   - If there are no changes, inform the user and stop.

3. **Create a descriptive branch name**:
   - Based on the changes (file names, content of diffs), generate a short, descriptive branch name.
   - Use kebab-case (e.g., `fix-login-validation`, `add-user-api-endpoint`, `refactor-config-loader`).
   - Prefix with a category when appropriate: `fix/`, `feat/`, `refactor/`, `docs/`, `chore/`.
   - Keep it concise (3-5 words max after the prefix).

4. **Create the branch from the default branch**:
   - Run `git switch -c <branch-name>` from the default branch.

5. **Stage and commit**:
   - Stage the relevant files with `git add`.
   - Write a commit message in **English** that clearly describes the **intent** of the changes, not just what files were modified.
   - Use the conventional commit format: `<type>: <description>` (e.g., `feat: add user authentication endpoint`).
   - The commit body should explain **why** the change was made if the reason is not obvious from the subject line.
   - Always create a **signed commit** using `git commit -s -S` (`-s` for Signed-off-by, `-S` for GPG signature).

6. **Push the branch**:
   - **Verify that the current branch is NOT the default branch.** If it is, abort and inform the user.
   - Run `git push -u origin <branch-name>`.

7. **Create the pull request**:
   - Use `gh pr create` to open a pull request.
   - Set the title to match or closely reflect the commit message subject.
   - Write a PR description that summarizes the changes and their intent.
   - Target the default branch.

## Important notes

- The `git push` command is NOT in the allowed-tools list intentionally. The user will be prompted by the tool permission system when push is executed.
- **NEVER push to the default branch directly.** Always push to the feature branch.
- Always use signed commits (`git commit -s -S`): `-s` adds Signed-off-by, `-S` adds GPG signature.
- Commit messages must be in English.
- Focus on the **intent** of changes in commit messages, not just listing modified files.
