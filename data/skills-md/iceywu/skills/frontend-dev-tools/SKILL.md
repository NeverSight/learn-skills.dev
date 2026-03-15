---
name: frontend-dev-tools
description: Use this skill when users ask to run/open/preview/debug a frontend project (including Chinese intents like 运行/打开/预览/调试). Enforce MCP browser tools (Playwright/Chrome DevTools) first, then fallback only if MCP is unavailable.
metadata:
  author: IceyWu
  homepage: https://github.com/IceyWu
  version: "0.1.0"
  source: https://github.com/IceyWu/skills
---

# Frontend Development Tools & Workflow

Use this skill to standardize frontend run/open/preview/debug tasks.

## 1. Trigger (Hard)

Apply this skill when the user intent includes frontend **run/open/preview/debug**.

Examples of hard triggers:

- English: run, open, preview, debug (frontend project/app/page)
- Chinese: 运行、打开、预览、调试（前端项目/页面）

## 2. Required Flow (MCP First)

For hard-trigger requests, execute in this order:

1. Start or confirm dev server (for example `pnpm dev`).
2. Use MCP browser tools first: `mcp_microsoft_pla_browser_*` or `mcp_chrome-devtoo_*`.
3. Verify at least one visible UI signal (title, heading, or key element).
4. Report result after verification.

Rules:

- If MCP browser tools are available, they are mandatory as the primary path.
- Do not finish the task with terminal startup logs only.

## 3. Fallback Policy

Fallback is allowed only when MCP path is unavailable or failed.

- You may use terminal checks and `open_simple_browser` as fallback.
- You must explicitly state the blocker (for example: MCP browser runtime unavailable).
- You should attempt recovery first when possible (for example install browser/runtime), then fallback.

## 4. Quick Example: “运行/打开项目”

1. Start server (`pnpm dev` or equivalent).
2. Open local URL via MCP browser tool.
3. Verify page signal (e.g., title/h1).
4. Then return completion status.
