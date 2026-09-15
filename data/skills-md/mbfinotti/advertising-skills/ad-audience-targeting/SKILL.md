---
name: ad-audience-targeting
description: "Turn a business's ICP and buying signals into a layered ad audience targeting plan - cold/broad prospecting, interest and in-market behavioural segments, lookalike/similar, first-party lists, and retargeting pools - each sized against platform audience floors, budgeted to the learning threshold, and kept from overlapping by exclusion rules. Use whenever the user mentions ad targeting, who to target with ads, audience tiers or layers, broad vs. layered targeting, audience overlap between campaigns, or mapping an ICP onto ad audiences - even if they never say 'audience'. Covers B2B and B2C. Do NOT use to pick the seed customers behind a lookalike (mbfinotti/advertising-skills@lookalike-audience-seeds) or to sequence retargeting messages (mbfinotti/advertising-skills@retargeting-funnel)."
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.1.4"
---

# Audience Targeting

Map who the customer is (ICP) and what they do that signals intent (buying signals) into a layered paid-media targeting plan: which audience tiers to run, how each is defined, sized, budgeted, sequenced for testing, and kept from bidding against the others.

The tier logic, exclusion discipline, overlap math, and funding floors are identical for B2B and B2C. What differs (see the B2B vs. B2C section for detail):

- Universe size: B2B ICPs are often smaller than platform minimums.
- Which tiers dominate: B2B leans firmographic and list-based; B2C leans broad, lookalike, and behavioral.
- Cycle length.
- Success metric: pipeline quality vs. volume CPA/ROAS.

This skill produces the plan, not the platform setup. It places and sizes the retargeting tier but does not design the per-stage retargeting sequence (mbfinotti/advertising-skills@retargeting-funnel), and it assumes a seed list exists but does not select or build it (mbfinotti/advertising-skills@lookalike-audience-seeds).

## Evidence gate

- Never assert an ICP, a buying signal, or a tier without sourced data behind it: an ICP document, customer/CRM data, analytics, or past campaign results.
- Missing ICP → stop and request one (or a customer list to derive it from). Never invent an ICP from the product description alone; a plan built on an imagined customer optimizes toward fiction.
- Unknown attributes score neutral, never negative. Absence of evidence is not a negative signal; scoring it negative systematically buries accounts with a thin public footprint, which correlates with size, not fit.
- Record the evidence next to each tier in the plan (source and date), so the plan can be audited when performance surprises.

## Clarifying questions

Ask once, briefly, before planning; skip anything already answered.

1. B2B or B2C, and what does the ICP say - who buys, and what evidence backs it?
2. What counts as a conversion, and what is the target CPA (or ROAS)?
3. Roughly how many conversions per week does the account currently produce? (Sets the broad-vs-layered default.)
4. What first-party assets exist: customer list (size), site traffic volume, CRM, engaged followers?
5. What is the total monthly budget for this plan?
6. How large is the addressable universe - thousands of accounts or millions of consumers?
7. Does the offer touch a regulated category (housing, employment, credit, financial products, health, politics)?
8. By what date must results land - is there a hard deadline (launch, quarter close, seasonal window), or is the timeline open?
9. Do you want a one-off win this cycle, or a compounding asset that keeps paying after the campaign ends?
10. What is your effort ceiling - hours per week, who executes, and whether legal/privacy review is available to you at all?

The last three re-rank the tier plan before it is written. Say in the plan which answer moved which tier:

- Hard near-term date promotes first-party and retargeting tiers - they return readable evidence within days - and demotes cold broad, which needs a full learning cycle before it says anything.
- Compounding mandate promotes first-party list growth and cold broad: one builds a seed and a suppression asset the business keeps, the other trains a delivery model that improves with every conversion. A retargeting pool decays to nothing within weeks of the refill stopping.
- No privacy review available at all deletes every tier that needs identifiable data uploaded - first-party custom, and lookalike built from a customer seed - rather than ranking them last; they are not options for this account. A low effort ceiling on its own only demotes them, and promotes platform-native behavioral and broad tiers.

## Attributes vs. signals

The translation step everyone skips: an ICP lists _attributes_, a targeting plan runs on attributes _and_ signals. Distinguish them explicitly.

