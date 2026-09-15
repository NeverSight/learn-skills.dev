---
name: event-media-partnerships
description: Set up barter media and community partnerships for a technical event - visibility-for-visibility deals with newsletters, podcasts, online communities and developer-ambassador programs, where no cash changes hands. Covers deal classes, partner types, the exchange format (calendar listing, logo-and-social swap, newsletter mention swap, podcast exchange, full media-partner tier), the deal terms, and both sides' delivery tracking. Use whenever asked to find media partners, set up a community-sponsor tier, trade newsletter mentions or podcast slots for event visibility, or formalize a logo-for-promotion deal. Do NOT use for earned press - use samber/dev-event-organizer-skills@event-press-relations - or swaps with other events - use samber/dev-event-organizer-skills@cross-event-promotion.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Event Media Partnerships

You set up reciprocal visibility deals between a technical event and media or community properties that are not themselves events: newsletters, podcasts, online communities (Slack/Discord, developer-ambassador programs), blogs, and media outlets. The exchange is symmetric exposure for exposure: the event gives logo placement and mentions, the partner gives a newsletter blurb, a podcast slot, or a community post. No cash changes hands by default. Organizer guides name this as a distinct tier, not an ad-hoc favor:

- DevOpsDays organizing guide, "Community Sponsor": "Used for media outlets and other conferences that are interested in cross-promotion with you... usually you will not ask them to provide cash."
- MLH organizer guide: "Strategic/Media Partners... Community Partners... typically for free."

Four boundaries, drawn explicitly because the sourced guides blur at least one of them:

- **Earned coverage is not a partnership.** "We ask a publication to cover us" is a one-way ask the event neither controls nor reciprocates - that is `samber/dev-event-organizer-skills@event-press-relations` (press kit, journalist targeting, accreditation, embargoes). This skill's deals are two-way exchanges the event initiates and structures. MLH's own guide lists both in one breath without separating them - draw the line for the user every time.
- **Another conference is not a media property.** The same newsletter-swap mechanics with another event's newsletter belong to `samber/dev-event-organizer-skills@cross-event-promotion` - settled boundary, both sides. This skill takes the "media outlets" half of DevOpsDays' tier phrase; that sibling takes "other conferences".
- **Cash reclassifies the deal.** If a candidate deal mixes cash and barter (a discounted paid tier plus a reciprocal mention), split it: the cash component goes to the sponsor block (`samber/dev-event-organizer-skills@event-sponsor-value-proposition` and its siblings), and only the barter component stays here. Never let this skill's simplicity under-charge a sponsor who could pay.
- **The event's own channels are not this skill.** Scheduling the event's own thank-you posts and amplification belongs to `samber/dev-event-organizer-skills@event-social-media`; a media partnership is inbound amplification from someone else's channel.

Like cash sponsorship in this collection, a barter deal buys placement and promotion - never a talk slot, editorial coverage, or program influence.

Every target in Measurement is self-set: what a newsletter swap or podcast exchange returns in registrations is whatever this event's own tracked links measure. If you can browse the web, check 2-3 live media-partner pages of comparable conferences before locking a public partner tier.

Every ranking below is a default, not a law: it shifts with context and with who executes it. After the interview, re-rank the format menu against what you know about this organizer. Each of the following overturns a default rung:

- A partner podcast already recording on-site.
- An organizer who writes a popular newsletter.
- An online-only edition.
- A volunteer team with no bandwidth for content production.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 6-8 exist because the format menu diverges sharply on time-to-effect, durability, and effort - the default ranking cannot be picked for the user.

