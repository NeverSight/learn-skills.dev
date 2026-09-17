---
name: wayfinder
description: Plan a huge chunk of work — more than one agent session can hold — as a shared map of decision tickets in a local directory, and resolve them one at a time until the way to the destination is clear.
disable-model-invocation: true
---

A loose idea has arrived — too big for one agent session, and wrapped in fog: the way from here to the **destination** isn't visible yet. Wayfinding is about finding that way, not charging at the destination. This skill charts the way as a **shared map** of markdown files in the repo, then works its **decision tickets** — questions whose resolution is a decision, not slices of a build to execute — one at a time until the route is clear.

The destination varies per effort, and naming it is the first act of charting — it shapes every ticket. It might be a spec to hand off and iterate on, a decision to lock before planning starts, or a change made in place like a data-structure migration. The map is domain-agnostic — engineering work, course content, whatever fits the shape.

## Plan, don't do

Wayfinder is **planning** by default: each ticket resolves a decision, and the map is done when the way is clear — nothing left to decide before someone goes and does the thing. The pull to just do the work is usually the signal you've reached the edge of the map and it's time to hand off. An effort can override this in its **Notes** — carrying execution into the map itself — but absent that, produce decisions, not deliverables.

## Refer by name

Every ticket is a file whose name is a readable phrase, not a number. In everything the human reads — narration, the map's Decisions-so-far — refer to a ticket by that name, never by a bare path or slug fragment. A wall of paths is illegible; names read at a glance.

## The Map

One effort is **one directory**, at `docs/wayfinder/<effort-slug>/`:

```
docs/wayfinder/<effort-slug>/
  map.md                         # the canonical artifact — the effort at low resolution
  tickets/
    push-or-email.md             # unresolved: named, unnumbered
  resolved/
    01-notification-types.md     # NN- is the position in the route walked
    02-sms-channel.md
```

**A ticket is numbered when it resolves, never when it is created.** In `tickets/` there is no order to record — a charting session writes several at once and which gets worked first isn't decided yet. `NN-` is assigned on filing, so `ls resolved/` reads as the route actually walked, in the order it was walked.

Both indexes share one sequence, because the number is a position in time rather than a slot in a category. A gap in **Decisions so far** is not a missing entry; it's the moment something was ruled out of scope instead.

`NN-` is not part of a ticket's identity. `Blocked by:` names the bare stem — `notification-types`, never `01-notification-types` — so a reference written at charting time stays correct after filing renames the file.

The map is an **index**, not a store. It lists the decisions made and points at the tickets that hold their detail; a decision lives in exactly one place — its ticket — so the map never restates it, only gists it and links.

**The map holds only what can't be derived.** A ticket's state is its file's location, and its dependencies are in its body, so which tickets are takeable is *computed from the directory*, never written into `map.md`. A derived value that gets stored is a cache, and a stale frontier is a future session confidently working a ticket whose premise isn't settled yet.

### The frontier

A ticket is **unblocked** when every ticket blocking it has moved to `resolved/`. The **frontier** is the unresolved, unblocked, unclaimed tickets — the edge of the known, and the answer to "what can I pick up right now".

Derive it, never read it off the map:

```bash
python3 skills/bam-mode/wayfinder/scripts/frontier.py <effort-slug>
```

Because state is location, **resolving a ticket is one move**, and every ticket it blocked becomes takeable with no second edit. Nothing to update means nothing to forget.

File a ticket with `--resolve`, which allocates the next `NN-`, moves the file, and syncs the map in one step:

```bash
python3 skills/bam-mode/wayfinder/scripts/frontier.py <effort-slug> --resolve <ticket>
```

It refuses to file a ticket holding neither `## Answer` nor `## Out of scope`, since that would produce a resolved ticket recording nothing.

### The session checkpoint

The frontier script runs at the start of every session, which makes it the one guaranteed moment to catch a resolution that was left half-finished — the real risk here, since filing happens at the end of a long session when context is most depleted.

