---
name: fmz
description: "Operate the FMZ Quant trading platform (fmz.com) through its MCP tools and write strategies for it in JavaScript/TypeScript, Python, C++, Rust, Pine Script or MyLanguage (麦语言). Covers getting authorized and connected (device-code flow, API key, Bearer header, scopes), the platform model (exchange accounts, nodes, strategies, templates, robots, backtests, messages), every MCP tool and the REST extended API, the complete strategy API documentation with four-language examples, TA/talib indicators, cloud backtest configuration and result reading, and the safety rules of a real-money platform. Use whenever the fmz MCP server is connected, or when a task mentions FMZ, its robots, strategies, backtests, nodes or API keys, or strategy code for the platform."
license: MIT
---
# FMZ platform via MCP

FMZ (fmz.com) is a quant trading platform: strategies written in JavaScript, TypeScript, Python, C++, Rust, Pine, MyLanguage (麦语言) or Blockly run as "robots" (实盘) on the user's own nodes (托管者) against the user's exchange accounts. Everything below is done through the `fmz` MCP server. Not connected yet? See "Connecting" below.

This file is the entry point: the platform model, how to connect, the tool catalog and the safety rules. Everything else — writing code in each language, the full API documentation, indicators, backtesting — lives in `references/` and is listed in "Where to read next" at the end; read only the file the task needs.

## Connecting (authorization)

The authoritative, always-current version is `https://www.fmz.com/agent/setup.md`; this is the short form. The user never types a password for you and you never see one: you ask for an API key, the user clicks Approve once in a browser.

1. **Request a key**: `POST https://www.fmz.com/api/agent/device/code` with JSON `{"name": "<your name @ machine>", "scopes": "read,backtest,write,trade"}`. The response has `device_code`, `user_code`, `verification_uri_complete` (`https://www.fmz.com/agent/authorize?code=XXXX-XXXX`), `expires_in` (600 s) and `interval` (5 s). Show `verification_uri_complete` to the user verbatim and ask them to open it and approve. `name` is the key's identity: approving a request with the same name revokes the previous key, so re-running setup does not pile up keys.
2. **Poll**: `POST https://www.fmz.com/api/agent/device/token` with `{"device_code": "..."}` every `interval` seconds. `status` is `pending` (keep waiting), `slow_down` (back off), `denied` / `expired` (stop and tell the user) or `approved`, which returns `access_key`, `secret_key`, `mcp_url` (`https://www.fmz.com/api/mcp/<access_key>`) and the granted `scopes` — **once**. Write it to your MCP configuration immediately; never into the conversation, logs or a repository.
3. **Connect**: MCP Streamable HTTP at `mcp_url` with header `Authorization: Bearer <secret_key>` (the secret goes in the header only, never in the URL). Claude Code: `claude mcp add --transport http fmz "<mcp_url>" --header "Authorization: Bearer <secret_key>"`; Cursor / Claude Desktop / other clients: the same URL and header in their MCP server configuration. Then `tools/list`; the `instructions` returned by `server/discover` (or `initialize` on older protocol revisions) describe the recommended workflow.

Scopes: `read`, `backtest`, `write`, `trade` are granted by default; `danger` (delete / publish) is never included unless you ask for it explicitly and tell the user why. The user can untick scopes on the approval page and change a key's privileges later at `/m/account#apikey`. A key created by hand on that page works the same way (same `mcp_url` form, same header).

Scripts can use the same key against the signed REST API instead (`references/rest-api.md`). To disconnect for good, call `revoke_my_key` with `confirm: true`.

## The platform model

