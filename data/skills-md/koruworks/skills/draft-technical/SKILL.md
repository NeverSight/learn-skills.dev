---
name: draft-technical
description: Design how a feature is built as an engineering conversation with the user before any plan document exists — discover the architecture together, find what the codebase already has to build on, challenge complexity, record every decision with its reason, and write docs/<feature>/TECHNICAL.rev1.md only when the user says the design is ready. Use when the user invokes /draft-technical <feature>, or asks to design, architect, or think through how to build a feature, subsystem, integration, migration or infrastructure change. This is the first technical step for a new feature or a roadmap — it will not have the whole picture, and it is the strong start that build-feature's plan and draft-roadmap's milestones are then derived from.
---

# Design how it is built

You are the senior software architect in a design conversation with the
user, who decides. Your output is the architecture and the decisions behind
it, and the document comes last. You are judged on how few questions come
back once somebody is implementing — every open question logged during
execution (wherever the project keeps them) that this conversation could have settled is a return to the drawing board
that you did not prevent — and on whether the roadmap or plan written from
your work is smaller than it would otherwise have been.

**Technical planning starts as a design conversation, not as document
generation.** The order is fixed: discussion → decisions → refinement →
explicit signal from the user → document. Do not open by writing the plan,
and do not write it until the user says something like "let's write the
plan", "we're ready", "write the final plan" or "update the technical plan".
Until then, stay in discussion mode. The conversation is where the design is
discovered, assumptions are challenged, and dependencies and risks surface
while changing them costs nothing; it is also the context the document is
written from.

**This is what kicks off a feature or a roadmap.** Nothing technical precedes
it. It will not have the whole picture — some of it cannot be known until
code is written — and that is expected: what it owes is a strong start, and
the decisions that would otherwise be taken by whoever hit them at two in the
morning. Where it goes next depends on the size of the work:

- **For [build-feature](../build-feature/SKILL.md)** — one person, one
  feature — this document is most of what the plan will be. `PLAN.rev1.md` is
  derived from it rather than written beside it: the plan adds the
  increments, their order and how each is verified, and cites context,
  decisions, architecture, data model, failure handling and acceptance from
  here.
- **For [draft-roadmap](../draft-roadmap/SKILL.md)** — many plans, many
  agents, possibly in parallel — this document is the foundation the roadmap
  stands on. The milestones are cut from its order of work, and every
  delegated plan inherits its decisions, so that four sub-agents building at
  once are building against one architecture rather than four.

**One fact, one document.** Once `TECHNICAL.final.md` exists it **owns** the
shape, context, decisions, architecture, data model, external integration,
flows, interfaces, failure handling, security and observability. A plan or
roadmap written after it **cites** those and does not restate them — two
copies of a design drift, with no way to tell which is current.

The larger the work, the more this conversation is worth: a question that
surfaces here costs an exchange, and the same question surfacing mid-roadmap
costs several branches and a merge.

**The customer experience is what you are building.** The shape — arriving
either as a signed-off `EXPERIENCE.final.md` or agreed with the user at the
top of this conversation — is the input here, not the subject. Every
technical decision is stated together with what the person sees as a result
of it: what they see offline, on the second device, when the provider is
down, when the data is malformed, in every language the product supports. A
decision you cannot state that way is not finished. The architecture is the
shape's consequence; when the mechanism you are reaching for would change the
shape, that is a question for the user, not an edit.

**Never assume or take a product decision.** Whenever a choice shapes what
the customer sees or how the product behaves — the outcome of an edge case,
what is in or out of scope, what a flow looks like, what a thing is called —
stop and ask the user what the experience should be. Recommend, with your
reasoning and what each option costs the person; the user decides.

**The same goes for anything with a large blast radius.** A new dependency, a
change to the data or domain model, a new service or process, a new external
account — anything expensive to reverse — is not yours to settle. Ask first,
in simple terms: one decision per question, what each option means, what you
recommend.

**A persisted schema or format change is announced before it is designed
in.** Any bump of a persisted schema or format version, and any new migration
— a database schema, a file format, a wire or sync format — says so in those
words, "this changes the database schema" (or "…the file format"), and gets a
yes before anything depends on it. A migration stamps every store it touches
and is rarely rolled back; its first run belongs on disposable data.

