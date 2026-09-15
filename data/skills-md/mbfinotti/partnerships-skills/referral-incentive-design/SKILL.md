---
name: referral-incentive-design
description: Design the reward structure of a customer refer-a-friend program - who gets rewarded (referrer, friend, or both), reward type (cash, account credit, discount, product value, status), how much to pay against LTV/CAC and gross margin, when the payout fires, and whether to build a tiered reward ladder. Use whenever the user mentions referral incentives, refer-a-friend rewards, referral bonus amounts, give-X-get-Y offers, double-sided referral rewards, or asks how big a referral reward should be, even if they never say incentive. Covers end-customer rewards only. Do NOT use for commission rates paid to professional affiliates - use mbfinotti/partnerships-skills@affiliate-commission-structure instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.0.9"
---

# Referral Incentive Design

Design the reward structure of a customer refer-a-friend program. No canonical named framework exists for this discipline - referral is one letter inside measurement funnels like AARRR, not a design method. What exists is four decision variables, each with its own evidence base, worked through in order because each shapes the next:

1. **Sidedness** - reward the referrer, the friend, or both (the Reward-Me / Reward-You / Reward-Both taxonomy, Ryu & Feick, _Journal of Marketing_ 2007).
2. **Reward type** - cash, account credit, discount, product value, status, or donation.
3. **Reward size** - anchored to gross margin, LTV, and CAC, with a floor set by non-monotonic response (a too-small reward performs worse than none).
4. **Payout trigger and tier structure** - when the reward fires, and whether rewards escalate with cumulative referrals.

## Interview

Ask before recommending anything. One question per message; offer multiple-choice answers when possible. Skip a question only when the user already gave the answer.

- Is the business B2B or B2C? Subscription or one-time purchase? Self-serve or sales-led?
- What are the gross margin, average LTV (or first-year revenue), blended/paid CAC, and entry-plan price?
- Do customers already recommend the product organically? Roughly what share of new customers arrive that way?
- Will the referrer plausibly buy again (account credit has value to them), or not (only cash-equivalents do)?
- For B2B: is the likely referrer the buyer, or an employee whose company pays?
- By what date must this show results? A hard quarter-end date promotes the fast rungs - a flat reward on a first-purchase trigger - and rules out ladders and retention-gated triggers, which need months to read.
- One-off acquisition win, or a compounding asset? Compounding promotes in-kind and status rewards, a tier ladder, and a retention-gated trigger; a one-off win promotes a flat friend-side offer.
- What is the effort ceiling: who builds and administers this, how many hours do they have, and can a published reward be withdrawn later? A low ceiling deletes swag, sweepstakes, and staged payouts outright; a dedicated owner puts the ladder back on the table.

## Workflow

1. Run the Interview above; collect every answer the structure depends on before designing.
2. Check the disqualifiers before designing. A referral program captures existing word-of-mouth; it does not create it. No organic referral signal, or an LTV too low to fund a meaningful reward, means the honest answer is "not yet" - say so and stop. Confirm the question is about end-customer referrals, not external affiliates or channel partners (different economics, different tooling; B2B programs tend to migrate from the former to the latter as ACV grows).
3. Decide sidedness, working from [references/sidedness-and-triggers.md](references/sidedness-and-triggers.md). Efficiency order: **friend-only > double-sided > referrer-only** - effort is identical across the three arms, so the value evidence decides, and field experiments found recipient-only rewards matching double-sided rewards that cost twice as much. Lead with friend-only; move to double-sided for an innovative product or a weak brand with weak ties, and to referrer-only only for a genuinely high-effort referral process.
4. Choose the reward type per side from [references/reward-types.md](references/reward-types.md), leading with its efficiency order: **in-kind product value > account credit == free months > discount > status > cash > swag > charity > sweepstakes**. Then apply the criteria that override it:
   - Cash-equivalents when the referrer will never rebuy or the product is money-adjacent.
   - Status over cash when referring is a public, identity-driven act.
   - Charity only ever as a choice.

   For B2B, resolve the principal-agent fork (individual reward vs company account credit) explicitly.

