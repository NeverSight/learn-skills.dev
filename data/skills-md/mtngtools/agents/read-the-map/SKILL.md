---
name: read-the-map
description: Read one wayfinder map — its body, its children, its frontier — and say where the effort stands and which door to enter next.
argument-hint: "The map (number or URL), if the session doesn't make it obvious"
metadata:
  type: command
  invocation: skill-callable
  applies-to: [planning, wayfinder, github, maps]
---

# Read The Map

Where does **this** map stand, and what comes next on it? This skill answers that for one map, and it owns [the checklist](#the-checklist) for what reading a map means — everything else that needs a map read, `/whats-next` and `/check-wayfinder-maps` included, follows this list rather than inventing its own.

**This skill never writes.** No claims, no comments, no closes, no map edits. It reads and reports. If the reading turns up work, hand it to `/wayfinder`, `/decisions-to-specs`, or `/specs-to-tickets`.

## Tracker conventions

Read the repo's issue-tracker doc (`docs/agents/issue-tracker.md`), specifically its **Wayfinding operations** section, for how *this* repo expresses maps, child tickets, and blocking. This is a per-repo lookup, not a per-map one. Defaults, where the doc is silent:

- **Map** — an issue labelled `wayfinder:map`
- **Child ticket** — a GitHub sub-issue of the map, labelled `wayfinder:<type>`
- **Blocking** — GitHub native issue dependencies; fall back to a `Blocked by: #n` line in the body
- **Claimed** — the ticket has an assignee

## The checklist

Everything below happens for the map in hand. Items 2 and 3 come from **list-level data** — title, state, labels, assignee, dependencies — which a tracker returns without opening anything; item 1 is the one body you always read.

1. **The map body, whole.** `Destination`, `Notes` (deferral pegs, execution overrides, skills this effort consults), `Decisions so far`, `Specs settled`, `Not yet specified`, `Out of scope`. The readiness signal lives here, not in the ticket counts — a map with zero open children can still be unstarted fog.
2. **Its children's state** — open or closed, `wayfinder:<type>`, assignee, and what blocks what.
3. **The build backlog** — open non-wayfinder issues from `/specs-to-tickets`, and whether any are merged. Readiness depends on whether the specs have been sliced yet.
4. **The frontier** — the open, unblocked, unclaimed children. That set is what a next session can actually take.
5. **The verdict** — exactly one, from [the table](#verdicts).
6. **The next move** — one door, from [the mapping](#verdict--next-move).

A map's own `Notes` outrank your inference. "Ready for tickets" written on the map is the author's judgment; report it as theirs, and contradict it only if the fog visibly says otherwise.

## Verdicts

Two questions, in order: **are the decisions done?** then **are the specs sliced into build tickets?**

| Verdict | When |
|---|---|
| **Yes — already sliced** | No open decisions, specs settled, implementation tickets exist |
| **Yes — not yet sliced** | No open decisions, specs settled, no build tickets yet |
| **Yes, with caveats** | Sliced, but tickets carry revision notes or a later decision invalidated them |
| **No — needs charting** | Stub map, or fog no ticket covers yet |
| **No — blocked on #n** | Waiting on another map's output |
| **No — deliberately deferred** | The map's `Notes` peg it to a future event; leave it alone |
| **Done** | Everything closed, sliced, and merged |

## Verdict → next move

| Verdict | Door |
|---|---|
| open frontier tickets to take | `take #<n> — <title>` — the one that unblocks the most, or the quickest |
| No open decisions, specs not settled | `/decisions-to-specs` |
| Yes — not yet sliced | `/specs-to-tickets` |
| Yes — already sliced | `/implement #<n> — <title>` |
| Sliced, but a ticket's shape is still a guess | `/prototype #<n> — <title>` — when asked for, or when trying it in experimental beats arguing it into stable |
| No — needs charting | `/wayfinder` on the fog |
| Blocked or deferred | nothing here; name what it waits on |
| Done | the map is finished — the next move is a different map |

## Zooming

Ticket **bodies** are not on the checklist. Open one only when:

- the map's `Notes` point at it as needing revision and you can't tell why, or
- two frontier tickets are live and their titles don't settle which is the better next take.

Everything else the checklist needs is list-level.

## Output

Short. The verdict, the next move as one line, the frontier by name, and anything on the map that contradicts them. Refer to every map and ticket **by name**, linked — never a bare `#42`. No table for one map; prose is shorter.

## Where this sits in the flow

The read that other skills stand on. `/whats-next` turns this skill's next move into a prompt. `/check-wayfinder-maps` runs [the checklist](#the-checklist) against every open map at once — it must cover every item, but it is free to satisfy them with **bulk tracker queries** rather than a pass per map, which is the efficient shape at ten maps and pointless at one.
