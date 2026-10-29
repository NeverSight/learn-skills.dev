---
name: cache-keep
description: Use when the user asks whether Cache Keep is working, what it did in this conversation, or how to change its settings.
license: MIT
---

# Cache Keep

Cache Keep is the Claude Code plugin beside this file. It works on its own in
every conversation of the project it is installed in; nothing needs to call it.

- An idle conversation is pinged 55 minutes after its last request, so its
  one-hour prompt cache stays warm. After 5 pings it is compacted when that
  leaves under 60% of it; otherwise it gets one last ping.
- Each ping and compaction is logged to `~/.claude/cache-keep/<session id>.log`.
- In Claude Desktop it runs a background `sleep` while pings are due, so
  Desktop does not stop the idle conversation; it stops the sleep afterwards.
- Settings are per user: Cache Keep in Claude Code's config menu, or
  `pluginConfigs` > `cache-keep@skills-dir` > `options` in
  `~/.claude/settings.json` (`enabled`, `pingMinutes`, `pings`,
  `compactBelowPercent`).
