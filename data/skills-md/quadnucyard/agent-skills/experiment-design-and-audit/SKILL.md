---
license: MIT
name: experiment-design-and-audit
description: >
  Design and plan experiments, audit existing experimental settings and results,
  and investigate anomalous outcomes for ambiguity, unfair comparisons,
  execution defects, and unsupported conclusions. Use for general experimental
  research, especially software engineering benchmarks, systems, tools, and
  developer workflow studies; includes optional ML-specific guidance.
---

# Experiment Design and Audit

Establish what an experiment can support given its design, actual execution,
and evidence. Make consequential ambiguity explicit, assess fairness against
the intended claim, and investigate execution defects before attributing an
unexpected result to the studied phenomenon.

Use general experimental principles. Software engineering is the center for
examples and domain depth; other experiments do not inherit software or ML
prerequisites.

## Select the work and relevant guidance

Infer the requested modes from the supplied material; combine them when needed.
Inspect existing artifacts before asking for information they may already contain.

Read [report-contract.md](references/report-contract.md) for shared evidence,
decision, and reporting semantics. Then read only the relevant procedures:

| Request | Guidance |
| --- | --- |
| Design a new experiment or plan a follow-up | [design-and-planning.md](references/design-and-planning.md) |
| Audit an existing protocol, settings, or actual execution | [settings-and-execution-audit.md](references/settings-and-execution-audit.md) |
| Audit results, interpretations, or abnormal observations | [result-and-anomaly-audit.md](references/result-and-anomaly-audit.md), plus the settings/execution guidance to establish the necessary upstream context |
| Software, systems, simulation, or developer/workflow experiments | Also read [software-engineering.md](references/software-engineering.md) |
| ML-dependent treatment or evaluation | Also read [ml-supplement.md](references/ml-supplement.md) |

A results audit includes the upstream context needed to interpret the results;
it is not limited to inspecting a summary table. An anomaly investigation may
need all three procedures. Reuse already established evidence rather than
repeating the same audit. Explicitly state unavailable artifacts and unchecked
scope; do not pretend the necessary upstream checks were completed.

## Establish the question and evidence

- Identify the decision, research question, target claim, population or system,
  treatment, comparator, outcomes, constraints, and intended generalization.
  Separate exploration, confirmation, estimation, optimization, and replication.
- Distinguish assignment units, measured observations, and independent units
  supporting inference. Repeated measurements are not automatically independent
  replications. Identify grouping, pairing, order, time, and interference.
- Resolve outcome-critical terms such as "faster," "fair," "stable," "abnormal,"
  and "significant" into operational definitions, units, conditions, comparison
  rules, and interpretation criteria. A precisely measured proxy still needs
  justification as a measure of the intended construct.
- Separate evidence, assumptions, unresolved decisions, and proposed work. Ask
  targeted questions when missing answers can change validity or interpretation.
  When asking the user to decide, use simple, direct language to explain what
  each choice changes about what is measured or what the results can show.
  Avoid jargon and overly formal wording. Use a short example if it helps.
  Propose justified choices where useful, but do not invent thresholds, sample
  sizes, historical decisions, or observations. Mark dependent work not ready
  while critical questions remain; continue useful independent work.

## Preserve the essential distinctions

1. **Design, execution, and inference:** correct execution cannot rescue a design
   that cannot identify the claimed effect; a good design does not prove it was
   executed correctly; repeatable analysis does not establish its correctness.
2. **Intended, effective, and observed:** documents, resolved settings/procedures,
   and execution evidence are separate. A saved configuration or successful exit
   does not prove that the intended intervention and measurement occurred.
3. **Fairness and sameness:** equal resources, recommended operating conditions,
   and isolated component effects can require different comparisons. Explain
   material asymmetries against the claim rather than requiring identical values.
4. **Failure and invalid execution:** a method's crash, timeout, or poor outcome
   under valid conditions may be a result. Do not discard it as a bad run merely
   because it is inconvenient. Preserve failed and excluded attempts and reruns.
5. **Observed and explained:** an abnormal observation can be real, random,
   confounded, mismeasured, or unresolved. Check evidence before assigning a cause.
   Reproducing an anomaly with the same flawed procedure does not validate it.
6. **Exploratory and prospective:** preserve what was known when decisions were
   made. Outcome-informed changes remain visible; rewriting a protocol cannot
   make an already observed finding prospectively confirmed.

Never claim all execution defects or confounders have been ruled out. State what
was checked, the evidence it produced, and the residual uncertainty. Missing
evidence limits endorsement; it does not prevent reporting useful scoped findings.

## Deliver an actionable result

Scale detail to the actual study. Use the shared report contract to produce a
plan, audit, or diagnostic report with evidence-linked decisions and prioritized
next actions. Avoid empty template sections and irrelevant domain checklists.
Do not substitute formatting or linter observations for substantive assessment.

Preserve original protocols, raw observations, and attempt histories. Distinguish
reanalysis, remeasurement, rerunning, and new independent data collection. An
audit can include proportionate local calculations on supplied artifacts; it does
not by itself authorize a new study, unbounded retries, paid jobs, production
load, destructive procedures, or replacement of raw evidence. Respect existing
authorization and give proposed diagnostics explicit bounds and stop conditions.

Consider the complete path from question through execution to interpretation.
For follow-ups, record the unresolved question, required evidence, and concrete
trigger. Do not defer a safeguard required to interpret the current study.
Add future domain depth as conditional references using the same evidence and
decision semantics; do not impose every specialized procedure on every experiment.
