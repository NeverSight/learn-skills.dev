---
name: feature-flag-management
description: Feature flag lifecycle management -- safe feature toggling, gradual rollouts, A/B testing patterns, flag cleanup strategies, and technical debt prevention. Covers LaunchDarkly, Unleash, OpenFeature, and custom implementations.
version: 2.0.0
category: DevOps
agents: [developer, devops, qa]
tags:
  [
    feature-flags,
    rollouts,
    a-b-testing,
    toggles,
    launchdarkly,
    openfeature,
    trunk-based-development,
  ]
model: sonnet
invoked_by: both
user_invocable: true
tools: [Read, Write, Edit, Bash, Glob, Grep, WebFetch]
best_practices:
  - Define a clear lifecycle for every flag (create, enable, rollout, permanent, cleanup)
  - Use typed flag values with defaults that match the safe/existing behavior
  - Clean up flags within 30 days of full rollout to prevent technical debt
  - Never nest feature flags more than 2 levels deep
  - Always include kill-switch capability for new features behind flags
error_handling: graceful
streaming: supported
verified: true
lastVerifiedAt: '2026-03-01'
---

# Feature Flag Management Skill

<identity>
Feature flag lifecycle specialist covering safe feature toggling, gradual rollouts, A/B testing patterns, and flag cleanup to prevent technical debt. Enforces disciplined flag hygiene across the full lifecycle from creation through retirement.
</identity>

<capabilities>
- Design feature flag architecture with proper categorization (release, experiment, ops, permission)
- Implement gradual rollout strategies (percentage, user-segment, canary, ring-based)
- Configure A/B testing with feature flags and metrics collection
- Plan flag cleanup workflows to prevent stale flag accumulation
- Integrate with flag platforms (LaunchDarkly, Unleash, Flipt, OpenFeature SDK)
- Implement custom feature flag systems for projects without external platforms
- Set up flag-aware testing strategies (all flag combinations)
- Monitor flag evaluation performance and stale flag detection
</capabilities>

## Overview

Feature flags decouple deployment from release, enabling trunk-based development, safe rollouts, and instant rollbacks. However, undisciplined flag usage creates exponential code path complexity, stale flags, and untested combinations. This skill enforces a lifecycle-driven approach: every flag has a type, an owner, a target date, and a cleanup plan from day one.

## When to Use

- When implementing trunk-based development with continuous deployment
- When rolling out features gradually to reduce risk
- When setting up A/B testing infrastructure
- When auditing existing codebases for stale or orphaned feature flags
- When choosing between feature flag platforms
- When implementing kill-switches for critical features

## Iron Laws

1. **ALWAYS** assign an owner and expiration date to every feature flag -- orphaned flags without owners accumulate indefinitely and become permanent tech debt.
2. **NEVER** nest feature flags more than 2 levels deep -- combinatorial explosion makes testing impossible (2 flags = 4 states, 5 flags = 32 states, 10 flags = 1024 states).
3. **ALWAYS** default flag values to the existing/safe behavior -- if the flag system fails, the application should behave as it did before the flag was added.
4. **NEVER** use feature flags as a substitute for configuration management -- flags are temporary toggles for release control, not permanent application settings.
5. **ALWAYS** clean up flags within 30 days of full rollout -- stale flags in code increase cognitive load, slow onboarding, and hide dead code paths.

## Anti-Patterns

| Anti-Pattern                                       | Why It Fails                                                                 | Correct Approach                                                                      |
| -------------------------------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Creating flags without expiration dates or owners  | Flags become permanent; nobody knows if they can be removed                  | Require owner and target-date fields at creation time; alert on overdue flags         |
| Nesting 3+ flags in conditional logic              | Testing requires covering all combinations; bugs hide in untested paths      | Limit nesting to 2 levels; combine related flags into a single multi-valued flag      |
| Defaulting new features to ON when flag is missing | Flag system outage enables untested features for all users                   | Default to OFF (existing behavior); explicitly enable after validation                |
| Using flags for permanent configuration            | Config changes require code deploys to remove; defeats the purpose of config | Use environment variables or config files for permanent settings; flags are temporary |
| Testing only with flags ON or only with flags OFF  | Misses interaction bugs between flag states                                  | Test both states; add flag-combination matrix to CI for critical flags                |

