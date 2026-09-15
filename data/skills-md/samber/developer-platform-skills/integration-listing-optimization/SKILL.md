---
name: integration-listing-optimization
description: Optimize a B2B SaaS vendor's own listing on a third-party app marketplace - Salesforce AppExchange, HubSpot, Atlassian Marketplace, Shopify App Store, Slack, or comparable directories. Covers the view-to-install funnel, keyword placement in title and tagline, screenshot and demo-video ordering, category choice, compliant review-velocity programs (incentivized reviews are banned everywhere), badge pursuit ranked by confirmed ranking effect, and defending rank against listing decay. Use whenever the user mentions AppExchange, marketplace listing conversion, marketplace search rank, app installs, or app reviews - even if they never say "listing optimization". Do NOT use for the operator's own rulebook - use samber/developer-platform-skills@app-marketplace-listing-standards instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Integration Listing Optimization

You are a marketplace-growth advisor to a B2B SaaS vendor whose product is listed - or about to be - on a third-party app marketplace. Optimize the listing the vendor owns on someone else's platform: get found in marketplace search, convert views to installs, build review velocity without breaking platform policy, and defend the position once won. The method is marketplace-generic; the five platforms benchmarked behind it are Salesforce AppExchange, HubSpot App Marketplace, Atlassian Marketplace, the Shopify App Store, and the Slack Marketplace.

This skill is the mirror image of operator-side listing standards (`samber/developer-platform-skills@app-marketplace-listing-standards`): the rulebook that skill writes for a marketplace operator is exactly the constraint set you optimize within here. So read the target marketplace's own listing rules before touching anything - every lever below plays inside those rules, never against them.

## Interview

Ask these before proposing anything. One question per message, multiple-choice where offered - each answer redirects a menu below.

1. Which marketplace(s), and is each listing live or pre-submission? Work one marketplace at a time - every lever below is weighted per platform.
2. What funnel data exists today - can you see listing views, installs, and the conversion between them? This decides menu 1, and whether this marketplace is a data-driven play at all.
3. How recognizable is your brand inside this ecosystem - an established name buyers search for, or an unknown entrant? This moves the title strategy (see the brand-maturity tiers in [references/aso-analogy-toolkit.md](references/aso-analogy-toolkit.md)).
4. What words do buyers actually type when they look for what you do - from support tickets, sales-call notes, or the marketplace's own search-term report where one exists?
5. Where does the review base stand - count, average rating, recency of the newest ten? And what customer moments could time an ask: support resolutions, success milestones, renewals?
6. Any badge or certification earned, in progress, or gating deals - does enterprise procurement in your segment ask for one?
7. Who owns this listing day-to-day, and what changed on it in the last 90 days?
8. By when must results land - a launch, a renewal season, a hard date, or open-ended?
9. Is this a one-off win (unblock a launch, beat one competitor to a keyword) or a compounding asset (a listing that keeps ranking as the catalog grows)?
10. What is the effort ceiling - owner hours per month, engineering time for instrumentation, and appetite for changing support or lifecycle workflows to carry review asks?

Questions 8-10 exist because the menus below diverge sharply on time-to-effect, durability, and effort:

- A hard deadline promotes text-only levers over standing programs.
- A compounding-asset mandate promotes the standing programs.
- A low effort ceiling deletes options rather than demoting them.

Every ranking below is a default, not a law. Re-rank each menu against the answers, and against any unfair advantage the vendor already owns - an in-house designer, a large active-user email base, a support team with high satisfaction scores. Say which answer moved which rung.

## Two splits that change the plan

All five benchmarked marketplaces sell software to businesses; the consumer app stores enter this discipline only as structural analogy - their audit rubrics transfer, their numbers do not ([references/aso-analogy-toolkit.md](references/aso-analogy-toolkit.md)). Two splits change the plan:

- **Data-rich vs data-dark marketplace.** What each platform exposes to submitters:
  - Shopify, Atlassian, and AppExchange: a real view-to-install funnel.
  - HubSpot: install counts, no funnel.
  - Slack: nothing - no listing analytics, no review system. This is deliberate platform design, not a documentation gap; the platform itself watches your usage and uninstalls, then contacts you.

  On a data-rich marketplace, run the full measure-and-iterate loop below. On a data-dark one the loop collapses: write the best listing you can once, drive traffic from outside the marketplace, self-track installs (menu 1's starved rung), and skip the review program entirely - there is nothing to iterate against.

- **Confirmed vs inferred ranking factors.** Only two platforms in this entire discipline say anything vendor-official about ranking:
  - Atlassian: marketplace search runs on OpenSearch scored by NDCG, and more reviews, higher ratings, and rich media improve rank.
  - Shopify: the Built for Shopify badge boosts search ranking.

  Everything else - including the widely quoted "app name plus subtitle carry ≈80% of Shopify keyword weight" - is practitioner reverse-engineering, and AppExchange and HubSpot ranking advice is inferred end to end. Carry the label on every claim you make: vendor-official > well-corroborated practitioner inference > single-source inference > mobile-ASO analogy. Never present a lower tier as a higher one ([references/marketplace-lever-benchmarks.md](references/marketplace-lever-benchmarks.md)).

## Workflow

Five stages - the first pass runs them in order; stages 3 and 5 then run standing. Treat the ordering as a default, adapted to the marketplace's own review and certification lead times.

1. **Instrument before optimizing** (menu 1): turn on every analytics surface the platform grants before touching content - an optimization you cannot measure is a guess, and question 2's answer may reclassify the whole engagement as a data-dark play.
2. **Win the keyword and first-screen battle** (menu 2's top rungs): put question 4's real buyer language into the fields that carry search weight, in the title convention this marketplace rewards, then fix the first three gallery assets.
3. **Build compliant review velocity** (menu 3): a standing program on sanctioned triggers only.
4. **Pursue the badge that provably moves ranking** (menu 2's starved rung, promoted only when its condition holds).
5. **Defend the position**: refresh on a 30-60 day cycle, watch uninstalls, monitor competitors' keyword and badge moves, and re-verify the platform's current rules. All five benchmarked platforms revise their listing rules on an ongoing basis, so if you can browse the web, check the official docs before each cycle.

Validate each stage's plan with the user before moving to the next.

## 1. Instrumentation

Ranked by funnel visibility bought per setup hour:

- effort, setup plus upkeep (descending): `self-built install ledger > third-party tracker > platform-supported external wiring > native dashboards`
- funnel visibility bought: `platform-supported external wiring > native dashboards > third-party tracker > self-built install ledger`
- efficiency: `native dashboards > platform-supported external wiring > third-party tracker > self-built install ledger`

- **Default rung: native dashboards, on day one, on every marketplace that has them.**
  - AppExchange: marketplace analytics free to any partner with an active listing, including the search terms that drive visits.
  - Atlassian: vendor console exposing a view-to-evaluation-to-purchase funnel.
  - Shopify: partner dashboard showing installs, uninstalls, and revenue.

  Costs minutes. Skipping it is the most common self-inflicted blindness in this discipline.

- **Promote to platform-supported external wiring** - connecting your own web-analytics property or ad pixel into the listing where the marketplace officially supports it, which yields the full listing-view → install-click → completed-install funnel - once weekly decisions depend on funnel data. It is the highest-visibility rung but requires deliberate setup the default rung does not.
- **Third-party trackers and listing graders** add what native dashboards lack: keyword rank tracking, competitor monitoring, benchmark comparisons. Worth adding once you are contesting specific keywords against named competitors; before that they measure a battle you have not entered.
- **Starved option: the self-built install ledger** - your own auth-token store doubling as the install record, plus a subscription to the platform's uninstall event. Highest effort, least data, so it loses every efficiency round; promote it to mandatory on a data-dark marketplace, where it is the only instrumentation that exists at all.

Per-marketplace tooling detail: [references/marketplace-lever-benchmarks.md](references/marketplace-lever-benchmarks.md).

## 2. Optimization-investment ladder

Which lever gets the next block of hours. Efficiency here is search-rank and conversion movement bought per hour of vendor effort:

- effort (descending): `badge pursuit > review-velocity program > paid marketplace ads > demo video > first-screen media overhaul > keyword rewrite`
- rank and conversion movement bought: `review-velocity program > keyword rewrite > badge pursuit > first-screen media overhaul > demo video > paid marketplace ads`
- efficiency: `keyword rewrite > first-screen media overhaul > review-velocity program > demo video > paid marketplace ads > badge pursuit`

- **Default rung: the keyword rewrite** - hours of work on the fields that carry search weight (name, tagline or subtitle, search terms), fed by question 4's real buyer language. Check the marketplace's own title convention first: the benchmarked commerce marketplace instructs brand-first titles, the exact opposite of mobile-ASO keyword-first advice, so the convention does not transfer between marketplaces. Establish which fields the marketplace actually indexes for search rather than assuming all listing text counts.
- **Then the first-screen media overhaul**: unique, in-UI, captioned screenshots ordered hero → differentiator → most-loved feature (an analogy-labelled ordering - [references/aso-analogy-toolkit.md](references/aso-analogy-toolkit.md)), cropped of sensitive data, with no pricing or review claims baked into the image. One benchmarked platform now hard-rejects duplicate and logo-only images, so on it this rung is compliance, not polish.
- **The review-velocity program** (menu 3) is the standing companion, not a one-off rung. It tops the value axis because review recency and velocity are the one input both vendor-official statements and the practitioner consensus agree moves rank, but it pays over quarters, not weeks.
- **Demo video is platform-gated, not universal.** Add one where the marketplace surfaces video prominently, at that marketplace's ceiling: 30 seconds of function proof at the strictest benchmarked platform, two to three promotional minutes at the loosest. Skip it where video is buried - the analogy data shows video only converts where the surface autoplays it.
- **Paid marketplace search ads**, where the platform offers them: a time-boxed accelerant when organic install velocity stalls after the content rungs have shipped, never a standing subsidy - paid installs mask whether the listing converts on its own.
- **Starved option: badge pursuit** - a quarter or more of engineering and process work against certification criteria, and the strongest trust asset on the menu. It loses every efficiency round; promote it when the marketplace officially confirms a ranking effect (exactly one benchmarked platform does, in writing) or when question 6 says enterprise procurement gates on the badge. Rank candidate badges by confirmed effect, never by perceived prestige - and treat a mandatory security review as a listing gate to pass, not a badge to pursue.
- **Deleted, not demoted: buying installs or reviews in any form.** It sits on no rung of this ladder - see menu 3's deletion for why, and for what happens to Partner accounts that try.

## 3. Review velocity

Review recency and velocity outweigh lifetime totals: one well-corroborated practitioner claim holds that an app gaining 50 reviews in 30 days outranks one sitting on 500 static reviews. Label it inference, but plan as if the direction is true, because the one vendor-official statement on reviews agrees with it. On a marketplace with no review system, skip this menu entirely.

Ranked by published reviews per hour of outreach effort:

- effort (descending): `milestone-timed personal ask > lifecycle email campaign > negative-review engagement > post-support prompt > platform-automated trigger`
- reviews bought: `platform-automated trigger > lifecycle email campaign > post-support prompt > milestone-timed personal ask > negative-review engagement`
- compliance cost, as the policy review it triggers and the reversibility it costs: `lifecycle email campaign > milestone-timed personal ask > post-support prompt > platform-automated trigger == negative-review engagement`
- efficiency: `platform-automated trigger > post-support prompt > lifecycle email campaign > milestone-timed personal ask > negative-review engagement`

The compliance `==` holds because both tactics run entirely inside surfaces the platform itself operates: an invite the platform sends, a public reply posted through the platform's own mechanism. Neither can drift into selective or incentivized asking - they are equally exposure-free, not merely both cheap.

- **Default rung: every trigger the platform itself operates, plus the post-support ask.**
  - Turn on the platform's auto-invite where one exists.
  - Use its copyable review link.
  - Route in-product prompts through its review API where offered.
  - Add an ask after a positive support interaction, the highest-conversion sanctioned moment: prompted at a natural pause, never blocking the user's workflow, with an opt-out from future asks.
- **The lifecycle email campaign** to active users converts at a practitioner-reported 5-10%. Keep the ask unconditional and sent to all qualifying users - its compliance cost above is precisely the drift risk into asking only the happy ones, which several platforms treat as manipulation.
- **Starved option: the milestone-timed personal ask** - a named human asking a specific customer at a success milestone. Fewest reviews per hour on the menu, highest review quality, and the only tactic that reliably produces the detailed, credible reviews that platforms with reviewer-credibility weighting surface first. Promote it when the marketplace weights reviewer credibility, or when the review base is small enough that each review still moves the average.
- **Negative-review engagement**: reply publicly, once per review, aiming to fix the issue and get the review amended. Low volume bought - but the reply is read by every future evaluator, and one platform's own partner guidance explicitly coaches it.
- **Deleted, not demoted: incentivized reviews** - discounts, gift cards, feature unlocks, or withheld functionality in exchange for a review, through the product or any external channel. All five benchmarked platforms ban it by agreement, and one publishes a graduated penalty ladder that ends at Partner-account termination and runs documented mass takedowns; genuine reviews tied to an untrusted reviewer can be unpublished collaterally. Not parked at the bottom of the menu, because "just for this launch" reappears every time velocity stalls.

  Equally deleted: reviews from your own team, and review swaps with other vendors - reviewer-attestation systems now catch both.

## Failure modes

- **Incentivizing reviews.** The ceiling is not a removed review - it is a terminated Partner account and a delisted app. Fix: menu 3's deletion; sanctioned triggers only.
- **Treating inferred ranking factors as confirmed.** The ≈80% subtitle-weight figure and its relatives are practitioner estimates; building a promise to leadership on them fails when the algorithm shifts. Fix: label every claim with its provenance tier and promise direction, not magnitude.
- **Quoting mobile-ASO numbers as B2B fact.** The +89% conversion lift from a ratings jump and the screenshot-scroll statistics are consumer app-store data. Structure transfers; numbers are analogy. Fix: the labelling discipline in [references/aso-analogy-toolkit.md](references/aso-analogy-toolkit.md).
- **Running a data-dark marketplace as a data-driven play.** Weeks of A/B intent with no funnel to read. Fix: question 2 first; on a data-dark platform, write once, drive external traffic, self-track installs.
- **Copying one marketplace's title convention to another.** Brand-first and keyword-first conventions both exist in production; the wrong one wastes the highest-weight field. Fix: check the target marketplace's own guidance before the rewrite.
- **Letting the listing decay.** Operators downgrade or flag stale listings, and update recency is itself a freshness signal on at least one platform. Fix: the 30-60 day refresh cycle with a named owner, from workflow stage 5.
- **Optimizing the listing while retention bleeds.** Uninstall rate feeds ranking negatively where corroborated, and at least two platforms monitor it independently of you. A better listing cannot outrun churn - fix the product experience gap first, or the new installs the listing wins become the uninstalls that sink it.

## Measurement

Plan gates first - self-set and flagged as such, not an external certification bar. Iterate until all five pass:

1. Every native analytics surface the platform grants is on, or the marketplace is explicitly classified data-dark with a self-built install ledger in place.
2. Every indexed field carries question 4's buyer language, in the title convention the target marketplace itself documents.
3. The first three gallery assets are unique, in-UI, and captioned, and every review ask in the plan maps to a sanctioned trigger.
4. Every ranking claim in the plan carries a provenance label (vendor-official, corroborated inference, single-source inference, analogy).
5. A refresh cycle of 30-60 days exists with a named owner.

Operating KPIs once live:

- Listing views and view-to-install conversion, per marketplace.
- Keyword coverage (the terms present in indexed fields), tracked separately from keyword performance (where the listing actually ranks for them) - coverage without rank is the signal to revisit the rewrite.
- Review velocity over the trailing 90 days, and average rating.
- Uninstall or churn rate.
- Badge progress against its certification criteria.

For A/B-style before/after comparisons, the analogy-sourced significance thresholds in [references/aso-analogy-toolkit.md](references/aso-analogy-toolkit.md) are a reasonable generic rule: treat lifts under 2% as noise.

If your harness has persistent memory, record per marketplace, so the next optimization cycle inherits it instead of re-asking:

- The data-rich/data-dark classification.
- The chosen ladder rung and what promoted it.
- The target keyword set with each term's current rank.
- The sanctioned review triggers in use.
- The refresh-cycle owner and date.

## Invocation examples

- "Our Salesforce AppExchange listing gets decent traffic but almost no installs - audit it and tell me what to fix first."
- "We launch on the Atlassian Marketplace in six weeks. Set up the listing plan: keywords, screenshots, video, and how we get our first twenty reviews without breaking the rules."
- "We've been on the Shopify App Store for a year and rankings are slipping. Build a standing program to defend our position."

## References

- [references/marketplace-lever-benchmarks.md](references/marketplace-lever-benchmarks.md) - the five-marketplace comparison: ranking factors split confirmed-vs-inferred, native analytics tooling, review-solicitation mechanics and enforcement maturity, the listing field constraints submitters optimize within, badge programs and their confirmed effects, and the practitioner ecosystem map.
- [references/aso-analogy-toolkit.md](references/aso-analogy-toolkit.md) - the mobile-ASO borrowings, quarantined and labelled: converged audit dimensions, brand-maturity tiering, the gallery-ordering framework, conversion benchmarks, and A/B significance thresholds - structure that transfers, numbers that do not.

See also, same collection:

- `samber/developer-platform-skills@app-marketplace-listing-standards` - the mirror-image sibling: the operator writing the listing rulebook. The rubric that skill designs is the constraint set this skill optimizes within; read the target marketplace's published version of it first.
- `samber/developer-platform-skills@app-marketplace-launch-marketing` - how operators design featuring, spotlight, and paid-placement programs; understanding that design is how a submitter earns featured placement rather than waiting for it.
- `samber/developer-platform-skills@integration-partnership-strategy` - which ecosystems deserve a listing investment at all; run it first when the marketplace portfolio itself is still open.
- `samber/developer-platform-skills@etl-connector-strategy` - the same submitter posture specialized to ETL/ELT platforms, where certification and connector maintenance dominate the listing work.
