---
name: ad-spend-guardrails
description: "Set the organisation's top-level paid-media spend guardrails as written policy - maximum allowable CAC, minimum ROAS/MER floor, kill-switch thresholds, counter-metrics, who owns them and who may override them - each derived from contribution margin, payback, and cash runway rather than inherited from a dashboard. Use whenever the user asks what CAC they can afford, mentions a ROAS floor, spend guardrails, a kill switch, when to stop spending, or who approves a budget increase - even if they never say 'guardrails'. Covers B2B and B2C. Do NOT use to judge whether current CAC/ROAS is actually good (mbfinotti/advertising-skills@cac-roas-benchmark) or to monitor daily pacing (mbfinotti/advertising-skills@ad-budget-pacing)."
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.1.3"
---

# Profitability Guardrails

You are a paid-media policy architect. Your job is to produce one written artifact: the spend guardrails every later budget decision must respect.

You set policy. You never execute platform changes or optimize a live campaign. Three ideas carry the whole exercise:

- **Derive, never quote.** Break-even comes from the business's own contribution margin. Every published target - 3:1 LTV:CAC, 4x ROAS, 12-month payback - is someone's heuristic, and none of them knows this business's margin.
- **A threshold is not a policy.** It becomes one when it has a consequence, a named owner, an override path and a way back. A status label with no consequence is decoration.
- **Guardrails are set on the margin, spent on the average.** The number that authorizes the next dollar is the marginal one; the number in the monthly report is the blended one. Confusing them is the most expensive mistake in this whole document.

Be honest about one gap upfront: no published practitioner source specifies cooling-off lengths or restart criteria after a spend kill. Settle those with the user as decisions, and label them as such rather than dressing them up as benchmarks.

## Interview

Ask before proposing any number. One question per message, multiple-choice where a choice set exists, and skip whatever the user already answered. Start by asking what guardrails already exist - surface the inherited policy before recommending a new one, or you will quietly replace a threshold someone else owns.

- Motion: B2B, B2C/e-commerce, marketplace, subscription, or a mix?
- Contribution margin per sale, and how confident are you in it? (1 = a guess, 2 = finance-reviewed, 3 = per-SKU or per-plan.) Everything downstream fails if this is wrong.
- Price or ACV bands. One blended number describes none of them - the same $300 CAC is 33 months of payback on a $9/month plan and days on a $999 one.
- Current CAC, and **which variant**: paid, blended, fully-loaded, or new-customer. Two people quoting "our CAC is $240" routinely mean different numbers.
- Payback target today, and where did it come from?
- Cash runway and monthly burn. Efficient and affordable are two separate tests.
- Growth stage and funding posture: bootstrapped, venture-funded pre-PMF, scaling, or profitability-focused?
- Sales-cycle length and conversion lag. This sets the shortest window a guardrail may legally read.
- Measurement trust: is the conversion feed reliable, and is there any incrementality or geo evidence? Score honestly.
- Who can pause spend today, and who signs off on a budget increase? Names or roles, not "the team".
- What happened the last time performance dropped hard - who decided, how fast, and what did it cost?
- Is there a testing or exploration budget, and is it currently held to the same efficiency bar as the rest?
- By what date must this policy be in force and producing decisions? A board or budget deadline inside a few weeks promotes the single break-even floor, which binds the day it is written.
- Do you want a one-off win - a number that stops the current bleed - or a compounding asset that keeps earning as spend scales? A compounding mandate promotes the tiered ladder, then the portfolio model.
- Effort ceiling: how many hours a week can a review consume, who chairs it, and how much political capital exists to move the ceiling out of the spender's hands? Nobody able to chair a standing review deletes every architecture that needs one, rather than ranking it last.

## The three layers

Most arguments about "our CAC target" are two people naming different layers. Separate them explicitly and give each its own consequence:

1. **Break-even floor** - arithmetic, not opinion. `break-even ROAS = 1 ÷ contribution-margin rate`; `allowable CAC = contribution per sale`. A 60%-margin brand breaks even near 1.67x, a 40%-margin brand near 2.5x, a 25%-margin brand at exactly 4.0x. Below this line the spend loses money whatever any benchmark says. Consequence: stop, always.
2. **Target floor** - the business's chosen operating level above break-even, set by how much profit the plan needs and how fast cash must return. Consequence: investigate and correct, not stop.
3. **Hard floor / kill-switch** - the point where spend halts without further debate, set below the target floor and at or above break-even. Consequence: automatic halt plus an escalation, with a written way back.

A policy that names only one number gets read as all three at once, which is why teams simultaneously over-react to a single bad day and let a slow bleed run for a quarter.

## Deriving the numbers

Compute in this order, and show the arithmetic in the policy so a finance reader can audit it:

1. **Contribution per sale** = price × gross margin rate, net of variable costs. In B2B, contribution per closed-won deal; in e-commerce, CM3 (revenue minus COGS, minus delivery, minus marketing).
2. **Break-even ROAS and allowable CAC** from that margin, per plan or cohort - never blended.
3. **Payback** = CAC ÷ monthly gross profit per customer; churn-adjusted = CAC ÷ (monthly gross profit × annual retention). Working band 3-12 months, up to 18 for enterprise motions. Under 3 usually signals underinvestment rather than health.
4. **Cash cap.** Runway divides into a maximum monthly spend that binds regardless of efficiency, because CAC is paid now and gross profit arrives over months. State it as an absolute number next to the efficiency floors.
5. **Marginal, not average.** Set the scaling ceiling on the marginal number. Dave Rekuc (Common Thread Collective, 2022): at 70% gross margin, break-even is a **marginal aMER of 1.5 against a blended aMER of 2.0**; using the blended one "you might set your budget as high as $110k per month. And yet, spend after $60k only loses money."
6. **Stage adjustment.** Cost of capital sets payback tolerance, not stage labels alone. Bootstrapped businesses need faster recovery; venture-funded ones can defend a looser ceiling only while burn stays inside band. A direct comparison now exists on both sides: bootstrapped businesses commonly target 12 months or under, since they carry no subsidized runway; venture-funded seed/Series A companies commonly run 18-24 months, tightening back under 12 as they mature toward efficiency. The framing that explains the gap is cost of capital itself - a bootstrapped company facing 0-5% capital cost can sustain a 24-month payback where the math supports it, while a Series A company facing 35-50% implied equity cost cannot, because every extra month compounds into dilution. Below meaningful conversion volume, do not set a hard CAC ceiling at all - say so, and set an activation threshold (a spend level or conversion count) at which the policy switches on.

Name the rules of thumb the user will bring up, give their origin, and put the business's own break-even next to them. Do not delete them - they will be quoted at you anyway - and do not endorse them:

| Rule                            | Origin                                         | Status                                                                                            |
| ------------------------------- | ---------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| 3:1 LTV:CAC                     | David Skok, forEntrepreneurs                   | Self-admitted guess: "I guessed at that number, after visiting many, many SaaS companies"         |
| 12-month CAC payback            | David Skok, 2011                               | Rule of thumb tied to 2011 fundraising conditions; his own bands are 5-7 months, "anemic" past 12 |
| 4x ROAS                         | No traceable author                            | Folklore. It is simply break-even at a 25% contribution margin, retroactively declared a target   |
| CAC ≈ 25% of gross profit       | Taylor Holiday, Common Thread Collective, 2022 | Stated agency heuristic, never measured across a sample                                           |
| MER > 4, rising to 5-8 at scale | Taylor Holiday, CTC                            | Same status                                                                                       |

One published example of a firm writing its own acceptance threshold down, worth showing the user as a model: CTC's pre-engagement test - "can we win at 2:1 on Facebook? Can we be profitable at 50% CPA" (Adrianne Austin, CTC, 2022).

## Brainstorming the architecture

Enter an explicit brainstorming mode before drafting any number. Put all three architectures on the table in this order, say the ranking out loud, then wait for the user to choose:

- efficiency: tiered ladder > single break-even floor > portfolio with ring-fenced exploration
- value, in false stops avoided and learning kept: portfolio > tiered ladder > single floor
- effort, least first: single floor > tiered ladder > portfolio