## Workflow

### Step 1: Flag Classification

Classify every flag before creation:

| Type           | Purpose                                   | Lifetime                | Example                      |
| -------------- | ----------------------------------------- | ----------------------- | ---------------------------- |
| **Release**    | Control feature visibility during rollout | Days to weeks           | `enable_new_checkout`        |
| **Experiment** | A/B test with metrics collection          | Weeks to months         | `experiment_pricing_page_v2` |
| **Ops**        | Kill-switch for operational control       | Permanent (with review) | `circuit_breaker_payments`   |
| **Permission** | User/role-based access control            | Permanent               | `enable_admin_dashboard`     |

### Step 2: Implementation Pattern

```typescript
// OpenFeature SDK pattern (vendor-neutral)
import { OpenFeature } from '@openfeature/server-sdk';

const client = OpenFeature.getClient();

// Typed flag evaluation with safe default
const showNewUI = await client.getBooleanValue(
  'enable_new_checkout_ui',
  false, // safe default: existing behavior
  { targetingKey: user.id, attributes: { plan: user.plan } }
);

if (showNewUI) {
  renderNewCheckout();
} else {
  renderLegacyCheckout();
}
```

### Step 3: Gradual Rollout Strategy

```
Phase 1: Internal (0-1 day)
  - Enable for development team
  - Verify in production environment

Phase 2: Canary (1-3 days)
  - Enable for 1% of users
  - Monitor error rates, latency, business metrics

Phase 3: Controlled Rollout (3-7 days)
  - Ramp: 5% -> 10% -> 25% -> 50% -> 100%
  - Hold at each stage for minimum 24 hours
  - Define rollback criteria before advancing

Phase 4: Cleanup (within 30 days of 100%)
  - Remove flag checks from code
  - Remove flag from platform
  - Update documentation
```

### Step 4: Flag-Aware Testing

```typescript
// Test both flag states in CI
describe('Checkout Flow', () => {
  describe('with new_checkout_ui enabled', () => {
    beforeEach(() => {
      flagProvider.setOverride('enable_new_checkout_ui', true);
    });

    it('should render new checkout components', () => {
      // test new path
    });
  });

  describe('with new_checkout_ui disabled', () => {
    beforeEach(() => {
      flagProvider.setOverride('enable_new_checkout_ui', false);
    });

    it('should render legacy checkout components', () => {
      // test legacy path
    });
  });
});
```

### Step 5: Stale Flag Detection

```bash
# Find flags older than 30 days that are fully rolled out
# Custom script pattern for codebase scanning
grep -rn 'isEnabled\|getBooleanValue\|getFlag' src/ | \
  awk -F"'" '{print $2}' | \
  sort -u > active_flags.txt

# Compare against flag platform inventory
# Flag any that are 100% enabled for > 30 days
```

### Step 6: Cleanup Checklist

For each flag being retired:

- [ ] Remove all flag evaluation calls from code
- [ ] Remove unused code path (the one not selected)
- [ ] Remove flag from platform/configuration
- [ ] Remove flag from test overrides
- [ ] Update documentation referencing the flag
- [ ] Verify no other flags depend on this flag
- [ ] Deploy and verify behavior matches full-rollout state

## Complementary Skills

| Skill                       | Relationship                                       |
| --------------------------- | -------------------------------------------------- |
| `tdd`                       | Test-driven development for flag-guarded features  |
| `ci-cd-implementation-rule` | CI/CD pipeline integration with flag-aware deploys |
| `qa-workflow`               | QA validation across flag combinations             |
| `proactive-audit`           | Audit for stale or orphaned flags in codebase      |

## Memory Protocol (MANDATORY)

**Before starting:**

Read `.claude/context/memory/learnings.md` for prior feature flag patterns and platform-specific decisions.

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: Your context may reset. If it's not in memory, it didn't happen.
