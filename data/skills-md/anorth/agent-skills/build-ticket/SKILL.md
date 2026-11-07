---
name: build-ticket
description: >-
  Builds one ready ticket through to a reviewed result with evidence, unattended unless the user asks to be in the loop:
  checks it's ready, builds to its design, runs its done checks, reflects, reviews, and reports.
  Use when the user asks to build, implement, or pick up a ticket.
disable-model-invocation: false
metadata:
  credit: "Adapted from Matt Pocock's implement skill, github.com/mattpocock/skills (MIT, (c) 2026 Matt Pocock)"
---

# Build ticket

Implement the work described by a ticket, and stop with a result the user can review:
built, checked, reflected on, reviewed, and with evidence for each done check.
Work unattended by default. Stop early only where this skill says to.

If the user asks to be in the loop (e.g. "with me", "let's collaborate"),
pause and ask them instead wherever this skill says to pick a default, make a significant decision,
or carry a question into the report. Continue with their answer.

## 1. Load the ticket

If the user passes a ticket reference, fetch it from the issue tracker and state its title before starting.
If the reference is ambiguous, ask.

Read the ticket in full, and the spec or design document its context points to.
Claim the ticket in the tracker, if the tracker supports that.

Skim other open tickets, and read the ones related to this one: for context, sequencing, and collisions.
Don't expand scope from them.

## 2. Ground in the code

Read the code the ticket touches, to know what the system does today.
Where the ticket and the code disagree, trust the code for what is true today.

## 3. Check it's ready

Run the readiness check in the `/ready-ticket` skill.
If any answer is no, stop: report which answers are no and what's missing, and release the claim.
Don't fill gaps with guesses.

If the user is in the loop, confirm the approach with them against the ticket's design and done checks,
and name anything still assumed. Wait for their confirmation.

## 4. Build

Build to the ticket's design. Keep it the minimum that meets the ticket.

For anything the ticket leaves to the builder, and forks that come up while building,
pick a sensible default, keep going, and note it for the report.

Always stop, rather than picking a default, when:

- the design can't be built as written (the code has moved on, or the design doesn't fit): don't redesign;
- the ticket turns out too big for one session: don't silently trim scope;
- a decision would change user-visible behaviour or be hard to reverse, and the ticket doesn't settle it.

Unattended, report why and hand off. In the loop, ask the user and continue with their answer.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

## 5. Run the done checks

Run each of the ticket's done checks and keep its evidence.
An inconclusive result, or evidence from the wrong surface, is not a pass: say so.
If a check can't be run as written and you adapt it, the adaptation is a decision: report it.

## 6. Reflect and review

Apply the `/reflect` skill, then the `/review-diff` skill.
Carry their open questions and design questions into the report.
Re-run any done check whose evidence the changes since step 5 could affect.

## 7. Hand off

Don't commit. Don't close the ticket: tickets close only when the change lands on `main`.
Add a short note to the ticket: what was built, the done-check results, and decisions you made.

Report to the user:

1. **Built**: the ticket's title, and what changed.
2. **Done checks**: each check with its result and its evidence, or where the evidence is.
3. **Decisions**: defaults you picked, builder's calls you made, and done checks you adapted.
4. **Open**: questions from reflection and review, and anything unfinished.
5. **Human review**: what the ticket asks a person to look at, if anything.
