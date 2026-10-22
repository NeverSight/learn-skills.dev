---
name: weapp-driver
description: Drive and debug WeChat Mini Programs through a fast batch JavaScript runtime with persistent automator sessions, semantic WXML snapshots, element refs, waits, logs, screenshots, wx API calls, and official wechatide tools. Use when an agent needs to inspect or operate a Mini Program, reproduce bugs, validate UI flows, or collect runtime evidence.
category: '测试工具'
tags: node, typescript, miniapp, wechat
---

# WeApp Driver

Use `weapp nodejs` to compose multiple Mini Program actions into one JavaScript execution. Prefer this runner over many separate `wechatide` calls for high-frequency page work; use `devtools` helpers for official project, compile, log, preview, upload, and cloud capabilities.

## Preconditions

- Require a valid absolute Mini Program project path.
- Require WeChat DevTools to be installed, logged in, and automation/CLI access enabled.
- Run `weapp doctor` only for setup or connection diagnosis, not before every task.
- Read [setup.md](references/setup.md) when installation or connection fails.

## Default workflow

1. Reuse the project session with `useProject(projectPath)`.
2. Navigate to a deterministic route.
3. Observe with `page.snapshot()` before acting.
4. Act with a current `@N` ref or emitted stable `loc=css:...` locator.
5. Wait for state, route, or selector inside the daemon.
6. Verify with page data, runtime info, logs, and screenshot.
7. Keep the session for follow-up work; call `completeProject({ keep: false })` only when the task is genuinely finished.

For a connection and page-level smoke check, prefer the built-in command:

```bash
weapp smoke --project /absolute/path/to/miniprogram \
  --route /pages/index/index \
  --screenshot /tmp/weapp-smoke.png
```

For a requested feature flow, translate the acceptance criteria into one batch script. Record assertions with `test.check`, `test.equal`, or `test.match`, then print `test.report(...)`. Include the final route, relevant page data or text, runtime errors, and a screenshot path. Do not claim success from a click completing without verifying the resulting state.

```bash
weapp nodejs <<'EOF'
await useProject('/absolute/path/to/miniprogram')
await mini.reLaunch('/pages/order/detail?id=123')

console.log(await page.snapshot({ includeLayout: true }))
await page.click('@12')
await page.waitForData('loading', false, { timeoutMs: 10000 })

console.log({
  info: await mini.info(),
  errors: await logs.errors(),
  screenshot: await page.screenshot('/tmp/order-detail.png'),
})
EOF
```

## Observation and targeting

- Use `page.snapshot()` for a compact semantic page view.
- Use `page.exists(selector)` or `page.count(selector)` for presence checks. `page.query(selector)` returns a snapshot object even when `refs` is empty; do not use object truthiness as a match check.
- Treat names in `ref.opaqueAttributes` as lossy WXML serialization. Read the runtime value with `page.property(ref, name)` or, for component state, `component.data(ref)`; do not parse `[object Object]` as JSON.
- Treat `@N` refs as short-lived: any later snapshot/query rebuilds the valid ref set.
- Prefer emitted `loc=css:#id`, `data-testid`, or `data-qa` locators across page updates.
- Use raw CSS when the project already has stable QA selectors.
- Use `text=...` or `loc=role:button[name="..."]` only when a unique match is expected.
- On ambiguous matches, refine the selector; do not retry unchanged.

## Batch execution

Combine dependent actions, waits, extraction, and verification in one heredoc. Split rounds only when the next action depends on fresh model inspection or manual user input.

Use:

- `mini` for routes, AppService evaluation, wx APIs, screenshot, and scrolling.
- `page` for snapshot, elements, page data, methods, and waits.
- `component` for custom-component snapshots, runtime data, `setData`, and methods. Start with a page ref or stable selector; use `component.query(parent, selector)` to enter an opaque component boundary.
- `logs` for persistent console/exception entries.
- `devtools` for official `wechatide` operations.

Read [api.md](references/api.md) for the complete helper surface.

## User-facing invocation

This Skill may be selected automatically for Mini Program testing requests. The user can force it with a prompt such as:

```text
使用 $weapp-driver 测试 /absolute/path/to/miniprogram：进入商品详情页，点击立即购买，填写收货信息，验证提交后进入确认订单页；不要真实付款。输出每一步 pass/fail、console 错误和截图路径。
```

Treat exclusions such as “不要真实付款” as hard boundaries. Stop before an action that would create an order, charge money, publish, upload, or otherwise mutate external state unless the user explicitly requested that action.

## Manual handoff and concurrency

Only one agent process controls a project session at once.

- Call `handOffProject()` before asking the user to interact manually.
- Do not reclaim automatically.
- After explicit user confirmation, call `claimProject(projectPath)`.
- Surface `SESSION_BUSY` or `SESSION_USER_IN_CONTROL` without retry loops.

## Official DevTools operations

Use `devtools.call(tool, args)` for registered official tools. Prefer convenience helpers for refresh, page opening, screenshot, console, network, preview, and upload. Never bypass official authorization or confirmation. When a call returns `status: "pending"`, stop and surface the authorization request; do not retry it or replace it with repeated page reloads.

Before the first `devtools` call, follow the installed official `wechatide-skill` readiness/version/token gate. Do not invent or hardcode the official Skill version.

## Failure handling

- Retry only transient missing/detached elements within the requested timeout.
- Element reads wait up to 5 seconds by default. For an optional element, check `page.exists()` first or pass a shorter `timeoutMs`.
- Fail immediately on invalid or multi-match selectors.
- After a timeout, collect current route, a fresh snapshot, errors, and screenshot before changing strategy.
- If the automator connection closes, run `weapp doctor`, verify DevTools is still open, then reuse the project session.
- Keep the daemon and project session alive across test rounds. When the default Automator port already belongs to the same AppID, the runtime reuses it instead of launching another authorization flow.
- Read [troubleshooting.md](references/troubleshooting.md) for known recovery paths.
