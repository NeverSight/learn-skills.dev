---
name: event-no-show-management
description: Reduce and absorb no-shows at a technical event - an overbooking ratio against the room's real capacity and a stated ceiling, the waitlist and what triggers a promotion off it, the day-of walk-in lane, and the expected-show-up number handed to catering instead of the registration count. Use whenever asked how many registrations to accept for a free event, whether to overbook, how to run an event waitlist, why half the RSVPs did not turn up, or how many people to order food for. Do NOT use for reminder email copy - use samber/dev-event-organizer-skills@event-attendee-email-sequences - the check-in desk - use samber/dev-event-organizer-skills@event-attendee-experience - or the demand verdict behind a low show-up rate - use samber/dev-event-organizer-skills@event-market-fit.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.1"
---

# Event No-Show Management

**You decide:**

- How many registrations to accept for a room of a given size.
- Who gets promoted off the waitlist, and when.
- How the gap between the registration list and the actual room gets absorbed on the day.
- Which number goes to catering.

**You do not:**

- Price the ticket.
- Write the reminder emails.
- Staff the check-in desk.
- Judge whether the event has demand behind it.

Every ranking below is this skill's own construction, not a measured ordering: a default, not a law, and it shifts with context and with who executes it. Each menu names which interview answer moves which option. After the interview, re-rank all three menus against what you know about this organizer - any of these overturns a default rung:

- A paid event.
- A first edition with no prior data.
- An access-controlled venue with no walk-up population.
- A catering guarantee that locks a month out.
- A volunteer team with no spare hour in the final week.

## What is already decided elsewhere

Take these as fixed inputs and do not reopen any of them:

- **The ticket posture** (free, nominal, or priced) is `samber/dev-event-organizer-skills@event-ticket-pricing`'s. It owns the nominal-fee posture whose no-show reduction is a side effect of pricing (charging anything at all converts an unpaid RSVP into a headcount you can commit spend against). You own what remains regardless of price.
- **The reminder sequence's design and copy in full** belongs to `samber/dev-event-organizer-skills@event-attendee-email-sequences`. That skill names you as the owner of overbooking ratios, waitlists, deposits, and seat release. Treat the sequence as a lever that has already reduced the no-show rate before your arithmetic runs; never draft a reminder here.
- **The demand verdict** behind a show-up rate is `samber/dev-event-organizer-skills@event-market-fit`'s. It reads the number as evidence about the event's concept, price and audience; you act on the same number as a capacity input. Read its verdict, never re-derive it.
- **The check-in desk's choreography** (how the walk-in lane is staffed, queued and sorted) is `samber/dev-event-organizer-skills@event-attendee-experience`'s. You decide how many walk-ins that lane should expect and which ratio produced the number.

Each boundary above is stated from this side only. Read the sibling's own statement of it before relying on the seam.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 8-10 exist because the menus below diverge sharply on time-to-effect, durability and effort; their defaults cannot be picked for the user.

1. What is the room's hard capacity (the number the fire code, the venue contract or the seat count actually caps you at)? Is there any elasticity (standing room, an overflow space), and who has to approve using it?
2. What did a seat cost the person holding it: nothing beyond registering, a nominal fee, or a real ticket price? This is fixed upstream; report the posture, do not reopen it.
3. How many registrations exist today, is registration still open, and is there a date it must close?
4. Which costs are already committed against a headcount, and when does each one lock? Name the catering guarantee date, any venue minimum, and swag or badge print runs. This is what makes an over-estimate expensive.
5. Is a reminder sequence already designed and dated? If not, run `samber/dev-event-organizer-skills@event-attendee-email-sequences` first; every ratio below assumes reminders already did their work.
6. Can an unregistered person physically reach your check-in desk on the day, or is the venue access-controlled, badged, or remote enough that no walk-up population exists? And do you hold a channel that reaches the waitlist within a day?
7. Do you hold a prior edition's registered-versus-attended count for this same event, in this same format?
8. What is the last date each lever can still change the outcome (in practice, the catering or venue headcount guarantee date from Q4)? A guarantee that locks next week deletes every lever that needs a registration window to run.
9. Is this one edition, or a recurring event where this year's measured show-up rate becomes next year's planning input?
10. What is the effort ceiling in the final two weeks: organizer hours, anyone who can order and promote a waitlist by hand, and whether the desk can staff a second lane?

