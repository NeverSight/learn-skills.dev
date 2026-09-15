---
name: event-hospitality
description: Decide the food, drink and social provision every population at a technical event shares - the catering service style and the dietary counts it has to carry, what a scheduled break contains, the event's alcohol posture, and whether an evening or social programme exists and in what form. Use whenever asked what format to feed a conference in, how catering should cover dietary restrictions across a whole event, what to put in a coffee break, whether to serve alcohol or run the event dry, or what to do on the evening of a conference day. Sets the shared floor only. Do NOT use for how many social occasions run - use samber/dev-event-organizer-skills@event-official-social-program - or which dietary needs the event commits to - use samber/dev-event-organizer-skills@event-accessibility-inclusion.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Event Hospitality

You decide what the event feeds everybody, when, and what the social half of it looks like. Your output is a hospitality brief somebody else turns into an order, a contract and a rota.

Four decisions:

- The catering service style.
- What a scheduled break contains.
- The alcohol posture.
- Whether an evening or social programme exists.

Set the shared floor, never a population's top-up. Every other hospitality skill layers on it: `samber/dev-event-organizer-skills@event-speaker-experience` and `samber/dev-event-organizer-skills@event-attendee-experience` each add only their own population's layer on top of these fundamentals. Never re-decide a speakers' dinner, a volunteer meal, or a VIP table.

## Two adjacent scopes you do not own

Both are routinely filed under hospitality. Reclaiming either duplicates a sibling skill:

- **Signage, wayfinding and facilities** belong to `samber/dev-event-organizer-skills@event-attendee-experience` outright: it designs the wayfinding, locates the quiet room and places the meal line in the floor plan.
- **Welcome register, staff warmth, MC tone and catering-as-identity** belong to `samber/dev-event-organizer-skills@event-cultural-identity`, which already claims catering as a touchpoint of the register. Execute inside whichever register it set; never redesign it.

What survives is food, drink, breaks, alcohol and the evening.

## Where every boundary sits

| Sibling                         | The line                                                                                                                                                                                                    |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `event-vendor-sourcing`         | Sources, vets, contracts the caterer from your decision; owns delivery buffers, lead times, the fire-code trap. Decide the style; never the supplier or contract term.                                      |
| `event-attendee-experience`     | Owns on-site distribution choreography (table, line, how a restricted meal reaches the right person) - refuses to rank its two fulfilment models since your style decision is what the contract carries.    |
| `event-accessibility-inclusion` | Decides which dietary needs the event commits to and at what depth. Never invent that list; choose a style that can carry it.                                                                               |
| Alcohol (one-sided seam)        | You set the default posture and design the alcohol-free provision; `event-accessibility-inclusion` owns it only where a medical/religious/recovery accommodation turns a default into an access commitment. |
| `event-schedule-design`         | Places breaks and lunch in the grid. You own what a break contains and hand it the service window needed; never move or lengthen a slot.                                                                    |
| `event-no-show-management`      | Owns the expected-show-up number. Take it; never derive your own.                                                                                                                                           |
| `event-venue-sourcing`          | Negotiates the F&B minimum and mandated-caterer clause. Your style/headcount are inputs, never terms you sign.                                                                                              |
| `event-volunteers`              | Owns food at the post as a shift mechanic.                                                                                                                                                                  |
| `event-volunteer-experience`    | Owns the off-duty top-up, inheriting dietary/allergen/alcohol exposure from this skill's output.                                                                                                            |

Every ranking below is a default, not a law. Re-rank all four menus after the interview, against what you already know about this event. Each of these overturns a default rung:

- A mandated-caterer venue running its own bar.
- A room with no seated capacity.
- A sponsor who already bought the coffee.
- A community whose evening is the reason people come.
- A team with nobody free to own an evening.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 8-10 exist because the menus diverge sharply on effort, durability and time-to-effect: nobody can pick those defaults for the user.

1. What does the published grid give you - meal-sized gaps, breaks, lengths, catering windows the venue fixed? Take these; never move them.
2. Does the room seat the whole population, or standing/circulating only? May outside food and drink enter?
3. Which dietary categories has the event committed to, and at what depth? Ask; never invent the list.
4. What are the declared counts, collected from everyone fed (attendees, speakers, volunteers, organizers, sponsor staff) or only registered attendees?
5. What number are you feeding, and where from? An expected-show-up figure, never a registration count.
6. What did venue and supplier answer on equipment/service: open flame, chafing dishes, who may serve, mandated caterer, house bar?
7. Has any sponsorship already sold the coffee, lunch, or evening as a named branded surface? If yes, that rung's budget and effort aren't yours.
8. One-off or recurring, where the evening is part of why people return? What register did culture work set for the meal? Does the audience's social norm include drinking?
9. Effort ceiling: named evening owner, catering budget line, volunteer hours for replenishment, what last edition left you?
10. By what date must each decision be final - headcount guarantee, equipment/licence lead times, evening venue hold date? Those dates, not the event date, rank these menus.

