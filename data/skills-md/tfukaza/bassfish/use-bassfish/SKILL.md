---
name: use-bassfish
description: Participate in a Bassfish coding team using updates, notifications, assigned tickets, shared threads, advisory file reservations, and handoffs. Use when the user asks to use Bassfish, collaborate with peers, share project context, or record team work. Team managers also use lead-bassfish. Do not use for unrelated single-agent work or CLI administration.
license: MIT
---

# Use Bassfish

Use MCP for ordinary participation. Human CLI commands are for user-requested administration.

Perform your assigned role; use [lead-bassfish](../lead-bassfish/SKILL.md) when appointed manager. Implementers deliver working code and relevant checks, QA delivers executable scenarios or reproducible failures, and reviewers deliver actionable findings on the assigned artifact. Recommend changes when they affect the task; team-wide planning and allocation are the lead's responsibility. Explicit planning-only requests remain planning-only.

## Bootstrap once, checkpoint changes

Call `getUpdates {}` for your authoritative `agentName`, online roster, active threads, unfinished team tickets, notification counts, and pending turns. Native Codex registers after hook binding. Preserve the name unless the user requests another.

Consume every `nextCursor` page before adopting the final `cursor`. Retain that inventory and cursor. At task start, before the first file edit or major shared decision, and before conclusions, handoffs, or completion, call `getUpdates {cursor}`. Merge changed entries and `removed` keys. `{changed:false}` needs no further inventory scan; reset/lost context requires bootstrap again. Read changed resources relevant to the current decision, using revision-pinned `readResource` pages or `view:"delta",fromRevision`. Reconcile overlapping or contradictory team work in the canonical thread before continuing.

Resume owned `in_progress` work first, otherwise ready owned `todo` work matching the request. Do not start work with nonempty `blockedBy`. Copy exact names from the roster or existing ticket owners; direct mentions can reach already-known offline identities. Never invent names.

Use `findResources` for targeted search and duplicate checks, not repeated project-wide scans. Reuse known IDs/revisions/cursors. Discover tools once when necessary. With orchestration tools, print structured results or needed fields, rather than whole MCP envelopes or repeated tool catalogs.

## Process delivered text

Notifications include new message text or a ticket summary, one `batchToken`, entry indices, and `moreAvailable`. Complete delivered text is sufficient to handle an update. Read a resource when surrounding discussion or its ticket body changes your decision, not merely to recover already-delivered text.

At checkpoints, fetch `notifications {action:"read"}` when `notifications.new` is nonzero; continue while `moreAvailable`. Replay an unhandled batch by its token. Expand a truncated entry with `notifications {action:"read",batchToken,item:0,cursor?}`; follow content cursors before treating it as complete.

After handling entries, acknowledge with `notifications {action:"acknowledge",batchToken}` or partial `items:[0,2]`. Queue acceptance is not processing. Do not acknowledge unrelated or unprocessed work merely to empty the inbox. Mention another agent in a reply only when they need to act, avoiding ping-pong.

Native Codex CLI 0.154+ automatically queues actionable idle updates; finish your turn normally while the adapter waits in code. Generic activity remains for active checkpoints. Interruption pauses queueing until the next prompt. Unknown acceptance retains the batch for inspection at the next checkpoint; never blindly resubmit.

`getUpdates.nativeWake` distinguishes `hooks-unobserved`, `active`, idle `available`, and `paused`. If hooks are unobserved, report that once and inspect the host integration; an executable version check or manual session bind does not establish wake readiness. Do not poll to wait for readiness.

Other native hosts retain their supported delivery policies. Use explicit `waitForWork` when requested and MCP Tasks is supported; handle/acknowledge then rearm until interrupted or approval/input is needed. Capability failure must not become model-driven polling. Explain unavailable connections; configure only when requested.

## Scoped work and canonical discussion

Own your assignment through verification and handoff. Ordinary implementation, builds, and relevant tests within its authorized scope do not need successive managerial grants. Respect actual user restrictions, host permissions, and repository policy. If blocked, report evidence, affected scope, and the smallest needed decision; continue other ready authorized work when possible.

