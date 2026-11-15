---
license: MIT
name: feature-plan-review
description: >
  Review feature plans for clear feature boundaries and dependencies, actionable
  vertical slices, incremental growth of interacting features, small verifiable
  commits, design complexity, complete scope, and
  effective validation; reject unreviewable plans with a rewrite request. Use to audit
  an existing feature plan or assess implementation readiness, rather than
  create a plan or review implemented code.
---

# Feature Plan Review

Assess whether the plan delivers the **complete intended outcome** through
**coherent, verifiable increments**. Focus on **behavior and design adoption**,
not formatting or linting. Scale review depth to the actual risk.

## Establish the basis

- Read the plan, requirements, constraints, exclusions, and prior decisions.
  Separate **confirmed requirements**, **assumptions**, and **optional extensions**.
- Inspect relevant existing code, callers, contracts, and tests when available.
  Verify reuse and compatibility claims; do not invent paths or evidence.
- Request consequential missing inputs while continuing independent checks.
  Keep affected conclusions **provisional**; silence is not confirmation.
- When asking the user to decide, explain what each choice would change in
  simple, direct language. Avoid jargon and overly formal wording. Give a short
  example when it helps the user see the difference.
- Review only unless changes are authorized. Local plans are deliberately
  untracked: read them as review input, without investigating tracking status
  or rereading solely to confirm an authorized write.

## Audit the plan

- **Design-question priority:** Require each design question to distinguish a
  decision needed now, a decision needed before a later agreed increment, and a
  deferred possibility. Check its consequence, affected work, and resolution
  trigger. Flag optional design dialogue that delays independent main-goal work;
  ask only about a minimal extension boundary when that is all that matters now.
- **Feature maturity:** Assess readiness separately from scope approval and
  delivery priority. Reject implementation steps for immature or unsound features,
  including speculative prerequisites and automatic post-main-goal expansions.
  For optional ideas, require only a brief possibility, uncertainty, reconsideration
  trigger, and minimal extension boundary; remove premature detailed designs,
  scaffolding, and implementation commitments. Promotion requires evidence of
  feasibility and coherent behavior, resolved material contradictions, and a
  confirmed design and delivery priority. For essential but immature capabilities,
  retain agreed scope and require bounded investigation or redesign first;
  block dependent implementation, not independent ready slices. An unsound approach
  needs replacement or rejection, not provisional implementation.
- **Earliest main-goal delivery:** Identify the first usable delivery of the user's
  main goal and its acceptance evidence. Require every preceding step to justify
  a necessary behavior, prerequisite, or safeguard. Flag optional side features,
  refactors, and infrastructure that delay it; defer them even when useful or
  well understood. Keep the mainline thin without dropping required correctness
  or agreed behavior. Optional design questions must not block independent main
  work. After the main goal works, require selected, ready extensions to arrive one small
  feature at a time with integration evidence before the next; reject a single
  expansion step or joint gate that adds all deferred features at once.
- **Unconfirmed scope additions:** Trace proposed behavior and constraints to raw
  requirements, prior user confirmations, or established contracts. Flag invented
  resource budgets, quotas, performance targets, configurable limits, and other
  additions presented as requirements without that basis. Ask the user whether
  they belong in scope when considering promotion into delivery; nontrivial
  additions need explicit discussion of design alternatives and consequences
  before their design and priority can be settled. Do not demand detailed design
  for possibilities that remain deferred.
  Require a separate pending proposal list until confirmed, outside the main
  delivery sequence, acceptance criteria, and urgent or required priorities.
  Potential value, uncertainty, or a reviewer recommendation does not establish
  urgency or permission to expand scope. Check claimed safeguard dependencies
  against evidence: preserve work necessary for existing requirements and
  contracts, while seeking a user decision for any new policy or unresolved
  limit. Block only dependent work; independent requested slices can remain ready.
- **Feature boundaries:** Establish whether the plan describes one coherent
  feature or a bundle of features before assessing individual delivery steps.
  For a bundle, identify each feature's user outcome, responsibilities, owned
  state or contracts, exclusions, and acceptance criteria. Flag unrelated goals,
  overlapping ownership, and shared work mixed into feature scope without clear
  boundaries. A shared roadmap is valid; placing everything under one feature
  heading does not establish cohesion. Preserve the full agreed outcome when
  separating features, and distinguish feature boundaries from delivery slices.
- **Unequal feature size and risk:** Flag a large, risky feature bundled with
  smaller features under one estimate, readiness verdict, or delivery gate.
  Assess their scope and readiness separately; prevent the larger feature's
  uncertainty, effort, or failure from obscuring or unnecessarily blocking smaller
  independent outcomes. Require explicit dependency evidence for joint delivery.
  Keep genuinely coupled behavior together with bounded increments and checks;
  a shared roadmap is acceptable, and separation must preserve the agreed scope.
