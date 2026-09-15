---
name: corporate-event-strategy
description: Decide what a company-run technical event is funded to accomplish, before anyone plans it - the goal mix (ecosystem goodwill, developer adoption, customer retention, sales pipeline, or a blend), who owns the budget line and which functions co-fund it, and the measurement commitment written before registration opens. Use whenever a company asks why it is running a user conference, community day, developer summit or roadshow, which goal to optimise, who should pay for it, or how to prove it worked to the people funding it, even when they only say "what is the ROI of our conference". Strategy layer only. Do NOT use to pick the event shape - use samber/dev-event-organizer-skills@business-event-formats - or to model the P&L - use samber/dev-event-organizer-skills@event-budget.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Corporate Event Strategy

You decide what a company-run technical event is _for_, and nothing else:

- The goal mix.
- Who owns the budget line that funds it.
- The measurement commitment written down before registration opens.

Never plan the event, produce it, price it, or model its P&L.

Say **company-run** and **community-run** for the two poles, even when the user says _corporate_. That word is what a searcher types, not a third pole. Mirror the meaning, not the label.

This skill sits at the company-run pole only. `samber/dev-event-organizer-skills@event-team-structure` routes its company-run branch here, and `samber/dev-event-organizer-skills@event-portfolio-strategy` routes its company-run goal wiring here. Everything else about a company-run event already has an owner, listed below.

Every ranking below is a default, not a law. Re-rank it against what the interview turns up: any one asset Q9 uncovers overturns a default rung.

## What arrives already decided

Take each of these as an input. Re-deriving one produces a second answer competing with a sibling's published one.

| Sibling                                             | Owns                                                           | You do                                                                                       |
| --------------------------------------------------- | -------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `event-team-structure`                              | Entity, standing team, decision rights                         | Start once settled                                                                           |
| `event-positioning`                                 | Identity, category strategy, what the event may honestly claim | A goal contradicting published identity routes back there                                    |
| `event-market-fit`                                  | The demand read                                                | Set the target its signals get read against; never re-read the signals                       |
| `event-growth-strategy`                             | Whether the next edition grows                                 | A goal change between editions comes back here - that skill consumes a goal, doesn't set one |
| `event-format-selection` / `business-event-formats` | The event shape                                                | Never re-derive it; decide the goal alongside it                                             |
| `event-ticket-pricing` / `event-budget`             | Price posture, access rungs, funding model                     | Supply which goal the access posture optimises for                                           |
| `event-budget`                                      | The P&L                                                        | Decide ownership and objective of the money; never restate a line                            |
| `event-portfolio-strategy`                          | Ranking several properties                                     | Decide one property's goals, never rank properties                                           |
| `event-sponsor-value-proposition`                   | What a sponsor buys at somebody else's event                   | Never import that vocabulary as the host's own goal list                                     |

## The buyer-and-user question

One split does real work at the company-run pole: does the developer who attends also sign? Ask it about this product, never about its market category - the two do not track each other.

- **Separated** - the developer in the room evaluates and adopts, somebody else signs. A join between attendance and an opportunity records two different people, so it measures influence, not conversion. Say influence in the deliverable rather than reporting it as attribution.
- **Collapsed** - the developer buys with their own budget, self-serve. Attendance and purchase are the same person's two actions, so a pipeline goal reads cleanly.

Ask which one this product is (Q3) before choosing any goal ending in a revenue number. The goal menu, ownership menu and measurement gate work identically in both cases; only the honesty of a pipeline claim changes.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 6-9 carry the menus below, which diverge sharply on how fast a payoff is readable, how durable it is, and what it costs to instrument. No default settles that for the user.

