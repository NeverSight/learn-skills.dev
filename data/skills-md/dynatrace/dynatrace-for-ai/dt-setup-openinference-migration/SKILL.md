---
name: dt-setup-openinference-migration
description: >-
  Migrate a GenAI/LLM app off Traceloop/OpenLLMetry onto OpenInference with its OTel gen_ai.*
  semconv option enabled (`enable_genai_semconv` / `OPENINFERENCE_ENABLE_GENAI_SEMCONV`). Covers
  detecting the existing Traceloop setup, swapping the instrumentor per SDK, and the
  ingestion-shape question that decides what's fixable afterward — an app-owned OTel trace
  exporter vs. instrumentation-only with OneAgent picking up the spans. Flags that the semconv
  option is additive, not a replacement — legacy llm.*/openinference.* attributes keep emitting
  alongside gen_ai.* — and covers the resulting cardinality trade-off and removal options
  (Collector transform vs. OpenPipeline), checking which is actually available first. Trigger:
  "migrate off Traceloop", "migrate off OpenLLMetry", "move to OpenInference", "enable
  OpenInference GenAI semconv". Do NOT use for a first instrumentation with no existing
  Traceloop setup, or an OpenInference app that never enables semconv (both dt-setup-genai).
license: Apache-2.0
---

# Migrate off Traceloop/OpenLLMetry onto OpenInference

The migration-specific decision process for an app that's **already emitting spans via
Traceloop/OpenLLMetry** and must move onto OpenInference with its `gen_ai.*` semantic-convention
option on. It shares Detect/Validate machinery with **dt-setup-genai** — load that skill for the
four-step instrument/enrich model, the `dtctl` validation contract, and multi-SDK handling. This
skill covers only what differs: identifying the Traceloop setup, the instrumentor swap, and the
gaps that remain once `gen_ai.*` flows — legacy attributes OpenInference keeps emitting,
invocation parameters left unparsed, and guardrail signals the instrumentation never captured.

## When you should not use this skill

- No existing Traceloop/OpenLLMetry instrumentation to migrate away from → **dt-setup-genai**
  (greenfield or enhance-existing instrumentation from scratch).
- Already on OpenInference, semconv option never enabled, spans still arrive as
  `llm.*`/`openinference.*` → load the **dt-setup-genai** skill and use its normalizer gate
  (`references/enrich-normalization.md`) instead — not a migration.
- TypeScript/Node app, or any language other than Python → out of scope. The semconv option
  this skill's flow depends on exists only in the Python OpenInference SDK today — a TypeScript
  app moving off Traceloop still needs dt-setup-genai's normalizer gate afterward, not this skill.

## Where this skill must stop and ask

- **Any edit to the customer's application code** — show the diff, get a yes, first.
- **Whether to remove the legacy `llm.*`/`openinference.*` attributes** (step 4a) — a
  trade-off, not a default to silently apply.
- **Deploying an OTel Collector transform or an OpenPipeline pipeline** to the tenant — same
  boundary dt-setup-genai draws — or the `gen_ai_normalizer` (collector processor or OpenPipeline
  pipeline), only after Validate shows gaps it would close. OpenPipeline needs extra care: its
  routing configuration is a single object shared by every pipeline on the tenant — read
  [references/openpipeline-safety.md](references/openpipeline-safety.md) first.
- **Adding app code to capture a guardrail signal** the instrumentation doesn't emit (step 4c).
- **Credentials** — never print, log, or store a token value.
- **Message-content capture** — OpenInference captures prompt/response content by default,
  independent of the semconv flag (as Traceloop does via `TRACELOOP_TRACE_CONTENT`); confirm the
  user still wants it once instrumentation changes hands.

## The migration flow

```
baseline ─▶ detect Traceloop ─▶ ingestion shape ─▶ swap instrumentor ─▶ close semconv gaps ─▶ validate
```

### 0. Capture baseline and rollback state

Before editing anything, record what the service emits today and how to undo the change — the
swap renames attributes and drops metrics that dashboards or alerts may read. Baseline query,
consumer inventory, rollback checklist: [references/baseline-and-rollback.md](references/baseline-and-rollback.md).

### 1. Detect the existing Traceloop/OpenLLMetry setup

Confirm this is actually a migration — grep patterns and the package-name trap (some
Traceloop packages are named `opentelemetry-instrumentation-<sdk>`, like genuine OTel ones) are
in [references/detect-traceloop.md](references/detect-traceloop.md). Record which SDK(s) it
wraps — each needs its own `openinference-instrumentation-<sdk>` replacement in step 3.

