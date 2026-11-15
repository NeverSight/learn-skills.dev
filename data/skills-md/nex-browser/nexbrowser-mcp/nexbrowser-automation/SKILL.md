---
name: nexbrowser-automation
description: Use whenever the user explicitly names NexBrowser/nexbrowser or asks to use NexBrowser OpenAPI, including listing or counting managed windows/environments/profiles (查看有多少窗口、查询环境), connecting to a managed window, navigation, clicking, typing, uploading, scraping, screenshots, tabs, or NexBrowser automation debugging. Route these requests to NexBrowser MCP tools, never generic Browser, Chrome, or computer-use tools.
---

# NexBrowser Automation Skill

Use this skill whenever the user names NexBrowser or needs to manage or automate a live NexBrowser session through the unified NexBrowser MCP tools.

## When to Use

- The user explicitly says NexBrowser/nexbrowser, NexBrowser OpenAPI, “使用 NexBrowser”, “查看有多少窗口”, “查询环境”, or “浏览器环境”.
- The user wants to list or count managed NexBrowser windows/environments/profiles. Call `nex_browser_list`; do not inspect Chrome, Edge, the Codex in-app browser, operating-system windows, processes, or tabs.
- The user wants to control a browser: navigate, click, type, scroll, upload, or scrape.
- The task needs element targets from an accessibility snapshot.
- The task needs help diagnosing a browser-automation failure.

## Quick Decision Matrix

| User intent              | Tool                                                                                                             | Notes                                                                                                            |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| List/count environments  | `nex_browser_list`                                                                                               | NexBrowser managed windows only; never OS windows or tabs.                                                       |
| Import custom proxies    | `nex_proxy_import`                                                                                               | Only with proxy lines the user pasted in the current request; credentials are never returned.                    |
| Create or edit a proxy   | `nex_proxy_create`, `nex_proxy_batch_create`, `nex_proxy_modify`, `nex_proxy_delete`, `nex_proxy_detect`         | Structured host/port create; delete is destructive. Credentials are never returned.                              |
| List proxies             | `nex_proxy_list`                                                                                                 | Select a proxyId for create or bind; credentials are never returned.                                             |
| Bind a proxy             | `nex_browser_bind_proxy`                                                                                         | Closed windows only; `proxyId=0` removes the binding.                                                            |
| Manage window groups     | `nex_browser_group_list`, `nex_browser_group_create`, `nex_browser_group_modify`                                 | Group 0 is the ungrouped bucket and cannot be renamed or deleted.                                                |
| Manage platform accounts | `nex_account_list`, `nex_account_create`, `nex_account_batch_create`, `nex_account_modify`, `nex_account_delete` | Workspace catalog only; secrets are never returned. Open-window vault fill still uses `nex_browser_accounts`.    |
| Bind a platform account  | `nex_browser_bind_account`                                                                                       | Closed windows only; replaces the window binding. `accountIds=[]` removes it.                                    |
| Create environments      | `nex_browser_create`                                                                                             | Desktop defaults fill every field you omit; only override on request.                                            |
| Open environments        | `nex_browser_open`                                                                                               | Pass all target IDs in one array when opening multiple windows.                                                  |
| Connect to NexBrowser    | `nex_browser_connect`                                                                                            | Requires a managed window ID; the active team is used by default.                                                |
| Navigate to a URL        | `nex_browser_navigate`                                                                                           | Use for an initial or explicitly supplied URL.                                                                   |
| Inspect elements         | `nex_browser_snapshot`                                                                                           | Preferred over a screenshot for interaction.                                                                     |
| Click, type, or select   | `nex_browser_click`, `nex_browser_type`, `nex_browser_select_option`                                             | Use snapshot `target` values.                                                                                    |
| Sign in to a platform    | `nex_browser_accounts`, `nex_browser_fill_account`, `nex_browser_fill_credentials`                               | Prefer a stored vault credential; use literal values only when the user explicitly supplies or asks to use them. |
| Wait for a page change   | `nex_browser_wait_for`                                                                                           | Prefer `text` with `timeout` over fixed `time`.                                                                  |
| Read structured data     | `nex_browser_evaluate`                                                                                           | Prefer UI tools for state-changing actions.                                                                      |
| Inspect visual state     | `nex_browser_take_screenshot`                                                                                    | Use when layout or rendered media matters.                                                                       |
| Click without a ref      | `nex_browser_take_screenshot`, `nex_browser_mouse_click_xy`                                                      | Image grids, canvas, extension overlays; map image coordinates with the returned origin and scale.               |
| Verify by SMS            | `nex_sms_project_list`, `nex_sms_buy`, `nex_sms_code_fill`, `nex_sms_release`                                    | `nex_sms_buy` charges the balance directly for the requested task.                                               |
| Debug failures           | `nex_browser_console_messages`, `nex_browser_network_requests`                                                   | Inspect after reproducing the issue.                                                                             |

