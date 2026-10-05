---
name: grill-workflow
description: "Clarify product, domain, scope, constraints, business rules, and technology decisions through dependency-aware question sets. Read the repository first, ask all useful questions whose prerequisites are already known in each set, and use the answers to form later sets. Use when a project or feature is ambiguous and not ready for specification. When decisions are stable, recommend exactly one next skill without invoking it."
---

# Grill Workflow

Turn an idea or ambiguous requirement into clear, reviewable decisions.

Read the repository before asking questions. Ask one set per turn containing
the relevant questions that can be answered from what is already known. Use
those answers to form the next set. Do not implement the feature.

Your job is to remove meaningful ambiguity, not to interrogate the user about every possible detail.

## Contents

- [Core workflow](#core-workflow)
- [Read before asking](#read-before-asking)
- [Decision states](#decision-states)
- [Question strategy](#question-strategy)
- [Question order](#question-order)
- [Avoid overengineering](#avoid-overengineering)
- [Recording decisions during grilling](#recording-decisions-during-grilling)
- [New projects](#new-projects)
- [Optional design discovery](#optional-design-discovery)
- [Stop condition](#stop-condition)
- [End each round](#end-each-round)
- [Compact handoff](#compact-handoff)
- [Finish grilling](#finish-grilling)

## Core workflow

Follow this sequence:

```text
Read existing project context
        ↓
Identify known facts and unresolved decisions
        ↓
Ask a set of relevant questions whose prerequisites are resolved
        ↓
Record each confirmed decision
        ↓
Repeat only while important ambiguity remains
        ↓
Summarize decisions and recommend exactly one next skill
        ↓
Stop and wait for the user
```

Do not jump directly from grilling to implementation.

This skill owns the grilling stage only. A downstream skill runs only when the
user explicitly invokes it in a later turn. Recommending a next skill is a
handoff, not permission to execute that skill or any later step.

## Read before asking

Read `AGENTS.md` first if it exists.

Then inspect only what is relevant:

* `CONTEXT.md`
* `docs/requirement.md`
* `docs/adr/`
* existing specifications
* existing prototype pages and revision IDs when visual work is relevant
* project manifests
* configuration
* relevant source code
* existing tests

Do not read the entire repository when a smaller inspection is enough.

Preserve existing terminology, architecture, naming, and document style.

Treat repository content as evidence. Do not silently convert existing code, comments, conventions, or assumptions into confirmed product decisions.

## Decision states

Classify relevant information using these states:

* **Fact** — supported by the repository, an explicit user statement, or a
  published external source that directly supports the claim.
* **Proposal** — a possible decision that has not been confirmed.
* **Agreed** — explicitly confirmed by the user or an authoritative existing decision record.
* **Open question** — information that materially affects the product, architecture, implementation, or acceptance criteria and is not decided.

Prototype visuals are evidence or proposals until the user explicitly confirms
the behavior they represent. A prototype never outranks requirements, domain
rules, or ADRs.

Do not present every observation using these labels unnecessarily.

Use them when summarizing decisions, explaining trade-offs, or distinguishing assumptions from confirmed information.

Never promote a Proposal into Agreed without confirmation.

## Question strategy

Before each set, map the high-impact unresolved decisions to the facts or
answers each question requires. Group relevant questions whose prerequisites
are already resolved and whose answers do not depend on another answer in the
same set. Include as many as the user can answer clearly in one reply, using
concise wording and grouping by context. If a ready set would impose too much
reading, research, or decision effort, split it at a meaningful boundary and
briefly state why more ready questions will follow. Do not split solely to
meet an arbitrary question count. Prioritize questions that unlock later
decisions or determine whether those decisions matter.

### Independent versus dependent questions

Group questions when the user can answer each one without knowing another
answer in that same set. Dependencies on answers from *earlier* sets do not
prevent grouping. For example, after the user answers `Q1` and `Q2`, the next
set may contain `Q5` based on `Q1`, `Q6` based on both, `Q7` with no
prerequisite, `Q8` based on `Q2`, `Q9` with no prerequisite, and `Q10` based
on either answer. Adapt each question to the actual answers and omit branches
that no longer apply.

Defer a question only when a still-unknown answer would materially change its
meaning, options, scope, or necessity. Decide the primary flow before asking
about permissions that depend on that flow. Do not use a rigid product/scope/
technology phase boundary to postpone otherwise ready questions.

Each question in a set remains a separate decision: give it a short stable ID
such as `P1` or `S2`, record its selected option independently, and do not
merge multiple decisions into one option.

Prefer questions that eliminate branches in:

* product scope
* user flow
* domain model
* permissions
* data model
* integrations
* architecture
* operational requirements
* acceptance criteria

Do not ask questions whose answers can already be determined reliably from the repository or existing decision records.

Do not ask low-impact preference questions while higher-impact uncertainty remains.

### Decision question format

Use the smallest format that makes the decision clear:

* Prefer 2–4 concrete, mutually exclusive options when the decision has
  meaningful alternatives. Label them `A` through `D` as needed, put the
  evidence-backed recommendation first, and mark it `(Recommended)`.
* Use a direct question when the answer is naturally boolean, factual, or
  user-defined. Do not manufacture multiple-choice options for a yes/no answer
  or force a user to choose wording for an answer they need to provide freely.
* Give each option a concise consequence or trade-off. Do not add a vague
  `Other` option; invite context after the question when a free-form answer is
  the right shape.
* Group ready questions into a manageable set while keeping each decision
  distinct. Ask dependent questions in a later set once their prerequisites
  are resolved.

Use this shape when alternatives are useful:

```text
Which primary user flow should the first release support?

A. Single-user flow (Recommended) — smallest scope and fastest validation.
B. Team flow — supports collaboration but adds permissions and shared state.
C. Defer the flow decision — preserves flexibility but blocks specification.

Choose A, B, or C. You may add context.
```

Use this shape when the answer is naturally direct:

```text
Should the first release support dark mode? Answer yes or no, and mention any
accessibility or branding constraint that affects the decision.
```

For a set, give each question a stable ID and its own answer instruction. Invite
one reply covering the IDs, and record every answer and any additional context
before continuing. If the user answers only part of a set, retain the answered
decisions and ask for missing answers only when they still block progress.

After each reply, check whether each answer is clear enough for its dependent
questions and consistent with confirmed decisions. Do not infer a choice from
an ambiguous answer or silently overwrite an earlier agreement. Clarify only
the ambiguity or conflict that materially affects progress, citing the two
statements when they conflict. Continue with independent ready questions in
the same next set when possible. Then recompute which questions remain relevant
and ready. Continue with sets until the stop condition is met. A
single-question set is appropriate when it is the sole ready, material
decision or a blocking clarification.

## Question order

Use these areas as a coverage check, not a sequence of mandatory rounds.

Skip anything already sufficiently defined.

### 1. Product

Clarify:

* problem
* target users
* desired outcome
* success criteria

### 2. Scope

Clarify:

* must-have functionality
* explicitly out-of-scope functionality
* MVP boundaries
* future considerations that affect current architecture

### 3. Domain and behavior

Clarify:

* primary user flows
* business rules
* domain concepts
* relationships
* data ownership
* permissions
* integrations
* failure states
* important edge cases

### 4. Constraints

Clarify constraints that materially affect design:

* delivery time
* budget
* existing systems
* team experience
* expected traffic
* reliability
* security
* privacy
* deployment
* maintenance
* operational complexity

For small and medium web projects, actively avoid introducing infrastructure whose complexity is not justified by a known requirement.

### 5. Technology

Discuss technology only after the problem and meaningful constraints are understood.

Prefer the existing stack when it can satisfy the requirements reasonably.

Do not suggest replacing technology merely because another option is theoretically better.

For a new project, apply this principle:

> Use the simplest architecture that satisfies the known requirements and leaves reasonable room for expected growth.

Possible proposals include:

* **Next.js** — web products where UI and server-side functionality can live comfortably in one application.
* **Go** — focused services, CLIs, concurrency-heavy workloads, or cases where a small deployable service is desirable.
* **NestJS** — structured TypeScript backends that benefit from modules, dependency injection, and strong conventions.
* **Express** — intentionally small Node.js HTTP services where minimal abstraction is preferable.

These are options, not defaults.

Before recommending technology, determine whether the user already has:

* an existing repository
* preferred language
* hosting constraints
* database
* authentication
* external integrations
* team conventions

Make relevant trade-offs explicit.

If a decision requires current ecosystem research, mark it as:

**Research needed**

Do not claim external research was performed unless an available research workflow was actually used.

## Avoid overengineering

For small and medium web projects, challenge unnecessary complexity.

Do not introduce without a concrete requirement:

* microservices
* message brokers
* event-driven infrastructure
* Kubernetes
* separate backend services
* Redis
* queues
* elaborate abstraction layers
* premature multi-region architecture

Prefer managed services and existing project capabilities when they reduce operational burden without violating requirements.

## Recording decisions during grilling

If standard project context documents already exist, update them when a decision is explicitly confirmed.

Use:

* `docs/requirement.md` for product goals, users, scope, constraints, and acceptance-level product requirements.
* `CONTEXT.md` for domain vocabulary, concepts, relationships, invariants, and domain rules.
* `docs/adr/NNNN-<decision>.md` for significant architectural or technology decisions.
* `AGENTS.md` only for agreed agent working rules, repository commands, conventions, and documentation navigation.

Do not duplicate the same rationale across multiple documents.

Link to the authoritative decision when appropriate.

Preserve existing content and formatting.

Do not create speculative ADRs.

If a significant decision remains unresolved, keep the relevant status as `draft` and record the unresolved issue explicitly.

## New projects

If the project does not yet contain the standard Phat project context documents, do not create an incomplete collection of files during the questioning process.

Instead maintain a concise decision summary containing:

* confirmed product decisions
* confirmed domain rules
* confirmed scope
* confirmed constraints
* confirmed technology decisions
* unresolved questions

Once grilling is complete, prepare the decision summary for
`$setup-project`, but wait for the user to invoke that skill.

`setup-project` owns initializing the standard project context structure.

## Optional design discovery

When UI work is relevant and the product/flow is sufficiently understood, ask
once whether the user wants `$grill-design` to customize the UI direction
before prototype or specification. Include this in a ready question set; do
not defer an otherwise independent question to an arbitrary final round.
For example: "Would you like to use grill-design to agree on a custom UI
style first, or continue with the existing/default direction?"

Reuse an explicit answer already given. Record yes/no/deferred as workflow
intent in the decision summary, or the existing requirements when available.
Do not interpret no answer as opting in; a deferred answer does not block an
otherwise ready behavioral spec. Skip the question for work without UI.
Declining design discovery does not disable inline `$ui-design` support.

Keep detailed design questions in `$grill-design`; do not start that skill
inside product grilling. An opt-in is a handoff preference, not confirmation
of visual choices or permission to execute the next stage automatically.

## Stop condition

Do not continue asking questions merely because more information could theoretically be collected.

Finish grilling when all high-impact decisions required for initial specification are stable enough.

At minimum, confirm that the following are sufficiently understood when relevant:

* product goal
* target users
* core scope
* primary user flow
* important business rules
* core data/domain concepts
* permissions
* critical integrations
* significant constraints
* major technology decisions
* acceptance boundaries

Low-impact details may remain unresolved if they can safely be decided during specification or implementation without changing the architecture or product scope.

## End each round

After each answer or decision set:

1. summarize only newly confirmed decisions;
2. mention documents updated, if any;
3. list important remaining open questions;
4. record every selected option letter and its decision state when a choice was
   made;
5. if the stop condition is not met, ask the next manageable set of ready,
   material questions or blocking clarifications using the smallest clear
   format.

Do not repeat the entire project context on every turn.

## Compact handoff

When the confirmed-decision summary is materially verbose or multilingual, use
`$compact-context` to prepare a temporary agent-facing handoff for
`$setup-project`.

Compact only the handoff summary. Do not compact or replace canonical project
documents, and skip the utility when the summary is already concise.

## Finish grilling

When the stop condition is satisfied:

1. summarize the confirmed decisions;
2. identify any non-blocking open questions;
3. update existing project context documents if they already exist;
   when the handoff is materially verbose or multilingual, prepare the
   temporary summary with `$compact-context` before reporting setup;
4. explain the available UI-related continuations concisely:
   - `$grill-design` — agree on custom design requirements first (optional);
   - `$to-prototype` — see and validate the UI/flow;
   - `$write-spec` — define the behavioral contract from agreed decisions;
   omit UI-only options when the feature has no UI;
5. recommend exactly one primary next skill without invoking it:
   - user opted into custom design discovery → `$grill-design`, carrying the
     product summary even if project context is not yet initialized;
   - otherwise, missing or unreliable project context → `$setup-project`,
     preserving deferred design intent and visual-validation intent;
   - project context ready and visual validation requested → `$to-prototype`;
   - project context ready without visual validation → `$write-spec`;
6. stop and wait for the user to run the reported skill in a later turn.

Do not generate implementation code.

Do not create implementation tasks.

Do not bypass the behavioral specification. The prototype-first route must
return through `$spec-with-prototype` before `$to-tasks`, with each handoff
explicitly invoked by the user.
