---
name: ad-buyer-group-mapper
description: "Map the likely buying committee for an offer, deal size, and industry, and give each role a messaging angle plus the ad-targeting proxy - job function and seniority, account list, account-level intent - that actually reaches them, sequenced by buying stage. Use whenever the user mentions a buying committee or buying group, decision makers, influencers or blockers, who signs off, targeting the economic buyer or a champion, per-role ad messaging, or whether one broad message beats per-role targeting - even if they never say 'buying committee'. Covers B2B committees and multi-decider household purchases. Do NOT use to size or build the audiences themselves - use mbfinotti/advertising-skills@ad-audience-targeting instead."
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.3.3"
---

# Buyer Group Mapper

Given a deal size, industry, and offer, identify the roles likely to sit on the buying committee, then pair each role with a messaging angle and the targeting proxy that actually reaches it on an ad platform. The output is a segment-level role map for campaign planning - role patterns for a market segment, not a named-contact map of one live deal, which is a different artifact with a stricter evidence standard.

Buying committees are B2B-native. The underlying model partially transfers to multi-decider consumer purchases (households) - see that section for what carries over and what does not.

This skill produces the role map. Turning it into sized, budgeted, sequenced audiences is mbfinotti/advertising-skills@ad-audience-targeting. Writing the ads themselves is mbfinotti/advertising-skills@ad-copy-variants.

## Clarifying questions

Ask once, briefly, before mapping; skip anything already answered.

1. What is the offer - and is this B2B, or a multi-decider consumer purchase?
2. What is the deal size / ACV band? (Drives committee size and whether per-role creative is affordable.)
3. What industry, and what buyer company size - SMB, mid-market, enterprise?
4. How large is the addressable market - hundreds of named accounts or tens of thousands?
5. What evidence about past buyers exists: closed-won/lost data, buyer interviews or call notes, review mining, account-level intent data?
6. Which platforms will run this, and at what monthly budget?
7. Is the purchase net-new for the category, a replacement, or an expansion? (Changes who is present.)
8. By what date must results land? A hard deadline promotes evidence you already own and reach you can buy this week; it demotes buyer interviews and anything needing a standing job to configure.
9. One-off campaign win, or a compounding asset the team re-uses each quarter? Compounding promotes closed-won analysis, buyer interviews and an owned account list; one-off promotes published bands and function-level reach.
10. What is the effort ceiling - research hours per account, creative variants you can actually produce, and how many roles you can coordinate across? A low ceiling promotes a merged map; a high one is what makes per-role creative affordable.

Every ranking in this skill is a default for a median team, not a law: it shifts with context and with who executes it. Re-rank each one against these answers and against what you already know about the user, then say in the output which answer moved which option. Signals worth weighing:

- An account list already owned.
- An in-house research function.
- An intent feed already licensed.
- A CRM too dirty to diff.

## Evidence gate

- Every role is a hypothesis until evidence supports it. Never assert a committee; propose one and mark each role's status.
- Pick evidence sources by efficiency - roles confirmed per hour spent - not by strength alone. The axes disagree:
  - efficiency: closed-won/lost diff > call notes > review mining > buyer interviews > published research > intent data > title inference
  - value: closed-won/lost diff > buyer interviews > call notes > review mining > published research > intent data > title inference
  - effort: buyer interviews > intent data > closed-won/lost diff > review mining > call notes == published research > title inference
  - compliance cost: intent data > buyer interviews > all others == none
- Effort in orders of magnitude:
  - Buyer interviews: a week of scheduling across roles.
  - Intent data: a standing job to configure and re-tune topics.
  - Closed-won/lost diff: a day per deal-size segment.
  - Review mining: a few hours.
  - Call notes or published research: an hour to read what already exists.
  - Title inference: near-zero.
