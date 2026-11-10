---
name: sync-permissions
description: "Reconcile the current project's Claude and Codex permission surfaces with the canonical global policy. Use when project permissions are missing, stale, or inconsistent after setup or migration. Not for syncing skills, hooks, or agents; use $sync-ai-infra."
allowed-tools: Bash(jq*), Bash(ls*), Bash(test*), Bash(readlink*), Read, Write, Edit
argument-hint: (no arguments)
---

# Update Rules Skill

> Sync global permissions, skills, and agents into the current project without losing project-specific settings.

## Purpose

The `SessionStart` hook only copies permissions when `.claude/settings.local.json` doesn't exist yet. After that, new global permissions never propagate to existing projects. This skill fills that gap — run it anytime to pull in new permissions additively.

## When to Use

- After adding new permissions to `~/.claude/settings.json`
- When starting work in a project that hasn't been updated in a while
- After creating a new skill and wanting it available everywhere
- When the user says "sync permissions", "update rules", "update my permissions"

## What It Does

1. **Merge permissions** — adds global permissions into project-local, keeping any project-specific ones
2. **Verify skills directory** — ensures `<skills-root>/` exists and has content
3. **Verify agents directory** — ensures `~/.claude/agents/` exists and has content
4. **Report changes** — shows exactly what was added

## What It Does NOT Do

- Never removes existing project permissions (additive only)
- Never modifies `~/.claude/settings.json` (reads it, never writes)
- Never touches `model`, `hooks`, or other global settings keys

---

## Workflow

### Step 1: Read Both Permission Files

Read these two files:
- **Global:** `~/.claude/settings.json` → extract `permissions.allow` array
- **Local:** `.claude/settings.local.json` → extract `permissions.allow` array

If the local file doesn't exist, create it with global permissions (same as the SessionStart hook).

### Step 2: Compute the Union

Merge the two permission arrays:
- Start with all existing **local** permissions (preserve everything)
- Add any **global** permissions not already present in local
- Sort the final array for readability

The merge logic:
```
new_permissions = local_permissions ∪ global_permissions
added = new_permissions - local_permissions
```

### Step 3: Write the Merged Result

If there are new permissions to add:
1. Read the full local settings file (preserve any non-permissions keys)
2. Replace `permissions.allow` with the merged array
3. Write back to `.claude/settings.local.json`

If no new permissions, skip the write.

### Step 4: Verify Skills Directory

Check that `<skills-root>/` exists and has content:
- If missing or empty, warn: "Skills directory missing — run the documented managed-copy installer or deployment command"
- If present, report file count

### Step 5: Verify Agents Directory

Check that `~/.claude/agents/` exists and has content:
- If missing or empty, warn: "Agents directory missing — run the documented managed-copy installer or deployment command"
- If present, report file count

### Step 6: Report

Output a summary:

```
Permissions sync complete:
- Global permissions: [N]
- Local permissions (before): [N]
- New permissions added: [N] — [list them]
- Local permissions (after): [N]
- Skills directory: ✓ [N] files / ✗ missing
- Agents directory: ✓ [N] files / ✗ missing
```

If nothing changed:
```
Everything up to date. No new permissions to add. Skills OK. Agents OK.
```

---

## Example

Running `sync-permissions` after adding `web fetch` and `Skill(literature)` to `~/.claude/settings.json`:

```
Permissions sync complete:
- Global permissions: 25
- Local permissions (before): 64
- New permissions added: 2 — web fetch, Skill(literature)
- Local permissions (after): 66
- Skills directory: ✓ 496 files
- Agents directory: ✓ 16 files
```

---

## Safety

- **Additive only** — the skill can only add permissions, never remove them
- **No global writes** — global settings are read-only
- **Directory check** — verifies skills/agents directories exist and have content
- **Idempotent** — safe to run multiple times; re-running with no changes produces no writes