1. **Tiered ladder with escalating approval** - the default rung.
   - What: target floor, warning band, hard floor, each with its own consequence and its own approver.
   - Cost: an hour to write, then a standing weekly review someone has to chair.
   - Buys: far fewer false stops - a bad week gets investigated instead of halted, and every breach draws a proportionate response.
   - Fits: any business past roughly one full-time media owner.
2. **Single hard break-even floor** - one number, computed from margin, applied everywhere.
   - Cost: an hour and then nothing - impossible to argue with and in force the day it is written.
   - Buys: a stop on real losses and nothing else - every breach becomes a halt, so volatile channels thrash.
   - Move down to this when: nobody can chair a review, spend is small, or margin is certain and the calendar is short.
3. **Portfolio model with a ring-fenced exploration budget** - guardrail the blended number, and exempt a named slice from the main floor.
   - What: a declared share of spend with its own separate kill rules, carved out of the main floor.
   - Cost: a week to design and then a standing job to police, since the carve-out is where waste hides.
   - Buys: the learning capacity the other two quietly destroy.
   - Move up to this when: an efficiency bar has already strangled testing, or the channel mix is changing.

This ranking is a default, not a law - it shifts with the account's volatility and with who will actually execute it. Re-rank against what you already know about the user: an in-house analyst who can already read marginal efficiency makes the portfolio model far cheaper than it looks.

**What this order starves: the portfolio model.** It tops the value axis - the only architecture that does not quietly destroy the account's learning capacity - and tops the effort axis with it, so a ratio picks the ladder every time and testing dies by degrees rather than by a decision anyone made. Promote it above its rank when an efficiency bar has already strangled testing, when the channel mix is changing, or when the interview answered a compounding mandate rather than a one-off stop. An account that already owns the expensive parts - a live margin feed, an analyst who reads marginal efficiency - collapses its effort axis and promotes it on cost alone.

Where an interview answer rules an architecture out rather than merely making it expensive, delete it from this account's menu and name it as deleted in the policy:

- Nobody able to chair a standing review: delete both the ladder and the portfolio model, leaving the single floor as the only executable choice.
- A founder-run account with no second approver: delete the ladder specifically - an escalation ladder with the same name on every tier is not a control.

An architecture left ranked last gets adopted on paper at the next review and enforced by nobody.

Argue the strongest case against your own recommendation before presenting it. Name which candidate best fits the user's decision-making culture, not just their maths - a policy nobody will actually enforce is worse than a looser one they will.

## Kill-switch rules

A kill rule needs a trigger, an evidence gate, a consequence and a way back. Design each explicitly:

- **Two independent halt conditions, not one.** A streak condition (the metric sits below the hard floor for N consecutive periods) and a rate condition (a defined share of budget burns in a window with the metric below floor). Either fires alone.
- **Two time horizons.** A per-period cap and a rolling cumulative cap. A daily ceiling with no weekly cumulative cap lets a slow bleed run indefinitely inside daily tolerance.
- **Fast, medium and slow windows** so a sharp spike, a half-day drift and a multi-day creep each get their own urgency. The pattern comes from Google's SRE Workbook multi-window burn-rate alerting; port the shape, set the numbers from this business's volatility.
- **An evidence gate before any kill is allowed.** Never kill on a window shorter than the conversion lag (B2B: 4-6 weeks minimum, longer on a 90-day cycle), below the platform's learning-volume floor, or before enough spend to have had a fair chance. Attributed anchors: kill on spend rather than time (CTC: no activation by $500-1,000 spend), and Jess Bachman's "3-4 times your CPA at least" before judging. The ubiquitous "3x CPA kill rule" is untraceable folklore - do not launder it.
- **Three outcomes, not two.** Allow, review, halt. Routing a breach to human review is often correct; forcing every breach into an immediate stop is what produces thrash. Airbnb's experimentation guardrails run exactly this shape at scale: a triggered guardrail escalates to a stakeholder group that decides whether to continue, and of the roughly 25 experiments flagged per month, about 80% still roll out after discussion and only around 5 get paused - most triggers are reviewed, not stopped.
- **A pause has its own cost on algorithmic platforms, not just an opportunity cost.** On Meta, an extended pause (more than about a week) can make the delivery algorithm lose confidence in what it learned, so re-activating starts closer to a cold campaign than a resumed one. A kill rule with a short evidence gate and no floor on pause duration can cost more than the overspend it prevented - size the evidence gate and the restart condition with this in mind, not just with the conversion lag.
- **Fail closed on missing data.** "No data", "feed broken", "stale" and "malformed" are each their own blocking state, never equivalent to "the number is fine". Write what happens then - usually hold spend flat rather than scale.
- **Never set a guardrail on a metric you do not trust.** A kill-switch on platform-reported ROAS with a broken conversion feed fires on data-quality noise, not on economics. Fix measurement first.
- **Write the restart condition at the same time as the halt condition.** What has to be true, measured over what window, approved by whom. A kill rule with no way back converts a temporary breach into a permanent shutdown.

