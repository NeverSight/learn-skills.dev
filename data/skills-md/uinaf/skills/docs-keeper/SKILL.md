---
name: docs-keeper
description: Maintain project documentation with clear human/agent separation. Use when setting up a new project, auditing docs, creating plans, or managing agent working memory. Triggers include "set up docs", "create a plan", "audit documentation", "init project structure", or any task involving project documentation conventions.
---

# docs-keeper

Maintain project documentation with clear human/agent separation. Includes planning workflow.

## Project Structure

```
project/
  README.md              ← project entrypoint (human-facing)
  AGENTS.md              ← agent instructions (project-specific)
  CLAUDE.md              ← symlink → AGENTS.md
  docs/
    ARCHITECTURE.md      ← human: high-level design, domain concepts
    *.md                 ← human: guides, ADRs, onboarding
    agents/
      PLAN.md            ← agent: living project plan
      ASSUMPTIONS.md     ← agent: tracked assumptions
      notes/             ← agent: session notes
        YYYYMMDD-HHMM-slug.md
```

### Project root

- **README.md** — canonical project entrypoint (setup, usage, status).
- **AGENTS.md** — project-specific agent instructions. Tech stack, commands, conventions, gotchas. Keep under 150 lines.
- **CLAUDE.md** — always a symlink to AGENTS.md. Ensure this exists: `ln -sf AGENTS.md CLAUDE.md`

### Human zone (`docs/*.md`)

Written by humans, maintained by humans. Agents read these but don't edit unless explicitly asked.

- `README.md` at project root is the primary project overview.
- **docs/ARCHITECTURE.md** — high-level design. Describe capabilities and domain concepts, not file paths.
- Other docs as needed: ADRs, API guides, onboarding.

### Agent zone (`docs/agents/`)

Written and maintained by agents. Committed to git. Survives context windows and agent rotations.

- **PLAN.md** — the living project plan (see Planning below)
- **ASSUMPTIONS.md** — document assumptions before acting. Update as confirmed or invalidated.
- **notes/** — timestamped session notes (see Session Notes below)

---

## Planning

Before any multi-step work, create or update `docs/agents/PLAN.md`.

### Brainstorming (before the plan)

Don't jump into planning. Understand first:

1. **Explore context** — read existing docs, code, recent commits
2. **Ask clarifying questions** — one at a time, understand purpose/constraints/success criteria
3. **Propose 2-3 approaches** — with trade-offs and your recommendation
4. **Present design in sections** — scaled to complexity, get approval after each section
5. **Save design** — write validated design to `docs/agents/PLAN.md`

Do NOT write code until the design is approved. Every project goes through this, even "simple" ones. Simple projects are where unexamined assumptions waste the most work.

### Plan format

Plans are bite-sized tasks. Each task is one action (2-5 minutes):

```markdown
# [Feature] Implementation Plan

**Goal:** One sentence.
**Approach:** 2-3 sentences.
**Tech:** Key technologies/libraries.

---

### Task 1: [Component]

**Files:**
- Create: `exact/path/to/file.go`
- Modify: `exact/path/to/existing.go`
- Test: `exact/path/to/file_test.go`

**Steps:**
1. Write failing test
2. Run test, verify it fails
3. Write minimal implementation
4. Run test, verify it passes
5. Commit

**Verify:** `go test ./... -run TestSpecificThing`
```

Rules:
- Exact file paths, always
- Complete code in plan (not "add validation")
- Exact commands with expected output
- Each step is one action, not a paragraph

### Execution

Execute plans in batches (3 tasks at a time):

1. Follow each step exactly
2. Run verifications as specified
3. After each batch: report what was done, show verification output, wait for feedback
4. Apply feedback, continue next batch

**Stop and ask when:**
- Hit a blocker (missing dep, test fails, instruction unclear)
- Plan has gaps
- Verification fails repeatedly
- Don't guess through blockers

---

## Session Notes

Write notes to `docs/agents/notes/YYYYMMDD-HHMM-slug.md` when you learn something worth preserving:

- Lessons learned from debugging
- Architecture decisions and rationale
- Failed approaches and why they didn't work
- Investigation findings (API quirks, library gotchas)
- Mistakes and how to avoid them

Keep notes concise. Future agents read these for context.

---

## Session Discipline

**Start:** Read `docs/agents/PLAN.md` and `AGENTS.md`.

**End:** Update plan if anything changed. Write a note if you learned something.

---

## Keeper Behavior

When invoked as docs-keeper (or when documentation is stale):

1. **Ensure structure** — AGENTS.md exists, CLAUDE.md is symlinked, `docs/agents/` exists
2. **Audit** — check all docs exist, are accurate, aren't contradicting code
3. **Fix** — update what you can (agents zone only, unless asked for human zone)
4. **Flag** — report what needs human attention
5. **Trim** — AGENTS.md should stay under 150 lines. Move overflow to `docs/`

## Rules

- One code example beats three paragraphs
- Describe capabilities, not file paths (paths go stale)
- Don't document what agents already know (language syntax, common patterns)
- Create `docs/agents/` and subdirectories if they don't exist
- Never edit human zone docs without explicit permission
