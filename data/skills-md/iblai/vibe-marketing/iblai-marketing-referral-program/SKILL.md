---
name: iblai-marketing-referral-program
description: "When the user wants to create, optimize, or analyze a referral program, affiliate program, or word-of-mouth strategy. Also use when the user mentions 'referral,' 'affiliate,' 'ambassador,' 'word of mouth,' 'viral loop,' 'refer a friend,' 'partner program,' 'referral incentive,' 'how to get referrals,' 'customers referring customers,' or 'affiliate payout.' Use this whenever someone wants existing users or partners to bring in new customers. For launch-specific virality, see iblai-marketing-launch-strategy."
globs:
alwaysApply: false
metadata:
  version: 1.1.0
---

# /iblai-marketing-referral-program

Design and optimize programs that turn customers into growth engines.
Covers customer referrals and affiliate programs.

## Step 0: Context Check

Read `.agents/product-marketing-context.md` (or `.claude/product-marketing-context.md`
on older setups) first. Only ask for what isn't there.

Pull this context:

### 1. Program Type
- Customer referral, affiliate, or both?
- B2B or B2C?
- Average customer LTV
- Current CAC from other channels

### 2. Current State
- Existing referral/affiliate program?
- Current referral rate (% who refer)?
- Incentives tried so far

### 3. Product Fit
- Is your product shareable?
- Network effects?
- Do customers naturally talk about it?

### 4. Resources
- Tools/platforms in use or under consideration
- Budget for referral incentives

---

## Referral vs. Affiliate

### Customer Referral Programs

**Best for:**
- Existing customers recommending to their network
- Products with natural word-of-mouth
- Lower-ticket or self-serve products

**Characteristics:**
- Referrer is an existing customer
- One-time or limited rewards
- Higher trust, lower volume

### Affiliate Programs

**Best for:**
- Reaching audiences you don't have access to
- Content creators, influencers, bloggers
- Higher-ticket products that justify commissions

**Characteristics:**
- Affiliates may not be customers
- Ongoing commission relationship
- Higher volume, variable trust

---

## Referral Program Design

### The Referral Loop

```
Trigger Moment → Share Action → Convert Referred → Reward → (Loop)
```

### Step 1: Identify Trigger Moments

**High-intent moments:**
- Right after the first aha moment
- After hitting a milestone
- After exceptional support
- After renewal or upgrade

### Step 2: Design Share Mechanism

**Ranked by effectiveness:**
1. In-product sharing (highest conversion)
2. Personalized link
3. Email invitation
4. Social sharing
5. Referral code (works offline)

### Step 3: Choose Incentive Structure

**Single-sided rewards** (referrer only) — simpler, works for high-value products.

**Double-sided rewards** (both parties) — higher conversion, win-win framing.

**Tiered rewards** — gamifies the referral process, drives engagement.

Examples and incentive sizing: [references/program-examples.md](references/program-examples.md).

---

## Program Optimization

### Improving Referral Rate

**Few customers referring:**
- Ask at better moments
- Simplify the sharing process
- Test different incentive types
- Make referral prominent in the product

**Referrals aren't converting:**
- Improve landing experience for referred users
- Strengthen incentive for new users
- Ensure referrer's endorsement is visible

### A/B Tests to Run

**Incentive tests:** amount, type, single vs. double-sided, timing.

**Messaging tests:** program description, CTA copy, landing page copy.

**Placement tests:** where and when the referral prompt appears.

### Common Problems & Fixes

| Problem | Fix |
|---------|-----|
| Low awareness | Prominent in-app prompts |
| Low share rate | Simplify to one click |
| Low conversion | Optimize referred user experience |
| Fraud/abuse | Verification, limits |
| One-time referrers | Tiered/gamified rewards |

---

## Measuring Success

### Key Metrics

**Program health:**
- Active referrers (referred someone in last 30 days)
- Referral conversion rate
- Rewards earned/paid

**Business impact:**
- % of new customers from referrals
- CAC via referral vs. other channels
- LTV of referred customers
- Referral program ROI

### Typical Findings

- Referred customers have 16-25% higher LTV
- Referred customers have 18-37% lower churn
- Referred customers refer others at 2-3x rate

---

## Launch Checklist

### Before Launch
- [ ] Define program goals and success metrics
- [ ] Design incentive structure
- [ ] Build or configure referral tool
- [ ] Create referral landing page
- [ ] Set up tracking and attribution
- [ ] Define fraud prevention rules
- [ ] Create terms and conditions
- [ ] Test the complete referral flow

### Launch
- [ ] Announce to existing customers
- [ ] Add in-app referral prompts
- [ ] Update website with program details
- [ ] Brief support team

### Post-Launch (First 30 Days)
- [ ] Review conversion funnel
- [ ] Identify top referrers
- [ ] Gather feedback
- [ ] Fix friction points
- [ ] Reminder emails to non-referrers

---

## Email Sequences

### Referral Program Launch

```
Subject: You can now earn [reward] for sharing [Product]

We just launched our referral program!

Share [Product] with friends and earn [reward] for each signup.
They get [their reward] too.

[Unique referral link]

1. Share your link
2. Friend signs up
3. You both get [reward]
```

### Referral Nurture Sequence

- Day 7: remind about the referral program
- Day 30: "Know anyone who'd benefit?"
- Day 60: success story + referral prompt
- After milestone: "You achieved [X] — know others who'd want this?"

---

## Affiliate Programs

Detailed affiliate program design, commission structures, recruitment, and tools: [references/affiliate-programs.md](references/affiliate-programs.md).

---

## Task-Specific Questions

1. Program type — referral, affiliate, or both?
2. Customer LTV and current CAC?
3. Existing program or starting from scratch?
4. Tools/platforms you're considering?
5. Budget for rewards/commissions?
6. Is the product naturally shareable?

---

## Tool Integrations

See the [tools registry](../../tools/REGISTRY.md). Key referral tools:

| Tool | Best For | Guide |
|------|----------|-------|
| **Rewardful** | Stripe-native affiliate programs | [rewardful.md](../../tools/integrations/rewardful.md) |
| **Tolt** | SaaS affiliate programs | [tolt.md](../../tools/integrations/tolt.md) |
| **Mention Me** | Enterprise referral programs | [mention-me.md](../../tools/integrations/mention-me.md) |
| **Dub.co** | Link tracking and attribution | [dub-co.md](../../tools/integrations/dub-co.md) |
| **Stripe** | Payment processing (for commission tracking) | [stripe.md](../../tools/integrations/stripe.md) |
| **Introw** | Channel partner programs with tiers, deal registration, QBRs | [introw.md](../../tools/integrations/introw.md) |
| **PartnerStack** | Enterprise partner and affiliate programs | [partnerstack.md](../../tools/integrations/partnerstack.md) |

---

## Related Skills

- **iblai-marketing-launch-strategy**: Launching a referral program effectively
- **iblai-marketing-email-sequence**: Referral nurture campaigns
- **iblai-marketing-psychology**: Referral motivation
- **iblai-marketing-analytics-tracking**: Referral attribution
