---
name: remember
description: |
  Rebuild context from previous Claude Code sessions in the current directory.
  Use when asked to "remember", "what was I working on", "recap last session",
  "summarize recent work", "catch me up", or when starting a new session and needing
  to understand what happened before.
license: MIT
metadata:
  author: Antonin Januska
  version: "1.0.0"
tags: [context, session, history, memory, resume]
---

# Remember

> **Context rebuild activated** - I'll scan previous sessions, git history, and project files to reconstruct what happened and what's next.

## Overview

Reconstructs working context from previous Claude Code sessions in the current directory. Reads conversation history, auto-memory, SESSION_PROGRESS.md, ROADMAP.md, and recent git activity to produce a structured summary of past work and suggested next steps.

**Core principle:** Never start from zero. Previous sessions contain valuable context - surface it so the user can pick up where they left off.

## When to Use

**Always use when:**
- Starting a new Claude Code session in a project with prior history
- User says "where was I?" or "what was I working on?"
- User wants a recap of recent work before deciding what to do next
- Returning to a project after a break

**Useful for:**
- Onboarding into a project you haven't touched in a while
- Reviewing what was accomplished across multiple sessions
- Deciding what to work on next based on recent momentum

**Avoid when:**
- Project has no prior Claude Code sessions (nothing to remember)
- User already knows exactly what to do and wants to start immediately
- Quick one-off tasks where context doesn't matter

---

## Process

### Phase 1: Gather Sources

Collect context from all available sources in this order:

**1. Claude Code conversation history (primary source)**

Read conversation JSONL files from the project's Claude directory:

```
~/.claude/projects/{project-path-slug}/*.jsonl
```

The slug is derived from the git repository root path with `/` replaced by `-` and prefixed with `-`. All worktrees and subdirectories within the same repo share one project directory. For example:
- `/Users/antonin/projects/myapp` → `-Users-antonin-projects-myapp`

If unsure, list `~/.claude/projects/` and match by checking the `cwd` field in conversation files.

Each `.jsonl` file is one conversation. Focus on the **3 most recent** by modification time (skip files under 1KB - likely abandoned sessions). For each, extract:
- **First user message** as the session topic (`type: "user"` → `message.content`)
- **Last 10 user messages** for decisions, direction changes, and session-ending context
- **Git branch** from the `gitBranch` field
- **Session timestamp** from file modification time

Filter out lines with `isSidechain: true` (subagent conversations) when reading the main session thread.

**2. Auto-memory**

Check `~/.claude/projects/{project-path-slug}/memory/` for `MEMORY.md` and any topic files (e.g., `debugging.md`, `patterns.md`). These contain Claude's accumulated project knowledge - build commands, architecture notes, and lessons learned from prior sessions.

**3. SESSION_PROGRESS.md**

If it exists in the project root, read it. This contains:
- Current plan with checked/unchecked items
- Failed attempts and their reasons
- Current status and next steps

**4. ROADMAP.md**

If it exists in the project root, read it. This provides:
- High-level feature plan
- What's been completed vs. planned
- Project direction and priorities

**5. Git state**

Run these commands to understand current and recent state:
```bash
git log --oneline -20 --format="%h %s (%ar)"
git status --short
git stash list
```

This shows what was committed, what's uncommitted, and what's stashed - the full picture of recent work.

**Verification before synthesizing:**
- [ ] All available sources were checked (skip missing ones gracefully)
- [ ] Most recent conversations were read (last 10 user messages from each)
- [ ] Git state includes status, log, and stash

### Phase 2: Synthesize

Combine all sources into a structured summary. Prioritize:

1. **What was the user doing most recently?** (latest conversation + SESSION_PROGRESS)
2. **What was accomplished?** (git commits + completed checklist items)
3. **What files were modified?** (git status + file-history-snapshot entries)
4. **What's unfinished?** (unchecked items in SESSION_PROGRESS, in-progress roadmap features)
5. **What should happen next?** (SESSION_PROGRESS "Next" field, uncompleted roadmap items)

