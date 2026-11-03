---
name: code-review
description: Reviews code changes for correctness, security, and maintainability and returns severity-ranked findings. Use when the user asks for a code review, PR review, review of a diff, or a second pass on local changes.
---

# Code Review

Review the diff the user named. If they did not name one, review the current branch against its base.

## What to read

1. PR description or the user’s intent, so findings are judged against the change’s purpose.
2. `git diff <base>...HEAD` (or the files they pasted).
3. Callers and tests around the changed lines. Do not review only the added lines in isolation.

Stay inside the change. Mention pre-existing issues only when the change makes them worse or touches them directly.

## What to check

- Correctness: edge cases, nulls, error paths, off-by-one, race conditions, wrong layer of the stack.
- Security: injection, authz gaps, secret leakage, unsafe deserialization, overly broad access.
- Behavior: user-visible regressions, API contract breaks, migration and rollback risk.
- Tests: the change has a test for the new behavior and the failure mode that motivated it. Missing tests are a finding when the change is non-trivial.
- Maintainability: only when it will cause a real bug or block the next change. Skip style nits the formatter owns.

## Findings

Lead with the outcome, then the findings. No finding means say the change looks sound and name what you checked.

Use these severities:

- **Blocker** — incorrect, unsafe, or will break users. Must be fixed before merge.
- **Should fix** — real bug or gap that is safe to ship only with a follow-up the author accepts.
- **Note** — optional improvement. Do not block on these.

Each finding:

```markdown
### [Severity] Short title
`path:line` — what is wrong, why it matters, and the concrete change to make.
```

Order findings Blocker, then Should fix, then Note. Quote the smallest code region that shows the issue.

## Do not

- Restate the diff.
- Invent a Jira key, ticket, or requirement the user did not provide.
- Approve a change that has an unaddressed Blocker.
- Request refactors that are unrelated to the change.
