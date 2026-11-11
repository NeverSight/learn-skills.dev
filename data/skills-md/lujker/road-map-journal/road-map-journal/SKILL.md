---
name: road-map-journal
description: "Use when working with a project's roadmap, development plan, queue, work journal or item status: asking what is next, continuing or resuming planned work, recording a decision, updating an item, or reconciling status with evidence. Follows the project's own conventions. Triggers include «дорожная карта», «что дальше по плану?», «продолжай разработку по плану», «запиши решение», «обнови статус пункта»."
license: MIT
metadata:
  version: "0.4.0"
---

# Roadmap and work journal

Maintain a useful current plan and a traceable record of decisions without imposing a new layout. Follow the user's instructions and the project's conventions. Preserve existing names, identifiers, language, links, uncommitted changes, and unrelated content. For a new plan, use the language the user specifies or reasonably indicates; ask if it is unclear. Do not impose a language.

## When to use

Use for requests about a roadmap, development plan, queue, work journal, item status, or continuing planned work. Examples include “what is next on the roadmap?”, “continue the agreed item”, «дорожная карта», «план разработки», «дневник разработки», «что дальше по плану?» and «продолжай разработку по плану». Determine the requested scope from context; a status question is read-only.

## Discover first

Identify the project root and read its instructions. Locate existing roadmaps, queues, item notes, and handoff documents; names and locations vary. Read the relevant item, its acceptance criteria, current queue and linked notes. Check the relevant implementation, version-control state if available, and evidence when the request needs a current-state assessment. Do not assume Git, a specific directory layout, or a particular status vocabulary. If the project has `board/config.json`, its plan is a card board: read [Board projects](references/board.md) before editing. For multiple repositories, follow existing links; ask for an inaccessible authoritative location rather than inventing a replacement.

Select the mode implied by the request:

- **Read-only:** Answer from the relevant documents and evidence. Distinguish recorded claims from independently checked facts; make no edits.
- **Init:** If no plan exists, discuss the owner's desired way of working and propose a suitable structure, location, scope, initial items and ordering; include tracks, agent roles and initial cards when relevant. For deeper exploration, use `grill-me` if available and appropriate; if absent, offer to install it, but do not install without permission or block the workflow. Otherwise facilitate a concise structured discussion yourself, with recommendations for unresolved choices. Obtain informed user consent before creating files; do not invent priorities or commitments.
- **Adopt:** If planning material already exists, use it in place. When the owner requests a substantial review, use the same optional structured discussion as for initialization, tailored to what is unresolved. Explain any proposed new file, migration, or substantial rewrite and obtain informed consent first. Do not silently create a parallel source of truth.
- **Resume:** Read the latest directive, active queue, item notes, and relevant current state. Resolve contradictory or stale instructions against current evidence and the user's latest decision; ask if a consequential conflict remains. If the item is not already selected or delegated, agree on one before implementation. A saved plan or approval to document is not authorization to start work.
- **Update:** Make the requested, scoped changes to existing records. Keep the item's status, remaining work, and affected queue entries consistent; preserve history and unrelated ordering. For a new file or substantial rewrite, explain the proposed change and obtain informed consent first. A request limited to one item does not authorize implementing or rewriting the rest of the plan.

## Record and reconcile

Use the project's established arrangement. Typically, a roadmap summarizes items and their current order; a journal holds decisions, findings, evidence and history. Link rather than duplicate long details. Keep identifiers stable. Do not silently delete decisions or cancelled work: mark them superseded or cancelled with the reason when relevant.

When a decision, pause, or order changes, update affected current summaries and next-step instructions within the authorized scope; label prior instructions as historical. A paused or deferred plan must not appear to be an active instruction to continue. Do not reprioritize unrelated work merely because a note was added. If a necessary correction falls outside the authorized scope, flag it to the user rather than expanding the edit.

Unless the owner has authorized a broader scope, work on one item at a time and do not automatically begin the next. A completed substage does not complete the parent item; record the remainder. Keep work mode separate from permissions and budgets: authorization to continue is not blanket permission for production actions or external writes. Keep recorded completion, pending user acceptance and fully accepted work distinct. Keep concise checkpoints at handoffs, decisions, verified results and blockers, including what remains and how to resume; verify uncertain in-flight actions before repeating them. Before a multi-file update in a shared checkout, check the version-control state and dirty paths immediately before writing, apply narrow edits against freshly read content, preserve unrelated work, and verify the scoped changes without committing or publishing unless authorized.

For work that spans several items, agents or sessions, has a budget, or where the owner authorizes a track or continuous mode, read [Long-running work](references/long-running.md) first.

## Status and evidence

Use the project's status vocabulary. If none exists, suggest OPEN, IN PROGRESS, BLOCKED, PARTIAL, and DONE, with meanings agreed for the project. Record status according to the acceptance criteria and actual evidence, not intention or a delegate's unsupported claim. For PARTIAL, name what remains and any blocker. Keep affected status references consistent.

Record checks actually performed, their outcomes and scope, and who performed them when relevant. Evidence may be historical or from another executor; label its source and applicability, and do not imply it was rerun. If later changes invalidate a check, identify or perform the appropriate verification. Never invent commands, results, test counts, approvals, or user acceptance. Automated tests, released code, and live operation are different claims: never infer live acceptance from implementation or tests. If required acceptance has not occurred, retain PARTIAL or the project's equivalent and state the missing environment or approval.

After an authorized edit, check the affected status, queue, links, and consistency with the evidence and scope. Report changes, checks actually made, and unresolved items. Do not claim verification that was not performed.

## References

- [Generic templates](references/templates.md) — optional starting points, adapted to the project.
- [Scenarios](references/scenarios.md) — concise examples of mode and scope choices.
- [Long-running work](references/long-running.md) — tracks, checkpoints, handoff and recovery, pause and stop, acceptance, budgets, shared checkouts.
- [Board projects](references/board.md) — working in a project whose plan is a card board.
- [Multi-repository reconciliation](references/multi-repo-sync.md) — preserve work and distinguish recorded, Git and live state across checkouts.
