---
name: partner-economics
description: Model the unit economics of one partner relationship - partner P&L, margin modeling, cost-to-serve, referral-fee and lifetime-value split, channel partner ROI, partner CAC vs direct CAC, ramp and payback - to decide whether to sign, scale, renegotiate, or exit that partner. Covers B2B channel and alliance partners plus B2C affiliate and creator economics. Use whenever the user mentions partnership unit economics, a single-partner business case, reseller, VAR, MSP, OEM or marketplace deal economics, revenue-share and margin-stack analysis, or asks whether a partner is worth pursuing, even if they never say economics. Do NOT use for ranking a portfolio of candidates - use mbfinotti/partnerships-skills@alliance-prioritization instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.4.1"
---

# Partner Economics

Model one partner relationship as a small P&L - attributable revenue net of every partner cost, against partner CAC, ramp, and incrementality - to decide sign, scale, renegotiate, or prune. Two structural facts frame the whole exercise; state them plainly rather than paper over them:

- **No canonical "partner P&L" template exists.** Practitioners converge on the same revenue and cost components, but vendors publish incompatible definitions, and any claim to _the_ standard (PARTNERNOMICS-style certification included) is a proprietary product, not industry consensus.
- **Most widely quoted partner benchmarks are vendor marketing, not research.** The famous "80% of channel revenue from 20% of partners / only 11% hit incentive goals" figures are untraceable; so are the "most partners never transact" claims. Label every number's evidence class; quote nothing as settled fact without a named source. Read [references/benchmarks-and-figure-grading.md](references/benchmarks-and-figure-grading.md) before citing any figure: the graded benchmark set, plus the untraceable figures to refuse.

What the field genuinely offers:

- **Hans Peter Bech's channel-partner P&L** - model the PARTNER's own 3-5 year economics, because "it is crucial that the channel partner takes ownership of the P&L." The single most articulated practitioner method for one relationship.
- **Spengler's double marginalization (1950)** and the two-part tariff fix (Jeuland & Shugan 1983; McGuire & Staelin 1983) - the peer-reviewed root of margin stacking.
- **Blake, Nosko & Tadelis (2015, Econometrica)** - when eBay halted brand-keyword ads, 99.5% of clicks were retained, the canonical proof a channel can show strong attributed revenue while being nearly non-incremental.
- **Dyer & Singh's relational view (1998, AMR)** - "relational rents", profit neither firm could generate alone - and **Gomes-Casseres' Third Law** (_Remix Strategy_, 2015): the value split must motivate both parties to keep contributing.
- **Dyer, Kale & Singh (2004, HBR)** ally-vs-acquire, plus **Anderson & Schmittlein (1984, RAND J. Econ.)** and the 2006 AMJ TCE meta-analysis - peer-reviewed grounding for whether a partner channel is even the right mode before any economics get modeled.

## Interview

Ask before modeling anything. One question per message; offer multiple-choice options; skip whatever the user already answered.

- Partner type: referral/agency, reseller/VAR, distributor/two-tier, MSP, OEM/embed, ISV tech alliance/co-sell/marketplace, or affiliate/creator?
- Whose economics: your side, the partner's own P&L (Bech's point - the partner must own theirs), or both? The ranked answer is in Brainstorming the model; the three questions below decide which rung applies.
- Which decision must this model serve - sign / don't sign, scale, renegotiate, prune/exit - and what go/no-go threshold applies? Who signs off?
- By what date must the verdict land - a signature deadline, a board or QBR slot? Anything inside a few weeks rules out both the dual-sided P&L and any incrementality experiment; each needs partner disclosure or a read-out window.
- One-off decision, or a model re-run at every QBR? A re-run mandate promotes the dual-sided P&L and a written assumption register; a one-off promotes the vendor-side contribution model alone.
- Effort ceiling: analyst hours available, whether a finance reviewer is assigned, and whether the partner will open its own numbers? No finance reviewer, or a partner that will not disclose, caps the work at the vendor-side model whatever the decision needs.
- What is your current direct CAC, and the average deal size it buys? Step 6 compares against both; without them there is no threshold to test.
- What is product gross margin, and the churn rate or average customer lifetime for this segment? Lifetime value is computed on margin, so guessing either one silently sets the verdict.
- Revenue mechanics: fee as % of first-year ACV or recurring, discount off list, royalty, revenue share, CPA?
- What stacks on top: rebates, SPIFFs, MDF commitments, deal-registration uplift, marketplace listing fee?
- Costs to recruit, enable, and serve: account-manager time, training/certification delivery, portal and tooling, support load?
- Contract shape: exclusivity, term, deal registration, clawback, MDF commitments, minimums?
- Ramp expectation: time to first revenue, and who funds the double-cost period?
- What data actually exists: CRM attribution with sourced/influenced tagged, marketplace disbursement reports, finance systems - or estimates only?
- B2B channel/alliance or B2C affiliate/creator?