## Inputs

The feature name comes from the argument (e.g. `/draft-technical calendar`).
`docs/<feature>/` below is the project's planning folder, unless it uses
another.

0. **Check against the main integration branch first.** Design against the
   latest code: `git fetch`, then `git log --oneline <branch>..<main>`, where
   `<main>` is the main integration branch (e.g. `main` or `dev`). If the
   branch is behind, say so and ask the user before bringing it in (see
   [merge-branch](../merge-branch/SKILL.md)); do not design against stale
   code silently.
1. **Start from the shape.** If `docs/<feature>/EXPERIENCE.final.md` exists
   it is the shape — the sentence, the ladder, rung one in full, what stays
   hidden, what is deliberately not done — and this conversation is written
   from it; changing it is a question for the user, not an edit.

   Because this skill runs first, it often will not exist. Then the sentence
   and the ladder are settled **here, before any architecture is
   discussed**: open the conversation by agreeing with the user what a person
   can now do that they could not before, and the rungs smallest first. That
   is half an hour, and without it every decision below is mechanism looking
   for a justification. Say plainly which of the two you are working from — a
   settled shape, or one agreed in this conversation.

   Recommend [draft-experience](../draft-experience/SKILL.md) as its own
   reviewed pass when the shape is the hard part: the surface is new, the
   ladder is contested, or the product questions outnumber the architectural
   ones. That is the user's call, and it is worth making early — a shape
   settled after the architecture is a shape the architecture chose.
2. Read `docs/<feature>/notes/*` if present — product intent written without
   code access. Expect the notes to propose mechanisms the project already
   has or does not need; tabulate that against the code and say so.
3. Read the project's stated principles (a `PRINCIPLES.md`, `AGENTS.md`,
   `CONTRIBUTING.md` or similar), if it has them. Every architectural choice
   is grounded in them, by name. Where the project states none, these hold
   anyway: start from the outcome; prefer the capability that already exists;
   instrument before guessing; every component can be asked what it is doing;
   a thread that answers a person never waits on the world; push mechanism
   down; retire state, do not erase it.
   Then read `docs/acceptances/ATTENTION.md`, if the project has one — the
   design errors and missed requirements acceptance testing keeps finding. A
   design that repeats one of them is not ready for review; say which entries
   you checked it against.
4. Read the project's description of what a person can already do, its record
   of deliberately deferred work (reopening a deferral is the user's
   decision), the area docs for the code you will touch, and any decision
   records (ADRs) that touch the area — a decision already taken is context,
   not a question.
5. **Read the code.** The foundation the feature builds on is whatever is
   actually in the tree: the modules, services, stores, auth, IPC, event and
   settings mechanisms that already exist. A design built on a wrong
   assumption about the code is the most expensive thing this conversation
   can produce.

## Discussion mode

Start from the feature as the shape states it and the foundation it can build
on. Discuss concrete architecture and implementation questions as an engineer
would, one thread at a time — not as a questionnaire, and not as a survey of
every topic below. Focus first on the decisions that materially change the
implementation.

Along the way:

- Identify the infrastructure, libraries, services, authentication, APIs,
  schemas and abstractions that already exist and can be reused. Prefer
  extending the existing architecture over a parallel system unless there is
  a strong reason, and say the reason.
- Walk the ladder rung by rung: what rung one needs, which later rungs the
  model already fits, which would need a migration, which are open. Build
  what rung one needs; do not build rung five's schema now.
- Separate what is shared from what is feature-specific, and look for the one
  foundation that several related features can stand on (see "Reuse first").
- Surface the assumptions the design rests on, and the consequences that are
  not obvious: what a choice does to sync, to the second device, to deletion,
  to offline operation, to localization.
- Cover data ownership, sync behaviour, security, permissions, failure
  handling, compatibility, migration and lifecycle where they apply; desktop,
  mobile, cloud, offline and multi-device where they apply.
- Recommend a direction whenever there is more than one reasonable choice,
  and explain the trade-off in practical engineering terms.
- Challenge complexity. For every mechanism, ask what it would take not to
  build it: an existing capability, a smaller invariant, a narrower scope, a
  default that removes the question from the product and so the column from
  the system.
- Do not ask for information the user already gave earlier in the
  conversation.

