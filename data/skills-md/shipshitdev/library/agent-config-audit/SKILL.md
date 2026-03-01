---
name: agent-config-audit
description: "Audit and sync AI agent configuration files (CLAUDE.md, CODEX.md, AGENTS.md, .cursorrules, hooks, settings) across workspaces. Use when agent configs drift, rules duplicate, files go stale, or after workspace restructuring."
version: 1.0.0
tags:
  - audit
  - claude-md
  - codex-md
  - agents-md
  - config
  - documentation
  - maintenance
triggers:
  - "audit CLAUDE.md"
  - "agent config audit"
  - "sync agent configs"
  - "check CLAUDE.md"
  - "docs out of date"
  - "rules duplicated"
  - "config drift"
  - "stale cursorrules"
  - "CODEX.md outdated"
  - "agent config maintenance"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Task
---

# Agent Config Audit

> Audit and maintain the full AI agent configuration stack across a workspace — CLAUDE.md, CODEX.md, AGENTS.md, .cursorrules, hooks, settings, and supporting `.agents/` docs.

## When to Use

- User mentions: "audit CLAUDE.md", "agent config", "rules out of date", "config drift", "sync docs"
- After restructuring repos, adding/removing projects, or changing conventions
- Periodic maintenance (monthly recommended)
- When agents keep making the same mistake despite rules existing (symptom of stale or contradictory config)
- After a major refactor where file paths, package names, or architecture changed

## When NOT to Use

- If writing actual application code → use **bugfix**, **refactor-code**, or repo-specific skills
- If capturing a single new rule from conversation → use **rules-capture**
- If auditing code quality / CRITICAL-NEVER-DO violations → use **genfeed-codebase-audit**
- If checking formatter/linter configs (biome, prettier, tsconfig) → use **genfeed-config-harmony**
- If scaffolding `.agents/` from scratch → use **agent-folder-init**

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Workspace root | Yes | Path to the workspace containing repos (auto-detected from cwd) |
| Scope | No | `full` (all checks) or specific: `dedup`, `stale`, `codex`, `cursor`, `settings` |
| Fix mode | No | `report` (default, read-only) or `fix` (apply recommended changes) |

## Workflow

### Step 1: Inventory — Discover All Config Files

Scan the workspace for every agent config file:

```bash
# Find all agent config files across workspace (including sub-repos)
glob "**/CLAUDE.md"
glob "**/CODEX.md"
glob "**/AGENTS.md"
glob "**/.cursorrules"
glob "**/.cursor/rules"
glob "**/.claude/settings.json"
glob "**/.claude/settings.local.json"
glob "**/.claude/hooks.json"
glob "**/.agents/SYSTEM/critical/*.md"
```

Build an inventory table:

```
| Layer           | Files Found | Total Lines |
|-----------------|-------------|-------------|
| CLAUDE.md       | N           | N           |
| CODEX.md        | N           | N           |
| AGENTS.md       | N           | N           |
| .cursorrules    | N           | N           |
| .claude/ config | N           | N           |
| .agents/ system | N           | N           |
```

### Step 2: Dedup Check — Find Duplicated Rules

These rules commonly appear in multiple places. Search for each across ALL config files:

**Rules to check:**

- `any` types / `No any` — should be in CLAUDE.md + hooks only
- `console.log` / logger — should be in CLAUDE.md only
- Conventional commits — should be in CLAUDE.md only
- AbortController — should be in CLAUDE_RULES.md / repo CLAUDE.md only
- Session file naming — should be in hooks.json + one doc reference only
- Import order — should be in CLAUDE_RULES.md only
- Soft delete (`isDeleted`) — should be in CRITICAL-NEVER-DO.md only
- Multi-tenancy (`organization: orgId`) — should be in CRITICAL-NEVER-DO.md only

For each rule, count occurrences:

```
grep "No \`any\`\|NO \`any\`\|no any types" across all config files
```

**Healthy target**: Each rule appears in max 2 files (one "teach" doc + one runtime enforcement like hooks).

**Flag**: Any rule appearing 3+ times across config files.

### Step 3: Staleness Check — Find Outdated Files

Check for stale dates and paths:

```bash
# Find files with old "Last Updated" dates (> 90 days old)
grep -r "Last Updated:" across .cursorrules, .cursor/rules

# Find hardcoded workspace paths that should be relative
grep -r "/Users/" across .agents/ config files

# Find references to directories that no longer exist
# Compare referenced paths against actual directory listing
```

**Flag**: Any file with "Last Updated" > 90 days behind current date.
**Flag**: Any hardcoded absolute path in config files.
**Flag**: Any reference to a directory that doesn't exist.

### Step 4: CODEX.md Value Check

For each CODEX.md, check if it has:

- [ ] Codex-specific constraints (sandbox, no network, no interactive)
- [ ] Repo-specific entry points (key files to read first)
- [ ] NOT just "read CLAUDE.md" (that's a zero-value redirect stub)

```bash
grep -l "Codex-Specific\|sandbox\|no network\|No network" across all CODEX.md files
```

**Flag**: Any CODEX.md without Codex-specific guidance.

### Step 5: AGENTS.md Consistency Check

For each AGENTS.md:

- [ ] Has repo-specific context (not just generic "docs in .agents/")
- [ ] Links to correct `.agents/` paths that actually exist
- [ ] Consistent structure across repos

**Flag**: Any AGENTS.md that's a pure generic stub (< 20 lines with no repo-specific content).

### Step 6: Cursor Config Check

For `.cursorrules` and `.cursor/rules`:

- [ ] No emoji in headers (wastes tokens)
- [ ] "Last Updated" within 90 days
- [ ] Project paths reference actual directories
- [ ] No duplicated session file rules (hooks.json handles this)

### Step 7: Settings Audit

For `.claude/settings.json` and `.claude/settings.local.json`:

- [ ] Denied skills have documented rationale (in SETTINGS-NOTES.md or equivalent)
- [ ] Local bash overrides don't contradict documented standards without explanation
- [ ] No stale tool references

### Step 8: Generate Report

Output format:

```markdown
# Agent Config Audit Report
**Date:** YYYY-MM-DD
**Workspace:** [path]
**Files Scanned:** N

## Summary
- Critical issues: N
- Moderate issues: N
- Minor issues: N
- Total config lines: N (target: reduce by dedup)

## Critical: Rule Duplication
| Rule | Occurrences | Files | Target |
|------|-------------|-------|--------|
| "No any types" | 6 | [list] | 2 |

## Critical: Stale Files
| File | Last Updated | Days Stale |
|------|-------------|------------|

## Moderate: Low-Value CODEX.md
| File | Lines | Has Codex Constraints | Has Entry Points |
|------|-------|----------------------|------------------|

## Moderate: Stub AGENTS.md
| File | Lines | Has Repo Context |
|------|-------|------------------|

## Minor: Emoji in Config
| File | Emoji Count |
|------|-------------|

## Recommendations
1. [Specific actionable fix]
2. [Specific actionable fix]
```

### Step 9: Apply Fixes (if fix mode)

If user requested `fix` mode, apply changes following these principles:

- Each rule lives in ONE canonical location
- Hooks enforce at runtime — docs teach, not repeat
- Strip emoji from all config files
- Update all "Last Updated" dates
- Replace hardcoded paths with relative references
- Expand zero-value CODEX.md stubs with Codex-specific constraints

## Reference Files

- `references/canonical-ownership.md` — Which rule belongs in which file
- `references/healthy-config-example.md` — Example of a well-structured config set

## Anti-Patterns

| DON'T | DO | Why |
|-------|-----|-----|
| Repeat the same rule in CLAUDE.md, RULES.md, CRITICAL-NEVER-DO.md, and hooks | Put the rule in ONE canonical file; others reference it | Duplication wastes context tokens and creates drift when one copy gets updated but others don't |
| Leave "Last Updated: 2025-10-07" in a file touched in 2026 | Update dates when modifying any config file | Stale dates signal neglect and erode trust in the config system |
| Write CODEX.md that just says "read CLAUDE.md" | Add Codex-specific constraints (sandbox, no network) and key entry points | Codex runs sandboxed — it needs different guidance than Claude Code |
| Use emoji in config headers | Use plain text headers | Emoji waste tokens on every context load and violate "no emoji unless requested" |
| Hardcode `/Users/username/path/` in config files | Use relative paths or describe location generically | Hardcoded paths break when workspace moves or another developer joins |
| Add new rules to CRITICAL-NEVER-DO.md that are positive standards | Keep CRITICAL-NEVER-DO.md for violations only; positive standards go in CLAUDE.md or RULES.md | Mixing positive and negative rules in the same file dilutes the "NEVER DO" signal |

## Validation

After running the audit:

- [ ] No rule appears in more than 2 config files
- [ ] All `.cursorrules` files have "Last Updated" within 90 days
- [ ] Every CODEX.md has Codex-specific sandbox guidance
- [ ] No hardcoded absolute paths in any config file
- [ ] No emoji in `.cursorrules` or `.cursor/rules` headers
- [ ] Denied skills in settings.json have documented rationale
- [ ] Total config file line count decreased or stayed flat (no bloat)

## Related Skills

- **rules-capture** — Route here if user is expressing a new rule during conversation (not auditing)
- **agent-folder-init** — Route here if scaffolding `.agents/` structure from scratch
- **genfeed-config-harmony** — Route here if the issue is formatter/linter configs (biome, prettier, tsconfig)
- **genfeed-codebase-audit** — Route here if auditing code quality, not config quality
- **claude-md-management:revise-claude-md** — Route here if updating a single CLAUDE.md with session learnings (not full audit)
- **claude-md-management:claude-md-improver** — Complementary; focuses on individual CLAUDE.md quality while this skill focuses on cross-file consistency