## Workflow

1. Run the Interview. Fix the decision the model serves and its go/no-go threshold before computing anything - a model built without a threshold produces a flattering number, not a verdict.
2. Pick the partner-type economic model; money flows and margin math differ sharply by type. See [references/partner-type-economics.md](references/partner-type-economics.md).
3. Separate partner-sourced, partner-influenced, and partner-attached revenue; never blend them. Cap influence credit so attributed revenue can never exceed total revenue - uncapped influence ends the conversation with finance immediately and permanently.
4. Build the fully-loaded cost stack: discount off list, rebates/SPIFFs, MDF, marketplace fee, account-manager time, enablement and certification delivery, support, portal/tooling allocation. A $2M partner net of $500K discounts, $200K MDF, $150K account management, and $100K training/support contributes $1.05M, not $2M.
5. Compute partner-adjusted gross margin and annual net contribution. Compute lifetime value on gross margin, never on revenue. See [references/metrics-and-formulas.md](references/metrics-and-formulas.md).
6. Compute partner CAC fully loaded, then compare it to direct CAC on a like-for-like basis: acquisition cost per $1 of net revenue, never per customer. Per-customer CAC prices different goods whenever a discount lowers revenue per partner deal.

   Two conventions are internally consistent; state which one you used and never mix them:
   - Book revenue gross and charge the discount to acquisition cost.
   - Book revenue net of discount and leave it out.

   Do not rank the two conventions: on the per-$1-of-net-revenue basis they produce the same number, so an ordering would be false precision. If partner cost per $1 of net revenue is not below direct's, the channel thesis is broken; say so in the memo.

7. Model ramp and payback. The first 6-12 months are a double cost - funding the partner's enablement and your own team simultaneously. State time to first revenue and the month cumulative contribution crosses zero.
8. Test incrementality explicitly: how much of this revenue would have arrived through direct anyway? Attributed is not incremental (Blake, Nosko & Tadelis).

   Start with the assumed-rate band, never with an experiment - efficiency: assumed-rate band > matched holdout > geo split > channel pause. Buy an experiment only when the verdict flips inside the plausible range.

   That order starves the channel pause, which buys the strongest evidence available and costs the most. Promote it only when incrementality is the entire verdict; delete it outright where exclusivity or minimums in the agreement forbid suspending the motion.

   Evidence strength, effort and compliance exposure are ranked separately in [references/metrics-and-formulas.md](references/metrics-and-formulas.md).

9. Run sensitivity on the 2-3 assumptions that actually move the answer - usually deal volume, effective discount, and ramp length. Report which shifts flip the verdict.
10. When modeling both sides, build the partner's own 3-5 year P&L (Bech) and test the Gomes-Casseres Third Law: does the value split motivate the partner to keep contributing?
11. Present the memo section by section - revenue, costs, contribution, CAC, ramp, incrementality, sensitivity, verdict - and validate each with the user before drafting the next.
12. Stop at the approval gate: finalize nothing without the user's explicit approval of the assembled memo.
13. Check the Pass Threshold below; iterate until every check holds.
14. Set the revisit cadence and triggers: joint-business-plan refresh at period start, a QBR economics review each quarter, a renewal/exit gate - plus event triggers such as a marketplace fee change, a commission renegotiation, or a ramp-milestone slip.
15. If your harness has persistent memory, memorize the approved model, its named assumptions, and the verdict, so QBR-time re-runs start from them instead of from scratch.
16. If you can browse the web, verify current marketplace fee rates and partner-type benchmark ranges before finalizing - fee schedules change (AWS restricted commit-retirement eligibility in May 2025). Otherwise flag every figure as user-supplied and unverified.

