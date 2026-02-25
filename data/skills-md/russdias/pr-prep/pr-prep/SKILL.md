---
name: pr-prep
description: >
  Use when preparing a pull request, crafting commit messages, or summarizing
  code changes for review. Triggers on tasks like "prepare my PR", "write a
  commit message", "summarize my changes", "generate PR description", or
  before pushing a feature branch.
---

# PR Prep

Analyze code changes on the current branch and generate ready-to-use PR
titles, commit messages, and PR descriptions.

## When to Use

- User asks to prepare, describe, or summarize a pull request
- User wants a commit message for staged or recent changes
- User says "what changed", "summarize my diff", or "review my changes"
- Before pushing a feature branch for review

Do NOT use when:
- There are no code changes (clean working tree and no branch commits)
- User is asking about a *remote* PR they didn't author (use `gh pr view` instead)

## Workflow

1. **Check the current branch** — run `git rev-parse --abbrev-ref HEAD`.
   If the user is on the default branch (`main`, `master`, etc.) and has
   uncommitted changes, suggest an appropriate branch name before proceeding:
   - Format: `<type>/<short-description>` (e.g. `feat/add-rate-limiting`,
     `fix/login-redirect-loop`)
   - Derive the name from the changes, not generic placeholders
   - Ask the user to create the branch before continuing

2. **Gather context** — determine the base branch (usually `main`) and run:
   - `git diff <base>...HEAD` to see all changes on the branch
   - `git diff --stat <base>...HEAD` for a summary of files changed
   - `git log --oneline <base>..HEAD` for commit history on this branch
   - `git diff` and `git diff --cached` for any uncommitted work
   - `git log --oneline -20 <base>` to see recent commit messages on the base branch
   - Read changed files when the diff alone isn't enough to understand intent

2. **Match the repo's conventions** — before generating anything, study the
   recent commit history from step 1. Look for patterns:
   - Do they use conventional commits (`feat:`, `fix:`)? Scoped (`feat(api):`)? Plain English?
   - Sentence case or lowercase? Imperative or past tense?
   - Are there PR templates in `.github/PULL_REQUEST_TEMPLATE.md`?
   - Match whatever style the team already uses. If no clear pattern exists,
     fall back to the templates below.

3. **Analyze the changes** — pay attention to:
   - Which files were added, modified, or deleted
   - The diff stat (lines added/removed per file)
   - Existing commit messages on the branch
   - The semantic *purpose* of the changes (bug fix, feature, refactor, docs, etc.)

4. **Generate suggestions** using the repo's conventions if found, otherwise
   the templates below.

## Output Templates

### Commit Message

```
<type>(<scope>): <short summary>

<body — what changed and why, wrapped at 72 chars>
```

**Type** must be one of: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`, `ci`, `style`, `build`.

**Scope** is the area of the codebase affected (e.g. `auth`, `api`, `ui`).
Omit scope if changes span many areas.

**Rules:**
- Subject line <= 70 characters, imperative mood ("add", not "added")
- Body explains *why*, not just *what*
- Reference issue numbers when available: `Fixes #123`

### PR Title

```
<type>(<scope>): <concise description under 70 chars>
```

Same conventions as commit subject line. The title should make sense
in a list of PRs without needing to read the description.

### PR Description

Use this structure:

```markdown
## Summary

<1-3 sentences explaining the motivation and what this PR accomplishes>

## Changes

- <Bulleted list of key changes, grouped logically>

## Test Plan

- [ ] <How to verify each major change>

## Notes

<Anything reviewers should know — migration steps, follow-ups, risks>
```

**Guidelines:**
- Summary answers *why* this change exists, not just *what* it does
- Changes list is scannable — one bullet per logical change, not per file
- Test plan is concrete — "run `npm test`" not "verify it works"
- Notes section is optional — omit if nothing special

## Deciding Change Type

| Indicator | Type |
|---|---|
| New files, new exports, new routes | `feat` |
| Existing tests now pass, error handling fixed | `fix` |
| Same behavior, different structure | `refactor` |
| Only `.md`, comments, or docstrings changed | `docs` |
| Only test files changed | `test` |
| Config, deps, CI files only | `chore` / `ci` / `build` |
| Measurable speed/size improvement | `perf` |

When changes span multiple types, use the *primary* type and mention
others in the body.

## Example

Given a branch that adds rate limiting to an API:

**Commit message:**
```
feat(api): add rate limiting to public endpoints

Apply token-bucket rate limiting (100 req/min) to all /api/v1 routes.
Returns 429 with Retry-After header when exceeded.

Fixes #42
```

**PR title:**
```
feat(api): add rate limiting to public endpoints
```

**PR description:**
```markdown
## Summary

Adds rate limiting to public API endpoints to prevent abuse and ensure
fair usage. Uses a token-bucket algorithm with configurable per-route limits.

## Changes

- Add `RateLimiter` middleware with token-bucket implementation
- Apply default 100 req/min limit to all `/api/v1` routes
- Return `429 Too Many Requests` with `Retry-After` header
- Add rate limit headers (`X-RateLimit-*`) to all responses
- Add unit and integration tests for rate limiter

## Test Plan

- [ ] `npm test` passes
- [ ] Hit endpoint 101 times in 1 minute → 429 response
- [ ] `Retry-After` header value counts down correctly
- [ ] Rate limit resets after window expires

## Notes

Default limit is 100/min. Per-route overrides can be added in
`config/rate-limits.json`. No migration needed.
```

## Common Mistakes

- **Vague titles** like "Update code" or "Fix stuff" — be specific
- **Mixing concerns** — if the diff has unrelated changes, suggest splitting into separate commits/PRs
- **Past tense** — use imperative mood ("add" not "added")
- **Missing test plan** — always include concrete verification steps
- **Wall of text** — PR descriptions should be scannable, use bullets
