---
name: partner-marketplace-strategy
description: Decide which third-party marketplaces to list on, how much to invest in each, what ROI to expect, and when to delist  - marketplace prioritization for partner teams. Covers cloud marketplace listing strategy, SaaS app store and integration directory prioritization, and retail marketplace selection for ecommerce (1P vs 3P vs hybrid), with a readiness gate, weighted scorecard, and provenance-flagged ROI expectations. Use whenever the user mentions AWS, Azure or GCP marketplaces, an app store listing, an integration directory, or asks whether a marketplace listing is worth it, even if they never say marketplace strategy. Do NOT use for choosing which partner category to launch next  - use mbfinotti/partnerships-skills@partner-ecosystem-expansion instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.0.3"
---

# Partner Marketplace Strategy

Set the strategy for listing on third-party marketplaces: which ones, how deep, in what order, with what investment, and the condition that ends it. The working method assembles:

- The list → transact → co-sell → scale capability ladder (broad B2B practitioner consensus).
- Tackle's Cloud GTM Maturity Model (vendor-authored, it sells stage-by-stage tooling).
- McFadyen Digital's Marketplace Maturity Model (consultancy-authored, B2C).
- For reading the vendor landscape: the Canalys Global Co-Sell Software Leadership Matrix, IDC MarketScape marketplace assessments, and Gartner's PERM market guide (independent analyst), plus Jay McBain's ecosystem work as the most credible individual voice.

No framework in this field has independent longitudinal validation. Every staged model is authored by a party selling the journey: use them as structure, not as evidence.

The output is a decision artifact an executive funds: the Marketplace Strategy memo, never execution work.

- Listing-form content, store optimization, and ad tactics belong elsewhere.
- Per-partner economics, named-alliance ranking, and joint GTM plans hand off to sibling skills (see Reference).

## Interview

Ask before strategizing. Ask one question per message, and offer multiple-choice answers when possible. Skip a question only when the user already gave the answer.

- B2B software, consumer brand, or hybrid?
- Product type and deployment model: SaaS, self-hosted/installable image, physical goods, services?
- Price band: typical ACV or order value, and gross margin? How much margin can a platform take rate consume?
- Which channels sell today, and does the direct motion already work repeatably? What is the evidence?
- Where does target buyers' procurement already sit: committed cloud spend (and with which provider), a dominant retail platform, or neither?
- Do buyers purchase through a marketplace today? Any committed-spend contracts among target accounts?
- Who owns this decision, and who must approve it (revenue, finance, product - or ecommerce, marketing, finance)?
- B2B: how is a marketplace-routed deal treated in sales compensation today - neutral, penalized, or undefined?
- Operational capacity: metering/entitlement engineering, deal desk, tax/legal for B2B, or inventory, fulfilment, returns, retail-media budget for B2C?
- What does success mean, in which metric, and by what date must the result land?
- Is this a one-off revenue win this period, or a compounding procurement asset that pays over years?
- What is the effort ceiling: engineering weeks available, deal-desk or fulfilment headcount, political capital for a comp-plan change, and how reversible the commitment must be?

The last three answers re-rank every option menu in this skill. Say out loud which answer moved which option:

- A hard near-term date promotes list-only and 3P, and demotes anything needing a build.
- A compounding mandate promotes the private-offer and deep-platform-bet rungs.
- A low effort ceiling deletes the channel/multiparty and hybrid rungs from the memo outright, rather than parking them at the bottom.

## Workflow

Hold three disciplines across every step:

- **Present options, then wait.** Wherever a real choice exists (which platform first, scorecard weights, depth of participation, 1P vs 3P, the delist condition), present 2-3 candidate approaches with trade-offs and a recommendation, then wait. Never present one option as the only one.
- **Flag provenance on every benchmark quoted.** Nearly all published marketplace ROI figures come from parties that profit when the number looks good: platform-commissioned studies, GTM-tooling vendors, agencies. Label each as operator-published, vendor, commissioned study, analyst, or agency, and treat precision as marketing.
- **Re-rank against the user.** Every ordering in this skill and its references is a default, not a law: it shifts with context and with who executes it. Say which fact moved which option, e.g. an existing metering and entitlement system deletes most of the transactable rung's cost, a committed-spend customer already asking to buy through the marketplace promotes the private-offer rung above everything else, and no deal desk at all demotes it below a rung the team can actually run.