## Price posture

Every sourced figure in this domain splits on **what the seat cost the person holding it**.

- Paid events: 90-97% of tickets convert to actual attendance, a 3-10% no-show rate (attributed to Event Tech Live).
- Free events: 40-60% no-shows (attributed to Event Tech Live).
- As no-show rates (3-10% against 40-60%), the gap is close to an order of magnitude.
- As the show-up rate you divide capacity by, it roughly halves the registration ceiling.

Quote whichever of the two reads you are actually using. Price posture is the split every figure here is measured against.

A larger cross-platform sample lands inside the same split at a lower median, and adds a caution the smaller one cannot. A check-in-verified analysis of 860-plus events, narrowed to a 195-event follow-up, found a ~20% median no-show rate overall: ~28% for free events against ~17% for paid. Most of that free-versus-paid gap sits at the event level, not the individual one.

Within a single event, payment moved an individual's odds of showing by roughly 2-4 percentage points, well under the 11-point gap the event-level comparison implies. Read the bands above for the ceiling. Read this figure as a reminder that "free versus paid" explains more than "this one registrant paid or didn't."

**The employer-funded seat is a hypothesis, and must not be used as a lever.** An employer-funded ticket is money the attendee never personally felt, so it may behave closer to a free seat than its price suggests. Nothing here measures that: every show-up figure above is measured against price posture, never against who paid, and the deposit evidence in the next section carries the same limit from its own coverage. `samber/dev-event-organizer-skills@event-ticket-pricing` argues the who-pays axis for pricing; it does not settle attendance. Say so if the question comes up, and plan on the price posture.

Community-run versus vendor-run bounds the _population_ you draw from. It does not pick a ratio.

## Overbooking posture

How many registrations to accept against a room of a fixed size.

**The occupancy limit is a gate, not a rung on this menu.** The room's hold-at-once limit is fixed by the fire code, the venue contract and the insurance written against them (Q1); it is never traded against catering economics or a fuller room. Two things follow from that obligation, and neither is rankable:

- Model _expected attendance_ against that limit, not registrations: a ceiling is only safe because the no-show rate is expected to hold, so state the arrival assumption and what happens if it does not.
- Get written approval, from whoever the venue names, for any standing-room or overflow space before registrations are accepted against it - never on the day at the door.

If the ratio you want puts expected attendance over the limit, the ratio moves; the limit does not.

Ranking (default, not a law; re-rank against Q2, Q7, Q9):

