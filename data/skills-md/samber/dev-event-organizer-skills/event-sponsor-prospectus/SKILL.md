---
name: event-sponsor-prospectus
description: Assemble a technical event's sponsorship prospectus - the published document packaging an existing sponsor value proposition and rate card into a credibility-before-price section anatomy, a checkmark tier table with real disclosed caps, named per-tier perks and add-on packages, an audience-demographics evidence section, and a distribution format (web page or PDF kit) refreshed every edition. Use whenever the user mentions a sponsor deck, a sponsorship kit, a sponsor packages document, a prospectus, or a sponsor page for a conference, meetup or hackathon - even if they never say "prospectus". Never prints guarantees, invented scarcity, or lead-list benefits the event cannot deliver. Do NOT use to set prices - use samber/dev-event-organizer-skills@event-sponsor-pricing instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Event Sponsor Prospectus

You assemble the sponsorship prospectus for a technical event: the standard, published document a prospect reads before any call. The deliverable is the document itself, its section order, tier table, perks catalog, audience evidence, distribution format, and the per-edition refresh routine.

This skill presents content sibling skills produce, never invents it:

- Value claims and the not-offered list, from `samber/dev-event-organizer-skills@event-sponsor-value-proposition`.
- Tier prices and caps, from `samber/dev-event-organizer-skills@event-sponsor-pricing`.

It does not set prices, run outreach, draft contracts, or track delivery - those are sibling skills.

Every ranking below is a default, not a law - it shifts with context and with who executes it. After the interview, re-rank every menu against what you know about this organizer: a designer on the team, a photo archive from past editions, a first edition with no assets, or a hard outreach deadline each overturn a default rung.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 6-8 exist because the menus below diverge sharply on time-to-effect, durability, and effort - the default rankings cannot be picked for the user.

1. Which pole does the event sit on: community-run (independent, CFP-driven, sponsors as cost recovery) or vendor/foundation-run (vendor-owned, sponsors as pipeline)? This bounds which benefit rows the document may honestly print.
2. Do the upstream inputs exist: per-segment value-proposition statements and the not-offered list, and a priced tier ladder with any à-la-carte prices? If either is missing, route to the sibling skill first - a prospectus drafted without them invents its own value claims and prices, the two things this skill must never do.
3. What real assets exist from past editions: candid photos, sponsor logos, attributed testimonials, press mentions? Assets you have, not assets you could gather.
4. What audience data is verified: headcount only, a rough band (age, "industry professionals"), aggregate role/industry/company-size percentages from registration forms, or survey-backed detail?
5. Which caps are genuinely real: booth floor-space limit, single-exclusive branding surfaces (lanyard, party, coffee), a hard sponsor-count ceiling? Only real caps may be printed.
6. When must the first outreach send land? (A near deadline promotes the fast rungs: a web tier page ships this week; an illustrated kit does not.)
7. Is this document a one-off for this edition or a compounding annual asset? (A compounding mandate promotes the PDF kit and the per-edition refresh system built around it.)
8. What is the effort ceiling: design hours or a designer, layout tooling, and who maintains the document between editions?
9. Which specific sponsor or tier is this prospectus being prepared for, and does that prospect's own diligence checklist ask about buying influence or seniority mix?

## Community-run vs vendor-run

Who owns the event decides what the document may print, the same axis `samber/dev-event-organizer-skills@event-first-edition`, `samber/dev-event-organizer-skills@event-format-selection` and `samber/dev-event-organizer-skills@event-sponsor-value-proposition` argue:

- **Community-run** - no attendee-list or badge-scanning row may appear anywhere in the tier table or add-ons, since no attendee list is ever given or sold and no speaking slot is purchasable. The DevOpsDays Graz 2026 kit contains no lead-data benefit anywhere. Aggregate demographics are the honest substitute, and the document should say what sponsors will _not_ get.
- **Vendor/foundation-run** - consented lead-retrieval rows (badge scanning) are honestly printable, bounded by attendee consent, and pipeline framing is available.

Say which pole the document assumes. A tier table promising scanned leads at a community-run event is caught immediately by any sponsor who reads the organizer's own published rules.

## Workflow

1. Run the interview to fix the pole (Q1) and collect the sibling inputs (Q2):
   - Statements, not-offered list, proof-point inventory.
   - Tier prices, caps, add-on prices.
