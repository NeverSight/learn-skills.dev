---
name: doubao
description: "Control Doubao through a Linux/macOS headless HTTPS CLI, or macOS desktop/browser backends. Headless supports chat, cloud and process-based local Work, attachments, models and reasoning, projects, enterprise knowledge, MCP, usage, profiles and task recovery without a browser or installed Doubao app. Requires Node.js 22+ and account sign-in."
---

# Doubao CLI

`doubao` supports direct headless HTTPS and macOS desktop CDP. `doubao web` is a compatibility alias for Headless. Requires Node.js 22+ and Doubao account sign-in. Linux defaults to Headless; macOS defaults to Work when installed, otherwise Doubao (unless `DOUBAO_APP` overrides the path). The desktop backend requires macOS.

If the CLI is missing: `npm install --global doubao-cli@latest` (or prefix commands with `npx --yes doubao-cli@latest`).

## Headless

Use `doubao headless <command>` on Linux or macOS to select Headless explicitly; `doubao --platform headless <command>` is equivalent. Linux also accepts unprefixed commands. On macOS, keep the `headless` prefix on login, session operations and recovery. `--runtime cloud` does not switch the backend.

Legacy `doubao web <command>` and `--platform web` select the same Headless backend, credentials and profiles. Browser login sessions are not imported; run `doubao headless login` to sign in. Browser `--target` and `web cdp` commands are unsupported.

```bash
doubao headless login                  # Terminal QR; approve on the phone
doubao headless status --json
doubao headless capabilities --json
doubao headless models --json
doubao headless profiles --json
doubao headless usage --json
doubao headless sessions list --json
doubao headless sessions create "..." --mode work --runtime cloud --wait --json
doubao headless sessions create "..." --mode chat --wait --json
doubao headless sessions send <id> "..." --wait --json
doubao headless sessions create "Review these" --attach ./report.pdf --model 'Orange 5.5' --reasoning high --wait --json
doubao headless sessions create "Inspect this project" --mode work --runtime local --project <id-or-name> --enterprise-knowledge --workspace /absolute/path --permission AskOnRisk --wait --json
doubao headless sessions wait <id> --run <run-id> --json
doubao headless sessions stop <id> --run <run-id> --json
doubao headless mcp register tools --command /absolute/path/node --arg /absolute/path/server.mjs --json
doubao headless sessions send <id> "Use my tool" --runtime local --mcp <connector-id> --wait --json
```

- No browser, CDP or installed desktop app is required. Do not launch an app to recover a headless connection.
- New conversations default to cloud Work; use `--mode chat` for ordinary chat. `--runtime` chooses cloud or local task execution and does not select the backend. Project, enterprise knowledge and local execution require Work mode.
- Headless local execution uses a Node.js HTTP/SSE worker with access to the local workspace. It is process-based and is not the native Doubao app sandbox. New local conversations default to `AskOnRisk`; follow-ups inherit the saved local permission, including `FullAccess`, unless overridden with `--permission`. Explicit or inherited `FullAccess` requires user confirmation in a terminal with TTY stdin/stderr before submission, including no-wait submissions; `--yes` cannot bypass it. Recovery of an unfinished `FullAccess` task requires fresh confirmation before starting a local executor. `AskOnRisk` and `AlwaysAsk` tool approvals require TTY input/output and `--wait`; without `--wait`, operations needing a prompt are denied. These policies do not confine MCP server processes.
- Headless MCP registration retains all `--env` values only in the private local store and stdio process; it sends an empty environment to the service. Command arguments and tool results still reach the service, so do not put credentials there. Previously uploaded values are not erased by this change.
- `--mcp` uses a local stdio server and selects local Work execution. Without `--wait`, one detached worker submits the original request and owns its local HTTP/SSE execution and MCP calls. The permission setting does not confine the MCP server process.
- `login --cookie-file <secret-path>` imports an existing Cookie header or cookie array. `DOUBAO_HEADLESS_COOKIE` is an in-memory alternative. Do not print credentials or place them in command operands.
- Model selection uses the exact model name from `headless models`. Profile-scoped defaults can be changed with `model select` and `model reasoning`; per-turn overrides use `--model` and `--reasoning`. Attachments use repeatable `--attach`; project and enterprise options are described in [the Headless guide](../../docs/headless.md).
- `profiles`, `current` and `open` refer to Headless account profiles and the CLI's selected conversation; they do not open a desktop UI. Desktop app profile account and tenant metadata remain documented separately in the README.
- Save both IDs; recover accepted timeouts with `wait`, never by resending. Without `--wait`, the detached submission worker continues execution for that same request. `sessions wait` uses the same IDs and may start a runtime to recover from the saved receipt; a persistent lease prevents concurrent execution while the original worker is active. `waiting_input` remains unresolved until an interactive control is answered in Doubao.
- Options unsupported on a Headless command are rejected before requests are sent. CLI 0.17 passed 357/357 tests on Linux x86_64 with Node 23.7.0 and macOS with Node 22.16.0. Live 0.17 acceptance used isolated configs on Linux and macOS and covered attachments, projects and enterprise knowledge, local execution, stdio MCP, and Linux detached-worker recovery. Fresh QR login was verified on macOS; Linux acceptance used an isolated install and cookie file from a QR-authenticated session, so it does not establish fresh Linux QR login. This is source/candidate evidence, not npm publication or release verification. See [Headless details and historical acceptance](../../docs/headless.md). This backend uses private service APIs.

