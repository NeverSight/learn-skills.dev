---
name: llm-collab
description: "Agent MUST load when dealing with ADRs, devlogs, or multi-session documentation"
---
--- # workaround: anthropics/claude-code#13005
setup: |
    All projects that depend on this skill should have as `CLAUDE.md` frontmatter:

    ```yaml
    --- # workaround: anthropics/claude-code#13003
    depends:
        - skills/llm-collab
    ```
---

# LLM-Collaborative Documentation

Principles and helpers for human-LLM agent swarm collaboration on long-running projects. Provides documentation patterns for coordination across agents, temporal conflict resolution, and just-in-time context loading through structured files (ADRs, devlogs), progressive-detail guides, and optional scripts.

**Note:** This skill focuses on documentation patterns. For task management across sessions, use the `llm-subtask` skill which handles ephemeral, tactical, and strategic task tracking.

> **Status:** Locally maintained, iteratively improving. Expect rough edges.

## Core Principles

### 1. Separation of Concerns

**Problem:** Mixing audiences wastes everyone's time.

**Pattern:** Different files for different audiences/purposes:
```
project/
├── README.md                 # Users: what it does, how to use
├── HACKING.md                # Contributors: how to develop
├── CLAUDE.md                 # Agents: architecture, conventions
└── docs/dev/
    ├── adr/                  # Why: decision rationale
    ├── devlog/               # When: session history
    └── design/               # What/how: living design knowledge
```

### 2. Tiered Detail

**Problem:** Loading full docs when you need a summary wastes context tokens.

**Pattern:** Three-level information hierarchy:
1. Top-level file: 1-2 sentence summary + link
2. Main doc: 1-paragraph summary + link to deep dive
3. Subdirectory: Full detail

**Example:**
```
CLAUDE.md: "Uses ADR format for decisions. See docs/adr/"
docs/adr/ directory: [Date-based ADRs, list with ls or grep]
references.kb/: [Categorized guides: file-types.kb/, guidelines.kb/, workflows.kb/]
```

### 3. Temporal Ordering

**Problem:** With 20+ sessions/day exploring ideas in parallel, codebase contains conflicting partial implementations. Which decision is current?

**Pattern:** Date-based naming provides temporal ordering:
- ADRs: `YYYY-MM-DD-NNN-title.md`
- Devlog: `YYYY-MM-DD.md` (or `YYYY-MM-DD-HHMM.md`)
- When conflicts found, newest decision wins

### 4. Baton-Passing

**Problem:** Agent swarm loses alignment between sessions.

**Pattern:** Devlogs capture what diffs can't: reasoning, principles, conventions.
- Decisions and their rationale (especially rejected alternatives)
- Conventions established and principles discovered
- Tradeoffs that shaped the approach

**For task tracking:** Use the `subtask` skill for managing ephemeral, tactical, and strategic tasks.

### 5. Living Documentation

**Problem:** Docs become stale and lie.

**Pattern:** Use directory listings as the source of truth:
- `docs/adr/` directory contains decisions—`ls -t` to see chronologically
- `docs/devlog/` directory contains session history—directory itself is the index
- Avoid maintaining separate index files that can drift

### 6. Design Knowledge

**Problem:** CLAUDE.md is too brief for deep understanding; ADRs are too granular.

**Pattern:** Use `docs/dev/design/` for living design documentation:
- Deeper than CLAUDE.md, more distilled than ADRs
- Organized by abstraction level (goals → requirements → design → components)
- Linked via `why[]` frontmatter for traceability

**When to read:** Orienting on architecture, before significant changes.

**When to update:** After architectural ADRs, when onboarding reveals gaps.

See `references/how-to-document-design-knowledge.md` for the full pattern.

## Frontmatter Directives

CLAUDE.md files use frontmatter to give agents operational instructions. These are **action triggers**, not passive metadata.

- `requires:` — Read these files before acting in this directory.
- `depends:` — Read when relevant.

## Adaptation Guidelines

**These are patterns, not rules.** Adapt based on:

- **Team size:** Solo vs multiple humans changes needs
- **Session frequency:** 5 sessions/day vs 20 changes patterns
- **Exploration style:** Serial vs parallel affects conflict frequency
- **Project phase:** Early exploration vs maintenance
- **Existing conventions:** Respect what team already uses

**Evolution is expected.** As you use these patterns:
- Keep what works
- Drop what doesn't
- Modify to fit your needs
- Share improvements

## Quick Reference

**Common workflows:**
- When to document what: <https:references.kb/workflows.kb/when-to-document-what.md>
- Session coordination: <https:references.kb/workflows.kb/llm-document-consumption-patterns.md>

**Key file types:**
- ADRs: <https:references.kb/file-types.kb/ADRs.md>
- Devlogs: <https:references.kb/file-types.kb/devlog.md>
- CLAUDE.md: <https:references.kb/file-types.kb/CLAUDE.md>
- Design knowledge: <https:references/how-to-document-design-knowledge.md>
- Browse all: <https:references.kb/file-types.kb/>

**Common tasks:**
```bash
# Orient yourself at session start
~/.claude/skills/llm-collab/bin/llm-collab-session-start

# Document a significant decision
~/.claude/skills/llm-collab/bin/llm-collab-adr "Decision title"

# Record what happened this session
~/.claude/skills/llm-collab/bin/llm-collab-devlog

# Backdate an entry (works with any date-based script)
DATE=2025-11-19 ~/.claude/skills/llm-collab/bin/llm-collab-adr "Decision title"

# Set up docs for new project
~/.claude/skills/llm-collab/bin/llm-collab-init
```

All scripts support `--help` for details.

## Detailed References

Browse <https:references.kb/> for categorized guides:
- **file-types.kb/** - What each doc type should contain
- **guidelines.kb/** - How to write effective docs
- **workflows.kb/** - How to use and maintain docs

Standalone references:
- **references/how-to-document-design-knowledge.md** - Living design documentation pattern

## Success Indicators

These patterns are working when:
- Agents orient quickly (<1 minute)
- "What's next?" has clear answer
- Multiple daily sessions stay aligned
- Conflicts resolve through temporal ordering
- Context loading feels efficient
- Both human and agents can drop in/out

## Design Goals

These patterns address:
- Projects with 10-20+ agent sessions per day
- Parallel exploration creating conflicting partial implementations
- Agents needing to hand off work to each other
- User frequently asking "What's next?" or losing thread
- Context waste from loading irrelevant documentation
