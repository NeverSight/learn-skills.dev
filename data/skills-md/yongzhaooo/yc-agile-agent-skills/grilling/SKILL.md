---
name: grilling
description: Use only when the user explicitly invokes grilling or asks for an exhaustive interview to stress-test a plan, decision, or design. Do not trigger from an ordinary planning or implementation request.
---

Run the requested exhaustive interview until we reach a shared understanding. This is an
opt-in workflow; ordinary work needs only questions whose answers materially affect the
result. Model the discussion as a **design tree**: every decision branches into the
decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are
already settled — the questions you can ask now without guessing. Ask the whole frontier
in one round, using a compact text table to compare the directions and trade-offs. For
each decision, normally give three materially reasonable options; use fewer when fewer
actually exist, and never pad the table with a strawman. Mark one option as recommended
and explain why. Number each question with a round-prefixed label (R1-Q1, R1-Q2, ...,
R2-Q1, R2-Q2a, ...) so labels are unique across the entire session.

Each round reshapes the tree. Settled decisions push the frontier outward and unblock questions that depended on them. A question whose answer depends on another question still open in the same round belongs to a later round, not this one.

State that unanswered questions in a partial reply will use their recommendations.
When the user answers only part of a round, record those answers, adopt the stated
recommendations for unanswered questions, and advance the frontier without asking again.
Briefly identify the defaults used; “the rest as recommended” applies to all remaining
questions in the round. Never repeat a question that has already been answered. If no
response arrives, pause the interview: silence or elapsed time is not an answer and
never authorizes an external, destructive, or other consequential action.

If a *fact* can be found by exploring the environment (filesystem, tools, etc.), look it up rather than asking me. A running lookup is an unsettled prerequisite: only the questions that depend on it wait, and the rest of the frontier goes out now. The *decisions*, though, are mine — put each one to me; apply the partial-round rule above when I answer only some of them.

Ground consequential choices in an observable outcome and one realistic failure or
boundary case when it could change the answer. Keep confirmed decisions, defaults,
and unresolved facts distinct; do not turn this into a separate reporting ritual.

Stop when the frontier is empty and no material branch remains silently assumed. Keep the
interview finite: do not invent extra questions, reopen settled decisions, or continue
after convergence. The interview itself does not authorize writing a spec, implementation,
or external actions. Preserve authority already supplied in the conversation: after
convergence, continue any already-authorized work without another confirmation round;
otherwise return the settled decisions and material open questions.

## Lessons

- Round-prefixed labels exist for a reason: plain `Q1/Q2/Q3` got reused across rounds and sub-labels like `Q2a` cross-contaminated, so decisions could no longer be traced to the round that raised them.
- A settled frontier does not expand authority; it also does not cancel work the user has already authorized.
- Exhaustive interviewing is an explicit choice, not the default response to an open decision.