To rerun live acceptance, use a source checkout, a separate config directory with its own completed login, and a separate output directory. Do not use `HOME` for isolation. For example, set `DOUBAO_CLI_CONFIG_DIR` to the isolated config for login, then run `npm run test:e2e:headless -- --config <absolute-config-path> --output <absolute-output-path> --stage all`. The script is part of the source checkout and is not included in the npm package. If an accepted task reports a failed receipt write, restore the error's structured `recoveryReceipt` to `recoveryReceiptPath` with mode 0600 after repairing storage, then recover with the same IDs; never resubmit the accepted request.

## Desktop app selection (macOS)

Check `doubao --version`; update older installations with `doubao update` before using the selectors below.

Prefer DoubaoWork when installed; fall back to Doubao only when Work is absent. Use `--platform work` or `--platform doubao` on any command to select explicitly. A login or CDP failure must not trigger a switch. Check `status --json` for `app`, `appPath`, `dataDir`, profile, and `cdpEndpoint`.

`--platform work|doubao|headless` is the standard backend selector. `--app work|doubao` remains a desktop compatibility alias; conflicting selectors are rejected. `--platform web` remains an alias for `headless`.

Work uses port 9226 and its own profile directory; regular Doubao uses 9225. Keep the same `--platform` on follow-ups. Connectors are account-level, so the same account can expose them in both apps. Restart authorization applies separately to each app.

## Desktop readiness check

```bash
doubao status --json        # app installed / running / version / profile
doubao capabilities --json  # per-feature availability; cdp.available gates messaging
```

If `cdp.available` is false, use `doubao cdp launch`. Restarting a running app needs the user's consent; pass `--yes` in non-interactive use only when that restart is authorized. Use `DOUBAO_CDP_ENDPOINT` for a non-default port.

## Desktop command routing

Pass `--json` to every data-returning command when another program consumes the output.

| Task | Command |
| --- | --- |
| Show usage quota (CLI 0.13.0+) | `doubao usage --json` |
| List runtimes / projects | `doubao runtimes --json` / `doubao projects list --json` |
| Create a project | `doubao projects create "name" [--workspace /absolute/directory] --json` |
| Select task context | add `--runtime local\|cloud --project <id-or-name> --enterprise-knowledge` to create/send |
| List sessions / archives | `doubao sessions list [--archived] [--all] --json` |
| Archive / restore session | `doubao sessions archive <id> --json` / `doubao sessions unarchive <id> --json` |
| Pin / unpin session | `doubao sessions pin <id> --json` / `doubao sessions unpin <id> --json` |
| Rename session | `doubao sessions rename <id> "New title" --json` (non-empty, at most 20 UTF-16 units) |
| Move session to project | `doubao sessions move <id> <project-id-or-exact-name\|none> --json` |
| Current session | `doubao sessions current --json` |
| Create session with first message | `doubao sessions create "..." --wait --json` |
| Blank draft session | `doubao sessions create --json` (returns `conversationId: null`) |
| Send to a session | `doubao sessions send <id> "..." --wait --json` |
| Query a turn | `doubao sessions status <id> --run <run-id> --json` |
| Resume waiting | `doubao sessions wait <id> --run <run-id> --timeout 600 --json` |
| Stop a turn and its tasks | `doubao sessions stop <id> --run <run-id> --json` |
| Register a local MCP server | `doubao mcp register <name> --command <path> [--arg X]... [--env K=V]... --json` |
| List / remove MCP connectors | `doubao mcp list --json` / `doubao mcp remove <connector-id> --json` |
| Send with MCP tools | add `--mcp <connector-id> --wait` to each `sessions create`/`sessions send` |
| Read messages | `doubao sessions read <id> --limit 20 --json` |
| Reveal session in the app | `doubao sessions open <id>` |
| List / show models | `doubao models --json` / `doubao model --json` |
| Switch model | `doubao model select <model> --json` or per-send `--model <model>` |
| Set reasoning effort | `doubao model reasoning <level> --json` or `--reasoning <level>` on select/send/create |
| Update the CLI | `doubao update` (`update check`, `update auto on`; reminders: `update notify on|off|status`) |

