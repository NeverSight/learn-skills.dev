---
name: wayfinder
description: Use to map multi-session work through issue-tracker decision tickets.
disable-model-invocation: true
---

# Wayfinder

Use when the destination is larger than one context window and the route is foggy. A
**decision ticket** resolves a question, not a build slice.

## Plan, don't do

Wayfinder stops when nothing remains to decide.
Notes hold planning preferences and do not authorize implementation or delivery.

## Invariants

- Refer to maps and tickets by **name**, not bare IDs.
- The map is an **index**, not a store. Answers live in tickets; the map keeps a gist and link.
- If `CLAUDE.md` exists, read `CLAUDE.md` first; otherwise read `AGENTS.md`. Follow its
  **Issue tracker** pointer and Wayfinding operations. If absent, use the local-markdown fallback.
- Claim a ticket by assigning it before work; this must be the first write. Open and
  unassigned means unclaimed.
- Prefer native blocking. Use `Blocked by:` only when native dependencies are absent.
- Resolve at most one ticket per session in the primary context; explicit delegation or an
  invoked `/swarm` may parallelize ready research. Otherwise do not resolve another ticket.
- For authorized waves, `/efficient-frontier` budgets lanes and the coordinator synthesizes.
- Audit another session's claims or resolved ticket with `/agent-watchdog`.

## Map shape

Create one issue or file marked `wayfinder:map`:

```markdown
## Destination
<the spec, decision, or change this map must reach>
## Notes
<domain, required skills, standing planning preferences>
## Decisions so far
- [<closed ticket name>](link) -- <one-line answer gist>
## Not yet specified
<in-scope fog not sharp enough to assign>
## Out of scope
<work beyond the destination>
```

Query the tracker for open children; do not copy them into the map body.

## Tickets

Each child is one focused question sized to one 100K-token agent session. Mark it **HITL**
(live human judgment) or **AFK** (agent-driven); HITL and AFK must not be conflated:

- **Research (AFK):** use `/research` against primary sources. Follow its artifact location;
  parallel lanes require consent and each lane does not invent a root file or branch.
- **Prototype (HITL):** create a cheap `/prototype` artifact and link it.
- **Grilling (HITL):** Always invoke `/grilling` and `/domain-modeling`.
- **Task:** manual work that unblocks a decision; never delivery for its own sake.

The answer is not part of the body; record it on resolution. Assets are linked, not pasted.

## Fog and scope

Do not chart what is invisible. Not yet specified excludes anything decided, already a ticket, or out of scope.
A sharp but blocked question is a ticket.
Fog points toward the Destination. Close a ticket discovered beyond it, explain one Out of
scope line, and do not record it as a route decision.

## Chart the map

1. Name the Destination with `/grilling` and `/domain-modeling`.
2. Grill breadth-first for decisions and first steps. **If this surfaces no fog**, stop and
   ask whether to proceed without a map.
3. Create the map, then only currently specifiable tickets.
4. Attach every ticket through the native child/sub-issue relationship when available;
   otherwise link it. Re-read and verify every ticket appears as a child, then add blockers.
5. Resolve one ready Research ticket inline. Authorized lanes claim first, follow `/research`,
   and return cited artifacts.
6. Stop after that ticket.

## Work through a map

1. Read the map at low resolution; select the named or first open, unblocked, unclaimed ticket.
2. Claim first, then resolve it using only relevant related tickets and skills from Notes.
3. Record the answer, resolve the ticket, and append its gist and link to Decisions so far.
4. Add new tickets and blockers; remove graduated fog. Rule beyond-destination work Out of scope.
5. Re-read tracker state before writes because other sessions may edit concurrently.

## Handoff

When clear, send the map to `/to-spec` for one buildable plan, then `/to-tickets`.
Recheck your claims first: reread answers, gists, assets, claims, and current tracker state.
End with one command for the recommended ticket and one per safe parallel frontier ticket.