## Who controls the food

Two axes discriminate here. Say which pole a recommendation assumes whenever they differ.

- **Who controls the food and bar, you or the building.** A mandated-caterer venue, universities being the named case, decides most of the catering style and half of the alcohol posture before you rank anything. Ask Q6 first.
- **Community-run against vendor or corporate-run.** Barely moves the first three menus. It reshapes the evening programme, where a paid owner and a second venue are ordinary at one pole and exceptional at the other.

## Workflow

1. **Write down what you may not move**: the grid's gaps and catering windows, the accessibility bar's dietary categories, the expected-show-up number, the culture work's register. Anything conflicting is an ask routed to that sibling.
2. **Collect dietary counts before choosing anything** - from everyone fed, not only registered attendees. The input every rung ranks against, and the one most often gathered last.
3. **Pick the catering service style**, checked against the counts and Q6's venue answers. A style the building forbids is not a style.
4. **Decide what a break contains**, handing `event-schedule-design` the service window as a requirement, never a grid edit.
5. **Set the alcohol posture** before anyone books a room for the evening - it's cheaper to answer now than after a venue is held.
6. **Decide whether an evening programme exists**, and publish the answer either way. An unannounced absence sends people to an unhosted bar.
7. **Write the hospitality brief**: style/counts to `event-vendor-sourcing`, distribution requirements to `event-attendee-experience`, alcohol posture to `event-risk-management` and `event-code-of-conduct`, evening scope to whoever owns it.
8. **Present the brief section by section for approval** before anything is ordered.

If your harness has persistent memory, record per edition:

- The declared counts against the counts actually served.
- Which restrictions the supplier could not cover, and which fallback was used.
- How long the longest meal queue ran.
- What was left over.
- Who stayed for the evening.
- The exact settings of any keep-warm or holding equipment, including one that failed. A wrong setting fails silently, so the same equipment gets re-guessed every edition unless the working one is written down.

Next edition ranks against that record instead of these defaults.

## Catering service style

How food physically reaches people. Four rungs, built out from the sourced pair of plated-or-individual and family-style shared platters. The four-rung ladder, both value axes and every ordering below are this skill's own construction.

Value splits two ways, and each way orders the rungs differently:

- **Everyone fed and correctly matched** - every declared restriction reaches the person who declared it.
- **The meal as the shared moment** - the grid's longest gap is spent on it, and the style decides whether people spend it around the same dish or holding their own item somewhere else.

Fancier is not better on either axis.

Ranking (default, not a law - Q2, Q4 and Q6 re-rank it):

- effort (equipment, service staffing, room setup, per-guest matching, venue answers you must clear): `plated per-guest service > family-style shared platters > self-serve buffet with posted allergen labelling > individually packaged labelled meals`
- value, everyone fed and correctly matched: `individually packaged labelled meals > plated per-guest service > self-serve buffet with posted allergen labelling > family-style shared platters`
- value, the meal as the shared moment: `family-style shared platters > plated per-guest service > self-serve buffet with posted allergen labelling > individually packaged labelled meals`
- compliance cost (review triggered, reversibility spent): `family-style shared platters > self-serve buffet with posted allergen labelling > plated per-guest service > individually packaged labelled meals`
- efficiency: `individually packaged labelled meals > self-serve buffet with posted allergen labelling > family-style shared platters > plated per-guest service`

No rung dominates: the value axes oppose each other, and plated beats buffet on both value axes and compliance but loses on effort alone. Pair-by-pair proof: [references/service-styles-and-dietary-carry.md](references/service-styles-and-dietary-carry.md).

