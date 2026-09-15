---
name: thought-leadership-ads
description: "Plan a campaign that promotes an executive's or founder's existing organic posts as paid person-fronted ads - post selection, sequencing, audience and exclusions, permission and governance, budget, and measurement. Use whenever the user mentions thought leader ads, promoting a founder's or CEO's post, sponsoring an employee's or a creator's post, executive content amplification, running ads from a personal profile, or B2B trust ads - even if they never say 'thought leadership'. Covers B2B trust-layer campaigns on professional networks with pipeline-lens measurement, and B2C founder-led brands with direct-response measurement. Plans the campaign only, never the featured person's content: ad copy is mbfinotti/advertising-skills@ad-copy-variants."
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.3.9"
---

# Thought Leadership Ads

Plan a paid campaign that amplifies a named person's own organic posts from that person's profile, under a paid-promotion label naming the sponsoring brand. The advertiser buys distribution for a post it does not own and cannot edit - every planning decision below follows from that constraint.

## Scope and handoffs

This skill selects posts, sequences the campaign, designs the audience, sets governance, sizes budget, and defines measurement. It hands off neighbouring work:

- Writing or improving the featured person's posts - never done here. This skill only chooses among posts that already exist.
- Working conversion tracking is a prerequisite → verify via `mbfinotti/advertising-skills@ad-conversion-tracking`.
- The broader layered targeting plan → `mbfinotti/advertising-skills@ad-audience-targeting`.
- The downstream retargeting sequence this campaign feeds → `mbfinotti/advertising-skills@retargeting-funnel`.
- Ad copy variants and creative briefs → `mbfinotti/advertising-skills@ad-copy-variants`, `mbfinotti/advertising-skills@ad-creative-brief`.
- Which channels to run at all → `mbfinotti/advertising-skills@ad-platform-selection`.
- Buying-committee role mapping → `mbfinotti/advertising-skills@ad-buyer-group-mapper`.
- Total budget split across campaigns → `mbfinotti/advertising-skills@ad-spend-allocation`.
- Ongoing decay monitoring after launch → `mbfinotti/advertising-skills@ad-creative-fatigue`.

If you draft any illustrative copy while explaining a step, route it through your preferred humanizer skill before the user ships it - AI-sounding text is a documented killer of this format (see Failure modes).

## Interview

Ask one question at a time, multiple-choice where possible. Stop as soon as you can plan. Do not run the full list when early answers already settle later questions.

1. Business model: (a) B2B, (b) B2C / consumer, (c) hybrid?
2. Who are the candidate featured people: (a) founder/CEO only, (b) several executives, (c) employees beyond the exec team, (d) customers or external creators, (e) a mix?
3. Have those people already agreed to have their posts promoted: (a) yes, explicitly, (b) informally / assumed, (c) not asked yet?
4. Does a written agreement exist beyond platform click-to-approve: (a) yes, (b) no, (c) only for some people?
5. B2B: typical ACV and sales-cycle length? B2C: typical order value and purchase-decision time?
6. Does each candidate already post organically - roughly how often, and is there an engagement history to score against?
7. What downstream capture layer exists today: (a) retargeting audiences + conversion campaigns live, (b) tracking live but no retargeting built, (c) nothing yet?
8. Monthly budget for this format, and a rough size for the target audience or account list?
9. What does the account currently pay per landing-page click on brand-account ads to a comparable audience, and what pipeline-to-spend bar should the two-quarter review judge against? Both are gate inputs, not context:
   - Without the first, the week-6 gate falls back to a provisional external bar.
   - Without the second, the lagging verdict has nothing to be measured against.
   - Agree the bar now, never at review time.
10. Regulated industry (financial services, health, or similar)?
11. Does the audience include the EEA or UK?
12. Date the result must land by: (a) inside this quarter, (b) two to four quarters out, (c) no fixed date?
13. One-off win or compounding asset: (a) clicks and pipeline from this flight, (b) a warm pool and a person-fronted channel that keeps paying?
14. Effort ceiling: hours per week available, and how much political capital - can you ask an executive to edit their own live post, and can you license a customer's content?

