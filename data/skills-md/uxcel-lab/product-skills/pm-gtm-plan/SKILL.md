---
name: pm-gtm-plan
description: "Build a go-to-market plan that's a stage-appropriate system — customers, channels, pricing, timing, and partnerships that fit the company's maturity — not a generic launch checklist. Gates on GTM readiness (validated demand) and company stage, picks the right channel and entry timing, and treats the buyer journey as non-linear. Catches the defaults Claude misses: GTM-as-one-time-launch, stage-skipping, channel/timing blindness, funnel-forcing, partnerships-as-shortcut. Trigger when asked to create a GTM/go-to-market plan, launch plan, channel or distribution strategy, market-entry/timing plan, or launch metrics."
license: MIT
metadata:
  author: uxcel
  version: "1.0.0"
---

# Go-to-Market Plan Skill

## How this skill behaves (read first)

This is a **generative** deliverable skill, and "write a GTM plan" is where an AI assistant defaults to a **generic launch checklist** — announce, blog post, social, email, press — with no strategy underneath. The deeper mistakes: treating GTM as a **one-time launch** rather than a living system, **stage-skipping** (bolting a reseller network or paid-acquisition engine onto a company with 8 customers), ignoring **timing** (seasonality, B2B budget cycles, market readiness), and **funnel-forcing** buyers through a pipeline on the company's schedule. A GTM plan that doesn't fit the company's stage burns the resources that should be going to the actual foundational work.

So this skill gates hard:

1. **Establish context** — GTM readiness (is demand validated?), company maturity stage, customer/business-model type, and timing conditions.
2. **Apply the always-true core** — GTM as a system of five interlocking components, stage-appropriate execution, channel-as-cost-structure, timing awareness, non-linear buyer journey.
3. **Surface the context-dependent decisions** (stage tactics, channel model, business-model motion, entry timing, partnerships) with trade-offs; let the user choose.

Then it **hands off to `pm-okr-metric-validity-audit`** (are the launch metrics valid, not vanity?) and **`pm-assumption-rigor-audit`** (is demand really validated, is the timing window real, will the channel actually work?).

Scope: this skill owns **the go-to-market plan and its launch execution**. It defers **product strategy** to `pm-vision-strategy`, **positioning and competitive set** to `pm-competitive-analysis`, **pricing strategy** to `ux-pricing`, **buyer-journey/funnel analytics** to `pm-analytics`, and **post-launch experiments/learning** to `pm-experimentation-ab`.

---

## Step 0 — Establish context before planning

Ask if not known; state the assumption if proceeding without an answer:

- **Is the product GTM-ready?** No GTM plan repairs a product without validated demand. Readiness test: have real customers paid (or seriously committed), used it repeatedly, and can you explain *why* they bought and what would make them leave? If not, route back to validation (`pm-discovery`, `pm-experimentation-ab`) before building channels and pricing.
- **What's the company maturity stage?** Level 1 early traction (3–5 customers, manual) → Level 2 demand generation (5–25, one channel experiment) → Level 3 efficiency (25–100+, 2–3 proven channels) → Level 4 scaling TAM (platform/partnership decisions). **Stage is set by context, not just customer count** — business model, ticket size, customer type, and relationship complexity (3 enterprise contracts ≠ 3 consumer signups).
- **Who's the customer / what's the business model?** Consumer/prosumer (self-serve, product sells itself), SMB (weeks, light sales support), enterprise (6–18 mo, multi-stakeholder, consultative); and B2B / B2C / B2G / B2B2C — each changes the motion.
- **What timing conditions apply?** Seasonality, B2B budget cycle, first-mover vs. fast-follower position, and technology/regulatory readiness. Name these before setting the calendar.

---

## The always-apply core (true for any GTM plan)

### GTM is a system, not a launch

- **Treat GTM as a living system, not a one-time launch plan.** A launch plan is fixed; a GTM strategy adapts as the company grows and the market shifts. Revisit decisions at intervals — when a channel's performance drops, ask "is this still the right channel for where we are now?" not just "how do we fix it?"
- **The five components interlock: customers, channels, pricing, timing, partnerships.** None operates in isolation — changing pricing without reconsidering channel fit, or adding a partnership without a working direct motion, creates misalignment that compounds. (Pricing depth → `ux-pricing`; positioning → `competitive-analysis`.)
- **Keep strategy, tactics, and operations aligned.** Strategy = what game and how we win; tactics = the actions; operations = what we do today. Tactics without a strategic anchor default to repeating last week.