It does not prevent forgetting in the session that did the work. It makes the **next** session unable to miss it. Integrity sections print **before** FRONTIER, each with a `→` line naming the fix, so an agent that skims the top of the output hits the leftover instead of the next takeable ticket.

| Section | What it means | Fix |
| --- | --- | --- |
| NEEDS FILING | a ticket has `## Answer` or `## Out of scope` but is still in `tickets/` — recorded, yet still on the frontier | `--resolve <ticket>` |
| UNRECORDED | a ticket in `resolved/` with neither `## Answer` nor `## Out of scope` — moved by hand without recording which it was | record it |
| UNNUMBERED | a ticket in `resolved/` with no `NN-` prefix, so it has no position in the route | renumber it |
| DUPLICATE NUMBERS | two resolved tickets claiming one position | renumber the later one |
| MAP OUT OF SYNC | `map.md`'s generated indexes disagree with `resolved/` | `--sync-map` |
| DANGLING BLOCKERS | a `Blocked by:` naming no ticket — so whether it's blocked is *unknown*, which is why it never appears in FRONTIER | fix the name |

UNNUMBERED and DUPLICATE NUMBERS only appear when a file was moved by hand instead of with `--resolve`, which allocates the number itself.

That is why **the answer is written before the move**: if a session dies mid-resolution, what's lost is the filing command, not the session's thinking. A ticket that already holds `## Answer` leaves FRONTIER immediately (it is NEEDS FILING, not takeable), so the next session cannot redo it.

CLAIMED prints as its own count next to FRONTIER for the same reason — a stale claim from a dead session is visible every run instead of silently shrinking what looks takeable.

### The map body

The whole map at low resolution, loaded once per session. Unresolved tickets are **not** listed — they live in `tickets/`, found by the frontier script.

```markdown
## Destination

<what reaching the end of this map looks like — the spec, decision, or change this effort is finding its way to. One or two lines; every session orients to it before choosing a ticket.>

## Notes

<domain; skills every session should consult; standing preferences for this effort>

## Not yet specified

<!-- see "Fog of war": in-scope fog you can't ticket yet; graduates as the frontier advances. Thin here means unexplored, never settled. -->

## Decisions so far

<!-- generated by frontier.py --sync-map; do not hand-edit -->
<!-- /generated -->

## Out of scope

<!-- generated by frontier.py --sync-map; do not hand-edit -->
<!-- /generated -->
```

**The last two sections are generated, never hand-written.** Each is an index of `resolved/`: the link and its position come from the filename, and the one-line gist comes from the ticket's own `Gist:` line. Both already exist at resolution time, so writing the index by hand copies information that is already on disk — and a copy is a step to forget. `--sync-map` rebuilds both blocks by sorting on the `NN-` prefix, so even the ordering is derived and there is nothing left for the map to hold stale.

So the hand-written map is exactly **Destination, Notes, and Not yet specified** — three sections with no derivable source. "The map holds only what can't be derived" is literal, not aspirational.

**Not yet specified** sits above **Decisions so far** on purpose. A tidy document with headings invites completeness, and the fog is the section a reader is most tempted to quietly fill in to make the map look finished. It ranks above the settled work because an unexplored question outranks a resolved one in what the next session needs to see.

### Tickets

Each ticket is one file in `tickets/`, named as a readable phrase — `notification-types.md`, not `ticket-3.md`. That stem **is** its identity, so it is what other tickets reference, and it survives the `NN-` prefix added on filing. Sized to one 100K token agent session:

```markdown
## Question

<the decision or investigation this ticket resolves>

Type: research | prototype | grilling | task
Blocked by: <ticket names, comma-separated, or none>
Claimed: <who is working it, or none>
```

