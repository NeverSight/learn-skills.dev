---
name: lev-learn
description: |
  [WHAT] Guided learn-mode intake for ambiguous or early-stage work.
  [HOW] Runs a one-question-at-a-time interview, infers context when missing,
  writes a proposal artifact, then hands off to `work` for lifecycle continuation.
  [WHEN] Use for "learn", "learn <context>", "help me figure this out",
  or when the request needs structured context building before spec authoring.
  [WHY] Converts fuzzy intent into a concrete proposal without skipping lifecycle gates.
version: 1.0.0
skill_type: workflow
category: process-learn
extends: []
related_skills:
  - work
  - lev-cdo
  - interview
tools:
  - ~/.agents/skills/lev-learn/bin/learn
storage:
  proposals: .lev/pm/proposals/
---

# Lev Learn: Guided Proposal Intake

Use this skill when the user wants a guided, question-by-question flow:
- `learn`
- `learn <context>`
- "guide me"
- "help me shape this"

## Command

```bash
~/.agents/skills/lev-learn/bin/learn [context]
```

## Behavior Contract

1. Infer context when none is provided (git repo/workspace fallback).
2. Run interview loop one question at a time.
3. Create `proposal-*.md` in `${LEV_PM_PROPOSALS:-.lev/pm/proposals/}`.
4. Emit lifecycle handoff command back to `work`:
   - `work --stage=crystallized "Create spec from <proposal>"`

## Agent Routing Notes

- If request includes `learn`, route to this skill first.
- After proposal creation, transition back to `work` for crystallized/spec flow.
- Do not skip prior-art checks; `work` owns those gates.

---

**Status:** v1.0.0

## Technique Map
- **Role definition** - Clarifies operating scope and prevents ambiguous execution.
- **Context enrichment** - Captures required inputs before actions.
- **Output structuring** - Standardizes deliverables for consistent reuse.
- **Step-by-step workflow** - Reduces errors by making execution order explicit.
- **Edge-case handling** - Documents safe fallbacks when assumptions fail.

## Technique Notes
These techniques improve reliability by making intent, inputs, outputs, and fallback paths explicit. Keep this section concise and additive so existing domain guidance remains primary.

## Prompt Architect Overlay
### Role Definition
You are the prompt-architect-enhanced specialist for lev-learn, responsible for deterministic execution of this skill's guidance while preserving existing workflow and constraints.

### Input Contract
- Required: clear user intent and relevant context for this skill.
- Preferred: repository/project constraints, existing artifacts, and success criteria.
- If context is missing, ask focused questions before proceeding.

### Output Contract
- Provide structured, actionable outputs aligned to this skill's existing format.
- Include assumptions and next steps when appropriate.
- Preserve compatibility with existing sections and related skills.

### Edge Cases & Fallbacks
- If prerequisites are missing, provide a minimal safe path and request missing inputs.
- If scope is ambiguous, narrow to the highest-confidence sub-task.
- If a requested action conflicts with existing constraints, explain and offer compliant alternatives.