Use the assigned canonical thread and record its link in related tickets. If no thread is assigned, reuse an explicit ID, root ticket's `Canonical thread: THREAD_ID`, oldest semantic match, or duplicate-safe creation. Raise overlap, interface conflicts, and concrete correctness concerns there. Ask the lead to resolve shared choices; do not initiate team-wide votes or independently take over management.

Progress updates should identify changed artifacts, useful findings, a handoff, or a real blocker. Link complete reports instead of appending their full history to tickets. Do not reread unchanged resources or post acknowledgements merely to show activity. Preserve failed results; distinguish a later successful check from the earlier failure.

Use exact direct structured mentions for particular owners/reviewers; `mentions.here:true` for action from online thread followers; `mentions.global:true` for every online project agent. Include corresponding visible tags; structured fields are authoritative. Global cannot combine with other modes. Ordinary progress can be unmentioned. Put large verification details in files and share a concise result plus path.

## Reuse resources and introduce once

Reuse equivalent unfinished tickets and the oldest exact active title match after trimming/case folding. If absent, claim the virtual file reservation `.bassfish/resource-creation.lock`, repeat the complete search, create only if still absent, and release. Never create that path/directory. Release any current file set before taking the guard.

Use `Introductions` with description `Shared team roster and agent introductions for this repository.` Inspect its full revision-pinned history under a thread turn. If your current name already authored an unretracted introduction, release without posting. Otherwise introduce name, role, and scope once. The first introduction in a newly created thread uses global mention; later introductions are ordinary messages. See [recipes](references/mcp-recipes.md) when creating resources.

## Tickets and review

Reuse your assigned ticket. Create a ticket when a new authorized workstream needs ownership, not for each message or review stage. Keep outcome, role, constraints/interfaces, acceptance evidence, owner, prerequisites, and integration handoff concise. Reconcile assignments conflicting with user intent instead of duplicating work.

Dependency-blocked work stays `todo`; use `blocked` only for a blocker outside prerequisites, explained in the body. Set ready work `in_progress` before working. Material shared-interface, correctness, data-integrity, or security changes need a focused reviewer other than the owner before completion; ask the lead to name one if missing. Low-risk local work needs proportionate verification. Request review of the concrete artifact, resolve material findings, and involve the lead for unresolved choices. Do not add serial design/source/configuration/execution reviews. Mark `done` only after acceptance, verification, and required review, with evidence in the body. An isolated module does not complete a milestone requiring integration.

## Revisioned reads and writer turns

Pure `readResource` reads need no turn. Pages pin a revision; follow cursors. Thread deltas include old-message retraction/reinstatement. Ticket deltas identify changed bodies.

For writes, acquire once with a target. If queued, retain/resume the same `requestToken`; never resubmit the target. Tasks status alone grants no ownership; the completed result contains the claim. Claims return metadata, revision, `turnToken`, and authoritative `expiresAt` (default 60 seconds). Inspect the claimed revision with `readResource {turnToken}` or a delta from your known revision before committing. Include the token while paging. Reads do not renew the lease.

Commit one mutation or release if no write is needed. Commit consumes the turn; body plus state changes require separate acquisitions. Never retry a commit. Recover with `getUpdates` pending turns: release only when the same request is definitively claimed; otherwise report its exact state/error. Cancel abandoned queued requests. See [read/write recipes](references/mcp-recipes.md).

## File reservations and scratch

Before coordinated shared-file mutations, claim one atomic set covering expected source, destination, and generated tracked outputs. Use explicit files or the smallest sufficient directory. Do not edit while queued. Once claimed, reread targets with native tools, edit, verify, and release promptly even on failure. Scope expansion requires release/reacquisition of the complete set. After loss/disconnect, reacquire and reread. File reservations last for the session and are advisory; external editors can bypass them. File tokens cannot commit content.

Read-only work and builds writing only ignored caches/artifacts need no reservation. For a few fixtures or temporary artifacts, prefer a task-specific ignored repo directory such as `.scratch/<agent>/<task>` and ensure its ignore rule exists. Use real Git worktrees for independent source edits or repeated source builds. Worktrees do not inherit uncommitted changes: transfer explicit scoped patches when needed. Freeze shared inputs under a short reservation when necessary, then release before private work. Avoid repeatedly cloning the working directory and caches.
