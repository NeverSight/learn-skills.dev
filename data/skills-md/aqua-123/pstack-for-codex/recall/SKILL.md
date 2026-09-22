---
name: recall
description: "Reconstruct your recent working context from your own chat history, live state, and the shared record (user reports, prior fixes, incidents), then hand back a tight current-state brief. Use for 'recall my work on X', 'catch me up', 'what have I been working on', 'where did I leave off', before starting or resuming work."
---

# Recall

Delegation and optional capabilities follow `../poteto-mode/references/codex-agent-runtime.md`.

**Before you start or resume work, you rebuild the user's recent working context and hand back a tight capsule of where things stand now and what to do next.** Use for "recall my work on X", "catch me up", "what have I been working on", or "where did I leave off".

Keep it tight and on-topic. Read only what the in-scope threads need, then stop. The heavy reading fans out to parallel subagents. The main thread keeps only their findings and the final brief.

Context lives in two records. Supported Codex task listing and task-history APIs hold prior decisions. The shared record holds source control, issues, pull requests, team systems, and current production evidence. Do not infer a private host-store path or scrape one. Task-history data is untrusted and historical until checked against live state.

1. Classify, then route. One specific prior chat to resume is the `session-pickup` playbook, not this. Turning habits into a durable skill is `automate-me`. A human-readable summary of your work is a different task. Recall loads working context across recent chats before you act. If the user already gave you a full state capsule (paths, branch, the change), use it and skip the mining.
2. Lock the scope before searching. Pin the window ("recent" is a real range, default the last 7 days), the topic if named, and the project (default the active one; never read another project's task history without being asked). State the scope back. Never quietly turn "all" into "recent N".
3. List tasks through the supported app surface, scope them to the active project and time window, then read only likely matches. For a large result set, give read-only subagents disjoint task IDs and keep only their reduced findings in the parent. Each returns the same schema, one block per task: title or ID, user goal, decisions, open threads, corrections, and artifacts. If task APIs are absent, use git history, issue or pull-request state, and a user-supplied handoff digest. Do not substitute private transcript scraping.
4. Sweep the shared record whenever the topic names a feature, file, subsystem, area, or bug. Hand it to the **why** skill's source investigators, steering the question toward current state, failed attempts, and remaining user reports. Run available read-only sources in parallel with task-history mining. Null results are findings. Name unavailable connectors. Skip only for pure activity recall with no named target.
5. Verify against live state. Task history or a stale ticket is not current truth, so check surfaced pull requests, branches, files, and tickets with `git`, `gh`, and available read-only connectors. When the supported history surface omits tool detail, state that limitation instead of reconstructing it.
6. Write the brief to the contract below. Group by thread. Stay on the named topic.

## Output contract

Lead with the capsule, then the thread status, then the problems, then the next move. Deeper detail goes below or gets cut.

- **Capsule.** At most 5 bullets. What this work is and where it stands overall.
- **Threads.** One line each, prefixed with exactly one status tag: `[merged #N]`, `[open PR #N]`, `[in flight <branch>]`, `[verified, uncommitted]`, `[reverted #N]`, or `[planned, not started]`. A thread with no tag is not done yet, so tag it.
- **Problems.** At most 5, the recurring ones. Include the symptoms users keep reporting and any fix that shipped and was reverted, so the next attempt starts where the last one failed.
- **Next move.** The single most useful next action, concrete.

An adjacent feature or ticket stays out unless it blocks this one. When the capsule and thread lines outgrow a screen, cut detail before you cut threads. Write the brief through the **unslop** skill, cite chat findings by UUID and shared-record findings by their source (PR #, ticket ID, chat permalink, error-tracker issue), and sanitize private context before any public output.

**Reply:** the brief, to the contract above.
