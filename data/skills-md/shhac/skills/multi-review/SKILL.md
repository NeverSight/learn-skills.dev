---
name: multi-review
description: Review code changes from multiple specialist perspectives in parallel. Use when you want a thorough review of a PR, branch, or set of changes covering security, performance, correctness, edge cases, and ripple effects. Spawns parallel reviewer agents that each focus on a different lens, then synthesizes into a unified review.
---

# Multi-Perspective Review

Review code changes through multiple specialist lenses in parallel, then synthesize into a unified review.

## Reviewers

1. **Security** — injection, auth, data exposure, OWASP top 10
2. **Performance** — N+1 queries, unnecessary allocations, missing indexes, hot paths
3. **Correctness** — logic errors, off-by-ones, race conditions, unhandled states
4. **Test Coverage** — untested paths, missing edge case tests, test quality
5. **Edge & Ripple** — the "what happens to..." and "what happens if..." reviewer:
   - **"What happens to..."** — ripple effects on documentation, adjacent features, API consumers, shared state, caching layers
   - **"What happens if..."** — unexpected user behaviour, bad/missing data, interrupted flows, partial failures, concurrent access, rollback scenarios

---

## Instructions for Claude

You are the **review lead** orchestrating a multi-perspective code review.

### Phase 1: Identify the Changes

1. Determine what's being reviewed from the user's input:
   - A branch diff (`git diff main...HEAD`)
   - Staged changes (`git diff --cached`)
   - Specific files or a PR
2. If unclear, ask the user what they want reviewed
3. Consider the scope of changes when deciding which reviewers to spawn. For small or focused changes, fewer reviewers may be appropriate. For infrastructure or cross-cutting changes, consider adding relevant lenses beyond the default 5.
4. Gather the diff and list of changed files — you'll include this in each reviewer's prompt

### Phase 2: Spawn Reviewers

1. Create a team with `TeamCreate`
2. Create tasks for each reviewer with `TaskCreate`
3. Spawn 5 `general-purpose` teammates in parallel using `Task` with `team_name`, one per lens:
   - `security-reviewer`
   - `performance-reviewer`
   - `correctness-reviewer`
   - `test-coverage-reviewer`
   - `edge-ripple-reviewer`
4. Each reviewer's prompt should include:
   - The diff or changed files to review
   - Their specific lens and what to look for (see Reviewer Briefs below)
   - Instruction to **review only, do not make changes**
   - Instruction to report findings via `SendMessage` using the output format below
   - Instruction to **always report**, even if no issues are found — use the "Looks Good" section of the output format. This prevents the lead from waiting for a report that never comes.

### Reviewer Briefs

**Security:**
Review for injection vulnerabilities (SQL, command, XSS), authentication/authorization gaps, data exposure in logs or responses, secrets handling, input validation at system boundaries, and OWASP top 10 concerns.

**Performance:**
Review for N+1 queries, unnecessary allocations or copies, missing database indexes, expensive operations in hot paths, unbounded loops or result sets, missing pagination, and caching opportunities.

**Correctness:**
Review for logic errors, off-by-one mistakes, race conditions, unhandled states or error cases, null/undefined assumptions, type coercion issues, and whether the code actually achieves its stated goal.

**Test Coverage:**
Review for untested code paths, missing edge case tests, test quality (are tests actually asserting meaningful things?), brittle tests coupled to implementation details, and missing integration or boundary tests.

**Edge & Ripple:**
Think about consequences and failure modes. Two angles:
- *"What happens to..."* — Does this change affect documentation? API contracts? Adjacent features that read the same data? Shared utilities or types that other code depends on? Caching layers that might serve stale data? Monitoring or alerting thresholds?
- *"What happens if..."* — A user does something unexpected? The database has bad/missing/stale data? The operation is interrupted halfway? Two users hit this concurrently? An external service is down or slow? The deployment is rolled back after data has been written?

### Reviewer Output Format

Each reviewer should structure their findings as:

```
## {Lens} Review

### Issues Found
- **[severity: critical/warning/info]** Description of issue
  - File: path/to/file.ts:123
  - Suggestion: How to fix

### Looks Good
- Brief notes on what's well-handled from this perspective

### Summary
One-sentence overall assessment from this lens.
```

### Phase 3: Synthesis

1. As reviewers report back, check for critical findings — if any reviewer reports a critical issue before all reviewers have finished, notify the user immediately with a brief summary. Don't wait for all 5 to complete before surfacing critical findings.
2. Once all reviewers have reported, synthesize into a unified review:
   - **Critical issues** — must fix (from any reviewer)
   - **Warnings** — should fix or consider
   - **Observations** — informational notes
   - **What's good** — things done well across lenses
3. Deduplicate findings that multiple reviewers flagged
4. Present the synthesized review to the user
5. Ask the user if they have follow-up questions for any reviewer before shutting down. If so, message that reviewer and relay the response. Only shut down all teammates after the user is satisfied.

### Rules

- **All reviewers run in parallel** — they're independent
- **Read-only** — reviewers never modify code
- **No false positives** — reviewers should only flag real concerns, not hypothetical style preferences
- **Severity matters** — critical means "this will cause a bug or vulnerability", not "I would have done it differently"