- Call notes and published research tie on effort because both are an hour of reading a document someone else already produced; neither buys any new collection. They do not tie on value - notes are about your buyers, the bands are about somebody else's.
- Act on the two places the axes disagree. Call notes carry nearly the value of buyer interviews at a fraction of the effort, because the recordings already exist. Intent data sits high on effort and low on value here, because it resolves to accounts and so never confirms a role.
- Compliance cost, where it applies. A third-party intent feed needs a licensing and privacy review before first use, and its terms constrain re-use once the data is inside your targeting stack. Recorded interviews need per-participant recording consent, and a call recorded without it cannot be cited as evidence later.
- Default rung: diff which roles appear in won deals against lost deals, filling gaps from call notes that already exist - the strongest derivation available to most teams. Move up to buyer interviews when the diff leaves a role's presence ambiguous across segments; add intent data only when the unknown is which accounts to cover, never which roles exist.
- What the efficiency order starves: buyer interviews, second on value and first on effort, lose every round to sources that already exist. Promote them the moment a role's presence stays ambiguous after the diff and the notes - that ambiguity is the one thing no existing document can resolve.
- Re-rank this order against the user: clean CRM stage history makes the diff near-free, no CRM hygiene drops it below review mining, an in-house research function makes interviews cheap, and an already-licensed intent feed makes intent near-zero effort.
- Delete, don't demote: a team that cannot obtain per-participant recording consent deletes buyer interviews from the menu and says so in the output; a team with no licensing route for third-party intent deletes intent data. A ruled-out source parked at the bottom of the ladder reappears later as scope nobody budgeted.
- Title inference is the only free source and the weakest one - it is the floor of the ladder, never a rung to stop on.
- Never invent an org chart from a title. Classify a role from seniority plus how close its function sits to the product category - nothing else. When title and department contradict each other, output "unknown", not a guess.
- A role with no evidence survives only as a labelled hypothesis with a stated disproof test (e.g. "cut security review if it appears in none of the next ten closed-won notes"). A role with no evidence and no disproof test gets cut.
- Apply the working test from persona research: if a role changes no targeting, creative, or offer decision, delete it. Roles that survive because they sound plausible are liabilities, not audiences.

## Committee sizing

Derive committee size from the user's own closed-won data first. Published figures are a sanity band only - primary studies disagree by a factor of two because each defines "involved" differently and samples different deal sizes.

| Source                          | Size                                                       | Qualifier to keep attached                                                  |
| ------------------------------- | ---------------------------------------------------------- | --------------------------------------------------------------------------- |
| Gartner                         | 6-10 decision makers                                       | complex solutions only - the qualifier is almost always dropped in citation |
| TrustRadius 2024 (2,164 buyers) | 96% of groups have ≤5; SMB peaks at 2-3, enterprise at 4-5 | tech purchases, self-report                                                 |
| 6sense                          | ~10.6 (North America)                                      | behaviorally captured active participants                                   |
| Forrester 2024 (>16,000 buyers) | 13 internal stakeholders                                   | broadest definition of "involved"                                           |

- Do not rank these four sources against each other: they sample different populations under different definitions of "involved", so any ordering would read as a quality ranking the disagreement does not support. Use them as a band and let the user's own closed-won data pick the number inside it.
- Seniority rises with deal size: 79% of purchases require CFO approval; 52% of groups include VP+ and 53% a C-suite executive (TrustRadius 2024).
- No primary study segments committee composition by industry or by purchase type (net-new vs. replacement vs. expansion). Say "no published data" instead of extrapolating.
- Sanity check both directions: a $6K ACV offer whose closed-won notes show two people does not get an eight-role matrix; a $500K enterprise deal mapped as champion-only is equally wrong.

## Role model

Use this six-slot vocabulary and define it inline in the output - no canonical role list exists, and the frameworks in circulation genuinely disagree.

