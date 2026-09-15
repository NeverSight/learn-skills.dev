---
name: co-selling-strategy
description: Design the operating model for how direct sales and partner sellers collaborate on shared deals - deal registration policy (protection windows, approval SLA, rejection grounds), deal credit and attribution split (partner-sourced vs partner-influenced, comp neutrality), and channel rules of engagement between direct and partner sellers. Covers B2B co-sell motions at the policy level. Use whenever the user mentions co-selling, partner deal registration, deal credit splits, partner attribution policy, or reps and partners working the same account, even if they never say co-sell. Do NOT use for adjudicating a live contested deal - use mbfinotti/partnerships-skills@partner-channel-conflict instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.3.4"
---

# Co-Selling Strategy

Define how direct sales and partner sellers collaborate on shared deals: the policy layer, never the deal-by-deal execution. This skill designs three artifacts as one coherent operating charter, and validates it with the user section by section:

- **Deal registration policy** - how a partner formally claims an opportunity and what that claim grants.
- **Credit and attribution model** - who gets counted and paid when a deal has more than one parent.
- **Rules of engagement** - between direct and partner sellers.

Co-selling is a B2B discipline with no true B2C analogue. It presupposes named accounts, quota-carrying reps, a consultative sales cycle, and an opportunity record - none of which exist in a consumer transaction.

The consumer-side counterparts are trade marketing, co-op advertising funds, and shelf-placement/channel agreements: a different discipline with different mechanics, so never force-fit deal registration or comp neutrality onto retail partnerships. The one part that transfers to any context, B2B or B2C, is the governance discipline itself: unambiguous ownership rules, documented tiebreakers, published criteria.

## Interview

Ask before proposing anything. One question per message; offer multiple-choice options when possible. Skip anything the user already answered. If your harness has persistent memory, check it for a previously approved charter first and confirm what changed instead of re-interviewing.

- What does the direct sales org look like - segments covered (SMB / mid-market / enterprise), inside vs field, how quota is structured?
- Which partner types are in play or planned: referral, reseller/VAR, distributor, SI/consultancy, ISV/tech, marketplace/hyperscaler?
- What are ACV, average sales-cycle length, and direct win rate? (Cycle length sets the registration protection window.)
- When did an AE last close a co-sell deal and call it a good experience - and what made it good?
- Does the current comp plan create any friction against attaching a partner to a deal?
- How does an AE find out which partner to call for a specific account today, and how long does that take?
- If an AE decided to ignore the partner motion entirely, what would happen?
- What is the goal: partner-sourced pipeline, influenced revenue, marketplace transaction volume, reaching segments direct can't?
- Is there a working attribution record today - timestamped registrations, or credit claims made at close?

Ask these three last, always. Every ranked menu later in this skill is re-ordered against the answers, and by the time the reader reaches a menu they have already committed to a path.

- By what date must this motion show a result, and what has to be true by then? A date inside one quarter deletes the heavyweight JBP track and promotes the one-hour registration and lock-window fixes. A date beyond two quarters keeps comp-plan work in play.
- One-off unblock, or a compounding asset? One-off promotes registration policy and rules of engagement, which pay out on the next deal. Compounding promotes comp neutrality and attribution co-ownership, which pay back every quarter and almost nothing in the first one.
- What is the effort ceiling - hours available, whether sales leadership will reopen the comp plan at all, and how reversible the change has to be? A refusal to reopen comp deletes every comp funding rung outright. A demand for reversibility demotes anything published to partners, since a granted discount is far harder to withdraw than an internal rule.

## Workflow

1. Run the Interview. If you can browse the web and the user has a published partner or deal-registration page, read it - audit reality before designing on a blank page.
2. Gate on readiness before designing anything. Decline, with reasons, when any disqualifier holds:
   - The ICP can't be clearly articulated yet.
   - Direct sales hasn't proven it closes reliably on its own.
   - Positioning, pricing, or process is still shifting.
   - ACV sits below roughly $3-5k, the practitioner floor for any sales-assisted motion (general SaaS consensus, not a co-sell-specific study).
   - Partnerships are being reached for as a fix for a growth problem.

   Partners amplify a working direct motion. They do not fix a broken one. When the gate fails, recommend two or three deeply engaged referral partners with no formal program, and stop.

   See [references/partner-types-and-process-tracks.md](references/partner-types-and-process-tracks.md) for deeper diagnostic questions for this gate.

