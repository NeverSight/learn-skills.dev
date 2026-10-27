---
name: wayfinder
description: Plan an effort too big for one grilling session as a map of decision tickets on the issue tracker, resolved one per session until nothing is left to decide.
disable-model-invocation: true
---

A loose idea has arrived, too big for one grilling session, and wrapped in fog: the way from here to the **destination** isn't visible yet. Wayfinding is about finding that way, not charging at the destination. This skill charts the way as a **shared map** on the repo's issue tracker, then works its **decision tickets** (questions whose resolution is a decision, not slices of a build) one at a time until the route is clear.

The destination is whatever this effort is finding its way to, and naming it is the first act of charting: it shapes every ticket. It might be a spec to hand off, the architecture a new project starts from, a decision to lock before planning starts, or a change made in place like a data migration. The map is domain-agnostic: any effort whose decisions outgrow one session fits.

## Plan, don't do

Every ticket resolves a decision, and the map is done when nothing is left to decide before someone builds the thing. The pull to just do the work is the signal you've reached the edge of the map: the map produces decisions, and building starts after `/to-spec`.

## Refer by name

Every map and ticket is an issue, so it has a **name**: its title. In everything the user reads (narration, the map's Decisions so far, the questionnaire), refer to it by that name with its link inside, never by a bare id or number.

## The map

The map is a single issue labelled `wayfinder:map`, the canonical artifact; its tickets are its child issues. The "Wayfinding operations" section of the tracker doc says how this repo expresses the map, children, blocking, claims, waiting, and the frontier. The issue tracker should have been provided to you. If not, tell the user to run `/setup-skills`.

The map is an **index**, not a store. A decision lives in exactly one place, its ticket; the map holds only a one-line gist and the link.

### The map body

The whole map at low resolution, loaded once per session. Open tickets are not listed: they are the map's open children, found by query.

```markdown
## Destination

<what reaching the end of this map looks like. One or two lines; every session orients to it before choosing a ticket.>

## Notes

<the domain; skills every session should consult; standing preferences; links to source material such as a requirements document; the open questionnaire, once there is one>

## Decisions so far

<!-- the index: one line per closed ticket, enough to judge relevance, then zoom the link for the detail -->

- [<closed ticket title>](link): <one-line gist of the answer>

## Not yet specified

<!-- the fog: in-scope questions not yet sharp enough to ticket -->

## Out of scope

<!-- work ruled beyond the destination; never graduates -->
```

### Tickets

Each ticket is a child issue of the map. Its body is one question, sized to one 100K-token agent session:

```markdown
## Question

<the decision or investigation this ticket resolves>
```

Each ticket carries one `wayfinder:<type>` label: `research`, `prototype`, `grilling`, or `task`. `wayfinder:` labels are the only labels the map and its tickets carry: they are decisions, and the flow's labels such as `ready-for-agent` mark build work for `/implement`.

A session **claims** a ticket by assigning it to the user driving the map, first, before any other work, so concurrent sessions skip it.

Blocking uses the tracker's native dependency link, so the tracker's own UI shows what's takeable. A ticket is **unblocked** when every ticket blocking it is closed. The **frontier** is the open children that are unblocked, unclaimed, and not waiting on an owner: the edge of the known.

The answer is recorded on resolution, not in the body. Assets created while resolving a ticket are linked from it.

## Ticket types

Every ticket is **HITL** (worked with the user, who speaks for themselves) or **AFK** (driven by the agent alone). A HITL ticket resolves only through that live exchange: the user answers the grill's questions and picks the prototype variant. A grilling agent that answers its own questions has broken this.

- **Grilling** (HITL): conversation, the default. Call the Skill tool for "grilling" and for "domain-modeling".
- **Prototype** (HITL): "how should it look" or "how should it behave" is the question, and talking can't settle it. Raise the fidelity with a cheap, rough, concrete artifact to react to: an outline, a rough take, a stub, or UI or logic code. For UI or logic code, call the Skill tool for "prototype". Link the prototype from the ticket. Its verdict is the ticket's answer; folding it into real code waits for the spec.
- **Research** (AFK): a fact from outside the working directory blocks a decision. Call the Skill tool for "research"; the answer is the finding in a few sentences plus the note's path. Facts inside the repo are found within whichever ticket needs them.
- **Task** (HITL or AFK): manual work a decision is blocked on, with nothing to decide: signing up for a service to judge its API, provisioning access, moving data to see its shape. The agent does it alone where it can; otherwise it hands the user a precise checklist. The answer records what was done and any facts later tickets need (where credentials live, new URLs, row counts). A task earns its place by unblocking a decision. Work that delivers part of the destination is a build slice, and goes to `/to-spec`.

## Decisions someone else owns

A question, or part of one, that is someone else's call (a client, a boss, another team) is **deferred**, as in the grill: record the owner and your recommended answer. In a map, deferred questions collect per map rather than per session:

1. Add the question to the map's **questionnaire**: one per map, filed the way the grill files its questionnaire, with the body from [QUESTIONNAIRE.md](../grilling/QUESTIONNAIRE.md) and each question naming its ticket. Create it with the first deferred question and link it from the map's Notes. Once the user has sent it, later questions start a new one.
2. Mark the ticket as waiting on its owner and release the claim. The frontier skips it; everything not downstream of it carries on.

When the user says the answers are in, record all of them in one session. Post each answer on its ticket and clear the waiting mark. If the answer settles the ticket, resolve it; if decisions remain, it returns to the frontier. An answer that contradicts a closed decision reopens that ticket: name the conflict and put it to the user. Close the questionnaire once every question in it has an answer.

## Fog of war

The map is deliberately incomplete: don't chart what you can't yet see. Beyond the tickets lies the **fog of war**: decisions you can tell are coming but can't yet pin down, because they hang on questions still open. Resolving a ticket clears the fog ahead of it, graduating whatever is now specifiable into fresh tickets, until the way to the destination is clear.

**Not yet specified** is where that dim view is written down: the suspected question, the area to revisit. Everything in it is in scope, just not sharp enough to ticket. Write as loosely or as fully as the view allows; it doubles as a signpost for anyone reading where the effort is headed.

**Fog or ticket?** The test is whether you can state the question precisely now, not whether you can answer it now. A sharp question is a ticket, even if it's blocked. A question you can't yet phrase that sharply stays fog. Write fog in coarse patches and leave the slicing until the frontier reaches it: one patch may graduate into several tickets, or none.

Not yet specified excludes what's already decided, what's already a live ticket, and what's out of scope.

## Out of scope

The destination fixes the scope, so work beyond it is **out of scope**, not fog. It goes in the **Out of scope** section and never graduates; it returns only if the destination is redrawn, as a fresh effort.

When an existing ticket turns out to sit past the destination, close it and leave one line in Out of scope: the gist and why, linking the closed ticket. It stays out of Decisions so far, which records the route actually walked.

## Invocation

Two modes. Either way, resolve at most one ticket per session. Research tickets, and recording a questionnaire's answers, are the exceptions.

### Chart the map

The user invokes with a loose idea, source material, or a conversation that already settled part of it.

1. **Name the destination.** Grill (the Skill tool for "grilling" and "domain-modeling") until the user agrees on it. Size it to what can be planned now: a whole product planned up front goes stale before the frontier reaches its far end.
2. **Map the frontier.** Grill again, **breadth-first** this time: fan out across the whole space rather than deep on any one thread, surfacing the open decisions. If this surfaces no fog (the whole way fits one session), there is no map to draw: stop and suggest `/grill-with-docs`.
3. **Create the map**: Destination and Notes filled in, the fog sketched into Not yet specified, anything ruled out in Out of scope. A decision already settled in the conversation becomes a ticket closed on creation, with the decision as its answer and its line in Decisions so far.
4. **Create the tickets you can phrase now** as children of the map, then wire blocking edges and write cross-references in a **second pass**, with real ids: issues need ids before they can reference each other, and a placeholder `#<n>` auto-links to an unrelated issue. A question already known to be someone else's call goes straight to the questionnaire.
5. **Start research.** Call the Skill tool for "research" on each research ticket, and resolve each as its note lands.
6. Stop. Charting resolves no grilling, prototype, or task ticket.

### Work through the map

The user invokes with a map. A ticket is optional: without one, you pick.

1. Load the map: the low-resolution view, not every ticket body.
2. Choose the ticket the user named, else the first frontier ticket. Claim it.
3. Resolve it as its `wayfinder:<type>` label says; the body never states the type. Hold the session to this ticket's question: a new branch it uncovers becomes a ticket or fog on the map. Zoom as needed: fetch any related or closed ticket, and call the Skill tool for whatever the Notes name. If in doubt, call the Skill tool for "grilling" and "domain-modeling".
4. Record the resolution: post the answer as a comment, close the ticket, and add its line to Decisions so far.
5. Update the map: create newly surfaced tickets (create, then wire); graduate fog the answer made specifiable, clearing it from Not yet specified; rule out of scope any ticket the answer puts past the destination; update or close tickets the decision invalidates.

The user may run unblocked tickets in parallel, so expect other sessions to be editing the tracker concurrently.

### When the map clears

The map clears when no ticket is open and Not yet specified is empty. Propose the specs to the user: one when the destination is a single feature, otherwise one per piece that can be built on its own, such as a module or the first feature. Once the user agrees, each runs as `/to-spec <map> <piece>` in its own session. The map stays open for the user to close.
