---
name: gh-cli-flow
description: GitHub workflow rules and Conventional Commits. Use for all git
  commits, PRs, addressing review feedback, fixing PR comments, CI checks, and
  any gh CLI work. Load this skill FIRST -- it governs how gh commands are used
---

# GitHub CLI Coding Flow

**Primary skill for all GitHub workflows and git commits.** This skill defines the rules: commit message format (Conventional Commits), PR workflows, review feedback handling, and CI queries. When both this skill and `gh-cli` are loaded, this skill's rules take priority. For the full `gh` command reference, install the companion skill:

```bash
npx skills add github/awesome-copilot --skill gh-cli
```

## When to Use

**Load this skill before any GitHub or git commit workflow.** Do not improvise -- follow these patterns instead of guessing at `gh` command sequences or commit message formats. When `gh-cli` is also loaded, this skill takes priority for workflow decisions.

- **Making any commit** -- this skill defines the required Conventional Commits format for all commit messages and PR titles
- **Creating PRs or branches** -- PR title format, draft workflows, and fill patterns
- **Addressing PR review feedback** -- "fix PR comments", "address review", "handle feedback", "resolve review threads"
- **Responding to code review** -- evaluating reviewer comments, replying, resolving threads
- **Checking PR/CI status** -- review state, merge readiness, failing checks, pending reviewers
- **Posting comments on PRs** -- line-specific comments, thread replies, review submissions
- **Querying GitHub data** -- `gh pr`, `gh issue`, `gh run`, `gh workflow`, `gh search`, `gh api` patterns
- **Configuring tool allowlists** -- auto-approval patterns for read-only `gh` commands

## Critical Rules

1. **This skill overrides default git/GitHub behavior.** When this skill is loaded alongside `gh-cli` or other references, follow this skill's workflow patterns, commit format, and review handling rules. Do not fall back to default `git commit` or `gh` patterns.
2. **Prefer `gh` subcommands over raw `gh api` when a subcommand exists.** Subcommands handle pagination, error formatting, and repo detection automatically. Only use `gh api` for operations not covered by subcommands (line-specific PR comments, review thread resolution, GraphQL queries).

---

## Read-Only vs Write Classification

All `gh` commands fall into two categories:

- **Read-only** (safe to auto-approve): `view`, `list`, `status`, `diff`, `checks`, `search`, `workflow list`
- **Write** (require user approval): `create`, `edit`, `merge`, `close`, `reopen`, `comment`, `review`, `run rerun`, `run cancel`, `workflow run`

See `references/allowlist.md` for copy-paste ready auto-approval patterns.

---

## PR Review Comment Handling

When asked to "address review comments", "fix PR feedback", "handle review", "resolve PR threads", "check PR comments", or "respond to reviewers":

> **Reference**: See `references/pr-comment-workflow.md` for the full opinionated workflow -- fetch unresolved threads, evaluate each comment critically, fix/reply/resolve.

Quick summary:
1. Fetch unresolved review threads (GraphQL query)
2. For each thread: read the code context, check if already addressed
3. Decide: fix code + reply + resolve, or reply with evidence + resolve, or leave for discussion
4. Don't blindly agree -- validate comments against actual code and conventions

---

## Conventional Commits

**All commit messages must follow [Conventional Commits](https://www.conventionalcommits.org/).** This is non-negotiable -- every commit, every PR title.

### Format

```
<type>(<optional scope>): <description>

[optional body]

[optional footer(s)]
```

### Types

| Type | When |
|---|---|
| `feat` | New feature or capability |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, whitespace, semicolons (no logic change) |
| `refactor` | Code change that neither fixes a bug nor adds a feature |
| `perf` | Performance improvement |
| `test` | Adding or updating tests |
| `build` | Build system or external dependencies |
| `ci` | CI/CD configuration |
| `chore` | Maintenance tasks, tooling, config |

### Rules

1. **Type is required** -- never commit without a type prefix
2. **Scope is optional** but encouraged for multi-module repos: `feat(auth): add OAuth2 flow`
3. **Description is lowercase**, imperative mood, no period: `fix: handle null response` not `Fix: Handled null response.`
4. **Breaking changes** use `!` after type/scope: `feat(api)!: remove v1 endpoints`
5. **PR titles follow the same format** -- squash merges use the PR title as the commit message
6. **No `Co-Authored-By` trailer** -- never add it to commit messages

### Examples

```bash
git commit -m "feat: add user profile page"
git commit -m "fix(auth): prevent token refresh race condition"
git commit -m "docs: update API reference for v2 endpoints"
git commit -m "refactor(db): extract connection pooling logic"
git commit -m "feat(api)!: change response format for /users"
```

### PR Titles

```bash
gh pr create --title "feat: add dark mode support" --body "..."
gh pr create --title "fix(payments): correct decimal rounding" --body "..."
```

---

## Common PR Workflows

**Create PR from current branch:**
```bash
gh pr create --draft --fill
```

**Quick review cycle:**
```bash
gh pr checks 123 --watch           # Wait for CI
gh pr diff 123 --stat              # Review scope
gh pr view 123 --json reviews      # Check review state
gh pr merge 123 --squash --delete-branch
```

**Find PRs needing review:**
```bash
gh pr list --search "review-requested:@me"
gh pr list --search "review:required -review:approved draft:false"
```

**Check workflow runs for a specific workflow:**
```bash
gh workflow list --json name,id --jq '.[] | "\(.id) \(.name)"'
gh run list --workflow ci.yml --limit 5 --json status,conclusion,headBranch
```

---

## Line-Specific PR Comments

Line comments require `gh api` -- no subcommand exists for this.

> **Reference**: See `references/line-comments.md` for full `gh api` patterns: single-line comments, multi-line ranges, replies to threads, edit/delete.

Quick reference:
```bash
# Single-line comment on latest commit
gh api repos/{owner}/{repo}/pulls/{pr}/comments \
  -f body="Comment" -f path="src/file.ts" -F line=42 -f side=RIGHT

# Reply to a review comment thread
gh api repos/{owner}/{repo}/pulls/{pr}/comments/{comment_id}/replies \
  -f body="Reply text"
```

---

## Review State & CI Queries

> **Reference**: See `references/review-queries.md` for advanced queries: full review state summary, pending reviewer detection, merge readiness assessment, PR metadata extraction.

Quick patterns:
```bash
# Who approved / requested changes
gh pr view 123 --json reviews --jq '.reviews | group_by(.author.login) | map({user: .[0].author.login, latest: .[-1].state})'

# Files changed with additions/deletions
gh pr view 123 --json files --jq '.files[] | "\(.additions)+/\(.deletions)- \(.path)"'
```

---

## Read-Only gh api Endpoints

When a subcommand doesn't exist, use `gh api` for read-only access.

> **Reference**: See `references/api-readonly.md` for the full list of read-only REST and GraphQL endpoints (PR data, issue timelines, review threads).

---

## Allowlist Reference

> **Reference**: See `references/allowlist.md` for copy-paste ready `Bash(command:*)` patterns covering all read-only operations -- safe to auto-approve in Claude Code `settings.json` or OpenCode config.
