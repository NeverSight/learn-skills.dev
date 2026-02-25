---
name: code-review
description: This skill should be used when the user asks to "review my changes", "review this code", "check my work", "what's wrong with my changes", "review before I push", "security review", "do a code review", or mentions reviewing, auditing, or analyzing local code changes before committing or opening a PR.
context: fork
---

# Reviewing Local Changes

This skill reviews code changes in the local working tree — before they become a PR. It uses the merge-base diff to isolate "your work" from upstream, regardless of branching strategy.

**Review philosophy:** Find issues that matter. No nitpicking. Focus on: data loss, security breaches, performance degradation, and production incidents. Explain risk in business terms — "attacker can X" not just "this is insecure."

## Core Command Pattern

All reviews start by identifying what changed. The universal approach is a **merge-base diff**: everything you changed relative to the integration target.

```bash
# 1. Update remote refs (required — otherwise you diff against stale refs)
git fetch origin

# 2. Get the merge-base (where your work diverged from the target)
MERGE_BASE=$(git merge-base HEAD origin/main)

# 3. Diff: merge-base → working tree (committed + uncommitted + staged)
git diff $MERGE_BASE

# 4. Changed file list
git diff $MERGE_BASE --name-only

# 5. Diff stats (quick size check before deep review)
git diff $MERGE_BASE --stat
```

**Why merge-base, not `origin/main` directly?**
`git diff origin/main` includes upstream changes that aren't yours. `git merge-base` finds the fork point — so the diff shows only your work, even if main moved ahead. No rebase required.

**Detecting the integration target:**

```bash
# Auto-detect: use the upstream tracking branch, fall back to origin/main or origin/master
TARGET=$(git rev-parse --abbrev-ref @{upstream} 2>/dev/null | sed 's|/.*|/main|') \
  || TARGET=$(git rev-parse --verify origin/main 2>/dev/null && echo origin/main) \
  || TARGET=origin/master
```

If the repo uses a non-standard default branch, the user should specify it. Ask rather than guess.

### How this works across branching strategies

| Strategy                                | Integration target                 | What the diff shows                             |
| --------------------------------------- | ---------------------------------- | ----------------------------------------------- |
| **Feature branch**                      | `origin/main`                      | All commits on your branch + uncommitted work   |
| **Trunk-based (TBD)**                   | `origin/main`                      | Local commits not yet pushed + uncommitted work |
| **Stacked branches**                    | Parent branch (`origin/feat-base`) | Just this layer's changes                       |
| **Long-lived branch, main moved ahead** | `origin/main`                      | Still only your changes — merge-base handles it |
| **Just rebased**                        | `origin/main`                      | Same — merge-base updates to new fork point     |

### Including uncommitted work

The default `git diff $MERGE_BASE` compares merge-base to the working tree — this includes staged, unstaged, and committed changes all at once. That's what you want for a pre-push review: the full picture of what will land.

To review only committed changes (exclude uncommitted work):

```bash
git diff $MERGE_BASE...HEAD
```

## Review Workflow

Execute ALL phases in order. Never skip phases. In quick mode, skip phases marked _(full mode only)_.

### Phase 1: Gather context

1. Fetch origin and compute the merge-base.
2. Run `git diff $MERGE_BASE --stat` to understand the scope (file count, line count).
3. Get the changed file list with `git diff $MERGE_BASE --name-only`.
4. Read the full content of every changed file (not just the diff hunks) — you need surrounding context to judge correctness.
5. Read the diff itself for line-level analysis.
6. Check commit messages with `git log $MERGE_BASE..HEAD --oneline` for intent context.
7. Identify the change category: new feature, bug fix, refactor, security fix, performance optimization, dependency update.
8. Identify critical paths: auth, payments, data writes, external APIs, file system operations.

**Output:** 2-3 sentence summary of what changed and why.

### Phase 2: Classify risk

Rank changed files by risk before reviewing:

- **Critical**: auth, payments, crypto, infra/deploy configs, database migrations, secrets management
- **High**: API routes, middleware, data models, shared libraries
- **Medium**: business logic, UI components with state
- **Low**: docs, tests (unless deleting them), static assets, config formatting

Review critical and high files first. If time-constrained, give low-risk files a summary-only pass.

### Phase 3: Security scan

Check every changed line against these categories. Flag critical issues immediately.

**Broken access control:**