## Brainstorming the model

Run the exercise the way channel and alliance teams actually run it - collaboratively, through joint business planning, deal-desk review, and QBR economics reviews - never as a finance-silo calculation:

- Ask one question per message throughout; never batch questions.
- Treat the model as co-created where both sides can be convened: in joint business planning the vendor and partner build the plan together, and the partner owns its own P&L. A model the partner never saw predicts a partnership the partner never agreed to.
- Put the modeling approaches on the table ranked, state your recommendation and why, then wait. Rank by decision quality bought per analyst hour - the axes disagree, so read all four:
  - efficiency: vendor-side contribution > dual-sided P&L > marketplace-mechanics-first
  - value, meaning decisions it can settle: dual-sided P&L > vendor-side contribution > marketplace-mechanics-first
  - effort: dual-sided P&L > vendor-side contribution > marketplace-mechanics-first
  - compliance cost: marketplace-mechanics-first > dual-sided P&L > vendor-side contribution

| Approach                           | Settles                                                                                                     | Effort                                                                                                                                                                                               |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Vendor-side contribution - default | sign / don't sign, scale, prune, partner CAC against direct                                                 | About a week of one analyst on data you already hold - CRM attribution and finance. One finance reviewer, no partner disclosure. Fully reversible.                                                   |
| Dual-sided Bech-style P&L          | everything above, plus the split itself: renegotiation terms and the Third-Law check                        | A quarter. Needs the partner to disclose cost and services economics you cannot see, and coordination across both finance teams. Asking is itself a commitment signal - hard to walk back.           |
| Marketplace-mechanics-first        | only the routed-deal cost stack: listing fee, private-offer rate, commit-drawdown eligibility, win discount | An hour; the rates are published primary sources. Settles nothing alone - a required layer on top of one of the two above whenever deals route through a marketplace, never a substitute for either. |

- Compliance cost by approach, heaviest first:
  - Marketplace mechanics: eligibility is the platform's to change (AWS restricted commit retirement in May 2025), so re-verify a routed model's eligibility against current platform documentation rather than against any figure written down here.
  - Dual-sided P&L: a smaller version of the same exposure - asking a partner to open its cost base usually means a mutual NDA, puts another company's confidential numbers in your files, and signals a commitment you cannot un-signal.
  - Vendor-side model: touches nobody outside the company.
- Default to the vendor-side contribution model. Move up to dual-sided when any of these hold: the decision is the split rather than the signature, the partner is reseller-class and must own its own P&L (Bech), or partner disclosure is already on the table.
- The dual-sided P&L is what this efficiency order starves: it settles strictly more than the default and costs a quarter against a week, so the ratio demotes it in every engagement and renegotiations keep getting run on one side's numbers. Promote it whenever the question is how the value splits rather than whether to sign - the split cannot be argued honestly from the vendor's ledger alone.
- Delete rather than demote what this user's answers rule out, and say in the memo that it was deleted and why:
  - A partner that will not open its books removes the dual-sided rung entirely.
  - No assigned finance reviewer removes it too.
  - A deal that routes through no marketplace removes the marketplace-mechanics layer.
  - A rung carried to the bottom of the list comes back as scope at the next review, from someone who never heard the constraint.
