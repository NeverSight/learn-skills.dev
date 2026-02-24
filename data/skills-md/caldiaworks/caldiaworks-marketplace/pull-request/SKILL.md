---
name: pull-request
version: 0.3.0
description: "Create GitHub pull requests with readiness checks, auto-drafted titles and descriptions, and remote push handling. Use when: create PR, pull request, open PR, submit PR, create pull request, PR for review, push and PR, pull-request, /pull-request."
---

# Pull Request Creation

Create a GitHub pull request for the current branch. Works in any Git repository with GitHub as the remote.

Pull requests are created at the user's discretion -- this skill is never triggered automatically after commits.

## Workflow

### Step 1: Readiness Check

Verify the branch is ready for a pull request.

1. Check that the current branch has commits ahead of the base branch using `git log <base>..HEAD`.
2. If there are no commits ahead, inform the user there is nothing to create a PR for and stop.
3. If the current branch is not pushed to the remote, push it with tracking: `git push -u origin <branch>`.
4. Check if a PR already exists for the current branch using `gh pr view`. If one exists, display the existing PR URL and ask the user whether to update it or abort.

### Step 2: Draft and Create PR

Generate a title and body from the commit history, then create the PR.

1. Display the commit log between the base branch and HEAD: `git log --oneline <base>..HEAD`.
2. Display the full diff: `git diff <base>...HEAD`.
3. Draft a PR title (under 72 characters) and body:
   - Title: concise summary of the changes in imperative form
   - Body: structured summary with sections as appropriate
   - Follow repository conventions if visible from recent PRs
4. Create the pull request:
   ```bash
   gh pr create --title "<title>" --body "$(cat <<'EOF'
   <body>
   EOF
   )"
   ```
5. Display the PR number and URL.

### Error Handling

If PR creation fails, display the error message returned by `gh pr create`.

## Before Finishing

After creating the PR, review it from a reviewer's perspective:

- **Understandable?** Can a reviewer who has no context about the conversation understand what this PR does and why, from the title and body alone?
- **Complete?** Does the diff include all intended changes? Check `git status` for unstaged changes that may have been missed.

## Constraints

- Do not merge the PR -- creation only.
- Do not force-push or rebase without explicit user request.
- The base branch defaults to the repository's default branch unless the user specifies otherwise.
