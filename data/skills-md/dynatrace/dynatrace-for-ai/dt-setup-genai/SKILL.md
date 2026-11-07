---
name: dt-setup-genai
description: >-
  Framework-independent decision process for instrumenting a GenAI/LLM app (Python or
  TypeScript, any provider/agent SDK) so it emits OTel GenAI semantic-convention
  (gen_ai.*) spans queryable in Dynatrace. Four steps: detect, instrument, enrich,
  validate. Decides which approach a given SDK needs; does not replace the concrete
  per-framework recipes in dynatrace-oss/dynatrace-ai-agent-instrumentation-examples.
  Trigger: "instrument this GenAI app", "add tracing to this LLM app", "how do I get
  gen_ai spans into Dynatrace", "onboard this agent app to AI Observability". Do NOT
  use for analyzing telemetry from an already-instrumented app (use dt-obs-genai) or
  for languages other than Python/TypeScript.
license: Apache-2.0
---

# Instrument a GenAI app for Dynatrace

This is the shared decision process behind the per-framework recipes in
[`dynatrace-oss/dynatrace-ai-agent-instrumentation-examples`](https://github.com/dynatrace-oss/dynatrace-ai-agent-instrumentation-examples)
— referred to throughout as **the examples repo** — factored out so it applies to an
SDK that repo doesn't cover yet. It tells you which recipe shape to reach for and why,
and what "done" looks like regardless of the SDK/language. Once spans are flowing, load
**dt-obs-genai** to analyze them.

## When you should not use this skill

- Already instrumented, and you want to query/debug GenAI telemetry → **dt-obs-genai**.
- You already know the SDK's recipe and just want the copy-paste code → go straight to the examples repo; this skill decides *which* recipe shape applies, not replaces it.
- The app isn't Python or TypeScript → out of scope for this skill.

## Where this skill must stop and ask

- **Any edit to the customer's application code** — show the diff, get a yes, first.
- **Credentials** — the customer creates the Dynatrace token and provider keys. Never print, log, or store a token value; reference it only via env var or secret store.
- **Deploying an OpenPipeline pipeline** to their tenant.
- **Provider config this skill can't infer** — Azure deployment name/API version, Ollama model tag, Bedrock region/profile.
- **Adding a collector to their runtime** — out of scope; infrastructure, not configuration.
- **Enabling message-content capture** — **off by default; only enable it if the user asks.**
  Prompts/completions can carry PII or sensitive data, and the knob is **SDK-specific**:
  `OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=true` for some instrumentors; a
  framework-native flag the env var does **not** control and that can **default to on** for others
  (e.g. pydantic-ai's `InstrumentationSettings(include_content=...)`); OpenInference captures
  content by default; and Traceloop/OpenLLMetry `opentelemetry-instrumentation-<sdk>` packages read
  `TRACELOOP_TRACE_CONTENT`, default **ON**, ignoring the OTel-standard var. Check the SDK's actual
  toggle so you don't ship capture on unnoticed; agree on redaction if needed.

## The four steps

```
detect ─▶ instrument ─▶ enrich ─▶ validate
  │                                  │
  └──────────── feedback loop ───────┘
   (validate failure → fix in enrich or instrument)
```

### 1. Detect

Figure out *what* you're instrumenting before touching any code.

**Inputs:**
- Dependency manifest (`pyproject.toml` / `requirements.txt` / `package.json`) — which
  LLM SDK(s), agent framework, or observability SDK are present (OpenAI, Anthropic,
  Bedrock, LangChain/LangGraph, CrewAI, MCP server/client, Langfuse, ...). An app can
  depend on more than one — see [references/multi-sdk-apps.md](references/multi-sdk-apps.md).
- Whether the host already runs Dynatrace **OneAgent** (`oneagent` process/package
  present) — if so, OneAgent auto-instruments common HTTP/SDK calls with zero code
  changes, which changes everything downstream.
- Whether the app already has *any* OTel wiring — an existing global `TracerProvider`,
  an existing `Traceloop.init()`/instrumentor call, or existing custom span code.

**Outputs:** a **routing key** `(framework/SDK, existing-instrumentation-state)` per SDK
(see [references/multi-sdk-apps.md](references/multi-sdk-apps.md) if more than one), a
**branch decision** (below), and a **native-OTel yes/no** decision (step 2) per SDK.

**How to decide native-OTel vs. fallback:** **prefer** SDKs with a pure-OTel path (native
`gen_ai.*`). An SDK without one falls back to OpenInference — which closes the loop only if it
emits `gen_ai.*` (Python semconv dual-write, step 2), else it stops at a normalizer gate. Work
through these in order and stop at the first hit:
1. Check `references/examples-index.md` for the SDK. A listed `opentelemetry/` recipe is
   the fast path — use it.
2. If the SDK isn't listed, check the [OpenTelemetry registry](https://opentelemetry.io/ecosystem/registry/)
   and the vendor SDK's own docs for native OTel/`gen_ai.*` support (e.g. an `otel`
   extra, a `span_exporter`/tracer-provider hook, or built-in semconv attributes).
   Finding one → instrument it (step 2).
3. **No native OTel path → OpenInference.** Instrument with the matching
   `openinference-instrumentation-<sdk>` package from an examples-repo recipe; if not even that
   exists, hand-write manual `gen_ai.*` spans
   ([references/no-native-instrumentation.md](references/no-native-instrumentation.md)).
   OpenInference closes the loop **only when it emits `gen_ai.*`** — a Python instrumentor with
   semconv dual-write on (step 2). Otherwise (TS/node, older version, unset) spans stay
   `llm.*`/`openinference.*` and the skill **stops at a normalizer gate**
   ([references/enrich-normalization.md](references/enrich-normalization.md)), then resumes.

### 2. Instrument

Wire up span emission. **Prefer the pure-OTel path**; fall back to OpenInference only when
no native OTel path exists. That fallback closes the loop only when it emits `gen_ai.*`
(semconv dual-write, below); otherwise it stops at a normalizer gate before Validate.

- **Pure OTel (preferred, supported end-to-end).** A native OTel instrumentation package, or
  the framework's own OTel integration, emitting `gen_ai.*` directly — exported straight to the
  Dynatrace OTLP endpoint (host + scope rules in the common shape below) or via a collector. Many
  agent frameworks and vendor SDKs ship one (or accept a custom `span_exporter`); the current list
  lives in the examples repo, not here. ⚠️ Prefer the genuine OTel-published instrumentor over a
  Traceloop/OpenLLMetry one — Traceloop/OpenLLMetry is reportedly sunset upstream, so **don't use it
  for new instrumentation** (treat an app already on it as enhance-existing/migration). It also
  defaults message-content capture on; which package and how to route it live in
  [references/examples-index.md](references/examples-index.md) §1a.
- **Fallback = OpenInference.** No native OTel path → the matching
  `openinference-instrumentation-<sdk>` package from an examples-repo recipe
  (`OpenAIInstrumentor`, `AnthropicInstrumentor`, ...). **Before initializing it, explicitly
  disable that SDK's default-on message-content capture using its documented setting; do not
  rely on the OTel-standard env var. If capture cannot be disabled, stop and ask before
  running a request.** Python instrumentors can dual-write
  it validates like native. **Otherwise** (TS/node, older version, or unset) spans stay
  `llm.*`/`openinference.*` and the skill **stops before Validate** until the user applies a
  normalizer ([references/enrich-normalization.md](references/enrich-normalization.md)). No
  OpenInference package either → hand-write manual spans
  ([references/no-native-instrumentation.md](references/no-native-instrumentation.md)).
- **OneAgent present:** skip this step — no code changes, OneAgent auto-instruments.
  Only give the app/service a **unique title** (e.g. `FastAPI(title=...)`) so
  Smartscape creates a distinct entity instead of merging it with another app.

**Common shape, in greenfield mode (when not using OneAgent):** match the app's existing
package manager; if creating from scratch (Python), default to **`uv`**.
1. Build a `Resource` with at least `service.name`, and create a `TracerProvider` with
   it. `gen_ai.agent.name` and other agent-identity attrs are **span-level**, not
   Resource-level — the GenAI views and agent quick filter read them off the span, so
   set them at span creation or in a span processor (see Enrich), not on the `Resource`.
2. Attach a span processor + OTLP exporter pointed at either Dynatrace directly or a
   local OTel Collector (`http://localhost:4318`) when Enrich needs a transform first.
   **The endpoint form depends on the exporter — they are not interchangeable:**
   - A collector's `otlphttp` exporter takes the base path (`$DT_ENDPOINT/api/v2/otlp`)
     and appends `/v1/<signal>` itself.
   - An SDK-native exporter (e.g. Python's `OTLPSpanExporter(endpoint=...)`, Node's
     `OTLPTraceExporter`) uses the endpoint **verbatim** as the POST URL — pass the full
     `$DT_ENDPOINT/api/v2/otlp/v1/traces` (or `/v1/metrics`, `/v1/logs`), or it 404s.
   Header: `Authorization: Api-Token $DT_API_TOKEN`, token scope `openTelemetryTrace.ingest`
   plus `metrics.ingest`/`logs.ingest` if needed. Never print, log, or store the token value.
3. Call the instrumentor / SDK init *before* the app's first LLM call, not lazily
   inside the request handler, and wrap the call so session/conversation correlation
   can be attached (see Enrich).

**Inputs:** routing key + native-OTel decision from step 1; `DT_ENDPOINT`/`DT_API_TOKEN` or
collector endpoint; service name.
**Outputs:** a running app emitting spans — `gen_ai.*` directly (pure OTel), or
`llm.*`/`openinference.*` pending a user-side normalizer (fallback).

### 3. Enrich

Get spans to full `gen_ai.*` semantic-convention compliance and add cross-cutting context.

**Always do, regardless of path:**
- Set metrics export to **delta temporality** (`OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE=delta`) — Dynatrace rejects cumulative metrics with a 400.
- Message-content capture (`OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=SPAN_ONLY` or
  `SPAN_AND_EVENT`, a framework-native flag, or OpenInference's default-on capture) is a
  **stop-and-ask** decision — see above. Once approved, confirm `gen_ai.input.messages` /
  `gen_ai.output.messages` land.
- Set a **stable conversation ID once per conversation, not regenerated per request**,
  targeting `gen_ai.conversation.id`. **Prefer a framework-native mechanism** where one exists
  (e.g. pydantic-ai derives `gen_ai.conversation.id` from its run/message history through its
  instrumentation); else the language-specific span mutation API at the call site if you create
  the span yourself (`set_attribute` in Python or `setAttribute` in Node — e.g. the
  no-native-instrumentation manual-span path); for an auto-instrumenting baseline package that
  creates spans internally with no call-site handle, register the language-specific span-processor
  hook (`on_start` in Python, `onStart` in Node) and set the attribute before the span is exported
  — the same mechanism works for any attribute the instrumentor omits that your app can supply.
  In **multi-agent apps, thread the same id through every agent/sub-agent call** — else each run
  emits its own id and the conversation fragments into pieces sharing only a `trace.id`.
  OpenInference users: `using_attributes(session_id=...)` emits `session.id`, not
  `gen_ai.conversation.id`, so confirm the
  [normalization rule](references/enrich-normalization.md) actually maps it.
- For agent frameworks, expect **nested spans** (crew/workflow → agent → task/tool);
  derive duration metrics from span-name/span-kind, not `gen_ai.operation.name` — CrewAI
  sets that to `invoke_agent` on all three levels at once, folding them into one histogram.

**Fallback path (OpenInference) — user-side normalization gate:** when semconv dual-write
isn't available (TS/node, older versions), spans arrive as `llm.*`/`openinference.*`, not
`gen_ai.*`, so Validate cannot pass until they're normalized — and the skill **can't do this
step for the user**. Hand them the example normalizer config (collector `gen_ai_normalizer` or
OpenPipeline — see [references/enrich-normalization.md](references/enrich-normalization.md)),
and only resume Validate once they confirm it's applied.

**Inputs:** raw spans from step 2 — `gen_ai.*` (pure OTel), or `llm.*`/`openinference.*`
awaiting the user-side normalizer (fallback).
**Outputs:** `gen_ai.*`-compliant spans, with conversation correlation, plus any derived
agent/workflow duration or token-usage metrics.

### 4. Validate

Confirm the pipeline works end-to-end, against a known contract — don't eyeball it.
**`dtctl` is the primary loop:** it queries the emitted spans in Dynatrace so the
assertion is mechanical and repeatable. The full recipe, contract pin, and severity rules
live in [references/validate-contract.md](references/validate-contract.md).

**Inputs:** the running, instrumented app from steps 2–3. On the OpenInference fallback,
only start Validate **after** the user confirms their normalizer is applied (the Enrich
gate) — otherwise every check below fails on `llm.*` spans that were never mapped.
**Steps:**
1. Send a real request through the app.
2. **Check `dtctl` is installed** (`dtctl version`); if not, install it from the
   [dtctl README](https://github.com/dynatrace-oss/dtctl) before continuing.
3. **Query the resulting spans with `dtctl`**, filtered by `service.name` — see the ready
   `dtctl query` in [references/validate-contract.md](references/validate-contract.md).
   (Manual fallback if `dtctl` is unavailable: the same `fetch spans` DQL in the AI
   Observability app's Explorer / Distributed Tracing app — load **dt-dql-essentials** for
   query syntax — but it loses the repeatable assertion `dtctl` gives you.)
4. Assert the mandatory fields and metrics declared by the contract profile matching the app's
   provider — at minimum `gen_ai.provider.name`/`gen_ai.system` (any-of; prefer emitting
   `gen_ai.provider.name`). Treat `gen_ai.operation.name` as recommended unless the selected
   profile/scenario marks it required, and apply inference/provider-specific fields only where
   that profile says they apply. Severity (fail vs. warn) and per-provider profiles:
   [references/validate-contract.md](references/validate-contract.md).
**Outputs:** pass/fail against the contract. On failure, the fix belongs in **Enrich**
(missing/wrong attribute mapping) or **Instrument** (wrong SDK/collector config) — not
in Validate itself; Validate only ever detects, it doesn't patch. After fixing, re-run the
same `dtctl` query to confirm.

**OneAgent path:** steps 1–4 are unchanged — still query with `dtctl` — but a failure has
no Instrument/Enrich step to route to: it's either an unfixable OneAgent-version gap
(report it) or a non-unique step 2 entity title (fix it). Once Validate passes, load
**dt-obs-genai** to analyze.

## Greenfield vs. enhance-existing

Both branches run the same four steps — they differ in what Detect finds and what
Instrument is allowed to touch. **Default to enhance-existing; greenfield is the narrow
exception.**

**Enhance-existing** — the task targets an **existing** repository, application, template,
example collection, workflow, or configuration, **even when the specific file or example you're
asked to add doesn't exist yet.** There is a contract to preserve — a sibling implementation, an
instrumentation setup, a build/dependency convention, a test harness, a deployment config — so
**conform to it; don't invent a parallel one.** The greenfield "Common shape" is **not safe to
copy verbatim**: a fresh `Resource`/`TracerProvider` silently replaces an existing one and can
drop spans the app relies on. See [references/enhance-existing.md](references/enhance-existing.md)
for the per-case breakdown and the service-naming collision rule.

**Greenfield** — applies **only** when there is no existing repository contract, sibling
implementation, instrumentation setup, build convention, test harness, or deployment
configuration to preserve. Only then does Instrument create a fresh
`Resource`/`TracerProvider`/exporter with no risk of clobbering anything. **If in doubt, it's
enhance-existing** — match what's there rather than scaffold something new.

## References

- [dynatrace-oss/dynatrace-ai-agent-instrumentation-examples](https://github.com/dynatrace-oss/dynatrace-ai-agent-instrumentation-examples) — concrete per-framework recipes this backbone is distilled from
- [OTel GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai) — the `gen_ai.*` attribute contract this skill instruments toward
- [OpenTelemetry registry](https://opentelemetry.io/ecosystem/registry/) — used in step 1's native-OTel-vs-fallback decision
- [references/examples-index.md](references/examples-index.md) — routing key → concrete recipe in the examples repo
- [references/enrich-normalization.md](references/enrich-normalization.md) — the OpenInference fallback gate: when normalization is needed before Validate can pass (and when the semconv flag skips it), plus the ready-made normalizer config (collector / OpenPipeline) the user applies
- [references/multi-sdk-apps.md](references/multi-sdk-apps.md) — running Detect/Instrument/Enrich when an app depends on more than one LLM SDK
- [references/no-native-instrumentation.md](references/no-native-instrumentation.md) — manual pure-OTel `gen_ai.*` spans as a stopgap when no packaged instrumentation exists for an SDK at all
- [references/enhance-existing.md](references/enhance-existing.md) — full reasoning for each enhance-existing case
- [references/validate-contract.md](references/validate-contract.md) — the contract (read on `main`), the `dtctl` validation loop, fail/warn severity, the any-of gate, provider profiles, and derived-metric lag
