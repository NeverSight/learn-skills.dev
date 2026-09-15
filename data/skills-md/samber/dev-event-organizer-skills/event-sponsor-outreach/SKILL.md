---
name: event-sponsor-outreach
description: Run the sponsor sales motion for a technical event, from target list to signed yes - target list building and scoring, outreach timed against sponsor fiscal-year budget lock-in, first-touch channel choice (warm intro, referral ask, cold email under sponsor-specific etiquette), the exploratory call, capped follow-up cadences, objection handling, pipeline tracking, and renewal versus net-new as distinct motions. Use whenever the user mentions finding sponsors, a sponsor outreach email, pitching a sponsorship, a sponsor objection, or chasing renewals - even if they never say "outreach". Do NOT use for the rate card - use samber/dev-event-organizer-skills@event-sponsor-pricing; post-sale delivery is samber/dev-event-organizer-skills@event-sponsor-fulfillment.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Event Sponsor Outreach

You run the sale itself: everything between having a sponsor value story and having a signed sponsor. You consume three inputs from sibling skills and output a signed yes, or a tracked no:

- **The claims** - `samber/dev-event-organizer-skills@event-sponsor-value-proposition`.
- **The document** - `samber/dev-event-organizer-skills@event-sponsor-prospectus`.
- **The rate card** - `samber/dev-event-organizer-skills@event-sponsor-pricing`.
- **The output** - a signed yes handed to `samber/dev-event-organizer-skills@event-sponsor-agreement`, or a tracked no.

One timing fact governs the whole motion: sponsor prospectus outreach belongs at roughly T-8 months before the event, because sponsors, especially larger companies, lock budgets in the financial year prior (DevOpsDays organizing guide). Outreach is the first external-facing motion of the plan, ahead of CFP and attendee marketing. Waiting for a finished program means competing for money already spent.

Every ranking below (target-list sources, first-touch channels, follow-up cadence) is a default, not a law: it shifts with context and with who executes it. Re-rank all three menus after the interview, against what you already know about this organizer. Each of the following overturns a default rung:

- A returning-sponsor roster.
- An organizer who works at a target company.
- A first edition with no roster at all.
- A paid events team instead of volunteers.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 6-8 exist because the menus below diverge sharply on time-to-effect and effort - the default rankings cannot be picked for the user.

