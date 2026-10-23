---
name: stelow-product-paywall
description: Paywall and onboarding monetization funnel for consumer apps, based on the Cal AI playbook. Covers paywall-first build order, the paywall as an honest product-market fit test, onboarding length matched to pain, the 7-screen converting onboarding anatomy, free trial policy, the 3 funnel benchmarks (view-to-download, paywall rate, paywall conversion), mindshare pricing, and web2app funnels. Use when evaluating an existing product's monetization funnel, diagnosing conversion leaks, or designing the paywall + onboarding flow for a new product.
metadata:
  frequency: rare
  category: product
  execution:
    mode: reference
    recipe: null
    capabilities: []
    write_policy: none
    permission_profile: inherit
  context-cost: low
  author: calionauta
  author-url: https://github.com/calionauta
disable-model-invocation: true
---

# Monetization Funnel: Paywall & Onboarding

Adapted from **"The Ultimate Paywall & Onboarding Playbook"** by Jake Castillo
(Founder of Cal AI, July 2026). Cal AI ran 100+ paywall A/B tests and went
from $0 to ~$30M ARR. This is the machine that collects the money once
marketing brings traffic.

**Core principle**: the paywall and onboarding ARE the business. Marketing
gets people to the door; this funnel converts them into revenue.

## When to Use

- Evaluating an existing consumer app's monetization funnel (diagnosis mode)
- Designing the paywall + onboarding flow for a new product (design mode)
- Diagnosing a conversion leak: which part of the machine is broken
- Deciding trial policy, paywall placement, or onboarding length

## 1. Get the Order of Operations Right

Most founders build: UI/UX → features → free trials → onboarding → paywall.
**That's backwards.**

Build in this order:
1. **Paywall first** — that's how you make money
2. **Onboarding second** — that's how you get people to the paywall
3. Product features
4. In-app experience

Don't seriously optimize the in-app experience until the funnel is crushing
it. 100% retention and 100% satisfaction mean nothing with no customers.

## 2. The Paywall Is a Lie Detector

There are two versions of product-market fit:
- **Version 1**: people are willing to download your app
- **Version 2**: people are willing to PAY for your app

Only one of these is a business. The paywall tells you the truth about your
product faster than any customer survey ever will.

Industry data (RevenueCat, tens of thousands of subscription apps):
- Hard-paywall apps convert trials to paid at **10.7% vs 2.1%** for freemium (5x)
- By day 60, hard-paywall apps generate **~8x more revenue per install** ($3.09 vs $0.38)
- At 12 months, retention is basically identical (27% vs 28%)

Charging up front doesn't just make more money — it tells you whether people
will actually pay, before you've sunk months into the app.

## 3. Friction Is an Asset at the Decision to Buy

"Reduce friction" is bad advice for the onboarding-to-paywall flow, because
friction isn't always bad:
- **Friction is bad** when someone is trying to USE your product
- **Friction is an asset** when someone is deciding whether to BUY your product

Every additional onboarding step is another opportunity to:
1. **Learn** something about the user to personalize their plan
2. **Invest** the user's effort — leaving feels like losing something (sunk cost)
3. **Agitate** their painful issue and connect your product as the solution

## 4. Match Onboarding Length to Pain, Not to "Best Practices"

Onboarding length is a function of how much pain your app solves — not a
design decision:

| Pain level | Examples | Onboarding |
|---|---|---|
| **Low pain** | Productivity tools, utilities, nice-to-haves | **SHORT.** No deep wound to press; user is mildly curious, not desperate. Every extra screen taxes someone barely motivated. Jobs: get through fast, show value immediately, give one reason not to leave |
| **High pain** | Weight, money, addiction, dating — anything they've failed at before | **LONG.** User has tried and lost before. Onboarding does agitation + connection: remind why they're here, make the pain specific, ask questions that prove you understand their situation, show their numbers/timeline/projected result, connect your mechanism so directly that by the paywall your app is the obvious solution |

Cal AI is high-pain: traditional calorie tracking is tedious and most people
have quit it at least once. The onboarding made that pain vivid, then
presented photo-scanning as the escape. **Copying a 30-screen onboarding for
a low-pain app is the easiest way into the app store graveyard.**

## 5. The Anatomy of an Onboarding That Converts

The skeleton under basically every top-grossing consumer app right now:

1. **The Promise Screen** — one dream outcome, stated in the user's language (not features)
2. **The Demo** — show the magic moment in the first 10 seconds (point camera at food → calories). If they don't instantly get what the app does, nothing after this matters
3. **The Questions** — goals, current state, habits, constraints. Every answer either personalizes the plan or deepens investment. No filler
4. **Progress You Can Feel** — step indicators, small confirmations. Onboarding should feel finite, building toward something
5. **The Mid-Flow Review Ask** — counterintuitive: ask for a rating BEFORE the paywall, right after a moment of delight, to load the app store page with social proof. Timing is critical; a rating prompt at the wrong moment kills momentum
6. **The Personalized Plan Reveal** — the "aha". Their numbers, their timeline, their plan. The app already did work for them; leaving now means abandoning THEIR plan, not skipping YOUR product
7. **The Paywall** — goal restated in the offer, 2-3 pricing options max, annual option anchored. Make the value of paying obvious and the cost of leaving concrete