Re-rank every ordered menu below against answers 12-14, and say out loud which answer moved which option. Where an answer rules an option out entirely instead of merely lowering it, delete it by name rather than ranking it last.

- Answer 12 (date inside this quarter): fails the B2B trust layer at the eligibility gate and promotes the B2C direct-response shape.
- Answer 13 (compounding mandate): promotes trust-first sequencing, the multi-person roster, and the declared pool-builder link option.
- Answer 14 (low political-capital ceiling): promotes the pinned-comment link and employee-authored posts over an exec edit or a licensed customer post.

Every ordering in this skill is a default, not a law - it shifts with context and with who executes it. Re-rank against what you already know about the user - each of these invalidates an assumption the default order makes:

- A founder whose audience outranks the brand's.
- An in-house editor.
- A customer who has already licensed their content.
- A compliance team that clears a post in a day.

## Eligibility gate

Do not produce a plan when any of these holds. Say which gate failed and what to do instead - a plan that dies at day 45 is worse than a refusal.

- **No downstream capture layer.** Retargeting is not retroactive: audiences not being captured today are gone forever, and this format's main output is a warm pool. Build tracking and the retargeting scaffold first (`mbfinotti/advertising-skills@ad-conversion-tracking`, then `mbfinotti/advertising-skills@retargeting-funnel`), then return.
- **The featured person has not consented.** Consent is per-post, personal, and revocable - marketing cannot run this unilaterally. Get explicit agreement (and the written agreement from Governance) before planning around anyone. Never treat "the CEO will probably say yes" as consent.
- **Budget cannot sustain frequency against the audience.** If the budget spread over the audience yields near-zero frequency, nobody changes their mind. Shrink the audience to fit the budget (see Audience). If the user refuses both, decline the format.
- **B2B with low ACV.** This is a slow-payback trust layer. Practitioners cite roughly $25k+ ACV with a narrow ICP as the justification bar (practitioner-cited, not a law). Far below that, route the budget to direct-response and retargeting instead, where payback is measurable within the quarter.

A single-person program is not a hard stop but flag it: one revocation or resignation ends it (see Governance).

## Post selection

Select from what the person already publishes, never manufacture a post purely to be advertised - volunteer output beats mandated programs, and manufactured posts read as ads, which defeats the format.

1. **Apply the organic-validation rule, and disclose that it is contested.**
   - Majority practice promotes posts that already earned organic engagement, because existing reactions and comments carry into the ad as visible social proof.
   - A minority of practitioners argue performance comes from content quality, not pre-validation, and write posts intending to promote them.
   - Both camps agree on one thing: a post with a dead comment thread inherits that dead thread.
   - Default to validation. Note the minority view when the user has strong content but a small following.
2. **Score relative to that account's own median, not an absolute bar.**
   - Rank each candidate post against the author's trailing posts (engagement rate, comments, shares). Promote from the top quartile.
   - There is no defensible absolute threshold to hold every account to. One agency benchmark cites ~2-3% organic CTR as the candidate bar (agency-reported), usable as a cross-check only.
3. **Check format eligibility as a concept.**
   - Networks typically allow single-asset posts (one image, one video, plain text, long-form article, newsletter, event) and reject multi-asset or interactive ones (carousels, polls, document posts, reshares, celebration posts).
   - Platform documentation on this is internally inconsistent and changes often.
   - If you can browse the web, verify the current list on the chosen network before finalizing.
   - If not, mark each selected post "format eligibility: verify in platform".
4. **Respect the recency and edit window.**
   - Organic reach concentrates in a post's first ~3 days.
   - Let the surge settle, roughly a day past peak engagement, then have the author make any edit or add the pinned comment before launch.
   - The ad references the live post. A later edit changes a running ad.
