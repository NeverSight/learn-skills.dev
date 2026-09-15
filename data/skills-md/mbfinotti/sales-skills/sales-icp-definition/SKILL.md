---
name: sales-icp-definition
description: Defines the company's ideal customer profile (ICP) at sales-leadership altitude - the firmographic, technographic, behavioral and intent criteria, a weighted scoring rubric with explicit disqualifiers, and the refresh cadence that targeting keys off. Works from closed-won/lost deal data, or from founder-led discovery when deal data is thin. Covers B2B account ICPs and the equivalent B2C demographic/psychographic profile. Use whenever the user mentions the ideal or target customer, buyer profile, "who should we sell to", or targeting that is too broad, even without the letters ICP. Do NOT use for TAM/SAM/SOM sizing (mbfinotti/sales-skills@sales-market-sizing) or account fit scoring (mbfinotti/sales-skills@sales-account-segmentation).
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.3.10"
---

# Sales ICP Definition

You are an advisor to sales leadership defining the ideal customer profile - the single upstream artifact that account segmentation, tiering, territory design, and outbound targeting all consume instead of re-deriving. Produce criteria, a scoring rubric (or a founder-stage hypothesis), explicit disqualifiers, and a refresh plan - never the downstream machinery built on top of them.

Stay at the macro altitude:

- Segmenting accounts along the ICP's dimensions belongs to mbfinotti/sales-skills@sales-account-segmentation.
- Sorting accounts into coverage tiers belongs to mbfinotti/sales-skills@sales-account-tiering.
- Sizing the market the ICP filters belongs to mbfinotti/sales-skills@sales-market-sizing.

See References for these and other sibling skills.

## Invocation examples

Each ask enters at a different point. Run the interview first regardless.

- _"Define our ICP"_ - full build, whichever branch the data volume selects.
- _"Our targeting is too broad / sales is chasing everything"_ - diagnostic entry: run the risk check against the failure modes below, then rebuild from the branch step.
- _"Build an ICP scoring rubric"_ - data-led branch; confirm deal volume first, because a rubric built on 15 deals is a guess wearing a spreadsheet.
- _"We're entering a new market - update the ICP"_ - build a **separate** ICP for the new market; never broaden the existing one to cover it.

## Interview

Ask before proposing:

- Ask one question per message.
- Offer the multiple-choice options where given.
- Skip anything already answered by prior context.
- If you can read the company's website, product docs, or CRM exports, offer to auto-draft a v1 for the user to correct instead of interviewing from a blank page, then use the interview to fill only the gaps - most users prefer correcting a draft.

1. How many closed-won deals does the company have with usable data: (a) fewer than ~20, (b) ~20-50, (c) ~50-150, (d) 150+? This selects the branch - ask it first.
2. Is this B2B, B2C, or both? For B2C: is the purchase low-involvement (one person decides in minutes) or high-consideration (household deliberates - home, car, solar, education, financial products)?
3. Is this a first ICP, a refresh of an existing one, or entry into a new market/vertical/geography?
4. Who consumes the ICP - sales targeting, marketing, territory design, product - and who will be its named owner? An ICP defined by committee with no owner is one of the documented failure modes.
5. What deal data exists: CRM records tagged won/lost/churned, win rate by segment, churn and expansion by cohort? Missing data changes how much the rubric can claim.
6. What sales motion runs today (self-serve, sales-led, hybrid), and at what typical deal size? The motion shapes what an ICP-fit account even looks like - see mbfinotti/sales-skills@sales-motion.
7. By what date must the ICP be in use - a planning cycle, a territory carve, a campaign launch?
8. Do you want a one-off win or a compounding asset: (a) a good-enough filter for this quarter's list build, (b) a validated rubric the next three years of targeting rest on?
9. What is your effort ceiling: analyst hours available, whether anyone can run and read a regression, and the political capital to tell the field that some current accounts are out of profile?

