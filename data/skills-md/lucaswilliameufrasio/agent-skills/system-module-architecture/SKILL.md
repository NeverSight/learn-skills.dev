---
name: system-module-architecture
description: >-
  Plan and build complete software systems in any domain or context, including
  customer-facing products, internal tools, web, mobile, and APIs. Use before
  starting a system, feature area, workflow, or major expansion—not only for
  architecture reviews. Start from users, jobs, and end-to-end journeys; derive
  screens, modules, contracts, and implementation slices from them. Prevent
  all-in-one screens and page-first architecture.
---

# Build systems from journeys and capabilities

This applies to complete products and systems of any size: customer-facing apps,
internal tools, APIs, mobile apps, and systems without a graphical interface.
Build around what each user or system actor needs to accomplish, not a list of
screens or a collection of CRUD endpoints. Do the product and workflow
structure before implementing. Respect existing domain language, API contracts,
and architecture decisions; do not silently replace them.

## Before implementation: map the system

For a new system, major feature area, or cross-module workflow, first produce a
concise plan covering:

1. **Actors and responsibilities** — who or what interacts with the system,
   what each actor may do, and which goals belong to each actor.
2. **Jobs and journeys** — each important task from its entry point through
   completion, including decisions, alternate paths, failures, and recovery.
3. **States and lifecycle** — the meaningful domain states, allowed transitions,
   who can cause them, and what must be recorded.
4. **Capability/module map** — the cohesive domain responsibilities and their
   ownership, lifecycle, dependencies, and failure modes.
5. **Interaction and information architecture** — navigation, routes, screens,
   API operations, or other interfaces, with a clear primary intent for each.
   When there is a UI, do not make one page responsible for unrelated jobs.
6. **Contracts and data ownership** — commands, queries, APIs, persistence,
   authorization, validation, integrations, and side effects.
7. **Implementation slices** — a vertical, testable build order that delivers
   complete user journeys instead of disconnected UI shells.

Read existing product/domain documentation and decisions first. If a material
choice is unresolved, show the alternatives and ask the user before locking the
architecture. Do not block routine implementation on questions whose answer is
already documented or can safely follow established conventions.

## Design journeys before screens

For each important user or system journey, identify:

- the actor, goal, permissions or authorization, and starting context;
- the steps and decisions the actor takes;
- data viewed or changed and the source of truth;
- success, empty/loading where applicable, validation, authorization-denied,
  and failure states;
- long-running, retry, cancellation, and recovery behavior where relevant;
- completion evidence, audit needs, and the next useful action.

Then choose the interface and route structure appropriate to the system. Split
journeys when intent, risk, permission, frequency, lifecycle, or completion
state differs. Related steps may share an interface when that makes the task
clearer; do not force every step into a separate page either. Avoid defaulting
to a giant dashboard or a CRUD table as the whole system design.

When asked to build an oversized “one screen for everything” or an equivalent
catch-all interface, do not implement it literally. Explain the competing jobs,
propose a journey-based structure, and proceed with the smallest coherent set of
flows. Ask for confirmation only when the split changes a meaningful product
decision.

## Module boundaries

A module owns a cohesive capability and should make its key responsibilities
discoverable:

- domain entities and lifecycle;
- commands and queries;
- states and transitions;
- authorization and ownership;
- dependencies and external contracts;
- failure modes, retries, and side effects.

A capability may span multiple screens or endpoints. Keep UI composition,
workflow coordination, domain rules, persistence, and integration adapters
separate where their responsibilities and change lifecycles differ. Do not
treat a folder, tab, or large component as a domain boundary by itself.

## Separate journeys by intent and risk

Use distinct flows when user intent, permission, risk, frequency, or completion
state differs. Typical examples include:

- overview/status versus search and collection management;
- read-only inspection versus creation/editing;
- routine operations versus configuration/policy changes;
- reversible actions versus destructive or irreversible actions;
- short interactions versus long-running work and progress;
- operational activity versus audit, diagnostics, and support.

Do not place destructive maintenance beside routine actions or bury important
configuration inside an unrelated operational screen. Do not solve wrong
journey topology merely by extracting more components, adding tabs, or splitting
one oversized page into smaller components that still share the same unclear
responsibility.

## Contracts and integrations

- Model APIs as named domain commands and queries, not generic forwarding
  proxies for arbitrary methods, paths, headers, or request bodies.
- Give each integration a named client and explicit operations, typed request
  and response models, validation, authorization, timeout, and safe error
  mapping.
- Parse external data at the boundary and map it into domain types before it
  enters business logic.
- Load configuration through named, typed contracts rather than arbitrary
  runtime key lookup.
- Validate long-running or destructive commands with authorization,
  idempotency where appropriate, explicit confirmation, and progress/final
  state.

## Review checklist

- Were user roles, jobs, end-to-end journeys, and lifecycle states mapped before
  screen implementation?
- Does navigation reflect distinct goals instead of exposing one page that does
  everything?
- Does each flow cover empty, loading, validation, permission, success, and
  failure states as applicable?
- Is the implementation sequenced as complete, testable journeys?
- Can each module be described as one coherent capability?
- Is ownership of state, permissions, and failure behavior clear?
- Does every route or screen have one primary intent?
- Are configuration, maintenance, and destructive actions separated from
  routine operation?
- Are integrations explicit and validated at their boundaries?
- Can a new contributor locate the contract and the source of truth for state?
