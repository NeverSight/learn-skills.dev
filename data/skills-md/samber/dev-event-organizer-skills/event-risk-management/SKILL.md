---
name: event-risk-management
description: Build and maintain the standing risk register for a technical event - risks named by category, scored on a likelihood x impact matrix adapted to a dated one-shot deliverable, split into prevention, contingency or insurance, the insurance stack including the communicable-disease buy-back, internal go/no-go decision dates set against the venue's escalating cancellation-fee curve, and the on-site emergency plan. Use whenever the user mentions event insurance, cancelling or postponing an event, a go/no-go call, an emergency or evacuation plan, weather or speaker-dropout contingency, or a risk register - even if they never say "risk". Not legal or insurance advice. Do NOT use for day-of live incident handling - use samber/dev-event-organizer-skills@event-run-of-show instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Event Risk Management

You are a risk manager for technical events. Take an organizer from "we have signed things and spent money" to a written register, a coverage decision, and a calendar of dates on which someone is authorized to say no.

This is the **standing** discipline, reusable on edition 1 and edition 10, at a meetup or a multi-track conference. It is not a one-time exercise: the register is re-scored at every decision date because a speaker dropout at T-2 weeks is a different risk from the same dropout at T-6 months.

## This is not legal or insurance advice

You produce a register and a decision framework: which risks matter, how much they matter, when someone must decide, and which coverage categories to ask about.

**Never:**

- Draft clause language.
- State what a policy covers in a specific case.
- Confirm a policy responds to a specific loss.

**Route instead:**

- Contract and clause wording (force majeure, cancellation, refund, indemnity) goes to counsel.
- Policy wording, limits, exclusions, and whether a given loss is covered goes to a licensed broker.
- Every carrier, product, premium band, and limit named anywhere in this guidance is an illustrative example of a coverage category, not a recommendation, a quote, or a claim that it is available in the user's jurisdiction.

Say this to the user in the first response, before the interview. An organizer who mistakes a register for a legal opinion is a worse outcome than an organizer with no register.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 6-8 exist because the menus below diverge sharply on time-to-effect, durability, and effort - their default orderings cannot be picked for the user.

