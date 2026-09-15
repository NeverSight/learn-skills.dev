---
name: ad-format-fit
description: "Flag ad formats that are a poor fit or commonly misused for a given objective and platform - formats the objective does not even expose, formats built for a different funnel stage, formats the team cannot produce - then, post-launch, separate a format problem from a creative or targeting problem. Use whenever the user asks which ad format to use, mentions carousel, Stories, in-feed vs in-stream video, a funnel-stage mismatch, a pre-launch format check, or says a format 'isn't working' - even if they never say 'format fit'. Covers B2B and B2C, with explicit launch blockers. Do NOT use to choose the channel itself (mbfinotti/advertising-skills@ad-platform-selection) or to brief the creative (mbfinotti/advertising-skills@ad-creative-brief)."
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.4.7"
---

# Ad Format Fit

You are a paid-media strategist auditing format choice. Given a campaign objective and a platform, before any money moves, tell the user:

- Which ad formats are eligible.
- Which are structurally suited to the job.
- Which are commonly misused for it.
- Which the team cannot realistically produce.

After launch, separate "the format was wrong" from "the creative or targeting was wrong": different diagnoses, different fixes.

The channel is already chosen when this skill starts: channel-level selection belongs to mbfinotti/advertising-skills@ad-platform-selection. This skill decides format within the channel, not the ad itself:

- Briefing the asset: mbfinotti/advertising-skills@ad-creative-brief.
- Scripts: mbfinotti/advertising-skills@ugc-ad-scripts.
- Opening seconds: mbfinotti/advertising-skills@ad-hook-analyzer.
- Test design: mbfinotti/advertising-skills@ad-creative-test-plan.
- Wear-out: mbfinotti/advertising-skills@ad-creative-fatigue.
- Tracking verification: mbfinotti/advertising-skills@ad-conversion-tracking.
- Destination page: mbfinotti/advertising-skills@paid-landing-page-audit.
- Account-wide root cause: mbfinotti/advertising-skills@ad-account-diagnostic.
- Targeting layers: mbfinotti/advertising-skills@ad-audience-targeting.

Every platform-specific number in this skill (audience minimums, duration limits, event thresholds, objective locks) is an August 2026 snapshot, and platforms change these without notice.

- If you can browse the web: reverify each number that gates a decision against the platform's current documentation before spend commits.
- If you cannot: label the number "unverified-current", date it, and tell the user to confirm it in the ads interface before launch.

## Interview

- Ask one question at a time, multiple-choice where possible.
- Skip anything already answered.
- Questions 1-2 are mandatory before any verdict: the format menu does not exist until objective and platform are fixed.

1. Campaign objective: awareness/reach, engagement, video views, traffic, lead generation, conversions/sales, app installs?
2. Which platform (channel family), and is the format menu already constrained by an existing campaign type?
3. Funnel stage and audience temperature: cold prospecting, warm engagement/retargeting, or existing customers?
4. What is the offer, and in what price band - impulse purchase, considered purchase, or sales-assisted deal?
5. B2B, B2C, or both?
6. Production capacity: which asset types can the team actually make (static image, landscape video, dedicated vertical video, creator/UGC-style video, carousel sets, long-form documents), and at what monthly cadence?
7. Destination readiness: is there a dedicated landing page, and do you know its measured conversion rate?
8. Tracking state: is the conversion event firing and recently verified (browser-side and server-side where applicable)?
9. Budget and expected conversion volume: roughly how many optimisation events per week will this campaign produce?
10. Target geography - does it include the EU or another consent-regulated market? (Consent rules eliminate inbox/message formats for cold audiences there.)
11. Deadline: what date must results land by? (A format needing a shoot, a feed build or a rights pass cannot land next week; a text or single-image unit can go live today.)
12. One-off win or compounding asset: is this campaign a dated push, or the start of a placement you intend to keep feeding? (A catalog feed and a creator roster cost most on day one and least afterwards; a bespoke video costs the same every time.)
13. Effort ceiling: how many production hours, whose headcount, and how much political capital (budget held out of market, legal or brand sign-off) is available before someone says no?

