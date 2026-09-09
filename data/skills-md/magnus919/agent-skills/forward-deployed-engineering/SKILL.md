---
name: forward-deployed-engineering
description: >-
  Guide embedded technical engagements from ambiguous stakeholder need through
  discovery, framing, hypothesis, build, evaluation, deployment, adoption,
  measurement, and generalization while preserving evidence, decision rights,
  and field learning. Use when one accountable technical lead must carry
  continuity across customer or stakeholder discovery, implementation,
  production fit, adoption, and measurable outcomes. Do not use for a bounded
  repository change, product investment governance, ongoing reliability or
  platform ownership, an isolated specialist task, or advisory work that ends
  before implementation and adoption.
license: MIT
compatibility: Agent harness with file read/write, terminal, and skill loading. No network or runtime dependency required by the bundle itself.
metadata:
  spec-version: "1.0"
  tags: forward-deployed-engineering, embedded-delivery, adoption, measurement, generalization
---

# Forward-Deployed Engineering

Use this bundle when the work is an embedded technical engagement whose success
depends on continuity, not merely a recommendation or a code change. This is a
normative operating model synthesized from the role observations in
[source-index.md](references/source-index.md) and from routed specialist
methods; the nine-stage sequence is not an externally standardized methodology.

## Lifecycle

`Discover → Frame → Hypothesize → Build → Evaluate → Deploy → Adopt → Measure → Generalize`

| Stage | Required question | Minimum output | Stop condition |
|---|---|---|---|
| Discover | What user workflow and problem are real? | [Stakeholder/workflow map](templates/stakeholder-workflow-map.md) and unknowns | No recognizable problem or access to the relevant workflow |
| Frame | What is in scope, who decides, and what outcome matters? | [Engagement charter](templates/engagement-charter.md) and [assumptions/decisions/risks ledger](templates/assumptions-decisions-risks-ledger.md) | Authority, constraints, or outcome cannot be named |
| Hypothesize | What smallest intervention could change the workflow? | Testable hypothesis and decision rule | No falsifiable hypothesis or unsafe test |
| Build | What operationally complete slice can be built? | Thin-slice implementation plan and owner | Dependencies or permissions are infeasible |
| Evaluate | What evidence supports quality, safety, and usefulness? | [Evaluation and release decision](templates/evaluation-and-release-decision.md) | Baseline, representative evidence, or risk constraints missing |
| Deploy | Can it be released, recovered, and verified in the authorized environment? | Readiness, rollout, rollback, and verification record | No authorized access, rollback, or release decision |
| Adopt | Do intended users activate and use it in the target workflow? | [Adoption scorecard](templates/adoption-scorecard.md) and intervention record | Adoption failure is unexplained or ownership/support is absent |
| Measure | Did the capability change the agreed outcome? | [Outcome measurement record](templates/outcome-measurement-record.md) | Instrumentation cannot distinguish expected from observed |
| Generalize | What should happen to the local learning? | [Productization record](templates/productization-record.md) and [field-learning record](templates/field-learning-record.md) | No evidence or receiving owner for the proposed next step |

At every stage, read the current charter, workflow map, and ledger and add
evidence rather than re-deriving prior decisions. Maintain one [engagement
charter](templates/engagement-charter.md), one [stakeholder/workflow
map](templates/stakeholder-workflow-map.md), and one
[assumptions-decisions-risks ledger](templates/assumptions-decisions-risks-ledger.md).
Each stage records entry evidence, the artifact produced, the accountable
decision maker, unresolved unknowns, and the next handoff. Never silently turn
an observation into a requirement, a prototype into a production claim, or a
local success into a reusable product capability. For the expected depth and
evidence labeling of these artifacts, see the
[worked example engagement](references/worked-example-engagement.md).

### Where to enter the lifecycle

Enter at the stage that matches what already exists. Do not restart earlier
stages unless the current charter's stop conditions require it.

| What you already have | Enter at |
|---|---|
| A stakeholder request or observed workflow opportunity, no validated problem | Discover |
| Validated problem and stakeholders, no charter | Frame (establish the charter first) |
| Charter, workflow map, and ledger; no approved requirement | Hypothesize |
| Approved requirement; thin slice in progress | Build |
| Built and tested slice; no release decision | Evaluate |
| Released within the authorized boundary | Adopt |
| Adopted and measuring against the decision rule | Measure |
| Post-launch evidence and a generalization question | Generalize |
| A well-specified bounded change with no continuity need | Route to [neckbeard](../neckbeard/SKILL.md) instead |

Before acting at any entry point, review the current charter, workflow map,
ledger, and preceding stage-handoff record as entry evidence.

## Loading protocol

1. Establish the charter before solution design: problem, users, workflow,
   outcome, scope, authority, constraints, success measure, and stop conditions.
2. Load [lifecycle and artifacts](references/lifecycle-and-artifacts.md) and
   update the shared ledger after every stage.
