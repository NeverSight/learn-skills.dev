---
name: ctx-upgrade
description: |
  Update context-mode from GitHub and fix hooks/settings.
  Pulls latest, builds, installs, updates npm global, configures hooks.
  Trigger: /context-mode:ctx-upgrade
user-invocable: true
---

# Context Mode Upgrade

Pull latest from GitHub and reinstall the plugin.

## Instructions

1. Derive the **plugin root** from this skill's base directory (go up 2 levels — remove `/skills/ctx-upgrade`).
2. Run with Bash:
   ```
   CLI="<PLUGIN_ROOT>/cli.bundle.mjs"; [ ! -f "$CLI" ] && CLI="<PLUGIN_ROOT>/build/cli.js"; node "$CLI" upgrade
   ```
3. **IMPORTANT**: After the Bash tool completes, re-display the key results as markdown text directly in the conversation so the user sees them without expanding the tool output. Format as:
   ```
   ## context-mode upgrade
   - [x] Pulled latest from GitHub
   - [x] Built and installed v0.9.13
   - [x] npm global updated
   - [x] Hooks configured
   - [x] Permissions set
   - [x] Doctor: all checks PASS
   ```
   Use `[x]` for success, `[ ]` for failure. Show the actual version numbers and any warnings.
   Tell the user to **restart their Claude Code session** to pick up the new version.
