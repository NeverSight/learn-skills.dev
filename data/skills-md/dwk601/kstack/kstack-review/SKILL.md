---
name: kstack-review
description: Review plans and code independently with evidenced verdicts.
disable-model-invocation: true
---

# kstack review

Shared rules: read `../kstack/SKILL.md` first.

Never review your own implementation. If you authored it, dispatch a fresh configured reviewer. Do not edit source or tests.

## Modes

- **plan**: check scope, code facts, file overlap, dependencies, parallelism, and checkable acceptance criteria. No code revision is required yet.
- **code**: review an exact base/head pair against the task.
- **security**: trace authorization, untrusted input, secrets, migrations, and data exposure.
- **audit**: check the combined diff with one assigned focus: scope, cross-task behavior, or regressions. Inspect evidence rather than trusting summaries; reproduce the claims relevant to that focus.

## Review the code

1. Record base/head SHAs. Code reviews run the task checks and lint. Security reviews and audits inspect gates evidence and run focused probes, not unrelated suites again. An unavailable required check is BLOCKED.
2. Read the diff against acceptance criteria, then follow callers, stored data, contracts, config, and shared state beyond the changed files.
3. Check correctness, edge cases, root cause, unnecessary complexity, and whether the evidence proves the behavior. Confirm the assumptions that make the change safe.

## Verdict

Return `task or lane | base/head SHAs | PASS/FAIL/BLOCKED | checks | evidence`. Plan reviews identify the reviewed in-chat plan instead of SHAs.

For FAIL, list every proven finding in one pass: severity, file:line, broken criterion, evidence, and fix. BLOCKED names the missing check and error. Style notes do not block. A missing test is a failure only when the repo tests that area and behavior is otherwise unproven.