### Fit the stage

- **Do the work the current stage requires; don't skip stages.** Each level builds on the one before — you can't run an efficient multi-channel motion (L3) without having found the channel that works (L2), which needs the direct customer learning only L1 forces. Borrowing a mature company's playbook early (reseller program at 8 customers, VP of Marketing before a proven sales motion) consumes the resources foundational work needs.
- **Master one primary channel before going multi-channel.** Multi-channel is an "eventually" — add a second channel as a tested experiment layered on a proven motion, not to paper over the first one's problems. Running three channels with limited resources runs all three poorly.

### Choose channels and timing deliberately

- **A channel is a cost structure and a relationship, not just "where customers come from."** It determines margin, control, scale speed, and what business you're building. Match it to the mechanics of who buys (high-ticket/complex → direct; low-ticket/high-volume → digital/marketplace/affiliate); compute CAC *per channel*; and avoid single-channel dependency — start a second channel before the first shows strain, since channels break (algorithm changes, reseller shifts, fee changes).
- **Timing can kill a good product.** Indifference often reads as a product problem when it's a timing problem. Assess seasonality, B2B budget cycles (Q1 intent peaks), first-mover vs. fast-follower (first movers fund category education; fast followers harvest it), and technology/regulatory readiness — *before* committing major spend. Build a timing-aware calendar (the January push starts in November).

### Respect how buyers actually buy

- **The journey is non-linear — don't funnel-force.** Buyers pause, backtrack, and move on their own timeline. Follow buyer signals (a pricing-page revisit, a trial invite) over calendar-driven follow-ups; aggressive funnel-forcing loses deals that were still in play. Map the journey from real customer conversations, and measure the conversion at each stage transition.
- **Partnerships amplify what already works — they're not a shortcut.** A signed partner deal is the start of the work, not the end. Earn partnerships with proof points, enablement materials, and a replicable direct-sales playbook; a partner will amplify a broken motion just as readily as a working one.

### Execute the launch (when ready)

- **Lead with value proposition + messaging, aligned across teams.** Frame the value proposition around outcomes ("For [customer] who [need], our [product] is a [category] that [benefit]. Unlike [alternative], we [differentiator]"); keep product, marketing, sales, and support aligned (a RACI + shared timeline); ready sales/support 2–3 months out.
- **Define success metrics with baselines before launch.** Across campaign (leads, reach), product adoption (activation, retention), market impact (revenue, share, CAC), and qualitative feedback — set baselines and targets up front so the launch can be honestly evaluated. (Validate those metrics with `okr-metric-validity`.)

---

## The context-dependent decisions (surface, don't auto-apply)

Present each with its trade-off and a recommendation tied to Step 0; let the user choose. **Applying a later stage's playbook early is the failure mode.**

| Decision | Apply when | Avoid / adapt when | Default recommendation |
|---|---|---|---|
| **Stage-appropriate tactics** | L1: manual direct selling + learning; L2: direct + one channel experiment; L3: optimize 2–3 proven channels + coordination; L4: platform partnerships, channel teams, brand | Running L3/L4 tactics (resellers, paid engine, brand ads, VP hires) at L1/L2 | Diagnose the real stage from context; do only that stage's work |
| **Channel model** | Direct for high-ticket/complex/relationship sales (max learning, margin, control); indirect (reseller/affiliate/distributor/marketplace) for reach/speed once demand is proven | Indirect before the direct motion is understood; distributors before proven demand (they require it) | Direct first to learn; add indirect as a tested second channel when the first is working |
| **Business-model motion** | Consumer/prosumer → self-serve/freemium; SMB → product + light sales; enterprise → consultative, multi-stakeholder; adapt for B2B/B2C/B2G/B2B2C | A human sales motion on a low-ticket consumer product, or self-serve on a complex enterprise sale | Match the motion to ticket size, cycle length, and who's in the buying group |
| **Entry timing position** | First-mover when you can build switching costs/brand before rivals; fast-follower to differentiate on an underserved segment after demand is established | Funding category education as a first mover with no lock-in (followers harvest it) | Fast-follower differentiation unless you can defend a first-mover lead |
| **Timing window** | Align peak spend to peak receptivity — seasonality (consumer), Q1 budgets (B2B), regulatory deadlines | Launching into a seasonal trough, a budget-freeze quarter, or regulatory uncertainty | Build a timing-aware calendar; start the push ahead of the intent wave |
| **Partnerships** | After a proven direct motion, with enablement + proof points, to extend reach | As a shortcut to fix a struggling sales motion, or at L1/L2 | Defer until the motion works; then use partners to amplify it |