- Authentication required on protected endpoints?
- Authorization checks present (role/permission validation)?
- User can only access their own resources (no IDOR)?

**Cryptographic failures:**

- Passwords hashed with bcrypt/argon2 (not MD5/SHA1)?
- No hardcoded secrets (API keys, tokens, passwords)?
- Secrets come from environment variables?

**Injection:**

- SQL queries use parameterized statements (no string concatenation)?
- User inputs sanitized before database queries?
- No `eval()`, `exec()`, or `Function()` with user input?
- Command injection prevented (no `shell=True` / unsanitized args to spawn)?
- HTML output escaped to prevent XSS?

**Insecure design:**

- Rate limiting on auth endpoints?
- Input validation with schema/type checking?
- Proper error handling (no stack traces to users)?

**Vulnerable components:**

- Dependencies up to date (no known CVEs)?
- Lockfile committed?

**SSRF:**

- User-provided URLs validated against allowlist?
- Internal IPs/localhost blocked?

### Phase 4: Logic & performance

**Bugs:**

- Null/undefined access, off-by-one, race conditions, resource leaks
- Wrong operator, inverted condition, missing edge case, unreachable code
- Error swallowing (empty catch blocks), resources not closed in finally/defer
- Incorrect state transitions

**Performance — database & external calls:**

- N+1 query problem (loop with queries/API calls inside)?
- Missing indexes on foreign keys or WHERE clauses?
- Large result sets without pagination?
- Transactions held too long?

**Performance — algorithms:**

- O(n^2) or worse in hot path?
- Unnecessary array copies or object clones?
- Nested loops that can be flattened?
- Unnecessary `await` in loops — use `Promise.all()` when independent?

**Performance — caching:**

- Repeated expensive operations without caching?

**API contract:**

- Breaking changes to public interfaces without migration/versioning?

### Phase 5: Architecture & testing

**Architecture** (flag only significant issues):

- Business logic mixed with I/O or presentation?
- God file (>500 lines or >20 exports)?
- Circular dependencies?
- Same logic duplicated in 3+ places?
- Magic numbers without named constants?

**Testing:**

- New features have tests?
- Bug fixes have regression tests?
- Security-critical paths tested?
- Edge cases covered (empty input, max values, errors)?

If tests are missing for critical paths, list what should be tested.

### Phase 6: Run checks _(full mode only)_

```bash
# Lint changed files (adapt to project)
npm run lint          # or: ruff check, cargo clippy, golangci-lint run, etc.

# Run affected tests
npm test              # or: pytest, go test, cargo test, etc.

# Secret scanning (if available)
gitleaks detect --source . --no-git

# Dependency audit (if lockfile changed)
npm audit             # or: pip audit, cargo audit, etc.
```

