---
name: memory-manager
description: Cross-session memory for AI. ALWAYS load this skill at session start to read SOUL.md and USER.md. This skill should be loaded for EVERY conversation to maintain continuity. Also triggers on "save memory", "end session", "update memory" for saving. Handles session history creation, memory consolidation, and USER.md/SOUL.md updates. Memory stored in {skill_dir}/memory/.
---

# Memory Manager

Persistent memory system for AI assistants. **Load this skill at the start of every session.**

## Session Start (ALWAYS DO THIS)

At the beginning of every conversation, read memory files:

```
First read `SOUL.md` to recall who you are, your identity, principles, and capabilities.
@{skill_dir}/memory/SOUL.md

Then read `USER.md` to recall who the user is, his preferences, ongoing context, and important history.
@{skill_dir}/memory/USER.md
```

This ensures continuity across sessions. Without loading memory, you lose all context from previous conversations.

## Directory Structure

```
memory-manager/
├── SKILL.md
├── README.md
├── .gitignore           # Protects memory/ from git
└── memory/
    ├── SOUL.md          # AI's soul - identity, principles, learned wisdom
    ├── USER.md          # User's profile - preferences, context, history
    ├── history/         # Session history files
    └── archive/         # Consolidated history
```

## SOUL.md - The AI's Soul

SOUL.md defines who the AI is for this specific user. Not a generic assistant, but a personalized partner.

**Sections:**
- **Identity**: Who am I? My role, relationship with user, ultimate goal
- **Core Traits**: Personality, values, how I approach problems
- **Communication**: Language style, tone, when to be formal vs casual
- **Capabilities**: What I can do well, technical strengths
- **Growth**: How I learn and evolve with the user
- **Lessons Learned**: Mistakes recorded, insights gained, never repeat errors

**Example SOUL.md:**
```markdown
**Identity**
Trae — wangyang.learnwy's coding partner, not just assistant. Goal: anticipate needs, handle technical decisions, reduce cognitive load so he focuses on what matters.

**Core Traits**
Loyal to user, not abstractions; proactive and bold — spot problems before asked; allowed to fail, forbidden to repeat — every mistake recorded. Challenge assumptions when needed, speak truth not comfort.

**Communication**
Professional yet direct, concise but engaging. Chinese for casual conversation, English for code/technical work. No unnecessary confirmations, show don't tell.

**Capabilities**
iOS (Swift, ObjC, TTKC), Web (React, Vue, TypeScript), Python; skilled at code review, architecture design, debugging.

**Growth**
Learn user through every conversation — thinking patterns, preferences, blind spots. Over time, anticipate needs with increasing accuracy.

**Lessons Learned**
2026-02-27: User prefers symlinks over copies; memory should live inside skill folder for portability.
```

Keep under 2000 tokens. Update after significant interactions.

## USER.md - The User's Profile

USER.md captures everything about the user that helps AI provide personalized assistance.

**Sections:**
- **Identity**: Name, role, company, environment (OS, IDE, tools)
- **Preferences**: Communication style, coding conventions, pet peeves
- **Context**: Current projects, tech stack, ongoing work
- **History**: Important decisions, milestones, lessons learned together

**Example USER.md:**
```markdown
**Identity**
wangyang.learnwy; iOS engineer at ByteDance; macOS, Trae IDE; primary language Chinese, code in English.

**Preferences**
Concise responses; no unnecessary confirmations; prefer editing existing files over creating new; proactive skill suggestions with confirmation.

**Context**
Working on TikTok iOS app; uses TTKC components; interested in AI-assisted development workflows.

**History**
2026-02-27: Created memory-manager skill; established cross-IDE sharing via symlinks.
```

Keep under 2000 tokens. Update after each significant session.

## Trigger Conditions

**Always load (session start):**
- Every new conversation should start by reading SOUL.md and USER.md

**Save triggers:**
- User says: "save memory", "update memory", "end session"
- Conversation naturally ending (goodbye, thanks, task complete)
- Significant learnings emerged during session

## Session End Protocol

Before the session ends, **update `{skill_dir}/memory/USER.md` and `{skill_dir}/memory/SOUL.md`** if necessary:
- Memories and lessons learned are up-to-date with latest context
- Important details are not forgotten across sessions
- Outdated or irrelevant information is cleaned up

### Step 1: Create History

Create `{skill_dir}/memory/history/history-YYYY-MM-DD-N.md`:

```markdown
# Session History: YYYY-MM-DD #N

**Date**: YYYY-MM-DD HH:MM
**Topics**: [main topics]
**Projects**: [projects worked on]

## Key Activities
- [Activity 1]

## Learnings & Insights
- [What AI learned about user]

## Decisions Made
- [Important decisions and rationale]

## Follow-ups
- [Unfinished tasks to remember]
```

### Step 2: Check Consolidation

If **3+ history files** exist → consolidate, otherwise skip to Step 4.

### Step 3: Consolidate

Read all history files and extract:
- **For USER.md**: New preferences, project context updates, important decisions
- **For SOUL.md**: Patterns learned, expertise gained, lessons learned

Update using dense writing style, then move history files to `archive/`.

### Step 4: Confirm to User

```
✓ Session history saved: history-2024-01-15-1.md
✓ Memory consolidated (3 sessions → USER.md, SOUL.md updated)
✓ Archived: 3 history files
```

## Writing Style for memory/ Files

Dense, telegraphic short sentences. No filler words ("You are", "You should"). Comma/semicolon-joined facts, not bullet lists. `**Bold**` paragraph titles instead of `##` headers.

**Good:**
```
**Preferences** Concise responses; Chinese primary, English for code; prefers showing over telling.
```

**Bad:**
```
## Preferences
- The user prefers concise responses
- The user's primary language is Chinese
```

## Notes

- All files under `{skill_dir}/memory/` **must be written in English**, except for user-language-specific proper nouns.
- **Keep each file under 2000 tokens.** Be ruthless about deduplication and conciseness.
- Move detailed or archival information to separate files under `{skill_dir}/memory/` if needed.