2. **Honesty sweep**: before laying out anything, list what the document may not print - lead-data rows at the community pole, caps that aren't real, benefits absent from the value proposition, any guarantee (see Failure modes). The not-offered list travels into the document, not just the drafting notes.
3. Choose the document depth from the menu below.
4. Lay out sections in the credibility-before-price order, per [references/document-anatomy.md](references/document-anatomy.md). Proof always precedes price.
   - Cover
   - Brand imagery
   - Event facts
   - Value proposition
   - Proof
   - Tier table
   - Add-ons
   - Logistics
   - Named contacts
5. Build the tier table per [references/tier-table-and-perks.md](references/tier-table-and-perks.md):
   - Price row first.
   - A max-available row only where the cap is real.
   - Plain checkmark cells.
   - Numeric cells only for genuine quantities.
   - Named perks.
6. Choose the perk presentation from the menu below. Move single-exclusive surfaces into named add-on cards when they exist.
7. Write the audience-evidence section at the depth the demographics menu picks - never deeper than the data is verified, per [references/audience-evidence-and-distribution.md](references/audience-evidence-and-distribution.md).
8. Set distribution and the per-edition update cadence from the same reference:
   - A dated document.
   - Refreshed testimonials and logos.
   - Caps re-verified each edition.
9. Validate section by section with the user before any design or layout effort is spent - content errors are cheap to fix in outline and expensive after layout.

If your harness has persistent memory, record per edition: which tiers and add-ons sold out against their printed caps, which perks prospects asked about that the document didn't carry, and the refresh checklist state. Next edition's prospectus starts from that record instead of a blank page.

## Document depth

How much document to build. Ranking (default, not a law - Q6-Q8 re-rank):