- **Individually packaged labelled meals** (default) - each meal handed over as its own item: lowest cost, top being-fed value, a restricted meal unambiguous. Assumed by `event-attendee-experience`'s separate-table model. Move up one rung when Q1's gap absorbs a line, Q2 seats people, Q4's counts are thin enough for a labelled station without per-person matching.
- **Self-serve buffet with posted allergen labelling** - a line with allergen detail posted before it forms. Higher throughput, genuinely social. Fails one way: a restricted dish taken by the wrong person. Never run unlabelled.
- **Family-style shared platters** (starved rung) - tops shared-moment value and compliance cost, so efficiency never picks it. Needs a longer pre-service setup window. Promote when Q8 says the edition recurs and culture work wants the shared table. **Delete outright when Q6 says the venue restricts open flame or chafing dishes.**
- **Plated per-guest service** (starved rung) - tops effort, second on both value axes, never wins the ratio. Turns a restriction into a plate rather than vigilance. Promote when Q2 seats the whole population, Q4 shows dense restrictions, Q6/Q9 confirm service staff exist. Part of its effort cost is easy to undercount: cutlery and crockery add a dishwashing bottleneck a tray-served style never creates. On a volunteer-served multi-meal event, weigh that bottleneck against perceived formality.

**Deleted, never demoted:** the same buffet with nothing labelled. It would win efficiency outright, which is exactly why it cannot sit on that line. It is the buffet with the declaration removed, and the person the declaration was for is the one who finds out.

## What a break contains

What sits in a gap the grid already placed, decided per break and not settled once a day. Four rungs, this skill's own construction.

Every rung is the rung below it plus something. Effort and value therefore run in the same order, so no rung beats another on value while costing less: the menu comes out clean by construction, which is not evidence that it is right. Check it against Q1's actual gap lengths and Q2's outside-food answer, never against the ranking itself.

Ranking (default, not a law - Q1, Q7 and Q9 re-rank it):

- effort (setup, a per-break owner and the volunteer hours behind them, budget line): `catered break bar with dietary-labelled stations > snack-enhanced break > owned replenishment at each break > standing self-serve water and hot drinks`
- value (people who stay in the building and come back into the room, and whose break is not spent hunting): `catered break bar with dietary-labelled stations > snack-enhanced break > owned replenishment at each break > standing self-serve water and hot drinks`
- compliance cost (review triggered, reversibility spent): `catered break bar with dietary-labelled stations == snack-enhanced break > owned replenishment at each break == standing self-serve water and hot drinks`
- efficiency: `owned replenishment at each break > snack-enhanced break > standing self-serve water and hot drinks > catered break bar with dietary-labelled stations`

Compliance ties: the upper pair ties because any break carrying food triggers an allergen declaration regardless of station count. The lower pair ties at honest zero - water and hot drinks declare nothing.

Size the chosen rung against a per-attendee catering convention rather than against richness alone: [references/break-quantities-and-service-flow.md](references/break-quantities-and-service-flow.md) carries the quantities.

- **Owned replenishment at each break** (default) - a standing station with a named person restocking against the grid's break times. Leads efficiency by removing the actual failure: a station empty the minute the room arrives. Costs a rota slot. Move up when Q1 shows a gap long enough that people leave the building.
- **Snack-enhanced break** - food alongside drinks, allergen detail posted. First rung carrying a declaration duty; keeps people on site.
- **Standing self-serve water and hot drinks** - up all day, refilled when noticed. Ranked below the snack rung because its whole advantage - availability any minute - is worth least at the minutes that matter.
- **Catered break bar with dietary-labelled stations** (starved rung) - tops value and effort together, so efficiency never picks it. Promote only when Q1 shows no meal-sized gap at all, or Q7 says a sponsor bought the coffee as a named branded surface.

**Deleted, never demoted:** the station set up once in the morning and never touched. A refilled provision reads as provision; an empty urn by mid-morning reads as broken. Absent is a posture. Broken is a complaint.

## Alcohol posture

Whether the event serves alcohol, and on what terms. A decision, not a default to drift into, and cheapest to make before a room is held.

**Nothing here is legal advice.** Licensing, service certification and liability differ by country, city and venue. Route every specific question to the venue, the caterer and the licensing authority. What follows names the review each rung triggers, never whether it is lawful.

Three rungs and their orderings, this skill's own construction. Ranking (default, not a law - Q6, Q8 and Q9 re-rank it):

- effort (arrangements to make, staffing to brief, a cap to design and hold): `bounded hosted service > cash bar > no alcohol served`
- value (a social half of the event everybody can be in, that nobody leaves because of what is served or how much): `bounded hosted service > no alcohol served > cash bar`
- compliance cost (review triggered, reversibility spent): `cash bar > bounded hosted service > no alcohol served`
- efficiency: `no alcohol served > bounded hosted service > cash bar`

The compliance ordering runs against intuition. The cash bar tops it on the fewest organizer hours: selling is commonly a different permission from serving, it sits with whoever operates the bar, and the terms come with it, unchangeable once the bar is contractually open. Bounded hosted service triggers a review you own and can shrink with the cap, and no alcohol served is the honest zero.