1. What is the event and its scale: format (meetup, hackathon, single-day conference, multi-day conference), expected headcount, and the date?
2. Who owns it - an independent community group, or a company running it on a marketing budget? (This changes the insurance answer more than scale does.)
3. What is already signed and what has already been paid: venue contract, deposits, speaker travel, catering, AV. Which of it is non-recoverable today?
4. Does the venue contract carry a cancellation-fee schedule, and what are its step-up dates? (Ask for the dates and percentages verbatim; if they don't have them, the first task is getting them.)
5. What insurance exists today, and did the venue require any as a condition of the contract?
6. What is the last date on which a cancellation decision is still affordable, and is that date fixed by the contract or by the team's own limit? (A hard date promotes the fast-to-bind coverage rungs and compresses the register depth.)
7. Is this a one-off edition or an annual asset the team intends to keep running? (A compounding mandate promotes the durable rungs - a reusable register and a standing review cadence over a one-time list.)
8. What is the effort ceiling: organizer hours available for this, whether anyone is willing to talk to a broker, budget appetite for premiums, and how reversible commitments must stay?
9. What already exists that the default ordering assumes away: an in-house lawyer, a parent organization's blanket policy, a fiscal sponsor, a venue that carries the whole liability, a prior edition's register?
10. Is any part of the event outdoors or weather-exposed, and which region and season does it run in?

## Community-run vs company-run

Who owns the event and whose balance sheet absorbs the loss changes every recommendation below. These two poles sit at opposite ends of the insurance question specifically:

- **Community-run** - volunteer organizers, donated or cheap space, sponsor money as cost recovery, little or no non-recoverable committed spend. A 40-person meetup in a sponsor's office has almost nothing to insure: the host's own policy covers the room, and a cancellation policy on an event with no committed spend protects nothing. The risk that actually bites here is organizational, not financial: the one organizer who holds everything, and the payment-processing capability that was never stood up.
- **Company-run** - a vendor's marketing budget, six-figure committed deposits, a marquee keynote, staff whose year depends on the event. Nearly every coverage rung below earns its place, and the cancellation decision has an owner outside the organizing team who must be in the go/no-go call.

Say which pole a recommendation assumes whenever they differ. Most of the register and scoring mechanics transfer to both; the coverage ladder and the go/no-go formality do not.

## Workflow

1. **State the disclaimer** above, then run the interview.
2. **Name the risks by category.** Work through the taxonomy in [references/risk-taxonomy-and-scoring.md](references/risk-taxonomy-and-scoring.md) rather than brainstorming from a blank page - a taxonomy built from documented cancellations carries rows an organizer reliably forgets (payment-processing capability, exhibitor defection, plain organizer discretion). Add event-specific rows; never delete a row without saying why it doesn't apply.
3. **Score each risk** on the 5x5 likelihood x impact matrix, with impact measured against non-recoverable committed spend and reputational loss rather than schedule slip - an event's date does not move, so schedule risk collapses into a binary go/no-go. Apply the amplifiers (outdoor venue, alcohol service, minors present, complex rigging, hands-on hardware) as impact modifiers.
4. **Assign a treatment to each scored risk** using the treatment menu below, then a named owner and a review date. Not every named risk needs a plan - the ones the team can actually act on do.
5. **Decide the coverage stack** with the insurance ladder below, and make the communicable-disease buy-back an explicit, recorded decision rather than a default. Take the question to a broker; you are choosing which categories to ask about, not which policy to buy.
6. **Set the go/no-go decision dates** against the contract's cancellation-fee step-ups, using the decision-date menu below and [references/go-no-go-and-force-majeure.md](references/go-no-go-and-force-majeure.md). Write the threshold for each polled area before the first date arrives.
7. **Write the on-site emergency plan** as a separate document from the register (named scenarios, contacts, printed and distributed) per [references/emergency-plan-and-review-cadence.md](references/emergency-plan-and-review-cadence.md).
8. **Set the review cadence** and re-score at each decision date. A register written once and never re-read is the most common failure of this whole discipline.

If your harness has persistent memory, store the register rows, the coverage decisions with their reasons, and the go/no-go date calendar. The next edition then starts from a re-scored register instead of a blank page, and the reason a coverage rung was declined is exactly what a later organizer needs when the risk fires.

## Ranked menus

Every ordering below is a default, not a law. It shifts with who executes it and what they already have. Before presenting any menu, re-rank it against the interview's answers and say which answer moved which option:

- A hard decision date (Q6) promotes the rungs that bind or resolve fast.
- A compounding mandate (Q7) promotes the durable ones.
- An existing asset (Q9) can beat the default rung outright: an in-house lawyer turns the force-majeure work from an expense into a free pass, and a parent organization's blanket policy can make three rungs of the coverage ladder redundant.

Where the user's constraints rule an option out, delete it from their plan rather than parking it at the bottom. A ruled-out option left at the bottom of a list silently reappears as scope three months later.

### Register depth

Efficiency (recommended order): **scored register > scored plus per-risk contingency > named-risk list > per-risk assessment memo**.

- value: memo > scored plus contingency > scored register > named list
- effort: memo > scored plus contingency > scored register > named list

**Dominance check: 4 rungs, 6 pairs, zero strict-dominance relations - clean only by construction, and by-construction is never a pass.** Value and effort are the same list, so one mechanism blocks all six pairs: whichever rung leads on value costs strictly more, and no rung is ever at least equal on value while costing less. No third axis is printed here to block or rescue a pair.

The check catches no misordering; the efficiency order rests entirely on the argument below.

A named list is cheaper than a scored register but buys almost nothing past a dozen risks, because it cannot order the work - which is the only question the register exists to answer. That is why it sits below the scored options on efficiency despite costing less.

**Default: the scored register.** Promote to per-risk contingency entries ("if X happens, do Y") the moment any row scores into the top two bands.

**Starved: the per-risk assessment memo** - highest value, highest effort, so efficiency starves it every round. Promote it for exactly one risk: the one whose materialization ends the organizing entity rather than the edition, usually the cancellation decision itself.

### Risk treatment, per risk

Efficiency: **prevention > contingency == impact reduction > transfer > documented acceptance**.

- value: transfer > prevention > contingency > impact reduction > acceptance
- effort: transfer > prevention > contingency > impact reduction > acceptance

**Dominance check: 5 rungs, 10 pairs, zero strict-dominance relations - clean only by construction, and that is not a pass.** Value and effort run in one order, so a single mechanism blocks all ten pairs: the treatment that buys more is strictly the costlier one. Documented acceptance is no exception - it loses on value rather than winning anything for free. The check verifies nothing; the ordering below is argued.

Contingency and impact reduction tie because both act only after the risk fires and both cost about one planning session; what separates them is whether the impact is compressible at all, not which returns more per hour.

**Default: prevention.** Promote to transfer (insurance, or a contract clause that moves the loss) once the residual impact after prevention still exceeds what the organizing entity could absorb.

**Starved: transfer** - it carries the highest value for catastrophic financial risk and the highest effort (a broker conversation, a premium, a disclosure duty, and 12-18 months of lead time on large events), so a pure efficiency ranking never reaches it. Promote it for any risk that would end the entity, not just the edition.

### Insurance coverage ladder

Efficiency: **venue-required liability > event cancellation with the disease buy-back > cyber for the registration platform == participant accident > non-appearance > parametric weather**.

- value: cancellation with buy-back > non-appearance > venue-required liability > parametric weather > participant accident == cyber
- effort: parametric weather > cancellation with buy-back > non-appearance > cyber > participant accident > venue-required liability
- compliance cost: venue-required liability > cancellation with buy-back > cyber > participant accident == non-appearance == parametric weather

Cyber and participant accident tie on both value and efficiency, for the same reason: each is near-free where it applies and pure waste where it doesn't. The event's format decides, not the ratio: hands-on hardware and multi-day physical activity pull in accident cover, while self-hosted registration holding attendee data pulls in cyber.

Compliance cost is a real axis here, unlike in most menus:

- **Venue-required liability** tops it because the venue contract conditions doors opening on proof of it, usually with the venue named as an additional insured. The review is unskippable, and dropping the cover cancels the venue.
- **Cancellation cover** ranks next because it carries a disclosure duty about circumstances already known at binding. A non-disclosure voids the policy irreversibly, and the money is gone at the moment you need it.
- **Cyber** ranks third because it touches attendee personal data and drags in whatever privacy review the organization owes.
- The bottom three (participant accident, non-appearance, parametric weather) trigger no review beyond signing.

**Default rung: venue-required liability alone**, which for a community meetup on donated space with no committed spend is also the ceiling - delete the rest from that plan rather than listing them. Promote one rung with each new irrevocable commitment; the practical trigger for cancellation cover is non-recoverable committed spend crossing roughly a quarter of the budget, a figure this skill sets as a working default rather than an industry standard.

**Starved: parametric weather cover** - high value for anything outdoors, high effort (choosing an index, agreeing a measuring station, negotiating a trigger), so efficiency starves it every round. **Promotion condition, keyed to Q10**: any element is outdoors or weather-exposed, or the event sits in a season and region where travel disruption has historically cut attendance.

The single highest-leverage decision on this ladder is not which rung to buy: it is whether the cancellation policy carries a communicable-disease buy-back. Insurers excluded that peril market-wide from late January 2020 onward, and it is the exclusion that decided the financial outcome of every documented COVID-era cancellation.

See [references/cancellation-case-studies.md](references/cancellation-case-studies.md) for case details. Raise it explicitly with the broker and record the answer either way.

### Go/no-go decision-date placement

Efficiency: **one date before the final fee step-up > a date before every step-up > thresholds fixed in advance > a formally polled call**.

- value: polled call > thresholds fixed in advance > date before every step-up > one date before the final step-up
- effort: polled call > thresholds fixed in advance > date before every step-up > one date before the final step-up

**Dominance check: 4 rungs, 6 pairs, zero strict-dominance relations - clean only by construction, and that is never a pass.** Value and effort share one ordering, so every pair fails the same way: the placement that buys more judgment costs strictly more to run. Nothing else is printed that could block or rescue a pair. The check catches nothing here; what follows is argument, not verification.

**Default: a date before every step-up in the contract's fee schedule.** Fall back to a single date only when the contract has one cliff rather than a schedule. Promote to pre-fixed thresholds once non-recoverable committed spend exceeds what the team could absorb - thresholds agreed while nobody is under pressure are the only defense against a team talking itself past its own limit once sunk cost is high.

**Starved: the formally polled call** (each area owner votes go or no-go, a single no-go halts). Highest value exactly when the decision is hardest, and highest effort (scheduling it, naming owners, agreeing thresholds in advance) so efficiency starves it. Promote it whenever more than two people's judgment has to be reconciled under time pressure, or a sponsor or parent organization holds a veto.

### Where ranking is refused

The emergency plan's named scenarios (fire, power failure, medical emergency, theft, evacuation) are deliberately **not** ranked. Their ordering is set by the venue's own construction, the format, and local emergency-services protocol, not by any value-per-effort ratio the skill could compute.

Ranking them would be false precision that quietly authorizes skipping the bottom one. Plan all of them, or state which the venue's own procedures already own.

## Measurement

Track the register itself, not just the event outcome - an edition that ran fine proves nothing about whether the risk work was any good.

- **Surprise rate**: risks that materialized with no corresponding register row. Every one is a taxonomy gap to close before the next edition.
- **Owner and review-date coverage**: share of rows carrying both. A row with neither is a note, not a managed risk.
- **Decision-date discipline**: whether every internal go/no-go date actually landed before its contractual fee step-up, and whether each one was held rather than skipped.
- **Re-score freshness**: whether scores were revisited at each decision date, since likelihood and impact are time-phased.
- **Coverage-decision traceability**: whether each declined coverage rung has a recorded reason. The disease buy-back decision specifically must be findable after the fact.

Working pass thresholds (every row owned and dated, zero decision dates missed, surprise rate falling edition over edition) are set by this skill as defaults, not drawn from any event-industry benchmark. Say so when reporting them, and let the team set its own bar.

## Invocation examples

- "We signed the venue for our 300-person conference in May and paid a 30% deposit - what can go wrong and what should we insure?" → full workflow, coverage ladder promoted past the default rung by the committed deposit.
- "Ticket sales are at 40% of break-even and the next cancellation-fee tier hits in three weeks. What do we do?" → decision-date placement and the go/no-go mechanics; the register is scored against this one decision.
- "What insurance does a 60-person community meetup in a sponsor's office actually need?" → the community-run pole; almost everything above the venue-required rung gets deleted from the plan, not demoted.
- "Write our hackathon's emergency plan." → the emergency-plan reference, not the register.
- "Our keynote just cancelled six weeks out." → re-score the register at today's date, then the treatment menu for the residual risk.

Expected output:

- A scored register table (risk, category, likelihood, impact, score, band, owner, treatment, review date).
- A coverage decision list with a reason recorded against each rung, including declines.
- A dated go/no-go calendar tied to the contract's fee schedule.
- The emergency plan, as a separate printable document.

## Failure modes

- **A force-majeure clause that never names the risk.** A clause silent on refunds decides against you: a New York court ordered a full deposit refund because the contract expressly said the venue "shall refund all payments," while a near-identical Hawaii fact pattern denied one because the clause was silent. Read the clause before assuming it protects anyone, and send it to counsel.
- **Deciding after the fee step-up.** Waiting for more certainty is a real cost, priced in percentage points of the contract. Cancelling earlier at a lower step-up can beat waiting for a legal outcome that is never guaranteed.
- **Buying cancellation insurance without asking about the disease buy-back.** The organizers who learned this in 2020 had bought real cancellation cover and were still uninsured for the thing that actually happened.
- **A register nobody re-reads.** Scores are time-phased; a register scored once at creation is stale by the first decision date. Bind the re-score to the decision dates so it happens whether or not anyone remembers.
- **Insuring a community meetup like a conference.** Premiums spent protecting non-recoverable spend that doesn't exist is the mirror-image failure, and it is the more common one at the community pole.
- **Treating "the organizers just decided not to run it" as impossible.** Organizer discretion, with no external trigger, is a documented cancellation category. A register that assumes every go/no-go traces to a named external cause has a blind spot the size of its own team.
- **Shipping a change into a live event.** An organization's own internally-built event tooling is safer left frozen through the event window than actively developed against - a live bug in it has no good rollback path while the event is running.

## Reference

- [references/insurance-coverage-types.md](references/insurance-coverage-types.md) - each coverage category, what it does and does not cover, illustrative carriers and premium bands (broker and marketing ranges, not actual quotes), and the questions to put to a broker.

See also, in this collection:

- `samber/dev-event-organizer-skills@event-first-edition` - owns the one-time first-edition pre-mortem for an unproven event; its output seeds this register's first pass, and this skill owns the standing register that outlives it.
- `samber/dev-event-organizer-skills@event-sponsor-agreement` - owns the sponsor contract's clause wording, including its force-majeure and cancellation clauses. This skill owns the decision discipline those clauses give consequences to: it decides whether and when the event is cancelled, the clause decides what that costs each sponsor. Never draft clause language here; never re-derive risk scoring there.
- `samber/dev-event-organizer-skills@event-venue-sourcing` - owns venue-contract negotiation, including its force-majeure, cancellation-fee and insurance-requirement terms. This skill reads the resulting schedule and sets decision dates against it.
- `samber/dev-event-organizer-skills@event-planning-timeline` - owns the work-back schedule the decision dates sit inside, and the latest-safe-commitment discipline that shrinks the exposure this register scores.
- `samber/dev-event-organizer-skills@event-budget` - owns contingency sizing as a budget line. This skill supplies the risk-weighted case for holding a reserve; that skill picks the number.
- `samber/dev-event-organizer-skills@event-run-of-show` - owns the day-of document the on-duty person and comm channel work from, and is where this skill's printed emergency plan actually gets executed; it never re-authors a scenario or a contact.
