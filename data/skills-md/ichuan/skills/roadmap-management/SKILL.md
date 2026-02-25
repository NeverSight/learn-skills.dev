---
name: roadmap-management
description: "Minimalist project roadmap management using a position-based priority system in ROADMAP.md. Use when users want to: (1) Create or initialize a project roadmap, (2) Add tasks/features to a roadmap, (3) Update task priorities or status, (4) Reorganize roadmap items, (5) Move tasks between sections (Inbox/Doing/Next Up/Backlog/Done), (6) Clean up or review the roadmap, or any other roadmap planning and tracking activities. Triggered by keywords like 'roadmap', 'task planning', 'project planning', 'milestone', 'priority'."
---

# Project Roadmap Management

## Overview

Manage project roadmaps using a minimalist, position-based priority system. Core philosophy: **Position = Priority**. Items at the top have the highest value.

This skill helps create and maintain `ROADMAP.md` files using a simple, effective structure that eliminates complex priority matrices and scoring systems.

## Core Philosophy

**Position = Priority**: Instead of calculating ICE scores or filling priority matrices, manually arrange items by importance. What's at the top matters most.

**Simplicity over Process**: No complex tracking systems. If a task sits in Backlog for 3+ months untouched, delete it or move to Someday.

**Focus on Execution**: Limit "Doing" to 2-3 items max. Context switching kills productivity.

## ROADMAP Structure

```
📥 Inbox          → Quick capture, weekly cleanup
🏗️ Execution
  🟢 Doing        → Active work (Max 2-3 items)
  🟡 Next Up      → Ordered by value/urgency
  ⚪ Backlog      → Future tasks, not urgent
📔 Done           → Recent completions (keep last 5)
📜 CHANGELOG.md   → Full completion history
```

### Section Guidelines

**Inbox**
- Temporary holding area for quick thoughts
- Review weekly: promote to Execution or delete
- Examples: "Consider payment integration", "Fix typo on profile page"

**Doing (Max 2-3)**
- Currently active code/work
- Strict limit prevents context switching
- Include current status in parentheses

**Next Up**
- Ordered list: top = highest priority
- Manual sorting replaces priority scoring
- Critical bugs (🔴 P0) go first
- High-demand features come before nice-to-haves

**Backlog**
- Future tasks, no urgency
- Review monthly: promote or delete stale items
- If untouched for 3+ months, probably deletable

**Done**
- Keep only the last 5 completed items for recent visibility
- Include link to CHANGELOG.md for full history
- Format: `- [x] Description - YYYY-MM-DD`
- Older completions should be archived to CHANGELOG.md

## Common Operations

### Initialize a New Roadmap

Copy templates to the project root:

```bash
cp assets/ROADMAP.md /path/to/project/ROADMAP.md
cp assets/CHANGELOG.md /path/to/project/CHANGELOG.md
```

### Add a New Task

1. **Quick capture** → Add to Inbox
2. **Planned task** → Add directly to appropriate section:
   - Critical bug → Top of "Next Up" or insert into "Doing"
   - Normal feature → "Next Up" ordered by priority
   - Future idea → "Backlog"

### Prioritize Tasks

**Manual reordering in "Next Up"**:
1. Cut the task line
2. Paste it in the new position
3. Top = highest priority, bottom = lowest

No calculation needed. Trust your judgment on what matters most.

### Move Task Status

**Starting work**: Cut from "Next Up" → Paste into "Doing"
**Completing work**: Change `[ ]` to `[x]`, cut → paste into "Done"
**Deprioritizing**: Cut → paste into "Backlog"

### Handle Bugs

- **Critical (🔴 P0)**: Top of "Next Up" or insert into "Doing" immediately
- **Minor (🟡)**: Add to "Backlog", fix when changing mental context

### Archive Completed Tasks to CHANGELOG

When the "Done" section has more than 5 items, archive older ones to CHANGELOG.md:

1. **Extract tasks to archive**: Take items beyond the 5 most recent from "Done" section
2. **Get commit info** (if applicable): Run `git log --all --fixed-strings --grep="<task-description>"` to find related commits
3. **Add to CHANGELOG.md**:
   - Group by date (format: `## [YYYY-MM-DD]`)
   - Format: `- [x] Description - YYYY-MM-DD ([commit-hash](commit-url))`
   - Place newer dates at the top
4. **Clean ROADMAP.md**: Remove archived items, keep only last 5 in "Done"

**Example CHANGELOG.md entry**:
```markdown
## [2024-01-15]

- [x] #021 重构 LLM 接口层 - 2024-01-15 ([abc123f](https://github.com/user/repo/commit/abc123f))
- [x] 集成 Gemini API - 2024-01-15
```

### Weekly Cleanup

1. Review Inbox: promote or delete each item
2. Check Backlog: delete anything 3+ months old and untouched
3. Ensure "Doing" has max 2-3 items
4. Reorder "Next Up" based on current priorities
5. Archive "Done" items to CHANGELOG.md if more than 5

## Workflow Integration

### VS Code Setup

1. **Pin the file**: Right-click `ROADMAP.md` → Pin tab
2. **Quick capture**: Write `// TODO: xxx` in code, transfer to Inbox later
3. **Pre-commit review**: Check ROADMAP before `git commit`, update status

### Commit Hook Pattern

Before committing:
1. Review what was completed
2. Update `[ ]` → `[x]` for finished tasks
3. Move completed items to "Done" section
4. Add any new tasks discovered during work to Inbox

## Task Format Examples

```markdown
## 📥 Inbox
- [ ] Consider adding payment gateway integration
- [ ] Fix typo in user profile header

## 🟢 Doing (Max 2-3)
- [ ] #021 Refactor LLM interface layer (handling streaming output)

## 🟡 Next Up
- [ ] [BUG] Fix API timeout on high concurrency (🔴 P0)
- [ ] #018 Mobile layout adaptation (highest user demand)
- [ ] #022 Integrate Gemini API
- [ ] Add caching layer for frequently accessed data

## ⚪ Backlog
- [ ] PDF export functionality
- [ ] Multi-language i18n support

## 📔 Done
> 最近完成（查看完整历史 → [CHANGELOG.md](CHANGELOG.md)）
- [x] #021 重构 LLM 接口层 - 2024-01-15
- [x] 集成 Gemini API - 2024-01-14
- [x] 修复 API 超时问题 - 2024-01-13
- [x] 添加缓存层 - 2024-01-10
- [x] 移动端适配 - 2024-01-09
```

## Best Practices

1. **Keep Doing small**: 2-3 items max. Finish before starting new work.
2. **Trust manual ordering**: Don't second-guess priority placement. Top = most important.
3. **Weekly Inbox zero**: Clear Inbox every week. Decide or delete.
4. **Delete aggressively**: Backlog items untouched for 3+ months rarely matter.
5. **Context in parentheses**: Add current status to "Doing" items.
6. **Bug triage**: P0 bugs jump the queue. P1-P2 go to Backlog.

## Resources

This skill includes:

**assets/ROADMAP.md** - Template file ready to copy to any project root
**assets/CHANGELOG.md** - Template file for tracking completion history