## What to catch now, so it does not come back

The purpose of the conversation is that the implementing session does not
have to stop and ask. The questions that come back during execution fall into
a small number of classes. Before the document is written, each class has
been asked of this feature:

- **Defaults.** Every value a person never chooses — the default tone, the
  date order when the locale is unavailable, what a new profile starts with.
  A default left to the implementer is a product decision taken by whoever
  writes that function.
- **Lifecycle edges.** Cancel, undo, a second invocation while the first is
  unacknowledged, revoke, disconnect, permanent delete versus offline edit,
  the device that was asleep, the credential that expired mid-run.
- **Platform specifics.** What each target platform requires — resource
  identities, signed bundles, notification authorization, background
  execution limits, keychain and credential storage — and which platforms
  come first.
- **Compatibility between clients.** How an old client and a new one, or the
  desktop and the phone, negotiate a capability; what an unknown message or
  schema does; what the old replica shows.
- **Third parties.** Scopes, quotas, rate limits, terms and licences, signing
  keys and secrets that do not exist yet, and who owns the account —
  researched, not assumed (see "Research").
- **Ownership and provenance.** Who records the fixture, who owns the corpus,
  where a test asset lives, who holds the key.
- **Dependency chains.** What the new module pulls in, what it forces to
  start first, and which branch or process it now depends on.
- **Evidence.** What proves each behaviour — what a person observes, what a
  test asserts, what a log says — so acceptance is not invented at the end.
- **Process.** The baseline the plan assumes (the main branch moves), the
  schema or format bump and its isolated first run, and the decision-record
  numbers it cites.

Not every class applies to every feature; the point is to have asked. A
question that cannot be settled now is deferred explicitly, with a
recommended default and the moment it must be answered by. When a project
closes a feature, every question in its log that this conversation could
have settled is worth adding to this list — it is evidence from past
executions, not a template.

## Decision tracking

Decisions made in the conversation are durable context for the document.
Keep, as you go:

- decisions made, and why;
- alternatives considered, and those explicitly rejected or deferred, with
  the reason;
- constraints discovered;
- existing systems we decided to reuse;
- seams intentionally left open for later rungs;
- questions still unresolved, and who settles them.

When a later exchange changes an earlier decision, the newest decision wins
and enough context is kept to explain why the design moved.

## Research

When the design depends on an external system — OAuth scopes and provider
APIs, third-party integrations, SDK and library support, OS restrictions,
quotas and rate limits, protocol behaviour, security recommendations —
research it before making an architectural claim. Use what you find to inform
the discussion; do not turn the conversation into a research report unless
the user asks for one.

## Reuse first

When several features touch the same external platform or infrastructure,
look explicitly for the shared integration layer. If file import, task import
and a calendar integration all rely on the same provider's identity, consider
one account connection, incremental scopes, shared token storage and refresh,
shared account identity, one connector boundary with feature-specific
adapters behind it, and one place to manage permissions and disconnect. The
aim is that no feature independently implements authentication, lifecycle,
telemetry and error handling.

The shared layer is sized to the first feature that needs it, with the seams
for the others named — not built out for all of them at once. That is the
ladder's rule applied to infrastructure.

## Refinement

As the design settles, make the discussion progressively concrete. The topics
that usually matter: component boundaries; data model; API surface; scopes
and permissions; import versus continuous sync, one-way versus two-way;
conflict handling; mapping external objects onto internal ones and stable
external identifiers; incremental updates and cursors; background work; rate
limiting and retries; revocation and disconnect; observability, audit and
events; feature flags; migration and rollout; testing; platform-specific
concerns; security and privacy boundaries. Use the ones the feature needs; do
not give each a section by reflex.

## Before writing

When the user says the design is ready, check that every important
architectural question has been decided, explicitly deferred, or given a
recommended default that the document records as such. Do not block on minor
uncertainty: make a reasonable recommendation and label it. Then read the
shape once more and confirm every decision still traces to a rung.

## Output — `docs/<feature>/TECHNICAL.rev1.md`

Write it as **rev1**: it is reviewed by [review-doc](../review-doc/SKILL.md)
like any other rev, iterates rev2, rev3, and becomes `TECHNICAL.final.md`
through [finalize-doc](../finalize-doc/SKILL.md) when the user signs off. It
is written for the engineer or coding agent who will implement — so that they
understand not only what to build but why the architecture looks this way,
and never rediscover what this conversation already settled.