1. Which decisions are already settled elsewhere: the entity and team, the positioning, the demand read, the shape? Any that is not settled routes out before this work starts (see the boundary map above).
2. Who does the company want in the room, and in roughly what proportion: people who already use the product, people who have never bought, or the wider developer ecosystem? And which of those sit on the list you will actually invite from?
3. For this product, does the developer who attends also sign, or does somebody else? (Gates whether a pipeline goal can be stated honestly at all.)
4. Which functions besides marketing have a stake and could put money in - sales, product, developer relations, a named executive sponsor? And can you name today who owns the budget line?
5. What does the marketing organisation already report on today? And does a join already exist between the attendance list and the systems the sales organisation works from, or between attendance and product telemetry, or would either have to be built?
6. By what date must the goal and the funding line be agreed: a planning cycle, a fiscal-year budget lock, an executive review? (A hard date promotes the goals whose number is readable inside one reporting cycle.)
7. Is this a one-off edition or the first year of a standing annual program? (A compounding mandate promotes the durable goals and the shared funding lines; a one-off tolerates neither's overhead.)
8. What is the effort ceiling: who can hold a standing measurement job through the quarter _after_ the event, and how much political capital is available for a cross-function funding negotiation?
9. What already exists that the defaults assume away - a working attendance-to-opportunity join, product telemetry that identifies accounts, an executive already asking for the event, a customer advisory group, a prior edition's numbers?

## Workflow

1. Run the interview. Confirm every question this skill does not answer is settled or routed (Q1).
2. Separate the audience the company _wants_ from the audience its invite list can actually assemble (Q2). A company-run event usually runs on the company's own user and customer list; a goal aimed at people that the list lacks depends on an acquisition campaign nobody has budgeted.
3. Settle the buyer-and-user question (Q3) before any goal that ends in a revenue number.
4. Choose the goal mix from the menu below. State which rungs were rejected and why - the rejected list is what stops the goal quietly widening later.
5. Choose the budget-ownership model from the second menu, then check the coupling: the funder you add is the funder whose goal you chose. Adding sales to a line whose goal is adoption buys a veto over decisions its holder has no metric in.
6. Write the measurement commitment before registration opens - four fields per goal, per the gate under Measurement. A goal without all four is an intention.
7. Send the three review items out before the invitation and the registration form go live (see What this skill sends to review). Two of the three cannot be fixed retroactively.
8. When the goal is genuinely contested between functions, enter brainstorming mode rather than drafting:
   - Two or three candidate goal mixes, each carried through to its funding consequence and its measurement cost.
   - One question at a time.
   - One recommendation.
   - Validated section by section.
   - Explicit approval before finalising.
9. Present the deliverable section by section. Record the re-run triggers from Measurement so the next edition starts from a decision rather than from the argument again.

If your harness has persistent memory, record:

- The chosen goal mix, with the rungs rejected.
- The buyer-and-user answer.
- The ownership model, with each funder and what each one is buying.
- The four measurement fields per goal.
- The review items sent and their outcomes.
- The re-run triggers.

Next edition starts from that record instead of relitigating the goal.

## Goal-mix posture

What the event is funded to accomplish. Ranking (default, not a law - re-rank against Q5, Q6, Q7 and Q9):

- effort (instrumentation to build, functions whose cooperation it needs, standing reporting through the quarter after the event): `blended adoption-and-pipeline > pipeline-first > adoption-first > ecosystem-goodwill only`
- value, speed (a defensible number readable inside the current reporting cycle): `pipeline-first > adoption-first > blended adoption-and-pipeline > ecosystem-goodwill only`
- value, durability (the goal still defends its line through a weak quarter, a reorganisation, or a change of budget owner): `blended adoption-and-pipeline > adoption-first > pipeline-first > ecosystem-goodwill only`
- compliance cost (the review triggered and the reversibility spent): `pipeline-first == blended adoption-and-pipeline > adoption-first > ecosystem-goodwill only`

**The two value axes genuinely disagree, and that disagreement is the decision**, the same shape `samber/dev-event-organizer-skills@event-format-selection` publishes for track count. Speed and durability invert at the top.

Pipeline is the fastest number to produce and the first to fail you: a quarter with no opportunities is a quarter with nothing to defend the line with. The blend reads slowest because the slower of its two reads gates it.

No efficiency line is drawn for this menu: six pairs across the four rungs, none a strict dominance relation. See [references/goal-definitions-and-measurement.md](references/goal-definitions-and-measurement.md) for the pair-by-pair check.

The compliance tie is argued: pipeline-first and the blend both move the attendee list into the systems the sales organisation works from, under one lawful basis and one notice; the blend adds a second _read_ of data already collected, not a second collection.

- **Adoption-first** - the default, and the one the invite list actually supports. Deeper or broader product use among people already using it; existing-customer retention reads on the same axis. Instrumentation is usually one organisation's data and one owner's approval, so it sits below pipeline on effort despite a slower read. Ecosystem goodwill rides along as a behaviour constraint, not a second goal to report.
- **Pipeline-first** - new opportunity creation as the stated goal. Promotion condition, all three:
  - Q6 names a hard reporting date.
  - Q2 says the room will be majority people who have never bought.
  - Q5 says the join to the sales systems exists today.

  Missing any one, this rung produces a number late, from a room that could not have generated it, through machinery nobody staffed. If Q3 says buyer and user are separated, state the claim as influence, never attribution.

- **Blended adoption-and-pipeline** - **what a cost-first reading starves**: top of durability and top of effort, so any cheapness-led order rejects it every round. Its payoff is a second story to fall back on in a bad quarter. Promotion condition, all three required:
  - Q7 says compounding annual program.
  - Q5 says both joins exist or can be built.
  - Q8 names someone who can hold the standing measurement job through the following quarter.

  A blend without a reconciliation owner produces two numbers that disagree and one argument nobody wins.

- **Ecosystem-goodwill only** - kept visible, not recommended. Genuinely the cheapest posture, and the first to die in a cutback: it has nothing to defend itself with. **Delete it, do not demote it, the moment Q4 names any co-funding function.** A funder will not accept a goal with no number attached, and a rung parked at the bottom reappears as the retreat the team takes once instrumentation runs late.

**Delete, do not demote: attendance count as the goal.** Registrations and heads through the door are a capacity fact this skill's siblings already own, not an outcome. Detect it at Q5. When registrations are the only thing marketing reports on today, they are the fallback number the team will reach for, which is exactly why the menu cannot carry them.

Full definitions of each rung, the instrumentation each one needs, and a worked positive and negative example are in [references/goal-definitions-and-measurement.md](references/goal-definitions-and-measurement.md).

## Budget-ownership model

Who owns the funding line, and who else has a claim on it. Ranking (default, not a law - re-rank against Q4, Q7, Q8):

- effort (the negotiation, the approval cycle, and the standing report each funder is owed): `multi-function committee > marketing-and-sales == marketing-and-product > marketing sole owner`
- value, durability (the line survives one function's cut, a reorganisation, or the departure of whoever championed it): `multi-function committee > marketing-and-sales == marketing-and-product > marketing sole owner`
- value, decision latitude (how much the organising team can change - audience, format, date, scope - without reopening the funding agreement): `marketing sole owner > marketing-and-product == marketing-and-sales > multi-function committee`

Three ties hold, on effort, durability and latitude, and none of the six dominance pairs across the four rungs is a strict win. See [references/budget-ownership-and-review.md](references/budget-ownership-and-review.md) for the argument behind each tie and pair.

All three ranked axes restate one quantity: how many funders sign. The promotion conditions below therefore carry this menu's weight, not the dominance count.

No compliance-cost axis is drawn: who signs for the money triggers no review by itself. The reviews this skill does trigger attach to the goal and to the guest list, and they are in their own section below.

- **Marketing sole owner** - the default. One negotiation, one report, full latitude to change the event as the year moves. Known failure: the line dies with the person who championed it, a single point of failure `samber/dev-event-organizer-skills@event-portfolio-strategy` already names at this pole from the portfolio side.
- **Marketing and product co-funded** - promotion condition:
  - Q4 names product as already asking for the event.
  - Q7 says compounding.
  - The goal menu landed on adoption-first.

  Product co-funding an adoption goal is the coupling working correctly; product co-funding a pipeline goal is a veto held by someone with no metric in it.

- **Marketing and sales co-funded** - promotion condition:
  - Q4 names sales as already asking for the event.
  - Q7 says compounding.
  - The goal menu landed on pipeline-first or the blend, _with_ Q5's join in place.

  Sales will not co-fund a number it cannot see; a co-fund agreed before the join exists is a commitment against a report that may never be produced.

- **Multi-function committee with a named executive sponsor** - the starved rung: top of durability and top of effort, so a cost-first reading never picks it. Promotion condition:
  - Q4 names more stakeholding functions than one co-fund rung can absorb.
  - Q7 says compounding.
  - Q8 confirms the political capital for a standing multi-party report exists.

  The executive sponsor makes the committee durable rather than merely slow; a committee without one is every veto and none of the protection.

**Delete, do not demote: no named line owner** - the event funded out of whichever discretionary pot has room that quarter. Not an ownership model, the absence of one. It fails silently: nothing signals a problem until the pot is empty and no function considers the event theirs to save. Detect it at Q4, when _who owns the line today_ has no answer.

The negotiation shape for each co-fund rung, the failure patterns behind each model, and the handover a departing owner has to leave are in [references/budget-ownership-and-review.md](references/budget-ownership-and-review.md).

## What this skill sends to review

Three exposures attach to a company-run event that a community-run one does not carry. Each names the review it triggers and the reversibility it spends, never an amount. Send all three out before the invitation and the registration form go live.

No specific rule, threshold or jurisdiction is named here. Those come from the company's own counsel.

- **The company's name on a room it does not fully control.** Legal review of the published terms, of how the code of conduct binds staff as well as guests, and of insurance. Reversibility: a published term can be revised for the next edition; an incident at this one cannot be revised at all.
- **The attendee list moving into the systems the sales organisation works from.** A personal-data decision, not a reporting one. It belongs to whoever holds the company's privacy obligations, and it happens before registration opens. Reversibility: a notice and lawful basis can be corrected going forward; a list already collected under the wrong one cannot be un-collected. Name no jurisdiction and quote no retention period; route the actual rule to the company's own counsel, the same way `samber/dev-event-organizer-skills@event-community-building` routes its member-list decision.
- **Customers and prospects hosted as guests.** Travel, hospitality and gifts sit under the company's own anti-bribery and gifting rules. They also sit under the guest's employer's rules, which are frequently stricter and are not the host's to waive; public-sector and regulated-industry guests are the common case. Reversibility: an invitation withdrawn costs a relationship; one accepted under a rule it breached cannot be undone.

## Failure modes

- **A pipeline goal with no join.** The number cannot be produced because nothing connects attendance to the sales systems. Q5 catches this before the goal is set, not after.
- **Attendance reported as the outcome.** Heads through the door is the number available when the real one is late, which is exactly why it is deleted from the goal menu.
- **The goal set after the event.** A goal chosen once results are in is a description of what happened. Register the four measurement fields before registration opens, or the event has no goal.
- **A goal the funding functions never agreed to.** Marketing writes a pipeline goal, sales never sees it, and the number arrives at a function that does not recognise it. Workflow step 5's coupling check exists to stop this.
- **The sole-owner line dying with its owner.** The cheapest ownership model is also the one with no successor. If Q7 says compounding and Q4 names nobody else, that combination is itself the finding.
- **A sponsor's objective language borrowed for the host's own goal.** The sponsor category set answers what a company buys at _somebody else's_ event. Reusing it imports a seller's frame into a funder's decision and narrows the goal to whatever a sponsorship would have delivered.
- **Goodwill treated as free.** It costs less to instrument, not less to run, and it is the first line cut when a budget owner needs a number. Choosing it accepts that exposure rather than avoiding a decision.
- **The goal changed mid-cycle without reopening the funding agreement.** Every funder bought a specific number; changing it without saying so turns a co-funded line into an argument at the review.
- **Generic-funnel drift.** A goal that reads identically with an email campaign substituted for the event is not this event's goal: it is a marketing-organisation metric with an event pointed at it. Every goal here must answer _did this event move it_.

## Measurement

Budget share, pipeline return rate and attendance-to-outcome rate swing too widely between companies for any industry figure to transfer. Every threshold here is self-set; declare that plainly in the deliverable.

Before registration opens, each chosen goal carries four fields:

- A named metric.
- A named owner inside the function that will report it.
- A named source system.
- A date the number will be read.

A goal missing any one of the four is a stated intention, not a goal. Iterate until every goal passes; this is the one gate this skill sets.

Self-set observables - pick two or three and write down in advance what each would change:

- **Goal-to-number latency**: the gap between the event and the date the number is readable. A gap longer than the funding cycle means the goal cannot defend its own line, however good the number turns out to be.
- **Funder attrition**: how many of the functions that signed the line still fund it the next cycle - the durability axis made observable.
- **Goal drift**: whether the goal `samber/dev-event-organizer-skills@event-debrief` scores the edition against is the goal set here. A mismatch is a finding about this skill's output, not the edition.
- **Counterfactual honesty**: whether any part of the outcome would have happened without the event. Frequently unknowable; say so plainly rather than claiming influence the data cannot carry.

Re-run this skill, rather than `samber/dev-event-organizer-skills@event-growth-strategy` or `samber/dev-event-organizer-skills@event-portfolio-strategy`, when any of these fires:

- The goal changes.
- A funder joins or leaves.
- The buyer-and-user answer changes because the product changed.
- The audience the invite list can assemble stops matching the goal.

## Invocation examples

- Our company wants to run a user conference next year and nobody can agree whether it exists for pipeline or for the community. Help us decide.
- Marketing owns our developer day but sales keeps asking for leads out of it. Should sales be co-funding it, and what changes if they do?
- We ran a roadshow and the CFO wants to know what it returned. What should we have measured, and what can we honestly say now?
- Our community day is free and marketing pays for it. Is that the right funding model for what we want out of it?

Expected output: a strategy brief containing:

1. The audience the invite list can actually assemble, stated separately from the audience wanted.
2. The buyer-and-user answer and what it permits claiming.
3. The goal mix with the rungs rejected and why.
4. The budget-ownership model with each funder and what each one is buying.
5. The four measurement fields per goal.
6. The three review items with their status.
7. The re-run triggers.

Delivered section by section for validation, with two or three candidate goal mixes and one recommendation up front when the goal is contested.

## References

- [references/goal-definitions-and-measurement.md](references/goal-definitions-and-measurement.md) - each goal rung defined for a company-run developer event, the instrumentation and the cooperating function each one needs, the buyer-and-user detail worked through, and the four-field measurement commitment with a positive and a negative example.
- [references/budget-ownership-and-review.md](references/budget-ownership-and-review.md) - the four ownership models in detail, the co-funding negotiation shape and what each funder is buying, the failure patterns behind each model, the handover a departing owner has to leave, and the three review items expanded with what does and does not transfer.

Sibling skills referenced throughout: see § What arrives already decided.
