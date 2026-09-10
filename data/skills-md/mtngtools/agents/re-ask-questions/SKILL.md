---
name: re-ask-questions
description: Re-ask the open questions from this session one at a time — each preceded by an overview of what's being asked and a pros/cons table per option with the recommendation clearly noted.
argument-hint: "Which questions to re-ask, if not the ones already on the table this session"
metadata:
  type: command
  invocation: skill-callable
  applies-to: [planning, questions, decisions]
---

# Re-Ask Questions

Take the questions already on the table — batched earlier, answered hastily, or listed in the arguments — and re-ask them **one at a time**. One question per round; wait for the answer before moving to the next. An answer may reshape or retire later questions, so re-check the remaining list after each round.

## Each round

1. **Overview first.** A short paragraph in plain prose: what this question decides, why it's open, and what hinges on the answer.
2. **The options table.** Every real option gets a row:

   | Option | Pros | Cons |
   |---|---|---|

   Mark the recommendation clearly — **(Recommended)** on its row — and say in one sentence after the table why it wins.
3. **Ask.** Use AskUserQuestion with the same options, the recommended one first and labelled **(Recommended)**. The overview and table go in your text *before* the tool call — the question UI can't hold them.

## Finish

When every question is answered, restate the decisions as a short list — question, answer, one line of consequence — so the session has one place to read what was settled.