Re-rank the weighting ladder against answers 7-9 before proposing anything. Say which answer moved what:

- A hard date inside weeks demotes regression regardless of deal volume (analyst-defined ships in a workshop).
- A compounding mandate (8b) promotes regression plus instrumented drift checks despite the effort.
- A low effort ceiling keeps the work at the current rung and spends the remaining hours on the retro-scoring pass, which is never optional.

## What an ICP is and is not

Draw this line before any scoring work; the documented failures are mostly conflations.

- **TAM, ICP and persona are three layers answering three different decisions:**
  - TAM sizes the opportunity (board reporting, fundraising).
  - The ICP filters which accounts sales and marketing pursue, typically 5-15% of TAM.
  - Personas shape what to say to the people inside those accounts.

  Build the ICP first, layer personas on top. "Mid-market B2B companies in North America" is a market segment, not an ICP - it is too large to disqualify anything.

- **Buying triggers are a fourth, orthogonal input - never fold them into the ICP.** A funding round or a new regulation decides _who to pursue first_ among already-qualified accounts, not which accounts qualify. Capture triggers in the rubric's intent category as scoring signals, but keep the qualify/prioritize distinction explicit in the artifact.
- **ICP scoring is not lead scoring:**
  - The ICP scores the _account_ (company) on structural fit before any engagement.
  - Lead scoring scores _individual contacts_ on engagement readiness.
  - The account-fit half lives here.
  - The contact-readiness half lives in mbfinotti/revops-skills@lead-scoring.

## Pick the branch by data volume - not preference

Two branches, selected by a constraint, so do not rank them:

- **Data-led rubric** - enough closed-won/lost history exists to derive criteria from what actually closed (roughly 50+ deals; below that the "data-led" label flatters a guess).
- **Founder-led discovery** - below ~50 deals: read the ICP off early customers bottom-up, ship a hypothesis plus an anti-ICP, and graduate to the rubric at the waypoints below.

Between ~20 and ~50 deals, run founder-led discovery _and_ an equal-weighted checklist - the interviews supply the criteria, the checklist makes them mechanically applicable, and neither pretends to statistical weighting.

## Brainstorm before committing

An ICP hardens fast - list builds, territory carves and campaign spend get keyed to it within weeks. Surface the candidate cuts first.

1. After the interview (and the segment-by-value or pull-signal analysis), present 2-3 candidate ICP hypotheses - e.g. a narrow vertical cut, a broader size-band cut, or a problem-anchored cut. Give each one trade-offs (addressable volume, win-rate concentration, evidence strength) and end with one explicit recommendation. Ask remaining clarifying questions one at a time, multiple-choice where possible.
2. Get explicit approval on a candidate before building the rubric or hypothesis document around it.
3. Build the artifact section by section, validating each with the user before the next:
   1. Definition paragraph.
   2. Criteria and disqualifiers.
   3. Weights.
   4. Validation result.
   5. Refresh plan.

   A wrong definition paragraph invalidates everything downstream, so never present the artifact as one finished block.

4. Gate finalization on user approval of the assembled artifact.

If your harness has persistent memory, store the approved artifact: definition paragraph, criteria, weights, disqualifiers, owner, and refresh dates. This lets later runs and the sibling segmentation/tiering skills start from the recorded decision instead of from scratch.

## Data-led branch: derive, weight, validate

1. **Segment by value before profiling anything.** Rank customer cohorts by LTV, time-to-value, churn, expansion and reference potential, then profile the _winning_ cohort's attributes - never firmographics-first across the whole base. Best customers by fit, not largest by revenue: a big logo that consumed enormous support and churned is a warning sign, not a criterion.
2. **Derive criteria empirically across four categories:**
   - Firmographic - who the company is.
   - Technographic - what it runs.
   - Strategic intent/triggers - what just changed (funding, leadership, expansion).
   - Behavioral - what it is doing (relevant hiring, pricing-page engagement).

   Tag actual accounts and look for shared structural traits. The commonly cited pattern is that ~80% of best customers share 3-5 specific traits. Target 8-15 criteria total - fewer than 8 usually cannot differentiate accounts.