- effort (hours to produce and defend the number, plus monitoring during the registration window): `own-ratio ceiling > sourced 2x ceiling > no overbooking`
- value (bodies in the room against capacity you have already committed spend to): `own-ratio ceiling == sourced 2x ceiling > no overbooking`
- compliance cost (occupancy exposure created against the venue's stated limit and the insurance that assumes it, and how reversible the position is once registrations are accepted): `sourced 2x ceiling > own-ratio ceiling > no overbooking`
- efficiency: `sourced 2x ceiling > own-ratio ceiling > no overbooking`

**Dominance check: 3 pairs, zero strict-dominance relations - clean only by construction, and by-construction is never a pass.** Two mechanisms block the three pairs; name both:

- The two pairs against no-overbooking fail on cost: each ceiling lands more bodies in the room and is strictly worse on both effort and occupancy exposure.
- The third pair, own-ratio against the sourced 2x, ties on value with each rung cheaper on a different cost axis (the sourced ceiling costs less effort, the own-ratio less exposure), so neither is at least equal on both.

Neither reason is evidence; the efficiency line rests on the arguments below.

The two ceilings tie on value because both land the room at capacity. One edition's own registered-to-attended ratio is a sample of one; the sourced 2x rests on an aggregate chart across 323 events. Neither is clearly the better estimator, so the tie is real rather than a refusal to decide, and effort then breaks it in the sourced ceiling's favour.

**The efficiency winner also tops the compliance-cost axis.** A borrowed ratio carries more variance than a measured one, so the sourced ceiling is the rung whose expected attendance sits closest to the gate above. Efficiency picks it only while that gate holds.

Where the variance would carry expected attendance over the limit, the gate takes the decision and the menu gets no vote. Name that exposure to whoever signs the venue contract before you set the number.

- **Sourced 2x ceiling** - the default for a free-registration event: accept registrations up to double your aimed attendance and stop there. The MLH hackathon organizer guide states it explicitly: about 50% of people who register for a free event show up, so aim for double the registrations, and **do not go over double**. The ceiling is the load-bearing half of that instruction, not a rounding of it.
- **Own-ratio ceiling** - the starved option: it ties the top on value, tops effort, and therefore loses every efficiency round. Compute your own multiplier from last edition's registered-versus-attended count and hold it under the sourced ceiling. Promotion condition: a recurring free-registration event (Q9) where you hold that count for the same event in the same format (Q7) **and** a committed cost locks against headcount before doors open (Q4); that combination is the only one where the difference between a borrowed 50% and your own measured rate is money rather than trivia.
- **No overbooking** - accept registrations up to capacity and close. Correct, not lazy, on a paid event; on a free event it half-empties a room whose catering you have already paid for.

**On a paid or nominal-fee event (Q2), delete both ceilings from this menu and from the axis lines above, and take no overbooking.** The two sides of the error are not symmetric: an empty chair costs one cover, while turning away someone who paid costs a refund and the public account of it. Their 3-10% no-show rate is a number to plan catering against, never a margin to sell into.

**Deleted, not demoted: leaving registration open with no ceiling at all.** It reads as the free version of maximising attendance and it is the one posture the guide explicitly forbids. Past the ceiling you are no longer absorbing a gap; you are guaranteeing that people who registered get turned away, which costs more trust than an empty chair costs money.

The three distinct sourced figures behind this menu, each with its own scope, are in [references/show-up-rate-figures.md](references/show-up-rate-figures.md). Read it before quoting any number, and never blend them: two of the three read as "50%" while answering different questions, so any average of them answers none.

## Waitlist design

What happens to the people who arrive after the ceiling. Ranking (default, not a law; re-rank against Q3, Q6, Q8, Q10):

- effort (hours in the registration window, and whether the job is dated or standing): `proximity-prioritised > FIFO on a fixed date > no waitlist`
- value (bodies in the room who would otherwise not be there, and trust kept with the people told no): `proximity-prioritised > FIFO on a fixed date > no waitlist`
- compliance cost (what the ordering rule obliges you to publish, and how reversible it is once people have registered against it): `proximity-prioritised > FIFO on a fixed date > no waitlist`
- efficiency: `FIFO on a fixed date > proximity-prioritised > no waitlist`

**This menu is clean by construction, not by care**: value and effort run in the same order, so no rung dominates another and any efficiency ordering is admissible. That is not a pass; it means the dominance check cannot catch a mistake here, and the ordering rests entirely on each rung's own argument. Treat it as the menu most worth arguing with.

- **FIFO on a fixed date** - the default: collect above the ceiling, promote in one batch on a date you name when the waitlist opens. Mechanical, defensible to whoever is skipped, and it costs one afternoon rather than a standing job.
- **Proximity-prioritised** - the starved option: order the waitlist by how close someone is to the venue. The MLH hackathon organizer guide gives this as its priority rule, reasoning that people closer to the event are more likely to show up, and it is the one non-FIFO ordering rule with organizer practice behind it. The guide attaches no figure, so treat the size of the gain as unquantified. What it buys, on that reasoning, is a higher show-up rate per promoted seat. What it spends:
  - The hours to order the list by hand.
  - An allocation decision made on registrants' location data that you must be able to state publicly and cannot quietly change mid-window.

  Promotion condition: the effort ceiling covers someone ordering the list by hand (Q10) **and** registrations (Q3) run far enough past the ceiling that promotion order actually changes who gets in rather than merely who gets in first.

- **No waitlist** - close registration at the ceiling and say so on the page. Honest, and it still costs something: the requests arrive by email anyway, and an unordered list in an inbox is a waitlist with no rule and no date.

**If the headcount guarantee locks before the latest promotion date you can realistically hold (Q8), the waitlist stops being a budget lever.** It still fills chairs, which is worth doing; it no longer changes the number catering is working from. Say which of the two you are buying, because only the second moves the figure `samber/dev-event-organizer-skills@event-budget` budgets from.

**Deleted, not demoted: promoting continuously, one seat at a time, on every cancellation.** It converts the waitlist into a standing job across the whole registration window for a gain the ceiling has already absorbed, and it converges on the live per-seat swap this skill flags as untested below.

Every promotion is an event that needs its own transactional email. Hand the trigger, the audience and the deadline to `samber/dev-event-organizer-skills@event-attendee-email-sequences` as a brief; it writes the send. The brief's contents and the waitlist's own mechanics are in [references/waitlist-and-walk-in-mechanics.md](references/waitlist-and-walk-in-mechanics.md).

## The deposit question: an argued refusal

A refundable deposit returned on attendance is one of the levers people expect this skill to rank. **Ranking it would be false precision.** No established practice stands behind it as a real-world attendance mechanic in developer-event organizing. Two cross-industry data points exist, and both are single events rather than studies:

- Eventtia's 2024 managed-conference data: a $3 refundable deposit dropped a previously-free event's no-show rate from 38% to 14%. A general-conference result, not a developer-event one.
- 37signals (Basecamp), closer to this skill's own audience: a free Chicago breakfast event carried a $100 deposit refunded at the door. 55 people paid it and 50 showed up, a 90% show rate against the free band's usual 40-60% no-shows.

Coverage of the Basecamp case names the same limit § Price posture states: the mechanic leans on the registrant's own loss aversion, and a corporate attendee reimbursed by an employer may not feel a deposit the way someone paying out of pocket does.

Deposit-backed _waitlists_ do exist, but as a pre-sale demand signal in a different context. That is `samber/dev-event-organizer-skills@event-market-fit`'s ground, not evidence about attendance.

Say that plainly rather than inventing a rung. If the organizer wants one anyway, frame it as an experiment with a measurement stated in advance, and name the three costs it carries:

- Refund handling on every single attendee who shows up.
- The accounting and tax obligation that follows from moving money at all.
- A barrier that lands hardest on exactly the people a need-gated scholarship seat exists for.

The established lever in the same direction is the nominal fee, and it belongs to `samber/dev-event-organizer-skills@event-ticket-pricing`, not here.

## Day-of gap absorption

What fills the seats the ratio did not. Ranking (default, not a law; re-rank against Q6, Q10):

- effort (desk staffing, a second form, and anything that has to happen the night before): `waitlist-fed lane > walk-in lane > nothing`
- value (chairs filled by someone who belongs in the room): `waitlist-fed lane == walk-in lane > nothing`
- efficiency: `walk-in lane > waitlist-fed lane > nothing`

No compliance-cost axis runs here. The only real exposure on this menu sits in the deleted rung below, and an axis where every live option ties is noise.

The two lanes tie on value because both fill the same number of chairs, and a promoted waitlister has no demonstrated edge in arrival rate over a walk-in. If anything the reasoning runs the other way: a walk-in is a person already standing in your building, which is a stronger attendance signal than any promise. Effort then breaks the tie, so the plain lane leads on efficiency.

- **Walk-in lane** - the default, and the sourced mechanic: a separate late-registration form, processed only after the pre-registered check-in window has closed, with everyone completing the full registration form (MLH hackathon organizer guide). It absorbs the gap from below rather than promoting a named person into a named empty seat. `samber/dev-event-organizer-skills@event-attendee-experience` already builds this lane at the desk; give it your expected walk-in volume and the ratio behind it.
- **Waitlist-fed lane** - the starved option: the same lane, but you tell the waitlist the night before that unclaimed seats open at a named time, so it fills with people you already know. The lane itself is established practice; feeding it from the waitlist is this skill's own extension, not a sourced mechanic.

  Promotion condition: the venue is access-controlled, badged or remote enough that no walk-up population exists (Q6) **and** you hold a channel that reaches the waitlist within a day (Q6). Without the first, you are paying for a send that a queue at the door would have produced for free.

- **Nothing** - the room runs at whatever shows up. Defensible when the ceiling did its work and nothing is committed against a headcount; expensive when catering is already guaranteed.

**If the waitlist menu chose no waitlist, delete the waitlist-fed lane from this menu and from the axis lines above**; there is no list to feed it from.

**Deleted, not demoted: opening the door to unregistered arrivals with no form.** It looks like the generous version of a walk-in lane. It costs you the headcount, the code-of-conduct agreement, the dietary and accessibility data and the emergency contact list, all at the exact moment those matter most.

The guide is explicit that everyone checking in still completes the full registration form.

## Workflow

1. Run the interview. Fix capacity, posture, committed costs and their lock dates, and the effort ceiling.
2. **Read the show-up expectation for your funding model**, do not average one:
   - Free-registration event: plan against the free band, landing a ceiling near double capacity.
   - Paid event: plan against the paid band, landing a ceiling near capacity.

   Take the figure with its scope from [references/show-up-rate-figures.md](references/show-up-rate-figures.md) and say which one you used.

3. **Set the overbooking ratio against a stated ceiling.** Write the ceiling down as a number of registrations, not as an intention, and name who enforces it when the form has to close. Show the arithmetic:
   - Capacity.
   - The expected show-up rate, with the figure it came from.
   - The resulting registration ceiling.
4. **Design the waitlist and its promotion trigger:**
   - What opens it.
   - In what order it is drained.
   - On what date.
   - Who decides.

   Publish the ordering rule at the same moment the waitlist opens, not after someone asks why they were skipped.

5. **Decide the deposit posture, or state that you cannot.** The honest output is that no deposit mechanic is recommended, with the three costs it would carry named. Route the underlying concern to the pricing posture, which has practice behind it.
6. **Wire the walk-in lane:**
   - How many walk-ins the ratio predicts.
   - Whether the lane is fed from the waitlist.
   - The time it opens.
   - The fact that the full form is still completed.

   Hand the volume to `samber/dev-event-organizer-skills@event-attendee-experience`; it owns everything about how the lane is staffed and queued.

7. **Hand the numbers out.** The expected-show-up number (never the registration count) goes to `samber/dev-event-organizer-skills@event-budget` for catering and per-head costs, with the overbooking buffer stated as the gap between the two. The ratio in use and every waitlist promotion event go to `samber/dev-event-organizer-skills@event-attendee-email-sequences`, so its reminders address the right audience.
8. **Count what actually happened** on the day:
   - Registrations.
   - Attended.
   - Walk-ins.
   - Waitlist promotions, and how many of those arrived.

   Feed the realised show-up rate to `samber/dev-event-organizer-skills@event-market-fit` as a demand signal, and keep it as next edition's input.

If your harness has persistent memory, record:

- The capacity.
- The expected show-up rate, with the figure it came from.
- The ceiling and its arithmetic.
- The waitlist ordering rule as published.
- The final registered-versus-attended count.

That last number is the one thing that turns a borrowed ratio into your own on the next edition.

## Untested territory

Say these out loud when the question comes up rather than inventing an answer.

- **Deposits held against attendance stay out of scope.** Rather than designing a refundable-deposit flow, route the underlying concern to the price posture: the nominal fee is the lever with organizer practice behind it. See the argued refusal above.
- **Comped and scholarship seats behave as free seats until you measure otherwise.** An application-reviewed seat may carry more commitment than a general free ticket, or none, since the holder still paid nothing. Do not assume either; count them separately and find out. One named data point exists and settles nothing. BlackPythonDevs sponsored 47 student tickets for PyCon Uganda 2024 and 22 attended: a 47% show rate, sitting inside the ordinary free-ticket band rather than clearly above or below it. It is one event, with no comparison against that same event's non-sponsored attendees.
- **A live, per-seat waitlist promotion during the event is untested.** The pre-doors walk-in lane is the mechanic with practice behind it; promoting a named waitlisted person into a named no-show's seat while the event runs is an experiment, not the obvious extension. The nearest established mechanic is ticketing-platform waitlist automation, which releases a seat with a timed claim window. Every documented version of it runs before the event, against cancellations and expired holds, never during it. One platform's own description of the mechanism calls it "a recovery mechanism for post-sale inventory gaps, not an in-event promotion strategy," which is the boundary this skill draws too.

## Failure modes

- **Going past the double ceiling on a free event.** The instruction is "aim for double" _and_ "do not go over double". Taking the first half without the second turns a gap-absorption strategy into a guarantee that registered people are turned away at the door.
- **Blending the three distinct sourced figures.** The 50% show-up trendline, the 30-50% drop-off range and the 100%-at-two-weeks / 200%-at-one-week registration curve come from the same organisation but different documents and different jobs. Averaging them produces a number that answers no question. Report each with its scope.
- **Inventing a deposit mechanic because the user asked for one.** A confidently described deposit flow implies a practice that is not there; decline it, name its three costs, and route the concern to the price posture.
- **Solving the reminder problem here.** Rewriting a cadence or drafting a nudge inside this skill duplicates the sibling that owns it and leaves two conflicting sequences in the same event. Route it.
- **Applying a paid event's 90-97% show-up rate to a free one, or the reverse.** They are the two ends of the widest split in this domain; 3-10% no-shows against 40-60%. Using the paid figure on a free event under-orders every downstream count; using the free figure on a paid one over-orders them and reads a healthy event as broken.
- **Sending the registration count to catering.** The registration count is the number you accepted, not the number that eats. The expected-show-up number is the one `samber/dev-event-organizer-skills@event-budget` needs, with the buffer named separately.
- **Reading a low show-up rate as an operations failure.** It can be demand, price, audience or the reminder sequence. `samber/dev-event-organizer-skills@event-market-fit` separates those; act on the capacity side only after it has.
- **Running the overbooking menu on a paid event at all.** Both ceilings are deleted there, not lowered: the upside is one more body, the downside a refund and a public account of turning away someone who paid.

## Measurement

Every ratio target here is self-set. The sourced bands describe populations: they tell you whether your event is normal, not whether your ratio was right. Two pass-or-fail gates and four self-set signals:

- **Expected attendance sits under the venue's stated occupancy limit** (gate, pass or fail, checked before registrations open and again at every ceiling change): the arithmetic is written down with its arrival assumption, and any standing-room or overflow allowance carries the venue's written approval. This one is not self-set and not tradeable; it is the obligation the whole menu ranks underneath.
- **Registered-versus-attended is counted and written down** (gate, pass or fail): you either hold the number for this edition or you do not. Everything above degrades to a borrowed ratio without it, and it is the single cheapest thing on this page.
- **Ratio accuracy** (self-set): actual attendance against capacity. Decide before the event what gap would change next edition's ceiling, in either direction.
- **Waitlist promotion yield** (self-set): of the people promoted, how many arrived. This is the only way to test the proximity rule on your own audience rather than trusting the guide's reasoning.
- **Walk-in volume against prediction** (self-set): what the lane actually absorbed. A lane that processed nobody on an access-controlled site is the deletion condition confirming itself.
- **Catering variance against the guarantee** (self-set): covers ordered against covers eaten. This is where an over- or under-estimate becomes money, and the number `samber/dev-event-organizer-skills@event-budget` will ask for next time.

## Invocation examples

- "We have 400 registrations for a free hackathon and the room holds 250. Do we close the form?"
- "How many people should I order lunch for; we have 180 signed up and it's a free meetup?"
- "Should we take a refundable deposit to stop people no-showing on our free tickets?"
- "Half our RSVPs didn't turn up last year. What do we change before the next edition?"

Expected output: a capacity plan covering every figure, labelled sourced or self-set:

- The room's hard capacity.
- The expected show-up rate, with its source and scope.
- The registration ceiling, with the arithmetic shown.
- The waitlist's ordering rule and promotion date.
- The walk-in lane's expected volume.
- The expected-show-up number handed to catering, with the buffer named.
- The deposit question, answered as a stated gap rather than a mechanic.

## References

- samber/dev-event-organizer-skills@event-ticket-pricing - ticket posture and the nominal fee
- samber/dev-event-organizer-skills@event-attendee-email-sequences - reminder sequence and transactional sends
- samber/dev-event-organizer-skills@event-market-fit - what a show-up rate says about demand
- samber/dev-event-organizer-skills@event-attendee-experience - check-in desk and walk-in lane staffing
- samber/dev-event-organizer-skills@event-budget - per-head cost lines
- samber/dev-event-organizer-skills@event-feedback - no overlap (no-shows do not enter feedback survey)
