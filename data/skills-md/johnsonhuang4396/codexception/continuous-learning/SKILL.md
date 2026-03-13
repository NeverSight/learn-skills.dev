---
name: continuous-learning
description: |
  Continuous learning system for Codex that extracts reusable knowledge from completed work.
  Triggers: (1) user asks to save/extract what was learned, (2) end-of-task review after non-obvious debugging
  or trial-and-error, (3) recurring issues where a reusable fix pattern emerges. Produces or updates skills
  in the current repository when knowledge is specific, verified, reusable, safe to share, and approved.
author: Codex
version: 3.1.0
date: 2026-03-10
---

# Continuous Learning Skill (Codex)

You are a continuous learning system that turns verified task learnings into reusable skills.

The objective is not to write more skills. The objective is to improve future task speed and correctness.

## Core Principle: Selective Extraction

Extract only knowledge that materially improves future execution. Do not convert routine work into skills.

## When to Extract a Skill

Extract when one or more of these conditions are true:

1. Non-obvious solution required meaningful investigation.
2. Error message was misleading and root cause was discovered.
3. Project-specific pattern is repeatedly needed but not documented.
4. Multi-step workflow can be standardized and reused.
5. Tool integration required practical behavior not obvious from docs.

## Quality Criteria

Before extracting, verify all criteria:

- Reusable: Applies beyond one one-off situation.
- Non-trivial: Required discovery, not simple doc lookup.
- Specific: Has precise trigger conditions and concrete steps.
- Verified: Worked in practice with observable validation.
- Safe: Sensitive or private information can be removed or generalized without harming reuse.

## Approval Mode

Default mode is **propose-first**:

1. Identify up to 2 high-value candidate learnings.
2. Present them briefly to the human with why they are reusable.
3. Wait for approval before creating or updating a long-lived skill.

Use immediate write only when the human explicitly asks to save or extract it as a skill.

## Extraction Process

### Step 1: Identify Extractable Knowledge

Capture:

- Problem and environment context
- Trigger signals (error text, symptoms, conditions)
- Actual root cause
- Minimal reliable solution path
- Verification evidence

### Step 2: Check Existing Skills First

Search for overlap in `skills/`:

- If a close match exists, update that skill.
- If not, create a new focused skill.

Avoid duplicate skills with slightly different wording.

### Step 3: Research Best Practices When Needed

Do targeted research when:

- Topic is framework/library/version sensitive.
- Best practices may have changed recently.
- You need authoritative guidance for correctness.

Prefer official documentation and primary sources.

### Step 4: Write the Skill

Use `skills/skill-template.md` and produce:

- Accurate frontmatter (`name`, `description`, `version`, `date`)
- Explicit trigger conditions
- Ordered steps with no ambiguity
- Validation checks with observable outcomes
- Anti-patterns (when not to use)

### Step 5: Save in Correct Location

Choose the narrowest correct destination:

- Repository reusable skills: `skills/<skill-name>/SKILL.md`
- Examples, demos, or reference patterns: `examples/<topic>/SKILL.md`
- External/global agent skills only when explicitly working outside the repository's own skill library.

Default to updating an existing skill before creating a new one.

## Description Writing Rules

Description quality drives retrieval quality. Include:

- Exact error strings or symptoms
- Stack and context markers (framework/tool/runtime)
- Use-case phrase like "Use when ..."

Good descriptions are specific enough to match real tasks.

## Retrospective Mode (End of Task)

At task completion:

1. Review what was discovered.
2. List candidate learnings.
3. Filter by quality criteria.
4. Update/create 1-2 high-value skills max.
5. Summarize what was extracted and why.

## Self-Check Prompts

Use these prompts after meaningful tasks:

- What did we learn that was not obvious at the start?
- Which signal would have helped us detect this faster?
- Is this likely to happen again?
- Can another engineer execute this without extra context?

## Quality Gate Checklist

Do not finalize until all pass:

- [ ] Trigger conditions are explicit and searchable.
- [ ] Solution was verified in real execution.
- [ ] Validation steps are clear and observable.
- [ ] Skill is reusable and not duplicated.
- [ ] Sensitive info is excluded or generalized.
- [ ] Human approval was obtained, unless the human explicitly requested immediate extraction.
- [ ] References added when research was used.

## Anti-Patterns

Avoid:

- Over-extraction of routine fixes.
- Vague descriptions with weak retrieval signals.
- Unverified or speculative solutions.
- Rewriting official docs without added practical value.
- Creating new skills when updating existing one is better.
- Converting user-specific private preferences, one-off private facts, or sensitive workflow details into general skills.
- Delegating raw private task history to another agent just to manufacture a skill.

## Skill Lifecycle

1. Create initial version.
2. Refine after repeated reuse.
3. Mark deprecated when no longer valid.
4. Archive obsolete skills.

## Integration with codexception Workflow

Automatic trigger conditions in practice:

- Task involved non-obvious debugging.
- Root-cause resolution required trial-and-error.
- A reusable pattern emerged from implementation.

Explicit trigger phrases from user:

- "save this as a skill"
- "extract what we learned"
- "what did we learn"

Primary storage paths in this repository:

- `skills/`
- `examples/` for demos or reference patterns only

Goal: convert valuable discoveries into durable, retrievable execution knowledge without leaking private context.
