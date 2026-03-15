---
name: quality-assurance
description: "End-to-end quality assurance for any software repo: code review, test strategy, bug triage, debugging, flaky-test repair, coverage improvement, suite architecture, and CI/CD quality gates for frontend, backend, or full-stack systems. Use when reviewing PRs, receiving review feedback, writing or repairing tests, debugging failing or flaky suites, proving browser behavior, hardening frontend or backend CI, or improving release confidence with reliable verification."
---

# Quality Assurance

Quality assurance is a delivery system, not a phase. Reconstruct intended behavior, choose the cheapest evidence that can prove or falsify it, then wire the same verification into repeatable local and CI workflows.

In command examples below, `<skill-dir>` means the installed `quality-assurance` skill directory and `<repo-root>` means the target repository root.

## Start Here

1. Run `python <skill-dir>/scripts/qa-scan.py <repo-root>` when the bundled scanner is available; otherwise perform the same stack and CI inventory manually.
2. Preserve and read the full failure artifact set before changing code: stack traces, failing assertions, screenshots, traces, query logs, retry logs, seeds, and the first bad CI step.
3. Reconstruct the intended behavior and the cheapest proof that can falsify or confirm it.
4. Reuse repo commands from `Makefile`, `package.json`, `pyproject.toml`, `tox.ini`, `noxfile.py`, `justfile`, `Taskfile.yml`, or CI config before inventing new ones.
5. Read repo-local instructions before deciding whether tests may be run, which suites are mandatory, or how evidence must be reported.
6. Load only the reference files that match the task, and state the proof command before making any success claim.

## Operating Rules

- Evidence before claims. Do not say fixed, passing, or complete without fresh command output.
- Reproduce before repair. A regression test is part of the fix whenever the repo and task permit it.
- Read the full artifact before editing. The first failing step, root-cause frame, slow query, or browser trace usually matters more than the last summary line.
- Use the lowest-fidelity test that can actually prove the behavior. Escalate only when cheaper layers cannot prove it.
- Mock boundaries, not business logic.
- Frontend QA must prove user-visible state transitions, not just that markup rendered.
- Do not delete, weaken, or silently skip existing tests without explicit sign-off from the user or repo owners.
- Review comments are technical claims to evaluate, not social cues to obey.
- Flaky tests are bugs. Quarantine is temporary containment, not completion.
- Coverage is a lagging indicator. Use it to find blind spots, not to justify weak tests.
- CI-only failures usually mean environment, ordering, timing, data, or cache assumptions were hidden locally. Debug those assumptions directly.
- At scale, speed comes from suite architecture, hermetic setup, sharding, disciplined test selection, and high-signal artifacts.

## QA Router

### Repo and stack detection

Use `scripts/qa-scan.py`. It detects likely languages, frameworks, test runners, linters, and CI providers, then suggests which references to load and which commands probably matter.

### Code review and review feedback

Read [references/code-review.md](./references/code-review.md) for:
- review output format
- severity taxonomy
- self-review before requesting review
- receiving feedback and pushing back with evidence

### Test strategy and regression design

Read [references/test-strategy.md](./references/test-strategy.md) for:
- test type selection
- red-green-refactor and regression rules
- mocking, fixtures, and data strategy
- coverage interpretation

### Backend-heavy QA

Read [references/backend-testing.md](./references/backend-testing.md) for:
- APIs, services, jobs, queues, migrations, and contracts
- common backend stack patterns
- database and concurrency concerns

### Frontend-heavy QA

Read [references/frontend-testing.md](./references/frontend-testing.md) for:
- component, integration, browser, accessibility, and visual testing
- async UI control
- provider and fixture setup
- network, storage, and time handling
- flake repair and incremental test workflow

### Failure triage and debugging

Read [references/debugging.md](./references/debugging.md) for:
- failing tests
- CI-only failures
- flaky tests
- performance and observability-led debugging

### CI/CD and quality gates

Read [references/ci-cd.md](./references/ci-cd.md) for:
- local-to-CI parity
- pipeline staging
- caching, sharding, artifacts, and branch protection
- provider patterns for common CI systems

### Suite scaling and monorepos

Read [references/suite-architecture.md](./references/suite-architecture.md) for:
- ownership
- test selection
- quarantine policy
- monorepo and large-suite design

### Completion and release verification

Read [references/verification.md](./references/verification.md) before saying something is fixed, asking for merge, or treating a release as ready.

### Anti-pattern sweep

Read [references/anti-patterns.md](./references/anti-patterns.md) for fast smell detection across review, testing, debugging, and CI.

## Standard Loops

### Review loop

1. Reconstruct intended behavior from the issue, PR description, diff, or failing report.
2. Review highest-risk paths first: correctness, data integrity, auth, concurrency, performance, and user-visible regressions.
3. Emit findings with severity, impact, and concrete file or command evidence.
4. Propose the smallest safe fix or the precise follow-up question needed to unblock.
5. Verify changed behavior with focused commands.

### Bug-fix loop

1. Reproduce.
2. Isolate the smallest failing case.
3. Add or identify a failing regression test.
4. Fix the root cause, not just the symptom.
5. Run the focused proof command, then broader regression commands.

### Frontend verification loop

1. Choose the correct test layer: unit, component, integration, browser, or visual.
2. Render through realistic providers and control network, time, storage, viewport, locale, and feature flags explicitly.
3. If browser state is unclear, inspect the rendered DOM, screenshot, console, or trace before automating more actions.
4. Assert loading, empty, error, success, retry, disabled, and optimistic states when they matter.
5. Verify accessible names, keyboard flow, and focus behavior for user-facing changes.
6. Run the smallest proof first, then broaden only when necessary.

### Test-authoring loop

1. Decide which layer owns the behavior.
2. Build data with factories, builders, or fixtures instead of ad hoc duplication.
3. Assert observable outcomes.
4. Remove timing, order, and environment sensitivity.
5. For large scopes, work incrementally: one file or behavior slice at a time, verify, then continue.
6. Wire the command into local scripts and CI if it protects a critical behavior.

### CI hardening loop

1. Inventory commands already trusted locally.
2. Split fast gates from slow gates.
3. Parallelize only isolated jobs.
4. Cache dependencies and reusable artifacts.
5. Publish logs and artifacts that make failures diagnosable.
6. Enforce merge protection only on stable, high-signal jobs.

## Helper Scripts

- `scripts/qa-scan.py`: detect stack, runners, CI providers, and likely QA commands.
- `scripts/qa-check.sh`: run lint, type, and test commands across common Python, JS, Ruby, and Go repos.
- `scripts/coverage-report.sh`: run coverage with configurable thresholds across common runners.

## Skill Orchestration

- Use `agentic-development` when repo orientation, architecture choice, or the code-change path itself is the bottleneck.
- Use `gh-fix-ci` when GitHub Actions failures need log retrieval and implementation.
- Use security, browser, visual, performance, or cloud-specific skills when the QA problem depends on those systems.
- Use repo-specific build, deploy, or observability skills when the failure depends on that tooling.

## Exit Criteria

Do not stop on "likely fixed". Stop on reproduced failure, root-cause explanation, regression protection, fresh verification output, and a clear statement of residual risk if verification is partial.