3. Pick the process track. Present both in ranked order with the trade-off in each, and recommend explicitly. The axes disagree:
   - efficiency: `lightweight playbook > heavyweight JBP`
   - value: `heavyweight JBP > lightweight playbook`
   - effort: `heavyweight JBP > lightweight playbook`

   **Lightweight playbook fill:** one fixed template filled per partner in a single 90-minute session. Buys a named owner per cell and a shared deal-stage map, the two things most disputes actually turn on, for one session per partner plus a one-time template. Best ratio, and the default for every partner until something moves it.

   **Heavyweight joint business planning:** exec kickoff on both sides, shared measurable objectives, multi-week drafting, formal sign-off, quarterly reviews. Buys two-sided executive sponsorship and a budgeted plan, the only lever that moves a partner whose own field sellers carry quota, for weeks of drafting, a two-sided sign-off chain, and a standing quarterly review job. Highest value, worst ratio - move up to it only for a partner whose sellers you need to influence directly and where both sides will fund the review cadence.

   Delete the JBP track from the menu, rather than recommending against it, when the partner side will not name an executive sponsor: an unsponsored joint plan produces a document nobody executes. Run lightweight and revisit when a sponsor exists.

   Read [references/partner-types-and-process-tracks.md](references/partner-types-and-process-tracks.md) before this step - the ordering above is a default that shifts with partner type, ACV, and who on the user's side actually runs the session.

4. Map each partner type in play to the registration and credit mechanic its economics actually require (same reference):
   - A referral partner needs clean attribution, not margin protection.
   - A reseller needs formal registration.
   - An SI is motivated by services pipeline.
   - An ISV/tech partner needs none of the resale mechanics.

   Never ship one undifferentiated policy across types.

5. Design the five policy decisions in order, one at a time. For each decision:
   - Present 2-3 candidate approaches ranked by value per unit of effort, never cheapest-first.
   - Fold each option's trade-off into its own line and state an explicit recommendation.
   - Get the user's call before moving on.
   - Say the ordering out loud with a `>` line, and emit a separate line per axis wherever cost, value, effort and efficiency disagree.
   - Express effort as hours, meetings, sign-off chains and reversibility, never as a currency amount.
   - Drop any option the user's answers to the last three interview questions rule out, instead of demoting it, and say which answer deleted it.

   Every ordering here is a default: re-rank it against what you already know about this user before presenting it.
   1. **Attribution taxonomy** - partner-sourced vs partner-influenced, and whether to also publish a combined "partner-attached" number. See [references/attribution-and-compensation.md](references/attribution-and-compensation.md).
   2. **Deal registration policy** - what a registration grants, protection window and extension rules, approval criteria and SLA, published rejection grounds. See [references/deal-registration-policy.md](references/deal-registration-policy.md).
   3. **Credit and compensation** - the comp-neutrality funding model and the multi-party split rule. Same attribution reference.
   4. **Rules of engagement** - account classes (direct-only / partner-only / shared-pursuit), co-sell trigger conditions, named-account exceptions, escalation ladder. See the registration reference.
   5. **Decision rights** - who approves registrations (never a role whose quota the decision affects), who co-owns attribution (partnerships plus revenue operations is the defensible default), who adjudicates disputes and under what SLA, and who owns the rules-of-engagement document. Practitioner convention puts this with partner or ecosystem leadership, co-designed with sales, CS, RevOps, and legal, but it is one consultancy's stated pattern rather than a measured norm - name it as a starting point and make the user confirm it for their own org rather than asserting it as settled.

6. Assemble the charter (next section) and present it section by section, validating each with the user before the next. Do not finalize without explicit approval of the whole document.
7. Score the approved draft against the pass checklist below. State which checks fail and iterate until every one passes.
8. If your harness has persistent memory, memorize the approved charter's decisions - later runs (KPI reviews, adding a partner type, revisiting a window) start from them instead of re-interviewing.
9. Hand off what this skill does not do - resolving a live contested deal, planning a launch with one partner, program tiers and economics - to the sibling skills in Reference.

