---
name: wayfinder
description: Map an uncertain project as decisions in a main Jira checklist or GitHub Issues until implementation is clear.
disable-model-invocation: true
---

# Wayfinder

Use Wayfinder when a loose idea is too large or uncertain for one agent session.
It charts the way to a **destination** as a shared map of **decision tickets**:
questions whose resolution clarifies the route, not implementation slices that deliver
the destination. In Jira, each decision ticket means a numbered checklist item in
the main map ticket; do not create subtickets. In GitHub, each is a separate Issue.

Wayfinder plans by default. Hand off to `to-spec` and `to-tickets` when the route is
clear. These decisions clarify the plan; the slices produced by `to-tickets` deliver it.

Resolve every `.agents/projects/` path from the opened workspace root, including
when the active repository is nested inside it. In a single-repository workspace,
that is the repository root. Keep this artifact root fixed when changing directories;
never use nested repositories or global agent-installation directories for artifacts.

## The Map

The active project's map lives at `.agents/projects/<project>/wayfinder.md` and is published
to the selected issue tracker as the shared tracker map with the `wayfinder:map`
label. Its decision-ticket drafts live at
`.agents/projects/<project>/wayfinder-ticket-drafts.md`. The local and tracker maps carry the
same content; update both after each resolved decision.

In Jira, keep the decision checklist and each item's question, type, blockers, owner,
and resolution in the main map ticket. Use stable item numbers; check an item when
its decision or blocking task is completed. In GitHub, the map is an index and each
resolution lives in its decision Issue. Refer to work by its linked title and include
the checklist item number when several decisions share the main Jira URL.

```md
# Wayfinder: <destination>

## Destination

<What reaching the end of this map looks like.>

## Notes

<Domain, required skills, and standing preferences.>

## Decisions So Far

- [<closed ticket title>](link) - <one-line gist of the answer>

## Decisions

<Jira: numbered checklist with item details. GitHub: links to decision Issues.>

## Not Yet Specified

<In-scope questions that are visible but not yet precise enough to ticket.>

## Out Of Scope

<Work consciously ruled beyond this destination.>
```

## Ticket Types

Each decision ticket has one type and is sized for one fresh agent session:

- **Research**: an agent investigates documentation, third-party APIs, or local
  sources to surface a fact a decision needs.
- **Prototype**: a user evaluates a cheap concrete artifact to decide behavior or
  appearance.
- **Grilling**: the user and agent resolve a decision through `grilling` and
  `domain-modeling`.
- **Task**: a blocking action such as provisioning access or preparing data; it exists
  only to unblock a later decision.

In Jira, prefix each item with `wayfinder:<type>` and state its blocking item numbers
or external ticket links. In GitHub, label each Issue `wayfinder:<type>` and use
native parent/child and blocking relationships. A decision is **unblocked** when
all blockers are completed. The **frontier** is the set of incomplete, unblocked,
unclaimed decisions.

## Chart The Map

1. Identify the active project and read its context, links, ADRs, and existing
   planning artifacts. Resolve the tracker from project context: Jira by default,
   GitHub Issues only when Jira is unavailable or the user explicitly selects GitHub.

   Done when the project facts, tracker, and existing constraints are known.

2. Use `grilling` and `domain-modeling` to name the destination. Then map the first
   frontier breadth-first: surface the decisions currently precise enough to state and
   capture the rest as fog. If there is no fog and the work fits one session, stop and
   recommend the smaller planning flow instead.

   Done when the destination, initial frontier, and in-scope fog are distinct.

3. Draft the local map and proposed decision tickets. Each draft names its question,
   type, blockers, and expected resolution. Keep a question in **Not Yet Specified**
   when it cannot yet be stated precisely; do not pre-slice fog into tickets. Put work
   outside the destination in **Out Of Scope**, never in fog.

   Done when `.agents/projects/<project>/wayfinder.md` and
   `.agents/projects/<project>/wayfinder-ticket-drafts.md` describe the map and initial
   decision tickets.

4. Show the map and decision drafts to the user. Do not publish them until the user
   explicitly approves the draft. In Jira, update the approved existing main ticket
   or create one main map ticket containing the decision checklist and item details.
   In GitHub, create the map first, then its decision Issues, then wire blocking edges.
   If authenticated tooling is unavailable, produce ready-to-paste tracker bodies
   and record the limitation in project context.

   Done when the approved map and every initial decision have tracker links and Jira
   item numbers where applicable, or ready-to-paste equivalents are recorded.

5. Update `CONTEXT.md` and `LINKS.md` with the map URL, tracker choice, ticket links,
   Jira item numbers, and current frontier. Start research tickets in parallel where
   tooling permits; charting itself resolves no decision tickets.

   Done when the map is published, project artifacts point to it, and the session has
   stopped before hand-resolving a ticket.

## Work Through The Map

Resolve no more than one non-research ticket per session.

1. Load the map. Use a decision supplied by the user, or select the first on the
   frontier. In Jira, read and record the owner beside the selected checklist item;
   in GitHub, load and claim its Issue. Claim the decision before beginning so
   concurrent sessions skip it.

   Done when one unblocked decision ticket is claimed.

2. Resolve the question using its ticket type. Fetch related ticket detail only when
   needed. Use `grilling` and `domain-modeling` for a Grilling ticket. A HITL ticket
   only resolves through the user; do not answer the user's side yourself.

   Done when the ticket's decision or blocking task has a concrete outcome.

3. In Jira, invoke `update-ticket` to check the completed item in the main ticket;
   this completion mark needs no further approval. In GitHub, close the decision
   Issue. Draft the resolution comment and any other description edits for approval:
   put the resolution beside the Jira item or in its GitHub Issue and add a linked
   one-line gist to the map's **Decisions So Far**. Post only approved edits, ending
   comments with `Written by AI Agent`. Mirror the published outcome locally; keep any
   pending description or comment updates identified until approved and posted.

   Done when the Jira checklist item is checked or the GitHub Issue is closed, and
   the resolution, map index, and local mirror agree; pending tracker updates and
   access limitations are explicitly recorded.

4. Graduate newly precise fog into fresh decision-ticket drafts. Obtain approval
   before adding Jira checklist items or creating GitHub Issues, then publish their
   details and blockers. For work beyond the destination, remove its Jira checklist
   item from active work or close its GitHub Issue, recording a linked reason under
   **Out Of Scope**. Include changed or invalidated Jira item details in the proposed
   description update for approval.

   Done when the frontier and fog accurately reflect what the resolved decision made
   visible.

5. When no unresolved decision remains between the map and the destination, record
   that the route is clear and hand off to `to-spec`, then `to-tickets`. Do not begin
   implementation in Wayfinder.

   Done when the user has a clear next planning handoff or the map identifies the next
   unresolved frontier ticket.

## Done when

- The approved map accounts for every decision, blocker, and remaining question.
- Jira decisions are checklist items in the main ticket, with no new subtickets;
  GitHub decisions have separate Issue links.
- Completed Jira decisions have checked items, or exact pending updates and tracker
  access limitations are recorded.
- Project artifacts mirror published decisions and identify pending tracker edits.
- The next decision or planning handoff is clear, and implementation has not begun.
