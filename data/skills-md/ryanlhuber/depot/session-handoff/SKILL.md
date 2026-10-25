---
name: session-handoff
description: "Condenses the current work into a self-contained handoff note so a fresh session, another agent, or a person can continue without the conversation history. Use when pausing or ending a session, switching tools or models, running out of context, or passing work to someone else. Not for final reports to stakeholders and not for archiving a full transcript."
disable-model-invocation: true
---

# Session Handoff

## Purpose
Capture what the next reader needs to continue work correctly: the goal, the current state, what was decided and why, what is unfinished, and what to do next. The note must stand alone.

## When to use
- Use when: work will continue later or elsewhere, the conversation is long or near its limit, or a different agent or person is taking over.
- Do not use when: the work is finished and the audience wants a report, or the request is a transcript or backup.

## Inputs
- Required: the current conversation and work state.
- Optional: the destination reader (a fresh session, a named person), where to save the note, and files, branches, or revisions to reference.
- Assumptions: the reader has repository access but none of the conversation.

## Process
1. State the goal in one or two sentences and the stopping point: what is done, in progress, and not started.
2. List decisions made with a one-line reason each, so the reader does not reopen them by accident.
3. List what was tried and did not work, so it is not repeated.
4. Point to artifacts by reference: file paths, branches, revisions, commands, links. Do not paste large content.
5. Mark each claim about the state as verified (checked, with how) or unverified. Do not report a test or check as passing unless it was run.
6. List open questions and blockers with who can resolve each.
7. Write the next actions in order, each concrete enough to start without asking.
8. Remove secrets, credentials, and private data. Save the note where requested, or return it in the reply, using the [handoff template](templates/handoff.md).

## Rules and heuristics
- Required: separate verified facts from unverified ones and from opinions.
- Required: use exact references (revision, path, command) instead of descriptions like "the latest file".
- Required: no secrets or private data in the note.
- Recommended: keep it to roughly one page; link to detail instead of restating it.
- Recommended: put the single most important next action first.

## Checks
- A reader with no context could start the first next action from the note alone.
- Every referenced path, branch, or command exists as written, or is marked unverified.
- Nothing claimed as done was not done, and nothing sensitive is included.

## Output
Return the handoff note and, if it was saved, its location. List any references that could not be verified.

## Completion criteria
- The note contains goal, state, decisions, failed attempts, references, open questions, and ordered next actions.
- The checks above pass, or the exceptions are listed in the note.
