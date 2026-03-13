---
name: managing-project-customizations
description: Use when initializing or refreshing project-specific WebdriverIO context so other skills can reuse cached configuration, conventions, and environment details with lower token and execution cost.
---

# Managing Project Customizations

Build and maintain a project context cache for all WebdriverIO skills.

This skill is the project bootstrap and refresh layer. It scans the current project, writes reference files, and keeps them current so other skills can load project details quickly instead of rediscovering them every session.

## When to Use

- First use of the WebdriverIO skill set in a project.
- On-demand refresh after significant test/config changes.
- End of orchestrator sessions when project context changed.
- When other skills report missing or stale project context.

## When Not to Use

- You only need to edit a single test and context is already fresh.
- You need test implementation logic (use `writing-webdriverio-code`).
- You need only test scaffolding (use `creating-test-structure`).

## Output Files (Project Cache)

Write/update these files under `.webdriverio-skills/` in the target project:

- `.webdriverio-skills/project-context.json`
- `.webdriverio-skills/project-context.md`
- `.webdriverio-skills/custom-rules.md` (team-maintained overrides)
- `.webdriverio-skills/health-recommendations.md`

Create `.webdriverio-skills/custom-rules.md` from this skill's template if missing.

## Required Data to Capture

- WDIO configuration files (`wdio.conf.*`, per-env configs, suite splits)
- Reporters and reporter output details
- Services and service-specific behavior
- Coding standards and conventions (naming, structure, style)
- Linting rules and test-related lint constraints
- NPM scripts related to test execution and debugging
- Custom functionality (custom commands, API interfaces, shared helpers)
- Relevant environment variables and toggles
- Server/environment targets (local/dev/staging/prod)

## Scanning Workflow

1. Discover test-related config files (`wdio.conf.*`, eslint, ts/js config, package scripts).
2. Extract reporter/service/configuration details.
3. Discover custom commands, shared helpers, and API utilities.
4. Extract relevant env var names from config and docs (never store secrets/values).
5. Map server targets and their intended usage from scripts/config.
6. Write structured + human-readable context files.
7. Run capability checks and produce recommendations.

## Capability Checks and Recommendations

Always check for features that improve skill effectiveness:

- JSON reporter support for easier machine parsing of results.
- Failure artifact capture (HTML snapshot and/or screenshot) in failure hooks.

If missing, add a recommendation entry in `.webdriverio-skills/health-recommendations.md` with:
- what is missing
- why it matters
- suggested implementation direction

Reference for failure artifacts:
- https://github.com/webdriverio/webdriverio/issues/2190#issuecomment-2245595191

## Update Policy

- Treat cache as stale if WDIO config, reporters, services, scripts, linting, or custom command files changed.
- Refresh on explicit user request.
- Refresh when orchestrator indicates project state changed during a session.
- Update only changed sections when possible; perform full refresh when core config changed.

## Custom Rules Support

Teams can tune behavior via `.webdriverio-skills/custom-rules.md`.

This file can define:
- preferred selectors and anti-patterns
- naming conventions
- required test hooks/setup patterns
- environment constraints
- mandatory scripts or checks

Other skills should read this file first and treat it as project override guidance.

## Downstream Skill Contract

All WebdriverIO skills should:

1. Attempt to read `.webdriverio-skills/project-context.*` and `.webdriverio-skills/custom-rules.md` first.
2. Attempt to read `references/website-analysis/<target>/website-analysis.*` when route/component context is relevant.
3. Treat `custom-rules.md` as team override guidance.
4. Request a refresh via `managing-project-customizations` when cache data appears stale.

### Target Resolution Rule

For `references/website-analysis/<target>/...`, downstream skills should resolve `<target>` to the lowercase site host (from URL or `baseUrl`), with `unknown-target` as fallback.

## Data Safety Rules

- Never store secret values (tokens, passwords, credentials).
- Store env var names and usage notes only.
- Redact sensitive command arguments in generated context docs.

## Quick Reference

| Artifact | Purpose |
|---|---|
| `project-context.json` | Fast machine-readable project context |
| `project-context.md` | Human summary for quick understanding |
| `custom-rules.md` | Team-specific overrides and conventions |
| `health-recommendations.md` | Suggested project improvements |

## Common Mistakes

- Storing secret env values in reference files.
- Updating context only once and never refreshing.
- Ignoring custom-rules overrides.
- Recording recommendations without actionable guidance.

## Minimal JSON Shape

```json
{
  "updatedAt": "ISO-8601",
  "wdioConfigs": [],
  "reporters": [],
  "services": [],
  "linting": {},
  "testScripts": {},
  "customCommands": [],
  "apiInterfaces": [],
  "envVars": [],
  "servers": [],
  "notes": []
}
```

Done means context files are current, recommendations are updated, and downstream skills can load project-specific behavior without a full rescan.
