---
name: vault-health
description: >
  Vault infrastructure diagnostics with actionable recommendations.
  Use when: "check vault health", "vault status", "run health check", "check sync status",
  "agent memory stats", "is the vault healthy", "skills health", "skill audit", "skills report".
  PROACTIVE TRIGGER (CONDITIONAL): Before or after major vault operations, at session start
  if vault issues are suspected, or monthly for skills audit (automated via cron on the 1st).
version: 3.0.0
gotchas_count: 0
---

# Vault Health Check

Run comprehensive diagnostics on the Obsidian vault and present findings with actionable recommendations. This is a read-only operation, never modify vault files during a health check.

## Prerequisites

- Working directory: `~/Documents/Obsidian Vault/`

## Procedure

### Step 1: Run Health Check Script

```bash
node "~/Documents/Obsidian Vault/system/scripts/vault-automation.js" health-check
```

This writes `system/health-report.md` with automated checks. Read it.

### Step 2: Present the Report

Format findings cleanly:

```
VAULT HEALTH REPORT
===================
Generated: YYYY-MM-DD HH:MM

INFRASTRUCTURE
  Obsidian Sync:    PASS   synced within last 24h
  File Count:       PASS   94 markdown files
  Notion Sync:      WARN   last sync 3 days ago
  Daily Scheduler:  PASS   launchd loaded, last run today 20:00

BACKFILL STATUS
  Notion Backfill:  INFO   in progress — 31 transcripts remaining

AGENT MEMORY
  claude-code-m4:   PASS   12 session logs, memory.md 87 lines
  ...

INBOX
  Items waiting:    3 files in inbox/

Overall: 1 WARN, 0 FAIL
```

**Status meanings:**
- **PASS**, healthy, no action needed
- **INFO**, expected state, informational only (e.g., backfill in progress on a new vault)
- **WARN**, needs attention. Provide a specific fix.
- **FAIL**, broken. Provide an immediate fix.

### Step 3: Provide Recommendations

For each WARN or FAIL, consult `references/troubleshooting.md` for the specific fix command or action. Present fixes inline, not just "check the thing" but the exact command to run.

If everything passes, keep it brief: "All clear. No issues found."

Always show inbox count as a useful nudge without being alarming.

### Step 4: Optional Deep Checks

Only run when user explicitly asks for "deep check" or "full audit":

1. **Folder structure audit**, scan for files outside conventional folders
2. **Frontmatter coverage**, sample 20 random .md files, check for valid frontmatter, report percentage
3. **Orphaned files**, files not linked from any index
4. **Config validation**, parse `system/scripts/config.json`, verify Notion IDs and folder paths
5. **Duplicate detection**, check for duplicate `notion-id` values in frontmatter

Report deep check results separately with their own status levels.

## Rules

- Read-only operation, never modify vault files during health check
- Present findings clearly and concisely
- Do not alarm about INFO items, they are expected states on a new vault
- `system/health-report.md` is auto-generated, do not treat it as user content
- Always include inbox item count in report

## Step 5: Skills Health (run when user asks for "skills health" or during monthly audit)

Audit the skills system and report on trigger coverage, usage, and health.

### 5a: Trigger Tier Distribution

Scan all `~/.claude/skills/*/SKILL.md` files and categorize by trigger quality:

| Tier | Criteria | Count |
|------|----------|-------|
| **Always-on** | Has `MANDATORY` in description | N |
| **Proactive** | Has `PROACTIVE TRIGGER (CRITICAL)` | N |
| **Contextual** | Has `PROACTIVE TRIGGER (CONDITIONAL)` | N |
| **On-demand** | Has `Use when:` but no PROACTIVE | N |
| **No triggers** | Missing both `Use when:` and `PROACTIVE` | N |

### 5b: Usage Report

For each skill, read the `last_used` field:
- List skills not used in 60+ days (candidates for trigger improvement)
- List skills never used (check if triggers are missing or too vague)
- Top 10 most recently used skills

### 5c: Missing Triggers

Flag skills where:
- Description has no "Use when:" keywords
- Description mentions "Proactively suggest" in prose but has no formal `PROACTIVE TRIGGER` label
- Hooks are described in text but missing from YAML `hooks:` section

### 5d: Recommendations

For each flagged skill, suggest:
- Specific trigger keywords to add
- Whether it should be PROACTIVE (CRITICAL) or (CONDITIONAL)
- Whether it needs a hook

### Report Format

```
SKILLS HEALTH
=============
Total skills: N
Trigger coverage: N% (skills with proper triggers / total)

TIER DISTRIBUTION
  Always-on:    N
  Proactive:    N
  Contextual:   N
  On-demand:    N
  No triggers:  N  [WARN if > 0]

USAGE (last 60 days)
  Active:       N skills used
  Dormant:      N skills not used
  Never used:   N skills

TOP CONCERNS
  [List skills with missing triggers or stale usage]

RECOMMENDATIONS
  [Specific fixes for top 5 flagged skills]
```

Write the full report to `~/Documents/jj-knowledge-vault/agents/claude-code-m4/reports/skills-audit-YYYY-MM.md`

## Additional Resources

### Reference Files

- **`references/troubleshooting.md`**, Fix commands for every WARN/FAIL type, deep check procedures, and common resolution patterns