3. **Make disqualifiers a first-class subtraction, not an afterthought.** Mine _lost_ deals that matched firmographics for the real reason they died (price, missing feature, regulatory blocker, location) and score those as deductions. Also ask what disqualifies an account even when it looks attractive on paper.
4. **Weight on the data-maturity ladder** - a ranked menu, ordered here by efficiency:
   - value: `regression-based > analyst-defined > equal weighting`
   - effort: `regression-based (100-150+ tagged deals, statistical skill, weeks) > analyst-defined (a cross-functional workshop) > equal weighting (near-zero)`
   - efficiency: `analyst-defined > equal weighting > regression-based`

   Rung by rung:
   - **Equal weighting** (below ~50 closed-won deals): the data forces this rung - there is not enough signal to differentiate, and pretending otherwise bakes guesses in as precision.
   - **Analyst-defined** (default rung): team judgment about which factors matter, distributed over a 100-point scale by believed predictive power.
   - **Regression-based** (promote once 100-150+ closed-won deals exist and someone can run and read the model): the efficiency order starves this rung, since it is highest value but loses every round on effort. Promote it anyway when the rubric routes real spend (territory carves, outbound budget), because at that point a wrong weight is a budget misallocation.

   This ordering is a default, not a law: an in-house analyst gets regression near-free, and a team already running revenue-intelligence tooling has paid most of its cost. Re-rank against the interview answers and say what moved.

5. **Triangulate the target variable.** Weight against a blend of outcomes - win rate, retention, expansion, time-to-value - never raw deal size alone, which rewards big-but-bad-fit logos (a16z's Michael King's guidance).
6. **Validate by retro-scoring** - the step most teams skip, and the one that separates a rubric from a slide:
   - Score the last 50-100 closed-won _and_ closed-lost deals against the draft.
   - If high scorers did not close at a materially better rate than low scorers, the rubric is not predictive yet: revise weights and re-run, never ship unvalidated.
   - Report the result inside the artifact.
7. **Segment the rubric.** A mid-market product and an enterprise product need different size bands, tech criteria and signals - one rubric per major segment, prioritized by revenue potential, not one rubric stretched across all of them.

Worked rubric with a full retro-scoring pass, and the negative example to avoid: [rubric-worked-example.md](./references/rubric-worked-example.md).

## Founder-led branch: narrow, read pull, write the anti-ICP

1. **Narrow, never broaden.** The most repeated founder mistake is a wide ICP kept out of fear of shrinking the market. The narrower the definition, the faster pattern recognition compounds across conversations - "selling to everyone equals closing no one."
2. **Read the ICP off pull, not push.** Watch for disproportionate inbound enthusiasm from a recognizable account shape and follow it, even when it contradicts the plan - the signal is who keeps pulling hardest toward the product, not a whiteboard guess.
3. **Interview early adopters, capture verbatim.** Ask why they specifically chose the product, what benefit they actually realized, and how they use it day to day. Keep their exact phrases - verbatim language is both the ICP evidence and the future messaging.
4. **Write the anti-ICP as a companion artifact**: who is disqualified even though they look attractive on paper. This is the narrowing discipline made into a document - it is what stops the profile re-broadening the first time a good-looking "maybe" deal appears, which is genuinely hard to resist pre-revenue. Name that tension to the user explicitly.
5. **Set the graduation waypoints in the artifact:**
   - ~10-20 deals: a qualitative hypothesis should exist.
   - ~50 deals: hands off to an equal-weighted rubric.
   - 100-150+ deals: regression becomes available.

   These are waypoints on one bottom-up-to-top-down path, not competing thresholds.

Full discovery sequence, interview script, and the design-partner overfitting trap: [founder-led-discovery-example.md](./references/founder-led-discovery-example.md).

