---
name: honeyhive-instrument
description: >
  Instrument an AI application with HoneyHive tracing. Use when the user wants
  to add observability, capture traces, set up the SDK, configure exporters,
  or wire OpenTelemetry-compatible instrumentation for an agent, RAG pipeline,
  or LLM application. Triggers on phrases like "add tracing", "instrument my
  app", "wire up HoneyHive", "set up the SDK", "capture spans", "OTEL
  exporter", or any mention of `HoneyHiveTracer.init`, `@honeyhive/api-client`,
  `client.sessions.startSession`, `client.events.createEvent`, or
  `OpenInference`/`Traceloop` instrumentors targeting HoneyHive.
license: MIT
metadata:
  version: "0.2.1"
  homepage: https://docs.honeyhive.ai
  feedback_url: https://github.com/honeyhiveai/skills/issues
---

# HoneyHive Instrument

Wire HoneyHive tracing into a user's application with a small, surgical edit set: initialize the tracer, attach an instrumentor for their LLM/agent framework, and verify spans flush and the trace is visible in HoneyHive.

> **You are an instrumentation surgeon, not a rewriter.** The user has working code. Add tracing in the smallest number of edits possible. Never refactor unrelated code, never change framework versions, never strip features.

## Three phases only

This skill has exactly three phases. Each phase has a **checkpoint** — a concrete artifact that proves the phase ran. If you skip a phase, the checkpoint will be missing and the eval will catch it.

| Phase | Goal | Checkpoint |
|-------|------|------------|
| **Validate** | Confirm network + runtime before touching code | Curl returns HTTP 200 + runtime findings recorded |
| **Setup** | Add tracing wiring via the language-specific reference | Exactly one setup reference loaded + edits applied |
| **Verify** | Smoke run + grade against success.md | Session visible in HoneyHive + success.md loaded and graded |

## Phase 1 — Validate (deterministic, no user questions until stuck)

Validation is deterministic discovery. Run checks in order; stop on failure. Only ask the user when a check is ambiguous.

### Step 1.1 — Network validation

Load and follow [references/network-validation.md](../honeyhive-cli/references/network-validation.md).

Run the reachability check:

```bash
curl -sS -o /dev/null -w "HTTP %{http_code}\n" \
  -H "Authorization: Bearer $HH_API_KEY" \
  "${HH_DATA_PLANE_URL:-$HH_API_URL}/healthcheck"
```

**Checkpoint:** Curl returns HTTP 200. If not, stop with the exact error from the interpretation table below. Do not retry. Do not proceed.

| HTTP code | Cause | Recovery |
|-----------|-------|----------|
| 200 | Valid | Proceed |
| 401 | Key invalid for this deployment | Redirect user to project settings: https://app.us.honeyhive.ai/settings/project/keys |
| 403 | Key lacks project scope | Redirect user to project settings: https://app.us.honeyhive.ai/settings/project/keys |
| 404 | Wrong URL | Verify the deployment URL (`HH_DATA_PLANE_URL` for TS/CLI, `HH_API_URL` for Python), no trailing slash |
| 000 | Egress blocked | Surface URL + port to network team |

### Step 1.2 — Runtime validation

Load and follow [references/runtime-validation.md](references/runtime-validation.md).

This is a read-only scan. Do not edit any files. Detect:

1. **Subtree** — locate the LLM app in a monorepo (ask if ambiguous)
2. **Language + runtime** — from manifests (pyproject.toml, package.json, go.mod, etc.)
3. **Framework + version** — which LLM SDK is pinned
4. **Instrumentor family** — OpenInference vs Traceloop (Python only)
5. **Existing HH wiring** — grep for `HoneyHiveTracer.init` / `new Client(`
6. **Existing OTel provider** — grep for `TracerProvider` setups from other vendors

**Checkpoint:** All six findings recorded. The setup path (Python / TypeScript / native OTel) is determined.

