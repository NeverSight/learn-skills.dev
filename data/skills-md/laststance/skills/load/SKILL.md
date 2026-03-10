---
name: load
description: |
  Load project context from Serena MCP memory for session initialization.
  Discovers memories, reads critical rules, and validates context sufficiency.
  Portable across all Serena-enabled agents (Claude Code, Cursor, Windsurf, etc.).

  Use when: starting a session, resuming work, or needing project context.
  Keywords: session, load, initialize, context, memory, restore, resume
---

# Session Load

Load project context from Serena MCP memory for cross-session continuity.

<essential_principles>

## Core Requirements

- All context loading uses Serena MCP tools exclusively (no agent-specific tools)
- Follow cross-references: if any memory contains "MUST read", "CRITICAL", or "also read" directives, obey them
- Never skip `think_about_collected_information` validation at the end
- Report loaded context as a structured summary to the user

</essential_principles>

## Phase 1: Project Activation

1. Call `check_onboarding_performed` to verify Serena knows this project
2. If not onboarded: call `onboarding` to index the project first
3. Call `list_memories` to discover all available memory keys

## Phase 2: Context Loading

**If memories exist (returning session):**

4. Read any `CRITICAL_*` prefixed memories from the list
5. Scan loaded content for cross-reference directives:
   - Look for: "CRITICAL", "MUST read", "also read", "see also"
   - Read each referenced memory key
6. Read the most recent `session_*` memory (sort by date in key name)

**If no memories exist (first session):**

4. Suggest running `onboarding` and creating memories for future sessions
5. Present minimal context and note that `/save` should be run at end of session

## Phase 3: Validation

6. Call `think_about_collected_information` to verify context sufficiency
7. If insufficient: read additional memories

## Phase 4: Session Report

Report to the user:

```
## Session Loaded

- **Project**: [name]
- **Memories Loaded**: [count] ([list of keys])
- **Key Context**: [1-2 sentence summary of project state]
- **Previous Session**: [summary from session_* memory, or "None"]
- **Status**: Ready
```

## Memory Prefix Reference

| Prefix | Purpose | Load Priority |
|--------|---------|---------------|
| `CRITICAL_*` | Must-read rules | 1st (never skip) |
| Cross-referenced | Memories referenced by loaded content | 2nd |
| `session_*` | Session checkpoints | 3rd (latest only) |
| `plan_*` | Active plans | 4th (if relevant) |
| `pattern_*` | Learned patterns | On demand |
| `discovery_*` | Brainstorming results | On demand |
| `todo_*` | Persistent TODOs | On demand |

## Success Criteria

- [ ] Serena project is activated/onboarded
- [ ] All `CRITICAL_*` memories read
- [ ] Cross-reference directives followed
- [ ] `think_about_collected_information` called
- [ ] Session report presented to user
