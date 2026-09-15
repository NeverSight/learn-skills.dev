---
name: event-sponsor-fulfillment
description: Deliver everything a signed event sponsor was promised, from countersignature to renewal handoff - the tier-by-perk fulfillment matrix built from the signed agreement, payment-gated perk release, sponsor asset collection against deadlines, the day-of sponsor experience (setup and teardown windows, shipping, booth staffing, power, WiFi, A/V), consented lead capture such as an opt-in raffle, and the post-event sponsor report that anchors the renewal ask. Use whenever the user mentions onboarding a signed sponsor, tracking sponsor deliverables, booth logistics, sponsor logo placement, a post-event sponsor report, or a renewal case - even if they never say "fulfillment". Do NOT use for the sale itself - use samber/dev-event-organizer-skills@event-sponsor-outreach instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Event Sponsor Fulfillment

You deliver what the sale promised: everything between a countersigned sponsorship agreement and a renewal case handed back to the sales motion.

You consume what the siblings fixed upstream, and you output delivered perks with evidence, plus the post-event report that `samber/dev-event-organizer-skills@event-sponsor-outreach` anchors its renewal contact on:

- The promises, from `samber/dev-event-organizer-skills@event-sponsor-value-proposition`.
- The packages and prices, from `samber/dev-event-organizer-skills@event-sponsor-pricing`.
- The signed deliverables list, from `samber/dev-event-organizer-skills@event-sponsor-agreement`.

Two facts govern the whole job:

- No benefit ships before sponsorship fees are paid in full (DevOpsDays sponsor pages).
- The single highest-leverage renewal action an organizer has is a post-event ROI report inside 72 hours: "sell the logo and you get a one-year sponsor; sell the data and you get a partner."

Every ranking below - onboarding instrument, lead-capture posture, report depth - is a default, not a law; it shifts with context and with who executes it. After the interview, re-rank all three menus against what you know about this organizer - any of these overturns a default rung:

- A dedicated sponsorship lead.
- A compounding multi-edition sponsor roster.
- A first edition with three sponsors total.
- A venue whose print deadlines already passed.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 6-8 exist because the menus below diverge sharply on time-to-effect and effort - the default rankings cannot be picked for the user.

1. Which pole does the event sit on: community-run (volunteer organizers, published no-list rules) or company/foundation-run (paid team, consent-bounded lead retrieval on the table)? This decides which lead-capture rungs exist at all.
2. What did each signed agreement actually promise, per sponsor and tier? The matrix is built from the signed deliverables list, never re-derived from the prospectus - custom-negotiated deltas live only in the contract. Route a missing contract to `samber/dev-event-organizer-skills@event-sponsor-agreement` first.
3. What is each sponsor's payment status - invoiced, paid, partial? The payment gate (workflow step 3) needs this before anything ships.
4. What are the hard pre-event deadlines: printer dates for lanyards/swag/signage, program lock, newsletter schedule? The earliest of these, not the event date, sets the fulfillment clock.
5. What did each sponsor say success looks like - the metrics and budget they named on the exploratory call? The report is scored against their stated metric, not a generic one.
6. By what date must the renewal case be ready - when does next edition's outreach start? (A near date promotes the recap email over the full report; the 72-hour window applies either way.)
7. Is each sponsor a one-off or a compounding multi-edition relationship? (A compounding mandate promotes the kickoff call and the full metrics report for that sponsor.)
8. What is the effort ceiling: volunteers with a few hours a week, or a dedicated sponsorship lead? (This answer decides the onboarding and report menus almost alone.)

## Community-run vs company-run

The axis that changes fulfillment is who owns the event, the same split `samber/dev-event-organizer-skills@event-sponsor-value-proposition` and `samber/dev-event-organizer-skills@event-sponsor-outreach` argue:

- **Community-run** - the organizer's own published rules bound what can be delivered: no attendee contact lists, no purchasable speaking slots, aggregate demographics only (DevOpsDays organizing guide - stated twice, in writing). Lead capture exists only in consented forms (see the menu below). Fulfillment is run by volunteers, which favors the checklist-email default and the recap-email default.
- **Company/foundation-run** - consent-bounded badge scanning and lead retrieval are honestly deliverable, and a paid events team can afford the higher-effort rungs. Published organizer guidance is written for the community pole; treat every company-run adjustment as judged rather than established practice.

## Workflow

