---
name: sales-outbound-sequence
description: Plans a touch-by-touch outbound cadence - which channel on which day, touch count, spacing, channel mix, multi-threading, exit and stop rules, recycle and re-entry, and the capacity math behind it, with pre-committed metric thresholds. Use whenever the user mentions a sequence, cadence, follow-up timing, Outreach or Salesloft steps, a drip, "how many touches", inbound-lead or event follow-up, closed-lost re-engagement, or B2C lifecycle and SMS flows, even without the word cadence. Do NOT use for message copy, subject lines (mbfinotti/sales-skills@cold-email-subject-line-tester), call scripts (mbfinotti/sales-skills@cold-call-opener), or inbox placement (mbfinotti/sales-skills@cold-email-deliverability).
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.3.6"
---

# Outbound Sequence

Design the skeleton of an outbound cadence - the touch-by-touch plan of channels, days, spacing, exits, and recycling - sized to the user's segment, list, and rep capacity, with metric thresholds committed before launch.

Two facts frame everything here:

- **Cadence length is contested.** Sales-training practitioners and sales-engagement vendors teach roughly 10-15 touches over 14-30 days. Email-quality vendors and outbound agencies cap it at 3-5 emails, fewer when multi-channel, and call long sequences a symptom of low relevance. Neither is law: this skill applies a decision rule instead of picking a side, see [references/cadence-patterns.md](references/cadence-patterns.md).
- **Most figures are vendor-published.** Nearly every statistic in the references comes from companies selling outreach tooling - trust the direction, never the magnitude, and label it as vendor-published when quoting it to the user. The only hard numbers are mailbox-provider policies (spam-complaint ceilings), flagged as platform policy where they appear.

Scope: the cadence plan is the whole deliverable. Never write message copy in depth, route it to the sibling skill for that copy type:

- Subject lines: `mbfinotti/sales-skills@cold-email-subject-line-tester`
- Call openers: `mbfinotti/sales-skills@cold-call-opener`
- Personalization-angle selection: `mbfinotti/sales-skills@sales-outreach-personalization`
- Rebuttals: `mbfinotti/sales-skills@sales-objection-handling`
- Post-meeting follow-up: `mbfinotti/sales-skills@sales-meeting-recap`

Never audit deliverability, domains, or authentication - plan within the sending constraints, then hand the audit to `mbfinotti/sales-skills@cold-email-deliverability`.

## Interview

- Ask one question per message.
- Offer multiple-choice options.
- Skip anything context already answers.

If your harness has persistent memory and a prior run stored this user's answers, confirm them instead of re-asking.

1. Regime: B2B outbound to businesses, or B2C to consumers? Ask first - consent, speed, and volume rules diverge.
2. By what date must this land results? A hard near date promotes the short pattern, the near-zero channels, and reply rate as the committed metric. A soft date lets the long multi-channel pattern and meetings-per-100 back in.
3. A one-off win, or a compounding asset? One-off promotes a single sprint on the best-scored cohort. Compounding promotes staggered cohort entry, a recycle window, and the trigger-watching that makes re-entry work - all of which cost more now and pay from cohort two onward.
4. Effort ceiling: rep hours per day, headcount, and how much sender risk is acceptable? A founder doing their own outbound has no daily call block, which deletes the manual channels rather than demoting them. A new or warm-up-limited domain caps email touches at any budget and promotes the call block instead.
5. Motion: cold outbound, inbound-lead follow-up, event follow-up, or closed-lost/dormant re-engagement? For B2C: which lifecycle trigger - signup, cart or browse abandonment, win-back?
6. B2B segment: SMB high-velocity, mid-market, or enterprise ABM? This drives the length decision rule.
7. Persona, seniority, and account size? Senior buyers tolerate fewer, better touches.
8. Which channels are actually available and staffed - email, phone, social, SMS, video - and what is the consent basis for each? SMS or messaging without express opt-in is off the table, not a design choice. Calling lists must be screened against do-not-call registries.
9. List size per launch, and how many reps with how much daily manual-touch capacity?
10. Personalization depth planned: deep per-account research, light segment-level, or templated? Also drives the length rule.
11. What can the sequencer automate versus surface as manual tasks? Does it auto-exit on reply? Are per-mailbox daily send caps known?
12. Which metric can you actually measure reliably: replies, meetings, call connects, conversions - or only opens?

Every ranking in this skill is a default, not a law. Re-rank against the answers before proposing anything, and say out loud which answer moved which option - the order shifts with the deadline, with the domain's state, and with who executes it.

## Workflow

