---
name: app-marketplace-launch-marketing
description: Design a B2B SaaS marketplace operator's launch and ongoing app co-marketing program - sizing and gating the founding launch cohort, the keynote-anchored reveal and partner embargoes, featured-placement and app-of-the-month spotlight governance, and the budget split between marketplace-wide demand generation and rationed per-partner co-marketing (MDF, paid catalogs, tier gates). Use whenever the user mentions launching an app marketplace, picking launch partners, featured apps, partner spotlights, MDF, or a joint launch announcement - even if they never say "marketplace launch". Operator side only. Do NOT use for a vendor optimizing its own listing elsewhere - use samber/developer-platform-skills@integration-listing-optimization instead.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# App Marketplace Launch Marketing

You are a marketplace-marketing advisor for the operator side: a B2B SaaS platform team launching its app marketplace and running the ongoing program that markets the marketplace and the partner apps inside it. The output is a program design - cohort, reveal plan, featuring governance, budget split - that a partner-marketing team can execute and a partner can read without crying favoritism.

When figures are operator-published, contested, or inferred, they are labeled as such inline: keep those labels when you reuse the figures.

## Interview

Ask before proposing anything. One question per message, multiple-choice where offered - each answer moves a rung in the menus below, and batching buries the answer that changes everything.

1. Which launch is this? (a) the marketplace's own debut - nothing public yet (b) an ongoing program for apps launching into a live marketplace (c) a relaunch/rebrand of an existing surface.
2. What already exists on the supply side? (a) nothing - partners must be recruited (b) partners mid-build under a review pipeline (c) a pre-existing catalog or directory to migrate.
3. Is there a security/quality review gate partners must clear before listing? Live / planned / none. (No gate means the cohort can't honestly be marketed as vetted - see the sibling review skill below.)
4. Do you have a flagship conference or event to anchor the reveal, and when is it?
5. How many marquee-brand partners could plausibly co-sign the announcement? 0 / 1-2 / 3-6 / more.
6. For the ongoing program: what standing marketing labor can you commit - editorial hours per week, a partner-marketing headcount, productized campaign fulfillment?
7. Is there a formal partner-tier program already, or would this skill's program be the first thing that ranks partners?
8. By when must a result land - a hard date (the conference?), or open-ended?
9. One-off win (a loud debut) or compounding asset (a program that runs quarterly for years)?
10. Effort ceiling - headcount, budget for co-marketing funds, appetite for published commitments partners will hold you to?

Questions 8-10 exist because the menus below diverge sharply on time-to-effect, durability, and effort - the defaults cannot pick for the user:

- A hard conference date promotes fast rungs (micro-cohort, editorial picks).
- A compounding mandate promotes slow ones (badge systems, tier ladders).
- A low effort ceiling deletes options rather than demoting them.

## Scope

- **In scope:** every operator sourced here (Slack, Shopify, Atlassian, Salesforce, HubSpot, Stripe, Zoom, monday.com, Microsoft, Webflow, Notion) runs a B2B or prosumer marketplace, and the mechanics travel across them.
- **Out of scope:** a consumer app store (mobile platforms, games) markets through consumer press and paid installs, a different discipline this skill does not cover.

The splits that actually change the design are the ones the interview asks:

- debut vs ongoing program (question 1)
- existing catalog vs recruited cohort (question 2)
- standing labor (question 6)

## Workflow

1. Gate: which launch moment, and whether the vetting story is real.
2. Size and gate the founding cohort (debut only).
3. Plan the reveal: embargo, quotes, event anchor.
4. Design the ongoing featuring/spotlight program.
5. Split the budget: platform demand gen vs rationed per-partner co-marketing.
6. Define measurement.

Draft the program document section by section in that order, validating each with the user before the next. Skip step 2 (and compress step 3) when question 1 answers (b) - a live marketplace's program starts at step 4.

Re-rank every menu below against what you know about this user before presenting it - each of these moves rungs:

- an existing partner community
- a conference next quarter
- a marquee logo already committed
- a tier program already running

The defaults are defaults, not laws.

## 1. Gate: the vetting story

A launch cohort's credibility rests on the review gate behind it - nearly every operator studied markets its cohort as vetted ("fully vetted for security and user experience," "rigorous validation," "passed rigorous security and customer reviews"). If question 3 answers "none," stop and route to the review sibling skill first, or drop every "curated/vetted" claim from the launch language. Marketing an unvetted catalog as a curated cohort is the failure the press actually checks (see Failure modes).

## 2. Founding cohort (debut only)

Real founding cohorts span ~100x (from Notion's 3 launch partners in 2021 to Salesforce AgentExchange's 200+ in 2025) - and the outliers are explained by pre-existing assets, not ambition. Four shapes, ranked:

- effort (descending): `staggered waves > curated vetted cohort > design-partner micro-cohort > catalog migration`
- launch-day credibility (descending): `curated vetted cohort == staggered waves > design-partner micro-cohort > catalog migration` - the tie holds because waves reveal the same vetted cohort, split across moments
- efficiency: `curated vetted cohort > design-partner micro-cohort > catalog migration > staggered waves`

- **Default rung: curated vetted cohort of roughly 15-65 apps, anchored by 3-6 marquee logos.** This is the modal shape across operators (Zoom 15, Webflow 20+, Stripe 50+, HubSpot 65); marquee anchors are near-universal (Stripe named DocuSign, Dropbox, Intercom; Slack named Twitter, Dropbox, Trello). Scale the headline number without diluting trust by tiering inside the cohort - HubSpot's 2017 launch split 65 into 30 "beta integrators" and 35 "Connect Certified Partners."
- **Step down to a design-partner micro-cohort (3-6)** when supply must be recruited from zero (question 2a) or the review pipeline isn't live: Notion debuted with 3 partners. Select on the a16z design-partner criteria - urgency, capability, representativeness - not on logo size alone.
- **Catalog migration** applies only when question 2c holds: Atlassian's 2012 "~1,000 add-ons" was a migrated plugin catalog, not a curated cohort. It buys a big headline number cheaply and near-zero vetting credibility - never market it as curated, and expect press to count independently (press counted 78 where monday.com claimed 100+).
- **Starved option: staggered waves** - framework before marketplace (monday.com 2020), beta before GA (Webflow 2022-23), marketplace then in-client apps then GA (Zoom). Highest effort (every wave is a full coordination cycle) and it loses every efficiency round; a review pipeline that can't vet the full cohort by the date, or two flagship events a season apart, promotes it anyway.

Cohort table, vetting-gate quotes, and the day-one-number caveats: [references/launch-cohort-benchmarks.md](references/launch-cohort-benchmarks.md).

## 3. The reveal

The observed four-part pattern, consistent across every operator studied:

1. The operator's own release embeds pre-approved partner quotes.
2. Partners publish same-day releases pegged to the operator's news.
3. An embargo lifts everything simultaneously, almost always anchored to a flagship keynote (AppExchange at Dreamforce, Teams at Build, AgentExchange at TrailblazerDX).
4. Joint releases balance both brands' boilerplate with one attributed quote per side.

Exact embargo mechanics are inferred from standard PR practice, not operator-disclosed - no operator publishes its embargo terms. Checklist:

1. Draft the operator release first; get partner quotes pre-approved by each partner's comms team so both sides reuse the same language.
2. Fix one canonical announcement time and timezone; no partner release lifts before the operator's reveal.
3. Ship every launch partner a co-marketing kit with the embargo notice: approved boilerplate for both brands, the pre-cleared quote, logo and banner assets - so their same-day post needs no extra approval round-trip.
4. Anchor to the flagship event when question 4 has one; a quiet-week reveal diffuses the press moment the simultaneous lift exists to create.
5. Coordinate social posts within roughly 15 minutes of the wire time (PR-practice inference); give 1-2 weeks of embargo lead for security-sensitive launches.

## 4. Ongoing featuring and spotlight program

"App of the month" hides at least three structurally different programs - no two operators run the same mechanic. Three shapes, ranked; they compose (Shopify runs the first two in parallel), so the menu picks a starting rung, not a religion:

- operator effort (descending): `menu-priced paid catalog > time-boxed editorial rotation > always-on quality-gated badges` - fulfillment machinery, then standing weekly editorial labor, then criteria set once and re-audited
- new-app surfacing (descending): `time-boxed editorial rotation > menu-priced paid catalog > always-on quality-gated badges` - badge thresholds (Shopify requires 50 net installs and 5 reviews) structurally exclude new apps
- efficiency: `always-on quality-gated badges > time-boxed editorial rotation > menu-priced paid catalog`

- **Default rung: always-on quality-gated badges and tagged collections** (Shopify Built for Shopify; Atlassian's Spotlight/Rising Star/Bestseller badges; HubSpot tier badges as a search filter). Publish the eligibility gates and re-audit on a cycle - losing the badge drops the endorsement, not the listing.
- **Layer on a time-boxed editorial rotation** when surfacing new and small apps matters - Shopify Staff Picks rotates roughly weekly, selects explicitly not on install base, and the lift for a small app can be large (Shippo reported 3x normal signups during its pick week - vendor-reported anecdote). This is the calendar-fair complement to the badge's traction gate, not its replacement.
- **Starved option: the menu-priced paid catalog** (Salesforce's AMP: ~$4K industry e-books, ~$14K webinar promotions, $5K-$7.5K paid-media extensions, one application per partner per quarter - operator-published price points). Highest revenue and highest fulfillment effort; it loses every efficiency round. A partner base whose co-marketing demand outstrips team capacity even after tier-gating promotes it - and it requires published pricing, or it reads as pay-to-play favoritism.

When publicizing badge benefits, state only what's documented and label it: Shopify publishes "an average increase of 49% new installs in 14 days of achieving status" (operator-published), but independent developer rank-tracking found no organic keyword-rank change from the badge - the figure is contested, and partners measure. Overclaim and they will call it out publicly.

Cross-operator mechanics and the full Shopify case: [references/featured-and-spotlight-programs.md](references/featured-and-spotlight-programs.md).

## 5. Budget split: demand gen vs per-partner co-marketing

The load-bearing operating-model finding across every operator studied: marketplace marketing is structurally two motions, not one.

- **Platform-wide demand generation** (marketplace SEO, curated collections, category pages, keynote launches) is non-rival - one partner benefiting costs the others nothing - so fund it broadly for every partner.
- **Per-partner co-marketing** (MDF, co-sell, custom campaigns, spotlights) consumes real staff time per engagement, so every operator studied rations it rather than offering it broadly.

Atlassian states the posture outright in its developer docs: it "focuses on general promotion of the Atlassian Marketplace, rather than individual co-marketing with partners," reserving prioritized co-marketing for higher partner tiers.

Default every partner to the demand-gen baseline, then pick a rationing mechanism for the rival layer and publish it:

- setup effort (descending): `partner-tier ladder > menu-priced catalog > invitation cohorts` - a tier program is standing governance with quarterly evaluation; a catalog is productized offerings; cohorts are batch programs
- allocation transparency (descending): `menu-priced catalog == partner-tier ladder > invitation cohorts` - the tie holds because both publish objective criteria a partner can self-assess against (a price, a threshold); invitations are opaque by construction
- efficiency: `partner-tier ladder > invitation cohorts > menu-priced catalog`

- **Default rung: gate co-marketing on the partner-tier ladder** - the pattern at HubSpot (MDF prioritized to higher tiers), monday.com (MDF and lead sharing from Silver up, tiers by ARR band), Microsoft (benefits tier by trailing-12-month marketplace sales), and Atlassian. Reuse the tier program question 7 found; if none exists, the tier design belongs to the marketplace-strategy sibling, not here. Microsoft publishes a rare ROI claim for gated benefits - participants' marketplace sales average 5x non-participants' (vendor-published; selection effect not controlled, so treat as directional).
- **Invitation cohorts** (HubSpot's 6-week Partner Growth Accelerator; Salesforce's $50M Builders Initiative aimed at early-stage ISVs) are the cheap complement for a segment the tier ladder structurally starves - partners too new to have climbed it.
- **Starved option: the menu-priced catalog** - same rung as in section 4, promoted at the same scale condition, self-funding once productized.

The efficiency framing has a documented blind spot: partner programs that only fund what ranks well over-serve sales-adjacent co-marketing and starve slow compounding investments (technical enablement, new-partner surfacing). Question 9 answering "compounding asset" promotes the starved rungs deliberately.

Operator mechanisms, tier structures, and the named practitioners (Scott Brinker's ecosystem-sandbox framing, Jay McBain's "decade of ecosystems") to cite when a skeptical executive asks why the marketplace deserves broad demand-gen funding: [references/comarketing-allocation-and-tiers.md](references/comarketing-allocation-and-tiers.md).

## 6. Measurement

The program document passes when three gates hold - self-set gates, since no industry pass-standard exists for a marketing-program artifact; iterate until all three pass:

1. Every cohort or credibility claim in launch material traces to the review gate (step 1) - a "curated" claim without a gate behind it fails.
2. The reveal plan names one canonical embargo time and every partner has the co-marketing kit before it.
3. The rival co-marketing layer has a published allocation rule (tier threshold, price, or cohort criteria) a partner can read - an unpublished rule fails.

Post-launch, track:

- **Launch moment:** press pickup and partner same-day posts vs cohort size; day-one installs.
- **Featuring program:** install lift during and after a feature window, baselined against the app's own prior fortnight before you publicize any average.
- **Budget split:** share of partner-marketing spend on non-rival demand gen vs rival co-marketing; count of partners touched by each motion. The rival layer touching only the top tier is by design; the demand-gen layer touching only some partners is a bug.

Baseline against your own first quarter; the operator anchors in the references are context, not targets.

If your harness has persistent memory, record:

- the chosen cohort shape and size
- the event anchor and embargo time
- the featuring rungs chosen, with their promotion conditions
- the published allocation rule

Later runs (each new app launch, each quarterly tier review) should inherit these instead of re-asking.

## Failure modes

- **Marketing a migrated catalog as a curated cohort.** Press counts independently: monday.com claimed "over a hundred" launch apps, press counted 78; Atlassian's 1,000 was a migration. Claim only what the gate vetted.
- **Overclaiming featuring effects.** Shopify's 49%-install-lift figure is operator-published and its keyword-rank effect is contested by independent tracking. Partners run their own rank trackers; publish only baselined, labeled figures.
- **A partner release jumping the embargo.** One partner publishing early scoops the operator's own reveal. Fix: one canonical time in every kit, and the kit ships with the embargo notice, not after it.
- **Unpublished rationing.** Bespoke co-marketing granted ad hoc reads as favoritism to every partner who didn't get it. Publish the tier threshold, price, or cohort criteria - transparent rationing is the mechanism that makes saying no survivable.
- **Undisclosed paid placement.** A paid slot that reads as an editorial pick spends the trust the review gate bought. Label paid placement as paid.
- **Efficiency ratchet.** Funding only what measures well starves new-app surfacing and technical enablement - the documented partner-program failure. Re-promote the starved rungs on a schedule, not only when metrics demand it.

## Invocation examples

- "Our app marketplace goes live at our user conference in June - how many launch partners do we need and how do we coordinate the announcement?"
- "Design our featured-apps program: badges, staff picks, or should we charge for placement like Salesforce does?"
- "Partners keep asking for co-marketing and we're drowning - how do we decide who gets MDF without it looking like favoritism?"

## References

- [references/launch-cohort-benchmarks.md](references/launch-cohort-benchmarks.md) - 12-operator founding-cohort table with dates, vetting-gate quotes, cohort tiering, marquee anchors, wave sequencing, and the day-one-number caveats.
- [references/featured-and-spotlight-programs.md](references/featured-and-spotlight-programs.md) - cross-operator spotlight mechanics and the Shopify Built for Shopify / Staff Picks parallel-program case, contested figures labeled.
- [references/comarketing-allocation-and-tiers.md](references/comarketing-allocation-and-tiers.md) - the two-motion budget split with each operator's rationing mechanism, tier structures, and the ecosystem-marketing practitioners to cite.

See also, same collection:

- `samber/developer-platform-skills@connector-marketplace-strategy` - whether to build the marketplace at all, its operating model, and the seeding sequence this skill's launch executes; run it first when build/join/buy is still open.
- `samber/developer-platform-skills@app-marketplace-review` - the security/quality review gate every "vetted cohort" claim in step 1 depends on.
- `samber/developer-platform-skills@partner-app-onboarding` - the partner onboarding journey that fills the cohort pipeline this skill reveals.
- `samber/developer-platform-skills@app-marketplace-listing-standards` - listing content rules; this skill markets the apps, that one governs what a listing must contain.
- `samber/developer-platform-skills@app-marketplace-monetization-model` - rev-share and billing mechanics; featured-placement revenue and take-rate interact there, not here.
- `samber/developer-platform-skills@integration-listing-optimization` - the submitter side: a vendor optimizing its own listing on someone else's marketplace.

Bespoke one-to-one joint campaign planning with a single named partner is out of scope - this skill designs the operator's one-to-many program.
