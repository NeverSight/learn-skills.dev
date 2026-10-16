---
name: pythia-deploy
description: Use when a change spans more than one statement or file - a release or migration script, "chay script DDL", "deploy ban release", "run these .sql files", a table with its comments and indexes, a package spec and body together, a directory of numbered scripts. Orders the statements, previews every one, gets one approval for the set, runs them through apply's six steps in order and stops at the first failure.
---

# Deploying a Release

**Announce at start:** "Using pythia-deploy — previewing every statement in the release first."

**Phase:** Ask → Do — the whole ordered set is previewed and approved once, then run step by step

A release script run with `sqlplus @release.sql` has no snapshot, no
preview, no verify and no record of what landed before line 212 failed.
`pythia deploy` runs the same file through the write path, statement by
statement, so a failure stops cleanly with an exact list of what landed and
how to undo it.

## The Iron Law

```
A RELEASE RUNS IN ORDER, AS PREVIEWED, AND STOPS AT THE FIRST BROKEN STEP
```

## How a script is read

- One statement per `;` for SQL; PL/SQL units (`CREATE ... PROCEDURE /
  FUNCTION / PACKAGE / TRIGGER / TYPE`) end at a line holding only `/`.
  A `;` or `/` inside a literal or a comment is text.
- SQL*Plus directives (`SET`, `PROMPT`, `SPOOL`, `SHOW ERRORS`, `WHENEVER`,
  `DEFINE`, …) run nothing on the database: they are skipped and listed.
- `@file` / `@@file` includes are **refused** — list the files instead;
  deploy never runs a path nobody looked at.
- Refused, never skipped: anonymous `BEGIN ... END;` blocks (as in `apply`),
  `EXEC` / `HOST` / `CONNECT`, and `ALTER SESSION` — it would silently change
  how every later statement runs, which no preview can show.
- Files run in the order given. A directory runs in natural name order when
  every file is numbered (`1_`, `02_`, `10_`, Flyway's `V3__`), otherwise by
  what each file creates — tables, indexes, comments, types, views, specs,
  procedures, bodies, triggers, grants, data. The preview says which.

## The Workflow

1. **Assemble** the files in the order they must run; impact
   (`pythia-impact`) for every existing object the release changes.
2. **Lint** the set: `pythia lint <files>` — errors are fixed before the
   preview, not after.
3. **Preview**: `pythia deploy <files>`. Nothing is written. Relay it
   verbatim: each statement's group, object, lines changed, impact,
   `! DESTRUCTIVE` and lint lines, the diffs. Policy refusals arrive **before
   anything runs** — relay them; the developer decides.
4. **Ask once** — the preview prints a deploy token (10 hex). The developer
   approves it through one door: the `pythia_approve` tool, an
   `AskUserQuestion` whose text is `pythia approve --card <token>` verbatim,
   or `pythia approve <token>` in their terminal.
5. **Run**: `pythia deploy <files> --confirm <token>` — the same file list.
   Each statement goes through snapshot → apply → verify with its own
   journal entry. Read the exit code, unpiped: `0` all landed · `1` refused
   (nothing after it ran) · `3` written but broken (stopped there).
6. **Report** every statement's result. On a stop: what landed stays landed
   (DDL commits itself); the rest of the approval is withdrawn; the output
   lists the undo commands newest first, which landed statements have no
   undo, and the `--from N` to resume with. Fixing forward or restoring is
   the developer's call.

Under an autopilot lease (`pythia-autopilot`) that covers **every**
statement, step 3 lands the release directly; if any statement is not
covered the whole release falls back to preview, and the output says which
one and why.

## Re-running after a stop

The statements before the stop are in the database; `CREATE TABLE`,
`ALTER TABLE ADD` and inserts cannot run twice. Fix the failing statement,
then `pythia deploy <files> --from <N>` — a fresh preview and a fresh
approval for the rest. A backfill that needs a column added earlier in the
same release cannot be measured before the DDL exists: deploy the DDL, then
the data part with `--from`.

## Red Flags — STOP if you catch yourself thinking

| Thought | Reality |
|---------|---------|
| "Faster to run it in sqlplus" | And no snapshot, no verify, no record of where it stopped. The hook denies it anyway. |
| "Statement 7 failed, skip it and continue" | The rest was ordered on top of it. Stop, report, let the developer decide. |
| "The includes are fine, I wrote them" | Deploy runs what was listed and previewed. List them. |
| "One approval covered the release, so I can edit a file and re-run" | The token binds the previewed content. Edited → preview again. |
| "Exit 3 on the last statement, everything else is fine" | Written but broken. Report it as broken, with the undo list. |

## When NOT to use this skill

- One statement in one file → `pythia-apply`.
- Designing the tables or packages inside the release → `pythia-table`,
  `pythia-package`; this skill only lands them.
