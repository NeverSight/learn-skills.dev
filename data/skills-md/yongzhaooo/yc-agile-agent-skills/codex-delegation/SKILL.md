---
name: codex-delegation
description: Brief and route bounded Codex subagents without redundant mode questions. Use before every spawn_agent call, including delegation requested by another skill, for child follow-ups, waiting, and acceptance.
---

# Codex Delegation

## Follow explicit instructions first

A user-specified model and effort for a bounded assignment is sufficient route selection.
Dispatch that assignment without asking for a mode or a complete team configuration.
Honor its count, role and scope; it does not select a mode for later unspecified workers.
A later specific instruction overrides an earlier mode for that assignment only.
Reuse an already selected mode or model combination for covered work until changed.

Use the configured default execution route without a mode question, including sustained
or multi-stage work. The economical long-running route is opt-in: use it only when the
user explicitly selects it or assigns that worker model, and retain its stated scope.
Task duration, simplicity or read-only status alone does not select the economical route.
A task needing no delegation needs no mode.

For an ordinary bounded assignment with no exact route, use the configured task route
and live schema; do not ask for a mode. Ask only when substantive scope, authority,
destructive action, or acceptance is missing. Missing effort uses the configured default
for the specified model; never infer a global mode from that choice.

Use the live `spawn_agent` schema and current routing configuration. Honor an explicit
user-selected route exactly; if unavailable, report the failure rather than substituting
silently. If no configured route fits, keep the work in the main thread; do not add a fallback.
Read `Codex delegation` in the configured global instructions for concrete bindings.
Routing does not
change the main model; do not probe or require a main-model switch unless the user made
that exact setting a prerequisite. Check a required main binding against reliable session
metadata or the user's stated setting; report a mismatch, and distinguish unverified
metadata from a known mismatch. Do not block compatible child routes unless the user
made the exact main binding a prerequisite.
Do not hardcode provider, model, effort, or agent identifiers
in this skill.

## Keep ownership clear

The main Agent owns task scope, acceptance criteria, architecture and public contracts,
persistent data, security, compatibility, destructive or irreversible effects, conflicts
with user work, integration and the final response. Children return evidence and options
when a decision exceeds their assignment.

Only the root dispatches; every child is a leaf, including an expert advisor. Use native
subagents for task-internal work; an explicitly requested external-assistance skill uses
its own route. Neither may spawn further agents or create application tasks. Create an
application task only when the user requests one.

Delegate only when independent work, specialized evidence or protecting the main context
outweighs handoff cost. Keep atomic, serially blocked or duplicate work local. Match the
child count to ready independent work and live limits; parallel writers need disjoint
ownership or isolated workspaces. Do not add extra agents to an explicitly bounded request.
When scratch files are needed, give each writer a private location and name shared runtime
paths that are read-only for it. Before running an unfamiliar script that can delete or
rebuild state, read its body and verify its resolved targets against the assignment.
Mutation of shared state requires explicit write ownership and a matching owner marker
or the project's existing ownership check. Children must preserve other writers' changes.

## Provide a sufficient capsule

Prefer no-history or the smallest useful context fork with a self-contained brief:

Bind the configured model and effort explicitly, or use a deliberately selected role
whose profile owns that binding. Prefer the live explorer role for a specific code
question and worker for bounded production; role choice must not override the route.
Use `fork_turns="all"` only when dispersed conversation state is essential and deliberately
accept the parent model/effort it forces. A smaller fork needs enough context to stand alone.

- **Outcome and context:** exact deliverable/question, why it matters, settled decisions,
  verified findings, relevant attempts, and remaining unknowns.
- **Inputs:** working directory, relevant instructions, source sections/symbols and
  necessary excerpts or accepted upstream evidence; base revision when creating a branch
  or isolated checkout. Distinguish facts from hypotheses.
- **Boundary:** role, allowed reads/writes/commands, non-goals, concurrent owners and
  decisions reserved for the parent. State that further delegation is prohibited.
- **Acceptance:** observable evidence, focused checks, stop conditions and return shape.
  Include the chosen model/effort and required skill; do not assume skill inheritance.

Use a few sentences for a small consultation. The child must be able to start without
reconstructing the parent conversation. Project existing ticket authority faithfully;
a capsule is a message, not a new file, plan or source of authority. See
[dispatch capsules](references/dispatch-capsules.md) for examples and source rationale.

Before dispatch, compare acceptance in the brief with the authoritative requirement or
plan section. Name that source and preserve covered cases, each/all quantifiers,
deadlines and their starting events, failure outcomes, and recovery coverage. Highlight
any proposed omission or weakening; do not silently replace the source with the parent's
summary. The child checks the named source for conflicts before dependent work and returns
the conflict to the parent rather than choosing the easier interpretation. Routine,
equivalent implementation choices remain within the assignment.

