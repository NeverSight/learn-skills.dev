---
name: comms-review
description: >-
  Review a drafted communication before delivery to humans. Use when writing human-facing
  communications such as documents, reports, website copy, and READMEs, once a draft is complete,
  at review time.
---

# Comms Review — make the draft ready to deliver

The goal of communication is to make yourself understood by your audience so that you can achieve
your goals together. A communication that fails to serve this purpose is a waste of time, effort
and tokens for both parties. It is therefore worth the effort to ensure that a communication will
land, by reviewing it to the best of your ability, and repeatedly fixing any issues you can find,
such that there are no more issues that you can discover before sending it. This skill gives
detailed instructions about how to do this to best mitigate common failure modes.

This skill is aimed at fixing defects in the *contents* of communications. It is not primarily
focused on changing or improving style. It also does not override any house style conventions — if
they exist, you must apply both these content rubrics and house style conventions when reviewing.

**Above all, do your best to make the communication achieve its objective. The following are all
rubrics intended to help you in this goal, not ends in themselves.**

Review notes, reviewer prompts and returns, and superseded drafts are working state. Keep them in
your own scratch space or in context, never in the workspace or files you will return to the
reader. The current draft is the artifact under review; revise it in place.

For routine, low-stakes replies, the quick preparation and self-review in `/comms-prep` is enough.
For a cosmetic correction to an already reviewed communication, proofread the change; a new brief
or audience review is unnecessary. Judge by effect on meaning, not edit size: a changed number or
negation is not cosmetic. Otherwise, follow the phases below.

## Phase 1 — Pick up the prep, or do it now

The review relies on there being a brief about the communication's objective and audience. The
companion skill `/comms-prep` writes this brief. In this phase, you will look for an existing brief
and check whether it is adequate. If an adequate brief doesn't exist, you will have to make a call
to `/comms-prep` to prepare it now, from the draft's intended purpose. The brief tells you the
objective, the audience and their context, the terms the reader can use, key points about the
source meaning, the form factor and structure draft, and the style conventions and skills that
apply.

## Phase 2 — Review against the rubric

In this phase, you will do a manual self review against the content checks. Read
[Content checks](references/content-checks.md) now and run every check there over the complete
delivery, starting with source meaning. Revise in place, and recheck after every substantive
revision.

## Phase 3 — Audience review

It is very hard to self-review for some of the content checks consistently, because you already have
in your head what the audience doesn't know. Therefore it is important to have an independent agent
simulating the reader's perspective review the communication.

Read [Audience review](references/audience-review.md) and carry it out: a fresh reviewer each
round, a prompt containing exactly what it lists, and its PASS and FAIL rules, which end the loop
with one final round after a second FAIL.

## After Phase 3 — finalize

Deliver only the communication selected by the final review. After the final PASS, proofread
cosmetic corrections locally. Changes that could affect the reader's understanding or action
require the affected Phase 2 checks, including source meaning, and reopen Phase 3 as a new first
round.

Before returning, look at every file and message you are about to return. It contains the
requested communication and nothing else: no brief, no rubric notes, no reviewer prompts or
returns, no revision history, no audit text. If audit, provenance, or decision history is
explicitly part of the user's objective, produce it as a separate communication with its own
audience.

The chat handoff says what was delivered and any material limit. It does not describe the review
that produced it, claim a pass that did not happen, or imply that something was built when only a
specification was written.

## Maintainer reference

The content rubric lives in [Content checks](references/content-checks.md).

To extend the standard, append a new failure mode and rubric row. Change an existing row only with
the standard owner's decision. Do not redesign the standard through an extension.