When presenting the summary, summarize actions and decisions - do not reproduce raw conversation content, code snippets, or credentials from conversation files.

### Phase 3: Present Summary

Output a structured summary in this format:

```markdown
## Context Restored

### Last Session
**Date:** [date of most recent conversation]
**Branch:** [git branch]
**Topic:** [first user message or session summary]
**Status:** [completed / in progress / abandoned]

### Recent Work
- [Bullet points of key accomplishments from last 1-3 sessions]
- [Include commit summaries for concrete evidence]

### Files Modified
- [Uncommitted changes from git status]
- [Stashed work from git stash list]

### Unfinished Work
- [Unchecked items from SESSION_PROGRESS.md]
- [In-progress roadmap features]
- [Anything started but not completed in conversations]

### Suggested Next Steps
1. [Most likely next action based on all context]
2. [Alternative if user wants to switch focus]
3. [Roadmap item if no active work exists]
```

### Phase 4: Offer to Continue

After presenting the summary, ask the user what they'd like to do next. Present options derived from the unfinished work and suggested next steps using AskUserQuestion. Include these handoffs:

| User wants to... | Hand off to |
|-------------------|-------------|
| Continue active tracked work | `/track-session resume` |
| Pick a roadmap feature | `/track-roadmap resume` |
| Start something new | Begin directly |

---

## Rules

1. **Read before summarizing** - Always check all sources before producing a summary
2. **Don't fabricate context** - Only report what's actually in the files. If a source doesn't exist, say so.
3. **Recency bias is correct** - The most recent session matters most. Weight it heavily.
4. **User messages are primary** - User messages tell you intent. Assistant messages tell you execution. Prioritize intent.
5. **Offer, don't assume** - Present options for what to do next. Don't auto-start work.
6. **Handle missing sources gracefully** - No SESSION_PROGRESS? No ROADMAP? No auto-memory? That's fine. Report what you found.
7. **Sanitize sensitive data** - Never include API keys, tokens, or credentials from conversation history in the summary output.

---

## Examples

### Example: Full Context Available

<Good>
```markdown
## Context Restored

### Last Session
**Date:** 2026-03-01
**Branch:** main
**Topic:** "Add resume command to track-roadmap skill"
**Status:** Completed - feature merged

### Recent Work
- Added `/track-roadmap resume` mode with session-check-first workflow (de5d3de)
- Fixed record-tui GIF looping offset (18e55e8)
- Prepared v1.5.0 release with changelog (6b29309)

### Files Modified
- No uncommitted changes
- No stashed work

### Unfinished Work
- No active SESSION_PROGRESS.md found
- ROADMAP.md has 3 features in "Core Features" not yet completed

### Suggested Next Steps
1. Pick a feature from ROADMAP.md to work on next
2. Review and update ROADMAP.md (last audit was 2 weeks ago)
3. Start a new feature or skill
```

**Why this is good:** Clear, structured, evidence-backed with commit hashes, honest about what's missing, actionable next steps.
</Good>

<Bad>
```
You were working on some stuff. Looks like there are things to do.
Want me to help?
```

**Why this is bad:** No specifics, no evidence, no structure, no actionable information. This is useless for restoring context.
</Bad>

### Example: Partial Context (No SESSION_PROGRESS)

<Good>
```markdown
## Context Restored

### Last Session
**Date:** 2026-02-27
**Branch:** main
**Topic:** "Version and commit the current change"
**Status:** Completed - versioning and push done

### Recent Work
- Versioned and pushed changes (ef532460)
- Previous session: security audit of the repo (2277ca43)

### Files Modified
- No uncommitted changes

### Unfinished Work
- No SESSION_PROGRESS.md found (no active tracked work)
- ROADMAP.md not present

### Suggested Next Steps
1. No active work detected - what would you like to work on?
2. Consider creating a ROADMAP.md to plan features (`/track-roadmap`)
```

**Why this is good:** Honest about missing sources, still extracts useful context from what's available, suggests relevant next actions.
</Good>

<Bad>
```
ERROR: No SESSION_PROGRESS.md found. Cannot restore context.
```