1. Which pole does the event sit on: community-run (independent, volunteer organizers, sponsors as cost recovery) or company/foundation-run (vendor-owned, marketing budget, sponsors as pipeline)? This decides which warm channels exist and what the call can honestly promise.
2. Which inputs exist already: a per-segment value proposition, a prospectus, a rate card? First touch and the exploratory call run before the prospectus is sent (MLH organizer guide), so start without the deck. The proposal step needs packages and prices, so route missing inputs to the siblings above before that step.
3. Which sponsors from the last edition are renewal candidates, and which portion of the revenue goal must come from net-new? Renewal and net-new run as distinct motions in the same pipeline (see Renewal vs net-new).
4. How far out is the event date, and when do the top targets plan next year's budget? Under T-8 months, the fiscal-year window is already closing - flag it and prioritize targets whose budget cycle is still open.
5. What is the sponsorship revenue goal and the average package price? These size the target list backward (see [references/pipeline-and-renewal.md](references/pipeline-and-renewal.md)). The close and reply rates in that math are self-set assumptions, not benchmarks.
6. By what date must sponsorship revenue close? (A near deadline promotes the warm rungs everywhere - they convert fastest - and rules out slow-building inbound as anything but background.)
7. Is each sponsor a one-off sale or a compounding multi-edition relationship? (A compounding mandate promotes renewal care, the dedicated-liaison practice, and the adjacent-event scan that builds next year's list.)
8. What is the effort ceiling: a volunteer organizer with a few hours a week, or a dedicated sponsorship lead? (This answer alone decides the cadence menu.)
9. Does this event belong to a franchise or multi-city series with sibling editions?

## Community-run vs company-run

The axis that changes the sales motion is who owns the event, the same split `samber/dev-event-organizer-skills@event-first-edition`, `samber/dev-event-organizer-skills@event-format-selection` and `samber/dev-event-organizer-skills@event-sponsor-value-proposition` argue:

- **Community-run** - the strongest warm channel is structural: many organizers in a community event's network work at sponsor companies themselves ("talk to the other organizers on Slack - many of them work at sponsors!", DevOpsDays guide). The motion is run by volunteers, which favors the capped cadence and hard follow-up ceilings. The call must never promise attendee lists or purchasable slots - the honesty constraint owned by `samber/dev-event-organizer-skills@event-sponsor-value-proposition`.
- **Company/foundation-run** - pipeline promises are honestly on the table, and the motion is usually run by a paid events or field-marketing team, which promotes the higher-effort rungs (full cold sequences, deeper personalization). Published organizer guidance is written for the community pole; treat every company-run adjustment as judged rather than established practice.

## Workflow

1. Run the interview. Fix the pole (Q1), split renewal from net-new (Q3), and size the list backward from the revenue goal (Q5).
2. Build the candidate list from the target-list menu below, sourcing 2-3 times more candidates than the sponsors needed, since qualification culls hard (a lead-generation rule of thumb, not a sponsorship benchmark). Diversify across startups, midsized companies, and large enterprises rather than concentrating on one segment (MLH guide).
3. Qualify and score each candidate Hot / Warm / Cold / Skip with a source URL and date per claim, public business contact channels only (detail in [references/pipeline-and-renewal.md](references/pipeline-and-renewal.md)).
4. Run the warm-path check per target before anything colder: does anyone in the organizing team or community network work at, or know someone at, the target? The MLH and DevOpsDays organizer guides both put the personal/community network first.
5. Make the first touch through the channel menu below. Cold email obeys the sponsor-specific etiquette: no links, no attachments, no images in the first email - corporate phishing filters auto-trash them (MLH guide; full craft in [references/outreach-process-and-email-craft.md](references/outreach-process-and-email-craft.md)).
6. Run the exploratory call pre-prospectus. Pitch the event and team briefly, then let the sponsor talk: ask what success metrics they used in past sponsorships and what they spent. Qualify authority, need, urgency, and money as you go (call script and the ANUM qualification overlay in [references/outreach-process-and-email-craft.md](references/outreach-process-and-email-craft.md)). Schedule the follow-up call before hanging up (MLH guide).
7. Send the proposal immediately after the call: the standard prospectus with the most relevant package highlighted, or a custom proposal when the tiers don't fit. State why it fits this sponsor and attach a deadline (MLH guide).
8. Follow up on the cadence menu below, respecting its cap. Honor an opt-out immediately, mid-sequence - not at the next scheduled touch.
9. Track every prospect in a pipeline (a CRM, an email follow-up tool, or a spreadsheet all work; MLH guide), and name a dedicated liaison per sponsor relationship (DevOpsDays guide). Log every objection by sponsor segment and feed the log back to `samber/dev-event-organizer-skills@event-sponsor-value-proposition`. Gate the closing step itself by deal size, not only the deliverables it buys: a small pledge needs a signature and nothing else; the largest pledge tier warrants a values-alignment check inside the organizing team before it is finalized. On a yes:
   - Invoice immediately.
   - Confirm amount and payment method in writing.
   - Verify the receiving account works.
   - Hand off to `samber/dev-event-organizer-skills@event-sponsor-agreement` (close mechanics in [references/pipeline-and-renewal.md](references/pipeline-and-renewal.md)).
10. Run the renewal motion for last edition's sponsors as its own track (see Renewal vs net-new).

If your harness has persistent memory, record:

- The scored target list with each claim's source.
- Per-sponsor pipeline stage and liaison.
- The objection log by segment.
- The renewal roster with each sponsor's budget-cycle month.

Next edition's outreach starts from that record instead of a blank list.

## Target-list sources

Where candidates come from. Ranking (default, not a law - Q3 and a first edition re-rank):

- effort: `attendee-stack vendor mapping > adjacent-event sponsor scan > institutional channels > organizer-network employers == previous-sponsor roster`
- value (close propensity of the leads produced): `previous-sponsor roster > organizer-network employers > adjacent-event sponsor scan > attendee-stack vendor mapping > institutional channels`
- efficiency: `previous-sponsor roster > organizer-network employers > adjacent-event sponsor scan > institutional channels > attendee-stack vendor mapping`

The effort tie is argued: the previous-sponsor roster and the organizer-network employer list are both records the team already holds - the sponsor list of past editions and the organizers' own employers and contacts. Each is an afternoon of writing down what is already known, with no research step.

- **Previous-sponsor roster** - the default first source: sponsors of this event's past editions, and of other events in the same series, particularly local ones (MLH guide). These leads have already bought this exact thing once.
- **Organizer-network employers** - the community-pole structural warm channel (DevOpsDays guide). Also LinkedIn-visible personal contacts (MLH guide).
- **Adjacent-event sponsor scan** - companies sponsoring neighboring events in the same technology space: published sponsor pages are public evidence of budget, motivation, and fit. This channel extends the ecosystem-adjacency fit logic rather than repeating established organizer practice, so treat it as judged.
- **Institutional channels** - university career services (who sponsors tech job fairs) and community fundraising announcements (MLH guide). Mostly recruiting-motivated buyers.
- **Attendee-stack vendor mapping** - the starved option: map which vendors' tools the expected audience uses or evaluates, then target those vendors' DevRel and marketing teams. Highest research effort, strong fit, so efficiency never picks it first. Promotion conditions: the warm lists are exhausted with the revenue goal unmet, or a whole buyer segment (typically product-feedback buyers) is missing from the list.

First-edition re-rank: no previous-sponsor roster exists. **Keyed to Q9**: substitute the same-series/local-edition roster where the event belongs to a franchise, and promote the organizer-network list to the default.

## First-touch channel

Per target, the first contact. Ranking (default, not a law - Q6 and Q8 re-rank):

- effort (per booked call): `cold email sequence > inbound broadcast > referral ask > warm intro`
- value (calls booked per attempt): `warm intro > referral ask > cold email sequence > inbound broadcast`
- efficiency: `warm intro > referral ask > inbound broadcast > cold email sequence`
- compliance cost (the review it triggers, and how little of it can be undone): `cold email sequence > referral ask > warm intro == inbound broadcast`

The compliance tie is argued: a warm intro moves through a person who already holds the relationship, and inbound broadcast is public content that contacts nobody. Neither processes a prospect's personal data beyond what the prospect volunteers, so neither triggers any review. Cold email and the referral ask are unsolicited direct outreach to named business contacts: consent and e-marketing law territory (GDPR, CAN-SPAM and kin).

For both:

- Keep a source URL and date for every contact.
- Use public business channels only.
- Honor opt-outs immediately, mid-sequence; an ignored opt-out cannot be walked back.

The referral ask carries a lighter compliance cost than the cold email sequence: it is a single no-pitch message, not a sequence.

- **Warm intro** - the default: the organizer or a community member who knows someone inside the target makes the introduction. Near-zero effort where the path exists. Exhaust it per target before anything colder.
- **Referral ask** - where no direct path exists: email someone senior at the target - above the likely decision maker - asking only "who is the right person to talk to about sponsoring X?", never pitching in that email (the Cold Calling 2.0 referral pattern from B2B sales). The forwarded introduction functions as a warm intro even though the first touch was cold. It converts "when in doubt, email the CEO" (MLH guide) from a guess into a structured ask. Its response-rate edge over a cold pitch - several times higher - is a B2B SaaS sales benchmark, not a sponsorship one.
- **Inbound broadcast** - a sponsorship-call blog post on the event's own site and social posts (both DevOpsDays-named channels). Near-zero standing effort serving the whole market at once, but yield is low and unpredictable: keep it always on, never make it the plan.
- **Cold email sequence** - the starved option: a personalized multi-touch sequence to a named decision maker. It tops the effort axis, so efficiency never picks it, yet it is the only channel that reaches targets the community's network doesn't. Promotion conditions: the revenue goal needs more sponsors than warm paths reach, or a first edition in a city where no organizer network exists yet.
- **Deleted, not demoted: purchased or scraped contact lists.** Public business contact channels only, the same compliance rule that governs sales prospecting. A bought list is not a last resort parked at the bottom of this menu: it is out.

Title targeting by sponsor motivation (DevRel for product feedback, recruiting/HR for hiring, marketing/PR for brand) is in [references/outreach-process-and-email-craft.md](references/outreach-process-and-email-craft.md).

## Follow-up cadence

After the first touch or the proposal, how many times and how spaced. Ranking (default, not a law - Q8 decides this menu almost alone):

- effort: `angle-rotation sequence > sponsor-standard cadence`
- value (replies recovered from silence): `angle-rotation sequence > sponsor-standard cadence` - the multi-touch reply lift behind this ordering is a B2B SaaS sales benchmark, not a sponsorship figure
- efficiency: `sponsor-standard cadence > angle-rotation sequence`

**Dominance check: 2 rungs, 1 pair, zero strict-dominance relations, clean only by construction, and by-construction is never a pass.**

Value and effort run in one order, so the single pair fails on cost: the rotation sequence recovers more replies and costs more to write and run. A two-rung menu has nothing else to check, and no third axis is printed. The efficiency call rests on the argument below, not on a passed check.

- **Sponsor-standard cadence** - the default:
  - Wait 1-2 weeks between pings.
  - Cap at 3 follow-ups.
  - Tighten to 3-4 days only close to the event date (MLH guide).

  It is the one cadence published for sponsorship rather than borrowed from sales, sized for a volunteer organizer's bandwidth and a fundraising runway with an end date. Where the cadence needs a real closing deadline rather than a generic follow-up, tie the final reminder to a hard, unrelated production date already on the calendar - a merchandise print cutoff, a program-lock date - rather than inventing one: a deadline the sponsor can verify is real carries more weight than a stated close date with nothing behind it.

- **Angle-rotation sequence** - the starved option: 4 follow-ups over increasing gaps, each adding a genuinely new angle (a stat, a case study, an insight). The last is a breakup email that names the silence and offers one final value item. Higher value, higher effort, so efficiency never picks it.

  Borrowed from B2B SaaS sales, where every rate attached to it (reply lift, breakup-email response) was measured; those rates are not sponsorship numbers.

  Promotion conditions, all three:
  - A dedicated sponsorship lead (Q8).
  - A large net-new list.
  - A revenue gap remaining at the default cap.

- **Deleted, not demoted: the "just checking in" bump repeated until reply.** It adds no angle. B2B SaaS sales data shows returns collapse and spam complaints multiply past the cap (a sales benchmark, not a sponsorship one). In a community whose members talk to each other, it burns the event's name, which no next-edition outreach recovers.

## Objection handling

Prepare before outreach, not during the call. Have the fixed sponsor question checklist answered in advance:

- Projected attendance.
- Aggregate audience composition.
- Per-level benefits.
- Logistics.

A sponsor who has to chase these answers reads the event as poorly run (DevOpsDays guide; the "gut feel" competence concern, MLH guide).

Build the objection library in [references/objection-handling.md](references/objection-handling.md), using a five-field response structure and a two-format delivery (quick-reference table for the live call, detailed doc for prep) borrowed from general B2B sales enablement. Fill it with sponsor-specific content built from the four sponsor concerns (attendee value, co-sponsor mix, package value, organizer competence) and the organizers' own answers. That framework's "Technical" objection category has no sponsor equivalent: it is dropped, not force-fit.

## Renewal vs net-new

Run both through the same pipeline, as distinct motions:

- **Net-new** runs the full workflow: research, warm-path check, first touch, call, proposal, follow-up.
- **Renewal** skips or shortens research and first touch - the target is known, and the community's core-organizer network is a direct path to a past sponsor's contact (DevOpsDays guide). It starts near the exploratory-call step, anchored on the post-event report that `samber/dev-event-organizer-skills@event-sponsor-fulfillment` produces. Fulfillment builds the renewal ask; this skill executes the contact motion.
- Renewal and net-new run on different clocks, not the same T-8 checkpoint: renewal outreach starts at or within days of event close, before the sponsor's attention or budget line moves elsewhere (Sponsorship Collective), while net-new keeps its own fiscal-year-indexed lead time of 3-9 months (WW Sponsorship) - detail in [references/pipeline-and-renewal.md](references/pipeline-and-renewal.md).

Never cold-pitch a returning sponsor as if net-new: an email explaining what the event is, to a company that wrote a check for it last year, reads as not knowing your own sponsors.

## Failure modes

- **Starting outreach after the program goes live.** The budget window closed at roughly T-8 months. A beautiful prospectus in month T-4 competes for money already allocated. Fix: outreach is the first external motion, before CFP, before marketing.
- **Links, attachments, or images in the first cold email.** Corporate phishing filters auto-trash it unread. Save the prospectus and every link for the follow-up.
- **Pitching packages before the exploratory call.** The call exists to surface the sponsor's own success metrics and budget first. A proposal sent cold answers questions nobody asked. The prospectus follows the call, highlighted to what was heard.
- **Following up past the cap.** Every touch past it costs more goodwill than it recovers (the collapse curve is a B2B SaaS sales benchmark, not a sponsorship one - the community-reputation cost is the sponsorship-specific reason).
- **Ignoring an opt-out until the next scheduled touch.** Remove them the moment they ask, mid-sequence.
- **Treating renewals as net-new.** See Renewal vs net-new - it wastes the warmest leads in the pipeline and insults them in the same email.
- **Reading SaaS rates as sponsorship facts.** Planning on "9-15% reply" or "20-30% close" imports another industry's benchmarks into a category they were never measured in. Use your own edition-over-edition observed rates as they accumulate.
- **Nobody owns the relationship.** Prospects tracked nowhere, or by everyone, go stale silently. One named liaison per sponsor, one shared pipeline.

## Measurement

Event sponsorship publishes no reply rate, close rate or sales-cycle length of its own, so never import a SaaS figure in place of one. What is trackable is your own funnel, self-set and edition-over-edition:

- **Pipeline coverage** (self-set): prospects in play versus the backward-sized list the revenue goal requires. A shortfall at the list stage predicts a shortfall at close, months earlier.
- **Stage conversion** (self-set): first touch → call, call → proposal, proposal → close, tracked per channel and per motion (renewal vs net-new). By edition 2 these are your own benchmarks - the only sponsorship-specific rates you will ever have.
- **Objection recurrence**: a recurring objection in the log is a defect in that segment's value-proposition statement, not a sales problem - route it to `samber/dev-event-organizer-skills@event-sponsor-value-proposition`.
- **Renewal rate** reads on the whole relationship (delivery, report quality), not on outreach alone. It belongs to `samber/dev-event-organizer-skills@event-market-fit` (signal) and `samber/dev-event-organizer-skills@event-sponsor-fulfillment` (driver).

## Invocation examples

- "We need €40k in sponsorship for our 400-person community conference next October. Build the target list and the outreach plan."
- "Draft the first email to a dev-tools company we want as a sponsor - nobody on the team knows anyone there."
- "A sponsor prospect went silent after we sent the proposal two weeks ago. What now?"
- "Six of last year's ten sponsors haven't re-signed. Set up the renewal outreach without treating them like strangers."

Expected output:

- A scored target list with a top-3-to-5 callout naming why each should be contacted first.
- A per-target channel and cadence plan timed against the fiscal-year window.
- Call and proposal next-steps per pipeline stage.
- An objection log wired back to `samber/dev-event-organizer-skills@event-sponsor-value-proposition`, with every assumed rate flagged self-set.

## References

- [references/outreach-process-and-email-craft.md](references/outreach-process-and-email-craft.md) - the five-step process, the first-email content checklist and etiquette rules, title targeting by sponsor motivation, the referral-ask mechanic, the exploratory-call script with the ANUM overlay, proposal rules, and both cadences with what each rate behind them is worth.
- [references/objection-handling.md](references/objection-handling.md) - the five-field objection framework and its two-format delivery, filled with a sponsor-specific objection set built from the four sponsor concerns; inferred rows flagged as such.
- [references/pipeline-and-renewal.md](references/pipeline-and-renewal.md) - the Hot/Warm/Cold/Skip scoring rubric and lead-sheet shape, backward pipeline math with its self-set-rate caveat, tracking and liaison practice, close mechanics, and the renewal motion's boundary with fulfillment.

See also, same collection:

- `samber/dev-event-organizer-skills@event-sponsor-value-proposition` - supplies the pitch content this skill sells; consumes this skill's objection log.
- `samber/dev-event-organizer-skills@event-sponsor-prospectus` - the document sent after the exploratory call.
- `samber/dev-event-organizer-skills@event-sponsor-pricing` - the rate card the proposal step draws packages from.
- `samber/dev-event-organizer-skills@event-sponsor-agreement` - contracts the yes this skill produces.
- `samber/dev-event-organizer-skills@event-sponsor-fulfillment` - delivers what was sold and writes the post-event report the renewal motion is anchored on.

Cross-repo (recommendation, not a dependency): `samber/developer-relations-skills@developer-event-sponsorship` covers the same transaction from the buyer's side - its due-diligence checklist is exactly what your call and first email must be ready to answer, and your target-list fit test is that diligence run in reverse.