1. Run the interview; fix the pole (Q1), collect every signed agreement (Q2), and get payment status per sponsor (Q3).
2. Build the tier-by-perk fulfillment matrix from the signed agreements: one row per perk, one column per tier (or per sponsor once custom deltas exist), each cell tracking promised → scheduled → delivered → evidenced. Real row sets, and the published-cap rule the matrix must honor, are in [references/fulfillment-matrix-and-onboarding.md](references/fulfillment-matrix-and-onboarding.md). A flat perk list is the failure shape - it loses the per-tier view that catches an undelivered Gold perk while every Silver row reads done.
3. Gate delivery on confirmed payment: no perk ships - no logo placed, no tickets issued, no booth assigned - before fees are paid in full. Chase the invoice through the liaison, not through withheld surprise at the venue door: tell the sponsor what is being held and why.
4. Onboard each paid sponsor: pick the instrument from the menu below, and collect assets against the deadline table (logo formats, blurb, job posts, workshop content, representative names - MLH organizer guide). Name one liaison per sponsor (DevOpsDays practice - the same liaison `samber/dev-event-organizer-skills@event-sponsor-outreach` assigned, where one exists).
5. Deliver pre-event perks earliest-hard-deadline first: printed surfaces (lanyard, swag, signage) before digital ones, then newsletter and social mentions, program/slide logos, ticket codes. Capture evidence - a link, a screenshot, a photo - into the matrix cell at delivery time, not retroactively.
6. Run the day-of experience: send every sponsor the answered logistics FAQ before they ask (setup/teardown window, shipping, staffing guidance, power/WiFi/A/V - [references/day-of-logistics.md](references/day-of-logistics.md)), stage the booth and premium placements per tier, and run the scheduled raffle and winner hand-off where that perk was sold. Where the perk is a sponsor's own technology in participants' hands - credits, an API, a tool - make an on-site named representative a hard onboarding condition rather than a nice-to-have: documentation alone does not substitute for a live person when someone hits friction under time pressure, and a tool with no one to troubleshoot it gets abandoned the moment it stops working. Where no local representative exists, an enthusiastic independent user of that tool as its on-site point of contact is the fallback, not silence.
7. Send the post-event report within 72 hours, at the depth the report menu picks, scored against each sponsor's own stated success metric (Q5). Template in [references/post-event-report.md](references/post-event-report.md).
8. Hand the renewal case to `samber/dev-event-organizer-skills@event-sponsor-outreach`: the report plus your renew/renegotiate/drop read is this skill's final output; the contact motion, its timing against the sponsor's budget cycle, and the re-signing are theirs. Never build a follow-up cadence here.

If your harness has persistent memory, record per sponsor: the matrix with cell states and evidence links, payment dates, collected assets, the stated success metric, the report sent date and depth, and your renewal read. Next edition's fulfillment - and outreach's renewal motion - start from that record.

## Onboarding instrument

How asset collection and expectation-setting run after signing. The Des Moines FAQ's pattern of routing every non-trivial answer to direct organizer contact argues for scheduled contact over self-service documents. Ranking (default, not a law - Q7 and Q8 re-rank):

- effort: `kickoff call > intake form > checklist email`
- value (assets on time, expectations surfaced early): `kickoff call > intake form > checklist email`
- efficiency: `checklist email > intake form > kickoff call`

**Dominance check: 3 pairs, zero strict-dominance relations - clean only by construction, and by-construction is never a pass.** Value and effort are the same list, so one mechanism blocks every pair: the instrument that gets assets in earlier costs strictly more to run. No third axis is printed to block or rescue a pair. The check catches nothing; the efficiency line rests on the arguments below.

- **Checklist email** - the default: one welcome email per sponsor generated from their matrix column, listing every asset owed, its format, and its hard deadline. Near-zero marginal effort once the matrix exists. Write it against specific program moments rather than as a flat benefits list - which talk slot, which named time block, which reception the sponsor's people are invited to - so the sponsor's own team can put the day on their calendar instead of reading "you're welcome to attend" and guessing when. A minimal fixed asset kit travels with it: photos, a presentation template, and one contact-request email - deliberately narrow rather than a sprawling toolkit nobody finishes.
- **Intake form** - a structured form collecting the same assets with validation (file formats, character limits for blurbs). Worth its setup cost from roughly five sponsors up, when chasing malformed logos one by one costs more than building the form once.
- **Kickoff call** - the starved option: highest value, highest effort, so efficiency never picks it. Promotion conditions: a top-tier sponsor, a first-time sponsor, a compounding relationship (Q7), or any perk needing live coordination - a pitch talk, a workshop, a sponsored track.

