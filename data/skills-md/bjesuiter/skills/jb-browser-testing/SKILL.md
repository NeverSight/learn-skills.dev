---
name: jb-browser-testing
description: Private browser testing rules for jb workflows. Prefer playwrighter_exec with careful tab selection, fall back to agent-browser, and avoid playwright-mcp.
skill_author: bjesuiter@gmail.com
private: true
---

# JB Browser Testing

Private skill for personal use. Do not publish.

## Rules

- **Primary**: Use the `playwrighter_exec` skill when possible. It may control multiple tabs from different projects, so confirm the right tab (port and main page heading) before acting.
- **Fallback**: Use the `agent-browser` skill (by vercel) when `playwrighter_exec` is unavailable or unsuitable.
- **Avoid**: Do not use `playwright-mcp` OR `playwright - opencode (built-in)` because it is token heavy.
