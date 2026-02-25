---
name: growth-engineering
description: >-
  A/B testing infrastructure, feature flags (LaunchDarkly, Unleash), experimentation platforms, PLG patterns, and funnel optimization. Use when building experimentation systems, implementing feature toggles, or optimizing conversion funnels.
---

# Growth Engineering Skill

Infrastructure and patterns for product-led growth, experimentation, and conversion optimization.

---

## Feature Flag Systems

### Implementation Pattern

```typescript
// lib/feature-flags.ts
import { PostHog } from 'posthog-node';

const posthog = new PostHog(process.env.POSTHOG_API_KEY!);

interface FeatureFlags {
  'new-onboarding-flow': boolean;
  'pricing-experiment': 'control' | 'variant-a' | 'variant-b';
  'ai-suggestions': boolean;
}

export async function getFlag<K extends keyof FeatureFlags>(
  key: K,
  userId: string,
): Promise<FeatureFlags[K]> {
  const value = await posthog.getFeatureFlag(key, userId);
  return value as FeatureFlags[K];
}

// Usage in component
const showNewOnboarding = await getFlag('new-onboarding-flow', user.id);
```

### Feature Flag Best Practices

- Short-lived flags: Remove after experiment concludes (< 2 weeks)
- Long-lived flags: Ops toggles for gradual rollouts, kill switches
- Never nest feature flags (creates exponential complexity)
- Clean up stale flags monthly
- Log flag evaluations for debugging

---

## A/B Testing Infrastructure

### Experiment Design

```typescript
// lib/experiments.ts
interface Experiment {
  id: string;
  name: string;
  variants: {
    id: string;
    weight: number; // 0-100, must sum to 100
  }[];
  targetAudience: {
    percentage: number; // % of users included
    filters?: Record<string, unknown>;
  };
  primaryMetric: string;
  secondaryMetrics: string[];
  minimumSampleSize: number;
  startDate: Date;
  endDate?: Date;
}

// Track experiment exposure
function trackExposure(experimentId: string, variantId: string, userId: string) {
  analytics.capture({
    event: '$experiment_started',
    distinctId: userId,
    properties: {
      $experiment_id: experimentId,
      $variant_id: variantId,
    },
  });
}
```

### Statistical Significance

- Minimum sample size: Calculate before starting (use Evan Miller calculator)
- Don't peek: Set duration upfront, don't stop early on promising results
- Sequential testing: Use if you must check early (adjusts p-values)
- Minimum detectable effect: Define what improvement matters (e.g., 5% lift)

---

## Product-Led Growth Patterns

### Activation Metrics

| Stage | Metric | Example |
|-------|--------|---------|
| Sign up | Registration complete | User creates account |
| Setup | Profile complete | Fills required fields |
| Aha moment | Core value experienced | Creates first project |
| Habit | Repeated engagement | 3 sessions in first week |
| Revenue | Conversion to paid | Subscribes to plan |

### Viral Loops

```typescript
// Referral system pattern
interface Referral {
  referrerId: string;
  referredEmail: string;
  status: 'pending' | 'signed_up' | 'activated' | 'converted';
  rewardGranted: boolean;
}

// Track referral funnel
function trackReferralStep(referralId: string, step: Referral['status']) {
  analytics.capture({
    event: 'referral_step',
    properties: { referralId, step },
  });
}
```

### Conversion Optimization

- Reduce friction: Minimize form fields, enable social login
- Social proof: Show user counts, testimonials, logos
- Urgency: Trial countdown, limited-time offers (use sparingly)
- Value demonstration: Interactive demos, free tier with clear upgrade path
- Personalization: Onboarding flow based on use case selection

---

## Growth Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| Activation rate | Activated / Signed up | > 40% |
| Trial-to-paid | Paid / Trial started | > 15% |
| Net revenue retention | (Start MRR + Expansion - Contraction - Churn) / Start MRR | > 110% |
| Viral coefficient | Invites sent * Conversion rate | > 0.5 |
| Time to value | Median time from signup to aha moment | < 5 min |
| DAU/MAU ratio | Daily active / Monthly active | > 20% |

---

## Experimentation Platforms

| Platform | Type | Best For |
|----------|------|----------|
| PostHog | Self-hosted/cloud | Full-stack, open source |
| LaunchDarkly | Cloud | Feature flags at scale |
| Statsig | Cloud | Auto-stats, warehouse-native |
| Growthbook | Self-hosted/cloud | Open source, Bayesian stats |
| Optimizely | Cloud | Enterprise, multi-channel |

---

## Related Resources

- `~/.claude/skills/product-analytics/SKILL.md` - Analytics and tracking
- `~/.claude/agents/product-analytics-specialist.md` - Analytics agent
- `~/.claude/skills/authentication-patterns/SKILL.md` - Auth for PLG

---

_Measure everything. Experiment constantly. Remove what doesn't work._
