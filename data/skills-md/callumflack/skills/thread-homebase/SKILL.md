---
name: thread-homebase
description: Reviews and prioritises Codex tasks when recovering forgotten work or deciding what to do next across projects.
---

# Thread homebase

Use the Codex task registry and recent task content to identify current work and unresolved commitments. Do not reconstruct repository delivery status from a coordination task.

## Find the work

Include active tasks and the 6–12 most recently updated non-archived Codex tasks. Broaden the search when the user asks for older or forgotten work.

Start with registry titles and summaries. Read recent turns when ownership, completion, or the next action is unclear. Prefer the latest user steer and unfinished assistant commitment over the original task premise. `idle` or `not loaded` does not mean completed; report only what the evidence supports.

Identify the smallest owner of the current decision or deliverable. For ordinary repository work, use the working directory as a starting point. A routing workspace such as Workspaces is not itself the project: infer the owner from task content. Preserve cross-project or unresolved ownership when a single repository would be misleading. Distinguish the owner from other repositories merely discussed or affected.

## Report

Put active work first, then group tasks by project or owner. Give each group a `## <project or owner>` header, with a blank line between groups. Do not repeat the project on every task line.

Use short lines:

`[Exact task title](codex://threads/<thread-id>) — <current work or open question; explicit PR # or Linear code when available> — <status>`

Preserve registry titles verbatim, including symbols. The title does not replace the current purpose. Include an explicit PR number or Linear task code from the title, summary, or recent task turns in the purpose; do not invent one. Add scope or other touched surfaces only when they resolve ambiguity.

Flag stale, blocked, or apparently abandoned work when relevant to the requested review, with one concrete reason for each. Age alone does not establish abandonment. Omit an empty outliers section.

Propose 1–3 priorities only when the user is deciding what to do next.

## Automation and continuity

Schedules and notification settings belong to the automation. Its prompt should tell the agent to load this skill from its installed path, rather than copy the report instructions.

Create a replacement homebase task or archive an existing one only when the user explicitly requests it. A triage report does not authorize task lifecycle changes.