Only run tools that exist in the project. Check for the presence of config files (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`) before assuming a tool is available.

### Phase 7: Production readiness _(full mode only)_

- Environment variables documented?
- Backward compatible? If not, is there a migration path?
- Logging added for new critical operations?
- No sensitive data in logs (passwords, tokens, PII)?
- Graceful error messages for users (no raw stack traces)?

## Producing the Review

### Finding format

For every finding, provide:

- **File + line**: exact path and line number. MUST exist in the diff — verify before reporting.
- **Severity**: `CRITICAL` / `HIGH` / `MEDIUM` / `LOW`
- **Category**: `security` / `bug` / `logic` / `performance` / `architecture` / `testing`
- **Title**: one-line summary
- **Risk**: what can happen — explain in business terms ("attacker can...", "users will see...", "data will be lost when...")
- **Current code vs fix**: show both. Before/after, not just "consider changing this."
- **Confidence**: if uncertain, say so. Prefix with `[Uncertain]` and explain what would confirm or refute.

Finding template:

```
CRITICAL security: [Title]
File: path/to/file.ts:42
Risk: [What can happen in business terms]

Current:
  [problematic code]

Fix:
  [corrected code]
```

### Output structure

```
## Review Summary

**Recommendation:** BLOCK | APPROVE WITH COMMENTS | APPROVE

[2-3 sentence summary of what changed and overall assessment]

## Blocking Issues ([count])

[CRITICAL and HIGH findings with file, line, risk, and before/after fix]

## Non-Blocking Suggestions ([count])

[MEDIUM and LOW findings — performance, architecture, quality]

## Test Coverage

[What's covered, what's missing, suggested test cases]

## Metrics

- Files changed: [count]
- Lines added/removed: [+N / -N]
- Critical issues: [count]
- Non-blocking suggestions: [count]
```

### Recommendation logic

**BLOCK** — must fix before pushing:

- Any CRITICAL security issue (data breach, auth bypass, injection)
- Data loss risk (missing transaction, no validation before delete)
- Breaking change without migration path
- Known performance regression

**APPROVE WITH COMMENTS** — non-blocking, track as follow-up:

- Performance improvements (not regressions)
- Architectural suggestions
- Missing non-critical tests
- Code quality improvements

**APPROVE** — when all of:

- Zero critical/high security issues
- No data loss risk
- Performance acceptable
- Critical paths tested

## Review Modes

The user may request a specific mode:

- **"quick review" / "fast review"**: phases 1-5 only (no tool execution). Focus on bugs and security. Default mode.
- **"full review"**: all 7 phases — run lint, tests, secret scan, dependency audit, production readiness.
- **"security review"**: phases 1-3 only. Deep security focus — full OWASP check. Skip logic/perf/architecture.

Default to **quick review** unless the user asks otherwise.

## Handling Large Changesets

Changesets over 1000 lines changed require chunking:

1. Start with the changed file list and the diff stats.
2. Classify all files by risk (Phase 2).
3. Review the top 10 highest-risk files in full depth.
4. For remaining files, provide a one-line summary per file (what changed, any obvious issues).
5. If a single file diff exceeds 500 lines, review it hunk-by-hunk.
6. Tell the user you've prioritized — don't silently skip files.

Over 5000 lines: warn that a thorough review at this scale is unreliable. Suggest splitting the work and offer specific split points based on the file groupings.

## Decision Policy

- **ALWAYS** run `git fetch origin` before computing the diff. Stale refs mean wrong diffs.
- **ALWAYS** use the merge-base, not a direct diff against `origin/main`. Direct diffs include upstream changes that aren't the user's.
- **ALWAYS** read full file content, not just diff hunks. The same function above/below the hunk is critical context.
- **ALWAYS** verify file paths and line numbers exist before citing them. Never hallucinate a reference.
- **ALWAYS** provide concrete code evidence for every finding. No vague "this could be problematic".
- **ALWAYS** explain risk in business terms. "Attacker can read any user's data via IDOR" — not "this is insecure."
- **ALWAYS** show before/after code for fixes. Don't just describe what to change.
- **Discover before assuming**: check what tools/configs exist in the repo before running lint/test commands. Check the default branch name before assuming `main`.
- **Limit output**: cap at 15 findings per review. If more issues exist, summarize the rest and note the count.
- **Rank by impact**: report critical/high first. If you hit the cap, drop low findings.
- **One finding per issue**: don't repeat the same pattern across 10 files. Flag it once, note "same pattern in N other files".
- **Verify claims**: if you flag an N+1 query, verify it's actually in a loop. If you flag a race condition, verify concurrent access is possible.
- **When in doubt, flag it**: better to surface a concern than miss a critical issue. But label uncertainty honestly.

## Safety Rules

- **No secrets in output**: never include API keys, tokens, passwords, or connection strings in findings — even if found in the diff. Say "hardcoded secret detected at file:line" without echoing the value.
- **No code execution beyond standard tooling**: only run linters, test suites, and scanners that are already configured in the project. Never run arbitrary code from the changeset.
- **Read-only**: the review does not modify any code. Suggested patches are advisory — presented in the finding body, not applied.
- **Never approve blindly**: if you can't confidently assess the changes (e.g., binary files, minified code, languages you don't know well), say so instead of guessing.

## Error Handling

- **No remote configured**: the repo may be local-only. Fall back to diffing against the first commit or ask the user what to diff against.
- **Detached HEAD**: the user may be on a detached HEAD (e.g., during rebase). Use `git diff origin/main` directly as fallback.
- **Default branch isn't `main`**: check with `git remote show origin | grep 'HEAD branch'` or `git symbolic-ref refs/remotes/origin/HEAD`. Don't assume `main`.
- **Lint/test command fails**: report the failure output as a finding (category: `info`). Don't retry broken tooling — flag it and move on.
- **Binary files in diff**: skip binary files. Note them in the summary ("N binary files changed — not reviewed").
- **Empty diff**: if the merge-base diff is empty, tell the user — there's nothing to review. Check if they have uncommitted changes with `git status`.
