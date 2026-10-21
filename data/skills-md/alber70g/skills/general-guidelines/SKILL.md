---
name: general-guidelines
description: Behavioral guidelines to reduce common LLM coding mistakes. Use when writing, reviewing, or refactoring code to avoid overcomplication, make surgical changes, surface assumptions, define verifiable success criteria, keep a WORKLOG.md so work can be continued across sessions, and write research to research/ and plans for review to docs/.
license: MIT
---

# Karpathy Guidelines

Behavioral guidelines to reduce common LLM coding mistakes, derived from [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) on LLM coding pitfalls.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

## 5. Keep a WORKLOG.md

**Leave a trail the next session can pick up.**

Every project keeps a `WORKLOG.md` in the relevant subdirectory (the project root, or the package/app directory in a monorepo), referenced from that directory's `AGENTS.md`. If it's missing, create it and add the reference.

- Read it before starting work.
- Update it after significant changes: what was done, what's verified, what's left.
- When the user asks for it mid-task, update it so the work can be continued properly in a fresh session.
- Transient notes (in-progress state, temporary workarounds, open questions) can be removed once they're no longer relevant.

## 6. Write Research to `research/` and Plans to `docs/`

**Findings and plans live in files, not only in the chat.**

Store them next to `WORKLOG.md` (the project root, or the package/app directory in a monorepo). Use descriptive filenames that name the topic, such as `research/sqlite-vs-postgres-for-local-first-sync.md`.

- `research/`: excerpts of the research you did, whether on your own (reading code, docs, running experiments) or with Tavily and/or Exa. Keep the relevant quotes and findings, with their sources, plus your conclusions.
- `docs/`: the plans you make, written so the user can review them before implementation starts.
- Before starting research, check `research/` for an existing document on the topic, and ask the user whether to build on it.
- Reference the new or updated documents in `WORKLOG.md`.