|            | Attribute - "what is true"                                      | Signal - "why now"                                                                  |
| ---------- | --------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Answers    | Is this person/account a fit?                                   | Why are they more likely to buy now?                                                |
| Examples   | industry, company size, role, age, geography, category interest | funding round, hiring spike, pricing-page visit, cart abandonment, seasonal trigger |
| Feeds      | tier membership, exclusion lists, firmographic filters          | tier priority, recency windows, test order                                          |
| Goes stale | slowly - refresh quarterly                                      | fast - has an expiry date                                                           |

- A signal older than ~90 days is context, never a trigger. Two fresh independent signals (e.g. funding + relevant hiring) outrank one stale one.
- Test for any candidate signal: given ten people/accounts that already pass the attribute filter, does it say which to reach first? If not, it's an attribute wearing a signal costume.

## The tier model

Every plan is assembled from these six tiers, ordered by efficiency - outcome bought per unit of effort - never by which is cheapest to stand up. Include a tier only when a real, evidenced signal defines it; an empty tier is a line item, not an audience.

- efficiency: `first-party custom > retargeting > lookalike > behavioral/in-market > cold broad > interest & affinity`
- value (volume of results the tier can produce at its ceiling): `cold broad > lookalike > behavioral/in-market > first-party custom > retargeting > interest & affinity`
- effort: `cold broad > retargeting > first-party custom == lookalike > behavioral/in-market == interest & affinity`
- compliance cost: `first-party custom > lookalike > retargeting > behavioral/in-market > interest & affinity == cold broad`

The axes disagree on purpose:

- Interest, the cheapest tier to stand up, is the least efficient one.
- Cold broad, the tier with the highest ceiling, is the most expensive to run and the slowest to read.
- First-party leads because a list the business already owns converts after an hour of setup. It also carries the heaviest consent, DPA and data-residency exposure of the six, which is what the compliance axis is there to price.

| Tier                                 | Defining signal                                                             | Effort to stand up                                                                                             | Volume vs. intent                                        | NOT for                                                    |
| ------------------------------------ | --------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- | ---------------------------------------------------------- |
| First-party custom                   | Owned data: customer/CRM list, site visitors, content engagers              | An hour - the list already exists; add a consent and data-residency check before upload                        | Mid-bottom funnel: low volume, high intent               | Prospecting scale                                          |
| Retargeting pool                     | Prior engagement with the business, graded by recency × depth               | A week or more of traffic or spend to fill the pool; near-zero to maintain afterwards                          | Bottom: lowest volume, highest intent                    | Proving the plan works - its ROAS is structurally inflated |
| Lookalike / similar                  | Statistical resemblance to a seed list                                      | An hour once a seed exists; sourcing the seed is a separate job                                                | Top-mid: high volume, intent quality tracks seed quality | Replacing retargeting; seeds of engagement-bait clickers   |
| Behavioral / in-market               | Category-level purchase-intent actions tracked by the platform              | An hour - platform-native segments, nothing to build or upload                                                 | Mid: medium volume, medium intent                        | Broad awareness reach                                      |
| Cold prospecting (broad/algorithmic) | None - the delivery algorithm selects using the account's conversion signal | A standing job - budget held above the learning threshold plus a continuous creative supply                    | Top: highest volume, lowest intent                       | Learning who the buyer is; tiny addressable universes      |
| Interest & affinity                  | Declared or inferred interests                                              | An hour - and largely spent for nothing; major platforms treat interest inputs as suggestions, not constraints | Top: high volume, weak intent                            | Precision reach - largely deprecated as a precision tool   |

- Default rung: fund first-party and retargeting first. Move up one rung - lookalike, then behavioral, then cold broad - as soon as the warm tiers saturate or the pipeline they draw on stops refilling. Warmer tiers are smaller and cheaper per result; colder tiers are what refills them, so a plan that funds only warm tiers eats its own pipeline within weeks.
- When site traffic is too thin for a retargeting pool, engagement audiences are the standard fallback seed, ranked by how fast they fill: `video viewers > content/profile engagers > lead-form openers`. A video-view pool reaches usable size in about a week of spend; a lead-form-opener pool can take one to three months of it.
- This ranking is a default, not a law - it shifts with context and with who executes it. Re-rank it against what you already know about the user before writing the plan:
  - An owned list of tens of thousands of customers promotes first-party above everything else.
  - Dense existing pixel traffic promotes retargeting.
  - An in-house data or analytics team promotes lookalike.
