---
name: negotiation-concession-planner
description: Builds a pre-negotiation concession plan for a pricing or contract conversation - every tradeable lever priced by cost-to-us vs value-to-them, tiered, each give paired with a required reciprocal get and its approval level, plus a BATNA-based walk-away. Covers B2B (terms, scope, service, risk, price protection) and B2C (bundles, financing, trade allowance). Use whenever the user mentions a discount request, procurement, redlines, give-get trades, walk-away point, or "the buyer wants 20% off", even without the word negotiation. Do NOT use for quantifying the value (mbfinotti/sales-skills@deal-value-calc) or scripting price rebuttals (mbfinotti/sales-skills@sales-objection-handling).
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.4.8"
---

# Concession Planner

Produce a pre-call concession plan: a tiered ledger of what the seller can trade, priced by cost-to-us vs value-to-them, every give paired with a required reciprocal get and the approval level it needs, bounded by a written walk-away line.

A concession plan is a preparation artifact, not an in-call improvisation. Mid-negotiation, emotional engagement degrades judgment of relative value - so the gives, the gets, the prices, and the limits get written before the conversation starts.

## Interview

Ask before planning. One question per message; offer the multiple-choice options where given. Skip anything already answered by prior context.

1. What are you selling, and at what price point is the deal on the table?
2. Is this B2B or B2C, and which segment: (a) enterprise, (b) SMB / mid-market, (c) consumer?
3. Who is the counterpart: (a) the decision maker, (b) procurement / purchasing, (c) a champion or influencer without final authority, (d) unknown?
4. What has the buyer actually asked for so far: (a) a price discount, (b) better terms - payment, contract length, risk, (c) more scope for the same price, (d) nothing yet, but you expect pushback?
5. What is your discount authority band, and who approves beyond it? Treat the existing approval matrix as an input - this skill never designs it.
6. Which non-price levers can you move: term length, payment timing, scope or volume, service level, risk terms (uptime, credits, liability), price protection, bundled goods?
7. What do you want in return: (a) references, case study, or logo rights, (b) prepay or multi-year, (c) a faster signature date, (d) referrals or introductions, (e) larger scope?
8. What is your walk-away alternative if no deal happens - the next-best use of the same time, capacity, or inventory?
9. By what date must this land, and whose date is it: (a) theirs, (b) yours, including your own quarter-end, (c) neither's?
10. Do you want a one-off win here, or a position that holds? A concession granted once tends to be expected forever - every renewal starts from it, and your other buyers hear about it. (a) close this one at almost any structure, (b) protect the baseline for the renewal and the deals after it.
11. What is your effort ceiling: delivery capacity you can actually commit, approvals you can realistically get in the time available (deal desk, finance, legal), and how much of this you can take back later?

Re-rank the inventory against those three answers before building the ledger, and say which answer moved what:

- A hard, near date promotes the fast-acting levers - cash timing, service access, a delivery commitment - and demotes multi-year structures that need approvals you cannot collect in time.
- A "protect the baseline" answer demotes the headline discount and every price-protection lever, since both are permanent by construction. "Close it now" is the only answer that promotes them above their tier.
- A low effort ceiling **deletes** levers rather than demoting them: anything needing legal or deal-desk sign-off you cannot get, anything creating delivery work you cannot staff. Strike them from the ledger and name which ones you struck - a ruled-out lever parked at the bottom reappears in the room as an offer.

If the counterpart cannot decide (3b without a mandate, or 3c/3d), flag it before planning: a concession granted to a non-decision-maker gets spent twice, because the real decision maker will ask for it again.

## Workflow

1. **Build the bargaining mix.** List every issue in play - price, terms, scope, service, risk, timing - including the issues the buyer will raise, not only the ones you plan to. Lay out the four levers (volume, cash timing, contract length, deal timing) before touching price, so you can trade across them instead of defaulting to a discount. Pull levers from [concession-inventory.md](./references/concession-inventory.md), already priced and ranked, minus the ones question 11 ruled out.
2. **Write two separate lists**: what you are willing to give, and what you will demand in exchange. Write both now, in full - in the room you will judge relative value poorly and forget half your asks.
3. **Price every item on cost-to-us vs value-to-them, and order it by the ratio.** Lead with the highest value per unit of cost, not with the cheapest lever.
   - Cost to us is margin, the precedent set for every deal after this one, delivery burden, and reversibility - never a currency figure, scored only in magnitudes: near-zero, an hour, a week, a quarter, a standing job.
   - Default B2B family order, efficiency axis: `service access > cash timing > scope > headline discount > price protection`.
   - Cost-to-us axis: `price protection > headline discount > scope > cash timing == service access` (the tie holds because both spend capacity or working capital you get back inside the term, leaving no clause behind).
   - Value-to-them axis: `price protection > headline discount > scope > cash timing > service access`.
   - [concession-inventory.md](./references/concession-inventory.md) carries every lever priced against those axes, the B2C order, and what each order starves.
   - Treat that order as a default, not a law: re-rank it against this deal and against who has to execute it. A renewal negotiates up from last time's concessions, a buyer already anchored on a number leaves you only the non-price rows, and a lever class your rep cannot get approved in time drops a tier.
