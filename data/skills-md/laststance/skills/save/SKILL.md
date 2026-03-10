---
name: save
description: |
  Save session context to Serena MCP memory for cross-session persistence.
  Analyzes accomplishments, persists learnings as structured memories,
  creates checkpoint for future session restoration.
  Portable across all Serena-enabled agents (Claude Code, Cursor, Windsurf, etc.).

  Use when: ending a session, pausing work, saving progress, or preserving learnings.
  Keywords: session, save, persist, checkpoint, memory, store, context, end
---

# Session Save

Persist session context to Serena MCP memory for cross-session continuity.

<essential_principles>

## Core Requirements

- All persistence uses Serena MCP tools exclusively (no agent-specific tools)
- Always check existing memories before writing to avoid overwriting valuable context
- Session checkpoint keys must include date: `session_YYYY-MM-DD_<description>`
- Pattern and learning memories use: `pattern_<topic>`
- Never skip `think_about_collected_information` for save validation
- Report what was saved as a structured summary to the user

</essential_principles>

## Phase 1: Session Analysis

1. Review what was accomplished this session:
   - Files created or modified
   - Decisions made and their rationale
   - Problems encountered and solutions found
   - Tasks completed and tasks remaining
2. Identify what is worth persisting:
   - **Session state**: Current progress, next steps, blockers
   - **Learnings**: Reusable patterns, solutions to problems
   - **Plans**: Active plans or updated plans
   - **TODOs**: Outstanding work items

## Phase 2: Memory Inventory

3. Call `list_memories` to see existing memories
4. Check if `project_overview` needs updating (significant new understanding gained?)
5. Identify which existing memories need updates vs. new memories to create

## Phase 3: Persist Session Checkpoint

6. Call `write_memory` with key `session_YYYY-MM-DD_<summary>`:

```
## Session: YYYY-MM-DD — <summary>

### Accomplished
- [what was done]

### Decisions Made
- [decision]: [rationale]

### Files Changed
- [file path]: [what changed]

### Pending / Next Steps
- [what remains to be done]

### Blockers (if any)
- [blocker description]
```

## Phase 4: Persist Learnings (if any)

7. For each reusable pattern discovered, call `write_memory` with key `pattern_<topic>`:

```
## Pattern: <name>

**Context**: [when this applies]
**Solution**: [the pattern/approach]
**Example**: [concrete example]
**When to Use**: [trigger conditions]
```

8. For each persistent TODO, call `write_memory` with key `todo_<description>`:

```
## TODO: <description>

**Priority**: [high/medium/low]
**Context**: [why this matters]
**Acceptance Criteria**: [how to know it's done]
```

## Phase 5: Update Project Overview (if needed)

9. If significant new project understanding was gained:
   - Call `read_memory("project_overview")` to get current content
   - Call `write_memory("project_overview", updated_content)` with additions
   - Do NOT overwrite existing content — append or update sections

## Phase 6: Validation

10. Call `think_about_collected_information` to verify save completeness
11. Verify: session checkpoint created, learnings persisted, no critical context lost

## Phase 7: Save Report

Report to the user:

```
## Session Saved

### Memories Written
| Key | Purpose |
|-----|---------|
| session_YYYY-MM-DD_xxx | Session checkpoint |
| pattern_xxx | [if any] |
| todo_xxx | [if any] |

### Memories Updated
| Key | What Changed |
|-----|-------------|
| project_overview | [if updated] |

### Next Session
Run `/load` to restore this context.
```

## Memory Naming Conventions

See `references/memory-conventions.md` for the complete naming reference.

Quick summary:

| Prefix | Purpose | Example |
|--------|---------|---------|
| `project_overview` | Project summary (singleton) | `project_overview` |
| `CRITICAL_*` | Must-read rules | `CRITICAL_activation_rule` |
| `session_YYYY-MM-DD_*` | Session checkpoints | `session_2026-02-09_auth-flow` |
| `plan_*` | Active plans | `plan_dark-mode` |
| `pattern_*` | Reusable patterns | `pattern_supabase-rls` |
| `discovery_*` | Brainstorming results | `discovery_api-options` |
| `todo_*` | Persistent TODOs | `todo_fix-login` |

## Success Criteria

- [ ] Session accomplishments analyzed
- [ ] Existing memories checked (no accidental overwrites)
- [ ] Session checkpoint memory written with date-stamped key
- [ ] Learnings/patterns persisted (if any discovered)
- [ ] Project overview updated (if significant new understanding)
- [ ] `think_about_collected_information` called
- [ ] Save report presented to user