Work in the profession's own collaborative formats, not generic brainstorming:

- B2B: business-case templates and stage-gate readiness reviews, QBRs with the marketplace/platform team, comp-neutrality policy drafted before the quarter, account mapping as the shared data layer.
- B2C: channel P&L models, written go/no-go criteria, pre-launch readiness checklists, weekly pacing reviews, and 90-day retros.

1. Run the Interview. Confirm scope is one business area with a stated goal before evaluating anything.
2. Apply the readiness gate. It is allowed to answer "not yet". Disqualifiers:
   - Direct motion not yet repeatable: a marketplace amplifies a working motion; it does not create one.
   - Margin that cannot absorb the take rate plus cost-to-serve. Resolve the deployment model first, because the take rate follows it: 3% for a SaaS listing but 20% for a server/AMI/container/ML image on AWS Marketplace, a gap that decides this gate on its own.
   - No named owner or executive sponsor.
   - Missing operational capacity with no budget to build it.

   If disqualified, say so, name what must change, and stop.

3. Run the demand-vs-procurement diagnosis and write the answer down. A marketplace is primarily a transaction and procurement rail, not a demand-generation channel: "list and pray" is the most-cited failure in both B2B and B2C.

   State explicitly what this listing is being asked to do:
   - Unlock committed-spend budgets and shorten procurement.
   - Capture demand that genuinely searches there.

   If the plan assumes demand the platform will not supply, the plan funds demand generation or does not proceed.

4. Inventory candidate marketplaces by category (hyperscaler/cloud, SaaS app store, integration directory, retail marketplace, regional champion), anchored on where the Interview says buyer procurement and traffic already sit. Evaluate in default efficiency order: value returned per unit of effort, where effort is engineering weeks, deal-desk rework and reversibility, never a fee. No order spans both sides:
   - B2B: `hyperscaler cloud > integration directory > SaaS app store`
   - B2C: `dominant retail marketplace > regional champion`

   If you can browse the web, extend the inventory from competitor listings, platform partner directories, and category neighbors. See [references/marketplace-taxonomy.md](references/marketplace-taxonomy.md) for the per-axis orderings and what each order starves.

5. Screen hard gates before scoring: scope violations, platform terms the business cannot accept, missing prerequisites. Mark unresolved compliance or fee questions "hold for verification". Never convert an unknown into a rejection or an acceptance.
6. Score survivors on the weighted prioritization scorecard: propose weights, agree them with the user before scoring, leave unsupported dimensions unscored rather than invent precision. Then apply the second-pass impact × effort filter on a provisional impact estimate - the ROI model is not built until step 11, so label the axis "provisional" and leave a candidate unplotted rather than inventing an impact number. Give each candidate a four-way outcome - pilot, prepare, hold for verification, do not prioritize - not a binary go/no-go. See [references/prioritization-scorecard.md](references/prioritization-scorecard.md).
7. Verify the economics of every ranked candidate.
   - If you can browse the web, read the operator's own published schedule and date it.
   - Otherwise, ask the user for it, and mark anything they cannot supply "unverified" rather than assuming a rate.

   Where the operator publishes no rate card at all, record that as a finding: the fee is a negotiation input, not a constant. Stress-test the business case against announced future rates and post-subsidy rates, not just today's. See [references/marketplace-economics.md](references/marketplace-economics.md).

8. Decide depth of participation per prioritized marketplace. Each rung has its own cost and capability gate, so rank by value per unit of effort rather than by rung order:
   - B2B cloud: `private offer > transactable > list-only > channel offer`
   - SaaS app store: `transactable paid app > free listing > deep platform bet`
   - Retail: `3P > 1P > hybrid`

   The cloud rungs are cumulative: aim the business case at the private-offer rung and treat transactable as the toll to reach it, because a case that stops at transactable pays nearly the whole cost for the smaller half of the value. Delete every rung the user's effort ceiling rules out from the memo, and name which. Never park it at the bottom. See [references/marketplace-taxonomy.md](references/marketplace-taxonomy.md) for the per-axis orderings, the ties, and what each order starves.

