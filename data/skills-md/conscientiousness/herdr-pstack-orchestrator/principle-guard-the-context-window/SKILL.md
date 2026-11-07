---
name: principle-guard-the-context-window
description: "Apply when context is filling up: large outputs, long files, repeated reads, fan-out planning. Route bulk to subagents; keep summaries in the main thread, not raw payloads."
---

## Herdr runtime

Before following the original instructions below, read the sibling [pstack-herdr](../pstack-herdr/SKILL.md) skill and its required mapping. Resolve relative references from this installed skill directory. Use a named sibling skill by reading ../<name>/SKILL.md, because explicit-only siblings are not in the harness skill list. The mapping translates original repository paths to bundled resources; no separate upstream checkout is needed. The Herdr mapping overrides upstream delegation tools, model defaults, setup files, and Cursor-specific capabilities. Delegate only through horch, using workers.toml. Keep workflow coordination in the controller. A bounded worker assignment remains bounded: do not start nested workers. User and project instructions take precedence. Check required capabilities before acting; keep unavailable steps unresolved. For setup-pstack, use the adapter's role setup instead of the original Cursor rule-writing procedure.


# Guard the Context Window

**Why:** Context overflow degrades reasoning quality, creates compression artifacts, and halts progress.

**Pattern:**
- **Size phases and cap scope.** Limit files per phase, set turn budgets, account for mechanism costs.
