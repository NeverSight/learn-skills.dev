---
name: lead-routing
description: Design the assignment logic that routes inbound leads to sales reps - rule precedence and waterfall ordering, lead-to-account matching, territory assignment rules (geography, segment, industry, named accounts), round-robin variants (straight, weighted, capacity-based, availability-aware), fallback catch-all queues, SLA escalation and reassignment, and safe rollout of routing changes. Use whenever the user mentions lead routing, lead assignment, territory assignment, round-robin, lead distribution, "who gets this lead", a lopsided round-robin, or leads sitting unworked in a CRM queue - even if they never say "routing". Covers B2B account-based and B2C/PLG high-volume routing. Do NOT use for designing the lead score itself - use mbfinotti/revops-skills@lead-scoring instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.3.5"
---

# Lead Routing

Design the assignment logic that gets every inbound lead to a named owner who accepts it. No industry-named framework exists for this discipline - practitioners independently converge on the same de facto pattern: an ordered precedence ladder (also called a rule waterfall), evaluated top-down, first match wins, terminating in a monitored catch-all. Present it as common practice, never as a branded methodology.

Routing is not assignment.

- **Assignment:** a CRM owner-field write.
- **Routing:** the full chain from capture to a person taking responsibility, or the system raising a visible exception with a timer and an escalation path.

Most routing failure is silent:

- rules fire
- dashboards show green
- leads sit unworked in queues nobody owns

Lead score is strictly an input here, never a design target. Use the score the user already has as:

- a ranking signal: which eligible lead to work first
- an eligibility gate: route only above a threshold

Do not design or tune the scoring model itself. That is the sibling skill `mbfinotti/revops-skills@lead-scoring`.

## Interview

- Ask before designing anything.
- One question per message.
- Offer multiple-choice options when possible.
- Skip a question only when the user already answered it.

- What creates a lead, and through which ingestion paths - web form, API, list import, chat, scheduling tool, CRM sync, manual entry?
- Which lead attributes are reliably populated at capture (country, company size, industry, email domain)? Which are often blank?
- What is the team shape - how many reps, in which pools (SDR, AE, segment teams, specialists), with what specialization?
- What are coverage hours and timezones? Is there after-hours or weekend inbound?
- Is the motion B2B account-based, B2C/high-volume, PLG self-serve, or mixed? Roughly how many leads per month?
- Do named-account lists, partner deal registration, or existing-customer carve-outs exist? Are they versioned anywhere?
- What does "fair" distribution mean to this team - equal turns, equal open workload, proportional share by ramp/tenure, or equal opportunity value?
- What response SLA exists today (if any), and is it measured?
- Any compliance constraints - data residency, consent requirements, regulated verticals?
- Is a lead score available as an input? What does it mean, and is it trusted?
- By what date must the new routing be live, and is that date hard or aspirational?
- Do you want a one-off fix to today's misrouting, or a distribution system that keeps holding as the team grows?
- What is the effort ceiling - admin hours available, whether anyone owns the CRM day to day, and whether the team will run a standing governance process (weight reviews, territory changes)?

The last three answers move the rankings in this skill, not just the timeline. Re-rank against them before proposing anything - see Distribution variants for which answer moves which option.

## Workflow

1. Run the Interview; collect the answers the design depends on before proposing rules.
2. Instrument before touching rules: add stage timestamps (captured, eligible, decision, assigned, notified, accepted, first action). Without them, nothing proves a routing change worked.
3. Fix lead-to-account matching before distribution. Standardize an account-domain field. Match on email domain first, fuzzy company name second. If the match rate is under ~90% or duplicates exceed ~5%, leads leak before any rule runs - clean first.
4. Write the precedence ladder (next section) top-down, most specific to most general, and version it as a document. Eligibility tiers decide who may own the lead. Distribution only chooses within the eligible pool.
5. Choose the distribution variant by first writing down the team's definition of "fair", then taking the highest rung the team's answers actually support - default rung 1, availability-checked straight rotation (see Distribution variants).
6. Design the catch-all as a real state, a monitored triage queue with:
   - a named owner
   - a same-business-day SLA
   - a weekly review that converts recurring exceptions into rules

   Designed here, shipped first - it is the top of the build order in The precedence ladder, ahead of every rule above it.