9. Sequence: one platform first, prove the motion, then expand. Define the gate that unlocks each stage - e.g. first transactions closed (renewals are the documented low-risk proof path in B2B), comp policy in writing, contribution margin positive - and the evidence each gate requires.
10. Set the investment envelope: platform fees, the real cost-to-serve, and a named owner's time.
    - B2B cost-to-serve: integration/metering engineering, deal desk, legal/tax setup.
    - B2C cost-to-serve: fulfilment, returns reserves, effectively-mandatory retail media.

    A listing without an owner and an envelope is visibility, not pipeline.

11. Build the ROI expectation and its measurement plan:
    - Baseline before listing.
    - Sourced vs. influenced definitions agreed with finance.
    - Net-new vs. relocated revenue, separated.
    - KPIs per side.

    Use published benchmarks only as provenance-flagged ceilings, never as the base case. Then re-run step 6's impact × effort filter against the finished model, and record every candidate whose quadrant moved. That shift is a finding, not a correction to bury. See [references/roi-and-kpis.md](references/roi-and-kpis.md).

12. Write the delist/deprioritize trigger now, before launch: the condition and review date that ends or downgrades a listing (e.g. ops cost with no transactions after an agreed number of quarters of genuine effort, or contribution margin negative after ads and returns). A trigger decided up front survives sunk-cost pressure. One decided later rarely fires.
13. Present the memo section by section, in the order shown below, and validate each section with the user before drafting the next. Require explicit approval on every section before finalizing.
14. Check the finished memo against the Pass Threshold, and iterate until it passes. If no candidate passes, recommend not listing and record why: that is a valid, fundable outcome.
15. If your harness has persistent memory, memorize the approved decisions (ranked marketplaces, weights, depth choices, envelope, gates, delist trigger) so later runs start from them instead of re-interviewing.

## The Marketplace Strategy Memo

Deliver every engagement as this decision record:

```
MARKETPLACE STRATEGY  - <company / business area>, <date>
Scope          : product line, ICP, geography; B2B, B2C, or hybrid; what was excluded
Diagnosis      : demand vs procurement  - what each listing is being asked to do
Candidates     : marketplaces evaluated, hard-gate screen results, holds for verification
Prioritization : scorecard result with weights shown; second-pass filter; four-way
                 outcome per candidate (pilot / prepare / hold / do not prioritize)
Depth          : per marketplace  - list-only / transactable / private offer / channel
                 offer (B2B) or 1P / 3P / hybrid (B2C); the rung funded, the reason,
                 and the rungs deleted because the effort ceiling rules them out
Economics      : take rate per ranked marketplace with source and date ("unverified"
                 stated where it is); envelope vs gross margin; comp treatment (B2B)
                 or contribution margin after ads/returns/fulfilment (B2C), in writing
Staged plan    : one platform first; the gate and evidence that unlock each stage
ROI expectation: expected range and payback horizon; provenance flag on every
                 benchmark used to build it
Delist trigger : the condition and date that deprioritizes or removes each listing
Owner          : named owner, approvers, review date
Open questions : what could not be verified, and what would verify it
```

Every line carries a reason a reviewer can check. The open-questions section is mandatory: a memo with no stated uncertainty stopped asking.

## Pass Threshold

The memo is done when all of these hold. Iterate until they do:

- **Every ranked marketplace has a take rate with a named source and date**: the operator's own published schedule where one exists, explicitly "unverified" where not. No silently assumed fees.
- **The business case survives the operator's announced future rate and post-subsidy rate**, not just today's schedule.
- **A named owner and approver exist**: "listed but no one owns the results" is the field's most common quiet failure.
- **Comp treatment (B2B) or contribution margin after ads, returns, and fulfilment (B2C) is decided in writing** before launch.
- **Every benchmark carries a provenance flag** (operator, vendor, commissioned study, analyst, agency).
- **A delist trigger with a review date exists**, written at approval time.
- **The demand-vs-procurement diagnosis is answered explicitly** in the memo.

## B2B and B2C

The decision logic is genuinely identical on five points. Say so instead of reinventing the method per side:

- The marketplace is a transaction mechanism, not a lead source ("list and pray" fails in both).
- Channel conflict is a first-class design problem (comp neutrality in B2B, MAP policy and the 1P/3P firewall in B2C).
- Sequence one platform, prove it, then expand, gating expansion on operational readiness.
- Measure influenced revenue as well as sourced revenue.
- Watch concentration risk and net-new vs. relocated revenue.

