---
name: session-handoff
description: >
  Use only when the user asks to write a handoff, continuation prompt, or
  session transfer file so another agent, model, or harness can continue the
  current work, or names session-handoff. Writes one short file under
  `.handoff/` that the successor executes: what was being done, what comes
  next, and the questions to put to the user. NOT when the user gives the path
  of an existing handoff file or says to continue from one: that asks you to
  carry out the file's task, not to write or improve a handoff. NOT for
  bounding a weaker executor on an approved plan (small-model-handoff),
  writing or executing plans (gigio-write-plan, gigio-execute-plan), or
  reading another session's transcript (read-agent-sessions). Never activate
  because a session has grown long or context is running low.
---

# Session Handoff

Write one file that a successor given only its path recognizes as its task and starts executing. If you were handed a handoff file instead, you are the successor: do its task and leave the file alone.

This request authorizes reading what the handoff needs and writing the file, nothing more. Grants the user gave for the task are recorded for the successor, not used here.

## Writing the File

1. Write to `.handoff/<YYYY-MM-DD>-<HHMM>-<task-slug>.md` at the project root, in local time with a short ASCII kebab-case slug. For several repositories, use their common root and label each.
2. Fill `assets/handoff.template.md`. Keep its bold opening instruction word for word and delete rows with nothing to say.
3. The user's current explicit words decide intent and scope; live files, version control, and fresh tool output decide status. Quote the user's decisive sentences verbatim with their date. Point to paths, commands, and commits instead of pasting them, and leave out secrets.
4. Subagents, background jobs, pending tool calls, and in-session grants end with this session. Record what each left on disk, and list as still running only handles the successor can check from outside, with the checking command. Record the origin harness and session id so `read-agent-sessions`, where installed, can recover the transcript.
5. Ask only about unknowns that would change the work and that only the user can settle, each with its consequence, concrete options with a recommended default, and what to do if unanswered. A fact that inspection or a cheap check can settle goes into Next Actions instead.
6. If a plan in `.plans/` or a PROJECT.md governs the work, point to it by path, carry only what it lacks, and name `gigio-execute-plan` when continuing means executing it.

The file is ready when a reader with nothing else can run the first action, sees evidence for each completed claim, and knows what to ask the user.

## Earlier Handoffs

The newest `.handoff/` file with the task's slug is current. Keep its still-valid decisions, name it on the new file's Supersedes line, and add only this line at the top of the old file: `Superseded by <new path>. Open that file instead.` A legacy root `handoff.md` is superseded the same way.

## Delivery

Report the path, the recorded status, and the first action. Read `references/source-notes.md` only when maintaining this skill.
