---
name: restate
description: >
  restate to say the last message again in plain words, catch the user up
  since their last message, and summarize any decision they need to make.
---

# Restate

## Options

The source is the agent's previous user-visible message in this conversation.
The window is every turn after the user's previous message through that
reply. "Restate", "say that again simply", "catch me up", and "what do I
need to decide" select this procedure.

A request to keep the jargon, skip the catch-up, rewrite some other text,
or change the underlying work blocks. No previous message blocks.
Record `source | window | decisions | terminal`.

## Voice

Write as one person talking to another. Use everyday words and short
sentences. Keep the facts, names, and outcomes. Say each thing once, in
fewer words than a long source. Use a specialist term only when the user
used it or the fact disappears without it.

## 1. Gather

Read the source message and the window. Fix what changed, what finished,
what is still open, and every action or decision waiting on the user.
Use only facts the conversation supports.
Done when the source, window, and user decisions are fixed, or the run is
blocked.

## 2. Write

The reply has this order:

1. Restate the source so a reader who missed it can follow it alone.
2. Catch up on the window: what changed, what finished, and what is still
   open. When that repeats the restatement, one placing sentence is enough.
3. When the user has an action or decision, close with an executive summary:
   the choice, the facts that matter, and what each option leads to. Several
   decisions each get that context. No user decision means no summary.

Done when the reply is plain, complete for the window, and every user
decision can be made from the summary.

## 3. Deliver

Send the reply in the current conversation. Leave files, tasks, and git
unchanged.
Done when the reply is sent.

Terminals: RESTATED, BLOCKED.
