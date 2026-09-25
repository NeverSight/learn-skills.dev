---
name: agent-browser-jev
description: Use Jev to perform short browser tasks through agent-browser, including contextual clicks, forms, dialogs and searches. Give the helper an intent instead of making each UI decision yourself; it returns observations and completion or handoff.
metadata:
  version: "0.2.0"
---

# Agent Browser Jev

Use Jev for a short browser task when interpreting the page would otherwise require repeated caller decisions. The helper observes the page, offers its actual controls to Jev, executes the selected action through agent-browser, and returns evidence. Prefer a direct browser command when the current control is already known.

## Setup

Resolve script paths relative to this skill directory. Run `node scripts/setup.mjs` once to install dependencies and configure the OpenRouter key. Setup reuses agent-browser from PATH or installs a local copy if absent. Preserve the user's chosen fork: pass `--binary /path/to/agent-browser` when needed. For subsequent direct browser commands, resolve its path with `configuredBrowser()` from `scripts/config.mjs`; do not print the raw configuration file, which may contain the key.

If no saved key or `OPENROUTER_API_KEY` exists, setup prompts in the terminal without echoing the key. Direct the user to that prompt; never ask them to paste a secret into chat. A saved key is stored outside the project with owner-only file permissions. Environment credentials take precedence. See the [README](README.md) for installation and key links.

## Run

1. Use agent-browser to open the website and authenticate with the existing credential provider. Continue in the user's chosen session; preserve project-specific account binding and permissions.
2. Invoke the bundled helper with the authorized intent, existing session and exact non-secret fill values:

   ```sh
   node /path/to/skill/scripts/run.mjs --session current-session \
     --intent "Fill Subject with the supplied subject; leave the form as a draft" \
     --value 'subject=Delivery question'
   ```

   Use `--binary` for a selected fork. No task file or custom policy is required. The default offers every supported observed click/fill and passes visible page text to Jev. This does not add authority beyond the user's task. Reuse any existing project permissions/redaction via `--policy`; see [references/usage.md](references/usage.md). Do not build a new policy module or screen parser for an ordinary task just to call the helper.
3. Review the summary and evidence path. `reported_complete` is Jev's assessment, so confirm the final outcome as appropriate to the task. On handoff or limits, continue in the same caller. An uncertain action may already have happened: observe before repeating it.

Keep credentials and OTPs with the browser's authentication provider, outside model input. Keep the browser session exclusive during a call. Other processes or human activity can change a page between observation and gesture; the in-process lock cannot prevent that.

The defaults are 8 actions, 16 decisions and 60 seconds. Clicks, literal fills and brief waits are supported. Use ordinary agent-browser operations for navigation, login, uploads and downloads. The JavaScript API and custom policy remain available for application integrations.

## Validation

Run `npm test` for offline regressions. `npm run benchmark -- --output /absolute/path/to/new-report.json` runs fresh local fixtures with the real browser and Jev, makes billable model calls, and records every trial including failures. `npm run benchmark:codex -- --output /absolute/path/to/new-report.json` compares actual Codex sessions using direct agent-browser versus the helper. See [references/benchmarks.md](references/benchmarks.md) for measurements and reproduction.
