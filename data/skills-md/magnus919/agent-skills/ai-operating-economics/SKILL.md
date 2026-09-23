---
name: ai-operating-economics
description: >-
  Use when deciding whether an AI-enabled workflow should be adopted, scaled,
  constrained, redesigned, or retired, and the decision must connect business
  outcomes, worker or user effects, quality guardrails, full operating cost,
  telemetry, uncertainty, and accountable governance. Do not use for a standalone
  financial model, infrastructure cost calculation, agent evaluation design,
  runtime operations, or general AI governance; route those details to the
  neighboring specialist skills.
license: MIT
compatibility: Agent-agnostic methodology; no runtime dependency.
metadata:
  tags: ai-economics, value-realization, ai-adoption, outcome-measurement, cost-attribution, worker-impact, evidence-led-decisions
  source: "Synthesized from primary and independent sources listed in references/source-index.md"
---

# AI Operating Economics

## Overview

AI initiatives are operating interventions, not merely model purchases or ROI spreadsheets. Their value depends on what work changes, who benefits, what quality or risk changes with it, what the complete intervention costs, and whether the organization can observe and govern those changes.

This skill provides the cross-domain decision spine for evaluating an AI-enabled workflow. It does not replace financial modeling, product measurement, statistical inference, agent evaluation, runtime operations, or AI governance. It makes those inputs meet in one accountable decision record.

The core question is not “Did the model make people faster?” It is: “What changed in this workflow, for whom, at what full cost, with what outcome and countermetric evidence, and what authority should the organization grant next?”

## Entry Points

| Starting state | Start with | Primary artifact or route |
|---|---|---|
| Idea or proposed AI workflow | Steps 1–2 | `templates/ai-initiative-evidence-record.md` |
| Existing pilot or outcome data | Steps 3–7 | `references/evidence-method.md` plus the evidence record |
| Request for broader population or side-effect authority | Steps 7–8; load `references/evidence-method.md` section 7a for the governance packet | Governance evidence packet plus the evidence record |
| Executive, portfolio, launch, or lifecycle review | Steps 8–9 | `templates/ai-economics-review.md`; route launch/runtime details onward |
| Standalone financial, statistical, telemetry, runtime, or governance implementation task | When Not to Use | Named adjacent specialist skill |

## When to Use

Load this skill when the user needs to:

- Build an evidence-backed business case for an AI use case or agentic workflow.
- Decide whether an AI pilot should scale, remain bounded, be redesigned, or stop.
- Review claimed AI productivity, savings, adoption, or transformation results.
- Design an AI value-realization or post-launch outcome review.
- Connect model and tool spend to workflow outcomes and worker or customer effects.
- Compare AI options while accounting for measurement uncertainty and non-comparable evidence.
- Prepare an executive, product, portfolio, or lifecycle decision about an AI-enabled intervention.

## When Not to Use

| If the task is primarily... | Route to | This skill still contributes... |
|---|---|---|
| Financial statements, pricing, CAC/LTV, runway, or SaaS metrics | [financial-modeling](../financial-modeling/SKILL.md) | The AI workflow's outcome and cost evidence can feed the model |
| Token, infrastructure, quota, capacity, or SLO-cost modeling | [capacity-and-cost-engineering](../capacity-and-cost-engineering/SKILL.md) | The economic decision can consume the resulting cost boundary |
| Metric trees, event schemas, instrumentation QA, or product dashboards | [product-analytics-and-measurement](../product-analytics-and-measurement/SKILL.md) | The decision defines which outcome and countermetric evidence matters |
| Experimental design, causal inference, statistical testing, or power analysis | [data-scientist](../data-scientist/SKILL.md) | The decision specifies the claim and comparison it must support |
| Agent datasets, graders, traces, regression analysis, or telemetry implementation | [agent-evals-and-observability](../agent-evals-and-observability/SKILL.md) | The decision consumes verified evaluation and telemetry evidence |
| Production rollout, runtime budgets, authority, fallback, escalation, or disablement | [agent-production-operations](../agent-production-operations/SKILL.md) | The decision sets the evidence and authority boundary |
| Organization-wide AI risk, policy, compliance, or governance operating models | [ai-governance](../ai-governance/SKILL.md) | The initiative record supplies an operating case and unresolved gaps |
| Launch-readiness packet or production go/no-go decision | [production-readiness](../production-readiness/SKILL.md) | The initiative disposition becomes one readiness input |
| General product governance cadence without an AI-specific value question | [product-operations-and-governance](../product-operations-and-governance/SKILL.md) | Use this skill only for the AI-specific value and operating-economics question |

