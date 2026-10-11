---
name: comms-prep
description: >-
  Write yourself a brief about the communication's objective and audience in order to communicate
  more successfully. Use immediately before drafting human-facing findings, explanations,
  recommendations, decision requests, or text intended for publication or reuse. For example, use
  before writing human-facing READMEs, PR messages in public repos, tutorials, documentation,
  recommendations, error messages, reports, or website copy. If the communication will come at the
  end of a piece of work, do the work first and invoke the skill later — for example, finish the
  bug fix and then call comms-prep when you are about to explain what you did to the user. While the
  conversation and objective remain the same, you can reuse the existing brief rather than invoke
  the skill again to write a new one. Use retroactively when a draft exists without an adequate
  brief.
---

# Comms Prep — prepare before drafting

A communication's success depends on its being appropriate for its audience, meeting their needs,
and having a clear measure of success. This skill helps you prepare the information you need to
succeed. When a full review is justified, run `/comms-review` once your draft is written; your brief
supplies the objective, audience, context, evidence sources, and structure plan if appropriate. This
is useful both when you are drafting and for independent review agents.

**Be liberal: any time you are writing something for people, think comms-prep.**

## 1. Decide whether to reuse or prepare

**Adequacy.** A brief is adequate when its answers for objective, audience and context, knowledge
model, source content, form factor, and style conventions are accurate and complete for the
communication.

**Reuse.** While the conversation and objective remain the same, generally reuse an adequate
existing brief. You can amend an existing brief if something has changed and it is no longer
adequate. If the form is a back-and-forth communication, it is not necessary to prepare again for
each reply.

**Scale.** Scale the brief to the artifact. For a small artifact it may be four lines answered in
seconds: who reads this and when · what do you know that they don't · what must they understand ·
what would mislead them.

For a routine, low-stakes reply, answer those questions directly, draft, and self-review for the
objective, reader understanding, and source meaning. A written brief and `/comms-review` are not
required on this path. A reply is low-stakes when a misunderstanding would be cheap to correct in
the next exchange: the same test of objective, audience, and cost of failure that decides below
whether a full review is justified. Shortness alone does not make a message low-stakes; a short
message that reaches a wide audience, fixes a decision, or will be reused is not on this path.
Continue below for substantive or consequential communications.

**Authoring boundary.** Generally run this skill once you have finished working out the actual
information you need to communicate and immediately before drafting the substantive communication.
When the requested work is itself writing, that boundary is the start of drafting. When underlying
work must happen first, stay with that work until those answers exist; the fact that a report will
eventually follow does not move the boundary to task start.

**Retroactive use.** If a draft already exists with no brief, prepare the brief from the draft's
intended purpose rather than copying assumptions out of its text. Then make the brief and draft
available to `/comms-review`.

**Where it lives.** The brief is an artifact, not a thought: keep it available with the draft for
`/comms-review` reviewers, while keeping it outside the primary reader-facing communication. Keep
it in your own scratch space, in context, or as a brief summary directly in chat if appropriate.
Do not include the brief with the workspace or files for the audience; this would generally not
be appropriate.

## 2. Write the communications brief

Write a short brief. Read [Write the communications brief](references/brief.md) when creating or
materially amending one: it holds the six lines to answer (objective, audience and context,
knowledge model, source meaning to preserve, form factor, style and conventions), the structure plan
for multi-section and long documents, and the check to run before drafting. Then decide on review:

### Add a reminder to call `/comms-review`

Decide whether the communication is substantive enough to justify running `/comms-review` once it
is complete. `/comms-review` uses an audience-review loop to check that the communication meets its
objective and avoids common failure modes. Judge whether that work is proportionate by considering
the objective, audience, and cost of failure. In most circumstances, a few rounds of review cost
less than repeated back-and-forth with a confused human. They almost certainly cost less than
misleading a wide audience.

If a full review is justified, add a note to the end of the brief instructing the drafting agent to
invoke `/comms-review` when the draft is complete.

## 3. Unresolved questions

If a question arises during comms prep and you don't know the answer, ask the user when you can
get a reply this turn. Otherwise, note the issue in the brief, and use an appropriate escalation
path if this significantly affects the quality of the communication. Even when you can ask,
sometimes neither of you knows the answer (for example, some information the absent author hasn't
provided). Use your best judgement together, and document ambiguity. Do not overstate your
certainty or confidence level. Never make stuff up. If some particular part of the communication
is not possible, say so, but deliver any unaffected or unrelated remaining parts.

## 4. Writing the communication

Once you have a good communication brief, use it to go and write a good communication. Say what
you mean, as simply as benefits your objective. Avoid mannered prose and metaphor unless it carries
key meaning that serves the objective and audience.

Follow the style conventions and skills the brief names.