1. Run the Interview. Confirm regime, motion, segment, channels-with-consent, volume, capacity, and metric before drafting.
2. Read [references/cadence-patterns.md](references/cadence-patterns.md). Apply the length decision rule and record which factors pushed the choice - never default to a template silently.
3. Draft the touch table: for every touch, a day, a channel, a step type (automated or manual), a one-line purpose, and the exit check that precedes it. Model the shape on the filled examples in [references/example-cadences.md](references/example-cadences.md) - match the structure, not the content.
4. Assign channel roles. Buy channels in efficiency order and stop where step 7's capacity math stops you:

   **in-thread bump > blank connection request > extra email angle > call + voicemail > social DM > video message**

   - Email carries the ask; every other channel exists to lift email replies.
   - Rep minutes per touch and how reversible the damage is decide the order: a domain burned by complaints is the one thing a cadence cannot undo, and a call block is a standing daily job.
   - Full axes, per-channel costs, the two deletions, and the re-ranking conditions are in [references/cadence-patterns.md](references/cadence-patterns.md).
   - Practitioner guidance, not law - say so.

5. B2B: add a multi-threading plan - 2-3 contacts per account, staggered entry, account-level pause when any one of them replies. Vendor-published data reports reply rates falling sharply past a handful of contacts per company; spraying a whole org is a failure mode, not thoroughness.
6. Define exits, suppression, recycle window, and trigger-gated re-entry (rules below; elaboration in the patterns reference).
7. Run the capacity math in [references/capacity-and-measurement.md](references/capacity-and-measurement.md). When the plan does not fit, buy the fix in this order:

   **stagger cohort entry > cut the active cohort > drop the heaviest manual touch > add mailboxes or reps**

   - Staggering costs a sequencer setting and changes nothing about the sequence under test.
   - Dropping a touch forfeits comparability with the last cohort.
   - Never plan touches nobody will execute.
   - Hand the actual mailbox/domain audit to `mbfinotti/sales-skills@cold-email-deliverability`.

8. Pre-commit the metrics: numeric thresholds, floors and ceilings, and a review date, using the template in the capacity reference. Commit the highest-ranked metric that is actually measurable (order in KPIs below).
9. Score the plan against the Quality gate below. Iterate until every item passes.
10. Deliver the output package (shape in [references/example-cadences.md](references/example-cadences.md)). If your harness has persistent memory, store the segment, chosen pattern, committed thresholds, and eventual results; otherwise include a compact log block the user can paste into a future session.
11. Route all copy work to the sibling skills listed in Scope. Any outline-level copy this plan does carry (touch themes, a voicemail one-liner) stays at outline level; anything shipped as actual copy goes through your preferred humanizer skill first.
12. At the committed review date, compare results against thresholds and change exactly one variable per revision. If you can browse the web, verify any re-entry trigger (funding, job change, product launch) before re-enrolling a prospect; otherwise ask the user to confirm it.

## Exit, stop, and recycle rules

Apply these exit rules:

- Exit immediately - mid-sequence, not at the next scheduled touch - on: any reply, meeting booked or conversion, opt-out or unsubscribe, hard bounce, or a hostile response. An opt-out processed "at the next step" is the fastest route to a complaint.
- Suppress before enrollment, not after:
  - Opt-outs and do-not-contact lists.
  - Hard bounces.
  - Current customers.
  - Accounts with an open opportunity.
  - Prospects active in another sequence.
  - Prospects inside a cooldown from a previous sequence.
  - Any channel lacking a consent basis (B2C especially).
- Breakup versus just stopping: **breakup touch > quiet stop**, on a long B2B cadence only.
  - Both cost one templated send or less, so value decides. One camp reports breakup emails drawing among the highest reply rates in the sequence when framed as an explicit yes/no; the other argues to skip the theater and return only with a new reason.
  - What the breakup spends is the account's re-entry option, since a sent breakup binds you to suppress until a genuine new trigger.
  - Default: breakup at the end of a long B2B cadence, quiet stop on a short sprint and on a named-account list you cannot afford to burn.
  - B2C is not a choice - the sunset/re-permission message is a consent obligation.
  - If a breakup is sent, honor it.
  - Evidence and axes in [references/cadence-patterns.md](references/cadence-patterns.md).
- Recycle: cooldown of 30-90 days (practitioner range), then re-entry gated on a fresh trigger - job change, funding, tech change, a new signal - never on the calendar alone.
  - Cap re-entries at two cycles, then choose once: long-term nurture where the account still fits the ICP and someone owns the list, sunset everywhere else.
  - Nurture is a standing job, so defaulting to it on a list nobody maintains just parks a dead cohort against your domain.
  - If your harness can run scheduled checks, watch the stale list for triggers on a recurring basis; otherwise instruct the user to review it manually at a fixed weekly slot.

