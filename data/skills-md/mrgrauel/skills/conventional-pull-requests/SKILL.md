---
name: conventional-pull-requests
description: Create pull requests with Conventional Commit-style titles and template-compliant descriptions using GitHub CLI. Use when asked to create, open, draft, or update a PR from the current branch and the team expects consistent semantic titles and structured PR bodies.
---

# Conventional Pull Requests

## Goal

Create pull requests with:

- a Conventional Commits style title
- a body that follows the repository PR template
- concise, accurate change context derived from the actual diff

## Workflow

1. Inspect branch and commit context.
   - Run `git status --short`, `git log --oneline --decorate -n 20`, and identify the current branch.
   - Determine the default base branch with `gh repo view --json defaultBranchRef -q '.defaultBranchRef.name'`.
   - Review diff scope with `git diff --name-status origin/<base>...HEAD`.
2. Confirm there is meaningful committed work for a PR.
   - If there are only uncommitted changes, ask whether to create commits first.
3. Find and read the PR template before drafting.
   - Check `.github/pull_request_template.md`, `.github/PULL_REQUEST_TEMPLATE.md`, and `.github/PULL_REQUEST_TEMPLATE/*.md`.
4. Draft a conventional title.
   - Format: `<type>[optional-scope]: <description>`
   - Use standard types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `build`, `ci`, `perf`, `style`, `revert`.
   - Keep description imperative and specific.
5. Draft the PR body from the template.
   - Fill all required sections with concrete details from the diff.
   - Include testing notes and risk notes when relevant.
   - Generate a comprehensive PR body with a summary, key changes, architecture benefits if necessary, technical details, and testing information.
6. Push the branch if needed.
   - Run `git push -u origin <branch>` when the branch has no upstream or local commits are not yet pushed.
7. Create the PR with GitHub CLI.
   - Use `gh pr create --base <base> --head <branch> --title "<title>" --body-file <file>`.
   - Use `--draft` only when explicitly requested.
8. Return the PR URL and a short summary of title/body decisions.

## Rules

- Do not invent changes; use only facts from the branch diff and commits.
- Ask one focused clarification when required template fields cannot be inferred.
- Prefer a small, clear PR description over verbose narrative.
