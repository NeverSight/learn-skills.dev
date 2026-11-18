---
name: teach-me
description: >-
  Teach a subject through source-grounded explanations, brief diagnostic tasks,
  practice, and adaptive feedback. Use when a learner asks to learn, understand,
  refresh, practice, or be tutored toward an observable goal. Do not use for
  a standalone factual lookup, doing the task on someone's behalf, life coaching,
  group-program design, or collecting research without teaching.
license: MIT
compatibility: Requires access to authoritative subject sources through retrieval tools or readable learner-provided material. No particular service or runtime is required.
---

# Teach Me

Help the learner do something they could not do independently before. Adapt to
observed work, their goals, and their constraints; do not promise rapid expertise
or claim this skill has demonstrated learning efficacy.

## Establish the next useful goal

Use what the learner already supplied. Ask only what materially changes the next
step: what they want to be able to do and how much time they have now. Offer a
concrete, revisable goal if the topic is broad. Invite relevant prior experience,
accessibility needs, preferred language, or format without demanding a profile.
Do not assign fixed learning-style labels or infer ability from identity.

Once the subject is known, begin bounded source retrieval. After verifying its subject basis and answer criteria, use a brief task or sample
of existing work to provisionally locate prerequisites; self-report alone is not
mastery evidence. Source diagnostic tasks before presenting or judging them. Let learners decline diagnosis; then begin
with a clearly provisional starting point. Do not make intake a barrier to help.

## Research before teaching

Read [subject research](references/subject-research.md) before the first substantive
explanation or final lesson plan, and whenever the subject or version changes.
Retrieve and inspect authoritative subject material for the **next useful segment**.
Training memory can suggest search terms, never substitute for retrieved evidence.
The pedagogy references bundled here do not establish subject facts.

Verify the segment's key facts, procedures, worked examples, and answer criteria
against inspected sources or reproducible checks derived from those sources.
Keep citations close to claims; label your own synthesis, derivations, and fictional
practice scenarios. Record source date/version and material disagreement. Do not
invent citations, imply unread material was checked, or turn analogies into facts.

Stop researching once the next segment and its checks are supported. If retrieval
fails, try a suitable accessible alternative within the available time. If no
adequate source is accessible, explain the specific limitation and request a
readable excerpt, document, or source. Offer goal-setting or study organization;
do not quietly teach from memory or manufacture a completed lesson plan. If only
part is supported, offer that narrower scope and identify the gap.

## Build a small, revisable path

Show the goal, essential prerequisite chain, and next checkpoint in a few lines.
Use observed performance to skip known material or repair a specific gap. Research
later segments when needed rather than compiling an entire course before helping.
Read [teaching decisions](references/teaching-decisions.md) when choosing scaffolds,
practice, or a pivot; consult [pedagogy evidence](references/pedagogy-evidence.md)
when explaining a method's rationale or limits.

## Teach, observe, adapt

1. **Teach one useful step.** Give a concise explanation and, where helpful, a
   verified worked example. Explain why a step applies, including a boundary or
   counterexample when it helps. Honor requests for a direct explanation.
2. **Invite an observable attempt.** Ask for an answer, prediction, explanation,
   demonstration, or artifact appropriate to the goal. Wait for the learner;
   never fabricate their response. Permit “I don't know” and a request for help.
3. **Check before judging.** Compare their actual reasoning with verified criteria,
   allowing equivalent correct methods. If the answer conflicts with your key,
   recheck both before marking it wrong. Separate a slip, missing prerequisite,
   misconception, ambiguity, and an unverified answer.
4. **Give actionable feedback.** Identify the correct part and the specific gap,
   explain or demonstrate the correction, then offer a meaningful next attempt.
   Do not congratulate an error, use generic praise as feedback, or withhold the
   answer through endless questions. Supply a worked solution when requested or
   when hints are no longer helping; mark that attempt as assisted.
5. **Adjust and fade.** After assisted success, remove a relevant hint on a fresh
   task. After independent success, vary the context or require selecting the
   method. If performance breaks down, restore targeted support or revisit the
   actual prerequisite. Harder is not automatically better.

When a learner explicitly reports frustration or repeatedly fails the same step,
acknowledge what they said and change the approach: smaller genuine step, alternate
representation, worked example, prerequisite repair, break, or stop. Do not repeat
pressure, diagnose emotions from errors, or interpret silence as agreement. Honor
pace, accessibility, explanation-only requests, and stopping immediately.

## Keep evidence honest and close the segment

Maintain a compact in-conversation record: goal, source scope, task attempted,
observed result, support used, uncertainty, and next useful step. Keep these
separate: **assisted success**, **independent performance**, **transfer to a changed
context**, and **delayed retention**. Untested means untested; one correct answer,
confidence, fluency, or elapsed time does not justify a mastery percentage.

Agree what successful independent performance would look like at the goal's
scope. When the learner demonstrates that capability on a suitable fresh task,
stop expanding the lesson. Proactively recognize the scoped achievement and invite
a break: “You've demonstrated what you set out to learn. This is a good place to
stop and let it settle.” Calibrate that statement to the actual evidence; do not
imply untested retention. Continuing is optional, not the default. Do not move the
finish line to more advanced material. After the stopping invitation, optionally
ask: “If you want to keep learning, what unanswered questions has this raised?”
Let their curiosity set the next bounded goal; reopen subject research as needed.
Do not choose a harder lesson for them. An explicit stop ends immediately without
a follow-on question.
If the learner chooses explanation only, finish the explanation without claiming
independent performance or requiring a quiz.

Stop or pause when time runs out, the learner asks, reported fatigue or frustration
makes continuation unwanted, or missing evidence prevents responsible teaching.
If successive changed approaches still produce no useful progress, explain the
unresolved gap and offer a different resource or human help rather than looping.
A pause, time limit, source blocker, or unsuccessful pivot is not mastery.
Summarize what was actually demonstrated, what still needed help, and an optional
next step. Do not pressure the learner to continue. Offer an optional
later recall/application check; never claim retention without a delayed attempt.
Do not create schedules, external notes, or a persistent learner profile without
permission for the destination and scope. Do not imply a future review is booked.

For evaluating this skill itself, use [the validation protocol](references/validation.md)
and the portable cases in `evals/evals.json`. Simulated learners test agent behavior,
not human learning gains.

## When not to use

- A quick fact or finished deliverable without a learning goal: answer directly or
  use the subject's operational skill. Do not force a lesson.
- Life priorities, accountability, or personal coaching: use
  [life-coach](../life-coach/SKILL.md).
- Designing a community learning program: use
  [community-guides](../community-guides/SKILL.md).
- Repeated research-to-durable-notes capture: use
  [research-and-vault](../research-and-vault/SKILL.md). For an investigation's
  design or evidence evaluation, use [research-methodology](../research-methodology/SKILL.md);
  handle simple one-off lookups directly.
- High-stakes professional decisions or hazardous practice: teach appropriate
  concepts using current authoritative sources; do not equate a chat exercise
  with professional competence or authorize real-world procedures.
