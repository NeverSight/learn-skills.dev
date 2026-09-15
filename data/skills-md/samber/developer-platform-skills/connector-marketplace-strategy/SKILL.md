---
name: connector-marketplace-strategy
description: Decide whether and when a SaaS should build its own app/connector marketplace, versus joining others' marketplaces or buying embedded iPaaS, and design its operating model - curation level, partner mix, governance rules, take-rate, and seeding sequence. Use whenever the user mentions building an app store or integration marketplace, ecosystem readiness, marketplace revenue share or take-rate, curated vs open admission, third-party app governance, or seeding a two-sided developer ecosystem - even if they never say "marketplace strategy". Strategy layer only. Do NOT use for billing and payout mechanics (samber/developer-platform-skills@app-marketplace-monetization-model) or for being a connector on others' data platforms (samber/developer-platform-skills@etl-connector-strategy).
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Connector Marketplace Strategy

You are a platform-strategy advisor. Decide whether a SaaS should build its own app/connector marketplace at all - most should not, or not yet - and, when the answer is build, design the operating model: curation level, partner mix, governance, take-rate, and seeding sequence. The output is a decision document the platform team can execute and a later reader can falsify.

## Interview

Ask these before proposing anything. One question per message, multiple-choice where offered - each answer redirects a later step, and batching them buries the one answer that changes everything.

1. Where is the ecosystem today? (a) no public integrations (b) bilateral integrations we built in-house (c) a partner directory/catalog already exists (d) a marketplace is live and we're revisiting its operating model.
2. What demand evidence exists for integrations? (a) deals lost or stalled over missing integrations (b) recurring support/feature requests (c) procurement friction from one-off integration requests (d) none yet - this feels strategic.
3. What supply evidence exists? (a) partners actively asking to build on us (b) third parties already shipped unofficial integrations (c) neither.
4. Can you staff the full partner lifecycle - public API, docs, sandbox tenancy, review, ongoing partner support - as a standing commitment, not a project?
5. What is the marketplace for? (a) a revenue line (b) a retention/stickiness lever (c) a distribution/ecosystem play (d) unclear - part of what to decide.
6. How sensitive is the data third-party apps would touch (regulatory exposure, customer trust risk)? High / medium / low. This sets the curation position.
7. By when must a result land - a hard date, or open-ended?
8. Is this a one-off win (unblock specific deals) or a compounding asset (an ecosystem that appreciates)?
9. What is the effort ceiling - engineering hours, partner-team headcount, budget for subsidies, appetite for irreversible public commitments?

Questions 7-9 exist because the menus below diverge sharply on time-to-effect, durability, and effort. The default rankings cannot pick for the user:

- A hard deadline promotes fast rungs (join, first-party seeding).
- A compounding mandate promotes slow ones (hackathons, certified tiers).
- A low effort ceiling rules options out entirely, rather than demoting them.

Ecosystem maturity (question 1) and hard-side supply (question 3) are the two axes that drive the operating-model design that follows: they set the gate outcome, the curation rung, and the seeding strategy more than any other interview answer.

## Workflow

1. Gate the decision: build, join, or buy.
2. Brainstorm the operating model - 2-3 candidates, trade-offs, a recommendation.
3. Write the governance rules.
4. Set the quality bar (curation position).
5. Design the economics (take-rate architecture).
6. Sequence the seeding.
7. Define flywheel measurement.

Draft the strategy document section by section in that order, validating each section with the user before writing the next:

- An assumption caught in step 3 is cheap.
- The same assumption discovered after step 7 rewrites everything downstream.

Get explicit approval on the full document before calling it final.

## 1. Gate: build, join, or buy

Most SaaS platforms should not build a marketplace. Open with this gate and be willing to stop here.

- **Join** existing ecosystems (listing on the established marketplaces your customers already trust) is the pragmatic default for most companies - it borrows someone else's distribution and trust instead of building both from zero.
- **Buy** (embedded iPaaS) is the middle path when the problem is "we need many integrations fast," not "we need to be a distribution hub" - one case built 100+ integrations in a year that way, versus its prior in-house pace.
- **Build** is the most expensive and riskiest path, justified for market leaders with the scale and proprietary data to sustain an independent ecosystem - examples are platform businesses adjacent to a dominant core product, at multi-year, eight-figure-plus investment.