## Non-Negotiable Reasoning Rules

1. **Workflow evidence beats model evidence.** A benchmark, demo, or vendor claim does not establish value in the target workflow.
2. **Speed is not value.** Time saved can be spent on lower-value work, offset by review and exception handling, or enable higher-value work. Measure the business or user outcome directly.
3. **Averages are not enough.** Inspect worker, user, task, geography, tenure, risk, and quality slices. An aggregate gain can hide a subgroup loss.
4. **Every benefit metric needs a countermetric.** Pair throughput or cost with quality, safety, customer, worker, privacy, or reliability measures appropriate to the workflow.
5. **Token cost is not total cost.** Include model calls, tools, retrieval, storage, networking, observability, engineering, human review, change management, governance, and unused committed capacity when material.
6. **Evidence classes must stay separate.** Label observed results, causal estimates, inferences, vendor-reported findings, stakeholder assertions, and normative requirements distinctly.
7. **Missing evidence is a decision input.** Do not turn an unknown into a favorable assumption. Record the gap, owner, consequence, and next evidence needed.
8. **Authority follows evidence.** A positive pilot does not justify unrestricted autonomy. Scale capability and authority in bounded slices with explicit reversal conditions.
9. **Do not manufacture precision.** Use ranges, scenarios, sensitivity, and confidence where inputs are uncertain. Do not rank non-comparable studies or vendors.
10. **The decision is reversible only if the artifact says how.** Record the stop trigger, rollback or containment path, decision owner, and review date.

## Core Workflow

Use this sequence for an AI initiative review. Load the detailed method and the evidence-record template when the task requires a durable artifact.

### Quick Start by Need

| Need | First action | Load next |
|---|---|---|
| Triage a claim | Name the workflow, decision, and evidence class | Steps 1–3; evidence classes are defined in Step 7 |
| Build a durable record | Copy the initiative evidence record and complete the header first | `templates/ai-initiative-evidence-record.md` |
| Investigate uncertain evidence | Freeze the claim table before drafting conclusions | `references/evidence-method.md` |
| Prepare a review | Assemble evidence, slices, cost, gaps, and disposition | `templates/ai-economics-review.md` |

### Choose Review Depth

| Mode | Use when | Minimum evidence | Output |
|---|---|---|---|
| Triage | A claim or opportunity needs a bounded first decision | Workflow, value hypothesis, one outcome, one countermetric, known gaps | Hold, with a routing/evidence plan |
| Standard | A pilot or workflow decision can change population or investment | Comparison, outcome/countermetrics, slices, cost boundary, owner, reversal path | Scale, constrain, redesign, or hold |
| High-assurance | Authority, sensitive data, material user impact, or irreversible change is involved | Standard evidence plus governance packet, human oversight, incident/revalidation, and decommissioning evidence | Scale only within an explicit authority boundary, or Hold |

### 1. Define the intervention and decision

Name the workflow, population, task boundary, intervention mode, baseline, decision sought, and decision owner. State whether the AI assists, recommends, routes, executes, or replaces/removes work. Define what remains human-controlled.

Do not begin with the model name or a claimed percentage. Begin with the work that changes and the decision the evidence must support.

### 2. State the value hypothesis

Write a falsifiable hypothesis:

> For [population] doing [workflow], [intervention] will change [outcome] by [direction/range] without exceeding [countermetric boundary], at [full operating cost boundary], compared with [baseline], over [period].

If the proposed outcome is only “productivity,” decompose it into the actual customer, employee, operational, financial, or mission outcome. If the outcome cannot be observed or credibly proxied, mark the initiative measurement-incomplete rather than inventing a proxy.

### 3. Build the outcome and countermetric map

Define:

- Primary outcome: the result the initiative exists to improve.
- Leading indicators: early evidence that the mechanism is operating.
- Countermetrics: quality, safety, customer, worker, privacy, reliability, or equity measures that could worsen.
- Adoption and substitution measures: who uses the system, what work changes, and what work is displaced or added.
- Guardrail thresholds: contextual limits with an owner and response.

Route metric definitions and instrumentation plans to product analytics. Route statistical or causal design to data science. This skill owns the connection between the evidence and the decision, not the detailed statistical method.

### 4. Establish the full economic boundary

Record both:

- **Marginal economics:** what changes when one more task, user, or workflow unit is served.
- **Fully loaded economics:** the costs required to make the intervention available and govern it.

At minimum consider inference, tool use, retrieval, storage, data transfer, observability, engineering, evaluation, human review, training, support, change management, governance, security, and committed capacity. Separate fixed, variable, step-function, and avoided costs. Define the denominator precisely: task, resolved case, completed workflow, active user, customer outcome, or another meaningful unit.

Route the detailed model to capacity-and-cost-engineering or financial-modeling. Never divide total spend by an undifferentiated request count when requests have materially different resource or outcome profiles.

### 5. Design the evidence comparison

Choose the strongest feasible comparison before interpreting results:

- Randomized or staggered rollout when feasible.
- Matched or difference-in-differences comparison when appropriate.
- Within-workflow baseline with explicit pre-period and seasonality limits.
- Controlled pilot with a documented task and population boundary.
- Descriptive before/after evidence only when stronger designs are infeasible, labeled accordingly.

Record selection effects, learning effects, concurrent initiatives, task-mix changes, worker self-selection, quality measurement gaps, and changes in pay or incentives. If the comparison cannot support the requested claim, narrow the claim rather than upgrading the method rhetorically.

### 6. Segment before aggregating

Report the overall result and inspect slices that could change the decision:

- Worker experience, skill, role, and training status.
- Task complexity, risk, volume, and exception rate.
- Customer or user segment.
- Geography, language, accessibility, and relevant demographic groups when lawful and appropriate.
- Human-review burden and escalation path.
- Quality, safety, and error severity.

Treat heterogeneous effects as a finding, not noise to average away. A tool that helps novices while harming expert quality may need differentiated assistance modes, not universal rollout.

### 7. Classify the evidence

For every material claim, label it:

| Class | Meaning | Permitted use |
|---|---|---|
| Observed | Directly measured in the target workflow with a stated method | Describe what happened within the stated scope |
| Causal estimate | Supported by a credible comparison or experiment | Attribute an effect only within the design's limits |
| Inferred | Reasoned from observed evidence and explicit assumptions | Guide a bounded hypothesis or scenario |
| Vendor-reported | Provider survey, case study, or product documentation | Establish reported adoption or available capability, not realized ROI |
| Asserted | Stakeholder or proposal claim not yet verified | Track as an assumption and evidence gap |
| Normative | Standard or framework recommendation | Define a control expectation, not an outcome claim |

Keep the source, access date, scope, version, caveat, and permitted interpretation with each claim. Load `references/source-index.md` for the research basis and evidence boundaries.

### Minimum Claim Ledger

For each material claim, record: **claim**, **evidence class**, **source and scope**, **what it supports**, **what it does not support**, **open challenge**, and **permitted language**. Keep unknown claims visible; do not let a source URL or vendor report stand in for direct workflow evidence.

### Minimum Decision Record

Every completed review must expose, in one durable artifact: the intervention and population, value hypothesis, primary outcome, countermetrics, comparison and limitations, cost boundary, relevant slices, evidence classes, missing evidence with owner, disposition, authority limit, reversal path, and review trigger.

### Disposition Quick Pick

| Evidence state | Default disposition | Next control |
|---|---|---|
| Outcome and countermetrics support a bounded expansion; cost and slices are understood | Scale | Name the next population and authority slice |
| Value is plausible but a cost, quality, subgroup, or authority boundary remains unresolved | Constrain | Limit population, task, quota, or human review |
| The mechanism creates avoidable failure or burden | Redesign | Change the workflow or control and rerun the comparison |
| Required evidence is missing or conflicting | Hold | Assign the evidence owner and review trigger |
| Value is absent or countermetrics exceed bounds | Retire | Protect affected people, migrate, and record learning |
| A material gap is accepted temporarily by a named human | Exception | Set expiry, containment, approver, and revisit condition |

