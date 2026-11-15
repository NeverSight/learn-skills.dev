---
license: MIT
name: feature-planning
description: >
  Design software features and turn requirements into actionable, incremental
  implementation plans through plain-language discussion of feature breakdown,
  architecture, important data types, and risks, with user-confirmed decisions,
  feature priorities, evidence-based confidence, and effective tests.
  Use when planning a new feature, extending existing behavior, redesigning
  an existing system, or breaking a proposal into verifiable delivery steps.
---

# Feature Design and Planning

Consider the complete intended feature and its foreseeable extensions, while
delivering the user's main goal as soon as possible. Keep the mainline limited
to the behavior, prerequisites, and safeguards needed for that goal. Defer all
optional side features; add selected extensions one small feature at a time
after the main goal works. Scale planning detail to the feature's complexity
and risk; avoid turning a small change into an architecture project.

## Establish the outcome and boundaries

- Identify the user's problem, expected observable behavior, scope, constraints,
  and completion criteria. Separate requirements from assumptions and optional
  extensions. Surface unresolved decisions for the design dialogue below;
  continue independent investigation while they remain unresolved.
- Inspect the existing implementation, callers, interfaces, and relevant tests
  before proposing replacements or new abstractions. Identify what can be reused
  and where current behavior must remain compatible.
- Consider the full path from input to result, including relevant failure modes,
  data lifecycle, permissions, integration, migration, and rollout. Address risks
  that affect correctness now; explain why a concern can be deferred when its
  omission would otherwise leave a gap in the design.
- Make foreseeable extension points explicit: what is likely to vary, which
  boundary accommodates it, and what change would justify extending that boundary.
  Reserve these paths through clear ownership and contracts. Do not prebuild
  speculative frameworks, configuration systems, or unused generalizations.

## Build a shared understanding through discussion

Discuss the feature with the user before finalizing its design or delivery plan.
Use simple, familiar words suited to the user's knowledge; explain necessary
technical terms when first used. Start with what the user will be able to do,
using concrete inputs, actions, results, and failure examples before introducing
implementation details.

- Break the requested feature into understandable capabilities together with
  the user. Explain what each part does, why it is needed, and how the parts
  connect to deliver the complete outcome. Invite corrections to the breakdown
  before using it as the basis for design choices or implementation steps.
- Identify the design points within those parts: choices that change behavior,
  responsibilities, how parts interact, or future extensions. Discuss the
  consequential choices as they arise instead of presenting a finished design
  for blanket approval. Reuse decisions the user has already made.
- When discussing a system redesign, start from the behavior users and callers
  observe today. Preserve it outside the changes the user requested. Limit any
  additional behavior change to a real defect that the proposed structural
  change resolves as part of the redesign itself. Show what should happen,
  what goes wrong today, and how the redesign fixes it. Keep fixes that need
  independent behavior changes outside the redesign scope.
- Develop and explain the architecture and important data type designs with the
  user during this discussion; recording specifications in the plan alone does
  not satisfy this requirement. Walk through concrete inputs, component
  interactions, representative data values, state changes, and failure cases.
  Explain why responsibilities and type boundaries belong where proposed, which
  invalid states the types prevent, and how foreseeable extensions fit. Discuss
  consequential alternatives and resolve the user's questions and corrections
  before treating those design choices as confirmed.
- For each consequential choice, describe the proposed behavior with an example,
  explain realistic alternatives and their tradeoffs, and give a recommendation
  with reasons. Make clear what the user is deciding and what it changes.
- Explain material risks in practical terms: what could go wrong, who or what
  would be affected, what evidence is missing, and how the design or a planned
  check addresses it. Surface remaining uncertainty and costly-to-reverse choices
  before asking the user to decide; a risk label alone is not an explanation.
- At meaningful decision points, recap the resulting design in plain language,
  including how the parts work together, the main risks, and what remains open.
  Ask focused questions that let the user correct the design and resolve pending
  choices. Do not infer understanding or agreement from silence or a generic
  approval; do not repeatedly reconfirm unchanged answers.

Carry these explanations and the user's corrections into the plan. A detailed
plan file does not replace the conversation needed for the user to understand
the proposed design and its consequences.

## Keep proposed additions outside the mainline

Trace proposed behavior and constraints to the user's raw requirements, prior
confirmed decisions, or an established contract. If an addition goes beyond that
basis, ask the user whether it belongs in scope before treating it as required.
This includes agent-proposed resource budgets, quotas, performance targets, and
configurable limits; their usefulness alone does not establish a requirement.

