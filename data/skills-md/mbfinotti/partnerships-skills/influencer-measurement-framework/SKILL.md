---
name: influencer-measurement-framework
description: Design the pre-launch measurement plan for one influencer or creator campaign - KPIs matched to the objective (awareness, engagement, conversion, affiliate-linked, always-on ambassador), an attribution method and data source behind each KPI, reporting cadence per stakeholder, and declared blind spots. Delivered as a measurement plan document before launch, for B2B and B2C alike. Use whenever the user mentions influencer KPIs, creator campaign attribution, campaign reporting, or asks how to measure a creator partnership, even if they never say measurement. Do NOT use for an ongoing affiliate program dashboard - use mbfinotti/partnerships-skills@affiliate-performance-dashboard instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.4.4"
---

# Influencer Measurement Framework

Design how one influencer/creator campaign will be measured - before it launches - and deliver a measurement plan document. The plan, not a dashboard or a report, is the artifact: it fixes KPIs, attribution methods, data sources, cadence, and blind spots so the post-campaign readout is decided in advance, not improvised after.

Influencer measurement has no comprehensive, benchmark-bearing standard behind it. Say this plainly to the user, and never present a branded framework as an industry standard.

The method borrows only genuinely established pieces:

- **ANA Influencer Marketing Measurement Guidelines** (June 2022, MRC-endorsed): standardized definitions only, without benchmark figures.
- **AMEC Barcelona Principles** (3.0 July 2020, reaffirmed 4.0 June 2025): Principle 5, "AVEs are not the value of communication".
- **MRC viewability standard**: 50% of pixels, 1s display / 2s video; most organic platform metrics fail it.
- **IAB Tech Lab Podcast Measurement Technical Guidelines v2.2** (May 2, 2024): for podcast/newsletter sponsorships.
- **Incrementality via geo-lift/synthetic control** (Meta's open-source GeoLift package, Google's CausalImpact): paired with a Minimum Detectable Effect power check.

## Ground Rules

- Match the primary KPI to the campaign objective's funnel stage. Optimizing an awareness campaign on conversion metrics, or the reverse, is the single most-cited practitioner error.
- Give every KPI a one-sentence definition naming numerator, denominator, and window. A metric nobody can recompute is decoration.
- Pick one engagement-rate denominator and one attribution window; hold both constant for the whole campaign and label them in the glossary.
- Never report EMV, MIV, or any AVE derivative as ROI or financial value - relative, same-vendor directional comparison is their only legitimate use.
- Never adopt a vendor benchmark as a target. Targets come from the program's own trailing history, or the plan honestly says "first flight - no target, baseline-setting run."
- Never use the "$5.78 per $1" figure (or its variants) as a planning input - it is a vendor benchmark with weak, inconsistent provenance.
- Triangulate attribution: no single method is reliable alone. Codes leak, links get stripped, pixels lose signal, surveys mis-remember - each covers another's blind spot.
- Provenance-tag every number the plan cites: standards-body definition, platform-published, vendor-sourced, single-practitioner claim, or the brand's own history.

## Interview

Ask before designing anything. One question per message; multiple-choice where possible; skip anything already answered.

- Campaign objective and funnel stage: awareness/reach, consideration/engagement, conversion/performance, affiliate-linked, or always-on ambassador?
- B2B or B2C? (Drives revenue object, window length, and which attribution signals exist at all.)
- Budget and program size: total spend, number of creators, one flight or always-on?
- Platforms in play? (Short video, image/social, long video, live, podcast, newsletter - each has different data access.)
- Deliverable types per creator? (Posts, stories, videos, streams, podcast reads, newsletter placements.)
- Which tracking capabilities actually exist today: unique promo codes, UTM-tagged links, affiliate network, platform pixel/shopping, post-purchase survey, CRM "how did you hear about us" field? (Multi-select; "none" is a valid answer.)
- Does a pre-launch baseline exist - trailing branded-search volume, direct traffic, follower and engagement history? If not, is there time to capture one before launch?
- Who reads the report, and what decision does it drive? (Renew the creator, reallocate budget, prove channel viability to finance, creative learnings.)
- What reporting cadence is expected, and by whom?
- What creator-side analytics access is contractual: API/account connection, platform partnership tooling, or screenshots only?
- By what date must the result land, and what decision is waiting on it? (A hard date promotes the near-zero-setup rungs - codes, UTMs, the branded-search proxy - and rules out geo-lift and panel brand-lift studies, which report after the decision is already made.)
- One-off readout for this flight, or a measurement asset reused every flight? (Compounding promotes the post-purchase survey, the affiliate network and a reusable geo design - each costs its setup once and pays every flight after. One-off keeps the stack at codes + UTMs + baseline proxy.)
- Effort ceiling: analyst hours available, whether checkout can be changed, whether ad spend can be committed to a holdout, and whether the channel can be withheld from whole regions?
  - No checkout change demotes the survey and the pixel.
  - No willingness to withhold deletes geo-lift and conversion-lift holdouts from the menu.
  - No analyst on hand promotes platform-run test designs above self-run ones.

