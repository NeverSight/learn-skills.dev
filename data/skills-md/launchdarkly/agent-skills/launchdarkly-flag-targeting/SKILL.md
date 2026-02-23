---
name: launchdarkly-flag-targeting
description: "Control LaunchDarkly feature flag targeting including toggling flags on/off, percentage rollouts, targeting rules, individual targets, and copying flag configurations between environments. Use when the user wants to change who sees a flag, roll out to a percentage, add targeting rules, or promote config between environments."
license: Apache-2.0
compatibility: Requires the remotely hosted LaunchDarkly MCP server
metadata:
  author: launchdarkly
  version: "1.0.0-experimental"
---

# LaunchDarkly Flag Targeting & Rollout

You're using a skill that will guide you through changing who sees what for a feature flag. Your job is to understand the current state of the flag, figure out the right targeting approach for what the user wants, make the changes safely, and verify the resulting state.

## Prerequisites

This skill requires the remotely hosted LaunchDarkly MCP server to be configured in your environment.

**Required MCP tools:**
- `get-flag` — understand current state before making changes
- `toggle-flag` — turn targeting on or off for a flag in an environment
- `update-rollout` — change the default rule (fallthrough) variation or percentage rollout
- `update-targeting-rules` — add, remove, or modify custom targeting rules
- `update-individual-targets` — add or remove specific users/contexts from individual targeting

**Optional MCP tools:**
- `copy-flag-config` — copy targeting configuration from one environment to another

## Core Concept: Evaluation Order

Before making any targeting changes, understand how LaunchDarkly evaluates flags. This determines what your changes actually do:

1. **Flag is OFF** → Serve the `offVariation` to everyone. Nothing else matters.
2. **Individual targets** → If the context matches a specific target list, serve that variation. Highest priority.
3. **Custom rules** → Evaluate rules top-to-bottom. First matching rule wins.
4. **Default rule (fallthrough)** → If nothing else matched, serve this variation or rollout.

This means: if you add a targeting rule but the flag is OFF, nobody sees the change. If you set a percentage rollout on the default rule but there's an individual target, that targeted user bypasses the rollout.

## Workflow

### Step 1: Understand Current State

Before changing anything, check what's already configured.

1. **Confirm the environment.** "Turn it on" without specifying an environment is ambiguous. Always confirm which environment the user means. Default to asking rather than assuming.
2. **Fetch the flag.** Use `get-flag` with the target environment to see:
   - `on` — Is targeting currently enabled?
   - `fallthrough` — What's the default rule? (variation or percentage rollout)
   - `offVariation` — What serves when the flag is off?
   - `rules` — Any custom targeting rules?
   - `targets` — Any individually targeted users/contexts?
   - `prerequisites` — Any flags this depends on?
3. **Assess complexity.** A flag with no rules and no individual targets is simple. A flag with multiple rules, targets, and prerequisites needs more care.

### Step 2: Determine the Right Approach

Based on what the user wants and what you found, choose the right tool and strategy. See [Targeting Patterns](references/targeting-patterns.md) for the full reference.

**Common scenarios:**

| User wants | Tool | Notes |
|-----------|------|-------|
| "Turn it on" | `toggle-flag` with `on: true` | Simplest change |
| "Turn it off" | `toggle-flag` with `on: false` | Serves offVariation to everyone |
| "Roll out to X%" | `update-rollout` with `rolloutType: "percentage"` | Weights must sum to 100 |
| "Enable for beta users" | `update-targeting-rules` — add a rule with clause | Rules are ANDed within, ORed between |
| "Add specific users" | `update-individual-targets` | Highest priority, overrides all rules |
| "Full rollout" | `update-rollout` with `rolloutType: "variation"` | Serve one variation to everyone |
| "Copy from staging" | `copy-flag-config` | Promote tested config to production |

### Step 3: Run the Safety Checklist

Before applying changes, especially in production, run through the [Safety Checklist](references/safety-checklist.md). The key checks:

1. **Right environment?** Double-check you're targeting the intended environment.
2. **Approval required?** Some environments require approval workflows. If `toggle-flag` or other tools return `requiresApproval: true`, surface this to the user with the approval URL.
3. **Prerequisite flags?** If this flag has prerequisites, they must be met before targeting works as expected.
4. **Rule ordering impact?** If adding rules, consider where they fall in evaluation order. Rules evaluate top-to-bottom, first match wins.
5. **Include a comment.** Always add an audit trail comment, especially for production changes.

### Step 4: Apply Changes

Use the appropriate tool for the change. Key notes:

- **`toggle-flag`**: Specify `on: true` or `on: false`, the `env`, and a `comment`.
- **`update-rollout`**: Use `rolloutType: "percentage"` with human-friendly weights (e.g., 80 for 80%) that sum to 100, or `rolloutType: "variation"` with a `variationIndex`.
- **`update-targeting-rules`**: Instructions support `addRule`, `removeRule`, `updateRuleVariationOrRollout`, `addClauses`, `removeClauses`, `reorderRules`.
- **`update-individual-targets`**: Instructions support `addTargets`, `removeTargets`, `addContextTargets`, `removeContextTargets`, `replaceTargets`.

See [Targeting Patterns](references/targeting-patterns.md) for detailed instruction examples.

### Step 5: Verify

After applying changes, confirm the result:

1. **Fetch the updated flag.** Use `get-flag` again to verify the new state.
2. **Confirm what the user expects.** Describe the resulting targeting in plain language:
   - "The flag is now ON in production, serving `true` to 25% of users and `false` to 75%."
   - "Beta users now see variation A. Everyone else gets the default (variation B)."
3. **Check for side effects.** If there are rules or individual targets, make sure the change interacts correctly with them.

## Important Context

- **`update-rollout` uses human-friendly percentages.** Pass 80 for 80%, not 80000. The tool handles the internal weight conversion.
- **Weights must sum to 100.** For percentage rollouts, the weights across all variations must total exactly 100.
- **Rule ordering matters.** Rules evaluate top-to-bottom. Reordering rules can change behavior without changing any individual rule.
- **Individual targets are highest priority.** They override all rules and the default. Adding someone as an individual target means rules don't apply to them.
- **"Launched" flags are still ON.** A flag with status "launched" is serving a single variation to everyone. If you want to remove the flag, use the [cleanup skill](../launchdarkly-flag-cleanup/SKILL.md), not targeting changes.

## References

- [Targeting Patterns](references/targeting-patterns.md) — Rollout strategies, rule construction, individual targeting, and cross-environment copying
- [Safety Checklist](references/safety-checklist.md) — Pre-change verification, approval workflows, environment awareness
