---
name: revenuecat-app-valuation
description:
  Use this skill when the user asks how much their app is worth, what they could sell their app for,
  how app valuations or acquisitions work, or how to prepare a subscription app for sale/exit.
---

# App valuation and selling

Help a founder understand what their app might be worth and how app acquisitions work. The
frameworks below come from RevenueCat's guidance on selling apps, extended with how buyers
reason about risk. Ground every estimate in the user's own RevenueCat data where you can, rather
than quoting the ranges in the abstract.

Two rules hold for this topic:

- Always present valuation as a range with a confidence level, never a single guaranteed number.
  An app is ultimately worth what a buyer will pay, and there is no guarantee a buyer exists at
  any given price.
- Treat this as general education, not financial, legal, or tax advice. For an appraisal, tax
  treatment, or deal terms, tell the user to consult a broker, attorney, or tax professional.

## The method

A valuation is four decisions, in order. Work through them explicitly.

1. Choose the profit base, and name it.
2. Choose the band that base earns.
3. Position the app within that band on the evidence.
4. State the range, the confidence, and what would move it.

## 1. Choose the profit base

Apps are valued as a multiple of profit, not revenue. Every multiple in this skill is a profit
multiple. Do not apply multiples directly to revenue metrics.

| Base                     | Multiple                              |
| ------------------------ | ------------------------------------- |
| Monthly operating profit | 12x–36x (broad), 36x–60x (mature sub) |
| Annual operating profit  | 1x–3x (broad), 3x–5x (mature sub)     |

MRR and ARR still matter — they are the top line the profit is computed from, and the input to
the retention, growth, and concentration checks below. They are not a valuation base.

When the user knows revenue but not costs, ask for costs. If they cannot give them, state the
assumed margin as an explicit assumption and show the arithmetic in full — "$200k ARR × 60%
assumed margin = $120k profit × 3–5x = $360k–$600k" — so the user can correct the assumption.

### Owner earnings or post-hire profit

There are two defensible profit bases, and they are not interchangeable. Pick one, name it in the
answer, and apply the matching multiple.

- Owner earnings — what a solo buyer who does the work themselves would take home. Proceeds minus
  cash operating costs, plus one-off and non-recurring costs added back. Use for owner-operated
  apps sold to individual buyers.
- Post-hire operating profit — what the app earns after paying market rate for the work the
  founder does for free today. Owner earnings minus the cost of replacing that work. Use when
  the buyer is a studio or portfolio acquirer who will staff the app. Default to this.

The published 3x–5x band is a post-hire number: the acquirers quoting it are portfolio buyers who
carry the operating cost.

To size replacement cost, ask how many hours a week go into the app across engineering, support,
marketing, and admin; who is paid today and how much; and whether the founder intends to stay
through a transition. A part-time maintenance load is a few thousand dollars a month of
replacement cost; a full-time founder doing engineering and user acquisition is a salary. Present
it as a stated assumption, not a derived fact.

### Computing the number

Start from proceeds — revenue net of sales tax/VAT and store commissions — rather than gross
revenue, since App Store / Play Store fees are already removed. Request proceeds from
`get-chart-data` on the `revenue` chart with the `revenue_type` selector set to `proceeds` (see
`revenuecat-charts`). Then subtract the expenses that directly keep the app running: operational
costs (servers, customer support, licensing), marketing and user-acquisition spend, and ongoing
maintenance. Apply the add-backs above.

- Do not subtract interest or corporate income tax — those reflect the seller's financing and tax
  situation, which the buyer replaces with their own. The "taxes" already removed in proceeds is
  sales tax/VAT; don't subtract income tax on top.
- Development costs for building _new_ features are usually excluded — they fund future profit,
  not the maintenance of existing profit. Every app differs, so note when some development cost
  belongs in the number.
- Use trailing-twelve-month (TTM) figures as the base.

Then compute the last two full quarters annualized as a run-rate sensitivity. When it differs
from the trailing-twelve-month base by more than about 20%, present both:

> On trailing-twelve-month profit of $100k, the range is $300k–$500k. At the current run rate of
> $140k, the same multiples give $420k–$700k. Buyers will anchor closer to the trailing figure
> and ask you to prove the run rate holds — sustained growth is the argument for the top of the
> range, not for a bigger base.

This applies in both directions: for a declining app, the run-rate number is the floor a buyer
will push toward and the trailing figure is what the seller defends. Show the gap either way. A
run-rate sensitivity is not license to annualize a spike — two or more quarters of consistent
movement is a trend, one strong month behind a launch or a seasonal peak is not. Check chart
`annotations` before calling something a trend.

## 2. Choose the band

RevenueCat publishes two ranges, and they are not the same range — they describe different tiers
of app:

- Broad-market heuristic: apps typically sell for 12x–36x monthly operating profit (≈ 1x–3x
  annual). This spans the whole market, including younger or higher-churn apps. Some sell for
  many multiples more, and some do not sell at all.