7. Add the acceptance clock: if a lead is assigned but not accepted or touched within N minutes, reroute to a named backup with a logged reason code. Keep the decision result and the CRM write result in separate fields, so a failed write is distinguishable from a rule that never matched.
8. Produce the routing matrix (criteria → assignee → SLA, in precedence order) and a synthetic test pack covering every rule, every overlap, and every ingestion path - see [references/precedence-ladder-example.md](references/precedence-ladder-example.md) and [references/test-pack-and-rollout.md](references/test-pack-and-rollout.md).
9. Test in a sandbox with the pack, ideally replaying real historical leads; then roll out through a canary segment with daily reconciliation and a rollback plan, reserving shadow mode for changes a canary cannot contain (see [references/test-pack-and-rollout.md](references/test-pack-and-rollout.md) for the ranking). Never edit assignment-affecting logic directly in production.
10. Validate against the pass thresholds in Measurement below. Iterate on rules, matching, or coverage until every threshold holds. Present the finished design for user approval, section by section:
    - routing matrix
    - test pack
    - monitoring plan
11. If your harness has persistent memory, memorize the approved ladder, fairness definition, and thresholds - a later change request starts from them instead of re-interviewing.

## The precedence ladder

Order rules top-down; first match wins. A defensible default ordering, adapted to what the user actually has:

1. Legal/regulatory/contractual overrides - data residency, consent constraints, contractual partner rights. Deterministic and versioned, never inferred.
2. Named-account or strategic ownership, from a versioned list.
3. Open opportunity or active commercial process on the matched account.
4. Existing account and hierarchy ownership - route to the relationship owner, not the next in rotation.
5. Territory boundary - geography, segment, industry, in whatever combination the team uses.
6. Product, skill, or language eligibility.
7. Capacity and availability - open-lead caps, PTO, business hours.
8. Fair allocation - the chosen distribution rung, within the pool tiers 1-7 produced.
9. Governed exception - the monitored catch-all triage queue.

Two structural rules:

- Tiers 1-6 define eligibility; tiers 7-8 only distribute within it. Mixing the two is how enterprise leads land on SMB reps.
- Hierarchy conflicts (a matched subsidiary whose parent is owned by a different rep) route to a human-owned conflict queue with a dwell timer, never to an automated rule.

This list is deliberately not ranked by efficiency, and never gets reordered by it. It is an evaluation order - most specific first, first match wins - so any efficiency reshuffle changes which rule fires, not which rule to build first.

Build order does rank, and it is a different order from the one above:

- efficiency (build order): tier 9 catch-all > tier 4 existing-account ownership > tier 5 territory > tier 6 product/skill/language > tiers 7-8 distribution
- effort (build order): tier 5 territory (a week, then a standing job) > tier 6 (a week, plus a per-rep skill field) > tier 4 (a week, gated on match rate) > tiers 7-8 (see Distribution variants) > tier 9 (an hour)

- **Tier 9 catch-all, first:** an hour of work turns every silent drop into a visible exception, and it is the only tier that makes the others measurable.
- **Tier 4 existing-account ownership, next:** it prevents the most damaging misroute, a current customer handed to a rep who has never spoken to them, but it is worthless below a 90% match rate, so fix matching first.
- **Tiers 1-3, outside the ranking:** legal overrides, named accounts, and open opportunities are non-negotiable, so their ratio never decides anything.

## Distribution variants, ranked

Round-robin is a family of algorithms, each answering a different definition of "fair".

The most common configuration mistakes:

1. picking the wrong one for the team's definition
2. picking the most elaborate one

Rank them by what they actually deliver, speed-to-lead and the fairness reps experience (not the fairness the algorithm claims), against what they cost:

- admin configuration time
- the standing governance the rule needs
- the fields the CRM must already carry
- how hard the rule is to unwind once reps have adapted to it

- efficiency: availability-checked straight rotation > capacity-based > weighted > the layered stack
- value: the layered stack > capacity-based > availability-checked straight rotation > weighted
- effort: the layered stack > weighted > capacity-based > availability check == straight rotation
- compliance cost: weighted == the layered stack > capacity-based == availability check == straight rotation

- **Straight rotation ties with the availability check on effort:** both are pure configuration over data the team already keeps (a rotation list, and whichever OOO calendar it already trusts), with no new field and no standing owner.
- **Weighted ties with the layered stack on compliance cost:** both hand some reps more inbound than others by design. That changes earning opportunity, so it needs sales-leadership and comp sign-off before it ships, and it cannot be quietly reverted once reps know their own weight.

The other three carry no such exposure.

**Rung 1 - availability-checked straight rotation (the default).** Next rep in the rotation, skipping anyone out of office or outside business hours. Fair means equal turns among the people actually present.

- _You get_: the largest single speed-to-lead gain available here - no lead parked on an absent rep, which is the failure that kills leads outright rather than merely distributing them unevenly.
- _You owe_: near-zero for the rotation, about an hour for the availability check, no standing owner.
- _Fails when_: equal turns end in very unequal open-lead piles, or calendar presence gets mistaken for sales capacity.
- _Cheap upgrade_: where an open-lead count already exists, add a hard cap that skips reps above it. Near-zero, and it buys most of rung 2's protection without rung 2's standing referee.