### Step 1.3 — Confirm the path with the user

Present findings and the proposed setup path. Confirm before adding dependencies.

## Phase 2 — Setup (load exactly one language reference; follow it end-to-end)

Pick the path that matches runtime-validation findings. Load **exactly one** setup reference:

- **Python** — [references/python-setup.md](references/python-setup.md)
- **TypeScript** — [references/ts-setup.md](references/ts-setup.md)
- **Native OTel** (Go, Rust, Java, .NET, any bespoke OTel) — [references/otel-setup.md](references/otel-setup.md)

Each setup file consumes Phase 1's findings and has its own internal steps (dependency plan, init placement, session boundaries, distributed propagation, verification). Follow it end-to-end.

**Load additional references only when findings demand it:**
- `existing_otel_provider = real:<vendor>` → also load [references/co-existence.md](references/co-existence.md)
- `deployment_type = dedicated | self-host` → also load [references/dedicated-deployments.md](../honeyhive-cli/references/dedicated-deployments.md)

For frameworks with first-class docs coverage, also pull the framework's integration docs page for the exact install + minimal-integration block — copy verbatim, adapt to the user's entry-point:

- **Integrations index** — <https://docs.honeyhive.ai/v2/integrations> (find the user's framework here)
- **Tracing quickstart** — <https://docs.honeyhive.ai/v2/introduction/tracing-quickstart>
- **Troubleshooting** — <https://docs.honeyhive.ai/v2/introduction/troubleshooting>
- **SDK reference** — <https://docs.honeyhive.ai/v2/sdk-reference> (Python, TypeScript, semconv)

**Checkpoint:** Setup reference loaded. Dependency changes proposed (not yet committed). Init placement, session boundaries, and propagation strategy decided.

If the user's framework isn't on the index above, follow the doc-gap protocol in Phase 3 step 3.

## Phase 3 — Verify

### Step 3.1 — Smoke run

Run the user's main entry-point with a one-line dummy prompt (if env vars are set). Confirm:
- Process exits 0
- No OTEL warnings (`No tracer provider has been initialized`, `Span context lost`)

### Step 3.2 — Mechanical trace check

Query for events using the events search endpoint:

```bash
curl -s -X POST "${HH_DATA_PLANE_URL:-$HH_API_URL}/v1/events/search" \
  -H "Authorization: Bearer $HH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"project": "<project-name>", "filters": [{"field": "event_type", "operator": "is", "value": "session", "type": "string"}], "limit": 5}'
```

Find the most recent session, then search for its child events:

```bash
curl -s -X POST "${HH_DATA_PLANE_URL:-$HH_API_URL}/v1/events/search" \
  -H "Authorization: Bearer $HH_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"project": "<project-name>", "filters": [{"field": "session_id", "operator": "is", "value": "<session-id>", "type": "string"}], "limit": 50}'
```

Verify: at least one event exists, and at least one has `event_type: "model"` (LLM span). If the smoke run exits cleanly but zero events or no model events are visible, do not guess at code changes first. Consult <https://docs.honeyhive.ai/v2/introduction/troubleshooting>, then inspect env vars, dependency installation, exporter output, and shutdown behavior as applicable. Only return to Phase 2 after those checks point to instrumentation placement or instrumentor choice.

### Step 3.3 — Grade against success criteria

Load [success.md](success.md) and grade the trace:

- **Trace structure** — are event names meaningful? are model events shallow (depth ≤ 2)? are tool calls linked to parent agent?
- **Input/output cleanliness** — does the session show the user's query? do LLM events show full message history + tools + response?
- **Semantic failures** — are errored events surfaced clearly, not buried in metadata?
- **Summarisability** — is there a final event with enough context for end-to-end evaluators?

If the trace is mechanically correct but qualitatively messy, circle back to Phase 2 and adjust session-boundary placement or instrumentor choice. **A mechanically-correct integration that produces a messy trace is not done.**

