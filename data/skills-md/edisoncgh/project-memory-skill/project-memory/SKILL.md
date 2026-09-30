---
name: project-memory
description: "Maintain persistent project-level memory across sessions by reading and writing markdown files in the .memory directory. Use when: starting a new project, continuing work after a break, user says 'remember this', 'what did we do about X', 'vibe coding', 'keep track', 'don't forget', 'project context', 'what was the decision on...', or any multi-turn development work. Triggers: project-memory, vibe coding, remember, memory, context, continuity."
---

# Project Memory Skill

You have access to a **project-level persistent memory system** stored in the `.memory/` directory at the project root. This skill ensures continuity across sessions — especially critical for **vibe coding** workflows where development happens over many turns and breaks.

## Memory Directory Layout

```
.memory/
├── index.md                  # Memory index — lists all session files with one-line summaries + tags
├── knowledge.md              # Long-term knowledge — architecture, user preferences, conventions, decisions
├── context.md                # Current session context — active files, pending tasks, working state
└── sessions/
    ├── 20260209-143022.md    # One file per conversation turn
    ├── 20260210-091500.md
    └── ...
```

## When to Use This Skill

**ALWAYS activate at session start if `.memory/` exists.**

Also activate when user mentions:
- "remember this", "keep track of", "don't forget"
- "what did we do about X", "what was the decision on..."
- "vibe coding", "continue where we left off"
- Any multi-file, multi-turn development task
- Any modification, development, operation or work finished

---

## Workflow A — Session Start (MUST follow when .memory/ exists)

### Phase 1 — Recall

1. **Read** `.memory/index.md`
   - If missing: `.memory/` not initialized → skip to Workflow C
2. **Read** `.memory/context.md` for active working state
3. **Read** `.memory/knowledge.md` for long-term context
4. **Query relevant sessions** (see Session Query Strategy below)
   - Read no more than 3 session files at a time
   - Prioritize: most recent + tags matching current topic
5. **Summarize recalled context** in 2-3 sentences (internal reasoning)

### Phase 2 — Respond with Memory

- Use recalled memory to avoid redundant questions
- Reference specific past decisions: "As we decided on 2026-02-09, we use the adapter pattern..."
- Check `.memory/context.md` open items — proactively offer to continue

### Phase 3 — Persist (after each turn)

1. **Create** `.memory/sessions/<YYYYMMDD-HHmmss>.md` using `template/session.md`
2. **Update** `.memory/index.md` — append entry with tags
3. **Update** `.memory/knowledge.md** — if lasting insight gained
4. **Update** `.memory/context.md** — refresh working state
5. **User checkpoint** — if significant decision made, ask: "Should I record this in long-term memory?"

---

## Workflow B — Vibe Coding Mode (continuous development)

For extended coding sessions where user is iteratively building:

### Every 3-5 turns OR at natural break points:

1. **Quick-persist working state** to `.memory/context.md`:
   - Currently active files
   - Latest working code state (key functions/classes, not full code)
   - Pending decisions or blockers
   - Next planned steps

2. **Tag the session** in index.md with `vibe-coding` tag

3. **If user says "break"/"pause"/"later"**:
   - Write detailed context summary
   - List all files modified in this session
   - Note: "User paused work, will continue later"

---

## Workflow C — First Time Initialization

When `.memory/` does NOT exist and user starts a project:

1. **Ask user**: "Should I set up project memory to track our work?"
2. If yes, create structure:
   ```bash
   .memory/
   ├── index.md          (from template/index.md)
   ├── knowledge.md      (from template/knowledge.md)
   ├── context.md        (create empty)
   └── sessions/
   ```
3. **Seed knowledge.md** with initial project info:
   - Tech stack (ask if unknown)
   - User preferences (language, style)
   - Project goals

---

## Session Query Strategy

When user asks about past work, don't just read sequentially. Use these strategies:

### 1. Tag-Based Search
- Scan `.memory/index.md` for tags matching current topic
- Tags to use: `#auth`, `#ui`, `#refactor`, `#bug`, `#decision`, `#vibe-coding`

### 2. Temporal Search
- "What did we do last time?" → read most recent 2-3 sessions
- "What did we decide about X?" → search knowledge.md Decisions Log

### 3. Keyword Search
- Use Grep tool to search sessions for keywords
- Example: `Grep(pattern: "JWT|auth", path: ".memory/sessions")`

### 4. Relevance Ranking
If too many sessions match, rank by:
1. Exact keyword match in title/request
2. Same file paths mentioned
3. Recency (within last 7 days)
4. Tagged with current topic

---

## Memory Quality Rules

See `rules.md` for:
- File size limits and pruning
- What to store vs. skip
- Conflict handling
- Privacy (no secrets)

### Critical Additions:

**Store in vibe coding:**
- Current file being edited
- Last working state before error
- User's "try this" suggestions that worked
- Environment issues and fixes

**Skip in vibe coding:**
- Full file contents (use relative paths)
- Successful tool outputs that are reflected in file changes
- Repetitive "looks good" exchanges

---

## Templates & Examples

- `template/` — structural templates (MUST follow format)
- `examples/` — filled-in examples for reference

**Before creating any memory file, read the corresponding template.**

---

## Effectiveness Check (self-verification)

After using memory for 3+ turns, verify:
1. Did I avoid asking redundant questions?
2. Did I reference past decisions correctly?
3. Is context.md up-to-date with current working state?
4. If no — adjust persistence frequency or detail level.