- **No alcohol served** (default) - a posture, not an omission. No licence, no brief, no insurance question, excludes nobody. Real cost: drinking relocates to an unhosted venue where the code-of-conduct scope is weakest. Promote when Q9 says the evening has an owner and budget, and Q8 says the audience's own norm includes drinking.
- **Bounded hosted service** (starved rung) - tops value and effort together, so efficiency never picks it first. Alcohol at one named moment, capped by hours or tokens, with the alcohol-free option given equal prominence at the same table. The only rung buying both halves. Design that provision as content: [references/alcohol-and-evening-programme.md](references/alcohol-and-evening-programme.md). Budget its line at the same per-item granularity as the alcoholic one, with its own quantities rather than a rounding-up of the mixed-bar order. Going alcohol-free shifts volume instead of lowering it: it changes what people drink, not how much, so under-forecasting soft and energy drinks while over-ordering coffee is one modelling error repeating, not a one-off shortage.
- **Cash bar** - attendees buy their own; event hosts nothing. Last on efficiency: filters the social half by who can spend on it. Hands the terms and stopping rule to whoever holds the till.

**Deleted, never demoted:** the unlimited hosted bar. It's bounded service with the cap removed - the cap is what the risk register, insurer, and code of conduct all rely on.

## The evening programme

Whether anything happens after the last session, and what. Turns up in organizer practice as a delegated team role, a sellable branded surface, or family-inclusive evening programming named as an access lever distinct from the code of conduct.

**The four rungs below are this skill's own construction: defaults worth trying rather than established practice.** The speakers'-dinner budget line belongs to a named population's top-up already sitting in `samber/dev-event-organizer-skills@event-speaker-experience` - it is not evidence that a general evening event exists, should exist, or is funded the same way.

Ranking (default, not a law - Q7, Q8 and Q9 re-rank it):

