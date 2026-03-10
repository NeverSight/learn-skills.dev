---
name: bump-hal-voice-version
description: (hal-9000) Use when editing any file under plugins/hal-voice/ to bump the plugin version before committing
user-invocable: true
model: haiku
allowed-tools:
  - Glob
  - Read
  - Edit
---

# Bump hal-voice Version

After editing files under `plugins/hal-voice/`, bump the `version` field in both files using semver:

1. `plugins/hal-voice/.claude-plugin/plugin.json`
2. `.claude-plugin/marketplace.json` (the `plugins[].version` for hal-voice)

- **Patch** (0.2.0 -> 0.2.1): bug fixes, config changes, style cleanup
- **Minor** (0.2.0 -> 0.3.0): new features, new hooks, new commands
- **Major** (0.2.0 -> 1.0.0): breaking changes to hook behavior or config format

Bump once per commit session, not per file edit.
