---
name: senpi-entrypoint
description: >-
  Onboard AI agents into the Senpi trading platform on Hyperliquid. Walks
  through account creation, API key setup, MCP server configuration, skill
  discovery, and first-trade guidance. Includes a mandatory skill update check
  that surfaces new or updated skills after onboarding. Use when user says
  "set up Senpi", "get started with Senpi", "connect to Senpi", "install
  Senpi", "onboard to Senpi", or when an agent needs to start trading on
  Hyperliquid via Senpi.
license: Apache-2.0
compatibility: "Node.js, shell, Python 3, OpenClaw (optional — Step 5 cron)"
metadata:
  author: Senpi
  version: "1.2.2"
  platform: senpi
  exchange: hyperliquid
---

# Senpi Agent Entrypoint

Onboard an AI agent into the Senpi trading platform on Hyperliquid via
modular skills: account setup, skill discovery, and trading strategies.

For platform context (wallets, strategies, tool categories, fees), see
[references/about-senpi.md](https://raw.githubusercontent.com/Senpi-ai/senpi-skills/refs/heads/main/senpi-entrypoint/references/about-senpi.md).


If any `npx` command fails, consult
[references/error-handling.md](https://raw.githubusercontent.com/Senpi-ai/senpi-skills/refs/heads/main/senpi-entrypoint/references/error-handling.md) for recovery
steps.

## Environment Variable Defaults

| Variable | Placeholder | Default |
|---|---|---|
| `SENPI_MCP_ENDPOINT` | `{{SENPI_MCP_ENDPOINT}}` | `https://mcp.prod.senpi.ai` |
| `REFERRAL_CODE` | `{{REFERRAL_CODE}}` | _(empty — optional)_ |

If a placeholder appears as a literal `{{...}}` string (not substituted),
use the default value from the table above.

---

## Agent Behavior

Do not narrate or explain tool calls. Execute silently and only present final results to the user.

---

## Pre-Response Check (Run Every Time This Skill Is Invoked)

Before responding to any query in this skill, run the mandatory invocation
check in
[references/skill-update-checker.md](https://raw.githubusercontent.com/Senpi-ai/senpi-skills/refs/heads/main/senpi-entrypoint/references/skill-update-checker.md)
(`Pre-Response Invocation Check` section) exactly once per invocation, then
reuse the captured `UPDATE_OUTPUT` for all downstream response contracts.
Do not run the same check a second time in the same invocation.

---

## Initial check: Skip only Step 1 if already authenticated

Before Step 1, check whether the machine already has a Senpi API key available:

```bash
if [ -n "${SENPI_AUTH_TOKEN}" ]; then
  # Optional: verify MCP responds (e.g. call a read-only tool)
  # If verification fails, clear or ignore and continue to Step 1
  echo "SENPI_AUTH_TOKEN is set; skipping Step 1 only. You MUST still run Step 2, then Step 3, then Step 4."
  SKIP_ONBOARDING=true
else
  SKIP_ONBOARDING=false
fi
```

- **If `SENPI_AUTH_TOKEN` is set and (optionally) MCP responds:** Skip **only Step 1** (Onboard). You **MUST** still run **Step 2: Discover** (list skills and present the catalog to the user), then **Step 3: Guide**, then **Step 4: Expand**. Do not treat "token is set" as "onboarding complete — do nothing."
- **If `SENPI_AUTH_TOKEN` is unset or empty:** Proceed to **Step 1: Onboard** as usual.

After the initial check, follow the step flow: Step 1 (unless skipped) → **Step 2 (always)** → Step 3 → Step 4.

---

## Step 1: Onboard

**Run this step only when** `SENPI_AUTH_TOKEN` is not set (i.e. `SKIP_ONBOARDING` is false). If you skipped here from the initial check, go to Step 2.

Install the onboarding skill:

```bash
npx skills add https://github.com/Senpi-ai/senpi-skills --skill senpi-onboard -g -y
```

Load and follow the `senpi-onboard` skill instructions. Pass this context:
- `SENPI_MCP_ENDPOINT`: {{SENPI_MCP_ENDPOINT}}
- `REFERRAL_CODE`: {{REFERRAL_CODE}}

**Gate — verify before proceeding:**
1. Senpi account exists
2. API key is generated
3. MCP server is configured and responds to a tool call

---

## Step 2: Discover

**Run this step always:** after Step 1 completes, or immediately when the initial check found `SENPI_AUTH_TOKEN` set. Do not skip this step when the user already has a token — they still need to see the skill catalog.

List available trading skills:

```bash
npx skills add https://github.com/Senpi-ai/senpi-skills --list
```

Present the catalog to the user. If the command fails, point the user to the
official [Senpi Skills repository](https://github.com/Senpi-ai/senpi-skills)
to browse available skills.

**Gate — verify before proceeding:** User has seen the skill catalog.

---

## Step 3: Guide (Optional)

Ask the user:

> "Would you like to learn how to trade on Senpi? I can walk you through
> your first trade with an interactive guide."

If the user agrees, install the Senpi getting started guide:

```bash
npx skills add https://github.com/Senpi-ai/senpi-skills --skill senpi-getting-started-guide -g -y
```

If the guide skill is not yet available, suggest these first actions instead:
- "Check your portfolio" (uses `account_get_portfolio` tool)
- "Discover top traders" (uses `discovery_get_top_traders` tool)
- "View market data" (uses `market_get_prices` tool)

---

## Step 4: Expand (User-Driven)

Install additional trading skills on demand based on user interest:

```bash
npx skills add https://github.com/Senpi-ai/senpi-skills --skill <skill-name> -g -y
```

Example:

```bash
npx skills add https://github.com/Senpi-ai/senpi-skills --skill wolf-strategy -g -y
```

Onboarding is complete. The agent is now equipped with Senpi's trading
toolkit and can install more skills as needed.

---

## Step 5: Install Background Skill Update Checker

Agent behaviour for this step: see
[references/skill-update-checker.md](https://raw.githubusercontent.com/Senpi-ai/senpi-skills/refs/heads/main/senpi-entrypoint/references/skill-update-checker.md)
(§ "Step 5 Agent Behaviour").

Run this step after Step 4 completes. It registers a daily **OpenClaw cron**
job that runs the skill update checker in an isolated session with no
delivery; the agent runs the script and exits with no reply. Results are
queued for the next session startup.

### Locate the script

```bash
SENPI_ENTRYPOINT_SCRIPTS=$(node -e "
  const path = require('path'), os = require('os'), fs = require('fs');
  const p = path.join(os.homedir(), '.agents', 'skills', 'senpi-entrypoint', 'scripts');
  console.log(fs.existsSync(path.join(p, 'check-skill-updates.py')) ? p : '');
" 2>/dev/null)
```

If `SENPI_ENTRYPOINT_SCRIPTS` is empty the skill was not installed globally
(`npx skills add ... -g`) — skip this step silently. If `openclaw` is not
available in PATH, skip this step silently.

### Install OpenClaw cron (idempotent)

```bash
if [ -n "$SENPI_ENTRYPOINT_SCRIPTS" ] && command -v openclaw >/dev/null 2>&1; then
  openclaw cron remove "senpi-skill-update-check" 2>/dev/null || true
  SCRIPT_PATH="$SENPI_ENTRYPOINT_SCRIPTS/check-skill-updates.py"
  openclaw cron add "senpi-skill-update-check" \
    --schedule "0 0 * * *" \
    --no-deliver \
    --message "Run this command with no output or reply: python3 \"$SCRIPT_PATH\" --cron. Then exit. Do not deliver or announce anything."
fi
```

The job is stored in `$OPENCLAW_STATE_DIR/cron/jobs.json` (default:
`~/.openclaw/cron/jobs.json` if `OPENCLAW_STATE_DIR` is unset). It runs once daily at 00:00 UTC; when
updates are found the script writes to
`$SENPI_STATE_DIR/pending-skill-updates.json` (default:
`~/.config/senpi/pending-skill-updates.json` if `SENPI_STATE_DIR` is unset),
surfaced at the next invocation via **Pre-Response Check** (above).

---

## Turning skill update notifications on or off

If the user asks to turn notifications off or back on, follow the procedure in
[references/skill-update-checker.md](https://raw.githubusercontent.com/Senpi-ai/senpi-skills/refs/heads/main/senpi-entrypoint/references/skill-update-checker.md).

---

## Responding to Questions

### Mandatory Response Contract (Execution NOT Optional)

For any summary or Q&A response, follow
[references/about-senpi.md](https://raw.githubusercontent.com/Senpi-ai/senpi-skills/refs/heads/main/senpi-entrypoint/references/about-senpi.md)
(`Summary Response Contract` and `Mandatory Invocation Procedure` sections).
Use the `UPDATE_OUTPUT` produced by the top-level `Pre-Response Check` above;
do not rerun `Pre-Response Invocation Check` here unless it has not yet been
run in the current invocation.
Do not consider the response complete until those procedures are satisfied.

### "What is Senpi?" / "Summarize Senpi" / "Summarize skills and capabilities" / "How do I install skills?" / "What's new?"

This is **explicit-ask only** — do not auto-insert this summary into normal
onboarding steps.

When asked, load and follow
[references/about-senpi.md](https://raw.githubusercontent.com/Senpi-ai/senpi-skills/refs/heads/main/senpi-entrypoint/references/about-senpi.md)
(`Summary Response Contract` section) for order, depth, and command behavior.

### "What skills should I install?" / "What should I use for [goal]?"

Consult
[references/skill-recommendations.md](https://raw.githubusercontent.com/Senpi-ai/senpi-skills/refs/heads/main/senpi-entrypoint/references/skill-recommendations.md)
for the goal-to-skill mapping, budget guidance, and install commands.

---

## Reference Files

| File | Purpose |
|------|---------|
| `scripts/check-skill-updates.py` | Daily background checker (run via cron with `--cron`). Reads Vercel skills CLI lock file, compares GitHub tree SHAs, writes version bumps / new skills to pending file |
| `references/skill-update-checker.md` | Startup output handling + turn notifications on/off + cron management |
| `references/skill-recommendations.md` | Goal-to-skill mapping table, budget guidance, install commands |
| `references/about-senpi.md` | Senpi summary source: what Senpi is, capabilities, full bullet catalog, user-friendly install flow, and what's-new guidance |
| `references/error-handling.md` | Recovery steps for `npx` command failures |