What genuinely differs:

| Dimension                 | B2B software / cloud                                                                                                                                               | B2C / retail                                                     |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------- |
| Decision owner            | Alliances / cloud GTM lead, chief partner or ecosystem officer                                                                                                     | Head/VP of Ecommerce, marketplace manager                        |
| Approvers                 | CRO + CFO + product                                                                                                                                                | VP Ecommerce / CMO + finance                                     |
| Core buying driver        | Committed-spend drawdown + co-sell access                                                                                                                          | Consumer demand, search ranking, fulfilment promise              |
| Platform take             | Deployment-dependent, not a constant: 3% for SaaS but 20% for server/AMI/container/ML images on the largest cloud marketplace; falls with deal size and on renewal | 6-45% by category, plus fulfilment and ads                       |
| Primary success variable  | Sales-comp neutrality                                                                                                                                              | Contribution margin after ads/returns/fulfilment                 |
| The marketplace really is | A procurement rail on an existing sales motion                                                                                                                     | A net-new operating business (listings, inventory, ads, returns) |

## Failure Modes

| Failure                                                                                 | Fix                                                                               |
| --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------- |
| List and pray - listing treated as a demand channel                                     | Demand-vs-procurement diagnosis in writing; fund demand separately or do not list |
| Comp plan penalizes marketplace deals; reps route around it (B2B)                       | Comp-neutrality policy written before the quarter, in the memo                    |
| Listed, but no one owns the results                                                     | Named owner and envelope in the memo; no owner means no listing                   |
| Business case built on today's take rate or an introductory 0% band                     | Stress-test announced future rates and post-subsidy rates                         |
| Hidden cost-to-serve breaks the case late (metering, tax, deal desk; VAT, returns, ads) | Full cost-to-serve inside the envelope before approval                            |
| 1P/3P self-competition or price erosion on the same product (B2C)                       | Firewall and pricing policy decided before going hybrid                           |
| Relocated revenue counted as marketplace ROI                                            | Baseline before listing; separate net-new from shifted                            |
| Second platform added before the first proves                                           | Stage gates with evidence; renewals-first proof on platform one                   |
| Delist decision deferred until sunk cost dominates                                      | Trigger and date written at approval time                                         |

## Invocation Examples

- "Should we list on a cloud marketplace? We sell a self-hosted container image at $40K ACV, sales-led, direct motion works."
- "We are listed on three marketplaces and none of them transact. Tell me which to keep, which to deprioritize, and what the delist trigger should be."
- "Build the business case for a transactable listing, including the take rate and the real cost-to-serve."

## Reference

- [references/marketplace-taxonomy.md](references/marketplace-taxonomy.md) - marketplace categories and depth-of-participation ladders, each ranked by value per unit of effort, with the per-axis orderings and what each order starves.
- [references/prioritization-scorecard.md](references/prioritization-scorecard.md) - hard-gate screen, weighted scorecard mechanics with a worked example, second-pass filter, four-way outcome gates.
- [references/marketplace-economics.md](references/marketplace-economics.md) - verified take rates with dates and sources, fee-structure strategic reads, committed-spend drawdown, total cost-to-serve.
- [references/roi-and-kpis.md](references/roi-and-kpis.md) - KPI sets per side, published benchmarks with provenance flags, building a defensible ROI expectation.

Sibling skills (same collection):

- `mbfinotti/partnerships-skills@partner-ecosystem-expansion` - adding new partner categories beyond marketplaces; use for scope decisions about non-marketplace channels.
- `mbfinotti/partnerships-skills@co-selling-strategy` - the co-sell motion a transactable cloud listing unlocks.
- `mbfinotti/partnerships-skills@joint-gtm-planning` - the joint motion with one named partner or platform after this strategy picks it.
- `mbfinotti/partnerships-skills@partner-channel-conflict` - rules of engagement for the conflict zones a marketplace creates.
- `mbfinotti/partnerships-skills@partner-performance` - ongoing scorecards and review cadence once listings run.
- `mbfinotti/partnerships-skills@partner-economics` - unit economics of one partner relationship, including one platform relationship.