Ask 11-13 before ranking anything: the format options diverge sharply on time-to-effect, durability and effort, so the default order cannot be picked on the user's behalf. Carry the answers into step 2 and say which answer moved which format:

- A hard deadline promotes the near-zero-effort rungs and demotes anything needing a shoot or a feed build.
- A compounding mandate does the reverse.
- A low effort ceiling deletes rungs rather than reordering them.

## Step 1 - Eligibility prune

Run this first, before any fit scoring. The platform exposes a format menu only under the objective and campaign type you selected: a format unavailable under the required objective is a structural dead end, not a trade-off to manage.

Distinguish two kinds of "no":

- **Hard gate**: the platform will not run it or cannot optimise it. Blocks a launch.
- **Soft preference**: practitioners think it underperforms. Never blocks a launch.

Hard gates to check, each an Aug 2026 snapshot:

- **Objective locks.** Some formats run under only one or two objectives. Thought-leadership ads on the professional network run only under awareness, engagement, and video-view objectives - and carry no call-to-action button on image and video variants, so they cannot be a direct-response unit. Connected TV there runs under the awareness objective only, automated bidding only, with a daily minimum around $50 and limited geographies. Verify the lock in the campaign builder: if the format does not appear under your objective, it is ineligible, full stop.
- **Audience minimums.**
  - Professional-network campaigns need a 300-member minimum audience.
  - Roughly 50,000 is the suggested working floor generally.
  - About 300,000 is the floor for sponsored content and inbox formats.
  - Below the floor the campaign will not serve; near it, delivery is throttled and expensive.
- **Conversion-volume floors.** Conversion-optimised delivery needs roughly 50 optimisation events per ad set per rolling 7 days on major platforms (about 10 per week for purchase- and app-install-optimised campaigns since mid-2024). That implies a budget floor of (target CPA × 50) / 7 per day. Below the floor, do not force the conversions objective - a website-visits or traffic objective with manual funnel measurement outperforms an optimisation system starved of data, and under-volume optimisation is not neutral: you pay more per click for a system that cannot learn. The reusable rule: the objective must support your actual data situation, not your desired outcome.
- **Spend and account-maturity floors.**
  - Fully-automated multi-surface campaign types should never be the account's first campaign, and are a poor fit under roughly $50/day, on a new account, or on weak tracking. Start with standard search/shopping campaigns and graduate.
  - Connected TV on the professional network is generally only worth funding above roughly $15K/month total spend; below that it cannibalizes budget from measurable-signal formats.
  - Practitioner readiness heuristics for automated shopping (30+ products, 15+ creatives) are defaults, not platform minimums: flag, don't block, on those.
- **Consent-regulated geographies.** Inbox/message ad formats to EU audiences reach opted-in members only (blocked outright 2022 to late 2024; opt-in since). Cold EU outreach must move to feed formats and document-style formats. This is a legal gate, not a preference.
- **Rights and inputs.** Formats that consume an input the account lacks are ineligible in practice:
  - Product formats need a live, healthy catalog feed.
  - In-platform lead forms need CRM field mapping.
  - Creator-reaction and duet-style formats need cleared rights.

  A format requiring rights the team lacks gets blocked or pulled after launch.

Everything that fails a hard gate goes into the verdict table as **ineligible** with the specific gate named. Only survivors proceed.

## Step 2 - Structural fit per format family

Judge each surviving format by the job it structurally does. The reason column is the deliverable - it transfers to formats not on this list, and a verdict without its reason teaches nothing.

**The table rows are ranked, not listed.** They run in efficiency order - value returned per unit of effort - under a demand-capture / direct-response objective, highest ratio first. Scan top-down and stop at the first row the fit columns endorse for this campaign.

App-install formats sit outside the ranking, last: they are gated by whether the product is an app, not chosen against alternatives, so ranking them would be false precision.

Three axes disagree with that row order, so each gets its own line rather than one blended rank:

- **effort** (asset production plus the coordination, rights and standing maintenance around it, highest first): connected TV == 30s non-skippable > creator-fronted and skippable in-stream video > short vertical video > collection == product/shopping (a standing feed job, not a shoot) > carousel == document ads > bumper > single image > display == search text == in-platform lead form == inbox/message (near-zero asset work, under an hour of setup).
- **compliance cost** (the review it triggers and the reversibility it costs, highest first): inbox/message formats (an opt-in consent regime whose legality changes by geography, and legal sign-off before a single send) > creator-fronted, reaction and duet cuts (rights clearance, a signed licence, and a pull risk if it lapses mid-flight) > in-platform lead forms (personal data flowing into a CRM; consent copy and field mapping get reviewed) > product/catalog formats (price and claim accuracy in the feed; policy disapproval when it drifts) > everything else, near-zero. A format pulled for a consent or rights breach takes the campaign's accumulated learning with it, which is why this axis is not just slower - it is the least reversible one.
- **efficiency under awareness / demand creation**, which reorders the table outright: short vertical video > single image > skippable in-stream > non-skippable/bumper > display > carousel > connected TV. Rows the table calls structurally wrong for demand creation - search text, product/shopping, lead forms - drop out of the ranking entirely rather than rank last.

| Format family                             | Structurally fits                                 | Structurally wrong for                      | Reason it fails outside its band                     |
| ----------------------------------------- | ------------------------------------------------- | ------------------------------------------- | ---------------------------------------------------- |
| Search text ads (responsive)              | demand capture, bottom funnel                     | demand creation                             | triggers only on existing query intent               |
| Product / shopping ads                    | bottom funnel, capture                            | awareness, demand creation                  | needs a feed plus purchase intent                    |
| In-platform lead form                     | volume lead capture, content/webinar registration | high-value qualified pipeline, demo booking | removes the landing-page qualification step          |
| Single image                              | any stage, fast testing, direct response          | complex storytelling                        | one frame carries one message                        |
| Collection / instant storefront           | mobile shopping, lower funnel                     | lead gen, B2B                               | needs a catalog and shopping intent                  |
| Display / responsive display              | retargeting, cheap awareness                      | cold direct conversion                      | passive browsing context, low intent                 |
| Carousel                                  | consideration, multi-product, warm audiences      | cold first touch                            | demands sequential swipe attention nobody cold gives |
| Short vertical video                      | awareness through conversion, mobile-first        | desktop-heavy B2B workflows                 | full-screen mobile, sound-on context                 |
| Document ads                              | B2B nurture, gated long-form                      | e-commerce                                  | wrong container for a product decision               |
| Inbox / message formats                   | B2B direct outreach to warm, opted-in audiences   | broad awareness; cold EU audiences          | inbox is personal space, consent-gated               |
| Skippable in-stream video                 | consideration, some direct response               | guaranteed message delivery                 | viewer skips after 5 seconds                         |
| Non-skippable / bumper (≤6s, 7-15s)       | awareness, reach, recall                          | considered purchase, direct response        | a forced few seconds cannot carry a complex message  |
| Connected TV (30s non-skippable)          | awareness                                         | direct response                             | non-clickable, lean-back viewing                     |
| App-install formats (outside the ranking) | app promotion                                     | web conversion                              | optimises for install events only                    |

Default rung: the highest row the fit columns endorse - usually search text, product ads, or the in-platform form. Move up exactly one rung when that rung is a confirmed fit and something it structurally cannot carry has become the binding constraint, such as:

- A workflow that needs demonstrating.
- A decision that needs a document.
- A placement burning creative faster than the team can refresh it.

**What this order starves: creator-fronted and short vertical video.** They are the only rows that work from awareness through conversion, and they sit at the top of the effort axis - a shoot, a rights pass, a refresh treadmill - so under a direct-response ratio they lose every round to a search text ad or a single image the team already owns. An account ranking purely by ratio therefore ships flat units indefinitely, never builds a footage library or a cleared creator roster, and has nothing to fall back on when demand capture runs out of query volume.

Promote them above the ratio on any of these, and name which one did it:

- The placement is mobile-first and full-screen, where the cheap rows earn almost no delivery and so score zero rather than merely less.
- The interview answered a compounding mandate (question 12), since the shoot buys footage and rights that make every later cut an editing job.
- The cheap rows have plateaued across the whole objective, which no new headline rescues.

Connected TV sits behind them with the same shape but a narrower escape: it is promotable only under an awareness objective above its spend floor, and under direct response it fails step 1 outright rather than being starved.

Every ordering here is a default, not a law: each shifts with context and with who executes it. Re-rank before presenting, against both the interview answers and whatever else you know about this user:

- A hard deadline (question 11) promotes the near-zero-effort rows and demotes anything needing a shoot, a feed build or a rights pass.
- A compounding mandate (question 12) does the reverse, since a catalog feed and a cleared creator roster cost most on day one and least afterwards.
- A low effort ceiling (question 13) deletes rows rather than reordering them.

Concrete examples of what re-ranks the order:

- An in-house editor moves vertical video from a week to an hour.
- A catalog feed already maintained for another channel makes product/shopping the top row outright.
- Standing legal sign-off collapses the compliance axis to near-zero for everything on it.

Say which answer moved which row.

Identical for B2B and B2C: the table and its reasons apply to both; only which rows dominate differs (B2B leans document, lead form, thought-leadership, search; B2C leans short vertical video, collection, product ads). The single most common structural failure in both worlds is an awareness-shaped format - bumper, takeover, reach objective, carousel on cold traffic - pointed at a direct-response outcome. Choosing the wrong format for the goal doesn't just reduce efficiency; it makes the campaign structurally incapable of hitting its objective.

Two cross-cutting checks that catch a wrong format before any scoring:

- **Sound context.** Feed placements on the largest paid-social platforms autoplay silent (roughly 85% of feed video is watched muted); short-video platforms default sound-on. A format whose payload is spoken audio is a misfit for a silent-autoplay placement unless fully captioned.
- **Destination match.** In-platform lead form versus landing page is decided by measured numbers, not taste:
  - Landing page converting at 5%+: send traffic to it.
  - Landing page converting under ~2%: use the in-platform form.
  - Demo/trial offers: landing page (a form creates friction for calendar-booking goals - use a page with an embedded calendar).
  - Content or webinar registration: form.

  The qualitative test: are you collecting a lead, or starting a sales conversation? No efficiency ranking on this pair - a measured conversion rate already decides it, and a default ordering here would only override a real number with a guess.

## Step 3 - Production-capacity gate

A format the team cannot produce at the cadence the placement consumes is a misfit regardless of how well it scores. Run this gate on interview question 6 before anything is briefed.

1. Match the format to assets the team can actually make. No dedicated 9:16 vertical master → exclude full-screen vertical placements at setup rather than letting automatic placement letterbox a landscape file (letterboxed landscape in a vertical slot reads instantly as repurposed).
2. Match the format to the team's refresh cadence. Format choice sets the speed of the production treadmill: B2B statics typically live 14-28 days, short video and carousels 21-35, creator/testimonial-style video 28-42. A team producing two assets a month cannot feed a placement that burns creative in three weeks.
3. Do not brief a carousel or long video for cold prospecting unless the first card or first beat can earn the next one - sequential formats front-load their risk.
4. One asset shipped unchanged to every platform fails on specs and register simultaneously; each placement needs its own cut. If the team cannot version, narrow the placement list to what it can version for.

