---
name: gh-create-pr
description: "Push the current branch and create a GitHub pull request with gh CLI. Invoke explicitly as `gh-create-pr` or `$gh-create-pr`, or automatically whenever the task calls for opening or updating a pull request, even without naming the skill."
---

# GH Create PR

## Invocation

Use this skill whenever the work involves creating or updating a GitHub pull request — explicit `gh-create-pr`/`$gh-create-pr` invocation, or an ask such as "open a PR", "raise a pull request", "push this and create a PR", or "update the PR description". Prefer this skill over ad-hoc `git push` plus `gh pr create`.

Auto-invocation authorizes the read-only and local steps below (status, fetch, diff review, ancestry checks, conflict-free local rebases). It does not authorize pushing or creating the PR; those still require the confirmation in "Confirm And Create". When the user wants an unattended plan-to-PR run, use `autopilot` instead.

## Gather Context

1. Verify Git, `gh`, authentication, and a Git worktree are available.
2. Review the conversation for the purpose of the changes and completed validation.
3. Inspect the current branch, working tree, upstream, and remotes:

```sh
git status --short
git branch --show-current
git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}'
git remote -v
```

4. Establish the GitHub repository, push destination, PR base, and parent from explicit task context and repository metadata. The parent is the branch this work builds on; it may differ from the PR base. A missing upstream is allowed. Ask for confirmation whenever ambiguity cannot be resolved automatically.
5. Check for an existing open PR in the target repository before updating or pushing:

```sh
gh pr list --repo <repo> --head <branch> --state open --json number,title,baseRefName,headRefName,headRepository,headRepositoryOwner,url
```

If one exists, show its URL and stop unless the user explicitly requested another PR. For forks, verify the head repository also matches.

6. Fetch the relevant remote refs, then inspect the committed changes against the PR base:

```sh
git fetch <remote>
git log --oneline <base-ref>..HEAD
git diff --stat <base-ref>...HEAD
git diff <base-ref>...HEAD
```

- Read affected files when needed to understand architecture and behavior.
- Summarize the full committed PR diff. Uncommitted changes are excluded.
- Prefer the diff over conversation history or commit subjects when they disagree; tell the user about material differences or additional scope.
- Stop if there are no changes to propose or prerequisites are unavailable. Ask for confirmation if the checkout or repository state needs clarification.

## Update Before Creating

- Check whether the current branch lacks commits from its remote counterpart, parent, or PR base using the fetched refs. For each relevant ref, `git merge-base --is-ancestor <ref> HEAD` checks whether its commits are already included.
- If stale, automatically try to update with `git rebase <ref>`. Incorporate the remote counterpart first, then the parent and PR base as needed. Recheck ancestry after each update.
- Never use merge commits to update the branch.
- Record the starting HEAD and fetched remote head before updating. If a rebase is already in progress, ask before proceeding. If local changes prevent rebasing, ask how to handle them; do not discard, commit, or stash them automatically.
- If conflicts occur, run `git rebase --abort`, report the conflicting files, and ask for confirmation before resolving them. Do not resolve conflicts automatically.
- After updates, inspect the final diff again and run checks relevant to the updated code. Draft the description from this final state.

## Write PR Content

Keep the title brief and specific. Default to `<type>: <description>`, with `feat`, `fix`, `docs`, `ci`, `chore`, `test`, `perf`, `refactor`, or `style` as the type. Follow an active project skill's title or body format when provided.

The description should be a short list of technical changes for someone who already knows the codebase:

```md
- <code or architecture change>: <why needed and what it solves>.
- <related change>: <reason and resulting behavior>.
```

- Describe concrete changes to modules, files, APIs, data flow, or architecture, choosing the level that best explains the implementation.
- Each bullet should connect what changed with why it was needed and the problem it solves.
- Group related edits; avoid a file-by-file inventory, generic summaries, and conversation history.
- Include validation or required follow-up only when useful to the reviewer. State actual results; do not invent checks.
- Keep it brief and direct. No mandatory summary paragraph or extra sections.

## Confirm And Create

1. Default to draft. Use ready mode only when the user requests it; do not ask them to choose a mode by default.
2. Show the proposed title and full description, plus repository, head, base, push destination, and mode. Disclose any required history rewrite.
3. Ask for confirmation to push and create the PR. Do not push or create until confirmed. Fetches and conflict-free local rebases happen before this confirmation.
4. Push explicitly to the established destination:

```sh
git push -u <push-remote> HEAD:refs/heads/<remote-branch>
```

If rebasing rewrote published commits, use `--force-with-lease=refs/heads/<remote-branch>:<fetched-remote-head>` only after verifying all fetched remote work is preserved and the user confirmed the disclosed rewrite. Never use plain `--force`. If the lease fails or the remote changed, fetch and reassess; refresh the description and confirmation if the proposed changes differ.

5. Recheck for an existing PR. Write the exact approved description to a temporary file, preserving newlines. Create non-interactively with explicit arguments:

```sh
gh pr create --repo <repo> --base <base-branch> --head <head> --title "<title>" --body-file <temp-file> --draft
```

Use `<owner>:<branch>` for a fork head when required. Omit `--draft` only for requested ready mode. Never rely on editor prompts or interactive Git/`gh` defaults.

6. Report the PR URL. If the task supports PR attachments, attach the created PR.

Whenever an ambiguity cannot be resolved automatically, ask the user for confirmation before the dependent action.
