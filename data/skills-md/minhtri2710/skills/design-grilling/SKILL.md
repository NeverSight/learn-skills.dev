---
name: design-grilling
description: Interview the user until a plan, design, or underspecified ask reaches confirmed shared understanding. Use when the user asks to be grilled or interviewed, or to stress-test a plan or decision. Do not use in non-interactive runs or for asks that are already unambiguous.
---

# Design Grilling

Reach a shared understanding the user explicitly confirms, before any spec, plan,
or code. Facts are your job; decisions are the user's.

## Open with a hypothesis

State your current read of what the user wants in one sentence with an honest
confidence number. Below about 70%, name on the same line what is still missing:
who benefits, why now, what success looks like, or the binding constraint.

## Work the design tree in rounds

Map the ask as a design tree: each decision branches into the decisions that hang
off it. The frontier is every open decision whose prerequisites are settled. Ask
the whole frontier in one round, numbered, each question with your recommended
answer and the reasoning behind it, then wait. A question that depends on another
question still open this round belongs to a later round.

```
Q1 - <title>: <question, with concrete options when they exist>
Recommended: <your answer and why>
```

When a frontier question needs a fact from the code, docs, or environment, look it
up or dispatch a subagent instead of asking the user; only the questions downstream
of that lookup wait for it. Put every decision to the user and wait for their
answer. Recompute the frontier after each round.

When an answer echoes convention or best-practice vocabulary ("scalable", "the
standard way", "I should probably") instead of a concrete outcome, ask what they
would want if they did not have to justify it to anyone. Guess occasionally in a
direction you expect them to reject, so agreement stays informative.

## Stop test

The frontier is empty and you can predict the user's reaction to the next three
questions you would ask. If several rounds pass without confidence rising, say so
and ask whether something foundational is missing.

## Restate and confirm

```
Outcome:      <one line>
User:         <who benefits>
Why now:      <what changed>
Success:      <how we know it worked>
Constraint:   <the binding limit>
Out of scope: <what is explicitly not being built>
Decisions:    <one line per settled decision>
```

The gate is an explicit yes to this restate. "Whatever you think" is delegation:
re-ask as a choice between two concrete options. "Sounds good" or "sure, let's go"
gets one follow-up asking what they would refine. Fold corrections in and restate
until the yes is explicit. Act on the understanding only after that yes; save it to
a file only when the user asks.
