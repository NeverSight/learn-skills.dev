---
name: pr-description
description: Generates structured pull request descriptions from branch diffs with context, motivation, testing instructions, rollback plans, and reviewer guidance. Produces descriptions that help reviewers understand what changed, why, and how to verify. Use when creating PRs, writing PR descriptions, preparing merge requests, or when the user asks for help describing their changes.
---

# PR Description Generator

## Overview

Generate pull request descriptions that tell reviewers WHY something changed,
not just WHAT changed. Every PR description includes structured sections for
motivation, changes, testing instructions, rollback plan, and reviewer guidance.
The goal is a description that lets a reviewer understand, verify, and safely
deploy the change without asking follow-up questions.

## When to use

- When creating a pull request or merge request
- When writing or improving a PR description
- When asked to summarize branch changes for review
- When preparing a changeset for code review
- When the user says "describe my changes" or "write a PR description"

**Do NOT use when:**

- The user wants a commit message (use a commit message skill)
- The user wants a changelog entry (use a changelog skill)
- The user wants a code review of the changes (use a code review skill)

## Workflow

### 1. Analyze the Full Branch Diff

Before writing anything, understand the complete scope of changes:

- **Read the full diff** between the branch and its base (usually `main`). Use
  `git diff main...HEAD` or equivalent.
- **Count changed files** and categorize them: new files, modified files,
  deleted files.
- **Identify the change type**: feature, bugfix, refactor, infrastructure,
  documentation, or mixed.
- **Map dependencies**: Which changes depend on others? What's the logical
  grouping?

Output: A mental model of what changed and how the pieces fit together.

### 2. Determine Motivation and Context

This is the most important step. Reviewers need to know WHY before WHAT.

- **What problem does this solve?** Link to issues, bug reports, or user
  feedback.
- **Why now?** What triggered this work — a bug report, a performance
  regression, a new requirement?
- **What alternatives were considered?** Briefly note rejected approaches and
  why.
- **What's the risk?** Security implications, performance impact, breaking
  changes.

If the motivation isn't obvious from the diff, ask the user. Never guess at
motivation — a wrong "why" is worse than no "why."

### 3. Write the Structured Description

Use the output template below. Fill every section. If a section genuinely
doesn't apply (e.g., no rollback needed for a docs-only change), explicitly
state why it's not applicable rather than omitting it.

### 4. Write Testing Instructions

Testing instructions must be **copy-pasteable**. A reviewer should be able to
follow them step-by-step without interpretation.

- Include exact commands to run (with flags and arguments)
- Specify expected output or behavior for each step
- Cover the happy path AND at least one edge case
- If manual testing is needed, describe exact UI steps
- Include setup steps if the reviewer needs specific data or configuration

Bad: "Test the login flow" Good: "1. Run `npm run dev` 2. Navigate to
`/login` 3. Click 'Sign in with Google' 4. Verify redirect to Google OAuth
consent screen 5. After consent, verify redirect back to `/dashboard` with user
avatar in top-right"

### 5. Write the Rollback Plan

Every production-facing change needs a rollback plan. Include:

- **How to revert**: Exact commands or steps (e.g., `git revert <sha>`)
- **Database migrations**: Are they reversible? What's the down migration?
- **Feature flags**: Can this be toggled off without a deploy?
- **Data impact**: Will reverting lose user data or leave orphaned records?
- **Dependencies**: Does reverting this break other deployed changes?

### 6. Flag Areas for Careful Review

Help reviewers focus their attention:

- **Security-sensitive changes**: Auth logic, input validation, data access
- **Performance-critical paths**: Hot loops, database queries, API calls
- **Breaking changes**: API contract changes, schema migrations
- **Complex logic**: Algorithms, state machines, concurrency
- **Areas you're uncertain about**: Be honest about what you're not sure of

Use inline comments in the PR diff for file-specific guidance, and the Reviewer
Notes section for cross-cutting concerns.

## Output Template

Structure every PR description as follows:

```markdown
## Summary

[1-3 sentence overview of what this PR does and why. Lead with the WHY.]

## Motivation

[What problem does this solve? Why is this change needed now? Link to issues or
bug reports. Mention alternatives considered and why they were rejected.]

## Changes

[Organized list of what changed, grouped logically. Not a file-by-file list —
group by concept or feature area.]

- **[Area 1]**: [What changed and why]
- **[Area 2]**: [What changed and why]
- **[Area 3]**: [What changed and why]

## Testing Instructions

[Step-by-step instructions a reviewer can follow to verify the change works.
Commands must be copy-pasteable.]

1. [Setup step if needed]
2. [Action to take]
3. [Expected result]
4. [Edge case to verify]

### Automated Tests

- [List of new or modified tests and what they cover]

## Rollback Plan

[How to revert this change safely. Include exact commands, migration reversal
steps, and data impact assessment.]

## Reviewer Notes

[Areas that need careful review. Security concerns, performance implications,
breaking changes, or areas of uncertainty. Help reviewers focus their
attention.]

- **[File or area]**: [What to look for and why]
```

## Example

**Scenario**: Branch adding rate limiting to the API gateway.

**Input diff summary**: 4 files changed — new middleware, config updates, tests,
docs.

**Output**:

