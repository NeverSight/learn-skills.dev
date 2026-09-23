---
name: product-experimentation
description: >-
  Run end-to-end product experiments from assumption to decision: translate
  assumptions into testable hypotheses and experiment briefs, select the right
  method among qualitative interviews, prototypes, concierge tests, fake doors,
  feature flags, and A/B tests, and produce readouts that update the roadmap
  and decision record. Do not use when a qualitative or prototype test is the
  clearly right answer without statistical measurement; do not prescribe A/B
  testing by default; do not treat statistical significance as the only
  decision criterion or hide ethical and guardrail considerations.
license: MIT
compatibility: Agent-agnostic — works with any agent framework supporting the Agent Skills format. No external services, proprietary tools, or runtime dependencies required.
metadata:
  tags: product-experimentation, hypothesis-testing, ab-testing, feature-flags, experiment-design, product-decisions, guardrails, statistical-validity
---

# Product Experimentation

End-to-end product experimentation: from assumption mapping through method selection, instrumentation, guardrail enforcement, and decision-readout that updates the product roadmap. Owns the complete experiment workflow; routes statistical design and rollout mechanics to specialist skills.

## Pipeline

```
ASSUMPTIONS → [HYPOTHESIS] → [METHOD SELECT] → [INSTRUMENT] → [RUN] → [DECIDE] → [RECORD]
                  |                |                |           |          |           |
             Experiment       Qualitative       Tracking     Guardrail   Decision    Readout
               brief          Prototype          plan         monitor     rules      learning
                              Operational
                              Quantitative
```

## Loading Guide

Load only the reference or template relevant to the task. Do not load every file at once.

| File | Load when |
|------|-----------|
| [references/discovery-brief.md](references/discovery-brief.md) | You need to understand how experimentation concepts map across skills and where this skill's boundaries are |
| [references/method-selection.md](references/method-selection.md) | Choosing among qualitative, prototype, operational, and quantitative test methods |
| [references/guardrails-and-ethics.md](references/guardrails-and-ethics.md) | Defining guardrail metrics, ethical boundaries, stopping rules, and decision ownership |
| [references/experiment-readout.md](references/experiment-readout.md) | Producing a decision-impact readout that updates the roadmap or decision record |
| [templates/experiment-brief.md](templates/experiment-brief.md) | Filling out a structured experiment brief from an assumption |
| [templates/assumption-map.md](templates/assumption-map.md) | Mapping assumptions to risk, evidence, and testability before designing experiments |
| [templates/guardrail-and-decision-rule.md](templates/guardrail-and-decision-rule.md) | Recording guardrails, stopping rules, and decision criteria for an experiment |
| [templates/readout-learning-entry.md](templates/readout-learning-entry.md) | Documenting experiment outcome and updating the roadmap, decision log, or lifecycle evidence |

## Working Method

### 1. Map assumptions

Surface the assumptions driving the proposed change. Classify each by risk (what breaks if it is wrong), evidence strength (what evidence already exists), and testability (can it be tested, and how cheaply). Use [templates/assumption-map.md](templates/assumption-map.md).

### 2. Translate into hypotheses

Convert the riskiest, least-evidenced assumptions into falsifiable hypotheses. Each hypothesis names the independent variable (what changes), the dependent variable (what outcome is measured), the predicted direction, and the smallest effect that matters. Use [templates/experiment-brief.md](templates/experiment-brief.md).

### 3. Select the appropriate method

Choose the lightest-weight method that can falsify the hypothesis with sufficient confidence. The method ladder, from lightest to heaviest:

| Method | Best for | Cost | Statistical rigor |
|--------|----------|------|-------------------|
| **Qualitative interviews** | Uncovering unknown unknowns, mental models, problem validation | Lowest | None (descriptive) |
| **Prototype tests** | Interaction flow, usability, concept validation | Low | None (observational) |
| **Concierge tests** | Value delivery, willingness to pay, operational feasibility | Low-Medium | None (manual) |
| **Fake doors** | Demand signals, willingness to click/commit | Medium | Low (conversion rate only) |
| **Feature flags** | Operational safety, incremental rollout, kill-switch | Medium | Medium (controlled rollout) |
| **A/B tests** | Causal attribution of a specific change to a metric | High | High (randomized controlled) |

Do **not** default to A/B testing. Start at the top of the ladder and only move down when the question cannot be answered at the current level. A qualitative interview or prototype test is often the right answer. Full method selection guidance is in [references/method-selection.md](references/method-selection.md).

