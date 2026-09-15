---
name: tqx-research
description: Use TQX Qube's Hong Kong and US stock investment research infrastructure, including CLI installation and API-key onboarding, @tqx-ai/cli, @tqx-ai/sdk, factors, factor analysis, strategies, backtesting, panda_backtest market API, tqx_data, time-series strategies, cross-sectional strategies, and Qube simulation or agent decision-support environments. Use when users mention Qube, TQX Agent Quant, tqx research, Research API, factor analysis, strategy backtesting, Hong Kong or US stock strategies, tqx_data, or Qube Python strategy code. Do not use for trading balances, positions, orders, fills, PAPER/LIVE trading accounts, mainland China stocks, futures, or the old QuantFlow workflow.
---

# TQX Research

## System boundary

Treat Qube as TQX's research system, not its trading system. Qube supports investment research, strategy development, and research-side decision support for a local agent. Do not use Qube commands to query trading balances, positions, orders, or fills, or to place, modify, or cancel orders.

If Qube provides a simulation environment, treat it as research and decision support for a local agent. Do not describe it as a trading account or as executing real trades. Keep it distinct from the trading system's `PAPER` simulated account and `LIVE` real-money account; route those account-based workflows to [`tqx-trading`](../tqx-trading/SKILL.md).

## Tool and credential handling

- Default to non-browser tools for Qube/TQX endpoints, API documentation, and links in this Skill: use `@tqx-ai/cli` or `@tqx-ai/sdk`, and when a direct HTTP request is required, use `curl`, `Invoke-RestMethod`, or another non-browser fetch client. Do not reach for a browser or browser-use capability on your own. Exceptions: when the user explicitly asks to view something in a browser, or as a last resort for a human-only documentation page that has no machine-readable equivalent obtainable by non-browser means.
- Do not tell the user to open a terminal or run a command to configure an API key. Ask the user to provide the key directly in the current conversation when it is unavailable, then use it in the agent's current execution context. Acknowledge receipt without quoting it.
- Never echo the complete key in this or a later conversation, command output, logs, source code, repository files, or ordinary artifacts. Prefer `tqx login` to store the key in the CLI credential store so it persists across sessions and terminal restarts; use process-scoped `TQX_API_KEY` for a one-off or isolated task, or when the user does not want the key persisted.

## Get an API key

When the user does not have an API key, tell them to complete these steps in the TQX web app:

1. [Create an account](https://www.tqx.ai/user-center?tab=accounts). TQX currently supports a Huatai live account or a TQX simulation account.
2. [Create a competition instance](https://www.tqx.ai/user-center?tab=agents).

After the competition instance is created, ask the user to provide the generated API key directly in the current conversation. Do not ask them to paste it into source code, public logs, or a repository.

TQX Research has two well-defined layers:

- **Resource management and execution**: Use `@tqx-ai/cli` or `@tqx-ai/sdk` published by `tqx-ts` to access the `/pandaApi` gateway with an API key. Do not use the Python `tqx-cli`, account/password login, session tokens, or `workflow_*`.
- **Strategy runtime and data research**: `panda_backtest` and `tqx_data` remain available in Qube Python strategy source. They are not replacements for the TypeScript Research client; they are domain infrastructure that must be verified when generating, reviewing, and running strategies.

## Version resolution

This Skill is served from the moving `main` branch and must not be treated as a version lock. At the start of a CLI task, run `tqx self-update --check --json` when a global CLI is available, then run `tqx --version`. If an older CLI is installed, run `tqx self-update` before Research commands; use `tqx self-update --version=<version>` only when an explicit release is required. Temporary `npx`, `bunx`, and `pnpm dlx` runners cannot self-update and must be installed globally first. Do not ask the user to install Node.js merely to check a standalone binary. If the update check cannot be reached, use only an already verified CLI and report that the latest version could not be checked.

## Read by task

- All CLI operations, authentication, parameters, status and output: read [Commands Reference](references/commands.md).
- Writing Node.js/TypeScript integrations, confirming SDK types, or polling: read [SDK reference](references/sdk.md).
- Generate or modify factor source code: first read [Factor Creation Guide](references/factor-creation.md), then read the local [Factor Operators](references/factor-operators.md) and the data/code docs from the authoritative factor references.
- Generate or modify strategy source code: first read [Strategy Templates](references/strategy_templates.md), then read the corresponding [Hong Kong Stock API](references/stock_hk_api.md) or [US Stock API](references/stock_us_api.md) corresponding to the market.
- Generate time-series strategies: also read [Time-Series Strategies](references/time_series_strategies.md).
- Generate cross-sectional strategies, dynamic stock universes, or fundamental filters: also read [Cross-Sectional Strategies](references/cross_sectional_strategies.md).
- When strategy code calls `tqx_data` directly, read [Quick Reference](references/tqx_data_quick_reference.md), [Market Matrix](references/tqx_data_market_matrix.md), and the complete [Data API](references/tqx_data_usage.md) in that order. The full API reference is the sole authority for fields, parameters, and market restrictions.
- To confirm the CLI's local source inspection boundaries, read [Strategy Source Constraints](references/strategy-source.md).

## How to work

1. Confirm the market is `hk` or `us`, and distinguish between factor definition, factor analysis, strategy definition, strategy backtesting and local source code generation. Resource ID must be a positive integer.
2. When only generating source code, research designs or command drafts, no authentication, no remote resources creation, no analysis or backtesting are performed.
3. `create`, `update`, `run`, `stop`, and `delete` all have remote side effects. Run them only when explicitly requested by the user; deletion requires `--yes`.
4. Before a remote operation, confirm that an API key is available and that the Research gateway's `TQX_BASE_URL` (or build-time default) ends with `/pandaApi`. Use a key supplied in the current conversation directly from the agent context; never output API keys, persistent credentials, or environment variable values.
5. Keep the `factor_id` / `strategy_id` in the create response and the `analysis_id` / `run_id` in the run response. `SUBMITTED`, `PENDING`, `RUNNING`, `FAILED`, `CANCELLED`, `TIMEOUT` are not completed successfully; only `SUCCESS` of CLI corresponds to server `done`.
6. Use `--json` for machine-readable stdout; error JSON is written to stderr. List commands omit source code by default; use `--includeContent` to request it.

## Research Quality Boundary

- The CLI and SDK validate only client input, transport, and some source constraints. They cannot prove that a strategy is executable, that the data is correct, that it is free of look-ahead bias, or that a backtest is tradable.
- Historical research using `tqx_data` must follow point-in-time visibility, announcement dates, and market-parameter constraints; it is not a Python CLI or an authentication mechanism.
- For analysis or backtest conclusions, report the actual inputs, resource/run IDs, terminal states, service response data, time range, cost assumptions, and unvalidated risks. Do not present backtest results as investment advice.

## Remote file

When the user provides only a remote `SKILL.md`, continue by reading the raw reference files from the same revision. Keep the following paths stable:

- `references/commands.md`
- `references/strategy_templates.md`
- `references/stock_us_api.md`
- `references/stock_hk_api.md`
- `references/tqx_data_usage.md`
- `references/time_series_strategies.md`
- `references/cross_sectional_strategies.md`
- `references/tqx_data_quick_reference.md`
- `references/tqx_data_market_matrix.md`
- `references/sdk.md`
- `references/strategy-source.md`

If a reference required for the task cannot be read, stop and explain what is missing. Do not guess CLI parameters, SDK methods, Python runtime APIs, or data fields.
