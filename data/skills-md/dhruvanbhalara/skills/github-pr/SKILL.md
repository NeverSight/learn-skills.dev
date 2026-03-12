---
name: github-pr
description: Pull Request Creation & Management
metadata:
    platforms: "cross-platform"
    languages: "generic"
    category: "git"
---

# Pull Request Creation & Management

This skill automates the process of creating high-quality Pull Requests using the GitHub CLI (`gh`) or providing instructions if it's unavailable.

## 1. Preparation
- **Check GitHub CLI**: Verify if `gh` is installed and authenticated (`gh auth status`).
- **Commits Check**: Ensure all changes are committed in the current feature branch.
- **Base Branch**: Identify the target base branch (usually `main`).

## 2. PR Quality & Metadata
- **Quality Gate**: All PRs MUST pass analysis (0 warnings), formatting, and tests before merge.
- **Branch Protection**: Ensure branch protection rules are respected (no direct pushes to `main`).
- **Metadata**: ALWAYS specify relevant labels and at least one assignee.
- **Checklist**: Ensure the development plan and requirements are reviewed before completing the task.

## 3. Generate PR Title
- **Conventional Commits**: The PR title MUST follow the pattern: `<type>(<scope>): <description>`.
    - Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`.
    - Example: `feat(auth): add google sign-in support`
- **Source**: Analyze the commit messages in the current branch to determine the most appropriate title.

## 3. Generate PR Description
- **Commit History**: Read all commits in the current branch (`git log origin/main..HEAD --oneline`).
- **PR Template**: Check for `.github/PULL_REQUEST_TEMPLATE.md` or similar. If it exists, populate it.
- **Content**:
    - Summarize the "What" and "Why" of the changes.
    - List the specific changes as bullet points.
    - Include any relevant issue numbers (e.g., `Closes #123`).

## 4. Labeling & Assignment
- **Available Labels**: Fetch labels from the repo (`gh label list`).
- **Auto-Label**: Assign labels based on the changes:
    - `enhancement` / `feat`: For new features.
    - `bug` / `fix`: For bug fixes.
    - `documentation` / `docs`: For documentation updates.
- **Assignee**: Assign the PR to the current user or as per project rules.

## 5. Execution
- **Using CLI**: If `gh` is available, run:
  ```bash
  gh pr create --title "<title>" --body "<body>" --label "<labels>"
  ```
- **Manual Fallback**: If `gh` is NOT available, present the generated title, description, and suggested labels to the user and ask how to proceed.