- Mature-subscription floor: for a proven, low-risk subscription business, disciplined buyers
  anchor at 3x–5x annual operating profit (≈ 36x–60x monthly). Worked example: an app earning
  $100k annual operating profit at 3–5x is worth roughly $300k–$500k.

These bands sit end-to-end, meeting only at 3x annual / 36x monthly. Do not average the two or
claim a single number reconciles them.

### The mature-subscription band needs evidence, not age

Qualification is about whether a full renewal cycle is observable, which is usually visible well
before an app's second birthday. Check all three:

- Subscription-dominant revenue — roughly 70%+ of proceeds from subscriptions.
- A completed renewal cycle for the dominant plan duration. Read `subscription_retention` or
  `cohort_explorer`: an annual-dominant app needs cohorts observed past month 12, so the first
  renewal is in the data. A monthly-dominant app needs cohorts observed well past the first-month
  churn cliff — several renewal periods, not one. Check the annual-vs-monthly mix by revenue
  first, since it decides which threshold applies. An 18-month-old annual-dominant app with
  complete month-12 cohorts qualifies; a three-year-old app that just launched annual plans does
  not.
- A curve that has flattened. Retention should decay and then level off across at least two
  consecutive cohorts. A curve still falling steeply at the last observed period is incomplete
  evidence however long the history is.

Fail any check and the broad-market band applies. Say which check failed and what would clear it
— usually a specific number of months.

Past the gate, age is not a factor: the multiple is set by what the cohorts show.

### Apps that are not subscription-dominant

RevenueCat currently has no published or recommended valuation insights for apps that are not
predominantly subscription apps. When the app you are asked about is not predominantly
subscription based, do not offer a valuation.

## 3. Position within the band

The band is the starting point; these factors set where in it the app lands. Score each factor
strong, neutral, or weak, and say which evidence drove each call.

| Factor                | Strong                                                       | Weak                                              | Where to look                                              |
| --------------------- | ------------------------------------------------------------ | ------------------------------------------------- | ---------------------------------------------------------- |
| Retention (2x weight) | Churn/retention in the top 30% of category peers, flat curve | Bottom 30%, or a still-falling curve              | `get-benchmarks` (monthly churn), `subscription_retention` |
| Trajectory            | Growing 25%+ YoY, sustained two or more quarters             | Declining 10%+ YoY                                | `revenue` (proceeds), trailing twelve vs prior twelve      |
| Monetization          | Realized LTV, trial and paying conversion in the top 30%     | Bottom 30%, or no pricing headroom left           | `get-benchmarks`, `conversion_to_paying`                   |
| Distribution          | Compounding channels, healthy paid payback                   | Borrowed growth, or paid that does not pay back   | Ask the user                                               |
| Concentration         | Diversified across store, geography and SKU                  | A single dependency past the thresholds below     | `revenue` segmented by `store`, `country`, `product_id`    |
| Transferability       | Low ops burden, documented, transferable store account       | Founder-dependent, undocumented, transfer-blocked | Ask the user                                               |

Use `get-benchmarks`' `percentile_bucket` directly: 70+ is strong, 30–70 neutral, under 30 weak.
It already accounts for reverse metrics, so a high percentile on churn means low churn. Rows with
`is_eligible_for_benchmarking: false` are low-confidence — score them neutral and say so.

Then position:

- Net two or more strong, no weak — top third of the band.
- Roughly balanced — middle third.
- Net two or more weak — bottom third.

Additional factors that cap what a buyer is willing to pay: declining revenue, issues that might
prevent transfer of the app, undocumented financials, concentration (see below). Mention any
that apply.

Show the scorecard, not just the conclusion. "Top-quartile retention and 30% year-over-year
growth, but 90% of revenue from one country" is the answer; the number summarizes it.

### Reading the factors

- Retention / subscriber stickiness — the strongest signal of product-market fit and future cash
  flow, and the biggest lever on the multiple, which is why it carries double weight. What counts
  as "good" is category-dependent: buyers cited healthy annual-subscription retention anywhere
  from ~25% to ~70%. Benchmark against the app's category rather than a universal number, and be
  ready to explain early churn (roughly 30% of subscriptions cancel in the first month) and show
  that later cohorts stabilize.
- Monetization headroom — under-monetization is a plus to buyers: proven monetization with clear
  room to grow (pricing, offers, plan mix).
- Distribution durability — treat acquisition channels as a quality tier, not a preference:
  - Compounding (strongest): organic ASO, SEO, brand, and word of mouth.
  - Rentable: paid user acquisition. Check payback period, not just volume.
  - Borrowed (weakest): UGC, viral loops, influencer-driven and algorithm-driven growth, a
    single creator, a store feature. Discount it heavily, and ask what happens to installs if it
    stops tomorrow.

  Buyers do differ on the organic/paid balance (cited preferences run from 100% organic through
  50/50 to 75/25 paid/organic), so a defensible mix beats a dogmatic one.

