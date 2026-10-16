---
name: pythia-autopilot
description: Use when the developer wants the agent to work without approving every write - "tu dong hoan toan", "cu lam het di", "dung hoi tung buoc", "work autonomously", "approve everything for this task", a long build session - or when an apply preview says autopilot is active, paused, expired or not covering a statement. Requests one developer-approved lease, works strictly inside it, stops where it stops, and reports every write it made.
---

# Working Under Autopilot

**Announce at start:** "Using pythia-autopilot — asking you once for a scoped lease instead of every write."

**Phase:** Ask → Do — one delegation the developer approves, then work inside its limits and account for every write

Twenty identical approvals teach a developer to click without reading — the
gate becomes theatre. An autopilot lease replaces them with one honest act:
the developer reads a card naming the connection, the statement groups, the
hours and a write budget, and approves it once. Until it ends, `apply` and
`deploy` land covered statements without asking. Every write is still
snapshotted, journaled and verified.

## The Iron Law

```
THE LEASE IS THE DEVELOPER'S. ITS LIMITS ARE NOT YOURS TO STRETCH.
```

## What a lease never covers

- A protected connection (`"protected": true` or `"env": "prod"` in
  connections.json) — refused outright.
- Destructive statements — `DROP`, `TRUNCATE`, `ALTER ... DROP`, renames,
  `SET UNUSED`, `REVOKE`, `UPDATE`/`DELETE` without `WHERE` — unless the
  card said "DESTRUCTIVE statements INCLUDED".
- Groups the card did not name; a file with lint **errors**; GRANT ... TO
  PUBLIC, ANY privileges or grant options; DML touching more than 1,000
  rows — those are shown to the developer first.
- Anything after it pauses: other objects went INVALID, or five failed
  writes in a row. Or after the clock, the budget, or `autopilot off`.

## The Workflow

1. **Settle the spec first** (`pythia-spec`). Autonomy removes per-write
   questions, not spec questions — ask every open decision up front, in one
   batch, before the lease starts.
2. **Propose the narrowest scope that fits the task**: the dev connection;
   groups `plsql_source,comments` by default, `structural` only if tables
   are part of the task, `data_dml` only if asked, destructive only if the
   developer names it; hours and writes sized to the job.
3. **Request** — `pythia autopilot request --groups ... --hours ... --note
   "<the task>"` prints the card and an 8-hex token. Ask through a door:
   the `pythia_approve` tool, or `AskUserQuestion` with `pythia approve
   --card <token>` verbatim, or the developer's own terminal. `autopilot on`
   is the developer's console command, never yours.
4. **Work** with the normal skills — `pythia-impact` before every change
   still applies; then `pythia apply <file>` / `pythia deploy <files>` land
   covered statements directly. Read every result:
   - exit 0 — landed; keep going.
   - exit 3 on your own object's compile errors — fix forward, within the
     lease.
   - exit 3 with other objects newly INVALID — the lease **pauses itself**.
     Stop and show the developer; do not request a new lease to continue.
5. **Not covered?** The preview says why (`! autopilot: not covered — ...`).
   Fix what is yours (lint errors), or ask for that one statement through
   the normal approval door. Never reshape a statement to dodge the
   destructive check.
6. **Finish**: `pythia autopilot report` — relay every write with its
   verdict and the undo commands (broken ones first); then `pythia
   autopilot off`. Revoking is always allowed; it only tightens.

`pythia autopilot status` shows the lease at any time; the session-start
state line shows it too.

## Red Flags — STOP if you catch yourself thinking

| Thought | Reality |
|---------|---------|
| "Ask for all groups and destructive, so nothing interrupts me" | The narrowest scope that fits. Interruptions on destructive statements are the point. |
| "The lease covers it, so skip impact" | The lease removes the approval, not the method. Impact first. |
| "Paused — I'll request a new lease and carry on" | The pause exists so a person looks. Show the result; they decide. |
| "Lint error, the developer won't mind" | Autopilot does not land it. Fix it, or ask for that one approval. |
| "I'll turn autopilot on myself" | The CLI refuses without a console. It is the developer's act. |
| "The report can list just the successes" | Every write, broken ones first, with the undo for each. |
| "It's prod but the developer said it's fine" | Protected connections are never leased. One approval per write there. |

## When NOT to use this skill

- The developer wants to review each change → the normal `pythia-apply`
  flow; never request a lease they did not ask for.
- A single change → one approval is simpler than a lease.