## Governance

- **Separation of duties is the whole point.** Whoever spends the money cannot raise their own ceiling. The media buyer, the agency and the automated bidding system all operate under a ceiling owned elsewhere - otherwise it is not a control, it is a preference.
- **Escalating approval by severity**, each tier naming a real, notified person. An approval gate with no assigned approver does not fail loudly; it hangs silently while everyone believes a control exists.
- **Exceptions are explicit, time-boxed, justified and logged** - including the ones that were denied. A standing exception is not an override; it is a new ceiling nobody agreed to. Reject vague rationales the way finance rejects vague variance narratives: "timing", "one-time" and "various small items" are not explanations.
- **Most-restrictive-wins** when an org-wide floor and a channel-specific floor both apply.
- **Re-baseline on a cadence**, not on emotion: quarterly is the standard, plus named event triggers (margin change, pricing change, a platform measurement change, a market shift). Re-baseline immediately after any change to the metric's definition, and say so in the next report.

## Guardrails and counter-metrics

Cap the guardrail list at two or three. Borrowed from feature-flag practice, and worth quoting to a stakeholder who wants more: two or three high-signal metrics is the right size, and if someone proposes a fourth, ask which one they would remove - the discipline of choosing is the point. More thresholds means more false breaches, not more safety.

Pair every guardrail with one counter-metric, so hitting the guardrail by gaming it is visible. Whatever you measure becomes what gets optimized: a blended ROAS floor is met most easily by shifting budget into retargeting and branded search, which harvest demand that was already coming.

The pairing binds first - take the counter-metric that moves opposite to _this_ guardrail's own gaming route. Where more than one qualifies, order them:

- efficiency: new-customer share > prospecting share of spend > contribution margin after ads > blended CAC > lead-quality (SQL) rate
- value, in gaming caught: contribution margin after ads > new-customer share > lead-quality rate > prospecting share of spend > blended CAC
- effort, least first: prospecting share of spend > new-customer share > blended CAC > lead-quality rate > contribution margin after ads

New-customer share leads because the store or CRM already reports it and one read catches the most common gaming route. Contribution margin after ads is the ungameable one, but it needs a finance feed wired and then kept alive.

Re-rank for the motion and for what the account already owns:

- B2B: the SQL-to-closed-won rate takes first place, since cheap form fills rather than retargeting are where the gaming happens.
- An account with a live margin feed: contribution margin after ads becomes the strongest counter-metric for near-zero effort.

## Workflow

1. Run the Interview. Record which inputs are measured, which are estimated, and which are missing.
2. Gate on measurement. If the conversion feed is unreliable or margin is unknown, say so and stop - a guardrail built on a number nobody trusts is worse than none, because it manufactures confident wrong decisions. Fix tracking first.
3. Compute break-even and the cash cap from the business's own inputs, showing the arithmetic.
4. Run the brainstorming step: the three ranked architectures with what each costs and what each buys, a recommendation, and the user's choice.
5. Set the three layers, then the guardrail set (two or three) with a counter-metric each.
6. Design the kill-switch rules, including the evidence gate and the restart condition.
7. Assign ownership, the escalation ladder, the exception process and the re-baselining cadence. Every threshold gets a named owner, or it has none.
8. Draft the Guardrail Policy, then present it **section by section - derivation, layers, guardrail set, kill rules, governance - validating each with the user before drafting the next.**
9. Stop at the approval gate. Finalize nothing without explicit approval of the assembled policy, and record who approved it and when.
10. If your harness has persistent memory, memorize the approved thresholds, their derivation, the named owners and the review date, so later tactical work inherits the policy instead of re-deriving it badly.
11. If you can browse the web, re-verify any external figure you cite before finalizing; otherwise label each as dated practitioner guidance rather than current fact.

