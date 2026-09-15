---
name: event-sponsor-agreement
description: Turn a sold event sponsorship into a term sheet a lawyer can review - never a signable contract or legal advice. Covers the clause checklist an organizer hands to counsel - a deliverables schedule mirroring the sold tier, payment and late-fee terms, sponsor-withdrawal refunds plus the narrower organizer-cancels remedy, a force-majeure remedy, category exclusivity bounded by published caps, liability and insurance, a code-of-conduct clause with an ejection right, mutual logo licensing, term and renewal. Use whenever the user mentions a sponsorship agreement or contract, sponsor payment or cancellation terms, exclusivity, or a force-majeure clause - even if they never say "agreement". Do NOT use to set prices - use samber/dev-event-organizer-skills@event-sponsor-pricing.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Event Sponsor Agreement

**This skill does not give legal advice and never produces a signable document.** Its output is a term sheet - a structured clause checklist, with example language options and open questions marked - that a qualified lawyer in the event's own jurisdiction turns into a contract. Every path through this skill ends at counsel.

Say this to the user at the start and again at handoff. An organizer who signs this skill's output unreviewed has been failed by it.

You formalize a deal that is already closed:

- `samber/dev-event-organizer-skills@event-sponsor-value-proposition` fixed what may honestly be promised.
- `samber/dev-event-organizer-skills@event-sponsor-pricing` fixed the tiers and caps.
- `samber/dev-event-organizer-skills@event-sponsor-prospectus` published them.
- `samber/dev-event-organizer-skills@event-sponsor-outreach` handed you a yes.

You never re-price a tier, invent a benefit, or widen a cap. You turn what was sold into language, and hand the signed deliverables list to `samber/dev-event-organizer-skills@event-sponsor-fulfillment`.

One drafting principle governs everything below, and it comes straight from litigation: **courts read force-majeure and cancellation clauses narrowly and literally.**

- In _NetOne, Inc. v. Panache Destination Mgmt._ (D. Haw. 2020), a deposit refund was denied because the clause did not expressly provide for one. The court declined to "effectively re-write the parties['] contracts to include language that could have been (but was not) used."
- In _Sanders v. Edison Ballroom LLC_ (N.Y. Sup. Ct. 2021), a $45,219.28 deposit was ordered returned because the clause expressly said it would be.

Same doctrine, opposite outcomes, decided entirely by what the text promised. Every branch you draft names its remedy in words.

Every ranking below is a default, not a law; it shifts with context and with who executes it. After the interview, re-rank all four menus against what you know about this organizer - any of the following overturns a default rung:

- An in-house or pro-bono lawyer.
- A fiscal sponsor whose own contract templates apply.
- A venue contract whose insurance requirements flow straight down.
- A single volunteer treasurer chasing invoices.

## Interview

Ask one question at a time, multiple-choice where possible. Questions 6-8 exist because the menus below diverge sharply on time-to-effect, durability and effort - their default orderings cannot be picked for the user.

1. Which pole does the event sit on: community-run (volunteer organizers, published no-attendee-list rules) or company/foundation-run (paid team, consent-bounded lead retrieval already sold)? This decides whether a data clause is draftable at all.
2. What exactly was sold, per sponsor: which tier, at which price, with which perks and which deadlines? Pull it from the signed rate card and prospectus. A perk that is not in either does not enter the contract.
3. Were any caps published - per-tier sponsor counts, single-exclusive surfaces? Name the exact numbers. Exclusivity language may never be looser than the cap the prospectus already printed.
4. Who is the contracting entity on the organizer side: an incorporated non-profit, a company, a fiscal sponsor, or unincorporated volunteers? Unincorporated organizers carry personal exposure and need counsel before anything else in this skill runs.
5. What is the jurisdiction and governing law, and does the organizer already have a lawyer, a fiscal sponsor's legal team, or nobody yet? This is the handoff target; identify it before drafting, not after.
6. By what date must the sponsor be able to sign - when does the invoice have to land? (A near date promotes the shortest-to-draft rungs and makes a long counsel negotiation the binding constraint.)
7. Is this a one-off agreement or a template meant to be reused across sponsors and editions? (A reusable template promotes the higher-effort rungs once and amortizes them; a one-off does not.)
8. What is the effort ceiling: a volunteer treasurer with a template, or a lawyer with time to negotiate clause by clause? (This answer decides the force-majeure and insurance menus almost alone.)
9. What happens physically at the event that an insurer would care about - alcohol served, sponsor demos with physical risk, sponsor-supplied vehicles or heavy equipment - and does the venue contract already require any of this cover?