### 2. Confirm the ingestion shape

This decides what's actually fixable in step 4, so settle it before touching code. Three
situations, not interchangeable for the cardinality question:

- **App-owned trace exporter** — the app builds its own `TracerProvider`, attaches a
  `BatchSpanProcessor` + OTLP exporter, and calls `set_tracer_provider(...)` before the
  instrumentor runs. The app controls the exporter, so a collector can sit in front of it.
- **Instrumentation-only, OneAgent picks it up** — the code calls only the instrumentor's
  `.instrument(...)`, with no `TracerProvider`/exporter setup; on a OneAgent-monitored host,
  OneAgent captures the spans by injecting into the process. Nothing the app controls sits on
  the wire, so a collector transform isn't an option later — only OpenPipeline can touch these
  spans post-ingestion.
- **Traceloop-managed exporter** — the app calls `Traceloop.init()` and none of the symbols
  above appear, but Traceloop itself creates the `TracerProvider` and a default OTLP exporter
  (destination via `TRACELOOP_BASE_URL`/`TRACELOOP_HEADERS`/`TRACELOOP_API_KEY`). Replacing it
  with only an OpenInference instrumentor silently drops the export path — first add an explicit
  provider + exporter with the same destination, then remove the init. `init_instrumentations(...)`
  is different: instrumentation only, like the second shape.

Full detection heuristic and a worked example of each shape:
[references/ingestion-shape.md](references/ingestion-shape.md).

### 3. Swap the instrumentor

- **Never run Traceloop/OpenLLMetry and OpenInference instrumentation for the same SDK in the
  same process** — every call gets wrapped twice (duplicate or nested spans). Remove (or exclude)
  the Traceloop instrumentation for that SDK in the same change that adds the OpenInference one.
- Replace the Traceloop package with the matching `openinference-instrumentation-<sdk>`
  package. Read the `<sdk>/openinference/` recipe folder in
  [the examples repo](https://github.com/dynatrace-oss/dynatrace-ai-agent-instrumentation-examples)
  for the current call shape — don't hand-author it (see `examples-index.md` in the
  **dt-setup-genai** skill — load it to read that file).
- **Take the instrumentor call shape from the recipe, not its collector/OpenPipeline config.**
  Those configs include the `gen_ai_normalizer` (`llm.*`/`openinference.* → gen_ai.*` mapping),
  which exists for spans *without* the semconv option. With the option on, `gen_ai.*` is already
  emitted natively — don't add the normalizer, or copy a config containing it, up front.
- Enable the semconv option — `TraceConfig(enable_genai_semconv=True)` passed to
  `.instrument(config=...)`, or the `OPENINFERENCE_ENABLE_GENAI_SEMCONV=true` env var where
  the instrumentor reads it instead. Both are Python-only (see "When you should not use this
  skill" above). Without this, the instrumentor only emits
  `llm.*`/`openinference.*` and you're back on dt-setup-genai's normalizer gate.
- Multi-SDK app → repeat per SDK; load **dt-setup-genai** and follow its `references/multi-sdk-apps.md`.
- Before deleting the Traceloop init, check nothing else (custom span processors, log
  correlation) still reads Traceloop-specific attributes (`traceloop.*`).

### 4. Close the gaps the semconv option leaves

The semconv option gets the core `gen_ai.*` contract fields flowing, but four known gaps remain,
each needing different handling. Run Validate (step 5) right after step 3 and let the result
drive this step. The **normalizer (`gen_ai_normalizer`) is a gap-driven fallback, not a
default**: add it only if the L3 check shows specific contract fields still missing that the
semconv option doesn't fill. Name those fields to the user and get approval first (it's a
collector/tenant change). If the only gaps are invocation parameters or guardrails, use 4b/4c.

