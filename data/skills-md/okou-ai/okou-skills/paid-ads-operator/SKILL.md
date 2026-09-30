---
name: paid-ads-operator
description: Launch, audit, monitor, or optimize paid advertising campaigns, tracking, budgets, CAC, CPA, and ROAS.
---

# Paid Ads Operator

Use this skill to run paid acquisition with a media buyer's operating discipline: tracking first, controlled launches, clean traffic, clear experiments, and business-metric reporting.

For platform API operations, combine this skill with the relevant connector skill, such as `google-ads`, `meta-ads`, `posthog`, `plausible`, `stripe`, or CRM/warehouse skills.

## Operating Principles

1. **Track before scaling.** Do not optimize paid spend until the conversion event, attribution path, and revenue/quality signal are visible outside the ad platform.
2. **Start paused or low-risk.** Create campaigns, ad groups, ad sets, ads, and keywords in `PAUSED` or draft state first. Enable only after the user explicitly confirms.
3. **Preserve budget intent.** Clarify whether a budget is an average daily budget, a lifetime cap, or a hard maximum. Google Ads daily budgets are averages and may spend above the daily amount on individual days.
4. **Optimize for business outcomes.** Treat clicks, CTR, and CPC as diagnostic metrics. Decisions should ultimately ladder to qualified leads, paid conversions, CAC, ROAS, LTV, or payback.
5. **Force signal, not churn.** Prefer clear hypotheses and meaningfully different tests over tiny daily tweaks to bids, budgets, and copy.
6. **Control policy risk.** For competitor campaigns, avoid using competitor trademarks in ad copy unless the user confirms legal/policy review. Bidding on competitor keywords can carry jurisdiction-specific risk.

## Launch Checklist

Before enabling spend, confirm:

- Objective: purchase, subscription, qualified lead, signup, app install, booked demo, or another measurable outcome.
- Primary conversion event: exact platform event/action name and where it fires.
- Attribution path: UTM parameters, click IDs, first-touch/last-touch behavior, CRM or payment metadata, and cross-domain redirects.
- Budget constraints: daily average, hard cap, test budget, end date, and acceptable loss during learning.
- Unit economics: target CPA/CAC, gross margin, LTV, payback target, trial-to-paid expectations, and minimum conversion quality.
- Audience and geo: countries, languages, excluded locations, demographics, customer segments, and existing remarketing audiences.
- Landing page: message match, load speed, offer clarity, CTA path, payment/signup flow, and analytics coverage.
- Naming and URLs: campaign/ad group/ad names, final URLs, `utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, and `utm_term`.
- Risk controls: negative keyword seed list, brand/trademark rules, excluded placements, spend alerts, and rollback criteria.

## Campaign Structure

### Paid Search

Structure around intent, not one broad bucket:

- Brand: own branded terms and close variants.
- Non-brand high intent: exact and phrase keywords tied to the product category.
- Competitor alternative: competitor and "alternative to" queries, with conservative copy.
- Problem/solution: use only when the landing page directly answers the query.
- Retargeting/search remarketing: if audience size and platform support make it useful.

Start with exact and phrase match for high-intent launches. Add broad match only after conversion tracking is reliable and there is enough conversion volume for automated bidding.

Include negative seeds for:

- Jobs, salaries, definitions, tutorials, free templates, academic/research terms, unrelated meanings, support queries, and low-intent software categories.
- Competitor legal risk terms if the user does not want competitor conquesting.
- Search terms discovered after launch that do not match buying intent.

### Paid Social

Structure around creative and audience signal:

- Prospecting: broad or lightly constrained audiences when pixel/conversion data is healthy.
- Retargeting: site visitors, product viewers, engaged users, abandoned checkout, or CRM lists.
- Creative concepts: each concept should test a distinct hook, problem, proof point, or offer.
- Funnel stage: awareness, consideration, conversion, and lifecycle should not share the same success metric.

On Meta/TikTok-style platforms, creative quality and volume often matter more than micro-targeting. Keep audience changes simple enough that creative signal remains interpretable.

## Daily Operating Loop

Use the ad account timezone when reporting "today."

1. **Serving and approval:** campaign status, ad/ad group status, policy review, disapprovals, limited eligibility, learning status.
2. **Pacing:** spend vs. budget, hourly/daily pace, remaining budget, abnormal spikes, account-level caps.
3. **Traffic quality:** search terms, placements, audience breakdowns, geo/device splits, invalid or irrelevant queries.
4. **Front-end metrics:** impressions, CTR, CPC, CPM, click volume, top impression share, frequency, creative fatigue.
5. **Conversion path:** landing page sessions, signup/checkout events, conversion tracking health, attribution metadata.
6. **Business quality:** paid conversions, trial quality, revenue, CAC, ROAS, LTV/payback, lead quality, refund/churn signals.
7. **Actions:** negatives, keyword promotion, creative refresh, landing-page fixes, bid/budget changes, and documented next checks.

Do not overreact to tiny samples. As rough guardrails:

- Fewer than 100 impressions: usually only check approval and obvious targeting mistakes.
- 100-500 impressions: inspect search terms, CTR direction, and early irrelevant traffic.
- 500+ impressions with weak CTR: test copy, query intent, bid position, and ad relevance.
- Meaningful conversion decisions require enough clicks and conversion volume to avoid noise.

## Diagnostic Playbooks

### Impressions but no clicks

Check:

- Search terms or audience intent do not match the offer.
- Ads are approved but showing in low positions or weak placements.
- Headlines do not mirror the user's query or urgency.
- Brand is unknown and the offer is not clear enough.
- There are too few impressions to judge.

Likely actions:

- Add negatives or placement exclusions.
- Split mismatched keywords into tighter ad groups.
- Rewrite headlines around the exact query intent.
- Check top impression share, CPC pressure, and Quality Score/ad relevance where available.

### Clicks but no conversions

Check:

- Conversion tracking is broken or firing on the wrong event.
- Landing page promise does not match ad copy or keyword.
- CTA path is too long, confusing, slow, or blocked by auth/payment.
- Offer is weak for cold traffic.
- Traffic is low-intent despite acceptable CTR.

Likely actions:

- Verify tracking with a real test path before changing bids.
- Compare ad clicks to analytics sessions and funnel events.
- Review landing page copy, speed, CTA, trust points, and checkout/signup friction.
- Separate exploratory traffic from high-intent traffic.

### Spend but poor conversion quality

Check:

- The ad platform is optimizing to a shallow event.
- Conversions are low-quality leads, accidental signups, or non-paying trials.
- Attribution stores click source but not revenue or lifecycle quality.
- Automated bidding is using insufficient or polluted conversion data.

Likely actions:

- Optimize to a deeper event when enough volume exists.
- Feed qualified conversion or revenue signals back to the platform where possible.
- Segment reports by campaign, ad group, keyword/search term, creative, geo, device, and landing page.

### No impressions

Check:

- Ads are under review, disapproved, limited, or paused.
- Budget, bid cap, audience, or keyword volume is too restrictive.
- Location/language/date schedule excludes the current user base.
- Campaign is learning, newly created, or waiting for asset approval.

Likely actions:

- Confirm statuses and policy summaries first.
- Validate targeting and eligible inventory.
- Increase bid/budget only after ruling out setup mistakes.

## Search Term Workflow

For search campaigns:

1. Pull search terms by campaign/ad group for the current day and last 7 days.
2. Classify each term as high intent, adjacent, low intent, irrelevant, or risky.
3. Add irrelevant/risky terms as campaign-level negatives when they should be blocked everywhere.
4. Add ad group-level negatives when the term belongs elsewhere but not in the current ad group.
5. Promote repeated high-intent terms into exact keywords with matching copy.
6. Keep a written change log: term, action, scope, reason, and expected impact.

Prefer phrase negatives for concepts like "free", "jobs", or unrelated product categories. Use exact negatives when the phrase may also appear in useful long-tail queries.

## Creative Testing Workflow

For each test, write:

- Hypothesis: what user belief or objection the creative addresses.
- Audience/query: who should see it and why.
- Control: current winning or baseline ad.
- Variant: one materially different hook, proof point, format, or offer.
- Primary metric: CTR for attention, CVR/CPA for conversion, ROAS/CAC for business impact.
- Minimum read: impressions/clicks/conversions required before judging.
- Decision rule: scale, iterate, pause, or keep learning.

Good creative tests are meaningfully different:

- Prompt-to-outcome vs. speed vs. quality vs. integrations.
- Founder/product demo vs. customer proof vs. comparison vs. problem agitation.
- Technical buyer promise vs. executive buyer promise.

## Budget and Bidding

- Keep early tests small enough to survive learning mistakes but large enough to generate signal.
- Document whether the user's cap is a hard cap or platform average.
- On Google Ads, average daily budget can overspend on a single day. If the user asks for a daily maximum, set the average lower to account for platform overdelivery.
- Avoid switching bidding strategies repeatedly during learning.
- Use click-maximizing or manual controls only when conversion data is absent or untrusted.
- Move toward conversion-based bidding only when the conversion event is reliable and has enough volume.

## Reporting Format

Lead with the current decision state:

- Running normally, learning, limited, under review, wasting spend, tracking broken, or ready to scale.

Then report:

- Spend, impressions, clicks, CTR, CPC/CPM, conversions, CPA/CAC, revenue/ROAS when available.
- Best and worst segments: campaign, ad group/ad set, keyword/search term, creative, geo, device, landing page.
- Actions taken since the last report.
- Recommended next action, with reason and expected effect.
- Open risks: tracking gaps, low sample size, policy review, budget pacing, or conversion lag.

When there is no spend yet, say that directly and focus on approval, eligibility, and setup status.

## Safety and Confirmation

- Never enable paused campaigns, increase budgets, widen targeting, remove negatives, or change live bidding without explicit user confirmation.
- Never trigger fake purchases or fake qualified conversions unless the user explicitly accepts data pollution and the test environment is isolated.
- Do not paste access tokens, bearer tokens, cookies, or customer PII into reports.
- Treat platform-reported conversions as delayed and directional until verified against the source of truth.
- If legal, medical, financial, employment, housing, credit, or other regulated targeting could apply, check special category rules before launching.
