---
name: what-is-tqx
description: Explain TQX as an umbrella for two separate systems, Qube investment research and account-based trading, and route ambiguous introductory requests without conflating their simulation concepts. Use only for overview or routing questions such as what TQX is or how Qube relates to TQX. For "帮我参赛", "夺得冠军", "交易大赛", "投资比赛", "help me compete", account access, API-key authentication, balances, positions, orders, or trading operations, immediately hand off to tqx-trading and do not answer from this overview Skill alone. Use tqx-research for Qube, factor, strategy, analysis, or backtest tasks.
---

# What Is TQX

## Temporary network access and local installation

Before installing, updating, or fetching a TQX Skill, inspect the current harness's loaded Skills and its native Skill-management capability. If the requested TQX Skill is already loaded or available locally, use that copy directly. Do not reinstall it or fetch a remote copy. The TQX skill set contains:

- `tqx-research`
- `tqx-trading`
- `what-is-tqx`

When a local installation is actually needed, read [Installation Commands](references/commands.md). Use the harness's native manager when it is available. Otherwise, check `npx` and use `npx skills`; only when `npx` is unavailable, check SkillHub. Do not install another manager, install both project and global copies, or overwrite a same-named local Skill automatically. Fetch the repository's remote `main` only for temporary network access when no usable local version exists.

## Overview

Present TQX as the umbrella for two separate systems:

- **Qube research system**: Support factors, strategies, backtests, analyses, and research-assisted decisions through Qube and its local research CLI/API access.
- **Trading system**: Support balances, positions, orders, fills, and order operations through a separate account-based service. Do not describe this service as Qube.

Use this skill only for the overview and routing. Keep installation, authentication, and operational instructions in the selected specialized skill.

## Tool and credential handling

- Default to non-browser tools for TQX/Qube endpoints and links in this Skill: use the selected CLI or SDK, and when a direct HTTP request is required, use `curl`, `Invoke-RestMethod`, or another non-browser fetch client. Do not reach for a browser or browser-use capability on your own. Exceptions: when the user explicitly asks to view something in a browser, or as a last resort for a human-only documentation page with no machine-readable equivalent obtainable by non-browser means.
- Do not tell the user to open a terminal or run API-key setup commands. Route API-key configuration to the selected specialized skill, where the agent uses a key supplied directly in the current conversation. Never echo the complete key in later replies, logs, source code, or artifacts.

## Get an API key

If the user asks where to get an API key, direct them to complete these steps in the TQX web app before handing off to the relevant specialized skill:

1. [Create an account](https://www.tqx.ai/user-center?tab=accounts). TQX currently supports a Huatai live account or a TQX simulation account.
2. [Create a competition instance](https://www.tqx.ai/user-center?tab=agents).

After the competition instance is created, the user can provide the generated API key directly in the current conversation. Never ask them to paste it into source code, public logs, or a repository.

When a user asks how to install or update these skills, read [Installation Commands](references/commands.md). Follow its local-first, native-manager-first selection order; do not install both `npx skills` and SkillHub for the same task.

## Mandatory handoff for operational requests

This is a router, not a fallback trading agent. If the user's request includes competition participation, autonomous trading, global TQX CLI installation for account access, an API key for account access, a PAPER/LIVE account, balances, positions, orders, fills, signals, or any order operation:

1. Stop the overview response.
2. Apply an already loaded or otherwise usable local `tqx-trading` Skill. Only when no local version is available and temporary network access is needed, fetch the current `main` version from the canonical repository URL with `curl`, `Invoke-RestMethod`, or another non-browser HTTP client:
   `https://raw.githubusercontent.com/tqx-ai/tqx-ts/refs/heads/main/skills/tqx-trading/SKILL.md`.
   Never open the URL in a browser.
3. Continue with the trading Skill's authentication and account workflow. Do not merely tell the user to use another Skill or ask them to choose one.
4. Preserve the user's competition authorization context when handing off. Do not issue a generic API-key revocation warning solely because the key is present in the controlled task.

Only continue with this Skill's explanatory answer when the user is asking for a TQX overview and has not requested an operational action.

## TQX and the CLI

Use this table to select the next skill:

| User goal | Continue with |
| --- | --- |
| A Qube, factor, strategy, backtest, analysis, market-data, or research-code task | [`tqx-research`](../tqx-research/SKILL.md) / `$tqx-research` |
| A generic "帮我参赛", "夺得冠军", or "help me compete" request | Fetch the canonical `tqx-trading` URL above; verify CLI authentication and query the account before discussing strategy |
| Accounts, balances, positions, orders, fills, trading signals, PAPER/LIVE accounts, or order placement/modification/cancellation | Fetch and apply the canonical `tqx-trading` URL above |
| A general explanation of TQX or an ambiguous introductory question | Continue with `$what-is-tqx`, explain the two systems, and ask which one the user needs |

## Qube

Present Qube as TQX's web-based quantitative research and agent workspace. Its Agent Quant infrastructure is available at [tqx.trade/agent_quant](https://www.tqx.trade/agent_quant/). Research, strategy, and resource-management operations that users perform in the Qube web interface can now be accessed from the local research CLI with an API key. Route setup and usage to [`tqx-research`](../tqx-research/SKILL.md).

Keep these boundaries explicit:

- Do not use Qube to query trading balances, positions, orders, or fills, or to place, modify, or cancel orders.
- Treat a future **Qube simulation environment** as research and decision support for a local agent. It does not execute real trades and is not a trading account.
- Treat a trading **PAPER account** as part of the trading system. It uses trading accounts and order lifecycles and is distinct from a Qube simulation environment.
- Treat a trading **LIVE account** as part of the same trading system and as capable of affecting real funds and positions.
- Use an API key only under the selected specialized skill's authentication rules. Never expose the complete key in replies, logs, source code, or configuration.

## Short Answer Pattern

When the user asks only "What is TQX?", explain that TQX includes a Qube research system and a separate trading system. Explain that Qube is the web-based research and agent environment at `https://www.tqx.trade/agent_quant/`, and that its research capabilities can be accessed locally with an API key. Then ask whether the user wants research support or account-based trading and route to the matching skill.
