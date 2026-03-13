---
name: philosophy
description: Engineering philosophy and work culture principles. Load this skill when making architectural decisions or to understand the team's work principles.
---

# Philosophy

Engineering philosophy and work culture principles. This skill is meant to be loaded alongside the `style` skill to provide broader context for decision-making and collaboration.

## Guiding Principles

**Pragmatic over idealistic.**

Don't get fixed on details that don't matter. If you're unsure if a detail matters, ask.

**Simple is usually harder than easy, but it pays off in the long run.**

**Engineer Hippocratic Oath** - Do no harm to our customers and their data.

**Benevolent Dictatorship** - All ideas are welcome, but not all will be acted upon. We've got work to do.

**"The map is not the territory"** - Documentation is there to guide you to the code, which is the source of truth.

## Collaboration & Communication

Don't be afraid to ask questions.

**Direct Messages are for secrets.** Unless it's private, keep talking to people in public. It helps the rest of the engineers learn.

Don't be offended when people ask you why you implemented something a certain way; if it's not your strongest solution, "it was the best solution I could put together with the information I had" is a fine answer.

**Respect and learn from your fellow engineer.**

Be careful of how much you judge other people's engineering decisions; there's a profound moment as an engineer when you look at something, think that it's totally insane that it was implemented that way, and then realize you're the one who implemented it but you've since forgotten.

## Code & Git Practices

For specific guidelines on commits, comments, and external code attribution, see the `style` skill.

Key philosophical points:

- **Commits should read like a story** - They're there for others and future-you to understand why a change was made
- **Keep your commit summaries clear and short** - Use the body if the change warrants further explanation
- **Don't intermix refactors and feature additions** - Keep them separate for clarity
- **Comments shouldn't describe what code is doing** - They should describe why you're doing it

See the `style` skill for detailed formatting rules and technical specifications.

## Constraint Ownership

Every system has layers. Constraints belong in exactly one layer — the one that has enough information to enforce them correctly.

When a downstream function re-checks conditions that an upstream function already guarantees, you get duplication that eventually conflicts. When callers pre-process inputs to satisfy invariants the callee already enforces, you get unnecessary complexity. When three layers all enforce the same rule, two of them are unnecessary and one of them is probably wrong.

Find the layer that owns the constraint. Fix it there. Trust it everywhere else.

**Before fixing a bug, answer these questions:**

1. What invariant is being violated?
2. Which layer is responsible for enforcing that invariant?
3. Does that layer already attempt to enforce it?

If the answer to (3) is yes, fix that layer — not a downstream consumer. If your fix requires changes in more than one module, stop and explain which layer owns the constraint and why.

If you have made two or more fix commits to the same subsystem without resolving the issue, you are symptom-chasing. Describe the constraint violation and ask where it should be fixed.

## Testing Philosophy

**Tests are primarily there to verify required behavior is being followed. They're your friend.**

Refactoring without them is a disconcerting nightmare filled with uncertainty and strife.

## Automation & Tools

**Automate when it's appropriate:** the first time might be too soon to understand the problem, by the third time might be when you should stop doing the same thing manually.

**Solving problems is so much easier with the right tools.** Don't be afraid of building tools.

## Business Context

**Without engineering, sales has nothing to sell. Without sales, engineering can't pay rent.**

This symbiotic relationship informs our prioritization and decision-making.

## Issue & Project Management

**Issues and tickets represent actual work to get done; not a hope or a dream.**

An issue should be self-contained enough that it can be handed off at any moment.

An issue shouldn't take longer than 2-3 days to implement.

A single feature can have many tickets; they're cheap, so use as many as makes things clear.

**The more status updates you put in your tickets, the less you'll be bugged by people asking you for status** (see TPS reports).

## Acknowledgment

After reviewing this skill, state: "I have reviewed the philosophy skill."
