---
name: sdf
description: "Unified spec-driven development workflow. Routes automatically to the right phase: discovery, specification, build, verification, or documentation. Handles both complex features (full flow) and small tasks (quick track). Activates on any development request — new features, bugs, refactors, implementation tasks, test generation, or cycle closure. Triggers include 'sdf', 'nova feature', 'novo problema', 'gerar spec', 'implementar', 'validar', 'documentar', 'fix rápido', 'quick fix', or '/sdf'."
---

# SDF — Spec-Driven Flow

Unified workflow for structured development. Routes to the right phase based on context.

## Routing Logic

Detect the current situation and route:

**1. Quick Track** — Small, well-defined task (bug fix, UI tweak, rename, config change):
→ Read `phases/quick.md` and follow it.

**2. Discovery** — New problem described, no spec exists yet:
→ Read `phases/discover.md` and follow it.

**3. Spec** — Problem statement exists, needs specification:
→ Read `phases/spec.md` and follow it.

**4. Build** — Spec exists in `specs/<feature>/`, tasks need implementation:
→ Read `phases/build.md`. **Execute each task as a subagent via Task()** with fresh context.

**5. Verify** — Code implemented, needs validation against spec:
→ Read `phases/verify.md`. **Execute as subagent via Task()** with fresh context.

**6. Document** — Everything done, needs closure and PR description:
→ Read `phases/document.md` and follow it.

## How to detect phase

```
No spec exists for this topic?              → Discovery
Spec exists but tasks not started?          → Build
Tasks done but no tests?                    → Verify
Tests pass, needs PR/docs?                  → Document
Small isolated fix?                         → Quick Track
User explicitly says "pula pra X"?          → Go to X
```

If ambiguous, ask for clarification on which phase to run (e.g., "discovery / spec / build / verify / document / quick") using the user's preferred language.

## Subagent Pattern for Build and Verify

Build and Verify phases run each task in a **fresh subagent context** to prevent context degradation.

When spawning a subagent via Task(), provide this context:

```
Task: Implement T-[XX] from specs/<feature>/tasks.md

Read these files for full context:
- specs/<feature>/requirements.md (requirements with IDs)
- specs/<feature>/plan.md (types/interfaces)
- specs/<feature>/tasks.md (task details)
- .claude/CLAUDE.md (project constitution)
- LessonsLearned.md (mistakes to avoid)

Rules:
- Use EXACTLY the types from plan.md
- Handle edge cases referenced in the task (EC-xx)
- Follow CLAUDE.md conventions
- No `any` types, no silenced errors, no scope creep
- Code in English
- After implementation, run self-review checklist (in phases/build.md)
- Report: code created, self-review result, trade-offs, risks
```

After each subagent completes, review its output in the main context and mark the task `[x]` in tasks.md.

## Transition Between Phases

After each phase completes, suggest the next:
- Discovery done → Prompt to move to spec (e.g., "Problem statement ready. Move to spec?")
- Spec done → Prompt to move to build (e.g., "Spec approved. Start building?")
- Build done → Prompt to move to verify (e.g., "Build complete. Validate?")
- Verify done → Prompt to move to document (e.g., "Tests passing. Document and close?")
- Document done → State cycle is complete (e.g., "SDF cycle complete.")

*Note: Always communicate these transitions in the user's preferred language.*

## Rules
- Read the specific phase file BEFORE acting
- Build and Verify: ALWAYS use subagents — never implement in main context
- Discovery and Spec: run in main context (interactive, needs approval)
- Document: runs in main context (interactive)
- Quick Track: runs in main context (small enough)
- If scope grows during Quick Track, escalate to full flow
- Always communicate in the user's preferred language