Keep unconfirmed additions in a separate proposal list with their rationale,
tradeoffs, and pending decision. Do not assign them urgent or required priority,
mix them into the main delivery sequence or acceptance criteria, or make them
prerequisites for independent requested work. When considering a nontrivial
addition for delivery, discuss design alternatives and consequences before requesting a scope decision;
approval of the general goal does not settle the added constraint or its value.
If accepted for later consideration, keep it deferred. Confirm design, priority,
and an explicit decision to promote it into delivery before integrating it.
Resolve optional design questions when selecting that extension; do not let
their discussion delay independent work on the main goal.

Distinguish optional additions from safeguards needed to satisfy existing
requirements or contracts. Show the dependency and evidence for a necessary
safeguard; if it introduces a new product policy or an unresolved limit, ask the
user to decide it and block only the work that depends on that decision. Keep
foreseeable extensions visible without making them current delivery obligations.

## Prioritize design questions and confirm decisions

Treat design as a dialogue with the user. Confirm each design decision needed
for selected delivery before treating it as settled; deferred possibilities do
not need detailed design now. Existing explicit
answers count as confirmation; do not repeatedly ask about unchanged decisions.
Classify each question before asking it and show that priority to the user:

- **Required now:** its answer changes the main goal's correctness, feasibility,
  or a choice that would be costly to reverse now. Explain the affected work and
  why the decision cannot wait; block only that work.
- **Required later:** it belongs to agreed scope but does not affect the current
  increment. State when it must be resolved and keep earlier independent work moving.
- **Deferred possibility:** it concerns an optional or immature extension. Record
  the possibility and a reconsideration trigger; defer detailed design questions
  until selecting it for delivery. If a decision is needed now only to preserve
  an extension path, ask about that minimal boundary, not the whole future feature.

- Keep a decision record with the question, concrete proposal or alternatives,
  rationale, priority and its reason, affected work, resolution trigger, and status:
  confirmed, pending, or conflicting. Cover behavior and
  exclusions, interfaces, data semantics, permissions, failures, compatibility,
  migration, rollout, extension boundaries, priorities, and acceptance criteria
  wherever they apply. Include the decision to defer or omit a concern.
- Ask focused questions in manageable batches. Explain the tradeoff in the
  simplest words that keep the meaning precise. Avoid jargon and overly formal
  language. Say what happens with each choice and what the user gains or gives
  up. Use a short example when it makes the difference clearer. For example,
  "If an import has one bad row, should we save the good rows right away and
  list the bad row for you to fix, or save nothing so your data stays as it is
  until you can import the whole file?" Offer a recommendation when evidence
  supports one. Use available question tools or direct conversational questions,
  and wait for the user's answers. A generic request to approve the whole plan
  does not confirm its individual details.
- Do not accept ambiguous terms such as "fast," "large," or "handles errors."
  Ask for concrete inputs, outputs, limits, units, examples, and failure behavior
  until the interpretation is unambiguous. Expose contradictions and obtain a
  decision; do not silently choose an interpretation or invent requirements.
- Silence, elapsed time, a preselected answer, and the agent's confidence do not
  count as confirmation. Mark unanswered questions as pending and block work that
  depends on them. Continue only independent investigation or already confirmed
  work. Present a provisional plan while questions remain; never call it agreed.
- Unknown empirical facts can have bounded investigations, but confirm their
  questions and decision rules. If findings require a new or changed design
  decision, return to the user. Preserve prior confirmations that still apply.

## Choose a proportionate design

When assessing complexity or explaining why a feature is hard to deliver,
distinguish its sources explicitly:

- **Inherent problem or feature complexity:** required rules, states,
  interactions, and safeguards that remain even with a well-fitting architecture.
- **Existing architecture friction:** current coupling, misplaced ownership,
  incompatible interfaces, or missing extension seams that make integration hard.

Both can contribute. Cite the requirements and implementation evidence for each;
mark uncertain attribution and name the investigation needed. Separately identify
avoidable complexity introduced by the proposal. Explain these sources to the
user and keep their effort and risk visible in the plan. For architectural
friction, compare a bounded structural change with direct integration, including
migration cost and reversibility. Difficulty does not make broad refactoring
necessary or authorize it, and architectural friction does not justify cutting
required behavior or describing the feature itself as inherently complex.

