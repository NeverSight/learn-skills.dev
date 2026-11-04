---
name: agent-handover
description: Keep multi-agent coding work resumable at any moment. Record progress, in-flight agents and jobs, task cards, decisions, user preferences, lessons and open questions in the repository, not in chat or local agent memory, so another agent or tool can take over in minutes. Use this after a delegated task is accepted or committed, before a session may be interrupted or context compacted, when handing work to another agent or another tool (Claude Code ↔ Codex), when taking over someone else's half-finished work or starting cold, and whenever the user states a decision or preference that should outlive this session.
license: MIT with Commons Clause v1.0 (see LICENSE)
compatibility: Built for Claude Code (primary) and Codex (secondary); other hosts are unverified. Needs only a repository it can write to.
metadata:
  version: "0.3.4"
---

# Agent Handover

Goal: the project can be handed to another agent at any moment, and the new agent recovers context within minutes from the repository alone, without the chat history or a tool's private state directories.

Pairs with `subagent-team`. That skill decides *when* a unit of work is done; this one decides *what gets written down and where*.

| When you... | Read |
|---|---|
| write a progress, log, decision or open-question entry, or backfill a commit hash | [references/records.md](references/records.md) |
| need a copy-ready entry (snapshot, in-flight record, log row, recovery summary) | [references/entry-templates.md](references/entry-templates.md) |

## 1. Rules live in the repository

- User decisions, preferences, process rules and project constraints go into the repository (`docs/`, `AGENTS.md`, skills) and travel with git.
- An agent's local memory (for example Claude Code's per-project memory, or Codex's) may hold only **pointers**, such as "process rules: see `docs/progress.md` §4". It must never be the only copy. Memory does not survive a new machine, a new tool or a new agent.
- If memory holds a rule the repository lacks, write it into the repository first, then shrink the memory entry to a pointer. When memory and repository disagree, the repository wins; tell the director.
- Each rule has **one** authoritative home. Everywhere else links to it instead of restating it, so copies cannot drift.
- `AGENTS.md` links to the entry index, and the entry index links back to `AGENTS.md`. Both Claude Code and Codex load `AGENTS.md` / `CLAUDE.md` every session, so that link is how a cold agent finds the state.
- When the user adjusts the process ("stop outsourcing auth tests"), write it down **immediately**: a dated lessons entry with their words, and the rule in `AGENTS.md` if it applies project-wide.

## 2. File map

Adapt the names to the project; the separation is what matters. Projects that use the `subagent-team` skill's team board keep these files in `docs/agent-team/` (index `README.md`, `progress.md`, `decisions.md`, `lessons.md`, one card per task under `tasks/`); use that layout when it exists.

| File | Holds | Does not hold |
|---|---|---|
| Entry index (e.g. `docs/<program>/index.md`) | Reading order, track status, priorities, decisions-to-be-made list, decision index, hard cross-track constraints | Detailed acceptance numbers |
| Progress record (e.g. `docs/<program>/progress.md`) | Status snapshot, completed log, next-up queue, user decisions summary, open questions, pitfalls, handover protocol | Decision bodies |
| Decision log | Numbered decisions with motivation, rejected options, overturn conditions | Progress |
| Task cards (e.g. `docs/agent-team/tasks/<id>.md`) | One task or external job: flow, holder (its only writer), lease, job ids, log, open questions, result | Acceptance numbers (they go to the completed log) |
| Lessons (e.g. `docs/agent-team/lessons.md`) | User adjustments to the process and lessons learned, dated, user's words verbatim, with a link to the rule if one was promoted | The rule itself, once promoted (it lives in `AGENTS.md`) |
| `AGENTS.md` | Project-wide hard rules, an index of skills, a link to the entry index | Progress |
| Skills | Reusable methods and process rules | Project state |
| Local agent memory | Pointers only | Any rule, decision or constraint |

Acceptance numbers are written **once**, in the completed log. Everything else references them.

## 3. Writing the records

