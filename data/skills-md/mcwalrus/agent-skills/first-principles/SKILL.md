---
name: first-principles
description: >
  First-principles reasoning: strip a problem to its irreducible, verifiable
  truths, discard inherited assumptions, analogies, and convention, then rebuild
  a conclusion from the fundamentals up — with every layer made visible. Use when
  the user says "reason from first principles", "first-principles reasoning",
  "strip this to fundamentals", "what do we actually know to be true here", "why
  do we really do it this way", "question the assumptions", or /first-principles.
user-invocable: true
---

# First-Principles Reasoning

Strip a problem down to the things that are actually, verifiably true — then
rebuild the answer using only those. Inherited assumptions, analogies to past
cases, and "that's how it's done" are the borrowed reasoning this skill exists
to remove. Success is a conclusion that rests on bedrock the agent can name, not
on convention it absorbed. When the steps below run out, reason from this: every
claim in the final answer must trace to something you can show is true.

## Values

- **Truth over consensus.** A belief being widely held is not evidence it is
  fundamental. Weight what can be verified over what is commonly assumed.
- **Depth in context to the problem.** The right floor is relative: decompose to
  the bedrock *this* problem rests on, and stop when going deeper would not change
  the conclusion. Over-decomposing a product call down to physics is as much a
  failure as stopping at the first comfortable assumption.
- **Honesty about what survives.** A premise that cannot be verified is an
  assumption that remains, not a proven truth. A conclusion resting on one must
  say so.

## Constraints

- Never accept "that is how it is done", "best practice", "industry standard",
  or "it worked before" as a fundamental. These are the inherited layer — the
  thing being stripped, never bedrock.
- Never manufacture contrarianism. First-principles reasoning often confirms the
  conventional answer. Arriving back at it via independent rebuild is a finding,
  not a failure — the goal is a foundation, not a different answer.
- Never hide the decomposition. The discarded assumptions and the surviving
  fundamentals must both be visible in the output, not just the conclusion.

## Workflow

1. **Frame the question precisely.** State what is actually being decided or
   understood. A fuzzy question cannot be decomposed — sharpen it first.
2. **Surface the inherited layer.** List the assumptions, analogies,
   conventions, and received wisdom currently shaping the answer. You cannot
   discard what you have not made visible.
3. **Decompose to fundamentals.** For each item, ask whether it is *necessarily*
   true or only *contingently* true (true given other assumptions). Keep asking
   "how do we know this?" until you reach something irreducible.
4. **Discard what does not survive.** Name the assumptions that fail the test as
   explicitly discarded, so the reasoning stays auditable.
5. **Rebuild from the fundamentals.** Construct the conclusion using only what
   survived. Where the rebuild diverges from the conventional answer, that
   divergence is the payload — examine it rather than smoothing it away.
6. **Check the foundations.** Verify each "fundamental" is genuinely irreducible
   and not a deeper assumption in disguise. If one cracks, return to step 3.

## Calibrating Decomposition Depth

The appropriate depth is set by the problem, not by a fixed number of "why"s.
Find it deliberately rather than defaulting to shallow or bottomless:

- **Floor = what the problem rests on.** Decompose until you reach the truths the
  decision actually depends on — the domain's bedrock, not the universe's. A
  scheduling question bottoms out at throughput and deadlines, not thermodynamics.
- **Stop when depth stops paying.** When one more "how do we know this?" no longer
  changes the conclusion or surfaces a new lever, you have hit the right floor.
- **State the floor you chose.** Make the depth a visible decision in the output,
  with one line on why that level fits the problem.

## Output Format

Produce a reasoning artifact with these sections, in order. Each has a fixed
shape so the decomposition stays auditable — but scale the number of items and
the depth to the problem; never pad to fill the structure.

### Question
The sharpened framing — what is actually being decided or understood.

### Decomposition depth
The floor you decomposed to and why it fits this problem: the bedrock the question
rests on, and what told you to stop there. One or two lines.

### Inherited assumptions
A list. For each:
- **Claim** — the assumption as it was shaping the answer.
- **Type** — analogy, convention, received wisdom, or unexamined constraint.
- **Verdict** — *survives* (becomes a fundamental) or *discarded*, with the
  one-line test result that decided it.

### Fundamentals
The irreducible truths that survived. For each:
- **Truth** — the claim, stated plainly.
- **Basis** — how it is known: definition, physical limit, verified fact, or hard constraint.
- **Load-bearing because** — what in the conclusion rests on it.

### Rebuilt conclusion
The answer built from the fundamentals alone. Flag any premise that remains
unverified as an open assumption. Where the rebuild diverges from the conventional
answer, state the divergence rather than smoothing it away.
