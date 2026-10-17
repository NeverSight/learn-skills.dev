---
name: pd-metrics
description: >-
  Use when defining how to measure a design's success, or evaluating its impact after ship: success
  metrics, HEART / Goal-Signal-Metric, task-based metrics, analytics event and instrumentation specs,
  guardrail metrics, and honest result-reading from the project's analytics source. Closes the loop
  research opens. Part of the pd-* design team.
metadata:
  team: product-design
  role: metrics
  version: "2.0.0"
---

# pd-metrics — define success, then measure it

## Overview

Decide what success looks like before building, and measure it after ship. Tie design to outcomes, not
opinions. Honesty is central here: fabricated metrics, benchmarks, or results are the most damaging
failure this skill can produce, so targets stay hypotheses until data confirms them.

## Before you start

- Load `pd-foundations`: `working-agreement.md` (honesty), `principles.md`, `integrations.md`
  (tracker goals, analytics source), `project-profile.md`.
- Read `docs/design/PROJECT.md` for the `analytics` source (Amplitude, Mixpanel, PostHog, GA4, or none)
  and the requirements tracker. If missing, proceed with defaults recorded as assumptions, or ask
  `pd-design-lead`.
- Read upstream `*-design-*.md` (required) and `*-research-*.md` (goals). Research may be replaced by
  goals from the requirement, stated as assumptions.

## When to use

- Defining success metrics for a feature before or while designing.
- Specifying analytics instrumentation.
- Reading post-ship results to judge whether the design worked.

## Frameworks (use the one that fits; cite accurately)

- **Goal, Signal, Metric (GSM):** for each goal, name an observable signal of success, then a concrete
  metric. A Google UX-research approach; verify specifics before quoting.
- **HEART:** Happiness, Engagement, Adoption, Retention, Task success. Use it to pick which categories
  matter for this feature, then run GSM within each chosen category. HEART names the dimensions; GSM
  fills them in, so they are not alternatives.
- **Task-based metrics:** completion rate, time-on-task, error rate, success rate. Best for flows.
- **AARRR:** Acquisition, Activation, Retention, Referral, Revenue (Dave McClure). Funnel-level.
- **North Star Metric:** the single metric best capturing core value delivered. When a feature rolls up
  to an existing one, state which and how this design moves it.

If you cite a statistic or study about these, follow the honesty charter; do not invent numbers or sources.

## Process

1. Pull the goal from the tracker item (`ref:`) and the research artifact: what outcome should this
   design produce?
2. Derive goal, signal, metric for each goal.
3. Specify analytics events with a consistent `object_action` convention (`signup_completed`, not
   `SignupDone` here and `signup_finish` there). Split event properties (context of this occurrence)
   from user properties (persistent traits), and give the trigger for each.
4. Set targets and guardrails. First estimate whether current traffic can detect the hypothesized
   effect in a reasonable window (rough sample-size/MDE check); a target you cannot measure is not a
   target. Label targets as hypotheses. Guardrails ("improve X without harming Y") come from concrete
   categories: performance/latency, error rate, support-ticket volume, unsubscribe/opt-out rate.
5. Post-ship, read honestly: report sample size and confidence; segment by cohort (new vs returning,
   platform, plan tier), since an aggregate lift can hide a subgroup regression; separate correlation
   from causation and recommend an A/B test where causal claims matter.

## Analytics source

Use the source named in PROJECT.md (see `integrations.md`) to define events, build charts, and query
results. Verify that event names exist before using them, read real data, and present only numbers you
actually read; cite the chart or query. Caveat sample size and confidence. If no analytics source is
connected, write the instrumentation spec anyway and state that results cannot be read yet and what
measurement would produce them.

## Output

`<artifacts_dir>/<date>-metrics-<topic>.md` with the artifact header (`ref:` the requirement), then: goals,
GSM table, event/instrumentation spec, targets (labelled hypotheses), guardrails, and post-ship results
with confidence and caveats. `upstream:` the artifacts actually consumed — research and design, if used. If you lack data, say so; approximate only
with an explicit caveat and a pointer to the primary source.

## Domain packs

If `PROJECT.md` lists domain packs, read each pack's section for metrics and apply it on top of this
skill.

## Common mistakes

- Vanity metrics that do not reflect the goal.
- Fabricated benchmarks or "industry-average" numbers.
- Claiming causation from correlation; presenting targets as facts.
- Metrics with no instrumentation to capture them.
- Metrics that sound instrumentable but are not reliably measurable on the platform (email open rates,
  cross-device attribution without stitched identity); flag these before committing to a target.
