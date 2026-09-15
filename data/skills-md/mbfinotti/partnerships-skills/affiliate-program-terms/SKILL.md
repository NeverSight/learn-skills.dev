---
name: affiliate-program-terms
description: Draft the terms and conditions an affiliate accepts when joining a commission-based program - the affiliate program agreement, with the canonical clause set, prohibited-tactics clauses and enforcement ladder, commission validation, clawback and termination mechanics, and jurisdiction overlays (FTC endorsement rules, EU P2B, UK ASA/CAP, GDPR roles). Output is a clause-complete draft flagged for mandatory legal review, for B2B SaaS and B2C ecommerce alike. Use whenever the user mentions affiliate program terms, an affiliate agreement, prohibited tactics, or a brand-bidding policy, even if they only ask what affiliates must agree to. Do NOT use for reviewing a published post's disclosure label - use mbfinotti/partnerships-skills@affiliate-disclosure-compliance instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.3.5"
---

# Affiliate Program Terms

Draft the terms and conditions an affiliate accepts when joining a commission-based program. No single canonical "how to draft affiliate terms" framework exists - the Performance Marketing Association's Retailer Affiliate Agreements Guide is the closest thing to an industry checklist, and the clause set itself is highly standardized across real published agreements. The governing drafting principle is Geno Prussakov's: "any practices that you do not explicitly prohibit are, implicitly, permitted" - this document earns its keep by enumerating, never by catch-alls.

These agreements are near-universally non-negotiated clickwrap contracts of adhesion, accepted by conduct and amended under "continued participation equals acceptance". They bind real people from the moment of signup, which is why legal review below is a workflow step, not a footnote.

## Legal Review Is a Step, Not a Footnote

The produced document is a draft for legal review - never legal advice, never a finished contract.

1. State before drafting anything: "This will be a draft for review by qualified counsel, not legal advice. Program terms are legally binding."
2. Mark each clause needing specific counsel attention inline with `[LEGAL REVIEW: <reason>]`, placed next to the clause - never pooled in a footer.
3. Always mark these clauses:
   - Governing law/arbitration.
   - Forfeiture of earned commissions.
   - GDPR role allocation.
   - Trademark-bidding ban.
   - Unilateral amendment.
   - Indemnity and liability caps.
   - Tax/contractor status.
4. Repeat the disclaimer with the delivered artifact, plus an instruction to keep every inline marker until counsel clears it.

Counsel sign-off, the canonical clause skeleton, and every jurisdiction obligation the interview surfaces - FTC disclosure, P2B notice and statement of reasons, ASA labeling - are gates, not menu items. They are drafted or the document is not deliverable, so they never enter an efficiency ordering and are never traded against effort. Only the genuinely optional policy positions get ranked, and each ranking sits at the point where that position is chosen.

## Interview

Ask before drafting, following these rules:

- One question per message.
- Offer multiple-choice answers.
- Skip anything the user already answered.

Ask the first three before anything else - they re-rank every policy position below, and asking them after the user has picked one is too late.

