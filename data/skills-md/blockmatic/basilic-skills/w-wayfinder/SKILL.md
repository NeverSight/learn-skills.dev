---
name: w-wayfinder
description: Chart multi-session fog as a plan-file map of decision tickets.
disable-model-invocation: true
---

Use when the way to a destination is bigger than one session. Tickets are **decisions**, not build slices. [Clarify](../w-clarify/SKILL.md) is sparse gaps; [grill](../w-grill/SKILL.md) is a design-tree interview; this playbook is fog. When the way is already clear, stop and offer [plan](../w-plan/SKILL.md) or [build](../w-build/SKILL.md). Do not implement on the map. Do not create GitHub issues.

Two modes. Never resolve more than one ticket per work-through session.

### Chart

User invokes with a loose idea.

1. Name the destination with [grill](../w-grill/SKILL.md). The destination fixes scope.
2. Grill again breadth-first for open decisions and first takeable steps. Explore facts via [council](../w-council/SKILL.md). If there is no fog, do not write a map; ask how to proceed.
3. Write the map per [map output](references/map-output.md). Decisions so far empty; fog in Not yet specified; ticket only what is already sharp.
4. List blocking edges on tickets that wait. Research-shaped tickets: council. Look-and-feel: [v0](../w-v0/SKILL.md) or [ui](../w-ui/SKILL.md) as a cheap artifact, not a product UI. Default tickets: grill.
5. Stop. Charting hands off; it does not resolve tickets.

### Work through

User invokes with a map (path or open plan). A ticket is optional.

1. Load the map at low resolution. Orient to Destination.
2. Take the named ticket, else the first frontier ticket. Mark it claimed on the map before any work.
3. Resolve it. Grill for HITL decisions. Council for in-repo or docs facts. Call skills named in Notes.
4. Record the answer on the ticket, gist it under Decisions so far, and close the ticket. Graduate fog that is now sharp. Move mis-scoped tickets to Out of scope.
5. When no tickets and no fog remain, the way is clear. Hand off to [plan](../w-plan/SKILL.md), then [build](../w-build/SKILL.md) if they asked to implement.