## The Co-Sell Operating Charter

Deliver every engagement as this artifact - a decision record the user can hand to sales leadership, finance, and partner operations:

```
CO-SELL OPERATING CHARTER - <company>, <date>
Scope            : partner types covered, segments, account classes (direct-only / partner-only / shared-pursuit)
Process track    : lightweight playbook-fill by default, heavyweight JBP by exception, per partner type
Attribution      : taxonomy adopted, the sourced test used, lock window after deal creation
Registration     : what it grants, protection window + extension rule, approval criteria, SLA, published rejection grounds
Credit & comp    : neutrality model + how it is funded, quota-retirement rule, multi-party split rule
Decision rights  : registration approver, attribution co-owners, dispute adjudicator + SLA, rules-of-engagement doc owner
Engagement rules : co-sell trigger conditions, named-account exceptions, escalation ladder
KPIs & review    : metrics tracked, targets, review cadence
```

Every line carries a reason: "90-day window because the average cycle is 100 days" is reviewable. A bare number is not.

**Pass checklist** - the charter is not done until every check passes. State the failing checks and the gap each time:

- Every decision-rights line names a specific role and, wherever possible, an individual. Shared ownership is no ownership.
- The registration approver's own quota is unaffected by approval decisions.
- The protection window is at least 75% of the average sales-cycle length the user reported.
- Rejection grounds are published, explicit, and a closed list - every ground objectively verifiable from the registration record, none discretionary. Take the canonical set from `mbfinotti/partnerships-skills@partner-channel-conflict`, which owns it. Enumerate rather than trimming, because a ground left off the list is a rejection nobody can defend.
- The comp model carries sign-off from finance and sales leadership, or the deviation is recorded as a deliberate exception with its risk stated.
- An AE can tell from one read whether a concrete deal is registerable, protected, and comp-neutral - walk one real deal scenario through the rules with the user to test this.
- Direct reps see registrations inside the system they already work in. A policy whose records live only in a portal the sales team never opens fails by definition.

## Established practice vs vendor vocabulary

Grade what you cite honestly - the co-sell literature mixes real standards with vendor marketing:

- **Established, safe to present prescriptively:** the partner-sourced / partner-influenced / partner-attached taxonomy, comp neutrality, rules-of-engagement documents, and deal registration with protection windows.
- **Real but vendor-originated vocabulary:** "ecosystem-led growth" and "nearbound" - widely adopted terms, but coined by vendors; use them as shared vocabulary, never as doctrine.
- **No standard exists:** co-sell readiness and maturity models are competing consultant frameworks. Present them as a category of options, not as a canonical model.
- **Directional at best:** the headline partner-lift benchmarks (bigger deals, higher win rates, faster cycles) trace to vendor marketing, not independent research. Quote them only with that flag attached.

## Diagnosing an existing motion

When the user arrives with a running co-sell motion instead of a blank page, work the fixes in the order below - highest value per unit of effort first, not cheapest first. The axes disagree, so state both when presenting the plan:

- efficiency: `published rejection grounds == lock window + dispute SLA > registration visibility > tiebreaker ladder > attribution co-ownership > comp neutrality`
- value: `comp neutrality > registration visibility > published rejection grounds > lock window + dispute SLA > attribution co-ownership > tiebreaker ladder`

The tie at the front is earned, not a hedge: both are one published paragraph, drafted in about an hour, signed off inside partnerships alone, and each kills a distinct high-frequency symptom.

Comp neutrality is what this order starves. It is the highest-value fix on the page and still ranks last on ratio, because it is a contractual commitment to the field costing a quarter and a finance-plus-CRO sign-off chain. A reader who only follows the efficiency line works the cheap rungs forever and never buys the one fix the others cannot substitute for.