## Critical Rules

### Routing and sessions

- Treat the NexBrowser product name as an explicit routing request for this MCP server. Never substitute generic Browser/Chrome plugins, computer-use, shell commands, or process enumeration.
- For one window, connect with `nex_browser_connect`; set `startIfNeeded=true` only when the user also wants the stopped window opened.
- For multiple windows, call `nex_browser_open` exactly once with every target ID in the `windowId` array. Wait for its per-window results, then call `nex_browser_connect(startIfNeeded=false)` once for each successfully opened window. Never use repeated `nex_browser_connect(startIfNeeded=true)` calls to launch a multi-window task.
- Retain every returned `sessionId` and pass it explicitly to subsequent tools for that window. The implicit active session only identifies the most recently connected window.
- If Desktop reports a per-client session-limit error, process windows in bounded waves: connect only up to the allowed limit, finish and disconnect those sessions, then continue with the next wave. Do not reopen windows between waves.
- Pass `teamId` only when it is already known. Never pass a raw CDP endpoint.

### Snapshots and interaction

- Call `nex_browser_snapshot` before the first target-based interaction and use its ref, such as `target: "e48"`; a unique CSS selector is a fallback. Multiple actions may reuse the same snapshot only while the page structure remains stable.
- Snapshot refs are temporary. Re-snapshot after navigation, an action that changes the DOM, a substantial asynchronous update, or any stale-reference error.
- Prefer visible controls: click links, buttons, filters, and pagination before using direct navigation or JavaScript.
- For sensitive flows such as login, upload, checkout, or account changes, slow down: operate visible controls step by step, verify each result, and preserve confirmation steps (see `guides/human-like-interaction.md`).
- Wait and verify after every state-changing action. Prefer observable text waits over fixed delays.
- Treat `nex_browser_evaluate` as an inspection and extraction tool; use it to change page state only when the normal UI cannot be operated. `nex_browser_evaluate` and `nex_browser_run_code` are permission-gated by the NexBrowser Desktop app.

### Sign-in and credentials

Order of preference: `nex_browser_fill_account` for a bound vault credential; `nex_browser_fill_credentials` only for literal values the user supplied. If `nex_browser_fill_account` fills nothing, snapshot the form to see where the fields are and retry once; then stop and ask the user. Never fall back to clicking the vault extension's dropdown or typing a stored secret.

- To sign in with a stored credential, open and connect the window, call `nex_browser_accounts` for an `accountId`, then call `nex_browser_fill_account` with that ID only. The vault plugin chooses visible fields and keeps passwords and 2FA secrets outside MCP. Call it again after each navigation in a multi-step sign-in. Never type a stored credential with `nex_browser_type` or `nex_browser_fill_form`, and never repeat one back. The tool does not submit; click the visible submit control yourself after verifying the filled state.
- Use `nex_browser_fill_credentials` only when the user explicitly supplies literal credentials in the current request or explicitly asks you to use them. Treat a login account, password, TOTP retrieval URL, recovery email, recovery-email password, and email login URL supplied together as one ephemeral credential bundle. Do not persist a bundle, and do not assign multiple bundles to windows unless the mapping is explicit. Literal values enter the model and MCP request boundary: never store, log, or repeat them in a response. The tool fills only current visible targets and never submits; snapshot each changed step before filling.
- If a sign-in requests a code available at a user-supplied retrieval URL, retain the login page ID, open the URL in a temporary tab, and accept a code only when exactly one current code is unambiguous. Close the temporary tab, reselect the login page, snapshot again, and fill the code with `nex_browser_fill_credentials`. A user-supplied retrieval URL is the only allowed URL exception for embedded secret material; never copy it into prose or logs.
- If a sign-in requires a recovery-email code, open the explicitly supplied email login URL in a temporary tab and fill the explicitly supplied email address and password only with `nex_browser_fill_credentials`. Accept only one message/code that is clearly tied to the current sign-in. On CAPTCHA, first follow the [NexCaptcha page workflow](guides/captcha.md). Stop on human confirmation, device approval, an SMS challenge to a number that is not a NexBrowser cloud number, an ambiguous code, or an inaccessible page. Close the email tab before returning to the retained login page. See [Sign-in with literal credentials](examples/sign-in-with-literal-credentials.md).

