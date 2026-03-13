---
name: dev-browser
description: Browser automation with persistent page state. Use when users ask to navigate websites, fill forms, take screenshots, extract web data, test web apps, or automate browser workflows. Trigger phrases include "go to [url]", "click on", "fill out the form", "take a screenshot", "scrape", "automate", "test the website", "log into", or any browser interaction request.
---

# Dev Browser Skill

Use `dev-browser` CLI to run multi-step browser automation with persistent page state.

## Defaults

- **Prefer multi-step execution**: Use one `run --code` block for multiple actions whenever possible.
- **Reuse page names**: Keep the same `--page` name across turns to preserve state.
- **Control via daemon commands**: Explicitly use `ensure/status/stop/clean`.
- **CLI must be available**: Ensure `dev-browser` command is installed and on `PATH` (from the separated CLI package).

## Setup

If `dev-browser` command is missing, install CLI globally:

```bash
pnpm add -g @jtsang/dev-browser-cli
# or: npm install -g @jtsang/dev-browser-cli
```

Ensure daemon is running before actions:

```bash
dev-browser daemon ensure --mode launch --json
# optional: choose launch engine (default: patchright)
dev-browser daemon ensure --mode launch --engine playwright --json
```

Use extension mode when user wants their existing Chrome session:

```bash
dev-browser daemon ensure --mode extension --json
```

Useful lifecycle commands:

```bash
dev-browser daemon status --json
dev-browser daemon stop --mode launch
dev-browser daemon clean --stale-only
dev-browser doctor
```

## Run Multi-Step Scripts

Use `run --code` as the primary execution command.

```bash
dev-browser run --mode launch --page checkout --json --code '
await page.goto("https://example.com");
await helpers.waitForPageLoad(page);
await page.fill("input[name=email]", "test@example.com");
await page.click("button[type=submit]");
return { url: page.url(), title: await page.title() };
'
```

### Execution Context

`--code` runs as async JavaScript function body with injected values:

- `page` - persistent Playwright `Page` for `--page` name
- `client` - dev-browser client instance
- `helpers` - utility helpers (`waitForPageLoad`)
- `log(entry)` - structured step logs collected in output

### Output Contract

Success (`ok: true`) includes:

- `mode`
- `pageName`
- `data` (your returned value)
- `logs`
- `timingMs`

Failure (`ok: false`) includes:

- `error.code` (`RUN_TIMEOUT` or `RUN_EXEC_ERROR`)
- `error.message`
- `error.retryable`

## Workflow Pattern

For complex tasks:

1. `daemon ensure`
2. Run one multi-step `run --code`
3. Evaluate JSON result
4. If needed, run another `run --code` with same `--page`
5. On completion, `daemon stop` (or rely on idle TTL)

## Page State Inspection

Use `run --code` for debugging snapshots/screenshots:

```bash
dev-browser run --page debug --json --code '
await page.screenshot({ path: "debug.png", fullPage: true });
const snapshot = await client.getAISnapshot("debug");
return { url: page.url(), title: await page.title(), snapshot };
'
```

## Notes

- `run --code` accepts JavaScript only (no TypeScript syntax inside code body).
- Same `--page` name is serialized by lock to prevent concurrent mutation conflicts.
- Runtime data is stored under `~/.dev-browser/` (override with `DEV_BROWSER_HOME`).
