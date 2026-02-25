---
name: spendguard-strict-budget-runner
description: Run application agents through SpendGuard with strict hard budget caps. Use when setting up `spendguard-sidecar`, creating agent IDs, setting or topping budgets, sending OpenAI/Grok/Gemini/Anthropic calls through SpendGuard endpoints, and troubleshooting budget enforcement errors like insufficient budget, in-flight lock conflicts, missing `x-cynsta-agent-id`, or remote pricing signature failures.
---

# SpendGuard Strict Budget Runner

## Overview

Use this skill to operationalize strict-budget execution.

## Quick Start

1. Load `references/strict-budget-quickstart.md`.
2. Start sidecar in strict remote-pricing mode.
3. Create agent and set hard budget with CLI or `scripts/bootstrap_strict_budget.py`.
4. Route model calls through SpendGuard and include required headers.
5. Confirm budget decrement and handle failures using `references/error-playbook.md`.

## Workflow

### 1) Start SpendGuard in strict mode

Use sidecar mode with remote signed pricing verification enabled. Do not bypass signature checks for normal usage.

See full env setup in `references/strict-budget-quickstart.md`.

### 2) Create budgeted agent identity

Prefer CLI:

```bash
spendguard agent create --name "my-agent"
spendguard budget set --agent <agent_id> --limit 5000 --topup 5000
spendguard budget get --agent <agent_id>
```

Use script when deterministic JSON output is needed:

```bash
python scripts/bootstrap_strict_budget.py --name my-agent --limit 5000 --topup 5000
```

### 3) Route model calls through SpendGuard

Send requests to sidecar `.../v1/...` routes, not directly to provider APIs.

Required:

- Header `x-cynsta-agent-id: <agent_id>`
- Optional `x-cynsta-run-id: <run_id>` for explicit run tracking

Load `references/routing-patterns.md` for OpenAI SDK and direct HTTP patterns.

### 4) Enforce strict budget behavior

Expect:

- `402` when budget is insufficient for reserve
- `409` when same agent budget is locked by another in-flight run
- `400` for malformed payload or missing required headers

Apply fixes from `references/error-playbook.md`.

### 5) Validate before finishing

Run these checks after setup:

1. Health endpoint returns `{"status":"ok"}`.
2. `budget get` returns expected `remaining_cents`.
3. One real or mocked model call succeeds through sidecar.
4. Remaining budget decreases after settled usage.

## Guardrails

- Use one agent per isolated budget domain; do not share agent IDs across unrelated workloads.
- Keep budgets in cents and treat `hard_limit_cents` as the strict cap.
- Keep `CAP_PRICING_VERIFY_SIGNATURE=true` in normal operation.
- In hosted mode, pass API key via `--api-key` or `CAP_API_KEY`.