Promote it to first on one symptom: reps still routing around or sandbagging partner deals after registration visibility, rejection grounds and the lock window are all in place. Where interview question 3 said sales leadership will not reopen the comp plan, comp neutrality is deleted from this plan and recorded as a known risk - never left at the bottom of the list, where it reappears as scope nobody can sign. Re-rank the rest against the user's own situation - a team whose rejection grounds are already published starts at the second rung.

| Symptom                                                                 | Check first                                                                            | Policy at fault                         | Fix effort                                                    |
| ----------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | --------------------------------------- | ------------------------------------------------------------- |
| Flood of speculative registrations on accounts the partner barely knows | Are proof-of-involvement criteria and rejection grounds published?                     | Registration - approval criteria        | An hour, partnerships alone                                   |
| Reps spend selling time arguing credit splits                           | Attribution lock window and dispute SLA                                                | Attribution governance                  | An hour, partnerships alone                                   |
| Direct AEs blindsided by partner registrations                          | Where the registration record lives - portal only, or the sales system?                | Rules of engagement - visibility        | A week of RevOps config                                       |
| Two claimants on one account, no clean resolution                       | Timestamped system of record and tiebreaker rules                                      | Decision rights - escalation ladder     | A week, plus tooling that may not exist                       |
| Partner-influenced revenue reported but nobody trusts it                | Are claims accepted at close, with partnerships as sole owner of the number?           | Attribution - taxonomy and co-ownership | A quarter of process change across two teams                  |
| Reps quietly avoid or sandbag partner deals                             | Does quota credit shrink when a partner attaches, or a marketplace fee hit commission? | Credit & comp - neutrality              | A quarter, finance + CRO sign-off, contractual once published |

## KPIs

Track sourced and influenced separately: collapsing them hides whether partners generate pipeline or accelerate it. Core KPIs:

- Partner-sourced pipeline share.
- Partner-influenced revenue share.
- Attach rate.
- Registration time-to-approval.
- Dispute rate.
- Adjudication-SLA compliance.

Compare win rate and cycle length for partner-attached vs direct deals inside the user's own data only, since cross-company benchmarks are unreliable: opportunity-creation criteria differ by company, and no independent industry benchmark exists for registration approval rate or time-to-approval. Review quarterly. A program where one partner drives more than ~30% of channel revenue carries concentration risk worth flagging.

The few published benchmark numbers that exist are vendor-sourced and directional only. They live, with their flags, in [references/attribution-and-compensation.md](references/attribution-and-compensation.md).

## Invocation Examples

- "Write the co-sell operating charter for our reseller and SI partners - mid-market, 100-day average sales cycle, comp treatment currently undefined."
- "Our AEs do not know when a partner-registered deal is protected. Draft the deal-registration policy and walk one real deal through it."
- "Partnerships and RevOps disagree about who owns attribution on partner-influenced deals. Write the decision-rights section."

## Reference

- See [references/deal-registration-policy.md](references/deal-registration-policy.md) for protection-window ranges, approval SLA and separation-of-powers rules, rejection grounds, escalation ladders, and rules-of-engagement document sections.
- See [references/attribution-and-compensation.md](references/attribution-and-compensation.md) for the attribution taxonomy, governance and lock windows, the three comp-neutrality funding models, and sign-off requirements.
- See [references/partner-types-and-process-tracks.md](references/partner-types-and-process-tracks.md) for the partner-type-to-mechanic map, ACV bands, the two process tracks, and partner discovery-session mechanics.
- See [references/charter-examples.md](references/charter-examples.md) for one worked charter and one annotated negative example.
- See `mbfinotti/partnerships-skills@partner-channel-conflict` for the contested-deal layer: protection-window sizing, the tie-break, the rejection-grounds list, the escalation and adjudication ladder, and the comp-neutrality decision. Both skills write rules, and they write different ones - this skill owns the cooperative layer (what a registration grants, approval SLA and separation of powers, attribution, the co-sell charter), and consumes that skill's numbers rather than restating them.
- See `mbfinotti/partnerships-skills@joint-gtm-planning` for the go-to-market motion with one specific partner (co-marketing, launch sequencing).
- See `mbfinotti/partnerships-skills@partner-channel-program` for overall program structure - tiers, requirements, benefits.
