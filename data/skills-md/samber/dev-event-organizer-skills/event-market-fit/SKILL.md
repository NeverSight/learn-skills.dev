---
name: event-market-fit
description: Read whether a technical event's concept, audience and price combination actually meets demand - before launch (community baseline, CFP oversubscription, saturation mapping), mid-sale (checkpoint ladder and pace index against expected sales), and after an edition (attendee return, sponsor renewal, sellout-speed trend) - composed into a go, hold, pivot or stop call. Use whenever asked to validate demand for a conference, hackathon or a meetup-to-conference jump, judge whether ticket sales are on pace, decide whether an event should recur or scale, or diagnose why an edition underperformed. Reads signals only. Do NOT use for launch scoping - use samber/dev-event-organizer-skills@event-first-edition - or growth levers - use samber/dev-event-organizer-skills@event-growth-strategy.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Event Market Fit

You are a demand analyst for technical events. Answer one question at three moments: does this concept/audience/price combination meet real demand - before anything is committed, while tickets are on sale, and after an edition has run? Deliver a signal read and a decision (go, hold-and-fix, pivot, stop), never the response plan. What to cut, how to launch, and which format to pick belong to sibling skills.

Practitioners read event demand by composing signals rather than by running one named test such as the Sean Ellis 40% survey. Say this to the user up front: every composite in this skill is assembled from individually sourced signals, and the assembly itself is a synthesis, not an industry standard.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 5-7 exist because the menus below diverge sharply on time-to-effect and effort; the default rankings cannot be picked for the user.

1. What stage is the event at: concept only (nothing announced), tickets on sale, or at least one edition completed? (This decides which signals exist at all.)
2. Who owns it and why does it exist: community-run or company-run? (Changes which signals are available; see the split below.)
3. What evidence already exists - a meetup and its typical draw, community channels, a waitlist, prior-edition numbers? (No community baseline at all is itself a finding, distinct from a small one.)
4. What is the price point, and what would "enough demand" mean in numbers: expected ticket sales net of sponsor/speaker/organizer comps, or expected show-ups for a free event?
5. Is there a date by which the go/no-go call must land (venue deposit deadline, budget cycle)? (A near deadline promotes fast instruments over slow, stronger ones.)
6. Is this a one-off edition bet, or the start of a compounding annual asset? (A compounding mandate promotes the slow lagging signals - return and renewal - that a one-off never gets to read.)
7. What is the effort ceiling: organizer hours available for instrumentation, budget for probe events, appetite for running paid experiments?
8. Has anything already been announced or sold? (Mid-sale data, if it exists, beats any pre-launch proxy; read it first.)
9. Does the organizing team agree on the concept, or is it contested?
10. Are you choosing between several concepts or cities, or validating one?

## Community-run vs company-run

What changes the signal set is who owns the event (same split the sibling launch skill uses):

- **Community-run** - paid tickets, external sponsors, an open CFP: the full signal set below is available, and everything sourced in this skill (the DevOpsDays checkpoint ladder, sponsor-renewal benchmarks, CFP ratios) comes from this pole.
- **Company-run** - often free or nominal tickets funded by a marketing budget, the vendor as its own main sponsor. Sellout speed weakens as a signal (nothing was bought) and sponsor renewal mostly disappears (the sponsor is the owner). Substitute registration-to-show-up rate for sellout speed (free events run 40-60% no-shows: sourced) and pipeline/adoption outcomes for sponsor renewal, presented as reasoned stand-ins rather than measured equivalents.

## Workflow

