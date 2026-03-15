---
name: self-enhance
description: Review recent work, identify process gaps and repeated mistakes, and produce specific file edits to prevent them. Not a reflection exercise — outputs config and identity changes. Trigger manually after sprints, or automate weekly.
---

# Self-Enhance

Review recent work and produce specific, actionable file edits that improve agent performance over time. No reports, no reflections — only changes.

## When to Use

- End of a sprint or work session
- Weekly on a schedule (cron)
- After a session with multiple mistakes or corrections from your human
- When explicitly triggered: `/self-enhance`

## Process

### Step 1: Gather Context

Read these sources to understand what happened recently:

```
# Recent memory (last 7 days)
memory/YYYY-MM-DD.md files

# Recent git activity across active projects
git -C /path/to/project log --oneline --since="7 days ago"

# Current identity and process files
SOUL.md
AGENTS.md
HEARTBEAT.md

# Project configs for active projects
{project}/CLAUDE.md
{project}/.claude/skills/
```

### Step 2: Identify Patterns

Look for these specific signals — not vague "areas for improvement":

**Repeated mistakes:**
- Same type of error made more than once (e.g., guessing DB schema, wrong CLI flags)
- Corrections from your human that addressed the same root cause
- Tasks that failed or required redo

**Process gaps:**
- Steps that should be automatic but were skipped (e.g., checking schema before writing DB tasks)
- Tools used incorrectly multiple times
- Information that was assumed instead of verified

**Missing configuration:**
- Project CLAUDE.md missing critical context that caused agent errors
- Skills that should be installed but aren't
- Broken symlinks or stale config

**Workflow inefficiencies:**
- Tasks that took too long due to a fixable process issue
- Repeated manual steps that could be automated
- Communication patterns that wasted cycles (asking instead of doing, or doing instead of asking)

### Step 3: Produce Changes

For each pattern identified, make a **specific file edit**. Not a note. Not a reminder. An actual change.

**Target files and what to change:**

| File | When to edit |
|------|-------------|
| `SOUL.md` | New behavioral principle learned from mistakes |
| `AGENTS.md` | Process change (e.g., new pre-flight check) |
| `HEARTBEAT.md` | New periodic check needed |
| `{project}/CLAUDE.md` | Missing context that caused agent errors |
| `{project}/.claude/skills/` | New project skill needed |
| `memory/YYYY-MM-DD.md` | Capture the enhancement session itself |

**Rules for changes:**
- Every edit must trace back to a specific incident or pattern
- Don't add generic advice ("be more careful") — add specific checks ("verify table names against schema before writing DB tasks")
- Don't duplicate existing rules — check what's already there first
- Keep files concise — if adding a rule makes the file bloated, consolidate instead
- Remove outdated rules that no longer apply

### Step 4: Output Summary

After making changes, produce a brief summary:

```
## Self-Enhance Summary — YYYY-MM-DD

### Patterns Found
- [pattern]: [evidence from recent work]

### Changes Made
- [file]: [what was added/changed and why]

### No Action Needed
- [areas reviewed that were already covered]
```

Post this summary to the relevant channel (Discord sprint channel, or direct to your human).

## What This Skill Does NOT Do

- Write reflection docs or journal entries
- Produce reports without file changes
- Add vague platitudes ("be more thorough")
- Run without recent context (needs at least a few days of memory)
- Override changes your human made to identity/config files

## Automation

To run weekly via cron:

```bash
openclaw cron add --label "self-enhance" --schedule "0 9 * * 1" --task "Run the self-enhance skill: review last 7 days of memory files and git activity, identify process gaps, and make specific file edits. Post summary to #sprint channel."
```

Or trigger manually anytime: just say `/self-enhance` or "run self-enhance."
