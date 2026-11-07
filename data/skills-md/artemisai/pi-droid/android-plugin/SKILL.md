---
name: android-plugin
description: Manage and execute app-specific plugins — install, configure, run actions, check status, approval workflows
---

## When to use

Use this skill when automating a specific app that has a dedicated plugin (e.g., messaging apps, social apps). Plugins wrap app-specific logic behind a standard interface with approval gates for sensitive actions.

## Tools

| Tool | Purpose |
|------|---------|
| `android_plugin_action` | Execute a plugin action (e.g., `weather.fetch`, `telegram.send`) |
| `android_plugin_status` | Get status of all loaded plugins (ready/offline, rate limits) |
| `android_plugin_cycle` | Run a plugin's autonomous heartbeat cycle |
| `android_skills` | Discover all plugin capabilities and their parameters |

## Plugin action workflow

1. **Discover capabilities:** `android_skills { format: "markdown" }`
2. **Check plugin health:** `android_plugin_status`
3. **Execute action:** `android_plugin_action { plugin: "name", action: "capability", params: {...} }`
4. **If approval required:** the system will prompt for confirmation before executing

## Approval gates

Actions marked `requiresApproval: true` trigger a confirmation flow before execution. This applies to actions that:
- Send messages to other people
- Make purchases or financial transactions
- Take irreversible actions (delete, block, unmatch)
- Post content visible to others

Read-only actions (status checks, profile viewing) execute immediately.

## Plugin lifecycle

```
plugin.initialize(config)    → Setup and auth
plugin.getStatus()           → Health check (ready/offline/rate-limited)
plugin.execute(action, params) → Run an action
plugin.onHeartbeat()         → Autonomous cycle (check for new activity)
plugin.destroy()             → Graceful shutdown
```

## Example

```
"What plugins are available?" → android_skills { format: "markdown" }
"Check if Telegram is connected" → android_plugin_status
"Run the weather cycle" → android_plugin_cycle { plugin: "weather" }
"Send a message via plugin" → android_plugin_action { plugin: "telegram", action: "telegram.send", params: { text: "Hello" } }
```
