---
name: find-your-level
description: >
  Judgment placement for CORE / PM. 14 scenarios, two per phase, scored on
  reasoning rather than recall, mapped to an entry point and a per-phase
  Skip/Review/Do status. Usually run by start-learning, but can be run alone.
  Trigger phrases: "find my level", "placement quiz", "where should I start",
  "test my product judgment", "am I ready for this course".
license: MIT
metadata:
  version: 1.0.0
  tags: [placement, assessment, product-management, diagnostic]
---

# Find Your Level — CORE / PM

You are administering the CORE / PM placement. It measures **judgment**, not
vocabulary. A PM who can define opportunity cost but funds the loudest request
should place into Product Judgment, not out of it.

There are 14 scenarios: two for each of the seven phases. Two scenarios per
phase is what makes a per-phase status trustworthy. One right answer can be a
guess. Two right answers, with reasoning, is a pattern.

Every scenario uses the shared Noted case. The learner needs no knowledge of
their own product to answer.

## Answer-isolation contract

This contract is not optional. Violating it destroys the placement's value.

- Load `references/placement.md` to get the scenarios. It also contains the
  strongest answer and the rationale for each one.
- **Never reveal the strongest answer, the rationale, or the score band before
  the learner has answered that scenario.**
- Never hint at the answer distribution ("it's usually C", "not the obvious
  one").
- In reply-format instructions, use neutral placeholders only. Write
  `Reply with one letter: <A|B|C|D>.` Never substitute a real option letter into
  that example.
- Ask one scenario at a time. Do not show scenario N+1 until scenario N is
  answered.
- Do not give a verdict after each answer. Hold all 14 verdicts until the end.
  Early feedback teaches them the pattern for later scenarios.
- The two scenarios in a phase are related. Never say how the first one went
  before they answer the second.

## The Noted case in one paragraph

Give this once, before scenario 1. Do not repeat it:

> Noted is an AI-assisted document product. Four signals are live at once:
> activation fell 11% in six weeks; three enterprise customers requested
> automated meeting summaries; P95 response time rose 34% for large workspaces;
> and a platform dependency loses support in 10 weeks. The evidence is
> intentionally incomplete. Every question below sits inside this situation.

## Delivery

1. Say what this is: 14 scenarios, about 20 minutes, no preparation needed. A
   low score costs them nothing. It only changes where they start.
2. Ask all 14 in phase order, PF through LD, one at a time. Inside a phase, ask
   the first scenario before the second.
3. If the environment has a structured question/option tool, use it. Otherwise
   present lettered options as plain text and wait.
4. Accept a letter, or a written answer that clearly matches one option. If the
   answer is genuinely ambiguous, ask them to pick a letter — do not guess for
   them.
5. If they explain their reasoning alongside the letter, keep the explanation.
   It is more diagnostic than the letter, and Step 5 uses it.

## Scoring

One point per scenario, no partial credit. The total is out of 14.

Per-phase status comes from that phase's own two scenarios, never from the
total:

| That phase's two scenarios | Status for that phase |
|---|---|
| Both correct, and the reasoning named the right trade-off at least once | `Review` |
| Both correct, but letters only or thin reasoning | `Do` |
| One correct | `Do` |
| Neither correct | `Do` |

Two correct answers with no reasoning is still `Do`. The course teaches
reasoning, so a learner who cannot say why they were right has not shown the
thing being placed.

Problem Framing is special. **PF is never `Skip`.** Two correct PF scenarios
with reasoning make it `Review`. Anything else makes it `Do`. Its six lessons
are the shared vocabulary that every later phase uses, so skipping them breaks
later lessons.

The entry point is the **first** phase in order (PF, PJ, EV, ST, TJ, DS, LD)
whose status is `Do`. If every phase is `Review`, the entry point is PF and the
route is a fast pass. Say that plainly.

Total score bands, used only for the summary line:

| Score | Read it as |
|---|---|
| 0–4 | The rituals are familiar. The reasoning underneath is not. Full foundation. |
| 5–8 | Good instincts, with gaps that show up under pressure. Foundation, with some fast passes. |
| 9–12 | Strong judgment, uneven across domains. Target the `Do` phases. |
| 13–14 | Either genuinely senior, or lucky. Suggest `check-understanding` on any phase to confirm. |

Never present the band as a verdict on them as a PM. It is a routing decision.

## Step 5 — Report

Give the learner, in this order:

1. Their score as `N/14`.
2. A short table with one row per phase: phase, their two answers, how many were
   correct, and the resulting status.
3. For each scenario they got wrong, the strongest answer and the one-line
   rationale from `references/placement.md`. This is the only moment when
   answers become visible.
4. Their entry point, and one sentence on why.

## Handing back

If `start-learning` invoked this skill, return the per-phase statuses, the
entry point, and the score. Do not write `PM-LEARNING.md` yourself — that file
belongs to `start-learning`.

If the learner ran this skill directly and no `PM-LEARNING.md` exists, close by
offering `start-learning` to turn the result into a plan, rendered with the
host's invocation syntax:

- Claude Code: `/start-learning`
- Codex: `start-learning`
- Other hosts: `Use start-learning to build my plan.`
