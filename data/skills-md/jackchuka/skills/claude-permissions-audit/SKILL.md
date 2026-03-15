---
name: claude-permissions-audit
description: >
  Review and reorganize Claude Code permission settings across all config files
  (global settings.json, project settings.local.json, dotfiles copies). Identifies
  redundancy, misplaced permissions, and lack of read/write organization. Produces
  a clean layout where global settings are the source of truth and project-local
  files only contain project-specific overrides. Use this skill whenever the user
  mentions reviewing permissions, cleaning up settings, auditing allowed tools,
  reorganizing settings.json, or asking "what permissions do I have". Also use when
  adding new MCP servers or tools and wanting to decide what to pre-allow.
  Triggers: "review permissions", "audit settings", "clean up settings.json",
  "permissions audit", "/permissions-audit".
compatibility: Designed for Claude Code
metadata:
  author: jackchuka
  scope: generic
  confirms:
    - modify settings files
---

# Permissions Audit

Review and reorganize Claude Code permission settings so global settings are the
source of truth, project-local files stay minimal, and read vs write operations
have clear separation.

## When to Use

- Reviewing what tools and commands are pre-allowed
- Cleaning up accumulated ad-hoc permission entries
- After adding a new MCP server and deciding which operations to pre-allow
- Ensuring global vs project-local settings are properly split
- Periodic hygiene check on permission sprawl

## Phase 1: Discover All Settings Files

Scan for every settings file that contributes to the effective permission set.

**Locations to check:**
- `~/.claude/settings.json` — global settings (source of truth)
- `<project>/.claude/settings.json` — project shared settings (committed)
- `<project>/.claude/settings.local.json` — project local settings (gitignored)
- `~/.claude/.claude/settings.local.json` — home directory project local
- Any dotfiles-managed copy (e.g. `home/.claude/settings.json` in a dotfiles repo)

Read all of them in parallel. If a file doesn't exist, note it and move on.

## Phase 2: Audit

For each permission entry across all files, assess:

1. **Redundancy** — Is this entry already covered by a broader rule elsewhere?
   - Example: `Bash(gws calendar events:*)` is redundant when `Bash(gws:*)` exists globally
2. **Misplacement** — Is this general-purpose but stuck in a project-local file?
   - Example: `Bash(python3:*)` in project local when it's useful everywhere
3. **Inconsistent granularity** — Are similar tools allowed at different specificity levels?
   - Example: Global has `gh pr list`, `gh pr view` individually, but project local has `gh:*`
4. **Missing read/write distinction** — Are read-only and write operations mixed together?
5. **Stale entries** — One-time approvals that accumulated (e.g., a specific git command with hardcoded paths)

Present findings as a table with issues and proposed resolution for each.

## Phase 3: Propose Reorganization

Design the new layout following these principles:

### Global settings (source of truth)

Organize permissions into labeled sections by grouping related entries together.
Do NOT use JSON comments (// or /* */) — settings.json must be valid JSON.
Instead, rely on the ordering of entries to convey grouping. Within the allow
array, cluster related permissions together in this order:

**Section order (group entries in this sequence, no separators needed):**

```
filesystem reads            — cat, tree, grep, wc, file reads
<lang> inspection           — go doc, cargo check, linters (no side effects)
GitHub CLI reads            — gh pr list/view/diff, gh issue list (no mutations)
external tool reads         — calendar, slack CLI, other read CLIs
web reads                   — WebSearch, WebFetch with domain allowlist
MCP <service> reads         — list, get, describe, search operations
build / test / install      — go build, cargo test, pnpm install (local side effects)
skills                      — Skill(superpowers:*), etc.
```

### Project-local settings (minimal overrides)

Only keep entries that are genuinely project-specific:
- Broader tool access needed for a specific workflow (e.g., `Bash(gh:*)` for a repo that creates PRs frequently)
- Project-specific MCP tools not used elsewhere
- Temporary elevated access during active development

### Clarifying questions

Before applying, ask the user about edge cases. Common questions:

- **Scope of CLI tools**: Should `gh:*` (all subcommands) go global, or keep read-only globally with broader access per-project?
- **MCP write operations**: Which write operations (send message, create issue) should stay prompted vs pre-allowed?
- **Environment separation**: Should dev and prod data sources have the same read access, or should prod be more restrictive?
- **Dotfiles sync**: Does the user maintain a dotfiles copy that needs updating?

Adapt questions to what's actually ambiguous — don't ask about things that are obvious from context.

## Phase 4: Apply Changes

Once the user confirms the plan:

1. Write the updated global settings file
2. Write the trimmed project-local settings file
3. Update any dotfiles copies to stay in sync
4. Clear out entries from other local files that were absorbed into global

## Phase 5: Summary

Present a before/after comparison:

| File | Before | After |
|------|--------|-------|
| Global | N flat entries | M entries in K sections |
| Project local | X entries | Y entries (project-specific only) |

List what moved where, and what still requires prompting (write operations not pre-allowed).