- By what date must the terms be live: a signup page opening on a fixed near date, or a program still being designed? A fixed near date deletes the keyword-whitelist and per-partner-tier brand-bidding positions outright - neither can be adjudicated partner by partner before launch.
- A one-off document, or a maintained one with dated versions and a change record? One-off promotes the strict positions that need no ongoing adjudication; maintained is what makes a whitelist or a chargeback reserve affordable at all.
- Effort ceiling: who drafts and who reviews - in-house counsel, outside counsel, or the program manager alone - and are there already-published terms with live affiliates on them? Published terms only tighten through the amendment cycle (15 days' notice for EU/UK business users, each with a right to leave rather than accept), so every tightening is a negotiation with the affiliates you already have, and reversibility, not hours, is the binding constraint.
- B2B SaaS, B2C ecommerce, or both?
- In-house/SaaS-hosted program, or network-hosted? Network-hosted means the network's master terms are the baseline and this document is only the program-specific layer on top.
- Where are the affiliates, and where are the customers?
  - EU/UK business users may trigger P2B procedural rules - whether an in-house program is in scope is a counsel question, so ask and flag it rather than assume either way.
  - US triggers FTC disclosure.
  - UK adds ASA/CAP and CMA exposure.
- Which commission mechanics are already decided elsewhere - rate, recurring vs one-time, validation window, payout threshold? This document references them; it never designs them.
- Any known abuse concerns?
- Which brand-keyword-bidding position? Offer the four standard ones in this order, ranked by what each buys per unit of drafting, adjudication, and renegotiation:

  - efficiency: strict prohibition > trademark-only ban with a modifier allowance > per-partner tiering > keyword whitelist
  - effort: keyword whitelist (a standing job - per-keyword requests, adjudication, an audit of live ads) > per-partner tiering (a week to define the tiers, then a negotiation with every partner promoted or refused) > trademark-only ban with a modifier allowance (an hour more than the strict ban, since the permitted modifiers have to be enumerated too) > strict prohibition (near-zero - one enumerated clause plus the brand as a negative keyword)
  - value: keyword whitelist == per-partner tiering (both keep the converting trademark-plus traffic of trusted partners while excluding everyone else, by different routes to the same short list) > trademark-only ban with a modifier allowance > strict prohibition (brand-term margin recovered, at the cost of the partners who only convert there)
  - compliance cost: per-partner tiering > keyword whitelist > trademark-only ban with a modifier allowance == strict prohibition (tied: each is one uniform rule cleared by counsel once, whatever its width). The first two apply different rules to different affiliates - the shape P2B asks you to state grounds for, and the one inconsistent enforcement destroys - so both need counsel on the discrimination question, and neither loosens or tightens again without an amendment cycle.

  Lead with strict prohibition because it wins the ratio; that it is also the least work is unusual here, not the reason. The whitelist is what this order starves - top of the value axis, bottom of the ratio, beaten every round.

  Promote it when a named partner already drives brand-term volume you would otherwise cede to unaffiliated arbitrage, and someone owns the adjudication as a standing job. Delete the whitelist and the tiering when nobody owns that job: a position no one enforces is indistinguishable from permission.

- Are coupon/deal sites permitted, restricted, or banned?

  - efficiency: restrict > ban == permit fully

  - Restricting (only issued codes, no expired or unissued codes, no trademark-plus-coupon terms) costs a week of definition and policing, but it keeps the discovery traffic while removing the code-scraping arbitrage.
  - Banning is near-zero to write and keeps the margin, at the cost of the orders.
  - Permitting fully is equally near-zero to write and keeps the orders, funding the arbitrage in exchange.

  Drafting detail in [references/prohibited-tactics.md](references/prohibited-tactics.md).

- Are browser extensions permitted or banned? efficiency: ban outright > permit with a stand-down obligation. The ban is one clause; permitting is a standing job, because a stand-down rule is only worth its ink if you can obtain clickstream evidence, and every permitted extension has to keep meeting disclosure and genuine-user-benefit tests you now warrant against. Promote permission when extension partners already drive a material share of tracked revenue and that evidence is available; see the same reference for the wording.
- Approval mode: manual review or auto-approval? Not ranked here - this document writes the eligibility clause, while the trade-off between the two belongs to the sibling fraud-detection skill, which ranks it against program size. Take the answer as given and draft to it.
- Revising existing terms, or starting from a blank page? If revising, request the current document.

Every ordering in this skill is a default, not a law: it shifts with context and with who executes it. Re-rank against what you already know about the user before proposing anything. In-house counsel makes each review-heavy position cheaper and promotes the contested ones. An already-published program with live affiliates prices every tightening at one amendment cycle plus the affiliates who leave, and demotes it accordingly. A regulated vertical - financial services, health, gambling - can make a permissive brand-bidding or review-content position unavailable at any effort level, which deletes it rather than demoting it.

## Workflow

1. Deliver the legal-review statement, then run the Interview.
2. Confirm the boundary: rates and tiers are designed elsewhere (see Reference); the terms cite the existing structure and nothing more.
3. Ask clarifying questions wherever the task is ambiguous - baseline paper (network master vs own), contested-area positions, which geographies count - before writing a word.
4. Assemble the canonical skeleton from [references/clause-library.md](references/clause-library.md). The skeleton is largely identical for B2B SaaS and B2C ecommerce; the divergent clauses live in [references/b2b-vs-b2c-contrast.md](references/b2b-vs-b2c-contrast.md).
5. Draft the prohibited-tactics section and its enforcement ladder from [references/prohibited-tactics.md](references/prohibited-tactics.md). Enumerate every banned tactic; never rely on a catch-all alone. The ban list is not a menu - only the three program positions settled in the Interview are choices, and the ladder is a sequence rather than a ranking.
6. Draft termination, validation/clawback, and amendment mechanics from [references/termination-and-payment-mechanics.md](references/termination-and-payment-mechanics.md). Close the three most commonly missing clauses:
   - Pending commissions at termination.
   - The enforcement ladder.
   - Automatic brand-licence revocation.

   Clawback authority is a gate wherever commissions are paid before the transaction is chargeback-safe - the clawback window always expires before chargeback exposure does. The two controls that keep working after it expires are ranked in that file; the sibling fraud skill treats an uncovered tail as a blocking finding, which is the condition that promotes the reserve.

7. Layer jurisdiction obligations from [references/jurisdiction-and-compliance.md](references/jurisdiction-and-compliance.md) for every geography the interview surfaced.
8. If you can browse the web, re-verify every regulatory figure, effective date, and notice period before citing it - penalty amounts are inflation-adjusted annually and guidance gets revised. Otherwise label each one "as of drafting - re-verify".
9. Flag the three genuinely contested areas instead of asserting a settled answer (next section).
10. Run the Completeness Check; iterate on the draft until every line passes.
11. Present the skeleton section by section for user validation, then deliver the full draft with the disclaimer repeated and all `[LEGAL REVIEW]` markers intact.
12. If your harness has persistent memory, memorize the decided positions - geographies, brand-bidding policy, validation and clawback windows, contested-area choices - so a later revision starts from them instead of re-interviewing.

## The Three Contested Areas

Present options and mark `[LEGAL REVIEW]`; never assert a settled answer.

- **Trademark-bidding bans** - contractual only; search engines will not enforce them, and bidding on a mark as a keyword is generally lawful. The clause still works as a contract-termination trigger. Which of the four positions to take is ranked in the Interview, where the user picks it.
- **Blanket forfeiture of earned commissions on termination** - lawfulness unsettled, with tension against US state escheatment law. Prefer narrow reversals (fraud, returns, cancellations) over forfeiture. Not an efficiency call: legality decides it, not payoff per unit of effort.
- **GDPR role of affiliates and networks** - processor vs joint controller vs independent controller is genuinely disputed among major networks. The advertiser is always a controller; resolve the rest explicitly in the DPA.

  Deliberately left unranked: these are three competing readings of one legal fact, not three options with different payoffs, so ordering them by effort would manufacture a recommendation the law itself does not support. Present all three, name which major networks take which, and let counsel decide.

## Output Shape

Deliver a markdown terms document in this section order (clause-by-clause detail in [references/clause-library.md](references/clause-library.md)):

1. Definitions
2. Eligibility & Approval
3. Licence to Brand Assets
4. Commission & Payment (citing the existing rate structure)
5. Tracking & Attribution
6. Prohibited Tactics & Enforcement
7. Disclosure Obligations
8. IP & Confidentiality
9. Data Protection
10. Representations & Warranties
11. Indemnity
12. Limitation of Liability
13. Term & Termination
14. Effect of Termination on Pending Commissions
15. Clawback & Reversal
16. Chargeback Reserve & Negative Balances
17. Amendment
18. Assignment
19. Governing Law & Disputes
20. Tax & Independent-Contractor Status

## Completeness Check

Do not deliver until every item passes; iterate until it does.

- [ ] Every canonical clause is drafted or explicitly marked "intentionally omitted - <reason>".
- [ ] The three commonly missing clauses are present: pending commissions at termination, prohibited-tactics enforcement ladder, automatic brand-licence revocation.
- [ ] Every jurisdiction trigger from the interview is addressed: P2B notice periods (or the in-scope question flagged `[LEGAL REVIEW]`), FTC disclosure obligation, ASA/CAP labeling, GDPR/DPA role.
- [ ] Clawback authority is drafted wherever commissions are paid before the transaction is chargeback-safe - it is a gate, never omitted, since a reversal right with no collection path enforces nothing.
- [ ] Negative-balance carry-forward is drafted; the chargeback reserve is drafted or explicitly marked "intentionally omitted - <reason>" with the residual chargeback tail named.
- [ ] Each contested area is either irrelevant to this program or flagged with options and `[LEGAL REVIEW]`.
- [ ] Prohibited tactics are enumerated with an enforcement ladder; no bare catch-all.
- [ ] Commission language cites the decided structure; nothing in the draft invents a rate, tier, or threshold.
- [ ] The legal-review disclaimer accompanies the delivered artifact and every inline marker is intact.

## Invocation Examples

- "Draft affiliate program terms for our B2B SaaS - 20% recurring for 12 months is already decided, affiliates mostly US and EU."
- "Our store's affiliate agreement says nothing about coupon extensions - rewrite the prohibited-tactics section with an enforcement ladder."
- "We're moving from a network-hosted program to in-house; write the agreement affiliates accept at signup."

## Common Failure Modes

| Defect                                          | Consequence                                                                                                                                                           | Fix                                                                                                                                              |
| ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| No clause on pending commissions at termination | Disputes, even small-claims filings, on every termination                                                                                                             | Distinguish fraud (forfeit) from non-fraud (pay accrued to termination date)                                                                     |
| Vague prohibited-tactics list, no ladder        | Unlisted tactic is implicitly permitted; no proportionate response short of termination                                                                               | Enumerate tactics; warning → voiding → suspension → termination → recovery                                                                       |
| No automatic brand-licence revocation           | Ex-affiliates keep using brand assets after termination                                                                                                               | Auto-revoke on any termination + asset-destruction window                                                                                        |
| Blanket forfeiture of earned commissions        | Legally contested; escheatment exposure; reads as punitive                                                                                                            | Narrow reversals to fraud, returns, cancellations                                                                                                |
| Unilateral amendment with no notice mechanism   | Null and void toward EU/UK business users wherever P2B applies - whether it reaches an in-house merchant program is unsettled, so treat it as exposure, not certainty | Electronic notice + continued-participation acceptance + 15-day notice for EU/UK business users, with the scope question marked `[LEGAL REVIEW]` |

## Reference

- See [references/clause-library.md](references/clause-library.md) when assembling the skeleton - every canonical clause, common variations, drafting cautions.
- See [references/prohibited-tactics.md](references/prohibited-tactics.md) when writing the ban list and enforcement ladder - tactic-by-tactic wording patterns, sourced principle.
- See [references/termination-and-payment-mechanics.md](references/termination-and-payment-mechanics.md) when drafting validation windows, clawback, termination, dormancy, and amendment.
- See [references/jurisdiction-and-compliance.md](references/jurisdiction-and-compliance.md) when the interview surfaces US, EU, or UK exposure - what is universal vs jurisdiction-specific.
- See [references/b2b-vs-b2c-contrast.md](references/b2b-vs-b2c-contrast.md) when tailoring to SaaS vs ecommerce - the divergent clauses side by side.
- See [references/worked-examples.md](references/worked-examples.md) when shaping the final document - real published agreements decomposed, one worked outline, one negative example.
- See `mbfinotti/partnerships-skills@affiliate-commission-structure` to design the commission rates and tiers this document only references.
- See `mbfinotti/partnerships-skills@affiliate-disclosure-compliance` to audit already-published affiliate content; this skill only writes the disclosure obligation into the terms.
- See `mbfinotti/partnerships-skills@affiliate-fraud-detection` for operational fraud detection; this skill only writes the prohibited-tactics clauses and the enforcement ladder.
- See `mbfinotti/partnerships-skills@referral-abuse-guardrails` for consumer refer-a-friend gaming rules - a different audience than professional affiliates. That skill also emits its own consumer-facing terms wording; this one covers the professional-affiliate agreement only, so do not accept a consumer refer-a-friend terms request routed back here.
- See `mbfinotti/partnerships-skills@affiliate-onboarding-sequence` for what happens after an affiliate is approved.
