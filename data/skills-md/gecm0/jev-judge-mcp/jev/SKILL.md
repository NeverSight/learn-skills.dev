---
name: jev
description: >
  Designing a call to TypeSafe's Jev: writing questions that survive the one-second test,
  splitting a multi-factor judgment into factors, fanning out speculative questions in one
  request, and turning probabilities into a decision. Read it before calling the judge tool, and
  when a call came back with low confidence or an answer that looks wrong.
  For writing application code that calls TypeSafe, use typesafe-ai instead.
---

# Designing a Jev call

Jev is for the **close call**. The `judge` tool description says when to reach for one; this file
is how to turn it into a call worth making.

## The one-second test

Every question must pass this before you send it: **could a well-informed person, with this
evidence in front of them, answer at a glance?**

If it needs reasoning, it is not a question yet. It is a decomposition you have not done.

| Instead of | Ask |
| --- | --- |
| "Analyse this message and determine the best course of action" | "Does this message convey urgency?" |
| "Score this startup pitch" | market size, technical feasibility, differentiation, as three questions |
| "Is this PR ready?" | test coverage, migration risk, scope creep, as three questions |

Split a multi-factor judgment into its factors and combine them yourself. The payoff arrives on
the day the result is wrong: you change a weight, not a prompt. Your weights stay inspectable;
Jev's judgments stay reusable.

**Ask the factors and stop there.** Adding "and which is best overall?" alongside them looks free,
and it is the answer you will then quote. It comes back mushy, because it is the compound question
you just decomposed, wearing a fresh ID. Compose the verdict yourself from the sharp answers.

## Fan out

An extra question costs its own tokens and almost no latency. TypeSafe's parallel-questions
cookbook measures 13 questions in one call against 13 separate calls: **11.5x cheaper, 9.6x
faster**, identical answers.

That economics changes the default. Carry **speculative** questions you may not end up needing:

- Ask the severity question even when the item may not be a bug. If it is not, drop that answer.
  Uncertainty on a branch you did not take costs nothing.
- Each question is evaluated alone against the same state, so carry its premise inside its own
  instructions: "If this is a defect, how severe is it?"
- Adding or removing a question leaves every other answer unchanged. There is no context rot here
  and no hidden ordering.

**A second request is the exception.** Chain only when you cannot build it without the first
answer: you must fetch more data, the answer decides the next set of options, or it defines what
the new state is. A question you could have asked against the original state belonged in call one.

## Shaping state and questions

**`state` holds facts. `questions` hold the logic for judging them.** Criteria drifting into the
state, or facts into a question, means the separation broke.

**Point at the state with backticked paths.** With JSON state: "Is the refund requested in
`ticket.messages[0].text` justified, given `order.charges`?" It tells Jev which part to judge.

**Carry the whole meaning in `instructions`.** Question IDs are keys for you; Jev never sees them.

**Give every `choice` a no-match option.** Jev picks from what you offer, so an incomplete list
forces a wrong answer into it. Before asking, confirm the real answer is among the candidates.

**Assembling the slate is your job, not Jev's.** It ranks what you hand it and cannot invent the
option you failed to think of. When the hard part is producing good candidates, that work happens
before the call.

**Rank many items with a `score` each, not one `choice`.** Choice returns a single winner and
splits its probability mass across rivals, so five decent candidates all land near 0.2. A
comparable per-item score gives every item a position you can sort, threshold and re-weight
without another call.

**Write score levels that stand alone.** "Broken functionality with an available workaround" beats
"medium". Each level must be readable without the others.

**One criterion names one state of the world.** "An unfamiliar token that tells a developer
nothing, and the name should describe the capability instead" is two claims, so Jev cannot place
evidence that satisfies one and not the other. Keep your reasoning in the instructions; leave the
criteria as plain descriptions of what is the case.

**Use structured objects or arrays** for `instructions` or `criteria` when a definition, contrast,
exclusion or example sharpens them. Plain strings are fine for simple questions.

## Turning probabilities into a decision

Scale the bar to what the answer will do. Tune these against real cases; they are a starting
shape, not constants:

| Consequence | Rough bar |
| --- | --- |
| Discard the genuinely uncertain | below 0.5 |
| Reading, reversible, cheap to redo | act above roughly 0.5 |
| Writing, destructive, hard to undo | above roughly 0.9, or ask the user |

**Low confidence is a debugging signal.** Low on one input means that input is ambiguous. Low on
*every* input means the design is wrong: options overlap, one question mixes several dimensions,
or the state lacks the evidence needed to answer. Systematic low confidence is your bug, not the
model's.

**On a slate you wrote yourself, low confidence is a verdict on the slate.** Jev spreading 0.49,
0.26 and 0.24 across your three candidates is not weak evidence about the world. It is saying the
three are interchangeable. Read it as "go find a better option", not as "the winner squeaked
through", and never promote a 0.49 into a recommendation on its own.

## Budget

About **32k tokens per request**, shared between the state and the longest question, roughly 150k
characters of English. The service enforces it.