- Re-rank against what you already know about this user before recommending: a finance reviewer already assigned collapses the dual-sided coordination cost, and an approved model from a past engagement makes extending it cheaper than any of the three. The ordering is a default, not a law - it shifts with the decision at stake and with who does the work.
- Name the assumptions out loud before computing: which volume number is partner enthusiasm, which benchmark is vendor-published, which cost is a guess.
- Argue the strongest case AGAINST the partnership before presenting the model; relationship investment and logo halo are the documented ways this exercise fools itself.
- Route non-standard terms through a deal-desk lens - written discount bands, exceptions justified in writing. A desk answering to the leader carrying the quarterly number approves what closes the quarter.
- For recurring reviews, insist both sides work off one shared scorecard read BEFORE the meeting. The two documented QBR failure modes: "status theater" - a meeting that ends with nobody owning a dated action - and "no shared data going in" - both sides arrive with different pipeline numbers and spend half the session arguing about whose spreadsheet is right.
- Secure CFO and CRO buy-in one-on-one before presenting the case to wider leadership.
- Present the deliverable one section at a time; validate each before drafting the next; gate finalization on the user's explicit approval.

## The Partner Economics Memo

Deliver the engagement as this artifact - the business case the user takes to their sign-off owner:

```
PARTNER ECONOMICS: <partner>, <date>
Decision        : sign / scale / renegotiate / prune, with the agreed go/no-go threshold
Partner type    : type + money-flow mechanics (fee %, discount, royalty, rev-share, CPA, marketplace)
Revenue model   : sourced and influenced projected separately: never one blended number
Cost stack      : discount | rebates/SPIFFs | MDF | marketplace fee | account mgmt | enablement | support | tooling
Net contribution: partner-adjusted gross margin and annual net contribution, by year across the ramp
Partner CAC     : fully loaded, vs direct CAC: attribution method stated
Ramp & payback  : time to first revenue, double-cost period, month cumulative contribution crosses zero
Incrementality  : share of attributed revenue that would have arrived anyway, and its evidence class
Partner's P&L   : the partner's own 3-5yr economics and the Third-Law check (when modeled dual-sided)
Sensitivity     : the 2-3 assumptions that move the verdict, and where each flips it
Verdict         : against the stated threshold: and what result would change it
Open questions  : missing data, unverified figures, and which finding would reverse the verdict
```

Three rules govern the memo:

- Every benchmark carries a source-quality label - peer-reviewed, analyst, industry survey, vendor benchmark, or untraceable.
- Every input traces to a named source or is marked "unverified, user-supplied" - never an invented number, and never a figure carried over from a worked example. If direct CAC, gross margin, or churn is still missing at step 5, stop and ask the user rather than reaching for the nearest number on the page.
- The open-questions section is mandatory: a model with no stated uncertainty has stopped asking.

## Pass Threshold

Ship nothing until all of these hold; iterate until they do:

1. **Partner acquisition cost per $1 of net revenue projected below the direct motion's**, fully loaded, on one stated convention. Per-customer CAC is not a valid comparison when a discount lowers revenue per partner deal. Otherwise the channel thesis is broken and the memo says so. Evidence class: practitioner consensus, anchored by the 2014 Pacific Crest/KeyBanc survey ($0.53 channel CAC per $1 of new ACV - the best-documented channel-CAC figure available, and already a ratio for this reason).
2. **Sourced and influenced never blended**, one partner credited per deal, influence capped so attributed revenue can never exceed total revenue.
3. **Cost-to-serve fully loaded.** The model survives the $2M-partner restatement: headline revenue re-expressed net of discount, MDF, account management, and training/support ($2M → $1.05M in the worked example).
4. **Lifetime value computed on gross margin**, never on revenue.
5. **Incrementality addressed explicitly**, never assumed at 100% - the cannibalization estimate and its evidence class appear in the memo.
6. **Sensitivity run and reported**; a verdict that survives only one assumption set is a bet, not a model.
7. **Every benchmark labeled** by evidence class; the untraceable famous figures (80/20 concentration, 11% incentive attainment, "most partners never transact") are flagged as untraceable or omitted.

## KPIs

Judge the economic decision itself, six to twelve months out - not the partner's ongoing performance, which belongs to `mbfinotti/partnerships-skills@partner-performance`:

- Realized partner CAC vs the modeled projection, and vs direct CAC over the same window.
- Actual cumulative net contribution vs the modeled ramp curve.
- Retention/NRR of partner-sourced customers vs direct-sourced - a gap beyond 10-15pp signals ICP misalignment (practitioner threshold; the SaaS Capital Aug 2019 survey found channel-majority companies run ~3pp lower retention).
- Time to first partner revenue vs the modeled ramp.
- Assumption audit: which modeled inputs proved wrong, by how much - the input to the next model.
- Verdict durability: did the sign/scale/prune call survive the first two quarterly reviews without reversing on facts the model should have caught?