| Role                | Definition                                                               | Typically arrives at                |
| ------------------- | ------------------------------------------------------------------------ | ----------------------------------- |
| Initiator           | Surfaces the problem and starts the search                               | problem identification              |
| Champion            | Feels the pain, drives the evaluation, spends political capital publicly | problem identification → throughout |
| End user            | Hands-on daily; judges impact on their own job                           | problem identification              |
| Economic buyer      | Owns the budget line; can approve or veto the spend                      | business-case stage                 |
| Technical evaluator | Screens against specs and architecture; veto power, no approval power    | requirements building               |
| Gatekeeper-blocker  | Procurement, security, legal, compliance - substantive veto holders      | validation                          |

Vocabulary flags to carry into the output:

- Champion, mobilizer, and coach are not synonyms:
  - Coach: feeds intelligence, may stay hidden.
  - Champion: advocates publicly.
  - Mobilizer: coined because traditional champions are often friendly contacts who cannot drive consensus.
  - When evidence shows your champion can't move the group, the map needs a consensus-driver, not a louder champion.
- "Gatekeeper" has two meanings: the classic administrative information filter, and the modern procurement/security/compliance functions holding substantive vetoes. This skill means the second; say which you mean.
- Never use "influencer" as a role label. It covers anyone whose opinion is sought, so it yields no targeting attribute and no messaging angle.
- Merge slots freely downward: SMB committees of 2-3 typically collapse to champion-who-is-the-user plus economic buyer. Do not fill empty slots for completeness.

## Per-role output

For each surviving role, fill all six fields - the angle is the deliverable; the first three are its inputs, and the proxy is what makes it operational:

| Field              | Answers                                                                        |
| ------------------ | ------------------------------------------------------------------------------ |
| Measured on        | What number or outcome is this role's job judged by?                           |
| Personal risk      | What happens to them if this purchase goes wrong?                              |
| Likely objection   | The first reason they'd say no, in their own words                             |
| Messaging angle    | The one framing that connects the offer to their metric and defuses their risk |
| Proof / offer type | Evidence format and CTA weight this role will accept                           |
| Targeting proxy    | The platform attribute combination that actually reaches this person           |

- Fine-grained per-role objection maps are weakly evidenced in published research - seniority-level content behavior is well evidenced, per-role objections mostly are not. Treat the starter patterns in [references/worked-example.md](references/worked-example.md) as defaults to verify against the user's own call notes and reviews, not as facts.

Offer types are a menu, and its axes disagree sharply - the cheapest asset to produce is not the one to build first:

- efficiency: compliance/security pack > ROI or savings calculator > ungated guide or checklist > demo or trial request > sandbox access > benchmark report
- value: demo or trial request > sandbox access > ROI or savings calculator > compliance/security pack > benchmark report > ungated guide or checklist
- effort: benchmark report > sandbox access > ROI or savings calculator > demo or trial request > compliance/security pack > ungated guide or checklist
- compliance cost: compliance/security pack > sandbox access > all others == none

- Effort in orders of magnitude:
  - Benchmark report: a quarter to collect data nobody else holds.
  - Sandbox access: a quarter of engineering.
  - ROI or savings calculator: a week to build.
  - Demo or trial request: a standing job, since each one spends sales capacity again.
  - Compliance/security pack: an hour to assemble from certifications already held, a quarter if none exist.
  - Ungated guide or checklist: near-zero.
- The pack leads because it is nearly free when the certifications exist and it is the only asset that removes a validation-stage veto - the highest-value outcome any single offer buys in this map.
- The demo does not lead despite the best per-person value: match offer friction to role warmth, because low-friction offers (guides, calculators, benchmarks) convert around 10-15% and high-friction offers (cold demo or trial requests) around 1.5-4%. Cold gatekeepers do not book demos at all.
- Compliance cost, where it applies: publishing a pen-test report or audit letter ungated needs security and legal sign-off, and a document published ungated cannot be recalled; a sandbox touching real data pulls in a data-processing review.
- Default rung per role: the ungated low-friction offer. Move up one rung once a role's proxy audience engages twice, never on the first touch.
- Re-rank against what the user owns: an existing SOC 2 pack promotes the compliance rung, and a proprietary data set already in hand promotes the benchmark report from last to first.
- Delete, don't demote: with no sales capacity to staff them, demos and trials leave the menu entirely - say "deleted: no sales capacity" rather than ranking them last, where they read as a stretch goal and quietly become one. Same for the sandbox with no engineering quarter to spend, and for the benchmark report when no proprietary data exists.
- Write angles in verbatim customer language wherever review mining or call notes supply it - exact phrases beat polished descriptions because they are how the buyer actually thinks.
- Every angle must be distinct. Run the swap test: if a role's angle could run unchanged against another role, rewrite one or merge the roles.