- **Inter-feature dependencies:** Identify which feature requires which other
  feature, the specific behavior or contract required, why it is required, and
  when it becomes available. Distinguish hard prerequisites from shared
  infrastructure, optional integrations, and convenient sequencing. Check that
  each feature has clear acceptance criteria and that combined behavior has an
  integration check. Expose cycles and hidden coupling; propose a contract change,
  bounded shared prerequisite, or coherent joint delivery when independence is
  unjustified. Do not force independent delivery or duplicate shared machinery
  merely to claim separation. Assign ownership and acceptance checks to shared
  work, and carry dependency gates into the delivery order.
- **Combinational complexity and growth:** Look for features whose interactions
  multiply behavior across options, modes, states, or integrations. Require a
  growth path from a narrow working combination to the complete agreed outcome,
  adding bounded capabilities or interactions with observable checks at each
  increment. Name supported and unsupported combinations at intermediate states,
  their gates, and the contract preserving room for the remaining combinations.
  Exercise meaningful interactions and failures as they become available; isolated
  feature tests alone cannot establish that combinations work. Challenge plans
  that deliver the whole interaction space at once or defer integration to the
  end. A jointly released feature can still grow through small internal commits;
  preserve required final coverage and safeguards throughout that sequence.
- **Complete scope:** Map every requirement and material risk to a step and
  acceptance check. Trace success, failure, and state transitions across the real
  path. Check applicable permissions, data lifecycle, concurrency, compatibility,
  migration, rollout, and recovery. Required work cannot disappear into "later."
- **Design adoption:** Check actual callers, ownership, and integration. Flag
  unused abstractions, duplicate sources of truth, old paths left active, and
  incomplete migrations. Resolve consequential ambiguity before dependent work.
- **Concrete implementation design:** Require important modules with existing or
  proposed locations, responsibilities, key function or method signatures,
  input/output/error contracts, and concrete caller wiring. Require definitions
  of important new or changed data structures with fields and types, variants,
  relationships, invariants, and enforcement; identify existing types reused
  unchanged. Walk a fixture through these interfaces and state transitions.
  Conceptual layers, diagrams, or file lists alone are insufficient. Missing
  consequential design choices block dependent steps; do not demand speculative
  implementation detail for deferred possibilities.
- **Complexity:** Compare with the simplest design satisfying the requirements.
  Require an explicit distinction between complexity inherent in required rules,
  states, and interactions and integration difficulty caused by the existing
  architecture. Both may contribute; check the requirement and code evidence,
  or mark attribution unverified. Assess avoidable complexity added by the
  proposal separately. Check that estimates and proposed structural preparation
  reflect these sources rather than treating all difficulty as feature complexity
  or using it to justify scope cuts or an unsupported broad refactor.
  Challenge unnecessary layers, services, dependencies, configuration, frameworks,
  duplicate state, and temporary bridges. Identify the concrete burden and offer
  a simpler alternative preserving behavior and justified extension seams.
  Do not simplify away required safeguards or judge complexity by file counts.
- **Redesign behavior:** Compare the proposed behavior with what users and
  callers observe today. For changes beyond the user's requested behavior,
  require evidence of a real defect and show how the proposed structural change
  fixes it as part of the redesign. Flag behavior drift and repairs that need
  independent changes. Check that the plan verifies preservation and covers
  any accepted defect with a regression fixture.
- **Vertical slices:** Check each delivery step individually: does it deliver a
  narrow behavior through the necessary layers, with **observable effects now**?
  Name the entry point and changed result exercisable when that step completes.
  Dependencies and rollout gates are valid; reliance on later repairs is not. Flag
  sequences of "all backend, all frontend, then integration" and discovery followed by one
  giant build. Keep wiring and meaningful tests with their behavior.
- **Verification and validation (V&V):** For every step, require a concrete way to
  exercise its effect, expected before/after behavior, and evidence to retain.
  **Verification** checks the step's contract; **validation** checks its contribution
  to the intended user outcome. Gated and backend-only changes can be observed
  through an appropriate API, command, test, or demo. If evidence depends on later
  steps, reslice the work or justify bounded enabling work with its own check.
- **Overloaded steps:** Look for independent outcomes, decisions, risks, or checks
  bundled together. Split concerns that can be delivered or reconsidered separately
  without breaking each other. Keep one coherent cross-layer behavior together;
  more bullets or artificial layer splits do not improve delivery boundaries.
  Separate substantial independent refactoring and unrelated fixes where useful.
- **Commit size and verifiability:** Treat each proposed implementation step as
  one commit. Require a small, coherent change whose purpose, affected contracts,
  and correctness can be assessed without holding a large set of simultaneous
  changes in mind. Give it focused acceptance evidence runnable at that commit,
  without later commits to finish wiring or make its checks meaningful. Split a
  large step even if it serves one feature; check conceptual scope and verification
  effort rather than imposing a line or file limit. Keep the smallest complete
  behavior and its tests together, or justify bounded enabling work with a directly
  verifiable contract. Relabeling a large batch as one step does not make it small.
