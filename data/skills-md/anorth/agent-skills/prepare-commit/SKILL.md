---
name: prepare-commit
description: >-
  Checklist before making a commit: check and update the originating ticket or task,
  run tests and lint, and commit if asked.
  Use when the user asks to prepare a commit, get ready to commit, or commit changes.
disable-model-invocation: false
---

# Prepare commit

Checklist before a commit.
Proceed to commit if explicitly asked, else stop when the checklist is done and wait.

## Workflow

Run in this order.

### 1. Originating artifacts

Re-read the ticket, task, or any other artifacts that were the starting point for this conversation, and the code diff.

- Is everything in the ticket addressed?
- Summarise the ticket and what changes have been made.
- Note whether this change completes the ticket.

Where we have made decisions that contradict the ticket, keep the original brief
and append a note saying what changed and why.

If there is no written starting point, say so and continue.

### 2. Tests and lint

Prefer the project's documented lint and test entrypoints. Run lint, then tests.
Fail-stop on either — do not present the work as ready to commit if either fails.
If asked to commit and a check fails, don't commit; report.

Don't run a full production build unless the project documents that as the check to use.

### 3. Commit (only if asked)

- Stage only the files that belong to this change.
  If the working tree has unrelated changes, stop and ask before committing; don't sweep them in.
- Follow the project's commit and branch conventions.
- Write a message saying what changed and why, and reference the ticket, if there is one.
- Don't bypass hooks (`--no-verify`). If a hook fails or changes files, stop and report.
- Afterwards, check `git status`, and report the branch status and anything left uncommitted.
- If you committed on `main` itself and the change completes the ticket, close the ticket.
  Otherwise leave it open.

## Hard rules

- Do not amend, rewrite history, or push unless explicitly asked.