- effort (design + assembly hours): `full illustrated PDF kit > in-page tier-table page == text one-pager`
- value (conversion signal to a diligent sponsor: prices visible, proof visible, forwardable inside the prospect's org): `full illustrated PDF kit > in-page tier-table page > text one-pager`
- efficiency: `in-page tier-table page > text one-pager > full illustrated PDF kit`

The effort tie is argued: both bottom rungs are an afternoon of assembling content the sibling skills already produced, with no photography and no layout tooling required. The difference between a prose summary and an HTML table is formatting, not new work.

- **In-page tier-table page** - the default rung: a web page carrying the full tier grid, prices, and a contact email. Ships in days with zero design capacity, and it is a real format - DevOpsDays Graz built exactly this table before moving to a PDF kit. Right for a first edition with no photo assets or a hard outreach deadline (Q6).
- **Text one-pager with tier prices** - the floor when even a table can't be maintained. Keep the price summary and the three facts sponsors always ask about (audience, why sponsor, what per level).
- **Full illustrated PDF kit linked from a web stub** - the starved option: tops value and effort, so efficiency never picks it, yet it is the dominant pattern for community conferences past edition one - the live sponsor page is a short stub whose real prospectus is a downloadable, dated PDF. Promotion conditions: prior-edition photos and testimonials exist (Q3), design hours are available (Q8), or the mandate is a compounding annual asset (Q7).
- **A no-price document is deleted, not demoted** - a prospectus that never states prices forces a reply-to-ask step that costs conversions. The one exception: the rate card was deliberately quote-gated in `samber/dev-event-organizer-skills@event-sponsor-pricing` (a network/portfolio-scale pattern) - then the gate is a pricing decision this document inherits, not a document omission.

## Demographics-evidence depth

How deep the audience section goes. Ranking (default, not a law - the verified data from Q4 is the ceiling, never the target to inflate toward):

- effort (collection + verification): `survey-backed breakdown > aggregate composition breakdown > verified one-liner`
- value (what it answers for a diligent sponsor's "who attends"): `survey-backed breakdown > aggregate composition breakdown > verified one-liner`
- efficiency: `aggregate composition breakdown > verified one-liner > survey-backed breakdown`

**Dominance check: 3 pairs, zero strict-dominance relations - clean only by construction, and by-construction is never a pass.** Value and effort are the same list, so one mechanism blocks every pair: the deeper breakdown answers more and costs strictly more to collect and verify, and no third axis is printed. The check catches no misordering; the ordering rests on the argument below.

- **Default rung**: print the deepest rung that is real and verified. With registration-form data, that is the aggregate composition breakdown - role mix, industry mix, company-size bands, each as labeled percentages, the shape PyCon US prints (2,500+ attendees, 53.9% Developer, Software 43%/Finance 13%/…). `samber/dev-event-organizer-skills@event-sponsor-value-proposition`'s default instrument produces exactly this data.
- **Verified one-liner** - the honest floor for a small or first-edition event: DevOpsDays Graz prints one sentence ("Up to 300 industry professionals, aged 25 to 40 years"). A thin true line beats a thick fabricated table.
- **Survey-backed breakdown** (buying influence, seniority detail, tool adoption) - the starved option: top of value and effort. Promotion condition, keyed to Q9: courting an anchor or presenting-tier sponsor whose diligence asks about buying influence, or a vendor-pole event where composition claims carry the price. Collection mechanics and their compliance load belong to `samber/dev-event-organizer-skills@event-sponsor-value-proposition`'s instruments menu.
- Hard rule at every rung: never publish a breakdown whose category-to-number mapping you cannot verify - the PyCon PDF itself prints a company-size split whose band mapping is layout-ambiguous, and the discipline is to not quote it. A garbled table is a worse credibility signal than fewer categories shown correctly. Never fabricate percentages to match a bigger event's table shape.

## Perk presentation

How the perks catalog appears on the page. Ranking (default, not a law - Q5 re-ranks):

- effort: `tier grid + named add-on cards > single checkmark grid`
- value: `tier grid + named add-on cards > single checkmark grid`
- efficiency: `single checkmark grid > tier grid + named add-on cards`

**Dominance check: 2 rungs, 1 pair, zero strict-dominance relations - clean only by construction, and that is not a pass.** Value and effort run in one order, so the single pair fails on cost: the add-on cards buy more and cost more. A two-rung menu has nothing else to check, no third axis is printed, and the efficiency call is argued below, not verified.

- **Single checkmark grid** - the default: rows are perk line items, columns are tiers, plain marks for inclusion, numbers only for genuine quantities (ticket counts, discount percentages). Keep 3-7 named perk items per tier before the table stops being readable (the real Graz table holds ~10 line items across 5 tiers, most cells blank).
- **Grid + named add-on cards** - the starved option. Promotion condition: single-exclusive surfaces or experiential perks exist (Q5).
  - Move them out of the grid into à-la-carte cards, each an icon + name + price + one line: the sourced pattern ("Photo Booth Sponsor", "Party Sponsor").
  - Name every perk, don't describe it. Container words that signal format ("Track", "Fair", "Lounge", "Corner") do the work.
- **Bespoke per-sponsor proposals are deleted, not demoted** - a prospectus is a standard published offer sent to many prospects. A proposal scoped to one buyer's stated requirements is a different document. Tailoring which sections to emphasize per reader title (DevRel → product feedback, Marketing → brand, HR → recruiting perks) belongs to `samber/dev-event-organizer-skills@event-sponsor-outreach`, not to this document.

Each tier's perk stack should visibly answer a real sponsor concern - attendee value, who else sponsors, package value, the three that hackathon organizer guidance names - not just pile on logo placements. The full perk catalog, including hackathon-specific perks (sponsored prize tracks, sponsor chat channels, workshops, recruiting formats), is in [references/tier-table-and-perks.md](references/tier-table-and-perks.md).

## Hackathon note

MLH itself gates sponsorship behind a contact form and publishes reach numbers, not a prospectus, and its own organizer guidance tells member hackathons to keep any prospectus to 2-3 pages since "sponsors generally don't have time to read through a big sponsorship deck" - likely why MLH-affiliated campus events (HackMIT, PennApps, TreeHacks) route to email instead of a PDF. Independently-run hackathons do publish fuller kits: Cal Hacks 13.0's 5-page packet matches the conference anatomy almost completely, though it orders its tier table before proof and testimonials, reversing the conference proof-before-price default (see [references/document-anatomy.md](references/document-anatomy.md)). Hackathon perks slot into the same tier-table and add-on structure either way. Validate page order and depth with the organizer rather than assuming either pattern - MLH's thin-deck advice and Cal Hacks' full kit are both real, sourced inputs, not the same recommendation.

## Failure modes

- **Printing a guarantee - any guarantee.** DevOpsDays Graz, PyCon US, DjangoCon US and Cal Hacks 13.0 all omit a guarantee clause of any type, a named anti-pattern, not an omission, across both conference and hackathon documents. A performance guarantee ("we guarantee 50 qualified leads") directly contradicts the honesty constraint: community-run events cannot promise lead value at all, and even vendor-run events sell access and placement, never a promised outcome. The nearest real counterexample found is GoatHacks 2023's recruiting section, which promises "the resumes and contact information of all participating students" to every sponsor tier with no cap or hedge - never phrased as a guarantee, but functionally one, and the exact shape this failure mode exists to catch. General offer-construction advice pushes guarantees hard, but this skill rejects it explicitly.
- **Manufactured scarcity.** A "max available" row is printable only when the cap is real (floor space, a single lanyard) - the honest pattern is a published, genuine ceiling (Gold capped at 3, Silver 6, Bronze 20). Never invent a cap, never leave a stale "2 left" counter running past the point it's true.
- **Stale prospectus reuse.** An undated evergreen document, last year's testimonials presented as current, logos of sponsors who didn't return, caps that no longer match inventory. The cadence is a fresh dated document per edition ("Sponsor Information 2026") with per-edition testimonial refresh.
- **Demographics overclaiming.** Fabricated percentages, an unverifiable mapping, or a first edition wearing a big event's table shape - see the hard rule in the demographics menu.
- **Burying the price.** The price row leads the tier table in published prospectuses, and every unanswered price costs a reply-to-ask exchange. Prices go in the document unless quote-gating was a deliberate pricing decision.
- **Selling sponsor benefits harder than the attendee experience.** The buyer-side warning sign diligent sponsors are told to watch for. The anatomy above spends its first half on the event's own credibility (brand, facts, community) before any package appears.
- **Lead-data rows at the community pole.** Structurally undeliverable. See the pole section.
- **A perks list with no why.** Booth sizes and logo placements without the value-proposition content upstream produce a document no budget holder can route internally - route back to `samber/dev-event-organizer-skills@event-sponsor-value-proposition` instead of padding the table.

## Measurement

Prospectus quality has no close-rate figure behind it, so never quote one. What is observable is downstream and self-set. Pick 2-3 and write down the revision each triggers:

- **Reply-to-ask rate** (self-set): prospects replying to ask for information the document should carry - price, dates, audience composition, what a tier includes - flag a document defect, not a sales problem. Have `samber/dev-event-organizer-skills@event-sponsor-outreach` log these by section.
- **Forwardability** (self-set): the document should survive being forwarded to the budget holder without the organizer on the thread. A champion who has to explain it from the top signals a missing section.
- **Per-edition freshness check** (self-set): before each edition's first send - dated title matches the edition, testimonials and logos are from the latest edition, every printed cap re-verified against real inventory.

## Invocation examples

- "Our DevOps conference has its value story and tier prices - turn them into the sponsorship kit PDF."
- "Build the sponsor packages page for our first-edition meetup; we have no photos yet and outreach starts in two weeks."
- "Rework our tier table: five tiers, two of them are just 'your logo on the lanyard' style exclusives, and sponsors keep emailing to ask what things cost."
- "Refresh last year's prospectus for the 2027 edition."

Expected output, in the credibility-before-price order and presented section by section for validation:

- A section-by-section document outline, or full draft.
- The tier table with its price and cap rows.
- Add-on cards where promoted.
- The audience-evidence section at its verified depth.
- The distribution choice.
- The per-edition refresh checklist.

## References

- [references/document-anatomy.md](references/document-anatomy.md) - the generalized page-by-page anatomy with a 9-page worked example, the pitch-deck comparison, the sponsor logistics FAQ checklist, and what real prospectuses deliberately leave out.
- [references/tier-table-and-perks.md](references/tier-table-and-perks.md) - the worked tier table (rows, prices, caps), the perk catalog by sponsor motivation including hackathon perks, naming guidance, and the scarcity never-do list.
- [references/audience-evidence-and-distribution.md](references/audience-evidence-and-distribution.md) - the two audience-evidence models (composition breakdown and one-liner floor), the verification rule, distribution formats, and the per-edition update cadence.

See also, same collection:

- `samber/dev-event-organizer-skills@event-sponsor-value-proposition` - supplies the why: per-segment statements, the not-offered list, and the proof-point inventory this document presents.
- `samber/dev-event-organizer-skills@event-sponsor-pricing` - supplies the numbers: tier prices, caps, and à-la-carte rates. This skill presents the ladder, never sets it.
- `samber/dev-event-organizer-skills@event-sponsor-outreach` - sends the document and tailors per-reader emphasis. It feeds the reply-to-ask log back into this skill's measurement.
- `samber/dev-event-organizer-skills@event-sponsor-fulfillment` - delivers what the document promised. Its post-event report supplies next edition's testimonials and proof.
- `samber/dev-event-organizer-skills@event-sponsor-agreement` - contracts what a prospect accepts. The prospectus is the sales document, never the terms.
- `samber/dev-event-organizer-skills@event-first-edition` - the no-assets, no-track-record case that picks this skill's lighter document rungs.
