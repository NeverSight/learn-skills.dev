---
name: openclaw-droidclaw-bridge
description: Integrate OpenClaw with DroidClaw for Android device automation using hosted or self-hosted deployments. Use when users ask to configure DroidClaw Android API key/server link fields, self-host DroidClaw, connect devices over Tailscale, run/stop DroidClaw goals, inspect device sessions/steps, or expose DroidClaw control APIs to OpenClaw.
---

# OpenClaw DroidClaw Bridge

Use this skill to run DroidClaw reliably from OpenClaw with explicit health checks, authenticated control calls, and repeatable troubleshooting.

## Default Operating Mode

Prefer on-demand runtime by default:
1. `scripts/droidclaw_service.sh ensure`
2. `scripts/droidclaw_preflight.sh`
3. `scripts/droidclaw_ctl.py ...`

Only keep DroidClaw always-on when the user asks for continuous availability.

## Lifecycle Commands

Run from this skill folder.

```bash
# one-time setup (clone/update, bun install, env templates, DB push attempt)
./scripts/droidclaw_service.sh setup

# start local server (and optionally web UI)
./scripts/droidclaw_service.sh start
./scripts/droidclaw_service.sh start --with-web

# start only if not healthy
./scripts/droidclaw_service.sh ensure

# inspect process and health
./scripts/droidclaw_service.sh status

# stop managed background processes
./scripts/droidclaw_service.sh stop
```

## Control API Toolkit

Use `droidclaw_ctl.py` for consistent JSON output.

```bash
# health
./scripts/droidclaw_ctl.py health

# list devices visible to configured user
./scripts/droidclaw_ctl.py list-devices

# start/stop a goal
./scripts/droidclaw_ctl.py run-goal <device_id> "Open WhatsApp and send hello"
./scripts/droidclaw_ctl.py stop-goal <device_id>

# inspect history
./scripts/droidclaw_ctl.py list-sessions <device_id>
./scripts/droidclaw_ctl.py list-steps <device_id> <session_id>
```

Use `--compact` when output feeds another script.

## Required Env for Authenticated Control

Set before `list-devices`, `run-goal`, and session inspection:
- `DROIDCLAW_BASE_URL` (default `http://127.0.0.1:8080`)
- `DROIDCLAW_INTERNAL_SECRET`
- `DROIDCLAW_USER_ID`

Control endpoints rely on internal headers (`x-internal-secret`, `x-internal-user-id`) instead of browser-cookie auth.

## Android Field Rules

When configuring Android app onboarding/settings:
- API Key: DroidClaw device API key from dashboard API Keys.
- Server URL/Link: hosted `wss://tunnel.droidclaw.ai` or self-host base URL.
- Do not paste OpenAI/Groq provider keys into Android API Key.

## Troubleshooting Order

1. `./scripts/droidclaw_service.sh status`
2. `./scripts/droidclaw_ctl.py health`
3. `./scripts/droidclaw_preflight.sh`
4. `./scripts/droidclaw_ctl.py list-devices`
5. If `401`: fix internal secret/user id.
6. If `404 device not connected`: reconnect Android to same server/account.
7. If `409 agent already running`: stop goal or wait.

## References

- `references/droidclaw-integration.md`
- `references/android-fields.md`
- `references/runtime-modes.md`