### Paid actions

- For a page CAPTCHA, default to `nex_captcha_product_list` → `nex_captcha_product_schema`. Collect real challenge inputs in the original page/frame with permitted browser tools according to `schema` and `integration.inputSources`. Read the result contract and confirm how to apply the answer before paying. Use free `nex_captcha_detect` with the actual URL, product code, adapter and applicable workflow. Set `canApply: true` only after confirming that application path. Use the validated arguments with `nex_captcha_buy`, poll `nex_captcha_query`, then apply the documented result with existing browser tools and verify website acceptance. HTML auto-detection and `nex_captcha_apply_result` are optional shortcuts for reCAPTCHA v2/enterprise and Turnstile. The fixed Desktop bridge remains optional. See [workflow selection and capability boundaries](guides/captcha.md#choose-the-integration-workflow).

- When using nexbrowser-mcp for browser tasks, reuse the selected NexBrowser environment or call `nex_browser_list` and `nex_browser_connect(windowId, startIfNeeded=true)`. Preserve its session, page/frame and filled form. Never bypass disabled evaluate/runCode permissions with raw CDP or shell/browser scripts, or substitute local image matching for NexCaptcha recognition. Missing fixed-bridge capture alone does not prohibit a permitted agent integration. Missing inputs, unsupported observed parameters such as an undeclared `s`, HTTP 403 and timeouts never justify ignoring the online contract, dropping required data or switching to GRID.

- Proxy market, mailbox, CAPTCHA and billing tools use `nex_ip_*`, `nex_mail_*`, `nex_captcha_*` and `nex_billing_*` within this same server. Every CAPTCHA charge remains in NexCaptcha; HTML detection/result generation are free and do not execute code. `nex_captcha_apply_result` requires a matching task bought in this MCP process; after restart, query/reconcile that existing task and use an explicit integration, never buy again to restore the binding. When suitable, the optional `nex_browser_captcha_prepare`/`nex_browser_captcha_submit`/`nex_browser_captcha_complete` route handles captured widgets and real supported Grid challenges. Other products require their online contract plus explicit agent integration or a fixed adapter; `HTTP_SUBMIT` requires an established site HTTP integration. See [page CAPTCHA](guides/captcha.md) and [service workflows](guides/services.md).
- Purchases, renewals and quota extraction needed for the user's task charge directly at the current server price without a quotation stage or separate payment confirmation. Honor user limits and resource scope. A price, availability or plan inquiry alone must never place an order. Interactive recovery continues without repeated approval: SMS waits 120 seconds, email waits 180 seconds; confirmed no-code/no-mail, proxy failure or CAPTCHA FAILED/EXPIRED/site rejection permits a compatible replacement or fresh challenge, at most 3 attempts including the first. Track rejected country/product/domain candidates and preserve user constraints. Release eligible task-owned numbers and bind replacement proxies without asking again. Show progress. Purchase/application timeouts require records/billing reconciliation and block new charges while unknown; -1208/insufficient balance stops paid operations. See [service recovery](guides/services.md).

- When the user asks to verify a site with a NexBrowser cloud phone number, select a project from `nex_sms_project_list` and call `nex_sms_buy` directly (it charges the account balance). After triggering the site's send-code control, fill the code with `nex_sms_code_fill` so it goes straight into the page. Release unusable numbers with `nex_sms_release`. See [SMS verification code](examples/sms-verification-code.md).

### Finishing a task

- When the task is finished (or abandoned), call `nex_browser_disconnect` for every session you opened. It clears the in-window "Nex Agent is operating" overlay and keeps the window open. Skip it only when the user says more steps will follow right away.

## Starter Workflow

Single window:

```text
1. nex_browser_connect(windowId="WINDOW_ID", startIfNeeded=true)
2. nex_browser_navigate(url="https://example.com")
3. nex_browser_wait_for(text="expected content")   # or time=2000 (milliseconds) as a fallback
4. nex_browser_snapshot()
```

Multiple windows:

```text
1. nex_browser_open(teamId="TEAM_ID", windowId=["WINDOW_1", "WINDOW_2", "WINDOW_3"])
2. nex_browser_connect(windowId="WINDOW_1", startIfNeeded=false) -> retain SESSION_1
3. nex_browser_connect(windowId="WINDOW_2", startIfNeeded=false) -> retain SESSION_2
4. nex_browser_connect(windowId="WINDOW_3", startIfNeeded=false) -> retain SESSION_3
5. Call automation tools with the matching explicit sessionId.
```

## Out of Scope

Do not invent tools for the following — they are outside this skill's scope; route the user instead:

- Deleting or editing existing browser environments/profiles or resetting fingerprints — not available through this MCP server; direct the user to the NexBrowser app. Creating new environments is available through `nex_browser_create`. Custom proxies use `nex_proxy_import`, `nex_proxy_create`, `nex_proxy_modify`, `nex_proxy_delete`, and `nex_proxy_detect`; binding or removing a proxy on a closed window uses `nex_browser_bind_proxy`.
- Reading credential secrets — workspace catalog tools (`nex_account_*`) and `nex_browser_accounts` never return passwords or 2FA secrets. Catalog create/modify may accept write-only secrets the user supplied in the current request. Literal credential filling is one-time form filling only; it does not persist an account unless the user also asks for `nex_account_create`.
- Raw CDP or WebSocket connections — never pass a CDP endpoint to an automation tool; `nex_browser_connect` with a `windowId` is the only automation entry point. Environment-management tools redact CDP endpoints by default; the operator-only `NEX_EXPOSE_CDP=1` mode is outside this skill workflow.
- Cookie export, UA queries, or profile sharing — not part of this tool set.
- Environment lifecycle (`nex_browser_list`, `nex_browser_create`, `nex_browser_open`, `nex_browser_close`, `nex_browser_connection_info`, `nex_browser_accounts`) manages windows only; it cannot automate pages. Page automation always requires `nex_browser_connect` first.

## Progressive Disclosure

| Reference                                                                          | When to use                                                                            |
| ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| [Tool catalog](references/tool-catalog.md)                                         | Confirm a tool's exact name, inputs, and read-only status.                             |
| [Tool selection](guides/tool-selection.md)                                         | Unsure which interaction tool fits the intent.                                         |
| [Snapshot modes](guides/snapshot-modes.md)                                         | Targets are stale or snapshots are too large.                                          |
| [Waiting and timing](guides/waiting-and-timing.md)                                 | Flaky results after navigation or slow pages.                                          |
| [Human-like interaction](guides/human-like-interaction.md)                         | Sensitive flows needing cautious pacing.                                               |
| [Error handling](guides/error-handling.md)                                         | A tool returned an error and the hint is not enough.                                   |
| [Examples](examples/connect-and-navigate.md)                                       | Full workflow templates for common tasks.                                              |
| [Sign-in with a bound account](examples/sign-in-with-bound-account.md)             | The task needs a platform login for a window.                                          |
| [Sign-in with literal credentials](examples/sign-in-with-literal-credentials.md)   | The user explicitly provides credentials and a one-time retrieval-code flow is needed. |
| [SMS verification code](examples/sms-verification-code.md)                         | A site needs a phone number and SMS code from a NexBrowser cloud number.               |
| [Image grids and extension overlays](examples/image-grid-and-extension-overlay.md) | Controls without snapshot refs: image grids, canvas, page-injected extension menus.    |

## NexBrowser Integration

Discover the target `windowId` with `nex_browser_list`, which is part of this same MCP server, then connect with `nex_browser_connect` and use this skill for live automation. The NexBrowser Desktop app validates ownership and resolves the browser connection internally.

`teamId` scopes browser discovery and lifecycle operations to a NexBrowser Team. When it is omitted
from tools that allow omission, Desktop uses the currently selected Team. This MCP does not list or
modify Teams or Projects, so never invent a `teamId`; use an ID already supplied by the user or
Desktop context.
