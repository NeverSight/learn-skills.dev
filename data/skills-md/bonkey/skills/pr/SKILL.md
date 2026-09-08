---
name: pr
description: "Create, update, and manage pull requests. Use when asked to 'create a PR', 'update PR', 'close PR', 'check PR status', 'open a pull request', '/pr', or any pull request workflow."
---

# PR

Create, update, and manage pull requests with auto-generated descriptions.

## Action Routing

Operations are combinable. If the user includes reviewers, labels, or other metadata alongside a create/update intent, create the PR first if needed, then apply the operations.

| User says                                 | Action                                     |
| ----------------------------------------- | ------------------------------------------ |
| `/pr` (no text)                           | Create or update PR (web interface)        |
| `/pr this fixes the timeout bug`          | Same, with added context for description   |
| `/pr against release/v2.x`                | PR against specified base branch           |
| `/pr close`                               | `gh pr close --delete-branch`              |
| `/pr merge`                               | `gh pr merge --squash --delete-branch`     |
| `/pr checks`                              | `gh pr checks`                             |
| `/pr status`                              | `gh pr view`                               |
| `/pr reviewers alice bob`                 | Create PR if needed, then add reviewers    |
| `/pr labels bug fix`                      | Create PR if needed, then add labels       |
| `/pr web`                                 | `gh pr view --web`                         |
| `/pr update`                              | Push + regenerate description              |
| `/pr rebase`                              | `gh pr update-branch`                      |
| `/pr context info, reviewers: alice, bob` | Create PR with context, then add reviewers |
| `/pr only swift files`                    | Restrict diff to matching paths            |
| `/pr ignore tests`                        | Drop matching paths from diff              |
| `/pr publish` / `/pr commit and push`     | Auto-commit unstaged changes, then push    |

If intent is unclear, ask.

### Path filters

Users can scope the diff with include/exclude glob patterns. Translate natural language ("only swift", "ignore generated files") into git pathspecs:

- Include → `*<pattern>` (e.g., `*.swift`)
- Exclude → `:!*<pattern>` (e.g., `:!*_test.go`)

Append them to every `git diff` / `git log` invocation in Step 1 after a `--` separator. Mention active filters in the Step 2 summary so the user can confirm.

## Core Workflow (Create / Update)

### Step 1 — Gather Context

Run these in parallel:

**Detect base branch** (in order, stop at first match):

1. User-specified base from input
2. Existing PR's base branch (if updating)
3. Git history — `git symbolic-ref refs/remotes/origin/HEAD` to get remote default, or `git config init.defaultBranch`
4. Last fallback: `gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'`

Then compute the merge base: `git merge-base HEAD <detected-base>`

**Diff and log:**

```bash
git diff --stat <base>...HEAD
git log --oneline <base>..HEAD
```

**Detect existing PR:**

```bash
gh pr list --head "$(git branch --show-current)" --state open --json number,url,title,isDraft,body,baseRefName --jq '.[0]'
```

This also fetches the existing description and base branch.

**Other context:**

- Branch name → extract ticket IDs matching `(?:^|[/_-])([A-Z]{3,}[A-Z0-9_]*-\d+)`. Deduplicate, sort, join with `,`.
- Repo template detection (first match wins):
  1. `.github/pull_request_template.md`
  2. `.github/PULL_REQUEST_TEMPLATE/` (directory — pick the most relevant file)
  3. `.gitlab/pull_request_template.md`
  4. `.gitlab/merge_request_templates/` (directory)
- Working tree state → `git status --porcelain` to detect uncommitted/unpushed changes (surface in Step 2).

### Step 2 — Summarize and Confirm

Print a summary before acting:

- **Commits:** N commits, N files changed, +N/-N lines
- **Tickets:** PROJ-123 (or "none detected")
- **Template:** repo template / default / minimal (and *why* — see auto-selection below)
- **Filters:** include=`*.swift`, exclude=`*_test.go` (omit line if none)
- **Action:** Create new PR against `<base>` or Update PR #42
- **Branch:** pushed / needs push / **N uncommitted files** / **N commits ahead of remote**