## Workflow

1. Run the Interview; collect every answer the plan depends on.
2. Fix the objective, then select the KPI set for that objective from [references/kpi-definitions.md](references/kpi-definitions.md) - primary, secondary, guardrail. Refuse a primary KPI from the wrong funnel stage; explain why instead of complying.
3. Write the metric glossary before anything else: one-sentence definition per KPI, the chosen engagement-rate denominator, the attribution window, and the view definition per platform. Platform "view" definitions changed materially in 2025-2026, so date-stamp them; if you can browse the web, verify current platform definitions - otherwise flag them as "as of plan date, re-verify".
4. Map each KPI to an attribution method and a data source the Interview confirmed exists, using [references/attribution-and-data-sources.md](references/attribution-and-data-sources.md). Cut or flag any KPI with no feasible source - a KPI backed by a capability the brand lacks is fiction.
5. Assemble the attribution stack in efficiency order: coverage and confidence bought per hour of setup, never per method's apparent rigour. Default order:

   a. Unique promo codes and UTM-tagged links together: an hour each, per-creator resolution from day one. The pair is the floor; a single-method stack is not triangulated.
   b. A one-question post-purchase/post-signup survey: a week to ship through whoever owns checkout, near-zero effort forever after, the only method that sees dark social.
   c. Affiliate-network links: near-zero when a platform is already live, a standing job of contracts and onboarding when it is not.
   d. Per-creator vanity URLs: narrow coverage, the only rung that exists on podcast and newsletter placements.
   e. Platform pixel/shopping last: engineering plus consent work, for a lossy signal the platform grades itself.

   ```
   effort:          pixel > affiliate network > survey > vanity URLs > promo codes == UTM links
   coverage:        survey > affiliate network > promo codes == UTM links > pixel > vanity URLs
   compliance cost: pixel > survey > affiliate network > promo codes == UTM links == vanity URLs
   efficiency:      promo codes == UTM links > survey > affiliate network > vanity URLs > pixel
   ```

   Codes and links tie because they cover different slices: a code survives being screenshotted or read aloud; a tagged link does not. This order is a default, not a law; it shifts with the brand's existing stack and with who has to build each rung.

   Re-rank against the Interview answers, and write in the plan which answer moved which rung:

   - An affiliate platform already running jumps to rung (a) at near-zero incremental effort.
   - A checkout survey already collecting responses is already rung (a).
   - A store that cannot issue unique per-creator codes drops half of (a) and promotes the survey.
   - A podcast or newsletter flight has no rungs available but codes and vanity URLs.

   Note each method's known failure and the code-leakage policy beside it in the plan.

6. Capture or schedule the pre-launch baseline; if launch precedes capture, write "no baseline - post-campaign lift claims will be unsupported" into the plan rather than hiding it.
7. Decide the test design with [references/incrementality-and-brand-lift.md](references/incrementality-and-brand-lift.md). Run the MDE power check first: an hour of analyst time that gates every rung below it, and the one step here with no alternative. Then take the highest rung the power check _and_ the effort ceiling both allow:

   a. Branded-search and direct-traffic movement against the pre-launch baseline: near-zero effort, correlational. It belongs in every plan including the powered ones, since it is the series that survives when the test does not.
   b. Geo-lift/synthetic control: the strongest causal evidence available without user-level identifiers, priced in analytics skill, a quarter of calendar time, and the political capital to withhold the channel from real markets.
   c. Platform conversion-lift holdout: the platform runs it, so less work than (b), but it needs ad spend on that platform and the platform grades its own homework.
   d. Platform-run brand-lift study: attitudes rather than behaviour, a spend minimum, 1-4 weeks of in-flight surveying, same self-measurement conflict.
   e. Independent-panel brand lift: cross-platform and conflict-free, and a standing job to commission.

   Below power on every rung above (a), write "directional measurement only" into the plan.

   ```
   effort:            panel lift > geo-lift > platform brand lift > conversion-lift holdout > search proxy
   time to an answer: panel lift == geo-lift > platform brand lift == conversion-lift holdout > search proxy
   evidence strength: geo-lift == conversion-lift holdout > panel lift > platform brand lift > search proxy
   compliance cost:   panel lift > platform brand lift > conversion-lift holdout > geo-lift == search proxy
   efficiency:        search proxy > geo-lift > conversion-lift holdout > platform brand lift > panel lift
   ```

   Default rung: (a) alone. Geo-lift and panel lift are what this order starves: the first buys the strongest causal evidence available, the second the only conflict-free one, and both lose every round to a proxy series that costs nothing. A plan run on the ratio alone never produces a causal number at all.

   Move up a rung on these conditions:

   - The power check passes _and_ the decision the report drives is a budget-size one: move up one rung, since proving the channel to finance justifies a quarter of work.
   - The claim has to survive the platform that sold the media grading its own work: reach panel lift.
   - The decision is a rebook or a creative learning: stay at (a).

   This order is a default, not a law. Re-rank on the Interview answers:

   - An awareness-primary campaign with no conversion volume skips (b) and (c) entirely, because brand lift is the only instrument that measures its objective at all.
   - An in-house analytics team collapses (b)'s effort and promotes it above (c).
   - A brand that will not withhold the channel from any region deletes (b) and (c) from the menu rather than demoting them.