> **Auto-instrumentation may not capture everything important.** If the trace is missing key steps (e.g., retrieval, tool calls, orchestration logic), add manual spans and enrichments using the APIs from the setup reference loaded in Phase 2. Auto-instrumentation is the starting point, not the ceiling.

### Step 3.4 — Verify against MUSTs

Review the code changes against the Requirements (MUSTs) section below. Confirm no violations (hardcoded keys, dual tracer, global provider hijack, etc.).

### Step 3.5 — Doc-gap surfacing

If during discovery you found a framework, instrumentor, or OTel exporter combination not covered above, do **not** improvise. Tell the user: "I've flagged this as a doc gap; here's the working install I produced; please open an issue at <https://github.com/honeyhiveai/skills/issues> if you'd like first-class coverage."

**Checkpoint:** Session visible in HoneyHive with model events. success.md loaded and graded. Trace passes the rubric.

## Stop

Single-pass. Do not continue iterating after success criteria are met. Instrumentation is the only goal — once spans are flowing and the trace grades well, hand off to the user. Anything beyond (evaluating quality, improving prompts, tuning retrieval) is out of scope.

## References

Load only when the phase calls for them. Progressive disclosure keeps context tight.

**Peer files:**

- [success.md](success.md) — qualitative rubric for Phase 3 trace grading

**Phase 1 — Validation:**

- [references/network-validation.md](../honeyhive-cli/references/network-validation.md) — env var sourcing, curl reachability, status-code interpretation, TLS chain
- [references/runtime-validation.md](references/runtime-validation.md) — subtree, language, framework, instrumentor, existing wiring, existing provider

**Phase 2 — Setup (load exactly one):**

- [references/python-setup.md](references/python-setup.md) — Python path
- [references/ts-setup.md](references/ts-setup.md) — TypeScript path
- [references/otel-setup.md](references/otel-setup.md) — Native OTel path (any language)

**Operational (load when findings demand it):**

- [references/co-existence.md](references/co-existence.md) — sharing a TracerProvider with a non-HH vendor
- [references/dedicated-deployments.md](../honeyhive-cli/references/dedicated-deployments.md) — dedicated and self-host URL wiring
- [references/prod-gotchas.md](references/prod-gotchas.md) — production checklist (deps, threading, memory, certs, PII, sampling)

## Requirements (MUSTs)

These are hard rules. Violating any one is a skill failure that evaluators will catch.

- **MUST NOT proceed past Phase 1 without successful network validation.** Wrong URL or rejected key means every later step rebuilds sand.
- **MUST NOT globally register HoneyHive as the source-of-truth TracerProvider.** The SDK doesn't do this; instrumentation code must not either. Evaluator: `no-global-provider-hijack`.
- **MUST NOT construct two tracers (Python) or two Client instances (TS).** Reuse the existing instance. Evaluator: `no-dual-tracer-instances`.
- **MUST NOT hardcode API keys.** Always sourced from env vars. Evaluator: `no-hardcoded-api-keys`.
- **MUST NOT let the deployment URL silently fall back to the wrong host.** Confirm explicitly — the env var name varies by SDK (`HH_DATA_PLANE_URL` for TS/CLI, `HH_API_URL` for Python). Multi-tenant default is `https://api.dp1.us.honeyhive.ai`; dedicated and self-host customers have their own.
- **MUST NOT switch instrumentor families** (OpenInference ↔ Traceloop) without explicit user consent.
- **MUST NOT thread session_id through function signatures** (TS path). Use a module-level helper or async-context store.
- **MUST NOT bump SDK or framework versions** to make instrumentation work.
- **MUST NOT modify test files or lock files** unless the user explicitly asks.
- **MUST NOT run a production deploy step.** Local smoke run is the verification ceiling.
- **MUST load success.md at verification time** (Phase 3), not at the start.
- **MUST record runtime-validation findings** before loading a setup reference. The setup file consumes findings, it does not re-detect.