### 4. Define instrumentation, guardrails, and ethics

Before running the experiment, define:

- **Instrumentation**: what metrics are tracked, how they are computed, and that they are measurable with the available tooling. Route measurement contracts to product-analytics-and-measurement.
- **Guardrails**: mandatory safety metrics that can stop the experiment regardless of the primary outcome. At minimum: error rate, latency/degradation, and any domain-specific harm metric. Every experiment must name at least one guardrail metric. See [references/guardrails-and-ethics.md](references/guardrails-and-ethics.md).
- **Ethical boundaries**: user consent, data minimization, vulnerable-population considerations, and institutional-review alignment. Record all ethical decisions.
- **Stopping rules**: when the experiment stops early — guardrail breach, sufficient evidence reached, or time cap reached.
- **Decision ownership**: who makes the ship/no-ship call and what inputs they consider (statistical evidence, guardrail evidence, qualitative signal, practical constraints).

Use [templates/guardrail-and-decision-rule.md](templates/guardrail-and-decision-rule.md) to record these.

### 5. Determine exposure and duration

Define the target population, allocation, and minimum detectable effect. Route statistical design (power analysis, sample-size calculation, estimator selection) to [../data-scientist/SKILL.md](../data-scientist/SKILL.md). An underpowered experiment — one that cannot detect the smallest effect that matters — is a validity failure; do not ship based on a null result from an underpowered test.

### 6. Run and monitor

Execute the experiment. Monitor guardrails continuously. Route production rollout mechanics (feature flags, canary stages, progressive delivery) to [../release-engineering/SKILL.md](../release-engineering/SKILL.md).

### 7. Decide

Make the ship/no-ship decision using **multiple criteria**, never statistical significance alone:

| Criterion | Weight | Source |
|-----------|--------|--------|
| Statistical evidence | Required | data-scientist |
| Practical significance | Required | Is the effect large enough to matter? |
| Guardrail evidence | Blocking | All guardrails must pass |
| Qualitative evidence | Informative | User feedback, support tickets |
| Reversibility | Informative | Can we undo this if wrong? |
| Opportunity cost | Informative | What else could we build instead? |

A statistically significant result with a failing guardrail is a **no-ship**. A statistically significant result that exceeds authority boundaries (e.g., safety, compliance, ethics) is a **no-ship**. Record the decision and its rationale.

### 8. Record the readout

Document what was learned and what changed as a result. The readout updates the product roadmap, backlog, decision log, or lifecycle evidence. Routing: feeds product-roadmapping-and-portfolio (roadmap updates), product-adoption (adoption evidence), and product-lifecycle-learning (retained learning). Use [templates/readout-learning-entry.md](templates/readout-learning-entry.md) and [references/experiment-readout.md](references/experiment-readout.md).

## Trigger Conditions

Load this skill when:

- The task involves designing, running, or deciding on a product experiment
- You need to choose between qualitative, prototype, operational, and quantitative test methods
- You have assumptions that need to be tested before committing to build
- You need to define guardrails, stopping rules, or decision criteria for an experiment
- You need to interpret experiment results and make a ship/no-ship decision
- You need to record experiment outcomes that update product direction

## When Not to Use

- **Statistical design** (power analysis, estimator selection, significance testing in depth) — route to [data-scientist](../data-scientist/SKILL.md). This skill frames the question and selects the method; data-scientist owns the statistical machinery.
- **Production rollout mechanics** (feature-flag infrastructure, canary stages, CD pipeline integration) — route to [release-engineering](../release-engineering/SKILL.md). This skill defines the experiment design; release-engineering owns the safe delivery.
- **User research and usability testing** — route to [product-design-and-ux](../product-design-and-ux/SKILL.md) for interaction-focused studies.
- **Pricing-specific tests** — route to [financial-modeling](../financial-modeling/SKILL.md) for elasticity, willingness-to-pay, and pricing-page experiments.
- **Opportunity-solution tree construction** — route to [product-methodology](../product-methodology/SKILL.md) for connecting customer needs to build decisions before experimentation.
- **Pure analytics instrumentation** (tracking-plan design, event taxonomy, metric definitions) — route to product-analytics-and-measurement for measurement contracts.

## Portability

This skill is intentionally host-neutral. It requires no profile system, output format, scripts, or external services. Load references and templates directly by path using the host agent's normal file-loading mechanism.
