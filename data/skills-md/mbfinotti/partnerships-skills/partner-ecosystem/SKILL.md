---
name: partner-ecosystem
description: Map a company's partner and channel ecosystem as a strategy exercise  - an inventory of every partner type (resellers, distributors, MSPs, ISVs, SIs, affiliates, marketplaces, plus retail, creator, licensing and co-branding partners for consumer brands), partner account overlap analysis, channel coverage gaps and conflict zones, a weighted partner scorecard, and a prioritization 2x2. Use whenever the user mentions partner ecosystem mapping, a partner landscape, channel coverage, partner type classification, ecosystem whitespace, or which partner categories deserve investment, even if they never say ecosystem. Do NOT use for sequencing which category to launch next  - use mbfinotti/partnerships-skills@partner-ecosystem-expansion instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.4.9"
---

# Partner Ecosystem Mapping

Map the full partner and channel landscape of one business area. No single canonical framework owns this discipline.

The map covers:

- Which partner types touch your customers.
- Who overlaps with your market.
- Where the coverage gaps and conflict zones sit.
- Which ecosystem segments deserve investment attention.

Built from:

- A role taxonomy: Jay McBain's trifurcation of the channel.
- An overlap mechanic: account mapping, popularized by Ecosystem-Led Growth.
- A mapping technique: Verna Allee's Value Network Analysis, Ron Adner's value blueprint.
- A prioritization pass: weighted scorecard plus 2×2.

The output is a decision artifact, never a partner program:

- Ecosystem map.
- Coverage/whitespace view.
- Prioritization view.
- A short ecosystem strategy memo.

Program design, tier criteria, conflict rules of engagement, and per-partner economics hand off to sibling skills instead (see Reference).

## Interview

Ask before mapping anything. One question per message; offer multiple-choice answers when possible. Skip a question only when the user already gave the answer.

- B2B, B2C, or hybrid? What does the company sell, to whom (ICP), at what price band, through which motion (self-serve or sales-led)?
- Which single business area or product line should the map cover? (Never the whole company at once - offer the 2-3 plausible scopes as choices.)
- What is the goal of the map: choose a channel strategy, find coverage gaps, diagnose conflict, size the ecosystem for an executive ask, or landscape before building a program?
- Current partner mix: which partner types exist today, roughly how many per type, and how many are actually active?
- What data exists: CRM closed-won history, sourced/influenced attribution fields, account-overlap data with any partner, customer tech-stack or purchase-channel information?
- Are you the platform others build on, or a participant in someone else's ecosystem? (Both can be true in different areas.)
- Constraints: who sponsors this, who must approve it, and how much capacity exists to act on it?
- By what date must the map land, and what decision is waiting on it? (A date inside a week promotes the closed-won review and the interview-based overlap proxy; a quarter of runway makes permissioned account mapping and a convened workshop affordable.)
- One-off win or compounding asset? (A single exec ask stops at a static matrix and a memo; a compounding mandate justifies the CRM field definitions, the overlap infrastructure, and the recurring review cadence that keep the map alive after the meeting.)
- What is the effort ceiling - your own hours, whose calendars you can command, and how much political capital you can spend convening stakeholders or asking a partner for their account list? (A solo ceiling rules out both the participative workshop and partner data sharing; both need other people to say yes.)

Carry these three answers into every ranking below. They are the only inputs that can reorder the defaults for this user.

## Workflow

Hold one discipline across every step below, wherever a real choice exists:

- Which business area to scope.
- Which overlap proxy to accept.
- How to weight a scorecard.
- Which visualization to build.
- Which categories make the cut.

Put 2-3 candidate approaches to the user with their trade-offs and your recommendation, then wait. Never present a single option as if it were the only one. Never let an assumption harden into the map unstated.

Every ordering in the steps below is a default, not a law. It ranks by value returned per unit of effort, never the same ordering as cheapest-first, and it shifts with context and with who executes it. Re-rank it against what you already know about this user before recommending anything.

Signals that move the reordering:

- A CRM that already carries structured partner-influence fields moves the internal data pull further ahead of everything else.
- A designer on hand moves the network diagram up.
- An audience that reads spreadsheets rather than diagrams moves it back down.
- An existing partner already sharing account data makes account mapping the cheap option rather than the expensive one.

Say which of their answers moved which option, so the reordering is auditable rather than a preference you asserted.

