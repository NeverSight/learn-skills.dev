---
name: check
description: Use when the user asks for a workspace health check, audit, or check report, or asks to fix numbered issues from that report, for example "fix issue 3". Runs the workspace integrity tool, which applies only fixes with one correct answer (journaled, undoable) and lists everything else as numbered issues.
---

# Check

The workspace's integrity tool does the checking; this skill runs it and
reports. Run commands from the workspace root. Use `python3` or `py -3` where `python` is
missing or older than 3.9.

## Before you start

If `tools/kb/kb.py` is missing but `AGENTS.md` and `modules.md` exist,
the workspace was built before the integrity tool. Tell the user to run
the init skill, which upgrades it, and stop.

## Run

1. Apply the fixes that have exactly one correct answer:
   `python tools/kb/kb.py fix --safe`. It prints each edit and a run id.
   Every edit is journaled; `python tools/kb/kb.py undo <run-id>` reverts
   that run if the files have not changed since.
2. Run the full check: `python tools/kb/kb.py check`. It writes a dated
   report in `docs/checks/`, rewrites `docs/checks/OPEN.md` (numbered
   open issues), and updates the health line in `known_issues.md`.
3. Report to the user: the summary line, the edits from step 1 with
   their run id, and the open issues from `docs/checks/OPEN.md` by id,
   blocking ones first. Blocking means routing or evidence tracking
   would give an agent wrong context.

The tool covers module registry paths, links that must open by path
(in the wiki, in the root and module `AGENTS.md`, and in the newest part
of each session log), legacy `[[...]]` links, index coverage, session stop markers,
confidence lines, required sections per page type, duplicate pages,
evidence tracking and freshness, recipe drift, encoding, unknown source
extensions, and the lookup index.

## Fix

4. When the user names ids ("fix #3, #5"), run
   `python tools/kb/kb.py fix --ids 3 5`. It applies the automatic fixes
   and prints one line per id it could not fix (`no automatic fix`,
   `unknown issue id`; exit 1). Work each of those through the `kb`
   skill (its issue-queue procedure), asking the user where the answer
   is a judgment call.
5. Run `python tools/kb/kb.py check` again and report what is still
   open.
