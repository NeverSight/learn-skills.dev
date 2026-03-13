---
name: memento
description: Extract session memories into CLAUDE.md - because Claude forgets, but your notes don't
disable-model-invocation: true
---

# Memento

Usage: `/memento [--project PATH] [--user PATH]`

Analyze this conversation to extract **actionable** memory updates for CLAUDE.md and SKILL.md files.

## Step 0: Resolve Paths

**Default paths:**
- Project Memory: `./CLAUDE.md`
- User Memory: `~/.claude/CLAUDE.md`

**Override via arguments:**
- `--project PATH` - custom project memory location
- `--user PATH` - custom user memory location

**Override via config (persistent):**
Check `~/.claude/CLAUDE.md` for a `## Memento Config` section:
```
## Memento Config
- PROJECT_PATH: ./docs/CLAUDE.md
- USER_PATH: ~/custom/CLAUDE.md
```

**Priority:** Arguments > Config > Defaults

Store resolved paths as `$PROJECT_PATH` and `$USER_PATH` for use in subsequent steps.

## Step 1: Analyze the Session

Review the conversation for:

- **Mistakes I made** - wrong assumptions, incorrect commands, things that failed
- **Corrections the user made** - "no", "actually", "I meant", "not that"
- **Preferences expressed** - how the user likes things done (explicit or implicit)
- **Project conventions discovered** - file structure, tooling, patterns in THIS codebase
- **Reusable learnings** - insights that apply across all projects
- **Improvements for Skills used**

## Step 2: Categorize Suggestions

### What counts as ACTIONABLE:
- Changes how Claude behaves in future sessions
- Specific enough to apply ("use pnpm not npm" vs "check package manager")
- Would have prevented a mistake made in this session

### What is NOT actionable (skip these):
- Observations or reflections ("this was a good session")
- Meta-advice ("run retro after meaningful sessions")
- Vague principles ("be more careful")
- Things already known or obvious

### Where suggestions go:

**Project Skills/Agents (`.claude/skills/*/SKILL.md`, `.claude/agents/*.md`)** - PREFER when:
- Learning is about how a specific skill or agent should behave
- Correction relates to a skill that was used in this session
- Convention improves a specific workflow (biographing, citation, etc.)

**Project Memory (`$PROJECT_PATH`)** - Use when:
- Convention is project-wide but not skill-specific
- Architecture or file structure pattern
- General project guidance that doesn't fit a skill

**User Memory (`$USER_PATH`)** - Use when:
- Preference applies across ALL projects
- It's about how the user likes to work generally
- It's a Claude Code tip that's universally useful

## Step 3: Check for Duplicates

Before suggesting, read:
- Both CLAUDE.md files
- Any skill files (`.claude/skills/*/SKILL.md`) relevant to the session
- Any agent files (`.claude/agents/*.md`) that were used

Never suggest something already present in these files.

## Step 4: Present Suggestions (or say "nothing meaningful")

If you have ZERO actionable suggestions, just say:
> "No actionable suggestions from this session. The conversation was straightforward or learnings were already captured."

If you DO have suggestions, use `AskUserQuestion` with multiSelect.

**IMPORTANT: Show ALL relevant categories in the same AskUserQuestion call.**

The `questions` array can include (only include categories with suggestions):
1. Skills/Agents question (if any skill or agent improvements)
2. Project Memory question (if any project-wide suggestions)
3. User Memory question (if any universal suggestions)

Example structure:
```json
{
  "questions": [
    {
      "header": "Skills/Agents",
      "question": "Which improvements should I add to skill/agent files?",
      "multiSelect": true,
      "options": [
        {"label": "biographing: [suggestion]", "description": "..."},
        {"label": "gardener: [suggestion]", "description": "..."}
      ]
    },
    {
      "header": "Project Memory",
      "question": "Which insights should I add to $PROJECT_PATH?",
      "multiSelect": true,
      "options": [...]
    },
    {
      "header": "User Memory",
      "question": "Which insights should I add to $USER_PATH?",
      "multiSelect": true,
      "options": [...]
    }
  ]
}
```

For Skills/Agents, prefix each option label with the target file (e.g., "biographing: ...").

Rules:
- Max 4 suggestions per category
- Each suggestion must be 1-2 lines, specific, actionable
- User can select none, some, or all from each category

## Step 5: Apply Selected Suggestions

For each selected suggestion:
1. Read the target file (CLAUDE.md or skill/agent file)
2. Find appropriate section (create if needed)
3. Append the suggestion using Edit tool

**For skill/agent files:** Add to an existing relevant section, or create a new section if appropriate (e.g., "## Constraints", "## Tips", "## Common Mistakes").

## Output Format

```
✅ Added to .claude/skills/biographing/SKILL.md:
- [suggestion]

✅ Added to $PROJECT_PATH:
- [suggestion]

✅ Added to $USER_PATH:
- [suggestion]
```

Or if nothing was added:
```
No changes made.
```