4. **Tier the ledger in ratio order**: first moves, mid, last resort, highest value per unit of cost at the top of each tier, never the cheapest item first.
   - The same concession is worth different amounts to different people:
     - Finance weighs payment terms and financial risk.
     - Procurement weighs documented savings.
     - The business sponsor weighs speed and outcomes.
     - Technical roles weigh support and integration.
   - Route each concession to the stakeholder who values it most, then re-rank. A lever's value is its value to that best recipient, not an average across the room.
   - Pair every item with (a) a named reciprocal get and (b) the approval level it needs. For a lever carrying contractual or regulatory exposure, record its compliance cost and how long it binds you in that approval cell.
   - No orphan gives: an unpaired concession is a defect in the plan, not a nice gesture.
5. **Set the walk-away from your alternative, never from your margin floor.** Value the no-deal alternative (your BATNA), derive the reservation price from it, and write it down. Estimate the counterpart's reservation point too: if the two ranges cannot overlap (no ZOPA), walking is the rational plan and no concession sequence fixes it.
6. **Plan ranges per issue and plan issues independently, not as a fixed sequence.** Set an opening, a target, and a limit for each issue.

   Do not script the order you will concede in: field observation of skilled vs average negotiators (Rackham & Carlisle) found heavy sequence planning is what average negotiators do. The order is itself negotiable, and a pre-set order collapses the moment the counterpart opens on your last item.

   Plan each issue so you can trade in whatever order the conversation takes. The ratio ranking from step 3 says which lever to reach for first when you do move; it is not a script for the order the issues come up in.

7. **Build 2-3 MESO packages** (multiple equivalent simultaneous offers): packages of equal value to you but different shape for the buyer - e.g., lower price with shorter term vs higher price with longer term and stronger support. Do not rank them: `A == B == C` on cost to us by construction, and if one is genuinely cheaper for you than the others it is not a MESO, it is a discount ladder wearing three hats. Which one they gravitate to reveals their priority ordering without you asking for it.
8. **Plan the log-rolls.** Where your priority ranking differs from theirs, trade your low-priority issues for their high-priority ones. Multi-issue deals create value exactly here, and negotiators miss these trades by default - mark the candidate pairs in the plan explicitly.
9. **Shape a decelerating pattern within each issue**: shrinking increments toward your limit signal that the limit is real. Honest caveat: the supporting evidence is lab-based and mostly single-issue; in a multi-issue deal, log-rolling (step 8) matters more than taper mechanics. Hold your pre-set target no matter what pattern the other side runs at you.
10. **Write the conditional line for every planned trade**: "If you can do X, then we can consider Y." Never plan an unconditional give. Draft the exact sentences now from [trade-language.md](./references/trade-language.md) - improvised phrasing under pressure turns trades into gifts.
11. **Produce the pre-call one-pager** (format below) and rehearse the two or three hardest asks out loud - the get requests, not the gives.
12. **Run the Measurement check** below; iterate on the plan until it passes.

If your harness has persistent memory, store the walk-away line, authority band, and remaining unspent tiers after each round - the next conversation on the same deal starts from the updated plan, not from scratch. Without memory, tell the user to keep the one-pager and mark spent concessions on it.

## B2B vs B2C

Every workflow step above applies identically to both - only the concession currency differs.

- B2B currency is contract terms whose cost arrives later: term length, payment timing, ramped pricing, scope, support tier, uptime and service credits, renewal-uplift caps, price holds, liability caps. That delay is why sellers systematically under-price them.
- B2C currency is bundled goods with a known unit cost: delivery, installation, extended warranty, trade allowance, financing terms, priority scheduling, accessories, a gift card instead of a headline discount (protects the reference price). Cheaper to price accurately, easier to give away thoughtlessly.
- B2C compresses the timeline: single session, counterpart in the room. Keep the plan to one page and memorize the tiers - there is no pause to consult a ledger.

Both catalogues, ranked and priced: [concession-inventory.md](./references/concession-inventory.md).

## Pre-call one-pager

Output the plan in this shape (filled examples in [concession-ledger-example.md](./references/concession-ledger-example.md)):

```
DEAL: <what, list price, counterpart, their role, timing pressure each side>
WALK-AWAY: <reservation point + the alternative it derives from>
DEAL SPACE: <estimate of their reservation point; ZOPA yes/no>

TRADE LEDGER  (rows in ratio order within each tier - best value per unit of cost first)
| Lever | Tier | Cost to us | Value to them | Best recipient | Required get | Approval | Range (open → limit) |

STRUCK LEVERS: <ruled out by the effort ceiling or authority - listed once, never carried in the ledger>
MESO PACKAGES: A == B == C on cost to us, different shape
LOG-ROLL CANDIDATES: <our low-priority issue ↔ their high-priority issue>
HARDEST ASKS TO REHEARSE: <2-3 get requests, verbatim>
```