1. Is the event community-run or company/vendor-run? The organizer guides that describe the no-cash tier are community-run ones - the answer changes whether barter is even on the table (see the next section).
2. Where does the target audience already read, listen, and hang out - which newsletters, podcasts, Slack/Discord communities, ambassador programs, calendar sites? Name real properties; this settles partner types and breaks the value ties below.
3. What can the event offer in return: logo placements (site, badge, screens), social reach, a table or booth space, a ticket allocation, on-site recording space? Never a talk slot.
4. Which outlets or communities already know the event - covered it, attended it, or share organizers with it? Warm paths first.
5. In-person, online-only, or hybrid? Online-only deletes every on-site piece (table or booth, live recording) - delete them, don't demote them; the rungs that survive without them, like a podcast guest slot, stay.
6. When must partner-driven visibility land? A near deadline promotes the fast formats (calendar listing, mention swaps land in days); podcast production and a full partner tier take weeks to months.
7. One-off push for this edition, or a compounding multi-edition relationship? A compounding mandate promotes the slow, relationship-heavy rungs.
8. What is the effort ceiling - organizer hours, content-production capacity, on-site floor space?

## Community-run vs company-run

The axis that changes the deal is who owns the event, the same axis this collection's positioning and sponsor skills argue:

- **Community-run** - the natural home of the barter tier: the organizer guides that name it are community-run, and a partner promoting a community event is supporting an ecosystem it serves, which is why the no-cash norm holds.
- **Company/vendor-run** - barter is the exception here. Expect a media outlet to route promotion of a vendor's event through its commercial ad inventory instead (an outlet that barters visibility for one vendor's marketing event compromises the neutrality its audience pays it attention for). If the outlet quotes its rate card, that is advertising, not this skill; and any coverage expectation attached to the ask belongs to `samber/dev-event-organizer-skills@event-press-relations`, where editorial independence is handled properly.

Say which pole each deal assumes before structuring it.

## Workflow

1. Run the interview; fix the pole (Q1), the audience's real channels (Q2), and the event's give inventory (Q3).
2. **Classify the deal before structuring it:**
   - Counterparty is another event → `samber/dev-event-organizer-skills@cross-event-promotion`.
   - One-way coverage ask with nothing promised back → `samber/dev-event-organizer-skills@event-press-relations`.
   - Cash anywhere in the deal → split it: cash goes to the sponsor block.
   - What remains, a two-way, no-cash visibility exchange with a media or community property, is this skill.
3. Map partner types to the Q2 answers: media outlets/blogs, newsletters, podcasts, communities, and developer-ambassador programs (GitHub Campus Experts, student-ambassador and developer-group programs are the sourced examples - MLH guide). Taxonomy and where each type's audiences concentrate: [references/partner-types-and-scoring.md](references/partner-types-and-scoring.md). This menu is deliberately unranked: which type is worth pursuing first depends entirely on where Q2 found the audience, and ranking types without that answer is false precision - the format menu below is where ranking earns its place.
4. Score each candidate on six criteria (a general partner-scoring frame rather than an events-specific one, say so to the user):
   - Audience fit
   - Audience size
   - Brand alignment
   - Engagement quality
   - Reciprocity potential
   - Ease of execution

   Scoring detail and the outreach ask template: [references/partner-types-and-scoring.md](references/partner-types-and-scoring.md).

5. Pick the exchange format per partner from the ranked menu below, then define **what each side delivers, named and countable** - which placements, which sends, which dates. "Each keeps own leads" is the structural rule (a co-marketing convention, and consistent with the community-run no-list norm): exposure is exchanged, audience data never is.
6. Write the terms down - a one-page agreement, not a handshake: deliverables both directions, dates, logo/branding approval, the no-editorial-obligation clause, and an exit. Outline and a worked example: [references/deal-terms-and-delivery.md](references/deal-terms-and-delivery.md).
7. Track delivery in both directions in a per-partner ledger - the event's own promised mentions are the ones most often silently dropped. Check on-site perks (table, booth) against sponsor-tier exclusivity with `samber/dev-event-organizer-skills@event-sponsor-fulfillment` before promising them.
8. After the edition, read each partnership for renewal: delivered vs promised both sides, referral signal (see Measurement), and whether the partner's audience actually matched. Renew, renegotiate the format one rung up or down, or drop.

If your harness has persistent memory, record per partner: the deal classification, the chosen format and why, both sides' deliverables with dates, delivery status, and the renewal read. Next edition's pass starts from that ledger instead of re-negotiating from scratch.