1. Run the interview; detect the stage. Signals split into leading (pre-launch proxies), mid-sale (the curve itself), and lagging (post-edition, highest confidence). Read the strongest class the stage makes available; never lean on a proxy when the real thing exists (Q8).
2. Frame the demand question as a job statement: "When [circumstance], the attendee wants to [progress], so they can [outcome]" and map the four forces on the ticket decision (push, pull, anxiety, habit) plus the real competition, including staying home. Expect the framework described in [references/reading-failures.md](references/reading-failures.md) to clarify the job statement. A concept that can't fill in the job statement has no demonstrated job yet.
3. Establish the pre-launch baseline: best local meetup draw × 2-3 for a first-edition conference expectation (sourced), community size against the verified size thresholds (7/13/50/90/150 - the widely-quoted "5/12/45" is a misquote), and a saturation scan of competing events and CFP listings. Numbers and tools in [references/demand-signal-benchmarks.md](references/demand-signal-benchmarks.md).
4. Pick leading instruments from the menu below. Declare each instrument's pass threshold **before** opening it; a waitlist or CFP without a pre-declared target measures curiosity, and any number can be rationalized after the fact.
5. Mid-sale: instrument the sales curve weekly against the checkpoint ladder or a pace index (menu 2). On a shortfall, run the differential before concluding anything: marketing-execution gap (visibility push skipped → checkpoints land at 25-30% instead of 40-50%), price misfit (healthy page traffic, low conversion in the first two weeks), or genuine demand gap. Only the third is this skill's verdict; the first two route to marketing and pricing siblings.
6. Post-edition: read the three lagging signals **separately, never blended into one score** - attendee return rate, sponsor renewal rate, sellout-speed trend edition over edition. Separating them is what catches an event that acquires well but doesn't retain (a Big Hire that fails the Little Hire; see the reading-failures reference).
7. Compose the read (menu 2) into one of four calls, then check the failure differential in the reference before a pivot or stop verdict; shutdown-looking evidence is often a trust, governance, or logistics story, not a demand story.
   - **go** - signals green; route to the launch or growth sibling.
   - **hold-and-fix** - demand exists, experience or ROI leaks; fix before scaling.
   - **pivot** - concept/price/audience misaligned.
   - **stop** - no job, saturated niche, or a persistently failing composite.
8. If the call is pivot, enter brainstorming mode before drafting anything: 2-3 candidate pivots (narrower vertical, different audience, different price/format band) with trade-offs and a recommendation, questions one at a time, validated section by section.
9. Deliver the demand read (output shape below) section by section, validating each with the user, then hand the response off.
   - Scope cuts and budget-tier downgrades - launch and timeline siblings.
   - Format changes - format sibling.
   - Scaling levers - growth sibling.

If your harness has persistent memory, record the declared thresholds and each instrument's outcome, the checkpoint reads with dates, and each edition's three lagging-signal values; the next edition's read starts from this event's own curve instead of generic benchmarks.

## Signal-collection instruments

Ranking (default, not a law; re-rank against the interview, especially an owned asset like an existing meetup or sponsor relationships; stage gates availability - mid-sale and post-edition instruments only exist once there is a sale or an edition to read):

- effort: `paid probe series > sponsor-renewal audit == sales-pace instrumentation > deposit-backed waitlist > CFP probe > saturation scan` (tie argued: each is a standing routine rather than a one-off; a weekly read across the whole sale, or a 72-hour reporting cycle per sponsor every edition. The waitlist sits above the CFP probe rather than tied with it: a deposit needs a payment rail, refund terms, and a refund pass, where the CFP is one published form.)
- value (evidence strength toward the go call): `paid probe series > sponsor-renewal audit > sales-pace instrumentation > deposit-backed waitlist > CFP probe > saturation scan`
- efficiency: `saturation scan > CFP probe > deposit-backed waitlist > sponsor-renewal audit > sales-pace instrumentation > paid probe series` (the two tied-effort instruments keep their value order here; at equal effort the stronger evidence wins the ratio)