**4a. Dual-write cardinality.** **The semconv option is additive, not a replacement.** With it
on, OpenInference emits `gen_ai.*` *alongside*, not instead of, `llm.*`/`openinference.*` on the
same span (dt-setup-genai's validation contract says so too). Verify on the migrated app: send
one request, list the span's attributes with `dtctl`/DQL, confirm both families are present.

Every span now carries roughly double the attribute count (payload/storage overhead); *metric*
cardinality only rises if something selects the legacy fields as dimensions — don't present
removal as a cardinality fix unless that's measured. **Ask the user whether to drop the legacy
set once `gen_ai.*` is confirmed present — don't decide this yourself.** If they want it
dropped, the mechanism depends on the ingestion shape from step 2:

| Ingestion shape | Removal mechanism |
|---|---|
| App-owned exporter, collector already in the path | OTel Collector `transform` processor |
| App-owned exporter, no collector today | A genuine trade-off, not a default: adding a collector is an infrastructure change (dt-setup-genai's stop-and-ask list draws the same line), so present both "stand up a collector" and "use OpenPipeline instead" and let the user pick |
| OneAgent picks up the spans | OpenPipeline only — nothing sits between OneAgent and Dynatrace to run a collector transform |

Check availability before proposing either; snippets and availability checks:
[references/dual-write-cardinality.md](references/dual-write-cardinality.md).

**4b. Invocation parameters — fixable in a collector or OpenPipeline config.** OpenInference
packs model parameters (`temperature`, `top_p`, ...) into one JSON string at
`llm.invocation_parameters`; check explicitly (query in the reference) whether the individual
`gen_ai.request.*` fields are populated — the semconv option has been seen to leave the blob
packed. If so, it's a pipeline fix in whichever mechanism step 2's shape allows; snippets:
[references/incomplete-attribute-mappings.md](references/incomplete-attribute-mappings.md).

**4c. Guardrail attributes — likely needs custom instrumentation code, not a pipeline fix.**
OpenInference has no standardized guardrail attribute — `openinference.span.kind = "GUARDRAIL"`
only marks the span kind, and whether a guardrail fired is signaled differently, or not captured
at all, per provider/library (per-provider table in
[references/incomplete-attribute-mappings.md](references/incomplete-attribute-mappings.md)).
Where the signal was never captured, no collector or OpenPipeline transform can recover it —
the app must capture it. **That is an app-code edit: stop and get explicit approval first**;
leaving it as a documented gap is fine if guardrail visibility isn't needed.

**4d. Derived metrics — gone after the swap.** OpenInference is span-only. The
`gen_ai.client.token.usage` and `gen_ai.client.operation.duration` metrics Traceloop emitted
disappear, and the AI Observability app's metric-based cost and latency charts lose the service.
Compare against the step 0 baseline; if gone, derive them from spans — collector connectors or
OpenPipeline metric extraction, per the ingestion shape. Ask first, and check the connectors
exist in the collector distro (Bindplane is the fallback): [references/derived-metrics.md](references/derived-metrics.md).

**Gap report — required, no silent skips.** Before finishing, show the user all four gaps in a
short table: what you observed, the proposed fix or an explicit "leave as is", what needs
approval. "Not checked" is not an outcome. With several services or collector configs in the
repo, check every one, ask once, and apply the same decision everywhere — never strip or unpack
in one service's pipeline and leave another's untouched.

### 5. Validate

Same contract, same loop — load the **dt-setup-genai** skill and delegate entirely to its
Validate step (`SKILL.md`, step 4) and its `references/validate-contract.md` for the full `dtctl`
L1–L4 loop, comparing against the step 0 baseline. Gaps found here are the only trigger for
adding the `gen_ai_normalizer`. Migration-specific L3 additions: if 4a stripped the legacy
attributes, assert they're gone (`isNull(llm.system)`, ...); if kept by choice, coexistence is
expected. If 4b exploded invocation parameters, confirm the fields the provider profile requires
now populate. L4 covers 4d. 4c has no gate — the attribute exists because the user approved
adding it, or it's an accepted, documented gap.

## References

- [references/baseline-and-rollback.md](references/baseline-and-rollback.md) — baseline, consumers, rollback
- [references/detect-traceloop.md](references/detect-traceloop.md) — grep patterns, package-name trap
- [references/ingestion-shape.md](references/ingestion-shape.md) — the three ingestion situations
- [references/dual-write-cardinality.md](references/dual-write-cardinality.md) — legacy attribute removal
- [references/incomplete-attribute-mappings.md](references/incomplete-attribute-mappings.md) — invocation parameters, guardrails
- [references/derived-metrics.md](references/derived-metrics.md) — re-creating token-usage/duration metrics
- [references/openpipeline-safety.md](references/openpipeline-safety.md) — shared routing object, matcher scoping
- **dt-setup-genai** — load by name for shared Detect/Enrich/Validate machinery and the `dtctl` contract
- [Examples repo](https://github.com/dynatrace-oss/dynatrace-ai-agent-instrumentation-examples) — per-SDK `openinference/` recipes (call shape only)
- [OTel GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai) — the `gen_ai.*` contract