### 8. Produce a bounded decision

Choose exactly one primary disposition:

- **Scale:** evidence supports expansion within a named scope and authority boundary.
- **Constrain:** value is plausible, but cost, quality, risk, or distributional effects require limits.
- **Redesign:** the mechanism or workflow needs modification before another test.
- **Hold:** evidence is insufficient for the requested decision; specify the missing evidence.
- **Retire:** observed value is absent or countermetrics exceed acceptable bounds, with a transition path.
- **Exception:** proceed despite a named gap only with an accountable human approver, expiry or revisit trigger, and containment plan.

### Closure Conditions

- **Scale:** next population, authority slice, owner, and review trigger are recorded.
- **Constrain:** the boundary, quota, human-review rule, and condition for expansion are recorded.
- **Redesign:** the changed mechanism, rerun comparison, and new acceptance boundary are recorded.
- **Hold:** the missing evidence, owner, method, and due trigger are recorded.
- **Retire:** transition, affected-person protection, decommissioning, and retained learning are recorded.
- **Exception:** named human approver, scope, expiry, containment, and revisit condition are recorded.

A decision is incomplete without an owner, review date or trigger, evidence gaps, and reversal path. Route launch or runtime consequences to the appropriate specialist skill.

### 9. Close the learning loop

At the review date, compare expected versus observed outcomes, cost, quality, worker or user effects, adoption, and incidents. Preserve the updated evidence record and state whether the prior hypothesis was supported, weakened, refuted, or still unresolved. Feed verified incidents and near misses into evaluation and governance work rather than treating them as anecdotal follow-up.

## Load-on-Demand References

| Need | Load when | File |
|---|---|---|
| Apply the full research and decision method, including comparison design and uncertainty | Evidence is incomplete, contested, or consequential | [references/evidence-method.md](references/evidence-method.md) |
| Review sources and permitted interpretations | A claim needs provenance or a source boundary | [references/source-index.md](references/source-index.md) |
| Fill a durable initiative record | Starting a new workflow review or pilot assessment | [templates/ai-initiative-evidence-record.md](templates/ai-initiative-evidence-record.md) |
| Prepare an executive or lifecycle review | Combining one or more initiative records for a decision | [templates/ai-economics-review.md](templates/ai-economics-review.md) |

## Common Pitfalls

- Treating an AI benchmark, speed increase, or demo as evidence of business value.
- Treating a vendor survey as an audited financial result or causal estimate.
- Reporting one average while omitting worker, task, quality, or customer slices.
- Calling token spend “AI cost” while omitting review, tooling, retrieval, infrastructure, or change costs.
- Choosing a denominator that makes the economics look favorable, such as all requests instead of completed or resolved workflows.
- Treating a missing baseline as zero or assuming adoption means benefit.
- Using a normative framework as proof that an intervention is safe or effective.
- Granting broader authority because a pilot had a positive mean result.
- Reusing a prior decision after the workflow, model, population, cost boundary, or evidence source changed.
- Writing a sophisticated recommendation without preserving the source-level evidence that supports it.

## Verification Checklist

Before delivering an AI operating economics decision, verify:

- [ ] The workflow, intervention, population, baseline, decision owner, and human-control boundary are explicit.
- [ ] The value hypothesis is falsifiable and tied to an observable outcome.
- [ ] At least one countermetric is defined for each benefit claim.
- [ ] Fixed, variable, step-function, and fully loaded costs are separated where material.
- [ ] The denominator represents meaningful work or value, not merely requests or tokens.
- [ ] The comparison design and its limitations are stated.
- [ ] Relevant worker, user, task, quality, and risk slices are inspected or explicitly unavailable.
- [ ] Claims are labeled by evidence class and traced to sources.
- [ ] Missing evidence is visible with an owner and next step.
- [ ] The disposition, authority boundary, reversal path, and review trigger are recorded.
- [ ] Detailed statistical, financial, instrumentation, governance, runtime, and launch checks were routed to their owning skills.

## Exit Criteria

Stop when the requested decision is supported by a durable evidence record, or when a bounded hold/escalation is the honest result. Do not continue refining prose to conceal missing evidence.
