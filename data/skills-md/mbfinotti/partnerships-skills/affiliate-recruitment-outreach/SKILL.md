---
name: affiliate-recruitment-outreach
description: Draft the outreach copy and sequence plan used to recruit new affiliates into a commission-based affiliate program - prospect qualification and tiering, pitch angle, first-touch recruitment email, follow-up sequence with a breakup touch, channel mix, and outreach tracking. Covers B2B SaaS and B2C ecommerce/DTC programs. Use whenever the user mentions recruiting affiliates, affiliate sourcing, or pitching content and review sites, coupon and cashback partners, newsletter operators, communities, podcasters, or agencies to join a program, even if they never say recruitment. Do NOT use for pitching one individually vetted creator - use mbfinotti/partnerships-skills@influencer-outreach instead.
license: MIT
metadata:
  author: Maya-Beth Finotti
  version: "1.4.5"
---

# Affiliate Recruitment Outreach

Draft the copy and sequence plan an affiliate program manager uses to actively recruit new affiliates. This skill owns active outreach only.

Affiliate recruitment has no canonical named industry framework. The only affiliate-native vocabulary with broad adoption is the active/passive recruitment split, coined by practitioner Geno Prussakov:

- _Passive_ recruitment makes the program findable.
- _Active_ recruitment reaches out to identified prospects.

Vendor and course models circulating in this space (five-P flywheels, "perfect partner" lists, 20-60-20 splits) are individual commercial programs, not industry standards. Never present one as a standard.

## Interview

Ask before drafting anything. One question per message; offer multiple-choice answers when possible. Skip any question the user already answered.

