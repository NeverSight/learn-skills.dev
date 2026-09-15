---
name: cold-email-subject-line-tester
description: Generates, scores, and split-tests email subject lines, producing angle-distinct variants, a numeric scorecard, and a test plan with sample size and decision metric. Covers B2B cold outbound and B2C lifecycle/promotional email, and flags spam-trigger words inside the subject line only. Use whenever the user mentions a subject line, open rates, email A/B test, preview text, or "nobody opens my emails", even if they don't say "subject line" explicitly. Do NOT use for body copy or inbox-placement audits (mbfinotti/sales-skills@cold-email-deliverability), personalization angles (mbfinotti/sales-skills@sales-outreach-personalization), or cadence design (mbfinotti/sales-skills@sales-outbound-sequence).
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.4.3"
---

# Subject Line Tester

Generate subject line variants from an already-chosen personalization angle, score them against a numeric rubric, and design a statistically honest split test to pick the winner.

Two facts frame everything here:

- No named, cross-source framework exists for subject lines the way MEDDIC exists for qualification - only single-vendor branded methods and one unbranded convergence (keep B2B cold subjects short; avoid numbers and question marks in them).
- Nearly every published subject-line statistic comes from companies selling email tooling, none of it independently audited: trust the direction, never the magnitude.

Where sources flatly contradict each other (notably lowercase vs. title case), treat the question as a test candidate, never a rule.

Scope: the subject line (plus preheader for B2C) is the whole deliverable.

Never:

- Write body copy.
- Audit deliverability, headers, domains, or authentication.
- Research prospect signals.
- Plan touch-by-touch cadence.

Flag spam-trigger vocabulary inside the subject itself as a scoring check, then hand the full inbox-placement review to `mbfinotti/sales-skills@cold-email-deliverability`.

## Interview

Ask one question per message. Offer multiple-choice options. Skip anything already answered by context. If your harness has persistent memory and a prior run stored this user's answers, confirm them instead of re-asking.

1. Regime: B2B cold outbound, or B2C lifecycle/promotional? Ask this first - the two follow different rules.
2. Recipient persona, role, and seniority? Executive inboxes decide in seconds; the pattern set narrows sharply for them.
3. Which personalization angle is already chosen - pain point, competitor, company initiative, executive priority, shared context, trigger event? If none, stop and route to `mbfinotti/sales-skills@sales-outreach-personalization` first. Ranking these is step 4's job, not this question's.
4. What does the email body actually promise or deliver? The subject must never outrun it.
5. Can your sending platform (sequencer or ESP) split-test? At what volume (list size or sends per day)?
6. Which decision metric can you trust in your setup: replies or meetings, clicks or conversions, or only opens?
7. By what date must the result land? A deadline inside the week promotes the near-zero-research angles and cuts the parked-question tests entirely; a date far enough out to collect 200+ sends per variant keeps a test in scope.
8. One-off win on this campaign, or a compounding asset? Compounding promotes the reusable angles (internal-style noun, persona pain, executive anchor) and the casing test; one-off promotes whichever angle today's list already supports.
9. Effort ceiling: how many research minutes per prospect are affordable, and how many sends per day are available? Near-zero minutes deletes the trigger-event, competitor and initiative angles outright; a quota too small to reach the per-variant floor deletes the test queue.
10. B2C only: do you control the preheader text, and is emoji acceptable to the brand?

Re-rank the angle catalog against the answers to 7-9 before drafting, and tell the user which answer moved which angle.

## Workflow

1. Run the Interview. Confirm regime, persona, angle, body promise, test capacity, metric, deadline, payoff horizon, and effort ceiling before drafting.
2. Read the matching regime section of [references/pattern-library.md](references/pattern-library.md). Never apply B2B cold rules to B2C lifecycle or vice versa.
3. Write a falsifiable hypothesis before drafting: "Because [observation], we believe [change] will [effect] for [audience]. We'll know when [metric]." Reject vague forms like "let's test a new subject line."
4. Draft 3-5 candidate variants, working down the catalog's efficiency order - for B2B cold, `internal-style noun > specific pain question > executive-world anchor > competitor == company initiative > trigger event`, ranked by replies bought per research minute. Delete any angle the interview ruled out instead of ranking it last, and say which angle was deleted and why. Each variant must express a distinct angle, never a synonym swap of another. For B2C, draft a preheader with every variant - subject plus preheader is the tested unit.
5. Score every variant with [references/scoring-rubric.md](references/scoring-rubric.md): hard-fail checks first, then the 10-point scorecard.
6. Regenerate any variant below the pass threshold, then re-score. Repeat until the full set clears the quality gate.
7. Run the surviving set through your preferred humanizer skill, then re-score. Raw first-draft model output is never shipped - templated AI phrasing is exactly the smell that gets an email deleted unread.
8. If you can browse the web, verify any volatile fact a variant leans on (trigger event, competitor claim, initiative name). Otherwise, ask the user to confirm it before shipping.
9. Design the test with [references/test-design.md](references/test-design.md): one variable, pre-committed sample size, minimum duration, decision metric, guardrail metrics.
10. Deliver the output package (shape below). If your harness has persistent memory, record persona, chosen angle, hypothesis, and shipped variants so later runs skip the interview and build on results.
11. When results come back, log winner, loser, or inconclusive against the hypothesis, then take the next single-variable test from the ranked queue in [references/pattern-library.md](references/pattern-library.md) - or say plainly that the volume supports no further test.

