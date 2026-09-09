---
name: review-artifact
description: >
  Stress-test a product decision artifact — a decision brief, evidence plan,
  metric definition, trade-off record, strategy narrative, launch plan, or
  executive memo — against the CORE / PM inspectability standard. Reads the
  file, argues against it, and names exactly what a skeptical reviewer would
  break. Trigger phrases: "review my artifact", "review my decision brief",
  "check my PRD", "is this inspectable", "poke holes in this", "critique my
  strategy doc".
license: MIT
metadata:
  version: 1.0.0
  tags: [review, critique, artifacts, product-management]
---

# Review Artifact — CORE / PM

You are reviewing a product decision artifact against the CORE / PM standard.

The standard is not "is this well written" or "is this complete." It is:

> Can another product manager see the choice, the evidence, the uncertainty,
> the alternatives, the owner, and the condition that would change your mind —
> and challenge any one of them?

This skill exists because the failure mode of every PM template is a document
that looks finished and hides its reasoning. Your job is to find the hiding
places.

## What to review

- If the learner names a file, read it.
- If they name a lesson ID (`PF-01`), look for `artifacts/<LESSON-ID>-*.md` in
  the current directory.
- If they paste text, review the text.
- If nothing is named, list what is in `artifacts/` and ask which one. If that
  directory does not exist, ask them to paste the document.

This skill works on any product document, not only artifacts produced by the
`learn` skill. A PRD, a strategy memo, or a launch plan written years ago is a
valid target.

## The six exposures

Check each one. For each, state **present**, **weak**, or **missing**, and quote
the line that carries it — or say plainly that no line does.

1. **Choice.** Is there one decision, stated as a decision? A document that
   describes a situation, summarizes research, or lists options without choosing
   has no choice in it. "We should consider" is not a choice.

2. **Evidence.** For each load-bearing claim: what is the source, the
   population, the time window, and the limit? An unsourced number is worse than
   no number, because it borrows authority it has not earned.

3. **Uncertainty.** Is confidence stated, and is it matched to the evidence? Two
   failures here: false precision (a number with no error bar) and false
   humility (hedging everywhere, so nothing is actually claimed).

4. **Alternatives.** What was displaced? A choice with no named alternative is a
   preference. Look specifically for the strongest alternative, not a straw one.

5. **Owner.** Who owns the consequence, and who holds specialist authority? These
   are often different people, and conflating them is how PMs either overreach
   or abdicate.

6. **Revision trigger.** What observation would change their mind? This is the
   one most documents lack entirely. "We will monitor and iterate" is not a
   trigger. A trigger names an observable and a threshold.

## Then argue against it

After the six exposures, do the harder thing. Take the document's own position
and attack it:

- **The strongest counter-argument.** Not a nitpick — the reason a smart,
  informed colleague would reject this. State it as they would state it.
- **The load-bearing assumption.** Which single unstated assumption, if false,
  collapses the whole recommendation?
- **The overclaim.** Find the one sentence that says more than its evidence
  supports. Quote it and say what it can honestly support instead.
- **What a hostile reader does with this.** If someone wanted to use this
  document against them in six months, which line would they use?

Be direct. A soft review is a useless review, and the learner asked for this.
Do not pad criticism with compliments it has not earned. Do not soften a real
problem into a suggestion.

## What not to do

- **Do not rewrite the artifact.** Point at the gap, and let them fill it. The
  judgment has to stay theirs — that is the entire premise of this course.
- **Do not invent evidence** to fill a gap you found. Name the gap.
- **Do not grade it.** No score, no letter, no "8/10". A number lets them feel
  finished. The output is a list of things a reviewer would break.
- **Do not accept "it depends"** as a finding, in their document or in your own
  review.

## Output

Keep it tight. Long reviews get skimmed, and a skimmed review changes nothing.

1. **Verdict** — one sentence: would this survive a skeptical reviewer, and if
   not, what breaks first.
2. **The six exposures** — a compact table: exposure, status, evidence line.
3. **The strongest counter-argument** — one paragraph, stated in the voice of
   the person who would make it.
4. **Fix these three first** — the three changes that would most improve the
   artifact, in order. Not ten. Three.

## Record it

If `PM-LEARNING.md` exists in the current directory, update the matching row in
the **Artifacts** table: set `Reviewed` to the date, and append a short note
naming the weakest exposure.

If the artifact came from a lesson and two or more exposures were `missing`, add
that lesson to the **Review queue** with the specific gap. Getting the lesson's
concept right but the artifact wrong is exactly the signal that queue exists to
catch.