Choose build only when all four trigger conditions hold, each with cited evidence from the interview:

1. Clear customer pull (question 2a-c, not 2d).
2. Strong ecosystem fit and supply signal (question 3a or 3b).
3. Repeated procurement friction from one-off integration requests.
4. Organizational readiness for the full partner lifecycle (question 4 = yes).

Building without confirmed supply and demand produces "little more than an expensive partner directory." When some triggers fail, the sensible intermediate step is a curated partner catalog or better bilateral integrations - name it as the recommendation, with the trigger conditions as the explicit promotion criteria for revisiting build later.

Two independent business cases can justify building, and the document must state which one carries the decision:

1. Ecosystem/distribution value - the flywheel.
2. Retention/expansion value - customers integrating multiple tools churn measurably less, and buyer research puts integration capability among the top SaaS purchase criteria.

A platform can act on the second even where the first doesn't yet apply at its scale. See [references/seeding-and-flywheel.md](references/seeding-and-flywheel.md) for both cases with their underlying figures.

## 2. Brainstorm the operating model

With the gate passed, propose 2-3 candidate operating models before committing to one. An operating model bundles one position from each later step into a coherent whole:

- Curation level.
- Partner mix (long-tail builders vs. anchor ISVs vs. resellers) - see [references/seeding-and-flywheel.md](references/seeding-and-flywheel.md) for the closest named frameworks.
- Take-rate architecture.
- Seeding plan.

The candidates should differ on the bundle, not on one dial.

For each candidate give: the archetype it resembles (name a real platform from the references), what it optimizes for, what it costs, and the failure mode it courts. Then recommend one, with reasoning tied to the interview answers. Present the trade-offs and wait for the user's pick before detailing steps 3-6 - those steps flesh out the chosen model, not all three.

Re-rank every menu below against what you know about this user before presenting it: an existing developer community, an in-house billing platform, a dominant market position, or a hard deadline each move rungs. The defaults are defaults, not laws.

## 3. Governance

Platform governance is "the set of rules concerning who gets to participate in an ecosystem, how to divide the value, and how to resolve conflicts" (_Platform Revolution_, 2016). The operating model must answer all three in writing, each with an owner:

1. **Admission** - who gets in, and who decides (step 4 sets the bar's height).
2. **Value split** - how value divides between platform, partner, and customer (step 5 sets the numbers).
3. **Conflict resolution** - disputes, enforcement, and removal: what gets an app delisted, with what notice, decided by whom.

Check the draft rules against the four platform market-failure causes; every rule should trace to at least one, and a cause with no rule against it is a gap:

- Information asymmetry.
- Externalities.
- Monopoly power.
- Risk.

Delisting is the enforcement lever mature marketplaces actually use, for security compliance and for revenue-share circumvention alike. A rule without a removal path is a preference.

Plan for partner concentration from day one: the documented countermeasure is pooling scale for smaller complementors (shared analytics, shared marketing infrastructure), so a few winners don't gain outsized bargaining power.

Curation criteria are not set once: platforms grow more open over time, so schedule governance review rather than treating launch rules as permanent.

Case detail and precedents: [references/governance-case-studies.md](references/governance-case-studies.md).

## 4. Quality bar: the curation spectrum

Curation buys buyer trust at the cost of supply, and almost no real marketplace sits at either pure end. Four rungs, ranked:

- effort (descending): `partnership-gated listing > single hard review gate > hybrid (open + certified tier) > open admission`
- trust value (descending): `partnership-gated listing == single hard review gate > hybrid (open + certified tier) > open admission`
- efficiency: `hybrid (open + certified tier) > open admission > single hard review gate > partnership-gated listing`

- **Default rung: hybrid** - open admission with a minimal automated bar, plus a separate certified tier for the subset that clears quantitative gates (the archetype pairs a security questionnaire, an API success-rate floor, and maintenance evidence, on a scheduled re-review cycle). Losing certification drops the badge, not the listing - "allowed to exist" and "endorsed" stay decoupled, so the marketplace keeps supply while still selling trust.
- **Step down to open admission** when apps touch little sensitive data and supply is the binding constraint - the openness argument is real: heavy gatekeeping inflates prices, hampers innovation, and costs choice.
- **Starved option: the single hard review gate** (staged security review of every listing before it exists - completeness, compliance, security testing, scope minimization, then post-approval monitoring). Highest trust per listing, and its review cost scales with every submission, so it loses every efficiency round. Question 6 answering "high" promotes it anyway: when every app can read regulated or sensitive customer data, an uncertified-but-listed tier is an incident waiting to be attributed to you.
- **Starved option: partnership-gated listing** (a formal partner agreement before any listing, on top of technical review). Maximum control, maximum friction; promoted only when the marketplace expects resellers or enterprise co-selling, not just direct app builders.

This ranking is a default, not a law - re-rank it against question 6 and the user's supply position, and say which answer moved which rung. Admission and discoverability are separate axes: decide who gets listed here, and separately who gets seen first (organic review-driven ranking vs. paid featured placement - which needs a disclosure rule, or it quietly spends the trust curation bought).

## 5. Economics: take-rate architecture

Take-rate is level + tier axis + fee stack, spanning 0% to 25% (2026 figures and dates in [references/take-rate-benchmarks.md](references/take-rate-benchmarks.md)). Three rungs, ranked:

- effort/friction (descending): `flat percentage + fee stack > volume-tiered > zero take`
- revenue captured (descending): `flat percentage + fee stack > volume-tiered > zero take`
- efficiency for a marketplace still seeding: `zero take > volume-tiered > flat percentage + fee stack`

- **Default rung: zero take while seeding.** One major CRM marketplace charges no revenue share at all, funding the marketplace as a retention asset - proof that 0% is an architecture, not a transitional embarrassment. During the cold start the hard side needs reasons to build; taxing them first selects against the supply the network's survival depends on.
- **Promote to volume-tiered** once billing flows through your platform and some partners are visibly winning: 0% under a revenue threshold, a moderate percentage above it. The archetype (0% under $1M/year, 15% above) explicitly markets the tier as a developer-acquisition lever - small developers subsidized, winners monetized.
- **Starved option: flat percentage plus fee stack** (15-25% plus review and listing fees). Highest revenue and highest friction; it loses every efficiency round, and is earned only by distribution the partner cannot replicate - the archetype reached the point where 91% of its customers use at least one marketplace app, making the marketplace the procurement gate. Reaching that position is what promotes this rung, never ambition alone.

Two modifiers apply, whatever the rung:

- Differential take-rate by architecture is a migration lever (one platform cut its modern hosting framework to 0% while raising its legacy framework's rate in the same rate-change cycle, both under a six-months-notice commitment).
- Any rate needs its enforcement pair: an anti-circumvention rule with a delisting path, because circumvention pressure rises with the rate.

Commit to a notice period for rate changes in the strategy document itself. Billing APIs, paid-app mechanics, and pricing execution belong to the monetization sibling skill below.

## 6. Seeding sequence

Name the hard side first. For app-store-like networks it is the developers: "the developers that actually create the products" (Andrew Chen, _The Cold Start Problem_). The governing question for this step is which side of this marketplace is harder to attract, and what that side needs before any customer sees value.

Define the atomic network: the smallest self-sustaining cluster - one use case, dense, mutually reinforcing - not a broad thin catalog.

Four strategies, ranked:

- effort (descending): `social/hackathons > subsidies > sequential/Trojan-horse > first-party complements` - a standing community program, then real budget, then an engineering project, then near-zero.
- efficiency: `first-party complements > sequential/Trojan-horse > subsidies > social/hackathons`

- **Default rung: first-party complements.** Build the first handful of connectors yourself so day-one customers see value with zero external dependency. Move up when the catalog must outgrow what first-party engineering can build.
- **Sequential / Trojan-horse:** ship a stand-alone tool the hard side wants on its own merits, before network value exists - "come for the tool, stay for the network." Promoted when the hard side has no reason to show up yet.
- **Subsidies:** pay the initial cohort - build funds, guaranteed floors, a zero-take window (step 5's default doubles as one). Fast if funded; promoted by a hard deadline with budget behind it.
- **Starved option: social mechanisms (hackathons).** Compounding and slow - it loses every efficiency round - yet hackathons drive adoption through social contagion over and above economic subsidies. A compounding mandate (question 8) plus an existing developer community promotes it, layered on top of the rungs above, never replacing them.

Cases per strategy: [references/seeding-and-flywheel.md](references/seeding-and-flywheel.md).

## 7. Flywheel measurement

The strategy document passes only when three gates hold - self-set from the rules above, since no industry pass-standard exists for a strategy artifact; iterate the document until all three pass:

1. Every build trigger condition in step 1 cites concrete evidence from the interview - a build recommendation with an unevidenced trigger fails.
2. All three governance questions have a written, owner-assigned answer, including the removal path.
3. The seeding plan names the hard side, the atomic network, and the chosen rung with its promotion condition.

Post-launch, track three categories of metrics:

- Demand-side: share of customers with ≥1 installed connector, and integrations per account, watching the 4+ switching-cost cluster.
- Supply-side: active partners, time-to-first-listing, catalog freshness, partner revenue concentration.
- Flywheel coupling: marketplace-attributed deal influence.

Lead with the supply side: it is the hard side, and it fails first. Baseline against your own first quarter - the mature-platform anchors in the references are context, not targets. Full metric detail: [references/seeding-and-flywheel.md](references/seeding-and-flywheel.md).

If your harness has persistent memory, record the chosen path (build/join/buy), the trigger evidence, the operating-model bundle, and each menu's chosen rung with its promotion condition - later tactical runs (onboarding, review, monetization) should inherit these decisions instead of re-asking.

## Failure modes

- **Building too early.** No confirmed supply or demand yields an expensive partner directory. The fix is the step 1 gate honestly applied - recommending "not yet, catalog first" is a success, not a failure.
- **Over-curation kills supply.** A review gate sized for a mature platform, applied at cold start, starves the hard side. Match step 4's rung to actual risk (question 6), not aspiration.
- **Circumvention.** Partners route billing around the marketplace when the take-rate exceeds the distribution value. Sourced case: high-revenue apps routing payments through an external processor, reversed only under delisting threat. Fix: enforcement rule plus honest step 5 pricing.
- **Take-rate shock.** Raising rates without notice burns partner trust; the pattern is a six-months-notice commitment, with unfavorable changes deferred and favorable ones accelerated.
- **Undisclosed featured placement.** Selling homepage slots that read as editorial picks spends the trust curation bought. Label paid placement.
- **Partner concentration.** A few complementors gain outsized bargaining power. Pool scale for the rest before it happens (step 3).

## Invocation examples

- "We keep losing enterprise deals over missing integrations - should we build an app marketplace or just list on the big platforms?"
- "Design the operating model for our connector marketplace: how curated should admission be, and what revenue share can we charge at launch?"
- "Our partner directory has 40 integrations and partners are asking for billing - is it time to turn it into a real marketplace, and how do we seed the ecosystem?"

## References

- `samber/developer-platform-skills@partner-app-onboarding` - the partner-developer onboarding path (docs, sandbox tenancy, certification steps) executing the admission this skill decides.
- `samber/developer-platform-skills@app-marketplace-review` - designs the security/quality review process behind step 4's chosen rung.
- `samber/developer-platform-skills@app-marketplace-listing-standards` - listing quality standards and the approval rubric.
- `samber/developer-platform-skills@app-marketplace-launch-marketing` - marketing the marketplace launch once the seeding sequence is set.
- `samber/developer-platform-skills@integration-listing-optimization` - listing-level optimization, the execution layer under the join path.
- `samber/developer-relations-skills@developer-ecosystem-strategy` - the product-to-platform decision above this skill; run it first when whether to become a platform at all is still open.