| Object | What it is | How you reach it |
|---|---|---|
| Exchange account (`platform`) | One exchange API key the user added on the website (spot, futures, or a CTP futures counter). The agent never sees or enters keys. | `list_platforms` → pick by `id` (`platform_id`). Sandbox accounts have `is_sandbox`. |
| Node (`node`, 托管者) | The host process that runs robots: the user's own docker/binary, or a platform-hosted one. A robot can only start on an online node. | `list_nodes`; `delete_node` is `[danger]`. |
| Strategy | Source code + language + parameter definitions (`args`) + optional templates. Has versions (snapshots), a group (folder), a visibility (private/shared/verify/premium/system). Rented or public strategies can be run but their source may be hidden. | `list_strategies` (scope mine/public/official/templates), `get_strategy`, `save_strategy`, `check_strategy`, `save_strategy_version`. |
| Template | A strategy of category "template" whose functions a strategy imports (`$.` namespace in JS). Listed in `save_strategy.templates` by id. | `list_strategies` with `scope: templates`. |
| Robot (实盘) | A running instance: strategy (+ pinned version) + `exchanges: [{platform_id, pair}]` + `args` + `period` + node. Prepaid by the hour from the account balance. Has a log database (trades, errors, prints), a status page (`LogStatus`), stdout/stderr output, and a profit curve (`LogProfit`). | `list_robots`, `get_robot`, `get_robot_logs`, `get_robot_output`; `create_robot` / `start_robot` / `stop_robot` / `restart_robot` / `send_robot_command` are `[trade]`. |
| Backtest | A cloud task that replays history data through the strategy with simulated accounts. Holds a concurrency slot until collected or stopped. | `run_backtest`, `get_backtest`, `list_backtests`, `stop_backtest` (see `references/backtest.md`). |
| Messages | Robot push messages (`Log("...@")`, trade notices) and system alerts (node offline, robot stopped). | `list_messages`, `delete_messages`, `set_robot_alert`, `set_node_alert`. |
| Groups | Folders for robots or strategies. | `list_groups`, `save_group`, `move_to_group`, `delete_group`. |

Robot `status` values: `queue` (waiting for a node), `running`, `stopping`, `complete` (strategy returned), `stopped`, `error` (read `error` and `get_robot_output`).

## Workflow

1. **Orient**: `ping`, `get_account_summary`, `list_platforms`, `list_nodes`. No online node → the user must start one (website: Nodes); nothing you do will run until then.
2. **Write**: pick the language skill, write the code, run `check_strategy` (`language`, `source`): syntax check for javascript/typescript, compile check for pine/mylanguage/flow/cpp/rust (cpp/rust compile on the build cluster and can take a minute); python and blockly have no static check.
3. **Save**: `save_strategy` with `name`, `language`, `source`, `args` (`[[name, label, description, default], ...]`; names become globals in the code), optional `description`, `manual`, `note`, `templates`, `group_id`. Returns `strategy_id`. Updating: pass `strategy_id` and only the changed fields; call `save_strategy_version` first if the old code must stay retrievable (max 20 versions; `delete_strategy_version` when full).
4. **Backtest**: `run_backtest` with `strategy_id` (or raw `source` + `language`), `begin`, `end`, `period`, `exchanges: [{exchange: eid, pair, balance, stocks, fee_maker, fee_taker}]`, optional `args`, `slippage`, `net_delay` → `task_id`. Then `get_backtest` with `wait` up to 60 and `detail` summary/logs/full → `profit`, `max_drawdown`, order and error counts, `error_lines`, final accounts, `profit_curve`. The profit metrics come from the strategy's own `LogProfit()` calls: a strategy that never calls it shows empty profit/drawdown/curve, so judge it by `final_accounts` (or add `LogProfit`). Always `stop_backtest` when you have what you need; slots are limited. `eid` values come from `list_exchanges`. For the fast write–run–fix loop on a JavaScript/Python strategy, run the local engine on this machine instead (`references/backtest-local.md`, seconds per run, no slot) and use the cloud for the confirming run.
5. **Go live** (`[trade]`, confirm with the user first): `create_robot` with `name`, `strategy_id`, `exchanges: [{platform_id, pair}]`, optional `args`, `period` (seconds, default 60), `node_id` (omit = least loaded online node), `strategy_version_id` (pin a version), `group_id`. It prepays one hour and starts the robot; the result is the robot after the start attempt. `status: error` → read `error`, `get_robot_output`, `get_robot_logs`.
6. **Watch**: `get_robot` (configuration, status, profit, status page text, last error), `get_robot_logs` (newest first; `before_id` pages back; `types` filters; `with_status` adds the status page), `get_robot_profit` (the LogProfit() curve, newest first, read from the node), `get_robot_output` (process stdout/stderr tail), `list_messages`.
7. **Change**: `stop_robot` → `update_robot` (only stopped robots; `args` merges into the current values — pass just the parameters to change, `replace_args: true` to reset the whole set; the strategy itself cannot change, create a new robot for that) → `start_robot`. `restart_robot` = stop + start. `send_robot_command` delivers a string to a running robot's `GetCommand()`; interactive buttons use the `name:value` form.
8. **Finish**: `stop_robot` does not close positions — say so. Delete only on explicit request (`delete_robot` needs a stopped robot; `remove_logs` is irreversible). When the user asks you to disconnect, `revoke_my_key` with `confirm: true` revokes only the key this connection uses.