## Invocation examples and expected output

Typical requests this skill handles:

- "Test my subject line for this cold email to a VP of Operations."
- "Write 5 subject line variants for our cart-abandonment campaign."
- "A/B test subject lines for next week's product launch email."
- "Why is my open rate low?" Diagnose the subject line only; route domain, authentication, and inbox-placement causes to `mbfinotti/sales-skills@cold-email-deliverability`.

Expected output package, in order:

1. Hypothesis statement in the falsifiable form above.
2. Variant scorecard table: variant, angle, word/character count, rubric score, notes (plus preheader column for B2C).
3. Test plan: split, sample per variant, duration, decision metric, guardrails.
4. Flagged risks: unverified facts, spam-trigger words found, angles deleted by the interview and why, and the parked questions in queue order with the send cost of resolving them.

Filled examples of the table and test plan live in [references/scoring-rubric.md](references/scoring-rubric.md) and [references/test-design.md](references/test-design.md).

## Quality gate

- Score every variant on the 10-point scorecard in [references/scoring-rubric.md](references/scoring-rubric.md).
- Pass threshold: every shipped variant scores at least 8/10 with zero hard fails.
- Hard fails (any one disqualifies the variant outright):
  - Fake "Re:"/"Fwd:" or other deceptive framing.
  - Subject promising what the body does not deliver.
  - Spam-trigger vocabulary.
  - Exceeding the regime's truncation budget.
  - Duplicate angle within the set.
  - Prospect first name in a B2B cold subject.
- Iterate: regenerate and re-score failing variants until the whole shipped set clears 8/10. Never ship a sub-threshold variant to "fill out" the test.

## KPIs and measurement

- B2B cold decision metric: reply rate, positive reply rate, or meetings booked - never opens alone. Mail-privacy proxies have pre-fetched tracking pixels since 2021, registering phantom opens; open rate is directional only.
- B2B calibration (vendor-published, not independently audited):
  - Average open ~27.7%, good 40-45%.
  - Average reply 4-5.8%, good 5-10%.
  - Falling year over year.
- B2C lifecycle: open rate is usable but must be paired with a downstream guardrail - click, conversion, unsubscribe under 0.5%, complaints under 0.1%.
- Success for this skill = the test reaches its pre-committed sample and produces a decision (winner, loser, or honest inconclusive) without any guardrail degrading.

## Failure modes

- Variant set is synonym swaps of one idea. Fix: force each variant onto a different angle from the pattern library.
- Capitalization enforced as a rule. Sources directly contradict each other (title case vs. lowercase, both vendor claims); hold it constant and park it in the ranked test queue.
- Efficiency order treated as law, or a ruled-out angle parked at the bottom of the set. The order is a default that shifts with list size, recipient seniority, and who executes it; an angle the interview ruled out gets deleted from the set and named, never demoted.
- Prospect first name in a B2B cold subject. It signals mail-merge and correlates with fewer replies; use a contextual token instead.
- Winner called on open rate in B2B cold. Phantom opens from privacy proxies manufacture false winners; decide on replies or meetings.
- Peeking and stopping early. Pre-commit to sample size and duration; an early "winner" is usually noise.
- Generic question subjects. Vendor data conflicts on questions overall; a specific pain question can work, a generic one fails. Default to statements.
- Subject outruns the body's promise. Opens rise, replies and trust collapse; the body-promise match is a scored criterion for this reason.
- B2B rules applied to B2C or vice versa. Numbers measure as a negative in B2B cold subjects yet perform fine in B2C lifecycle.
- Shipping raw model output. Always run the humanizer pass and re-score afterward.
