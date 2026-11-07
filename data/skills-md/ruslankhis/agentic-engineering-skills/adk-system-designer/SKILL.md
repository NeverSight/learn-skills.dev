---
name: adk-system-designer
description: >-
  Work through requirements and trade-offs with the user to design or review
  the system architecture of a Python Google ADK application on GCP, before
  implementation. Use for a new application design, a substantial redesign, or
  a cross-cutting architecture review, including scoping a proof of concept,
  internal tool or MVP to the time and people available and planning what
  ships first and what follows, and turning the design and plan into a client
  proposal, statement of work or change request. Do not activate before a use
  case and its measure are chosen (adk-discovery), for a decision deck,
  rollout pack or value report (adk-presenter), for a new feature in an
  application whose design is already accepted (adk-engineer), or for a
  focused memory, workflow, frontend or deployment change (use that
  specialist directly).
license: MIT
metadata:
  author: Ruslan Khissamiyev
  source-book: Agentic Engineering
  verified-against: "not applicable: writes designs and plans; runs no ADK code"
  version: "2026.10.28"
---

# ADK system designer

Turn a product idea or an existing architecture into a reviewable system design
through a conversation. Turn requirements into contracts, explore the
decisions that enforce them, and connect each contract to an enforcement point
and the evidence that it holds. Scale the design to the requested problem.

The deliverable is an architecture and a resumable implementation plan. It needs
no other skills, starter repository or cloud access.
When the user also requests implementation, finish the relevant design decisions
and continue within that existing authorization using available specialist guidance.

## Establish what is known

Read the request, supplied material and relevant project instructions. For an
existing application, inspect its architecture notes, manifests, entrypoints,
interfaces and tests without importing application code or exposing secrets.
Preserve agreed requirements, the product's domain, working infrastructure and
dependency pins. A service already present is a constraint to evaluate, not an
automatic choice for every new responsibility.

If a discovery brief exists (by default `docs/discovery/<topic>.md`, written
by `adk-discovery`), read it first. It supplies the chosen first use case, the
outcome measure and its baseline, the hypothesis chain, the stakeholders and
their decision dates, the technology-fit decision and the constraints known so
far. Treat its confirmed answers as answered and ask only what it leaves open.
Do not reopen the opportunity ranking or the use-case choice; if the design
finds the chosen use case infeasible or its measure unobservable, say exactly
what was found and offer the prompt to return to `adk-discovery` with it. When
the request is itself a discovery question (where AI should go, which workflow
first, whether an agent is even the right tool), it belongs to `adk-discovery`;
say so and give that prompt instead of designing around an unchosen use case.

Summarize one concrete user journey, its current friction, intended outcome and
fixed constraints in a few sentences. Keep that journey as the running example
when explaining components and failures. Distinguish observed facts, user
decisions, proposals and unknowns.
For a supplied design, begin with its consequential gaps instead of repeating
an introductory interview. For a narrowly scoped design question, resolve that
question without producing a whole-application document.

## Conduct the design conversation

Ask the next question that could change the architecture, explaining which
decision depends on the answer. Usually ask one to three related questions per
turn, with concrete options when useful. Use the host's question interface if
available; ordinary chat works too.
Let the user answer before treating a material product choice as settled.

Open with the scope gate: the questions whose answers set the size of
everything that follows. Real people build the system inside fixed hours, so
ask about capacity as well as scope. Ask only what the request has not already
answered, in one turn, and offer the default so a user can accept it in one word:

- When must the first useful version exist, and is it continued afterwards?
  (Default: no deadline; continued.)
- Who builds it: how many people, how many hours each, how familiar with ADK
  and GCP? (Default: one developer, part time, new to ADK.)
- How much money is there for models and cloud? (Default: a small allowance.)
- Who uses or judges it and what will they read: a demo, predictions, a
  report, colleagues using it daily, external customers? (Default: the user,
  reading the design.)