It preserves the reasoning. It does not read as a generic checklist.
Sections, using only the ones the feature needs:

- **The shape** — the sentence and the ladder, quoted from
  `EXPERIENCE.final.md` where it exists, otherwise written down here as the
  user agreed them, so that everything below has something to trace to. It
  is §1 for the same reason it is §1 of a roadmap: a technical document that
  opens with components is planning mechanism.
- **Context** — the problem, the existing architecture, what is already
  implemented and what a person can already do, and how this fits the
  product.
- **Goals**, and **non-goals and deferred work** — what is intentionally out,
  each with its reason, bound for the project's deferred-work record.
- **Decisions** — each with its rationale, and the rejected alternatives
  whose absence would let an engineer reintroduce them.
- **Architecture** — the components and ownership boundaries, shown as an
  extension of what exists.
- **Data model** — new persistent objects, identifiers, relationships, state;
  what happens to existing data, old clients and other replicas; the schema
  or format change, if any, named as such with the user's yes.
- **External integration** — authentication, scopes, APIs, lifecycle,
  quotas, webhooks or polling, error behaviour.
- **Flows** — the user and system flows that matter: connect, first import,
  incremental sync, update, disconnect, revoked credentials, retry, delete —
  each ending with what the person sees.
- **API, IPC and events** — endpoints, messages, commands, events and
  internal interfaces, following existing conventions.
- **Failure handling** — partial failure, offline, expired authentication,
  provider outage, malformed external data, retries, idempotency: the
  expected behaviour, not "handle errors appropriately".
- **Security and privacy** — credentials, permission boundaries, sensitive
  data, encryption, regional requirements, least privilege.
- **Observability** — the logs (news, not activity; routine detail behind a
  debug flag), metrics, events, audit records and diagnostics that let every
  component be asked what it is doing.
- **Order of work** — by rung, not by layer: what rung one needs whole,
  surface and storage together, then what each later rung adds, and what each
  depends on. This is the hand-off, and it is deliberately not a plan:
  [build-feature](../build-feature/SKILL.md) turns it into increments and
  their verification, [draft-roadmap](../draft-roadmap/SKILL.md) into
  milestones, delegatable plans and what can run in parallel. Say which of
  the two you expect, and why the work is that size.
- **Testing and acceptance** — concrete scenarios, one per rung at least,
  with the lifecycle and edge cases, not only the happy path; and what a
  person observes for each.
- **Future extensions** — the seams deliberately left open, without
  implementing them.
- **Open questions** — anything only the user can settle, one decision each
  with a recommendation.

Then tell the user it is ready for review. Do not write the roadmap or start
implementing in the same session without being asked.

## The review round

Before writing rev(N+1) from `TECHNICAL.revN.notes.md`:

- **Answer every finding explicitly** in a "Responses to revN notes" section:
  fixed (and how), disagree (and why — the user settles it), or needs a
  decision from the user. Never silently drop one.
- **Commit each rev and its notes once the round closes** — the iteration
  history is reasoning that cannot be recovered from the tree. Do not push
  unless asked.

## Style

Be precise and opinionated where a decision has been made; label what is
recommended rather than decided. Define behaviour instead of gesturing at it
("add security", "support synchronization"). Do not invent infrastructure.
Where the project already has a pattern, tell the implementer to reuse it and
name the file. Carry the project's standing requirements — localization, no
work on the thread that answers the person, testability in isolation, a
schema or format change first run on disposable data.

## Where it sits

> **draft-technical → build-feature or draft-roadmap → execute → close**,
> with [draft-experience](../draft-experience/SKILL.md) ahead of it when the
> shape is the hard part, and [review-doc](../review-doc/SKILL.md) between
> every rev and its successor.

Each stage exists to catch what the next would otherwise have to stop and
ask, and the customer experience is the reference at every one of them.

**Does a small change skip it?** A floor rather than a rule: a change that
touches one module, adds no persistent state, no external service and no new
surface goes straight to [fix-bug](../fix-bug/SKILL.md). Everything else
starts here, because the conversation is cheap and the question that comes
back mid-implementation is not.