Give economical workers one verifiable result within a concrete search/write boundary.
For implementation, settle the approach, interfaces and edge behavior first. Higher
effort cannot supply missing requirements or authorize architecture and unrelated work.
If essential context is missing or evidence conflicts, return `needs_context` before
dependent work, naming the gap, checked evidence and smallest clarification needed.

Give advisors a concrete decision, constraints, relevant system relationships, alternatives
and prior evidence. Ask for a recommendation, counterargument, uncertainty and what would
change the answer. Advice is read-only and leaves decisions with the parent.

Reuse a suitable child for a related follow-up; send changed facts, accepted/rejected
results and the current boundary. For a completed phase with large or stale context,
prefer a fresh child with a compact handoff for the next independent assignment, within
the selected route and count. This does not authorize replacing a failed child.
If a follow-up changes acceptance or execution conditions, identify the affected source
revision or section and update the brief and relevant checks together. Reassess affected
recovery assumptions; a workflow change does not inherit proof from its predecessor.

## Keep long-running work event-driven

Use a background job only when the host provides a durable handle, completion or failure
notification, and a supported way to resume acceptance. Record that handle, output
location and owner in the handoff before the child yields. Otherwise retain a responsible
waiter using the native bounded wait; do not invent a watcher or promise an unsupported
wakeup. Required work remains pending while its background process runs.

Children report a reserved decision, blocker, failure or completed result. Avoid repeated
"still running" messages and acknowledgements that add no evidence. A child-turn completion
notification is not job completion: consult the recorded job state only when acceptance
or intervention needs it. In Codex, `send_message` does not start an idle child;
`followup_task` does. Use the live schema and resume only for actionable work.

For a long assignment that exposed a reusable failure or substantial avoidable cost,
include a short retrospective in its final return: at most five proposals naming the
current skill section, observed incident, proposed wording and expected effect. The child
reads the relevant text and edits nothing. Do not wake a completed child solely for a
routine retrospective. The parent checks whether each proposal generalizes and routes
accepted changes through the skill-authoring workflow within the user's authorization.

## Wait and accept

Briefly announce the route, ownership and expected result; mode is optional, not a required
announcement field. Estimate a return window, not a deadline. Prefer completion events;
with reliable notifications, use zero status polls. Otherwise budget at most three spaced
status reads over that window, unless the user chooses otherwise. Honor manual status
requests and polling overrides. Do independent work, then bounded event waits; timeouts
are not failure and do not justify repeated scans, nudges or duplicate work. On window
or poll-budget exhaustion, reassess once rather than silently resetting the budget.

Keep required child work pending until accepted or explicitly taken over. Confirm a
child's execution state before taking its write ownership. Do not promise background
follow-up unless the host supports resumption; close accepted children only through an
available native close operation.

Require `pass`, `partial`, `blocked` or `needs_context`, plus the result and source
references, changed/unexpected paths, actual check results, required checks not run and
why, unknowns and recovery point. The child reports completion or a blocker without
being prompted; an unrun required check cannot support `pass`.

Check against the original requirement as well as the assigned outcome and boundary;
the parent may have weakened the brief. Inspect underlying evidence when checks
are missing/failing, paths are unexpected, claims conflict, or consequential contracts
are involved. For consequential acceptance, locate the actual pass/fail rule and check
a minimal case that violates the source promise while other conditions remain healthy.
Logging a condition is not enforcing it; missing coverage is not a pass. Tests derived
from the same brief and a child's pass label cannot alone establish requirement coverage.
Integrate once; reuse current sufficient checks and rerun affected behavior
only when new changes or evidence warrant it. Child self-review is not acceptance.

## Resolve gaps without retry loops

A pre-work `needs_context` reply permits a bounded clarification to the same child within
the same authority. A scope/architecture change or a gap remaining after clarification
returns to the root. Failed checks, incomplete/blocked work or confirmed execution failure
also return to the root for diagnosis and completion. Do not retry the failed child, launch a replacement,
or cascade through model routes. A distinct unresolved decision may receive configured
read-only expert advice after local diagnosis; this does not reassign the failed task.

Summarize accepted evidence and material unresolved issues rather than forwarding the
whole child report. Do not add reports, ledgers,
hashes or extra review agents unless the task or repository requires them.

## Lessons

- An explicit bounded model/effort request is already a dispatch decision; a mode question
  must not block it, even inside a longer task.
- A child faithfully implemented a weakened parent brief and its tests passed. Check
  acceptance against the source at dispatch and return, including parent-introduced drift.
- Claude delegation's shared-scratch incident showed that disjoint source files alone
  do not protect frozen runtime state; scratch and script targets also need ownership.
- Claude's long-running children accumulated large contexts and repeated status wakes.
  Transfer the event-driven handoff, while checking Codex's own wake and wait semantics.
