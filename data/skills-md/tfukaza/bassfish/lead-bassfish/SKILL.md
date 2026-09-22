---
name: lead-bassfish
description: Manage a Bassfish coding team with clear roles, implementable assignments, integration ownership, focused review, and intervention when progress stalls. Use when the user appoints you manager or lead of a multi-agent initiative. Do not use for ordinary participation or Bassfish CLI administration.
license: MIT
---

# Lead a Bassfish team

Use [use-bassfish](../use-bassfish/SKILL.md) for shared MCP protocols. This skill adds management judgment; read its [examples](references/manager-recipes.md) when framing an assignment, resolving a decision, or intervening in stalled work. Human CLI administration belongs to `manage-bassfish`.

## Establish the delivery target

Identify the user's working journey, current acceptance criteria, constraints, and smallest useful next increment. Separate required acceptance from suggestions and future hardening. A prototype's placeholder policy must not grow into an unsolicited production proof programme. Preserve genuine safety, licensing, transaction, and permission requirements.

Use the authoritative roster and existing tickets to identify the lead and owners. Preserve identities and reconcile conflicting leadership rather than creating a second manager. Choose one canonical thread: explicit ID, root ticket's canonical link, oldest semantic match, then duplicate-safe creation. Link related tickets there. Consolidate split discussion with a concise summary and redirect to participants needing action.

Start ready work without waiting for every introduction or model report. Confirm capabilities once when relevant to allocation; use observed performance and bounded tasks when model details are unknown.

## Assign roles and working increments

Give each agent a primary role with a concrete deliverable and boundary:

- **Implementer:** working code, relevant verification, and a handoff to integration.
- **QA:** executable tests or a reproducible failure through the scoped user journey.
- **Reviewer:** actionable findings on a specific artifact and an explicit disposition.
- **Security tester:** evidence about the assigned threat or boundary within authorized test scope.
- **Integration owner:** connect increments, run the combined journey, and resolve interface gaps.

Do not require every role on every project. Change roles explicitly when the work changes. Keep implementation capacity available; avoid assigning the whole team to design or review while ready implementation remains. The lead may own a bounded implementation or integration slice.

Keep assignments compact: owner, role, outcome, source/interface scope, first working increment, integration owner, acceptance checks, and reviewer when needed. Reuse tickets and real prerequisites. Preserve implementation latitude.

Include ordinary edits, builds, and relevant tests within the user's authorized assignment. Do not divide them into successive managerial grants for design, source, configuration, compilation, and execution. Preserve actual host approvals and user/repository restrictions, including dependency rules and scope boundaries; do not request authorization already provided.

## Keep progress visible and unblock it

At normal checkpoints, inspect changed artifacts and relevant updates. Ask for what changed, evidence, the next artifact, and any concrete blocker when these are unclear. Avoid repeated full inventories and unchanged-history reads. Use native delivery or requested waiting; respect explicit polling instructions without adding busy loops or unchanged status posts.

Default intervention point: two consecutive checkpoints without role-appropriate progress or a resolved blocker. Narrow the task, decide the missing interface, pair agents, or reassign it. Observable phases of a running test, a useful QA reproduction, and concrete review findings count as progress; lines of code alone do not.

Require additional specification or proof work to name the unresolved question, why it blocks implementation, and the decision it enables. Prefer a small experiment or working increment when that answers the question. Planning-only requests remain planning-only.

When integration is required, an isolated module is an intermediate delivery. Name its integration owner and next step; do not leave reviewed artifacts inactive indefinitely. Release shared reservations before waits and use private worktrees or reviewed snapshots as described in `use-bassfish`.

## Decide and review proportionately

For a shared choice, get focused input from affected owners or relevant experts, then decide within the user's constraints. Record the chosen direction, reason, material dissent, and next action. No default voting round or mandatory thesis from every agent. Silence is not approval; the lead's decision is explicit. Escalate a requirement change or unresolved material risk rather than overruling a safety constraint.

Use one focused independent review for material shared interfaces, correctness, data integrity, or security work, plus relevant tests. Low-risk local changes need proportionate verification. Name the reviewer, target artifact, and question. Additional review addresses changed code or unresolved findings; do not require every specialist or repeatedly audit unchanged historical evidence.

Failed tests remain failures. Diagnose and fix the concrete problem, preserve earlier evidence, and qualify subsequent results separately. Specialized acceptance procedures apply when relevant; ordinary functional checks do not automatically require a team-wide performance window.

## Close work and improve recurring workflows

Record a concise result linked to code, tests, review, integration status, and remaining gaps. Mark milestones complete only when their acceptance criteria pass. Keep the initiative moving until its outcome is complete, the user stops it, or a genuine input/permission blocker prevents progress.

For demonstrated repetition, reuse existing tools first. Create a narrow helper or skill when it saves recurring effort and helps current delivery. Do not turn workflow improvement into another open-ended workstream for the whole team.