## Behavior notes

- Task tracking requires CLI 0.11.0 or newer. Check `doubao --version` and run `doubao update` before using `sessions status/wait` or `stop --run` on an older installation.
- Save both `conversationId` and `runId` from each accepted send. `--wait` follows organizer/subagents and returns only the final main reply in `reply`; interim text is `progress`, produced files are `artifacts`, and `tasks` gives server thread counts. Omit `--wait` to return on acceptance with `reply: null` (desktop MCP requires `--wait`; Headless MCP can run in its background worker).
- Timeout defaults to 120 s; set `--timeout <seconds>` when needed. Timeout or disconnection does not cancel work. Use `sessions wait <id> --run <run-id>` in a new process instead of resending; tools may already have executed. Keep the same app, account, profile and config directory for recovery receipts. Receipt files include request content and have mode 0600.
- `waiting_input` includes `pending` questions or approval controls. Ask the user to respond in Doubao, then wait again; do not automatically choose or approve. Waiting commands exit nonzero for timeout, unknown state, waiting input, failure or cancellation. A `status` lookup itself exits zero when the lookup succeeds.
- Explicit cancellation uses `sessions stop <id> --run <run-id>`. Confirm `stopped: true`; otherwise report unconfirmed cancellation. It does not undo tool effects. Without `--run`, status/wait/stop pin the latest submitted turn once; prefer the saved ID for automation. An already completed old turn can be queried/stopped without targeting a newer one.
- `--expect-json` / `--reply-schema <path>` validate the final reply. Use them on create/send with a message and `--wait`, or on `sessions wait`. They mark `replyValid` and exit nonzero on invalid output. Pending/error states are not successful replies.
- Runtime/project commands and enterprise knowledge require CLI 0.12.0 or newer.
- `--runtime local|cloud` selects execution on 本地电脑 or in the cloud. New sessions default to local with `FullAccess`; follow-ups inherit the server's runtime/project. An unavailable local runtime fails explicitly. Use `--runtime local --permission AlwaysAsk` or `AskOnRisk` to request Doubao approvals.
- `projects create <name>` returns `id`, `name`, `folders` and `operationId`. Optional `--workspace` must be an existing directory and binds it as this app/device's primary folder. Names allow 40 units (Chinese characters count as 2). Creation is not retried automatically; an error retains `operationId` and any known `id`. Check `projects list` before repeating an uncertain create.
- `--project <id-or-exact-name>` selects a project; `--project none` clears it. Use the ID from `projects create` or `projects list`; duplicate names require an ID. Only current-device project folders are granted to local tasks; folders bound to another app/device are not reused. Selecting a project does not edit its folders.
- `--enterprise-knowledge` selects the official 企业知识 skill using the live catalog. Repeat it on each desired turn. Missing account/runtime availability fails before sending. Omitting it does not revoke tools or knowledge already available to the model.
- All three context flags require a message and support attachments. The result's `context` records the submitted choice. Cloud rejects MCP, workspace, local skill and permission flags.
- `--workspace <path>` overrides the local working directory. Otherwise use the project's current-device primary folder, inherited session workspace, or a new app chat directory. `--no-skills` omits default local skill paths; repeat it when wanted. Agent mode remains enabled; this is not a tool-permission sandbox.
- Prefer `sessions create "first message"` over create-then-send: a conversation id exists only after the first message.
- Ordinary session, model and MCP commands run in the background. Do not run `sessions open` before sending or reading; it uses a deep link and can briefly change focus. A missing chat page fails explicitly without opening a window. Launching or restarting the app with `cdp launch` may show its window.
- Prefix the message with `--` when it begins with option-like text: `doubao sessions send <id> -- "--model means what here"`.
- `--profile "Profile 1"` accepts a directory or display name. Messaging, model and connector commands require that profile to be active in the selected app; switch it in the app first.
- Repeat `--attach <path>` for attachments (max 50 files, 100 MiB each). The CLI uploads through the app's drop path and confirms the upload before sending; the app's formatter encodes uploads for the direct protocol path. Sending preserves existing composer text and removes only its own staged uploads.
- The composer auto-inserts spaces at CJK/latin boundaries; verify content with `sessions read` rather than raw string comparison.