## Tool catalog

`references/tools.md` is the complete, generated list (40 tools: every parameter, type, default). By scope:

| Scope | Tools | Granted |
|---|---|---|
| `read` | ping, revoke_my_key, get_account_summary, list_exchanges, list_platforms, list_nodes, list_strategies, get_strategy, list_strategy_versions, get_strategy_version, list_robots, get_robot, get_robot_logs, get_robot_profit, get_robot_output, list_messages, list_groups | default |
| `backtest` | run_backtest, get_backtest, list_backtests, stop_backtest | default |
| `write` | check_strategy, save_strategy, save_strategy_version, delete_strategy_version, update_robot, save_group, move_to_group, delete_group, set_robot_alert, set_node_alert, delete_messages | default |
| `trade` | create_robot, start_robot, stop_robot, restart_robot, send_robot_command | default (device-flow keys); costs money and places real orders |
| `danger` | delete_strategy, delete_robot, delete_node, publish_strategy | never by default; the user grants it explicitly |

A tool missing from `tools/list` means the key lacks that scope; the user can edit the key's privileges at `/m/account#apikey` (scope names, tool names, `*`, `!name` to exclude). Trading-terminal tools named `plugin*` may also appear; they belong to the website's trading terminal and need the `trade` scope.

## Conventions

- `args` everywhere: `{name: value}` object or `[[name, value], ...]`; omitted parameters keep the strategy defaults. Values are typed by the default (number / string / boolean).
- Enumerations are words, not numbers: robot `status` queue/running/stopping/complete/stopped/error; strategy `visibility` private/shared/verify/premium/system; `language` javascript/typescript/python/cpp/blockly/mylanguage/pine/flow/rust.
- Times: ISO 8601 or unix seconds in; ISO UTC out. Backtest `period`: 1m/5m/15m/30m/1h/4h/1d. Robot `period` is in seconds.
- Pairs: `BTC_USDT` (spot). Futures contracts are chosen in code with `exchange.SetContractType("swap" | "quarter" | ...)`, so the robot pair stays `BTC_USDT`.
- Backtest `exchanges[].exchange` is the `eid` from `list_exchanges` (e.g. `Binance`, `Futures_Binance`, `Futures_CTP`); robots use `platform_id` from `list_platforms` instead.
- All list tools paginate with `offset` / `limit` (max 200). Results never contain secrets.

## Safety rules