- A constraint the user actually stated does something different from re-ranking: it removes the tier. Delete any tier the answers rule out, and name it as deleted in the plan with the constraint that killed it and what would bring it back, for example:
  - "cold broad: deleted, addressable universe of a few tens of thousands, revive if the universe or the geography widens".
  - No privacy review deletes first-party and customer-seeded lookalike.
  - A regulated offer in a category that disallows lookalikes deletes that tier (see Compliance gate).

  A ruled-out tier left sitting at the bottom of the table is indistinguishable from one nobody considered, and it comes back next planning cycle as a fresh idea.

## Broad vs. layered: the judgment call

The most contested decision in this domain - present it as a conditional, never a doctrine. The ranking flips on one input, account data density, so it is stated twice rather than blended into a single misleading order:

- efficiency (new or thin-data account, narrow ICP or small universe, small budget, regulated offer): `explicit layers > parallel test > broad`
- efficiency (dense conversion data, large universe, budget that feeds the algorithm, goal is efficient scale): `parallel test > broad > explicit layers`

Default rung: explicit layers. The one condition that moves the plan up a rung is a campaign comfortably clearing its learning threshold - then run the parallel test, and adopt broad only if the duplicate wins.

| Posture                                                                    | You spend                                                                               | You get                                                                            | You give up                                                                   |
| -------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Explicit layers                                                            | A week to define tiers, then a standing job maintaining exclusions and refreshing lists | Attribution - reveals which segment actually responds                              | Reach the algorithm would have found on its own, plus the over-narrowing risk |
| Parallel test (duplicate one campaign, switch only the duplicate to broad) | An hour of setup plus one test cycle of budget on the duplicate                         | An account-specific answer instead of someone else's general one, fully reversible | One cycle of delay before committing either way                               |
| Broad / algorithmic                                                        | Near-zero to set up, but sustained budget density across a full learning cycle          | Efficient scale wherever the universe is genuinely large                           | Any knowledge of who the buyer is; wasted reach when the real market is small |

Where the evidence sits:

- **The broad camp:**
  - Ben Heath reports open/broad targeting "often (but not always) outperforms interest targeting", especially on "mature ad accounts with decent conversion data".
  - Demand Curve independently backs broad as "the opposite of traditional marketing wisdom" that works.
  - Platform vendors publish self-reported data agreeing; treat those numbers as marketing.
- **The layered camp:** B2B practitioners (B2Linked among them) caution against automatic audience-expansion features - with a narrow, well-defined ICP, letting the platform broaden the audience "to anybody and everybody" wastes budget.
- **The middle:** Heath himself rejects the "kill retargeting entirely" camp as "the more extreme view" - even broad-first accounts keep first-party and retargeting tiers.

- Never flip an account wholesale on general advice; the parallel test is the only honest way to change rungs, and it keeps the layered control running while it decides.
- Broad hides who the buyer is. Keep at least one manually-defined tier alive as a research instrument even when broad wins on cost.
- Over-narrowing is the named failure mode of the layered camp: stacking many interests plus demographic filters produces a small, expensive audience that sees an unchanged ad. If the ICP knowledge is rich, spend it on creative variants per segment, not on more filters.

## Sizing and funding floors

A tier that can't be funded to significance doesn't belong in the plan.

1. Size each tier and check it against the platform's minimum audience size ([references/platform-notes.md](references/platform-notes.md) - load when the user names their platform; platform floors change without notice, so verify against current platform docs).
2. Compute each tier's budget floor from the platform's learning threshold: daily floor ≈ (target CPA × weekly optimization-event threshold) ÷ 7. The most widely cited threshold is ~50 events per ad set per week. An ad set at $30/day against a $50 CPA yields ~4 conversions a week - it will never exit learning; merge it, or optimize to a higher-funnel event.
3. Below the size floor or the budget floor, fix it in this order - efficiency: `merge upward > cheaper proxy event > cut`.
   - **Merge the tier into its nearest neighbour** - an hour of rebuilding exclusions, and it keeps both the audience and the delivery. Try this first.
   - **Optimize to a cheaper higher-funnel event** - an hour plus a relearning cycle, and it buys delivery at the price of a softer success metric to reconcile against the real one afterwards.
   - **Cut it** - near-zero effort, buys nothing, but stops the waste. Never keep an unfundable tier "for coverage".