## Local MCP tools

MCP depends on app internals. The dual-app implementation was tested on DoubaoWork 2.30.5 and Doubao 2.30.2, including real tool execution through automatic fallback with Work absence simulated. If the local runtime is unavailable, select **本地电脑** in a work task and let it initialize, then retry readiness checks.

```bash
# Register an existing stdio MCP server; returns connectorId after READY.
doubao mcp register my-tools --command "$(command -v node)" --arg /absolute/path/server.mjs --json
doubao mcp list --json

# Replace the ids with values returned by register and create.
doubao sessions create "Call my_tool with ..." --mcp <connector-id> --wait --json
doubao sessions send <conversation-id> "Call my_tool again with ..." --mcp <connector-id> --wait --json

doubao mcp remove <connector-id> --json
doubao mcp list --json
```

- Use absolute executable and server paths. Repeat `--arg` for arguments and `--env KEY=value` for environment variables; the app starts the server.
- Pass every required `--mcp <connector-id>` on **each turn**, including follow-ups. A message and `--wait` are required so the sandbox binding completes. `--mcp` cannot be combined with `--attach`.
- MCP turns inherit the workspace; use `--workspace /absolute/path` to override it and repeat `--no-skills` when wanted.
- `--permission FullAccess|AskOnRisk|AlwaysAsk` sets execution permission for a turn with `--mcp` or `--runtime local`. Default: `FullAccess` (no additional approval). `AskOnRisk` and `AlwaysAsk` request Doubao's corresponding approval policies; respond to approval requests in the app. Repeat the flag on each turn; omitting it returns to `FullAccess`. Doubao 2.30.1 handles `connector.call` separately from native command approval, so this does not guarantee approval for every MCP call or restrict the server process itself. Requires CLI 0.9.0 or newer.
- Connectors are account-level. `mcp remove` verifies an absent/disabled account entry and removal from the selected app's tool catalog. A failed readback is reported as unconfirmed; check `mcp list` before retrying.
- Verify tool execution from the server's actual result or log, not just the model's claim. Do not automatically resend a timed-out request that may already have run a tool.

## Model values

Use the exact `name` from `doubao models --json` or `doubao headless models --json`. Quote names with spaces: `--model 'Orange 5.5'`.

Reasoning effort levels: `low` (低), `medium` (中), `high` (高), `xhigh` (极高), `max` (最高). `--reasoning` on `sessions send` requires `--model`; `model reasoning <level>` changes the current session without switching models.

## Environment overrides

- `DOUBAO_APP` — explicit application path; overrides automatic selection. `--platform work|doubao` selects the other variant when specified.
- `DOUBAO_DATA_DIR` — selected app user-data directory override
- `DOUBAO_CDP_ENDPOINT` — CDP endpoint (Work: `http://127.0.0.1:9226`; Doubao: `http://127.0.0.1:9225`). An endpoint belonging to the other app is rejected.
- `DOUBAO_CLI_CONFIG_DIR` — CLI settings directory
- `DOUBAO_CLI_DISABLE_AUTO_UPDATE=1` — disable reminders and automatic updates; explicit `update` and `update check` still work

## Troubleshooting

- `Doubao CDP is unavailable` → use the CDP launch procedure above.
- `Doubao connectors are not ready` → check the id with `mcp list` and the connector's local status in the app; list output alone does not prove READY.
- `no Doubao chat page found` → CDP is up but no chat window exists. Ask the user to open a chat window in the selected app, then retry; do not silently run `sessions open` as recovery.
- Missing requested turn in history → the lookup is limited to the latest 100 main-conversation messages; do not substitute a newer turn. Full child lists/event streaming are not CLI features yet.
- Commands break after an app update → the app changed its DOM/API surface; run `doubao update check` for a fixed CLI release.
- CDP is unauthenticated but bound to 127.0.0.1; quit and relaunch Doubao normally when automation is no longer needed.

Session management commands also support the `headless` prefix, `--profile`, and `--timeout`. Use project IDs when names are duplicated; `none` clears the project assignment. Changes read server state before writing and confirm it afterward. `verified: false` means the result is uncertain; inspect the session before retrying. Writes are never automatically retried.