Prefer the simplest design that satisfies the complete current requirements and
keeps justified extensions possible. Compare alternatives only where a material
tradeoff exists. Explain consequential choices using existing constraints and
evidence, including migration cost or reversibility where relevant.

Control architecture without expanding delivery scope: identify the ownership,
interfaces, data contracts, and dependency direction that let foreseeable
extensions be added independently. Resolve choices that would lock those paths
out now, and state how each deferred feature can attach later. Use the smallest
boundary that preserves that path; implement shared machinery only when current
behavior needs it. Future extensibility must not become a prerequisite to build
all future capabilities before delivering the main goal.

If uncertainty could invalidate the main goal's architecture or delivery order,
schedule a bounded investigation with a specific question, evidence to collect, and a decision it
will unlock. Distinguish its findings from delivered functionality; remove or
integrate exploratory code deliberately. Avoid open-ended research and abstractions
whose only justification is that they might be useful someday.

## Design architecture and important data types with the user

Provide concrete architecture and important data type designs in the design
discussion, explain and resolve their consequential choices with the user, and
carry the resulting designs into every delivered plan, including provisional
plans. A specification without that discussion is insufficient. Scale their depth to
the feature's complexity; a small change may need only a concise description of
the existing architecture and types it reuses. Do not omit these designs or
replace them with a list of files to change. Mark unresolved choices as pending
and keep dependent implementation provisional.

- **Architecture:** identify the components and their responsibilities, ownership,
  interfaces, dependency direction, and integration with existing code. Walk through
  the main input-to-result flow and relevant failure paths, showing where state
  lives and which component enforces each important rule. Explain material design
  tradeoffs, compatibility or migration needs, and the boundaries reserved for
  foreseeable extensions without building speculative machinery.
  Name the important modules and their existing or proposed locations, the key
  functions or methods they expose, and their input, output, and error contracts.
  Show signatures or equivalent interface definitions and concrete caller wiring;
  conceptual layers or a diagram alone do not constitute an implementation design.
  Distinguish inspected existing symbols from proposed ones.
- **Important data types:** define the domain, state, and boundary types that carry
  the feature's important contracts. Provide concrete declarations, schemas, or
  field tables for important new or changed structures. Specify meaningful fields and their types,
  identity and relationships, valid variants or states, invariants, and how those
  invariants are enforced. Explain ownership and lifecycle, state transitions, and
  error representations where relevant. Cover serialization, persistence, and
  compatibility when data crosses those boundaries. Identify existing types to
  reuse or change; if no new types are needed, state that and describe the relevant
  existing contracts.
- Connect the designs: show how the important types pass through component
  interfaces and how responsibilities preserve their invariants. Map the design
  changes to delivery increments and acceptance checks. Resolve decisions needed
  for current correctness and extension boundaries now; retain explicit triggers
  for deferred detail rather than leaving gaps that block implementation.

## Prioritize capabilities and uncertainty

Assign each capability a priority and explain it using user impact, actual timing
constraints, dependencies, and the cost of being wrong. Confirm these assignments
with the user rather than inventing deadlines or business urgency.
Apply delivery priorities only after establishing scope; uncertainty or potential
value does not promote an unconfirmed addition into urgent mainline work.

- **Urgent:** needed for the immediate user outcome, a prerequisite that blocks
  that outcome, or an investigation needed to avoid invalidating its delivery.
  State why it must happen now and the smallest useful result it can deliver.
- **Required later:** part of the agreed complete feature, but safely sequenced
  after earlier increments. Give it a concrete delivery step and acceptance check.
  Lower urgency does not remove it from completion criteria.
- **Deferred:** all optional side features, even when useful or well understood,
  plus user-confirmed scope changes postponed from current delivery. Record the
  consequence of deferral, evidence needed, and a concrete reconsideration trigger
  such as a resolved dependency, measured threshold, or confirmed user need.

Priority and confidence are separate judgments. A low-confidence decision with a
large downstream impact on the main goal may require urgent investigation.
Optional extensions remain deferred. Do not defer essential correctness,
permissions, data integrity, or their acceptance checks merely because they are
difficult or unclear.
Reduce uncertainty with a bounded check, or obtain an explicit scope decision.
Keep deferred work visible without implementing speculative support for it.