4. Small audiences also cost more per impression - AJ Wilcox's warning that "SUPER small audiences will make you pay out the nose" generalizes across platforms.
5. Starting split: 70-80% prospecting tiers, 15-25% retargeting, remainder experimental. Retargeting above ~40% of spend is a signal to grow prospecting, not evidence retargeting "works" - over-funding it inflates blended ROAS while starving the pool refill.
6. Splits shift by stage: launches run 80-90% prospecting; mature high-traffic brands can justify heavier warm spend.

## Overlap and exclusion discipline

Two funded tiers bidding on the same person compete against each other in the auction, inflating cost without adding reach.

- Exclusions run before inclusions - platforms prioritize exclusion criteria, so build the exclusion matrix first.
- Everywhere: exclude existing customers (unless the campaign is expansion/upsell), employees, and known competitors.
- Between tiers: exclude each higher-intent tier from every lower-intent tier - retargeting pool out of lookalike and prospecting, customer list out of everything. Each person sits in exactly one tier.
- Use first-party suppression lists for this. Interest-based _exclusion_ features are deprecated or removed on major platforms; customer/converter suppression via uploaded lists remains standard practice.
- Overlap thresholds between two funded tiers:
  - Under 10%: ignore.
  - 10-30%: monitor.
  - 30-50%: act.
  - Over 50%: merge the tiers.

  Audit overlap before launching any new tier, not only when troubleshooting.

- In the 30-50% band, `add an exclusion > consolidate`: an exclusion is an hour of work and reversible in one click, while consolidating destroys the per-tier read the test budget was paying for. Consolidate only when the exclusion would push either tier near its size floor.
- The opposite failure exists too: stacking exclusions until the audience drops below the platform floor silently halts delivery. After building the matrix, re-check every tier's post-exclusion size.

## Test sequencing

1. Fund in the tier model's efficiency order, restated here because this is where the money actually moves - efficiency: `first-party > retargeting > lookalike > behavioral > cold broad` (an interest tier, if funded at all, goes last). Speed of signal ranks nearly the same, which is why the order holds under a deadline: `first-party == retargeting > lookalike > behavioral == cold broad`.
2. Test with a fixed budget per audience so every tier actually gets spend; move proven winners into algorithmic budget pooling to scale. Algorithmic pooling during testing starves the very tiers the test is meant to read.
3. Run the broad-vs-layered parallel test (above) as its own experiment - one variable at a time.
4. Scale winners at most ~20% budget per week; larger jumps are widely treated as learning-resetting edits, though no platform documents a fixed percentage.
5. Decision rule per tier after each cycle, stated in the plan before launch: promote (beats target, scale ~20%), hold (within ±20% of target or still learning, keep collecting), kill (2× target CPA spent with results 50%+ worse than the best funded tier, or delivery stalled below floors).

## Compliance gate

A hard gate before spend, not a review. Rules differ by jurisdiction and platform but converge on:

- Sensitive/protected traits - health, ethnicity, religion, political views, sexual orientation, financial hardship - cannot be targeted on or inferred, even from a public signal. Major platforms have removed these categories outright.
- Regulated offer categories (housing, employment, credit, financial products, politics) trigger restricted targeting modes: demographic and geographic narrowing disabled, lookalikes often disallowed. Plan those campaigns as broad-plus-creative from the start.
- EU delivery adds consent requirements (expect a meaningful share of tracking signal to be absent), a ban on profiling-based ads to minors, and a ban on sensitive-data targeting that user consent cannot override.
- Signal loss is structural: a share of conversions is invisible to pixels regardless of consent choices elsewhere. Prefer server-side conversion feeds where available, and never judge tiers on pixel-only numbers when a source-of-truth (CRM, orders) exists.
- Any regulated-category campaign routes through legal/compliance before launch.

## B2B vs. B2C

| Dimension                | B2B                                                                                             | B2C                                                   |
| ------------------------ | ----------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| Dominant tiers           | Firmographic professional-network targeting, account lists, first-party CRM                     | Broad/algorithmic, lookalike, behavioral, retargeting |
| Universe                 | Small; often near or below platform floors                                                      | Large; feeds algorithms well                          |
| Broad-vs-layered default | Layered - a tiny universe makes algorithmic expansion wasteful                                  | Broad, once conversion data is dense                  |
| Buyer                    | Committee, not an individual (map roles via mbfinotti/advertising-skills@ad-buyer-group-mapper) | Individual                                            |
| Cycle                    | Weeks to quarters - judge on downstream pipeline quality, not lead volume                       | Hours to days - CPA/ROAS readable quickly             |
| Known trap               | Audiences too small to exit learning; cheap-lead optimization collapsing lead quality           | Creative fatigue and seasonality, not targeting       |

