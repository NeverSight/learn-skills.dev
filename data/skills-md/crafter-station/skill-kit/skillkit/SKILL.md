---
name: skillkit
version: 0.14.0
description: "Local-first analytics and structural audits for AI agent skills. Use when reviewing skill health, context cost, private local or Tailscale-remote usage receipts, conflicts, coverage, token burn, or pruning."
allowed-tools: Bash(skillkit:*), Bash(bunx @crafter/skillkit:*)
hidden: true
---

# skillkit

This file is a discovery stub. Load the version-matched workflow from the installed CLI before running skillkit commands:

```bash
skillkit skills get core
skillkit skills get core --full
```

The first command returns the operating workflow. Use `--full` when exact flags, JSON fields, CI behavior, or the complete command catalog matter.

The CLI ships its own skill content, so the instructions match the installed skillkit version. Run `skillkit skills list` to see the bundled catalog.

If `skillkit` is unavailable, install it with Bun:

```bash
bun add -g @crafter/skillkit
```