```markdown
## Summary

Adds request rate limiting to the API gateway to prevent abuse and protect
downstream services from traffic spikes. Triggered by the outage on 2026-02-28
where a single client sent 50k requests/minute.

## Motivation

On Feb 28, a misconfigured client script hammered `/api/orders` at 50k req/min,
overwhelming the orders service and causing a 23-minute outage (INC-4521). We
need per-client rate limiting at the gateway level to prevent any single client
from degrading service for others.

Alternatives considered:

- **Application-level rate limiting**: Rejected because each service would need
  its own implementation, and the gateway already sees all traffic.
- **CDN-level rate limiting**: Too coarse — we need per-API-key limits, not
  per-IP.

## Changes

- **Rate limit middleware** (`src/middleware/rate-limiter.ts`): New sliding
  window rate limiter using Redis. Configurable per-route limits with sensible
  defaults (1000 req/min for reads, 100 req/min for writes).
- **Configuration** (`config/rate-limits.yaml`): Per-route limit definitions.
  Defaults can be overridden per API key via the admin dashboard.
- **Gateway integration** (`src/gateway.ts`): Middleware registered before
  routing. Returns 429 with `Retry-After` header when limit exceeded.
- **Tests** (`tests/rate-limiter.test.ts`): 12 new tests covering sliding window
  accuracy, Redis failure fallback, and per-key override behavior.

## Testing Instructions

1. Start Redis locally: `docker run -d -p 6379:6379 redis:7-alpine`
2. Run the test suite: `npm test -- --grep "rate-limiter"`
3. Verify all 12 tests pass
4. Start the dev server: `REDIS_URL=redis://localhost:6379 npm run dev`
5. Send 5 rapid requests:
   `for i in {1..5}; do curl -s -o /dev/null -w "%{http_code}\n" http://localhost:3000/api/orders; done`
6. Verify all return 200
7. Send 1001 requests rapidly:
   `ab -n 1001 -c 10 http://localhost:3000/api/orders`
8. Verify the last requests return 429 with a `Retry-After` header

### Automated Tests

- `rate-limiter.test.ts`: Sliding window counting, Redis connection failure
  fallback to in-memory, per-key limit overrides, 429 response format

## Rollback Plan

1. Revert this PR: `git revert <merge-sha>`
2. Deploy the revert — no database migrations to reverse
3. Redis rate limit keys will expire naturally (TTL = window size)
4. No data loss risk — rate limiting is stateless from the application's
   perspective
5. If Redis is the issue (not this code), disable rate limiting via env var:
   `RATE_LIMIT_ENABLED=false`

## Reviewer Notes

- **`src/middleware/rate-limiter.ts:45-62`**: The sliding window algorithm —
  please verify the math on window boundary transitions. I'm using a weighted
  overlap approach rather than fixed windows.
- **Redis failure mode** (`rate-limiter.ts:78`): When Redis is unreachable, we
  fall back to in-memory limiting. This means limits aren't shared across
  instances — acceptable for a degraded mode, but worth discussing.
- **Security**: Rate limit headers expose the client's current usage. Verify
  this doesn't leak sensitive information for your use case.
```

## Common Mistakes

| Mistake                                                 | Fix                                                                                 |
| ------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| File-by-file change list instead of conceptual grouping | Group changes by feature area or concept, not by filename                           |
| Missing motivation ("what" without "why")               | Always explain the problem being solved and why this approach was chosen            |
| Vague testing instructions ("test the feature")         | Write copy-pasteable commands with expected outputs for each step                   |
| No rollback plan                                        | Every production change needs revert steps, migration reversal, and data impact     |
| Omitting reviewer guidance                              | Flag security-sensitive, performance-critical, and uncertain areas explicitly       |
| Assuming reviewers have context                         | Link to issues, explain acronyms, provide background for domain-specific changes    |
| Listing every file changed                              | Summarize conceptually — reviewers can see the file list in the diff                |
| No edge case in testing instructions                    | Include at least one error path or boundary condition to verify                     |
| Rollback plan says "revert the PR" with no details      | Specify exact commands, migration steps, data impact, and dependency considerations |

## Key Principles

1. **WHY before WHAT** — The motivation section is the most important part of a
   PR description. A reviewer who understands why a change was made can evaluate
   whether the approach is correct. A reviewer who only knows what changed can
   only check for typos. Lead every description with the problem being solved.

2. **Testing instructions must be copy-pasteable** — If a reviewer has to
   interpret, adapt, or guess at your testing instructions, they won't test.
   Include exact commands, expected outputs, and setup steps. A reviewer should
   be able to verify the change by copying and pasting from the PR description.

3. **Every change is revertible until proven otherwise** — Include a rollback
   plan for every PR. If the change truly can't be reverted (destructive
   migration, data format change), say so explicitly and explain the mitigation
   strategy. "No rollback needed" is almost always wrong.

4. **Guide the reviewer's attention** — Reviewers have limited time and
   attention. Flag the 2-3 areas that matter most: security-sensitive logic,
   complex algorithms, performance-critical paths, or areas where you're
   uncertain. Don't make them discover the important parts on their own.

5. **Describe concepts, not files** — Group changes by what they accomplish, not
   which files they touch. "Added rate limiting middleware with Redis-backed
   sliding windows" is useful. "Changed rate-limiter.ts, gateway.ts,
   config.yaml" is not — the reviewer can see the file list in the diff.