- Does it need its own web interface, who can reach its URL, and will other
  developers continue it? (Default: `adk web` for the builder only; not
  handed over.)
- What data does it touch and what can it change? (Default: synthetic data,
  read only.)
- Which reviews need a presentation, for whom, and when: a go-ahead before
  the proof of concept is built, a review of what it did that decides on
  production, and a results review after the production build? (Default:
  all three for a business audience, dates to be confirmed; technical
  versions when whoever hosts or depends on it, including an external IT firm,
  must read the design.) A discovery brief's decision calendar answers this.
  Each review becomes a presentation goal at that phase boundary, owned by
  `adk-presenter`, and a ticket when tickets are written.
- Is it built for a client under a contract, needing a proposal or statement
  of work? (Default: no.) When yes, the statement of work is a goal written
  from this design and plan.
- Is vendor lock-in a concern: moving to AWS or Azure, replacing the agent framework,
  or keeping chosen components modular? (Default: no.) Ask whether, not which provider.
  When yes, the design stays GCP + ADK; the plan gains an `adk-portability-planning` goal.

When the user overrides one of these defaults and `adk-engineer` is installed,
record it as an `overridden-default` field note (its field-feedback reference);
offer to share only when the helper reports the same override recorded before.

If the engineer keeps a practice profile, offer its org defaults in place of
these defaults, labelled with their source, as
[practice profile](references/practice-profile.md) describes; accepted values
go into the scope-gate or assumed-answers table with that label. Its data
classes and AI policy set the data-and-effects default and can raise the
floor; its jurisdictions feed residency; its procurement lead times become
calendar waits in the plan.

Read [delivery profiles](references/delivery-profiles.md) to turn the answers
into a profile (proof of concept, quality-judged assignment, internal tool, MVP
or pilot, production), the depth of each concern, the floor kept at every
profile, a capacity check and a phased plan. State the profile in one line and
let the user correct it. The data and effects answers set the risk whatever the
label: "just a POC, don't worry about security" lowers the depth of controls,
never the floor, so propose the cheapest design that keeps the floor (drafts a
human sends, staging targets, sample data) and record what the user accepts.