## Platform reality

A role list is worthless if no targeting attribute reaches it. Choose the proxy by efficiency - mapped roles reached per hour of setup - then check it against the floors below:

- efficiency: account list + function + seniority > function + seniority alone > intent-ranked account list + function + seniority > exact job title
- value: intent-ranked account list + function + seniority > account list + function + seniority > function + seniority alone > exact job title
- effort: intent-ranked account list > account list > exact job title > function + seniority
- compliance cost: intent-ranked account list > account list > all others == none

- Effort in orders of magnitude:
  - Intent-ranked account list: a standing job to configure and re-tune topics.
  - Account list: a week to build, then continuous maintenance.
  - Exact job title: a day enumerating variants, and you still miss the ones the platform never learned.
  - Function + seniority: an hour.
- Compliance cost, where it applies: uploading a matched audience triggers a data-processing review and the platform's own matched-audience policy, and a list does not unwind from the platform once matched; a licensed intent feed layers its own re-use restrictions on top.
- Default rung: account list + function + seniority whenever the addressable market is small enough to enumerate; fall back to function + seniority alone when it is not. Move up to intent ranking only when the list is larger than the budget can cover.
- Re-rank against what the user owns: an account list already built and maintained makes the top rung near-free, and a licensed intent feed already in the stack moves intent ranking up two places.
- Delete, don't demote: in a market of tens of thousands of accounts, both list-based rungs leave the menu. Name them deleted and plan on function + seniority, instead of leaving a list the team will never finish sitting at the bottom of the order.
- Exact-title targeting ranks worst on every axis: more setup effort than function + seniority for less reach, and it survives only where no function cell exists for the role. Platforms understand roughly 30-50% of job titles, each variant you didn't list is missed, and function + seniority roughly triples the addressable audience at similar engagement. On professional networks, title and seniority targeting are mutually exclusive: they cannot be stacked.
- Professional networks assign each person exactly one job function - a "Marketing Operations Manager" lands in Marketing or Operations, never both. Cross-functional roles, precisely the ones committees care about, straddle cells; expect to target two functions to cover one role.
- Function and seniority derive from self-reported profiles with no inference, so they inherit every stale and inflated title on the platform.
- Audience floors gate everything: the technical floor for matched audiences is around 300 members (about 1,000 for consumer-keyed matches), but the practitioner floor is 20,000-50,000 for typical budgets - below ~5,000 results rarely reach significance, and stacking AND conditions below ~50,000 degrades delivery. State the floor before splitting roles, not after.
- Intent data resolves to accounts, not people, at roughly 81% account-level accuracy - about one in five surging accounts has no genuine near-term intent, and narrow, well-configured topics reach only 60-70%. It ranks which accounts to cover, never who is inside them; a surge is never a committee member.
- An account list is an account signal, not familiarity - every individual on it is still cold from a messaging standpoint.
- Gate committee-wide coverage on account-level intent or engagement: run full multi-role targeting against a mini account list distilled from inbound leads or surging accounts, not against a cold industry-wide list. Cold committee-wide coverage burns budget on stakeholders with no reason to care yet.

## Precision vs. reach: an unresolved dispute

Three postures buy committee coverage. Rank them, state which one the map takes and why, and never pretend the dispute behind them is settled.

