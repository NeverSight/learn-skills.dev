---
name: business-event-formats
description: Choose which company-run event shape to run - invite-only dinner, executive summit, single-city user conference, multi-city roadshow, or a floor-primary trade-show event - plus how its program is sourced and what shape its floor takes. Use whenever a company weighs a user conference against a roadshow or a summit, asks what kind of event to put on for developers, customers or partners, or asks whether to run its own floor or exhibit on someone else's, even if they only say "we want to do an event". Format catalog only. Do NOT use for track count or session mix - use samber/dev-event-organizer-skills@event-format-selection; for floor operations use samber/dev-event-organizer-skills@event-booth-experience; for goals and budget use samber/dev-event-organizer-skills@corporate-event-strategy.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Business Event Formats

You pick which company-run event shape a company runs this year: invite-only dinner or roundtable, executive summit, single-city user conference, multi-city roadshow, or floor-primary event. Pick how its program is sourced, and for floor-primary shapes, which of three floor shapes it takes.

Decide the shape and stop. Track count and session mix, floor operations, goals and funding, and positioning claims each belong to a sibling (§ Sibling skills that own adjacent ground). Never re-derive them.

Say **company-run** and **community-run**. Use those two pole names everywhere, even when a user says "corporate": mirror their meaning, not their label.

## Sizing constraints

State no headcount, city count, agenda length, ticket price, or budget figure, here or in any deliverable built from this skill. Every such number would be invented, and an invented number outlives its caveat.

Every effort, value and compliance ordering below is argued from these shapes' mechanics and contestable on its own terms: a reasoned default, not an industry ranking.

## Sibling skills that own adjacent ground

- **`samber/dev-event-organizer-skills@event-format-selection`**: owns the community-pole shape ladder, track count, session mix, delivery mode and hackathon demo structure. It hands "the vendor-side format family in depth" here by name. Once the shape is named, track count and session mix are its decision, not this skill's.
- **`samber/dev-event-organizer-skills@event-booth-experience`**: owns the expo floor as a system: layout, tier-to-spec catalog, setup and teardown windows, staffing, traffic mechanics. The floor-shape menu here stops at naming the shape. Hand every physical question over; never restate a layout, tier spec or traffic mechanic inline. It serves the organizer who owns the hall, not a company exhibiting on someone else's floor, so that menu's third rung hands off to nothing. Say so rather than improvising.
- **`samber/dev-event-organizer-skills@corporate-event-strategy`**: names this skill by `owner/repo@skill` as owner of the company-run shape catalog, and tells its reader never to re-derive which shape to run. It owns the goal mix, the funding and the measurement commitment: this skill answers _which shape_, that one answers _why, funded by whom, measured how_. It does **not** own access pricing, which is `samber/dev-event-organizer-skills@event-ticket-pricing`'s.
- **`samber/dev-event-organizer-skills@event-positioning`**: its governance spectrum argues what a company-run event can honestly claim about itself, including the roughly 30-40% single-vendor-content share above which a neutrality claim is forfeit (a reasoned default, not an industry standard). The program-sourcing menu picks the posture; that skill decides what the posture entitles the event to say. Cite it, and never re-derive an identity claim here.

The sponsor block (`samber/dev-event-organizer-skills@event-sponsor-value-proposition`, `-pricing`, `-prospectus`, `-agreement` and `-fulfillment`) owns none of this. A summit and a roadshow change what a sponsor is buying; this skill states the shape, and those skills price and deliver against it.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 3, 6, 8 and 10 exist because the menus below diverge on which value is being bought, not merely on how much it costs. Those defaults cannot be picked for the user.

1. Which decision is on the table: the whole shape from scratch, or one axis (program sourcing, floor shape)? Skip menus already settled.
2. Who is the intended attendee, named: existing customers, buyers inside a target-account list, the broad developer public, or partners and ecosystem builders?
3. Is this edition's goal **volume** of qualified conversations, or **penetration of a named account list**? If a list exists, how long: a handful, a page, or a market? This selects the value axis the shape ladder ranks on. Without it the ladder cannot be ordered at all.
4. Do you already have an audience that will travel to you: a customer base, a mailable list, a past edition's registrations? Evidence, not impressions.
5. Is there a launch or announcement this event must carry, and is its date fixed?
6. Who is being marketed to as an attendee: customers only, or people who are not customers yet? (A "not yet" changes what the program may honestly consist of.)
7. Is this a one-off bet or a compounding annual property?
8. What is the effort ceiling: how many people can own this end to end, how much runway exists, and how much political capital to tell an executive their slot is not on the agenda?
9. What already exists that would overturn a default: a field-marketing team running city events, a venue you control, a partner ecosystem exhibiting elsewhere, an advisory board already meeting, a recorded-content pipeline?
10. Is the partner and ecosystem story what you are selling this year, or is the product?