3. Treat the stage skills in `manifest.yaml` as candidates. Apply the
   [route-selection conditions](references/route-selection.md), load one primary
   specialist, and follow its method rather than copying it into this bundle.
4. Before action in a constrained or sensitive environment, load
   [authority and escalation](references/authority-and-escalation.md) and route
   access, security, privacy, irreversible, cost, and external-commitment
   decisions to their authorized owner.
5. Before calling applied AI or any risky capability production-ready, load
   [agent-evals-and-observability](../agent-evals-and-observability/SKILL.md)
   and [production-readiness](../production-readiness/SKILL.md), and require
   baseline, representative and adversarial evidence, constraints, and a
   release decision.
6. Treat adoption and measured workflow impact as completion conditions, not
   postscript communications. Use [adoption and measurement](references/adoption-and-measurement.md).
7. Apply the classification rules in [generalization and
   productization](references/generalization-and-productization.md), then close
   with the [productization record](templates/productization-record.md). Classify
   local work as configuration, reusable pattern, product capability,
   transfer/replacement, or retirement, with evidence and an owner.
8. Treat artifacts as private by default and apply the [external-sharing
   gate](references/communication.md#external-sharing-gate) before they leave
   the authorized engagement context.

Load only the primary specialist for the active stage. Add a secondary
specialist only for a named blocker, risk, or handoff; do not preload every
skill in the manifest. If one specialist fully owns the request, stop routing
and hand the task to that specialist instead of running the FDE lifecycle.

## Epistemic and communication contract

Label each material statement as one of: **source fact**, **engagement
observation**, **inference**, **recommendation**, **decision**, or
**commitment**. Use the [communication reference](references/communication.md)
for concise status and escalation updates. The [discovery brief](references/discovery-brief.md)
records the overlap audit and source limitations.

## Completion and stop rules

The engagement is complete only when the capability is technically verified,
deployed within the authorized boundary, adopted by the intended workflow,
measured against an agreed outcome, and its learning has a generalization
decision. A prototype, demo, or stakeholder approval alone is not completion.

Stop and preserve the ledger when the problem cannot be articulated, authority
or access is missing, evidence fails, adoption remains unexplained or below the
decision rule, or the next action exceeds the charter. Escalate rather than
guess on security, privacy, irreversible changes, material cost, external
commitments, or business authority. Route a well-specified repository bug
directly to [neckbeard](../neckbeard/SKILL.md) and the relevant
specialist instead of invoking this lifecycle.

## When not to use

| Scenario | Reach for | Why |
|---|---|---|
| Well-bounded repository change | [neckbeard](../neckbeard/SKILL.md) | Owns intake through verified PR and authorized release for a bounded change |
| Product investment, portfolio, or lifecycle governance | [product-lifecycle](../product-lifecycle/SKILL.md) | Owns investment and lifecycle governance, not delivery continuity |
| Ongoing reliability ownership (SLOs, alerts, incidents) | [site-reliability-engineering](../site-reliability-engineering/SKILL.md) | Standing operational ownership, not an embedded engagement |
| Internal platform design or operation | [platform-engineering](../platform-engineering/SKILL.md) | Platform ownership, not customer delivery |
| One discipline fully owns the task | That specialist directly | FDE stops routing when one specialist owns the request |
| Advisory analysis ending before implementation and adoption | The relevant architecture or decision specialist | FDE completion requires adoption and outcome continuity |

## File map

| Path | Load when |
|---|---|
| [references/discovery-brief.md](references/discovery-brief.md) | Reviewing the boundary, overlap audit, or evidence basis |
| [references/source-index.md](references/source-index.md) | Checking an externally verifiable role claim or refresh date |
| [references/lifecycle-and-artifacts.md](references/lifecycle-and-artifacts.md) | Starting or handing off any lifecycle stage |
| [references/route-selection.md](references/route-selection.md) | Selecting one stage specialist without violating its entry boundary |
| [references/authority-and-escalation.md](references/authority-and-escalation.md) | Working under access, security, privacy, cost, or authority constraints |
| [references/adoption-and-measurement.md](references/adoption-and-measurement.md) | Evaluating activation, workflow adoption, and measurable impact |
| [references/generalization-and-productization.md](references/generalization-and-productization.md) | Deciding what field work becomes or does not become reusable |
| [references/communication.md](references/communication.md) | Writing status, decision, escalation, or handoff communication |
| [references/worked-example-engagement.md](references/worked-example-engagement.md) | Calibrating expected artifact depth or evidence labeling at any stage |
| [templates/](templates/) | Creating the charter, workflow map, ledger, stage handoff, engagement status, evaluation and release decision, adoption scorecard, outcome measurement record, productization record, or field learning record |
| [manifest.yaml](manifest.yaml) | Reading machine-readable stages, routes, outputs, and conflicts |
