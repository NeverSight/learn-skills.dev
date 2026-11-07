---
name: troubleshoot-ngrok
description: Diagnose and fix common ngrok errors and connection problems - offline endpoints (ERR_NGROK_3200), agent authentication and connection failures, upstream/tunnel connection refused, and Traffic Policy errors. Reads the error code and explains the specific cause and fix. Use when an ngrok URL returns an error, a tunnel won't come up, or the agent reports a connection problem. Use when the user says "ngrok says endpoint offline", "ERR_NGROK_3200", "my tunnel isn't working", "why is my ngrok URL down", or pastes an ngrok error code.
license: MIT
metadata:
  author: ngrok
  version: "1.0"
  category: troubleshooting
  surface: job
compatibility: Requires ngrok CLI installed and authenticated.
---

# Troubleshoot ngrok

Diagnose a failing ngrok endpoint or agent. Work from the error code when there is one - `references/error-codes.md` has the high-frequency codes with causes and fixes.

## First: get the code

ngrok errors carry an `ERR_NGROK_####` code, on the error page or in agent output. Get it - it points straight at the cause. If there's no code, use the symptom sections below.

## High-frequency codes

**ERR_NGROK_3200 - endpoint offline.** The URL is being visited but no agent is currently serving it. Either the agent isn't running, or it's running a *different* endpoint/URL than the one being visited. Check the agent is up, the URL matches, and (for reserved domains) that the agent is bound to that domain. This is by far the most common one, and it's often shown to *visitors* of a tunnel whose owner's agent has stopped.

**ERR_NGROK_8012 - upstream connection refused.** The agent is up and reachable, but nothing is listening on the local port/address it forwards to, or the upstream refused. Confirm the local service is running on exactly the port the endpoint forwards to.

**Auth failures (agent won't start / authentication required).** Missing or invalid authtoken. Go to `ngrok-setup` for the token flow.

**Traffic Policy errors.** A malformed policy, an unknown action, or a bad expression. Validate the YAML against `ngrok-engine`; check the action names and config keys match; check CEL expressions.

Others (agent session limits, TLS, DNS/reserved-domain issues) are in `references/error-codes.md`.

## By symptom (no code)

- **URL loads an ngrok error page** -> almost always 3200 (offline) or an upstream error (8012). Check agent running, then local service running.
- **Agent exits immediately on start** -> auth (see `ngrok-setup`) or a config-file parse error.
- **Works locally, 400/rejected through the URL** -> host-header or allowed-hosts mismatch (common with dev servers and internal forwarding); see the host-header notes in `expose-localhost/references/TROUBLESHOOTING.md` / `run-mcp-gateway`.
- **Policy has no effect** -> it may not be attached to the endpoint being hit; confirm attachment per the surface skill.

## Notes for agents

- Diagnose from the code first; don't guess when the code names the cause.
- 3200 shown to a visitor (not the developer) usually just means the owner's agent stopped - there may be nothing for *this* user to fix.
- If the cause is auth or policy, hand to `ngrok-setup` or `ngrok-engine` rather than duplicating them here.