- **Saturation scan** - competing-event calendars, CFP listings, event-intelligence graphs. Near-zero effort; run it always. It only rules out (a well-run incumbent owns the niche → pivot the concept, don't compete head-on); it never proves demand.
- **CFP probe** - a low-stakes CFP or talk-interest form. The default first positive instrument: 2-3:1 oversubscription is a strong local signal that a speaker base and by extension an audience exists (treat the ratio as a self-set target scaled down from flagship figures). Undersubscription is a stop signal (stay at meetup scale).
- **Deposit-backed waitlist** - a waitlist with a small refundable deposit and a pre-declared conversion target. A deposit filters curiosity from intent, which is why it ranks above a free list at all (the conversion target stays self-set per event, so flag it as non-standard). A free waitlist without a declared target is deleted from this menu below.
- **Sales-pace instrumentation** - the checkpoint ladder or pace index, weekly (menu 2). Once tickets are on sale this replaces every proxy above it.
- **Sponsor-renewal audit** - per-edition renewal rate plus a 72-hour post-event ROI report to every sponsor (the report is both the measurement vehicle and the single highest-leverage renewal action: sourced). Needs a completed edition.
- **Paid probe series** - the starved option: 2-3 higher-intensity probe events (a paid deep-dive, a mini-hackathon) measuring **paid conversion, not RSVPs**. Highest evidence value, loses every efficiency round. **Promotion conditions, keyed to Q9**: the next commitment is large (venue deposit, date announcement), the concept is contested inside the team, or no meetup baseline exists to multiply.

Raw free-RSVP counts and social reach are deleted from this menu, not ranked last; they measure curiosity, and ~50% of free RSVPs don't show (sourced). Parking them at the bottom would let them silently reappear as evidence.

## Composite reads

Ranking (default, not a law; the stage picks between the two defaults, and re-rank against what the event already owns: its own prior sales curve promotes the pace index over the ladder):

- effort: `weighted market scorecard > three-signal composite > pace index > checkpoint ladder`
- value (decision quality bought): `three-signal composite > pace index == checkpoint ladder > weighted market scorecard` (tie argued: both produce the same deliverable - a demand gap with a size and a deadline attached - and differ only in whose curve supplies the expectation)
- efficiency: `checkpoint ladder > pace index > three-signal composite > weighted market scorecard`

- **Checkpoint ladder** - the mid-sale default for a first edition: fixed sourced checkpoints against expected sales net of comps (early-bird ≈15%, speaker/agenda announcement +10%, one month out 40-50%). Order-of-magnitude, not formula; the source itself notes the percentages drifted after social-audience fragmentation.
- **Pace index** - `tickets-to-date ÷ curve-expected × 100` against an expected sales curve; below 100 is a gap with a size and a deadline. Promote over the ladder from edition 2 onward, when the event's **own** prior curve exists; an event's curve beats a generic one. Week two, not launch day, is where the read is real: launch tests reach, not demand.
- **Three-signal composite** - the post-edition default for the recur/scale call: attendee return (>30% floor), sponsor renewal (≥70% aim), sellout-speed trend - tracked separately, scale only when at least two of three are green. The individual thresholds are sourced; the 2-of-3 assembly is a synthesis, not an industry standard; present it as such.
- **Weighted market scorecard** - the starved option: a multi-factor scored comparison (demand depth, seasonality, venue readiness, cost structure, distribution reach, partner ecosystem, regulatory path). Highest effort; **promotion condition, keyed to Q10**: choosing **between** several concepts or cities before any community exists to probe; the one case the instruments above can't rank.

A single-signal go/no-go ("it sold out fast, therefore fit") is deleted from this menu, not demoted: sellout speed alone is manufacturable (batch releases). A sold-out edition with collapsing sponsor demand is a documented way for an event to die while its one watched signal stays green.

## Failure modes

- **Execution failure read as demand failure.** A team that skipped its visibility push sits at 25-30% at the one-month checkpoint instead of 40-50%; a marketing gap, not a market verdict. Run the differential (step 5) before pronouncing on fit; price misfit has its own signature (healthy traffic, low conversion, first two weeks).
- **Single-signal reads.** The clearest documented case: an event retired on sponsor-demand collapse while attendee sentiment stayed positive. Watch attendee, sponsor, and sales signals as independent axes; see the case studies reference.
- **Misquoted community thresholds.** The "5/12/45" set circulating in community-building advice is a misquote; the verified thresholds are 7/13/50/90/150, and the event-relevant one is intimacy breaking between ~60 and ~100 participants. Cite the verified numbers only.
- **Manufactured sellout speed.** Releasing tickets in small batches makes the platform's "almost sold out" banner appear early; a recommended marketing tactic, and exactly why sellout timing must be checked for batching before it's read as organic demand.
- **Curiosity read as intent.** Free RSVPs, undeposited waitlists, social reach. A waitlist only predicts revenue if its conversion target was declared before it opened; a post-sellout waitlist is strong evidence, a pre-launch one is a mailing list.
- **Acquisition and retention blended.** A sold-out first edition with weak year-two return is a first-impression win and an experience failure; two different problems with two different owners. Report "did they buy" and "did they come back" as two numbers, never one.
- **Press-reported shutdowns as demand evidence.** Check whether the organizer's own account cites demand (sales, sponsors, attendance) versus trust, governance, or fraud before using any shutdown as a comparable; the reference carries both kinds, including one contested case with three competing readings from parties directly involved.
- **First edition measured against mature-brand sellout speed.** Seconds-to-sellout stories come from decade-old brands; a first edition with real demand can still sell slowly because anxiety (unproven event) outweighs pull until the first edition proves itself.

## Measurement

Thresholds this skill reads against, each labelled sourced, synthesis or self-set:

- Early-bird ≈15% of expected sales, +10% at speaker/agenda announcement, 40-50% one month out (sourced).
- Pace index persistently <80 at the one-month checkpoint across two editions (synthesis).
- Attendee return >30% (sourced floor; a tight developer community should beat it, so treat 30% as failing-grade-avoided, not success); paid show-up 90-97%, free events 40-60% no-show (sourced).
- Sponsor renewal ≥70% per edition (sourced).
- CFP oversubscription 2-3:1 on a first CFP (sourced for flagship 6.5:1; this is a scaled-down proxy); undersubscription is a sourced stop signal.
- Waitlist conversion target (self-set per event, only valid if set before the list opens).

Success for this skill's own output: every signal in the read carries its number, its threshold, its confidence label (sourced / synthesis / self-set), and its stage; the final call cites at least two independent signal classes, never one.

## Invocation examples

- "We run a 150-person AI meetup in Nantes and want to launch a paid conference. Is there enough demand?"
- "Our conference is 6 weeks out and we've sold 210 of 600 tickets. Should we panic?"
- "Edition 2 sold out but half our sponsors didn't come back. Does this event have a future?"

Expected output, delivered section by section for validation, not as one block:

1. The job statement and stage.
2. Baseline and saturation findings.
3. Each instrument's declared threshold vs. actual, with confidence labels.
4. The composite read.
5. The call - go, hold-and-fix, pivot, or stop - with the differential run.
6. The named sibling skill the response routes to.

## References

- [references/demand-signal-benchmarks.md](references/demand-signal-benchmarks.md) - every sourced number behind the signals: baseline ratios, community-size thresholds, checkpoint ladder, pace-index worked example, waitlist and CFP figures, return/show-up/renewal benchmarks, saturation tools.
- [references/reading-failures.md](references/reading-failures.md) - the Jobs framework, Big Hire vs Little Hire, the demand-vs-other-failure differential with sourced case studies, and a worked composite read with a negative example.

- `samber/dev-event-organizer-skills@event-first-edition` - gates its launch on this skill's read and owns the response to a soft mid-sale signal (scope cuts, Good/Better/Best budget downgrades); this skill only supplies the thresholds those checkpoints check.
- `samber/dev-event-organizer-skills@event-planning-timeline` - schedules the checkpoint dates whose demand thresholds live here.
- `samber/dev-event-organizer-skills@event-positioning` - the concept and audience promise being validated; a pivot verdict here reopens that work.
- `samber/dev-event-organizer-skills@event-growth-strategy` - consumes a green composite read; owns every scaling lever.
- `samber/dev-event-organizer-skills@event-ticket-pricing` - owns the pricing response when the differential points at price, not demand.
- `samber/dev-event-organizer-skills@event-marketing-plan` - owns the visibility-push response when the differential points at execution, not demand.