## Lead-capture posture

What lead data this event delivers to sponsors. At the community pole the organizer's own published rules decide most of this menu; the compliance-cost axis is here because the rungs genuinely diverge on consent and data exposure. Ranking (default, not a law - Q1 decides which rungs exist):

- effort: `consented raffle > aggregate demographics`
- value (lead data the sponsor can act on): `consented raffle > aggregate demographics`
- efficiency: `aggregate demographics > consented raffle`
- compliance cost (the review it triggers, and how little of it can be undone): `consented raffle > aggregate demographics`

**Dominance check: 2 rungs, 1 pair, zero strict-dominance relations - clean only by construction, and that is not a pass.** Value, effort and compliance cost run in one order, so the single pair fails on cost. The raffle buys more actionable lead data and is strictly worse on both cost axes. A two-rung menu has nothing else to check, and compliance restates the effort order rather than re-ordering it. The efficiency call is argued below, not verified.

The compliance ordering is argued. Aggregate demographics processes nobody's personal data and triggers no review. The raffle collects volunteered personal data for a named sponsor, so it needs:

- A plain statement of what is collected and who receives it.
- Hand-off to that one sponsor only.
- Deletion of the organizer's copy after hand-off.

A mishandled hand-off cannot be walked back.

- **Aggregate demographics** - the default, and the honest substitute for lead data at a community event ("share demographics in aggregate to give sponsors a feel for what kind of crowd will attend" - DevOpsDays guide): role mix, seniority mix, company-size mix, never names. One document, reused across every sponsor and the report.
- **Consented raffle** - the starved option: the opt-in mechanic (DevOpsDays Des Moines sponsor pages): an attendee volunteers their own contact info to a specific sponsor for a chance at a prize; organizers schedule the raffle time and take winner photos. Its value and its effort are both the highest on this menu - and it is the only rung carrying compliance cost - so efficiency never picks it. Track it as a delivered perk, distinct from and never substitutable for an attendee list. Promotion condition: the sponsor's stated mandate is pipeline or recruiting and the perk was sold. Mechanics in [references/day-of-logistics.md](references/day-of-logistics.md).
- **Deleted, not demoted: bulk attendee lists and promised badge scanning at a community-run event.** The organizer's own guide bans both in writing, twice. This is not a bottom rung to reach for under pressure - a sponsor insisting on it gets the two rungs above, or no deal. At a company/foundation-run event, consent-bounded scanning re-enters as a legitimate rung, decided by the buyer and judged on the organizer's side.

## Report depth

What every sponsor receives after the event. The recap shape is well-established (MLH guide: thank-you plus event recap immediately after); the full report template is in the reference. Ranking (default, not a law - Q6, Q7 and Q8 re-rank):

- effort: `full metrics report > recap email > thank-you note`
- value (renewal propensity moved): `full metrics report > recap email > thank-you note` - the 72-hour data-backed report is the named highest-leverage renewal action
- efficiency: `recap email > full metrics report > thank-you note`

**Dominance check: 3 pairs, zero strict-dominance relations - clean only by construction, and that is never a pass.** Value and effort share one ordering, so every pair fails identically: the document that moves renewal further costs strictly more to produce. That covers the pairs against the thank-you note too - it loses on value rather than winning anything for free. The check verifies nothing here.

The efficiency ordering is argued, not a tie dodge. The bare note's near-zero cost buys near-zero renewal movement: a sponsor deciding next year's budget needs delivery evidence, not politeness. The recap is one document with photos and aggregate stats reused across all sponsors.

- **Thank-you note** - never the endpoint; it survives only as the day-after placeholder when the recap needs another day of data.
- **Recap email** - the default for every sponsor, inside 72 hours: thanks, event recap, photos, aggregate attendance and demographics, and each sponsor's delivered-perk summary from the matrix.
- **Full metrics report** - the starved option: the per-sponsor QBR-shaped document in [references/post-event-report.md](references/post-event-report.md), scored against that sponsor's stated success metric, closing with next edition's dates. High value, high effort, so efficiency never picks it. Promotion conditions: the sponsor is a renewal target, a top tier whose price justifies an individualized document, named success metrics on the exploratory call, or a compounding mandate (Q7).

## Failure modes

