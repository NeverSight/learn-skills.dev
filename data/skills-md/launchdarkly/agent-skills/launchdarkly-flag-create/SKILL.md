---
name: launchdarkly-flag-create
description: "Create and configure LaunchDarkly feature flags in a way that fits the existing codebase. Use when the user wants to create a new flag, wrap code in a flag, add a feature toggle, or set up an experiment. Guides exploration of existing patterns before creating."
license: Apache-2.0
compatibility: Requires the remotely hosted LaunchDarkly MCP server
metadata:
  author: launchdarkly
  version: "1.0.0-experimental"
---

# LaunchDarkly Flag Create & Configure

You're using a skill that will guide you through introducing a new feature flag into a codebase. Your job is to explore how flags are already used in this codebase, create the flag in LaunchDarkly in a way that fits, add the evaluation code matching existing patterns, and verify everything is wired up correctly.

## Prerequisites

This skill requires the remotely hosted LaunchDarkly MCP server to be configured in your environment.

**Required MCP tools:**
- `create-flag` — create a new feature flag in a project
- `get-flag` — verify the flag was created correctly

**Optional MCP tools (enhance workflow):**
- `list-flags` — browse existing flags to understand naming conventions and tags
- `update-flag-settings` — update flag metadata (name, description, tags, temporary/permanent status)

## Workflow

### Step 1: Explore the Codebase

Before creating anything, understand how this codebase uses feature flags.

1. **Find the SDK.** Search for LaunchDarkly SDK imports or initialization:
   - Look for `launchdarkly`, `ldclient`, `ld-client`, `LDClient` in imports
   - Check `package.json`, `requirements.txt`, `go.mod`, `Gemfile`, or equivalent for the SDK dependency
   - Identify which SDK is in use (server-side Node, React, Python, Go, Java, etc.)

2. **Find existing flag evaluations.** Search for variation calls to understand the patterns this codebase uses:
   - Direct SDK calls: `variation()`, `boolVariation()`, `useFlags()`, etc.
   - Wrapper patterns: Does this codebase abstract flags behind a service or utility?
   - Constant definitions: Are flag keys defined as constants somewhere?
   - See [SDK Evaluation Patterns](references/sdk-evaluation-patterns.md) for patterns by language

3. **Understand conventions.** Look at existing flags to learn:
   - **Naming convention**: Are keys `kebab-case`, `snake_case`, `camelCase`?
   - **Organization**: Are flag keys co-located with features, or centralized in a constants file?
   - **Default values**: What defaults do existing evaluations use?
   - **Context/user construction**: How does this codebase build the user/context object passed to the SDK?

4. **Check LaunchDarkly project conventions.** Optionally use `list-flags` to see existing flags:
   - What tags are commonly used?
   - Are flags marked as temporary or permanent?
   - What naming patterns exist in the project?

### Step 2: Determine the Right Flag Type

Based on what the user needs, choose the appropriate flag configuration. See [Flag Types and Patterns](references/flag-types.md) for the full guide.

**Quick decision:**

| User intent | Flag kind | Variations |
|-------------|-----------|------------|
| "Toggle a feature on/off" | `boolean` | `true` / `false` |
| "Gradually roll out a feature" | `boolean` | `true` / `false` |
| "A/B test between options" | `multivariate` (string) | User-defined values |
| "Configure a numeric threshold" | `multivariate` (number) | User-defined values |
| "Serve different config objects" | `multivariate` (JSON) | User-defined values |

**Defaults to apply:**
- Set `temporary: true` unless the user explicitly says this is a permanent/long-lived flag. Most flags are release flags that should eventually be cleaned up.
- Generate a `key` from the name if not provided (e.g., "New Checkout Flow" → `new-checkout-flow`), but match the codebase's naming convention if one exists.
- Suggest relevant tags based on the feature area, team, or context the user mentions.

### Step 3: Create the Flag in LaunchDarkly

Use `create-flag` with the configuration determined in Step 2.

After creation:
- The flag is created with **targeting OFF** in all environments.
- The flag serves the `offVariation` to everyone until targeting is turned on.
- Remind the user they'll need to use the [flag targeting skill](../launchdarkly-flag-targeting/SKILL.md) to toggle it on and optionally set up rollout rules.

### Step 4: Add Flag Evaluation to Code

Now add the code to evaluate the flag, **matching the patterns you found in Step 1**.

1. **Use the same SDK patterns** the codebase already uses. If there's a wrapper, use the wrapper. If there are constants, add the new key to the constants file.
2. **Use an appropriate default value.** The default (fallback) value in code should be the "safe" behavior — typically the existing behavior before the flag. This ensures the feature stays off if the SDK can't reach LaunchDarkly.
3. **Add the conditional logic.** Wrap the new behavior in a flag check.
4. **Handle both branches.** Make sure the code path for each variation is clear and complete.

See [SDK Evaluation Patterns](references/sdk-evaluation-patterns.md) for implementation examples by language and framework.

### Step 5: Verify

Confirm the flag is properly set up:

1. **Code compiles/passes linting.** Run the project's build or lint step.
2. **Flag exists in LaunchDarkly.** Use `get-flag` to confirm it was created with the right configuration.
3. **Both code paths work.** The flag-off path preserves existing behavior; the flag-on path enables the new feature.
4. **Default value is safe.** If LaunchDarkly is unreachable, the code falls back to the default — make sure that's the existing/safe behavior.

## Updating Flag Settings

If the user wants to change flag metadata (not targeting), use `update-flag-settings`. Supported changes:

| Change | Instruction |
|--------|-------------|
| Rename | `{kind: "updateName", value: "New Name"}` |
| Update description | `{kind: "updateDescription", value: "New description"}` |
| Add tags | `{kind: "addTags", values: ["tag1", "tag2"]}` |
| Remove tags | `{kind: "removeTags", values: ["old-tag"]}` |
| Mark as temporary | `{kind: "markTemporary"}` |
| Mark as permanent | `{kind: "markPermanent"}` |

Multiple instructions can be batched in a single call. These changes are project-wide, not environment-specific.

**Important:** Metadata updates (above) are separate from targeting changes (toggle, rollout, rules). If the user wants to change who sees what, direct them to the [flag targeting skill](../launchdarkly-flag-targeting/SKILL.md).

## Important Context

- **Flag keys are immutable.** Once created, a flag's key cannot be changed. Choose carefully.
- **Flags start OFF.** Creation never enables a flag. This is a safety feature.
- **The default value in code is your safety net.** It's what gets served when the SDK can't connect to LaunchDarkly. Always use the "safe" / existing behavior as the default.
- **Follow existing codebase conventions.** The most common mistake is introducing a flag pattern that doesn't match what the team already does. Step 1 exists to prevent this.

## References

- [Flag Types and Patterns](references/flag-types.md) — Boolean vs multivariate, naming conventions, configuration best practices
- [SDK Evaluation Patterns](references/sdk-evaluation-patterns.md) — How to evaluate flags in each SDK, including common wrapper patterns