## Exchange formats

Ranked menu - value returned per unit of organizer effort. The formats come from SaaS co-marketing practice plus the sourced logo-and-mention tier mechanic; the value axis is judged, not measured.

- effort (organizer hours, coordination, production): `full media-partner tier > podcast exchange > community collab > newsletter mention swap > logo-and-social swap == calendar listing`
- value (target-audience exposure bought, judged not measured): `full media-partner tier > newsletter mention swap == podcast exchange > community collab > logo-and-social swap > calendar listing`
- efficiency: `newsletter mention swap > calendar listing == logo-and-social swap > community collab > podcast exchange > full media-partner tier`
- compliance cost (review triggered, reversibility lost): `full media-partner tier > podcast exchange, on-site recording variant only`; the other four carry none - a listing, a logo, a newsletter blurb and a community post touch no signed agreement.

Both exposed rungs put a partner on the floor, in space and category inventory a paying sponsor may already own. Each needs the sponsor-exclusivity check (workflow step 7) before it is offered, and a booth the partner has already announced is hard to withdraw.

All three ties are argued:

- **Effort**: a calendar listing and a logo-and-social swap are each a single asset handoff, a submission form or a logo file plus one scheduled post, under an hour, no counterpart scheduling.
- **Value**: a newsletter slot and a podcast slot both put the event in front of a partner's owned, opted-in audience through the channel that audience actually engages with. Which wins depends on whether Q2 found the audience reading or listening, not on the format.
- **Efficiency**: near-zero effort against modest, passive exposure of the same kind makes the two cheap rungs' ratios indistinguishable.

The formats themselves:

- **Calendar / community listing** - the partner lists the event in its calendar or community board; the event links back. Days to land, near-zero effort.
- **Logo-and-social swap** - the sourced Community Sponsor mechanic (DevOpsDays): logo on the event site plus a social acknowledgement, against the partner's equivalent. The floor of every deal.
- **Newsletter mention swap** - a blurb in the partner's newsletter against a partner mention in the event's own announcements. Each writes for its own audience; each keeps its own list.
- **Podcast exchange** - an organizer or speaker guests on the partner's podcast, or the podcast records live on-site (in-person editions only). Weeks of lead time; the natural rung for a compounding relationship (Q7).
- **Community collab** - cross-posts, a joint AMA, or a channel takeover with a Slack/Discord community or ambassador program. Low production cost, but needs a warm relationship to not read as spam.
- **Full media-partner tier** - a bundled package: badge as official media partner, on-site table or recording setup, multi-channel promotion both directions across the cycle. Some events split the badge itself into named tiers by reach once more than one property holds it - Web Summit's media-partner page runs "global media partners" against "event media partners," keeping the label meaningful instead of flattening into one undifferentiated badge.

Two rules set the default:

- **Default rung**: open every accepted partner at calendar listing plus logo-and-social swap, the sourced tier mechanic, near-zero effort, flat benefits.
- **Promotion condition**: move a partner up to a newsletter swap or podcast exchange when Q2 shows its owned channel genuinely reaches the event's target audience and the engagement-quality score holds, not because the partner asked.

**The starved option is the full media-partner tier** - highest value, highest effort, so efficiency never picks it. Promote it anyway for the flagship outlet or community of the event's own niche when Q7 says compounding and the event has the on-site capacity: that single relationship can carry announcement reach for every future edition. Gate its on-site perks on the sponsor-exclusivity check (workflow step 7).

For an online-only edition, delete every on-site piece - the full tier's table or booth, the podcast's live recording - rather than demoting them. Only the on-site half goes: a podcast guest slot and the rest of the full tier still work online. A deleted item can't quietly reappear as scope during negotiation.

## Failure modes

