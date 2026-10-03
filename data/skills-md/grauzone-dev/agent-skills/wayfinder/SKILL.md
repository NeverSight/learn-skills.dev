---
name: wayfinder
description: Plan a huge chunk of work - more than one agent session can hold - as a shared map of decision tickets on your issue tracker, and resolve them one at a time until the way to the destination is clear. Use when an initiative is too large to plan in one session or when working a ticket on an existing Wayfinder map.
license: MIT
disable-model-invocation: true
metadata:
  author: "Sascha Grau"
  version: "1.0.0"
  category: "engineering"
---

# Wayfinder

A loose idea has arrived - too big for one agent session, and wrapped in fog: the way from here to the **destination** isn't visible yet. Wayfinding is about finding that way, not charging at the destination. This skill charts the way as a **shared map** on the repo's issue tracker, then works its **decision tickets** - questions whose resolution is a decision, not slices of a build to execute - one at a time until the route is clear.

The destination varies per effort, and naming it is the first act of charting - it shapes every ticket. It might be a spec to hand off and iterate on, a decision to lock before planning starts, or a change made in place like a data-structure migration. The map is domain-agnostic - engineering work, course content, whatever fits the shape.

## Plan, don't do

Wayfinder is **planning** by default: each ticket resolves a decision, and the map is done when the way is clear - nothing left to decide before someone goes and does the thing. The pull to just do the work is usually the signal you've reached the edge of the map and it's time to hand off. An effort can override this in its **Notes** - carrying execution into the map itself - but absent that, produce decisions, not deliverables.

## Refer by name

Every map and ticket is an issue, so it has a **name** - its title. In everything the human reads - narration, the map's Decisions-so-far - refer to it by that name, never by a bare id, number, or slug. A wall of `#42, #43, #44` is illegible; names read at a glance. The id and URL don't vanish - a name wraps its link - but they ride _inside_ the name, never stand in for it.

## The map

The map is a single issue on this repo's issue tracker, labelled `wayfinder:map` - the canonical artifact. Its tickets are child issues of the map.

The map is an **index**, not a store. It lists the decisions made and points at the tickets that hold their detail; a decision lives in exactly one place - its ticket - so the map records only a one-line gist and link, never the detail.

**Where the map, its child tickets, blocking, membership query, and frontier ordering physically live is tracker-specific.** Before creating or working a map, load `docs/agents/issue-tracker.md` and consult its **Wayfinding operations**. If that document does not exist, run the `setup-software-engineering-skills` skill first; it establishes the tracker contract that this skill consumes.

### The map body

The whole map at low resolution, loaded once per session. Open tickets are **not** listed - they are open child issues, found by query.

```markdown
## Destination

<what reaching the end of this map looks like - the spec, decision, or change this effort is finding its way to. One or two lines; every session orients to it before choosing a ticket.>

## Notes

<domain; skills every session should consult; standing preferences for this effort>

## Decisions so far

<!-- the index - one line per closed ticket: enough to judge relevance, then zoom the link for the detail the ticket holds -->

- [<closed ticket title>](link) - <one-line gist of the answer>

## Not yet specified

<!-- see "Fog of war": in-scope fog you can't ticket yet; graduates as the frontier advances -->

## Out of scope

<!-- see "Out of scope": work ruled beyond the destination; closed, never graduates -->
```

### Tickets

Each ticket is a **child issue** of the map; where the tracker lacks a native child relationship, the configured tracker contract defines the equivalent membership marker and query. The tracker's issue id is its identity. Put every tracker-required membership and frontier-order field in the body or description first, using the contract's exact syntax and placement. The remaining canonical body is the question, sized to one 100K token agent session:

```markdown
## Question

<the decision or investigation this ticket resolves>
```