5. Size the reward using [references/sizing-and-tiers.md](references/sizing-and-tiers.md): compute the gross-profit ceiling, pick a target inside it starting from the least-effort anchor (**% of CAC > % of LTV > payback discipline**), verify the floor (non-monotonic response: pay meaningfully or pay nothing), and frame the number with the Rule of 100 (percentage below $100, absolute amount above).
6. Set the payout trigger on a verified value event, never bare signup. Efficiency order: **first purchase > qualified activation > closed-won/first invoice > retention threshold > staged payout**; promote closed-won for a sales-led B2B motion, and the retention threshold when refund or churn exposure is large. Match the holding period to refund risk and sales-cycle length.
7. Decide whether to tier, against the ladder rules in [references/sizing-and-tiers.md](references/sizing-and-tiers.md). Efficiency order: **flat > threshold ladder > stepwise**; the ladder is worth its build cost only when volume is high, repeat referrers are plausible, and advocacy concentrates in a few advocates. First tier trivially achievable; top tier always capped - the best-documented failure in this field is an uncapped ladder.
8. Present the four decisions one by one - options considered, trade-offs, and your recommendation - and validate each with the user; revise on pushback before moving to the next.
9. After explicit approval on all four, emit the full structure as a testable spec (next section), grounded in a matching worked example from [references/examples.md](references/examples.md) when one fits the user's situation.
10. If your harness has persistent memory, memorize the approved spec's key decisions and economics - a later diagnosis run starts from them instead of re-interviewing.

Every ordering above ranks value returned per unit of _effort_ - build time, administration, fulfillment, coordination, and how hard the choice is to reverse once published. Never rank by payout size; what a reward costs is a separate axis, and the two disagree often enough that a blended rank hides the case where the cheapest option and the strongest one are different options.

Each order is a default, not a law: it shifts with the situation and with who has to execute it. Re-rank against what you already know about this user before presenting any menu:

- A product whose marginal unit costs near zero promotes in-kind rewards above everything.
- A finance team that refuses cash payouts deletes cash from the menu rather than demoting it.
- An existing rewards platform erases the effort gap that puts ladders and swag near the bottom.

Say out loud which fact moved which option, so the user can argue with the reasoning instead of the row order.

## The Reward Structure Spec

Deliver every engagement as this artifact - a decision record the user can hand to product, finance, and a test-plan owner:

```
REWARD STRUCTURE - <product>, <date>
Sidedness        : both | friend-only | referrer-only, split, disclosure choice
Reward (friend)  : type, amount, framing ("first month free", not "$49 off")
Reward (referrer): type, amount, framing
Payout trigger   : verified event per side + holding period + pending-state display
Tiers            : ladder breakpoints + top-tier cap, or "flat - revisit when <condition>"
Caps             : per-referrer/year, total-earned, program budget ceiling
Economics        : gross-profit ceiling, projected cost per referred customer vs current CAC
Validation       : test arms, % of base exposed, duration, decision metric, incrementality check
KPIs             : participation rate, share-to-signup conversion, cost per incremental referred customer vs CAC
```

Three rules about the spec itself:

- **Every line carries a reason.** "Referrer credit fires on the second invoice - survives the refund window" is reviewable; a bare amount is not.
- **The validation plan is not optional.** Sidedness is genuinely contested between practitioners and field research, so name its test arms (both / friend-only / referrer-only, on 5-10% of the base) and its incrementality check. The incrementality check means holding out a slice: flat acquisition volume with rising CAC shows the program pays for customers who would have come anyway.
- **The spec has a pass threshold.** Projected cost per incremental referred customer must land below current blended CAC and inside the gross-profit ceiling. Iterate size, type, or trigger until both hold; if no structure passes, recommend not launching.

## Diagnosing an Existing Program

When the user arrives with a running program instead of a blank page ("we give $10 credit and nobody uses it"), work the fixes in efficiency order - most program repaired per unit of effort, which is not the same as the cheapest fix first:

**efficiency**: reposition the ask > reweight the split toward the friend > raise the size above the floor > cap the ladder and move the trigger > switch reward type > run the incrementality holdout

| Symptom                                     | Check first                                                                               | Effort                                                                           | Variable at fault                                                                  |
| ------------------------------------------- | ----------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Few customers ever share                    | Timing and friction of the ask - placement moves participation more than reward size does | An hour - move the prompt, change the copy                                       | None - fix the ask before touching the reward                                      |
| Shares happen, friends do not convert       | Friend-side offer strength - the friend has the harder job                                | An hour - reweight a budget you are already spending                             | Sidedness/split                                                                    |
| Participation dropped after adding a reward | Token amount below the motivation floor turned a favor into a badly paid job              | An hour of config, against a permanent budget increase                           | Size                                                                               |
| Power referrers milk the ladder             | Missing top-tier cap or signup-fired trigger                                              | A week - and capping a published ladder is the hardest change here to make stick | Tiers/trigger                                                                      |
| B2B referrers decline rewards               | Corporate gift policy collision                                                           | A quarter - finance, procurement and legal all touch it                          | Type: switch to the two-track pattern (company credit + optional individual token) |
| Healthy referral volume, rising CAC         | Incrementality - rewards paying for organic word-of-mouth                                 | A quarter - design the holdout, wait out a full cycle to read it                 | Economics: run the holdout, then narrow the reward to low-organic-reach segments   |

The order starves the incrementality holdout: it lands last on ratio and first on truth, because it is the only check that can reveal the whole program is buying customers who were coming anyway. Promote it immediately when referral volume looks healthy while CAC climbs - that is the one symptom no cheap fix explains. Re-rank the rest against the user's constraints too: a team that cannot ship UI this quarter cannot reposition the ask, which pushes the split reweight to the top.

## B2B and B2C

Identical in both, whether B2B or B2C:

- The four decisions and their order.
- The gross-profit ceiling.
- The non-monotonic floor.
- The Rule of 100 framing.
- The payout trigger on a verified value event.
- The incrementality haircut.

Do not reinvent any of them per side.

The evidence base is the asymmetry worth stating out loud: the field experiments and academic results this skill leans on are overwhelmingly consumer-side. Treat every number here as B2C-measured and B2B-inferred, and say so when advising a B2B program.

| Dimension              | B2C                                                 | B2B                                                                                                                                                                     |
| ---------------------- | --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Who is rewarded        | The customer, who is also the payer                 | Often an employee who is not the payer - resolve the principal-agent fork explicitly at step 4                                                                          |
| Reward vehicle         | Account credit or cash-equivalent to the individual | Company account credit by default; an individual reward is a gift-policy and procurement question before it is an incentive                                             |
| Payout trigger         | First paid invoice or an activation milestone       | Later - closed-won or a retention threshold, because the cycle is longer and refund exposure larger                                                                     |
| Scaling ceiling        | Holds at scale                                      | Real: as ACV grows, customer-referral programs migrate into affiliate or partner programs. Watch for the migration signal rather than stretching this structure past it |
| Disclosure sensitivity | Moderate                                            | Higher - a referrer recommending a vendor to their own network carries a material connection their employer may also police                                             |

## Invocation Examples

- "Design the refer-a-friend rewards for a $49/mo B2B SaaS - 80% margin, 14-month average tenure, $220 paid CAC."
- "We give $10 credit both sides and nobody uses it. Diagnose which of the four variables is at fault."
- "Should our referral rewards be tiered? About 8% of customers refer, and a handful refer repeatedly."

## Reference

- `mbfinotti/partnerships-skills@affiliate-commission-structure` for commission design aimed at professional affiliates and partners.
- `mbfinotti/partnerships-skills@referral-abuse-guardrails` for the enforcement layer around caps - velocity limits, cooldowns, burst detection, verification gates, and the published wording that makes a cap stick. This skill sets the cap values; that skill makes them hold.