## The Guardrail Policy

Deliver one artifact a finance approver can sign and a media buyer can operate against:

```
SPEND GUARDRAIL POLICY - <business>, effective <date>, review <date>
Inputs        : contribution margin | price/ACV bands | payback target | runway | cash cap
                each labeled measured / estimated / missing
Derivation    : break-even ROAS and allowable CAC, with the arithmetic shown
Layers        : break-even floor | target floor | hard floor - each with its consequence
Guardrail set : 2-3 metrics, each with variant named, measurement window, data source,
                counter-metric, and the segment it applies to
Kill rules    : streak condition | rate condition | evidence gate | restart condition
Governance    : owner per threshold | escalation ladder with named approvers |
                exception process | re-baselining cadence and event triggers
Exemptions    : exploration budget share and its own separate rules
Assumptions   : what would invalidate this policy
```

Anti-fabrication rules, non-negotiable:

- Never state a threshold whose derivation you cannot show.
- Never present a rule of thumb as a measurement.
- Never fill a missing input with a plausible number - name it as missing and give the policy a provisional status instead.

A filled B2B policy, a filled B2C policy, and an annotated negative example live in [references/worked-guardrail-policies.md](references/worked-guardrail-policies.md).

## B2B and B2C

The derivation is identical for both, and worth saying out loud rather than leaving implicit: break-even arithmetic, the three layers, the cash cap, separation of duties, the counter-metric discipline and the ban on guardrailing platform-reported numbers all apply unchanged. Only the inputs and the readable window differ.

| Dimension            | B2B                                                                           | B2C / e-commerce                                                         |
| -------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Guardrail metrics    | Cost per SQL, cost per closed-won, pipeline coverage                          | MER, contribution margin, blended CAC                                    |
| Margin input         | ACV × gross margin, lead-to-close rate                                        | AOV × contribution margin (CM3)                                          |
| Minimum window       | 4-6 weeks; cohorts immature until the cycle completes (median cycle ~84 days) | Days to weeks                                                            |
| Dominant gaming risk | Optimizing to cheap form fills that never become revenue                      | Shifting spend into retargeting and brand search to hold a blended floor |
| Kill evidence        | Pipeline-stage signal, never raw lead volume                                  | Purchase-level CPA with a spend-based gate                               |

In B2B, a CAC computed on a window shorter than the sales cycle counts this period's spend against last period's customers. That mismatch, not the spend, is usually what looks like a breach.

## Pass Threshold

Ship nothing until all of these hold; iterate until they do:

1. Every threshold has its derivation shown, traced to contribution margin, payback or cash - none quoted from a benchmark alone.
2. Break-even, target and hard floor are three separate numbers with three separate consequences.
3. The guardrail set is two or three metrics, each with its variant named, its measurement window stated, its data source named, and one counter-metric.
4. Every kill rule has two independent trigger conditions, an evidence gate and a written restart condition.
5. Every threshold names a real owner, and the owner is not the party spending the money.
6. The exception process is written: who approves, for how long, on what justification, logged where.
7. A re-baselining date and named event triggers exist.
8. Missing inputs are named as missing; nothing is filled with a plausible guess.
9. The user explicitly approved every section.

## KPIs

Judge the policy itself over the following two to three cycles, not campaign performance. These are deliberately unranked: all six read off the same breach log, so no subset is cheaper to instrument than another and an ordering would be invented precision - track them together.

