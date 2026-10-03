---
name: clarify-intent
description: One round of 2–5 clarifying questions, each with a suggested answer, then a one-line goal and definition of done before starting work. Run manually with /clarify-intent.
disable-model-invocation: true
argument-hint: "[task]"
---

Before starting a task, ask the user one quick round of questions to pin down what they're trying to achieve, then confirm the goal and get to work.

**The task:** $ARGUMENTS

If that's empty, the task is the user's most recent request in this conversation. If there isn't one, ask what they want done and stop.

## 1. Look things up first

Finding facts is your job, never the user's. Before writing questions, read the relevant files, search the code, and check config, docs, and git state. Dispatch a subagent for anything broad. Never ask something you could look up.

Questions are only for what the user alone can decide: intent, scope, priorities, preferences, and trade-offs.

## 2. Ask one round

Ask 2–5 numbered questions, most important first. Only ask a question if its answer would change what you do or how you do it. Give every question a suggested answer, grounded in what you found, so the user can reply "all good".

Don't pad. If something has an obvious default, list it as an assumption instead of asking. If nothing would change the plan, ask no questions: post the **Goal** and **Done when** lines from step 3 with your assumptions and ask for a go-ahead. That counts as the round.

Format the round like so:

```
❓ **Q1** - **<question title>**: <short question, with options if that helps>

➡️ <suggested answer>

---

❓ **Q2** - **<question title>**: <short question>

➡️ <suggested answer>
```

After the questions, add one line of assumptions if you have any (`Assuming: …`), then close with:

> Reply "all good" to take the suggestions, or answer just the ones you'd change (e.g. "Q2: …").

Then stop and wait. Don't start the work in this turn.

## 3. Confirm and start

Read the user's reply. Any question they didn't answer keeps its suggested answer. Then write:

**Goal:** <one line on what the user is trying to achieve>
**Done when:** <one line, concrete and checkable>

Start the work right after, in the same turn. Don't ask for a go-ahead.

There's no second round. The only exception is an answer that would really change the plan: a different deliverable or scope, answers that conflict with each other, or an answer that contradicts what you found in the code. Then ask just those follow-ups (two at most) in the same format before restating the goal.