5. **Solve the edit problem explicitly.** On trust-layer networks the advertiser cannot attach a URL or CTA. A link exists only if the author put one there. Three options, ordered by attributable clicks bought per ask made of the author:
   1. **Link in a pinned first comment.** The ask is one comment and it never touches the approved post, so it repeats across every person on the roster and every post in the quarter without spending capital you need later. Clicks are fully tracked. The volume is lower than an in-post link because the destination sits one tap away.
   2. **Tracked link edited into the post.** The most attributable clicks, and the only rung that puts the destination where the reader already is. It is also the largest ask in the format - an executive editing their own live post - plus a wait on their calendar and, in a regulated firm, a second pass through pre-publication review and retention (Governance).
   3. **No click destination, declared in writing as a retargeting-pool builder.** Near-zero ask, near-zero attribution: gate 1 below cannot be computed without landing-page clicks, so the campaign is judged on pool growth alone. A post with no link and no such declaration is a failure mode, not a minimalist choice.
   - value (attributable click volume): tracked link in post > pinned comment > no destination (zero)
   - effort (political capital spent, and a wait on someone else's calendar): tracked link in post > pinned comment > no destination
   - efficiency: pinned comment > tracked link in post > no destination

   **Default: the pinned first comment.**
   - What this order starves: the tracked in-post link buys the most attributable clicks in the format and costs the most political capital, so the ratio refuses it every round. A plan computing only efficiency never once puts the destination where the reader already is.
   - Promote the in-post link whenever the author edits their own posts without being chased - a founder who runs their own marketing, or anyone already on auto-approval - because the political-capital term collapses and the value term decides alone.
   - The ranking is a default, not a law: it turns entirely on who has to make the ask and to whom.

   **Delete, don't demote.** An executive who will not edit a live post does not push the in-post link to second place. It leaves that person's menu instead, and the plan names it deleted with the reason. Ranked second, it comes back in week 4 as an ask nobody is willing to make, against a gate that was already computed without it.

6. **Prefer the content the format rewards**, ordered by inherited engagement bought per unit of clearance work:
   1. **Employee low-polish posts about building the product or about the buyer's problem.**
      - The paid-promotion label plus the author's visible role clears them.
      - No licence, no negotiation, no second label.
   2. **Customer- or creator-authored posts.** They outperform employee posts on engagement and credibility (practitioner-reported) and rank second only because each one costs a licence, a partnership label, and a negotiation (Governance). They take first place once the licence is signed, or when the author is a name your ICP already knows.
   3. **Produced brand content posted from a personal profile.** Reads as an ad from the one account whose entire asset is not reading like one.
   4. **Product pitches.** Practitioners hold roughly 80% genuine thought leadership to 20% solution content across the promoted set.
   - value (engagement and credibility carried into the ad): customer/creator > employee build-in-public > brand-produced > pitch
   - effort and compliance cost (licence, extra label, negotiation): customer/creator > employee post > brand-produced == pitch
   - Brand-produced posts and pitches tie on that axis because clearance treats them identically - the brand's own words about the brand's own product, no licence, no partnership label, no negotiation. Everything separating them lives on the value axis, not the clearance one.
   - Delete, don't demote: with no route to license a customer's content (interview question 14), the customer/creator rung leaves the menu by name rather than sitting at the top of an order the user cannot execute.
   - Independent of the four rungs: evergreen > news spikes.

## Sequencing

Two documented sequences compete, ordered by warm pool built per week of setup:

1. **Trust-first (default).**
   - Person-fronted ads run cold to the ICP.
   - Engagers become a cheap, engaged retargeting pool.
   - Brand-labelled ads run to those engagers.
   - Social-proof formats run last.
   - Right whenever the featured person outranks the brand in recognition - the usual founder-led, early-stage, personal-brand-heavy case.
2. **Awareness-first.**
   - Cold brand-account ads establish awareness.
   - Person-fronted ads warm that audience mid-funnel.
   - Engagers get conversion-capable formats for the direct ask.
   - Right whenever the brand outranks the person in recognition.
   - Also right whenever a cold prospecting layer has to be built anyway to seed retargeting pools - then its extra layer buys two things at once and stops being extra.

- efficiency: trust-first > awareness-first
- effort (layers to stand up before this format serves one impression): awareness-first > trust-first
- value (minds changed per impression): trust-first > awareness-first where the person outranks the brand; the order inverts where the brand outranks the person

Say which one you chose and why - the wrong default here wastes the whole budget. The order is a default, not a law: recognition flips it, a compounding mandate (question 13) reinforces trust-first, and a deadline inside the quarter promotes neither, because both sequences pay back slowly (see Eligibility gate).

Both sequences agree on two invariants:

1. **The format must hand off to something that can convert.**
   - On professional networks it cannot carry a conversion objective at all. Prospects who engage with a person often never connect that person to the company.
   - Bridge deliberately: the person references the company in some posts, themes align across personal and brand streams, and proof formats reinforce later.
   - Design the downstream sequence via `mbfinotti/advertising-skills@retargeting-funnel` before launch.
2. **Every retargeting audience the sequence will ever need exists before the first ad serves.**
   - Post engagers, video viewers, ad engagers, page and site visitors: create them all up front.
   - Data not captured is unrecoverable.

B2C difference: consumer platforms allow direct-response objectives on the same mechanic, so the sequence can collapse to a single performance campaign - sequencing becomes optional there, not structural.

## Audience

- **Build from a matched account list plus function/seniority layering** (B2B): upload the target company list, expect a partial match rate, then layer job function and seniority on top. For named-account programs, contact-level lists of 500-2,000 people run at high frequency (agency-reported). B2C: start from the featured person's follower lookalikes and interest layers instead.
- **Size the audience to the budget, never to the market.** Published practitioner bands: 20,000-50,000 members for sub-$10k/month budgets (practitioner-cited), and a wider 5,000-50,000 band (vendor-published). The rule behind the bands is what matters: compute expected frequency (budget ÷ CPM ÷ audience) and shrink the list until frequency is meaningful. "Spending 2k/month against 300k people, no one's seeing your stuff" (practitioner).
- **Write the exclusion list.** It often ends up longer than the inclusion list (agency-reported, and correct).
  - Build every entry. When only part of it can ship before launch, order by wasted spend prevented per minute of setup: existing customers == open pipeline > employees > competitors > students > URL-based exclusion of logged-in users (the only entry that needs tracking work, and the only one platform support can withhold).
  - Existing customers and open pipeline tie because one CRM export produces both lists in the same minute of setup, and an impression on either is bought against an account already reached by name.
  - Every dollar shown to a customer or an employee is wasted twice: spend and credibility.
  - Where platform support withholds the URL-based exclusion, delete that entry from the list and say so in the plan. Left ranked last, it reads as pending work and quietly never lands.
- Route the wider layered-targeting design (interest, lookalike, retargeting tiers across the account) to `mbfinotti/advertising-skills@ad-audience-targeting`.

## Governance

Keep this practical: it decides whether the campaign can exist, keep running, and survive a departure.

- **Consent is per-post and instantly revocable.** The author approves each sponsorship in-platform, may enable auto-approval, and can revoke at any time - on revocation the ad turns off immediately. Plan for it as a live switch someone else holds.
- **Departure ends the campaign.** On professional networks the featured person must list the sponsor as a current employer or collaborator. Leaving breaks eligibility, and the creative cannot be retained, re-run, or re-hosted, because the post lives on their profile. Absent a written agreement, case law leans toward the individual owning the account and its content.
- **Mitigate with a portfolio.** Run several people's posts in parallel so one revocation or resignation cannot end the program, and write an explicit takedown-and-replace step into the plan.
- **Platform click-to-approve is not a commercial agreement.** Sign a written agreement per featured person, covering:
  - Usage fee (if any).
  - Term (commonly 30/60/90 days).
  - Spend caps.
  - Who may edit the post.
  - Pause and revocation handling.
  - Disclosure obligations.
  - For non-employees, add licensed usage rights.
- **Disclose.** A brand paying to amplify a post about itself is an endorsement with a material connection.
  - Employees: the platform's paid-promotion label plus the author's visible role is the practical mechanism.
  - Non-employees (customers, creators, independent experts): additionally require the partnership label.
  - Regulated firms (financial, health): pre-publication compliance review and retention are mandatory. A US regulator's first enforcement action in this area (2024) fined a firm $850,000 over unsupervised influencer posts.
  - UK/EEA: ads must be obviously identifiable as advertising even when the poster is commercially connected to the brand. EEA targeting excludes sensitive-category signals (some group/affinity targeting is disabled there entirely).
- **Treat the featured person as an approver with a veto, not a content supplier.** That inversion is the documented relationship failure mode.
- B2C difference: permission is commonly a per-video authorization code with a fixed term (7/30/60/365 days) - a licence with an expiry date to track and renew, rather than an open-ended toggle that can vanish mid-flight. Plan continuity around expiry dates instead of revocation risk.

## Budget and bidding

- **Concept first: the floor is the spend that buys meaningful frequency against the chosen audience for 4-6 weeks.** Compute it from audience size and expected CPM before quoting any published number.
- Published ranges, with provenance:
  - $50-100/day per campaign as the floor for meaningful data (practitioner-cited).
  - $1,500-3,000/month minimum and $2,000-5,000/month optimal per campaign (vendor-published).
  - Expected CPC $2-6 with precise targeting, $5-12 broader (practitioner-cited).
  - Treat all of these as cohort-dependent, not targets.
- **Cap the format's share of channel budget at roughly 25-40%.** The best-performing tier in the largest published portfolio was 25-50% of channel budget (vendor-published). The same source warns to expand the account list before scaling past ~40% - beyond that, you are buying more frequency against the same accounts, not more minds.
- **Widen the audience before adding budget.** Above the optimal per-campaign range, extra spend meets a saturated list. Grow the list first.
- Bidding pattern (practitioner-cited): maximum delivery for the first 7-14 days to gather cost data, then manual or cost-cap at 70-80% of the platform's suggested bid.
- Reconcile the funding-order dispute honestly:
  - One agency doctrine funds this format last (slowest payback of any campaign type, 90+ days to ROI).
  - The portfolio data above says once funded, fund it properly.
  - Resolution: fund it last, but never at token levels - a trust layer at 5% of budget produces frequency too low to change anyone's mind.
- Route the account-wide split across all campaigns through `mbfinotti/advertising-skills@ad-spend-allocation`.

## Measurement and pass gate

**Never judge this format on reported CTR.** The largest published dataset (119 sponsored posts, ~$300k spend, 211 companies - vendor-published) found reported CTR negatively correlated with pipeline (rho = -0.170). Worse, under an engagement objective the reported-CTR denominator includes reactions, comments, shares, and follows - so the format always "wins" on a number that is partly an artifact and does not predict revenue. The metric this format wins on is the metric that fails.

Split metrics:

- **Leading (diagnostics only, weekly), ordered by decisions changed per minute spent reading them:** cost per landing-page click (never reported CTR) > retargeting-pool growth > comment volume (highest-intent signal) > account-level engagement > frequency > engagement rate. The first two decide the week-6 gate below. Engagement rate ranks last because it is the closest cousin of the metric this format wins on and does not deserve.
- **Lagging (the verdict, 2-4 quarter window, B2B):** influenced pipeline, sales-accepted opportunities from engaged accounts, cost per opportunity. B2C: pixel-based CPA/ROAS on a short window - the CTR caution does not transfer, because the conversion is a purchase days later, not a pipeline guess.

**Week-6 review gate (B2B).** The campaign passes only if both hold:

1. Cost per landing-page click ≤ the account's own cost per landing-page click on brand-account ads to a comparable audience. If no brand baseline exists, use $3-5 as a provisional bar (vendor-published median territory), and label it provisional in the plan.
2. The engager retargeting pool has crossed the downstream platform's minimum serveable audience floor (commonly ~300 matched members - verify the current floor), so the handoff stage can actually launch.

Fail branches:

- Fails gate 1 only: the post is the problem. Rotate in a different validated post before touching audience or budget.
- Fails gate 2 only: the audience or budget is the problem. Widen the list or raise spend toward the floor.
- Both fail again after one post rotation (~week 10): pause the format and return budget to retargeting and direct-response.
- At the 2-quarter review, judge on the lagging set against a pipeline-to-spend bar agreed with the user during planning (account-based programs commonly plan against 3-5x, agency-reported).

**B2C gate:** run the person-fronted post against the brand-account creative as a split test. Keep it only while its CPA is at or below the brand-creative control. Refresh creative on the short-video cadence (3-7 days) or feed cadence (14-21 days) - both agency-reported - instead of the B2B two-week rotation.

## Failure modes

| Failure                            | What it looks like                                                                 | Fix                                                                                                                  |
| ---------------------------------- | ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Permission revoked / person leaves | Ad turns off instantly; creative unrecoverable                                     | Multi-person portfolio; written agreement before spend; takedown-and-replace step in the plan                        |
| Run cold as direct response        | Spend with no pipeline; "the format doesn't work"                                  | It has no conversion objective; design the handoff before launch (Sequencing)                                        |
| One profile carries everything     | The person's feed reads as all-sponsored; credibility being purchased is destroyed | Cap the promoted share of any individual's output; spread across people                                              |
| Budget-to-audience mismatch        | Frequency collapses; nobody sees anything twice                                    | Size audience to budget (Audience); shrink the list, not the ambition                                                |
| AI-sounding copy                   | Practitioners name it directly: "the em dashes, the vocabulary… AI slop"           | The format's only asset is a real person speaking; select only genuinely authored posts; humanize anything you touch |
| No link anywhere                   | Promoted post with no destination and no declared purpose                          | Pick one of the three edit-problem options and instrument it (Post selection, step 5)                                |

One criticism to state in the plan rather than suppress: the format works because it does not look like advertising, and critics call that stealth branding. The honest answer is stronger disclosure and genuinely useful content, not defending the ambiguity.

## Output shape

Deliver one plan document containing:

- Featured-person roster with consent and agreement status.
- Selected posts with their relative scores and link plan.
- The chosen sequence with the handoff design.
- Audience definition, exclusion list, and frequency math.
- Budget, bidding pattern, and allocation share.
- Governance annex (agreement terms, disclosure duties, takedown-and-replace).
- The measurement plan with both review gates and their fail branches.
- A named list of every option a stated constraint deleted from a menu.

A full worked example and a broken counter-example live in [./references/worked-plan-examples.md](./references/worked-plan-examples.md).

If your harness has persistent memory, record for later sessions to tune against instead of re-deriving:

- The chosen sequence.
- Audience sizing math.
- Gate thresholds.
- Each featured person's consent status.

If not, put that rationale block at the top of the delivered plan.

## Integration note (optional, vendor-specific)

The mechanic is platform-generic, but the named products differ in objectives, permission tokens, and CTA rights:

- LinkedIn Thought Leader Ads: trust-layer constraints described above.
- Meta Partnership Ads and TikTok Spark Ads: full-funnel objectives, per-post or per-video authorization.
- X Amplify: runs from the advertiser's account.

Two networks (YouTube, Reddit) have no equivalent - a plan naming them for this format is wrong, not suboptimal. Full comparison in [./references/platform-capability-matrix.md](./references/platform-capability-matrix.md). Capabilities changed repeatedly in recent years, so verify live before building.

## References

- [./references/worked-plan-examples.md](./references/worked-plan-examples.md) - one worked B2B plan, one worked B2C variant, one broken plan with diagnosis. Load when producing the deliverable.
- [./references/platform-capability-matrix.md](./references/platform-capability-matrix.md) - per-network objectives, permission tokens, format eligibility, CTA rights. Load when mapping the plan onto concrete networks.
- [./references/published-benchmarks.md](./references/published-benchmarks.md) - every performance number with its source, and how to judge one before using it. Load before quoting any benchmark to the user.
