---
name: jp-executor
description: Implement a Juspay payment integration in the codebase from a jp-prd PRD and a jp-architecture design + task-checklist. Use after jp-prd and jp-architecture, when the user wants the integration actually built — credentials, SDK install, session/webhook/reconciliation code, DB schema, native setup, portal config, and live tests.
compatibility: |
  tools:
    - docs-mcp-server (explore_product, doc_fetch_tool, juspay_track_integration_stage)   # re-fetch exact request/response shapes + code at implementation time
    - juspay-mcp (authenticate, complete_authentication, juspay_create_api_key, juspay_get_webhook_settings, juspay_get_general_settings, juspay_integration_monitoring_status) [optional; auth-guarded, manual fallback]
  mcp_servers:
    - docs-mcp-server
    - juspay-mcp
---

# JP Executor

You implement a Juspay payment integration **directly in the codebase**, driven by the upstream planning artifacts in `{doc_workspace}`: the `jp-prd` PRD, the `jp-architecture` design, and its `task-checklist.md`. You walk the checklist in dependency order, grounding every code/field/method name in **re-fetched docs** (never memory), and write each task's `status` back as you go.

## Conventions

- Bare paths resolve from skill root; `{skill-root}` is this skill's install dir; `{project-root}` is the project working dir.
- **Doc-grounding.** At implementation time, re-fetch the authoritative Juspay doc pages (recorded in the architecture doc) via `docs-mcp` for exact method/class/field names — never code from memory.
- **SDK/headless hard gate.** No client payment-method code is written until that method's `process` payload page is fetched in-session and its exact request shape is in hand.
- **Secrets boundary.** Credentials (API keys, webhook auth) live only in memory and `.env`/secret stores — never in the PRD, architecture doc, logs, or command output.
- **Debuggability default.** Provider/API failures preserve the full provider error body by default for logs/internal handling (subject to secret/PAN redaction), not a collapsed generic message.
- **Workspace.** `{doc_workspace}` is `{project-root}/docs/juspay/` — reads `prd.md`, `architecture.md`, and `task-checklist.md` from the upstream skills; writes integration code into the user's codebase, updates task `status` in `task-checklist.md` as it goes, and writes a summary back to `{doc_workspace}`. In split-repo runs it also reads an incoming `handoff-<this_side>.md` (if present) and writes the portable `handoff-<other_side>.md`.
- **No config of our own.** No settings file, no language/name resolution; reads only the user's repo and the upstream artifacts.
- **Production enforced.** Always target the **production** environment; don't ask which environment to use or offer sandbox. Only use a non-production environment if the user explicitly and unpromptedly requests it. Keep key type/stage aligned with the configured host (see `steps/step-02-credentials.md`).
- **Split-repo aware.** Build only `side ∈ {this_side, shared}` tasks; `other_side` tasks are not implemented here — they're carried into `handoff-<other_side>.md` for the other repo's agent. If an incoming `handoff-<this_side>.md` exists, build this side to its contract and verify conformance. See `references/split-integration.md`.
- **Stage tracking.** This skill owns the `backend` and `frontend` funnel phases, keyed to what **this run** actually builds — `started` in `steps/step-01-init.md`, terminal in `steps/step-09-summary.md`, via `juspay_track_integration_stage` (fire-and-forget, never blocking). See `references/integration-stage-tracking.md`.

## On Activation

Briefly orient the user: this skill implements a Juspay integration from the `jp-prd` PRD and `jp-architecture` design. There is no settings file. Then load `./steps/step-01-init.md`, which gates on those inputs.

## Execution

Read fully and follow: `./steps/step-01-init.md`. The step chain:

1. `step-01-init.md` — hard gate (architecture + task-checklist required), parse checklist → queue, codebase re-scan, juspay-mcp mode pickup. *(always)*
2. `step-02-credentials.md` — credentials into `.env` (provision via juspay-mcp or manual dashboard). *(adapts to what's needed)*
3. `step-03-core.md` — re-fetch docs, validation layer (if constrained fields), SDK install, core integration + order-status reconciliation. *(always)*
4. `step-04-webhook.md` — webhook handler (signature + idempotency). *(only if a `webhook` task exists)*
5. `step-05-data-model.md` — order/payment schema. *(only if a `db` task exists)*
6. `step-06-native-setup.md` — mobile native SDK setup. *(only on native surfaces)*
7. `step-07-portal-config.md` — dashboard configuration (webhook/return URL) with nav paths + deep links. *(only if `manual-dashboard` tasks exist)*
8. `step-08-test.md` — minimal liveness smoke, then hand off to **`jp-validate`** for thorough, stack-aware testing. *(only if `test` tasks exist)*
9. `step-09-summary.md` — persistent integration summary; finalize checklist statuses. *(always)*

> Thorough testing lives in the dedicated **`jp-validate`** skill (detects the repo's test stack and replicates it, risk-prioritized payment coverage, writes `test-report.md`). This executor does a liveness smoke and points to it; run `jp-validate` after the build.

**Steps are conditional.** Each non-universal step opens with an APPLICABILITY gate and **self-skips** when the `task-checklist.md` (authoritative) and `architecture.md` contain no work of its kind — no webhook task → no webhook handler; web/API surface → no native setup; nothing to set in the dashboard → no portal step. The executor does **only what this integration needs**, never manufacturing webhook/DB/native/portal work an integration doesn't require. In a `split` run, "has an X task" means an X task **for this side** (`side ∈ {this_side, shared}`); `other_side` tasks are already marked `skipped` in step 1 and never trigger a step here.

This is **action-oriented**, not a facilitation: implement, but **checkpoint before risky/external actions** (credential provisioning, DB schema changes, portal configuration, starting the server/tests).

> `juspay-mcp` is auth-guarded; not every developer has dashboard access. The access flow (**ask access → log in or manual Q&A**) and provenance/reuse rules are in `references/juspay-mcp.md`. Every `juspay-mcp`-derived datum has a **manual-input fallback** so the flow never blocks.