8. Set reporting cadence per stakeholder - each row names who, how often, which metrics, and the decision it drives. A report driving no decision gets cut.
9. Declare blind spots explicitly: dark social, view-through, stripped UTMs, code leakage, screenshot-only sources, platform definition changes crossing the flight window.
10. Validate the plan with the user section by section - glossary, then KPI tree, then attribution, then test design, then cadence - before assembling the final document, grounded in a matching worked example from [references/worked-examples.md](references/worked-examples.md).
11. Check the Pass Threshold below; iterate until every criterion holds.
12. If your harness has persistent memory, memorize the agreed metric definitions, chosen denominators, attribution windows, and derived baselines - later campaigns then start from them instead of re-negotiating. Otherwise hand the glossary to the user as the standing reference for the next campaign.

## Output Shape

Deliver every plan as this artifact:

```
MEASUREMENT PLAN - <campaign>, <date>
Header      : brand, campaign, objective + funnel stage, flight dates, budget, platforms, creators
Glossary    : one-sentence definition per metric (numerator / denominator / window);
              chosen ER denominator; attribution window; view definition per platform, date-stamped
KPI tree    : primary | secondary | guardrail - per KPI: definition ref, target basis
              (internal trailing baseline or "first flight - none"), attribution method, data source
Attribution : the stack in use, known limitation per method, code-leakage policy and monitor
Baseline    : pre-launch values captured (branded search, direct traffic, trailing ER median)
              or an explicit "no baseline" declaration
Test design : incrementality / brand lift with MDE + power check result, or "directional only" + why
Cadence     : stakeholder -> frequency -> metrics shown -> decision it drives
Data sources: per KPI - API / ads manager / affiliate network / CRM / survey / screenshot (flagged)
Blind spots : declared list - what this plan structurally cannot see
Open items  : unconfirmed capabilities, contract clauses to add, questions before launch
```

Full worked examples live in [references/worked-examples.md](references/worked-examples.md), never inline.

## Pass Threshold

The plan passes only when the stakeholder named in the Interview could, at campaign end, make their stated decision from it without arguing about definitions. Concretely, all six must hold; iterate until they do:

- Every KPI's definition is recomputable by someone who did not write the plan - numerator, denominator, window all stated.
- The primary KPI's funnel stage matches the campaign objective's funnel stage.
- Every KPI is backed by an attribution method and data source the Interview confirmed exists - zero KPIs resting on wished-for capabilities.
- Baseline status is explicit: captured, scheduled pre-launch, or declared absent with the consequence stated.
- Incrementality or brand lift appears only with a passing power check attached; otherwise "directional only" is written in the plan.
- Zero EMV/MIV/AVE-derived numbers presented as financial value, and zero vendor benchmarks used as targets.

## B2B vs B2C

Identical for both, apply without modification:

- Glossary discipline.
- KPI-to-objective matching.
- Triangulation.
- Baseline capture.
- Provenance tagging.
- The cadence-drives-a-decision rule.

What genuinely diverges:

- **Revenue object.** B2C measures orders, AOV, and revenue inside the flight window. B2B measures influenced pipeline and opportunities - purchase rarely happens during the campaign at all.
- **Cycle length and windows.** B2C attribution windows run days to ~30 days; B2B cycles run months, so per-flight conversion KPIs undercount and windows must stretch or shift to pipeline-stage metrics.
- **Dark social dominance.** B2B creator content spreads through DMs, communities, and podcasts that strip all tracking; self-reported "how did you hear about us" (HDYHAU) on demo/signup forms, analyzed at cohort level, becomes a primary source, not a tiebreaker - with branded-search volume as the corroborating proxy.
- **Audience size and statistical power.** B2B creator audiences are small; conversion volumes almost never power an incrementality test, so B2B plans default to triangulation + HDYHAU and say so.
- **Survey placement.** B2C asks post-purchase at checkout; B2B asks on the demo-request or signup form and again qualitatively on sales calls.

## Failure Modes

| Defect                                                            | Consequence                                                                              | Fix                                                                                               |
| ----------------------------------------------------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Vanity-metric worship (reach, likes, follower counts as headline) | Report looks busy; decision-maker learns nothing                                         | Primary KPI must match objective and drive the named decision; demote counts to context           |
| EMV/MIV/AVE reported as ROI                                       | Finance discovers the number is fictional; whole program loses credibility               | Barcelona Principle 5; directional same-vendor comparison only, never financial value             |
| Last-click as the only conversion lens                            | Upper-funnel creator content structurally under-credited; program looks worse than it is | Triangulate with survey + codes; report click-based and survey-based attribution side by side     |
| No baseline captured before launch                                | "Lift" claims unsupported; awareness campaigns unmeasurable                              | Capture trailing branded search, direct traffic, ER median pre-launch - or declare the gap        |
| Mixing engagement-rate denominators                               | Same post reads 9% or 1.2% depending on denominator; trends meaningless                  | One denominator, chosen in the glossary, labeled on every number                                  |
| Comparing periods across a platform metric-definition change      | False trend in either direction                                                          | Split reporting at the change date; date-stamp view definitions in the glossary                   |
| Underpowered incrementality test                                  | "No significant lift" read as failure; a working channel gets cut                        | MDE power check before committing; below power, declare directional-only                          |
| Trusting creator screenshots                                      | Trivially falsified numbers enter the report                                             | Contract API/account-level access up front; flag screenshot-sourced data in every output          |
| Vendor benchmark adopted as target                                | Targets miscalibrated; success or failure declared arbitrarily                           | Internal trailing median by platform/tier/objective; vendor figures are calibration context only  |
| Promo-code leakage to coupon extensions                           | Extension harvests the code; creator's credit inflated, spend misallocated               | Monitor redemptions with zero matching link clicks; switch to single-use codes past a few percent |

## Invocation Examples

- "We're paying 8 TikTok micro-influencers for a skincare launch next month - how do we measure it? Build the measurement plan."
- "Design the KPI and attribution plan for our B2B always-on ambassador program: 4 newsletter writers, goal is pipeline."
- "Marketing wants an awareness push with 3 YouTube creators and finance wants proof it works. Write the influencer measurement framework before we sign."
- "We have promo codes and GA, nothing else. What can we honestly measure on this creator campaign, and what should the reporting cadence be?"

## Reference

- Read [references/kpi-definitions.md](references/kpi-definitions.md) when selecting the KPI set and writing the glossary - formulas, KPI sets per objective, ER denominators, the EMV/AVE case, target-setting rules.
- Read [references/attribution-and-data-sources.md](references/attribution-and-data-sources.md) when mapping KPIs to methods and sources - method-by-method failure modes, code leakage, platform data access, view-definition changes, podcast/newsletter measurement, B2B HDYHAU design.
- Read [references/incrementality-and-brand-lift.md](references/incrementality-and-brand-lift.md) when deciding the test design - geo-lift/synthetic control, the MDE power check, brand-lift options and their conflicts, decision thresholds.
- Read [references/worked-examples.md](references/worked-examples.md) when shaping the deliverable - one B2C conversion plan, one B2B always-on plan, one annotated negative example.
- See `mbfinotti/partnerships-skills@influencer-campaign-brief` for stating the campaign goal and deliverables handed to the creator - this skill designs how that goal gets measured.
- See `mbfinotti/partnerships-skills@affiliate-payout-audit` for payout and commission math - never done here, even for affiliate-linked campaigns.
- See `mbfinotti/partnerships-skills@influencer-discovery-brief` for sourcing and vetting the creators being measured.
- See `mbfinotti/partnerships-skills@affiliate-disclosure-compliance` for disclosure obligations - out of scope here.