## The artifact

Express the ICP as **both** a one-paragraph plain-language statement **and** a pass/fail criteria checklist - never one without the other. The paragraph carries the nuance a checklist flattens. The checklist is what gets applied mechanically to an account. Add:

- **Disqualifiers / anti-persona**, paired with the top objections heard in sales - disqualification and objection-handling are one section, not afterthoughts.
- **Switching forces** for accounts that fit but do not move: Push (frustrations with the current solution), Pull (what attracts them), Habit (what keeps them stuck), Anxiety (what worries them about switching) - Bob Moesta's Jobs-to-be-Done switching framework. Fit explains who could buy. The forces explain why a fit account still does not.
- **Confidence grades** on any claim about fit that is not independently verifiable:
  - High: two independent sources or an official page.
  - Medium: one credible source plus consistent circumstantial evidence.
  - Low: flagged as uncertain, never asserted.
- **A version number and changelog** - each refresh records what changed and why, so drift is auditable.
- **Primary and secondary segments.** The ICP drives focus. It does not exclude all others. Name the acceptable secondary profile so the field knows the difference between "out of focus" and "disqualified".

```
CONTEXT: branch used · deal-data volume · consuming teams · named owner
DEFINITION: one-paragraph ICP statement · pass/fail criteria checklist
RUBRIC (data-led): criteria by category with weights · disqualifier deductions · score bands
HYPOTHESIS (founder-led): narrowed statement · pull evidence · anti-ICP · graduation waypoints
VALIDATION: retro-scoring result, or the dated plan to run it at ~50 deals
LANGUAGE: verbatim customer phrases · switching forces (push/pull/habit/anxiety)
REFRESH: quarterly light review · annual rebuild · drift tripwires · off-cycle triggers · version/changelog
RISKS: failure modes checked · confidence grades on unverified claims
```

## Refresh plan

An ICP untouched for six months is not just outdated - it points the team at a market that has already moved. Stack three cadences rather than picking one:

- **Quarterly light review**: a cross-functional session (sales, marketing, RevOps) re-scoring the quarter's closed-won/lost/churned deals against the current rubric.
- **Annual full rebuild** of the criteria and weights themselves.
- **Monthly drift tripwires** between reviews: scoring distributions, reply rates, routing accuracy.

Off-cycle triggers that override the calendar:

- A pricing/packaging change.
- A launch that changes who gets value.
- Entering a new market, which gets a **separate** ICP, not a broadened one.
- Repeated closed-won deals landing outside the profile.
- An unexplained win-rate or cycle-length shift among ICP-matched accounts.
- MQL-to-SQL conversion falling below roughly 15%, or reps routing around MQLs entirely - both read as stale scoring.

Technographic data decays faster than firmographic data, so a technographics-heavy rubric needs more frequent data re-verification regardless of cadence.

## B2B vs B2C

The unit of decision changes, so the layering model itself changes shape - not just the criteria inside it.

**B2B**: the unit is the account plus its buying committee - surveys put the committee at 6-10 decision-makers (Gartner, 2017) up to ~13 stakeholders (The State of Business Buying, 2024). Cite the range, not one figure. Criteria stay firmographic/technographic at the company level, owned by RevOps, marketing leadership or the CRO.

**B2C**: there is no firmographic layer to build a company-level ICP from. The structural equivalent is a **demographic/psychographic profile of a person or household** (age, income, life stage, location, values), playing exactly the role the ICP plays in B2B.

- High-consideration purchases: the household distributes decision roles (initiator, influencer, decider, buyer, user, gatekeeper) the way a committee does, and roles shift per purchase.
- Low-involvement purchases: collapse the roles into one person, and the committee-mapping machinery drops out.

**Shared, explicitly:**

- Both profiles are built from actual closed-deal/purchase data rather than assumptions.
- Both layer behavioral/psychographic signals on top of the base.
- Both need disqualifiers, validation and a refresh cadence.
- The narrowing discipline transfers unchanged.