## B2B and B2C

The method is identical on both sides - attributable revenue minus fully-loaded partner cost, against partner CAC, over a lifetime, adjusted for incrementality. Say so when asked; never reinvent it per side.

What genuinely differs - design for it:

| Dimension           | B2B channel/alliance                              | B2C affiliate/creator                                                  |
| ------------------- | ------------------------------------------------- | ---------------------------------------------------------------------- |
| Unit of analysis    | Partner firm - few, large                         | Creator/publisher - many, long tail                                    |
| Money flow          | Discount off list, rebates, MDF, marketplace fees | CPA or revenue share paid per action                                   |
| Ramp & enablement   | 6-12+ months double-cost, certification           | Near zero; instant activation                                          |
| Attribution         | Deal registration, CRM opportunity tagging        | Cookie/attribution window per action                                   |
| Concentration       | A handful of partners dominate                    | Power-law long tail of small earners                                   |
| Effective-rate trap | Margin stacking across tiers                      | Effective rev-share runs 20-40% below the stated rate after deductions |

Full sourced contrast: [references/b2b-vs-b2c-contrast.md](references/b2b-vs-b2c-contrast.md).

## Failure Modes

Work the table in row order - it is ranked by verdict distortion removed per hour spent, not by how often the failure occurs. The first five rows are re-runs of arithmetic and labeling you already hold, each able to reverse a verdict on its own within a working day. The rest are term-design and program-hygiene fixes measured in quarters: they change the next contract, not the number in this week's memo.

| Failure                                          | Fix                                                                                                                                 |
| ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------- |
| Double-counting influenced revenue               | Separate sourced/influenced; one partner per deal; cap influence at total revenue                                                   |
| Ignoring cost to serve                           | Fully-loaded stack; run the $2M → $1.05M restatement on every headline number                                                       |
| Counting cannibalized revenue as incremental     | Model incrementality explicitly; segmentation and rules of engagement, not hope                                                     |
| Misattributed partner CAC                        | If partner CAC exceeds direct, check in this order - double-counted influence, then commission against deal size, then lead quality |
| Quoting an untraceable benchmark as fact         | Label the evidence class; prefer named-source figures; write "unverified" over inventing                                            |
| Margin stacking collapse across tiers            | Model the full stack (Spengler); consider a two-part tariff shape for the terms                                                     |
| Over-discounting to win the partner              | Model the win discount together with the marketplace fee - the discount frequently dwarfs a 3% listing fee                          |
| Marketplace commit-drawdown surprises            | Model commit-retirement mechanics and eligibility rules, not just the listing fee                                                   |
| MDF that never converts                          | Tie MDF to documented plan commitments; model utilization, not allocation                                                           |
| Sunk-cost persistence and the long-tail illusion | 100 signed partners with 12 active is a 12-partner channel; prune on net contribution, not tenure                                   |

## Invocation Examples

- "Model the economics of a proposed reseller before we sign - 30% effective discount, $40K ACV, they project 14 deals in year two."
- "Is this marketplace partner worth keeping? Two years in, decent attributed revenue, and I suspect most of it is not incremental."
- "Build both sides of the P&L for an MSP alliance - ours and theirs - so we can renegotiate the split with real numbers."

## Reference

- `mbfinotti/partnerships-skills@alliance-prioritization` - ranks a portfolio of candidate alliances; hands single-partner P&L modeling to this skill.
- `mbfinotti/partnerships-skills@partner-channel-program` - sets the program-wide economics envelope this single-partner model must live within.
- `mbfinotti/partnerships-skills@partner-tiering` - tier criteria and benefits inside an existing program.
- `mbfinotti/partnerships-skills@partner-performance` - ongoing scorecards and QBR performance review once the model is approved.
- `mbfinotti/partnerships-skills@affiliate-commission-structure` - designs affiliate payout tiers for professional affiliates; a different discipline from single-partner modeling.