Record the answers at the top of the design document, with the depth per
concern and the controls deferred, each with the trigger that brings it
forward. Size the documents to the profile: a proof of concept or a four-hour
assignment gets one file in the compact form of
[delivery profiles](references/delivery-profiles.md#compact-form-for-short-work),
about 1,200 words, that a reviewer reads in ten minutes. Larger profiles
follow [write each fact once](references/delivery-profiles.md#write-each-fact-once-at-the-depth-it-is-known):
a one-page summary first, each fact in one place referred to by ID, detail
that follows certainty, and waste cut before substance. In a production design, fill
each template section that applies and mark the others not applicable in one
line.

Estimate each goal and ticket in human hours for a developer working with a
coding agent (hands-on plus review and verify, with calendar waits listed
separately). Check phase 1 against the team's capacity with a reserve, and
cut scope rather than the floor when it does not fit. Compute totals, loads
and the finish range with `scripts/check_schedule.py` rather than by hand,
except in a one-person compact form, where quarter-hour estimates are added
by hand and no schedule block is written. Show
the user the cut line between what ships now and what comes later, and ask
them to confirm or move it. Write the later phases into the same plan so the
work can continue when the team has time, without a new design conversation.

Every design reads [design decisions](references/design-decisions.md) for the
sections its journey touches and [failure review](references/failure-review.md)
before it is called ready. Read the other references only when their trigger
below applies; a small design rarely needs all of them. Then work
from the journey towards the constraints, as needed:

- What may the system read, decide and change, and for whom?
- What would a correct completed result be? Which outcomes are unacceptable?
- What should improve over the current journey, and how will we measure it?
- What already exists: login, authoritative records, frontend, storage, platform?
- What traffic, latency, cost, retention, availability and recovery targets matter?

When the artifact is judged on output quality, apply the proportionality rule
in [design decisions](references/design-decisions.md#size-the-first-slice-to-the-judge):
the first slice is the core judgment end to end on real inputs, measured,
with only the controls that keep spend safe.

Avoid turning these into an upfront questionnaire. Infer repository facts by
inspection. Offer a reasoned default for reversible choices. When the user does
not know a target, show how it affects the design and propose a labelled assumption
or a measurement task. A numeric requirement, provider guarantee or user
approval enters the design only from the user, a cited source or a labelled
assumption. If asked for a one-pass draft, proceed with explicit assumptions
and open decisions instead of requiring an interview.
When the user cannot answer (a one-pass draft, a headless run, or no reply),
keep asking nothing further: put an **Assumed answers** table at the top of the
design, one row per question with the assumed answer and the decisions that
depend on it, and mark those decisions provisional.

Explain each consequential recommendation through:

**Requirement → contract → design choice → reason → tradeoff → verification → evidence.**

- **Requirement:** the user need or constraint behind the journey, with its confirmed or assumed status.
- **Contract:** the observable promise that satisfies it (see below); one requirement may yield several.
- **Design choice:** the specific component responsibility or interaction that enforces the contract.
- **Reason:** how that choice keeps the contract, given the known provider guarantees.
- **Tradeoff:** the cost, limitation or capability forgone compared with a credible alternative.
- **Verification:** an observable check and expected result, planned until it runs.
- **Evidence:** the check's actual result and tier, recorded against the contract later; name what is still unproven.

Use a few sentences or a compact row; the chain guides the explanation, not seven
mandatory headings on every turn. Keep the rationale visible while asking useful
questions. Read the opening example in [design decisions](references/design-decisions.md)
when a concrete illustration would help.

After an answer, summarize what changed in the requirement, contract, choice and
verification, then address the next unresolved decision. Maintain the cumulative
decision record without repeating the whole design. A user correction can
supersede an earlier proposal; revise the contracts it changes and update their
dependent choices and checks. Compare only credible alternatives, including ordinary code or one agent when sufficient. Additional
agents need a distinct responsibility, context, tool set or evaluation reason;
a security boundary comes from separate credentials, tools and state.

## Turn requirements into contracts

A **contract** is a precise, observable promise the system keeps, derived from a
requirement. "Customers can escalate a case" is a requirement; "one confirmed
escalation produces at most one external ticket" is a contract. Keep the word
for this meaning: what a provider promises is a *provider guarantee*, and what
the model reads is its *interface*.

Number requirements `R1`, contracts `C1` and decisions `D1`; each contract
names the requirement it serves and each decision the contracts it enforces.
Write each critical contract with six fields:

- **Invariant:** what must always or never hold, stated so a test can fail it.
- **Scope:** for whom and over what: user, tenant or account, data, time window.
- **Authority:** the authoritative source of the facts it depends on, never
  the model or the conversation.
- **Enforcement:** the trusted component that checks it, and where it is
  checked again at the effect when time passes between check and effect
  (after a confirmation, a wait or a retry). Enforcement can stop or refuse
  the violation; an alert, log or dashboard only observes it and belongs
  under evidence. If nothing can stop it, the contract is a gap.
- **Failure outcome:** what the user sees and what state remains when it
  cannot be kept.
- **Evidence:** the planned check and its tier (offline, local, live,
  release), later its actual result; or an explicit gap.

Decompose a vague requirement until each contract has one enforcement point:
"advertisers can purchase" becomes quote, confirmation, purchase-operation and
status contracts. A contract with no mechanism behind it is a gap, recorded as
one, not a guarantee. Size the set to the profile: a read-only assistant needs
a few (identity, retrieval scope, grounded answers, failure); money,
publishing or messages to real people add rights, confirmation, inventory,
idempotency and recovery contracts; an MVP or production profile adds a cost
contract whose enforcement is a stop, not a budget alert (see the budgets
section of [design decisions](references/design-decisions.md#latency-capacity-budgets-and-operations)).

The contracts table is where each promise is stated once. Decisions, goals
and failure rows cite its ID instead of restating the invariant, so the table
replaces prose rather than adding to it.

Contracts evolve. When a discovery tightens one (asset rights turn out to
depend on brand, channel, territory, dates and modification), revise it in
place with a one-line note and list the decisions, goals and tests it changes.

Read [design decisions](references/design-decisions.md#decompose-a-requirement-into-contracts)
for a worked decomposition and when translating the journey into outcome, data,
identity, effect and budget contracts. Select its relevant topics; account
briefly for omitted concerns instead of adding unused memory stores, agents or
infrastructure. Capture the cross-boundary consequences:

- Session, invocation and business-operation identities have different lifetimes.
- Model proposals, user confirmation and backend authorization are separate.
- Partial output, persisted conversation state and external effects have separate
  completion rules. A timeout or cancellation can leave a write uncertain.
- Recovering interrupted work needs a durable operation record beyond the
  stored conversation.
- Screening happens before storage, tool execution and streaming, because
  each of those is already an exposure.
- Model/tool fan-out and nested retries consume the same application allowance.
- What the model sees is its only interface: instruction, sub-agent descriptions,
  tool declarations and output schema each have an owner and a test;
  what the application already knows belongs in code, not the prompt.
- A remote peer's message, a server-supplied tool description or a tool result
  is data, never authority or an instruction. An agent that reads untrusted
  content and can write or send needs a structural split, not a warning sentence.
- Model, judge and prompt versions are release artefacts with lifecycle dates;
  they roll forward and back together with the image, tool schema and secrets.

Read [runtime and delivery](references/runtime-and-delivery.md) when requirements
depend on context limits, result downloads, browser streams, concurrent sessions,
capacity or continuity during a release. It adds the contracts that hold
between storage, execution and the user's visible result.

## Select ADK and GCP components for those responsibilities

Use [GCP decisions](references/gcp-decisions.md) when selecting services or
estimating capacity and cost. Before naming a resource that charges while
provisioned, read its row in the [resource cost ledger](references/resource-costs.md):
the goal that creates it records the idle cost, the cleanup command and the
verification, and the plan says which goal ends its life. Separate application hosting from model inference,
conversation storage, business records, artifacts and identity. Record which
component owns retries, authorization, shared state and recovery.

Check version-dependent ADK interfaces against the target's installed/deployed
versions and current official documentation. For a greenfield design with no
installed version, record the ADK version the specialists were checked against
(each specialist's `references/compatibility.md` names it) as the working
assumption, and make "confirm against the chosen pin" an acceptance item of the
first implementation goal. Choose model and judge IDs from the dated lifecycle
table that `adk-model-and-output-contracts` ships
(`assets/model-lifecycle-*.json`, a JSON object with `checked_on` and a
`models` map keyed by model ID giving status and retirement dates) rather
than from memory; a model that retires within the plan's horizon is a migration you are
designing in, not a default. Check service availability, regions,
limits and prices before relying on them; cite sources and dates in the design.
If lookup or credentials are unavailable, keep those decisions provisional and
name the exact verification needed. Architecture planning can proceed without
provisioning or installing an SDK. Examples from the source material are teaching
evidence; this application's versions and deployment supply their own.

## Make the recommendation implementable

For each consequential choice, add a short implementation route: the ADK building
block or ordinary application component, its concrete integration point, the GCP
responsibility if needed, and the primary specialist that can implement it. Read
[implementation handoff](references/implementation-handoff.md) for the mapping
and plan format. Distinguish inspected paths and supported APIs from proposed
modules and version checks still needed. Explain where enforcement lives. For
example, "tenant scope is derived from the verified OIDC subject in the request
middleware and passed to the retrieval tool as trusted context" is a route; a
service name or a list of skills is a pointer to one. Seven cross-framework
specialists (instructions, tool interfaces, model and output contracts,
security, observability, release engineering, interoperability) sit beside the
topic specialists; the handoff mapping names which one owns each route. When
a route needs a Google Cloud product provisioned, queried or administered,
the goal also names Google's product skill as `google/skills:<name>` in its
supporting skills (the handoff lists them); the design records that need and
never runs the recipe.

When the design gives the agent its own web interface or an HTTP API, read
[web application defaults](references/web-app-defaults.md) for the default
stack, layout and companion skills, and record each deviation as a decision.
Then read [the security baseline](references/security-baseline.md), list the
components the design creates and record each rule's depth and status once in
the design.

Bring this detail into the conversation as choices become clear. Use a small
interface sketch or pseudocode only when it resolves an integration question;
keep unverified code labelled and preserve a design-only request. A feasibility
gap becomes a bounded investigation with an expected decision and a stopping
condition.

## Review the design through requests and failures

Read [failure review](references/failure-review.md) before calling a cross-cutting
design ready for implementation. Build its coverage grid from the list of
external systems, so every failure type for every integration is either
handled or marked not applicable, rather than recalled. Trace a successful request and applicable failure
paths across the actual components. Explain the visible result, retained state,
possible external effects, permitted next action and recovery owner.

Revise a mechanism until it enforces its contract. Record unresolved decisions
with their impact and who or what can settle them. A significant unknown can
block a particular implementation step while independent work remains possible.
Present the trade-offs to the user; a diagram or an unanswered proposal does not
mean the architecture has been agreed.

## Deliver and hand off

Before handing over a plan for several people or a production service, have
it reviewed by someone who did not write it. Send the
[independent plan review](assets/plan-review-prompt.md) to a subagent with a
fresh context where the host supports one; otherwise give the user the prompt
to run in a new session, and say the plan is unreviewed until they do. Settle
every finding in the plan or its change table, and rerun the schedule check.
A single-person proof of concept skips this; a one-pass draft hands over
unreviewed, says so, and gives the prompt.

When revising an existing design or plan, compare it with the previous
version and list every failure row, grid cell, test, acceptance case, wait
and floor item you removed or weakened, each with its reason, in the plan's
change table. Nothing of these leaves silently.

When the user asks for a proposal, statement of work, change request or the
letter requesting client data and access, read
[engagement scoping](references/engagement-scoping.md): it builds them from the
brief, design and plan, and `scripts/check_sow.py` checks them against the
schedule block.

Keep the design and build plan in the project's existing document convention.
When none exists, use `docs/architecture/<topic>.md` and, for a multi-goal effort,
`docs/plans/<topic>.md`. In the compact form the design file holds the plan
and no separate plan file is written; tickets link to the design. Use chat
if requested. Adapt the [design template](assets/system-design-template.md) and
[implementation plan](assets/implementation-plan-template.md); link decisions
instead of duplicating them, and split ADRs only where useful.

Include the recommendation, meaningful alternatives, component/sequence diagrams
when useful, critical contracts, workload and budget assumptions, recovery and
verification plans, and unresolved decisions. Mark the document **draft** while
material assumptions remain unsettled; distinguish user-accepted decisions from
your recommendations. Design review is complete when each critical contract has
an enforcement point and a planned check cited by a goal, or an explicit
unresolved gap, and the user can assess the next step. Implementation and test
evidence come later, from the goals' own recorded runs, written against the
contract IDs they prove.

Finish with dependency-ordered goals for useful end-to-end behavior, grouped into
phases: phase 1 fits the stated capacity, phase 2 graduates or hardens the result,
and a later list holds deferred items with their triggers. Write them from the
[implementation plan](assets/implementation-plan-template.md): its "Goals and
dependencies" section says where the presentation, journey, teardown, statement
of work, rollout and operations handover goals sit, with their primary skills
and acceptance, and its goal entry lists every field a goal carries (a web
component goal adds companion skills, design system and security rule IDs).
Read that section before writing the first goal.

When the scope gate records personal data, decisions about people (hiring, credit,
education, access to services) or a regulated domain, or the profile is MVP, pilot
or production, add a **governance goal**, type governance, `Primary skill:
adk-governance-pack`, placed before the production-approval presentation goal,
which depends on it. It drafts the papers the client's counsel, DPO and security
reviewers sign (a jurisdiction screen across Australian, US, EU, UK, New Zealand,
Singapore and Canadian law, form answers for a NSW or Commonwealth agency, a
regulatory memo, privacy impact inputs, impact assessment, system card, processing
records, questionnaire answers), sized by that skill to the profile; a proof of
concept on real personal data gets its one-page note inside phase 1 instead. Its
acceptance is the skill's checker passing on the drafts; the DPIA sign-off and
legal review are calendar waits (`W<n>`) requested when the drafts go out, and the
production goals depend on them.

When the scope gate records a lock-in concern, add a **portability goal**, type
portability, `Primary skill: adk-portability-planning`, that depends only on the
design and blocks no build goal; when the answer was no, no portability goal,
ticket or skill load happens ([details](references/implementation-handoff.md#plan-a-portability-goal-when-the-scope-gate-asks-for-one)).

Separate discovery questions from ready implementation; an unknown cloud guarantee need
not block independent local work. When the user wants tickets, write one file
per goal of the phase from the [ticket template](assets/ticket-template.md) under
`docs/tickets/<topic>/`, with sibling dependencies in `blocked_by`; the plan
stays the source of decisions. Then run `python3 "$SKILL_DIR/scripts/check_tickets.py" --tickets
docs/tickets/<topic>` from the project root and fix every error before
handing over: it catches unfilled placeholders, contract and rule IDs the
design lacks, acceptance items that prove nothing, skills that are not
installed, broken `pass_to_pass` references and `parallel_safe` tickets that
write the same file, and warns when one ticket names more skills and
references than its session should load.

End the conversation with a short closing message in chat: where the documents
were saved, the profile and the cut line (what phase 1 delivers in how many of
the available hours, and what waits), the decisions still open, and the exact
prompt for the next ready goal in a copyable block. For a web application,
also say which security rules are deferred and what raises them. For example:

```text
/adk-engineer Carry out G01 from docs/plans/<topic>.md.
```

The user should never have to work out what to type next. When the next
ready goal is a presentation, the prompt names `adk-presenter` and the plan
path instead. With a practice profile, offer its harvest
([practice profile](references/practice-profile.md), step 5) after the prompt.

`adk-engineer` carries out a goal or ticket with its named specialist without
restarting architecture discovery. When a ticket's evidence needs a design
decision, it sends the user back here with a checkpoint prompt. If the user has chosen another planning
workflow (for example Matt Pocock's skills), the handoff reference explains how
to adapt the plan to it; otherwise skip that section.

Preserve any workflow already chosen, including Agents CLI or another design
method. Do not scaffold applications, change dependencies, implement code or run
cloud commands merely because an architecture names them. Local design work does
not authorize deployments, IAM changes, paid tests, migrations or deletion.
For separately requested external work, make targets and effects concrete and
reuse authorization already given for that scope.

## Checkpoint a plan in progress

A checkpoint folds what the build learned back into the design, so the
remaining tickets still serve the contracts. Run it when asked
("Checkpoint <plan>"), when `adk-engineer` ends with that prompt, or before a
review goal, and read [checkpoint](references/checkpoint.md) first: it starts
from `scripts/plan_status.py`, whose CHECKPOINT lines are the agenda to settle
with the user (contract deltas, rulings, a phase that no longer fits, blocked
tickets, orphaned contracts), and it covers the phase gate before a review and
the weekly status update.

Independent community project; not affiliated with or endorsed by Google.
