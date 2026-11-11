---
name: architecture-principles
description: 'Architecture principles for manifest-dev: how its maintainer wants skills, wrappers, references, state and the workflow structured, and why. Use before planning, designing, building or reviewing a new skill or entry point, a change to where state or a decision lives, how skills call or coordinate with each other, or a wait or loop a workflow can enter.'
---

Edit rule: each line is a principle with its reason and when it yields. Decisions go to the
decision records, rules a check can hold go to the check, and a line is added only on a person's
yes, after sharpening an existing line is ruled out.

- A new need lands on a mechanism, concept and state owner that already exist — figure-out, define, do, task files, the logs, the Ticket — before it earns a new skill, setting, file, ledger or surface, and a named entry is at most a thin wrapper that routes and restates no rule — a second loop or record is a second place to drift and disagree, every added concept is one more thing each user learns, and a rule in a wrapper reaches only runs that start there. Yields when no existing owner can carry it without changing what it means, or when people reach for a name: then add only the wrapper.
- Ship skills as the protocol, never the platform: no scheduler, hosting or host-bound runner; start from what the user already runs, use a host capability where it is offered and a plain path where it is not — infrastructure ties the project to one host and adds complexity each user carries. Yields to a coordinating skill, started by hand or by the user's own scheduler, when the alternative leaves users to build the machinery themselves.
- A skill that inspects or reports stays blind to its caller's workflow and returns what it saw with hints that name an action on the thing inspected, never a step of the caller's workflow; each decision lives once, in the skill that holds the context to make it — the caller steers toward the hint, a fixed set alone cannot cover the unexpected, and a rule restated per caller drifts. No yield has been stated beyond the verdict itself, which stays fixed.
- Every wait or loop a workflow can enter has a stated exit — done, a bounded retry, or a named person — reading the prose missed these: they surfaced as a landing that stalled for good and an escalation that fired every tick. No yield has been stated.

Before calling architecture work done, check it against these principles from a fresh start — a new
session, or a reviewer who did not do the work. Fix what departs unless the person chose the
departure, and check again only after a fix, until a check finds none. Name each departure kept,
with the principle and why.