- **Actionability:** Each step needs an outcome, concrete actions, affected
  components or contracts, prerequisites, and observable acceptance criteria.
  Reference details elsewhere rather than demanding a fixed template. Enabling
  work and investigations need a bounded question or contract, evidence to collect,
  and the next behavior they unlock; they are not delivered functionality.
- **Ordering and intermediate states:** Expose hidden prerequisites and cycles.
  Investigate high-impact uncertainty before expensive dependent work. Keep
  intermediate states compatible and safe; assign temporary bridge removal and
  necessary cleanup to explicit steps. Challenge vague "finish everything" steps.
- **Confidence, effort, risk, and expected benefits:** Evaluate all four for each
  feature, including shared prerequisites, rather than averaging across a bundle.
  Confidence means confidence in the proposed behavior and approach: give evidence,
  consequential unknowns, and the next check; distinguish planned from completed
  checks. Effort covers implementation, integration, validation, migration, and
  ongoing maintenance where applicable; state the estimate's basis and uncertainty.
  Risk covers plausible failure, likelihood, impact, affected scope, and mitigation
  or recovery. Benefits mean the expected user or business gain, who receives it,
  and how it will be observed; quantify financial profit only when relevant and
  supported. Qualitative assessments are valid when justified; expose missing
  evidence instead of inventing precise estimates or scores.
- **Priority:** Use the separate confidence, effort, risk, and benefit assessments,
  actual constraints, and dependencies to justify urgent, required-later, and
  deferred work. High value does not establish high confidence or low risk.
  Optional deferrals need reasons, consequences, and reconsideration triggers.
  Do not invent deadlines or agreement.
- **Acceptance and regression fixtures:** Require concrete reproducible cases in
  the plan or referenced repository fixtures, with initial state, input or action,
  independently justified expected result, execution boundary and command or
  harness, and owning step. New-feature fixtures must define acceptance criteria
  that implementation will make pass. Fix fixtures must expose the reported
  defect on unfixed behavior and pass after the repair with the same expectation;
  unrelated harness or build failures do not count. A promise to add tests or
  supplementary unit tests alone is insufficient. Missing fixtures block the
  affected implementation steps; distinguish planned checks from observed evidence.
- **Effective tests:** Require a meaningful setup, expected observable result, and
  plausible defect each check detects. Could it pass with the behavior broken?
  Flag implementation-mirroring assertions, no-crash checks, and mocks that hide
  the contract under review. Cover relevant boundaries and failures at appropriate
  test levels; avoid redundant coverage. Concrete manual checks can suffice for
  low-impact changes when expressed as reproducible fixtures with concrete
  expectations. Reject tautological checks, expectations derived from the same
  implementation, unchecked copied output, and assertions only about mock setup.
  Reviewing a plan does not require running future tests.
- **Future extensions:** Name foreseeable variation, the boundary accommodating
  it, and a concrete expansion trigger. Resolve decisions that constrain it now
  through clear ownership, interfaces, data contracts, and dependency direction.
  Check how deferred features can attach independently; flag architecture that
  forces them into the mainline or requires speculative shared machinery before
  the main goal works. Preserve extension paths with the smallest sufficient
  boundaries. Consider the full outcome; avoid
  version labels that conceal unexplained scope cuts.

## Report findings

Lead with **implementation readiness**: ready, ready only for identified independent
slices, needs targeted repairs, or **rejected — rewrite required**. Name the specific features and steps
blocked. Reject the plan when mixed scope, missing boundaries or dependency
contracts, contradictions, or missing outcomes make it impossible to reliably
assess implementation readiness without inventing consequential decisions.
Poor prose or a different template alone is not grounds for rejection.

For a rejection, cite representative defects and explain why local edits cannot
resolve them. Explicitly request a rewritten plan, specifying the required feature
boundaries, dependency contracts and order, unresolved decisions, and acceptance
evidence. Do not manufacture a full replacement plan or imply implementation is
approved. A rewrite request is a review outcome, not permission to edit the plan.

Unresolved work need not block independent ready slices; a small coherent feature may need
only one implementation step.

Include a concise per-feature assessment of **confidence, effort, risk, and expected
benefits**, with evidence or explicit unknowns and the resulting priority and
readiness implications. Identify shared costs and dependency gates without hiding
individual assessments in a bundle-wide score. Scale detail to the decision;
do not omit a dimension merely because no defect was found.

For each substantive root cause, provide **location and evidence**, **consequence**,
**blocking scope**, **concrete repair**, and **acceptance evidence**. Distinguish
confirmed defects, open questions, and optional improvements; order by consequence.
Do not turn preferences or unsupported possibilities into findings.

For locally repairable overloaded or misordered work, propose **replacement steps in dependency
order**, each sized for one small commit with an outcome, actions,
**observable effects**, and **V&V checks**. For interacting features, show how these
commits grow supported combinations toward the complete outcome.
Preserve agreed scope and necessary safeguards. Rewrite only what findings require.

State evidence limits and remaining required decisions. If no substantive findings
exist, say so; do not invent objections or claim the feature itself is verified.