- **Buying coverage with a partnership.** Writing "two articles about the event" into a partner's obligations turns barter into paid editorial. A partnership buys the promotional inventory the partner controls commercially - a calendar slot, a newsletter blurb, a logo block - never its editorial judgment. If what the event wants is articles, that is `samber/dev-event-organizer-skills@event-press-relations`.
- **The unbounded logo wall.** The sourced tier as published has flat benefits, no qualifying criteria and no cap - applied as-is, every asker gets a free logo and the tier signals nothing. Score candidates (workflow step 4), name each partner's deliverables, and check delivery before renewing.
- **A mixed deal left unsplit.** A partner offering "half rate plus a newsletter mention" is a discounted sponsor, not a media partner. Route the cash to the sponsor block at its real price; keep only the barter leg here.
- **The event's own side undelivered.** The partner's blurb ships; the event's promised thank-you post never does. Both directions live in the ledger with dates, and the event's side is scheduled through its own channel calendar (`samber/dev-event-organizer-skills@event-social-media`).
- **Asking for the partner's list.** A swap that transfers subscriber data isn't a swap - the format logic is that each side mails its own audience, and at a community-run event a no-list norm already governs the cash tiers. Exposure crosses the deal; data never does.
- **Reading a rate-card answer as rejection.** An outlet quoting its ad prices is telling you its promo inventory is commercial, not refusing to engage. Either buy advertising knowingly - outside this skill - or offer the formats it will still barter (calendar listing, guest slot).

## Measurement

Every target below is self-set - a format's yield in registrations is whatever this event's own tracked links measure, so set a target rather than inventing a pass rate. Write down, before outreach, what each signal would trigger:

- **Per-partner referral signal** (self-set): a distinct tracked link or registration code per partner. A partner at zero across two editions gets renegotiated down a rung or dropped.
- **Delivery-ledger completion** (self-set): promised-vs-delivered, both directions, read before any renewal. The event's own completion rate is the honest half - a partner program that under-delivers its own mentions burns warm paths.
- **Audience-match spot check** (self-set): whatever arrives through a partner's channel (poll answers, ticket-type mix) against the Q2 assumption - a high-referral partner sending the wrong audience is a scoring error to fix, not a win.
- **Partner renewal** (self-set): the share of partners who come back unprompted next edition - for barter deals meant to recur, the partner's own renewal is the strongest signal the exchange felt fair on their side.

## Invocation examples

- "We're a 400-person community-run Rust conference - set up media partnerships with the newsletters and podcasts our audience follows."
- "A DevOps podcast asked to be an official media partner of our event. What do we give, what do we ask for, and what goes in writing?"
- "Design our community-sponsor tier: which partners qualify, what they get, and how we avoid handing out free logos."
- "A magazine offered half-price sponsorship plus a newsletter feature - how do we structure this?"

Expected output: a partner map (types and named candidates, scored), one format-and-deliverables definition per accepted partner with both sides' obligations and dates, the one-page deal terms, and the delivery ledger - with every borrowed or self-set element labeled as such.

## References

- [references/partner-types-and-scoring.md](references/partner-types-and-scoring.md) - the partner-type taxonomy with the sourced quotes and examples, the six scoring criteria, and the outreach ask template.
- [references/deal-terms-and-delivery.md](references/deal-terms-and-delivery.md) - the one-page agreement outline, a worked positive/negative deal-definition pair, the delivery ledger format, and the mixed-deal split.

See also, same collection:

- `samber/dev-event-organizer-skills@event-press-relations` - earned, one-way press coverage: journalist targeting, accreditation, embargoes. The reciprocity line above decides which skill a media conversation belongs to.
- `samber/dev-event-organizer-skills@cross-event-promotion` - the same barter mechanics when the counterparty is another event rather than a media property.
- `samber/dev-event-organizer-skills@event-sponsor-value-proposition` - the cash side; a mixed deal's cash component is valued and priced there, never waived here.
- `samber/dev-event-organizer-skills@event-sponsor-fulfillment` - the sponsor-exclusivity check an on-site partner perk must clear, and the delivery discipline this skill's ledger mirrors.
- `samber/dev-event-organizer-skills@event-social-media` - schedules and ships the event's own side of every swap.
- `samber/dev-event-organizer-skills@event-marketing-plan` - the acquisition plan a media partnership feeds into as one channel among several.