**Rung 2 - capacity-based, still availability-checked.** Fewest open leads takes the next one. Fair means equal open workload.

- _You get_: skew measured in workload rather than turns, and visible relief for the rep buried in leads nobody noticed.
- _You owe_: an open-lead field the CRM maintains, about a week to agree what counts as an open lead, and a standing referee for when one stops counting.
- _Fails when_: "a lead" varies wildly in effort, so equal counts hide unequal work just as turns did.

**Rung 3 - weighted rotation.** Weight 2 receives roughly twice weight 1. Fair means proportional share by ramp, tenure, or role.

- _You get_: ramping and part-time reps protected - a narrow gain that only pays while someone is actually ramping.
- _You owe_: a standing weight-governance process (who sets weights, on what evidence, when they are revisited), plus the comp sign-off above.
- _Fails when_: nobody owns the review, and last year's ramp weights are still running as an unexamined performance judgment.

**Rung 4 - the full layered stack.** Eligibility narrows the pool, a capacity or weighted base allocates, an availability check sits on top. Fair means every definition at once.

- _You get_: the best achieved outcome of the four, and the only one that satisfies a team holding two fairness definitions simultaneously.
- _You owe_: all three costs plus the interactions between them - a standing job, and the least reversible option here.
- _Fails when_: nobody can explain in one sentence why a given lead went where it went, at which point the team cannot safely unwind it either.

Promote one rung only when the failure condition of the current rung is observed in the canary data, never in anticipation of it.

- Persistent open-lead pile-up promotes rung 1 to rung 2.
- A genuine ramp cohort promotes rung 2 to rung 3.

**What this order starves.** Rung 4 loses every round: highest value, highest standing cost, so a ratio never selects it.

Promote it anyway when all three hold:

- someone owns the CRM day to day
- more than one pool has genuinely different economics
- a fairness dispute is already on the table

A team of three reps that ships rung 4 has built a system it will not be able to change.

**Delete, do not demote.**

- A CRM with no open-lead field and no appetite to add one deletes rung 2 outright, and rung 4 with it. A demoted option silently reappears as scope three months later.
- No weight-governance owner deletes rung 3.
- Missing availability data is the exception: it deletes nothing, because the first thing to build is that availability source, not a rotation variant chosen around its absence.

**Re-rank against the answers.**

- A hard date promotes rung 1 and deletes rung 4: the standing process cannot be stood up before the deadline.
- A compounding-asset mandate promotes rung 2, because a workload field pays off as the team grows while a rotation list does not.
- An effort ceiling below "a standing job" deletes rungs 3 and 4 in one move.

This ordering is a default, not a law. It shifts with context and with who executes it, so re-rank it against everything already known about this user before proposing anything:

- an admin who owns the CRM full-time moves rung 4 within reach
- three reps in one timezone make skew self-correct and delete rungs 2-4
- an existing territory model already does most of the eligibility narrowing, which lowers what any distribution variant can add

## B2B vs B2C / high-volume / PLG

The ladder shape, catch-all design, testing method, and measurement are identical for both motions. What differs is the routing key and the coverage model:

- **B2B account-based**: route on account ownership first. All contacts from one account go to one owner - a buying committee submitting three forms must not hit three reps. Honor named-account carve-outs and partner deal-registration protection windows as hard overrides. A 24-hour SLA on target accounts is a common practitioner starting point.
- **B2C / high-volume / PLG**: route on geography, language, and coverage hours. Route product-qualified signals (usage threshold hit, teammates invited) within 24-48 hours of the trigger, and pass the underlying signal to the rep, not just a bare score. The coverage model itself is a ranked choice, below.
- **Mixed motions**: run both branches under one ladder - account-based tiers first, high-volume distribution as the general pool beneath them.

Coverage mechanisms for high-volume motions:

- efficiency: no-touch floor > shift-based pools > skills-based queues > follow-the-sun
- effort: follow-the-sun (a quarter, and a hiring decision) > skills-based queues (a week, then a standing skill matrix) > shift-based pools (an hour, over rosters the team already keeps) > no-touch floor (near-zero)

- **No-touch floor, first:** one eligibility rule cutting the lowest-value self-serve segment out of sales entirely is the highest-ratio move in the whole high-volume design. It costs a single tier, and it removes volume from every rule beneath it, so every later variant gets cheaper.
- **Shift-based pools, next:** buying in-hours coverage over rosters that already exist.
- **Skills-based queues:** pay only where language or product genuinely gates who can work the lead, and they need a per-rep skill field somebody keeps current.

