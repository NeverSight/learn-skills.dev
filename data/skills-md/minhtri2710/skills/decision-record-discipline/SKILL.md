---
name: decision-record-discipline
description: "Keep a project's glossary current and record only the decisions and rejections worth remembering: terms in CONTEXT.md, decisions that pass a three-part gate where the project keeps them, and rejected concepts as one file each so they are not re-litigated. Use when a term is resolved or contested, a decision with real alternatives is made, or a request is ruled out of scope. Do not use for implementation notes, specs, or task tracking."
---

# Decision Record Discipline

Three kinds of knowledge evaporate at the end of a session: what a word means
here, why a surprising choice was made, and why a request was refused. Each gets
one home, written the moment it crystallises rather than batched.

## Glossary: CONTEXT.md

One `CONTEXT.md` at the repository root (a `CONTEXT-MAP.md` lists them when a
repository has several contexts), created when the first term is resolved. It is a
glossary and nothing else: no implementation detail, no scratch notes, no
decisions.

```markdown
**Invoice**:
A request for payment sent to a customer after delivery.
_Avoid_: bill, payment request
```

Be opinionated: pick one word per concept and list the others under `_Avoid_`.
Define what a term is in one or two sentences, not what it does. Include only
concepts specific to this project; a timeout or a retry is not a domain term.

During work, challenge usage against it: a term used to mean something the
glossary does not say, or two words for one concept, is surfaced at once and
resolved before code is written. Cross-check claims against the code and surface
contradictions ("the glossary says partial cancellation exists; the code cancels
whole orders").

## Decisions: where the project keeps them

Record a decision only when all three hold:

1. **Hard to reverse**: changing it later costs something real.
2. **Surprising without context**: a future reader would ask why it was done
   this way.
3. **A real trade-off**: genuine alternatives existed and one was chosen for
   reasons.

Easy to reverse means it will just be reversed; not surprising means nobody will
ask; no alternative means "we did the obvious thing", which needs no record. What
qualifies: architectural shape, integration patterns between contexts,
technology with lock-in, ownership and boundary decisions, deliberate deviations
from the obvious path, constraints invisible in the code, and rejected
alternatives whose rejection is non-obvious.

A decision lives where the project says: a comment at the code that enforces it,
a rule in `AGENTS.md`, or the project's ledger. Write a separate record only when
no code or rule can carry it, in the place the project names: one paragraph,
context, decision, why, with considered options or consequences only when they
carry weight. When a decision changes, rewrite it to say what is true now; there
is no status field or supersession chain, because a reader wants the current
answer, not the history of answers.

## Rejections: .out-of-scope/<concept>.md

One file per rejected concept, not per request, named so the directory can be
read without opening files (`dark-mode.md`, `plugin-system.md`). Each states what
the project does not do, why, what accepting it would require, and the requests
it answered. Before engaging a new request, check the directory by concept, not
by wording; a match is answered with the record instead of a fresh debate. The
record is rewritten when the reasoning changes, and deleted when the concept is
accepted.