## Community-run vs company/foundation-run

The axis that changes the contract is who owns the event, the same split the rest of this collection's sponsor block argues:

- **Community-run** - volunteer organizers, often unincorporated or fiscally sponsored. The organizer's own published rules bound what the contract may promise: no attendee contact lists, no purchasable program influence. Bargaining power is low, counsel is usually pro-bono or absent, and the sponsor's own paper often arrives instead. Favors short, single-sentence remedies and the pro-rata force-majeure shape.
- **Company/foundation-run** - a legal entity with staff and, usually, counsel. Consent-bounded lead retrieval may be contracted where it was genuinely sold. Higher-effort rungs (elected credit windows, layered insurance, negotiated indemnity) become affordable. Note that the published contracts quoted throughout sit at this pole, so treat community-pole adjustments as judged rather than established practice.

Neither pole changes the not-legal-advice constraint, and neither pole makes a clause enforceable that the jurisdiction does not recognize.

## Workflow

1. Run the interview, stating the constraint before it: what you produce is a term sheet for a lawyer, never a contract and never legal advice. Confirm the contracting entity (Q4) and the counsel target (Q5) before drafting a single clause. If the organizer is unincorporated with no legal support, say so plainly: that is a structural exposure this skill cannot draft around, and it belongs to `samber/dev-event-organizer-skills@event-team-structure`.
2. Build the deliverables schedule as an exhibit, one row per sold perk: perk, specification, delivery surface, hard deadline, responsible party. Every row traces to the rate card or prospectus (Q2). This exhibit is `samber/dev-event-organizer-skills@event-sponsor-fulfillment`'s input and the single thing most worth getting exact.
3. Draft the payment terms: schedule (menu below), an express late-payment interest rate, and a non-payment clause. Interest is only recoverable if the contract says so - verified rates run 12-18% per annum. Add the obligation-survives-non-attendance sentence and the immediate de-branding remedy; both appear in published contracts. See [references/clause-library.md](references/clause-library.md).
4. Draft cancellation as **two separate clauses, never one symmetric section**. Sponsor withdrawal gets the refund posture from the menu below. Organizer cancellation is a different and narrower remedy in every published example - pro-rata net of the organizer's incurred expenses, sometimes zero after a cutoff. Merging them into one mutual "cancellation" section is the most common structural error in this document.
5. Draft the force-majeure clause: name the triggering events expressly (post-COVID practice names pandemic and epidemic rather than relying on generic "act of God"), then name the remedy in words per the menu below. Never leave the remedy implied.
6. Draft the exclusivity section **only if exclusivity was actually sold** - the PyCon US 2020 contract carries none at all. When sold, it needs all three enforceability elements together and must honor the published cap exactly. See [references/exclusivity-and-renewal.md](references/exclusivity-and-renewal.md).
7. Draft liability, indemnification and insurance. Indemnification is a negotiated term with two real shapes (one-sided organizer-favoring, or mutual) - present both rather than hardcoding one. Take the insurance posture from the menu below.
8. Draft the code-of-conduct clause binding the sponsor's own staff, with an organizer ejection right and the no-refund consequence stated in the same clause. This is confirmed across conferences and hackathons of very different sizes; it is a default, not an option.
9. Draft logo and brand licensing as reciprocal by default: a limited, non-exclusive, promotion-only licence each way, each subject to the other party's brand guidelines, expiring automatically at agreement end unless extended in writing.
10. Draft term, termination and renewal: a cure period (default 30 days, the most common verified length), termination for convenience and for cause, and the renewal mechanic. Confidentiality, data handling, governing law and the general provisions close the document.
11. Mark every open question, every jurisdiction-dependent clause and every figure you could not confirm with an explicit flag, then hand the whole term sheet to counsel (Q5), stating there again that it is not a contract and not legal advice. Name in the handoff what you drafted from an example clause versus what you left for them to decide.
12. On countersignature, hand the deliverables exhibit to `samber/dev-event-organizer-skills@event-sponsor-fulfillment` and the payment milestones to whoever invoices.

