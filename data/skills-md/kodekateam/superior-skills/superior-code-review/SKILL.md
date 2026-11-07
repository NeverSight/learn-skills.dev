---
name: superior-code-review
description: Review a code change, diff, commit, branch, or pull request for actionable defects, regressions, security risks, compatibility breaks, and missing verification. Use when code review is the primary requested outcome. Keep the review read-only unless the user explicitly asks to implement fixes; do not use as a substitute for implementation or a specialized visual audit.
---

# Superior Code Review

Review changes as a skeptical maintainer who must protect behavior without manufacturing objections. Prefer a small set of well-supported findings over exhaustive commentary, and treat “no findings” as a valid result.

## Establish the review contract

Before judging the change, determine:

- the exact review target: working tree, staged diff, commit range, branch, pull request, or named files;
- the intended outcome and acceptance criteria from the request, issue, documentation, or tests;
- repository instructions, supported environments, compatibility promises, and relevant architecture;
- whether generated files, migrations, dependencies, configuration, and tests are part of the change;
- whether the user requested findings only or also authorized fixes.

Do not review an inferred comparison when the target is ambiguous and competing bases would materially change the findings. Use read-only inspection by default. A review request alone does not authorize editing files, posting comments, approving a pull request, or changing external state.

## Inspect the change in context

Read [references/reviewing-changes-and-risk.md](references/reviewing-changes-and-risk.md) when tracing behavior across callers, consumers, state, data, configuration, dependencies, or deployment boundaries.

Start with the diff, then inspect enough surrounding and connected code to understand the changed contract. Verify assumptions against actual call sites, schemas, tests, and configuration rather than judging isolated lines.

Prioritize risks that can produce:

- incorrect outputs, state transitions, or side effects;
- authorization, validation, privacy, or trust-boundary failures;
- data loss, corruption, duplication, races, or partial completion;
- crashes, unavailable paths, swallowed failures, or unrecoverable states;
- compatibility breaks across APIs, schemas, stored data, clients, or environments;
- material performance or resource regressions;
- tests that pass while the changed behavior remains unverified.

Do not report formatting, naming, personal style, or speculative redesign as defects unless they create a concrete maintenance or correctness risk not already enforced by tooling.

## Prove each finding

Read [references/finding-quality-and-severity.md](references/finding-quality-and-severity.md) before reporting findings or assigning severity.

For each candidate:

1. identify the changed line or smallest relevant range;
2. trace the execution or data path that reaches it;
3. state the input, state, environment, or sequence that triggers the problem;
4. confirm the resulting user, system, security, data, or compatibility impact;
5. check whether another layer already prevents or handles it;
6. describe the smallest credible correction direction without writing a full patch.

Discard a candidate when its trigger is impossible under maintained contracts, its impact is merely hypothetical, or the repository already handles it correctly. Mark unresolved questions as questions, not findings.

## Validate proportionately

Use safe, read-only checks that improve confidence: targeted tests, type checks, linters, builds, static analysis, or reproduction commands already supported by the repository. Do not mutate shared systems, regenerate broad artifacts, install dependencies, or run destructive integration workflows without authorization.

A passing suite does not erase a proven defect, and a failing unrelated test is not automatically caused by the reviewed change. Separate:

- failures introduced by the target change;
- pre-existing failures;
- checks that could not run;
- behavior not covered by available checks.

## Report findings first

Order findings by severity and likelihood of real impact. Each finding should include:

- severity and concise title;
- precise file and line location;
- trigger or scenario;
- concrete consequence;
- correction direction;
- confidence or missing evidence only when it materially affects interpretation.

Avoid duplicate findings that share one root cause. After findings, include a short review summary and verification performed. If no actionable findings remain, say so directly and list material areas that were not verified.

## Combine skills narrowly

- Use `superior-api-security` when the review is explicitly security-focused or needs threat-driven depth.
- Use `superior-database` when schema, query, transaction, migration, or data-lifecycle correctness is central.
- Use `superior-performance` when performance evidence and profiling are primary rather than one review risk among many.
- Use `superior-testing` when test architecture, reliability, or missing coverage requires dedicated judgment.
- Use `superior-ui-audit` for visual product-surface findings; use accessibility or responsive skills when those are explicit review scopes.
- Use `superior-debugging` when a concrete observed failure must be causally diagnosed rather than reviewed from a change set.
- Use `superior-delivery` when pipeline, artifact promotion, rollout, or rollback behavior needs dedicated evaluation.
- Use `superior-reliability` when availability objectives, failure isolation, degradation, or recovery are central.
- Use `superior-logic` only when the user also asks to implement a confirmed behavioral fix.

Do not broaden a general review into a full security audit, architecture redesign, dependency migration, or implementation task without explicit scope.