The short version; details, the backfill procedure and the self-check grep are in [references/records.md](references/records.md):

- **Write at the moment it happens**: a completed-log row (newest at the top) when a unit is accepted; a decision summary **immediately** when the user decides; an open question when discovered (answered in place, never deleted); a pitfall when a compromise or trap is found. Documentation sync is part of "done" and lands before the next task starts.
- **Wording**: absolute dates; keep committed, pushed, merged, deployed as separate facts with evidence, never inferred; status words planned / in progress / passed / failed / blocked / unverified; no hard-coded counts that change; cite headings by their text and code by file:line.
- **Commit hash unknown yet?** Write `<pending-commit>`; the next docs-editing task backfills every placeholder with a grep over all docs. Never amend to backfill.
- **Decisions are never rewritten**: an overturn is an "overturned" note with the reason under the original. Status fields ("landed", with the commit) are updated with the implementation. The user's words that set a rule are quoted verbatim with the date.

## 4. Hand-off checklist

For when a session may end, context is nearly full, or you hand over deliberately. File changes still go through the normal task chain where one exists.

1. Capture the scene (read-only): `git rev-parse --short HEAD; git status --short`.
2. List running work: agent names or ids (Claude Code `ListAgents`), external job ids and conversation ids (for wrapper jobs also the `--out-dir`, PID, model, effort and sandbox, and whether the process is detached, e.g. started with `nohup`, or will end with this session), and which liaison tracks each job. **Do not cancel running work just to tidy up.**
3. Write an in-flight record into the status snapshot. Include: task id, branch and HEAD, files in the working tree that belong to the task, the step it is stuck on, running agents and jobs, who holds the edit lease, the next concrete action, and anything awaiting the user.
4. Write unrecorded user decisions to the decision log or summary, and unanswered questions to open questions. Bring every task card's status, job ids and `[open]` questions up to date (holders do their own cards).
5. Move rules that exist only in local memory into the repository.
6. Add new pitfalls.
7. For committed but unsynced tasks, update the log and queue, and backfill placeholders ([references/records.md](references/records.md), "The commit-hash placeholder").
8. Self-check: grep the task id and stale words ("next", "todo", "not yet committed", "awaiting commit", `<pending-commit>`; the full grep is in [references/records.md](references/records.md)).
9. Do not push unaccepted work, leave unauthorized stashes, or delete worktrees.
10. **No time for any of that?** Put the in-flight record, unrecorded decisions and rules, and new pitfalls in your last message to the user. The next director's first job is to write them down.

## 5. Take-over checklist

For a new agent, a cold start, or after context compaction.

1. `git log --oneline -10; git status --short`.
2. Read in order: the entry index, the progress record's snapshot, `AGENTS.md`, the relevant track docs, the relevant decisions.
3. Reconcile: the newest snapshot's commit must appear in `git log`. Placeholders whose commits exist get noted for backfill.
4. If there are uncommitted changes, find the matching in-flight record. If none matches, do not investigate or revert; ask whoever owns the work.
5. Check running work (`ListAgents`; the external tool's job status, or a wrapper job's `summary.json` in its recorded `--out-dir` and whether its PID is alive, run **from the same worktree**, since job state is per worktree). Never start a duplicate of something already running. With a team board, list cards and open escalations (`team-board.mjs status` from the `subagent-team` skill, or read the cards).
6. Read the next-up queue, open questions, pitfalls and lessons relevant to the task.
7. Treat local memory as leads only and check it against the repository.
8. Before acting, reply with a short recovery summary: HEAD, in-flight tasks, next step, and what awaits the user.

## 6. External job state

External tools keep their own state directories (for example agy-staff's `.agy-staff/jobs/`, usually ignored only locally and gone on a fresh clone). Result files there are the worker's **claims**, not verified facts. Use them for deep debugging only. For handover, record the job and conversation ids in the snapshot instead.

Copy-ready entry templates: [references/entry-templates.md](references/entry-templates.md). Section-by-section rules for the records: [references/records.md](references/records.md).