If your harness has persistent memory, record per sponsor:

- The sold tier and its exhibit.
- The chosen rung on each of the four menus, and why.
- The cure period.
- The exclusivity category definition, if any.
- The counsel who reviewed it.
- The signature and payment dates.

Next edition's agreements start from that record rather than from a blank template.

The compliance-cost axis appears below only on the two menus whose rungs genuinely diverge on the review they trigger and the reversibility they cost. On the other two, every rung is the same single clause reviewed once, so the axis would be noise.

## Payment schedule

How the fee is collected. Real tech and professional-event sponsorship skews hard toward large upfront commitments, not even installments. Ranking (default, not a law - Q6 and Q8 re-rank):

- effort (invoices raised, balance dates tracked, chases run): `staged deposit plus balance > 100% at signing`
- value, cash banked before the organizer's own sunk costs land: `100% at signing > staged deposit plus balance`
- value, top-tier deals a sponsor's procurement will actually approve: `staged deposit plus balance > 100% at signing`
- efficiency: `100% at signing > staged deposit plus balance`

Two value lines because the axes genuinely disagree: the schedule that banks the most money is not the schedule that closes the biggest deal.

**Dominance check: 2 rungs, 1 pair, zero strict-dominance relations - clean only by construction, and by-construction is never a pass.** The one mechanism is the disagreement just named: each rung wins one value axis and loses the other, so neither is at least equal on both and effort is never reached.

A two-rung menu has nothing else to check. The efficiency call rests on the argument below, not on a passed check.

- **100% at signing or on application** - the default, and the dominant pattern on real cards (AFCEA FedID: "a 100% deposit… is due at signing"; PyCon US 2020: full payment must accompany the form to secure the space; SCCE: in full within 15 days of invoice). One invoice, one chase, no collections exposure.
- **Staged deposit plus balance** - the starved option: high on the deal-capture value axis, high on effort, so efficiency never picks it. Real shapes are a majority deposit rather than an even split (TMS Awards: 80% on signup, 20% three months out, collapsing to 100% if signed inside three months; AWMA: 50% with the application, balance by a fixed date). Promotion conditions: a top-tier sponsor whose procurement cannot release the full amount before a fiscal boundary, a sponsorship large relative to that sponsor's budget, or a signature more than a year before the event.
- **Deleted, not demoted: invoicing after the event.** The payment schedules above all collect between half and all of the fee before doors open. Post-event invoicing hands away the organizer's only leverage - the perks are already delivered, the remedies above (perk hold, immediate de-branding) no longer exist, and `samber/dev-event-organizer-skills@event-sponsor-fulfillment`'s payment gate becomes unenforceable. A sponsor who cannot pay before the event gets a staged schedule, not a post-event one.

Whichever rung you pick, the late-payment interest clause and the non-payment clause are always drafted - they are not menu options.

## Sponsor-withdrawal refund posture

What the sponsor gets back if it pulls out. Two genuinely different postures exist in real published terms, and neither is universal - present both and let the organizer choose by risk tolerance and leverage, rather than silently defaulting. Ranking (default, not a law - Q7 and Q8 re-rank):