1. Run the Interview; confirm the scope is one business area with a stated goal before touching data.
2. Inventory every third party that touches customers of that area, working the evidence sources in this order. Never build the inventory from inbound partnership requests or the team's personal network; teams that do sign partners with no shared accounts, no shared ICP, and no path to joint pipeline.

   - **Internal data pull** - CRM records, closed-won notes, support tickets, integration and product usage. An hour or two on data you already own, and every name it returns is evidence that the player touched a real customer. Start here always.
   - **Customer interviews** - a week of scheduling and conversations. The only source that finds the advisors, communities, and unlogged influencers nothing in your systems ever recorded, which is exactly the band a transaction-only view misses.
   - **Public sweep** - competitor partner directories, marketplace listings, review-site category neighbors, conference sponsor lists. Near-zero effort where you can browse the web, and it returns breadth fast, but nothing it finds is evidence that any of those players touch _your_ customers. Treat its output as candidates to verify, never as inventory.
   - **Value Network Analysis participative workshop** - a week of calendars plus the political capital to convene stakeholders. It buys the intangible exchanges (trust, market insight, brand association) and, more importantly, shared ownership of the map by people outside partnerships. See [references/discovery-workshops.md](references/discovery-workshops.md).

   - effort: workshop > customer interviews > internal data pull == public sweep
   - value: customer interviews > workshop > internal data pull > public sweep
   - efficiency: internal data pull > customer interviews > public sweep > workshop

   The internal data pull and the public sweep tie on effort: each is an hour or two of one person working alone, with no permission to obtain and no calendar to negotiate. They are nowhere near equal on value: the pull wins that axis because only its output is evidence about _your_ customers.

   Where you cannot browse the web, the sweep is not cheap but impossible: delete it and say so, rather than listing a source nobody can reach.

   - **Default:** the internal data pull alone.
   - **Escalate to customer interviews when** closed-won notes name third parties you cannot classify, or the influence band comes back empty. It usually does; that is a gap in your logging, not in the ecosystem.
   - **What this order starves:** the workshop. It is second on value, first on effort, last on efficiency, so a ratio never once convenes it, and it is the only source that makes people outside partnerships own the map instead of receive it.
   - **Promote the workshop when** the map has to be owned by sales, product, or an exec sponsor rather than merely read by them; the map is drafted there, not after it has been scored.
   - **Delete the workshop when** the Interview gave a solo effort ceiling. Name it as deleted: it needs other people to say yes, and one carried at the bottom of the list returns as a week of calendars nobody agreed to.