Write "Cost to us" in magnitudes only - near-zero, an hour, a week, a quarter, a standing job - never as a currency figure. The deal's own prices belong on the DEAL and WALK-AWAY lines, not in the axis cells.

## Failure modes

These are not ranked, and deliberately so: they are not alternatives you pick between. Several can fire in the same call, and which one arrives first is the buyer's choice rather than yours - an order here would read as a queue to work through and leave the rest unguarded.

- **Unilateral discounting** - a give without a get teaches the buyer the next ask is also free. Fix: conditional line on every trade, no exceptions.
- **Conceding before pushback** - moving before the buyer has actually pressed is bidding against yourself. Hold the plan until an ask lands.
- **The sucker pattern** - one big opening concession then nothing signals the open was padded. Open small; keep increments shrinking.
- **Salami slicing and the last-minute nibble** - many small asks, or one "tiny" ask after handshake. Counter procedurally: get their full list on the table before moving, keep all issues linked, and re-open the whole package if a new ask appears after agreement.
- **Conceding to the wrong stakeholder** - giving procurement what the sponsor never asked for converts a relationship asset into a commodity input. Route per step 3.
- **Negotiating with a non-decision-maker** - every concession will be re-requested by the person who actually decides. Confirm authority before spending tiers.
- **Quarter-end capitulation** - the seller's own commission timing drives the deepest discounts, and buyers schedule to it. Decouple the plan from your fiscal calendar; cap what quarter-end is allowed to unlock.
- **Discount stacking** - promotions, bundle incentives, competitive matches, and discretionary discount compound past what any single approval intended. Compute the combined concession before granting the last piece.
- **Verbal-only concessions** - anything not written on the order form dies with the champion. Every granted trade and its get goes into the written recap and the order form.
- **Argument dilution** - extra weak reasons hand the counterpart something to attack. One strong reason per position; stop talking.

## Procurement counter-tactics

Procurement is measured on reportable savings against a baseline - they need a documented win more than a genuinely cheaper deal. A credible anchor plus a documented, low-real-cost concession package satisfies their scoreboard without margin loss. Operational rule: **never reduce price without removing scope.**

The table below is a lookup, not a menu - each row is keyed to the move the buyer makes, so ranking the counters would be false precision: you never choose between them.

| Buyer move                           | Mechanism                                                       | Counter                                                                                                          |
| ------------------------------------ | --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| "You'll have to do better than that" | Vague pressure inviting you to cut against yourself             | Ask what specifically must improve, and by how much; trade, do not move                                          |
| Budget bogey                         | Friendly fixed-budget anchor that makes you solve their problem | Confirm who decides and who pays; fit scope to the number; present a pre-built MESO at that budget               |
| Claimed limited authority            | "I can't approve that" buys time and free movement              | Mirror it - your pricing is set above your level too; withhold firm concessions until their authority is present |
| Competitor price claim               | Real or bluffed cheaper quote                                   | Ask for the quote in writing; price the scope difference instead of matching the number                          |
| Unbundling / line-item pricing       | Exposes where margin concentrates                               | Re-price components so the bundle discount disappears when unbundled                                             |
| Timing to your quarter-end           | Buys your calendar-driven desperation                           | Anchor timeline on their compelling event; cap end-of-quarter discount authority                                 |

## Measurement

Plan readiness - the plan is not done until all of these pass; iterate until 100%:

- Every listed concession has (a) a named reciprocal get, (b) a cost-to-us magnitude, not a currency figure, (c) the approval level required - including the review a compliance-exposed lever triggers.
- Rows sit in ratio order within each tier, and the levers the effort ceiling ruled out are struck and named, not sitting at the bottom of a tier.
- The walk-away line is stated in writing and derived from the alternative, not the margin floor.
- Every planned trade has its conditional sentence written out.
- At least two MESO packages exist, roughly equal in value to the seller.

Outcome KPIs to track after the negotiation:

- Concession-to-get ratio: share of granted concessions with a documented reciprocal commitment on the order form.
- Realized price vs list, per deal and per segment.
- Discount distribution shape: bunching just under an approval threshold means the matrix is being gamed, not respected.
- Win rate and cycle time by discount band - confirms price gains are not buying losses elsewhere.
- B2C: front-end vs back-end gross per unit, and retained vs booked (a deal can post strong gross and lose it to refunds and early payoffs).

## References

- mbfinotti/sales-skills@deal-value-calc - quantify the deal's underlying value and ROI (the value-to-them inputs for step 3)
- mbfinotti/sales-skills@sales-objection-handling - in-call rebuttals to price and competitor objections
- mbfinotti/sales-skills@deal-champion-mapping - map which stakeholder receives which concession
- mbfinotti/sales-skills@sales-meeting-recap - paper the granted trades and their gets after the call