Delete follow-the-sun outright when the team has no out-of-region headcount - it is a hiring decision wearing a routing rule's clothes, and demoting it invites someone to "phase it in". The after-hours queue with instant auto-acknowledgment (ladder tier 7) covers the same gap at near-zero cost and is what to build instead.

## Failure modes and fixes

Not ranked, deliberately: fix the symptom actually observed. Ordering symptom-driven repairs by ratio would be false precision.

Two rows are the exception, built before any symptom appears because their symptom is invisible by construction:

- per-source alert-on-silence
- the hard-failure branch on a null assignment

| Symptom                                                   | Likely cause                                                                                        | Fix                                                                                                                     |
| --------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| One ingestion path produces different owners than another | A path bypasses assignment rules (common with API-created records)                                  | Push the identical synthetic pack through every path; add a hard-failure branch that pages an owner on null assignment  |
| Leads match the wrong rule                                | Overlapping entries accumulated over time; earlier entry silently wins                              | Audit and merge overlapping conditions; version the rule set; re-document precedence after any two-rules-match incident |
| Rules misroute on blank fields                            | Stale or empty territory/segment data                                                               | Validate or enrich before routing, with a hard timeout and an explicit missing-field branch - never misroute silently   |
| Leads assigned to absent reps                             | No PTO/holiday skip logic; some platforms treat reps who never set availability as always available | Availability-aware rotation, coverage pools, a dedicated holiday rule for known periods                                 |
| Weekend/after-hours leads go cold                         | No timezone- or business-hours-aware branch                                                         | Follow-the-sun pools or an after-hours queue with next-open-hours SLA plus instant auto-acknowledgment                  |
| Reps dispute fairness                                     | Equal counts hiding unequal lead value; or gaming (insta-closing to draw more)                      | Transparent assignment logs; distribute high-score leads separately from the standard pool; monitor for gaming patterns |
| Catch-all quietly fills up                                | Manual overflow review that never happens                                                           | Named owner, same-business-day SLA, weekly review with teeth - recurring exception types become new rules               |
| Dashboards green, pipeline missing                        | Nothing alerts when a source goes silent                                                            | Volume monitoring per source; alert on silence, not just on errors                                                      |

## Measurement and pass thresholds

Decompose speed-to-lead into a chain of clocks: captured → eligible → decision → assigned → notified → accepted → first action. Report the acceptance gap (accepted minus assigned), the interval where queue dwell and failed notifications hide.

Track alongside it:

- never-touched-lead count
- distribution skew per rep
- lead-to-account match rate
- catch-all queue volume and dwell

The design must meet every threshold below before it ships. Iterate until it does:

- Lead-to-account match rate ≥ 90% on inbound volume; below that, return to matching before touching distribution.
- Every ingestion path covered by at least one test case, and the identical synthetic record produces the identical owner on all paths.
- Zero unmonitored queues: the catch-all (and any conflict queue) has a named owner, an SLA, and a scheduled review.
- During the canary period, zero leads queue-owned past the acceptance SLA, and per-source volume monitoring with alert-on-silence is live.
- Distribution skew within the variance the team's fairness definition allows, verified over the canary window - not assumed from the algorithm choice.

Set the response SLA itself from the user's own conversion-by-response-time history when it exists. The famous urgency statistics (the 5-minute / 21x / 100x figures) come from a 2007 InsideSales/MIT phone-era study and a 2011 HBR audit, are widely misattributed, and evidence urgency - not routing ROI. See [references/speed-to-lead-evidence.md](references/speed-to-lead-evidence.md) before quoting any number to stakeholders.

## Optional integration note

Skip this section unless the user names one of these platforms.

- **Salesforce:** one active lead assignment rule per object, entries evaluated top-down first-match. API-created leads skip the rule unless the assignment-rule header is set, and native territory management does not cover leads or round-robin.
- **HubSpot:** rotation fairness is counted per rotate action, not per global ownership, so two individually fair workflows can produce a lopsided total. Adding or removing an owner resets the rotation.
- **Dynamics 365:** sellers who never configure availability count as always available and silently become the fallback.

## Reference

- See [references/precedence-ladder-example.md](references/precedence-ladder-example.md) for a worked precedence ladder and routing matrix (B2B and PLG variants), plus a negative example.
- See [references/test-pack-and-rollout.md](references/test-pack-and-rollout.md) for the synthetic test pack template and the sandbox → shadow → canary rollout sequence.
- See [references/speed-to-lead-evidence.md](references/speed-to-lead-evidence.md) for citable speed-to-lead and matching statistics with source, year, and credibility flags.
- `mbfinotti/revops-skills@crm-data-governance` for field ownership and source-of-truth rules on the fields routing reads.