- Is the program B2B SaaS or B2C ecommerce/DTC? (Or both - then segment everything downstream.)
- What makes the product worth promoting - the value prop an affiliate's audience would actually care about?
- What is the already-decided commission, exactly: rate/model, cookie or attribution window, payout terms? This skill communicates the commission; it never designs or adjusts it.
- Which affiliate categories does this list target? (Content/review/comparison sites, coupon/cashback/loyalty, newsletter operators, communities, YouTube/podcast, consultants/agencies/integration partners, existing customers, competitors' current affiliates.)
- Where did the prospect list come from, and how warm is it? (Competitor backlink analysis, marketplace directory, event contacts, existing customers, inbound-adjacent, purchased.)
- Where are the prospects located? (US / EU / UK / Canada / mixed - this drives the legal regime for each segment.)
- What is the brand voice? (Formal, peer-casual, playful - or point to an example message.)
- Which CTA can you actually honor: apply link, pre-approved account, reply-for-more-info, or a booked call?
- Who signs the email, and from which address?
- By what date must recruited affiliates be producing? (A live date, next quarter, or no fixed date.)
- Is this a one-off win - a launch, a seasonal push - or a compounding channel you will still be running next year?
- What is the effort ceiling: manager hours per week, and what is already owned? (An existing affiliate roster, a licensed backlink or publisher-discovery tool, a retained agency, an existing customer list.)

The last three questions decide every ranking downstream - sourcing categories, discovery methods, tier attention split, cadence, CTA - so ask them before drafting, never at the moment of choosing.

- A hard near date promotes the fast rungs: competitor-affiliate and SERP sourcing, the 5-touch cadence, the reply-for-info CTA. It demotes complementary vendors and agency/integration partners, which pay a quarter later.
- A compounding mandate reverses that: complementary vendors, agencies, and podcast partners move up, and the long tier-1 pursuit becomes affordable.
- A low effort ceiling deletes the rungs needing coordination or procurement rather than demoting them - name which ones you dropped and why.
- Anything already owned re-ranks on top of all of this: a licensed backlink tool promotes link-intersect sourcing, a retained agency promotes the 12-attempt cadence, an existing roster of dormant partners beats a fresh tier-1 build.

Every ranking in this skill and its references is a default, not a law - it shifts with the segment, the list, and who executes it. Re-rank against the answers before presenting anything, and say out loud what moved.

## Workflow

1. Run the Interview; collect every answer before touching the list.
2. Qualify each prospect: audience fit first, then traffic/authority, then evidence of existing monetization. Treat "already promotes a competitor" as a positive signal, not a conflict. See [references/prospect-sourcing-and-qualification.md](references/prospect-sourcing-and-qualification.md).
3. Run a manual brand-safety screen - trademark bidding, coupon-injection/adware, spam sites - and drop failures before any outreach.
4. Verify prospect sites yourself if you can browse the web; otherwise ask the user for metrics from their backlink/link-intersect or publisher-discovery tooling.
5. Tier the survivors (1/2/3) per the sourcing reference; tier drives personalization depth, cadence length, and the order the week's hours are spent - tier 1 to exhaustion first, then down.
6. Segment the list by jurisdiction; apply each segment's outreach regime. Flag Canadian and German prospects - no cold email to them without a documented consent basis. See [references/outreach-compliance.md](references/outreach-compliance.md).
7. Brainstorm the pitch angle before drafting: enter brainstorming mode and propose 2-3 candidate angles with trade-offs and a recommendation, in the manager's own vocabulary (prospect list, pitch angle, sequence, activation).
8. Ask brainstorming questions one at a time; write no message until the manager explicitly picks an angle.
9. Draft the first touch per tier and segment, following [references/pitch-anatomy.md](references/pitch-anatomy.md). Every message references one specific, verifiable thing about that prospect - never fabricated familiarity.
10. Draft the follow-up sequence with rotating angles and a breakup touch, following [references/sequence-and-cadence.md](references/sequence-and-cadence.md).
11. Run your preferred humanizer skill over every drafted message. Never ship raw first-draft model output as final - it reads as the mass template affiliates delete on sight.
12. Self-check every message against the Quality gate below; iterate until every item passes on every message.
13. Present the plan section by section - tiers, angle, first touch, sequence, tracking - and validate each with the user before finalizing.
14. Hand off the full artifact (next section) including the pipeline-tracking plan.
15. If your harness has persistent memory, memorize the approved angle, brand voice, commission facts, and prospect tiers - later runs then skip straight past the interview.

## What to lead with - and what to withhold

Lead with one audience-fit reason: why this program fits _their_ audience, stated in one sentence. Then the economics, stated plainly - affiliates evaluate economics early, so make the commission easy to find rather than burying it.

- B2B SaaS: lead with recurring commission and the cookie/attribution window; add one proof the product converts (conversion rate, review credibility). CTA skews reply-for-info or booked call.
- B2C ecommerce/DTC: lead with order value, earnings-per-click if known, and seasonal/promo fit. CTA skews apply link or pre-approved account.
- Identical for both: personalization depth, the one-ask rule, message length, follow-up discipline, and every legal constraint. Only the proof points, CTA, and incentive framing diverge.

Withhold, always:

- The feature dump.
- Unearned-riches earnings math ("you could make $X/month").
- Long text.
- Cliché "partnership proposal" framing.

Documented practitioner guidance is unanimous that overlong first emails and hypothetical earnings calculations kill replies.

## Expected output

Deliver one structured artifact:

```
RECRUITMENT OUTREACH PLAN - <program>, <date>
Prospect tiers : tier 1/2/3 segments, counts, qualification rationale per tier
Legal segments : jurisdiction buckets + regime applied to each
Chosen angle   : approved pitch angle + why it beat the alternatives
First touch    : subject + body, one variant per tier/segment
Sequence       : table - touch / day / channel / angle / message summary
Breakup touch  : final message + what would reopen the thread later
Tracking plan  : pipeline stages, where tracked, review cadence, KPIs + targets
```

## Cadence

Two candidate cadences for affiliate recruitment:

- The 12-attempt cadence: follow up 7 days after first contact, then weekly, closing the file after ~12 attempts over ~3 months, rotating channels (email, social DM, contact form) across attempts.
- The 3-5 touch cadence: escalating gaps (day 0 / 3 / 7 / 14 / 21-28).

Both share these core principles:

- A single touch is ignored, not rejected - non-response usually means busy.
- Follow-ups are short (1-2 sentences).
- Each follow-up adds a new angle.
- A sent breakup email is honored.

Choose on manager hours, not on which source sounds more thorough:

- efficiency (replies per manager hour): `5 touches / ~4 weeks > 12 attempts / ~3 months`
- value (share of the list eventually reached): `12 attempts > 5 touches`
- effort (most first): `12 attempts > 5 touches`
- compliance cost (most first): `12 attempts > 5 touches`

Default to 5 touches over ~4 weeks for the standard list - four value touches plus the mandatory breakup, which lands day 21-28 and is what pushes the window past three weeks. The 12-attempt cadence costs roughly two and a half times the sends plus a per-attempt channel hunt, which makes it a standing job rather than a campaign.

It is also what this order starves: top of the value line, top of the effort line, last in the ratio, so it never wins a round on its own. Promote it deliberately for tier-1 prospects the manager both names and has the weekly hours for.

Delete both cadences rather than shorten either one when a prospect has no documented consent basis - passive recruitment is the only route there. See [references/sequence-and-cadence.md](references/sequence-and-cadence.md).

## Quality gate

Score every message in the sequence against all eight items. Pass threshold: 8/8 on every message. Iterate - redraft, re-run the humanizer - until no item fails.

1. Names one specific, verifiable fact about this prospect (their content, what they promote). No fabricated familiarity.
2. Exactly one ask, matching a CTA the manager confirmed they can honor.
3. First touch under 120 words; follow-ups under 50. (Working caps, not affiliate-specific published standards, but consistent with general cold-outreach research - see [references/pitch-anatomy.md](references/pitch-anatomy.md).)
4. Commission facts match the interview answers exactly - never rounded, never embellished.
5. No feature dump, no hypothetical earnings math, no "partnership proposal" cliché.
6. Sender identity, physical address where required, and a working opt-out satisfy the prospect's jurisdiction; no Canada/Germany cold email without a consent basis.
7. Angle rotates across the sequence; no "just checking in" touch.
8. Reads human aloud after the humanizer pass.

## KPIs

- Outreach-side: reply rate and application rate per tier and per angle. Expect cold-email-norm reply rates (roughly 3-9%, from general cold-outreach studies - not affiliate-specific data).
- Program-side, the KPI that actually matters: the share of recruited affiliates that become sales-active - the "activity index" (practitioner benchmark: ~20% of affiliates producing at least one click a week in a mature program; self-reported, not independently measured).
- Applications and approvals alone are vanity metrics - a recruit who never promotes cost you the outreach and returned nothing.
- Track the outreach pipeline (contacted → replied → applied → activated) in a CRM or spreadsheet; program dashboards show approvals and payouts, not outreach. Review weekly during a campaign.

## Common failure modes

| Failure                                                                              | Fix                                                                 |
| ------------------------------------------------------------------------------------ | ------------------------------------------------------------------- |
| Mass blast from one generic template                                                 | Tier the list; personalize per prospect; small batches              |
| Leading with commission % alone, no audience fit                                     | One fit sentence first; economics stated plainly right after        |
| Fabricated familiarity ("long-time fan of your work")                                | Cite one verifiable specific, or say honestly why you found them    |
| Recruiting cannibalizing partner types (coupon-injection, adware, trademark bidders) | Brand-safety screen before outreach, not after joining              |
| Slow application review souring the pitch                                            | Commit to 24-48h review before launching outreach                   |
| Terms surfacing post-pitch that contradict the email                                 | Gate on interview Q3; the email states only confirmed terms         |
| No follow-up after the first email                                                   | Ship the sequence with the first touch, never the first touch alone |
| Promising lax disclosure to close a prospect                                         | Never - affiliate promotions require disclosed material connections |

## Invocation Examples

- "Write the first-touch email and follow-up sequence for 40 comparison-site editors we want in our B2B SaaS program - 25% recurring for 12 months, already decided."
- "Our affiliate recruitment emails get no replies. Here are the last three we sent - rewrite them and fix the cadence."
- "We have a list of 200 prospects mixing UK sole traders, US bloggers and German media sites. Tier the list and tell me who we can cold-email."

## Reference

- `mbfinotti/partnerships-skills@influencer-outreach` - pitching one individually-vetted influencer or creator.
- `mbfinotti/partnerships-skills@affiliate-commission-structure` - designing the commission this skill only communicates.
- `mbfinotti/partnerships-skills@affiliate-program-terms` - the terms and conditions recruits sign.
- `mbfinotti/partnerships-skills@affiliate-onboarding-sequence` - everything after an affiliate is approved.
- `mbfinotti/partnerships-skills@affiliate-fraud-detection` - post-join traffic-fraud rules beyond the pre-outreach screen.
- `mbfinotti/partnerships-skills@affiliate-performance-dashboard` - the live program dashboard; this skill tracks only the outreach pipeline.
