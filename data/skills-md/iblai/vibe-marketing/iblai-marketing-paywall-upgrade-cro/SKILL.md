---
name: iblai-marketing-paywall-upgrade-cro
description: When the user wants to create or optimize in-app paywalls, upgrade screens, upsell modals, or feature gates. Also use when the user mentions "paywall," "upgrade screen," "upgrade modal," "upsell," "feature gate," "convert free to paid," "freemium conversion," "trial expiration screen," "limit reached screen," "plan upgrade prompt," "in-app pricing," "free users won't upgrade," "trial to paid conversion," or "how do I get users to pay." Use this for any in-product moment where you're asking users to upgrade. Distinct from public pricing pages (see iblai-marketing-page-cro) — this focuses on in-product upgrade moments where the user has already experienced value. For pricing decisions, see iblai-marketing-pricing-strategy.
globs:
alwaysApply: false
metadata:
  version: 1.1.0
---

# /iblai-marketing-paywall-upgrade-cro

Convert free users to paid (or upgrade users to higher tiers) at moments
when they've experienced enough value to justify the commitment.

## Step 0: Context Check

Read `.agents/product-marketing-context.md` (or `.claude/product-marketing-context.md`
on older setups) first. Only ask for what isn't there.

Identify before recommending:

1. **Upgrade context** — freemium → paid? Trial → paid? Tier upgrade? Feature upsell? Usage limit?
2. **Product model** — what's free? What's behind the paywall? What triggers prompts? Current conversion rate?
3. **User journey** — when does this appear? What have they experienced? What are they trying to do?

---

## Core Principles

1. **Value before ask.** The user should have experienced real value first. Upgrade should feel like a natural next step. Timing: after the aha moment, not before.
2. **Show, don't just tell.** Demonstrate the value of paid features. Preview what they're missing. Make the upgrade feel tangible.
3. **Friction-free path.** Easy to upgrade when ready. Don't make them hunt for pricing.
4. **Respect the no.** Don't trap or pressure. Make it easy to continue free. Keep trust for future conversion.

---

## Trigger Points

### Feature Gates

When the user clicks a paid-only feature:
- Clear explanation of why it's paid
- Show what the feature does
- Quick path to unlock
- Option to continue without

### Usage Limits

When the user hits a limit:
- Clear indication of limit reached
- Show what upgrading provides
- Don't block abruptly

### Trial Expiration

When the trial is ending:
- Early warnings (7, 3, 1 day)
- Clear "what happens" on expiration
- Summarize value received

### Time-Based Prompts

After X days of free use:
- Gentle upgrade reminder
- Highlight unused paid features
- Easy to dismiss

---

## Paywall Screen Components

1. **Headline** — focus on what they get: "Unlock [Feature] to [Benefit]"
2. **Value demonstration** — preview, before/after, "With Pro you could..."
3. **Feature comparison** — highlight key differences, current plan marked
4. **Pricing** — clear, simple, annual vs. monthly options
5. **Social proof** — customer quotes, "X teams use this"
6. **CTA** — specific and value-oriented: "Start Getting [Benefit]"
7. **Escape hatch** — clear "Not now" or "Continue with Free"

---

## Specific Paywall Types

### Feature Lock Paywall

```
[Lock Icon]
This feature is available on Pro

[Feature preview/screenshot]

[Feature name] helps you [benefit]:
• [Capability]
• [Capability]

[Upgrade to Pro - $X/mo]
[Maybe Later]
```

### Usage Limit Paywall

```
You've reached your free limit

[Progress bar at 100%]

Free: 3 projects | Pro: Unlimited

[Upgrade to Pro]  [Delete a project]
```

### Trial Expiration Paywall

```
Your trial ends in 3 days

What you'll lose:
• [Feature used]
• [Data created]

What you've accomplished:
• Created X projects

[Continue with Pro]
[Remind me later]  [Downgrade]
```

---

## Timing and Frequency

### When to Show
- After a value moment, before frustration
- After activation / aha moment
- When hitting genuine limits

### When NOT to Show
- During onboarding (too early)
- Mid-flow
- Repeatedly after dismissal

### Frequency Rules
- Cap per session
- Cool-down after dismiss (days, not hours)
- Track annoyance signals

---

## Upgrade Flow Optimization

### From Paywall to Payment
- Minimize steps
- Keep in-context where possible
- Pre-fill known information

### Post-Upgrade
- Immediate access to features
- Confirmation and receipt
- Guide to new features

---

## A/B Testing

### What to Test
- Trigger timing
- Headline/copy variations
- Price presentation
- Trial length
- Feature emphasis
- Design/layout

### Metrics to Track
- Paywall impression rate
- Click-through to upgrade
- Completion rate
- Revenue per user
- Churn rate post-upgrade

Comprehensive experiments: [references/experiments.md](references/experiments.md).

---

## Anti-Patterns

### Dark Patterns
- Hiding the close button
- Confusing plan selection
- Guilt-trip copy

### Conversion Killers
- Asking before value delivered
- Too-frequent prompts
- Blocking critical flows
- Complicated upgrade process

---

## Task-Specific Questions

1. Current free → paid conversion rate?
2. What triggers upgrade prompts today?
3. What features sit behind the paywall?
4. What's the user's aha moment?
5. Pricing model? (Per seat, usage, flat.)
6. Mobile app, web app, or both?

---

## Related Skills

- **iblai-marketing-churn-prevention**: Cancel flows, save offers, post-upgrade churn
- **iblai-marketing-page-cro**: Public pricing page optimization
- **iblai-marketing-onboarding-cro**: Driving to aha moment before upgrade
- **iblai-marketing-ab-test-setup**: Testing paywall variations
