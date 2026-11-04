---
name: ready-ticket
description: >-
  What makes a ticket ready for an agent to build without further input: a durable brief with behaviour,
  the technical design, done checks with evidence, scope, and blockers. Use when writing a ticket for agent pickup,
  turning a rough ticket into a ready one, or checking whether a ticket is ready to build.
disable-model-invocation: false
metadata:
  credit: "Adapted from Matt Pocock's triage AGENT-BRIEF.md, github.com/mattpocock/skills (MIT, (c) 2026 Matt Pocock)"
---

# Ready ticket

A ticket is ready when an agent can build it, prove it, and stop, without asking anyone anything.
A ready ticket provides the authoritative specification the agent works from.

Note that some tickets might be questions, investigations, placeholders, or actions other than development.
They're still fine as tickets; this spec doesn't apply to them.

## Principles

### Durability over precision

The ticket may sit ready for days or weeks. The codebase will change in the meantime.
Write the brief so it stays useful even as files are renamed, moved, or refactored.

- **Do** describe interfaces, types, and behavioral contracts
- **Do** name specific types, function signatures, or config shapes that the agent should look for or modify
- **Don't** reference file paths: they go stale
- **Don't** reference line numbers
- **Don't** assume the current implementation structure will remain the same

Durable references are fine: a spec or design document, a parent ticket, glossary terms, ADRs.

### Behavioral, not procedural

Describe **what** the system should do, not **how** to implement it step by step.
The agent will explore the codebase fresh.

- **Good:** "The `SkillConfig` type should accept an optional `schedule` field of type `CronExpression`"
- **Bad:** "Open src/types/skill.ts and add a schedule field on line 42"
- **Good:** "When a user runs `/triage` with no arguments, they should see a summary of issues needing attention"
- **Bad:** "Add a switch statement in the main handler function"

### The design travels with the ticket

A ticket is often one part of a larger change, designed and vetted with the user beforehand.
Give the builder that design, so it builds to it rather than redesigning:
the interfaces, types, and data shapes, where the change sits (named modules or components, not paths),
and the decisions behind them, with why.
Put it in the ticket, or reference the spec or design document that covers it, wherever the project keeps those.
When the ticket is part of a larger change, always reference that change's spec or design document.

A ticket isn't ready if its design can't be built as written.
If the code has moved on or the design doesn't fit, the builder stops and reports why rather than redesigning.

Anything the design leaves open is either a question that makes the ticket not ready,
or explicitly left to the builder's judgement, and named as such.
Context that's available in the repository, such as glossary and ADRs, need not be re-stated.

### Done checks with evidence

The agent needs to know when it's done, and supervisors need to be able to verify it.
Every brief has concrete done checks. Each is independently verifiable, and names the evidence that shows it passed:
a test, a command and its output, a screenshot, a measured number.

Tests alone aren't enough evidence for user-visible behaviour: state how to see it working on the real surface.
State the edge cases that matter as their own checks.
Checks shouldn't depend on whether or not the work has been committed yet.

### Explicit scope boundaries

State what is out of scope. This prevents the agent from gold-plating or making assumptions about adjacent features.

### Sized for one session

A ready ticket fits in a single fresh agent session.
If it doesn't, split it, and record the blocking edges between the parts.

Scale the brief to the change. A small, fully specified change needs a few lines and a check or two,
not every field written out at length.

## Template

Write this into the ticket, in whatever fields or structure the project's tracker uses.

```markdown
**Summary:** one-line description of what needs to happen
**Context:** the spec or design document for the larger change, parent ticket

**Current behavior:**
Describe what happens now. For bugs, this is the broken behavior.
For enhancements, this is the status quo the feature builds on.

**Desired behavior:**
Describe what should happen after the agent's work is complete.
Be specific about edge cases and error conditions.

**Design:**
The technical design for this ticket, or a reference to the section of the design document that covers it:
- `TypeName` / `functionName()` / config shape: what changes and why
- Decision already made, and why
- Builder's call: anything explicitly left to the builder's judgement

**Done checks:**
- [ ] Specific, testable check 1. Evidence: what shows it passed
- [ ] Specific, testable check 2. Evidence: what shows it passed

**Human review:** none, or what a person must look at before this is accepted (for example, a UI change)

**Out of scope:**
- Thing that should NOT be changed or addressed in this ticket
- Adjacent feature that might seem related but is separate

**Blocked by:** tickets that must be done first, or "none"
```

**Desired behavior**, **Done checks**, **Out of scope**, and **Human review** are required;
write "none" where that's true.
Omit other fields when there's nothing to say.

## Is it ready?

A ticket is ready for building when every answer is yes:

1. Does it fully describe desired behavior?
2. Does every done check name its evidence, and could an agent produce that evidence without asking anyone?
3. Is the design settled, in **Design** or by reference, with anything open explicitly left to the builder,
   and can it be built as written?
4. Is scope bounded, with **Out of scope** stated?
5. Does it fit in one fresh session?
6. Are all blockers closed?

If not, say which answers are no and what's missing. Don't fill gaps with guesses.