- Concentration — check the top segment's share of proceeds by `store`, `country` and
  `product_id` over the trailing twelve months:
  - Platform/store. Being iOS-only is common and only a mild discount on its own.
  - Geography. One country above ~70% of revenue is a real cap.
  - SKU / product. One product above ~70% of revenue means the business rests on one price point.
  - Beyond the charts: a single traffic source, a single integration, and — for B2B-shaped apps
    — a handful of accounts carrying revenue.

- Technical infrastructure — clean architecture, low operating burden, and good documentation
  reduce perceived risk and are most of the transferability score.

### Outside the scorecard

These change the deal rather than the app's position in its band. Raise them, but do not bake
them into the range:

- Strategic / portfolio fit — the best price often comes from the buyer who sees the most
  synergy.
- Founder involvement — most buyers view the founder staying through a transition as a positive.
  Large studios with in-house teams are the exception.
- Deal structure — offers come as cash (most common), equity, or earnouts. Roughly two-thirds of
  offers are pure cash. Cash deals often pay ~50% at close and the remainder over the following
  6–12 months.

## 4. State the range and the confidence

Present the result as: named profit base × low-end multiple to × high-end multiple, the position
within the band and why, then a confidence level.

Confidence is low with thin or lumpy data, when the factors conflict, when several inputs are
user-supplied and unverifiable, or when a large share of revenue is non-recurring. It is higher
with 12+ clean months, low churn, a completed renewal cycle, and diversified revenue. A wide,
honest range beats a tight one you cannot defend.

## Grounding an estimate in the user's RevenueCat data

When the user wants an estimate for their own app, pull their real metrics first.

- Use `revenuecat-charts` to fetch what the steps above need. Prioritize: proceeds (trailing
  twelve months and by quarter), subscription retention by cohort, monthly churn, trial and
  paying conversion, ARPU, annual-vs-monthly plan mix, realized LTV, and proceeds segmented by
  store, country and product.
- Compare against category benchmarks via `get-benchmarks` (realized LTV, trial conversion,
  initial conversion, conversion to paying, monthly churn, refund rate). Read the percentiles
  into the scorecard as described in step 3.
- RevenueCat has no acquisition-cost data, so it cannot compute CAC, LTV/CAC, or payback period
  on its own. Do not present a CAC-based number without user-supplied acquisition data.
- Link the user to the relevant charts with `revenuecat-charts` (e.g. MRR, churn, subscription
  retention) so they can see the inputs behind the estimate.

Several inputs are not in RevenueCat at all. Ask for them together, once, rather than one at a
time:

| Input                                           | Needed for                     |
| ----------------------------------------------- | ------------------------------ |
| Operating costs (servers, support, tooling, UA) | The profit base                |
| Founder and team hours, and who is paid         | Add-backs and replacement cost |
| Ad revenue, by network                          | Valuing non-recurring streams  |
| Channel split, UA spend, payback period         | Distribution durability        |
| Ops burden, documentation, transferability      | Transferability, and hard caps |

## Preparing to sell, finding buyers, negotiating

If the user is moving toward an actual sale, summarize the relevant parts and point them to the
full posts for detail:

- Can they even sell it? Most App Store apps can be transferred between developer accounts; a
  few cannot (e.g. conflicting in-app-purchase product IDs, some sandboxed Mac apps, Apple Arcade
  apps), in which case the whole developer account transfers instead. Direct them to Apple's
  app-transfer criteria to confirm.
- Prep before talking to buyers: clean, reconciled financials, a clear retention/growth story,
  tidy metrics, low-friction product and infrastructure, and handover documentation.
- Finding buyers: marketplaces and brokers (e.g. Flippa, AppFlip, App Business Brokers) and
  direct acquirers exist; warm intros generally outperform cold outreach.
- Negotiating: the first offer often lowballs. Recommend independent legal/financial advice for
  the actual transaction.

## Citing sources

Base answers on RevenueCat's own material and cite it. The two primary posts are:

- "How to sell your mobile app" — https://www.revenuecat.com/blog/growth/how-to-sell-an-app/
- "What app buyers really want: insights from 10 leading acquirers" —
  https://www.revenuecat.com/blog/growth/guide-to-selling-apps/

Attribute the two published bands, the retention ranges, the channel-preference splits, and the
deal-structure figures to those posts. The factor scorecard, the concentration thresholds, the
add-back treatment, and the handling of non-recurring revenue are general market practice rather
than RevenueCat findings — present them as how a buyer reasons, and do not cite a RevenueCat post
for them.

For deeper or more current detail, fetch those posts or search the RevenueCat blog (selling and
acquisition content) and the State of Subscription Apps report. To benchmark the user's app
against its peers, use `get-benchmarks`.