**If there are uncommitted or unpushed changes**, call them out explicitly and list the files (up to ~10). Ask the user whether to:

1. Stop and let them handle it manually, or
2. Auto-commit + push (only if the user already said `/pr publish` or similar, or confirms it now).

Then ask: "Proceed?"

### Step 3 — Generate Description

#### Rules for writing

- Follow any user-provided context verbatim.
- Focus only on important changes. Skip comments, formatting, year bumps, typos.
- A PR may contain multiple issues — describe them all, weighted by importance.
- Technical but clear language. Short sentences, prefer bullet points.
- No line-by-line analysis — high-level descriptions only.
- Never deviate from the template structure.
- Use commit messages for intent/context when the diff is ambiguous.
- Title: concise, 5–10 words, under 72 chars.
- No yapping.

#### Template selection (priority order)

1. **Explicit override** — user said something like "use the minimal template" / "use default" / "use the repo template".
2. **Auto-classify by change importance** (default when no override):
   - **minimal** — typo fixes, formatting, comments, tiny one-line bug fixes (< ~20 lines, 1–2 files).
   - **default** (built-in) — refactors, dependency bumps, moderate bug fixes.
   - **detected** — repo template from Step 1, used for significant changes, new features, breaking changes.

   Judge importance from the diff + commit messages. State the chosen template and the reasoning in the Step 2 summary.
3. **Fallback** — built-in `assets/default-template.md`.

Built-in templates live in `assets/default-template.md` and `assets/minimal-template.md`.

#### Title

- Generate a concise title (5–10 words) summarizing the main change.
- **Prefix with ticket IDs** if found in the branch name: `PROJ-123: <title>` (or `PROJ-123,PROJ-456: <title>` for multiple). Skip prefix only when no tickets were detected.
- When updating an existing PR, **keep the existing title** unless the user asks to regenerate it.

#### Body

- Focus on *why* not *what*.
- Group changes by area.
- Flag breaking changes explicitly.
- Strip any `<!-- GenAI ... -->` comments from the output.

**For updates:** always read the existing PR description first (fetched in Step 1). Preserve any user-added context, notes, or sections. Only remove content that is clearly irrelevant to the current diff (e.g., describes files/changes that no longer exist). Regenerate the auto-generated portions from the current diff.

**Large diffs (>500 lines):** use `--stat` first, selectively read the most relevant file diffs, summarize the rest from stat output.

### Step 4 — Execute

1. **Auto-commit (if requested)** — when the user opted into publish:
   - Stage only the relevant files by name (avoid blanket `git add -A`; never stage `.env`, credentials, or large binaries).
   - Generate a short conventional-commit-style message (`feat:`, `fix:`, `docs:` …) under 72 chars from the staged diff.
   - Commit, then proceed.
2. Push branch if needed: `git push -u origin HEAD`
3. Create or update:
   - **New PR:** `gh pr create --web` — **ONLY open the browser**. Do NOT pass `--title` or `--body` to `gh pr create`; those flags cause CLI creation. Print the generated title and body to the console for the user to paste in the browser. Use `gh pr create --title "..." --body "..."` only if the user explicitly asks for CLI creation.
   - **Existing PR:** `gh pr edit --title "..." --body "..."`
4. Apply any combined operations (reviewers, labels) from the user's input

**Reviewers:** before adding, check availability via `gh api`:

```bash
gh api repos/{owner}/{repo}/collaborators --jq '.[].login'
```

Warn if a requested reviewer is not a collaborator.

## Troubleshooting

- **No `gh` auth:** run `gh auth login`
- **Detached HEAD:** check out a branch first
- **No upstream remote:** `git remote add origin <url>`
- **Push rejected:** branch may need rebase — suggest `git pull --rebase origin <base>`