## Quality gate

The plan ships only when every item passes. Iterate until it does.

1. Every touch has a day, channel, step type (automated/manual), purpose, and preceding exit check.
2. Touch count and duration follow the decision rule, with the deciding factors recorded in the plan.
3. No accidental same-day pile-up: at most one intentional, labeled multi-channel cluster day; no day mixes more than two channels otherwise.
4. Gaps widen toward the tail of the sequence (trigger-anchored B2C flows, which compress to hours, exempt).
5. All five immediate-exit conditions are listed with the mid-sequence stop rule.
6. The suppression checklist is written into the plan as a pre-enrollment step.
7. Recycle cooldown, re-entry trigger, and re-entry cap are defined.
8. Capacity math is shown and the plan fits within rep and per-mailbox limits.
9. B2C: consent basis, quiet hours, and a cross-flow frequency cap are stated per channel.
10. Metric thresholds and a review date are committed in writing before launch.
11. Sends are scheduled in recipient-local time and skip the recipient geography's holidays.
12. No in-depth message copy in the plan - copy tasks are routed to the sibling skills.

## KPIs and measurement

Full definitions, calibration numbers, and the pre-commitment template live in [references/capacity-and-measurement.md](references/capacity-and-measurement.md).

- Instrument in efficiency order, and commit the first one the user can actually measure:

  **reply rate > positive-reply rate > meetings per 100 prospects > connect rate > completion rate**

  - Reply rate leads because the sequencer emits it for free and it settles most cadence questions.
  - Meetings per 100 is worth more but costs CRM plumbing and a full cohort cycle before it reads. Promote it anyway when the cadence has to be compared against another channel's investment.
  - Opt-out and spam-complaint rates sit outside the ranking - they are guardrails, not goals.

- Open rate is deleted, not ranked: mail-privacy proxies register phantom opens, so it never decides a cadence question while any downstream metric exists. Use it only when literally nothing else is measurable, and say the number is inflated.
- Judge the sequence as a whole, never on touch 1 - multiple vendor-published datasets independently report that most replies arrive after the first touch.
- Success for this skill = the plan clears the Quality gate before launch, and at the review date the sequence has met its committed reply/meeting thresholds without breaching the opt-out or spam-complaint ceilings. If a threshold is missed, revise one variable and re-commit.

## Failure modes

- Same-day multi-channel pile-up. Five touches landing in one afternoon reads as harassment. Fix: one labeled cluster day at most; spread the rest.
- Colliding prospects - two reps or two sequences hitting the same person or account. Fix: pre-enrollment dedupe against active sequences and open opportunities; account-level pause on reply.
- Sequence judged on touch 1 and killed early. Fix: pre-commit the review date; evaluate cumulative reply rate at sequence level.
- Automation replacing relevance. A 14-touch templated blast is not persistence, and the short-cadence camp's core argument is that length often substitutes for relevance. Fix: rerun the decision rule - low personalization depth points to fewer, better touches.
- Time-zone and holiday sends. 3 a.m. touches and Thanksgiving-week calls burn goodwill silently. Fix: recipient-local send windows; holiday calendar per geography.
- Breakup sent, then contact resumes two weeks later. Fix: breakup implies suppression until a genuine new trigger.
- B2B cadence copied onto B2C without a consent check. SMS without express opt-in or quiet-hours handling is a legal exposure, not a tuning problem. Fix: gate every B2C channel on its consent basis first.
- Cadence wider than capacity. Manual call and social steps silently skipped by overloaded reps corrupt the experiment - the sequence tested is not the sequence designed. Fix: capacity math before launch; stagger cohort entry.

## References

- [references/cadence-patterns.md](references/cadence-patterns.md) - length decision rule, channel-role logic, motion-specific and B2C shapes, breakup evidence, and the vendor-published or practitioner-reported label on every figure.
- [references/example-cadences.md](references/example-cadences.md) - filled cadence tables (B2B long, B2B sprint, B2C flow), a negative example, and the output package sample.
- [references/capacity-and-measurement.md](references/capacity-and-measurement.md) - capacity formulas and worked example, sender constraints, KPI definitions, calibration table, pre-commitment template.
- [references/sequencer-vocabulary.md](references/sequencer-vocabulary.md) - mapping generic cadence terms to sequencer products (the only place vendor names appear).