Readiness is a separate gate from priority and scope approval. Never schedule an
immature or unsound feature for implementation, even as an early prerequisite
or an automatic follow-on after the main goal. Interest or user confirmation
alone does not establish feasibility or a coherent design. For an optional idea,
reserve only a brief possibility, known uncertainty, reconsideration trigger,
and the smallest existing boundary that keeps it possible; no speculative APIs,
configuration, abstractions, scaffolding, or implementation tasks are needed.
Promote it only after evidence supports its behavior and approach, material
contradictions are resolved, and the user selects its design and delivery priority.
If an immature capability is essential to agreed scope, retain the obligation
but schedule only a bounded investigation or redesign before dependent delivery.
An unsound approach must be replaced or rejected, not implemented provisionally.

## Build an ordered sequence of increments

- Mark the earliest usable delivery of the main goal and its acceptance check.
  Every step before it must explain why the goal requires that work now. Remove
  optional side features from that path, including optional refactors and shared
  infrastructure justified only by later extensions. Preserve all requirements
  and safeguards needed for the main goal; a thin mainline must still work.
- After that delivery, introduce each selected, implementation-ready extension
  through its own small, verifiable increments. Validate its integration before adding the next feature.
  Do not bundle the deferred feature list into one expansion step or joint gate.
- Begin with the smallest coherent behavior that can be exercised through the
  relevant real path. Expand capability and integration step by step toward the
  full outcome. Name steps by the behavior or decision they deliver.
- Discovery followed by one step containing all functionality and a final cleanup
  step is still one-shot delivery. Split the implementation itself into working
  increments. Keep incomplete paths gated until their required safeguards work;
  incremental development does not require exposing unfinished behavior to users.
- Prefer working slices across the necessary layers. Avoid a sequence consisting
  only of all data structures, then all services, then all UI, with no observable
  result until the end. Necessary enabling work must state which next behavior it
  unlocks and how its contract can be checked independently.
- Order prerequisites explicitly. Bring forward cheap checks of high-impact
  assumptions; keep later steps from depending on unresolved guesses. Split any
  step that hides several independently risky changes or has vague completion
  criteria. Do not manufacture steps that add no meaningful outcome or evidence.
- Keep intermediate states coherent and compatible. Identify temporary bridges,
  migration ordering, gating, cleanup, and recovery when needed. Assign removal of
  temporary mechanisms to a concrete step so they do not become permanent debt.
- Map every current requirement and material risk to a delivery step and a check.
  Deferring an agreed requirement to an unspecified future effort does not complete
  the plan. Keep optional extensions separate from required completion work.

For example, a data export can first download a small authorized result behind a
gate, then expand to complete traversal and failure handling, then establish the
supported scale. Each increment exercises the real export path; grouping all
backend work before all frontend work does not provide that progression.

For **each step**, provide:

1. **Outcome, scope, and priority:** the observable behavior or resolved uncertainty,
   affected boundaries, prerequisites, and why it belongs at this point in the plan.
2. **Actions:** concrete changes, in enough detail that implementation can start;
   identify relevant components without inventing uninspected file paths.
3. **Acceptance fixtures and tests:** concrete fixtures with observable completion
   criteria, how to exercise them, and any relevant failure or compatibility case.
4. **Confidence:** low, medium, or high, with supporting evidence, remaining
   uncertainty, and the next check that could increase or reduce confidence.
5. **Commit boundaries:** the small, coherent commits that deliver the step,
   each with its purpose and verification. Split a step into multiple commits
   when it contains independently reviewable changes; keep required tests with
   the behavior they verify and preserve coherent intermediate states.

Use confidence as a reasoned judgment, not a fabricated probability. High means
direct evidence supports the approach and important risks have effective checks;
medium means the approach is supported but a material assumption remains untested;
low means missing evidence could change the design or sequence. Distinguish planned
checks from checks already performed. A confident design is not a verified result.

## Plan tests that can expose defects

- Provide concrete fixtures for each new feature or fix in the plan, not just a
  promise to add tests. A fixture is a reproducible case: setup or initial state,
  specific input or action, independently justified expected output or state,
  and the public boundary and command or harness that exercises it. Include the
  case inline or reference an existing repository fixture; name its owning step.
- For a new feature, the fixtures serve as acceptance criteria. Plan the
  implementation to make them pass through the real behavior path.
- For a fix, provide a regression fixture that fails on the unfixed behavior
  because of the reported defect and passes after the repair. Plan to run the
  same case and expectation before and after the fix; a missing harness, build
  failure, or unrelated error does not demonstrate reproduction. Record observed
  results only when actually run; otherwise mark the baseline check as pending.
