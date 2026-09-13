---
name: openclaw-browser-setup
description: Troubleshoot and operate OpenClaw browser on local or remote gateways. Use when Codex needs to enable the bundled browser plugin, resolve `pairing required` or device approval errors, choose between the managed `openclaw` profile and the attached `user` profile, handle Linux headless or Chrome CDP startup failures, or prove browser control with `profiles`, `start`, `open`, `snapshot`, and `screenshot`.
---

# OpenClaw Browser Setup

## Overview

Get OpenClaw browser working with the shortest reliable path, then prove it with a real page interaction instead of stopping at config inspection.

Read [references/official-docs.md](references/official-docs.md) when you need the official passages behind a fix.

## Choose The Target

Decide whether the user means the local gateway or a remote gateway before changing anything.

Run:

```bash
openclaw gateway status --json
openclaw config get gateway.mode
openclaw config get gateway.remote.url
```

Use `--url` explicitly when the user has both a local and VPS instance and the target is ambiguous.

## Fast Path

Try the documented local flow first:

```bash
openclaw browser profiles
openclaw browser --browser-profile openclaw start
openclaw browser --browser-profile openclaw open https://example.com
openclaw browser --browser-profile openclaw snapshot
```

Treat a successful `open` plus `snapshot` or `screenshot` as the proof that browser control works. `status` can lag or look stale.

## Fix Pairing And Auth First

If browser commands fail with `pairing required` or `PAIRING_REQUIRED`, fix device approval before debugging browser internals.

Run:

```bash
openclaw devices list
openclaw devices approve <requestId>
```

If the connection retried with broader scopes or changed auth details, list devices again before approval because the pending `requestId` may have changed.

If shared-token auth matters, inspect the configured token instead of guessing:

```bash
openclaw config get gateway.auth.token
```

## Fix Missing Browser Command Or Plugin State

If `openclaw browser` is missing, or the agent reports the browser tool as unavailable, check plugin loading before touching browser profiles.

Inspect:

```bash
openclaw config get plugins.allow
openclaw config get plugins.entries.browser.enabled
openclaw config get browser.enabled
```

When `plugins.allow` is present, make sure it includes `browser`. If you change browser plugin or browser config, restart the gateway:

```bash
openclaw gateway restart
```

## Pick The Right Profile

Use:

- `openclaw` for the isolated managed browser.
- `user` for the existing signed-in Chrome session when login state matters and the user is present to approve attach prompts.

Do not default to `user` on servers, containers, or headless Linux hosts.

## Handle Linux Headless And CDP Startup Failures

If `openclaw browser start` fails, inspect logs before changing config:

```bash
openclaw logs --limit 120 --plain
openclaw browser status
```

Common fix on Linux servers without a desktop session:

```bash
openclaw config set browser.headless true
openclaw gateway restart
openclaw browser --browser-profile openclaw start
```

If the configured browser binary is wrong or missing, inspect what is installed:

```bash
which google-chrome-stable
google-chrome-stable --version
which chromium-browser
```

If logs mention snap Chromium or CDP launch failures, read [references/official-docs.md](references/official-docs.md) for the official `executablePath`, `attachOnly`, and manual-CDP guidance.

## Verify With Real Actions

After startup succeeds, always execute a real loop:

```bash
openclaw browser --browser-profile openclaw open https://example.com
openclaw browser --browser-profile openclaw snapshot
openclaw browser --browser-profile openclaw screenshot
openclaw browser --browser-profile openclaw tabs
```

If `open` succeeds but `tabs` looks odd, keep following the live page actions. The browser path is good once `snapshot` or `screenshot` returns useful page state.

## Escalate Methodically

When the first pass fails, use this order:

1. Confirm the target gateway.
2. Resolve `pairing required` with `openclaw devices list` and `approve`.
3. Confirm the browser plugin is loaded.
4. Retry the managed `openclaw` profile.
5. Switch to headless on Linux hosts without a GUI.
6. Check browser binary path or snap/attach-only cases.
7. Only then try `user` or a remote CDP profile.