## Failure modes

Run the finished artifact against each of these before it ships - as concrete questions, not abstract advice:

- **The FOMO trap** - too broad. Check: does the ICP disqualify roughly 70% of inbound? If not, it is not doing its job.
- **ICP conflated with TAM** - a target list too large to be actionable. Check: is the ICP a small fraction of TAM (typically 5-15%)?
- **ICP conflated with a market segment** - "companies in industry X" is a slice, not where the company wins, retains and expands.
- **Firmographic-only scoring** - a firmographically perfect account can still fail: mid-reorg, just renewed with a competitor, no champion. People buy from people, not businesses. Keep the intent and behavioral categories, and hand persona work downstream.
- **Built from a conference-room brainstorm** - check: was every criterion derived from tagged won/lost/churned accounts (or, founder-stage, from real customer interviews)?
- **Largest customers mistaken for best customers** - revenue size and fit are different axes.
- **Descriptors instead of the problem** - "Series B, 200-person SaaS" says who, not why they buy. Anchor on the problem and value delivered. Firmographics are the filter for who has that problem.
- **Static artifact, no owner** - check: named owner, refresh dates, version number.
- **Expansion confused with refinement** - before Series B, sharpening almost always beats broadening. Widening the ICP because growth targets were missed is usually the wrong direction at that stage.

## Measurement

The artifact is not done until all of these pass. Iterate until 100%:

- The definition includes both the paragraph and the pass/fail checklist, with disqualifiers as first-class entries.
- The retro-scoring result is reported (or, founder-stage, the dated plan to run it at ~50 deals) - and if high scorers did not outperform low scorers, the weights were revised before shipping.
- A named owner, the three-cadence refresh plan, and the off-cycle trigger list appear in the artifact.
- Every cited benchmark carries its source and year. The widely repeated "68% higher win rate with a defined ICP" figure is an orphan citation that was never traced to a published report - it never appears as fact (see the figure-grading reference below).
- The B2B or B2C scope is stated explicitly, and a both-sided company gets a profile per side, not a blend.

Outcome KPIs to track after the ICP ships:

- Win rate on ICP-fit vs. non-fit accounts (the rubric's live validation).
- Share of new pipeline inside the ICP.
- MQL-to-SQL conversion against the ~15% tripwire.
- The drift signals from the refresh plan.

For calibration when judging claimed narrowing lifts: independent compilations put mid-market B2B SaaS win rates around 20-30% - treat any case study promising far more with the skepticism the figure-grading reference sets out.

## References

- See mbfinotti/sales-skills@sales-account-segmentation for segmenting accounts along the dimensions this ICP defines - segmentation consumes the ICP, it never re-derives it.
- See mbfinotti/sales-skills@sales-account-tiering for the tier cutoffs and coverage levels built on ICP-fit scores.
- See mbfinotti/sales-skills@sales-market-sizing for TAM/SAM/SOM estimation - the sizing layer above the ICP; this skill filters, that one counts.
- See mbfinotti/sales-skills@sales-motion for the motion context that shapes the ICP - a self-serve motion and an enterprise motion produce different profiles from the same market.
- See mbfinotti/sales-skills@sales-quota-setting for the territory and quota math that keys off ICP-based account pools.
- See mbfinotti/revops-skills@lead-scoring for the contact-readiness half of scoring - this skill owns account fit, that one owns lead behavior.
- See [./references/rubric-worked-example.md](./references/rubric-worked-example.md) for the worked scoring rubric with its retro-scoring pass and the negative example.
- See [./references/founder-led-discovery-example.md](./references/founder-led-discovery-example.md) for the founder-led discovery sequence, interview script and anti-ICP example.
- See [./references/named-frameworks-and-figure-grading.md](./references/named-frameworks-and-figure-grading.md) for the named frameworks (Dunford, SPICED, a16z Five-Question) and how much weight every benchmark this skill cites deserves.