- Additional unit tests may cover rules, boundaries, and failure paths, but do
  not replace the required acceptance or regression fixtures. Reuse existing
  fixtures when they meet these requirements; no separate fixture file format
  or test level is mandatory.
- Tie each check to a requirement, risk, or plausible regression. State the input
  or setup, expected observable result, and the defect it would detect. If a test
  would still pass with that defect present, strengthen its assertion or replace it.
- Check behavior through the appropriate public boundary. Choose unit tests for
  isolated rules, integration tests for real contracts, and end-to-end tests for
  critical user paths; use only the levels the risk justifies. Reuse good coverage
  instead of duplicating it at every layer.
- Include meaningful boundaries and failure paths where applicable, such as empty
  input, invalid state, permissions, partial failure, retry, or migration of existing
  data. Select cases from the design's actual risks rather than a generic checklist.
- Keep expectations independent of the implementation. Do not recompute the answer
  with the same algorithm under test, assert only that execution did not crash, or
  mock away the integration whose behavior needs verification. Use controlled
  dependencies when needed, while preserving the contract being tested.
  Derive fixture expectations from requirements, established contracts, or an
  independent oracle. Avoid tautologies such as comparing output with itself,
  copying actual output into expectations without checking it, or asserting
  only values configured on a mock.
- Match effort to impact. Avoid brittle assertions about internal call order,
  snapshots without a behavioral purpose, and tests that merely mirror code.
  Identify manual or exploratory checks when automation would add little value;
  say what evidence they should produce and what remains unverified.

## Deliver and evaluate the plan

Begin every delivered plan, including provisional plans, with the required feature
and its decomposition so the user can verify that the planned feature matches
their intent. Unroll it step by step:

1. **Raw request:** preserve the user's original request verbatim before
   interpreting it. Keep assumptions and agent proposals separate.
2. **Requirement decomposition:** derive the intended outcome, required
   capabilities, and observable behaviors from that request. Show how each level
   follows from the preceding one, retaining links to its source requirement or
   confirmed decision rather than jumping straight to implementation tasks.
3. **Discussion revisions:** retain an ordered record of changes and
   clarifications, including the prior interpretation, the revised requirement,
   its source and rationale, and confirmation status. Preserve superseded decisions
   as history while making the current requirement clear; never silently replace
   the raw request or treat an unconfirmed proposal as agreed scope.

Use this opening section as the basis for the rest of the plan. Trace current
requirements to delivery steps and acceptance checks so omissions and unintended
additions can be identified, and update those links when discussion changes scope.

Then provide the required architecture and important data type designs described
above. Explain in plain language how the confirmed design works and how its parts
fit together, including the material risks, planned safeguards, and remaining
uncertainty discussed with the user. Present the intended outcome, confirmed
design decisions, ordered steps with their priorities, tests, and confidence,
and the explicit extension boundaries.
List deferred capabilities with reasons and reconsideration triggers. Keep pending
questions visible and dependent steps provisional. Do not impose a fixed number
of stages or leave the final step as an unexplained instruction to finish
everything else.

Every delivered plan, including each local plan file, must contain an explicit
**Implementation contract** for the implementing agent. Include these obligations
in the plan itself rather than relying on this skill being loaded during execution:

- Implement in fine-grained, coherent commits following the planned boundaries.
  Do not squeeze the implementation into one large commit or accumulate all
  increments for a single final commit.
- Verify each commit's behavior with its applicable acceptance checks and commit
  the completed unit before advancing to the next. Keep related implementation
  and tests together; do not split merely by file or create broken intermediate
  commits to meet an arbitrary size or count.
- Make the planned acceptance fixtures pass. For fixes, first demonstrate the
  regression fixture failing for the defect, then passing after the repair.
  Preserve independent expectations; do not weaken fixtures to fit the code.
- If evidence requires changing the sequence or boundaries, update the remaining
  plan while preserving small, independently reviewable commits. Reconfirm any
  changed design decisions before dependent work.

When writing a local plan file, treat it as deliberately untracked. Do not check
its tracking status or reread it solely to confirm the write.

For a planning-only request, deliver the plan without implementing the feature.
When implementation is authorized, follow the plan's implementation contract:
execute one commit unit at a time, inspect the result, run its checks, commit the
verified unit, and update confidence before progressing. Passing checks
must support the claimed behavior; failures or contradictory evidence require
fixing the step or revising dependent steps. Report the remaining gap to the full
outcome. Reconfirm new or changed design details with the user before dependent
implementation; proceed with unchanged, already confirmed decisions.