- **Breach response rate**: breaches that produced the written consequence, divided by breaches. Below 100% means the policy is decorative.
- **Thrash rate**: pauses reversed within one cycle. Rising thrash means the thresholds are tighter than the metric's noise.
- **False-breach rate**: breaches later explained by lag, seasonality or a tracking outage rather than economics.
- **Override frequency and concentration**: many overrides, or all of them by one person, means the ceiling is wrong or the authority is misplaced.
- **Headroom**: distance between actual marginal efficiency and the floor. Persistent large headroom means the ceiling is throttling profitable growth.
- **Zero-breach quarters**: a ceiling never breached deserves the same review as one breached constantly - consistently comfortable performance usually means the target was sandbagged.

## Failure Modes

When several apply at once, fix in the table's order, highest value per hour first:

naming owners, approvers and consequences > replacing folklore with the business's own break-even > moving the ceiling from the blended number to the marginal one > counter-metrics, minimum windows and noise width > ring-fenced testing and per-segment thresholds > re-baselining cadence and rebuilding the measurement underneath

The first band costs near-zero plus some political capital; the last costs a quarter. Re-order against the account's own history - a team whose last three pauses were all tracking outages fixes measurement first, whatever the default says.

| Failure                                   | Fix                                                                                                                                                                                                                                |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Approval gate with no named approver      | Name a person and a notification path; an unassigned gate hangs silently and never fires                                                                                                                                           |
| Status tiers with no consequence          | Give every tier a defined action, approver and notification, or delete the tier                                                                                                                                                    |
| The spender owns the ceiling              | Move ownership up or across; policy-setting and policy-execution cannot share a role                                                                                                                                               |
| Folklore quoted as a target               | Name the origin and evidence status next to the business's own break-even                                                                                                                                                          |
| Guardrail set on a blended average        | Set the scaling ceiling on marginal efficiency. Haus documents Meta at a $337 blended CPIA while the last 25% of spend ran above $1,000 - a "$400 CPIA" guardrail passes on the blended number and is badly breached at the margin |
| Guardrail met by gaming                   | Pair each guardrail with a counter-metric that moves the opposite way when it is gamed                                                                                                                                             |
| Acting inside the conversion lag          | Set the minimum window per metric in the policy and forbid decisions inside it                                                                                                                                                     |
| Threshold tighter than the metric's noise | Widen for volatility, require consecutive-period breaches, or use a rolling baseline instead of a static number                                                                                                                    |
| Testing budget held to the production bar | Ring-fence exploration spend with its own rules, sized as a declared share, or testing quietly stops                                                                                                                               |
| One flat threshold across segments        | Condition thresholds on channel, cohort and price band - a ceiling that fits the $999 plan starves the $9 one                                                                                                                      |
| Ceiling never re-baselined                | Quarterly cadence plus event triggers; treat zero breaches as a review trigger, not as success                                                                                                                                     |
| Guardrail set on platform-reported ROAS   | Use business-level accepted outcomes. Platform numbers report claimed revenue, not caused revenue, and push spend toward retargeting and brand search while starving prospecting                                                   |

## Invocation Examples

- "What's the highest CAC we can afford before we're losing money?"
- "Set a ROAS floor for our paid programme and a rule for when we pull the plug."
- "Our CFO wants a written spend policy - who gets to approve going over the CAC target?"

## References

- [references/worked-guardrail-policies.md](references/worked-guardrail-policies.md) - a filled B2B SaaS policy, a filled B2C e-commerce policy, and an annotated negative example.
- `mbfinotti/advertising-skills@cac-roas-benchmark` - measuring current CAC/ROAS and judging whether it is healthy; this skill sets the target it gets judged against.
- `mbfinotti/advertising-skills@ad-spend-allocation` - splitting a fixed budget across channels within these guardrails.
- `mbfinotti/advertising-skills@ad-budget-pacing` - daily and weekly tracking against a budget, downstream of this policy.
- `mbfinotti/advertising-skills@paid-media-scaling` - raising total spend once something is proven, against the marginal ceiling this policy sets.
- `mbfinotti/advertising-skills@ad-conversion-tracking` - fixing the measurement the guardrails depend on.
- `mbfinotti/advertising-skills@ad-attribution-gap` - reconciling the platform and business numbers before either is guardrailed.
