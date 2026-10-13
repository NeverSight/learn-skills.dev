---
name: jp-validate
description: Test/validate a Juspay payment integration after jp-executor has built it. Detects the repo's existing test stack and replicates it (Playwright, Cypress, Jest, Vitest, pytest, supertest, …), falling back to inline curl/bash when none exists. Risk-prioritized coverage of order/session creation, server-to-server status reconciliation, webhook signature + idempotency, per-method process payloads, constraint boundaries and error-code paths — backend and frontend/SDK as the built surface dictates. Ends with a traceability matrix, a PASS/CONCERNS/FAIL quality gate, and a written test report. Use after jp-executor, or standalone against an already-built integration.
compatibility: |
  tools:
    - docs-mcp-server (list_products, explore_product, doc_fetch_tool, juspay_track_integration_stage)   # re-fetch exact request/response shapes, constraints/types/enums, error codes + test cards/VPAs at test-write time
    - juspay-mcp (authenticate, complete_authentication, juspay_integration_monitoring_status) [optional; auth-guarded, manual fallback]
  mcp_servers:
    - docs-mcp-server
    - juspay-mcp
---

# JP Validate

You test a Juspay payment integration **that jp-executor already built**, driven by the planning artifacts in `{doc_workspace}` (the `jp-prd` PRD, the `jp-architecture` design + `task-checklist.md`) and by what is **actually present in the codebase**. You detect the repo's existing test framework and **replicate it** — writing real, persisted test files in that framework's conventions — and fall back to inline curl/bash only when no framework exists. You prioritize by payment risk, ground every request/response shape in **re-fetched docs** (never memory), and finish with a traceability matrix, a quality-gate decision, and a written `test-report.md`.

## Conventions

- Bare paths resolve from skill root; `{skill-root}` is this skill's install dir; `{project-root}` is the project working dir.
- **Doc-grounding.** At test-write time, re-fetch the authoritative Juspay doc pages (recorded in the architecture doc / `task-checklist.md` `doc-refs`) via `docs-mcp` for exact field names, request/response shapes, error codes, and test cards/VPAs — never assert them from memory.
- **Stack-mirroring.** Detect the repo's existing test framework and conventions (dir layout, naming, fixtures) and **write tests in that framework**. Use inline curl/bash **only** when no runner exists. Never bolt on a new framework the repo doesn't already use without checkpointing first.
- **Test-quality DoD.** Every persisted test is deterministic, isolated, explicit, and focused — no hard waits/sleeps, no inter-test order dependence, no uncontrolled random data, assertions visible in the test body. See `references/payment-test-matrix.md`.
- **Secrets boundary.** Credentials (API keys, webhook auth) are read from `.env`/secret stores and passed to tests via exported env vars only — never inlined in a test file, the report, logs, or command output. No secret value ever appears in any artifact.
- **Scope is the intersection.** Test only what the architecture put **in scope** ∩ what jp-executor **actually built** ∩ what the **environment supports**. Never manufacture tests for un-built work or out-of-scope methods.
- **Split-repo aware.** FE and BE may live in separate repos. In a `split` run, validate only the side present here and add **contract-conformance** checks (this side honors the Cross-Side Contract); the cross-side end-to-end transaction can't be driven (the other repo is absent) → record it as a documented manual/gap. See `references/split-integration.md`.
- **Workspace.** `{doc_workspace}` is `{project-root}/docs/juspay/` — reads `prd.md`, `architecture.md`, `task-checklist.md`, `integration-summary.md` (if present), and an incoming `handoff-<this_side>.md` (if present, for the contract); writes test code into the user's codebase, updates the `test` task `status` values in `task-checklist.md`, and writes `test-report.md` back to `{doc_workspace}`. It does **not** write or alter `integration-summary.md` or `handoff-*.md` — those belong to `jp-executor`.
- **No config of our own.** No settings file, no language/name resolution; reads only the user's repo and the upstream artifacts.
- **Stage tracking.** This skill owns the `validation` funnel phase (and the `live` phase, strictly gated) — `started` in `steps/step-01-init.md`, terminal in `steps/step-05-report.md`, via `juspay_track_integration_stage` (fire-and-forget, never blocking). See `references/integration-stage-tracking.md`.

## On Activation

Briefly orient the user: this skill tests a Juspay integration that `jp-executor` built, adapting to the repo's existing test stack and writing a `test-report.md`. There is no settings file. Then load `./steps/step-01-init.md`, which gates on a built integration.

## Execution

Read fully and follow: `./steps/step-01-init.md`. The step chain:

1. `step-01-init.md` — gate (a *built* integration is required), load artifacts, **detect the test stack**, re-scan what was actually built → test-target inventory, reuse juspay-mcp mode. *(always)*
2. `step-02-test-design.md` — risk-based test design: intersect in-scope × built × env-supported, assign P0–P3, choose level + execution mode (framework-native file vs inline) per item, build the traceability matrix, environment preflight, checkpoint the plan. *(always)*
3. `step-03-backend-tests.md` — order/session creation, status + reconciliation, webhook signature + idempotency, refund/payout, constraint boundaries, error-code paths. *(only if a backend/API surface was built)*
4. `step-04-frontend-sdk-tests.md` — web transaction drive (test cards/VPAs) + return-URL/reconciliation check; mobile/native manual guide. *(only if a web/SDK/native surface was built)*
5. `step-05-report.md` — traceability matrix, PASS/CONCERNS/FAIL quality gate, payment-NFR checks, integration-stage confirmation; write `test-report.md`, finalize `test` task statuses. *(always)*

**Steps 3 and 4 are conditional.** Each opens with an APPLICABILITY gate and **self-skips** when the test-target inventory has no surface of its kind — a backend-only integration skips frontend/SDK; a web/SDK-only integration skips backend-specific items. Test **only what this integration actually built**.

This is **action-oriented**: write and run real tests, but **checkpoint before risky/external actions** (starting the dev server, running live transactions, anything that moves money or hits production). **Production is enforced** — run against production; don't ask which environment to use, and only use a non-production environment if the user explicitly and unpromptedly requested it. A dummy/test gateway returned by the MCP is acceptable for integration testing.

> `juspay-mcp` is auth-guarded and optional; reuse the **mode** the upstream skills already recorded (see `references/juspay-mcp.md`) and don't re-ask. Every `juspay-mcp`-derived datum has a manual fallback so the flow never blocks.