A couple of contexts flip several defaults at once: a **pre-PMF / Level 1** company should have a deliberately minimal GTM (founder-led direct selling, manual onboarding, no partnerships or paid engine); a **regulated B2B** product weights timing windows, multi-stakeholder motion, and proof points far more heavily.

---

## Validate the result (orchestration)

> Hand-offs name each lens by its installable skill `name`. Invoke one only if that skill is installed; if it isn't, this skill's own core already carries these rules — proceed without it rather than blocking.

After producing or revising, hand it to the audit lenses rather than declaring it done. These are **candidate** lenses — posture per `docs/orchestration-policy.md`, or route the whole artifact through `pm-product-review`. Here **`assumption-rigor` is the always-relevant lens (auto-runs)**; the others are **offered**, tied to what the artifact actually contains. If the user invoked this skill for one specific thing, respect that scope.

- **`pm-assumption-rigor-audit`** *(auto-runs)* — the plan rests on load-bearing bets: that demand is genuinely validated, that the timing window is real, that the chosen channel will perform, that the partner will prioritize you. Are those evidenced or assumed?
- **`pm-okr-metric-validity-audit`** *(offer — if it names launch/success metrics)* — are the launch/success metrics valid and actionable (activation, retention, revenue, share) rather than vanity (press hits, total signups), with baselines set before launch?
- **`pm-decision-quality-audit`** *(offer — if it makes a high-stakes, hard-to-reverse channel or timing commitment)* — checks the decision process behind it.

**Composition (per `docs/orchestration-policy.md` §9):** this skill feeds from and defers to its neighbors. **Strategy** (`pm-vision-strategy`), **positioning/competitive set** (`pm-competitive-analysis`), **pricing** (`ux-pricing`), and **buyer-journey/funnel analytics** (`pm-analytics`) are upstream inputs; **post-launch experiments** (`pm-experimentation-ab`) are downstream (offer to produce next, don't auto-generate). If the audits surface a conflict, resolve toward the purpose: **a GTM plan exists to reach customers in a way that fits the company's stage — if it skips validation, borrows a later stage's tactics, or ignores timing, fix that before spending.**

---

## Common do/don't patterns

| ❌ Don't | ✅ Do |
|---|---|
| Write a generic launch checklist | Build a system of customers, channels, pricing, timing, partnerships |
| Treat GTM as a one-time launch | Treat it as a living system, revisited as the company grows |
| Plan GTM for an unvalidated product | Confirm validated demand first (readiness test) |
| Apply a later stage's playbook early | Diagnose the real stage; do only that stage's work |
| Spin up multiple channels at once | Master one primary channel, then add a tested second |
| Treat a channel as just a traffic source | Treat it as cost structure + relationship; compute CAC per channel |
| Depend on a single channel | Build a second before the first strains |
| Ignore timing | Assess seasonality, budget cycles, first/fast-follower, readiness |
| Funnel-force buyers on your calendar | Follow buyer signals; map the journey from real conversations |
| Use partnerships to fix a broken motion | Earn partnerships with a proven motion + enablement |
| Report vanity launch metrics | Set valid campaign/adoption/impact metrics with baselines |
| Ship the plan unchecked | Hand off to okr-metric-validity + assumption-rigor |

---

## Source lessons (Uxcel)

- [The Go-to-Market Strategy](https://uxcel.com/lessons/the-go-to-market-strategy-294)
- [Go-To-Market Strategy](https://uxcel.com/lessons/go-to-market-strategy-302)
- [Direct vs. Indirect Channels](https://uxcel.com/lessons/direct-vs-indirect-channels-398)
- [Market Timing & Entry Conditions](https://uxcel.com/lessons/market-timing-entry-conditions-014)
- [The Customer & Their Buying Journey](https://uxcel.com/lessons/the-customer-their-buying-journey-905)
- [How Channel Strategy Evolves](https://uxcel.com/lessons/how-channel-strategy-evolves-174)
- [The Company Maturity Model](https://uxcel.com/lessons/the-company-maturity-model-625)