**Why this is bad:** Treats a missing file as a failure. The skill should work with whatever sources exist, not require all of them.
</Bad>

### Example: Multiple Active Threads

<Good>
```markdown
## Context Restored

### Last Session
**Date:** 2026-03-01
**Branch:** feat/dark-mode
**Topic:** "Implement dark mode theme switching"
**Status:** In progress - Phase 2 of 4 complete

### Recent Work
- Session 1 (Mar 1): Started dark mode - theme context + light theme done
- Session 2 (Feb 28): Fixed auth token refresh bug (hotfix, merged to main)
- Session 3 (Feb 27): Reviewed PR #42 for teammate

### Files Modified
- 2 uncommitted files in src/theme/
- 1 stash: "WIP dark theme variables"

### Unfinished Work
- Dark mode: Phase 3 (dark theme CSS) and Phase 4 (testing) remaining
- SESSION_PROGRESS.md has 2 unchecked items for dark mode

### Suggested Next Steps
1. Continue dark mode implementation (Phase 3: dark theme CSS variables)
2. Switch to main for other work if dark mode is deprioritized
```

**Why this is good:** Shows multiple sessions with different contexts, identifies the most relevant in-progress work, surfaces uncommitted and stashed work, gives a clear "continue" option.
</Good>

---

## Troubleshooting

### Problem: No conversation files found

**Cause:** The project path slug doesn't match, or this is the first session in this directory.

**Solution:**
- List `~/.claude/projects/` and look for a matching slug
- The slug is derived from the git repo root, not just the current directory - all worktrees share one project directory
- If no files exist, report: "No previous sessions found for this project."

### Problem: Conversation files are very large (>1MB)

**Cause:** Long sessions produce large JSONL files.

**Solution:**
- Read the last 10-15 user messages first (most important context is at the end)
- Then read the first user message for the session topic
- Skip `progress` and `file-history-snapshot` type lines for speed
- Filter out `isSidechain: true` entries (subagent conversations)

### Problem: Git history doesn't match conversation context

**Cause:** Work was done but not committed, or commits came from another branch.

**Solution:**
- Check `git status` for uncommitted work
- Check `git stash list` for stashed changes
- Note the branch in conversation metadata vs. current branch
- Report discrepancies: "Last session was on branch X, but you're now on Y"

### Problem: Older sessions are missing

**Cause:** Claude Code deletes conversation history after 30 days by default.

**Solution:**
- Check `~/.claude/settings.json` for the `cleanupPeriodDays` setting
- Recommend increasing it if the user frequently takes long breaks between sessions
- Fall back to git log for historical context when conversations are unavailable

### Problem: Multiple projects share similar paths

**Cause:** Projects with similar names create similar slugs.

**Solution:**
- Always use the full `cwd` from conversation files to verify the match
- The slug is based on the git repo root, so subdirectories share the same project directory

---

## Integration

**This skill works with:**
- **track-session** - If SESSION_PROGRESS.md exists, remember surfaces its contents. If the user wants to continue, invoke `/track-session resume`.
- **track-roadmap** - If ROADMAP.md exists, remember includes roadmap status. If the user wants to pick a roadmap item, invoke `/track-roadmap resume`.
- **git-worktree** - When multiple worktrees exist, check the current worktree's branch against conversation history. Different worktrees may have separate SESSION_PROGRESS.md files.

**Workflow pattern:**
```
/remember  →  See context summary  →  Pick next action  →  /track-session or /track-roadmap
```

**Pairs with:**
- New session onboarding
- Post-break orientation
- Multi-day feature work across sessions
- Context handoff between developers

**How this skill differs from related commands:**

| Command | Purpose | Use when |
|---------|---------|----------|
| `/remember` | Summarize all recent context, then choose | Returning to a project, unsure what to do next |
| `/track-session resume` | Continue an active tracked session | You know there's a SESSION_PROGRESS.md to resume |
| `/track-roadmap resume` | Pick a roadmap feature and start working | You want to start a new feature from the roadmap |
| `claude --continue` | Blindly resume the last conversation | You know exactly where you left off |