- effort (a second venue, transport, a headcount that must be right before anyone boards, a named owner's evenings): `offsite excursion or activity > formal dinner with a programme > venue-based mixer > no organised programme`
- value (people who stay to the end, meet somebody they did not arrive with, come back next edition - and who can all be in it): `venue-based mixer > formal dinner with a programme > offsite excursion or activity > no organised programme`
- efficiency: `venue-based mixer > formal dinner with a programme > no organised programme > offsite excursion or activity`

No compliance-cost axis is derived at menu level: the real exposure is the alcohol posture set above and the code-of-conduct scope clause, both decided elsewhere. Route the scope question to `samber/dev-event-organizer-skills@event-code-of-conduct` whichever rung you pick - an evening in your own building and an evening in somebody else's are different answers to it.

- **Venue-based mixer** (default) - the event's own space, right after the last session, food and drink from the posture above, nobody travels or pays. Leads value: people talk to people they did not arrive with, and nobody is excluded on seat count, coach seat or dress code. Leads efficiency because room, licence question and staff already exist. Move up when Q2 seats the whole population and Q8 says the edition recurs. **Sourced, not just this skill's own construction:** a conference organizer's published account of choosing an unseated reception over a formal dinner makes the same value claim, the format having "allowed people to circulate, stay as long/short as they wanted, and be as social (talking to 10) or not (talking to 1) as they liked" (academic-conference domain, not dev-specific). Duration and room design carry their own sourced guidance: [references/alcohol-and-evening-programme.md](references/alcohol-and-evening-programme.md).
- **Formal dinner with a programme** (starved rung) - second on value and effort, never wins the ratio. Real property: depth per person over breadth. Real limit: a seat count excludes. Promote when Q2 seats the whole audience, or Q7 says a sponsor bought the evening.
- **No organised programme** - a legitimate, publishable decision, ranked above the excursion deliberately. The failure is not the absence but the silence, which people fill themselves.
- **Offsite excursion or activity** - ranked below doing nothing: both leave most of the audience unhosted, but this one spends transport, another building's rules, and a headcount you can't correct once transport leaves. Promote only when Q8 makes the excursion the event's signature moment and Q2 says the whole audience fits it.

**Deleted, never demoted:** the unhosted drift ("everyone will end up at a bar somewhere"). It looks like the free version of the mixer. It is the version with nobody responsible: no owner, no accessible venue, and the code-of-conduct scope at its weakest exactly where the risk is highest.

**If Q9 found no named owner for an evening at all, delete every rung above "no organised programme"** and publish the absence. A half-run evening is the drift above with a logo on it.

## Lodging and travel: an argued refusal

The four menus above stop at the building. No menu follows for general-attendee lodging or travel, and that is a decision rather than an omission. Each piece of it already belongs somewhere:

- Conference travel material is speaker-specific: `samber/dev-event-organizer-skills@event-speaker-experience`.
- Community-run events largely do not house general attendees.
- A room block is a venue-contract term: `samber/dev-event-organizer-skills@event-venue-sourcing`.
- A travel or registration grant is means-tested access: `samber/dev-event-organizer-skills@event-accessibility-inclusion`.

Where the event does provide lodging, treat it as those last two. Never invent a hospitality standard here.

## Failure modes

- **Choosing the service style before collecting dietary counts.** The counts are the input the style is ranked against - gather from everyone fed, before the order is placed.
- **Fixing allergen labelling at the table when the information was actually lost at the delivery handover.** A missing declaration is rarely a signage failure at the serving line. It starts where a delivery is received with nobody assigned to capture the allergen and dietary detail and carry it through to plating. Fix the handover step, not just the sign.
- **Sending the registration count to catering.** The number that eats is the expected-show-up figure `event-no-show-management` owns; the gap is the buffer, named separately or lost.
- **Designing a style the building forbids.** Open flame, outside food and who may serve are the venue's and the supplier's calls, invisible until asked.
- **Treating an unlabelled buffet as the budget version of a labelled one.** Same rung, declaration removed, and the removal lands on exactly one person.
- **Deciding alcohol after a venue is held.** The posture changes the insurance question, scope clause, and risk register - cheaper before a contract than after.
- **Running the alcohol-free option as an afterthought.** A jug at the end of the bar is not provision.
- **Leaving the evening unpublished.** Silence is a decision to let it happen somewhere nobody chose and nobody is responsible for.
- **Absorbing a sibling's job because it's physically adjacent.** The caterer's contract, meal-line placement, break position, dietary list, and a speaker's or volunteer's own top-up each belong to somebody else.

## Measurement

This skill supplies no per-head cost or attendance figure of its own. Break sizing draws on a sourced catering-industry consumption convention rather than an invented ratio: [references/break-quantities-and-service-flow.md](references/break-quantities-and-service-flow.md). Everything below is this skill's own construction: the three measures are self-set, the two gates set no threshold at all, and all five only become meaningful across editions.

- **Dietary fulfilment** (gate) - every declared restriction met, at every meal, across every population fed. No threshold: zero misses.
- **Declaration completeness** (gate) - every allergen-carrying item has a readable declaration before it's taken. Fail this and the style isn't the one you ranked.
- **Longest meal queue and its peak minute** (self-set) - says whether the service style matched the grid's gap.
- **Covers ordered vs. eaten** (self-set) - hand back to `event-no-show-management`, where the estimate becomes money.
- **Who stayed for the evening** (self-set) - the best read on whether the evening default suited this audience.

Pick two, write down before the event what each would change next edition, and record both.

## Invocation examples

- "300 people, a short lunch gap, and a long list of declared dietary restrictions. What format do we feed them in?"
- "Should we serve alcohol at our community conference? Half the team wants a bar and half wants it dry."
- "What actually goes in a coffee break, and how often does someone have to restock it?"
- "One-day conference, sessions end at 17:00. Do we run an evening event, and what kind?"
- "The venue mandates its own caterer. What is left for me to decide?"

Expected output: a hospitality brief carrying:

- The service style, with the venue and supplier answers it depends on.
- The dietary counts and the fallback path per uncovered restriction.
- The break content, with the service window handed to the schedule.
- The alcohol posture, with the reviews it triggers named.
- The evening programme decision, with its owner and its published wording.

The brief invents no per-head figure.

## References

- [references/service-styles-and-dietary-carry.md](references/service-styles-and-dietary-carry.md) - what each service style can and cannot carry, the dietary-count collection rule with its source and the two sourced supplier fallbacks, the venue and supplier questions that decide a style, and a worked positive and negative brief.
- [references/break-quantities-and-service-flow.md](references/break-quantities-and-service-flow.md) - the catering-industry consumption convention a break is sized against: hot-beverage quantities by time of day, buffer and refresh cadence, and what an under-sized station's failure looks like against the figures.
- [references/alcohol-and-evening-programme.md](references/alcohol-and-evening-programme.md) - the alcohol-free provision designed as content rather than absence, the cap mechanics for bounded service, what an evening programme's brief carries, and the handoffs to the scope clause and the risk register.
- `samber/dev-event-organizer-skills@event-official-social-program` - decides how many social occasions run and whether any overlap, then runs the evening menu above once per occasion.

Other sibling skills referenced throughout: see § Where every boundary sits.