`Type:` is one of the four in [Ticket Types](#ticket-types). `Blocked by:` names other tickets by stem, comma-separated, and is written once at creation — it never needs maintaining, because what changes is the blocker's *location*, not the dependency.

`Claimed:` is set **first**, before any work, so concurrent sessions skip the ticket. It is the one stored field here, so it can go stale — a dead session leaves a claim behind. The frontier script therefore always prints CLAIMED as its own count next to FRONTIER: a claim that has gone stale is visible on every run rather than silently shrinking what looks takeable. Clear it by hand when that happens.

The answer isn't part of the body — it's appended on resolution as an `## Answer` section whose first line is `Gist: <one line>`, the compressed form that carries into the map's index:

```markdown
## Answer

Gist: four types — mention, reply, digest, security

<the reasoning, at whatever length the decision needs>
```

Assets created while resolving a ticket are linked from it by relative path, not pasted in.

Local files need no create-then-wire pass: you choose the names, so a ticket can reference a blocker written in the same breath.

## Ticket Types

Every ticket is either **HITL** — human in the loop, worked _with_ a human who speaks for themselves — or **AFK**, driven by the agent alone. A HITL ticket only resolves through that live exchange; the agent never stands in for the human's side of it (a grilling agent that answers its own questions has broken this).

- **Research** (AFK): Reading documentation, third-party APIs, or local resources like knowledge bases to surface a fact a decision waits on. Resolved by a subagent that calls the Skill tool with "research". Use when knowledge outside the current working directory is required.
- **Prototype** (HITL): Raise the fidelity of the discussion by making a cheap, rough, concrete artifact to react to — an outline, a rough take, a stub, or UI/logic code, by calling the Skill tool with "prototype". Links the prototype as an asset. Use when "how should it look" or "how should it behave" is the key question.
- **Grilling** (HITL): Conversation. The default case. Always call the Skill tool twice, for "grilling" and "domain-modeling".
- **Task** (HITL or AFK): Manual work that must happen before a _decision_ can be made — nothing to decide, prototype, or research, but the discussion is blocked until it's done. Signing up for a service so its API can be judged, provisioning access, moving data so its shape can be seen. This is the one type that _does_ rather than decides — and it earns its place by unblocking a decision, not by delivering the destination. The agent drives it alone where it can (AFK); otherwise it hands the human a precise checklist (HITL). Resolved when the work is done; the answer records what was done and any resulting facts (credentials location, new URLs, row counts) later tickets depend on.

## Fog of war

The map is _deliberately_ incomplete: don't chart what you can't yet see. Beyond the live tickets lies the **fog of war** — the dim view of decisions and investigations you can tell are coming but can't yet pin down, because they hang on questions still open. Resolving a ticket clears the fog ahead of it, graduating whatever's now specifiable into fresh tickets — one at a time, until the way to the destination is clear and no tickets remain.

The map's **Not yet specified** section is where that dim view is written down: the suspected question, the area to revisit later. It's the undiscovered frontier _toward_ the destination — everything here is in scope, just not sharp enough to ticket. Write as loosely or as fully as the view allows; it doubles as a signpost for collaborators reading where the effort is headed.

**Fog or ticket?** The test is whether you can state the question precisely now — _not_ whether you can answer it now.

- **Ticket when** the question is already sharp — even if it's blocked and you can't act on it yet.
- **Not yet specified when** you can't yet phrase it that sharply. Don't pre-slice the fog into ticket-sized pieces: it's coarser than a ticket, and one patch may graduate into several tickets, or none, once the frontier reaches it.

**Not yet specified** excludes what's already decided (Decisions so far), what's already a live ticket, and what's out of scope (the next section).

## Out of scope

Fog only ever gathers _toward_ the destination. The destination fixes the scope, so work beyond it is **out of scope** — it isn't fog, and it doesn't belong in **Not yet specified**. It gets its own **Out of scope** section on the map: work you've consciously ruled out of _this_ effort. Scope, not sharpness, lands it here.

Out-of-scope work never graduates — the frontier stops at the destination — so it returns only if the destination is redrawn, and then as a fresh effort, not a resumption.

Ruling something out of scope is a scoping act, not a step on the route. When a ticket that already exists turns out to sit past the destination — mis-scoped in while charting, or exposed by a resolution — give it an `## Out of scope` section in place of an `## Answer`, again with a `Gist:` line saying why, and file it with `--resolve` like any other. `resolved/` means "off the frontier", not "answered"; the section heading says which it was, and the sync routes it to the map's **Out of scope** index instead of **Decisions so far**.

It still takes a number, because it happened at a point in time and the two indexes share one sequence. What it doesn't take is a place in **Decisions so far** — that section records the route actually walked, and a scope boundary isn't a step on it.

## Invocation

Two modes. Either way, **never resolve more than one ticket per session** — with the exception of research tickets.

### Chart the map

User invokes with a loose idea.

1. **Name the destination.** Call the Skill tool twice, for "grilling" and "domain-modeling", to pin down what this map is finding its way to — the spec, decision, or change. The destination fixes the scope, so it's settled first.
2. **Map the frontier.** Grill again, **breadth-first** this time: fan out across the whole space rather than deep on any one thread, surfacing the open decisions and the first steps takeable now. **If this surfaces no fog** — the way to the destination is already clear, the whole journey small enough for one session — you don't need a map. Stop and ask the user how they'd like to proceed.
3. **Create the directory** — `docs/wayfinder/<effort-slug>/` with `tickets/` and `resolved/` — and write `map.md`: Destination and Notes filled in, the fog sketched into **Not yet specified**, Decisions-so-far and Out-of-scope empty.
4. **Write the tickets you can specify now**, each with its `Blocked by:` filled in as you go. Everything you can't yet specify stays in the fog — the **Not yet specified** section.
5. **Run the frontier script** to check your work: no dangling blockers, and a frontier that isn't empty. An empty frontier at charting time means everything is blocked on something unwritten.
   ```bash
   python3 skills/bam-mode/wayfinder/scripts/frontier.py <effort-slug>
   ```
6. **Fire the research subagents.** For each `research` ticket you just wrote, spin up a subagent that calls the Skill tool with "research" to resolve it in parallel.
7. Stop — charting is one session's work; it hand-resolves nothing else.

### Work through the map

User invokes with a map (effort slug or directory). A ticket is **optional** — without one, you pick the next decision, not the user.

1. **Run the frontier script**, then load `map.md` — the low-res view, not every ticket body. If anything prints above FRONTIER, it is an integrity problem: clear it before taking a new ticket. A previous session left a resolution half-filed, and finishing it costs `--resolve` (or `--sync-map`) where redoing the ticket costs a session.
2. Choose the ticket. If the user named one, use it. Otherwise take the first ticket in FRONTIER. **Claim it**: set `Claimed:` before any work.
3. Resolve it — **zoom as needed**: read the full body of any related or resolved ticket on demand; call the Skill tool for whichever skills the `## Notes` block names. If in doubt, call the Skill tool twice, for "grilling" and "domain-modeling".
4. Record the resolution, **in this order**: append `## Answer` with its `Gist:` line to the ticket, then file it. Answer first, so that an interrupted session loses a file move rather than the thinking — and `--resolve` refuses a ticket with nothing recorded, which enforces that order.
   ```bash
   python3 skills/bam-mode/wayfinder/scripts/frontier.py <effort-slug> --resolve <ticket>
   ```
5. Add newly-surfaced tickets; graduate any fog the answer has made specifiable, clearing each graduated patch from **Not yet specified** so it lives only as its new ticket. If the answer reveals a ticket — this one or another — sits beyond the destination, **rule it out of scope** rather than resolving it on the route. If the decision invalidates other parts of the map, update or delete those tickets.

The user may run unblocked tickets in parallel, so expect other sessions to be editing the directory concurrently. In one working tree a claim is visible immediately; across clones it is visible only once pushed.