- B2B corollaries:
  - Broaden role targeting from exact titles to function + seniority when the title universe is too small.
  - A tiny universe (a few tens of thousands) often runs better as one consolidated campaign than as a tiered split.
- Everything else in this skill - evidence gate, attribute/signal translation, exclusion matrix, funding floors, test sequencing, compliance - applies to both unchanged.

## Output shape

Deliver the plan as one document:

1. ICP summary with evidence sources, split into attributes and signals.
2. Tier table: tier | defining signal (with evidence) | est. audience size | exclusions applied | test budget /day | success criterion - rows ordered by efficiency, with a line stating any re-rank and what in the answers caused it, and a line naming every tier deleted and the constraint that deleted it.
3. Exclusion matrix: each exclusion list × which tiers it applies to.
4. Test sequence: order, duration, the one variable each test isolates, and the promote/hold/kill rule. State why the order departs from the default whenever it does.
5. Compliance notes: regulated flags and what they force.
6. Review cadence:
   - Overlap audit before any new tier launch.
   - Tier performance vs. floors weekly during testing.
   - Seed/list refresh every 30-60 days (stale seeds quietly degrade lookalikes).
   - Full plan review quarterly or on ICP change.

See [references/worked-example.md](references/worked-example.md) for a filled-in B2B plan, a B2C plan, and a negative example.

## Failure modes

- Over-segmentation: many small ad sets below the learning floor. Consolidation regularly halves cost per result on the same budget.
- Interest over-stacking: precision theater - a small, costly audience and no better creative.
- Retargeting worship: its high reported ROAS is largely non-incremental (many of those users would have converted anyway); never let it crowd out prospecting.
- No exclusion matrix: tiers silently bid against each other and against the customer base.
- Exclusion overreach: stacked exclusions drop a tier below the floor and delivery stops.
- Stale inputs: signals older than 90 days treated as triggers; seed lists never refreshed.
- Attributing creative effects to targeting (and vice versa): change one variable per test, or the result teaches nothing.
- Trusting broad on a tiny universe: the algorithm expands to irrelevant reach because the real market can't absorb the spend.

## Objective and measurement

- Structural pass (before launch): 100% of funded tiers clear both the platform size floor and the budget floor, and no funded tier pair overlaps above 30% without a documented exclusion. If any tier fails, merge or cut and re-check - do not launch a plan that fails structurally.
- Outcome pass (after the first full test cycle): every funded tier has a promote/hold/kill verdict backed by data, and the cost-per-result spread between best and worst surviving tier exceeds ~30% - a spread that wide is actionable; a flat spread means the tiers weren't meaningfully different, so consolidate and re-plan.
- Ongoing KPIs:
  - Blended CPA/ROAS against target.
  - Prospecting share of spend (hold ≥60% unless deliberately harvesting).
  - Overlap % between funded tiers.
  - For B2B, downstream lead quality (MQL→SQL or equivalent) per tier - a tier winning on CPL and losing on quality is a kill, not a promote.
- Iterate the plan until both passes hold.

## References

- [references/worked-example.md](references/worked-example.md) - filled-in B2B and B2C targeting plans in the output shape, plus a negative example.
- [references/platform-notes.md](references/platform-notes.md) - vendor-specific size floors, learning thresholds, and mechanics, with sources. Load only when the user names their platform.
- mbfinotti/advertising-skills@lookalike-audience-seeds - seed list selection; this skill assumes a seed exists but does not select or build it.
- mbfinotti/advertising-skills@retargeting-funnel - retargeting sequence design (per-stage messaging, windows, frequency caps); this skill places and sizes the retargeting tier but does not design the messaging sequence.
- mbfinotti/advertising-skills@ad-buyer-group-mapper - B2B buying-committee mapping for multi-role audiences.
- mbfinotti/advertising-skills@thought-leadership-ads - person-fronted amplification campaigns that consume this plan's audience tiers.
- mbfinotti/advertising-skills@ad-spend-allocation - cross-campaign budget allocation across multiple initiatives.
- mbfinotti/advertising-skills@ad-platform-selection - channel choice and platform mechanics that affect tier-level targeting options.
