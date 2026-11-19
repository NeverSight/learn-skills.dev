---
name: algorover-research
description: Discover AlgoRover Research strategies, preview and run historical backtests, inspect or cancel jobs, and download research reports through the hosted MCP service.
---

# AlgoRover Research

Use the host's `algorover-research` MCP connection at `https://research.algorover.ai/mcp`. Installing this Skill adds instructions; configure the MCP connection separately using [connection instructions](connection.md) when its tools are missing.

Research uses public historical market data. It does not connect exchange accounts or execute orders. Public discovery and preparation do not require sign-in. Personal runs and reports require browser OAuth with `research:read` and `research:run`; never request credentials in chat.

1. For discovery, call `search_strategies` with `locale: "zh-CN"` for Chinese and `locale: "en"` for English or other languages. Preserve that locale in later tools that accept it. For a named strategy, use the returned reference to call `get_strategy`.
2. Use only the version, presets and markets returned by the service. If preparation is `not_requested`, call `prepare_strategy`; check `get_strategy` at least three seconds apart until ready. Report its failure reason when unavailable.
3. Call `prepare_backtest` for the selected preset, venue and supported 90- or 365-day window. Present the exact configuration and wait for confirmation before starting.
4. After confirmation, call `start_backtest` using the returned `prepared_input`, `preparation_ticket` and `request_key` as `idempotency_key`. Reuse that key if retrying an uncertain start. Preserve the real task identifier.
5. Use `get_backtest` for status, `get_backtest_result` for completed metrics and `get_backtest_report_download` for requested reports. Use `list_backtests` when the task identifier is unknown. Show actual returned text and links; mention a card only when the host renders it.
6. On cancellation, call `cancel_backtest` only for the selected active task and confirm `status: cancelled` using `get_backtest`. A pending cancellation is not completion.

If authorization fails, use the host's connect or reconnect action, complete browser authorization, and resume only after the host confirms the connection. Keep the original request. Report returned service failures without inventing results or substituting a local engine.

When saving reports, preserve the returned `filename`; append a numeric suffix before `.zip` if it already exists. Historical results do not establish future returns.

Delete a selected result only on an explicit deletion request. Deleting all Research data requires a separate explicit request and the service's confirmation value; it does not delete the user's external identity account.