3. Classify each player on two axes:

   - Role in the customer journey: influence, transact, or integrate-and-deliver (McBain's trifurcation, Canalys).
   - Engagement depth: from listing through embedded.

   Include competitors. Coopetition and the partners you share with them are signal, not noise. See [references/partner-type-taxonomy.md](references/partner-type-taxonomy.md).

4. Establish overlap using one of two mechanics. This is the one place in the exercise where the cheaper option is not merely weaker but _safer_, so rank all four axes before recommending:

   - **Permissioned account mapping** - exchange filtered account lists with the partner and classify shared accounts into the four overlap quadrants. The only mechanic that yields overlap at account granularity, which is what makes co-sell targets and whitespace countable rather than adjectival.
   - **Interview and tech-stack proxy** - infer overlap from what customers say they use and buy through. Directional per category, never per account.

   - effort: account mapping (a partner contact who agrees, plus a filtering and grading pass per partner) > proxy (a few hours on interviews you are running anyway)
   - compliance cost: account mapping (a data-sharing agreement, a privacy review of what leaves your systems, and an account list you cannot un-share once sent) > proxy (none)
   - value: account mapping (countable quadrants) > proxy (directional signal)
   - efficiency: proxy > account mapping while only one or two partners will share; account mapping > proxy once three or more will, since the legal and filtering setup is paid once and reused per partner

   - **Default:** the proxy, for the first map. Never let its absence stall the exercise.
   - **Start account-mapping paperwork in parallel when** the answers say a compounding asset, so the second map has real quadrants.
   - **Delete account mapping when** no partner will share a list, or a privacy review will not clear in the time available. Record it as deleted with the reason: a mechanic parked as "phase two" is how a map ships claiming account-level overlap it never measured.
   - Approximate from evidence, never from assumption. See [references/overlap-and-conflict.md](references/overlap-and-conflict.md).

5. Run the retroactive closed-won review: sample recent closed-won deals and record every third party that influenced each one. This is the cheapest high-signal step in the whole exercise. It proves whether the ecosystem already influences revenue before anything new is recruited.
6. Surface coverage gaps: segments, geographies, and journey stages with no partner coverage. Surface conflict zones too: partner-vs-partner, direct-vs-partner, multi-channel, and D2C-vs-retail for consumer brands. Quantify each one by accounts, revenue at stake, and territory.

   Detect and measure only. Writing the resolution rules belongs to `mbfinotti/partnerships-skills@partner-channel-conflict`.

7. Ask the self-positioning question: on this map, are you a keystone, a niche player in someone else's ecosystem, or accidentally behaving like a dominator (Iansiti & Levien, 2004)? The answer determines whether you recruit partners or get recruited.

   Read overall ecosystem health through three measures:

   - Productivity: does participation make members more efficient?
   - Robustness: does it survive shocks?
   - Niche creation: does it keep spawning new specialist roles?

   The typology predates modern digital platforms.

8. Run the category-level discovery sessions in the profession's own formats, not generic brainstorming:

   - An IPP definition session for each candidate category.
   - A JVP workshop testing whether the category can articulate joint customer value.

   A category that fails the JVP test does not proceed. Run this _before_ scoring, so a category that cannot state its joint value never receives a composite that later has to be retracted. See [references/discovery-workshops.md](references/discovery-workshops.md).

9. Prioritize the surviving categories. Build a weighted scorecard composite for each axis, then plot categories on the prioritization 2×2: strategic fit × ease of execution (Chris Lavoie's quadrants). Segment scorecard weights by partner type: a referral partner and a systems integrator must never share one scorecard.

   Rank the categories that already exist in this ecosystem, for investment attention among them. Two handoffs apply beyond this ranking:

   - Ranking named candidate alliances belongs to `mbfinotti/partnerships-skills@alliance-prioritization`.
   - Sequencing categories the company does _not_ yet have (entry order, readiness gates, capacity limits) belongs to `mbfinotti/partnerships-skills@partner-ecosystem-expansion`, which takes this ranking and the whitespace below as its input.

   See [references/prioritization-scorecards.md](references/prioritization-scorecards.md).

10. Choose the visualization by the decision it settles, not by how it looks in a deck. Rank the four formats before offering them. Present the top 2-3 with their trade-offs and your recommendation, then let the user pick before building it.

    - **Matrix** - a grid of partners on coverage × capability depth. Settles the investment call, which is the decision this whole map exists to inform. Near-zero build: it is a table, and it reads from the scorecard composites you already have.
    - **Heat map** - colour by geography, vertical, or capability. Settles where the whitespace is, at a glance and in one image an exec will actually retain. An hour, and it needs one clean dimension attached to every player.
    - **Network diagram** - vendor, partners, and the connections between them. Settles who the hubs are, and it is the only format that can. A day or more plus real layout skill; without it the picture reads as a hairball and settles nothing.
    - **Tiered view** - concentric circles or a pyramid by strategic relevance. Settles core versus periphery, but that ranking was already decided in step 9, so the format mostly restates it.

    - effort: network diagram > heat map > tiered view > matrix
    - value: matrix > heat map > network diagram > tiered view
    - efficiency: matrix > heat map > tiered view > network diagram

    Default to the matrix. Build the heat map instead when the stated goal from the Interview was coverage gaps rather than investment. It costs an hour more than the tiered view because it needs one clean dimension attached to every player, where the tiered view only redraws a ranking step 9 already produced.

    - **What this order starves:** the network diagram. It answers a question no other format can answer at all, and it is the only one that costs a day plus a skill the team may not have, so a ratio rejects it every time and hub structure simply never gets looked at.
    - **Promote it when** the decision in front of the user is which player is the hub (routing, aggregation, or a partner other partners depend on) and someone with real layout skill is free.
    - **Delete it when** nobody has that skill. A hairball settles nothing and costs a day, so don't present it as ambitious.
    - **Skip the tiered view entirely** once the prioritization 2×2 exists: two views of one ranking invite the reader to look for a difference that is not there.

    See [references/overlap-and-conflict.md](references/overlap-and-conflict.md).

11. Validate the map against ecosystem-level health metrics, as a diagnostic reading only. Per-partner scorecards and review cadences belong to `mbfinotti/partnerships-skills@partner-performance`.

    - effort: sourced-vs-influenced split (CRM field definitions plus a written de-duplication policy - a week where they don't exist, near-zero where they do) > activation ratio (near-zero wherever registration dates exist) == coverage read (already computed in step 6)
    - value: sourced-vs-influenced split (whether the ecosystem earns money at all, and whether recruitment is outrunning enablement) > activation ratio (catches logo collecting) > coverage read (restates step 6)
    - efficiency: activation ratio > sourced-vs-influenced split > coverage read

    Activation ratio and coverage read tie on effort at a genuine zero: one is a single query against registration dates you already store, the other is a number step 6 has already computed. Neither costs anything beyond reading it. They separate on value, and the activation ratio wins.

    - **Read first:** the activation ratio. It is one query and it invalidates a whole class of map.
    - **What this order starves:** the sourced-vs-influenced split. It is the only reading that says whether the ecosystem earns money at all, and the week of CRM field definitions and de-duplication policy behind it loses to two free numbers every time.
    - **Promote it when** the map is asking for investment rather than reporting coverage, since no exec funds an ecosystem on an activation ratio. It leads outright wherever those CRM fields already exist, which turns the most expensive reading here into a free one.
    - **Delete it when** the CRM cannot carry those fields. Say plainly that the earning question stays unanswered: carrying it as a pending metric lets a later reader assume it was measured.

    See [references/ecosystem-health-kpis.md](references/ecosystem-health-kpis.md).

12. Present the deliverable section by section, and validate each section with the user before drafting the next:

    - Inventory
    - Classification
    - Overlap findings
    - Gaps and conflicts
    - Self-positioning
    - Prioritization
    - Memo

    Revise on pushback. Require explicit approval on every section before finalizing anything.

13. Score the finished map against the pass threshold below. Iterate until it passes. If it cannot pass (fewer than ten real ecosystem players, no verifiable overlap), say so plainly and scope the honest next step, usually customer interviews, rather than shipping a decorative map.
14. Set the review discipline: the map is never finished. Agree a recurring review cadence plus immediate-update triggers:

    - A merger or acquisition.
    - New regulation.
    - A category moving quadrants.

    Timelines for the exercise itself are not reliably published. Treat any duration as an estimate, though a founder-led compressed first pass has been done in roughly a day.

15. If your harness has persistent memory, memorize the approved map's scope, partner categories, and prioritization decisions so a later run starts from them instead of re-interviewing.

## Pass Threshold

A first map is done when all of these hold. Iterate, meaning more interviews, more deal reviews, or a tighter scope, until they do:

- **At least ten ecosystem players categorized** by journey role and engagement depth.
- **Verified overlap data** behind every overlap claim - account mapping output or customer-interview evidence, never assumption.
- **A retroactive closed-won influence analysis** showing where the ecosystem already touches revenue.
- **At least one named decision the map informs**, with an owner - a map that drives no decision is the discipline's most common failure.
- **Every quoted benchmark carries a provenance flag** (vendor first-party, analyst, aggregator, or consultancy) - almost every published number in this field comes from a vendor that profits when the number looks good.

## The Ecosystem Strategy Memo

The map is the evidence. The memo is what an executive actually reads and funds. Keep it to roughly two pages, and write every line so a reader can trace it back to map evidence:

```
ECOSYSTEM MAP  - <business area>, <date>
Scope          : business area, ICP, geography, and what was deliberately excluded
Inventory      : players found, by journey role × engagement depth, with data sources
Overlap        : verified overlap per partner category + the four-quadrant read
Closed-won read: what the retroactive review showed about existing ecosystem influence
Gaps           : uncovered segments/geographies/journey stages, each sized
Conflicts      : zones detected, accounts and revenue at stake (detection only)
Positioning    : keystone, niche player, or drifting toward dominator  - and why
Priorities     : categories on the 2x2, with the scorecard weights that placed them
Decisions      : what this map asks for, each with an owner and a review date
Open questions : what the data could not answer, and what would answer it
```

Two rules govern the memo:

- **Every claim names its source.** "Three of eight closed-won deals named an implementation partner" is reviewable; "SIs matter to us" is not.
- **The open-questions section is mandatory.** A map with no stated uncertainty is a map that stopped asking, which is how a decorative landscape gets mistaken for evidence.

## B2B and B2C

The spine is identical in both:

- The identify, analyze, visualize, optimize sequence.
- The one-business-area scoping rule.
- The map-from-customer-data-not-inbound-requests rule.
- The recurring-review discipline.
- Strategic-fit × ease-of-execution prioritization logic.

Say so when the user asks. Do not reinvent the method per side.

What genuinely changes:

| Dimension          | B2B                                                                    | B2C                                                                                                      |
| ------------------ | ---------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Partner vocabulary | Resellers/VARs, distributors, MSPs, SIs, ISVs, marketplaces, alliances | Retail/wholesale, creators and affiliates, licensing, co-branding                                        |
| Partner counts     | Tens to hundreds; high value per partner                               | Influence band runs to thousands at far lower value each                                                 |
| Attribution        | Sourced vs influenced pipeline over long cycles                        | Transactional and fast-cycling: LTV of partnership-acquired customers vs other channels, plus brand lift |
| Signature conflict | Partner-vs-partner and direct-vs-partner                               | D2C vs retail partner                                                                                    |

Both taxonomies and the D2C-vs-retail conflict pattern are detailed in [references/partner-type-taxonomy.md](references/partner-type-taxonomy.md) and [references/overlap-and-conflict.md](references/overlap-and-conflict.md).

## Failure Modes

These carry no efficiency ordering, deliberately, because each row is a different diagnosis with one fix, not a menu of competing fixes for one problem. Ranking them would rank the reader's symptoms rather than their options, which is false precision. Apply every row that matches.

| Failure                                                                | Fix                                                                                                                                   |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| Map created but never used for a decision                              | Attach named next steps with owners; put the map into a recurring strategic review                                                    |
| Competitors excluded from the map                                      | Map coopetition and the partners you share with competitors - they are signal                                                         |
| Map treated as finished                                                | Review cadence plus event triggers (M&A, regulation, quadrant moves)                                                                  |
| Whole company mapped at once                                           | Scope to one business area; re-run per area later                                                                                     |
| Inventory sourced from inbound requests or personal network            | Rebuild from customer data and verified overlap                                                                                       |
| Logo collecting - a long tail of inactive partners counted as coverage | Read the activation ratio; a partner list is not a channel                                                                            |
| One scorecard for all partner types                                    | Segment weights by type; each type has a different route to revenue                                                                   |
| Recruitment running ahead of enablement                                | Partner count rising while sourced revenue stays flat is the tell; capacity to support a category belongs in its prioritization score |

## Invocation Examples

- "Map the partner ecosystem around our mid-market product line - I need to show the exec team where the coverage gaps are."
- "Which partner categories actually influence our closed-won deals? We have three years of CRM history and no attribution fields."
- "We keep signing partners with no shared accounts. Build the overlap analysis that would have caught that."

## Reference

- [references/partner-type-taxonomy.md](references/partner-type-taxonomy.md) - journey-role and depth axes, the B2B and B2C type tables, contested boundaries and misclassification traps.
- [references/overlap-and-conflict.md](references/overlap-and-conflict.md) - account mapping quadrants, whitespace rules, the three conflict patterns plus D2C-vs-retail, and the artifact format table.
- [references/prioritization-scorecards.md](references/prioritization-scorecards.md) - weighted scorecard mechanics, the Lavoie 2×2, how the two combine, with a worked category example.
- [references/ecosystem-health-kpis.md](references/ecosystem-health-kpis.md) - sourced vs influenced, activation ratio, the four-bucket frame, benchmarks with provenance flags.
- [references/discovery-workshops.md](references/discovery-workshops.md) - Value Network Analysis workshop format, Adner's value blueprint, IPP definition session, JVP workshop question set.

Sibling skills (downstream handoffs, same collection):

- `mbfinotti/partnerships-skills@partner-channel-program` - designing the partner program the map says is warranted.
- `mbfinotti/partnerships-skills@partner-tiering` - tier criteria and benefits inside an existing program; the map's concentric circles are a layout, not tiers.
- `mbfinotti/partnerships-skills@partner-ecosystem-expansion` - planning which partner categories to add into the whitespace this map quantifies.
- `mbfinotti/partnerships-skills@alliance-prioritization` - ranking named candidate alliances; this skill ranks categories only.
- `mbfinotti/partnerships-skills@partner-channel-conflict` - rules of engagement for the conflict zones this map detects.
- `mbfinotti/partnerships-skills@partner-performance` - per-partner scorecards and review cadences beyond this map's ecosystem-level diagnostic.