- efficiency: merged map (one primary angle + role-aware proof points) > one strong broad message > full per-role campaigns
- value: full per-role campaigns > merged map > one strong broad message - but per-role value only materializes above the thresholds below; under them it inverts
- effort: full per-role campaigns > merged map > one strong broad message

- Effort in orders of magnitude:
  - Per-role campaigns: a quarter, one creative set and one campaign per role, plus coordination across every role's reviewer.
  - Merged map: a week, one campaign and a handful of proof variants.
  - Single broad message: a week, then near-zero for each further role it happens to reach.
- What the efficiency order starves: per-role creative. It leads on value and leads on effort, so a ratio never selects it, and a skill that only computes efficiency will ship one generic asset against a six-role committee every single time. The two thresholds below exist to promote it anyway - say explicitly in the output which of them you tested and what the answer was, so the starved option gets refused on evidence rather than by default.
- **Against narrow role targeting:** the Ehrenberg-Bass 95-5 rule - roughly 95% of B2B buyers are out-market at any time - implies hyper-narrow targeting wastes exactly the reach that builds future mental availability. The proposed alternative is linking the brand to category entry points broadly.
- **For it, steelmanned:**
  - In a market of a few hundred named accounts, reach is bounded anyway and precision becomes affordable.
  - At high ACV, the economics support bespoke per-role creative even at inflated CPM.
  - The 95-5 argument itself concedes the in-market 5% should get activation.
- **Thresholds that move the default:** per-role campaigns are defensible below roughly 500 named accounts or above roughly $100K ACV. Below those, ship the merged map to a 20,000-50,000 audience - one primary angle plus role-aware proof points, not six campaigns.
- **Flip check:** if CPM inflation and frequency on the narrow audiences are not degrading cost per opportunity, tightening further is justified.
- Re-rank against what the user owns: an in-house creative team promotes per-role campaigns by cutting their effort, and a brand with no existing reach promotes the broad message, because a committee that has never heard of you converts on nothing.
- Delete, don't demote: one generalist marketer producing everything alone cannot run six campaigns whatever the thresholds say - delete per-role campaigns from that user's menu by name, and spend the role map on proof variants inside the merged map instead. Ranked last, they return in three months as an unfunded plan.
- Nobody has resolved this: no controlled test compares role-differentiated creative against a single strong message in matched programs, so the ordering above is an argued default, not a measured one.

## Sequencing: which role matters when

- The journey loops through six buying jobs, and 90% of buyers revisit at least one. Do not map roles to a linear funnel. The six jobs:
  - Problem identification.
  - Solution exploration.
  - Requirements building.
  - Supplier selection.
  - Validation.
  - Consensus creation.
- Arrival order:
  - End users and the initiator: surface at problem identification.
  - The economic buyer: engages with the business case (79% of purchases need CFO approval).
  - Security, legal, and procurement: arrive at validation, and a security reviewer added late can reopen requirements and reset agreed work.
- Reaching validation-stage roles _before_ validation is the cheapest insurance in the map.
- About 70% of the journey completes before any seller contact, 81-84% of deals go to the first vendor contacted, and fewer than 30% of eventual buyers ever fill out a form on the winning vendor's site. Committee reach therefore cannot be gated on form fills - ungated, role-relevant content and paid reach carry the pre-contact phase.
- No-decision is the real competitor: 40-60% of deals end in no-decision, and 56% of those are lost to indecision (fear of messing up) rather than status-quo preference. Amplifying urgency backfires on indecision - for economic buyers and gatekeepers especially, weight angles toward risk reduction and proof, not pressure.

## Multi-decider consumer purchases

The role vocabulary transfers. The consumer five-role model descends directly from the same organizational buying-center research. Its five roles:

- Initiator.
- Influencer.
- Decider.
- Buyer.
- User.

What genuinely carries over:

- The user often isn't the person approving the spend.
- Each decider needs a different message.
- One unconvinced member can veto the purchase.

What does not transfer:

- No procurement, legal, or security review.
- No career risk: the fear of a bad call is personal and financial, never professional.
- Personal money, not company money.
- Emotional and relational dynamics dominate over functional-role conflict.
- The unit pre-exists the purchase.
- The process runs on reviews and peers, not RFPs.

Apply this model only to high-consideration categories with a genuine second decider - vehicles, home improvement, family travel, insurance, private education, major appliances. Routine purchases have one decider, and this whole skill is overhead. Household-level targeting (connected-TV household graphs, shared devices) is real but imprecise and unquantified: prefer role-differentiated creative shown to a shared household audience over trying to isolate each member.

## Output shape

Deliver the map as one document:

1. Committee summary: estimated size with its evidence source, purchase type, the precision-vs-reach posture chosen with the thresholds applied, which interview answer moved any ranking off its default, and a named list of every option a stated constraint deleted from a menu.
2. Role map table, one row per surviving role: role | evidence (source + status: evidenced / hypothesis + disproof test) | measured on | personal risk | likely objection | messaging angle | proof/offer type | targeting proxy | estimated proxy audience vs. floor.
3. Sequencing notes: which roles to reach at which buying job, and where risk-reduction messaging replaces urgency.
4. Handoffs: which neighboring skill takes each next step (see References).

Short invocation examples: "Map the buying committee for our $80K ACV compliance platform selling to mid-market fintech" or "Who else decides when a family buys solar panels, and what do we say to each?"

See [references/worked-example.md](references/worked-example.md) for a filled-in B2B map, a household example, and a negative example.

## Failure modes

- Asserting the committee instead of hypothesizing it: every role ships with an evidence status or it doesn't ship.
- Inventing an org chart from a title: classify from seniority + functional distance; output "unknown" on contradiction.
- Over-splitting into per-role audiences below platform floors: merge roles whose proxies collide or undershoot.
- Filter stacking on generic creative: a narrow audience all seeing one unchanged ad is worse than a broad audience seeing role variants. Rich role knowledge should buy creative variants first, filters second.
- Running committee-wide targeting cold: gate it on account-level intent.
- Treating an account list as a warm audience: list membership is an account signal; the person is still cold.
- Letting the segment map impersonate a deal map: segment-level role patterns never substitute for evidence-graded work on named contacts in one live deal.
- Quoting "6 to 10 decision makers" as universal: it describes complex purchases only, and primary studies disagree by 2x.
- Keeping decorative roles: a role that changes no targeting, creative, or offer decision gets deleted.

## Objective and measurement

- Structural pass (before handoff): every surviving role has (a) an evidence source or a labelled hypothesis with a disproof test, (b) a targeting proxy whose estimated audience clears the practical floor, and (c) an angle that survives the swap test against every other role. Merge roles failing (b), cut roles failing (a), rewrite angles failing (c). Iterate until 100% of surviving roles pass all three - do not hand off a map that fails structurally.
- Outcome KPIs (after campaigns run, read with mbfinotti/advertising-skills@ad-audience-targeting's measurement):
  - Account penetration: distinct roles reached per target account vs. the map's role count.
  - Per-role engagement spread: a role whose proxy audience never engages is evidence against the hypothesis, so revisit its disproof test.
  - Downstream opportunity or meeting rate: on accounts where 2+ mapped roles were reached vs. one.
- Caveat to state in the map: per-role creative outperforming a single strong message is not proven by controlled evidence. The map is a testable structure, not a guaranteed lift - the KPIs above are how the user finds out which side of the precision-vs-reach dispute their market is on.

## References

- mbfinotti/advertising-skills@ad-audience-targeting - audience tiers, sizing, budgets, and test sequencing.
- mbfinotti/advertising-skills@lookalike-audience-seeds - seed list selection.
- mbfinotti/advertising-skills@retargeting-funnel - retargeting sequence design.
- mbfinotti/advertising-skills@ad-copy-variants - ad copy variants per angle.
