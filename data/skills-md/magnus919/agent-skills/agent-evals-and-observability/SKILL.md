---
name: agent-evals-and-observability
description: >-
  Design, run, review, or release framework- and vendor-neutral evaluations and
  observability for AI agents. Use when defining agent evals, datasets, graders,
  trajectory review, regression analysis, release gates, production traces, or
  privacy-aware telemetry. Covers task and trajectory contracts, statistical comparisons,
  and incident-to-case learning; route framework implementation to pydanticai or langgraph
  when needed. Do not use this skill for unrelated requests; route to the nearest named
  specialist.
license: MIT
compatibility: No runtime dependency. Host-, framework-, model-, and telemetry-backend-neutral methodology.
metadata:
  source: "Curated from primary and official sources listed in references/source-index.md; checked 2026-07-13"
---

# Agent Evals and Observability

Evaluation asks whether behavior meets a defined criterion on a declared dataset or production sample. Observability supplies traces, logs, metrics, correlations, and diagnostic context. Use both; neither proves what the other does.

## Workflow

1. Define the decision, risk, task contract, trajectory contract, and unacceptable outcomes. Select evidence by harm, reversibility, and deployment stage, not a staged completeness scale.
2. Create an immutable dataset version and manifest before comparing versions. Declare provenance, rights/consent, slices, fixtures, expected side effects, contamination risk, limitations, retention, and changelog.
3. Select complementary graders that observe the claimed property. Use deterministic checks for observable mechanics; use execution/environment checks for state and side effects; use human, model-judge, pairwise/ranking, domain, and safety review where appropriate.
4. Run the candidate and baseline under comparable conditions. Preserve run configuration, stochastic repeats where variability affects the decision, failures/timeouts, and trajectory evidence.
5. Report a multidimensional profile and uncertainty. Use paired comparisons where possible; inspect slices, missingness, base rates, confounders, effect sizes, and multiple comparisons. Non-significance is not equivalence.
6. Apply a risk-tiered release gate: hard safety, privacy, authorization, and side-effect invariants cannot be averaged away. Record authority, insufficient-evidence outcomes, rollback, and follow-up. Load [release-engineering](../release-engineering/SKILL.md) when this evidence must be incorporated into artifact promotion, deployment, rollback, or a broader release train.
7. Instrument production with minimized, redacted telemetry. Feed verified incidents and near misses into cases after consent, transformation, and contamination review.

Stop when the supported decision, evidence gaps, residual risks, and responsible owner are recorded. Escalate rather than infer a pass when required evidence is unavailable or conflicts.

## Load By Need

| Need | Load |
|---|---|
| Choose evaluation evidence and contracts | [references/evaluation-design.md](references/evaluation-design.md) |
| Separate performance, diagnostic, and replay evidence; connect offline to online measures | [references/evidence-modes-and-metric-mirrors.md](references/evidence-modes-and-metric-mirrors.md) |
| Build immutable cases, fixtures, and provenance | [references/datasets.md](references/datasets.md) |
| Select or calibrate graders | [references/graders.md](references/graders.md) |
| Validate judge stability, abstention, and escalation | [references/judge-stability.md](references/judge-stability.md) |
| Evaluate grounded claims and attribute RAG failures | [references/grounding-attribution.md](references/grounding-attribution.md) |
| Define measures or compare runs | [references/metrics-and-statistics.md](references/metrics-and-statistics.md) |
| Review tools, state, recovery, or side effects | [references/trajectory-review.md](references/trajectory-review.md) |
| Triage a regression or decide release readiness | [references/regression-and-release.md](references/regression-and-release.md) |
| Design traces, logs, metrics, or privacy controls | [references/production-observability.md](references/production-observability.md) |
| Interoperate with OpenTelemetry | [references/opentelemetry-genai.md](references/opentelemetry-genai.md) |
| Need framework-specific implementation | [references/framework-routing.md](references/framework-routing.md) |
| Exercise the methodology with safe probes | [references/synthetic-scenarios.md](references/synthetic-scenarios.md) |
| Benchmark an agent's Supabase task competence with the official harness | [supabase agent evals reference](../supabase/references/agent-evals.md) |
| Verify a source claim or status | [references/source-index.md](references/source-index.md) |

## Templates

Use [templates/eval-plan.md](templates/eval-plan.md), [templates/dataset-manifest.md](templates/dataset-manifest.md), [templates/grader-specification.md](templates/grader-specification.md), [templates/trace-review.md](templates/trace-review.md), [templates/run-report.md](templates/run-report.md), [templates/release-gate.md](templates/release-gate.md), and [templates/metric-mirror.md](templates/metric-mirror.md). They are decision records, not checklists that manufacture evidence.

## Guardrails

- Do not use a scalar score, keyword hit, schema validation, or repeated output as proof beyond the property it directly observes.
- Do not capture prompts, outputs, tool arguments, intermediate reasoning, credentials, or personal data by default. Minimize before export, redact early, restrict access, set retention/deletion paths, and prepare incident response.
- Do not treat human judgment as definitive truth. Human and model graders require explicit rubrics, calibration, disagreement analysis, and revalidation when conditions change.
- Keep prevalence-oriented production samples separate from risk-enriched challenge cases. Do not silently reweight either into the other.

## When Not To Use

Use [systematic-debugging](../systematic-debugging/SKILL.md) to investigate one active defect before proposing fixes. Use [verification-methodology](../verification-methodology/SKILL.md) for general evidence-backed completion claims, [secure-software-engineering](../secure-software-engineering/SKILL.md) to design preventive controls, and framework skills for SDK-specific code. To benchmark an agent's competence on Supabase tasks with the official scored scenarios, use the [supabase agent evals reference](../supabase/references/agent-evals.md) — this skill covers methodology, not a named harness.
