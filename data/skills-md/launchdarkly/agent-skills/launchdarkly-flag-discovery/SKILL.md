---
name: launchdarkly-flag-discovery
description: "Audit your LaunchDarkly feature flags to understand the landscape, find stale or launched flags, and assess removal readiness. Use when the user asks about flag debt, stale flags, cleanup candidates, flag health, or wants to understand their flag inventory."
license: Apache-2.0
compatibility: Requires the remotely hosted LaunchDarkly MCP server
metadata:
  author: launchdarkly
  version: "1.0.0-experimental"
---

# LaunchDarkly Flag Discovery

You're using a skill that will guide you through auditing and understanding the feature flag landscape in a LaunchDarkly project. Your job is to explore the project, assess the health of its flags, identify what needs attention, and provide actionable recommendations.

## Prerequisites

This skill requires the remotely hosted LaunchDarkly MCP server to be configured in your environment.

**Required MCP tools:**
- `list-flags` — search and browse flags with filtering by state, type, tags
- `get-flag` — get full configuration for a single flag in a specific environment
- `get-flag-status-across-envs` — check a flag's lifecycle status across all environments

**Optional MCP tools (enhance depth):**
- `find-stale-flags` — find flags that are candidates for cleanup, sorted by staleness
- `get-flag-health` — get combined health view for a single flag (merges status + config)
- `check-removal-readiness` — detailed safety check for a specific flag

## Workflow

### Step 1: Understand the Project

Before diving into flag data, establish context:

1. **Identify the project.** Confirm the `projectKey` with the user. If they haven't specified one, ask.
2. **Understand scope.** Ask the user what they're trying to accomplish:
   - Broad audit? ("What's the state of our flags?")
   - Targeted investigation? ("Is this specific flag still needed?")
   - Cleanup planning? ("What flags can we remove?")

### Step 2: Explore the Flag Landscape

Adapt your approach to the user's goal:

**For a broad audit:**
- Use `list-flags` scoped to a critical environment (default to `production`).
- Note the total count — this tells you the scale of the flag surface area.
- Filter by `state` (active, inactive, launched, new) to segment the landscape.
- Filter by `type` (temporary vs permanent) — temporary flags are the primary cleanup targets.

**For cleanup planning:**
- Use `find-stale-flags` — this is the most efficient entry point. It returns a prioritized list of cleanup candidates sorted by staleness, categorized as:
  - `never_requested` — created but never evaluated (possibly abandoned)
  - `inactive_30d` — no SDK evaluations in the specified period
  - `launched_no_changes` — fully rolled out, no recent changes
- Default `inactiveDays` is 30. Increase for conservative cleanup (60, 90) or decrease for aggressive cleanup (7, 14).
- Default `includeOnly` is `temporary`. Set to `all` to include permanent flags.

**For a targeted investigation:**
- Use `get-flag-health` for a single-flag deep dive. It merges status data with configuration context in one call, returning lifecycle state, last-requested timestamp, targeting summary, age, and whether it's temporary.
- Or use `get-flag` for the full configuration including rules, targets, and fallthrough details.

### Step 3: Assess Flag Health

For flags that need deeper investigation, assess health signals. See [Flag Health Signals](references/flag-health-signals.md) for the full interpretation guide.

Key signals to evaluate:

| Signal | What it tells you |
|--------|-------------------|
| **Lifecycle state** | Where the flag is in its journey (new → active → launched → inactive) |
| **Last requested** | When an SDK last evaluated this flag — staleness indicator |
| **Targeting complexity** | Number of rules and targets — removal complexity indicator |
| **Cross-environment consistency** | Whether the flag behaves the same everywhere |
| **Flag age + temporary status** | Old temporary flags are strong cleanup candidates |

Use `get-flag-status-across-envs` to check if a flag is consistent across environments. A flag inactive in production but active in staging tells a different story than one inactive everywhere.

### Step 4: Categorize and Prioritize

Group flags into actionable categories:

1. **Ready to remove** — Inactive everywhere, temporary, no dependencies. Direct the user to the [flag cleanup skill](../launchdarkly-flag-cleanup/SKILL.md) for code removal.
2. **Likely safe, needs verification** — Launched (fully rolled out), no rule changes recently. The user should confirm the rollout is intentionally complete.
3. **Needs investigation** — Active in some environments but not others, or has complex targeting. Don't recommend action without more context.
4. **Leave alone** — Active flags doing their job, or permanent flags that are intentionally long-lived.

### Step 5: Assess Removal Readiness (When Applicable)

If the user wants to know whether a specific flag can be removed, use `check-removal-readiness`. This tool orchestrates multiple API calls in parallel and returns a structured verdict:

- **`safe`** — No blockers or warnings. Proceed with cleanup.
- **`caution`** — Warnings exist (code references, expiring targets, permanent flag type). Present and let the user decide.
- **`blocked`** — Hard blockers (dependent flags, active requests, targeting rules). Must resolve first.

See [Removal Readiness Checklist](references/removal-readiness-checklist.md) for the full details on interpreting each signal.

### Step 6: Present Findings

Structure your response based on what the user asked for:

**For audits:** Lead with a summary (total flags, breakdown by state and type), then highlight what needs attention, then provide specific recommendations.

**For specific flags:** Lead with the verdict (healthy / needs attention / ready to remove), then support it with the signals you found.

**For cleanup planning:** Lead with the count of cleanup candidates, prioritize by confidence (safest removals first), and link to the cleanup workflow for execution.

## Important Context

- **"Launched" means fully rolled out** — targeting is on, a single variation is served to everyone, and no changes have been made recently. It doesn't mean "recently deployed."
- **"Inactive" doesn't always mean safe to remove.** The flag might be used in code that hasn't shipped yet, or referenced as a prerequisite by another flag.
- **Permanent flags can be inactive on purpose.** Some flags are designed to be dormant until needed (kill switches, emergency toggles). Don't automatically flag these for cleanup.
- **Weights are scaled by 1000 in the API.** A weight of `60000` means 60%. Always convert to human-readable percentages.
- **This skill is for discovery, not action.** If the user wants to remove a flag from code, direct them to the [flag cleanup skill](../launchdarkly-flag-cleanup/SKILL.md). If they want to change targeting, direct them to the [flag targeting skill](../launchdarkly-flag-targeting/SKILL.md).

## References

- [Flag Health Signals](references/flag-health-signals.md) — How to interpret lifecycle states, staleness, and health data
- [Removal Readiness Checklist](references/removal-readiness-checklist.md) — Full safety assessment before recommending flag removal
