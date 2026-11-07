---
name: poka-yoke
description: "Prevent software mistakes through strong boundaries, safe defaults, meaningful tests, and mechanically enforced invariants. Use for TDD, validation, schemas, authorization, edge cases, regression coverage, or reliability-sensitive behavior."
---

# Poka-yoke

Poka-yoke means mistake-proofing. In software, do not rely only on memory or
discipline when types, schemas, constraints, validation, tests, or safe
defaults can prevent an invalid state. This is a Japanese-inspired engineering
metaphor, applied with context rather than maximal defensive code.

## Use this skill when

- adding or changing behavior at an input, API, database, or permission
  boundary;
- designing tests or working test-first;
- fixing a regression or recurring failure;
- handling untrusted data, retries, concurrency, migrations, or external
  services;
- deciding whether a bad state should be representable; or
- reliability and safety matter more than a happy-path demo.

## Outcome

Produce a behavior that is difficult to misuse and easy to verify, with:

- explicit invariants and boundary conditions;
- validation at the correct boundary;
- types, schemas, constraints, or exhaustive cases where they reduce risk;
- deterministic tests for normal, edge, failure, and authorization behavior;
- safe defaults, idempotency, and clear error handling where relevant; and
- evidence that the protection catches the intended mistake.

## Workflow

### 1. Enumerate failure modes

List realistic invalid inputs, missing data, duplicate requests, retries,
partial failures, unauthorized actions, stale state, malformed dependencies,
and boundary conditions. Prioritize by impact and likelihood.

### 2. Make invalid states hard to express

Prefer domain types, validated constructors, enums, non-null constraints,
foreign keys, unique constraints, transactional boundaries, permission checks,
and safe defaults when they encode a real invariant. Keep validation close to
the boundary that owns the rule.

### 3. Test behavior, not implementation

Write the smallest meaningful test for the desired behavior or regression.
Cover important edge and failure paths. Assert user-visible outcomes,
contracts, persisted state, and security decisions rather than private call
counts or incidental structure.

### 4. Run the feedback loop

Use a narrow check first, then broaden to integration, contract, end-to-end,
type, lint, migration, build, or smoke checks according to risk. Keep tests
deterministic and explain any unrun check.

### 5. Make failure actionable

Return errors that identify the boundary and next action without leaking
secrets. Do not silently coerce, retry forever, discard data, or convert a
failed invariant into a successful-looking result.

## Evidence standard

Each guardrail must correspond to a realistic failure mode. Each test must
fail for the defect it protects against and pass for the intended behavior.
Verification claims must be traceable to an executed command, observed result,
or authoritative evidence. Coverage percentage alone is not evidence of
mistake-proofing.

## Boundaries

- Do not add defensive branches for impossible or irrelevant states without a
  reason.
- Do not duplicate validation everywhere when one authoritative boundary owns
  the invariant.
- Do not make a test green by weakening its assertion.
- Do not use mocks to hide an integration contract that needs verification.
- Do not trade clarity for clever type machinery when a simple check is safer.

## Handoff

Report the failure modes considered, protections added, tests run, and residual
risk. Use `jidoka` when a check fails, `kodawari` for a quality review, or
`andon` when the remaining risk needs operational visibility.

If a referenced skill is not installed, apply its named lens inline instead of
trying to invoke it.