## Workflow

1. Run the interview; skip settled menus (Q1).
2. Confirm this is a company-run event. If the user is a community or volunteer organizer, route to `samber/dev-event-organizer-skills@event-format-selection` and stop: its ladder serves community-run events.
3. Fix the value axis from Q3 before touching the shape ladder. Volume selects the reach axis; a named account list selects the account-depth axis.
4. Pick the **shape** from the ladder, applying its delete rule before ranking anything.
5. Pick the **program-sourcing posture**, applying its delete rule.
6. Floor-primary shapes only: pick the **floor shape**, then hand everything physical to `samber/dev-event-organizer-skills@event-booth-experience`.
7. Load [references/company-run-format-catalog.md](references/company-run-format-catalog.md) for what each shape actually is: room, invitation model, agenda shape, what it cannot do, and which sibling each shape's open question routes to.
8. Present 2-3 candidate shapes with trade-offs and one recommendation. Validate section by section, never as one block, and get explicit approval before finalizing.
9. Hand off: the chosen shape goes to `samber/dev-event-organizer-skills@event-format-selection` for internal structure, to `samber/dev-event-organizer-skills@corporate-event-strategy` for goals and funding, and to `samber/dev-event-organizer-skills@event-positioning` for what the shape entitles you to claim.

Every ranking below is a default, not a law. It shifts with context and with who executes it. Re-rank all three menus against Q9 before recommending anything:

- A field-marketing team already on the road makes the roadshow's marginal city near-free and promotes it a rung.
- An advisory board already meeting makes the summit nearly an agenda change rather than a new event.

If your harness has persistent memory, record the chosen shape, the value axis Q3 selected, and the condition that would flip it. Next year's shape review starts from that condition instead of re-arguing the ladder.

## Company-run event-shape ladder

Which shape the company runs. **The two value axes are exact inverses of each other.** That inversion is the decision, and why Q3 comes first.