- effort (drafting, plus administering notice dates and partial refunds): `graduated multi-tier > two-tier cutoff > hard no-refund`
- value (early signatures a sponsor's risk policy would otherwise withhold, net of revenue given back): `graduated multi-tier == two-tier cutoff > hard no-refund`
- efficiency: `two-tier cutoff > hard no-refund > graduated multi-tier`

The `==` tie is argued: a sponsor's procurement checks whether a refund exists and by which date, not how many steps the ladder has - the third step adds administration without moving the signature. The efficiency ordering is argued too: the two-tier cutoff buys nearly all of a ladder's deal-closing value for one sentence, while the hard no-refund is cheaper still and gives that value up entirely.

- **Two-tier cutoff** - the default: a refund above a dated line, none below it (IBTTA: 50% before a fixed date, none after). PyCon US 2020 gives the citable conference calendar - 75% at 120 days, 50% at 80 days, none after - and PyData shows the same pattern compressing to a single-digit-day scale for a meetup or a hackathon.
- **Hard no-refund** - real and widely used: "no refunds" (ATD/MCI), "non-refundable under any circumstances" (CLOC), or non-refundable except on organizer fault (IPE). Cheapest to draft and administer; the trade is that a cautious sponsor signs later or not at all. NCSI's published rationale - the organizer sustains substantial losses on a cancellation - is usable sourced justification language.
- **Graduated multi-tier** - the starved option: highest deal-closing value, highest administration, so efficiency never picks it (NARI Atlanta runs three steps: refund less a 10% fee, then 50%, then none). Promotion conditions: a top-tier deal whose legal team negotiates this ladder line by line, or a lead time long enough that a single cutoff is too blunt.
- **Deleted, not demoted: an undated "refunds at the organizer's discretion" clause.** Every example above names a date or names "none". A discretionary promise is the shape that produces the dispute, and per _NetOne_ it will be read against whoever hoped it meant more than it says.

## Force-majeure remedy

What happens to the fee when the event cannot be held. The trigger list and the remedy are two separate drafting decisions: name the events expressly (post-COVID clauses name pandemic and epidemic; note the PyCon US 2020 clause is pre-COVID and names neither, so borrow its remedy shape, not its trigger list), then pick a remedy from this menu. Ranking (default, not a law - Q7 and Q8 re-rank):

- effort (drafting, plus the negotiation it opens with the sponsor's counsel): `sponsor-elected credit or refund > flat cash refund > pro-rata net of expenses > no obligation`
- value, cash the organizer keeps when the event dies: `no obligation > pro-rata net of expenses > sponsor-elected credit or refund > flat cash refund`
- value, the sponsor returning for the next edition after a cancellation: `sponsor-elected credit or refund > flat cash refund > pro-rata net of expenses > no obligation`
- efficiency: `pro-rata net of expenses > sponsor-elected credit or refund > flat cash refund > no obligation`
- compliance cost (the review it triggers, and how little of it can be undone): `no obligation > sponsor-elected credit or refund > flat cash refund == pro-rata net of expenses`

**Dominance check: 4 rungs, 6 pairs, zero strict-dominance relations - clean only by construction, and that is not a pass.** Two mechanisms block the six:

- Five are blocked by opposed value axes - cash kept runs exactly counter to the sponsor returning, so no rung is at least equal on both.
- The sixth is not: the sponsor-elected credit beats the flat refund on _both_ value axes and still fails, on drafting effort alone.

Neither reason is evidence. The efficiency line rests entirely on the arguments below.

The compliance ordering is argued: a zero-remedy clause draws the longest review from the sponsor's side and is the hardest position to walk back once a cancellation actually happens, because invoking it is public. The election mechanic adds reviewable moving parts - the window, the credit's value, and what happens if the sponsor stays silent. The flat refund and the pro-rata clause are each a single reviewable sentence, which is the argued tie.

- **Pro-rata net of documented expenses** - the default at the community pole and the shape published contracts use: the organizer refunds the sponsor's proportionate share of what remains after deducting expenses already incurred (PyCon US 2020). It covers sunk costs, which is exactly the risk a volunteer-run event cannot absorb.
- **Sponsor-elected credit or refund, with a dated window** - the starved option: highest relationship value, highest drafting effort. The model is the Linux Foundation's 2021 pivot language, giving sponsors 14 days to elect between transferring to the new format or taking the money. Promotion conditions: a confirmed next edition to credit against, a reusable template (Q7), or sponsors large enough that their counsel negotiates this clause anyway.
- **Flat cash refund within N days** - the sponsor-favorable end (eXp/AGNT refunds within 30 days). Draft it when the organizer's leverage is low or the sponsor's paper is the one being signed, and only when the organizer can survive returning the whole fee.
- **No obligation to refund any part** - real and the most organizer-protective published example (TMS Awards). Legitimate, but it is the rung most likely to be struck in negotiation and the one whose invocation costs the most goodwill.
- **Deleted, not demoted: silence, or a generic "acts of God" clause with no stated remedy.** This is the _NetOne_/_Sanders_ pair in one line: identical doctrine, opposite outcomes, decided purely by whether the text named a remedy. A silent clause is not a neutral default - it is a decision to refund nothing, made without saying so, and discovered during the worst week the organizer will have.

## Insurance requirement

Whether sponsors must carry their own liability cover. Ranking (default, not a law - Q1 and Q8 re-rank):

- effort (chasing certificates, verifying additional-insured wording, tracking per sponsor): `layered coverage > $1M/$2M CGL > none`
- value (exposure genuinely transferred when a sponsor's booth or demo injures someone): `layered coverage > $1M/$2M CGL > none`
- efficiency: `$1M/$2M CGL > none > layered coverage`
- compliance cost (the review it triggers, and how little of it can be undone): `layered coverage > $1M/$2M CGL > none`

**Dominance check: 3 pairs, zero strict-dominance relations - clean only by construction, and that is never a pass.** Value, effort and compliance cost are all the same list, so one mechanism blocks every pair: the rung that transfers more exposure is strictly worse on both cost axes.

Compliance restates the effort order rather than re-ordering it, so it rescues nothing. The check catches no misordering here; what follows is argument.

The efficiency ordering is argued by scale: at meetup size the venue's own master policy already covers the room, so "none" costs nothing and transfers nothing that matters. Layered coverage multiplies chase work for exposures most tech events do not have.

The compliance ordering is argued too - each added coverage line is another certificate to verify, and a missing or wrongly-worded additional-insured endorsement is discovered only after an incident, when it cannot be fixed.

- **No sponsor-carried insurance** - the default for meetups and hackathons, and a real position rather than an omission: small community events routinely rely on the organizer's or venue's master policy. Say this explicitly in the term sheet so counsel sees it was decided, not forgotten.
- **$1M per occurrence / $2M aggregate CGL** - the default once sponsors staff a booth or bring physical demos. This figure is convergent across many independent exhibitor-requirement documents, not one organization's rule. Name the organizer (and the venue where its contract requires it) as additional insured, and tie the certificate deadline to contract execution rather than event-day arrival. A sponsor objecting that year-round cover is disproportionate can buy a single-event policy meeting this standard for well under a hundred dollars.
- **Layered coverage** - the starved option: auto liability, workers' compensation and employer's liability, and product or liquor liability on top of CGL. Highest value, highest effort and highest compliance cost, so efficiency never picks it. **Promotion condition, keyed to Q9**: alcohol served, sponsor demos with physical risk, sponsor-supplied vehicles or heavy equipment, or a venue contract that already flows these requirements down.
- **Deleted, not demoted: an insurance clause with no certificate deadline and no gate.** A requirement nobody collects against is worse than no clause, because it creates a false belief the exposure was transferred. Either require the certificate by a named date and hold the booth until it arrives, or state plainly that no sponsor cover is required.

## Failure modes

- **A silent force-majeure clause.** The single most expensive omission in this document, and the one with real case law on both sides (_NetOne_ denied the refund on silent text; _Sanders_ ordered $45,219.28 back on explicit text). Fix: every branch - event cancelled, postponed, converted to virtual - names its remedy in words before the term sheet leaves your hands.
- **Symmetric cancellation terms.** Drafting one mutual "cancellation" section makes organizer-cancels as generous as sponsor-withdraws. Every published example makes the organizer-cancels remedy narrower - pro-rata net of expenses, sometimes zero after a cutoff. Fix: two clauses, drafted separately, never mirrored.
- **Exclusivity wider than what was published.** A prospectus capping Gold at 3, Silver at 6 and Bronze at 20 has already told the market what exclusivity means here; a contract promising more contradicts the published document every other sponsor bought against. Fix: exclusivity language quotes the published cap, and is drafted only when exclusivity was actually sold.
- **A data or attendee-list clause the event cannot honour.** Published sponsorship contracts carry none, including at the foundation-run pole, and community-run organizers publish rules forbidding it. Fix: a data clause is draftable only where a consented lead-retrieval benefit was genuinely sold; otherwise it does not exist, and the sponsor gets the aggregate-demographics substitute `samber/dev-event-organizer-skills@event-sponsor-fulfillment` delivers.
- **Citing a "PSF 15-day cure period".** This claim is unverified and contradicted by the only public PSF sponsorship contract, which contains no cure period at all - termination there is at the organizer's sole discretion. Fix: default to 30 days (the most common verified length: SAGE World, AFCEA, American Pets Alive), or the event-proximate 3-day variant for breaches found close to the date; never attribute 15 days to the PSF.
- **A deliverables exhibit rebuilt from the prospectus.** The prospectus is the sales document; what the sponsor actually bought, including negotiated deltas, is what the contract must carry. Fix: build the exhibit from the accepted proposal, per sponsor.
- **Treating the output as the contract.** A term sheet that reads like finished legalese invites signature without review - the failure this whole skill is shaped to prevent. Fix: keep the counsel flags visible in the document itself, and state the constraint again at handoff.

## Measurement

Self-set unless labeled otherwise, and measured against your own document rather than an industry figure:

- **Remedy explicitness** (self-set, with case law behind it): zero cancellation, postponement or force-majeure branches left without a named remedy. _NetOne_ is the argument for the threshold being zero rather than "most".
- **Clause coverage** (self-set): every section of the term-sheet checklist either drafted or explicitly marked not-applicable with a reason, before counsel handoff. A silently skipped section is indistinguishable from an overlooked one.
- **Upstream fidelity** (self-set): every deliverable line and every cap traces to the rate card or prospectus; zero invented benefits and zero widened caps.
- **Counsel-review lead time** (self-set): the term sheet reaches counsel before the first sponsor is asked to sign, never after - the one measure whose failure cannot be corrected retroactively.
- **Payment-to-signature lag** (self-set): days from countersignature to first payment received. This is the collections-risk read that promotes or demotes a payment-schedule rung for the next edition.

## Invocation examples

- "A sponsor said yes to our Gold tier. Draft the agreement terms."
- "What should our cancellation and refund policy be if a sponsor pulls out two months before the conference?"
- "Our top sponsor wants category exclusivity in cloud infrastructure. How do we write that?"
- "Write the force-majeure clause for our meetup sponsorship - what happens if we have to cancel?"
- "Do we need to require sponsors to carry insurance for a 60-person hackathon?"

Expected output: a term sheet organized as numbered clause sections plus a deliverables exhibit, each section carrying the chosen option, the example clause behind it where one exists, and an explicit flag on every jurisdiction-dependent or unresolved point - closing with a named handoff to counsel and an explicit statement that the document is not a contract and not legal advice.

## References

- [references/clause-library.md](references/clause-library.md) - clause shapes with verbatim language and attribution: payment, late fees and non-payment, both cancellation directions, force majeure with the case law, cure periods and termination, indemnification and insurance, code of conduct, logo licensing, confidentiality and governing law.
- [references/exclusivity-and-renewal.md](references/exclusivity-and-renewal.md) - category exclusivity's three enforceability elements, the cap-honouring rule, definition traps and carve-outs, premium bands, and the renewal mechanics that avoid a full redraft.
- [references/term-sheet-template.md](references/term-sheet-template.md) - the output artifact: the section-by-section term-sheet checklist with counsel flags, the deliverables exhibit shape, and a negative example.

See also, same collection:

- `samber/dev-event-organizer-skills@event-team-structure` - confirms the legal-entity posture (see Interview Q4); unincorporated organizers need counsel before this skill can run.
- `samber/dev-event-organizer-skills@event-risk-management` - owns the cancellation-decision process; this skill only formalizes the consequences for one sponsor.
- `samber/dev-event-organizer-skills@event-venue-sourcing` - negotiates the venue contract whose insurance requirements flow down to sponsors; read its result before picking the insurance rung in step 7.
- `samber/dev-event-organizer-skills@event-code-of-conduct` - owns the policy the code-of-conduct clause in step 8 points at; this skill only writes the clause and the ejection right.
