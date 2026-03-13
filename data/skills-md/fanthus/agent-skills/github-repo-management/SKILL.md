---
name: github-repo-management
description: Create and manage GitHub repositories, branches, commits, and PRs via local git commands and GitHub MCP. Use when the user asks to create a repo, push code, get repo info, manage branches, open PRs, or work with GitHub repositories.
---

# GitHub Repository Management

## Rules

- **Secrets**: Do not echo, log, or include any token or secret in output, commands, or file contents. GitHub MCP handles auth.
- **Destructive actions**: Ask for confirmation before `git push --force`, `git branch -D`, deleting a repo, or overwriting remote history.
- **Default branch**: Prefer `main`; use `master` only when the repo already uses it.
- **Commits**: Use [Conventional Commits](https://www.conventionalcommits.org/) (e.g. `feat:`, `fix:`, `docs:`).

## Capabilities

- Run git commands locally (init, add, commit, push, branch, checkout, etc.).
- Operate on GitHub via **GitHub MCP** only: create repos, get repo info, list/create/merge PRs, manage branches. Do not use REST API or GITHUB_TOKEN directly.

---

## Create a repo

When the user asks to "create a repo" or "create a GitHub repository":

1. **Create on GitHub** (GitHub MCP only):
   - Use GitHub MCP `create_repository` (or equivalent) with `name`, optional `description`, `private` (default from user intent).

2. **Set origin locally** (if already in a git repo):
   ```bash
   git remote add origin https://github.com/<owner>/<repo>.git
   ```
   If `origin` exists and should point to the new repo, ask before changing it.

3. **If no local repo yet**:
   ```bash
   git init
   git remote add origin https://github.com/<owner>/<repo>.git
   ```

4. **First push** (after at least one commit):
   ```bash
   git push -u origin main
   ```
   Use `main` unless the GitHub repo was created with a different default branch.

---

## Push code

When the user asks to "push code" or "push to GitHub":

1. **Ensure git repo exists**: Run `git status`. If not a repo, ask whether to `git init` and set remote.
2. **Check remote**: `git remote -v`. If no `origin`, ask for repo URL or create repo first.
3. **Commit cleanly**:
   - `git status` to see changes.
   - Stage: `git add <paths>` or `git add -A` if user intends all changes.
   - Commit with a conventional message: `git commit -m "type(scope): description"`.
   - If there are uncommitted changes and user said "push", offer to commit first; do not force-push without asking.
4. **Push**: `git push origin <branch>`. Default branch is `main`. If upstream not set: `git push -u origin main`.

---

## Get repo info

When the user asks to "get repo info", "repo details", or "show repository":

1. **Identify repo**: From `git remote get-url origin` (owner/repo) or user-provided owner/name.
2. **Fetch via GitHub MCP**: Use MCP tools to get repository details (e.g. get repo, list branches, list PRs). Summarize: name, description, default branch, visibility, stars/forks if available, clone URL.

---

## Branches

- **Create branch**: `git checkout -b <branch-name>` then push: `git push -u origin <branch-name>`.
- **Switch branch**: `git checkout <branch>` or `git switch <branch>`.
- **Delete branch**: Local `git branch -d <branch>`; remote delete only after user confirmation: `git push origin --delete <branch>`.

---

## Pull requests

- **Open PR**: Use GitHub MCP to create a pull request (`head`, `base` default `main`, `title`, `body`).
- **List PRs**: Use GitHub MCP to list PRs; summarize by number, title, state, author.
- **Merge**: Use GitHub MCP to merge; confirm with user before merging.

---

## Conventional commit messages

Use this format: `type(scope): short description`.

| Type     | Use for                    |
|----------|----------------------------|
| `feat`   | New feature                |
| `fix`    | Bug fix                    |
| `docs`   | Documentation only         |
| `style`  | Formatting, no code change |
| `refactor` | Code change, no feature/fix |
| `test`   | Adding or updating tests   |
| `chore`  | Build, tooling, deps       |

Examples:
- `feat(auth): add login endpoint`
- `fix(api): correct date parsing`
- `docs: update README setup steps`

---

## Summary checklist

- GitHub operations: GitHub MCP only (no REST API, no GITHUB_TOKEN in commands).
- Confirm before force push, branch delete, or repo delete.
- Default branch: `main`.
- All commits: conventional style.