Each ticket carries a `wayfinder:<type>` label - one of `research`, `prototype`, `grilling`, `task` (see [Ticket types](#ticket-types)). The tracker contract defines the authoritative order for the frontier; assign it when creating the ticket, in breadth-first discovery order.

A session **claims** a ticket by assigning it to the dev driving the map, **first**, before any work, so concurrent sessions skip it. That assignee _is_ the claim: an open, unassigned ticket is unclaimed. The session that dispatches a research subagent claims that research ticket before dispatch and owns its later tracker writes.

Blocking uses the tracker's **native** dependency relationship - essential because it renders the frontier _visually_ in the tracker's own UI, so the human sees what's takeable without opening the map. Only a tracker that lacks native blocking falls back to a body convention. A ticket is **unblocked** when every ticket blocking it is closed; the **frontier** is the open, unblocked, unclaimed children - the edge of the known.

The answer isn't part of the body - it's recorded on resolution (see [Work through the map](#work-through-the-map)). Assets created while resolving a ticket are linked from the issue, not pasted in.

## Ticket types

Every ticket is either **HITL** - human in the loop, worked _with_ a human who speaks for themselves - or **AFK**, driven by the agent alone. A HITL ticket only resolves through that live exchange; the agent never stands in for the human's side of it (a grilling agent that answers its own questions has broken this).

- **Research** (AFK): Source-backed investigation that surfaces a fact a decision waits on. Use when evidence outside the current session is required. A **subagent** running the `research` skill investigates and writes the cited finding; the session that dispatched it records that finding as the ticket's resolution. The `research` skill owns source selection and the finding's evidence contract.
- **Prototype** (HITL): Raise the fidelity of the discussion by making a cheap, rough, concrete artifact to react to - an outline, a rough take, a stub, or UI/logic code via the `prototype` skill. Links the prototype as an asset. Use when "how should it look" or "how should it behave" is the key question.
- **Grilling** (HITL): Conversation. The default case. Always invoke the `grilling` and `domain-modeling` skills.
- **Task** (HITL or AFK): Manual work that must happen before a _decision_ can be made - nothing to decide, prototype, or research, but the discussion is blocked until it's done. Signing up for a service so its API can be judged, provisioning access, moving data so its shape can be seen. This is the one type that _does_ rather than decides - and it earns its place by unblocking a decision, not by delivering the destination. The agent drives it alone where it can (AFK); otherwise it hands the human a precise checklist (HITL). Resolved when the work is done; the answer records what was done and any resulting facts (credentials location, new URLs, row counts) later tickets depend on.

## Fog of war

The map is _deliberately_ incomplete: don't chart what you can't yet see. Beyond the live tickets lies the **fog of war** - the dim view of decisions and investigations you can tell are coming but can't yet pin down, because they hang on questions still open. Resolving a ticket clears the fog ahead of it, graduating whatever's now specifiable into fresh tickets - one at a time, until the way to the destination is clear and no tickets remain.

The map's **Not yet specified** section is where that dim view is written down: the suspected question, the area to revisit later. It's the undiscovered frontier _toward_ the destination - everything here is in scope, just not sharp enough to ticket. Write as loosely or as fully as the view allows; it doubles as a signpost for collaborators reading where the effort is headed.

**Fog or ticket?** The test is whether you can state the question precisely now - _not_ whether you can answer it now.

- **Ticket when** the question is already sharp - even if it's blocked and you can't act on it yet.
- **Not yet specified when** you can't yet phrase it that sharply. Don't pre-slice the fog into ticket-sized pieces: it's coarser than a ticket, and one patch may graduate into several tickets, or none, once the frontier reaches it.

**Not yet specified** excludes what's already decided (Decisions so far), what's already a live ticket, and what's out of scope (the next section).

## Out of scope

Fog only ever gathers _toward_ the destination. The destination fixes the scope, so work beyond it is **out of scope** - it isn't fog, and it doesn't belong in **Not yet specified**. It gets its own **Out of scope** section on the map: work you've consciously ruled out of _this_ effort. Scope, not sharpness, lands it here.

Out-of-scope work never graduates - the frontier stops at the destination - so it returns only if the destination is redrawn, and then as a fresh effort, not a resumption.

Ruling something out of scope is a scoping act, not a step on the route. When a ticket that already exists turns out to sit past the destination - mis-scoped in while charting, or exposed by a resolution - **close it** (a closed ticket is unambiguously off the frontier) and leave one line in the **Out of scope** section: the gist plus why it's out of scope, linking the closed ticket. It stays out of **Decisions so far**, which records the route actually walked - a scope boundary isn't a step on it.

## Invocation

Two modes. Either way, **never resolve more than one ticket per session** - with the exception of research tickets.

### Chart the map

User invokes with a loose idea.

1. **Name the destination.** Run a `grilling` and `domain-modeling` session to pin down what this map is finding its way to - the spec, decision, or change. The destination fixes the scope, so it's settled first.
2. **Map the frontier.** Grill again, **breadth-first** this time: fan out across the whole space rather than deep on any one thread, surfacing the open decisions and the first steps takeable now. **If this surfaces no fog** - the way to the destination is already clear, the whole journey small enough for one session - you don't need a map. Stop and ask the user how they'd like to proceed.
3. **Create the map** (label `wayfinder:map`): Destination and Notes filled in, Decisions-so-far empty, the fog sketched into **Not yet specified**.
4. **Create the tickets you can specify now** as child issues of the map, assigning their tracker-defined order in breadth-first discovery order - then wire blocking edges in a **second pass** (issues need ids before they can reference each other). Wiring sorts them into the frontier and the blocked; everything you can't yet specify stays in the fog - the **Not yet specified** section.
5. **Dispatch research.** For each `research` ticket, claim it first, then spin up a `research` subagent with the map and ticket references. It returns one cited finding artifact. The charting session records that artifact's link in a resolution comment, closes the ticket, and appends the one-line pointer to **Decisions so far**. Research tickets are the exception to the one-ticket session limit.
6. Stop - charting is one session's work; apart from the dispatched research tickets, it hand-resolves nothing.

**Complete when:** the map records its destination, notes, current fog, and no decisions; every currently specifiable ticket has its configured membership, order, type, and blocking relationship; each research ticket has been claimed and dispatched or resolved; and no non-research ticket has been resolved.

### Work through the map

User invokes with a map (URL or number). A ticket is **optional** - without one, you pick the next decision, not the user.

1. Load the **map** - the low-res view, not every ticket body.
2. Choose the ticket. If the user named one, use it. Otherwise take the first frontier ticket in the configured tracker order. **Claim it**: assign it to yourself before any work.
3. Resolve it - **zoom as needed**: fetch the full body of any related or closed ticket on demand; invoke the skills the `## Notes` block names. A research ticket is claimed, dispatched to a `research` subagent, and then resolved by this session when its cited finding returns. If in doubt, use the `grilling` and `domain-modeling` skills.
4. Record the resolution: post the answer as a **resolution comment**, **close** the issue, and **append a context pointer** to the map's Decisions-so-far.
5. Add newly-surfaced tickets (create-then-wire); graduate any fog the answer has made specifiable, clearing each graduated patch from **Not yet specified** so it lives only as its new ticket. If the answer reveals a ticket - this one or another - sits beyond the destination, **rule it out of scope** rather than resolving it on the route. If the decision invalidates other parts of the map, update or delete those tickets.

The user may run unblocked tickets in parallel, so expect other sessions to be editing the tracker concurrently.

**Complete when:** exactly one claimed non-research ticket has a resolution, required tracker state, and map index entry; every newly specifiable decision has a correctly wired ticket or remains in fog; and the map's out-of-scope and invalidated work reflects the resolution.
