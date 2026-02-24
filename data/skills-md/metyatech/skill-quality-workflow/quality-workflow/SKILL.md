---
name: quality-workflow
description: Use when writing tests, designing test coverage, handling defect fixes, or performing root-cause analysis. Also use when creating test matrices or choosing between unit/integration/E2E tests. Do not use for general development, linting setup, or CI configuration.
---

# Quality workflow

## Test coverage methodology

- Cover success, failure, boundary, invalid input, and key state transitions (including first-run/cold-start vs subsequent-run behavior when relevant); include representative concurrency/retry/recovery when relevant.
- For deterministic output files, use full-content snapshot/golden tests.
- Prefer making nondeterministic failures reproducible over adding sleeps/retries; do not mask flakiness.
- For timing/order/race issues, prefer deterministic synchronization (events, versioned state, acks/handshakes) over fixed sleeps.
- For integration boundaries (network/DB/external services/UI flows), add an integration/E2E/contract test that exercises the boundary; avoid unit-only coverage for integration bugs.
- For non-trivial changes, create a small test matrix (scenarios x inputs x states) and cover the highest-risk combinations; document intentional gaps.

## Feedback loops and root causes

- Treat time-to-detect and time-to-fix as quality attributes; shorten the feedback loop with automation and observability rather than relying on manual QA.
- For any defect fix or incident remediation, perform a brief root-cause classification: implementation mistake, design deficit, and/or ambiguous/incorrect requirements.
- Feed the root cause upstream in the same change set: add or tighten tests/checks/alerts, update specs/acceptance criteria, and update design docs/ADRs when applicable.
- If the failure should have been detected earlier, add a gate at the earliest reliable point (lint/typecheck/tests/CI required checks or runtime alerts/health checks); skipping this requires explicit user approval.
- Record the prevention mechanism (what will catch it next time) in the PR description or issue comment; avoid "fixed" without a concrete feedback-loop improvement.