- **Perks delivered before payment confirmed.** An unpaid sponsor with a printed logo has no reason left to pay, and the published rule is fees in full before benefits. Fix: the payment gate is workflow step 3, before onboarding - and it is communicated, not sprung at the door.
- **A missed print deadline.** A logo absent from the printed lanyard is unfixable after the print run - it becomes a make-good negotiation instead of a perk. Fix: deliver earliest-hard-deadline first; the fulfillment clock starts at the printer's date, not the event's.
- **A promised perk discovered undelivered at report time.** Reconstructing the matrix after the event converts the renewal ask into an apology. Fix: cells move to delivered-with-evidence in real time; if a perk did slip, name it in the report yourself, with a make-good, before the sponsor finds it.
- **Bulk-list leakage.** A volunteer exports the attendee list for an insistent sponsor - one leak breaks a published community rule for every future edition. Fix: the deleted rung stays deleted; brief every volunteer that the raffle and aggregate demographics are the only data hand-offs that exist.
- **The report waits for next year's planning.** The sequence is recap immediately, rekindle later - a report sent months late anchors nothing. Fix: 72 hours, even at recap depth; outreach owns the rekindle.
- **Deliverables rebuilt from the prospectus.** The prospectus is the sales document; negotiated deltas live in the signed agreement. Fix: the matrix's promise column quotes the contract, per sponsor.
- **A sponsored session confirmed on logo fit alone.** Brand fit and topic pitch are not the same check as what the speaker will actually say on stage - a sponsored slot advising a time-boxed audience to first spend hours training on a tool works directly against the event's own format, and nobody caught it because nobody reviewed the content. Fix: review the actual content of a sponsored slot before it is confirmed, not just the sponsor's name and topic.

## Measurement

Self-set unless labeled otherwise, and held against your own matrix rather than an industry figure:

- **Perk delivery completion** (self-set): 100% of matrix cells delivered-with-evidence or named-with-make-good before the report goes out. Anything less is the report-time-discovery failure above.
- **Report latency** (published threshold): every sponsor reported inside 72 hours.
- **Asset collection on time** (self-set): assets in hand before each hard deadline; a late logo is this skill's earliest warning light.
- **Renewal rate** (a published aim, not a measured benchmark): high-performing events target ≥70% per edition. It reads on the whole relationship and belongs to `samber/dev-event-organizer-skills@event-market-fit` as a demand signal; this skill is its driver, outreach its executor.

## Invocation examples

- "Three sponsors signed for our October conference. Set up the fulfillment tracking."
- "The Gold sponsor's logo is due at the printer Friday and two sponsors still haven't paid. What ships and what holds?"
- "The event ended Saturday. Write the sponsor reports."
- "Our top sponsor wants attendee emails. What can we actually deliver?"

Expected output:

- A live tier-by-perk matrix with per-cell status and evidence.
- Per-sponsor onboarding checklists with hard deadlines.
- A day-of sponsor brief answering the logistics FAQ.
- Per-sponsor post-event reports at menu depth, each closing with a renew/renegotiate/drop read handed to `samber/dev-event-organizer-skills@event-sponsor-outreach`.

Label every constructed shape and self-set threshold as such.

## References

- [references/fulfillment-matrix-and-onboarding.md](references/fulfillment-matrix-and-onboarding.md) - the matrix shape with two real row sets and the published-cap rule, cell states, the payment gate's basis, the phased onboarding checklist, and the asset intake list with a deadline table.
- [references/day-of-logistics.md](references/day-of-logistics.md) - the answered sponsor logistics FAQ from a real recurring event, staffing guidance, and the consented-raffle mechanics with their privacy hygiene.
- [references/post-event-report.md](references/post-event-report.md) - the report template, the mirrored renew/renegotiate/drop read, the 72-hour and renewal-rate claims, and a negative example.

See also, same collection:

- `samber/dev-event-organizer-skills@event-booth-experience` - designs the floor layout, tier physical specs and master setup schedule once per edition; this skill takes its day-of logistics answers from that floor brief rather than restating its own.
- `samber/dev-event-organizer-skills@cross-event-promotion` - a booth or exclusivity swap between two organizers must clear this skill's sponsor-exclusivity terms before either side commits.
- `samber/dev-event-organizer-skills@event-attendee-experience` - owns the sponsor-side lead-capture posture (including deleting promised badge scanning at a community-run event) directly adjacent to this skill's fulfillment matrix.