- Tools whose description starts with `[trade]` spend the user's balance and place real orders; `[danger]` tools delete or publish. Ask the user before each such call and say what it will do.
- Never configure exchange API keys; never ask the user for them. They add accounts on the website, you choose by `platform_id`.
- Never paste `secret_key` or any credential anywhere; tool results never contain them.
- `stop_robot` does not close positions. Say so when stopping a robot that may hold positions.
- Prefer sandbox/simulated accounts (`is_sandbox`) or a tiny amount for a first live run, after a backtest with no `error_lines`.
- Do not create robots in a loop or retry `create_robot` blindly: each attempt prepays an hour.
- Deleting is the user's decision, named explicitly, every time.

## Errors you will see

- `no online node` → the user must start a node. Nothing was created or charged.
- `too many backtests running` → `list_backtests`, then `stop_backtest` the stale one.
- `Tool not allowed` / tool missing from `tools/list` → the key lacks that scope.
- `strategy ... not usable` → not owned/rented, deleted, or a version that is not the author's.
- `robot is not stopped` on `update_robot` / `delete_robot` → `stop_robot` first and wait for `stopped`.
- `still referenced by a robot` on `delete_strategy` → `list_robots` with `strategy_id` lists them (stopped ones count); delete those robots first.
- Robot `status: error` right after `create_robot` → compile/runtime failure: `get_robot_output` shows the traceback; insufficient balance and expired rented strategies are reported in `error`.
- Backtest `errors > 0` → `get_backtest` with `detail: logs` and read `error_lines`; data gaps for the pair/period/date range are the usual cause.

## REST instead of MCP

Scripts and schedulers can use the signed REST "extended API" with the same key: `references/rest-api.md` has the endpoint, the signature, the return codes, the robot status codes and the method list (GetRobotList, GetRobotDetail, GetRobotLogs, CommandRobot, StopRobot, RestartRobot, NewRobot, GetNodeList, GetPlatformList, ...). The REST surface is older and lower-level than the MCP tools; prefer MCP when it is available.

## Where to read next

| Task | Read |
|---|---|
| Write or review a strategy in JavaScript / TypeScript | `references/javascript.md` (signatures: `references/fmz.d.ts`, Chinese `references/fmz.zh_CN.d.ts`; native event API `references/ctx.d.ts` + `references/events.md`; known-good sample `references/selfcheck.js`) |
| Python | `references/python.md` (`references/fmz.pyi`, `references/fmz.zh_CN.pyi`, `references/talib.pyi`, `references/selfcheck.py`) |
| C++ | `references/cpp.md` (`references/fmz.hpp`, `references/json.hpp`, `references/TA.hpp`, `references/talib.hpp`, `references/selfcheck.cpp`) |
| Rust | `references/rust.md` (`references/fmz.rs`, `references/selfcheck.rs`) |
| Pine Script | `references/pine.md` (built-ins the engine implements: `references/pine-builtins.md`) |
| MyLanguage (麦语言) | `references/mylanguage.md` (`references/mylanguage-functions.md`, official templates in `references/mylanguage-examples/`) |
| Exact signature / return fields / failure behaviour of one API call, structure or constant | `references/api-docs.md` explains how to grep `references/api.en.md` (English, 1 MB, four-language examples) or `references/api.zh.md` |
| Indicators (`TA.*`, `talib.*`) | `references/indicators.md` (`references/ta.md`, `references/talib.md`) |
| Configure, run, debug or interpret a backtest | `references/backtest.md` (every config key: `references/backtest-config.md`) |
| Backtest locally in seconds on this machine (Python engine; no cloud slot) | `references/backtest-local.md` |
| Exact parameters of an MCP tool | `references/tools.md` (generated from the server) |
| Scripts that call the platform without MCP | `references/rest-api.md` |
| Platform concepts as written for people (nodes, robots, templates, parameters, interactive controls, options, debugging tool...) | `references/user-guide.en.md` / `references/user-guide.zh.md` (grep the `## ` section titles) |

Read one language file plus `references/api-docs.md` for a coding task; `references/backtest.md` before the first backtest; nothing else unless the task calls for it.