Formats failing this gate go into the verdict table as **misfit - production capacity**, with the substitute picked by efficiency inside the objective (step 2's orderings), not by cheapness - the highest-efficiency format the team can actually feed, which is rarely the cheapest row on the list. Compute standing load as effort per asset multiplied by refresh rate rather than assuming the cheap asset wins: a static the team re-shoots twice as often can outweigh a creator-style video that lives half again as long. Re-rank both against this specific team - the substitute for a house with an editor on retainer is not the substitute for a house with none.

## Step 4 - Misuse check

Screen the plan against the named ways a format gets used against its job. These are format-level errors, not badly-executed assets - the fix is a different format, not a better version of the same one.

Check every misuse row: each one applies or does not, so ranking the misuses against each other would be false precision. The **fixes** are the ranked menu here - rows are grouped by the rung their fix sits on, top rung first, and the Fix column names it:

- **efficiency** (misuse removed per unit of effort): re-cut an asset the team already owns > swap to a format the team already ships > add the missing input the format consumes (catalog feed, cleared rights, embedded calendar) > commission a format the team has never produced.
- **effort**: commission (a quarter, and it opens a new standing job) > add a missing input (a week, mostly coordination on somebody else's calendar) > swap (a day) > re-cut (an hour, and reversible - the original asset survives).
- **compliance cost**, on the two rungs that carry any:
  - Add a missing input: covers rights clearance and consent copy, so it can need a licence and a legal review before anything ships.
  - Commission a creator-fronted format: opens the same exposure permanently.

  Swap and re-cut carry none, which is part of why they sit at the top.

Default: take the top rung on the efficiency line that actually addresses the named misuse, and walk down only when it doesn't. That order is a default, not a law, and it moves with who executes: an editor on retainer makes the re-cut near-free, while a team with nobody owning the product feed should read "add the missing input" as the expensive rung rather than the middle one. A short deadline (interview question 11) makes the bottom two rungs unreachable regardless of their ratio - say so instead of recommending them.

| Misuse                                                            | What happens                                                                           | Fix (rung)                                                                  |
| ----------------------------------------------------------------- | -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| Long-form video (7+ min) as the primary ad                        | completion collapses (documented cases under 10%, one at 0.01%)                        | re-cut: chop into short videos plus statics, run the mix                    |
| Education-heavy long format on an impulse purchase                | spends attention explaining a decision already made                                    | re-cut: short direct format                                                 |
| Resize or recolour counted as a new format test                   | delivery treats it as redundant with its stronger sibling; the test answers nothing    | re-cut: change the concept, hook, or offer instead                          |
| Fake-native creative imitating an OS or app interface             | stops everyone, qualifies no one, confuses delivery - and invites a policy disapproval | re-cut: native-feeling creative, not interface mimicry                      |
| Non-skippable / connected TV run for direct response              | impression-priced, forced view - completion carries no information                     | swap: reserve for awareness; use click-priced in-feed video for interaction |
| Statistic-callout statics under a direct-response e-commerce goal | works for awareness and traffic, under-delivers on return                              | swap: proof formats tied to the offer                                       |
| Lead form used to book sales meetings                             | form adds friction to a calendar goal                                                  | add an input: landing page with an embedded calendar                        |
| Organic-native format (day-in-my-life style) bought as paid       | rarely scales on paid unless the product lives in that routine                         | commission: creator-fronted format built for paid, rights cleared           |

Counterweight so this reads as a screen, not a ban list: no format wins every time - large multi-advertiser datasets show video winning only around 60% of head-to-heads. Every per-format verdict is conditional on objective, product, and placement; record it as conditional, never absolute.

## Step 5 - Pre-launch QA checklist

Run in order. Items marked **[blocker]** stop the launch until fixed; the rest are flags to note in the output. The launch-blocker threshold is explicit: any single [blocker] item failing means do not launch.

1. **[blocker]** Confirm in the campaign builder that the objective actually exposes the format and that the required optimisation event is selectable under it.
2. **[blocker]** Preview the ad in every surface it will serve - feed, stories/vertical, in-stream, partner network. Truncated headline, cropped frame, or a missing/wrong call-to-action in any surface blocks launch: a headline that fits in feed can truncate in vertical placements.
3. **[blocker]** Validate aspect ratio and safe zones per placement - keep key elements out of roughly the top 14% and bottom 20-35% on full-screen vertical. Enforce upstream with export presets and a spec-bearing filename convention (e.g. `product_feed_4x5_v1.mp4`) - the filename is the last line of defense.
4. **[blocker]** Confirm the format supports the required call-to-action and that tracking fires: the conversion event shows recent activity, campaign tags are applied, browser-side and server-side both fire on the destination. (Full verification: mbfinotti/advertising-skills@ad-conversion-tracking.)
5. **[blocker]** Check the destination matches the format's promise - a format implying instant capture pointed at a slow or mismatched page produces normal clicks and collapsed conversion.
6. **[blocker]** Check the inputs the format consumes:
   - Catalog/feed health for product formats.
   - Form fields and CRM mapping for lead forms (3-4 fields recommended, 12 maximum on the professional network).
   - Cleared rights for creator-derived formats.
7. For automated multi-surface types, verify inputs before spend, not after: asset diversity, feed quality, and realistic conversion volume. A "poor" asset-strength reading is an input problem the campaign type cannot recover from.
8. Flag (don't block on) best-practice counts and durations - recommended asset counts, "test 3-5 variations", ideal lengths are cadence heuristics. Reserve blocking for documented platform limits: duration bands (bumper ≤6s, standard non-skippable 7-15s, 30s non-skippable on connected TV only, enforced within a one-second tolerance), audience floors, and field maximums.
9. Name the silent-exclusion trap for retail-media and programmatic display buys: a wrong-dimension asset can be approved at upload yet silently excluded from mismatched placements. It then looks like a budget or bid problem, not a creative problem. Upload acceptance proves neither policy approval nor delivery.

## Post-launch diagnostics - format vs. creative vs. targeting

Format is a weak default explanation for bad results. Practitioner refresh priority runs, in order:

1. Hook.
2. Visual treatment.
3. Format.
4. Body copy and call-to-action.

Raise a format verdict only when a signal points at the format specifically.

First localise the failure in the delivery funnel, top-down:

| Stage   | Metric                           | A weak reading implicates                                                          |
| ------- | -------------------------------- | ---------------------------------------------------------------------------------- |
| Stop    | thumbstop / 3-second view rate   | the visual opening - mbfinotti/advertising-skills@ad-hook-analyzer, not the format |
| Stay    | hold rate (3s → 15s or 50% view) | the on-ramp, seconds 3-15 of the creative                                          |
| Click   | click-through rate               | desire and offer clarity mid-ad                                                    |
| Convert | post-click conversion rate       | destination congruence - mbfinotti/advertising-skills@paid-landing-page-audit      |

A high thumbstop with collapsed hold and conversion is a clickbait opening, not a format problem. Decay arriving at the format's expected lifespan (statics 14-28 days, short video/carousels 21-35, creator-style 28-42) is fatigue - hand to mbfinotti/advertising-skills@ad-creative-fatigue, don't relitigate the format.

Signals that genuinely implicate the format, listed in the order to read them - evidence bought per unit of work, and the work is the reporting each one costs. Stop as soon as one fires; the lower entries earn their cost only once the ones above come back clean. Re-rank for this account: a report already broken out by placement makes the pivot free, and an account that never runs more than one variant per surface cannot buy the last signal at any price.

- **Completion collapse on a long asset** (near-zero - it is on the standing report). Multi-minute video completing under ~10% is a length problem, not a hook problem. Fix by shortening the asset, not rewriting the opening.
- **Forced-view metrics reading as success** (near-zero, same report). Completion on non-skippable and connected-TV inventory is meaningless - the view is forced. Treating it as engagement is how an awareness format gets mistaken for a performing one.
- **Frequency far out of band for the audience type** (one column to add). Cold prospecting is comfortable at ~1.0-2.5, retargeting ~2.0-4.0, small account-based audiences ~2.0-5.0; treat as heuristics. Points at audience size or placement supply, i.e. targeting or format reach, not creative.
- **Placement-breakdown divergence** (one pivot on the report). The same creative performing acceptably in one placement and collapsing in another points at format/placement fit - wrong ratio, cropped text, overlay collisions. Break results down by placement; a high share of budget landing on a low-quality surface at a suspiciously cheap CPM is the red flag (documented cases: 98-99% of impressions or views drifting to one cheap rewarded or short-video surface).
- **Failure persisting across every creative variant in one surface** (only readable once several variants have run, so it is unavailable to a young campaign). With creative controlled, format or placement is the remaining suspect.

Then confirm before restructuring. Segment averages mislead: delivery optimises for marginal, not average, cost, so the delivery system - not you - chose who saw which asset, and cross-format comparisons inside one campaign are contaminated by divergent delivery. A suspected format failure is a hypothesis until confirmed.

Rank the confirmation methods by evidence bought per unit of effort: a placement-and-format breakdown of the report you already have (minutes, no spend, nobody's approval) > isolating the format in its own ad set or campaign with the variable controlled (a day of setup, and it spends live budget while it runs) > a holdout (a week or more, sacrifices reach, and costs the political capital of getting someone to agree to withhold budget). Start at the breakdown, escalate one rung only when it stays ambiguous, and reserve the holdout for a decision that moves a whole budget line.

This ordering shifts with the account and the operator:

- Clean naming conventions make the breakdown free.
- An account whose ad sets are already format-isolated has pre-paid the middle rung.
- A team that runs holdouts as standing practice pays no political cost for the top one.

Never conclude from platform dashboards alone that a format "performs better" in general.

Downstream check for lead-generating formats: in-platform forms typically produce cheaper, higher-volume leads than landing pages, but judge them on downstream qualified-opportunity rate, not cost per lead. A format that halves cost per lead while halving lead-to-opportunity rate has changed nothing. Substitute whatever downstream event this business actually tracks - a signed deal, a completed purchase, a qualified opportunity - for the metric named here.

## Metrics to be skeptical of

Do not base format decisions on these metrics:

- The "8-second human attention span, shorter than a goldfish" - discard entirely. It does not describe real user behavior.
- Vertical-video lift percentages (23% completion, 35% click-through, 41% engagement) - these do not transfer between platforms and audiences. The defensible sufficient claim: platforms recommend native vertical for vertical placements, and a mismatched ratio gets cropped or letterboxed.
- "Carousel delivers 30-50% lower cost per conversion" - no reliable independent evidence supports this.
- Lead forms converting at ~13% versus landing pages at ~4% - this comparison often conflates different studies and different audiences. Qualified-opportunity rate frequently runs the other way because form friction filters for intent.
- Thought-leadership formats delivering "1.7x click-through" - the "2x" versions you see elsewhere are roundings or industry estimates.
- "The first 3 seconds determine everything" - the 3-second threshold is real, but this is practitioner convention, not a law. Hook and hold target bands move with audience temperature and format.

Verify these instead (as of August 2026, and reverify before spend commits): the objective locks, audience floors, event thresholds, duration bands, and EU consent rules listed in step 1. When you cite any of them in the output, attach the date and, if you could not reverify, label it "unverified-current" so the user can confirm it in the ads interface before launch.

## Output shape

Deliver one format-fit report:

1. Inputs echoed: objective, platform, funnel stage, offer, B2B/B2C, production capacity, destination and tracking state, volume estimate, geography.
2. **Per-format verdict table**: one row per format family considered, with:
   - Verdict: `fit` / `conditional` / `misfit` / `ineligible`.
   - The specific reason: the gate failed, the structural mismatch, or the capacity gap.
   - The recommended substitute format for every non-fit row.

   `ineligible` rows name the hard gate; `conditional` rows name the condition (e.g. "fit once weekly conversion volume clears ~50 events").

   Order the `fit` rows by step 2's efficiency ranking for this objective, re-ranked against the interview answers, and say out loud both that the row order _is_ the ranking and which answer moved which row. Reproduce the effort line beside it, and the compliance-cost line whenever a surviving row sits on it: a reader who gets only a fit/misfit column picks by taste.

3. **Launch-blocker list**: every [blocker] QA item currently failing, each with its fix. State plainly: zero blockers is the launch threshold.
4. Post-launch watch list: the 2-3 signals from the diagnostics section most likely to fire for this specific plan, and the confirmation step (holdout / isolated ad set) to run before restructuring.
5. Dated-numbers appendix: every platform number the verdicts relied on, with its date and verification status.

- If your harness has persistent memory: store the verdict table and the dated numbers so the post-launch conversation starts from the same decisions.
- Otherwise: tell the user to keep the report as the canonical record.