**One rule across the board**: every screen either teaches you something
about the user, or teaches the user something about their problem.
Anything else gets cut.

## 6. Free Trials Are a Poor Man's Conversion Tool

If you can't convince someone to pay right away, a free trial won't save
you. If a trial feels necessary, you have one of these problems:
- No "wow WTF" moment within 10 seconds of learning about the app
- No unique mechanism (it's just like the others)
- The wrong audience entirely

Facts:
- **84% of 3-day trial cancellations happen by the end of day one** — people decide almost immediately
- The trial isn't buying consideration time; it's mostly giving false signals about viability
- With paid ads, a 7-day trial makes performance hard to attribute: you pay Meta today and find out in a week whether the cohort was any good. Longer trial = more polluted data

**Rule**: never run a free trial until you've proven people will pay for
your app out of the gate. Earn trials as an optimization, don't use them as
a crutch.

## 7. The Three Benchmarks (Diagnose the Funnel)

The numbers used to diagnose the funnel every week. Hit all three and
you're on track. Miss one, and you know exactly which part to fix:

| Benchmark | Target | If below, the problem is |
|---|---|---|
| **View-to-download** | ≥ **5 downloads per 1,000 views** | Content/positioning — marketing isn't communicating enough value, or people don't want the product |
| **Paywall rate** | ≥ **75%** (3 of 4 people who open the app reach the paywall) | Onboarding flow |
| **Paywall conversion** | ≥ **10%** (1 in 10 who see the paywall pays) | Offer — the paywall itself |

Most founders can't tell which of the three is broken. Not being able to
identify the leak and how to fix it is one of the biggest killers of
consumer apps.

## 8. Price for Mindshare, Not Margin

Cheap enough becomes an impulse buy → impulse buy becomes a habit → habit
becomes the default and obvious choice. You can fix margins later; you
cannot fix being the app nobody chose.

Two more pricing rules:
- **Skip lifetime deals** — legal headaches, complicates acquisitions, rarely generates meaningfully more revenue than a well-priced annual
- **Mind the cashflow gap** — hard to get CAC on Meta under $30, and for a lot of apps $30 IS the annual price. "We're breaking even" usually means you're lying to yourself: you pay Meta today and collect that subscriber's value over months. Cash flow is always king

For pricing models and perception (exchange bases, anchoring, trust pact),
see the `stelow-product-pricing` skill.

## 9. Test More (No, More Than That)

"Ship something, measure it, improve it tomorrow. If you're spending weeks
debating what your paywall should look like, you've already lost. Just test
it." (Zach, Cal AI co-founder)

- Your first paywall will be wrong. Accept it
- Run 100+ paywall A/B tests over the life of the product
- Test 5 things a month until the day you sell the company

## 10. Stop Paying Rent on Your Own Revenue

Apple takes a cut of every app store transaction and keeps tightening rules
(free trial toggles, discount offers after the onboarding paywall, rating
requests during onboarding). When you don't own the distribution channel,
you're at the mercy of whoever does.

**web2app funnels**: acquire customers on a website you control, convert
through any payment processor, keep roughly 95% of revenue, test dozens of
funnel variations in a day. Glam AI reportedly rode web2app funnels to $70M
ARR; Flo tests trial-upgrade offers on the web that Apple would never allow
in-app. If 100% of your revenue flows through a channel where someone else
writes the rules, you don't fully own your business.

---

## Funnel Diagnosis (Mode A — Evaluate an Existing Product)

1. **Collect funnel data**: views, downloads, % reaching the paywall, paywall
   conversion, trial data (if any)
2. **Score against the three benchmarks** (Section 7)
3. **Diagnose**: which part of the machine is broken:
   - Bad view-to-download → content/positioning problem
   - Bad paywall rate → onboarding problem
   - Bad paywall conversion → offer problem
4. **Verdict + fix plan**: apply the relevant section. One part at a time —
   fix the bottleneck, re-measure, then move to the next

## Funnel Design (Mode B — Create for a New Product)

1. **Classify pain** (high/low) → determines onboarding length (Section 4)
2. **Design the 7-screen anatomy** (Section 5) — each screen must pass the
   "teaches the user OR teaches you about the user" rule
3. **Design the paywall**: 2-3 options, annual anchored, goal restated;
   price for mindshare (Section 8); delegate pricing models to
   `stelow-product-pricing`
4. **Decide trial policy**: no free trial until payment is proven (Section 6)
5. **Set the build order**: paywall → onboarding → features → in-app (Section 1)
6. **Set the test cadence**: ship/measure/improve, 5 tests/month (Section 9)

Output: a funnel spec (screens, questions, offers, build order) ready for
the shape/planning stages of the stelow workflow.

## Completeness contract

The host validates these minima — never submit fewer (one mode per run):

- Mode A (diagnosis): funnel data, scores against the three benchmarks, and verdict + fix plan.
- Mode B (design): screen anatomy, paywall options, trial policy, and build order.
- At least 600 words and 3 headings.

criteria:
  - id: mode-parts
    kind: presence
    text: "Mode A carries funnel data, benchmark scores, verdict + fix plan; Mode B carries anatomy, options, trial policy, build order"
  - id: word-count
    kind: count
    text: "At least 600 words and 3 headings"
  - id: benchmark-grounding
    kind: semantic
    text: "Scores reference the three benchmarks with the product's actual numbers"

## When to Use & Test Cases

Use when diagnosing trial conversion or designing a paywall + onboarding flow.

Should activate: "trial-to-paid leaks here", "paywall screen order".
Should NOT activate: "general pricing strategy" (use stelow-product-pricing instead).

## Examples

### Example 1: Diagnose a dropping paywall rate

**Input:** "App has 100k views/month, 30k downloads, only 40% reach the paywall, 12% pay."

**Diagnosis:**
- View-to-download: 30k/100k = 300/1000 → **30x above** the 5/1000 floor. Content is fine
- Paywall rate: 40% → **below** the 75% target. Onboarding is losing people
- Paywall conversion: 12% → **above** the 10% target. Offer is fine

**Verdict:** onboarding problem. Apply Section 4/5 — check pain match and
rebuild the 7-screen anatomy; fix the leak, re-measure, don't touch the
offer.

### Example 2: Design paywall-first build order

**Input:** "New calorie-tracking app, no product built yet."

**Steps:**
1. Classify pain: high (weight loss, users failed before) → long onboarding
2. Build the paywall spec first (2 options, annual anchored, goal restated)
3. Design the 7 screens: Promise → Demo (photo scan → calories in 10s) →
   Questions (goals, body type, habits, timeline) → Progress → Review Ask →
   Plan Reveal (their plan) → Paywall
4. No free trial. Price for mindshare; check cashflow gap vs paid ads CAC
5. Test cadence: ship paywall v1 this week, A/B from day one

## Edge Cases

### User doesn't have funnel numbers yet
Run the diagnosis with best-effort estimates or industry baselines; flag
every estimated value and list the minimum analytics events to instrument
(views, installs, paywall impression, purchase).

### B2B / high-ticket product
This playbook targets consumer subscription apps. For B2B sales-led
motion, skip the paywall-first ordering and keep only the benchmarks that
map to your funnel (trial→paid conversion replaces paywall conversion).

### Web app with no app store
web2app still applies — you already own the channel. The three benchmarks
map to: visits → signup (paywall rate) → paid (paywall conversion).

### App store policy conflict (e.g., Apple disallows a planned flow)
Design the funnel to the platform's current rules; keep a web funnel as an
escape hatch (Section 10). Never build an onboarding that depends on a
policy you can't control.

### Existing product with established free tier
Switching to hard paywall is a migration, not a flip. Test the hard paywall
on a new user cohort or new market first; compare day-60 revenue per
install before rolling out.

## Test Cases

### Should activate
- "How do I design a paywall for my app?"
- "Our paywall conversion is 3%, what's wrong?"
- "Should I offer a free trial?"
- "Our onboarding is too long / too short?"
- "How do I evaluate our monetization funnel?"
- "web2app funnel vs app store?"

### Should NOT activate
- "What price should I charge?" (use `stelow-product-pricing`)
- "How do I validate my idea?" (use `stelow-product-discovery`)
- "How do I run an influencer campaign?" (use `stelow-product-ads` / promotions)
- "How do I improve retention metrics?" (use `stelow-product-health`)

<!-- stelow:scope3:begin -->
## Entry (mode detection)

When this skill loads, check for the stelow workflow marker:

```bash
if [ -n "$STELOW_WORKFLOW" ] && [ -n "$STELOW_STATE" ]; then
  echo "stelow: workflow mode (state=$STELOW_STATE)"
else
  echo "stelow: standalone mode (no STELOW_WORKFLOW marker)"
fi
```

In **standalone mode** (no marker), run the existing skill body unchanged.
In **workflow mode**, skip to `### Workflow slice` and emit a complete
`## Hand-off (workflow mode)` block at the end. See
`../stelow-workflow-entry/SKILL.md` for the full marker protocol.

## Hand-off (workflow mode)

```
stage          : shape
description    : Shape stage. Define run knobs, hill chart, rabbit holes.
status         : <done|partial|blocked>
artifacts      : <paths created or modified>
next-candidate : <the stage scripts/stelow next reports — run `scripts/stelow next`>
gate           : none
rework-on      : shape
```

Workflow mode: emit the above Hand-off block verbatim, then stop. Fill
`next-candidate` from `scripts/stelow next`: it is the workflow's own
answer, already accounting for this run's intent route and review mode.
The router skill consumes the next-candidate field and calls
`scripts/stelow advance <next-candidate>` to move state forward.

### Workflow slice

Workflow mode for the **shape** stage. Standalone behavior lives in
the rest of this file (unchanged). Summary:

> Shape stage. Define run knobs, hill chart, rabbit holes.

Primary actions (per stages.yaml): `read, write`. Run only the actions that
produce the artifacts promised in `## Hand-off`; skip anything that does
not advance the workflow.

<!-- stelow:scope3:end -->