- effort (runway, coordination touches, travelling headcount, political capital, reversibility): `floor-primary event > multi-city roadshow == single-city user conference > executive summit > invite-only dinner or roundtable`
- value by **reach** (people reached per edition, including people who didn't already know the company): `floor-primary event > multi-city roadshow > single-city user conference > executive summit > invite-only dinner or roundtable`
- value by **account depth** (named target accounts materially moved - a decision-maker in a real conversation about their own situation): `invite-only dinner or roundtable > executive summit > single-city user conference > multi-city roadshow > floor-primary event`
- compliance cost (the review it triggers at the _guest's_ employer, and what stops being reversible): `invite-only dinner or roundtable > executive summit > multi-city roadshow > single-city user conference == floor-primary event`
- efficiency **if Q3 said volume** (reach per unit effort): `multi-city roadshow > single-city user conference > floor-primary event > executive summit > invite-only dinner or roundtable`
- efficiency **if Q3 said named accounts** (account depth per unit effort): `invite-only dinner or roundtable > executive summit > single-city user conference > multi-city roadshow > floor-primary event`

Both ties are argued, not hedged:

- **Effort tie** (`multi-city roadshow == single-city user conference`): both spend comparable total effort in incompatible shapes. One concentrates it into a single venue commitment; the other spreads it across repeated cancellable productions.
- **Compliance tie** (`single-city user conference == floor-primary event`): both sign the same ordinary venue and vendor paper. Hosted hospitality for a named guest creates a per-guest obligation neither does, and a roadshow adds a per-jurisdiction consent review instead.

The account-depth efficiency line discriminates nothing. It is rank-identical to the account-depth value axis and to inverse effort at once, so it only confirms the Q3-named-accounts case.

No pair strictly dominates. The two value axes reverse across all five rungs, so the ranking is clean by construction, not by care. See [references/ranking-dominance-analysis.md](references/ranking-dominance-analysis.md) for the full pairwise check.

- **Invite-only dinner or roundtable**: the default when Q3 names a short account list. Top of account depth, bottom of everything else, and the only shape committable inside a quarter. **Delete it when Q3 has no named account list**: with nobody specific to invite, it degrades into a generic mixer buying neither axis. Cut it from the menu and from every axis line above, rather than leaving it at the bottom to reappear as scope.
- **Executive summit**: a curated, hosted, senior-audience room. Second on depth and second-cheapest, it is the safe promotion from a dinner once the list outgrows one table. Its live risk is compliance, not budget.
- **Single-city user conference**: the default when Q3 says volume **and** Q4 confirms an audience that will travel to you. It is the only shape that becomes an owned annual property, which is why Q7's compounding answer promotes it past the roadshow despite the roadshow leading reach-efficiency.
- **Multi-city roadshow**: leads reach per unit effort because later stops reuse one deck, one crew and one run-of-show while the first stop absorbs the setup. That marginal structure is the whole argument for it. Where a city stops paying back depends on the company, so set a per-city stop rule in advance and route the economics to `samber/dev-event-organizer-skills@corporate-event-strategy` rather than guessing a count.
- **Floor-primary event**: **the starved option on both efficiency lines.** Top of reach, bottom of depth, top of effort, so neither line ever picks it. Promotion condition: Q4 says you have no audience that will travel **and** Q10 says the ecosystem rather than the product is what you're selling. Only then is the floor the sole shape that puts you before a crowd someone else assembled. Absent both, it loses every round, correctly.

## Program-sourcing posture

Who supplies the content. **Two value axes, again exact inverses.** This menu decides the posture only. What the posture entitles the event to _claim_ about itself belongs to `samber/dev-event-organizer-skills@event-positioning`; how the resulting sessions are formatted belongs to `samber/dev-event-organizer-skills@event-format-selection`.

- effort (sourcing, review, rehearsal, approvals, political capital to refuse an internal speaker): `open submissions with the company as named host > mixed practitioner program with labelled company slots > customer-story program > company-supplied program`
- value by **credibility** (a technical audience believes and repeats what it heard): `open submissions with the company as named host > mixed practitioner program with labelled company slots > customer-story program > company-supplied program`
- value by **message control** (the launch narrative lands intact, on schedule): `company-supplied program > customer-story program > mixed practitioner program with labelled company slots > open submissions with the company as named host`
- efficiency (credibility per unit effort): `mixed practitioner program with labelled company slots > customer-story program > open submissions with the company as named host > company-supplied program`
- efficiency (message control per unit effort): `company-supplied program > customer-story program > mixed practitioner program with labelled company slots > open submissions with the company as named host`

The message-control efficiency line discriminates nothing. It is rank-identical to inverse effort and to the control value axis at once, so it reduces to cheapest-first. Never let it pick the posture alone; use it only to see what the credibility ordering costs.

No pair strictly dominates. Credibility and message control reverse each other across all four rungs, the same mechanism that keeps the shape ladder dominance-free. See [references/ranking-dominance-analysis.md](references/ranking-dominance-analysis.md) for the full check.

- **Mixed practitioner program with labelled company slots**: the default. Buys most of open submissions' credibility without the review cycle, provided company slots are labelled as such rather than dressed as neutral content.
- **Customer-story program**: customers on stage, company framing. It looks cheap until reference approval and legal sign-off per customer are counted. Promote it when Q9 named a customer advisory board that already meets.
- **Open submissions with the company as named host**: **the starved option.** Top of credibility, top of effort, so efficiency never picks it. Promotion condition: Q7 says compounding annual property **and** Q8 confirms the political capital to tell an executive their slot did not make the program. Without that second answer, the posture collapses into a company-supplied program with extra administration, the worst cell on this menu.
- **Company-supplied program**: legitimate at a customers-only event where everyone came to hear the roadmap. **Delete it when Q6 says people who are not customers yet are being marketed to**: the program then fails the neutrality test `samber/dev-event-organizer-skills@event-positioning` owns, and the shape or the marketing has to change. Cut it from this menu and from every axis line above.

## Floor shape

Run this menu **only** when the shape ladder landed on the floor-primary rung. It decides which floor shape the event has and nothing else. Every physical question that follows (layout, tiers, specs, schedules, staffing, traffic) belongs to `samber/dev-event-organizer-skills@event-booth-experience`. Route it; never answer it here.

- effort (production, exhibitor recruitment and servicing, floor coordination): `program-plus-floor event > own showcase floor > presence on a third party's floor`
- value by **ecosystem visibility** (partners and third parties staking something public on your platform): `program-plus-floor event > own showcase floor > presence on a third party's floor`
- value by **borrowed buyer access** (qualified people in the room you didn't have to assemble): `presence on a third party's floor > own showcase floor == program-plus-floor event`
- efficiency (ecosystem visibility per unit effort): `own showcase floor > program-plus-floor event > presence on a third party's floor`
- efficiency (borrowed buyer access per unit effort): `presence on a third party's floor > own showcase floor == program-plus-floor event`

The borrowed-access tie is argued at zero: both own-floor rungs fill their own room without borrowing an attendee, so their ratio stays zero whatever effort is spent. That is also why the second efficiency line ties them at the bottom rather than separating them.

No pair strictly dominates. The two third-party-rung pairs split because ecosystem visibility runs opposite to both effort and borrowed access. The remaining pair, own showcase against program-plus-floor, splits on ecosystem visibility against effort once the zero tie is set aside. See [references/ranking-dominance-analysis.md](references/ranking-dominance-analysis.md) for the full mechanism.

- **Own showcase floor**: the default and ecosystem-efficiency leader, because a floor without a full program alongside it is where partner visibility is bought most cheaply.
- **Program-plus-floor event**: **the starved option.** Top of ecosystem visibility, top of effort, so it never wins an efficiency round. Promotion condition: Q10 says the ecosystem rather than the product is what you're selling this year, so the program exists to give partners something to be adjacent to.
- **Presence on a third party's floor**: pick this when Q4 produced no audience of your own. It is the only rung that borrows an assembled audience, and the only one this collection cannot support afterwards: `samber/dev-event-organizer-skills@event-booth-experience` serves the organizer who owns the hall, not a company exhibiting on it. Say that limit out loud instead of improvising booth advice.

## Failure modes

- **Ranking the shape ladder before Q3 is answered.** The two value axes are exact inverses, so an unanswered Q3 leaves the ladder genuinely unordered. A recommendation made anyway is really a recommendation to run the cheapest thing.
- **Reading the reach axis as the value axis.** Reach tracks effort almost exactly here, so ranking on reach alone picks the floor-primary rung that neither efficiency line ever chooses. It also makes the dinner disappear for the reader whose whole job is a short named account list.
- **Treating a summit or a dinner as low-risk because it is small.** It is top of the compliance axis: hosted hospitality for a named guest lands on that guest's employer's gift policy, and an accepted invitation cannot be quietly withdrawn.
- **Inventing a roadshow city count, a summit headcount or a dinner seat count.** None has a defensible default; each follows from the room, the list and the runway in front of you. Set a per-city stop rule and describe rooms qualitatively instead.
- **Answering floor questions inside this skill.** The moment the conversation reaches layout, tiers, power or setup windows, it has left this skill. Hand it over mid-sentence.
- **Deciding the shape and the goals together.** Shape is here; goal mix, funding and metrics are `samber/dev-event-organizer-skills@corporate-event-strategy`. A shape chosen to fit a metric nobody agreed on gets rebuilt after the budget conversation.
- **A company-supplied program marketed to non-customers.** That is the delete condition on the sourcing menu, not a rung to demote. It is the failure `samber/dev-event-organizer-skills@event-positioning`'s neutrality threshold exists to catch.
- **Copying a named company's shape without its constraints.** The precedents describe how those companies talk about their own events, not a template. Import the reasoning; the audience, launch cadence and installed base are not transferable.

## Measurement

Every check below is a gate set in advance, not a threshold read off a benchmark. These shapes vary too much between companies for a shared bar to mean anything. Whether the event succeeded on its own terms belongs to `samber/dev-event-organizer-skills@corporate-event-strategy`; what follows only tests whether the _shape_ was the right one.

- **Shape-versus-axis check**: name in advance, in writing, what the shape had to move on the axis Q3 selected: accounts touched for depth, or people reached for volume. A shape that scored well on the axis not picked chose the wrong rung, however good the event felt.
- **Roadshow stop rule**: fix before the first city what a stop must return for the next one to run, and hold to it. This is the only defence available against a marginal-city question that has no general answer.
- **Sourcing-posture check**: if the posture was mixed or open, count how many company slots ended up on the program against what was planned. Drift here is what turns a labelled program into the deleted rung by accident.
- **Floor-shape check**: count exhibitors who returned, not attendees who walked past. Attendee traffic reads on the floor's operation, which is `samber/dev-event-organizer-skills@event-booth-experience`'s outcome, not this skill's.

## Invocation examples

- "We ship a developer platform and marketing wants a user conference next year. Is that the right shape, or should we run city events?"
- "We have eleven target accounts and a quarter. What kind of event moves them?"
- "Should we run our own floor for partners, or just take a big booth at the industry show?"
- "Our summit agenda is all product marketing. Is that a problem if we are inviting prospects?"

Expected output: a shape brief with:

1. The value axis Q3 selected and why.
2. The chosen shape with the rungs deleted and the reason each was cut.
3. The program-sourcing posture and what it entitles the event to claim.
4. The floor shape when one applies.
5. For each choice, the interview answer that would flip it next year.
6. An explicit list of the questions handed to `corporate-event-strategy`, `event-format-selection` and `event-booth-experience`.

Presented section by section for validation, with 2-3 candidate shapes and one recommendation up front.

## References

- [references/company-run-format-catalog.md](references/company-run-format-catalog.md): what each shape actually is (room, invitation model, agenda shape, what it cannot do), how a roundtable differs from a dinner and a summit from both, and the sibling each shape's open question routes to.
- [references/vendor-conference-precedents.md](references/vendor-conference-precedents.md): named, dated company-run conference self-descriptions, each attributed to the company that published it, plus the transposition note stating what corporate-events-industry material does not carry over to a developer audience.
- [references/ranking-dominance-analysis.md](references/ranking-dominance-analysis.md): the full pairwise dominance check and tie justification behind each of the three ranked menus above.
